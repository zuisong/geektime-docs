你好，我是盛延敏，这里是网络编程实战第6讲，欢迎回来。

前面几讲我们讲述了TCP方面的编程知识，这一讲我们来讲讲UDP方面的编程知识。

如果说TCP是网络协议的“大哥”，那么UDP可以说是“小兄弟”。这个小兄弟和大哥比，有什么差异呢？

首先，UDP是一种“数据报”协议，而TCP是一种面向连接的“数据流”协议。

TCP可以用日常生活中打电话的场景打比方，前面也多次用到了这样的例子。在这个例子中，拨打号码、接通电话、开始交流，分别对应了TCP的三次握手和报文传送。一旦双方的连接建立，那么双方对话时，一定知道彼此是谁。这个时候我们就说，这种对话是有上下文的。

同样的，我们也可以给UDP找一个类似的例子，这个例子就是邮寄明信片。在这个例子中，发信方在明信片中填上了接收方的地址和邮编，投递到邮局的邮筒之后，就可以不管了。发信方也可以给这个接收方再邮寄第二张、第三张，甚至是第四张明信片，但是这几张明信片之间是没有任何关系的，他们的到达顺序也是不保证的，有可能最后寄出的第四张明信片最先到达接收者的手中，因为没有序号，接收者也不知道这是第四张寄出的明信片；而且，即使接收方没有收到明信片，也没有办法重新邮寄一遍该明信片。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/23/74/b81c9f8c.jpg" width="30px"><span>何赫赫</span> 👍（26） 💬（2）<div>老师，UDP没有发送缓冲区这个概念吗</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/62/f873cd8f.jpg" width="30px"><span>tongmin_tsai</span> 👍（22） 💬（3）<div>老师，UDP被IP层分包发送后，对端如何保证UDP包整个组合的？比如用UDP发送3000字节，假设拆分2个MTU发送，后一个先到服务端，前一个后到服务端，那应用层接收的时候，UDP怎么组装的？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/74/636ea0f3.jpg" width="30px"><span>你好</span> 👍（12） 💬（4）<div>多人聊天室使用UDP，消息发出后怎么保证消息可以被收到呀，UDP不是不可靠传输嘛，中间丢了消息咋办呀</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（10） 💬（1）<div>第一个思考题 另起一个线程进行recvfrom</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dd/6e/8f6f79d2.jpg" width="30px"><span>YUAN</span> 👍（6） 💬（1）<div>udp之所以sendto要目的地址是因为他是非连接的，否则不知道将数据发给谁，recvfrom要发送方地址也是因为udp是非连接的，有了from内核就可以判定将数据上传给谁（应用进程）。是这样吗？</div>2020-10-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（5） 💬（4）<div>老师，TCP 流，UDP包，流的说法怎么理解？</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/8f/a998a456.jpg" width="30px"><span>范龙dragon</span> 👍（5） 💬（2）<div>客户端代码的29行sendline数组之前没有初始化数组元素为0，直接用strlen应该会有问题吧，strlen不是以0作为结束标志吗？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/ca/4560f06b.jpg" width="30px"><span>zhchnchn</span> 👍（5） 💬（2）<div>如果不开启服务端，TCP 客户端的 connect 函数会直接返回“Connection refused”报错信息。而在 UDP 程序里，则会一直阻塞在这里。
-------------------------
这个地方不太理解。请问老师,对TCP来说，收到“Connection refused”报错信息，表明收到了服务端的RST包，如果服务端不开启，谁负责发送RST包呢?</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/3d/e97e661c.jpg" width="30px"><span>江永枫</span> 👍（3） 💬（1）<div>关于阻塞io，可以考虑使用多线程模型去提升性能，或者结合io多路复用来处理能力。


https:&#47;&#47;m.php.cn&#47;article&#47;410029.html</div>2019-08-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（2） 💬（1）<div>老师好，有 3 个问题请教一下：
1. TCP 有序传输的意思是：需要等到当前发送的包 ACK 之后，才发下一个包么？还是说可以一直发消息，收到 ACK 之后再确认对应的包发送成功？

2. 关于 TCP 和 UDP 连接，我可以这么理解么？
TCP 连接之后直到关闭，这期间发的消息，比如 client 发给(send 函数) server，
然后 server 回复(不知道用啥函数写回，也是 send 函数么？) client；
client 又继续发给 server，继续重复刚才的步骤....，
走的都是同一个连接。

而 UDP，client 发给（sendto 函数） server 是一个连接。而 server 回复（sendto 函数） client，又是另一个连接。

3. 下面的循环发送，我甚至是可以动态更改对端 client_addr 地址和端口信息的吧？
for (;;) {
  sendto(socket_fd, send_line, strlen(send_line), 0, (struct sockaddr *) &amp;client_addr, client_len);
}</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/0e/4e2b06d5.jpg" width="30px"><span>流浪在寂寞古城</span> 👍（2） 💬（3）<div>https:&#47;&#47;github.com&#47;worsun&#47;study&#47;tree&#47;master&#47;hack_time&#47;socket_code&#47;6</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/28/f4b4ed22.jpg" width="30px"><span>马留</span> 👍（2） 💬（5）<div>如果对udp套接字调用了listen函数，会怎么样呢？</div>2019-08-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7zuDYFIutbSPc4eEtcMhdNBTI1FRR7q0xrGh2X1QdiaNxvAV31HcRUsjPWLaaWftqgwTnVoiaica8Nw/132" width="30px"><span>胜辉（大V）</span> 👍（1） 💬（1）<div>示例程序在我的测试机(ubuntu 20.04）上有几个报错。除了include需要添加多个库，还有就是sprintf不分需要改为如下：
        char send_line[MAXLINE+4];
        sprintf(send_line, &quot;Hi, %s&quot;, message);

因为&quot;Hi, &quot;本身占用了额外的4个字节，所以导致send_line跟&quot;Hi, &quot;+message的长度不匹配，需要修改send_line为message长度加4。不知道其他同学的测试环境那里如何？</div>2021-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（1） 💬（1）<div>如果不开启服务端，而在 UDP 程序里，则会一直阻塞在这里（sendto）。

阻塞是为了等待消息发出去之后的 ACK 确认么？
不是说把明信片放到邮筒就不管了么？
邮筒可以认为是 IP 协议栈（即网络接口层？）吧？把 udp 包传递给 IP 层就不管了。

谢谢老师</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（1） 💬（1）<div>老师，你之前说过，创建套接字应该使用PF_INET，初始化套接字结构体地址才使用AF_INET，我看你在创建套接字的时候使用AF_INET。</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/af/4307867a.jpg" width="30px"><span>JJj</span> 👍（1） 💬（1）<div>服务端要发送数据给客户端，客户端不需要bind吗？</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/e6/ea4b2c10.jpg" width="30px"><span>........</span> 👍（1） 💬（1）<div>老师, 请问一下, 这个read函数, 是不是每次可以不读够1024字节, 所以才需要使用readn取封装一下</div>2019-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Gswh7ibY4tubXhp0BXOmV2pXZ3XsXic1d942ZMAEgWrRSF99bDskOTsG1g172ibORXxSCWTn9HWUX5vSSUVWU5I4A/132" width="30px"><span>奔奔奔跑</span> 👍（1） 💬（2）<div>老师，学完这章我有个不理解的地方，UDP是客户端向服务端发消息，服务端收到客户端的报文，根据报文的地址在传消息回去，因此服务端不能主动向客户端发消息。那么客户端如果也bind，那么服务端也能向客户端发消息了，老师我这么理解对吗</div>2019-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUgnMApgafcbOicQJYOlApkHf6AzxF5edzeXAtVNhwOZTh3WB5wtIrbf1Algg6Axy5rEfZjj0B6Ng/132" width="30px"><span>云端</span> 👍（1） 💬（1）<div>老师您好:
阻塞=进程或线程挂起？</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/98/2be9d17b.jpg" width="30px"><span>破晓^_^</span> 👍（1） 💬（1）<div>函数sendto原型参数写错了,应该为ssize_t sendto(int sockfd, const void *buff, size_t nbytes, int flags,const struct sockaddr *to, socklen_t addrlen);  最后一个参数与recvfrom不一样.</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/03/eba78e43.jpg" width="30px"><span>风清扬</span> 👍（0） 💬（1）<div>场景一：只运行客户端 这里是不是有点问题
now sending g1
send bytes: 2
看输入那里只有1？</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/25/c7/edd74dfb.jpg" width="30px"><span>淡C</span> 👍（0） 💬（1）<div>服务端的count++有什么用
</div>2022-01-26</li><br/><li><img src="" width="30px"><span>Geek_88aaae</span> 👍（0） 💬（1）<div>老师您好，为什么我在进行第三个实验的过程中，在服务端关闭时，客户端发送数据的数据没有在服务端重新打开时收到呢？客户端也一直阻塞在了recv from</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/62/78/6e7642a3.jpg" width="30px"><span>王蓬勃</span> 👍（0） 💬（1）<div>为什么说UDP比TCP安全，但不可靠？这个UDP的安全体现在哪里？</div>2021-10-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ooYDTtTQHL9CZQmonDOQSC4Af9S4uqicXzUicOqEJqSOtHyOZ81PTpxcTqK5ibNHsaNWJIuHiaVcxB8gIo9RNXsshA/132" width="30px"><span>小叶</span> 👍（0） 💬（1）<div>能不能讲下阻塞跟非阻塞先呢，一说到阻塞就不知道是什么了</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/33/32/8f304f6c.jpg" width="30px"><span>--SNIPER</span> 👍（0） 💬（1）<div>老师 您好
ss -anlpx发现存在3w多的udp端口占用，state都是UNCONN，这类是未close套接字吗，正常吗
期待您的回复</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（1）<div>老师这个讲解还是相当明白的，这个通过举例子来比较“打电话”的TCP，“发邮件”的UDP，来比较。同样通过服务器重启是否能继续接受，来说明为什么UDP是无连接的，TCP是面向连接的。</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/19/a235f31d.jpg" width="30px"><span>云淡风轻</span> 👍（0） 💬（1）<div>请教老师：
问题：
服务器端 recvfrom 读取客户端的信息到message中，如果多个客户端一直发信息，后来的 message 会将前面的 message 覆盖掉吗？
测试：
服务器端将 message 回传给客户端，发现没有覆盖的现象。
疑问：
请问老师，这里面是什么原理</div>2020-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5kv7IqibneNnMLqtWZQR5f1et8lJmoxiaU43Ttzz3zqW7QzBqMkib8GCtImKsms7PPbWmTB51xRnZQAnRPfA1wVaw/132" width="30px"><span>Geek_63bb29</span> 👍（0） 💬（2）<div>老师，cmake可以讲解或详细注释一下吗？有点弄不清楚这个</div>2020-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epKJlW7sqts2ZbPuhMbseTAdvHWnrc4ficAeSZyKibkvn6qyxflPrkKKU3mH6XCNmYvDg11tB6y0pxg/132" width="30px"><span>pc</span> 👍（0） 💬（1）<div>所以服务端的recvfrom(socket_fd, message, MAXLINE, 0, (struct sockaddr *) &amp;client_addr, &amp;client_len)也会阻塞是么？等任意一个客户端发消息过来了，就receive到message而继续执行？</div>2020-05-11</li><br/>
</ul>