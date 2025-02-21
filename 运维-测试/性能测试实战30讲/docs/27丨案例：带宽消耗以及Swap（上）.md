今天我们来看一个真实的案例。事情是这样的，之前有人在微信上问我一个问题，这个问题的现象很典型：典型的TPS上不去，响应时间增加，资源用不上。

大概的情况是这样的：有两台4C8G的服务器，一台服务器上有2个Tomcat，一台服务器上是DB。压测的混合场景有4个功能模块，其中3个访问一个Tomcat，另外一个访问一个Tomcat。

Tomcat的监控页面如下：

![](https://static001.geekbang.org/resource/image/53/0b/532bbd1525be0ad0d08da7335645260b.png?wh=882%2A262)

应用服务器系统资源监控页面如下：

![](https://static001.geekbang.org/resource/image/19/e5/1944bc692902fed979815a538d879be5.png?wh=892%2A687)

数据库服务器系统资源监控如下：

![](https://static001.geekbang.org/resource/image/50/f0/50a996ac196dbfd2b9a23858e87dc8f0.png?wh=1174%2A745)

JMeter结果如下：

![](https://static001.geekbang.org/resource/image/f8/33/f8b228a61b980c338046fbb3c8875033.png?wh=1099%2A219)

综上现象就是，单业务场景执行起来并不慢，但是一混合起来就很慢，应用服务器和数据库服务器的系统资源使用率并不高。请问慢在哪？

这是非常典型的询问性能问题的方式，虽然多给了系统资源信息，但是这些信息也不足以说明瓶颈在哪。

为什么呢？在现在多如牛毛的监控工具中，除非我们在系统中提前做好分析算法或警告，否则不会有监控工具主动告诉你， 监控出的某个数据有问题，而这个只能靠做性能分析的人来判断。

我在很多场合听一些“专家”说：性能分析判断要遵守木桶原理。但是在做具体技术分析的时候，又不给人说明白木桶的短板在哪里。这就好像，一个赛车手说要是有一个各方面都好的车，我肯定能得第一名，但是，我没有车。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/3f/3b/119fd0ef.jpg" width="30px"><span>土耳其小土豆</span> 👍（14） 💬（1）<div>高老师，网络队列的截图的具体命令能告知以下嘛？我想打印跟你那一样的</div>2020-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/aCVlj0fom8geRoXFkO34Jbpf9oia79QxdbwDuyyLqL1WAVC7iaViaE4YNUvcatEwwUF6102MeH6kBxo5CwLibrCiajg/132" width="30px"><span>Geek_9e9d56</span> 👍（5） 💬（1）<div>高老师，应用和数据库服务器带宽截图的具体命令能否告知一下？谢谢</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/46/ed/a7cb8b2a.jpg" width="30px"><span>Geek_Jean</span> 👍（4） 💬（1）<div>高老师，谢谢您给大家分享这么多的干货，真的受益非浅，但看完这讲后，我有3个问题没明白：
1. 我有这样一个认知：服务端Send-Q如果有积压，那实时查看网络带宽的时候服务端的发送量和客户端的接收量不会对等。这个认知对吗？
如果上面说的是对的，那我又有一个新问题：
服务端网络资源接收 900KB&#47;s 左右，发送 11M 左右；然后通过查看压力机上的网络接收流量可以看到是93Mbps，换算之后也就是11M左右,
这么看服务端的发送量和客户端的接收量是一样的，带宽是对得上的。依据这样的推断服务端的Send-Q应该不会有积压才对。这个怎么理解呢？
如果上面的认知不对：那我有另外一个新问题：
实时查看服务端的时候Send-Q都有积压了，那说明这些数据还没有到达客户端，那客户端的接收量就不会接近服务端的发送量了。但实际上他们都是93Mbps.这是怎么回事呢？</div>2021-09-02</li><br/><li><img src="" width="30px"><span>Geek_237b86</span> 👍（4） 💬（1）<div>老师swapping标黄的是什么工具？</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/7c/cc192a8c.jpg" width="30px"><span>糯糯</span> 👍（3） 💬（1）<div>老师 有个问题，如果说要找到系统上限，是找到系统瓶颈呢，还是尽可能的压测至服务器资源沾满呢</div>2021-04-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epFQPMPrP3V6HhlGLPp0JKMiaHQDibFKnE7z8To27tYEH42XvvmmQGyYvL4CK1lLJBIUAw7jtBnezibA/132" width="30px"><span>bettynie</span> 👍（3） 💬（1）<div>高老师，我们做内网测试时采用直连的方式，是不是可以更好的避免内网的网络问题，只考虑网卡的限制，这样可以把精力放在程序本身，先找出比较严重的性能问题再来考虑网络影响？</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/72/72a8bcfd.jpg" width="30px"><span>大拇哥</span> 👍（2） 💬（1）<div>1）查看服务器发包数量，客户端接口数据包的量是不基本一致，如果出现明显的差别，可以基本确定客户端网络问题
2）查看jmeter聚会报告上面客户端接口数据量是否已经接近宽带的限制
队列：
服务端消息发送队列
客户端接收数据的队列
服务端超时队列</div>2020-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLx577ko7FBh90vfSFM4oqSz8wFBW4ztau8PUxY18R7yKJnRD4WB4sF7ibOmlqBYAZqwNsEbWT6bbg/132" width="30px"><span>Geek_a8d2eb</span> 👍（1） 💬（1）<div>压测时在应用服务上执行命令netstat -naop，发现Recv-Q和send-Q都有间歇性的非0状态，5秒内就恢复0了。网上搜说可接受短暂的非0情况，短暂的Send-Q队列发送pakets非0是正常状态。请问这种说法靠谱么，观察tps和响应曲线也会出现相应的锯齿状</div>2021-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/60/95/ef2af905.jpg" width="30px"><span>😂</span> 👍（1） 💬（2）<div>老师，如何判断带宽不够呀？1.服务器接受和发送的流量接近或超过带宽，说明带宽不够？2.压力机接受和发送的流量接近或变过带宽，说明带宽不够？</div>2020-12-08</li><br/><li><img src="" width="30px"><span>nelson</span> 👍（1） 💬（1）<div>文稿中提及“综上现象就是，单业务场景执行起来并不慢，但是一混合起来就很慢，应用服务器和数据库服务器的系统资源使用率并不高。请问慢在哪？”
经过一系列分析，没有给出单业务为什么不慢，如果是带宽问题，单业务也一定会慢</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（1） 💬（1）<div>为什么同一个服务器，同一个环境，用Nmon监控，显示swap正常，page fault 也很小，用spotlight监控，swap就黄了，不科学啊。</div>2020-04-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIc8vg1BUJPaajoaylfCmicNGyj1ggoFtJwM86s5lZIicBIFAvOPuQ6u85n2xboHRQHG8ibHNgkRDUDA/132" width="30px"><span>Geek_454a8f</span> 👍（1） 💬（1）<div>tomcat使用什么监控的</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/34/6e3e962f.jpg" width="30px"><span>yayiyaya</span> 👍（0） 💬（1）<div>网络瓶颈的判断：
    简单的方法，就是在这段链路中传输大文件， 查看传输速率，判断带宽；
     如果带宽较大的情况下， 服务网络性能还是达到瓶颈，使用tcpdump  在两端进行抓包； 查看数据包是否存在乱序，重传、拥塞的情况（网络性能不佳的情况，往往会出现这样的现象）
</div>2023-07-18</li><br/><li><img src="" width="30px"><span>Geek_588072</span> 👍（0） 💬（1）<div>老师和同学好。
想请教一个简单的问题，&quot;应用服务器网络队列&quot;那张图的记录是用什么命令得到的？</div>2022-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/6c/18bf99bf.jpg" width="30px"><span>徐峥</span> 👍（0） 💬（1）<div>高老師，您好。查看发送和接收队列是否堆积的命令是什麽？</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cd/b3/4e518c2c.jpg" width="30px"><span>Allister🏅</span> 👍（0） 💬（1）<div>高老师，第一张资源监控（cpu，内存，网络等）用什么看的呢？</div>2021-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（1）<div>请问下，应用服务器上的 send-Q那个图，是应用listen状态还是非listen状态的截图？</div>2021-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLx577ko7FBh90vfSFM4oqSz8wFBW4ztau8PUxY18R7yKJnRD4WB4sF7ibOmlqBYAZqwNsEbWT6bbg/132" width="30px"><span>Geek_a8d2eb</span> 👍（0） 💬（2）<div>高老师，带宽分析那里没看懂，应用服务器发送约11MB，约等于88Mbqs。压力机接收的带宽是93Mbqs。怎么就是带宽的问题呢，发出的比接收的还小呀？</div>2021-02-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKlMfib72C2pyeiclc7U5ybwN0rVUMIwox8TcAjIjJKywfPIWSvyiaVpCFQccvaeSZ7M8Oko4EA09icrw/132" width="30px"><span>Geek_ed7255</span> 👍（0） 💬（1）<div>老师，内网和外网压测有什么区别</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/06/ab/ba20f342.jpg" width="30px"><span>餘生</span> 👍（0） 💬（2）<div>对于性能分析来说，带宽能不能对得上非常重要。比如，客户端接收了多少流量，服务端就应该是发出了多少流量。如果服务端发了很多包，但是客户端没有接收，那就是堵在队列上了。

关于这一段话，我想请问下，为什么没有提到客户端发出请求的流量大于服务端接收的情况？这种情况需要考虑吗？如果要考虑的话，通常会出现哪几种现象，要如何分析</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/36/fc9e80c4.jpg" width="30px"><span>啊啊</span> 👍（0） 💬（2）<div>单场景时网络的情况是怎样的？没想明白为什么单场景网络不是瓶颈？</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/23/46/d1d548d1.jpg" width="30px"><span>Melody</span> 👍（0） 💬（4）<div>老师，有一个问题想请教您，服务器使用的是容器，且做了负载均衡，在加压的过程中会报连接超时的错误，服务器cpu，内存，带宽都正常，压力机也未出现瓶颈，该如何分析？</div>2020-02-25</li><br/>
</ul>