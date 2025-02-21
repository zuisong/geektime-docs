你好，我是盛延敏，这里是网络编程实战的第14讲，欢迎回来。

在前面的基础篇中，我们已经接触到了UDP数据报协议相关的知识，在我们的脑海里，已经深深印上了“**UDP 等于无连接协议**”的特性。那么看到这一讲的题目，你是不是觉得有点困惑？没关系，和我一起进入“已连接”的UDP的世界，回头再看这个标题，相信你就会恍然大悟。

## 从一个例子开始

我们先从一个客户端例子开始，在这个例子中，客户端在UDP套接字上调用connect函数，之后将标准输入的字符串发送到服务器端，并从服务器端接收处理后的报文。当然，向服务器端发送和接收报文是通过调用函数sendto和recvfrom来完成的。

```
#include "lib/common.h"
# define    MAXLINE     4096

int main(int argc, char **argv) {
    if (argc != 2) {
        error(1, 0, "usage: udpclient1 <IPaddress>");
    }

    int socket_fd;
    socket_fd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in server_addr;
    bzero(&server_addr, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERV_PORT);
    inet_pton(AF_INET, argv[1], &server_addr.sin_addr);

    socklen_t server_len = sizeof(server_addr);

    if (connect(socket_fd, (struct sockaddr *) &server_addr, server_len)) {
        error(1, errno, "connect failed");
    }

    struct sockaddr *reply_addr;
    reply_addr = malloc(server_len);

    char send_line[MAXLINE], recv_line[MAXLINE + 1];
    socklen_t len;
    int n;

    while (fgets(send_line, MAXLINE, stdin) != NULL) {
        int i = strlen(send_line);
        if (send_line[i - 1] == '\n') {
            send_line[i - 1] = 0;
        }

        printf("now sending %s\n", send_line);
        size_t rt = sendto(socket_fd, send_line, strlen(send_line), 0, (struct sockaddr *) &server_addr, server_len);
        if (rt < 0) {
            error(1, errno, "sendto failed");
        }
        printf("send bytes: %zu \n", rt);
        
        len = 0;
        recv_line[0] = 0;
        n = recvfrom(socket_fd, recv_line, MAXLINE, 0, reply_addr, &len);
        if (n < 0)
            error(1, errno, "recvfrom failed");
        recv_line[n] = 0;
        fputs(recv_line, stdout);
        fputs("\n", stdout);
    }

    exit(0);
}
```

我对这个程序做一个简单的解释：

- 9-10行创建了一个UDP套接字；
- 12-16行创建了一个IPv4地址，绑定到指定端口和IP；
- **20-22行调用connect将UDP套接字和IPv4地址进行了“绑定”，这里connect函数的名称有点让人误解，其实可能更好的选择是叫做setpeername**；
- 31-55行是程序的主体，读取标准输入字符串后，调用sendto发送给对端；之后调用recvfrom等待对端的响应，并把对端响应信息打印到标准输出。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/5kv7IqibneNnMLqtWZQR5f1et8lJmoxiaU43Ttzz3zqW7QzBqMkib8GCtImKsms7PPbWmTB51xRnZQAnRPfA1wVaw/132" width="30px"><span>Geek_63bb29</span> 👍（27） 💬（3）<div>老师，面试过程中问道udp如何实现可靠性，这个怎么答呀。要求具体每部实现</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/e7/9ce305ec.jpg" width="30px"><span>Sancho</span> 👍（16） 💬（1）<div>老师，你好。我有两个疑问：
1.不进行connect操作，UDP套接字与服务端的地址和端口就没有产生关系，那recvfrom是怎么收到对应的报文呢？
2.UDP的connect操作，会引发内核的ICMP报文发送？如果不是，ICMP是在什么时机下发送的？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（10） 💬（2）<div>问题1：亲测可以；
问题2：可以参考https:&#47;&#47;yq.aliyun.com&#47;articles&#47;523036。</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/ae/a6d5e24a.jpg" width="30px"><span>🐗Jinx</span> 👍（7） 💬（1）<div>对于广播的话，先把广播的option打开。然后再 connect 255.255.255.255 对吗？</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（6） 💬（4）<div>按照老师的说法，只有connect才建立socket和ip地址的映射；那么，如果不进行connect，收到信息后内核又是如何把数据交给对应的socket呢</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（5） 💬（1）<div>还是不太理解为什么UDP的sendto方法会有一个&quot;连接&quot;过程的性能损耗，直接按照目标地址发过去不就可以了吗？我的理解是操作系统会先用ICMP协议探一探目标地址是否存在，然后再用UDP协议发送具体的数据，不知道理解的对不？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/54/85/ab5148ce.jpg" width="30px"><span>duckman</span> 👍（2） 💬（1）<div>connect 将一个socket绑定到一个udp的客户端进程，其他的udp客户端进程想要再次绑定该socket(4元组)发送数据的时候就会报错。所以connect起到了 &quot;声明式&quot;独占的作用?</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（2） 💬（1）<div>udp 连接套接字 这个是什么过程？ 断开套接字这又是什么过程呢？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/71/9d4eead3.jpg" width="30px"><span>孙升</span> 👍（1） 💬（1）<div>发现在输入完goodbye之后，服务端执行exit,后面client再去请求的时候又会被阻塞而不是返回错误，是因connect是单次操作吗？</div>2021-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep1aHicNquR3ETTicbInlCpfawcDMB8ILYyzegVTubTgQ0w6icarsK7fglpZVr7VfiaJaQ0eokNAHVYLA/132" width="30px"><span>一个戒</span> 👍（1） 💬（1）<div>老师，请问第一个程序中，在没有开启服务端的情况下开启客户端，不会在第20行connect的时候就error报错了吗？为什么还能接收标准输入并send出去？</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5b/12/b9ec95e2.jpg" width="30px"><span>n3bul2</span> 👍（1） 💬（1）<div>老师，我想问一下第一个问题，多次绑定connect是怎么弄的呢？</div>2020-05-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJWFdKjyLOXtCzowmdCUFHezNlnux4NPWmYsqETjiaHNbnmb7xdzibDncZqP06nNbpN4AhmD76cpicfw/132" width="30px"><span>fhs</span> 👍（1） 💬（1）<div>请问一下，在客户端的代码中，在send之前进行了connect。测试发现，不启动服务端的情况下，使用使用客户端send的函数的返回值是输入的字节数，既然文章说到&quot;因为对应的地址和端口不可达，一个ICMP报文会返回给操作系统内核，该ICMP报文含有目的地址和端口等信息&quot;，那为什么send函数返回是成功，而recv就返回失败呢？send的时候不应该也能知道icmp报文返回错误而返回错误么？</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（1）<div>老师 文中提到的icmp报文 发源地 是本机的网卡吗？</div>2019-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er5SNsSoiaZw4Qzd2ctH4vtibHQordcLrYsX43oFZFloRTId0op617mcGlrvGx33U8ic2LTgdicoEFPvQ/132" width="30px"><span>Frankey</span> 👍（0） 💬（1）<div>连接套接字是需要一定开销的，比如需要查找路由表信息。
这个路由表信息是什么？</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/11/9c55033e.jpg" width="30px"><span>MuteX</span> 👍（0） 💬（1）<div>提一个细节，sendto&#47;recvfrom和send&#47;recv的返回值类型是ssize_t，也就是long，而文章例子中很多地方用的是size_t，也就是unsigned long，很显然会导致问题。</div>2021-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4rbCWDxib3FHibYBouTwZqZBH6h5IgvjibEiaBv4Ceekib9SYg0peBBlFGu8hDuGvwjKp6LNznvEAibYw/132" width="30px"><span>DonaldTrumpppppppppp</span> 👍（0） 💬（2）<div>不调用connect时，有个评论问题老师你是这么答的。1.是通过sendto函数来绑定服务端地址的，之后再通过recvfrom引用到之前的socket，这样收到的报文就是指定的服务地址和端口了。  难道recvfrom不是收到后再填充from的地址的吗，还可以指定从某个服务端收数据？任何一个服务端只要知道了客户端的ip和端口就能发，客户端没有拒绝的权力吧</div>2021-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（0） 💬（1）<div>还是不太理解为什么UDP的sendto方法会有一个&quot;连接&quot;过程的性能损耗，直接按照目标地址发过去不就可以了吗？我的理解是操作系统会先用ICMP协议探一探目标地址是否存在，然后再用UDP协议发送具体的数据，不知道理解的对不？
我也同意这个说法，可能客户端提前connect可以解决不用sendto以后，是否可以到达服务器，省的堵塞在recv函数里面了，同时使用connect可以提前判断服务器是否存在，至于是否会节省性能这需要抓包分析</div>2021-05-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKn2fx2UTaWgMl3fSOSicJEDOibbtYicHUVSG8JsA8j6Njibc9j3YVSvHtMZb2Z20l4NmjibiaSv8m7hz9w/132" width="30px"><span>Geek_de83f6</span> 👍（0） 💬（2）<div>为什么我在第一个实例中，没有打开服务器，然后客户端connect并且send了之后，在recv的地方阻塞了，并没有收到connect失败的消息呢？</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/67/03c95ec2.jpg" width="30px"><span>守望</span> 👍（0） 💬（1）<div>老师您好，文中提到udp性能问题，connect一定程度上是可以提高性能的，不过在一般机器上测试发现，一个进程收一个进程发的状态下，貌似tcp每秒能收发的包要比tcp多？另外，如果个客户端发送，tcp可以一个线程处理一个连接请求，不断收包，而udp似乎不可以？即便在端口重用的情况下，tcp可以通过多进程接收数据，而udp同端口接收数据是否被限制住了，即和一个进程一个端口的收包能力差不多，因为同用一个udp缓冲区。

以上，是对udp和tcp性能的疑问，从上面看以及实际测试，tcp的性能似乎好于udp（每秒收包能力），但是理论上来说，udp.发送简单，不需要ack应答之类，不是应该会更快？不知道老师有什么见解？感谢。</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/19/a235f31d.jpg" width="30px"><span>云淡风轻</span> 👍（0） 💬（2）<div>老师您好，按照你文章中的代码我运行了一下，client 发送 “goodbay&quot; 后直接阻塞到了recvfrom，没有像未启动服务器下的直接报错，文章中不是说connect 后就可以收到操作系统内核返回的错误信息吗？</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（3）<div>老师，在我的电脑上，测试例子udpconnectclient2.c（里面使用的是send） 通不过，报没有那个文件，使用udpconnectclient.c(里面调用的是sendto)可以通过，什么情况，</div>2020-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（0） 💬（1）<div>老师，在python里UPD加connetion没有作用呢</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f2/48/d5b30171.jpg" width="30px"><span>凤梨酥</span> 👍（0） 💬（1）<div>这个recvfrom得知icmp获取异常有时效性吗？ 如果之前连接失败，下一秒服务端又打开了呢</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/20/8b1291ad.jpg" width="30px"><span>神秘的火柴人</span> 👍（0） 💬（1）<div>在 实现一个 connect 的客户端程序 章节中，“客户端 2 从操作系统内核得到了 ICMP 的错误，该错误在 recv 函数中返回，显示了“Connection refused”的错误信息“，这里的错误是在connect函数中返回吧</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（1）<div>老师我们遇到一个问题，A--》B发送UDP报文，发现在B上用tcpdump可以抓到udp报文信息，但是，用nc -ul 启动端口的却收不到报文，后面检查了下发现B上对A网段的路由走的是另外一个网卡eth1，而A发送到B的UDP包走的是eth0网卡，我把B上对A网段的路由改成也用eth0网卡，就正常了，请问老师是什么原因那？谢谢</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>老师 include &quot;lib&#47;common.h&quot; 这个头文件在哪里</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（3）<div>在我电脑上，第一个案例的现象是阻塞在了connect函数上</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b4/f6/735673f7.jpg" width="30px"><span>W.jyao</span> 👍（0） 💬（1）<div>第一个留言的问题，程序不调用connect的话是因为recvfrom带有目标地址吧，</div>2019-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqyicZYyW7ahaXgXUD8ZAS8x0t8jx5rYLhwbUCJiawRepKIZfsLdkxdQ9XQMo99c1UDibmNVfFnAqwPg/132" width="30px"><span>程序水果宝</span> 👍（42） 💬（0）<div>对于recvfrom函数，我们可以看成是TCP中accept函数和read函数的结合，前三个参数是read的参数，后两个参数是accept的参数。对于sendto函数，则可以看成是TCP中connect函数和send函数的结合，前三个参数是send的参数，后两个参数则是connect的参数。所以udp在发送和接收数据的过程中都会建立套接字连接，只不过每次调用sendto发送完数据后，内核都会将临时保存的对端地址数据删除掉，也就是断开套接字，从而就会出现老师所说的那个循环</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（1） 💬（0）<div>1、因为UDP调用connect并不会真正创建链接，所以多次调用都不会有问题。
2、connect到路由器中的广播地址</div>2021-12-05</li><br/>
</ul>