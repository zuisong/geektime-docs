你好，我是盛延敏，这里是网络编程实战第4讲，欢迎回来。

在上一讲里我们介绍了IPv4、IPv6以及本地套接字格式，这一讲我们来讲一讲怎么使用这些套接字格式完成连接的建立，当然，经典的TCP三次握手理论也会贯穿其中。我希望经过这一讲的讲解，你会牢牢记住TCP三次握手和客户端、服务器模型。

让我们先从服务器端开始。

## 服务端准备连接的过程

### 创建套接字

要创建一个可用的套接字，需要使用下面的函数：

```
int socket(int domain, int type, int protocol)
```

domain就是指PF\_INET、PF\_INET6以及PF\_LOCAL等，表示什么样的套接字。

type可用的值是：

- **SOCK\_STREAM: 表示的是字节流，对应TCP；**
- **SOCK\_DGRAM： 表示的是数据报，对应UDP；**
- **SOCK\_RAW: 表示的是原始套接字。**

参数protocol原本是用来指定通信协议的，但现在基本废弃。因为协议已经通过前面两个参数指定完成。protocol目前一般写成0即可。

### bind: 设定电话号码

创建出来的套接字如果需要被别人使用，就需要调用bind函数把套接字和套接字地址绑定，就像去电信局登记我们的电话号码一样。

调用bind函数的方式如下：

```
bind(int fd, sockaddr * addr, socklen_t len)
```

我们需要注意到bind函数后面的第二个参数是通用地址格式`sockaddr * addr`。这里有一个地方值得注意，那就是虽然接收的是通用地址格式，实际上传入的参数可能是IPv4、IPv6或者本地套接字格式。bind函数会根据len字段判断传入的参数addr该怎么解析，len字段表示的就是传入的地址长度，它是一个可变值。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/14/97/8a3aa317.jpg" width="30px"><span>疾风知劲草</span> 👍（211） 💬（18）<div>之前看过一些文章解释，为什么tcp建立连接需要三次握手，解释如下

tcp连接的双方要确保各自的收发消息的能力都是正常的。
客户端第一次发送握手消息到服务端，
服务端接收到握手消息后把ack和自己的syn一同发送给客户端，这是第二次握手，
当客户端接收到服务端发送来的第二次握手消息后，客户端可以确认“服务端的收发能力OK，客户端的收发能力OK”，但是服务端只能确认“客户端的发送OK，服务端的接收OK”，
所以还需要第三次握手，客户端收到服务端的第二次握手消息后，发起第三次握手消息，服务端收到客户端发送的第三次握手消息后，就能够确定“服务端的发送OK，客户端的接收OK”，
至此，客户端和服务端都能够确认自己和对方的收发能力OK，，tcp连接建立完成。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（95） 💬（4）<div>这个问题的本质是, 信道不可靠, 但是通信双发需要就某个问题达成一致. 而要解决这个问题, 无论你在消息中包含什么信息, 三次通信是理论上的最小值. 所以三次握手不是TCP本身的要求, 而是为了满足&quot;在不可靠信道上可靠地传输信息&quot;这一需求所导致的</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c0/cb5341ec.jpg" width="30px"><span>leesper</span> 👍（55） 💬（1）<div>思考题1：非阻塞调用的场景就是高性能服务器编程！我所有的调用都不需要等待对方准备好了再返回，而是立即返回，那么我怎么知道是否准备好了？就是把这些fd注册到类似select或者epoll这样的调用中，变多个fd阻塞为一个fd阻塞，只要有任何一个fd准备好了，select或者epoll都会返回，然后我们在从中取出准备好了的fd进行各种IO操作，从容自然 ^o^</div>2019-08-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（51） 💬（1）<div>关于三次握手
几句话解释清楚
1.信道不安全 保证通信需要一来一回
2.客户端的来回和服务端的来回 共四次 这是最多四次
3.客户端的回和服务端的来合并成一个，就是那个sync k ack j+1
4.这样就是三次握手
</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d2/a5/7acbd63a.jpg" width="30px"><span>eddy</span> 👍（30） 💬（5）<div>有个问题, 一次面试中遇到的, 客户端的第三次应答, 服务器没有收到, 然后客户端开始发消息给服务器, 这时候服务器和客户端的表现是什么? 客户端会收到什么返回?</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（14） 💬（1）<div>学完这节，感觉TCP的三次握手机制，更明白了一些，相信此生都会记得，养成了翻评论的习惯，感觉有些同学的解释比老师的还要通俗易懂。
我的小结如下，假设只有客户端C和服务端S，两台机器：
1：啥是TCP的三次握手机制？
TCP的三次握手机制，是C和S使用TCP协议进行通信，他们在正式建立链接前，先进行了三次简单的通信，只有这三次简单的同学成功了，才建立正式的连接，之所以说是简单的通信，因为这三次通信发送的消息比较简单，就是固定格式的同步报文和确认报文

2：TCP的三次握手机制的目的是啥？
TCP协议的设计目标之一，就是保证通信信道的安全，而TCP的三次握手机制就是用于确认信道是否安全的手段之一，确认信道安全，最基本的首先要确认C和S都具备信息首发的能力吧！也就是C要确定S能收发信息，S要确定C能收发信息，咋确认呢？那就发送一条消息实验一下呗！所以，就有了TCP的三次握手机制，TCP的三次握手机制的核心目标就是要确认C和S之间的通信信道是安全的。

3：为啥是三次？
按道理来讲，C要确认S是否能够正确的收发消息，需要发生一条消息给S，然后接收到S的一条确认收到的消息才行，这一来一回就是两条消息。同理，S要确认C是否能够正确的收发消息，也需要这么玩。这样就需要两趟一来一回，总共需要四次通信，其实这么玩思维上一点负载都是没有的自然而然。
不过只是为了确认C和S能否正常通信的话，就如此设计，被聪明一看到就会骂傻X，人类孜孜不倦所追求是更快、更高、更强，计算机世界中这种追求更加的强烈，将S的确认收到C发送的消息和S能正常发生的消息一次性的都发给C岂不是更好，虽然增加了点消息的内容，但是相对于消息的传输消耗而言还是非常少的，而且从整体消耗上看，是减少了一次通信的过程，性能想必会更好。
很明显一次握手、两次握手都确认不了C和S的收发消息的能力是否OK。三次握手是比较简洁有效的方式，大于三次之上的握手机制也可以确认C和S是否能够正常通信，不过有些浪费资源了，毕竟三次就能搞定的事情，没必要搞三次至少，毕竟对于性能的追求我们是纳秒必争的。</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（12） 💬（4）<div>Linux内核2.2之后，socket backlog参数的形为改变了，现在它指等待accept的完全建立的套接字的队列长度，而不是不完全连接请求的数量。 不完全连接的长度可以使用&#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_max_syn_backlog设置。
老师，这里你讲的backlog是未完成连接的队列，是不是有误？</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/00/6d14972a.jpg" width="30px"><span>Arthur.Li</span> 👍（8） 💬（1）<div>SYN：建立连接
FIN：关闭连接
ACK：响应
PSH：有DATA数据传输
RST：连接重置</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/24/ceac00af.jpg" width="30px"><span>dan</span> 👍（8） 💬（1）<div>&quot;请问能听见吗&quot;&quot;我能听见你的声音，你能听见我的声音吗&quot;
A先对B：你在么？我在的，我发一个消息看你能不能收到，我发J；
B收到后，回答：我收到了你发的J，你的发送和我的接收功能正常,回你J+1;并且，我给你发个消息K，看我的发送和你的接收是否正常？
A收到后，回答：我收到了你发的J+1和K，我回你K+1，告诉你的发送和我的接收正常；
通过前2次，表明：起点的发送和终点的接收，功能正常；
通过后2次，表明：终点的发送和起点的接收，功能正常；
由此保证：双方可以发送和接收对方的信息。</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/78/6b/9451a800.jpg" width="30px"><span>weeeee</span> 👍（8） 💬（2）<div>老师好，有一个问题想请教您一下
服务器端的连接进入ESTABLISHED 状态，课程上说的是accept返回后才进入，但是我自己实验发现只要客户端发送ack后，也就是第三次握手完成就进入了ESTABLISHED 状态，和accept没有关系，请问一下老师是我哪里理解错了吗？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/91/65ff3154.jpg" width="30px"><span>_stuView</span> 👍（6） 💬（7）<div>sockfd里的这个fd代表什么</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/da/4f50f1b2.jpg" width="30px"><span>Knight²º¹⁸</span> 👍（5） 💬（3）<div>老师我有一个问题，编程语言中的IO模型和操作系统中的IO关系是什么？</div>2019-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b6/6c/bae0461c.jpg" width="30px"><span>浦上清风</span> 👍（4） 💬（1）<div>1. 非阻塞 == 异步通信 ？？？
2. 可以是可以，但是不安全？？？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（3） 💬（4）<div>思考题2 

客户端可以bind 指定使用固定端口来连接。 
没有bind 则会产生一个随机的端口来完成连接请求。

想到一个比较有意思的事情：

客户端bind 以后，对内网进行端口扫描，表象则是，远程随机端口，到本地固定端口完成通信。看似，是本地开启了服务。如果bind 80 443 22这些常规端口，则可以迷惑安全人员 😄 </div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（2） 💬（3）<div>老师 两个问题麻烦解答下
1.如果服务端 使用随机端口 那么客户端时怎么知道的 不使用随机的话 是客户端要先知道服务端的端口然后配置进去吗
2.三次握手时 每次通信的消息都加一  这个目的是什么 每次返回一个&quot;1&quot; 或者&quot;success&quot; 是不是也行?</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/ae/11dad6f3.jpg" width="30px"><span>啦啦的小猪</span> 👍（2） 💬（1）<div>listen的第二个参数backlog的值是规定ACCEPT队列大小的;当ACCEPT队列满了时后来的客户端，就会被放到syn队列中</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（2） 💬（3）<div>1. 非阻塞调用是不是通过回调函数完成的呢？ 

就是我调用完connect之后不等你，你处理完了通知我，我先去和其他服务端connect去了。是这样子嘛？

题外话:
搜索老师布置的题目的过程中，无意中看到了这么一个话题。客户端端发起connect,服务端不调用accept能不能成功？

顺着那篇文章看下去:
客户端的syn请求被响应的同时，被linux内核放到了syn队列中，而客户端向服务端发完ack之后，这个socket才会被移入accept队列中。(accept队列长度的大小就是listen方法的第二个参数backlog)

进入accpet队列的socket会被通知其相应监听的服务端进程，由服务端进程执行accept操作将这个socket取出来进行处理。

由此可见，服务端将这个socket移入accept队列后，就算连接创建成功了。而accept操作，是由服务进程发起的。所以，不执行accept操作，连接也可以创建成功，只是这个socket还没有被服务进程处理而积压在了accept队列中了。

不知道我看的文章写的对不对，可以再看看。其实我很期待老师分析这些问题，然后我们就可以有意想不到的收获!

(ps:目前看来，还没遇到太trouble的问题，理解起来太困难的篇幅。)</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（2） 💬（3）<div>老师，想问一下，为什么是三次握手，而不是四次、五次握手？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/95/12/33028a3f.jpg" width="30px"><span>小仙女</span> 👍（1） 💬（1）<div>accept队列中里面存放的是什么? 四元组，还是客户端传来的数据</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/b6/40/6060d233.jpg" width="30px"><span>徐衡</span> 👍（1） 💬（2）<div>为什么是四次挥手？
因为在关闭连接时，服务器收到对方的FIN报文时，仅仅表示对方不再发送数据了（还能接收数据），而自己也未必全部数据都发送给对方了，所以可以发送一些数据给对方后，再发送FIN报文给对方来表示同意现在关闭连接，因此，己方ACK和FIN一般都会分开发送，从而导致多了一次</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/55/3f0bc345.jpg" width="30px"><span>Ghost</span> 👍（1） 💬（1）<div>简单的就是
A：你能听到我说话吗？
B：听得到，你能听得到我说话吗？
A：听得到

保证通信的双方都是有接收跟发送消息的能力</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUgnMApgafcbOicQJYOlApkHf6AzxF5edzeXAtVNhwOZTh3WB5wtIrbf1Algg6Axy5rEfZjj0B6Ng/132" width="30px"><span>云端</span> 👍（1） 💬（6）<div>
您好:老师

int socket_init()
{
       struct protoent* protocol = NULL;
        protocol=getprotobyname(&quot;icmp&quot;);
        int sock=socket(AF_INET,SOCK_RAW,protocol-&gt;p_proto);

}

在外部两次调用该函数，icmp协议原始套接字返回文件描述符相同，每次都是sock=5,为什么？怎么才能在外部多次调用该函数时返回的上下文描述符不一样？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/02/fcab58d1.jpg" width="30px"><span>JasonZhi</span> 👍（1） 💬（1）<div>老师你好，没有响应SYN包和路由不通的错误怎么区分？在我看来两种情况都会没有响应SYN包？</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（1） 💬（2）<div>老师，关于listen函数的参数backlog的解释，说是未完成连接队列的大小，然后影响并发数。有点疑问。
listen函数为每个监听socket维护两个队列：未完成连接队列（SYN_RCVD状态）和已完成连接的队列（ESTABLISHED状态）。
backlog表示的是未完成连接队列的大小，那已完成连接的队列的大小的有限制吗？
关于并发的影响，如果都是已经建立连接的状态，那么并发还是取决于已完成连接的队列的大小的吧。
</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/13/104d9501.jpg" width="30px"><span>另一半棉花糖</span> 👍（1） 💬（1）<div>我认为bind函数的第三个参数实际上没啥用，有前两个参数就可以确定是哪种结构了，结构的最大长度也就确定了，根本不需要第三个参数，即便是地址长度可变的AF_UNIX类型，只要对路径按照字符串来解析就行了。

我理解bind函数的作用就是把socket的文件描述符与（ip地址,端口号）这个对儿绑定在一起，但如果这么理解的话，accept的时候会返回一个新的socket，这个新的socket是否对应一个新的端口号呢？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（1） 💬（2）<div>一直有一个疑惑，客户端通过指定服务端的ip+port(10.10.88.99:80)并创建一个socket去connect服务端，服务端接受到客户端的请求并创建一个新的连接socket去和客户端进行通信，那客户端通过之前创建的客户端socket给服务端发送信息时还是会往ip+port(10.10.88.99:80)上发送，我的问题是服务端如何得知当前发送消息过来的客户端是与之前创建的连接socket通信？</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/ca/4560f06b.jpg" width="30px"><span>zhchnchn</span> 👍（1） 💬（4）<div>这篇很是解惑，感谢。有2个问题想请教老师：
1. `socket`函数的参数`domain`的值，在`bind`函数的参数`addr`的`sin_family`中也需要设置，这样不是重复了吗？
2. `connect`函数出错返回可能的3种情况中，其中第1种“TIMEOUT 错误”和第3种“destination unreachable”，感觉都是连接不到服务端的IP，这两种情况有什么区别吗？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/1f/6bc10297.jpg" width="30px"><span>Allen</span> 👍（1） 💬（1）<div>客户端在connect之前可以调用bind函数绑定一个固定端口。但是通常，不建议这样做，因为操作系统自己随机分配端口，避免了自己分配端口带来端口冲突的问题；

====================================
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/62/3c6041e7.jpg" width="30px"><span>木小柒</span> 👍（1） 💬（2）<div>记得很久前学套接字，提供的例子就是客户端bind端口，基本第二次和以后在运行，就告诉端口被占用，那时候不懂，就换个端口再来一次</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f0/d9343049.jpg" width="30px"><span>星亦辰</span> 👍（1） 💬（1）<div>非阻塞，一般是把请求接收到的套接字传递给子进程或子线程，然后，主进程，主线程继续等待下一个请求。多数网络服务器都是这个路子吧</div>2019-08-09</li><br/>
</ul>