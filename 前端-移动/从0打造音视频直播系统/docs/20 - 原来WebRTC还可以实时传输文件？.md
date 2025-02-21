在[上一篇文章](https://time.geekbang.org/column/article/127360)中我向你介绍了在 WebRTC 中如何传输非音视频数据，并通过实现一个1对1实时聊天的例子向你展示了如何使用RTCDataChannel 对象进行文本数据的传输。

其实利用 WebRTC 的 RTCDataChannel 对象，不光可以实现 1 对 1 的实时聊天，你还可以利用它进行**实时的文件传输**。

实时文件传输是一个非常有用的工具，尤其是通过浏览器进行实时文件传输就更加有价值，因为**它不会受到操作系统或开发语言的影响**，所以你可以在任何不同的操作系统上进行文件的传输，非常方便。

举个例子，由于工作的需要，你可能经常需要在不同的操作系统间切来切去（一会儿在 Windows 系统上开发，一会儿在 Linux 系统上开发，一会儿又在 Mac 系统上开发），当你想将 Windows上的文件传到 Linux系统上时就特别不方便，但如果可以通过浏览器传输文件的话，那将会大大提高你的工作效率。

## 基本原理

在WebRTC中，**实时文件的传输与实时文本消息传输的基本原理是一样的，都是使用 RTCDataChannel 对象进行传输**。但它们之间还是有一些差别的，一方面是**传输数据的类型**不一样，另一方面是**数据的大小**不一样。下面我们就从这两方面来具体讨论一下。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/45/87f44f50.jpg" width="30px"><span>xw616525957</span> 👍（5） 💬（1）<div>页面被关掉的情况可以考虑用浏览器做个缓存，比如indexedDB.将发送端和接收端的状态和file数据都保存下来，下次进room的时候再恢复上传。

这里有个问题，在一对多的情况下，发送端是不是要维护每个接收端的收发状态。这种情况是不是通过server中转一层比较好，这样可以利用cdn来加速接收端的下载速度。
</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ea/47/6f73cde6.jpg" width="30px"><span>Happy任</span> 👍（0） 💬（1）<div>可以将续传chunk序号缓存到localStorage中吧，不过这样用户换浏览器就无法续传了。请问老师有其他解决方案吗？</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（0） 💬（2）<div>有办法恢复被中断的传输：将传输的连接、状态信息保存下来，浏览器再次启动时加载这些信息。</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/52/d67f276d.jpg" width="30px"><span>轩爷</span> 👍（0） 💬（0）<div>下次再进行连接时，接收方获取本地最后一个块的偏移量，通过信令服务器转发给发送端，发送端监听到message，拿到偏移量，经过计算，开始断点续传。</div>2020-07-02</li><br/>
</ul>