你好，我是盛延敏，这里是网络编程实战第12讲，欢迎回来。

上一篇文章中，我们讲到了如何使用close和shutdown来完成连接的关闭，在大多数情况下，我们会优选shutdown来完成对连接一个方向的关闭，待对端处理完之后，再完成另外一个方向的关闭。

在很多情况下，连接的一端需要一直感知连接的状态，如果连接无效了，应用程序可能需要报错，或者重新发起连接等。

在这一篇文章中，我将带你体验一下对连接状态的检测，并提供检测连接状态的最佳实践。

## 从一个例子开始

让我们用一个例子开始今天的话题。

我之前做过一个基于NATS消息系统的项目，多个消息的提供者 （pub）和订阅者（sub）都连到NATS消息系统，通过这个系统来完成消息的投递和订阅处理。

突然有一天，线上报了一个故障，一个流程不能正常处理。经排查，发现消息正确地投递到了NATS服务端，但是消息订阅者没有收到该消息，也没能做出处理，导致流程没能进行下去。

通过观察消息订阅者后发现，消息订阅者到NATS服务端的连接虽然显示是“正常”的，但实际上，这个连接已经是无效的了。为什么呢？这是因为NATS服务器崩溃过，NATS服务器和消息订阅者之间的连接中断FIN包，由于异常情况，没能够正常到达消息订阅者，这样造成的结果就是消息订阅者一直维护着一个“过时的”连接，不会收到NATS服务器发送来的消息。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（21） 💬（5）<div>思考题
1. udp不需要连接 所以没有必要心跳包
2. 我觉得还是很有必要判定存活 像以前网吧打游戏 朋友的电脑突然蓝屏死机 朋友的角色还残留于游戏中,所以服务器为了判定他是否真的存活还是需要一个心跳包 隔了一段时间过后把朋友角色踢下线</div>2019-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ61zTDmLk7IhLJn6seBPOwsVaKIWUWaxk5YmsdYBZUOYMQCsyl9iaQVSg9U5qJVLLOCFUoLUuYnRA/132" width="30px"><span>fjpcode</span> 👍（52） 💬（2）<div>1.UDP里面各方并不会维护一个socket上下文状态是无连接的，如果为了连接而保活是不必要的，如果为了探测对端是否正常工作而做ping-pong也是可行的。
2.额外的探活报文是会占用一些带宽资源，可根据实际业务场景，适当增加保活时间，降低探活频率，简化ping-pong协议。 
3.多次探活是为了防止误伤，避免ping包在网络中丢失掉了，而误认为对端死亡。</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（21） 💬（2）<div>想到HTTP Header也能设置Connection: Keep-Alive，也是应用层协议，是不是底层实现也类似于定时器+Ping Pong的思路？</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（10） 💬（1）<div>文章中提到保活有两个方向，实际应用中，会有两个方向同时探测的场景吗</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/69/0ddda908.jpg" width="30px"><span>满怀</span> 👍（8） 💬（1）<div>老师 我想问一下 看您在回复当中有说 虽然TCP本身的keep-alive机制可以设置保活时间，保活探测时间间隔以及探测次数，但是应用层会无法感知，那么这种情况下会怎么处理呢 就是文中所给出的三种情况吗</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（7） 💬（3）<div>老师  同步连接可以实现心跳包么 如果不能的话  那同步连接如果因为客户端崩溃 没有通过四次挥手结束连接  服务端还堵塞在接收数据  那么这样如何判断对方已经离开呢</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/d8/d7c77764.jpg" width="30px"><span>HunterYuan</span> 👍（6） 💬（1）<div>对于协议栈中的TCP的keep-alive是可以手动配置的，全局配置通过修改net.ipv4下的等参数；局部配置可以通过setsockopt修改socket选项。在工作中遇到过一个oracle,windows服务器的保活时间大于，我们设备状态连接表的保活时间，导致，一段时间后重连，导致服务器报错问题。当时最最快的处理办法是，修改window默认的保活时间小于状态连接失效时间。</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（5） 💬（1）<div>服务器端恢复心跳包这段   
case MSG_PING:   
{  
    messageObject pong_message;     
    pong_message.type = MSG_PONG;  
    sleep(sleepingTime);      
     ssize_t rc = send(connfd, (char *) &amp;pong_message, sizeof(pong_message), 0);     
老师，这个type是int类型，应该将其转为网络序才对吧？ pong_message.type = htonl(MSG_PONG);     
而且你的客户端程序也是有转换的，是不是服务器端这里忘记了？</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/81/1864f266.jpg" width="30px"><span>石将从</span> 👍（5） 💬（4）<div>为啥这句套接字要加1呢？int rc = select(socket_fd + 1, &amp;readmask, NULL, NULL, &amp;tv);</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（5） 💬（1）<div>TCP本身的keep-alive的时间是可以自己设置的吗？如果是可以自己设置的，为何还需要自己实现这个机制？</div>2019-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/wwM75BhyU43UYOJ6fZCZgY6pfNPGHHRlooPLQEtDGUNic4aLRHWmBRTpIiblBAFheUVm9Sw8HWAChcFsnVM2sd5Q/132" width="30px"><span>Geek_d6f50f</span> 👍（2） 💬（1）<div>老师，第二次运行程序，客户端的定时器设定为每10秒钟进行一次select返回0，此时进行探测包发送。而服务器端延迟5秒进行应答，为什么客户端每次都能发送两个包后才清零？不应该是只进行一个包的发送，服务器端延迟5秒就给出应答，然后清零吗？</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（1） 💬（1）<div>这个是客户端探活服务器是否还存活，还可以用服务器来探活客户端是否还存活。我原先也有接触过这个心跳，不过实现的机制比较简单，就是客户端连上服务器了，客户端要每个M秒向服务器发包，服务器如果在M+10秒内没收到这个心跳包就判定客户端已经死亡。就会在应用层方面判定客户端已经失去连接。</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/1a/fd82b2d5.jpg" width="30px"><span>Tachone</span> 👍（1） 💬（4）<div>请问老师一个tcp长连接，网络发生故障， client和server都还没有断开这个连接， 这时候client调用send发送数据是个什么行为？我理解send进缓冲区是一直成功的， 但是由于网络不通， 数据不会发出去。这时候如果想要发现这个tcp断开就只能client应用层设置一个超时， 超时后调用shutdown， 有其他的方式可以感知到这个tcp断开么</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（1） 💬（2）<div>我看到大家对于第二个问题的答案都提到了为了避免探活包丢包 所以要发多个探活包。但是我觉得只要发了探活包对方就一定能收到，就算丢了 发送端也会重传。而大家说的发送多个探活包的原因 是因为重传需要等到计时器超时才传，而如果网络堵塞的话可能会出现频繁丢包 那么服务端可能需要很久才能知道对方已经离开 发多个探活包的话 就减少了这个等待的时间 这样理解对么</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（0） 💬（1）<div>老师你在留言里面回复，很多实际的场景都是自己在应用层加心跳，这个是指http的keep-alive么？如果是在java开发的应用，这个心跳是指客户端定时向服务端发起请求么？可不可以结合一下java应用举一个例子</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（0） 💬（1）<div>老师我想问一下， 连接无效：使用Keep-Alive还是应用心跳来检测？
是不是应该使用应用心跳来检测，比使用Keep-Alive更好啊？
</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/67/03c95ec2.jpg" width="30px"><span>守望</span> 👍（0） 💬（2）<div>老师您好，有个问题想请教一下，假设服务端重启了，起来后还是绑定同样的ip和端口，而客户端仍然发送，如何最大程度的避免客户端发送数据丢失呢？这种心跳检测貌似发现过慢。</div>2020-08-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（0） 💬（3）<div>老师，一台服务器同时在线的tcp&#47;ip连接数，理论上是不是最多只有65535个?</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/22/b820e079.jpg" width="30px"><span>拖鞋汉</span> 👍（0） 💬（1）<div>select监听socket_fd，那么如果服务端探活呢，一个socket_fd上可能有多个connection_fd，这里面只要有一个触发了事件，select返回的值不就大于0了吗，心跳逻辑不就无法触发了？还是说心跳针对的是socket_fd，而不是connection_fd?</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/36/d2/32d3545a.jpg" width="30px"><span>A.Windy</span> 👍（0） 💬（2）<div>程序编译不过， 说lib&#47;common.h 找不到， 怎么搞啊</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/ff/e2c331e0.jpg" width="30px"><span>bbbi</span> 👍（0） 💬（2）<div>我的理解是这样的：
TCP协议并没有提供一个保活的措施，如果出现TCP已经连接后，两端异常崩溃或者是编码问题没有及时的关闭连接(比如客户端发送--&gt;服务端收到消息返回数据--&gt;客户端收到后直接退出，没有调用close)，那么服务器会一直维护着这个通道，造成资源浪费。所以加入keepalive，系统提供一个计时器，在约定的时间下发送检测包。但是这个计时器检测时间默认是2小时开始检测时间太长，所以我们可以在应用层，手动发送检测包</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/b5/4159fa05.jpg" width="30px"><span>zhanyd</span> 👍（0） 💬（1）<div>这程序，没看懂。。。</div>2019-10-26</li><br/><li><img src="" width="30px"><span>15652790052</span> 👍（0） 💬（1）<div>请教一个问题: 客户端如果奔溃了-&gt;进程退出了-&gt;内核会收到关于此进程的所有资源,包括socket文件-&gt;意味这个socket的两个方向都关闭了,怎么会感知不到而傻等呢</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5a/9e/8f2ccc1d.jpg" width="30px"><span>有点意思</span> 👍（0） 💬（3）<div>老师 你好
现在做的项目中要用到心跳，具体是这样的
服务端一个 客户端多个
每个客户端会持续的往服务端发送从网卡抓取的流量，如果某段时间网卡没有流量就不发 但是连接还需要维持 之前用的keepalive 现在想换成应用层心跳
想到的方案如下:
客户端开启线程1来发送抓到的流量 并且每间隔1秒就发送一次心跳给服务端 服务端收到心跳会回复一下
同时开启另外一个线程2启用select和recv来接收心跳响应 如果在 3秒内没接受到心跳 那么就判断连接断开

老师你觉得这种方案可以么 有什么缺点么</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/13/104d9501.jpg" width="30px"><span>另一半棉花糖</span> 👍（0） 💬（1）<div>在对端计算能力紧张、或者网络延迟比较大的时候，仍然会对每一个ping包都做回复，但是本端可能在发了第KEEP_ALIVE_PROBETIMES-1个包之后才收到对端针对第一个ping做的回复。这样虽然本端就会认为这个连接是有效的，但会在接下来接收到好几个pong包；如果这一批的某一个pong包的到来时间正好落在本端第二次由于select超时而进行链路探测的时间段内的话，则可能产生“对端实际已经down了，但是本端过很久才能检测到（可能要达到N个select超时时间）”的问题。这个问题该怎么解决？要给ping和pong加序列号以用于匹配么？</div>2019-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ub4icibeRLzff8Nf6ORsolib9KHtmeu3d4cCCAFd3Xgah3v78WfDYQB7WKq9iaIPXPwHBxw7mkBP9wYxDGMT9m1Rbw/132" width="30px"><span>wyf2317</span> 👍（0） 💬（1）<div>1 udp不需要
2 9102年了，这点带宽不成问题。反倒是保持连接带来的一系列资源消耗才是重点。增加心跳检查可以快速确认客户端是否存活或者客户端快速重连。减少资源消耗，提升用户体验。</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（1）<div>使用心跳包不就是为了保持keep alive吗？文章内容到最后也没有点题？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（2）<div>老师在pingclient的实现中，为什么只要该一下结构体的字段值就能重置探活时间了？

        if (FD_ISSET(socket_fd, &amp;readmask)) {
            &#47;&#47;......
            &#47;&#47; 重置探活时间
            tv.tv_sec = KEEP_ALIVE_TIME;
        }</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/61/b62d8a3b.jpg" width="30px"><span>张立华</span> 👍（0） 💬（1）<div>请问下作者，你提到的nats客户端的问题，是nats客户端的那个版本的bug</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>其实我也在想比如客户端崩溃重启过后 然后重新建立连接 创建socket 那之前那个连接是怎么处理的？因为之前那个服务器那个连接发往的还是我 所以就想知道这个时候是怎么处理的</div>2019-08-28</li><br/>
</ul>