你好，我是蒋德钧。

Redis的主从同步机制不仅可以让从库服务更多的读请求，分担主库的压力，而且还能在主库发生故障时，进行主从库切换，提供高可靠服务。

不过，在实际使用主从机制的时候，我们很容易踩到一些坑。这节课，我就向你介绍3个坑，分别是主从数据不一致、读到过期数据，以及配置项设置得不合理从而导致服务挂掉。

一旦踩到这些坑，业务应用不仅会读到错误数据，而且很可能会导致Redis无法正常使用，我们必须要全面地掌握这些坑的成因，提前准备一套规避方案。不过，即使不小心掉进了陷阱里，也不要担心，我还会给你介绍相应的解决方案。

好了，话不多说，下面我们先来看看第一个坑：主从数据不一致。

## 主从数据不一致

主从数据不一致，就是指客户端从从库中读取到的值和主库中的最新值并不一致。

举个例子，假设主从库之前保存的用户年龄值是19，但是主库接收到了修改命令，已经把这个数据更新为20了，但是，从库中的值仍然是19。那么，如果客户端从从库中读取用户年龄值，就会读到旧值。

那为啥会出现这个坑呢？其实这是因为**主从库间的命令复制是异步进行的**。

具体来说，在主从库命令传播阶段，主库收到新的写命令后，会发送给从库。但是，主库并不会等到从库实际执行完命令后，再把结果返回给客户端，而是主库自己在本地执行完命令后，就会向客户端返回结果了。如果从库还没有执行主库同步过来的命令，主从库间的数据就不一致了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（229） 💬（11）<div>把 slave-read-only 设置为 no，让从库也能直接删除数据，以此来避免读到过期数据，这种方案是否可行？

我个人觉得这个问题有些歧义，因为尽管把 slave-read-only 设置为 no，其实 slave 也不会主动过期删除从 master 同步过来的数据的。

我猜老师想问的应该是：假设让 slave 也可以自动删除过期数据，是否可以保证主从库的一致性？

其实这样也无法保证，例如以下场景：

1、主从同步存在网络延迟。例如 master 先执行 SET key 1 10，这个 key 同步到了 slave，此时 key 在主从库都是 10s 后过期，之后这个 key 还剩 1s 过期时，master 又执行了 expire key 60，重设这个 key 的过期时间。但 expire 命令向 slave 同步时，发生了网络延迟并且超过了 1s，如果 slave 可以自动删除过期 key，那么这个 key 正好达到过期时间，就会被 slave 删除了，之后 slave 再收到 expire 命令时，执行会失败。最后的结果是这个 key 在 slave 上丢失了，主从库发生了不一致。

2、主从机器时钟不一致。同样 master 执行 SET key 1 10，然后把这个 key 同步到 slave，但是此时 slave 机器时钟如果发生跳跃，优先把这个 key 过期删除了，也会发生上面说的不一致问题。

所以 Redis 为了保证主从同步的一致性，不会让 slave 自动删除过期 key，而只在 master 删除过期 key，之后 master 会向 slave 发送一个 DEL，slave 再把这个 key 删除掉，这种方式可以解决主从网络延迟和机器时钟不一致带来的影响。

再解释一下 slave-read-only 的作用，它主要用来控制 slave 是否可写，但是否主动删除过期 key，根据 Redis 版本不同，执行逻辑也不同。

1、如果版本低于 Redis 4.0，slave-read-only 设置为 no，此时 slave 允许写入数据，但如果 key 设置了过期时间，那么这个 key 过期后，虽然在 slave 上查询不到了，但并不会在内存中删除，这些过期 key 会一直占着 Redis 内存无法释放。

2、Redis 4.0 版本解决了上述问题，在 slave 写入带过期时间的 key，slave 会记下这些 key，并且在后台定时检测这些 key 是否已过期，过期后从内存中删除。

但是请注意，这 2 种情况，slave 都不会主动删除由 *master 同步过来带有过期时间的 key*。也就是 master 带有过期时间的 key，什么时候删除由 master 自己维护，slave 不会介入。如果 slave 设置了 slave-read-only = no，而且是 4.0+ 版本，slave 也只维护直接向自己写入 的带有过期的 key，过期时只删除这些 key。

另外，我还能想到的主从同步的 2 个问题:

1、主从库设置的 maxmemory 不同，如果 slave 比 master 小，那么 slave 内存就会优先达到 maxmemroy，然后开始淘汰数据，此时主从库也会产生不一致。

2、如果主从同步的 client-output-buffer-limit 设置过小，并且 master 数据量很大，主从全量同步时可能会导致 buffer 溢出，溢出后主从全量同步就会失败。如果主从集群配置了哨兵，那么哨兵会让 slave 继续向 master 发起全量同步请求，然后 buffer 又溢出同步失败，如此反复，会形成复制风暴，这会浪费 master 大量的 CPU、内存、带宽资源，也会让 master 产生阻塞的风险。</div>2020-11-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRFRX8kNzNet7FibNvtavbVpAwK09AhIhrib9k762qWtH6mre8ickP7hM5mgZC4ytr8NnmIfmAhxMSQ/132" width="30px"><span>老大不小</span> 👍（31） 💬（2）<div>老师，slave-serve-stale-data这个命令说的不清不楚的，对于初学者来说不明就里。

slave-serve-stale-data

解释：当一个slave与master失去联系时，或者复制正在进行的时候，slave应对请求的行为：1) 如果为 yes（默认值） ，slave 仍然会应答客户端请求，但返回的数据可能是过时，或者数据可能是空的在第一次同步的时候；2) 如果为 no ，在你执行除了 info 和 salveof 之外的其他命令时，slave 都将返回一个 &quot;SYNC with master in progress&quot; 的错误。


29、slave-read-only

解释：设置slave是否是只读的。从2.6版起，slave默认是只读的。
</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/a6/7b/1b581f07.jpg" width="30px"><span>思变</span> 👍（6） 💬（2）<div>老师您好,关于bind参数,不是设置redis能接受哪个本机网卡接入的连接吗?为什么要配置多个哨兵的IP呢</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/81/96f656ef.jpg" width="30px"><span>杨逸林</span> 👍（6） 💬（0）<div>不是个好方法，如果不同客户端，去非当前从库读取数据时，就会出现缓存不一致的情况。</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d2/65/79d89c77.jpg" width="30px"><span>小白白不白</span> 👍（5） 💬（3）<div>EXPIRE、PEXPIRE和EXPIREAT三个命令都会转换成PEXPIREAT命令来执行,难道redis对于aof日志文件没有转为PEXPIREAT吗?</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/5b/f700f9ef.jpg" width="30px"><span>刘浩</span> 👍（4） 💬（0）<div>slave-serve-stale-data配置了主从中断后，从库的逻辑
--no ：从库只能应答INFO和SLAVEOF
--yes默认 ：正常应答
这样不知道对不对</div>2020-11-13</li><br/><li><img src="" width="30px"><span>赵茭茭</span> 👍（3） 💬（1）<div>主从复制 不是复制的是rdb吗 不是aof啊 这个和指令 带AT的还有效吗 还是我理解的有问题</div>2020-12-07</li><br/><li><img src="" width="30px"><span>Geek_be8402</span> 👍（2） 💬（0）<div>这篇内容已经过时了，2021.5 以后主节点上执行的 expire 命令已经会转换为绝对时间传播给 replica
https:&#47;&#47;github.com&#47;redis&#47;redis&#47;commit&#47;53d1acd598b689b2bbc470d907b9e40e548d63f6</div>2024-04-19</li><br/><li><img src="" width="30px"><span>Geek1254</span> 👍（2） 💬（0）<div>为什么不在主库删除过期key时给从库发送删除命令</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/dc/85515477.jpg" width="30px"><span>yu</span> 👍（2） 💬（2）<div>redis为何不把底层的expire实现成为expireAt，再发给从库进行同步，避免出现过期数据问题？</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/72/e7bc6ff1.jpg" width="30px"><span>零点999</span> 👍（2） 💬（0）<div>只有主库提供服务，从库只保证高可用</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（1） 💬（0）<div>不是一个好方法，这样从库也能处理写命令，这样更容易造成主从不一致。</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/a6/7b/1b581f07.jpg" width="30px"><span>思变</span> 👍（1） 💬（1）<div>protected-mode我看参数文件的解释是,如果protected-mode设置为yes,如果实例未设置密码且未设置bind参数,只能通过127.0.0.1进行本地连接,是我理解的不对吗?</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c3/b6/7483c3b7.jpg" width="30px"><span>淡蓝色</span> 👍（0） 💬（0）<div>slave-serve-stale-data参数设置成yes，主从复制中，从服务器可以响应客户端请求；

slave-serve-stale-data参数设置成no，主从复制中，从服务器将阻塞所有请求，有客户端请求时返回“SYNC with master in progress”；</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>从库执行写命令后，也需要给其它从库和主库做同步，同样会发生读到过期数据的问题。所以不是有效的方法。</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/33/acacb6ac.jpg" width="30px"><span>砖用冰西瓜</span> 👍（0） 💬（0）<div>这个过期数据的问题是不是也有可能影响到 Redis 分布式锁的使用？</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/e8/7734b8d3.jpg" width="30px"><span>P</span> 👍（0） 💬（0）<div>仔细看了下，逻辑有问题，从库读到过期数据跟过期策略没有关系吧</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/cb/8b/fa482708.jpg" width="30px"><span>Zhqqqq</span> 👍（0） 💬（0）<div>老师问一下关于外部程序监控 Redis INFO replication 主从延迟信息来为客户端是否能访问改从节点。这个方案似乎就是把 AP 模型改为 CP。而且增加了架构复杂度，毕竟又增加了外部程序，在客户端进行监控不行吗？</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/a0/aa6d4ecd.jpg" width="30px"><span>张潇赟</span> 👍（0） 💬（0）<div>老师说的slave-serve-stale-data 这个参数在后面的版本应该是修改成了replica-serve-stale-data了吧。官方的配置文件中并没有找到slave-serve-stale-data这个配置参数
</div>2022-03-30</li><br/><li><img src="" width="30px"><span>受超凡</span> 👍（0） 💬（0）<div>老师好，有个问题请教下。主从同步不是通过RDB的方式进行的吗，从库读RDB的话不用执行命令吧，是直接读的数据吧，那从库为什么还会设置过期时间呢？不是直接读的吗？</div>2021-11-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKib3vNM6TPT1umvR3TictnLurJPKuQq4iblH5upgBB3kHL9hoN3Pgh3MaR2rjz6fWgMiaDpicd8R5wsAQ/132" width="30px"><span>陈阳</span> 👍（0） 💬（1）<div>主从库在一个机房不会降低容灾性吗？</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>这个问题有些没看懂,是直接从从库上删除数据吗,这应该是不被允许的把,现在在云上用K8S管理,也是设置了多个service,一个用来写一个用来读,从库只用来读取数据,不应该负责删除数据
而且,即使设置了过期时间,从库在达到之后也不会删除数据,只是返回空,只有接到主库删除操作才会进行删除</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ea/65/ab8748c5.jpg" width="30px"><span>玄墨</span> 👍（0） 💬（0）<div>过期键脏读问题,有个疑惑:老师建议使用expireat 和pexpireat 因为后面跟的是时间戳,而不是当前服务时间+过期时间.但是实际上redis内部在配置过期时间之后,不是都转换成了pexpireat并存储到过期字典中吗?所以这几个命令最后在redis过期字典中理论上表现是一致的,不应该出现老师说的因为命令不一样而出现脏读现象吧.麻烦老师解读下🙏</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/bf/415023b5.jpg" width="30px"><span>璩雷</span> 👍（0） 💬（1）<div>从库不能执行写操作，过期的数据是如何被删除的呢？具体过程是怎样的？</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/99/aefe1b12.jpg" width="30px"><span>n0thing</span> 👍（0） 💬（0）<div>不管redis自身还是哨兵的protected-mode， 看官方配置解释，从安全性上考虑设置为yes可能更加合理？看上去只用加上密码和Bind本机redis listen的对外IP和方便本地连接的127.0.0.1即可。不用Bind另外两台哨兵的对外IP。</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>Redis 主从同步有三个坑：主从数据不一致、读到过期数据、配置不合理服务挂掉。

为了避免主从数据不一致，一方面要保证主从之间的网络状况良好，另外主从服务器的配置也不能相差太远；另一方面，可以写一个外部程序，监控 master_repl_offset 和 slave_repl_offset 之间的差值，如果差值过大，就先不让客户端和这个从库连接。

读到过期数据是因为 Redis 本身的过期删除策略（惰性删除和定期删除）引起的，主库上的过期数据被惰性删除了，但是从库上没有（从库只读）。

为了避免读到过期数据，一方面是尽量使用 Redis 3.2 以后的版本，另外一条就是尽量使用 EXPIREAT&#47;PEXPIREAT 命令，指定具体的过期时间点。

因为配置不当，导致在主从切换的过程中服务挂掉的参数主要是两个，protected-mode 和 cluster-node-timeout。

为了让哨兵之间可以互相访问，那么 protected-mode 需要设置为 no，并且将哨兵的 IP 都列在 bind 里。

为了避免实例主从切换，导致集群心跳超时，需要把 cluster-node-timeout 配置的大一点 （10~20 秒）

最后，将 slave-serve-stale-data 设置为 no，从库只能服务 INFO、SLAVEOF 命令，可以避免从库中读到不一致的数据；而 slave-save-only 设置为 yes，从库只能处理读请求。

对于课后题，将 slave-read-only 设置为 no，从库也能处理写命令，肯定不是一个好办法，这样一来主从之间的同步就变得复杂无比，或者说就干脆变成了双主结构了。

课代表补充，slave 不会主动删除由  master 同步过来的带有过期时间的 key，删除由 master 自己维护。

老师的补充，主从复制中的增删改都需要在主库执行。</div>2021-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e1/9d/3ec0adec.jpg" width="30px"><span>喃寻</span> 👍（0） 💬（0）<div>课后题: 不能让从库执行写操作，否则会造成主从数据不一致。</div>2021-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c2/64/5cd6efa0.jpg" width="30px"><span>泊</span> 👍（0） 💬（0）<div>如果过期数据很多，并且一直没有再被访问的话，这些数据就会留存在 Redis 实例中。业务应用之所以会读到过期数据，这些留存数据就是一个重要因素。  
这里不太明白，如果业务应用再次读取数据的话如果数据过期的话不应该会惰性删除吗，怎么还会读取到过期数据呢？还有从库不会执行删除操作的话它内存直增不减吗，一直等到lru回收吗？</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（0） 💬（0）<div>并不是一个好方法。
增删改都应该在主库做。如果在从库处理会有数据不一致的情况出现。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/66/719292c3.jpg" width="30px"><span>Ray</span> 👍（0） 💬（0）<div>Redis主从模式部署时，如01为主，02为从，在客户端连接读写数据时是需要自行指定IP嘛？ 像这种主从读写的情况，常见的开源客户端是如何处理的，如Java中的redission和.net中的stackexchang.redis.</div>2020-12-01</li><br/>
</ul>