你好，我是盛延敏，这里是网络编程实战的第20讲，欢迎回来。

这一讲是性能篇的第一讲。在性能篇里，我们将把注意力放到如何设计高并发高性能的网络服务器程序上。我希望通过这一模块的学习，让你能够掌握多路复用、异步I/O、多线程等知识，从而可以写出支持并发10K以上的高性能网络服务器程序。

还等什么呢？让我们开始吧。

## 什么是I/O多路复用

在[第11讲](https://time.geekbang.org/column/article/126126)中，我们设计了这样一个应用程序，该程序从标准输入接收数据输入，然后通过套接字发送出去，同时，该程序也通过套接字接收对方发送的数据流。

我们可以使用fgets方法等待标准输入，但是一旦这样做，就没有办法在套接字有数据的时候读出数据；我们也可以使用read方法等待套接字有数据返回，但是这样做，也没有办法在标准输入有数据的情况下，读入数据并发送给对方。

I/O多路复用的设计初衷就是解决这样的场景。我们可以把标准输入、套接字等都看做I/O的一路，多路复用的意思，就是在任何一路I/O有“事件”发生的情况下，通知应用程序去处理相应的I/O事件，这样我们的程序就变成了“多面手”，在同一时刻仿佛可以处理多个I/O事件。

像刚才的例子，使用I/O复用以后，如果标准输入有数据，立即从标准输入读入数据，通过套接字发送出去；如果套接字有数据可以读，立即可以读出数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/05/431d380f.jpg" width="30px"><span>拂尘</span> 👍（52） 💬（3）<div>我一直很好奇，为啥说select函数对fd有1024的限制，找了点资料共勉：
首先，man select，搜索FD_SETSIZE会看到如下的内容
An fd_set is a fixed size buffer. Executing FD_CLR() or FD_SET() with a value of fd that is negative or is equal to or larger than FD_SETSIZE will result in undefined behavior. Moreover, POSIX requires fd to be a valid file descriptor.
其中最关键的是FD_SETSIZE，是在bitmap位图运算的时候会受到他的影响
其次，sys&#47;select.h头文件有如下定义：
#define FD_SETSIZE __FD_SETSIZE
typesizes.h头文件有如下定义：
#define __FD_SETSIZE 1024

由此，终于看到了1024的准确限制。

同时man里也说明了一个限制，不是0-1023的fd会导致未定义的行为。</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（16） 💬（9）<div>allreads = {0, 3};
老师，这一步是怎么实现的？没看出来
</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（14） 💬（4）<div>对于套接字可写状态中说的：套接字发送缓冲区足够大，怎么样算足够大呢？</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（12） 💬（5）<div>1：I&#47;O 多路复用的设计初衷就是解决这样的场景，把标准输入、套接字等都看做 I&#47;O 的一路，多路复用的意思，就是在任何一路 I&#47;O 有“事件”发生的情况下，通知应用程序去处理相应的 I&#47;O 事件，这样我们的程序就变成了“多面手”，在同一时刻仿佛可以处理多个 I&#47;O 事件。
2：select 函数就是这样一种常见的 I&#47;O 多路复用技术，使用 select 函数，通知内核挂起进程，当一个或多个 I&#47;O 事件发生后，控制权返还给应用程序，由应用程序进行 I&#47;O 事件的处理。

int select(int maxfd, fd_set *readset, fd_set *writeset, fd_set *exceptset, const struct timeval *timeout);

返回：若有就绪描述符则为其数目，若超时则为 0，若出错则为 -1

在这个函数中，maxfd 表示的是待测试的描述符基数，它的值是待测试的最大描述符加 1。
紧接着的是三个描述符集合，分别是读描述符集合 readset、写描述符集合 writeset 和异常描述符集合 exceptset，这三个分别通知内核，在哪些描述符上检测数据可以读，可以写和有异常发生。
三个描述符集合中的每一个都可以设置成空，这样就表示不需要内核进行相关的检测。
timeout设置成不同的值，会有不同的可能：
第一个可能是设置成空 (NULL)，表示如果没有 I&#47;O 事件发生，则 select 一直等待下去。
第二个可能是设置一个非零的值，这个表示等待固定的一段时间后从 select 阻塞调用中返回。
第三个可能是将 tv_sec 和 tv_usec 都设置成 0，表示根本不等待，检测完毕立即返回。这种情况使用得比较少。

3：内核通知我们套接字有数据可以读了，使用 read 函数不会阻塞。
内核通知我们套接字可以往里写了，使用 write 函数就不会阻塞。

读了几遍，感觉还是没有抓住核心，所以，就将文中的要点摘录下来。
对IO多路复用的大概理解是，通过select函数去监听一组文件描述符，如果有事件就绪就交给应用程序去做对应的处理。</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（11） 💬（1）<div>size_t rt = write(socket_fd, send_line, strlen(send_line));
if (rt &lt; 0) {
     error(1, errno, &quot;write failed &quot;);
 }
这个代码中有错吧，应该将size_t改为sszie_t，size_t为unsigned long，这样错误-1被转换了。</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/93/85/f5d9474c.jpg" width="30px"><span>乔丹</span> 👍（10） 💬（1）<div>老师，两个疑问：
1. 为什么socket_fd一定是3呢？ 
2. 如果socket_fd = 2000, 那么传入select函数的值就是2001了， 这样不是大于1024了吗？
这个点我没有想通。</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/02/cce1cf67.jpg" width="30px"><span>awmthink</span> 👍（7） 💬（1）<div>老师，哪种场景下需要多路复用　“写描述符”　呢？ 什么时候能写应用程序不知道吗？</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ed/1c662e93.jpg" width="30px"><span>莫珣</span> 👍（7） 💬（2）<div>我有些疑问，select的FD数组大小默认是1024，但是Linux的文件描述符大小一定不是1024，假设现在使用ulimit将一个进程可以打开的文件数设置成了65535，那么大于1024的文件描述符怎么加到FD数组中去呢，如果按照文本里说的，文件描述符代表数组下标的话不就加不进去了？

第二个问题，套接字有两个属性，接收低水位线和发送低水位线，当接收缓冲区中待接收的字节数大于接收低水位线，一个可读事件产生，那么如果永远都不能达到接收低水位线呢？
</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/aa/49bbb007.jpg" width="30px"><span>нáпの゛</span> 👍（5） 💬（2）<div>第一道题，理解管道也是文件，往管道输入数据和输出数据对应可读可写的就绪条件。
第二道题，我理解fd_set本身是数组，如果不传入描述字基数，无法得知fd_set的具体大小，应该是无法进行遍历操作的。</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（4） 💬（1）<div>“第一种是套接字发送缓冲区足够大，如果我们使用非阻塞套接字进行 write 操作，将不会被阻塞，直接返回。”
老师，请问这里是不是应该写成“如果我们使用阻塞套接字进行write操作......”才对？</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/31/17/02fc18b1.jpg" width="30px"><span>麻雀</span> 👍（4） 💬（1）<div>您好，
第一，想问下select是不是能够在处理数据的同时继续轮询（监听）是否有新的套接字来到，它的内部是不是多线程呢？因为accept就是因为单线程在处理数据时，不能对这段时间内到来的套接字进行监听。 
第二，FD_SET它是一个unsigned long数组，那么它怎么实现Bitmap，只是对数组的每个元素例如fd_set[10]对文件描述符为10的套接字来数据的时候设置为1吗？</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（3） 💬（1）<div>小明原来只在一个家书店里等着，后来发现等着无聊，回家，然后在去书店等；后来发现别的书店，索性就好几家一起问，问了这个去下一家，看看哪家书到了，就先买哪一家的。</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/f4/1e4d6941.jpg" width="30px"><span>打奥特曼的小怪兽</span> 👍（3） 💬（1）<div>关于 FD_SET() 函数，debug看了下内存结构，{0,3} 如果设置了，实际上存储的是 2^0 + 2^3 = 9,并不会像图示的在每个位置上设置1。</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/a8/fa10583f.jpg" width="30px"><span>imsunv</span> 👍（2） 💬（2）<div>内核通知我们套接字可以往里写了，使用 write 函数就不会阻塞 。
那么如果写的内容超过了 缓冲区的大小，会阻塞么</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/95/12/33028a3f.jpg" width="30px"><span>小仙女</span> 👍（2） 💬（1）<div>int select(int maxfd, fd_set *readset, fd_set *writeset, fd_set *exceptset, const struct timeval *timeout);
这里的fd_set 是什么结构

0:标准输入
1：标准输出
2：标准错误
3：socket

是这样吗？？
</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/00/9b49f42b.jpg" width="30px"><span>skye</span> 👍（2） 💬（2）<div>用select做多路复用，如果不用多线程，其中一路阻塞或者死锁了，那其它路就无法处理了，所以单线程处理的前提时没有阻塞和死锁，这样理解对吗？</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/41/ec/d0e2bfa4.jpg" width="30px"><span>Navelwort、</span> 👍（1） 💬（1）<div>如果select 检测到可写事件，但是缓冲区还不够大，不能完成应用层数据的全部拷贝，如果是阻塞类套接字，那write函数还是会阻塞吧？</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/35/079d04c8.jpg" width="30px"><span>向东</span> 👍（1） 💬（1）<div>32位整数，那么该数组的第一个元素对应于描述字0~31，第二个元素对应于描述字32~63，依此类推。 没读懂，解答一下？多谢🙏</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/d2/498cd2d1.jpg" width="30px"><span>程序员班吉</span> 👍（0） 💬（1）<div>有个地方没搞明白，明明监听了stdin和socket_fd，但for循环里的select传入的只有socket_fd + 1， 那select 是如何知道stdin的状态的呢？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/31/17/ab2c27a6.jpg" width="30px"><span>菜鸡互啄</span> 👍（0） 💬（1）<div>老师你好 看github上面的代码 塞进set的描述字没有设置非阻塞的。看相关资料 最佳实践是说要设置成非阻塞的。原因是select返回时并不能完全保证read读到数据 也有可能会阻塞。老师认可吗</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b4/3c/e4a08d98.jpg" width="30px"><span>Janus Pen</span> 👍（0） 💬（1）<div>两个疑问：
我感觉select没想讲清楚；
1、第 17 行是每次测试完之后，重新设置待测试的描述符集合。你可以看到上面的例子，在 select 测试之前的数据是{0,3}，select 测试之后就变成了{0}。那24行还判断什么了，结果肯定是0;
2、13和14行吧allreads[0] 和 allreads[3]设置成了1；FD_ISSET 对这个向量进行检测，判断出对应套接字的元素 a[fd]是 0 还是 1。本来就是1，经过select处理后，对这个1有什么影响？FD_ISSET判断感觉没有意义</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a9/ce/23f2e185.jpg" width="30px"><span>Running man</span> 👍（0） 💬（1）<div>这里FD_SET应该放在循环体内部吧</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b9/7c/afe6f1eb.jpg" width="30px"><span>vv_test</span> 👍（0） 💬（1）<div>第二道我是这样理解的，因为fd_set大部分是底层是数组维护，那么程序为了扩展性，一般会设置得比较大，比如初始化是10，那么其实当前是只用到了4，那传入基数是不是就可以把后面的忽略掉了。回头再来验证一下。</div>2021-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/dd/6e/8f6f79d2.jpg" width="30px"><span>YUAN</span> 👍（0） 💬（1）<div>为什么把fd_set用位向量实现，用set实现不就不需要对无用位进行测试了吗？例如我想检测0和1023。我只要检测两个位，但是使用fd_set就要检测1024个。</div>2020-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/aa/49bbb007.jpg" width="30px"><span>нáпの゛</span> 👍（0） 💬（1）<div>老师，如果放了1024个句柄，相当于要把句柄集合存起来，遍历每一个判断FD_ISSET 做处理是吗？</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（0） 💬（2）<div>老师经常喜欢用rc作变量名，想求问一下这个rc是哪两个单词的缩写~</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/5b/c7e9fa5f.jpg" width="30px"><span>ABC</span> 👍（0） 💬（1）<div>可读 可写的监控我看里面包含了一些异常情况，那exceptset这个一般在什么场景使用？</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（0） 💬（1）<div>1. 套接字准备好读的就绪条件第一条，为啥是通过非阻塞套接字进行write操作，直接返回；不应该是阻塞套接字么？
2. 套接字准备好读的就绪条件第三条，为啥是通过write读操作啊</div>2020-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIRm3kWsgiaEXjO0rr0Aiav7o89StFTFSXbLTkEmiaibmnw8EQTejibrtzKla0emibePT0R0KXjFRIpfXrQ/132" width="30px"><span>zhang</span> 👍（0） 💬（3）<div>问一个关于writefds的问题。有两个线程，以及一块要发送的内存buffer。第一个线程是创建了socket，设置为none blocking，并在select监听，代码类似select(max_fd+1, &amp;read_fds, &amp;write_fds, NULL, NULL)，在监听到writefds中if(FD_ISSET(client.sd, &amp;write_fds))，从内存buffer中取出数据发送出去。第二个线程写入了一些字节到内存buffer，但怎么唤醒第一个线程还处于阻塞的select？
我试验第二个线程写入字节到内存buffer后调用FD_ZERO(&amp;write_fds);FD_SET(client.sd, &amp;write_fds);。第一个线程的if(FD_ISSET(client.sd, &amp;write_fds)) { processSendRingBuf(); FD_ZERO(&amp;write_fds); }。但并没有唤醒select。</div>2019-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/tjhOILHBAmlx6YiaTZJzqzxn1uyB6XpdvGDIZhBn127TYEcoLLzxRiaKvtVd3HllQqPx7cqf2YmibyBUgGGGJPDkw/132" width="30px"><span>zmysang</span> 👍（0） 💬（1）<div>为什么描述字集合{0,1,4}，对应的 maxfd 是 5，而不是 4，就比较方便了。因为这个向量对应的是下面这样的：a[4],a[3],a[2],a[1],a[0]，待测试的描述符个数显然是 5。
请问老师这里的意思是假设待检测的描述字集合是{0，100}，那么实际上select函数会判断0-100这101个fd中值为1的fd,然后对其检测吗？</div>2019-11-18</li><br/>
</ul>