你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课，我们已经构造出了MiniTomcat + MiniSpring的核心环境。但是我们知道，到目前为止，我们的MiniTomcat只实现了BIO模式，因此在高并发的情况下它的性能是不高的。我们能想到的一个解决办法就是把网络BIO换成NIO，作为MiniTomcat的扩展部分，同时我们也会探讨一下怎么用NIO实现网络接口。

## Java中的BIO与NIO

Java网络访问的传统模式是BIO（即在java.io包下的类），也就是线程要访问网络的时候，是等着网络I/O完成后，才接着运行线程后面的任务，你可以想象成几个任务串行的样子。从线程本身来看，就是在网络I/O这里阻塞住了，这也是BIO这个词的字面含义。因为线程阻塞住了，意味着一个线程只能响应一个网络请求，如果有多个网络请求就要开多个线程来处理。你可以看一下示意图。

![图片](https://static001.geekbang.org/resource/image/b9/34/b9047e18f17154acfd9ced0657bcf334.png?wh=1920x853)

在BIO模型下，accept和read都是阻塞的。没有网络连接请求的时候，accept方法死等，没有数据的时候，read方法死等。

从处理线程的角度来看，网络I/O很耗费时间，而线程还要无所事事地死等着，这是很浪费资源的。我们希望在等待网络I/O的过程中可以干点别的，然后回头看看网络I/O的结果。这个思路就像我们日常生活中在烧开水的时候，一般是去看看书、看看电视，等到某个时刻再回头看看水烧开了没有。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：thread不属于服务器吗？
本课第一张图，几个thread连接到server。“server”如果是服务器，那thread难道不是服务器端的吗？

Q2：selector.select(1000); 这行代码的行为是什么？
该行代码阻塞，一秒后阻塞结束，继续运行，是这样吗？
Q3：BIO、NIO用户量的分界线是什么？
文中谈到，BIO适合小用户量，NIO适合大用户量。那么，两者的分界线是什么？
Q4：《Tomcat 内核设计剖析》这本书怎么样？
京东上简单看了一下，作者好像没有特殊的经历，不知道这本书怎么样。
Q5：socketChannel与serverSocketChannel有什么区别？
搜“你可以看一个细化后的结构图”后找到的图中，有socketChannel和serverSocketChannel，两者有什么区别？ （文中有多个图的时候，图有个编号还是比较好的）

Q6：thread怎么从Multiplexer Selector读取数据？
搜“图示如下”后找到的图中，thread从Multiplexer Selector读取数据，具体是怎么实现的？轮询一个队列吗？ （哎呀，图最好有个编号啊）</div>2024-01-21</li><br/>
</ul>