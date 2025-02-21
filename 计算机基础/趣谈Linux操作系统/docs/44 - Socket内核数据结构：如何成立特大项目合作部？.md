上一节我们讲了Socket在TCP和UDP场景下的调用流程。这一节，我们就沿着这个流程到内核里面一探究竟，看看在内核里面，都创建了哪些数据结构，做了哪些事情。

## 解析socket函数

我们从Socket系统调用开始。

```
SYSCALL_DEFINE3(socket, int, family, int, type, int, protocol)
{
	int retval;
	struct socket *sock;
	int flags;
......
	if (SOCK_NONBLOCK != O_NONBLOCK && (flags & SOCK_NONBLOCK))
		flags = (flags & ~SOCK_NONBLOCK) | O_NONBLOCK;

	retval = sock_create(family, type, protocol, &sock);
......
	retval = sock_map_fd(sock, flags & (O_CLOEXEC | O_NONBLOCK));
......
	return retval;
}
```

这里面的代码比较容易看懂，Socket系统调用会调用sock\_create创建一个struct socket结构，然后通过sock\_map\_fd和文件描述符对应起来。

在创建Socket的时候，有三个参数。

一个是**family**，表示地址族。不是所有的Socket都要通过IP进行通信，还有其他的通信方式。例如，下面的定义中，domain sockets就是通过本地文件进行通信的，不需要IP地址。只不过，通过IP地址只是最常用的模式，所以我们这里着重分析这种模式。

```
#define AF_UNIX 1/* Unix domain sockets */
#define AF_INET 2/* Internet IP Protocol */
```

第二个参数是**type**，也即Socket的类型。类型是比较少的。

第三个参数是**protocol**，是协议。协议数目是比较多的，也就是说，多个协议会属于同一种类型。

常用的Socket类型有三种，分别是SOCK\_STREAM、SOCK\_DGRAM和SOCK\_RAW。

```
enum sock_type {
SOCK_STREAM = 1,
SOCK_DGRAM = 2,
SOCK_RAW = 3,
......
}
```

SOCK\_STREAM是面向数据流的，协议IPPROTO\_TCP属于这种类型。SOCK\_DGRAM是面向数据报的，协议IPPROTO\_UDP属于这种类型。如果在内核里面看的话，IPPROTO\_ICMP也属于这种类型。SOCK\_RAW是原始的IP包，IPPROTO\_IP属于这种类型。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（13） 💬（1）<div>看了一遍，然后花了一天把源码又过了一遍，很有收货，对socket的理解不再浮于表面。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（5） 💬（1）<div>原来得先看总结图，再看内容。。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b4/f6/735673f7.jpg" width="30px"><span>W.jyao</span> 👍（3） 💬（1）<div>老师，能解释下listenfd和acceptfd的端口为什么一样吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/4f/f8868b94.jpg" width="30px"><span>无心之福</span> 👍（1） 💬（2）<div>开头的那个代码的 逗号加的不对吧？</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（0） 💬（2）<div>调用accept的时候,会新建一个socket,以及其对应的struct file,然后会从icsk_accept_queue 取出一个req,将其sk赋值给新建的socket-&gt;sk,这样就可以读取到请求的数据了,不理解的是后面讲到接收数据包时tcp层有三个队列,会根据内核低延时 高吞吐量的等策略以及socket当时的状态来决定放入哪个队列,这里的socket是怎么选出来的啊,数据包是先发送到处于监听队列的socket然后由其将数据分发到其通过accept生成的sokcet上吗,如果是直接由通过accept生成的socket来处理,怎么分辨出来到底该给哪个socket呢,根据数据包的源地址与端口吗?</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（0） 💬（3）<div>syn到底是个什么东西呀？是个integer还是char类型</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/00/2a248fd8.jpg" width="30px"><span>二星球</span> 👍（0） 💬（2）<div>老师好，同一个TCP链接上先后发送2次rpc请求，后发送的请求其结果先返回，先发送的请求结果后返回，这样有没有问题呢，系统能区分各自的返回结果么，靠什么机制保证的呢？一直没有想明白</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/90/8f/9c691a5f.jpg" width="30px"><span>奔跑的码仔</span> 👍（16） 💬（0）<div>struct tcp_sock继承自struct inet_connection_sock inet_conn，inet_connection_sock继承自struct inet_sock，struct inet_sock继承自struct sock；

1.上述四个结构的关系具有十足的面向对象的特征，struct是基类，通过层层继承，实现了类的复用；
2.内核中网络相关的很多函数，参数往往都是struct sock，函数内部依照不同的业务逻辑，将struct sock转换为不同的业务结构；
这样做的好处：
1.简化接口的设计复杂度；
2.使用基类作为参数，十分类似于面向对象中的多态特性，能够有效的增强接口的稳定性、提升扩展性。</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/8f/51f044dc.jpg" width="30px"><span>谛听</span> 👍（6） 💬（0）<div>socket: 根据参数创建相应socket
bind: 绑定IP、端口
listen: 建立两个队列，改变状态为TCP_LISTEN
accept: 从完成三次握手的队列中取出一个socket，没有的话让出cpu
connect: 三次握手
</div>2019-11-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epZhOmpZpicOzalVU7kibd59dMJc25N9cfGu9icBAIUPzYNYDedtzlYHZBiazaYiadgqvlotrjM4CA6KOQ/132" width="30px"><span>Geek_ty</span> 👍（1） 💬（0）<div>老师您好，我在认真阅读了文章和代码后还是存在一个疑惑：icsk_accept_queue是全连接队列当然没有问题，但是服务端LISTEN状态下，调用tcp_v4_conn_request()时inet_csk_reqsk_queue_hash_add()函数也是增加了该队列的长度。但是实际上应该修改的时半连接队列才对。我反复看了几遍源码，没有发现在什么地方有保存syn队列，也没有syn队列的相关操作，都是对icsk_accept_queue的操作，这让我十分困惑，还请老师帮忙解答。</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（1） 💬（0）<div>老师，请问服务端维护的未完全建立链接队列的元素sock是什么时候创建的呢？是每次收到客户端的SYN包后创建？还是listen时会初始化几个sock？</div>2019-10-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uG2kliaKAroGkNaXSwFNEmVz8xM6srw7OEHBMSBbPibuXQMctibLyuQEpRVmOth8sdojb3u5VUEjWm2D2lzRGuMDA/132" width="30px"><span>Geek_ae11ce</span> 👍（0） 💬（0）<div>一篇过于简单了，可能是函数较多的原因。实际更好的是一个函数或两个函数放在一章中</div>2024-05-31</li><br/><li><img src="" width="30px"><span>Geek_a9a743</span> 👍（0） 💬（0）<div>太复杂了……</div>2023-11-26</li><br/>
</ul>