你好，我是盛延敏，这是网络编程实战的第10讲，欢迎回来。

在前面的基础篇里，我们对网络编程涉及到的基础知识进行了梳理，主要内容包括C/S编程模型、TCP协议、UDP协议和本地套接字等内容。在提高篇里，我将结合我的经验，引导你对TCP和UDP进行更深入的理解。

学习完提高篇之后，我希望你对如何提高TCP及UDP程序的健壮性有一个全面清晰的认识，从而为深入理解性能篇打下良好的基础。

在前面的基础篇里，我们了解了TCP四次挥手，在四次挥手的过程中，发起连接断开的一方会有一段时间处于TIME\_WAIT的状态，你知道TIME\_WAIT是用来做什么的么？在面试和实战中，TIME\_WAIT相关的问题始终是绕不过去的一道难题。下面就请跟随我，一起找出隐藏在细节下的魔鬼吧。

## TIME\_WAIT发生的场景

让我们先从一例线上故障说起。在一次升级线上应用服务之后，我们发现该服务的可用性变得时好时坏，一段时间可以对外提供服务，一段时间突然又不可以，大家都百思不得其解。运维同学登录到服务所在的主机上，使用netstat命令查看后才发现，主机上有成千上万处于TIME\_WAIT状态的连接。

经过层层剖析后，我们发现罪魁祸首就是TIME\_WAIT。为什么呢？我们这个应用服务需要通过发起TCP连接对外提供服务。每个连接会占用一个本地端口，当在高并发的情况下，TIME\_WAIT状态的连接过多，多到把本机可用的端口耗尽，应用服务对外表现的症状，就是不能正常工作了。当过了一段时间之后，处于TIME\_WAIT的连接被系统回收并关闭后，释放出本地端口可供使用，应用服务对外表现为，可以正常工作。这样周而复始，便会出现了一会儿不可以，过一两分钟又可以正常工作的现象。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（35） 💬（2）<div>net.ipv4.tcp_tw_recycle是客户端和服务器端都可以复用，但是容易造成端口接收数据混乱，4.12内核直接砍掉了，老师是因为内核去掉了所以没提了嘛</div>2019-08-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/VZ96qlUtD0jEib5gn8mVthSm6sLJ66o1YRn4OgmCseGWBPw055Cw6sYyib5fRFiabnTzl2Nhuomc3qIhgRibkH6iakw/132" width="30px"><span>雷神的盛宴</span> 👍（34） 💬（7）<div>net.ipv4.tcp_tw_reuse 要慎用，当客户端与服务端主机时间不同步时，客户端的发送的消息会被直接拒绝掉</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/10/723a149c.jpg" width="30px"><span>何某人</span> 👍（34） 💬（6）<div>老师，那么通过setsockopt设置SO_REUSEADDR这个方法呢？网上资料基本上都是通过设置这个来解决TIME_WAIT。这个方法有什么优劣吗？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fb/1a/57480c9c.jpg" width="30px"><span>AnonymousUser</span> 👍（22） 💬（2）<div>TIME_WAIT的作用：
1） 确保对方能够正确收到最后的ACK，帮助其关闭；
2） 防迷走报文对程序带来的影响。
TIME_WAIT的危害：
1） 占用内存；
2） 占用端口。</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（17） 💬（5）<div>文中的问题有个前提，必须是监听的端口。我看有评论提到80,8080这种服务，是否只能同时访问一次？答案是否定的。因为网络中的服务分为监听端口和连接端口，当建立一个连接之后，监听端口是不被占用的，此时会用一个新的端口来建立连接，而且就算是新的端口，一个TCP连接也是（客户端ip,客户端端口 ，服务端ip，服务端端口）共同决定的，不冲突。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（12） 💬（1）<div>Reuse只适用于连接发起方（C&#47;S 模型中的客户端），但目前要解决的是服务端连接不足问题，这个方法要如何发挥作用呢？</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/cd/d85c6361.jpg" width="30px"><span>丹枫无迹</span> 👍（11） 💬（3）<div>由于引入了时间戳，我们在前面提到的 2MSL 问题就不复存在了，因为重复的数据包会因为时间戳过期被自然丢弃。
这个没理解，为什么 2MSL 问题就不存在了？老师能解释下吗？</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/33/03/3f2df287.jpg" width="30px"><span>吴光庆</span> 👍（10） 💬（2）<div>为什么是2MSL，不是3 MSL，4 MSL。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/02/fcab58d1.jpg" width="30px"><span>JasonZhi</span> 👍（7） 💬（1）<div>SO_REUSEADDR和SO_REUSEPORT可以详细说下作用吗？有点迷糊，文章都没有说明这两个参数，评论区就冒出一大堆关于这两个参数的评论。</div>2019-09-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epKJlW7sqts2ZbPuhMbseTAdvHWnrc4ficAeSZyKibkvn6qyxflPrkKKU3mH6XCNmYvDg11tB6y0pxg/132" width="30px"><span>pc</span> 👍（6） 💬（1）<div>先说点其他的吧：看完了基础篇，收获了很多，也更加期待后面的内容（本来就是冲着time_wait和epoll来到这个课程）。当然其中也遇到很多问题，其中也在评论区提了两个。本来以为这么长时间了老师也不会再回复了，周末一看，竟然回复了我的问题！其实一边是开心，另一边是得到答案的开心（其实自己也搜索过，但是感觉搜到文章都不是我想问的内容）。

【提问啦～】
1、看到评论区的“通过setsockopt设置SO_REUSEADDR这个方法”，感觉和net.ipv4.tcp_tw_reuse选项的作用也很像，都是端口复用，只是后者是在安全可控的基础上---这样理解对吗？
2、老师在文中说的“过了2MLS这个时间之后，主机 1 就进入 CLOSED 状态”，我自己还是没有总结出答案，是评论区所说的“去时ACK的最大存活时间（MSL）+来时FIIN的最大存活时间（MSL） = 2MSL”这个原因吗？
3、TIME_WAIT=2MLS和TCP_TIMEWAIT_LEN有啥关系？是：TIME_WAIT实际上是由TCP_TIMEWAIT_LEN控制，然后只不过其值约等于2MLS来控制迷走报文的消亡 这样么？
4、文中说TCP_TIMEWAIT_LEN、net.ipv4.tcp_tw_reuse都是linux的选项，但是客户端来说的话，有android、ios、windows各种系统吧？是每个系统都有类似的控制选项么？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/62/f873cd8f.jpg" width="30px"><span>tongmin_tsai</span> 👍（6） 💬（5）<div>老师，我有疑问的是，IP包中TTL每经过一次路由就少1，那么2MSL怎么确保可以一定大于TTL的？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（6） 💬（4）<div>老师好，想问个问题，一般我们服务器上运行一个服务，比如tomcat，zk这种，然后监听8080或2181端口，这时候外部直连（不再经过web服务器转发）的话，虽然有很多连接但服务端应该都是只占用一个端口，也就是说netstat -anp命令看到的本机都是ip+固定端口，那么此时如果服务端主动关闭一些连接的话，也会有大量time_wait问题对吧，但此时好像并没有消耗更多端口，那这个影响对于服务端来说是什么呢？老师讲的出现大量time_wait应该都是在客户端的一方吧，因为客户端发起请求会占用一个新端口，主动关闭到time_wait阶段就相当于这个新的端口一直被占用。我还有个疑问是，这种大量time_wait在连接数多的情况下是肯定会出现的，是不是可以从减少连接的方向去解决问题呢，比如用连接池这种技术可以解决吗？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/8e/eecebc1a.jpg" width="30px"><span>Geek_9a0180</span> 👍（4） 💬（2）<div>印象中是当一端关闭socket连接，另一端如果尝试从TCP连接中读取数据，则会报connect reset，如果偿试向连接中写入数据，则会报connect reset by peer，好像和老师说的正相反，还请老师帮忙解答一下，谢谢：）</div>2019-08-23</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9zRdkKuXMKh30ibeludlAsztmR4rD9iaiclPicOfIhbC4fWxGPz7iceb3o4hKx7qgX2dKwogYvT6VQ0g/132" width="30px"><span>Initiative Thinker</span> 👍（3） 💬（1）<div>复用后的套接字，如何恢复旧连接的FIN呢？</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9c/a2/06604a01.jpg" width="30px"><span>列夫托尔斯泰克洛伊来文列夫斯德夫</span> 👍（3） 💬（1）<div>这个可控优化的方法没明白，是复用端口的意思吗？不过复用端口数据不混乱了？</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（3） 💬（1）<div>老师好，我又2个问题不明白：
1 为什么说time_wait会占用过多端口，难道不是占用socket而已吗？比如一个server与多个client建立多个连接，对于server而言只会占用一个端口吧

2 什么是报文的自然消亡，指的是报文发送到对方或报文正常丢弃吗？然后对连接化身这段看不明白</div>2019-08-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIVSkMRsMAXJ0sqO9CPwQmQyZ4l0xf0Bn4kIrD8jd2EOaOfHdibmIEhCexC9g9UTgh6tH9tAvd5Mlw/132" width="30px"><span>Geek_9edd4f</span> 👍（2） 💬（1）<div>“第二是对端口资源的占用，一个 TCP 连接至少消耗一个本地端口。要知道，端口资源也是有限的，一般可以开启的端口为 32768～61000 ，也可以通过net.ipv4.ip_local_port_range指定，如果 TIME_WAIT 状态过多，会导致无法创建新连接。这个也是我们在一开始讲到的那个例子。”
这里不是很理解，服务端提供服务应该就只用一个端口号吧？而客户端请求服务应该也是只使用一个端口号吧？普通个人客户就发起一个请求只用一个端口号，为什么会出现端口号不够用的情况？难道指的的为客户服务的代理服务器可能会端口号不够用吗？因为代理服务器要处理来自成千上万的客户请求，需要选择不同的端口号为客户服务，将请求发给服务器吗？</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/8d/a2a4e97e.jpg" width="30px"><span>Atong</span> 👍（2） 💬（3）<div>老师有一个问题请教：
已知的知识点：
1. TCP的四次挥手，只有主动断开的那端才会出现TIME_WAIT状态。
2. 一个socket连接，是由一个四元祖标识，client_ip,client_port,server_ip,server_port

针对老师提到的一个线上服务时好时坏的描述，存在疑问的点：
【原文】
该服务的可用性变得时好时坏，一段时间可以对外提供服务，一段时间突然又不可以，大家都百思不得其解。运维同学登录到服务所在的主机上，使用 netstat 命令查看后才发现，主机上有成千上万处于 TIME_WAIT 状态的连接。

【疑问】
问题1.  线上服务作为服务端，对外提供给客户端连接。假如都是服务端主动断开了连接，会存在较多TIME_WAIT。 此时会占用掉一些部分服务端的内容。除此之外会有什么其他的资源占用吗？ 

问题2. 接问题1的情况，理论服务端的程序监听端口可以复用，就算是存在较多TIME_WAIT。Client端还是能够连接到服务端的监听端口的。为什么会表现为有时可连，有时不可连呢？

问题3：最终这个线上的问题，是通过什么方法进行解决的？

【我的猜测】
1. 我个人的推测，是不是因为server端存在较多time_wait。就说明socket是还没有完全关闭的。也就是说除了占用内存资源。也占用着套接字资源，套接字就是一个文件描述符。过多的TIME_WAIT，再加上已经建立的正常连接，就造成服务端没有更多的文件描述符来服务新的连接请求。 
老师不懂我这样推测是不是对的，望您能帮忙解答下。</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（2） 💬（1）<div>服务器出现大量time wait并且一直不消失 老师这是啥情况 怎么解决？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/17/d0b8135f.jpg" width="30px"><span>灰色</span> 👍（2） 💬（1）<div>如果服务端主动关闭一些连接，那么在服务端会出现一些处于TIME_WAIT状态的连接，如果客户端绑定相同的端口，重新连接服务端，连接还是可以立即建立成功，那是不是就出现了原来连接的“化身”？</div>2019-09-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VTPuhJb5xxuRwH1iblqrAe3De4PoETgNWibZRkLlhvszysdtpAvSPZFuYtsJfWJmoXOFFWnpR02W9NGIiammU8UPg/132" width="30px"><span>Info_E</span> 👍（1） 💬（2）<div>为什么是2MSL，不是1MSL 原因是 ：
服务端发送FIN后开始倒计时，假设0.2MSL到达客户端，并且超过1MSL没有收到ACK就重发FIN；
客户端收到FIN后，发送ACK，假设网络拥堵，这个ACK在客户端发送0.9MSL才到达服务端；
服务端因为发送FIN 耗时 0.2 + 客户端发送ACK 0.9 = 1.1 &gt; 1 MSL，所以服务端重发了FIN；
假设这个FIN又因为拥堵，花费了0.9MSL才到达客户端；
在客户端看来，从发送ACK，到重新接受FIN，花费时间是ACK0.9 + FIN0.9 = 1.8MSL。
综上：为了确保客户端能接收到服务端的FIN，那么客户端接受到FIN后必须等待时间 &gt;1.8MSL才行。以上数据只是假设，可以把0.9替换成0.9999999999999，取个极限，那么客户端TIME_WAIT 就无限趋近于2MSL。 所以 TIME_WAIT设置为2MSL是安全的。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/96/98/89b96cda.jpg" width="30px"><span>三年二班邱小东</span> 👍（1） 💬（2）<div>基础篇里没讲四次挥手啊</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b9/7c/afe6f1eb.jpg" width="30px"><span>vv_test</span> 👍（1） 💬（1）<div>假如开启了net.ipv4.tcp_tw_reuse，对方主机的时间跟发送方时间本来就有差，这个要怎么避免?</div>2021-06-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（1）<div>原文：只有发起连接终止的一方会进入 TIME_WAIT 状态。


socket 操作：角色
connect：client
accept：server

老师，原文的那句话是说，server 也是可以主动发起连接终止进入 TIME_WAIT 状态是么？之前一直以为只有 connect(client) 端才能发起连接终止。
谢谢老师！</div>2021-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（2）<div>老师您的回复：
不是端口复用，是复用处于 TIME_WAIT 的套接字为新的连接所用。

----

约定：
旧的四元组：&lt;old_client_ip，old_client_port，old_server_ip，old_server_port&gt;
新的四元组：&lt;new_client_ip，new_client_port，new_server_ip，new_server_port&gt;

当前 TIME_WAIT 的套接字（假设名字为 socket_a）被新的连接复用了，新连接使用该套接字完成三次握手、发数据。
1. socket_a 为两个连接服务么？因此 socket_a 需要通过 &lt;old_server_ip&#47;port&gt; 和 &lt;new_server_ip&#47;port&gt; 来区分消息是谁发的？
2. old_client_ip 与 new_client_ip 相同，但是 old_client_port 和 new_client_port 不同，是么？
3. 当 socket_a 被新连接复用后，old_server 目前只会发送 FIN（不会发其他数据），socket_a 收到后需要对 old_server 回复 ACK 么，还是说直接不理会？

谢谢老师！</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（1） 💬（1）<div>最简单直接的方法是使用长连接</div>2020-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（1）<div>老师好，一个tcp占用一个端口的话，那一个http请求是不是也要占用一个端口？除非使用异步网络编程模型，否则一个http会新建一个线程并占用一个端口吗？</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1b/4d/2cc44d9a.jpg" width="30px"><span>刘忽悠</span> 👍（1） 💬（1）<div>2msl一定能保证服务器正常关闭吗？
如果服务器一直收不到最后的ack呢？假如说当服务器发送fin以后，客户端也收到了，但是因为网络状态不好，ack传不过去，导致客户端2msl计时器到时了，接着关闭了，那服务器是不是一直处在last_lack状态，服务器的rto计时器不停超时重传，一直到客户端收到fin以后，发现自己已经关闭了，发送rst报文给服务器，服务器收到rst以后出错呢？</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/33/4e/507ad4ea.jpg" width="30px"><span>网络人</span> 👍（1） 💬（1）<div>老师，能讲下windows平台下有没有提供更安全的选择呢？有没有类似的方法？可以提供代码参考下吗？
</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（1） 💬（2）<div>当机器出现大量的time wait 状态，原因该如何排查呀，谢谢老师</div>2019-08-31</li><br/>
</ul>