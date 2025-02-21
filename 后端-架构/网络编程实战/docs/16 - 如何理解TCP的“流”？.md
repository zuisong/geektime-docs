你好，我是盛延敏，这里是网络编程实战第16讲，欢迎回来。

上一讲我们讲到了使用SO\_REUSEADDR套接字选项，可以让服务器满足快速重启的需求。在这一讲里，我们回到数据的收发这个主题，谈一谈如何理解TCP的数据流特性。

## TCP是一种流式协议

在前面的章节中，我们讲的都是单个客户端-服务器的例子，可能会给你造成一种错觉，好像TCP是一种应答形式的数据传输过程，比如发送端一次发送network和program这样的报文，在前面的例子中，我们看到的结果基本是这样的：

发送端：network ----&gt; 接收端回应：Hi, network

发送端：program -----&gt; 接收端回应：Hi, program

这其实是一个假象，之所以会这样，是因为网络条件比较好，而且发送的数据也比较少。

为了让大家理解TCP数据是流式的这个特性，我们分别从发送端和接收端来阐述。

我们知道，在发送端，当我们调用send函数完成数据“发送”以后，数据并没有被真正从网络上发送出去，只是从应用程序拷贝到了操作系统内核协议栈中，至于什么时候真正被发送，取决于发送窗口、拥塞窗口以及当前发送缓冲区的大小等条件。也就是说，我们不能假设每次send调用发送的数据，都会作为一个整体完整地被发送出去。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（58） 💬（3）<div>一直有个疑问，趁这堂课向老师请教一下，前面客户端发送消息时，消息长度转成网络序了，后面的消息为何没有转成网络序，如果消息里面含有数字呢？如果消息里面全是字符呢？</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（12） 💬（6）<div>message.message_length = htonl( n );
message.message_type = 1;
我在自己写代码实现的时候突然想起这两句代码为什么一个需要htonl一个不需要呢？
</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/02/fcab58d1.jpg" width="30px"><span>JasonZhi</span> 👍（8） 💬（4）<div>老师，针对粘包问题会有相关的讲解吗？经常会听说相关的名词，但是还是不太懂具体是怎么样的。</div>2019-09-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（7） 💬（2）<div>为什么需要进行端序转换？
因为数据传输、存储的最小单位是字节，
当我想传输的数据需要一个以上字节才能表示的时候，比如int 类型的 123,
这时接收端收到的是按顺序的四个字节,
他需要知道如何用这四个字节来还原成一个int,
端序转换指定了这个方法，
当然，如果传输的是一个字节就能表示的char类型,就不需要转换了

</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/a5/71358d7b.jpg" width="30px"><span>J.M.Liu</span> 👍（7） 💬（3）<div>老师，关于网络序和主机序，我有3个问题想要请教一下：
1.在数据发送的时候，是先发送内存中高地址的数据，还是先发内存中低地址的数据？比如char* sendline=&quot;abcdef&quot;，是从a到f的顺序去发，还是从f到a的顺序去发。
2.接受的时候，是现接受到的是网络序中的高地址，还是低地址？
3.socket接口，如read，send这些函数，会自动帮我们完成主机序和网络序之间的转换吗，还是必须要自己去转？我看老师你有些数据显式调用了htonl()，有些没有，这是为什么呢？
谢谢老师。</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/61/b62d8a3b.jpg" width="30px"><span>张立华</span> 👍（7） 💬（2）<div>我的操作系统是：centos 7.4 64位操作系统。

short int = 258;

258=0x0102

x的地址是（每次运行地址不一样）： 0x7fffffffe33e

258在内存中：

低位					 高位						 
0x7fffffffe33e			0x7fffffffe33f
00000010				00000001

也就是说，在我的linux电脑上，内存的数据，是小端字节序

可以写个简单的程序，用gdb调试下，通过 x命令查看内存</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（5） 💬（1）<div>老师您好，您在第一位留言中有如下回答：“我们在网络传输中，一个常见的方法是把0-9这样的数字，直接用ASCII码作为字符发送出去，在这种情况下，你可以理解成发送出去的都是字符类型的数据，因为是字符类型的数据，就没有所谓的网络顺序了”。我对此有些疑问，要说现在网络上普遍以UTF-8编码进行传输的话（而UTF-8是单字节码元，因此字节序无关），我能理解您说的“无所谓网络顺序“，但是如果以其他编码方式传输字符呢？所以我有两个问题：
1. 如过通信两端采用UTF-16、UFT-32这些多字节码元编码方式传输是否存在字节序问题？
2.字符集编码是否是socket要考虑的问题？我理解socket只负责传输字节流，编码解码由通信两端完成，不知是否正确？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/84/07f0c0d6.jpg" width="30px"><span>supermouse</span> 👍（4） 💬（1）<div>思考题第一题：本来想说是因为Unix下的文件的行尾只有\n，而Windows下的文件行尾是\r\n，但是发现老师的代码里考虑的“\r”和“\r\n”这两种情况。所以这一题的答案是考虑到操作系统不同吗？
思考题第二题：区别的话应该是所属层级不同吧，我们自己定义的报文格式是用于应用层，而TCP分组的报文格式是用于传输层；而联系就在于，我们自己定义的报文格式是包含在TCP分组的报文格式中的，即TCP分组报文去掉消息头之后，得到的消息体的格式就是我们自己定义的报文格式</div>2020-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（3） 💬（2）<div>我们在网络传输中，一个常见的方法是把0-9这样的数字，直接用ASCII码作为字符发送出去，在这种情况下，你可以理解成发送出去的都是字符类型的数据，

老师，对这段回答，再加上我们项目现在划分微服务，我一直有疑问。我们服务间现在都是用grpc，而不用基于http的restful服务。因为考虑字符文本传输效率是最低的，体积大。比如本例当中125，如果作为数字传输，不是明显1个字节就可以了，如果用asc要3个字节，如果作为中文unicode，好像6个字节。
而我们传输的 数据对象中，既有字符类型字段(有中文文本)，也有数字字段。这种情况下，协议栈是怎么传输的了，整体作为字符传送？</div>2020-07-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83errIIarFicghpKamvkUaJmGdIV488iaOUyUqcTwbQ6IeRS40ZFfIOfb369fgleydAT8pkucHuj2x45A/132" width="30px"><span>xupeng1644</span> 👍（3） 💬（1）<div>老师 客户端发送message时 为什么不将messsage_type也转换成网络字节序 而只将message_length转换成网络字节序       </div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/93/b79a44b8.jpg" width="30px"><span>zjstone</span> 👍（3） 💬（1）<div>
read_line函数用很多次read操作，效率很低，老师应该发个高效率的版本：)</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（2） 💬（1）<div>我想到一个问题，倘若发送端send一个很大的buf,而接收端如果只能接收定长的buf的话就不能一次性处理，这个时候是不是要像文中那样自定义一个结构体包含buf长度和buf来构成一个通信协议来达成一次性处理
http又是怎么处理这种情况的，他是一次性还是分段呢</div>2019-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（1） 💬（1）<div>为什么像&quot;abcdef&quot;这样的字符串不需要端序转换，因为字符串的本质是char类型的数组，虽然发送的时候可能会被分割成很多段，但是每个段都有相应的序号，接收端只要按照序号从小到大一组装，还是原来的字符串，这个段与段之间的顺序是由tcp协议栈保证的</div>2020-06-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（1） 💬（1）<div>哦，是调用read或者recv读取的时候会移动协议栈接收缓冲区的指针是吗？这样每次都是在上一次的后面开始读取的</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（1） 💬（1）<div>有点疑惑  对于两种方案，不管是数字还是换行符，都有可能在报文的内容中出现，怎么区分是报文正文还是分隔符呢</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9d/ab/6589d91a.jpg" width="30px"><span>林林</span> 👍（1） 💬（1）<div>老师，关于大小端的问题，服务端和客户端互相发包的情况下，为了安全起见，是不是都应该统一进行大小端处理？比如发包都得先转成大端数据，收包再转成机器的顺序？(无论是字符数据还是数值数据)</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（1）<div>第1问:
大胆猜测因为http是以回车换行作为分界符但是在程序在编码过程中有可能随时只产生一个回车符
第2问:
tcp分组格式 是tcp层面的东西 而本文提到的报文是应用层方面的东西,联系在于tcp层面的分组可能导致数据流出现意想不到的情况,只有通过应用层处理成想要的情况

我记得之前公司解析字节流的时候是以字符0作为结束符,通过字符0 分割出一段数据流 然后通过类型转换 比如( char* ) pbuff转换成字符串或者其他类型的数据,编码的时候也是把数据的编码进去最后添加一个字符0</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（2）<div>老师同学好，文中&quot;我们并不需要关心主机到底是什么样的字节顺序，只要使用函数给定值进行网络字节序和主机字节序的转换就可以了。&quot;，不太明白为什么，这里的给定值，比如，端口号5678【不是以二进制存储到内存中？如何知道系统是采用大端字节序还是小端？】，直接使用函数进行处理即可？ </div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（1）<div>老师同学好，看到另外专栏的老师的文章内容：

此外，UTF-8 的编码单元为一个字节（也就是一次编解码一个字节），所以我们在处理 UTF-8 方案表示的 Unicode 字符的时候，就不需要像 UTF-32 方案那样考虑字节序问题了。相对于 UTF-32 方案，UTF-8 方案的空间利用率也是最高的。

UTF-8 的编码不考虑字节序？不是很明白。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/25/c7/edd74dfb.jpg" width="30px"><span>淡C</span> 👍（0） 💬（1）<div>那个u_int32_t msg_length是如何指向消息长度的;</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（0） 💬（1）<div>这里面的流和http中post请求时携带的body体中的流是一回事吗</div>2021-12-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（0） 💬（1）<div>原文：最后我们看到 23 行实际发送的字节流大小为消息长度 4 字节，加上消息类型 4 字节，以及标准输入的字符串大小。
这里是 33 行吧。

原文：注意这里使用了 htonl 函数将字节大小转化为了网络字节顺序，这一点很重要。
1. 为什么很重要呀？为啥 type 字段不需要转换：message.message_type = htonl(1)？

2. 显式编码报文长度的方式，socket 会不会读取到其他连接请求剩余的数据（比如开启了 net.ipv4.tcp_tw_reuse），导致解析之后的字符错误了？

3. http 的回车换行符为报文协议边界，每次读取一行的数据，如何辨别哪几行数据是同一个请求的呀？

谢谢老师</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/8a/f4/a4243808.jpg" width="30px"><span>卡布猴纸</span> 👍（0） 💬（1）<div>老师你好，如果结构体不是严格的对齐方式。那么在结构体中会出现空洞，用来结构体对齐。这样的话，除了通过结构#pragma pack(1)取消对齐，保证结构体是紧凑的。对于结构化的非对齐的数据传输的处理方式怎么处理比较好</div>2021-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（0） 💬（2）<div>read_message里面第6行调用readn读取4个字节的msg_length， 11行又调用readn读取4个字节的msg_type,读取msg_type的时候协议栈是怎么知道要从第4个字节开始的呢？</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b3/17/19ea024f.jpg" width="30px"><span>chs</span> 👍（0） 💬（1）<div>老师请问这个客户端协议的发送顺序是怎样的？是按照协议里字段的定义顺序发送即先发送数据长度然后发送数据类型最后是发送数据？</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/54/55/613ddc42.jpg" width="30px"><span>Edison</span> 👍（0） 💬（2）<div>老师，我在Linux平台下，照着你的程序写了一遍，客户端发数据，但是好像服务端不能够把数据包给解析出来。</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/24/e1329796.jpg" width="30px"><span>甘远林</span> 👍（0） 💬（1）<div>大小端问题，如果两边机器的大小端一样，这样两边都不转也没问题吧</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5a/9e/8f2ccc1d.jpg" width="30px"><span>有点意思</span> 👍（0） 💬（1）<div>老师好
问题是这样的：
客户端这边有两个线程：
一个线程采集网卡流量存到环形缓冲区，另外一个线程从环形缓冲区读取并发送
格式是：四字节长度+具体内容
服务端收到后，根据提取到的长度去读取具体内容
但是在程序运行了一段时间后，发现服务端处理报文出错了，原因是提取的长度是0,
现在想到的是遇到这种特殊情况，直接断开连接在连，但是总感觉这样处理不好，有点应付差事一样
我现在有个疑问  出现这种情况是不是一定是服务端拆包的逻辑或者客户端组包的逻辑出了问题 除此之外不会再有其他原因了
使用原生socket在两台机子间发送接收大数据量的网卡流量 是不是一定能做到可靠没问题？
</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>这个字节序转换是不是IP地址，端口，数据都要啊</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/39/11904266.jpg" width="30px"><span>Steiner</span> 👍（0） 💬（1）<div>当我用htonl(999999999)时netstat -tanlp 显示的IP地址是0.0.0.0，数字小一点再试一次是127.0.0.1 当初地址绑定是就是127.0.0.01，这是怎么回事</div>2019-09-11</li><br/>
</ul>