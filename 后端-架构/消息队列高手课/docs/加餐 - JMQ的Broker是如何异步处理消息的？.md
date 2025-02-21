你好，我是李玥。

我们的课程更新到进阶篇之后，通过评论区的留言，我看到有一些同学不太理解，为什么在进阶篇中要讲这些“看起来和消息队列关系不大的”内容呢？

在这里，我跟你分享一下这门课程的设计思路。我们这门课程的名称是“消息队列高手课”，我希望你在学习完这门课程之后，不仅仅只是成为一个使用消息队列的高手，而是**设计和实现**消息队列的高手。所以我们在设计课程的时候，分了基础篇、进阶篇和案例篇三部分。

基础篇中我们给大家讲解消息队列的原理和一些使用方法，重点是让大家学会使用消息队列。

你在进阶篇中，我们课程设计的重点是讲解实现消息队列必备的技术知识，通过分析源码讲解消息队列的实现原理。**希望你通过进阶篇的学习能够掌握到设计、实现消息队列所必备的知识和技术，这些知识和技术也是设计所有高性能、高可靠的分布式系统都需要具备的。**

进阶篇的上半部分，我们每一节课一个专题，来讲解设计实现一个高性能消息队列，必备的技术和知识。这里面每节课中讲解的技术点，不仅可以用来设计消息队列，同学们在设计日常的应用系统中也一定会用得到。

前几天我在极客时间直播的时候也跟大家透露过，由我所在的京东基础架构团队开发的消息队列JMQ，它的综合性能要显著优于目前公认性能非常好的Kafka。虽然在开发JMQ的过程中有很多的创新，但是对于性能的优化这块，并没有什么全新的划时代的新技术，JMQ之所以能做到这样的极致性能，靠的就是合理地设计和正确地使用已有的这些通用的底层技术和优化技巧。我把这些技术和知识点加以提炼和总结，放在进阶篇的上半部分中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/95/1c/3cefe42b.jpg" width="30px"><span>包明</span> 👍（70） 💬（4）<div>Requests Queue 内存级的 怎么做到不丢请求？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/1c/59a4e803.jpg" width="30px"><span>青舟</span> 👍（29） 💬（3）<div>https:&#47;&#47;github.com&#47;qingzhou413&#47;geektime-mq-rpc.git

使用netty作为网络库，server和client的io线程数都是1，笔记本4核标压2.3G时间2.3秒。</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/53/ade0afb0.jpg" width="30px"><span>ub8</span> 👍（15） 💬（4）<div>老师，文中提到的 “我们把回复响应这个需要等待资源的操作，也异步放到其他的线程中去执行。”；这个是怎么实现的呢？ ResponseThread ,和 RequestThread 是如何对应上的？</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（9） 💬（1）<div>老师有个疑问，帮忙解答下哦，在上面的那个流程图中，WriteThread是单线程从请求队列中获取到消息然后把消息放到journal Cache，开启ReplicationThread、FlushThread进行处理，能否把WriteThread做成分配器了，mq只要保证topic下的队列有序就可以，同一个队列的消息由WriteThread分配给同一个线程进行处理，线程池的形式，线程池中的每个工作线程内部都有个集合保存消息，如果前面没有同一个队列的消息，分配给最空闲的线程进行执行，那这样的话，WriteThread只要分配消息，比如可以对发送过来的消息中要保存的队列属性值进行hash，然后根据hash值判断线程池中的所有线程的消息集合是否有相同队列的消息，有的话分配给同一个线程执行，没有的话最空闲的线程执行，mysql的binlog同步也是有几种这种策略，并发的同步sql，刚开始是基于库，同一个库的sql分配到一个线程执行同步，不同库进行并发，后来是基于redo log的组提交形式，能组提交的sql可以并发的同步，再后来是WRITESET，根据库名、表名、索引（主键和唯一索引）计算hash进行分发策略。</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/82/b5808a60.jpg" width="30px"><span>李冲</span> 👍（8） 💬（2）<div>借用老师的的go源码经过读，写，去掉锁3次演进，分别在金山云ECS（2核4G）上跑到3.1&#47;2.4&#47;1.4秒的样子。
最终的文件：https:&#47;&#47;github.com&#47;lichongsw&#47;algorithm&#47;blob&#47;master&#47;duplex_communication_optimization_3_no_write_lock.go</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/33/abf321b7.jpg" width="30px"><span>吾皇万岁万岁万万岁</span> 👍（8） 💬（6）<div>请问老师，JMQ在follower节点响应后，就给生产者发送确认消息，此时如果leader节点故障，数据还在JournalCache里面，拿是不是可以认为这部分数据丢失？</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/f2/1f77b0bd.jpg" width="30px"><span>李心宇🦉</span> 👍（5） 💬（3）<div>老师好，我对JMQ的broker接收生产者请求并写入消息的流程有个疑问。
在处理完数据落盘和多节点数据复制之后，要给生产者回复响应了，这时候broker如何能找到生产者呢？我理解是第一步生产者发送请求建立的TCP连接句柄没有释放，最后再通过这个连接句柄来write响应。这样的话，还是每个连接在得到响应之前不能释放需要占用一个线程啊。请问是怎么做到在第一步接收响应阶段只需要很少的线程的？是不是利用异步非阻塞，在线程里设置大量的协程来处理请求？</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/58/3d/4ba98f04.jpg" width="30px"><span>Martin</span> 👍（5） 💬（2）<div>https:&#47;&#47;github.com&#47;MartinDai&#47;mq-in-action&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;doodl6&#47;mq&#47;MeetInRpc.java

基于netty4实现的，Macbook pro 2015款 13寸 测试差不多4.2秒左右，老师帮忙看看哪里还可以有优化空间吗</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/26/b8c53cee.jpg" width="30px"><span>南辕北辙</span> 👍（4） 💬（4）<div>把老师的代码看了n遍，再用java的原生nio实现了一遍，理解了老师的用心良苦。前二章序列化与网络协议那块的知识，对应代码对于struct的构造，四字节的总长度，四字节的序号，以及变长内容，然后二个大爷在接受到数据以后也是根据这个协议进行取数据。也就对应了序列化以及协议都是自定义的！！二个大爷都懂该怎么从二进制的数据中，提取出对话。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/0f/fa840c1b.jpg" width="30px"><span>刘天鹏</span> 👍（3） 💬（2）<div>老师的writeTo函数没必要加锁吧，用一个局部缓冲把lengthByte serialBytes payloadBytes拼装好再一起发送应该就可以了
我把我的大爷改成双工的，多线程的，可以打包发送的，现在大爷还只有一张嘴一个耳朵（一个socket连接）
可能是没有逻辑处理的负担，多线程没啥改变
打包发送有一定的改进，1次3条数据 14s
现在100万次胡同碰面，8.66s(公司的i7)

https:&#47;&#47;gist.github.com&#47;liutianpeng&#47;d9330f85d47525a8e32dcd24f5738e55</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d7/e3/e6cf6352.jpg" width="30px"><span>nfx</span> 👍（2） 💬（3）<div>有个疑问,  request queue, journal cache都是生产者, 消费者模型的队列,  里面应该会有锁吧?  只是这种队列锁需要的资源很少. 
 不知道怎么理解对不对</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/16/6347bbc0.jpg" width="30px"><span>顶新</span> 👍（2） 💬（1）<div>FlushThread 和 ReplicationThread线程对内存的链表 Pending Callbacks 中数据的更新，然后ResponseThread扫描链表Pending Callbacks，批量取出符合 QOS 规则的响应及超时的响应，然后并发返回给客户端。这块也存在对 Pending Callbacks 存在互斥锁吧？不知道理解的对不对，还请老师答疑 :)</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（2） 💬（1）<div>如果要保证前一句话要对方确认回复后再发送下一句话 就不能用这种方式了吧？这样吞吐量就会很低了</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/3d/5d51fda4.jpg" width="30px"><span>TWT_Marq</span> 👍（2） 💬（1）<div>JMQ中，接受请求的iothreads将请求丢给request queue，WriteThread从queue中取出来开始干活。这个queue是concurrentBlockingQueue吗？</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（2） 💬（10）<div>我用java实现了一版，老师帮忙看下哦，评论只能发2000字，其余在评论区补上
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

&#47;**
 * @author linqw
 *&#47;
public class SocketExample {

    private static final Logger LOGGER = LoggerFactory.getLogger(SocketExample.class);

    private static final ReentrantLock LI_WRITE_REENTRANT_LOCK = new ReentrantLock();

    private static final ReentrantLock ZHANG_WRITE_REENTRANT_LOCK = new ReentrantLock();

    private static final int NCPU = Runtime.getRuntime().availableProcessors();

    private final ThreadPoolExecutor serverThreadPoolExecutor = new ThreadPoolExecutor(NCPU, NCPU, 5, TimeUnit.SECONDS, new ArrayBlockingQueue&lt;Runnable&gt;(200000), new ThreadFactoryImpl(&quot;server-&quot;), new ThreadPoolExecutor.CallerRunsPolicy());

    private final ThreadPoolExecutor clientThreadPoolExecutor = new ThreadPoolExecutor(NCPU, NCPU, 5, TimeUnit.SECONDS, new ArrayBlockingQueue&lt;Runnable&gt;(200000), new ThreadFactoryImpl(&quot;client-&quot;), new ThreadPoolExecutor.CallerRunsPolicy());

    private volatile boolean started = false;

    &#47;**
     * 俩大爷已经遇见了多少次
     *&#47;
    private volatile AtomicInteger count = new AtomicInteger(0);

    &#47;**
     * 总共需要遇见多少次
     *&#47;
    private static final int TOTAL = 1;

    private static final String Z0 = &quot; 吃了没，您吶?&quot;;

    private static final String Z3 = &quot; 嗨！吃饱了溜溜弯儿。&quot;;
    private static final String Z5 = &quot; 回头去给老太太请安！&quot;;
    private static final String L1 = &quot; 刚吃。&quot;;
    private static final String L2 = &quot; 您这，嘛去？&quot;;
    private static final String L4 = &quot; 有空家里坐坐啊。&quot;;</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/12/d4d54dd2.jpg" width="30px"><span>豆沙包</span> 👍（2） 💬（1）<div>老师，我在运行你的老大爷代码的时候发现了一个问题，经常报读长度故障。我调试了一下，应该是因为张大爷阻塞在readfrom的时候，李大爷count++了。然后count大于total，client释放了tcp。这导致readfrom无法读出准确数据。我在返回读数据故障前判断了一下count和total的关系，如果count大于等于total正常返回，就没有再报过异常了。您看我分析的是否有问题呢</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ff/09a058f3.jpg" width="30px"><span>solar</span> 👍（2） 💬（2）<div>一些分配内存地方也可以优化，可以预先分配一块复用，减少向内核申请分配内存次数.</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（2） 💬（1）<div>想简单请教一下JMQ
1. writeThread与ReplicationThread&#47;FlushThread之间的同步也要基于无锁队列是吧？
2. JournalCache就是简单的用户态内存，还是基于mmap？（从描述上看感觉就是用户态内存）。
3. 老师能不能透露一下，在研发JMQ的过程中，解决了哪个瓶颈之后，吞吐量一下子提了很多呢？</div>2019-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（2）<div>老师好，请问一下WriteThread中将消息序列化并维护起止位置offset，这个offset是否就是头部信息中保存消息长度呢？比如04abcd08abcdefgh，通过04就可以知道abcd消息的起止位置，下一个读到的08则代表下一条消息的起止位置？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>老师好， ReponseThreads 这组线程，怎么实现异步并行的没太理解，她不是需要等待复制响应或者落盘后才发消息给客户端嘛？</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/e7/ed0a0131.jpg" width="30px"><span>大白先生</span> 👍（1） 💬（1）<div>老师，我基于之前半包粘包的问题还想问一个问题。之前您说如果按照咱们课上讲的自定义消息格式，不会出现这种情况。我想问，如果出现概念上的半包情况，也就是说，soket首发缓存去8k，我这边写入一条10k的消息，那么接收方按照咱们定义的格式解析，那不就是解析到了前8k的数据，那么按照数据钱的包长度解析的时候，数据的长度就不够，这样不会引起数据错误么</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/e7/ed0a0131.jpg" width="30px"><span>大白先生</span> 👍（1） 💬（2）<div>老师，我在学习java实现tcp发送数据时，我有看到有讲解tcp粘包或者是半包的情况，我看的文章说是可能是因为一次写入的数据大于soket发送缓冲区。会导致接收方接受数据有问题。但是我写例子的时候没有发现这个问题，请问，怎么能弄出这两种情况？假如不用netty时，利用soket能如何处理这种问题。</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL6ibvATzI5FKR6r71GU3CjdlPkZYYSBYBtNibIGENFZDnqajW7LOPKZXUPWSsjt8OiaxTZ0neT8LwQQ/132" width="30px"><span>Geek_498c16</span> 👍（0） 💬（2）<div>Requests Queue 不会存在 WriteThread处理慢导致队列塞满的情况吗? 看了下流程Requests Queue 的取是比放慢的.</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/df/4949b250.jpg" width="30px"><span>Six Days</span> 👍（0） 💬（1）<div>老师，希望能给出一份java 版本的参考代码以供学习，谢谢你了</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/a8/d103904b.jpg" width="30px"><span>mark</span> 👍（0） 💬（2）<div>做了一点优化，到了 3s

https:&#47;&#47;gist.github.com&#47;vipwzw&#47;382f68995e26a2696e4da8cc5039c595</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/4b/97926cba.jpg" width="30px"><span>Luciano李鑫</span> 👍（0） 💬（2）<div>读长度故障 read: connection reset by peer ,请问下这是为什么，macOS系统</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（0） 💬（1）<div>老师，你用go语言实现的代码，我把fmt.Println放开之后跑了一下，发现有消息丢失的现象，&quot; 嗨！吃饱了溜溜弯儿。&quot;（这一句总是少一次），&quot; 刚吃。&quot;（这一句时有时没有），我对go了解不多，没看出来咋回事</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/29/1be3dd40.jpg" width="30px"><span>ykkk88</span> 👍（0） 💬（2）<div>老师  重新看了下上面这个例子我的理解是异步方式发送消息吧，发送完不会等到消息回来再发第二个？</div>2019-08-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vK7WwQG23CI29w0iamcgetTicMdQ8NsJsQWSXIia3aSUbVE6dqfTiaVtqTdibJu31f7k2BkOSkQianxOUaqojEYP6ic3w/132" width="30px"><span>coffee</span> 👍（0） 💬（1）<div>老师，已将单工通讯改成了双工通讯，时间上确定有提高。10万次大概在3364-4873毫秒这个区间。
https:&#47;&#47;github.com&#47;swgithub1006&#47;mqlearning
协议上的确还有优化的空间，比如借鉴下protobuf的设计思想。</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8b/83/d2afc837.jpg" width="30px"><span>路人</span> 👍（0） 💬（1）<div>老师的课讲的很好，基本上讲的都是一些消息相关的设计理念，站的角度也比较高，非常实用。请问下老师文中的图用的什么工具画的</div>2019-08-24</li><br/>
</ul>