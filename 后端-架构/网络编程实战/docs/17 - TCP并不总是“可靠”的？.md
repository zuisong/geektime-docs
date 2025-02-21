你好，我是盛延敏，这里是网络编程实战第17讲，欢迎回来。

在前面一讲中，我们讲到如何理解TCP数据流的本质，进而引出了报文格式和解析。在这一讲里，我们讨论通过如何增强读写操作，以处理各种“不可靠”的场景。

## TCP是可靠的？

你可能会认为，TCP是一种可靠的协议，这种可靠体现在端到端的通信上。这似乎给我们带来了一种错觉，从发送端来看，应用程序通过调用send函数发送的数据流总能可靠地到达接收端；而从接收端来看，总是可以把对端发送的数据流完整无损地传递给应用程序来处理。

事实上，如果我们对TCP传输环节进行详细的分析，你就会沮丧地发现，上述论断是不正确的。

前面我们已经了解，发送端通过调用send函数之后，数据流并没有马上通过网络传输出去，而是存储在套接字的发送缓冲区中，由网络协议栈决定何时发送、如何发送。当对应的数据发送给接收端，接收端回应ACK，存储在发送缓冲区的这部分数据就可以删除了，但是，发送端并无法获取对应数据流的ACK情况，也就是说，发送端没有办法判断对端的接收方是否已经接收发送的数据流，如果需要知道这部分信息，就必须在应用层自己添加处理逻辑，例如显式的报文确认机制。

从接收端来说，也没有办法保证ACK过的数据部分可以被应用程序处理，因为数据需要接收端程序从接收缓冲区中拷贝，可能出现的状况是，已经ACK的数据保存在接收端缓冲区中，接收端处理程序突然崩溃了，这部分数据就没有办法被应用程序继续处理。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（18） 💬（4）<div>看到后面我好像理解了我上面那个提问,当崩溃重启过后是重新三次握手建立连接,创建新的套接字,只是在网络上传输的包,因为是通过ip地址和端口方式进行的寻址,所以新连接上去的客户端会接收到之前还没接收到的包,然后新连接的客户端没有这些包的tcp分组信息所以就会给服务器端(对端)发送一个RST</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/1d/ec173090.jpg" width="30px"><span>melon</span> 👍（17） 💬（3）<div>最后的例子没有触发SIGPIPE，是因为老师例子设计的有点儿瑕疵。client 在不断的发送数据，server 则每次接受数据之后都 sleep 一会，也就导致接收速度小于发送速度，进而导致 server 终止的时候接收缓冲区还有数据没有被读取，server 终止触发 close 调用，close 调用时如果接收缓冲区有尚未被应用程序读取的数据时，不发 FIN 包，直接发 RST 包。client 每次发送数据之后 sleep 2秒，再试就会出SIGPIPE 了。</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（9） 💬（2）<div>我的电脑，结果也是一样的，
第二个问题，服务器正常关闭，客户端应该是受到了fin包，read返回eOF,wirte返回rst</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/23/28311447.jpg" width="30px"><span>盘尼西林</span> 👍（9） 💬（1）<div>没有理解 reset by peer 和 broken pipe 的区别。。</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/62/536aef06.jpg" width="30px"><span>tim</span> 👍（5） 💬（4）<div>&gt;&gt;&quot;但是，发送端并无法获取对应数据流的 ACK 情况&quot;
对上面这段话不理解，TCP 的 ACK不是带着序号的吗？发送端根据这个序号能计算出是哪次发送的ACK。
哪位大牛能解释一下吗？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（2）<div>老师，你文章的案例默认fd都是阻塞的吧，如果是非阻塞的话，返回的n &lt; 0 不一定是错误啊</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（2） 💬（1）<div>error(1, 0, &quot;usage: reliable_client01 &lt;IPaddress&gt;&quot;);这个error函数，具体是什么作用？</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（2） 💬（1）<div>老师 我提一个read直接感知FIN包的疑问哈:

我停留在 stdin这里 等我输入完之后，就能调用read感知到对端已经关闭了呀？ 是因为等到stdin之后，再感知是不是太晚了呀？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（1） 💬（2）<div>第二题  客户端--------服务器

1.  客户端发送FIN包，处于发送缓冲区的数据会逐一发送（可能通过一次或多次write操作发送），FIN包处于这段数据的末尾，当数据到达接收端的接收缓冲区时，FIN起到了一个结束符的作用，当接收端接收数据时遇到FIN包，read操作返回EOF通知应用层。然后接收端返回一个ACK表示对这次发送的确认。（此时客户端进入FIN_WAIT1，服务端进入CLOSE_WAIT状态）

2.  客户端接收到ACK之后，关闭自己的发送通道，客户端此时处于半关闭状态。等待服务器发送FIN包。

  (客户端进入FIN_WAIT2状态)

3.  服务端发送FIN包，同上类似处于发送缓冲区的内容会连同FIN包一起发过去，当客户端接收成功后同时将FIN解析为EOF信号使得上层调用返回。（客户端进入TIME_WAIT状态 服务端进入LAST_ACK状态）

4. 客户端等待2MSL的时间，在此期间向服务器发送ACK。如果丢包进行重传。如果服务器收到ACK后 服务器进入CLOSED状态 客户端也进入CLOSED状态。

5. 连接关闭
我想问一下  如果最后一次挥手一直丢包  在2MSL的时间内都没到  TCP会咋办  会重置计时器么 还是就不管了直接关闭呢</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/60/eae432c6.jpg" width="30px"><span>yusuf</span> 👍（1） 💬（1）<div># uname -a
Linux tst 3.10.0-957.21.3.el7.x86_64 #1 SMP Tue Jun 18 16:35:19 UTC 2019 x86_64 x86_64 x86_64 GNU&#47;Linux
# 
# .&#47;reliable_client01 127.0.0.1
good
peer connection closed
# 
# .&#47;reliable_client01 127.0.0.1
bad
bad
bad2
peer connection closed
# 
# .&#47;reliable_client02 127.0.0.1
send into buffer 19 
send into buffer -1 
send error: Connection reset by peer (104)
</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/03/9c/5a0b8825.jpg" width="30px"><span>Bin Watson</span> 👍（0） 💬（1）<div>在内核4.15.0-158-generic版本中，在服务器关闭后，客户端是返SIGPIPE错误。</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（0） 💬（1）<div>当对应的数据发送给接收端，接收端回应 ACK，存储在发送缓冲区的这部分数据就可以删除了，但是，发送端并无法获取对应数据流的 ACK 情况，也就是说，发送端没有办法判断对端的接收方是否已经接收发送的数据流，如果需要知道这部分信息，就必须在应用层自己添加处理逻辑，例如显式的报文确认机制


不是很明白，为什么发送端无法获取对应数据流的ACK情况？  不是收到对方回的ACK包了吗？</div>2021-07-23</li><br/><li><img src="" width="30px"><span>highfly029</span> 👍（0） 💬（1）<div>老师好，请教个问题，对于网络中断导致的故障，我们的处理是服务端因为timeout而主动close连接，在timeout之前的这段时间内，服务端会不断的发送消息，如果保证这段时间的消息不丢失？</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/15/c5dc2b0d.jpg" width="30px"><span>James</span> 👍（0） 💬（1）<div>想问下接收端为什么接受不到ACK,你说从应用层的角度看，网络层保证可靠性就可以了，应用层还需要再次保证吗</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>write触发SIGPIPE后，程序会自动退出，还是继续执行？？</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/54/85/ab5148ce.jpg" width="30px"><span>duckman</span> 👍（0） 💬（1）<div>本系列的代码中send 和 write 都有用，搜了一下, 确实可以替换

There should be no difference. Quoting from man 2 send:

The only difference between send() and write() is the presence of flags. With zero flags parameter, send() is equivalent to write().

https:&#47;&#47;stackoverflow.com&#47;questions&#47;1100432&#47;performance-impact-of-using-write-instead-of-send-when-writing-to-a-socket</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d5/a4/5dd93357.jpg" width="30px"><span>Passion</span> 👍（0） 💬（1）<div>老师 我的数据通过send函数写入内核发送缓冲区没问题， 我抓取发送的端口 发现与我写入的数据对不上 怎么定位  比如我写入缓冲区100sql  发出去的只找到80个sql</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fa/84/f01d203a.jpg" width="30px"><span>Simple life</span> 👍（0） 💬（1）<div>有个疑问，FIN包这些底层操作，怎么与READ,WRITE有关，不是TCP底层直接处理好了吗？read,write不是操作用户应用层的数据吗？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（0） 💬（1）<div>第一题我的服务器关闭，但是客户端并没有打印Connection reset by peer，而是打印send into buffer 4294967295,同时打印send error。是不是版本的原因。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d5/70/93a34aa5.jpg" width="30px"><span>Geek_76f04f</span> 👍（0） 💬（1）<div>老师您好，我在运行第二个程序的时候，当关闭服务端的时候，客户端很大的概率不会收到RST，相反会持续的write，直到wireshark抓包显示窗口为0 。 请教老师为什么客户端收不到RST，窗口为0是不是因为内核缓冲区满了？</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/cb/ede92cd5.jpg" width="30px"><span>Alex</span> 👍（0） 💬（1）<div>SIGPIPE的处理对出错处理很重要，深有体会</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/fe/c451a509.jpg" width="30px"><span>吴向兵</span> 👍（0） 💬（1）<div>老师，你好，想问一下，epoll能感知到tcp连接的异常吗？</div>2020-03-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/86QEF74Mhc6ECbBBMr62hVz0ezOicI2Kbv8QBA7qR7KepeoDib9W6KLxxMPuQ24JGusvjC03NNr8uj8GyK0DxKiaw/132" width="30px"><span>HerofH</span> 👍（0） 💬（1）<div>老师您好，我想请问一个关于感知到RST后的一个处理问题。
如前所述，如果对端调用shutdown(SD_RD)关闭读端，那么此时本端向对端进行写操作后收到对端的RST；而如果对端是突然崩溃后重启，由于本端不知道对端已经崩溃，此时本端发送的数据到达对端，也会收到RST。
针对这两种情况的处理方式，根据我的理解，前者应该是关闭本端的写，而后者则应该直接关闭本端到对端的连接。那么如何区分这两种情况呢？我感觉在本端的反应都是同样的read返回，然后errno被设置为ECONNRESET，我该怎么知道到底是哪种情况呢？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>假如让你设计一个网络通信协议，你会怎么设计？</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（0） 💬（1）<div>老师好，有个问题想请教下。
有进程A和B(在同一物理机下)，A会监听B的连接。在我对进程A kill -2后，B与A的连接一直保持着ESTABILISH,  进程A重启时，绑定监听端口会出现端口被占用的异常。

这种情况是否表示B没有收到A的fin包，所以才一直保持着ESTABILISH的状态？ 这种情况应该怎么解决？

如果我给进程B加上一个对A的心跳检测，能否解决这个问题？

期待老师能给我答疑</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/02/fcab58d1.jpg" width="30px"><span>JasonZhi</span> 👍（0） 💬（1）<div>老师你好，文章的最后一个例子还有一些疑问。我的理解是对于一个已经关闭的socket ，执行两次write ，第一次write 会导致对端返回RST，第二次write 由于对收到RST的socket 执行写操作，会触发SIGPIPE。但是为什么例子却说会返回peer reset的错误呢？是不是我哪里理解错了。</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/02/fcab58d1.jpg" width="30px"><span>JasonZhi</span> 👍（0） 💬（2）<div>老师你好，我在linux环境下测试最后一个例子时，在客户端代码的count--后面加上sleep(4)，那么关闭服务端后，连续向服务端写入就会返回PIPIE错误，并且会收到SIGPIPIE信号，能解释其中原因吗？
贴上代码：
 while (count &gt; 0) {
        n_written = send(socket_fd, msg, strlen(msg), 0);
        fprintf(stdout, &quot;send into buffer %ld \n&quot;, n_written);

        if (n_written &lt;= 0) {
            error(1, errno, &quot;send error&quot;);
            return -1;
        }
        count--;

        sleep(4);
    }</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（0） 💬（1）<div>老师，最后一行的Connection reset by peer是从哪里打印输出的？是内核协议栈打印输出到终端上的吗？在程序代码中没找到对应的printf语句</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>其实我也一直想问 比如 我客户端突然崩溃了 然后再启动客户端连接上服务器 到底是新建立一个链接 还是老的连接 并且发送rst?</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/81/1864f266.jpg" width="30px"><span>石将从</span> 👍（0） 💬（2）<div>这篇读了几遍还是很懵，很多概念理不清楚，不知道对端到底是服务器端还是客户端，都混淆了</div>2019-09-09</li><br/>
</ul>