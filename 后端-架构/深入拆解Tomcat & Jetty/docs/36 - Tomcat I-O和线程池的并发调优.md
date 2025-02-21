上一期我们谈到了如何监控Tomcat的性能指标，在这个基础上，今天我们接着聊如何对Tomcat进行调优。

Tomcat的调优涉及I/O模型和线程池调优、JVM内存调优以及网络优化等，今天我们来聊聊I/O模型和线程池调优，由于Web应用程序跑在Tomcat的工作线程中，因此Web应用对请求的处理时间也直接影响Tomcat整体的性能，而Tomcat和Web应用在运行过程中所用到的资源都来自于操作系统，因此调优需要将服务端看作是一个整体来考虑。

所谓的I/O调优指的是选择NIO、NIO.2还是APR，而线程池调优指的是给Tomcat的线程池设置合适的参数，使得Tomcat能够又快又好地处理请求。

## I/O模型的选择

I/O调优实际上是连接器类型的选择，一般情况下默认都是NIO，在绝大多数情况下都是够用的，除非你的Web应用用到了TLS加密传输，而且对性能要求极高，这个时候可以考虑APR，因为APR通过OpenSSL来处理TLS握手和加/解密。OpenSSL本身用C语言实现，它还对TLS通信做了优化，所以性能比Java要高。

那你可能会问那什么时候考虑选择NIO.2？我的建议是如果你的Tomcat跑在Windows平台上，并且HTTP请求的数据量比较大，可以考虑NIO.2，这是因为Windows从操作系统层面实现了真正意义上的异步I/O，如果传输的数据量比较大，异步I/O的效果就能显现出来。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（25） 💬（2）<div>猜测请求处理时间过长，应该增大线程池线程数量</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（7） 💬（1）<div>查看调用的服务是不是耗时太长</div>2019-08-03</li><br/><li><img src="" width="30px"><span>Geek_xbye50</span> 👍（8） 💬（1）<div>老师！第二种I&#47;O时间与CPU时间这两个指标如何查看？</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（5） 💬（0）<div>可能是线程池设置太小，可以先查看当前线程数，线程的状态(线程都在干嘛，是blocked还是wait&#47;time wait),然后去看为什么会这样，blocked是否发生了锁未释放，wait&#47;time wait是否是下游服务导致</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/ea/c8136dfd.jpg" width="30px"><span>草戊</span> 👍（3） 💬（0）<div>〈因此队列的长度等于新人加入队列的频率乘以平均每个人处理的时间。〉我觉得这句话有问题，举例说明，一分钟五个人加入排队，二分钟处理一个人，则按公式队列长度为十个人。假设过了十分钟，加入排队人数为50人，处理完人数为5人，队列还有45人则对。那么这个队列的长度，实际上指的是？应该是平均每分钟的到达队伍长度。
利特尔法则为：在一个稳定的系统中，长时间观察到的平均顾客数量L，等于长时间观察到的有效到达速率λ与平均每个顾客在系统中花费的时间之乘积，即L = λW</div>2019-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIHtJX5Qam0jNu6zlPX2CmR8QibdAd2c3R98Zh8HYiaVlHuVX1zk902Yy8KqnUyvnibiayEyEowiaw9Uw/132" width="30px"><span>芒夏</span> 👍（2） 💬（0）<div>Linux选择NIO，与操作系统有关，线程池压力测试寻找最优的最大线程数</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/4c/4e5e5721.jpg" width="30px"><span>月如钩</span> 👍（2） 💬（0）<div>需要排查下外部服务或者数据库连接</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（1） 💬（0）<div>程序如何统计io阻塞，cpu时间？
请求总时间是可以统计到。
那io阻塞的时间是调用数据库等io操作的时间？</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/11/a7/6ee3f556.jpg" width="30px"><span>Wx</span> 👍（0） 💬（0）<div>利特尔法则 =&gt; 考虑全部为`CPU`时间, 每秒请求数 × 平均请求处理时间, 计算需要最大的并发数;

CPU 时间与 I&#47;O 时间的比率 =&gt; 有限核心下, 根据`CPU 时间与 I&#47;O 时间的比率` 计算理论上能支持的最大并发数.</div>2024-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/3e/77c9b529.jpg" width="30px"><span>Sanhong</span> 👍（0） 💬（0）<div>先看看线程堆栈，看能不能看得到工作线程是否是卡到哪个方法上了</div>2024-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/16/99a7045d.jpg" width="30px"><span>倔强</span> 👍（0） 💬（0）<div>CPU使用率很低，cpu load很高，任务在排队，是不是可以直接调大tomcat线程数</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（0）<div>假如有个状况：系统响应比较慢，但 CPU 的用率不高，内存有所增加，通过分析 Heap Dump 发现大量请求堆积在线程池的队列中，请问这种情况下应该怎么办呢？

这种情况一般是磁盘 I&#47;O 获网络 I&#47;O 操作太慢了，或者是访问第三方接口太慢了。
1、可以先排查 I&#47;O 操作为什么慢，比如是否有慢 SQL，是否有大量的读写文件、是否有大量的网络操作或网络不畅通问题。
2、如果是第三方接口太慢了，可以先让第三方系统进行排查，如果第三方解决不了，再继续往下看。
3、如果这些请求不需要同步返回请求结果，那可以选用异步操作，引入消息队列进行解耦，线程池中的线程就可以将请求丢到消息队列，然后线程回收到线程池。
2、</div>2023-01-18</li><br/><li><img src="" width="30px"><span>知行</span> 👍（0） 💬（0）<div>一台机器上部署了多个应用，或者一个应用里有多个线程池，它们中的线程都会被cpu调度，这时候线程数又该怎么考虑呢</div>2022-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/eb/732e9707.jpg" width="30px"><span>青苹果</span> 👍（0） 💬（0）<div>课后题：这种基本就是堵在I&#47;O上，或者调用其他系统卡住了&#47;response太慢了</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cf/7d/d9085aaa.jpg" width="30px"><span>punnpkin</span> 👍（0） 💬（0）<div>讲的真好 要是再多点就好了</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>老师这里的minSpareThreads就是线程池中的核心线程数是吗?只不过minSpareThreads默认是也是会被超时回收的,而核心线程默认不被回收</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/78/23c56bce.jpg" width="30px"><span>james</span> 👍（0） 💬（0）<div>对于我们来说一台4c16g的ecs 部署6个springboot应用 除了tomcat 应用里面还有线程池 是不是基本就没法调了  我们目前都是用默认的，</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（0） 💬（0）<div>1、tomcat调优涉及io模型、各种池大小配置。io模型默认nio够用，如果使用tls加密且要求性能很高则可以选择apr连接器。线程池主要是maxthreadcount参数的设置了，可通过请求时间*请求处理时间确定线程数大小，或者通过io时间加上cpu时间除以cpu时间计算出。实际情况先估算出个最小值，然后压测再调整。
2、思考题：业务处理过慢</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/fe/1241bc83.jpg" width="30px"><span>水如天</span> 👍（0） 💬（0）<div>protected void stopCurrentThreadIfNeeded() {
        if (currentThreadShouldBeStopped()) {
            long lastTime = lastTimeThreadKilledItself.longValue();
            if (lastTime + threadRenewalDelay &lt; System.currentTimeMillis()) {
                if (lastTimeThreadKilledItself.compareAndSet(lastTime,
                        System.currentTimeMillis() + 1)) {
                    &#47;&#47; OK, it&#39;s really time to dispose of this thread

                    final String msg = sm.getString(
                                    &quot;threadPoolExecutor.threadStoppedToAvoidPotentialLeak&quot;,
                                    Thread.currentThread().getName());

                    throw new StopPooledThreadException(msg);
                }
            }
        }
    } 
请问老师，lastTimeThreadKilledItself.compareAndSet(lastTime,
                        System.currentTimeMillis() + 1) 这里为何需要+1呢？不理解</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（0） 💬（1）<div>老师请教一个问题   当线程阻塞  查数据库发生了全表扫描的时候  查数据库的线程是谁创建的  和tomcat的线程是不是一个线程。。。</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/78/4f0cd172.jpg" width="30px"><span>妥协</span> 👍（0） 💬（0）<div>阅读tomcat源码，有个地方不明白，NioEndpoint在处理感兴趣的IO事件时，在processKey函数中，调用了unreg(sk, attachment, sk.readyOps()); 这个不是在selector上取消了感兴趣感兴趣的事件吗？为何要这么处理？？tomcat源码版本8.5.38</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/76/4abc8ac1.jpg" width="30px"><span>完美世界</span> 👍（0） 💬（0）<div>线程阻塞或者下游服务响应时间过长，导致CPU处理变慢，响应时间过长。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/ea/c8136dfd.jpg" width="30px"><span>草戊</span> 👍（0） 💬（0）<div>刚才没编写完不小心发出去了。〈〉因此队列的长度等于新人加入队列的频率乘以平均每个人处理的时间。</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/ea/c8136dfd.jpg" width="30px"><span>草戊</span> 👍（0） 💬（0）<div>因此队列的长度等于新人加入队列的频率乘以平均每个人处理的时间。  这句话有问题吧。比如一分钟来五个人，每个人花费2分钟，按公式计算队列长度是10。实际上，十分钟时，总共来了5＊10=50人，总共处理了</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cf/97/fcd8957d.jpg" width="30px"><span>82</span> 👍（0） 💬（1）<div>老师好，如果请求数据相对比较大，但实际逻辑处理会很快完成，那么如何调优提高并发值呢？</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（0）<div>提高Tomcat最大线程数压榨CPU，优化程序降低响应时间，目测程序阻塞比较多。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>应该是最大池线程大小设置得过小导致的，具体原因还需要看性能监控和线程池参数配置。</div>2019-08-03</li><br/>
</ul>