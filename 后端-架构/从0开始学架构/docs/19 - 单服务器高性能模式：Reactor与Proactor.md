[专栏上一期](http://time.geekbang.org/column/article/8697)我介绍了单服务器高性能的PPC和TPC模式，它们的优点是实现简单，缺点是都无法支撑高并发的场景，尤其是互联网发展到现在，各种海量用户业务的出现，PPC和TPC完全无能为力。今天我将介绍可以应对高并发场景的单服务器高性能架构模式：Reactor和Proactor。

## Reactor

PPC模式最主要的问题就是每个连接都要创建进程（为了描述简洁，这里只以PPC和进程为例，实际上换成TPC和线程，原理是一样的），连接结束后进程就销毁了，这样做其实是很大的浪费。为了解决这个问题，一个自然而然的想法就是资源复用，即不再单独为每个连接创建进程，而是创建一个进程池，将连接分配给进程，一个进程可以处理多个连接的业务。

引入资源池的处理方式后，会引出一个新的问题：进程如何才能高效地处理多个连接的业务？当一个连接一个进程时，进程可以采用“read -&gt; 业务处理 -&gt; write”的处理流程，如果当前连接没有数据可以读，则进程就阻塞在read操作上。这种阻塞的方式在一个连接一个进程的场景下没有问题，但如果一个进程处理多个连接，进程阻塞在某个连接的read操作上，此时即使其他连接有数据可读，进程也无法去处理，很显然这样是无法做到高性能的。

解决这个问题的最简单的方式是将read操作改为非阻塞，然后进程不断地轮询多个连接。这种方式能够解决阻塞的问题，但解决的方式并不优雅。首先，轮询是要消耗CPU的；其次，如果一个进程处理几千上万的连接，则轮询的效率是很低的。

为了能够更好地解决上述问题，很容易可以想到，只有当连接上有数据的时候进程才去处理，这就是I/O多路复用技术的来源。

I/O多路复用技术归纳起来有两个关键实现点：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/23/3c3272bd.jpg" width="30px"><span>林</span> 👍（523） 💬（11）<div>IO操作分两个阶段1、等待数据准备好(读到内核缓存)2、将数据从内核读到用户空间(进程空间)一般来说1花费的时间远远大于2。1上阻塞2上也阻塞的是同步阻塞IO1上非阻塞2阻塞的是同步非阻塞IO，这讲说的Reactor就是这种模型 1上非阻塞2上非阻塞是异步非阻塞IO，这讲说的Proactor模型就是这种模型 </div>2018-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/23/3c3272bd.jpg" width="30px"><span>林</span> 👍（493） 💬（18）<div>Reactor与Proactor能不能这样打个比方：
1、假如我们去饭店点餐，饭店人很多，如果我们付了钱后站在收银台等着饭端上来我们才离开，这就成了同步阻塞了。
2、如果我们付了钱后给你一个号就可以离开，饭好了老板会叫号，你过来取。这就是Reactor模型。
3、如果我们付了钱后给我一个号就可以坐到坐位上该干啥干啥，饭好了老板会把饭端上来送给你。这就是Proactor模型了。</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（101） 💬（1）<div>感谢华仔，我也再实验了下netty4，其实handler的独立的线程池里面执行其实也没有问题，netty已经帮我们处理好了，当我们处理完业务，write数据的时候，会先放到一个队列里面，真正出站还是由io线程统一调度，这样就避免了netty3的问题！</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（64） 💬（5）<div>根据华仔之前对前浪微博消息中间件的分析，TPS定位在1380，QPS定位在13800，消息要高可靠（不能丢失消息），定位在常量连接海量请求的系统吧。基于此来分析下吧。

1、单Reactor单进程&#47;线程
redis采用这种模式，原因是redis是基于内存的数据库，在处理业务会非常快，所以不会对IO读写进行过长时间的阻塞，但是如果redis开启同步持久化后，业务处理会变慢，阻塞了IO线程，也就无法处理更多的连接了，而我们的消息中间件需要消息的高可靠，必定要同步持久化，如果异步的话，就看异步持久化的时间间隔了，假设500ms持久化一次，那就有可能会丢失500ms的消息。当然华仔分析的无法利用多核cpu的特性也是一大缺点；虽然我们要求的TPS不算很高，但是QPS很高了，所以我觉得这种模式不合适
2、单Reactor多进程&#47;线程
这种模式我觉得也不是和合适，虽然真正的业务处理在独立的线程了，IO线程并没有被阻塞，可以处理更多的连接和读写事件。我们的中间件可能不会面对海量的连接数，但是会面对大量的读请求，瓶颈是在处理读操作上，跟单Reactor单进程&#47;线程差别不大；我倒觉得前一讲说的TPC prethread 模式是合适的，有独立的线程负责read-业务处理-send。
3、多Reactor多进程&#47;线程
这种模式是最合适的了，不过华仔在讲解是read→业务处理→send，业务处理还是在IO线程上，如果业务处理的慢，还是会阻塞IO线程的，我觉得最好是业务处理放到独立的线程池里面去，这就变成了mainReactor负责监听连接，subReactor 负责IO读写，后面的业务线程池负责真正的业务处理，这样就既可以面对海量的连接，海量的请求也可以支撑。

不知理解的是否正确？</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a8/1b/ced1d171.jpg" width="30px"><span>空档滑行</span> 👍（46） 💬（2）<div>消息队列系统属于中间件系统，连接数相对固定，长链接为主，所以把accept分离出来的意义是不大的。消息中间件要保证数据持久性，所以入库操作应该是耗时最大的操作。综合起来我觉得单reactor，多线程&#47;进程的方式比较合适。</div>2018-06-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/NicGuX4PVAEHDmodLO5n313OVn024K4D2kCsuorM11H5c4HJZDVzJ9KMj5auzgQW5YNl06edSypHAhpNs41zuEw/132" width="30px"><span>LinMoo</span> 👍（26） 💬（1）<div>请教两个问题 谢谢
之前学习NIO和AIO的时候是这么描述的：进程请求IO（无论是硬盘还是网络IO），先让内核读取数据到内核缓存，然后从内核缓存读取到进程。这里面就有2个IO等待时间，第一个是读取到内核缓存，第二个是读取到进程。前者花费的时间远远大于后者。在第一个时间中进程不做等待就是NIO，即非阻塞。第二个时间中进程也不需要等待就是AIO，即异步。
第一个问题：文章中说Reactor 是非阻塞同步网络模型，因为真正的 read 和 send 操作都需要用户进程同步操作。这里的read和send指的是我上面说的第二个时间吗？
第二个问题：因为我理解你的“来了事件我来处理，处理完了我通知你”。这里的我来处理就是包括第一和第二个时间吗？

感觉我之前被误解了，是我哪个地方理解不对吗？麻烦解答一下。</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（17） 💬（4）<div>感谢华仔的解答，我看到在针对多reactor多线程模型，也有同学留言有疑问，我想请教下华仔，多reactor多线程模型中IO线程与业务处理在同一线程中，如果业务处理很耗时，定会阻塞IO线程，所以留言同学“衣申人”也说要不要将IO线程跟业务处理分开，华仔的答案是性能没有提升，复杂度提升很多，我还没见过这种处理方式，华仔对netty应该是很熟悉的，我的疑问是：在netty中boss线程池就是mainReactor，work线程池就是subReactor，正常在ChannelPipeline中添加ChannelHandler是在work线程即IO线程中串行执行，但是如果pipeline.addLast(group, &quot;handler&quot;, new MyBusinessLogicHandler());这样的话，业务hangdle就会在group线程池里面执行了，这样不就是多reactor多线程模型中把IO线程和业务处理线程分开么？而且我在很多著名开源项目里面看到使用netty都是这样处理的，比如阿里的开源消息中间件rocketmq使用netty也是如此。华仔说没有见过这种处理方式，能否解答下？不知道是不是我理解错了</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/e4/ec572f55.jpg" width="30px"><span>沙亮亮</span> 👍（12） 💬（1）<div>根据unix网络编程上说的，select和poll都是轮询方式，epoll是注册方式。为什么您说select也不是轮询方式</div>2018-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b9/9e/7e801469.jpg" width="30px"><span>努力成为架构师的萌新</span> 👍（11） 💬（1）<div>萌新，没有什么实践经验，理解和总结的可能不到位，也有些疑问希望得到解答

总结:
少连接，多请求 - PPC&#47;TPC
多连接，多请求
    - 单Rector 单线程 (无法充分利用内核，需要业务处理迅速)
    - 单Rector 多线程 (复杂度较高，应对瞬间高并发能力较差)
    - 多Rector 多线程 (复杂度比 单Rector多线程 低，强化应对高并发的能力)

疑问:
    1. 多Rector多线程 相比于其他Rector模式的缺点是什么， 既可以充分利用内核，复杂度不错，也有一定应对高并发的能力，岂不是万金油的选择？
    2. 多Rector多线程&#47;进程 的模式和PPC&#47;TPC很像，都是在请求连接的时候开始新线程&#47;进程 进行处理，这两者之间有什么区别？

后浪微博的场景会有多连接，多请求(访问量)，并且可能存在高并发的场合， 所以可以采用多Rector多线程(分析错的话希望指点)</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（7） 💬（1）<div>这个Reactor Proactor好抽象，不太理解

</div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/3f/80bf4841.jpg" width="30px"><span>文竹</span> 👍（7） 💬（1）<div>服务基本上都是部署在Linux上的，所以仅能使用reactor。前浪微博的写QPS在千级别，读在万级别，一般单台稍微好点配置好点的机器都能承受这两个QPS，再加上这两个QPS因任务分配器被分摊到了多态机器，最终单台机器上的QPS并不高。所以使用单reactor多线程模式足矣。</div>2018-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/bb/22af0e52.jpg" width="30px"><span>孙振超</span> 👍（7） 💬（1）<div>ppc和tpc时是每一个连接创建一个进程或线程，处理完请求后将其销毁，这样的性能比较低，为提升性能，首先考虑是链接处理完后不再销毁进程或线程，将这一部分的成本给降下来。改进后存在的问题是如果当前的链接没有请求又把进程或线程都给占住的情况下，新进来的链接就没有处理资源了。对此的解决方法是把io处理从阻塞改为非阻塞，这样当链接没有请求的时候可以去其他有请求的链接，这样改完后存在的问题有两个：一是寻找有请求的链接需要轮询需要耗费cpu而是当请求特别多的时候轮询一遍也需要耗费很长时间。基于这种情况引出了io多路复用，在处理进程和链接这之间加了一个中间人，将所有的链接都汇总到一个地方，处理进程都阻塞在中间人上，当某一个链接有请求进来了，就通知一个进程去处理。在具体的实现方式上根据中间人reactor的个数和处理请求进程的个数上有四种组合，用的比较多的还是多reactor和多进程。
之前的留言中有一个类比成去餐厅吃饭的例子还是蛮恰当的，肯德基麦当劳里面是reactor模式，需要用户先领个号然后等叫号取餐；海底捞和大多数中餐厅就是paractor模式，下完单后服务员直接将食品送过来。


回到文章中的问题，消息中间件的场景是链接数少请求量大，采用多进程或多线程来处理会比较好，对应单reactor还是多reactor应该都可以。</div>2018-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/78/71d37164.jpg" width="30px"><span>老北</span> 👍（5） 💬（3）<div>华仔，请教个问题。
redis是使用单reactor单进程模式。缺点是handler在处理某个连接上的业务时，整个进程无法处理其他连接的事件。
但是我做了个测试，在redis里面存放了一个1000w长度的list，然后使用lrange 0  -1全取出来，这会用很久。
这时候我新建个连接，继续其他key的读写操作都是可以的。不是应该阻塞吗？</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/97/4ca1377c.jpg" width="30px"><span>luck bear</span> 👍（4） 💬（1）<div>你好，我是小白，针对单reactor,多线程的方式，负责处理业务的processor的子线程，是在什么时候创建，由谁创建，每来一个新链接，都要创建一个新的子线程吗？</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ab/4b/01c56dda.jpg" width="30px"><span>FelixSun</span> 👍（3） 💬（1）<div>小白有一个问题困扰了好几天，可能也是经验不足没接触过这方面，请问一下。这里反复说的连接和请求究竟是什么意思？我查了一些资料，用MySQL举例，是不是说，mysql的连接数就是指的连接，mysql在最大连接数下支持的一秒内的请求处理数量是指的请求？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（3） 💬（1）<div>nodejs的异步模型是io线程池来监听io，然后通过管道通信来通知事件循环的线程。事件循环线程调用主线程注册的回调函数来实现的。不知道这种模式跟今天说的两种相比有什么优缺点啊</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/81/28418795.jpg" width="30px"><span>衣申人</span> 👍（3） 💬（1）<div>华仔，我有两个疑问:
1.单reactor多线程模式，业务处理之后，处理线程将结果传输给reactor线程去send，这个具体能怎么实现？reactor既要等待网络事件，又要等待业务线程的处理结果，然后作出响应，这个除了两边轮询还有更直接的方式吗？
2.多reactor多线程模型，现在你给出的方案是连接线程与io线程分开，但io线程与业务处理在一起的。而有的资料建议将io线程和业务线程分开，你认为有这个必要吗？
</div>2018-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/0c/0fb4a739.jpg" width="30px"><span>码钉</span> 👍（3） 💬（1）<div>Proactor 可以理解为“来了事件我来处理，处理完了我通知你”。

请问一下这里的“处理”具体指什么? 把数据从内核层复制到应用层么?</div>2018-06-09</li><br/><li><img src="" width="30px"><span>mxmkeep</span> 👍（2） 💬（1）<div>nginx已经默认废弃使用锁来均衡accept，而是使用设置socket reuse来让内核负载均衡到各进程</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/49/bd914b5f.jpg" width="30px"><span>公号-彤哥读源码</span> 👍（2） 💬（1）<div>关于下面同学说的Reactor主从模型中业务处理使用另外的线程池处理，我不同意老师的观点哈，原因有三点：
1. Doug Lea在《Scalable IO in Java》中关于Reactor主从的讲解用的确实是这位同学说的业务线程池独立出来处理；
2. Netty中的io.netty.channel.ChannelPipeline#addLast(io.netty.util.concurrent.EventExecutorGroup, java.lang.String, io.netty.channel.ChannelHandler)方法是可以支持你的Handler定制一个线程池来处理的，Netty中的线程池就是这里的EventExecutorGroup，Netty的Handler使用另外的线程池处理的时候一样使用ctx.write()操作写出数据，此时会判断在不在EventLoop中，如果不在就异步放到EventLoop中写出数据，老师可以看下这块的源码io.netty.channel.AbstractChannelHandlerContext#write(java.lang.Object, boolean, io.netty.channel.ChannelPromise)，简单点来说，就是我们不用关心read&#47;write操作与自定义线程池的交互，Netty都帮我们处理好了。
3. 实际场景中确实存在业务处理耗时的情况，比如写数据库，而Netty中是一个EventLoop（线程）监听多个连接的事件，如果业务处理跟IO放一块一个事件业务处理慢容易导致这个EventLoop监听的事件都阻塞住；

关于Doug Lea的《Scalable IO in Java》我放在gitee上了，欢迎下载：https:&#47;&#47;gitee.com&#47;alan-tang-tt&#47;reactor</div>2021-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（2）<div>老师，可以发一下reactor编码实现的官方连接吗？</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/e4/ec572f55.jpg" width="30px"><span>沙亮亮</span> 👍（2） 💬（1）<div>两个轮询不是一个意思，select和poll是收到通知后轮询socket列表看看哪个socket可以读，普通的socket轮询是指重复调用read操作

感谢大神回复，那对于select实现的I&#47;O多路复用技术，和普通的轮询区别在于，一个是socket上有数据时，系统通知select，然后select去轮询所有的socket，而普通的轮询就是一直不停的轮询所有socket。

还有一个有关真实应用场景中的问题，对于nginx+php-fpm这样一个场景，对于I&#47;O多路复用技术，在nginx处理外部请求的时候用到了Reactor模式。当nginx把请求转发给php-fpm，然后php通过读数据库，代码业务逻辑处理完后，再从php−fpm读取数据，返回给客户端请求过程中，有没有再使用Reactor模式了？</div>2018-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/69/113da382.jpg" width="30px"><span>宇飞</span> 👍（1） 💬（1）<div>阻塞是对内核说的，同步异步对用户态而言</div>2022-08-11</li><br/><li><img src="" width="30px"><span>GeekZY</span> 👍（1） 💬（2）<div>老师，在微服务架构，SpringBoot应用，单机性能要达到10万，用什么方案比较合适？</div>2021-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/ae/a6d5e24a.jpg" width="30px"><span>🐗Jinx</span> 👍（1） 💬（1）<div>老师我想问一下。在多Reactor多进程&#47;线程模式下，是不是需要为每一个Reactor创建一个epoll实例。例如，主Reactor需要一个监听epoll实例用于accept新的链接，然后需要为每一个从Reactor创建一个读写epoll实例。

因为如果多个Reactor共享同一个epoll实例，就会出现很多维护问题，例如某个Reactor可能会更改或者删除掉别的Reactor的关注文件描述符。</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/33/4562472d.jpg" width="30px"><span>蓓岑2015</span> 👍（1） 💬（1）<div>请问这是哪一方面的知识？我到这篇文章为止，已经看不懂了，一脸懵逼啊，求老师指点一下，对Reactor与Proactor根本就没有概念。</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/ae/7614163c.jpg" width="30px"><span>李继鹏</span> 👍（1） 💬（1）<div>李老师能讲一下udp服务是否能用reactor模型吗？网上这方面的资料甚少</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/fb/ef99d6ca.jpg" width="30px"><span>tiger</span> 👍（1） 💬（3）<div>老师，你好，你有说到单线程单连接的时候，线程会阻塞，。这种模型还可以通过协程(比如go语言的goroutine)方式解决，一个协程一个连接，因为协程属于用户态线程，轻量，所以同一时间可以产生大量的协程。这种方式就可以实现同步阻塞并发模型。

当然协程会增加额外的内存使用，另外也是通过线程轮询协程状态的方式驱动的</div>2018-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/9f/f3bcd2d0.jpg" width="30px"><span>爱逃课的橡皮擦</span> 👍（1） 💬（1）<div>“当多条连接共用一个阻塞对象后，进程只需要在一个阻塞对象上等待，而无须再轮询所有连接“ 华仔你好，这句话能详细解释下吗，多条连接怎么公用一个阻塞对象，为什么解决了轮训的问题，连接处于什么事件不去轮询怎么知道，是说自己不去轮询系统帮你轮询吗</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/e5/aa579968.jpg" width="30px"><span>王磊</span> 👍（1） 💬（1）<div>我们用的是Vertx, 我了解它是多Reactor, 多线程的模式，Reactor只负责消息的分发，耗时的操作都在专有的线程池内操作，也可以方便的指定新的线程池的名字在自己的线程池内运行。
问题，这里明确一个定义，说单Reactor单进程&#47;线程的时候，是否包含了Reactor的进程&#47;线程? 理解应该没有，所以&#39;单Reactor单进程&#47;线程&#39;应该有2个进程&#47;线程在工作?</div>2018-06-09</li><br/>
</ul>