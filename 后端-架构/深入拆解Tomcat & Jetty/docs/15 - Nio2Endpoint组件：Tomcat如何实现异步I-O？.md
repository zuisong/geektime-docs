我在专栏上一期里提到了5种I/O模型，相应的，Java提供了BIO、NIO和NIO.2这些API来实现这些I/O模型。BIO是我们最熟悉的同步阻塞，NIO是同步非阻塞，那NIO.2又是什么呢？NIO已经足够好了，为什么还要NIO.2呢？

NIO和NIO.2最大的区别是，一个是同步一个是异步。我在上期提到过，异步最大的特点是，应用程序不需要自己去**触发**数据从内核空间到用户空间的**拷贝**。

为什么是应用程序去“触发”数据的拷贝，而不是直接从内核拷贝数据呢？这是因为应用程序是不能访问内核空间的，因此数据拷贝肯定是由内核来做，关键是谁来触发这个动作。

是内核主动将数据拷贝到用户空间并通知应用程序。还是等待应用程序通过Selector来查询，当数据就绪后，应用程序再发起一个read调用，这时内核再把数据从内核空间拷贝到用户空间。

需要注意的是，数据从内核空间拷贝到用户空间这段时间，应用程序还是阻塞的。所以你会看到异步的效率是高于同步的，因为异步模式下应用程序始终不会被阻塞。下面我以网络数据读取为例，来说明异步模式的工作过程。

首先，应用程序在调用read API的同时告诉内核两件事情：数据准备好了以后拷贝到哪个Buffer，以及调用哪个回调函数去处理这些数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（32） 💬（3）<div>老师好!Windows 的 IOCP 和 Linux 内核 2.6 的 AIO 都提供了异步 I&#47;O 的支持，Java 的 NIO.2 API 就是对操作系统异步 I&#47;O API 的封装。
这句话怎么理解啊？我看别的老师说Linux不支持异步IO，评论里也有同学说Linux下的AIO其实只是NIO之类的。老师能具体讲讲么谢谢。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（20） 💬（1）<div>老师好!那个两次read能理解为，连接被保留着，数据没就绪处理的线程资源先释放了。收到异步数据就绪通知后，根据原有的连接重建处理线程，继续处理。阻塞期间线程可复用</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（17） 💬（1）<div>李老师好，请问nio1，tomcat里nio为什么不参考netty，通过使用堆外内存来避免零拷贝问题？</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（13） 💬（2）<div>老师，NIO2中，由于TCP是一个流，那内核把多少字节拷贝到buff中才触发回调函数呢？比如一次http请求，有没有可能触发回调函数时，还没有把一个完整的http请求包接受完整呀？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（8） 💬（1）<div>老师 ， 这两张讲的I&#47;O有点难啃 ，主要还是底子太薄 。 反复看了几遍有几个疑问点希望老师指点一下 😄

1. read请求是怎么发出来的 是通过调用select方法发出来的么 ？

2. 异步我看发了一个read 就返回了，那实际是应该是指异步非阻塞 ， 那么存在异步阻塞的模型么？

3. 老师说从tcp&#47;ip那层解数据包。我理解的过程是 当客户端发一个uri请求，当通过一系列的路由后最终到我们的服务器，再从七层网络模型的最底层开始一路向上到最顶层的应用层。 当应用层（Tomcat容器）接收到请求（连接器endpoint监听端口）后向操作系统发送一个read请求 ，然后等待操作系统内核回调应用程序（Tomcat容器）的回调接口 。那么按照我这种脑补的过程，实际上当服务端tomcat接收到客户端的I&#47;O请求时，向操作系统发送read请求要求操作系统将客户端发送的数据（前台的入参信息）从内核拷贝到用户空间。因为tcp&#47;ip层在应用层下面，那么从网卡解析数据到内核这个过程是不是在tomcat获取到请求之前的的时候就已经处理好了，而不是在tomcat发送read请求时再去从网卡解析数据..？
</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/c5/aaacb98f.jpg" width="30px"><span>yungoo</span> 👍（8） 💬（3）<div>我所看的tomcat 8.5的代码跟专栏所讲已经有些不一致了。已经没有Nio2Acceptor了，accept获取连接用的是Future aceept()。</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/65/cce8eb34.jpg" width="30px"><span>nimil</span> 👍（7） 💬（1）<div>问下老师，这个Tomcat这个IO模型是将数据拷贝了两次么，还是有做特殊优化</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（6） 💬（3）<div>怎么模拟呢。现在springboot内置的Tomcat使用的都是nio  。设定NIO2呢</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（6） 💬（1）<div>linux没有真正实现异步IO，所以linux环境下NIO和NIO2的性能差别是不是不大 ？</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（6） 💬（1）<div>Http11Processor的2次read是在哪个类中呢，没有找到。。。。</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（4） 💬（1）<div>老师关于IO模型内存我有两个问题：
1. 配内存的时候，是不是因为堆内存会受到GC的影响导致地址变化，所以不能直接使用不能使用堆内存， 如果使用堆内存的话也需要先指向一个固定的堆外内存，所以使用堆外内存就可以避免GC对内存地址的影响。
2. 是不是IO在读数据的时候经过两次数据拷贝，从网卡到内核态，从内核态到用户态，这两次数据拷贝有什么方法可以减少1次吗？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b5/d4/e58e39f0.jpg" width="30px"><span>Geek_0quh3e</span> 👍（3） 💬（3）<div>Http11Processor 是通过 2 次 read 调用来完成数据读取操作的。
这一点看了好几遍始终没明白，
作者回复: Nio2SocketWrapper的read方法，这个方法会被调用两次，不是串行调两次，而是Poller会先后创建两个SocketProcessor任务类，在两个线程中执行，执行过程中每次Http11Processor都会调Nio2SocketWrapper的read方法。

public int read(boolean block, ByteBuffer to){

&#47;&#47;第二次调用时直接通过这个方法取数据
int nRead = populateReadBuffer(to);

...

&#47;&#47;第一次时数据没取到，会调用下面这个方法去真正执行I&#47;O操作并注册回调函数：
nRead = fillReadBuffer(block);

...
}
以上是针对802.11的回答，可是我没有在Nio2EndPoint中找到对应poller内部类啊
 </div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（3） 💬（1）<div>老师tomcat 在哪里配置 使用nioendpoint 还是nio2endpoint，能否给个例子</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/95/866bccb7.jpg" width="30px"><span>helloWorld</span> 👍（1） 💬（1）<div>老师以后在文章中的例子可以给出完整的代码吗？</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（0） 💬（1）<div>老师 有了nio2endpoint是不是就没人用nioendpoint了？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（0） 💬（1）<div>老师，为什么IO操作的返回值第一个参数是channel呢，不理解。按照描述，既然是返回值应该是一些具体的值吧，channel为什么会出现在这里呢。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/5e/7556634b.jpg" width="30px"><span>binginx</span> 👍（0） 💬（1）<div>老师，tomcat使用异步nio2比使用nio性能上提高很大吗？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/66/d3d19642.jpg" width="30px"><span>半斤八两</span> 👍（0） 💬（1）<div>老师图片上Acceptor的行为还是交给poller，是不是有问题啊……还是我理解错了……</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（4） 💬（0）<div>李老师好，这节精彩，特别是两次read讲的用心。
1 nio2图里确实有个poller字样
2 思考题回答，个人认为第二次read用的是work线程池， 因为内核已经准备好完整开箱可用的数据， 直接使用即可， 无须过多的线程上下文切换。</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（3） 💬（0）<div>走到io就渐渐要掉队，虽然看了很多遍</div>2019-06-17</li><br/><li><img src="" width="30px"><span>世纪猛男</span> 👍（3） 💬（0）<div>&quot;同时为了提高处理速度，会提供一个线程池给内核使用，样不会耽误内核线程的工作&quot;

请问老师，这里不太明白，用户线程不能操作内核空间， 那这个线程池 如何能替代 内核线程的工作 </div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（2） 💬（0）<div>李老师实力派！👍</div>2019-06-13</li><br/><li><img src="" width="30px"><span>Carla</span> 👍（1） 💬（1）<div>老师好，我是初学者，自己用AIO写一个简单的服务器接收连接
public class Server implements Runnable {

	private ExecutorService executorService;
	private AsynchronousChannelGroup channelGroup;
	private AsynchronousServerSocketChannel serverChannel;

	public Server() {
		try {
			this.executorService = Executors.newCachedThreadPool();
			this.channelGroup = AsynchronousChannelGroup.withCachedThreadPool(this.executorService, 10);
			this.serverChannel = AsynchronousServerSocketChannel.open(channelGroup);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void run() {
		try {
			this.serverChannel.bind(new InetSocketAddress(666));
			this.serverChannel.accept(this, new CompletionHandler&lt;AsynchronousSocketChannel, Server04&gt;() {

				@Override
				public void completed(AsynchronousSocketChannel result, Server04 attachment) {
					attachment.serverChannel.accept(attachment, this);
				}

				@Override
				public void failed(Throwable exc, Server04 attachment) {
				}

			});
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
想问下，回调函数里只有连接成功和失败两个，如果没有任何连接到达，accept方法没有任何效果，服务端线程直接结束了，如何才能即使没有客户端连接，服务端也保持监听呢。在bio可以死循环accept，nio1中可以死循环selector，aio该如何实现，还是说我的用法是错的</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>问题中两个线程池的作用不太一样。前者的作用是直接处理数据，后者是首先向内核发起io请求和注册回调函数，然后才在回调函数处理数据。</div>2022-07-11</li><br/><li><img src="" width="30px"><span>Geek_0258c1</span> 👍（0） 💬（0）<div>老师你好，看着9.x之后的版本源码，acceptor 跟 poller 都变成了只有一个线程了，没有多个线程，比如 acceptor 线程的启动，调用的方法是 startAcceptorThread()，跟你这边说的多个并不一致，请老师确认下，多谢</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div>Java NIO.2 的使用时，提到过要创建一个线程池来处理异步 I&#47;O 的回调，那么这个线程池跟 Tomcat 的工作线程池 Executor 是同一个吗？

看了评论同一个线程池。数据已经到了应用层能直接使用。但是为啥呢。</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（1）<div>请问老师回答题答案是啥。
Java NIO.2 的使用时，提到过要创建一个线程池来处理异步 I&#47;O 的回调，那么这个线程池跟 Tomcat 的工作线程池 Executor 是同一个吗。</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div>流程图还有poller.</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c7/52/c5adf218.jpg" width="30px"><span>喜欢地球的阿培同学</span> 👍（0） 💬（0）<div>老师你好，问一个问题。

数据从网卡到内核需要CPU一直运行吗？ 数据从内核到用户空间需要CPU一直运行吗？
如果上述两种情况都需要CPU一直运行，那么在高并发情况下，我感觉异步对性能的提升不会太高呀。 假设当前请求线程数大于CPU总核心数，不管同步还是异步，CPU都是100%运行的。</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>接收新链接需要被阻塞,但是completed方法不应该被阻塞.所以放在一个线程里,脱离开completed方法单独执行. 但是新new线程,和在线程池中执行.不都是不会导致completed方法被阻塞吗?这里使用线程池的原因应该是管理线程开销,而不是防止completed被阻塞吧?</div>2021-01-25</li><br/>
</ul>