你好，我是蒋德钧。

今天这节课是咱们课程的最后一节课了，我们来聊聊Redis的下一步发展。

这几年呢，新型非易失存储（Non-Volatile Memory，NVM）器件发展得非常快。NVM器件具有容量大、性能快、能持久化保存数据的特性，这些刚好就是Redis追求的目标。同时，NVM器件像DRAM一样，可以让软件以字节粒度进行寻址访问，所以，在实际应用中，NVM可以作为内存来使用，我们称为NVM内存。

你肯定会想到，Redis作为内存键值数据库，如果能和NVM内存结合起来使用，就可以充分享受到这些特性。我认为，Redis发展的下一步，就可以基于NVM内存来实现大容量实例，或者是实现快速持久化数据和恢复。这节课，我就带你了解下这个新趋势。

接下来，我们先来学习下NVM内存的特性，以及软件使用NVM内存的两种模式。在不同的使用模式下，软件能用到的NVM特性是不一样的，所以，掌握这部分知识，可以帮助我们更好地根据业务需求选择适合的模式。

## NVM内存的特性与使用模式

Redis是基于DRAM内存的键值数据库，而跟传统的DRAM内存相比，NVM有三个显著的特点。

首先，**NVM内存最大的优势是可以直接持久化保存数据**。也就是说，数据保存在NVM内存上后，即使发生了宕机或是掉电，数据仍然存在NVM内存上。但如果数据是保存在DRAM上，那么，掉电后数据就会丢失。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/11/ba/2175bc50.jpg" width="30px"><span>Mr.Brooks</span> 👍（29） 💬（3）<div>使用NVM，没有了RDB，主从复制对于新添加的机器，是怎么实现的呢</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（19） 💬（1）<div>老师，比较好奇应用程序是如何基于持久化内存来恢复自身的状态的，还是说应用程序本身也作为持久化的一部分，在重启后就存在于内存中？</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/99/5e/33481a74.jpg" width="30px"><span>Lemon</span> 👍（8） 💬（2）<div>肯定还是需要的，两者是互补的。

NVM 给了数据存储方面的新方案，但目前用作 PM 的读写速度比 DRAM 慢，不使用主从集群仍会有明显的访问瓶颈。【过大的实例在主从同步时会有影响（缓存、带宽）】

而集群是为了高可用，分散了数据的访问和存储，便于拓展与维护。对于单实例而言，即便单实例恢复的再快，挂了对业务仍会有影响。

感觉 NVM 内存用作 PM 有点像第 28 将的 Pika，如果把 SSD 换为 NVM ，岂不是都再内存中操作？是否可以解决 Pika 操作慢的缺点？</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/34/891dd45b.jpg" width="30px"><span>宙斯</span> 👍（7） 💬（1）<div>需要。主从集群 1读写分离，降低实例压力 2数据冗余，防止介质损坏数据丢失</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/95/bb237f51.jpg" width="30px"><span>李梦嘉</span> 👍（7） 💬（2）<div>老师，请问有AEP方案redis的最佳实践么，最近在调研这方面</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（4） 💬（1）<div>问题：有了持久化内存，是否还需要 Redis 主从集群？
解答：需要，主从集群解决的单点故障问题，而且还能起到一定的负载分担。而NVM解决的是数据丢失</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/f9/75d08ccf.jpg" width="30px"><span>Mr.蜜</span> 👍（1） 💬（2）<div>由于PM的读写速度存在差异，使用读写分离的主从集群，还是有必要，这样可以分担单实例的处理压力，提升redis整体的性能，所以使用主从集群还是非常有必要的。</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（114） 💬（5）<div>有了持久化内存，是否还需要 Redis 主从集群？

肯定还是需要主从集群的。持久化内存只能解决存储容量和数据恢复问题，关注点在于单个实例。

而 Redis 主从集群，既可以提升集群的访问性能，还能提高集群的可靠性。

例如部署多个从节点，采用读写分离的方式，可以分担单个实例的请求压力，提升集群的访问性能。而且当主节点故障时，可以提升从节点为新的主节点，降低故障对应用的影响。

两者属于不同维度的东西，互不影响。</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/8f/77b5a753.jpg" width="30px"><span>好好学习</span> 👍（17） 💬（1）<div>终于学完了。 我真棒！</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（4） 💬（0）<div>请问蒋老师，Redis将PM用作内存模式的话，是否需要修改Redis代码。我理解内存模式是对程序透明的，虽然PM可以把数据持久化保存，但是如果Redis进程把它看做内存，如果希望进程启动能够自动回复，就会涉及到进程内存空间的恢复，OS里是没有这个功能的，是不是应该需要Redis来做个事情，才可以直接从PM保存的上一次数据中作为新进程的内存空间，而不再需要通过RDB或者AOF来做数据持久化？</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（2） 💬（0）<div>老师好，关于mmap映射的问题，没看明白，有几点不清楚，还望帮忙解答：
1、将redis内存空间，用mmap映射到PM的ext系统文件后，保持的就是内存信息吧？那进程信息、线程信息、寄存器状态什么的，需要额外保持吗？
2、redis挂掉后，重新启动要如何做呢？
3、操作系统重启动后，再启动redis时，还能用这个持久化后的文件吗？要如何做呢？
4、用集群的时候，节点间复制要如何做呢？
感谢！</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（1） 💬（0）<div>主从集群仍旧需要。
单机失踪了持久化内存只能解决单机的存储容量和数据恢复问题。
主从集群可以提高访问速度，提高可靠性，做到HA。</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/ab/fd201314.jpg" width="30px"><span>小耿</span> 👍（0） 💬（0）<div>有了持久化内存后，还需要 Redis 主从集群吗?
我认为需要，主从集群保障了 redis 服务的高可用。当某个redis实例宕机以后，即使使用持久化内存，也需要时间恢复，恢复期间无法对外提供服务。因此还需要主从集群保障 redis 能持续对外提供服务。</div>2023-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（0）<div>需要主从集群。NVM再厉害，依然会有单点故障，另外单实例的处理效率也是有限的。对于大业务量的业务场景，横向扩容的能力是必须的。</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/7e/ebc28e10.jpg" width="30px"><span>NULL</span> 👍（0） 💬（0）<div>关于dram, nvm, ssd的区别, 可以看下Intel Optane AEP的介绍, 在1:18秒处 https:&#47;&#47;www.intel.cn&#47;content&#47;www&#47;cn&#47;zh&#47;architecture-and-technology&#47;optane-dc-persistent-memory.html</div>2022-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>gpu 内存可以加速redis性能吗？</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>nvm后还要记内存日志更好，一些操作执行到中间步骤的时候失败了，重启之后要有办法回滚。</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>解决主从一致性的问题，redis就可以当个分布式db了</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7b/62/ec94cee4.jpg" width="30px"><span>小彭</span> 👍（0） 💬（0）<div>完结撒花</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/8c/d9330d2b.jpg" width="30px"><span>花儿少年</span> 👍（0） 💬（0）<div>NVM 也是有些缺陷的，也可能会导致数据不一致。例如，在redis的新增一个数据节点，那么会有两步操作，1、分配内存，写入数据；2、将此内存地址的指针指向redis管理；而这两步我们知道在很多情况下都可能是乱序执行的，如果第二步先执行，此时机器crash了，redis就指向了一个无效地址。</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>单机版的Redis必然存在着实例服务器宕机的问题,那么Redis主从集群必然有存在的需求
不过有了NVM,使用K8S直接管理也是可以的,毕竟绑定了固定的volume,也可以保证持久化和自动重启</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>从高可用角度考虑，主从集群还是非常必要，
NVM只是解决读写性能，可持久存储，只要是硬件也需要考虑坏的可能。
Redis数据需要备份，还是要做足工作的</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>有一点好奇，NVM 内存在 Memory 模式下，为什么还需要 DRAM 来做缓存？

使用 App Direct 模式，将 Redis 运行在持久化内存（Persistent Memory, PM）上，不需要额外的 RDB 或者 AOF，那岂不是要快的飞起？

有一个疑问，Redis 原本的优势建立在内存访问速度上，如果有了 NVM 内存，那么其他的数据库或者 KV 数据库也会变得比较快，Redis 的优势可能就没那么大。

对于课后题，有了持久化内存，应该还是需要 Redis 主从集群的，一方面可以读写分离，分散支撑高性能读写需求；另外一方面，主从集群也可以提高系统的可靠性。

有同学在留言里提到了 Pika，这个确实可以在 NVM 上。</div>2021-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/8e/8a39ee55.jpg" width="30px"><span>文古</span> 👍（0） 💬（0）<div>老师您好，redis多路利用模式epoll创建fd的时候为什么只创建1024个，难道为了跟select兼容吗？这不是降低epoll的效率</div>2020-12-14</li><br/><li><img src="" width="30px"><span>dfuru</span> 👍（0） 💬（0）<div>主从集群功能：
1. 保证数据的可靠性；
2. 保障业务的可用性。及时用了PM后，当发生宕机，仍然需要主从切换，保证业务可用。</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/86/e3/a31f6869.jpg" width="30px"><span> 尿布</span> 👍（0） 💬（1）<div>pika</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/3b/f0/0dd9ca93.jpg" width="30px"><span>林林要加油鸭</span> 👍（0） 💬（0）<div>沙发！</div>2020-11-25</li><br/>
</ul>