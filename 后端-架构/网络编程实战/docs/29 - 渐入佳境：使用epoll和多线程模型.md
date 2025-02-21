你好，我是盛延敏，这里是网络编程实战第29讲，欢迎回来。

在前面的第27讲和第28讲中，我介绍了基于poll事件分发的reactor反应堆模式，以及主从反应堆模式。我们知道，和poll相比，Linux提供的epoll是一种更为高效的事件分发机制。在这一讲里，我们将切换到epoll实现的主从反应堆模式，并且分析一下为什么epoll的性能会强于poll等传统的事件分发机制。

## 如何切换到epoll

我已经将所有的代码已经放置到[GitHub](https://github.com/froghui/yolanda)上，你可以自行查看或下载。

我们的网络编程框架是可以同时支持poll和epoll机制的，那么如何开启epoll的支持呢？

lib/event\_loop.c文件的event\_loop\_init\_with\_name函数是关键，可以看到，这里是通过宏EPOLL\_ENABLE来决定是使用epoll还是poll的。

```
struct event_loop *event_loop_init_with_name(char *thread_name) {
  ...
#ifdef EPOLL_ENABLE
    yolanda_msgx("set epoll as dispatcher, %s", eventLoop->thread_name);
    eventLoop->eventDispatcher = &epoll_dispatcher;
#else
    yolanda_msgx("set poll as dispatcher, %s", eventLoop->thread_name);
    eventLoop->eventDispatcher = &poll_dispatcher;
#endif
    eventLoop->event_dispatcher_data = eventLoop->eventDispatcher->init(eventLoop);
    ...
}
```

在根目录下的CMakeLists.txt文件里，引入CheckSymbolExists，如果系统里有epoll\_create函数和sys/epoll.h，就自动开启EPOLL\_ENABLE。如果没有，EPOLL\_ENABLE就不会开启，自动使用poll作为默认的事件分发机制。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（19） 💬（1）<div>在ET的情况下，write ready notification只会在套接字可写的时候通知一次的话，那个时候应用还没准备好数据，等到应用准备好数据时，却又没有通知了，会不会导致数据滞留发不出去？这种情况是怎么解决的呢？</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/f8/b13674e6.jpg" width="30px"><span>LiYanbin</span> 👍（14） 💬（1）<div>源代码看起来有点花了点时间，将这部分的代码从抽离了出来，便于大家跟踪代码理解，同时写了简单的makefile。代码地址：https:&#47;&#47;github.com&#47;kevinrsa&#47;epoll_server_multithreads 。如有不妥，联系删除</div>2020-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/97/9e342700.jpg" width="30px"><span> JJ</span> 👍（7） 💬（2）<div>边缘条件，当套接字缓冲区可写，会不断触发ready notification事件，不是应该条件触发才是这样吗？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（5） 💬（2）<div>如果应用程序只读取了 50 个字节，边缘触发就会陷入等待；
这里的陷入等待是什么意思呢</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/04/7904829d.jpg" width="30px"><span>张三说</span> 👍（5） 💬（2）<div>老师，一直没搞懂ET和LT的性能区别，仅仅因为LT会多提醒一些次数就与ET相差明显的性能吗？一直很纠结这个问题</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/19/c058bcbf.jpg" width="30px"><span>流浪地球</span> 👍（5） 💬（1）<div>细读了下老师git上的代码，套接字都是设置为非阻塞模式的，但并没有对返回值做判断处理，看上去好像是阻塞式的用法，求解？</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（1） 💬（2）<div>27章以及以后源代码的难度提升了一个等级了。看了相当吃力呀。</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（1） 💬（1）<div>老师，这个就绪列表是建立在事件集合之上的对吧。</div>2020-04-16</li><br/><li><img src="" width="30px"><span>ray</span> 👍（1） 💬（2）<div>老师好，
针对第2题，目前想到onMessage函数应该要注意，如果当前程序无法处理该通知，应该要想办法再次注册该事件。

只是具体程序实现就不知道应该怎么写了，可能还要请老师说明一下 哈哈XD

谢谢老师^^</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6d/46/e16291f8.jpg" width="30px"><span>丁小明</span> 👍（1） 💬（2）<div>为什么 socket已经有缓冲区了，应用层还要缓冲区呢，比如发送，socket也会合并发送</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（1）<div>看到CMake我就完全懵逼。。。。</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（1） 💬（3）<div>老师能不能为这个框架写一份README.md，我对这个实现很感兴趣</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b9/7c/afe6f1eb.jpg" width="30px"><span>vv_test</span> 👍（0） 💬（1）<div>性能对比第一点，是否可以这样理解。select、poll在用户态声明的事件拷贝(我在这里理解拷贝，不是注册，因为下一次调用依旧要传入)到内核态，大量操作copy的情况下耗时不容小觑。而epoll是已经注册到对应的epoll实例。主要是省去了这个copy的时间</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（3）<div>有个疑问，这个程序与下一章的HTTP服务器的设计，处理连接的时候，服务器什么时候会关闭对端的连接？
是不断与客户端交互，客户端发送关闭请求才关闭；还是处理完客户端的请求后，发送响应，再关闭</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/aa/49bbb007.jpg" width="30px"><span>нáпの゛</span> 👍（0） 💬（1）<div>老师，所以不删除写事件，就不需要重新注册是吗？每次缓冲区由满变成可写都会通知一次，是这样理解吗？</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9b/2d/f7fca208.jpg" width="30px"><span>fedwing</span> 👍（0） 💬（1）<div>第一个角度是事件集合。在每次使用 poll 或 select 之前，都需要准备一个感兴趣的事件集合，系统内核拿到事件集合，进行分析并在内核空间构建相应的数据结构来完成对事件集合的注册。而 epoll 则不是这样，epoll 维护了一个全局的事件集合，通过 epoll 句柄，可以操纵这个事件集合，增加、删除或修改这个事件集合里的某个元素。要知道在绝大多数情况下，事件集合的变化没有那么的大，这样操纵系统内核就不需要每次重新扫描事件集合，构建内核空间数据结构。
  老师，这个不是很理解，看了下，前面的epoll实例代码，epoll_wait时，还是需要传入一个events（看起来是初始化了下）的，这个是做什么用的，我理解，epoll对象本身不是已经有它所关联的事件信息了吗（通过epoll_ctrl add进去）</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9b/2d/f7fca208.jpg" width="30px"><span>fedwing</span> 👍（0） 💬（1）<div>老师，请问下，我看用poll实现里的结构配图，可以用threadpool来解耦具体业务逻辑，epoll里的配图，没有这个，其实也是可以加的吧，本质上线程池解耦业务这部分应该是通用吧，只是在事件触发， 事件分发机制上的差别吧？</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（0） 💬（1）<div>文稿中的框架示意图，我看到main reactor 和 sub reactor都各自运行了epoll,请问是否各自处理不同的socket？ 如果处理了相同的socket会发生什么吗？</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>看了github上面的lib目录，很多文件里的函数没有介绍，注释也不多。</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>终于看到github地址了，建议每节课都写一下链接地址，没代码的章节除外。</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/e8/7734b8d3.jpg" width="30px"><span>P</span> 👍（0） 💬（1）<div>只提一点，所有关于Reactor的图片都不太准确。流程应该是client-&gt;Acceptor-&gt;Poller(select&#47;poll&#47;epoll)，然而文章中所有的Acceptor都放在了后面，令人疑惑。</div>2023-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/ce/23f2e185.jpg" width="30px"><span>Running man</span> 👍（0） 💬（0）<div>event_loop.c编译链接不上pthread库，有哪位朋友知道如何修改cmakelist，gcc版本是11.2.0 ubuntu系统版本是11.2.0，对应内核版本5.15.0-41</div>2022-09-30</li><br/>
</ul>