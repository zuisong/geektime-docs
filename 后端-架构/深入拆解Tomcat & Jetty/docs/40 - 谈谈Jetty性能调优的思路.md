关于Tomcat的性能调优，前面我主要谈了工作经常会遇到的有关JVM GC、监控、I/O和线程池以及CPU的问题定位和调优，今天我们来看看Jetty有哪些调优的思路。

关于Jetty的性能调优，官网上给出了一些很好的建议，分为操作系统层面和Jetty本身的调优，我们将分别来看一看它们具体是怎么做的，最后再通过一个实战案例来学习一下如何确定Jetty的最佳线程数。

## 操作系统层面调优

对于Linux操作系统调优来说，我们需要加大一些默认的限制值，这些参数主要可以在`/etc/security/limits.conf`中或通过`sysctl`命令进行配置，其实这些配置对于Tomcat来说也是适用的，下面我来详细介绍一下这些参数。

**TCP缓冲区大小**

TCP的发送和接收缓冲区最好加大到16MB，可以通过下面的命令配置：

```
 sysctl -w net.core.rmem_max = 16777216
 sysctl -w net.core.wmem_max = 16777216
 sysctl -w net.ipv4.tcp_rmem =“4096 87380 16777216”
 sysctl -w net.ipv4.tcp_wmem =“4096 16384 16777216”
```

**TCP队列大小**

`net.core.somaxconn`控制TCP连接队列的大小，默认值为128，在高并发情况下明显不够用，会出现拒绝连接的错误。但是这个值也不能调得过高，因为过多积压的TCP连接会消耗服务端的资源，并且会造成请求处理的延迟，给用户带来不好的体验。因此我建议适当调大，推荐设置为4096。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（18） 💬（1）<div>但是我们的实验中测试发现，最大线程数为 6 时最佳，这是不是矛盾了？
不矛盾，老师已经说了，这个案例里面没有IO操作。
有IO操作的时候，用这个公式：(线程IO阻塞时间+线程CPU时间) &#47; 线程CPU时间</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（6） 💬（2）<div>1.课后习题不矛盾。老师课上说了实力是纯CPU密集型没有IO阻塞，这种情况下线程数比核数多一点就好。正式环境，要连接各种缓存，数据库，第三方调用都会IO阻塞。IO阻塞越多可开的线程数越多。

老师好!服务器分配的端口号只是服务监听的端口号，然后服务器作为客户端调用别的服务时，会随机占用一个端口号建立TCP连接是么(同样需要fd)?rmi技术无法穿透防火墙，理由是端口号不固定随机生成。rmi技术服务提供方的端口号会变的意思么?不太理解谢谢李老师，课程快结束了不舍</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/9f/8dbd9558.jpg" width="30px"><span>逆流的鱼</span> 👍（0） 💬（1）<div>系统相关调节和servlet容器强相关？</div>2019-08-13</li><br/><li><img src="" width="30px"><span>Geek_xbye50</span> 👍（0） 💬（1）<div>测试中的最大线程数指的是接入线程类似netty的boss eventloop，50到500处理线程类似work eventloop！猜测是这样？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（0）<div>不矛盾呀，针对于CPU密集型的计算，一般建议都是略大于当前的cpu核数，如果是IO密集型的计算，就需要根据实际的计算公司来套用了。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/11/a7/6ee3f556.jpg" width="30px"><span>Wx</span> 👍（0） 💬（0）<div>案例中, 是不是应该把`server.setHandler(new HelloWorld());`?</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/09/2171f9a3.jpg" width="30px"><span>小白哥哥</span> 👍（0） 💬（0）<div>别用tcp_tw_recycle，用tcp_tw_reuse</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7f/d1/d9de3d0a.jpg" width="30px"><span>桂桂</span> 👍（0） 💬（0）<div>hi，老师你好，碰到一个问题解决不了，inetaccess白名单无法获取实际client ip进行拦截，这个咋整，各种配置调了一个星期没解决，烦请提供一些idea, thanks</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（0） 💬（0）<div>课后思考：这里的例子只是cpu消耗，所以稍微大于或等于核心数比较合适。正常情况下会有各种io阻塞等，线程数大概公式可以是：（io时间+cpu时间）&#47; cpu时间</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/bf/a44cde46.jpg" width="30px"><span>lorancechen</span> 👍（0） 💬（0）<div>无io操作时，工作线程设置成和cpu核数相等不是最少的线程上下文切换吗，为何是1.5倍吞吐最高呢？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（0）<div>限制 Jetty 的任务队列非常重要。默认情况下，队列是无限的
Jetty 9.4 好像不是无限队列吧</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/4c/2cefec07.jpg" width="30px"><span>静水流深</span> 👍（0） 💬（0）<div>看来老师对4096这个数情有独钟啊，哈哈😄</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/6b/ea60cde5.jpg" width="30px"><span>郭浩</span> 👍（0） 💬（0）<div>老师您好：
Acceptor 的个数 accepts 应该设置为大于等于 1，并且小于等于 CPU 核数。
这个是在哪里配置呢？有没有示例分享出来呢？</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/9c/4e7a76a4.jpg" width="30px"><span>Winter</span> 👍（0） 💬（0）<div>李老师好：tomcat的应用发生内存溢出为何会导致tomcat假死，我的理解是tomcat的应用内存溢出应该直接释放内存，不影响其他请求才对，期望老师回复，感谢哈。</div>2019-10-13</li><br/>
</ul>