在当今Spring Cloud微服务架构盛行的时代，Tomcat仍然作为应用最广的应用服务器而存在着，所以我们不得不说一说对它的性能分析。

很多时候，我们做性能测试分析时，都会把Tomcat这类的应用弄混淆。对它的监控和分析，总是会和JDK、框架代码、业务代码混合来看，这就导致了分析上的混乱。我们应该把这些分析内容分隔开来，哪些是tomcat，哪些是JDK等。

在我看来，Tomcat、WebLogic、WebSphere、JBoss等，它们都具有同样的分析思路。因为Tomcat的市场范围更大，所以，今天，我们以它为例来说明这类应用应该如何分析。

首先我们得知道它的架构是什么样的。

![](https://static001.geekbang.org/resource/image/bb/10/bb22a5bea7abe133a8db73e2fe311f10.jpg?wh=1650%2A1123)

这是一个在网上随处可见的架构图，它能告诉我们Tomcat内部如何运作。如果你有兴趣，还可以看一下官方对它的架构描述。

然而，我们做性能分析的人真的要完全掌握这些细节吗？当然不是。从经验上来说，基本上有几大方面，是Tomcat优化时需要关注的。

如下图所示：

![](https://static001.geekbang.org/resource/image/c1/90/c1c6e4a479c53a3365cbffe476ab6090.png?wh=1353%2A904)

最上面，我放了两个框，分别是操作系统和JDK。因为要调优Tomcat，和这两者非常相关，但是操作系统和JDK又各自有独立的分析逻辑，而在本篇中，我专门讲Tomcat类型的组件，所以上面两块的内容我将尽量不涉及，以免混乱。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGXndj5N66z9BL1ic9GibZzWWgoVeWaWTL2XUnCYic7iba2kAEvN9WfjmlXELD5lqt8IJ1P023N5ZWicg/132" width="30px"><span>Geek_f93234</span> 👍（11） 💬（2）<div>1.如何判断代码快不快，我的理解是，压力工具中的线程数设置低于中间件的线程数，看看测试过程中服务器返回响应是否足够快
2.如何判断应用服务器线程是否够用？
测试过程中应用监控工具如jvisualvm监控线程同一时刻是否有空闲状态，如果一直是run那able状态，同时响应时间不断增加，说明线程数不够用
3.类似 Tomcat 的应用服务器，应该如何拆解监控计数器呢？
从以下几个方面的计数器来分析：协议（http,https）,运行模式（BIO,AIO,APR），线程池；超时时间，压缩，TCP不延迟，禁用DNS查询，禁用AJP
</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/90/807689c3.jpg" width="30px"><span>Geek_9ius3m</span> 👍（7） 💬（2）<div>老师教案中的NIO和AIO没看懂，图中poller的画着是NIO，下面的文字又说成AIO了。是说两个的原理都是基于poller吗</div>2020-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiabrzic7IeQJGzicQDzyiaXkD3kY1E4rzXnU5XChibwSyvqqqnUpDMEtVv1BjjYQ8ZKD7k7KQJBhib0zg/132" width="30px"><span>ldm</span> 👍（2） 💬（1）<div>高老师，你好，想请问下，压力线程和服务器线程的区别？看了文章后有点弄不清楚了。并发用户数理解的意思是在同一时间点对同一事务做同一个操作的用户数；压力线程数是指的压力工具上配置的vuser数？服务器线程数是指tomcat上配置的maxthreads数吗？</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（2）<div>1，如何判断问题是Tomcat发生还是自己写的代码发生的。2，tomcat的log日志太多，会影响性能的吧？3，JBoos、Weblogic是不是自身性能会更好？</div>2020-02-25</li><br/><li><img src="" width="30px"><span>信大捷安</span> 👍（0） 💬（1）<div>高老师好，%D 就是请求时间，%F 是响应时间这两个不太明白，可以详细解释一下吗？</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>我需要说明的是，以下场景均基于以下配置：acceptCount=“10000”。这个值对我们来说，也是非常关键的数据，因为它影响着 KeepAlive 的超时和 connection 的超时。我们在性能分析的时候，会遇到一种情况是，很多应用都用默认超时，而在压力大的时候，会有少量的报错是因为前端的超时已经到了，而后端还没到，因为毕竟后端是后接收到的请求。这就导致了大压力下少量的错误是因为超时配置导致的。</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/eePa5cW5DNLD2iaIgcSe545dZib4aOYCHouHsF7hQ42bPVibHPk1VibZT7HOuwReBIYX3qUxnl0ojKQ8TQ5HI83Log/132" width="30px"><span>Geek_13df3b</span> 👍（0） 💬（2）<div>高老师，请问执行压测前服务器的内存使用率30%，对服务器持续加压后，内存使用率升到80%，压测结束后，内存使用率一直保持在80%左右，不会将下来。这是正常的吗？该如何排查，请您指导下，感谢了
</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/72/8f77ddb0.jpg" width="30px"><span>johnny</span> 👍（0） 💬（1）<div>应该如何拆解监控计数器呢？
根据对性能指标影响程度，最重要的三类计数器为协议、运行模式（用默认的就行）、线程池，线程池下的几个重要的计数器为maxThreads、minSpareThreads、maxSpareThreads、acceptCount。
我们应该如何判断应用服务器的线程是否够用？
可以通过jvisuavlvm工具查看线程是否忙碌来判断。
另外根据“服务端能处理的压力线程必然不会超过自身的线程上限”这句话，从服务器线程是否够用的角度来看，将tomcat的线程数设置为大于或者等于压力机线程数，一般是够用的，但是也要根据硬件资源情况而定，不能盲目增大tomcat线程数,比如将tomcat线程设置为4000。
我的回答正确吗？
我有个问题，老师所说的“计数器”的概念是不是就是指的tomcat的配置参数（acceptCount、maxThreads、minSpareThreads等）呢？</div>2021-06-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKbt3JKCxyeRvkfXMSlkbHlwFqPjXw5kZAXxzKhC8aRtNUyUl7nfmMdnZh88oibfOChuNPCODPMyibQ/132" width="30px"><span>陈诚</span> 👍（0） 💬（1）<div>疑问：
1、设置不同的压力线程，对服务器来讲压力不同，势必响应时间会有不同，这如何判断是代码运行快慢的问题呢？
麻烦老师解疑，谢谢</div>2021-05-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIPaILq1Tq7aEhULkMl6W4icECiaqWINRmZwPe3ctQDKHNAbmfruT3jdM2raR03p3Loc0nekBKJf4RA/132" width="30px"><span>sunny</span> 👍（0） 💬（1）<div>操作系统的CS，CS指的是什么呢</div>2021-05-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ibaGFsFicWRKlUjhGsw4ibm9eGLQHrmlwxia1W28yqDUNbao2YD1icAQ07ux3mDZviaZACicsicoibrCndCV1kStN3PuPYw/132" width="30px"><span>Geek_65c0a2</span> 👍（0） 💬（1）<div>精华呀，有理有据。</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>以下场景均基于以下配置：acceptCount=“10000”。</div>2021-12-20</li><br/>
</ul>