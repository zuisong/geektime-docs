在Java领域，实现并发程序的主要手段就是多线程，使用多线程还是比较简单的，但是使用多少个线程却是个困难的问题。工作中，经常有人问，“各种线程池的线程数量调整成多少是合适的？”或者“Tomcat的线程数、Jdbc连接池的连接数是多少？”等等。那我们应该如何设置合适的线程数呢？

要解决这个问题，首先要分析以下两个问题：

1. 为什么要使用多线程？
2. 多线程的应用场景有哪些？

## 为什么要使用多线程？

使用多线程，本质上就是提升程序性能。不过此刻谈到的性能，可能在你脑海里还是比较笼统的，基本上就是快、快、快，这种无法度量的感性认识很不科学，所以在提升性能之前，首要问题是：如何度量性能。

度量性能的指标有很多，但是有两个指标是最核心的，它们就是延迟和吞吐量。**延迟**指的是发出请求到收到响应这个过程的时间；延迟越短，意味着程序执行得越快，性能也就越好。 **吞吐量**指的是在单位时间内能处理请求的数量；吞吐量越大，意味着程序能处理的请求越多，性能也就越好。这两个指标内部有一定的联系（同等条件下，延迟越短，吞吐量越大），但是由于它们隶属不同的维度（一个是时间维度，一个是空间维度），并不能互相转换。

我们所谓提升性能，从度量的角度，主要是**降低延迟，提高吞吐量**。这也是我们使用多线程的主要目的。那我们该怎么降低延迟，提高吞吐量呢？这个就要从多线程的应用场景说起了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/d9/d74e4c61.jpg" width="30px"><span>假行僧</span> 👍（78） 💬（5）<div>个人觉得公式话性能问题有些不妥，定性的io密集或者cpu密集很难在定量的维度上反应出性能瓶颈，而且公式上忽略了线程数增加带来的cpu消耗，性能优化还是要定量比较好，这样不会盲目，比如io已经成为了瓶颈，增加线程或许带来不了性能提升，这个时候是不是可以考虑用cpu换取带宽，压缩数据，或者逻辑上少发送一些。最后一个问题，我的答案是大部分应用环境是合理的，老师也说了是积累了一些调优经验后给出的方案，没有特殊需求，初始值我会选大家都在用伪标准</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/6a/38a3fa8d.jpg" width="30px"><span>多拉格·five</span> 👍（54） 💬（3）<div>问一下老师，这个线程配置比我在其他的资料也看过，但是最后那个公式没见过，方便说一下如何测试IO&#47;CPU 这个耗时比例吗</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/71/e8229703.jpg" width="30px"><span>aksonic</span> 👍（47） 💬（1）<div>早起的鸟果然有食吃，抢到了顶楼，哈哈。
对于老师的思考题，我觉得不合理，本来就是分CPU密集型和IO密集型的，尤其是IO密集型更是需要进行测试和分析而得到结果，差别很大，比如IO&#47;CPU的比率很大，比如10倍，2核，较佳配置：2*（1+10）=22个线程，而2*CPU核数+1 = 5，这两个差别就很大了。老师，我说的对不对？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b7/15/6a2b6b83.jpg" width="30px"><span>董宗磊</span> 👍（43） 💬（2）<div>思考题：认为不合理，不能只考虑经验，还有根据是IO密集型或者是CPU密集型，具体问题具体分析。
看今天文章内容，分享个实际问题；我们公司服务器都是容器，一个物理机分出好多容器，有个哥们设置线程池数量直接就是：Runtime.getRuntime().availableProcessors() * 2；本来想获取容器的CPU数量 * 2，其实Runtime.getRuntime().availableProcessors()获取到的是物理机CPU合数，一下开启了好多线程 ^_^</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（32） 💬（1）<div>理论加经验加实际场景，比如现在大多数公司的系统是以服务的形式来通过docker部署的，每个docker服务其实对应部署的就一个服务，这样的情况下是可以按照理论为基础，再加上实际情况来设置线程池大小的，当然通过各种监控来调整是最好的，但是实际情况是但服务几十上百，除非是核心功能，否则很难通过监控指标来调整线程池大小。理论加经验起码不会让设置跑偏太多，还有就是服务中的各种线程池统一管理是很有必要的</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（18） 💬（7）<div>老师早上好，当应用来的请数量过大，此时线程池的线程已经不够使用，排队的队列也已经满了，那么后面的请求就会被丢弃掉，如果这是一个更新数据的请求操作，那么就会出现数据更新丢失，老师有没有什么具体的解决思路？期待解答</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（17） 💬（1）<div>在4核8线程的处理器使用Runtime.availableProcessors()结果是8，超线程技术属于硬件层面上的并发，从cpu硬件来看是一个物理核心有两个逻辑核心，但因为缓存、执行资源等存在共享和竞争，所以两个核心并不能并行工作。超线程技术统计性能提升大概是30%左右，并不是100%。另外，不管设置成4还是8，现代操作系统层面的调度应该是按逻辑核心数，也就是8来调度的（除非禁用超线程技术）。所以我觉得这种情况下，严格来说，4和8都不一定是合适的，具体情况还是要根据应用性能和资源的使用情况进行调整。这是个人的理解，请老师指正。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（11） 💬（1）<div>我就想问下如何测试io耗时和cpu耗时</div>2019-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epLhKkTgowm9PqUwP9k90DecpOU7HQ0IRuAp515kIonbfyqYm6ME7s2bmaPX0sSA14micZ2DAfLLibw/132" width="30px"><span>zsh0103</span> 👍（7） 💬（1）<div>请问老师，
1 在现实项目如何计算I&#47;O耗时与CPU耗时呢，比如程序是读取网络数据，然后分析，最后插入数据库。这里网络读取何数据库插入是两次IO操作，计算IO耗时是两次的和吗？
2. 如果我在一台机器上部署2个服务，那计算线程数是要每个服务各占一半的数量吗？
3. 如果我用一个8核CPU的机器部署服务，启动8个不同端口的相同服务，和启动一个包含8个线程的服务在处理性能上会有区别吗？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/13/6c/08b8829d.jpg" width="30px"><span>已忘二</span> 👍（6） 💬（10）<div>老师，有个疑问，就是那个I&#47;O和CPU比为2:1时，CPU使用率达到了100%，但是I&#47;O使用率却到了200%，也就是时刻有两个I&#47;O同时执行，这样是可以的么？I&#47;O不需要等待的么？</div>2019-03-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKg7RjNMzSrIwUnjYstbdicVv5MawrQLTHc6rdpwm0Q04b7icj7eAb0F8zSxe8gmM99QBvTECK5KvrQ/132" width="30px"><span>阿冲</span> 👍（6） 💬（3）<div>老师，你好！有个疑惑就是我在写web应用的时候一般都是一个请求里既包含cpu计算（比如字符串检验）又包含操作（比如数据库操作），这种操作就是一个线程完成的。那么这种情况按你写的这个公式还起作用吗？c#里面有对io操作基本都封装了异步方法，很容易解决我刚说的问题(调用异步方法就会切换线程进行io操作，等操作完了再切回来)。java要达到这种效果代码一般怎么写比较合适？</div>2019-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjRETqRjvLESLDZkNTjIiaSibtNYBaS1o8WMUicOFn3ycF3Mgh6LRJibqSBjVBjiaO2ibW0gHkafATb21A/132" width="30px"><span>lmdcx</span> 👍（5） 💬（1）<div>我有个疑惑哈，老师的算法都是以 CPU 核数为参数，但是在硬件上有这种情况：
比如Intel 赛扬G460是单核心，双线程的CPU，
Intel 酷睿i3 3220是双核心 四线程，
Intel 酷睿i5 4570是四核心 四线程，
Intel 酷睿i7 4770K是四核心 八线程 等等
这个对那个算法有影响吗？
还有就是线程让出CPU内核 时，他的数据是要刷新到内存中保存吗？（我不是想要挑刺啊，我是觉得这个和前面讲的可见性应该有关系，比如单核多线程是不是不会有可见性的问题？当然只要是单线程不管多少核则定没有可见性的问题）
@董宗磊 提到了 availableProcessors ，这个我看文档写的是获得可用的Java虚拟机的可用的处理器数量，和实际的主机 CPU 核数不是一致的吧，先忽略 docker 的问题，它可以用作算法中的 CPU核数吗？（我对“可用”俩字也很迷惑，难道这个数量会动态变化吗？）</div>2019-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EmXS3Kmby5usibRic8rPzFoVhk2mGmQHm5pvsuF9e5dILLffm1VqZEK6CnLuamBhxdrFdyR211zXqmRPZ3aQiaygw/132" width="30px"><span>JSON</span> 👍（3） 💬（1）<div>一个java实例应用中可以使用多个TreadPoolExcutor线程池吗？以避免不同的业务都阻塞在一个线程池中，那么有多个线程池的话，每个TreadPoolExcutor参数中的核心线程和最大线程，该如何设置呢？
还有就是一个java的应用实例，dump 当前的jvm日志，都会有上千的线程在运行，并不满足2*CPU核数，这个对性能有影响吗？</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/1a/79b052df.jpg" width="30px"><span>Weixiao</span> 👍（3） 💬（3）<div>最佳线程数 =1 +（I&#47;O 耗时 &#47; CPU 耗时），

文中说，1表示一个线程执行io，另外R个线程刚好执行完cpu计算。

这里理解有点问题，这个公式是按照单核给出的，所以不可能存在同时R个线程执行cpu计算。所以我理解文章中说反了，应该是1个线程在执行cpu，然后有R个线程可以同时在执行io，这样cpu的利用率为100%</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（3） 💬（1）<div>老师我记得csapp那本书中说过，x86架构的CPU是拥有超程技术的，也就是一个核可以当成两个使用，AMD的却没有，不知道您的这个计算公式是否适合其它厂商的CPU呢？</div>2019-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroydkGP6m3OsQ8QuI4jAibv21tNkm7KVGPffJibj8Y29yIdKl4qkDGd3iaGJCSGVarfxoibQ/132" width="30px"><span>狂战俄洛伊</span> 👍（3） 💬（1）<div>对于这个思考题，我觉得是比较合理。
因为经验是经过大量实践的结果，是符合大多数的情况，而且是一种快速估计的方法。
我看留言区里很多都说不合理，并且给出了例子。我觉得他们说的也没错，只是举出了经验没覆盖到的情况而已。
这里我还有个疑问，这篇文章中都是在讲一台机器工作的情况下。我想问的是如果是在一个集群里，这个线程数又该怎么计算？
例如有三台机器构成一个集群，这三台机器的cpu分别是8核，4核，2核。就打算是cpu密集型，这时候该怎么计算线程数？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/eb/30864e40.jpg" width="30px"><span>漂泊者及其影子</span> 👍（2） 💬（1）<div>对于网关这种服务，io时长和cpu时长的比例可能是99:1 ,那一个8核的网关服务的线程数是配置成8*（99+1）=800？</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/2f/2f73fd52.jpg" width="30px"><span>水滴s</span> 👍（2） 💬（1）<div>老师，您好 问下IO操作可以并行进行吗？按照上述这个公式：最佳线程数 =1 +（I&#47;O 耗时 &#47; CPU 耗时），假设I&#47;O耗时&#47;CPU耗时是4，最佳线程数是5，那么在运行的过程中，CPU利用率理论上的确是100%，但是会存在某一个时间段同时进行多个IO操作？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/9d/e20b37d7.jpg" width="30px"><span>机遇号</span> 👍（2） 💬（1）<div>实际项目中怎么确定IO耗时、CPU耗时？</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/15/ad1d202c.jpg" width="30px"><span>纽扣</span> 👍（1） 💬（2）<div>“我们令 R=I&#47;O 耗时 &#47; CPU 耗时，综合上图，可以这样理解：当线程 A 执行 IO 操作时，另外 R 个线程正好执行完各自的 CPU 计算。这样 CPU 的利用率就达到了 100%。”

老师您好，请问：如果 IO耗时 : CPU耗时=R : 1，说明IO更加耗时，那不应该R条线程去处理IO，一条处理CPU更快吗？为什么反过来了呢？</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（1） 💬（1）<div>老师你好，在CPU密集型的最佳线程数公式为：CPU核数+1，但是如果线程没有发生阻塞，那么多出来这个1不就会造成上下文切换的开销了吗？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/5e/ddbdde5a.jpg" width="30px"><span>邢宇超</span> 👍（1） 💬（1）<div>老师你说 堆栈寄存器指向栈顶内存地址 
我记得程序计数器是干这事的  
堆栈寄存器和程序计数器有关系不 老师</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1b/2c/6b3c0911.jpg" width="30px"><span>Hour</span> 👍（1） 💬（1）<div>老师好，再次回顾这片文章，发现个问题：
任务切换是如何控制的？这些线程执行的任务都是相同的，比如都是先从数据库中获取数据(IO操作)，再从进行分析(CPU操作)。这个顺序不可逆的。
那CPU是如何准确的切换，让线程A执行IO操作的同时，线程B和线程C执行CPU操作呢？</div>2019-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1c/d5/248a9c38.jpg" width="30px"><span>你只是看起来很努力</span> 👍（1） 💬（2）<div>假设4核，i&#47;o耗时：cpu耗时=8:3
按经验来算：2*4+1=9
按工式来算：4（1+8&#47;3）=15
差距有点大
老师，这个线程数与cpu线程数没关系么，比如说4核8线程的cpu与4核的cpu最佳线程数是一样的？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/40/2c4ba425.jpg" width="30px"><span>IMSolar</span> 👍（1） 💬（1）<div>“最佳线程数 =1 +（I&#47;O 耗时 &#47; CPU 耗时） 
我们令 R=I&#47;O 耗时 &#47; CPU 耗时，综合上图，可以这样理解：当线程 A 执行 IO 操作时，另外 R 个线程正好执行完各自的 CPU 计算。这样 CPU 的利用率就达到了100%。”

假设线程A和线程B同时开始IO操作，而且线程C开始CPU计算，当线程C计算结束的时候，线程A和线程B的IO操作还没有结束，这样的话50%的CPU是不是被浪费了？是不是还差一条线程接上CPU呢？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/99/f886543d.jpg" width="30px"><span>渔夫</span> 👍（1） 💬（1）<div>对于I&#47;O密集型应用，工程上一般会区分I&#47;O请求响应线程和工作线程的话，而前者的线程池大小——按照Hikari推荐的——比较好数量是: 核数*2+1，因为前者可以进行I&#47;O多路复用，请问老师这个事情是否是这么理解的？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/03/89/e1621a01.jpg" width="30px"><span>zhangtnty</span> 👍（1） 💬（1）<div>王老师，我对问题的理解：没有考虑各自耗时情况。如果核数越多，I&#47;O耗时越大，会造成CPU多核都在I&#47;O中执行，影响了延时和吞吐量。
另外想请教个问题：近期工作需要调用三方接口，需要组织参数，调用，响应处理。如果考虑2种耗时来设置多线程数量，I&#47;O耗时和CPU耗时该如何划分呢？辛苦老师。</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/f4/ce6acfc0.jpg" width="30px"><span>NARUTO</span> 👍（0） 💬（1）<div>怎么知道IO耗时与CPU耗时的比值是多少？否则这公式也没法套用</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/93/124d8cd8.jpg" width="30px"><span>努力努力再努力</span> 👍（0） 💬（1）<div>有个疑问，如果是cpu密集型 4核心的话，就设置4个线程吗，tomcat正常运行下不是都200个线程最大吗😥😥那是不是得将tomcat的线程改成4才对</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/0d/00424e81.jpg" width="30px"><span>到道可道</span> 👍（0） 💬（1）<div>个人认为这个经验值有一定的合理性，如果是程序首次运行，可以将线程数设置为这个经验值，以得到比较好的运行效果；不过运行一段时间后，能够根据工具（如apm等）分析得出I&#47;O耗时&#47;CPU耗时的比值，则应该采用更优化的线程数设置（最佳线程数 =CPU 核数 * [ 1 +（I&#47;O 耗时 &#47; CPU 耗时）]）。</div>2021-09-08</li><br/>
</ul>