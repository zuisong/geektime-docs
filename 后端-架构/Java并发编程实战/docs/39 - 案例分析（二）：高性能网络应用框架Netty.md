Netty是一个高性能网络应用框架，应用非常普遍，目前在Java领域里，Netty基本上成为网络程序的标配了。Netty框架功能丰富，也非常复杂，今天我们主要分析Netty框架中的线程模型，而**线程模型直接影响着网络程序的性能**。

在介绍Netty的线程模型之前，我们首先需要把问题搞清楚，了解网络编程性能的瓶颈在哪里，然后再看Netty的线程模型是如何解决这个问题的。

## 网络编程性能的瓶颈

在[《33 | Thread-Per-Message模式：最简单实用的分工方法》](https://time.geekbang.org/column/article/95098)中，我们写过一个简单的网络程序echo，采用的是阻塞式I/O（BIO）。BIO模型里，所有read()操作和write()操作都会阻塞当前线程的，如果客户端已经和服务端建立了一个连接，而迟迟不发送数据，那么服务端的read()操作会一直阻塞，所以**使用BIO模型，一般都会为每个socket分配一个独立的线程**，这样就不会因为线程阻塞在一个socket上而影响对其他socket的读写。BIO的线程模型如下图所示，每一个socket都对应一个独立的线程；为了避免频繁创建、消耗线程，可以采用线程池，但是socket和线程之间的对应关系并不会变化。

![](https://static001.geekbang.org/resource/image/e7/e2/e712c37ea0483e9dde0d6efe76e687e2.png?wh=1138%2A393)

BIO的线程模型
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/38/853be0c3.jpg" width="30px"><span>那只羊</span> 👍（34） 💬（1）<div>QQ怪：Netty可以先从《Netty实战》开始，虽然翻译得一般，但是对于它的整体及各个组件你都能了解到；再就是调试源码来了解它了；最后应用到项目中去啦，比如实现一个简单的RPC，一个IM之类的</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（17） 💬（1）<div>老师，学习netty除了学习老师的专栏还有什么从入门到专精的学习路线吗？</div>2019-05-28</li><br/><li><img src="" width="30px"><span>墙角儿的花</span> 👍（10） 💬（1）<div>这是我读过的最好的netty基本原理介绍</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7c/b5/4a7a2bd4.jpg" width="30px"><span>Sunqc</span> 👍（5） 💬（2）<div>我想知道老师后续有发布新的课程吗，喜欢你的课程</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（4） 💬（1）<div>谢谢老师讲这个reactor模式  我最近要优化的系统主体就是采用这个模式  今天看了一天都云里雾里的  看到这篇文章瞬间有了一种有章可循的感觉</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/18/3d05adb4.jpg" width="30px"><span>蓝山</span> 👍（2） 💬（1）<div>网络通信程序性能设计重点要关注三个方面：
1、网络传输方式：同步阻塞方式、异步非阻塞方式；
2、数据序列化：Java序列化（基本不能考虑）、protobuf、jason、Avro等等；
3、网络IO处理线程模型：同步阻塞IO、同步非阻塞IO、IO多路复用（Reactor模式）、AIO异步IO；
Netty在应对解决上述三个问题中提供了比较完善的方案。采用IO多路复用机制实现网络传输，同时配合灵活的reactor实现模式，支持通过编码灵活选择不同的reactor模式以应对不同负载和性能要求的场景。同时提供了完善的异步事件驱动实现和API，为开发人员提供了如何获取数据、数据编解码、编解码之后业务处理线程具体在哪个线程执行、编解码之后消息如何派发等等灵活且方便的机制。同时在协议层面直接支持了通用的网络通讯协议，同时对于扩展针对个性化性能需求的私有化协议定制提供了便利的开发工具支持。</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b1/b8/9ff50118.jpg" width="30px"><span>sswrock</span> 👍（1） 💬（1）<div>看了 Doug Lee的 “Scalable IO in Java”，对于做个Swing GUI开发的人豁然开朗，
感谢宝哥 和 DougLee</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/c8/15c85ee4.jpg" width="30px"><span>潭州太守</span> 👍（1） 💬（1）<div>老师，Reactor可以理解是Actor模式的一种吗</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>反过来说的话就是一个线程有多个EventLoop 一个EventLoop有多个网络连接 对吧</div>2019-09-24</li><br/><li><img src="" width="30px"><span>墙角儿的花</span> 👍（0） 💬（1）<div>问下老师，im服务端除了用netty，是不是用go的协程也好，连接和协程1对1服务，感觉这个场景下go协程并发能力绝对在netty之上啊</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（0） 💬（2）<div>问下老师零拷贝是怎么实现的呢？</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（0） 💬（1）<div>之前做的充电桩也是用的netty，但是只能单机部署，因为netty用的是长连接，但是在分布式框架中网络连接是随机的，请问老师这种情况怎么解决</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/8b/97601f22.jpg" width="30px"><span>王维</span> 👍（59） 💬（3）<div>分享一下我之前学Netty的学习笔记，主要是源码分析：https:&#47;&#47;wangwei.one&#47;tags&#47;Netty&#47;</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/c2/46ebe3a0.jpg" width="30px"><span>侧耳倾听</span> 👍（27） 💬（3）<div>你如果对java nio比较了解的话，应该就明白netty的线程模型。tomcat是在收到请求的时候，为每一个请求创建一个线程处理该次请求，消耗的是服务器的线程池，当并发连接数大的时候，性能下降很快。ngix相较于tomcat的区别就在于处理请求连接的线程只有一个，相当于一个分发器，只负责接受请求，不负责处理请求，连接建立成功后，为该连接分发一个工作线程处理请求和返回结果。这样子的话，服务器的最大并发数就没有了限制，受限的就是服务器的硬件所能支持的最大并发，这一块可以通过横向或者纵向扩展来解决。netty的线程模型也是如此，一个负责接受，一个负责处理，就是之前讲述的Work thread模式</div>2020-04-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKR3ibELhjgVicCNShZCBwvaDxibnzibggG4wUzVkS2mkDxUBZyIs87nDEdJ7PiahJBVoZcuhQ84RxAziag/132" width="30px"><span>周治慧</span> 👍（7） 💬（5）<div>没太明白netty的线程模型，老师说一个socket对应一个Java线程，一个Java线程对应一个eventGroup，那图中不应该是一个socket对应一个eventgroup吗</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（5） 💬（1）<div>网络编程和文件操作是我的疼，今天又疼了…希望疼着疼着就好了</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/0b/a438de52.jpg" width="30px"><span>0xTang</span> 👍（2） 💬（1）<div>Tcp处理连接和io分2个socket这个知识点有用。</div>2020-03-28</li><br/><li><img src="" width="30px"><span>poordickey</span> 👍（1） 💬（0）<div>这是渊博的人  写的文章和一般人写的博客区别真的太大了  跟着学习思维不断发散 感觉可以串起来好多知识点  怪不得老师强调让我们有操作系统的基础呢 </div>2021-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（1） 💬（0）<div>打卡！了解皮毛是不够的。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7f/5dc11380.jpg" width="30px"><span>苏志辉</span> 👍（1） 💬（0）<div>netty中eventloop是延迟创建的</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（1） 💬（0）<div>netty可以开设另一门课啦</div>2019-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpibfWGQ563ARjRF6yGa7XoWOMn1ZmVyNldafdzZzvOOqf9gmhacx0utXu12BsGB0w22VSlXTInPg/132" width="30px"><span>InfoQ_09e721f0120c</span> 👍（0） 💬（0）<div>bossGroup 就用来处理连接请求的。是不是一个线程就够了，不需要线程池吧？</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（0） 💬（0）<div>写得太好了吧</div>2020-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/ea/5bfce6c5.jpg" width="30px"><span>mgs2002</span> 👍（0） 💬（0）<div>受教了，去看netty实战去了</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/c9/88837387.jpg" width="30px"><span>😜哈哈</span> 👍（0） 💬（0）<div>netty中使用reactor事件驱动并发编程模型</div>2020-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>
void Reactor::handle_events(){
  &#47;&#47;通过同步事件多路选择器提供的
  &#47;&#47;select()方法监听网络事件
  select(handlers);
  &#47;&#47;处理网络事件
  for(h in handlers){
    h.handle_event();
  }
}
&#47;&#47; 在主程序中启动事件循环
while (true) {
  handle_events();

老师，这段代码是否应该在for循环里加一个if判断是否是该handler事件发生，无需对每一个hander遍历？
for(h in handlers){
   if(h事件发生)
         h.handle_event();
  }
或者我理解是事件注册到select（）中时也会有个socket编号，事件发生，select会直接回调该编号线程，但这时候也不需要遍历事件处理器了？</div>2020-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（2）<div>同一个EventLoop连接很多客户端会不会造成线程切换严重？</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/3f/155d81ef.jpg" width="30px"><span>我有切糕</span> 👍（0） 💬（0）<div>bossGroup和workerGroup是不是就是生产者-消费者的模式？</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/96/be53e80f.jpg" width="30px"><span>豪哥笑了</span> 👍（0） 💬（0）<div>后台采用Mina，单机16核，用c++测并发数目只有20个，可能什么问题</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c2/d5/126eac1a.jpg" width="30px"><span>宝石山</span> 👍（0） 💬（0）<div>在netty4中, 业务线程执行以下代码, name字段不是volatile, 根据happens-before原则, 在序列化层可能看不到name值. 我这理解有问题吗? 请老师指正

User user = new User(); &#47;&#47;business thread
user.setName(&quot;admin&quot;);
channel.write(user); 
...
encoder.encode(user); &#47;&#47;io thread
...</div>2019-07-25</li><br/>
</ul>