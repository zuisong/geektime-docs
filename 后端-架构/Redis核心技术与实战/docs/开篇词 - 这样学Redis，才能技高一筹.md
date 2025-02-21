你好，我是蒋德钧，欢迎和我一起学习Redis。

我博士毕业后，就一直在中科院计算所工作，现在的职位是副研究员。在过去的14年时间里，我一直从事互联网底层基础设施方面的研究工作，主要的研究方向为新型存储介质、键值数据库、存储系统和操作系统。

2015年的时候，我和我的团队接到了一个高难度任务，目标是设计一个单机性能达到千万级吞吐量的键值数据库。为了实现这个目标，我们就开始重点研究Redis，从此，我就和这个数据库结缘了。

作为键值数据库，Redis的应用非常广泛，如果你是后端工程师，我猜你出去面试，八成都会被问到与它相关的性能问题。比如说，为了保证数据的可靠性，Redis需要在磁盘上读写AOF和RDB，但在高并发场景里，这就会直接带来两个新问题：一个是写AOF和RDB会造成Redis性能抖动，另一个是Redis集群数据同步和实例恢复时，读RDB比较慢，限制了同步和恢复速度。

那这个问题有没有好的解决方法呢？哈哈，这里我卖了个关子。其实，一个可行的解决方案就是使用非易失内存NVM，因为它既能保证高速的读写，又能快速持久化数据。我和团队就在NVM的键值数据库上开展了诸多深入研究，先后申请了二十余项专利，也在顶级学术会议上发表了学术论文。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/19/28074c40.jpg" width="30px"><span>小盖</span> 👍（376） 💬（13）<div>给这个我们打磨了两年的专栏留个印记吧，就像我们编辑说的，希望这不只是一个课程，而且还是一个作品，我们要精益求精，追求卓越。

这不，昨天一上线，我们就发现课程配图虽然够用，但不精致。于是，我们的编辑同学就连夜赶工做了替换。

上周刚做完Java工程师方面的招聘调研，我可以确定地说，绝大多数的一线公司在面试后端岗位时，都会问到Redis相关的问题（RPC、缓存、MQ三驾马车）。咱们就从今天开始，和蒋老师，一起学Redis吧。</div>2020-08-04</li><br/><li><img src="" width="30px"><span>Geek_48707a</span> 👍（62） 💬（8）<div>请问一下老师，Redis中sorted set 底层实现是一个dict + 一个zskiplist， Redis底层为什么要如此设计。zadd key score value 这样的形式，那如果底层采用了跳表的数据结构zset到底是如何存储数据的呢？dict中存储的是什么，跳表中存储的又是什么呢</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ed/70/d1fc87bc.jpg" width="30px"><span>闫攀</span> 👍（38） 💬（5）<div>课程最后会梳理怎么更高效的读redis源码吗，  希望可以得到作者的回复</div>2020-08-03</li><br/><li><img src="" width="30px"><span>Geek_224f63</span> 👍（29） 💬（10）<div>蒋老师你好，不知道研发hikv的背景是什么呢？难道redis都不能满足这个需求吗？</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/dc/1a/04f212f6.jpg" width="30px"><span>张晗_Jeremy</span> 👍（19） 💬（1）<div>第一个沙发，收到通知就买了。gogogo！</div>2020-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1LIW93RQ3ZvevCcfgib9Z4NwHsNAbicmGkicZwe9zCBPc9A2IXfLtXGUmzqrsibn1FibZcNIOddOrF9icuww9cYZD5ibA/132" width="30px"><span>Geek_75d94a</span> 👍（17） 💬（3）<div>两张图给我很深的启发，很好的归纳零散的知识点，让我想尝试用在其他地方建立一下知识体系。</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（16） 💬（4）<div>如果使用非易失内存 NVM, 这样设计出来的 高性能的健值数据库 是不是就对硬件的依赖就很大了？</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/c5/78626367.jpg" width="30px"><span>型火🔥</span> 👍（12） 💬（1）<div>两大维度和三大主线的系统方法论可以迁移到大部分的中间件体系学习中</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6d/b1/34ed2fb8.jpg" width="30px"><span>💕</span> 👍（7） 💬（2）<div>您好，还有就是你说的redis技术，存储数据。是不是说就不用数据库了比如mysql sql server等，直接用redis当数据库了呢？</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/85/f72f1d94.jpg" width="30px"><span>与路同飞</span> 👍（7） 💬（2）<div>老师说的以这种问题画像图这种学习方式挺好的，用什么技术点解决什么场景问题，自己在以后学习也要善于用这种方式去归纳总结，不至于学了不会用</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（3） 💬（1）<div>被两张图吸引了， 一直想总结Redis的全景图，自己水平有限，一直都不满意，直到看到这两张图，期待后续～～～</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7a/a4/79ffe77c.jpg" width="30px"><span>发飙的蜗牛</span> 👍（1） 💬（1）<div>刚刚在哔哩哔哩学习完一门入门的redis,但是对于它得原理性东西还是有点懵，然后就遇见了你，感谢！会坚持看下去</div>2020-12-19</li><br/><li><img src="" width="30px"><span>Geek_1e8830</span> 👍（0） 💬（1）<div>感觉开头就不错，加油！</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/86/cc/d63bb0f2.jpg" width="30px"><span>苏格拉没底</span> 👍（0） 💬（1）<div>赞一下蒋老师作品，已经全部读完，虽然还是很迷惑，但有一个很系统的认知，个人之言，这是我在极客时间读过的作品中最好的一个</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9d/1e/962902e1.jpg" width="30px"><span>Sincey</span> 👍（0） 💬（1）<div>2020年11月20日开始学习，紧跟老师的步伐，希望自己能把redis吃透吃懂，立Flag。</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/99/5e/33481a74.jpg" width="30px"><span>Lemon</span> 👍（0） 💬（1）<div>挑了一圈入手的第一个课程，感觉物超所值。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/24/c6100ac6.jpg" width="30px"><span>C家族铁粉</span> 👍（0） 💬（2）<div>课程后面会不会大篇幅的插入java相关的内容啊，没学java有点担心，看目录后面有谈到读源码，挺感兴趣的。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/ed/50019f1f.jpg" width="30px"><span>真心蛋疼</span> 👍（0） 💬（2）<div>Redis是目前最主流的消息队列中间健，之前一直专注于应用层的运维。希望能通过本次课程对底层的源码有系统的了解和优化。加油！！！</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/47/f6c772a1.jpg" width="30px"><span>Jackey</span> 👍（0） 💬（1）<div>去年学过redis，也读过一部分源码。现在很多知识点有些模糊了，打算跟着老师再来一遍</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（0） 💬（1）<div>看到三个维度，高性能，高可用，高拓展，这应该也是大部分中间件的三大维度。</div>2020-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIgyJnqj4CXmyU1l15tNjkvr0fcicic3FDeNT8pxTojA6CuY01rIuT89fb6IjuwAbc42JuXl0tdzj8Q/132" width="30px"><span>Geek_351cba</span> 👍（0） 💬（1）<div>如果要进行实践的话，是用docker for windows版本还是在虚拟机中使用好
</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/52/7abc67cc.jpg" width="30px"><span>亚伦</span> 👍（0） 💬（1）<div>来学习如何处理长尾延迟问题</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5a/03/ce24280c.jpg" width="30px"><span>秋梵</span> 👍（0） 💬（1）<div>之前都是自己看书学习，感觉掌握的知识点很零碎，程度深不深浅不浅的 没有啥很系统的知识体系 希望能通过这门课的学习深入学习redis 能学的比较透彻</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>老师，服务器一旦重启，感觉数据很容易丢失啊，希望老师多多讲解如何保证数据的可靠性。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/fe/d0e25d57.jpg" width="30px"><span>朱晔</span> 👍（65） 💬（2）<div>干货🈵🈵</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fd/94/8704d2b0.jpg" width="30px"><span>spoofer</span> 👍（32） 💬（2）<div>整理的 笔记 https:&#47;&#47;github.com&#47;TopSpoofer&#47;learning&#47;tree&#47;master&#47;redis</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b9/19/f4ef2c9a.jpg" width="30px"><span>秦穆之</span> 👍（28） 💬（8）<div>
## 基础数据结构
* **02 | 数据结构：快速的Redis有哪些慢操作？**
* **11 | “万金油”的String，为什么不好用了？**
* **12 | 有一亿个keys要统计，应该用哪种集合？**
* **13 | GEO是什么？还可以定义新的数据类型吗？**
* **14 | 如何在Redis中保存时间序列数据？**
## 网络与性能
* **03 | 高性能IO模型：为什么单线程Redis能那么快？**
* **16 | 异步机制：如何避免单线程模型的阻塞？**
* **17 | 为什么CPU结构也会影响Redis的性能？**
* **18 | 波动的响应延迟：如何应对变慢的Redis？（上）**
* **19 | 波动的响应延迟：如何应对变慢的Redis？（下）**
* **20 | 删除数据后，为什么内存占用率还是很高？**
* **21 | 缓冲区：一个可能引发“惨案”的地方**
## 持久化
* **04 | AOF日志：宕机了，Redis如何避免数据丢失？**
* **05 | 内存快照：宕机后，Redis如何实现快速恢复？**
* **06 | 数据同步：主从库如何实现数据一致？**
## 哨兵机制
* **07 | 哨兵机制：主库挂了，如何不间断服务？**
* **08 | 哨兵集群：哨兵挂了，主从库还能切换吗？**
* **32 | Redis主从同步与故障切换，有哪些坑？**
## 分布式
* **09 | 切片集群：数据增多了，是该加内存还是加实例？**
* **29 | 无锁的原子操作：Redis如何应对并发访问？**
* **30 | 如何使用Redis实现分布式锁？**
* **31 | 事务机制：Redis能实现ACID属性吗？**
* **35 | Codis VS Redis Cluster：我该选择哪一个集群方案？**
* **37 | 数据分布优化：如何应对数据倾斜？**
## 缓存策略与常用架构
* **23 | 旁路缓存：Redis是如何工作的？**
* **24 | 替换策略：缓存满了怎么办？**
* **25 | 缓存异常（上）：如何解决缓存和数据库的数据不一致问题？**
* **26 | 缓存异常（下）：如何解决缓存雪崩、击穿、穿透难题？**
* **27 | 缓存被污染了，该怎么办？**
* **33 | 脑裂：一次奇怪的数据丢失**
## 实用项目
* **28 | Pika: 如何基于SSD实现大容量Redis？**
* **36 | Redis支撑秒杀场景的关键技术和实践都有哪些？**</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/64/be/12c37d15.jpg" width="30px"><span>CityAnimal</span> 👍（22） 💬（0）<div>打卡
* [ ] “坑“
    * [ ] CPU上的坑
    * [ ] 内存使用上的坑
    * [ ] 持久化存储上的坑
    * [ ] 网络通信上的坑
* [ ] 系统观
    * [ ] 建立完整的知识框架
        * [ ] 两大维度
            * [ ] 应用纬度
                * [ ] 缓存应用
                * [ ] 集群应用
                * [ ] 数据结构应用
            * [ ] 系统纬度
                * [ ] 处理层
                    * [ ] 线程模型 - （缓存应用，高性能主线）
                    * [ ] 主从复制 - （集群应用，高可靠主线）
                    * [ ] 数据分片 - （数据应用，高可扩展主线）
                * [ ] 内存层
                    * [ ] 数据结构 - （缓存应用，高性能主线）
                    * [ ] 哨兵机制 - （集群应用，高可靠主线）
                * [ ] 存储层
                    * [ ] AOF - （缓存应用，高性能主线）
                    * [ ] RDF - （集群应用，高可靠主线）
                    * [ ] 负载均衡 - （数据结构应用，高可扩展主线）
                * [ ] 网络层
                    * [ ] epoll- （缓存应用，高性能主线）
        * [ ] 三大主线
            * [ ] 高性能
            * [ ] 高可用
            * [ ] 高可扩展</div>2021-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/ff/986ffb41.jpg" width="30px"><span>轻飘飘过</span> 👍（12） 💬（0）<div>redis它终于来了</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ee/ce/c024a857.jpg" width="30px"><span>藏锋</span> 👍（6） 💬（5）<div>我一直有个疑问，对于原理性的知识，真的要掌握这么细吗？就是达到能够随口将每个细节说出来说清楚的地步。说实话我之前对于原理性的东西只会了解个大概，能说出个大概，不会抠细节。而且我们作为开发，要学习的东西实在太多，越往高处走，会发现什么底层、开发、运维、架构、软件工程、测试、业务设计都是一体的都要涉猎。但是我们个人时间和精力都很有限，那么我们学习某项技术的时候，真的要把这门技术的所有细节都掌握吗？而这些细节真的不只是靠理解就够的，更多的要靠记忆，怎么说呢，就是不仅要理解还要背书。因为工作中用不到，时间不长肯定会忘。各位大牛们还有老师，麻烦谁给我解惑！</div>2021-04-09</li><br/>
</ul>