你好，我是盛延敏，这里是网络编程实战第27讲，欢迎回来。

我在前面两讲里，分别使用了fork进程和pthread线程来处理多并发，这两种技术使用简单，但是性能却会随着并发数的上涨而快速下降，并不能满足极端高并发的需求。就像第24讲中讲到的一样，这个时候我们需要寻找更好的解决之道，这个解决之道基本的思想就是I/O事件分发。

关于代码，你可以去[GitHub](https://github.com/froghui/yolanda)上查看或下载完整代码。

## 重温事件驱动

### 基于事件的程序设计: GUI、Web

事件驱动的好处是占用资源少，效率高，可扩展性强，是支持高性能高并发的不二之选。

如果你熟悉GUI编程的话，你就会知道，GUI设定了一系列的控件，如Button、Label、文本框等，当我们设计基于控件的程序时，一般都会给Button的点击安排一个函数，类似这样：

```
//按钮点击的事件处理
void onButtonClick(){
  
}
```

这个设计的思想是，一个无限循环的事件分发线程在后台运行，一旦用户在界面上产生了某种操作，例如点击了某个Button，或者点击了某个文本框，一个事件会被产生并放置到事件队列中，这个事件会有一个类似前面的onButtonClick回调函数。事件分发线程的任务，就是为每个发生的事件找到对应的事件回调函数并执行它。这样，一个基于事件驱动的GUI程序就可以完美地工作了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（15） 💬（1）<div>worker thread 和 reactor thread之间怎么进行数据传递？是要利用队列+锁吗？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（12） 💬（4）<div>1：事件驱动模型的设计思想是啥？
事件驱动模型的设计的思想是，一个无限循环的事件分发线程在后台运行，一旦做了某种操作触发了一个事件，这个事件就会被放置到事件队列中，事件分发线程的任务，就为这个发生的事件找到对应的事件回调函数并执行它。
这里有个疑问，事件分发线程怎么找到事件的回调函数，并调用它的？

2：事件驱动模型的优势是啥？
事件驱动的好处是占用资源少，效率高，可扩展性强，是支持高性能高并发的不二之选。
老师好，请问占用资源少这个结论是怎么得出来的？

3：IO网络通信是怎么实现事件驱动模型的？
通过使用 poll、epoll 等 I&#47;O 分发技术，可以设计出基于套接字的事件驱动程序，从而满足高性能、高并发的需求。

4：Reactor模型是啥玩意？
Reactor模型（中文叫做反应堆模型）也就是事件驱动模型或者是 Event loop 模型。
这个模型的核心有两点。
第一，它存在一个无限循环的事件分发线程，或者叫做 reactor 线程、Event loop 线程。这个事件分发线程的背后，就是 poll、epoll 等 I&#47;O 分发技术的使用。
第二，所有的 I&#47;O 操作都可以抽象成事件，每个事件必须有回调函数来处理。acceptor 上有连接建立成功、已连接套接字上发送缓冲区空出可以写、通信管道 pipe 上有数据可以读，这些都是一个个事件，通过事件分发，这些事件都可以一一被检测，并调用对应的回调函数加以处理。
5：Reactor模型——解决了空闲连接占用资源的问题，Reactor线程只负责处理 I&#47;O 相关的工作，业务逻辑相关的工作都被裁剪成一个一个的小任务，放到线程池里由空闲的线程来执行。当结果完成后，再交给反应堆线程，由Reactor线程通过套接字将结果发送出去。
所以，这个模式性能更优。

6：阻塞IO+多进程——实现简单，性能一般
7：阻塞IO+多线程——相比于阻塞IO+多进程，减少了上下文切换所带来的开销，性能有所提高。
8：阻塞IO+线程池——相比于阻塞IO+多线程，减少了线程频繁创建和销毁的开销，性能有了进一步的提高。
9：Reactor+线程池——相比于阻塞IO+线程池，采用了更加先进的事件驱动设计思想，资源占用少、效率高、扩展性强，是支持高性能高并发场景的利器。</div>2019-11-24</li><br/><li><img src="" width="30px"><span>fxzhang</span> 👍（10） 💬（1）<div>老师可否讲解linux下如何开发的，最近想换工作，但是之前都在windows下面开发，想自学一下linux下是如何开发的，但是有一种找不到开头不知道该怎么学习的感觉，很无力</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/86/d34800a4.jpg" width="30px"><span>heyman</span> 👍（6） 💬（1）<div> reactor 线程无限循环，有点像轮询，效率不会很低吗？</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/4d/2cc44d9a.jpg" width="30px"><span>刘忽悠</span> 👍（5） 💬（3）<div>没太理解epoll反应堆模型，和直接eopll的区别是什么？
不知道我这么理解对不对，一般使用epoll，假如新连接建立，注册cfd读事件，当事件触发，接着在主线程里面读出来，然后处理，接着发送；epoll反应堆模式是不是仅仅只是在注册事件的时候加了一个对应的回调函数，当事件触发，然后调用回调去处理？相当于统一了一下接口？
对于老师说的reactor+threadpool不知道理解的对不对，我个人理解是，当有新连接建立，因为监听描述符注册的是acceptor事件，这时候这个事件触发，触发之后注册新的描述符cfd的read事件，当cfd的读事件触发，这时候在reactor线程（主线程）里面调当初注册的回调函数来处理读事件，读出来之后，然后注销cfd的读事件，这时候把读出来的内容封装成Task，放到线程池的Task队列，通知线程池的工作线程——有任务了，唤醒一个线程对任务进行处理，处理完成之后，这时候注册cfd的写事件，然后work线程处理完成，一般情况下写缓冲区都是可以写，所以这时候在reactor线程里面，cfd的写事件被触发，这时候在reactor线程里面调用对应的回调函数把数据发送过去，接着然后注销写事件，注册读事件，继续监听客户端请求。这样一来，业务逻辑都在线程池里面去做，然后读，写都是通过在主线程，也就是reactor线程里面调用对应的回调函数来完成。
不知道这么理解reactor模式+线程池对不对？</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（5） 💬（1）<div>第一遍看完这篇文章 我就感受颇深 尤其是事件触发 这个模式 然后就想到工作当中的用到的skynet框架底层就是采用事件驱动,某个服务有数据达到 就去触发对应的服务,然后再回想工作当中很多逻辑都抽象成事件,通过一个主循环检测时间然后来触发对应的事件！
更重要的一点,专栏下的代码我全部是自己手动实现了一遍 还用上了gdb很开心 很满足
第27讲和第24讲 应该重点学习,这两讲都是很重要的理论基础</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/d6/6101dbd7.jpg" width="30px"><span>CPP</span> 👍（3） 💬（1）<div>C语言要是没两把刷子，买了也是浪费钱。再调试也得建立再看懂的基础上......</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/88/34c171f1.jpg" width="30px"><span>herongwei</span> 👍（2） 💬（1）<div>这篇文章，多了很多生动的图片，感觉干货满满啊，哈哈，希望后面的课程，也能多加点对应的图片就更好了。</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/84/07f0c0d6.jpg" width="30px"><span>supermouse</span> 👍（1） 💬（1）<div>思考题第一道：https:&#47;&#47;github.com&#47;YoungYo&#47;yolanda&#47;blob&#47;master&#47;chap-27&#47;poll-server-onethread-homework.c 这是修改后的代码
思考题第二道： onMessage 方法就是处理 decode-compute-encode 逻辑的吧？</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（1） 💬（2）<div>使用多线程有线程池，使用多进程有进程池吗？</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（1） 💬（1）<div>我看到别人的代码用到了老师说的这个思想，在接收消息它采用的是分发订阅模式   通过订阅者的回调来接收消息  没有特定的recv接口露给外界  这种设计思想老师怎么看</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（4）<div>之前由于忙着买房子 落下了很多课程 现在都在追,不过不管是追还是慢慢跟 我都会再好好复习的</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（0） 💬（1）<div>Synchronous Event Demultiplexer（同步事件分离器）  是这个吗</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（0） 💬（1）<div>不会。这里不是轮询哦，轮询是消耗cpu时间的，这里是系统提供的事件驱动，看似在无限循环，其实这个时候cpu被调度干其他事了。
老师，这里系统提供的事件驱动是指什么？既然不是无限轮训，那是怎么样执行呢？</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（0） 💬（1）<div>有一个问题，有一个无线轮询的线程会对CPU的消耗有影响吗？</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（1）<div>老师你好 这边开始有点晕了。代码里贴的event_loop反应堆就是基于系统轮询（如slect&#47;poll&#47;epoll）+非阻塞封装的吗</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2d/37/f8733b67.jpg" width="30px"><span>S</span> 👍（0） 💬（2）<div>请问老师，你程序第一句打印add channel fd == 4, main thread，为什么第一个fd是4而不是3？ 0，1，2分别代表输入，输出，错误。那么fd:3被谁占用了？</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（0） 💬（1）<div>netty也是用的reactor模型</div>2020-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/48/3ab39c86.jpg" width="30px"><span>insist</span> 👍（0） 💬（1）<div>老师，请问在reactor+work thread模式下，reactor线程负责分发客户端连接的acceptor事件，这样的话reactor看起来的作用是监听客户端连接。但是前面说到acceptor是用来监听客户端连接的，怎么理解呢</div>2020-10-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUzv6S9wroyXaoFIwvC1mdDiav4BVS4BbPTuwtvWibthL5PyMuxFNicY06QJMZicVpib7E88S19nH4I9Q/132" width="30px"><span>木子皿</span> 👍（0） 💬（1）<div>老师，这一讲直接抛出来来了一个框架，感觉好难啊，无法理解了</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（0） 💬（1）<div>看了第三遍，想知道为什么把IO压力给监听现成，其他线程做cpu计算会好一点?这不是代表主线程变为瓶颈了么</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/4e/5c3153b2.jpg" width="30px"><span>知行合一</span> 👍（0） 💬（1）<div>一个分发线程负责几万个套接字连接，那真正的从套接字读和往套接字写都是阻塞的是么？</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9f/8d/56f338b8.jpg" width="30px"><span>赵玉炜</span> 👍（0） 💬（1）<div>老师您好，请问一下不同浏览器会有不同的限制吗？
我仿照您的代码实现了一个基于epoll的http服务器。
它在360极速浏览器，旧版的ie浏览器上可以正确显示。
但是在chrome浏览器就会出现这样的错误。
client ip: 10.10.10.1, port : 5118
fd_read_to_buf(socket_fd, input);
GET &#47; HTTP&#47;1.1
Host: 10.10.10.135:8080
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla&#47;5.0 (Windows NT 10.0; WOW64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;83.0.4103.61 Safari&#47;537.36
Accept: text&#47;html,application&#47;xhtml+xml,application&#47;xml;q=0.9,image&#47;webp,image&#47;apng,*&#47;*;q=0.8,application&#47;signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

httpRequest-&gt;current_state == REQUEST_STATUS
buf-&gt;read_index= 0, buf-&gt;write-&gt;index=454
REQUEST_STATUS done!
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
httpRequest-&gt;current_state == REQUEST_HEADERS
parse_http_request.
epoll_http: malloc.c:2394: sysmalloc: Assertion `(old_top == initial_top (av) &amp;&amp; old_size == 0) || ((unsigned long) (old_size) &gt;= MINSIZE &amp;&amp; prev_inuse (old_top) &amp;&amp; ((unsigned long) old_end &amp; (pagesize - 1)) == 0)&#39; failed.
Aborted (core dumped)

请问老师我应该如何修改呢</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（0） 💬（1）<div>请问老师，这里的     
&#47;&#47; 开启监听    
tcp_server_start(tcpServer);     
应该怎么理解？
</div>2020-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jry2KckuIjxsMjErZNELxVibVYtKW4H9MDjnZeyJHsaU1IdCrU3ssFOTb0eXjnQ6ymvV76JmW6aozfaM3NIYDPA/132" width="30px"><span>Geek_Jolin</span> 👍（0） 💬（1）<div>Flag，一定要把这块硬骨头啃下来。</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（1）<div>struct event_loop {
    int socketPair[2];
}

请问为什么要创建这两个AF_UNIX套接字？
使用的场景是什么？</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/34/9a/1587bc6f.jpg" width="30px"><span>JDY</span> 👍（0） 💬（1）<div>老师，你这个代码能不能把头文件也放上啊，要不然怎么跑？</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/69/0ddda908.jpg" width="30px"><span>满怀</span> 👍（0） 💬（1）<div>老师，学到这里开始有些看不懂了，因为虽然之前的代码会引一些其他的lib，但是还算可以接收，这一次的代码，一下子有很多东西，event_loop等等。</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/54/4e/3d5de8e3.jpg" width="30px"><span>LIFE__MM</span> 👍（0） 💬（1）<div>https:&#47;&#47;github.com&#47;froghui&#47;yolanda&#47;issues&#47;8
这个问题是运行服务器程序成功后，开启第一个客户端时报错Segmentation fault (core dumped)，我通过GDB找出来dump原因，但是第一次遇到这样的问题不知道如何解决，希望老师帮助一下，谢谢！</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/54/4e/3d5de8e3.jpg" width="30px"><span>LIFE__MM</span> 👍（0） 💬（1）<div>https:&#47;&#47;github.com&#47;froghui&#47;yolanda&#47;issues&#47;8
这是我在写完所有源文件后cmake make 收到的警告，一直无法解决，希望老师可以帮助一下，谢谢</div>2019-10-31</li><br/>
</ul>