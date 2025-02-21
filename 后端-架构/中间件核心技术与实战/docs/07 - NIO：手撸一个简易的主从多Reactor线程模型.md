你好，我是丁威。

中间件是互联网发展的产物，而互联网有一个非常显著的特点：集群部署、分布式部署。当越来越多的服务节点分布在不同的机器上，高效地进行网络传输就变得更加迫切了。在这之后，一大批网络编程类库如雨后春笋般出现，经过不断的实践表明，Netty框架几乎成为了网络编程领域的不二之选。

接下来的两节课，我们会通过对NIO与Netty的详细解读，让你对网络编程有一个更直观的认识。

## NIO和BIO模型的工作机制

NIO是什么呢？简单来说，NIO就是一种新型IO编程模式，它的特点是**同步**、**非阻塞**。

很多资料将NIO中的“N”翻译为New，即新型IO模型，既然有新型的IO模式，那当然也存在中老型的IO模型，这就是BIO，同步阻塞IO模型。

定义往往是枯燥的，我们结合实际场景看一下BIO和NIO两种IO通讯模式的工作机制，更直观地感受一下它们的差异。

MySQL的客户端(mysql-connector-java)采用的就是BIO模式，它的工作机制如下图所示：

![图片](https://static001.geekbang.org/resource/image/ef/c7/effdb1302033dc76c329315cece78fc7.jpg?wh=1920x1195)

我们模拟场景，向MySQL服务端查询表中的数据，这时会经过四个步骤。

第一步，应用程序拼接SQL，然后mysql-connector-java会将SQL语句按照MySQL通讯协议编码成二进制，通过网络API将数据写入到网络中进行传输。底层最终是使用Socket的OutputStream的write与flush这两个方法实现的。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/c6/36/70f2083c.jpg" width="30px"><span>open！？</span> 👍（2） 💬（1）<div>问题一 ：请求体很大 当前subreactor线程耗时会比较久 这时如果有别的channel来请求到当前subreactor线程会阻塞很久吧 不知道对不对</div>2022-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d2/03/aeaec5bf.jpg" width="30px"><span>呢喃</span> 👍（1） 💬（1）<div>写的非常好，对我很有帮助，感谢老师</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（4）<div>网络传输涉及带宽 就算你是nio  你也必须过带宽吧 木桶效应？</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（2） 💬（0）<div>建议参考文档，对照着学习，思考
https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;8697 -- 18 | 单服务器高性能模式：PPC与TPC
https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;8805 -- 19 | 单服务器高性能模式：Reactor与Proactor
</div>2022-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpibfWGQ563ARjRF6yGa7XoWOMn1ZmVyNldafdzZzvOOqf9gmhacx0utXu12BsGB0w22VSlXTInPg/132" width="30px"><span>InfoQ_09e721f0120c</span> 👍（0） 💬（0）<div>mainReactor只是用于建立连接，为什么要用线程池？一个线程不够吗？</div>2024-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/55/34055533.jpg" width="30px"><span>哲里哲里</span> 👍（0） 💬（0）<div>建议吧图文结合起来，比如那段文字是描述图中哪个过程</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（1）<div>老师同学好，全是java代码，不过注释还是比较清晰。
但是关于NioClient 类中

&#47;&#47; 再次发送消息，重复输出
buffer = ByteBuffer.allocate(1024);
buffer.put(&quot;hello server.&quot;.getBytes());
buffer.flip();
sc.write(buffer);

没明白，为什么在读取数据的代码里，还要写入数据？</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（0）<div>FYI
OP_CONNECT OP是Operation。</div>2022-07-11</li><br/>
</ul>