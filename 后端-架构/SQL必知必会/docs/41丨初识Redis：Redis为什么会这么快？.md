之前我们讲解了一些RDBMS的使用，比如MySQL、Oracle、SQL Server和SQLite等，实际上在日常工作中，我们还会接触到一些NoSQL类型的数据库。如果对比RDBMS和NoSQL数据库，你会发现RDBMS建立在关系模型基础上，强调数据的一致性和各种约束条件，而NoSQL的规则是“只提供你想要的”，数据模型灵活，查询效率高，成本低。但同时，相比RDBMS，NoSQL数据库没有统一的架构和标准语言，每种数据库之间差异较大，各有所长。

今天我们要讲解的Redis属于键值（key-value）数据库，键值数据库会使用哈希表存储键值和数据，其中key作为唯一的标识，而且key和value可以是任何的内容，不论是简单的对象还是复杂的对象都可以存储。键值数据库的查询性能高，易于扩展。

今天我们就来了解下Redis，具体的内容包括以下几个方面：

1. Redis是什么，为什么使用Redis会非常快？
2. Redis支持的数据类型都有哪些？
3. 如何通过Python和Redis进行交互？

## Redis是什么，为什么这么快

Redis全称是REmote DIctionary Server，从名字中你也能看出来它用字典结构存储数据，也就是key-value类型的数据。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/90/4e/efaea936.jpg" width="30px"><span>墨禾</span> 👍（45） 💬（6）<div>为什么要设计成单线程？
1.单线程减少了cpu资源的争用，避免了上下文的切换。
2.基于内存读写，单线程读写耗时更少。

为啥redis单线程模型也能效率这么高？

1）纯内存操作
2）核心是基于非阻塞的IO多路复用机制
3）单线程反而避免了多线程的频繁上下文切换问题</div>2019-09-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（35） 💬（2）<div>老师能否讲下mongodb，以及redis和mongodb的差别，实际使用时选择应该做哪些方面的考虑</div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/46/209ca424.jpg" width="30px"><span>Coool</span> 👍（7） 💬（1）<div>为什么使用单线程？
1、代码更清晰，处理逻辑更简单
2、不用去考虑各种锁的问题，不存在加锁释放锁操作，没有因为可能出现死锁而导致的性能消耗
3、不存在多进程或者多线程导致的切换而消耗CPU</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/5f/cec1e980.jpg" width="30px"><span>xcoder</span> 👍（3） 💬（6）<div>不好意思，我觉得这个课程对初学者，或者完全没接触过python和redis的同学来说不太友好吧。还得补充很多知识，安装python和redis，如何操作等等。。。这些都还需要网上找下教程，虽然最近都有在看起来，但觉得学起来还是有点力不从心，越到后面感觉评论的人也越来越少了，不知道后面的课时学的人也是不是越来越少了</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（1）<div>跟着老师一起精进。加油。</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/f1/16545faf.jpg" width="30px"><span>学习</span> 👍（1） 💬（1）<div>文中多次提到key-filed-value，是field还是filed啊！！！！

Redis采用单进程单线程模型，这样做的好处就是避免了上下文切换和不必要的线程之间引起的资源竞争。这样就会很快。

Redis采用多路I&#47;O复用技术，这样就会解决单线程慢效率弊端，其中有个集群模式，能支持多客户端使用</div>2019-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcFhGY0NV4kFzOSXWDHR2lrI2UbUP4Y016GOnpTH7dqSbicqJarX0pHxMsfLopRiacKEPXLx7IHHqg/132" width="30px"><span>一路前行</span> 👍（2） 💬（0）<div>redis6.0，采用了多线程模式，老师怎么看？？？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（2） 💬（0）<div>用Python连接Redis报错“ConnectionRefusedError: [WinError 10061]由于目标计算机积极拒绝，无法连接。”的解决办法 ：
https:&#47;&#47;blog.csdn.net&#47;weixin_41013322&#47;article&#47;details&#47;106387319
希望对各位有帮助</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/59/1d/c89abcd8.jpg" width="30px"><span>四喜</span> 👍（2） 💬（0）<div>我的速度是老师的1&#47;10</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/c4/f2d7ce76.jpg" width="30px"><span>有所思</span> 👍（2） 💬（8）<div>老师，为什么你讲的Redis底层数据结构和王争讲的数据结构与算法课里面的有些不一样，他说的里面redis会根据数据大小和数量选择不同的数据结构，而且有序集合用的是跳表实现，有点蒙</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（0）<div>1. Redis用作缓存数据库
2.单线程IO复用模型
3.持久化方式有RDB,AOF , 一般开启aof </div>2022-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/56/5a5098d1.jpg" width="30px"><span>明月</span> 👍（0） 💬（0）<div>使用单线程，是不是原理就是类似JavaScript的线程模型，采用轮询一个队列的方式</div>2022-10-22</li><br/><li><img src="" width="30px"><span>小虾米</span> 👍（0） 💬（0）<div>1.0412158966064453
1.049706220626831


感谢老师，初识redis</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（0） 💬（1）<div>老师您好：
      Redis用跳表来实现有序集合的，不是使用hash表来实现有序集合吧？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/6a/6d82e7a3.jpg" width="30px"><span>暮雨</span> 👍（0） 💬（0）<div>redis的单线程怎么理解？查看redis服务不至一个线程</div>2019-11-05</li><br/>
</ul>