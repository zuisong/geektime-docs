你好，我是盛延敏，这里是网络编程实战第34讲，欢迎回来。

这一讲，我们延续第33讲的话题，继续解析高性能网络编程框架的字节流处理部分，并为网络编程框架增加HTTP相关的功能，在此基础上完成HTTP高性能服务器的编写。

## buffer对象

你肯定在各种语言、各种框架里面看到过不同的buffer对象，buffer，顾名思义，就是一个缓冲区对象，缓存了从套接字接收来的数据以及需要发往套接字的数据。

如果是从套接字接收来的数据，事件处理回调函数在不断地往buffer对象增加数据，同时，应用程序需要不断把buffer对象中的数据处理掉，这样，buffer对象才可以空出新的位置容纳更多的数据。

如果是发往套接字的数据，应用程序不断地往buffer对象增加数据，同时，事件处理回调函数不断调用套接字上的发送函数将数据发送出去，减少buffer对象中的写入数据。

可见，buffer对象是同时可以作为输入缓冲（input buffer）和输出缓冲（output buffer）两个方向使用的，只不过，在两种情形下，写入和读出的对象是有区别的。

这张图描述了buffer对象的设计。

![](https://static001.geekbang.org/resource/image/44/bb/44eaf37e860212a5c6c9e7f8dc2560bb.png?wh=946%2A316)  
下面是buffer对象的数据结构。

```
//数据缓冲区
struct buffer {
    char *data;          //实际缓冲
    int readIndex;       //缓冲读取位置
    int writeIndex;      //缓冲写入位置
    int total_size;      //总大小
};
```
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/17/19ea024f.jpg" width="30px"><span>chs</span> 👍（9） 💬（2）<div>老师不明白缓冲区为什么要这样设计。用两块内存当做缓冲区，一个用于接收数据，另一个用于发送数据。这两种方式的优缺点能说一下吗？</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（4） 💬（1）<div>老师，在tcp_connection.c文件tcp_connection_new方法创建channel时传入的data是tcp_connection类型，但在channel.c中channel_write_event_enable方法会直接从channel-&gt;data中取一个event_loop类型指针出来，阅读了整个tcp框架看起来没有找到直接传入event_loop类型的地方，这里是一个代码bug吗</div>2020-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/d3/80/dd0b26cb.jpg" width="30px"><span>罗兆峰</span> 👍（2） 💬（1）<div>第二题： 用户申请图片的时候可以申请一个GET 方法的request, GET URI version, URI 是图片相对服务器程序的地址，在服务器端程序使用io 函数read&#47;或者mmap 读取图片文件的内容， 并且写到connectedfd 中即可， http response 中的文件类型标记为image&#47;png。</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/a4/9d/95900f70.jpg" width="30px"><span>T------T</span> 👍（2） 💬（2）<div>老师好，发现一个memmem函数运行错误的Bug.
环境：Ubuntu18.04 GCC 10.3 glic 2.33
问题：返回void* 的memmem函数未声明，系统默认调用了返回int的memmem函数。返回值由int强转成char*,导致后续处理出现错误。
解决办法：在#include&lt;string.h&gt; 之前添加#define _GNU_SOURCE解决
参考：https:&#47;&#47;insidelinuxdev.net&#47;article&#47;a09522.html</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/4d/82/2bb78658.jpg" width="30px"><span>小家伙54</span> 👍（2） 💬（4）<div>老师，ubuntu20.4运行lib程序会出现段错误，这是怎么回事啊？

nuc@nuc-NUC8i5BEHS:~&#47;learn&#47;GeekTime&#47;net_prog&#47;yolanda&#47;build&#47;bin$ .&#47;http_server01
[msg] set epoll as dispatcher, main thread
[msg] add channel fd == 5, main thread
[msg] set epoll as dispatcher, Thread-1
[msg] add channel fd == 9, Thread-1
[msg] event loop thread init and signal, Thread-1
[msg] event loop run, Thread-1
[msg] event loop thread started, Thread-1
[msg] set epoll as dispatcher, Thread-2
[msg] add channel fd == 12, Thread-2
[msg] event loop thread init and signal, Thread-2
[msg] event loop run, Thread-2
[msg] event loop thread started, Thread-2
[msg] add channel fd == 6, main thread
[msg] event loop run, main thread
[msg] epoll_wait wakeup, main thread
[msg] get message channel fd==6 for read, main thread
[msg] activate channel fd == 6, revents=2, main thread
[msg] new connection established, socket == 13
[msg] connection completed
[msg] epoll_wait wakeup, Thread-1
[msg] get message channel fd==9 for read, Thread-1
[msg] activate channel fd == 9, revents=2, Thread-1
[msg] wakeup, Thread-1
[msg] add channel fd == 13, Thread-1
[msg] epoll_wait wakeup, Thread-1
[msg] get message channel fd==13 for read, Thread-1
[msg] activate channel fd == 13, revents=2, Thread-1
[msg] get message from tcp connection connection-13
段错误 (核心已转储)</div>2021-07-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/zkbuproauw8Ov7jjIGYertOQMLGtIzo26bc1m0CsnAHhQ96bpbh4A4jmdE2qm6lccpnr7nnDG93W6JUyDrCjPg/132" width="30px"><span>JeQer</span> 👍（1） 💬（1）<div>没有经过压力测试的服务器怎么能称为高性能呢?</div>2021-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/9d/4a/09a5041e.jpg" width="30px"><span>TinyCalf</span> 👍（1） 💬（1）<div>&#47;&#47;初始化一个request对象
struct http_request *http_request_new() {
    struct http_request *httpRequest = malloc(sizeof(struct http_request));
    httpRequest-&gt;method = NULL;
    httpRequest-&gt;current_state = REQUEST_STATUS;
    httpRequest-&gt;version = NULL;
    httpRequest-&gt;url = NULL;
    httpRequest-&gt;request_headers = malloc(sizeof(struct http_request) * INIT_REQUEST_HEADER_SIZE);
    httpRequest-&gt;request_headers_number = 0;
    return httpRequest;
}
这里的
httpRequest-&gt;request_headers = malloc(sizeof(struct http_request) * INIT_REQUEST_HEADER_SIZE);
是不是写错了 ；）</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/36/f62471c5.jpg" width="30px"><span>不诉离殇</span> 👍（1） 💬（2）<div>老师好，parse_http_request函数没太看懂，while循环中如果数据没收全，这个函数不会返回，那么底层的handle_read函数也不会返回?那就没有机会再将数据写到input_buffer了呀？这样不是就卡住了？</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（1） 💬（1）<div>c语言写bbs网站的年代，真的是太疯狂了，一个一个字符的print（哭脸）</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（1） 💬（6）<div>在ubuntu系统上一运行老师的程序就会出现“interrupted by signal 11: SIGSEGV”错误</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/11/d7e08b5b.jpg" width="30px"><span>dll</span> 👍（0） 💬（1）<div>好不容易看完了 打卡纪念一下</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/19/14dd81d9.jpg" width="30px"><span>铲铲队</span> 👍（0） 💬（1）<div>make_room 函数就是起这个作用的，如果右边绿色的连续空间不足以容纳新的数据，而最左边灰色部分加上右边绿色部分一起可以容纳下新数据，就会触发这样的移动拷贝，最终红色部分占据了最左边，绿色部分占据了右边，右边绿色的部分成为一个连续的可写入空间，就可以容纳下新的数据
----》个人觉得好像不用移动拷贝，数据一部分拷贝满writeable_size,剩余部分拷贝到front_spare_size。即循环缓冲，这样效率更高吧
</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e0/5d/c2867e36.jpg" width="30px"><span>肥磊</span> 👍（0） 💬（2）<div>老师，用wenbench测试出现段错误，是什么原因，
[msg] get message channel i==0, fd==7, Thread-1
[msg] activate channel fd == 7, revents=2, Thread-1
[msg] wakeup, Thread-1
[msg] add channel fd == 14, Thread-1
[msg] poll added channel fd==14, Thread-1
[msg] get message channel i==2, fd==14, Thread-1
[msg] activate channel fd == 14, revents=2, Thread-1
[msg] get message from tcp connection connection-14
[1]    2424 segmentation fault (core dumped)  .&#47;http_server01
</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（1）<div>哦 我知道了。front_spare_size是被读了一段之后产生的。</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（1）<div>老师你好 为什么要设计front_spare_size？或者说为什么存在front_spare_size？readIndex和writeIndex一开始不是从0开始的吗？</div>2021-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cabLXAUXiavXnEckAgo971o4l1CxP4L9wOV2eUGTyKBUicTib6gJyKV9iatM4GG1scz5Ym17GOzXWQEGzhE31tXUtQ/132" width="30px"><span>日就月将</span> 👍（0） 💬（2）<div>老师  http服务器request初始化的时候 http_header申请内存为什么还要乘128</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b9/7c/afe6f1eb.jpg" width="30px"><span>vv_test</span> 👍（0） 💬（1）<div>[msg] set poll as dispatcher, main thread
[msg] add channel fd == 4, main thread
[msg] poll added channel fd==4, main thread
[msg] set poll as dispatcher, Thread-1
[msg] add channel fd == 7, Thread-1
[msg] poll added channel fd==7, Thread-1
[msg] event loop thread init and signal, Thread-1
[msg] event loop run, Thread-1
[msg] event loop thread started, Thread-1
poll failed : Invalid argument (22)
[msg] set poll as dispatcher, Thread-2
[msg] add channel fd == 9, Thread-2
[msg] poll added channel fd==9, Thread-2
[msg] event loop thread init and signal, Thread-2
[msg] event loop run, Thread-2
poll failed : Invalid argument (22)</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/7d/774e07f9.jpg" width="30px"><span>study的程序员</span> 👍（0） 💬（1）<div>缓冲区可以设置为环形的，避免移动</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/8a/f4/a4243808.jpg" width="30px"><span>卡布猴纸</span> 👍（0） 💬（1）<div>老师你好，断连的tcpconnection和channel资源怎么管理的？</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/03/e9/6358059c.jpg" width="30px"><span>GalaxyCreater</span> 👍（0） 💬（1）<div>在buffer_socket_read函数用了char additional_buffer[INIT_BUFFER_SIZE]这个临时变量，那么预创建buffer来减少内存创建的开销就没效了，最少在读数据上的优化已经没效了</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/98/fa/d87a1432.jpg" width="30px"><span>I believe you</span> 👍（0） 💬（3）<div>老师，用你的程序在linux中使用webbench进行压力测试，每次请求都只有一个成功，其他全都失败，能请问下是什么原因吗</div>2020-07-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJQWW7Vp2GGMFwPwZdIG0Xbr4yv3lsToeCQ8Zuic9ibJibcsJXjkic5mH1ml2KA1ydyaLVZwmAt3iaic8Kg/132" width="30px"><span>Geek_e5533e</span> 👍（0） 💬（2）<div>请问下课件示例代码的github地址？想好好学习下。</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（0） 💬（1）<div>希望老师加一个客户端请求到服务器响应的全过程流程图包括tcp连接和应用程序处理的流程😁</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>嗯，对于第二个问题，因为我是从C++语言开始进入编程的，老师的C代码确实很多都是面向对象的。

很多模块，比如tcp_connection，对应的头文件中声明的函数，第一个参数都是tcp_connection指针，这就相当于this指针。而相应的以&quot;_new&quot;结尾的函数就相当于C++中的构造函数。
而结构体里的函数指针，我把它理解为了实现了继承C++中的虚拟基类或类似于java中实现了一个接口。

画UML图的时候，完全可以用C++的术语进行。</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/c1/54ef6885.jpg" width="30px"><span>MoonGod</span> 👍（0） 💬（1）<div>如果发现当前 channel 没有注册 WRITE 事件，并且当前 tcp_connection 对应的发送缓冲无数据需要发送，就直接调用 write 函数将数据发送出去。
老师好，这里没有理解，为啥不能做成无论有没有write事件都统一往发送缓冲区写呢，之后如果没有write事件，就再注册一个就好了不是？</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（2）<div>实在学不动了，我想抄袭老师的创意自己写一个框架，然后慢慢该吧
(◦`~´◦)</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>老师的的c代码看上去是一种享受。
逻辑很清晰，很佩服函数命名。

以前我们缓冲区是用的循环，避免频繁的挪动数据，不过要处理好溢出的情况。

文中好像拼错了单词。
“只需要看到 http_request 和 http_responsde 结构。”
“创建了一个 buffe 对象”</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（0）<div>第二个问题 才是把我考到了 我感觉现在我对设计模式的理解并不深,但是我现在感受特深的一点就是单一职责原理 buffer类才套接字的处理 tcpconnect应用层面的处理,而且最近在工作中我也是尝试着画流程图 把每个功能进行细分 分到一个流程分支里面只处理一个逻辑</div>2019-10-25</li><br/>
</ul>