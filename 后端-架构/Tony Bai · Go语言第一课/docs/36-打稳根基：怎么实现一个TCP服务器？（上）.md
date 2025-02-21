你好，我是Tony Bai。欢迎来到这门课的最后一个部分：实战篇。

在进入正文之前，我先来说点题外话。去年我读过一本名为[《陪孩子走过初中三年》](https://book.douban.com/subject/26935989/)的书，书中作者女儿的初中班主任有一句“名言”：“跟上了！”作者对这句名言的解读是：学习上，她强调孩子们学习的时候不要掉队，意思是一要跟上老师的步子，上课认真听讲，课后老师留的作业要不打折扣地去完成；二也要跟上年级和班级的进度。只要能紧紧地跟上，学习就不会有太大的问题。

在前面课程的留言区，我也经常用“**跟上了**”作为学习这门课的建议，和我一起同步走到这里的同学，都是践行“跟上了”这句“名言”的典范，从开篇词到现在，你是不是已经感受到了自己在Go语言方面的进步了呢？

好了，我们言归正传。关于最后一篇写啥，我也想了许久。开篇词中提过，实战篇的职责是带着你走完Go语言学习的“最后一公里”，那究竟什么是“最后一公里呢？该如何理解这最后一公里呢？

我的理解是，在掌握了前面的Go语言语法的前提下，这“最后一公里”就是**面对一个实际问题的解决思路**。很多语言初学者都有这样一个问题，即便学完了语法，面对一个实际问题时，还是也不知道该从何处着手。

其实这个事并没有那么难，尤其是程序员这一行，遇到一个实际问题，我们通常使用这个思路：
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/31/2a/4e/a3f53cae.jpg" width="30px"><span>撕影</span> 👍（5） 💬（1）<div>由于go的GPM模型存在，实现多路复用简直就是降维打击。只挂起G而不挂起M，在G的视角里就是个阻塞模型而已，妙啊</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b0/6e/921cb700.jpg" width="30px"><span>在下宝龙、</span> 👍（5） 💬（1）<div>老师我想问一下 按照老师你的图，select不是也阻塞了线程么，应用线程也不能做其他的事情，难道应用线程和select的线程不是同一个吗</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（5） 💬（1）<div>老师，有没有netpoller的相关实现资料参考？</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/96/0cf9f3c7.jpg" width="30px"><span>Aeins</span> 👍（3） 💬（1）<div>读完，好多细节还抓不住

1. go 中的 Socket 是操作系统 socket 的封装。go 通过 netpoller 模拟了阻塞式的I&#47;O，运行时还是使用的I&#47;O多路复用(不同操作系统提供了不同的系统调用，epoll等)

连接复用的情况

0. 读写都有锁保护

1. 多 goroutine 并发读，如何正确的指定度多少数据呢，给少了，会读不全，被其他 goroutine 读走，给多了，会读取不属于自己的数据吧。

2. 多 goroutine 并发写，如果一次写入一个完整的”业务包“，一般能保证单个业务包的完整
，如果写超时，会有部分写入问题吗？
一次写入一个业务包，TCP会从面向数据流，退化到面向业务包码？
读的一端，为了区分不同goroutine(共用连接，数据不共享)的数据，要采取特殊的读取方式吗，需要以包为单位读取？</div>2022-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（3） 💬（3）<div>谢谢老师。我跟上了。还特意买了你新出的Go语言精进之路1，2，打算过年继续精进。</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/d9/75dd7cf9.jpg" width="30px"><span>Mew151</span> 👍（2） 💬（2）<div>本节课的代码参见：https:&#47;&#47;github.com&#47;dgqypl&#47;tcpprogramming</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（2） 💬（1）<div>老师，有个地方想不清楚，请教一下。现在都是长连接复用一个tcp连接，这时服务端读取一个请求的部分数据后异常了，还有一部分数据未读取，这时下一个请求过来了，服务端应该怎么处理上一个请求遗留的那部分数据？因为tcp层面是没有业务语义的，怎么区分这部分数据要不要丢弃。</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>以前没接触过socket编程，只是经常看到这个知识点。感谢Tony Bai老师的细致讲解。有几点疑惑，烦请老师解答。

1. 我们的输入，是一个基于传输层自定义的应用层协议规范。 这里的输入该怎么理解呢？

2. 在阻塞 I&#47;O 模型下，并等所有数据就绪后，将数据从内核空间拷贝到用户空间，最后系统调用从内核空间返回。为什么不是用户空间返回呢？

3. 文中的非阻塞 I&#47;O 模型架构图中的：EAGAIN&#47;EWOULDBLOCK 这几个英文单词是什么意思，没查出来。</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（2） 💬（2）<div>老师，文章中“I&#47;O 多路复用框架”的举例中：
1、libev 的链接点击没反应（是 http:&#47;&#47;software.schmorp.de&#47;pkg&#47;libev.html 这个链接吗？）；
2、libuv 的链接对应的 github 仓库貌似已经迁移到 https:&#47;&#47;github.com&#47;libuv&#47;libuv 了。</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（3）<div>并发往 socket 中写数据时，需要一次 write 操作完整的写入一个“业务包”，这实现有点难呀，万一只成功写入一部分，这可不能回滚呀。</div>2022-01-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKEDxLO0wLibic5WkVl1x7TIL0fsxX1zl2GbRjutYQ89fGRrv2VKJtNmmJb32iarbcHROlmW8SOQsHag/132" width="30px"><span>X</span> 👍（1） 💬（1）<div>能把复杂的东西讲的老少皆宜,各层次人都能看懂，可见基础扎实,内功深厚,感谢老师！</div>2022-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>网络编程是自己的弱项，老师的这篇文章解决了我不少疑惑，需要再次消化。</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（1） 💬（1）<div>文中“我们以net&#47;fd_posix.go中的netFD为例看看”这里的fd_posix.go是不是有问题呀，我看下面代码引用注释里是fd_unix.go</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（1） 💬（2）<div>老师，文中的socket读设置超时时间的这个地方，“一旦通过这个方法设置了某个 socket 的 Read deadline，那么无论后续的 Read 操作是否超时，只要我们不重新设置 Deadline，那么后面与这个 socket 有关的所有读操作，都会返回超时失败错误。”这里是不是应该是“设置了某个socket的Read deadline，然后再发生了读超时，这个读超时后面如果不从新设置，后面所有的读操作都会返回超时失败错误呢？”。这里先是设置了，应该要发生读超时，才行吧？这里没看大懂</div>2022-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLBFkSq1oiaEMRjtyyv4ZpCI0OuaSsqs04ODm0OkZF6QhsAh3SvqhxibS2n7PLAVZE3QRSn5Hic0DyXg/132" width="30px"><span>ddh</span> 👍（1） 💬（1）<div>老师什么时候出Go语言第二课</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/68/373b90c8.jpg" width="30px"><span>River</span> 👍（1） 💬（1）<div>白老师，tc, ok := c.(*TCPConn) 这是什么用法？ 是把变量 c 强制转换成一个新的*TCPConn类型变量吗，并返回一个布尔值（表示强转是否成功吗？），变量后跟“.()”的用法既不像调用变量的属性也不想调用变量的方法，这种用法是go语言内置的吗？</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/27/e5a74107.jpg" width="30px"><span>Da Vinci</span> 👍（1） 💬（1）<div>整个课程下来，感觉自己还是收获不少的，以前很多比较模糊的东西，学习完课程后很明了了，被白老师圈粉了。</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/d5/ca522e83.jpg" width="30px"><span>爱吃胡萝卜</span> 👍（0） 💬（1）<div>老师我想问下这里具体的错误处理是怎么做的，
比如客户端和服务端 遇到读写超时的具体应该怎么处理，

像文中提到 的客户端已经关闭socket， 而服务端还在写数据的时候，这个时候 服务端收到socket关闭的信息了 是不是首先应该停止写入，再关掉socket。
因为继续写入已经没有意义，如果写缓冲区满了 还会造成写超时。

关于读写超时： 我的理解是服务端 
如果遇到 读超时 这个时候应该认为客户端不活跃了，应该关闭socket
写超时的话。 有可能是网络不好，也有可能客户端下线了 ，是不是也是关闭socket。


客户端的处理是不是要复杂一些？
客户端遇到读超时，一般是因为发起了请求，而请求没有得到回应，这个时候是不是应该关闭socket，然后重新建立socket连接，与此同时还要做一些额外的状态恢复操作。
写超时是不是同样如此，
烦请老师解惑， 有关于这方面好的文章和书籍都可以推荐给我细看，谢谢</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（8） 💬（4）<div>终于明白用 Go 替换 Java 做 IO 密集型压测为什么没有压到性的优势。因为多个 Goroutine 从 conn 中读写时都有锁保护，没有逃出枷锁。
</div>2022-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>go最搞笑的地方，非要把fd藏起来，每次要拿他都贼麻烦</div>2022-10-09</li><br/>
</ul>