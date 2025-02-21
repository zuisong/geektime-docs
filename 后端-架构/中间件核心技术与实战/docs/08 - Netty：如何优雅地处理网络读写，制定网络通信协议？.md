你好，我是丁威。

上一节课，我们介绍了中间件领域最经典的网络编程模型NIO，我也在文稿的最后给你提供了用NIO模拟Reactor线程模型的示例代码。如果你真正上手了，你会明显感知到，如果代码处理得过于粗糙，只关注正常逻辑却对一些异常逻辑考虑不足，就不能成为一个生产级的产品。

这是因为要直接基于NIO编写网络通讯层代码，需要开发者拥有很强的代码功底和丰富的网络通信理论知识。所以，为了降低网络编程的门槛，Netty框架就出现了，它能够对NIO进行更高层级的封装。

从这之后，开发人员只需要关注业务逻辑的开发就好了，网络通信的底层可以放心交给Netty，大大降低了网络编程的开发难度。

这节课，我们就来好好谈谈Netty。

我会先从网络编程中通信协议、线程模型这些网络编程框架的共性问题入手，然后重点分析Netty NIO的读写流程，最后通过一个Netty编程实战，教会你怎么使用Netty解决具体问题，让你彻底掌握Netty。

## 通信协议

如果你不从事中间件开发工作，那估计网络编程对你来说会非常陌生，为了让你对它有一个直观的认知，我给你举一个例子。

假如我们在使用Dubbo构建微服务应用，Dubbo客户端在向服务提供者发起远程调用的过程中，需要告诉服务提供者服务名、方法名和参数。但这些参数是怎么在网络中传递的呢？服务提供者又怎么识别出客户端的意图呢？
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/25/9d/d612cbf8.jpg" width="30px"><span>防腐基</span> 👍（0） 💬（1）<div>讲的不够通俗易懂</div>2022-12-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/U5vvFI4v3jibf6uHbOFtkm1sBaXeLZnJicCOia0KW5KNb2KK06we5gkzJE7RiawfDzMAicHIpINUrTYfjrdZweQsuUA/132" width="30px"><span>Geek_1cd0c8</span> 👍（1） 💬（0）<div>问题：将数据写入网络最终通过socket的read，write接口吧，为什么还需要注册读写事件和开辟不属于socket的读写缓存

作者回复：
首先需要明确的是，通过Socket的write方法写入数据，并不需要注册写事件，那在什么时候需要注册写事件呢？

是在通过调用 SocketChannel的write方法，返回写入的字节数为0，但应用程序本次数据并未全部写入到通道中，这个是需要注册写事件，等待底层网络通知应用程序，该通道可以继续再写入，应用程序的事件选择器将会再次选择该通道，让应用程序可以继续写入

那在什么时候会出现写入的字节数为0呢，这个是与tcp的通信与拥塞控制有关，因为我们知道,tcp传输是 可靠传输，发送端将数据发送给接受端，如果接受端接受后，会通过ack机制告知发送端数据已接收，那发送端就可以把这些数据从底层的缓存区中删除，相反，如果接受端没有发送ack，则发生端底层会重新发送，直到收到ack，但发送端接收缓存区是有大小限制的，一旦缓存区满了，应用程序就无法通过该网络通道继续发送数据，注册写事件，就是等缓存区有空闲时，就会通知应用程序

那为什么Netty的Channel内部还要维护一个缓存区呢？这个缓存区，是为了存储应用程序待发送的数据，因为如果底层的缓存区满了后，未发送完的，需要有一个地方存储，这个缓存区就是用来存储这个用的，这个缓存区，还有一个作用就是确保数据的顺序发送，因为一个底层网络通道，会被多个线程共享用来发送数据，这样可以确保一个线程发送时，会锁这个队列，然后完整存储一个数据包，另外一个线程才可以继续写</div>2023-03-24</li><br/><li><img src="" width="30px"><span>Geek_b4cc9d</span> 👍（0） 💬（0）<div>这段代码背后蕴含的知识点是，事件注册是一次性的。这个说法有问题吧，如果selector没有主动移除监听事件，是会一直监听的。</div>2025-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/6c/5af32271.jpg" width="30px"><span>Dylan</span> 👍（0） 💬（0）<div>Java看得真累</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（0）<div>不是Java开发者，而且文章看有点懵～需要捋捋
</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（0）<div>滴 追番卡</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/bf/aed8ea2a.jpg" width="30px"><span>冠生！🤪</span> 👍（0） 💬（0）<div>netty 的nioEventLoopGroup 默认线程数不等于cpu核数，而是cpu核数*2啊。</div>2022-07-02</li><br/>
</ul>