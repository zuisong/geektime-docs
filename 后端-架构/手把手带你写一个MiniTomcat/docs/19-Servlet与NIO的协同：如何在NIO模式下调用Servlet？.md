你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们从原理出发探讨了Java的NIO模式，以及Tomcat如何实现NIO的。我们知道把Socket设置为NIO模式，通过注册事件的方法来进行读写处理，就相当于有一排信号灯，来了请求就会亮灯，还可以用不同的颜色区分不同的请求，比如连接、读、写等等，然后有一个Poller程序轮询，对不同的信号进行不同的处理。

这节课我们继续聊这个话题，看一下在NIO模式下如何调用Servlet。我们最后再来探讨一下MiniTomcat如何支持NIO。同样的，这节课也是对思路和原理的讨论，并没有对应的源码。

## NIO与Servlet的协同

我们来探讨支持NIO的另一件事情：Servlet协同。我们得先描述一下，前面说了，改成NIO模式之后，网络连接这一部分现在是非阻塞的模式了，主线程不用阻塞等待网络返回，而是可以接着做别的工作了。反映在程序上，我们现在拿到的不再是一个普通的Java socket了，而是SocketChannel。

但是Servlet的行为呢？按照通常的理解，是要阻塞地对数据进行读取，也就是说Servlet程序员写程序的时候，头脑里总是想象数据同步读写完成。这样我们就了解到了，现在网络连接和Servlet调用之间存在一个模式的差别。你可以结合我给出的示意图来理解。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/35/89/4c/791d0f5e.jpg" width="30px"><span>彩笔采购</span> 👍（1） 💬（1）<div>这两节很赞啊。“Tomcat NioEndPoint结构”还有“NIO模拟BIO的方式”让我有了很直观的了解</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（0） 💬（1）<div>老师，miniRedis有想法吗？最近一直在学redis源码，很想自己从头实现一个redis</div>2024-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：SocketChannel与Socket是什么关系吗？
Q2：第16课的代码链接打开后是第七课的链接
第16课的末尾放的链接是：
https:&#47;&#47;gitee.com&#47;yaleguo1&#47;minit-learning-demo&#47;tree&#47;geek_chapter16
点击以后，浏览器地址栏中显示的是：
https:&#47;&#47;gitee.com&#47;yaleguo1&#47;minit-learning-demo&#47;tree&#47;geek_chapter07
Q3：能否讲一下Tomcat中的设计模式？</div>2024-01-21</li><br/>
</ul>