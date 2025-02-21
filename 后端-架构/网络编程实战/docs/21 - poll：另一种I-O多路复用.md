你好，我是盛延敏，这是网络编程实战第21讲，欢迎回来。

上一讲我们讲到了I/O多路复用技术，并以select为核心，展示了I/O多路复用技术的能力。select方法是多个UNIX平台支持的非常常见的I/O多路复用技术，它通过描述符集合来表示检测的I/O对象，通过三个不同的描述符集合来描述I/O事件 ：可读、可写和异常。但是select有一个缺点，那就是所支持的文件描述符的个数是有限的。在Linux系统中，select的默认最大值为1024。

那么有没有别的I/O多路复用技术可以突破文件描述符个数限制呢？当然有，这就是poll函数。这一讲，我们就来学习一下另一种I/O多路复用的技术：poll。

## poll函数介绍

poll是除了select之外，另一种普遍使用的I/O多路复用技术，和select相比，它和内核交互的数据结构有所变化，另外，也突破了文件描述符的个数限制。

下面是poll函数的原型：

```
int poll(struct pollfd *fds, unsigned long nfds, int timeout); 
　　　
返回值：若有就绪描述符则为其数目，若超时则为0，若出错则为-1
```

这个函数里面输入了三个参数，第一个参数是一个pollfd的数组。其中pollfd的结构如下：

```
struct pollfd {
    int    fd;       /* file descriptor */
    short  events;   /* events to look for */
    short  revents;  /* events returned */
 };
```

这个结构体由三个部分组成，首先是描述符fd，然后是描述符上待检测的事件类型events，注意这里的events可以表示多个不同的事件，具体的实现可以通过使用二进制掩码位操作来完成，例如，POLLIN和POLLOUT可以表示读和写事件。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（27） 💬（5）<div>老师，我还是没明白poll和select的本质区别是什么，能否指点一下</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/3f/bbb8a88c.jpg" width="30px"><span>徐凯</span> 👍（20） 💬（1）<div>1.采用动态分配数组的方式
2.如果内存不够 进行realloc 或者申请一块更大的内存 然后把源数组拷贝过来</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（12） 💬（1）<div>还有种信号驱动型I&#47;O，老师可以讲解吗</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/03/b2d9a084.jpg" width="30px"><span>Hale</span> 👍（10） 💬（4）<div>能讲讲为什么不用POLLIN来判断套接字可读？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/0c/f39f847a.jpg" width="30px"><span>D</span> 👍（9） 💬（3）<div>老师可否简单讲下底层实现，比如底层是数组，队列，红黑树等。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9b/2d/f7fca208.jpg" width="30px"><span>fedwing</span> 👍（5） 💬（2）<div>老师，请教个问题，我看ready_number在29行的if里如果有会--，后面read for循环里，如果处理也--，我是不是可以这样理解，events_set[0]表示listen的套接字，这个套接字里如果有pollin，那么肯定是新连接（而不是普通套接字的读数据），所以这时就是获取对应的连接的文件描述符，将其加入到event_set数组里，用于后续poll的时候，多检测一个文件描述符，如果ready_number在前面的处理--后，还大于0，则表示events_set里其他的文件描述符也有待检测的事件触发，这些就是常规的双端连接对应的套接字，它们pollin的话，就是我们常规意义里的read数据了。</div>2020-08-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqf54z1ZmqQY1kmJ6t1HAnrqMM3j6WKf0oDeVLhtnA2ZUKY6AX9MK6RjvcO8SiczXy3uU0IzBQ3tpw/132" width="30px"><span>Geek_68d3d2</span> 👍（5） 💬（1）<div>老师我看网络编程里面使用了各种函数，函数里面各种参数，您那里有没有什么文档参考手册啥的可供我们需要时翻阅，光靠脑子记，记不来啊。您平常都是怎么写代码啊，这些函数都是背下来了吗。</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fa/84/f01d203a.jpg" width="30px"><span>Simple life</span> 👍（3） 💬（3）<div>我搞不懂，accept后的fd要加入event_set，然后再遍历取出，直接拿来读写不行吗？</div>2020-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（2） 💬（1）<div>老师 poll不改变传入检测的event的状态，而是返回revent，是出于什么目的呢？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（2） 💬（1）<div>我还是不太明白select和poll进行事件注册的区别,希望老师再给我指点指点</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（2） 💬（1）<div>第一问: 我觉得需要改进的原因在于他是一个固定死了的值,而很多时候我们都要考虑到扩容的问题,所以可以把所有的描述符push_back到一个vector等类似的容器当中,直接对容器取size就可以获得数量
第二问:把新连接上来的connfd添加进去,对上面问题的容器进行一次取size操作就行了
通过前面两个问题 我产生了第三个问题
我们都知道select 每次循环都需要向内核重新注册一次需要关心的描述符, 在Poll当中他是怎么处理的呢？也是每次都要注册一次吗？新增了描述放到集合当中肯定也需要通知内核啊 ！</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（2） 💬（1）<div>为什么程序里使用POLLRDNORM而不是POLLIN呢？这两者又何不同？</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（1） 💬（1）<div>老师 28行不是太明白 如果listen_fd有可读事件 为什么说明有连接要accept了？</div>2021-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIcxz0quUK7Q06aNC3qglvvpTQKOanK3suG0qQkK00Q815zF5oiad1wABibCkm8Lk18LmX8UQoUMS5Q/132" width="30px"><span>panda</span> 👍（1） 💬（1）<div>老师，什么情况下会使套接字数目多余select数目呢，我所理解的是一般服务端对一个套接字就会开一个线程，客户端一个进程也不会创建出很多套接字，感觉都不会导致数量过多的情况，求指点</div>2020-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/af/4307867a.jpg" width="30px"><span>JJj</span> 👍（1） 💬（1）<div>请问下，如果select同时关注可读、可写、异常。那是不是最多支持关注3*1024个IO事件</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/61/36/7a28f544.jpg" width="30px"><span>Jimmy Xiong</span> 👍（1） 💬（1）<div>请问老师，例子的全代码（可以直接运行起来）哪里可以找得到？</div>2019-09-28</li><br/><li><img src="" width="30px"><span>pippin</span> 👍（0） 💬（1）<div>套接字和文件描述符有什么区别
</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/c5/76/f7c24b63.jpg" width="30px"><span>你已经长大了，别皮</span> 👍（0） 💬（1）<div>老师服务器程序在49-68处理连接事件时，此时如果有新连接来，ready_number是否会++，这样是否会死循环？还是内核会存储起来，等待下一次poll时再往上报？</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/2d/dbb5570f.jpg" width="30px"><span>huadanian</span> 👍（0） 💬（1）<div>请问一下老师，上面代码第53行用于判断的revents的值，在第54行的read之后，是否需要清除掉，否则之后的循环会不会重复判断这个revents的值？？</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/62/78/6e7642a3.jpg" width="30px"><span>王蓬勃</span> 👍（0） 💬（1）<div>老师，为什么ready_number 的返回值一直都是1， 模拟了客户端一个个登录每次返回的都是1。
它只会返回1吗？</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/bd/acf40fa0.jpg" width="30px"><span>lwenbin</span> 👍（0） 💬（2）<div>老师
能否问一下对于 accept，每次只能处理一个吗？比如同时有100个client连接过来等待 accept，需要多次循环才能处理完吗？</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c0/cb5341ec.jpg" width="30px"><span>leesper</span> 👍（0） 💬（1）<div>在MacOS下写这个程序，只要struct pollfd[]数组超过256，poll()就报错退出了，查看man poll，说是数组长度超过了OPEN_MAX</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（3）<div>poll 是另一种在各种 UNIX 系统上被广泛支持的 I&#47;O 多路复用技术，虽然名声没有 select 那么响，能力一点不比 select 差，而且因为可以突破 select 文件描述符的个数限制，在高并发的场景下尤其占优势。

老师好，之前听过IO多路复用存在一个使CPU飙升的问题，不知具体是哪个IO多路复用函数引起的，具体原因是什么，怎么解决的，老师能否介绍一下？</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/6a/3272e095.jpg" width="30px"><span>李春恒</span> 👍（0） 💬（1）<div>老师讲的真好，非常感谢。</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（1）<div>我不太理解的是 之前好像理解到一个概念就是select每次轮训都会重新向内核注册需要关心的描述符这个缺点,那Poll呢？</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/da/ed4803cb.jpg" width="30px"><span>CCC</span> 👍（0） 💬（1）<div>&gt; lsof -i:43211
COMMAND     PID       USER   FD   TYPE             DEVICE SIZE&#47;OFF NODE NAME
pollserve 56364 jinhaoplus    3u  IPv4 0xd6b66f6bf4c36f21      0t0  TCP *:43211 (LISTEN)
pollserve 56364 jinhaoplus    4u  IPv4 0xd6b66f6bf3b80f21      0t0  TCP localhost:43211-&gt;localhost:63829 (ESTABLISHED)
pollserve 56364 jinhaoplus    5u  IPv4 0xd6b66f6bf49d05a1      0t0  TCP localhost:43211-&gt;localhost:63851 (ESTABLISHED)
pollserve 56364 jinhaoplus    6u  IPv4 0xd6b66f6bf427d921      0t0  TCP localhost:43211-&gt;localhost:63876 (ESTABLISHED)
telnet    56379 jinhaoplus    5u  IPv4 0xd6b66f6be79fc921      0t0  TCP localhost:63829-&gt;localhost:43211 (ESTABLISHED)
telnet    56381 jinhaoplus    5u  IPv4 0xd6b66f6be1866f21      0t0  TCP localhost:63851-&gt;localhost:43211 (ESTABLISHED)
telnet    56529 jinhaoplus    5u  IPv4 0xd6b66f6bf4944921      0t0  TCP localhost:63876-&gt;localhost:43211 (ESTABLISHED)

我开启了三个telnet客户端连接这个pollserver，老师能否解释下上面的lsof命令中为什么客户端持有的FD是这样的情况呢？客户端持有的FD不应该是各自的connectfd嘛？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/5d/5297717a.jpg" width="30px"><span>初见</span> 👍（0） 💬（1）<div>老师您好~

我们既然有了poll，是不是代表着select 可以废弃了呢？

还是说他们各自仍然有不同的使用场景？</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（2）<div>fd可读事件是不是有可能会误触发？也就是fd发生了可读事件，但是实际上并没有数据可读？ 所以我们要用非阻塞的读。 这是内核的一个bug吗？还是。。。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6c/a8/1922a0f5.jpg" width="30px"><span>郑祖煌</span> 👍（1） 💬（0）<div>1)第一道，可以用vector存储所有的连接描述符，然后当需要调用poll的时候，再用vector.size获取数组的大小，然后再创建出fd_set tmp[vector.size]存储所有需要的fd，将他传入到poll函数中。

</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>epoll背后，系统内核是不断轮询pollfds数组检查是否有事件吗？</div>2023-07-03</li><br/>
</ul>