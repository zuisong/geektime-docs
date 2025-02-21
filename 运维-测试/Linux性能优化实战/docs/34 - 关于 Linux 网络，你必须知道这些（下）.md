你好，我是倪朋飞。

上一节，我带你学习了 Linux 网络的基础原理。简单回顾一下，Linux 网络根据 TCP/IP 模型，构建其网络协议栈。TCP/IP 模型由应用层、传输层、网络层、网络接口层等四层组成，这也是 Linux 网络栈最核心的构成部分。

应用程序通过套接字接口发送数据包时，先要在网络协议栈中从上到下逐层处理，然后才最终送到网卡发送出去；而接收数据包时，也要先经过网络栈从下到上的逐层处理，最后送到应用程序。

了解Linux 网络的基本原理和收发流程后，你肯定迫不及待想知道，如何去观察网络的性能情况。具体而言，哪些指标可以用来衡量 Linux 的网络性能呢？

## 性能指标

实际上，我们通常用带宽、吞吐量、延时、PPS（Packet Per Second）等指标衡量网络的性能。

- **带宽**，表示链路的最大传输速率，单位通常为 b/s （比特/秒）。
- **吞吐量**，表示单位时间内成功传输的数据量，单位通常为 b/s（比特/秒）或者 B/s（字节/秒）。吞吐量受带宽限制，而吞吐量/带宽，也就是该网络的使用率。
- **延时**，表示从网络请求发出后，一直到收到远端响应，所需要的时间延迟。在不同场景中，这一指标可能会有不同含义。比如，它可以表示，建立连接需要的时间（比如 TCP 握手延时），或一个数据包往返所需的时间（比如 RTT）。
- **PPS**，是 Packet Per Second（包/秒）的缩写，表示以网络包为单位的传输速率。PPS 通常用来评估网络的转发能力，比如硬件交换机，通常可以达到线性转发（即 PPS 可以达到或者接近理论最大值）。而基于 Linux 服务器的转发，则容易受网络包大小的影响。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（38） 💬（6）<div>小狗同学问到： 老师，您好 ss —lntp 这个 当session处于listening中 rec-q 确定是 syn的backlog吗？  
A:  Recv-Q为全连接队列当前使用了多少。 中文资料里这个问题讲得最明白的文章：https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;yH3PzGEFopbpA-jw4MythQ</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/ca/9afb89a2.jpg" width="30px"><span>Days</span> 👍（14） 💬（1）<div>老师春节不休息，大赞啊，老师可否讲解一下一个包从网卡接收，发送在内核协议栈的整个流程，这样性能分析的时候，更好的理解数据包阻塞在哪里？</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/4e/c266bdb4.jpg" width="30px"><span>[小狗]</span> 👍（8） 💬（3）<div>老师，您好  ss —lntp  这个  当session处于listening中  rec-q  确定是  syn的backlog吗？  我之前都是当做全队列的长度</div>2019-02-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/8OPzdpDraQMvCNWAicicDt54sDaIYJZicBLfMyibXVs4V0ZibEdkZlbzxxL7aGpRoeyvibag5LaAaaGKSdwYQMY2hUrQ/132" width="30px"><span>code2</span> 👍（5） 💬（1）<div>每期读两遍，看看别人怎么做!</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（4） 💬（1）<div>老师，有一事疑惑，希望帮忙解惑。

一台64个千兆端口的交换机，全双工模式，交换容量计算：64*1000*2
包转发速率计算：64*1.488Mpp

交换容量有个乘以2，为什么包转发速率不需要乘以2？
（我理解，端口速率1000bps，在全双工模式下，按照双向速率计算，即总速率是2000bps）</div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（3） 💬（1）<div>老师好，
“当套接字处于listen状态时，使用ss命令看到的Send-Q表示最大的syn_backlog值”
但是和&#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_max_syn_backlog   查看到的值不一致，是我理解错了吗？
谢谢</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e2/4f/0748c63e.jpg" width="30px"><span>Gaoyc</span> 👍（3） 💬（1）<div>通过ifconfig和ss看到的错误包或丢弃包等的一些错误是累加的嘛？是否可以清空这些错误包信息？</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（3） 💬（1）<div>Speed 有的通过ethtool查不到，是什么原因呢，那查不到的话，默认值是多少呢</div>2019-02-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（2） 💬（1）<div>老师好，再请教一个问题，查看max_syn_backlog值为2048，表示同时最大只能接受2048个请求吗？
# cat &#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_max_syn_backlog 
2048
</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/35/25/bab760a1.jpg" width="30px"><span>好好学习</span> 👍（2） 💬（1）<div>eth0: flags=4163
这个什么意思，有点好奇</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c3/48/3a739da6.jpg" width="30px"><span>天草二十六</span> 👍（1） 💬（1）<div>请教下：丢包率，计算客户端程序到IDC机房的，一般使用什么量化工具？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>centos 6.8执行 sar 命令没有%ifutil,这个指标可以理解为网络利用率吗？</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/a0/c342c50e.jpg" width="30px"><span>bzadhere</span> 👍（1） 💬（2）<div>netstat -nta  命令看到Listening状态下的Send-Q 值都是0，用man netstat 看到说明和实际情况不一样； 然后用ss -lnt 看到Send-Q  非0，应该怎么理解？

[root@localhost ~]# man netstat
......
   Recv-Q
       Established:  The count of bytes not copied by the user program connected to this socket.  Listening: Since
       Kernel 2.6.18 this column contains the current syn backlog.

   Send-Q
       Established: The count of bytes not acknowledged by the remote host.  Listening: Since Kernel  2.6.18  this
       column contains the maximum size of the syn backlog.
.......

[root@localhost ~]# netstat -tna
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:21              0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN     
tcp        0      0 192.168.137.20:22       192.168.137.1:52521     ESTABLISHED
tcp6       0      0 :::22                   :::*                    LISTEN     
tcp6       0      0 ::1:25                  :::*                    LISTEN     

[root@localhost ~]# ss -lnt
State       Recv-Q Send-Q             Local Address:Port                            Peer Address:Port              
LISTEN      0      32                             *:21                                         *:*                  
LISTEN      0      128                            *:22                                         *:*                  
LISTEN      0      100                    127.0.0.1:25                                         *:*                  
LISTEN      0      128                           :::22                                        :::*                  
LISTEN      0      100                          ::1:25                                        :::*  </div>2019-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（1） 💬（1）<div>老师，带宽和吞吐量指标。区分上下行吗，？还是统计总量？</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/33/32/8f304f6c.jpg" width="30px"><span>--SNIPER</span> 👍（1） 💬（1）<div>老师好，netstat -anu 输出中：网卡收发队列时不时的会排队500，这种该如何再深入排查下是哪里的问题</div>2019-02-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（1） 💬（1）<div>打卡day36
去年之前喜欢用netstat，ifconfig，去年年中的时候入坑ss，ip</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/b4/6892eabe.jpg" width="30px"><span>Geek_33409b</span> 👍（1） 💬（1）<div>老师，有没有什么办法可以知道路由器的带宽是不是被打满了？除了路由器的图形监控之外。怎么从连接到路由器上的机器知道路由器的带宽情况？</div>2019-02-10</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（1） 💬（1）<div>你好，我man一下netstat，看到Foreign Address的定义如下
Foreign Address
       Address and port number of the remote end of the socket.  Analogous to &quot;Local Address.&quot;

请教一下，我用netstat -nlp看到的Foreign Address都是0.0.0.0:*，我特意浏览器开了一个下载，依然看到都是这样。
</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/bb/4a749b6c.jpg" width="30px"><span>孙成子</span> 👍（0） 💬（1）<div>每一篇都是精华， 需要多看几遍，多思考。谢谢老师</div>2019-06-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（0） 💬（2）<div>温习一遍，有个疑问，套接字 Listening状态时， Send-Q 表示的是全连接 最大值吧？</div>2019-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKq0oQVibKcmYJqmpqaNNQibVgia7EsEgW65LZJIpDZBMc7FyMcs7J1JmFCtp06pY8ibbcpW4ibRtG7Frg/132" width="30px"><span>zhoufeng</span> 👍（0） 💬（1）<div>太赞了，结课这么久了还能收到老师的回复，老师严谨负责。</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>吞吐量，表示没丢包时的最大数据传输速率
这个翻译有点问题？
Throughput is how much data actually does travel through the &#39;channel&#39; successfully.</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（28） 💬（4）<div>今天查一个问题，花了半天功夫。
如果文中的一句话还记得的话，可能就只需要几分钟了。

而 Send-Q 表示还没有被远端主机确认的字节数（即发送队列长度）。

原本ngnix在物理机上是没问题的，结果有个环境中放到了docker里，且还是走的普通端口映射模式，还不是—net=host模式，结果websocket发往ngnix的数据过大后就被阻塞了。
最后发现相应被阻塞的端口 send-q一直很大。
最后docker尝试使用net=host后故障消除。
具体的原因还没有细究。

留个言，给后面看专栏的同学一个教训吧。</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/e7/53416498.jpg" width="30px"><span>曹龙飞</span> 👍（16） 💬（3）<div>看了源码发现，这个地方讲的有问题.关于ss输出中listen状态套接字的Recv-Q表示全连接队列当前使用了多少,也就是全连接队列的当前长度,而Send-Q表示全连接队列的最大长度</div>2019-08-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJx33zpGe1Y42dghX3Df4l0Ny8iaibR1vGpicAbXEScGqQSs42X5dNU2nHIkVHUDC9xlwVIqqRwAEoJg/132" width="30px"><span>Geek_4ojwyf</span> 👍（4） 💬（2）<div>老师，listening状态下，Recv-Q和Send-Q应该分别指的是，当前全连接的使用数量和最大全连接可用数量，但是文中说成了是半连接。参考阿里技术博客：http:&#47;&#47;jm.taobao.org&#47;2017&#47;05&#47;25&#47;525-1&#47;</div>2020-01-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/u8g8UoUaBZTGpDgAQKDwL5IzicBILfpDmz0tOXibSQWkmTjr3m57ofUKVPgRiaFTRYZkE7dBxOmmJBhqCpYJWd2GA/132" width="30px"><span>mfj1st</span> 👍（3） 💬（0）<div>倪老师，虚拟机用ethtool获取不到网卡带宽，有其他方法吗？</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（0）<div>[D34打卡]
平常只用netstat 和 ifconfig ，前面的专栏里学了sar观测网络指标，今天又接触了两个类似的：ss和ip。
平常遇到的网络问题比较简单，先看能否正常连上，再看看并发连接数。有时忘记执行ulimit -n会导致默认账号的一个进程同时打开文件数只有1024。
除了带宽没买够，平常不会遇到网络方面的瓶颈，毕竟我们的业务处理数据的消耗比收发数据的消耗大得多。</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a0/b7/1327ae60.jpg" width="30px"><span>hellojd_gk</span> 👍（2） 💬（1）<div>在阿里云ECS上执行如下命令，怎么啥也不返回
[root@iZ8vb31waukedizc39ffofZ ~]# ethtool eth0
Settings for eth0:
        Link detected: yes</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a1/29/ac0f2c83.jpg" width="30px"><span>芥菜</span> 👍（2） 💬（0）<div>春节期间终于跟上节奏，春节里做到只长知识不长肉：）</div>2019-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（1） 💬（2）<div>老师， 网卡  dropped  不为零，而且还在增加，怎么排查问题哦？</div>2020-04-15</li><br/>
</ul>