在上一篇文章中，我们已经对Redis有了初步的认识，了解到Redis采用Key-Value的方式进行存储，在Redis内部，使用的是redisObject对象来表示所有的key和value。同时我们还了解到Redis本身用的是单线程的机制，采用了多路I/O复用的技术，在处理多个I/O请求的时候效率很高。

今天我们来更加深入地了解一下Redis的原理，内容包括以下几方面：

1. Redis的事务处理机制是怎样的？与RDBMS有何不同？
2. Redis的事务处理的命令都有哪些？如何使用它们完成事务操作？
3. 如何使用Python的多线程机制和Redis的事务命令模拟多用户抢票？

## Redis的事务处理机制

在此之前，让我们先来回忆下RDBMS中事务满足的4个特性ACID，它们分别代表原子性、一致性、隔离性和持久性。

Redis的事务处理与RDBMS的事务有一些不同。

首先Redis不支持事务的回滚机制（Rollback），这也就意味着当事务发生了错误（只要不是语法错误），整个事务依然会继续执行下去，直到事务队列中所有命令都执行完毕。在[Redis官方文档](https://redis.io/topics/transactions)中说明了为什么Redis不支持事务回滚。

只有当编程语法错误的时候，Redis命令执行才会失败。这种错误通常出现在开发环境中，而很少出现在生产环境中，没有必要开发事务回滚功能。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（21） 💬（1）<div>客户端2首先返回 OK，客户端1返回 nil 。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（16） 💬（2）<div>单线程的REDIS也采用事物，我觉得主要是用来监视自己是否可以执行的条件是否得以满足，尤其是这个条件有可能不在REDIS自身的控制范围之内的时候。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（6） 💬（2）<div>返回结果跟之前一样，因为客户端1还是因为key变化了执行失败</div>2019-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJETibDh9wrP19gj9VdlLRmppuG1FibI7nyUGldEXCnoqKibKIB18UMxyEHBkZNlf5vibLNeofiaN5U6Hw/132" width="30px"><span>steve</span> 👍（5） 💬（1）<div>是否能用DECR实现呢？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/18/ee/a1ed60d1.jpg" width="30px"><span>ABC</span> 👍（4） 💬（1）<div>推荐大家在Docker容器里面搭建各种开发环境,方便而且又不用配置特别多东西.以前我是在Windows上直接部署MySQL作为开发环境,后来就换到Docker了,才发现那么方便!~</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（1）<div>对于第一个问题，我觉得原因在于WATCH+MULTI主要是事物来监视自身执行得以的条件是否满足的</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ee/54/dac0a6b6.jpg" width="30px"><span>小白菜</span> 👍（0） 💬（1）<div>总感觉后面这几篇讲的Redis,有点浅显，抛砖引玉一下。可能由于篇幅的缘故吧！</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（1）<div>上面的抢票时序，Redis是串行化的，不能在T2时刻同时两个客户端都执行Watch吧。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（24） 💬（1）<div>思考题：
1、redis服务器只支持单进程单线程，但是redis的客户端可以有多个，为了保证一连串动作的原子性，所以要支持事务。
2、客户端2成功，客户端1失败。这个问题类似于Java并发的CAS的ABA问题。redis应该是除了看ticket的值外，每个key还有一个隐藏的类似于版本的属性。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/9d/d487c368.jpg" width="30px"><span>花见笑</span> 👍（6） 💬（5）<div>推荐使用 Redis 脚本功能 来代替事务 性能高出很多</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/6b/03c290de.jpg" width="30px"><span>godfish</span> 👍（6） 💬（1）<div>抢票那个我有个问题是如果ticket大于1的情况，因为watch了key，客户端1岂不是也抢票失败了？实际上不应该失败吧。或者是这里ticket的1不是代表数量代表其中一张票？</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/56/5a5098d1.jpg" width="30px"><span>明月</span> 👍（0） 💬（0）<div>不是串行化事物了么，没有问题</div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（1）<div>虽然Redis是单线程的，但是多个客户端进行多个操作时却无法保证原子性，也就是说多个指令是交叉执行的</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/b6/5f80d0dc.jpg" width="30px"><span>漫山遍野都是橘</span> 👍（0） 💬（0）<div>用 redis lua script 来实现更方便</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/ec/3d51d5e6.jpg" width="30px"><span>上校</span> 👍（0） 💬（1）<div>redis内抢完票如何同步到mysql呢？如何和mysql最终一致性？是通过持久化？还是说抢票成功就同步呢？老师有没有经验分享？谢谢</div>2020-07-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EcYNib1bnDf5dz6JcrE8AoyZYMdqic2VNmbBtCcVZTO9EoDZZxqlQDEqQKo6klCCmklOtN9m0dTd2AOXqSneJYLw/132" width="30px"><span>博弈</span> 👍（0） 💬（0）<div>问题一：我认为是用来判断当前事务执行得条件是否满足
问题二：这是ABA问题，每变化一次，相应的版本也会跟着变化</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（0） 💬（0）<div>Redis 集群的情况下，会不会抢票就因此不适用？</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（0）<div>思考题：
1，Redis是单线程程序，多个客户端在并发访问的时候要在多个线程间切换来交替执行，所以还是要进行并发控制。
2，？？</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/fe/1241bc83.jpg" width="30px"><span>水如天</span> 👍（0） 💬（0）<div>能分析下JSON类型的存储和查询原理吗</div>2019-09-11</li><br/>
</ul>