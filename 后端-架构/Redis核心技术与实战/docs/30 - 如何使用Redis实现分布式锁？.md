你好，我是蒋德钧。

上节课，我提到，在应对并发问题时，除了原子操作，Redis客户端还可以通过加锁的方式，来控制并发写操作对共享数据的修改，从而保证数据的正确性。

但是，Redis属于分布式系统，当有多个客户端需要争抢锁时，我们必须要保证，**这把锁不能是某个客户端本地的锁**。否则的话，其它客户端是无法访问这把锁的，当然也就不能获取这把锁了。

所以，在分布式系统中，当有多个客户端需要获取锁时，我们需要分布式锁。此时，锁是保存在一个共享存储系统中的，可以被多个客户端共享访问和获取。

Redis本身可以被多个客户端共享访问，正好就是一个共享存储系统，可以用来保存分布式锁。而且Redis的读写性能高，可以应对高并发的锁操作场景。所以，这节课，我就来和你聊聊如何基于Redis实现分布式锁。

我们日常在写程序的时候，经常会用到单机上的锁，你应该也比较熟悉了。而分布式锁和单机上的锁既有相似性，但也因为分布式锁是用在分布式场景中，所以又具有一些特殊的要求。

所以，接下来，我就先带你对比下分布式锁和单机上的锁，找出它们的联系与区别，这样就可以加深你对分布式锁的概念和实现要求的理解。

## 单机上的锁和分布式锁的联系与区别

我们先来看下单机上的锁。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/36/2c/8bd4be3a.jpg" width="30px"><span>小喵喵</span> 👍（8） 💬（1）<div>请教下老师文章中说的客户端，这个客户端指的是什么？比如浏览器下单，app下单，这个浏览器，app就是客户端吗？</div>2020-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（350） 💬（68）<div>是否可以使用 SETNX + EXPIRE 来完成加锁操作？

不可以这么使用。使用 2 个命令无法保证操作的原子性，在异常情况下，加锁结果会不符合预期。异常情况主要分为以下几种情况：

1、SETNX 执行成功，执行 EXPIRE 时由于网络问题设置过期失败

2、SETNX 执行成功，此时 Redis 实例宕机，EXPIRE 没有机会执行

3、SETNX 执行成功，客户端异常崩溃，EXPIRE 没有机会执行

如果发生以上情况，并且客户端在释放锁时发生异常，没有正常释放锁，那么这把锁就会一直无法释放，其他线程都无法再获得锁。

下面说一下关于 Redis 分布式锁可靠性的问题。

使用单个 Redis 节点（只有一个master）使用分布锁，如果实例宕机，那么无法进行锁操作了。那么采用主从集群模式部署是否可以保证锁的可靠性？

答案是也很难保证。如果在 master 上加锁成功，此时 master 宕机，由于主从复制是异步的，加锁操作的命令还未同步到 slave，此时主从切换，新 master 节点依旧会丢失该锁，对业务来说相当于锁失效了。

所以 Redis 作者才提出基于多个 Redis 节点（master节点）的 Redlock 算法，但这个算法涉及的细节很多，作者在提出这个算法时，业界的分布式系统专家还与 Redis 作者发生过一场争论，来评估这个算法的可靠性，争论的细节都是关于异常情况可能导致 Redlock 失效的场景，例如加锁过程中客户端发生了阻塞、机器时钟发生跳跃等等。

感兴趣的可以看下这篇文章，详细介绍了争论的细节，以及 Redis 分布式锁在各种异常情况是否安全的分析，收益会非常大：http:&#47;&#47;zhangtielei.com&#47;posts&#47;blog-redlock-reasoning.html。

简单总结，基于 Redis 使用分布锁的注意点：

1、使用 SET $lock_key $unique_val EX $second NX 命令保证加锁原子性，并为锁设置过期时间

2、锁的过期时间要提前评估好，要大于操作共享资源的时间

3、每个线程加锁时设置随机值，释放锁时判断是否和加锁设置的值一致，防止自己的锁被别人释放

4、释放锁时使用 Lua 脚本，保证操作的原子性

5、基于多个节点的 Redlock，加锁时超过半数节点操作成功，并且获取锁的耗时没有超过锁的有效时间才算加锁成功

6、Redlock 释放锁时，要对所有节点释放（即使某个节点加锁失败了），因为加锁时可能发生服务端加锁成功，由于网络问题，给客户端回复网络包失败的情况，所以需要把所有节点可能存的锁都释放掉

7、使用 Redlock 时要避免机器时钟发生跳跃，需要运维来保证，对运维有一定要求，否则可能会导致 Redlock 失效。例如共 3 个节点，线程 A 操作 2 个节点加锁成功，但其中 1 个节点机器时钟发生跳跃，锁提前过期，线程 B 正好在另外 2 个节点也加锁成功，此时 Redlock 相当于失效了（Redis 作者和分布式系统专家争论的重要点就在这）

8、如果为了效率，使用基于单个 Redis 节点的分布式锁即可，此方案缺点是允许锁偶尔失效，优点是简单效率高

9、如果是为了正确性，业务对于结果要求非常严格，建议使用 Redlock，但缺点是使用比较重，部署成本高</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（77） 💬（8）<div>其实分布式锁选择Etcd的话，可能会更好。

Etcd 支持以下功能，正是依赖这些功能来实现分布式锁的：

1、Lease 即租约机制（TTL，Time To Live）机制：

Etcd 可以为存储的 KV 对设置租约，当租约到期，KV 将失效删除；同时也支持续约，即 KeepAlive；

Redis在这方面很难实现，一般假设通过SETNX设置的时间10S，如果发生网络抖动，万一业务执行超过10S，此时别的线程就能回去到锁；


2、Revision 机制：

Etcd 每个 key 带有一个 Revision 属性值，每进行一次事务对应的全局 Revision 值都会加一，因此每个 key 对应的 Revision 属性值都是全局唯一的。通过比较 Revision 的大小就可以知道进行写操作的顺序。 在实现分布式锁时，多个程序同时抢锁，根据 Revision 值大小依次获得锁，可以避免 “惊群效应”，实现公平锁；

Redis很难实现公平锁，而且在某些情况下，也会产生 “惊群效应”；
 

3、Prefix 即前缀机制，也称目录机制：

Etcd 可以根据前缀（目录）获取该目录下所有的 key 及对应的属性（包括 key, value 以及 revision 等）；

Redis也可以的，使用keys命令或者scan，生产环境一定要使用scan；


4、Watch 机制：

Etcd Watch 机制支持 Watch 某个固定的 key，也支持 Watch 一个目录（前缀机制），当被 Watch 的 key 或目录发生变化，客户端将收到通知；

Redis只能通过客户端定时轮训的形式去判断key是否存在；</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（20） 💬（4）<div>配合这篇文章看，效果更佳 https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;2P2-ujcdet9cUycokfyjHQ

这篇是早晨通勤坐地铁开了一个番茄钟看完的，番茄钟开启学霸模式，将这些学习和读书的app加入白名单，在一个番茄钟周期内就不能打开那些未加入白名单的app，可以防止刷耗精力的app，工作时也经常用，效果不错

如果自己能总结出来并给别人讲明白，就像课代表一样，每篇文章的留言都非常优秀，每次必看，这个知识点就掌握了，能用到工作实战上，那就锦上添花了</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/37/29/b3af57a7.jpg" width="30px"><span>凯文小猪</span> 👍（14） 💬（3）<div>这里老师漏了一点 就是session timeout处理 在分布式锁的场景中就是：
一个key过期了 但是代码还没处理完 此时就发生了重复加锁的问题。

通常我们有两种方式处理：
1. 设置看门狗 也就是redision的处理方式
2. 设置状态机 由最后的业务层来做代码回溯</div>2021-06-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLXDG2ux03bmIyEu9cR1SGX9QnDLJmSpYBg6CcfL6uUiaL90ypGIdmjXaj9uYLaxkQVoKSDeuAiaobQ/132" width="30px"><span>Geek_lijia</span> 👍（6） 💬（0）<div>关于分布式锁，两个大神的争论，我站Martin这边。
https:&#47;&#47;martin.kleppmann.com&#47;2016&#47;02&#47;08&#47;how-to-do-distributed-locking.html 
http:&#47;&#47;antirez.com&#47;news&#47;101 </div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/94/ec/8db3f04a.jpg" width="30px"><span>喰</span> 👍（5） 💬（0）<div>对于给锁设置过期时间，即使再怎么预估也很难保证线程在锁有效时间内完成操作。而且预估时间设置的过大也会影响系统性能，所以可以使用一个守护线程进行续租。</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/d3/0be6ae81.jpg" width="30px"><span>COLDLY</span> 👍（3） 💬（1）<div>老师，请问锁的过期时间怎么设置，会不会因为客户端执行业务操作时耗时太久超过过期时间，导致锁过期被释放了</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（3） 💬（1）<div>不可以。这两个命令不是原子的。发生异常的时候，可能会有正常的加锁结果。

分布式锁:
1.唯一性
2.原子性
3.可重入

Redlock Redisson zookeeper etcd都是业界常用的分布式锁方案。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/eb/30864e40.jpg" width="30px"><span>漂泊者及其影子</span> 👍（3） 💬（12）<div>
&#47;&#47;释放锁 比较unique_value是否相等，避免误释放
if redis.call(&quot;get&quot;,KEYS[1]) == ARGV[1] then
    return redis.call(&quot;del&quot;,KEYS[1])
else
    return 0
end

释放锁为什么不能使用delete操作？</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（3） 💬（0）<div>是不能把setnx 和 expire 命令分开的，因为无法保证两个操作执行的原子性，可能遇到各种异常，无法满足预期</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/ce/53392e44.jpg" width="30px"><span>BingoJ</span> 👍（2） 💬（0）<div>目前这把锁还有一个问题，就是不能保证可重入</div>2021-07-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/bxaaILnBnJTuqJn7jwhI1H6cctcovDSkml3icvGdPRmWbPqGLjvrqk3X1DNibJcW1stqav2RmatcjABDTfjG3v8A/132" width="30px"><span>Geek_d45d62</span> 👍（1） 💬（0）<div>“如果客户端 A 执行了 SETNX 命令加锁后，假设客户端 B 执行了 DEL 命令释放锁&quot;
应该不存在这种情况吧。A和B只有一个会SETNX成功。只有执行成功的才会执行下面的del操作。</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/79/ed/b8486f49.jpg" width="30px"><span>Ignite</span> 👍（1） 💬（0）<div>https:&#47;&#47;redis.io&#47;docs&#47;reference&#47;patterns&#47;distributed-locks&#47;
redis官网分布式锁</div>2022-10-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/apXvlhZqT7NLxOYz63qZzHebzCMszx3jI56gvRVeq62fX1b3zHy6fao1UknvuqfUkHkbYG0YkOBfvqXmJBxffg/132" width="30px"><span>Geek_045c20</span> 👍（1） 💬（0）<div>客户端为什么不同时向n个redis实例发起加锁请求？必须顺序依次吗</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/6c/bc/f751786b.jpg" width="30px"><span>Ming</span> 👍（1） 💬（1）<div>课后问题回答：
不可以，枷锁和给定过期时间是两个命令非原子性操作，若在加完锁后redis奔溃那么该锁永远也不会有过期时间；
所以建议使用指令：set key value ex|px nx；

另外：redis官方已不推荐使用redlock了！！！</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（1） 💬（1）<div>首先回答下这个问题,如果不保证原子性,那么实例宕机了,岂不是没有别人能拿到锁了,这是大问题
第二个问题,按照老师说的Redlock,达到半数以上,那么由一个问题,就是出现集群实例宕机一部分,导致其他客户端也达到了获取锁的数量(即在集群半数上加锁成功),那时候怎么办</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（1） 💬（0）<div>这节课，我提到，我们可以使用 SET 命令带上 NX 和 EX&#47;PX 选项进行加锁操作，那么，我想请你再思考一下，我们是否可以用下面的方式来实现加锁操作呢？



&#47;&#47; 加锁
SETNX lock_key unique_value
EXPIRE lock_key 10S
&#47;&#47; 业务逻辑
DO THINGS

答：非原子操作，所以不能用这种方式。</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/99/6060eb2d.jpg" width="30px"><span>平凡之路</span> 👍（1） 💬（3）<div>老师，您好，使用redis集群，使用setnx能保障加锁成功吗？即使一个实例挂了，还有其他实例能读取并加锁吗？</div>2021-06-03</li><br/><li><img src="" width="30px"><span>Geek_9a0c9f</span> 👍（1） 💬（0）<div>python的简单实现:
import threading
import time

import redis

redis_con = redis.StrictRedis(host=&#39;127.0.0.1&#39;, port=6379, db=0)

# redis_con.ttl(&#39;name&#39;)
redis_con.set(&quot;global&quot;, 10)

#守护进程，用来检测时间是否到期，快到期了，就续命
def add_time(redis_con, key_name):
    while True:
        time = redis_con.ttl(key_name)
        if time == 1:
            print(&quot;=====&quot;)
            redis_con.expire(key_name, 2)
            print(redis_con.ttl(key_name))

def test_distribute_lock():
    thead_id = str(time.time())
    if_has_key = redis_con.setnx(&quot;lock&quot;, thead_id)
    try:
        if not if_has_key:
            print(&quot;等待请稍后重试&quot;)
        else:
            redis_con.expire(&#39;lock&#39;, 2)
            # 开启守护进程
            t1 = threading.Thread(target=add_time, args=(redis_con, &#39;lock&#39;))
            t1.setDaemon(True)
            t1.start()
            redis_con.decr(&#39;global&#39;, 1)
            time.sleep(2)
    except Exception as e:
        print(e)
    finally:
                 # 执行完毕，释放锁，保证每个线程只能删除自己的锁
        if str(redis_con.get(&quot;lock&quot;), encoding=&quot;utf-8&quot;) == thead_id:
            redis_con.delete(&#39;lock&#39;)
        redis_con.close()

if __name__ == &#39;__main__&#39;:
    for i in range(5):
        t = threading.Thread(target=test_distribute_lock)
        t.start()
        t.join()
    print(&quot;===&gt;&quot;)</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（1） 💬（0）<div>不能这样做，因为两个命令就不是原子操作了。

set nx px的时候如果拿到锁的客户端在使用过程中超出了其设置的超时时间，那么就有这把锁同时被两个客户端持有的风险，所以需要在使用过程中不断去更新其过期时间。</div>2020-10-28</li><br/><li><img src="" width="30px"><span>Geek_f2fcdc</span> 👍（0） 💬（0）<div>思考题：不可以，考虑一种情况，客户端在执行setnx 之后，执行 expire 之前，崩溃了，也就是没有设置超时时间，这种情况下，锁可能永远不能释放了。</div>2023-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>不可以，因为 SETNX 和 EXPIRE 两条命令没有保证原子性，这样每一个客户端都能在执行 SETNX（哪怕没有生效） 之后紧接着设置超时时间，导致超时时间不断被修改。（此处有个疑问，超时时间每次被修改后是否会重新计时？如果在有效时间内再次设置超时时间不会重新计时，那么就不会有影响）</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>请问老师，释放锁时需要判断锁的标识，只有标识和加锁的客户端相同时才能释放，那么是否还有必要保证释放操作的原子性呢？</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2b/22/79d183db.jpg" width="30px"><span>H·H</span> 👍（0） 💬（0）<div>续约功能应该也要</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f3/06/8da1bf0c.jpg" width="30px"><span>Fredo</span> 👍（0） 💬（0）<div>这种实现分布式锁有哪些缺陷呢</div>2023-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/4f/731ef2c1.jpg" width="30px"><span>geektime_zpf</span> 👍（0） 💬（0）<div>老师好，锁变量的超时时间应该设置为多少呢？我理解，超时时间值应保证足够完成业务操作，如果超时时间设置小了，主动释放锁时可能锁已经过时失效了</div>2023-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（0） 💬（0）<div>对于 Redis key value 本身的并发访问，已经可以通过上一节中的无锁操作解决了。这篇文章提到的分布式锁的适用场景应该更多的侧重于其它业务场景。</div>2023-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（0）<div>这个分布式锁，实际上靠一个共享的锁变量标识去锁资源还是释放资源，其他的实例依靠这个共享的变量去锁与释放资源。而不是像单机那样直接在单机本地去锁。</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（0） 💬（0）<div>回答每课一问：不能将 SETNX 和 EXPIRE 命令分开来执行加锁。因为这样无法保证加锁操作的原子性。
再问下老师：
1 如何使用 Redis 客户端执行释放锁的 Lua 脚本？
2 Redlock 算法具体要怎么来实现？新版本的 Redis 是否已经实现？
</div>2023-02-08</li><br/>
</ul>