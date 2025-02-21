你好，我是盛延敏，这里是网络编程实战第7讲，欢迎回来。

上一篇文章中，我们讲了UDP。很多同学都知道TCP和UDP，但是对本地套接字却不甚了解。

实际上，本地套接字是IPC，也就是本地进程间通信的一种实现方式。除了本地套接字以外，其它技术，诸如管道、共享消息队列等也是进程间通信的常用方法，但因为本地套接字开发便捷，接受度高，所以普遍适用于在同一台主机上进程间通信的各种场景。

那么今天我们就来学习下本地套接字方面的知识，并且利用本地套接字完成可靠字节流和数据报两种协议。

## 从例子开始

现在最火的云计算技术是什么？无疑是Kubernetes和Docker。在Kubernetes和Docker的技术体系中，有很多优秀的设计，比如Kubernetes的CRI（Container Runtime Interface），其思想是将Kubernetes的主要逻辑和Container Runtime的实现解耦。

我们可以通过netstat命令查看Linux系统内的本地套接字状况，下面这张图列出了路径为/var/run/dockershim.socket的stream类型的本地套接字，可以清楚地看到开启这个套接字的进程为kubelet。kubelet是Kubernetes的一个组件，这个组件负责将控制器和调度器的命令转化为单机上的容器实例。为了实现和容器运行时的解耦，kubelet设计了基于本地套接字的客户端-服务器GRPC调用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>将本地套接字的文件unlink后没有任何操作，难道在bind本地套接字到文件的过程中会自动创建文件吗</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/49/96/7523cdb6.jpg" width="30px"><span>spark</span> 👍（0） 💬（1）<div>stream_server:
clilen = sizeof(cliaddr); 
if ((connfd = accept(listenfd, (struct sockaddr *) &amp;cliaddr, &amp;clilen)) &lt; 0) { 
if (errno == EINTR) error(1, errno, &quot;accept failed&quot;); &#47;* back to for() *&#47; 
else error(1, errno, &quot;accept failed&quot;); }
这段程序有问题吧? 不明白怎么back to for()?
谢谢</div>2020-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/wwM75BhyU43UYOJ6fZCZgY6pfNPGHHRlooPLQEtDGUNic4aLRHWmBRTpIiblBAFheUVm9Sw8HWAChcFsnVM2sd5Q/132" width="30px"><span>Geek_d6f50f</span> 👍（0） 💬（1）<div>老师，为什么UDP本地套接字，在服务器端，接收数据和发送数据共用一块缓冲区，先接收，再把接收缓冲区的数据sendto到客户端，这时候发送错误，但是如果接收和发送各自的缓冲区，就不会出错，这是为什么呢？</div>2020-06-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5kv7IqibneNnMLqtWZQR5f1et8lJmoxiaU43Ttzz3zqW7QzBqMkib8GCtImKsms7PPbWmTB51xRnZQAnRPfA1wVaw/132" width="30px"><span>Geek_63bb29</span> 👍（0） 💬（1）<div>老师。看了第八部分Docker那里，好像有些明白了。TCP是监听端口，这里的话，服务器是监听本地文件，是这样吧【之前提了一条问题】</div>2020-06-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5kv7IqibneNnMLqtWZQR5f1et8lJmoxiaU43Ttzz3zqW7QzBqMkib8GCtImKsms7PPbWmTB51xRnZQAnRPfA1wVaw/132" width="30px"><span>Geek_63bb29</span> 👍（0） 💬（1）<div>老师，对于本地套接字，我的理解是：通过本地套接字的客户端和服务端，对各进程管理的内存进行信息交换，但是没能理解 &#47;var&#47;lib&#47;unixstream.sock这个文件的作用，因为我用TCP、UDP交换信息的思路，觉着信息流没有经过 这个文件呀，还请指点一下，谢谢老师。</div>2020-06-20</li><br/><li><img src="" width="30px"><span>Ray</span> 👍（0） 💬（1）<div>你可以看到 16～22 行将本地数据报套接字 bind 到本地一个路径上，然而 UDP 客户端程序是不需要这么做的。本地数据报套接字这么做的原因是，它需要指定一个本地路径，以便在服务器端回包时，可以正确地找到地址；
----------------------------
关于上文中的内容，想请教一下老师，为什么TCP的本地客户端不需要bind到一个地址？</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/76/c69b7fe5.jpg" width="30px"><span>youngitachi</span> 👍（0） 💬（1）<div>不知道为啥write函数使用的nbytes，我这里使用sizeof获取的话多交互几次数据显示就会有问题。
改成strlen函数有就好了</div>2020-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/78/4f0cd172.jpg" width="30px"><span>妥协</span> 👍（0） 💬（2）<div>本机通过 127.0.0.1地址通信时，走网络协议栈的全部流程吗？</div>2020-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（0） 💬（1）<div>window下，没有本地套接字枚举，是不是会自动根据IP判断本地地址的话，就走本地套接字</div>2020-05-07</li><br/><li><img src="" width="30px"><span>ray</span> 👍（0） 💬（3）<div>老师您好，
请问什么时机应该使用sock_stream，sock_data呢？
会有这个问题是因为，本地传输没有可靠性问题需要解决，两者速度都很快。既然如此，本地传输又会什么要分sock_stream，sock_data呢？

谢谢老师的解答^^</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/03/e9/6358059c.jpg" width="30px"><span>GalaxyCreater</span> 👍（0） 💬（2）<div>使用本地套接字和直接读写本地文件有什么不同；记得管道也会创建文件的，他们有什么不一样的</div>2020-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLTPmSgD6QSgicqsbzibiau9xWSYgdsvYlnVWBg91ibHQBYg39MT4O3AV5CHlJlVUvw9Ks9TZEmRvicfTw/132" width="30px"><span>InfoQ_0ef441e6756e</span> 👍（0） 💬（2）<div>老师。udp客户端bind 还是没理解，server坚挺的哪个文件，回复的时候发给那个文件不就行了么？</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/73/51/aaedc2a6.jpg" width="30px"><span>treasure</span> 👍（0） 💬（1）<div>我看代码为什么客户端和服务端都bind这个函数，客户端不加bind可以吗？</div>2020-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NTSD503ibERiba4wcsoiaezDrjLMOVVlAlliagHc6ic3icWFfuzaFWaHwuULQDo22mPiabicImFTB7ial82OuBD96bl4RTQ/132" width="30px"><span>Geek_d4f974</span> 👍（0） 💬（1）<div>运行server后，在netstat -lx中可以查看到，但是在&#47;tmp文件夹中没有生成unixstream.sock文件</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/c4/28b58d33.jpg" width="30px"><span>曹绍坚</span> 👍（0） 💬（1）<div>&quot;另外还要明确一点，这个本地文件，必须是一个“文件”，不能是一个&quot;目录&quot;；&quot;
这么说本地套接字是不是不适合实现多并发的服务器？</div>2019-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4HlmmWfWicNmo3x3HKaOwz3ibcicDFlV5xILbILKGFCXbnaLf2fZRARfBdVBC5NhIPmXxaxA0T9Jhg/132" width="30px"><span>Geek_Wison</span> 👍（0） 💬（2）<div>老师您好，这篇文章的第一段代码的第33～36行的if else是不是写得不太对？</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/1c/d323b066.jpg" width="30px"><span>knull</span> 👍（0） 💬（2）<div>老师，能不能说说两种unix套接字的使用场景？tcp和udp有明显的特征差异。但是，unix的好像差别不是特别明显。我想象中，本地的话，丢包可能基本没有吧？仅仅是为了与tcp、udp对应，还是有特别的意义？</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3f/7d/6fb0d4e9.jpg" width="30px"><span>fee</span> 👍（0） 💬（1）<div>计算地址长度 len = offset（struct sockaddr_un， sun_family） + strlen（.sun_family）公司代码</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div> #include&quot;..&#47;my_head.h&quot; 
 #define LISTENQ 10 
 #define BUFFSIZE 1024 
 int 
 main( int argc, char* argv[] ) { 
     if ( argc != 2 ) { 
         error( 1, 0, &quot;useage unixstreamserver &lt;local path&gt;&quot; ); 
     } 
 15     socklen_t clilen; 
 16     struct sockaddr_un cliaddr; 
 17     struct sockaddr_un serveraddr; 
 18     int sockfd = socket( AF_LOCAL, SOCK_DGRAM, 0 ); 
 19     if ( sockfd &lt; 0 ) { 
 20         error( 1, errno, &quot;socket create failed&quot; ); 
 21     } 
 22  
 23     char* local_path = argv[1]; 
 24     unlink( local_path ); 
 25     bzero( &amp;serveraddr, sizeof( serveraddr ) ); 
 26     serveraddr.sun_family = AF_LOCAL;   strcpy( serveraddr.sun_path,local_path ); 
 27     if ( bind( sockfd, ( struct sockaddr*  ) &amp;serveraddr, sizeof( serveraddr ) ) &lt; 0 ) { 
 28         error( 1, errno, &quot;bind failed&quot; );
 29     } 
 30 &#47;*
 31     if ( listen( listenfd, LISTENQ ) &lt; 0 ) {
 32         error( 1, errno, &quot;listen failed&quot; );
 33     }
 34 *&#47;
 35 
 36     clilen = sizeof( cliaddr );
 42     char buf[BUFFSIZE];
 43     while( 1 ) {
 44         bzero( buf, sizeof( buf ) );
 45         if ( recvfrom( sockfd, buf, BUFFSIZE, 0, ( struct sockaddr*  ) &amp;cliaddr, &amp;clilen ) == 0 ) {
 46             printf( &quot;client quit&quot; );
 47             break;
 48         }
 49         printf( &quot;Recevie: %s&quot;, buf );
 50         char send_line[MAXLINE];
 51         sprintf( send_line, &quot;Hi, %s&quot;, buf );
 52         int nbytes = sizeof( send_line );
 53         if ( sendto( sockfd, send_line, nbytes, 0,  ( struct sockaddr* ) &amp;cliaddr, clilen ) != nbytes ) {
 54             error( 1, errno, &quot;write error&quot; );
 55         }
 56     }
 57 
 58     exit( 0 );
 59 } 
我这个代码本地数据报套接字 服务器端接收到数据过后发送时就报错如下
ubuntu@VM-0-17-ubuntu:~&#47;network&#47;local_socket$ .&#47;dgrams .&#47;dgram.sock 
Recevie: 1
.&#47;dgrams: write error: Transport endpoint is not connected 就不知道怎么解决了                       </div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/98/2be9d17b.jpg" width="30px"><span>破晓^_^</span> 👍（0） 💬（1）<div>那些拼命要老师贴代码带git上的有点懒啊，这本来就是一门注重实践的课程，编程不实践你能有收获？不妨自己敲一下收获更深呢？各位兄弟。</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/23/a379f47d.jpg" width="30px"><span>Time Machine</span> 👍（0） 💬（0）<div>请问下代码去哪儿获取啊？ &quot;lib&#47;common.h&quot; 是个啥包啊</div>2022-11-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/88nXicqmkJWm3IXVfPfGQSk8SKIBVKjuC4qhzaCkf5Ud88uvKgS4Vf5AzCJ1uaFO0gpPnxdh4CowfhpxV1kSbXw/132" width="30px"><span>lixin</span> 👍（0） 💬（0）<div>可不可以多个客户端连接一个服务端。那一个客户端退出会引起服务端的退出么</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>本地套接字一般也叫做 UNIX 域套接字，本地套接字是一种特殊类型的套接字，和 TCP&#47;UDP 套接字不同。TCP&#47;UDP 即使在本地地址通信，也要走系统网络协议栈，而本地套接字，严格意义上说提供了一种单主机跨进程间调用的手段，减少了协议栈实现的复杂度，效率比 TCP&#47;UDP 套接字都要高许多（可以理解为读本地文件）</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（0） 💬（0）<div>1. 连接不上，因为客户端还没有赋予权限。 
2. 因为服务器做了判断 当read()==0的时候 也就是客户端退出的时候，服务器也退出了。
    原因就是服务器在代码逻辑层做了一个退出的判断。
3.客户端在连接时会报错，错误提示是“Protocol wrong type for socket (91)</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/13/ab/d73e25de.jpg" width="30px"><span>Geek_wannaBgeek</span> 👍（0） 💬（0）<div>打卡打卡</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>本地套接字是一种特殊类型的套接字，和 TCP&#47;UDP 套接字不同。TCP&#47;UDP 即使在本地地址通信，也要走系统网络协议栈，而本地套接字，严格意义上说提供了一种单主机跨进程间调用的手段，减少了协议栈实现的复杂度，效率比 TCP&#47;UDP 套接字都要高许多。类似的 IPC 机制还有 UNIX 管道、共享内存和 RPC 调用等。
这里的描述，“减少了协议栈实现的复杂度”，没理解本地套接字，具体还走不走网络的协议栈？如果走应该仍然属于网络通信的范畴，如果不走，他具体怎么实现的，和共享内存有什么本质区别？
这里确实刷新了认知，之前认为进程间通信，必须要走网络协议的，哪怕是单机上的两个进程也是这样。其实只要他们能交流信息，走不走网络没什么必然联系，共享内存这个就容易理解和实现，不过还是需要约定双方交流的方式，否则信息能获取但不理解也不成。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/4f/3b24dccc.jpg" width="30px"><span>岸超</span> 👍（0） 💬（0）<div>1:普通用户应该是没有 &#47;var&#47;lib&#47;unixstream.sock 这个文件的读写权限的，root创建一般会是700的形式。可以手动chmod添加权限，使得普通用户也可以访问该本地套接字。
2:这个问题在 流式套接字和数据报两种情况应该是不同的吧。流式套接字中应该是复用了socket close的语义，进程退出会关闭fd，而对端的read在tcp连接时，收到fin分节会返回0，这里在本地套接字上应该是模拟了对端close时的这种效果。但是数据报套接字是不存在这种情况下返回0的实现的，故而这段代码其实不会生效，实际效果展示中也没有退出
3:问题三肯定会报错，虽不会三次握手，但内核肯定无法把这两种套接字在底层连接起来，但具体错误未知。</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/fc/379387a4.jpg" width="30px"><span>ly</span> 👍（0） 💬（0）<div>问题一：
个人感觉客户端没有权限也可以连接，这个sock文件是服务端创建的，客户端仅仅是向这个套接字发送、接受数据而已；类推到tcp的套接字，服务端只要监听一个端口，防火墙放开端口，默认情况下是对客户端无限制的（所以客户端都可以连接）。
问题二：
这个服务端随着客户端的退出而退出，应该是服务端的代码所致，代码中read方法正常情况下是会阻塞，客户端发完消息这个就会解除阻塞，但是客户端退出，这个read方法读不到数据，进入break语句，main方法结束。
问题三：
服务端以数据包接受，客户端用字节流发送（有点好玩）；由于本地套接字的字节流没有三次握手，我想客户端还是可以把数据发给服务端的，至于服务端的接收情况......实在编不下去了，请老师指教！</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>(ps: 老师讲的是真的好 对比分析都有)</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>1. 文件是服务端服务器上的 服务端本地监听的 服务端需要权限 客户端应该不需要吧 所以应该可以连接成功吧

2. 看代码是read返回值是0的时候退出的

3. 一个是socket_stream 一个是datagram 两个格式不一样 应该会报错吧</div>2019-08-16</li><br/>
</ul>