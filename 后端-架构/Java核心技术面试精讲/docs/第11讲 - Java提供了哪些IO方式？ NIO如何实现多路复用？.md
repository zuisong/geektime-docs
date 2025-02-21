IO一直是软件开发中的核心部分之一，伴随着海量数据增长和分布式系统的发展，IO扩展能力愈发重要。幸运的是，Java平台IO机制经过不断完善，虽然在某些方面仍有不足，但已经在实践中证明了其构建高扩展性应用的能力。

今天我要问你的问题是，**Java提供了哪些IO方式？ NIO如何实现多路复用？**

## 典型回答

Java IO方式有很多种，基于不同的IO抽象模型和交互方式，可以进行简单区分。

第一，传统的java.io包，它基于流模型实现，提供了我们最熟知的一些IO功能，比如File抽象、输入输出流等。交互方式是同步、阻塞的方式，也就是说，在读取输入流或者写入输出流时，在读、写动作完成之前，线程会一直阻塞在那里，它们之间的调用是可靠的线性顺序。

java.io包的好处是代码比较简单、直观，缺点则是IO效率和扩展性存在局限性，容易成为应用性能的瓶颈。

很多时候，人们也把java.net下面提供的部分网络API，比如Socket、ServerSocket、HttpURLConnection也归类到同步阻塞IO类库，因为网络通信同样是IO行为。

第二，在Java 1.4中引入了NIO框架（java.nio包），提供了Channel、Selector、Buffer等新的抽象，可以构建多路复用的、同步非阻塞IO程序，同时提供了更接近操作系统底层的高性能数据操作方式。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/15/02/66f65388.jpg" width="30px"><span>雷霹雳的爸爸</span> 👍（61） 💬（1）<div>批评NIO确实要小心，我觉得主要是三方面，首先是如果是从写BIO过来的同学，需要有一个巨大的观念上的转变，要清楚网络就是并非时刻可读可写，我们用NIO就是在认真的面对这个问题，别把channel当流往死里用，没读出来写不进去的时候，就是该考虑让度线程资源了，第二点是NIO在不同的平台上的实现方式是不一样的，如果你工作用电脑是win，生产是linux，那么建议直接在linux上调试和测试，第三点，概念上的，理解了会在各方面都有益处，NIO在IO操作本身上还是阻塞的，也就是他还是同步IO，AIO读写行为的回调才是异步IO，而这个真正实现，还是看系统底层的，写完之后，我觉得我这一二三有点凑数的嫌疑</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/08/49416831.jpg" width="30px"><span>Chan</span> 👍（40） 💬（2）<div>忘记回答问题了。所以对于多路复用IO，当出现有的IO请求在数据拷贝阶段，会出现由于资源类型过份庞大而导致线程长期阻塞，最后造成性能瓶颈的情况</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/53/6c/46c4efb0.jpg" width="30px"><span>扁担</span> 👍（20） 💬（3）<div>据我理解，NIO2的局限性在于，如果回调时客户端做了重操作，就会影响调度，导致后续的client回调缓慢</div>2018-10-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ZwLEEpglswe8uzYj4W6ZVxx0W0OdicjicFzkha4O99wZWGRXqOTF1LO8SsJaBicCXugIQhn8BQicVoTcDJic82RbwDg/132" width="30px"><span>扁扁圆圆</span> 👍（12） 💬（2）<div>这里Nio的Selector只注册了一个sever chanel，这没有实现多路复用吧，多路复用不是注册了多个channel ，处理就绪的吗？而且处理客户端请求也是在同线程内，这还不如上面给的Bio解决方案吧</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/19/43/51154077.jpg" width="30px"><span>萧萧</span> 👍（9） 💬（3）<div>作者对同步&#47;异步， 阻塞&#47;非阻塞的概念说明存在问题。

《操作系统（第9版）》中关于进程通信中有对这部分概念做过解释， 在进程间通信的维度， 同步和阻塞，异步和非阻塞是相同的概念。

 沿着作者的概念解释简单推论一下就可以发现: 

如果同步操作是需要等待调用返回才能进行下一步， 显然这个调用是阻塞的。 

反之， 不需要等待调用返回的接口，必然需要提供事件， 回调等机制，这种调用显然是非阻塞的。 </div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/e9/f667649e.jpg" width="30px"><span>yxw</span> 👍（9） 💬（1）<div>java nio的selector主要的问题是效率，当并发连接数达到数万甚至数十万的时候 ，单线程的selector会是一个瓶颈；另一个问题就是再线上运行过程中经常出现cpu占用100%的情况，原因也是由于selector依赖的操作系统底层机制bug 导致的selector假死，需要程序重建selector来解决，这个问题再jdk中似乎并没有很好的解决，netty成为了线上更加可靠的网络框架。不知理解的是否正确，请老师指教。</div>2018-06-03</li><br/><li><img src="" width="30px"><span>zjh</span> 👍（9） 💬（1）<div>看nio代码部分，请求接受和处理都是一个线程在做。这样的话，如果有多个请求过来都是按顺序处理吧，其中一个处理时间比较耗时的话那所有请求不都卡住了吗？如果把nio的处理部分也改成多线程会有什么问题吗</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/bf/a44cde46.jpg" width="30px"><span>lorancechen</span> 👍（9） 💬（1）<div>我也自己写过一个基于nio2的网络程序，觉得配合futrue写起来很舒服。
仓库地址：https:&#47;&#47;github.com&#47;LoranceChen&#47;RxSocket  欢迎相互交流开发经验～

记得在netty中，有一个搁置的netty5.x项目被废弃掉了，原因有一点官方说是性能提升不明显，这是可以理解的，因为linux下是基于epoll，本质还是select操作。

听了课程之后，有一点印象比较深刻，select模式是使用一个线程做监听，而bio每次来一个链接都要做线程切换，所以节省的时间在线程切换上，当然如果是c&#47;c++实现，原理也是一样的。


想问一个一直困惑的问题，select内部如何实现的呢？
个人猜测：不考虑内核，应用层的区分，单纯从代码角度考虑，我猜测，当select开始工作时，有一个定时器，比如每10ms去检查一下网络缓冲区中是否有tcp的链接请求包，然后把这些包筛选出来，作为一个集合（即代码中的迭代器）填入java select类的一个集合成员中，然后唤醒select线程，做一个while遍历处理链接请求，这样一次线程调度就可以处理10ms内的所有链接。与bio比，节省的时间在线程上下文切换上。不知道这么理解对不对。
另外，也希望能出一个课程，按照上面这种理解底层的方式，讲讲select（因为我平常工作在linux机器，所以对select epoll比较感兴趣）如何处理read，write操作的。谢谢～

</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/bf/a44cde46.jpg" width="30px"><span>lorancechen</span> 👍（8） 💬（1）<div>还有一个问题请教，select在单线程下处理监听任务是否会成为瓶颈？能否通过创建多个select实例，并发监听socket事件呢？</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/77/7e852c51.jpg" width="30px"><span>残月@诗雨</span> 👍（5） 💬（2）<div>杨老师，有个问题一直不太明白：BufferedInputStream和普通的InputStream直接read到一个缓冲数组这两种方式有什么区别？</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（4） 💬（1）<div>NIO多路复用模式，如果对应事件的处理比较耗时，是不是会导致后续事件的响应出现延迟。</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（4） 💬（1）<div>老师 注册管道到select上，应该用队列实现的吧？
开启一个线程大概需要多少内存开销呢，我记得数据库连接大概2M</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（3） 💬（1）<div>杨老师，把你给的NIOServer的例子做了一下，发现sayHelloWorld()方法，client.write()后，如果没有client.close(),线程一直在挂着。请确认一下，是否例子缺了client.close()？</div>2018-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/3c/13175251.jpg" width="30px"><span>Miaozhe</span> 👍（2） 💬（1）<div>问个问题，看到你写的样例中，几处try (),小括号里面写了一些逻辑，这种写法跟放在{}里面有啥区别？望专家回复一下。</div>2018-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/d6/f331dba7.jpg" width="30px"><span>Forrest</span> 👍（1） 💬（2）<div>使用线程池可以很好的解决线程复用，避免线程创建带来的开销，效果也很好，一个问题想请教下，当线程池无法满足需要时可以用什么方式解决？</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/a5/ad6b2938.jpg" width="30px"><span>王睿</span> 👍（229） 💬（9）<div>举个收快递的例子不知道理解是否正确。

BIO，快递员通知你有一份快递会在今天送到某某地方，你需要在某某地方一致等待快递员的到来。

NIO，快递员通知你有一份快递会送到你公司的前台，你需要每隔一段时间去前台询问是否有你的快递。

AIO，快递员通知你有一份快递会送到你公司的前台，并且前台收到后会给你打电话通知你过来取。</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/8d/7db04ad3.jpg" width="30px"><span>I am a psycho</span> 👍（141） 💬（1）<div>由于nio实际上是同步非阻塞io，是一个线程在同步的进行事件处理，当一组事channel处理完毕以后，去检查有没有又可以处理的channel。这也就是同步+非阻塞。同步，指每个准备好的channel处理是依次进行的，非阻塞，是指线程不会傻傻的等待读。只有当channel准备好后，才会进行。那么就会有这样一个问题，当每个channel所进行的都是耗时操作时，由于是同步操作，就会积压很多channel任务，从而完成影响。那么就需要对nio进行类似负载均衡的操作，如用线程池去进行管理读写，将channel分给其他的线程去执行，这样既充分利用了每一个线程，又不至于都堆积在一个线程中，等待执行。杨老师，不知道上述理解是否正确？</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/4d/e24fc9e4.jpg" width="30px"><span>蔡光明</span> 👍（88） 💬（1）<div>看完之后还是不了解nio，感觉看起来越来越吃力了，大半天都啃不了一篇，好多东西都不熟悉，还要自己查资料去了解然后再回过来看，，，老师最好给些学习的资料让我们能找到，就这一篇感觉根本不够</div>2018-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/08/49416831.jpg" width="30px"><span>Chan</span> 👍（67） 💬（0）<div>B和N通常是针对数据是否就绪的处理方式来
sync和async是对阻塞进行更深一层次的阐释，区别在于数据拷贝由用户线程完成还是内核完成，讨论范围一定是两个线程及以上了。


同步阻塞，从数据是否准备就绪到数据拷贝都是由用户线程完成

同步非阻塞，数据是否准备就绪由内核判断，数据拷贝还是用户线程完成

异步非阻塞，数据是否准备就绪到数据拷贝都是内核来完成

所以真正的异步IO一定是非阻塞的。

多路复用IO即使有Reactor通知用户线程也是同步IO范畴，因为数据拷贝期间仍然是用户线程完成。

所以假如我们没有内核支持数据拷贝的情况下，讨论的非阻塞并不是彻底的非阻塞，也就没有引入sync和async讨论的必要了

不知道这样理解是否正确

</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/43/11acdc02.jpg" width="30px"><span>Allen</span> 👍（48） 💬（0）<div>希望能听到更多原理性的东西，而不是在网上能搜到的样例代码</div>2018-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（23） 💬（2）<div>对比而言，感觉这节讲解的不够细致，学完以后，能回答开篇的两个问题了，Java提供了IO&#47;BIO&#47;NIO&#47;AIO这几种IO的方式，但是他们的优缺点，使用场景等讲解的不多，推荐看下慕课的 https:&#47;&#47;www.imooc.com&#47;learn&#47;941 这个课程，前半部分把Java IO相关的东西讲解的还是比较详细的。多路复用，这个东西能节省服务端的线程创建成本，一个线程监听多个通道，那个通道就绪了，就处理那个通道，不过具体他是怎么实现的呢？主动的不断轮询？还是被动的接受信息？
如果一个通道的处理时间比较长，其他的多个通道又都就绪了，此时该怎么办？就让其他的就绪的通道等待着？
感觉是开眼界还行，如果是全弄明白，还是乏力的，要看专业的书啦！</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/2a/8037612c.jpg" width="30px"><span>Barry</span> 👍（15） 💬（0）<div>写的啥，看着跟一个普通高级工程师写出来没啥区别</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/da/23a4a0c4.jpg" width="30px"><span>aiwen</span> 👍（15） 💬（8）<div>到底啥是多路复用？一个线程管理多个链接就是多路复用？</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/32/8d59aaef.jpg" width="30px"><span>unclenought</span> 👍（10） 💬（1）<div>http:&#47;&#47;tutorials.jenkov.com&#47;java-nio&#47;index.html，这篇教程对NIO讲得很好，容易理解且有一些实际例子。</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（7） 💬（0）<div>这个nio看起来还是单线程在处理，如果放到多线程池中处理和bio加线程池有啥区别呢 </div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/c8/7679cd2a.jpg" width="30px"><span>冬青树</span> 👍（5） 💬（0）<div>IO的调用可以分为三大块，请求调用，逻辑处理，响应返回处理。常规的BIO在这三个阶段会串行的阻塞的。NIO其实可以理解为将这三个阶段尽可能的去阻塞或者减少阻塞。看了上面的例子，NIO的服务器端在接受客户端请求的时候，是单线程执行的，而BIO是多线程处理的。但是不管咋的，他们服务器端处理具体的客户业务逻辑是都要用多线程的吧？</div>2018-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/b6/3d8fcc2c.jpg" width="30px"><span>张凯江</span> 👍（4） 💬（0）<div>cpu运算密集型应用。node得诟病</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/a5/eccc7653.jpg" width="30px"><span>clz1341521</span> 👍（3） 💬（0）<div>1,基于nio的tcp 编程代码复杂
2,nio本质是同步非阻塞的
总结：select模式是使用一个线程做监听，而bio每次来一个链接都要做线程切换，所以节省的时间在线程切换</div>2018-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/38/59dda970.jpg" width="30px"><span>RoverYe</span> 👍（3） 💬（0）<div>nio不适合数据量太大交互的场景</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/bd/23aeb6d0.jpg" width="30px"><span>java届-Mr.吉</span> 👍（2） 💬（0）<div>同步和阻塞的区别方便解释一下嘛。字面理解的哈，都是两个线程同时过来，一个线程先执行，另一个线程就被阻塞，直到条件满足或者事件回掉，才能继续。没明白他俩的本质区别</div>2019-03-13</li><br/>
</ul>