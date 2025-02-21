你好，我是蒋德钧。

今天，我们来探讨一个很多人都很关心的问题：“为什么单线程的Redis能那么快？”

首先，我要和你厘清一个事实，我们通常说，Redis是单线程，主要是指**Redis的网络IO和键值对读写是由一个线程来完成的，这也是Redis对外提供键值存储服务的主要流程**。但Redis的其他功能，比如持久化、异步删除、集群数据同步等，其实是由额外的线程执行的。

所以，严格来说，Redis并不是单线程，但是我们一般把Redis称为单线程高性能，这样显得“酷”些。接下来，我也会把Redis称为单线程模式。而且，这也会促使你紧接着提问：“为什么用单线程？为什么单线程能这么快？”

要弄明白这个问题，我们就要深入地学习下Redis的单线程设计机制以及多路复用机制。之后你在调优Redis性能时，也能更有针对性地避免会导致Redis单线程阻塞的操作，例如执行复杂度高的命令。

好了，话不多说，接下来，我们就先来学习下Redis采用单线程的原因。

## Redis为什么用单线程？

要更好地理解Redis为什么用单线程，我们就要先了解多线程的开销。

### 多线程的开销

日常写程序时，我们经常会听到一种说法：“使用多线程，可以增加系统吞吐率，或是可以增加系统扩展性。”的确，对于一个多线程的系统来说，在有合理的资源分配的情况下，可以增加系统中处理请求操作的资源实体，进而提升系统能够同时处理的请求数，即吞吐率。下面的左图是我们采用多线程时所期待的结果。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/86/a380cbad.jpg" width="30px"><span>柳磊</span> 👍（63） 💬（5）<div>作者您好，引用文中一段话“我们知道了，Redis 单线程是指它对网络 IO 和数据读写的操作采用了一个线程”，我有个疑问，redis为什么要网络IO与业务处理（读写）用一个线程？而不用Netty中常见的Reactor线程模型，把io线程（netty中的boss线程）与业务处理线程（netty中的work线程）分开，业务处理线程只开启一个线程，也不会有共享资源竞争的问题。</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/5e/9d2953a3.jpg" width="30px"><span>zhou</span> 👍（18） 💬（2）<div>老师分析的 redis io 模型中，redis 线程是循环处理每个事件的。如果其中一个事件比较耗时，会影响后面事件的及时处理。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/8a/82587883.jpg" width="30px"><span>竹真</span> 👍（17） 💬（3）<div>作者您好，读完您的文章还有点疑惑，Redis读取客户端数据和读内存是一个线程？</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/fd/94/8704d2b0.jpg" width="30px"><span>spoofer</span> 👍（12） 💬（1）<div>还有的性能瓶颈：即使io复用已经很牛叉了，但是redis线程始终是用户线程，要读取或者写入网络数据，还是要进行read和write的系统调用的，而系统调用是一个耗时的操作。so~~ 为什么6.0要引入多线程？一个原因就是要找些小弟来处理这个耗时的数据读写啊~~~</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/f8/6b311ad9.jpg" width="30px"><span>BrightLoong</span> 👍（7） 💬（8）<div>Redis 单线程是指它对网络 IO 和数据读写的操作采用了一个线程
对这句话不是很理解，总觉得是处理网络IO是一个线程，然后把事件放入队列；读写操作又是一个线程，从队列中处理请求。求解答</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/92/6361802a.jpg" width="30px"><span>滴流乱转小胖儿</span> 👍（4） 💬（1）<div>老师你好，单线程的处理事件队列中的事件，这样还是会遇到性能瓶颈吧？  </div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/14/653b2a89.jpg" width="30px"><span>华仔</span> 👍（2） 💬（2）<div>Redis在Linux上应该是单进程，不能说是单线程，main函数完成初始化后就进入事件循环处理，快照的时候也是直接fork一个新进程，而不是pthread_create一个新线程，请老师确认一下</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/8f/5b224f54.jpg" width="30px"><span>LovePeace</span> 👍（1） 💬（1）<div>请问文章提到的套接字是指socket吗？</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/06/df/60126ff3.jpg" width="30px"><span>0bug</span> 👍（1） 💬（2）<div>操作大key的时候，IO是性能瓶颈</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（1389） 💬（83）<div>Redis单线程处理IO请求性能瓶颈主要包括2个方面：

1、任意一个请求在server中一旦发生耗时，都会影响整个server的性能，也就是说后面的请求都要等前面这个耗时请求处理完成，自己才能被处理到。耗时的操作包括以下几种：
	a、操作bigkey：写入一个bigkey在分配内存时需要消耗更多的时间，同样，删除bigkey释放内存同样会产生耗时；
	b、使用复杂度过高的命令：例如SORT&#47;SUNION&#47;ZUNIONSTORE，或者O(N)命令，但是N很大，例如lrange key 0 -1一次查询全量数据；
	c、大量key集中过期：Redis的过期机制也是在主线程中执行的，大量key集中过期会导致处理一个请求时，耗时都在删除过期key，耗时变长；
	d、淘汰策略：淘汰策略也是在主线程执行的，当内存超过Redis内存上限后，每次写入都需要淘汰一些key，也会造成耗时变长；
	e、AOF刷盘开启always机制：每次写入都需要把这个操作刷到磁盘，写磁盘的速度远比写内存慢，会拖慢Redis的性能；
	f、主从全量同步生成RDB：虽然采用fork子进程生成数据快照，但fork这一瞬间也是会阻塞整个线程的，实例越大，阻塞时间越久；
2、并发量非常大时，单线程读写客户端IO数据存在性能瓶颈，虽然采用IO多路复用机制，但是读写客户端数据依旧是同步IO，只能单线程依次读取客户端的数据，无法利用到CPU多核。

针对问题1，一方面需要业务人员去规避，一方面Redis在4.0推出了lazy-free机制，把bigkey释放内存的耗时操作放在了异步线程中执行，降低对主线程的影响。

针对问题2，Redis在6.0推出了多线程，可以在高并发场景下利用CPU多核多线程读写客户端数据，进一步提升server性能，当然，只是针对客户端的读写是并行的，每个命令的真正操作依旧是单线程的。</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（138） 💬（20）<div>1.big key的操作。
2.潜在的大量数据操作，比如 key *或者get all之类的操作，所以才引入了scan的相关操作。
3.特殊的场景，大量的客户端接入。


简单介绍下select poll epoll的区别，select和poll本质上没啥区别，就是文件描述符数量的限制，select根据不同的系统，文件描述符限制为1024或者2048，poll没有数量限制。他两都是把文件描述符集合保存在用户态，每次把集合传入内核态，内核态返回ready的文件描述符。
epoll是通过epoll_create和epoll_ctl和epoll_await三个系统调用完成的，每当接入一个文件描述符，通过ctl添加到内核维护的红黑树中，通过事件机制，当数据ready后，从红黑树移动到链表，通过await获取链表中准备好数据的fd，程序去处理。</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（107） 💬（6）<div>Redis 的单线程指 Redis 的网络 IO 和键值对读写由一个线程来完成的（这是 Redis 对外提供键值对存储服务的主要流程）
Redis 的持久化、异步删除、集群数据同步等功能是由其他线程而不是主线程来执行的，所以严格来说，Redis 并不是单线程

为什么用单线程？
多线程会有共享资源的并发访问控制问题，为了避免这些问题，Redis 采用了单线程的模式，而且采用单线程对于 Redis 的内部实现的复杂度大大降低

为什么单线程就挺快？
1.Redis 大部分操作是在内存上完成，并且采用了高效的数据结构如哈希表和跳表
2.Redis 采用多路复用，能保证在网络 IO 中可以并发处理大量的客户端请求，实现高吞吐率

Redis 6.0 版本为什么又引入了多线程？
Redis 的瓶颈不在 CPU ，而在内存和网络，内存不够可以增加内存或通过数据结构等进行优化
但 Redis 的网络 IO 的读写占用了发部分 CPU 的时间，如果可以把网络处理改成多线程的方式，性能会有很大提升
所以总结下 Redis 6.0 版本引入多线程有两个原因
1.充分利用服务器的多核资源
2.多线程分摊 Redis 同步 IO 读写负荷

执行命令还是由单线程顺序执行，只是处理网络数据读写采用了多线程，而且 IO 线程要么同时读 Socket ，要么同时写 Socket ，不会同时读写</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/c6/0167415c.jpg" width="30px"><span>林肯</span> 👍（74） 💬（13）<div>反复看了很多遍终于明白了：关键点在于accpet和recv时可能会阻塞线程，使用IO多路复用技术可以让线程先处理其他事情，等需要的资源到位后epoll会调用回调函数通知线程，然后线程再去处理存&#47;取数据；这样一个redis服务端线程就可以同时处理多个客户端请求了。
redis之所以适合用多路复用技术有一个很重要的原因时它是在内存中处理数据速度极快，这时io成了瓶颈。为什么Mysql不用多路复用技术呢？因为Mysql的主要性能瓶颈在于数据的存&#47;取，优化方向不一样。</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（65） 💬（1）<div>1，作者讲了什么？
	redis实现单线程实现高性能IO的设计机制
2，作者是怎么把这事给讲明白的？
	作者首先从简单的网络通信socket讲起，引出了非阻塞socket，由此谈到了著名的I&#47;O多路复用，Linux内核的select&#47;epoll机制
3，为了讲明白，作者讲了哪些要点?有哪些亮点？
	（1）首先声明“redis单线程”这个概念的具体含义
	（2）引入具体业务场景：redis的数据读取，事件处理机制模型
	（3）解析单线程相对多线程带来的优势，已及多线程所特有的问题
	（4）基于redis单线程的，设计机制，引出了网络socket的问题</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（42） 💬（0）<div>虽然单线程很快，没有锁的单线程更快借助CPU的多级缓存可以把性能发挥到最大。但是随着访问量的增加，以及数据量的增加，IO的写入写出会成为性能瓶颈。10个socket的IO吞吐处理肯定比1000个socket吞吐处理的快，为了解决这个问题，Redis6引入了IO多线程的方式以及client缓冲区，在实际指令处理还是单线程模式。在IO上变成的了【主线程】带着众多【IO线程】进行IO，IO线程听从主线程的指挥是写入还是写出。Read的时候IO线程会和主线程一起读取并且解析命令（RESP协议）存入缓冲区，写的时候会从缓冲区写出到Socket。IO线程听从主线程的指挥，在同一个时间点上主线程和IO线程会一起写出或者读取，并且主线程会等待IO线程的结束。但是这种模式的多线程会面临一给NUMA陷阱的问题，在最近的Redis版本中加强了IO线程和CPU的亲和性解决了这个问题。（不过目前官方在默认情况下并不推荐使用多线程IO模式，需要手动开启）</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（20） 💬（1）<div>Redis的网络模式是单reactor模式。non-blocking io + epoll</div>2020-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiao0orF0gDeDCwnAEicrCgY6NickyOJ8ialw0GiavInZL0DMctRYlZicj4bLMNTtBmFtH4eIiaVfr8DPVw/132" width="30px"><span>Geek_84971a</span> 👍（18） 💬（4）<div>老师在讲解redis网络IO模型的时候，如果可以结合epoll的多路复用机制，顺便提一下redis源码里面的实现，相信可以让人理解的更加深入一些；</div>2020-08-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzvaL724GwtzZ5mcldUnlicicSlI8BXL9icRZbUOB10qjRMlmog7UTvwxSBHXagnPGGR1BYdjWcGGSg/132" width="30px"><span>wwj</span> 👍（16） 💬（19）<div>这篇的io模型和我了解到的不一样，既然是select&#47;epoll的模式，那应该就是Reactor设计模式，哪来的回调，回调肯定设计到多个线程，单线程模式在用户层不可能有回调的，如果是在内核层的话，是有aio模式，但select&#47;epoll明显不是aio的实现</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/66/59e0647a.jpg" width="30px"><span>万历十五年</span> 👍（14） 💬（5）<div>个人理解，IO多路复用简单说是IO阻塞或非阻塞的都不准确。严格来说应用程序从网络读取数据到数据可用，分两个阶段：第一阶段读网络数据到内核，第二阶段读内核数据到用户态。IO多路复用解决了第一阶段阻塞问题，而第二阶段的读取阻塞的串行读。为了进一步提高REDIS的吞吐量，REDIS6.0使用多线程利用多CPU的优势解决第二阶段的阻塞。说的不对的地方，请斧正。</div>2020-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（13） 💬（5）<div>re: 
原文一：Redis 在对事件队列中的事件进行处理时，会调用相应的处理函数，这就实现了基于事件的回调。

原文二：此时，内核就会回调 Redis 相应的 accept 和 get 函数进行处理。


是redis 调用accept 和 get函数，还是内核吖？谢谢老师。</div>2020-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（11） 💬（2）<div>Redis的事件处理队列只有一个吗？不同的事件的优先级都是一样的吗？只是简单的按照对接的先进先出的特性依次进行处理的吗？</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/72/1f/9ddfeff7.jpg" width="30px"><span>文进</span> 👍（8） 💬（4）<div>IO多路的单线程模型：
1，redis启动时，向epoll注册还未使用的FD的可连接事件。
2，连接事件产生时，epoll机制自动将其放入自己的可连接事件队列中。
3，redis线程调用epoll的wait，获取所有事件，拷贝存入自己用户线程的内存队列中。
4，遍历这些内存队列，通过事件分派器，交由对应事件处理器处理。如是可连接事件则交由对应的连接应答事件处理器处理。可读事件交给命令请求处理器，可写事件交给命令回复处理器处理。
5，对应处理器执行相应逻辑。执行完成时，再次向epoll注册对应事件，比如连接事件的那个FD，接下来要注册可读事件，并重新注册可连接事件。命令请求处理器执行完后，要将FD注册可写事件。命令回复处理器执行完后，需要将FD取消注册可写事件。
6，产生了新的注册（如可读事件）之后，又回到了2，等待新的事件产生。</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/94/0247f945.jpg" width="30px"><span>咸鱼</span> 👍（7） 💬（0）<div>这章让我对IO多路复用的理解又深了些</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/5f/3400d01b.jpg" width="30px"><span>Y、先生</span> 👍（5） 💬（1）<div>现在，我们知道了，Redis 单线程是指它对网络 IO 和数据读写的操作采用了一个线程。 
这里的网络IO是指redis处理事件队列的阶段么，数据读写对应的是回调函数，是这样理解吗。 这部分很困惑，希望老师帮忙确认下</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/f9/75d08ccf.jpg" width="30px"><span>Mr.蜜</span> 👍（5） 💬（8）<div>忘记提另一个问题，既然老师说道select和epoll，为什么不提一下poll呢？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（5） 💬（0）<div>单线程同步非阻塞读取网络IO的时候会有性能瓶颈，如果读取的内容过多的时候</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/5c/e09eac13.jpg" width="30px"><span>刘強</span> 👍（4） 💬（0）<div>epoll并没有什么回调，你这到底讲的是epoll的回调，还是redis的事件循环，linux内核回调redis函数？不懂不要瞎讲啊，浪费别人的时间</div>2022-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/87/37/b071398c.jpg" width="30px"><span>等风来🎧</span> 👍（4） 💬（1）<div>老师，有很多同学提出来相同的疑问，就是您在文中提到的，
原文一：Redis 在对事件队列中的事件进行处理时，会调用相应的处理函数，这就实现了基于事件的回调。

原文二：当 Linux 内核监听到有连接请求或读数据请求时，就会触发 Accept 事件和 Read 事件，此时，内核就会回调 Redis 相应的 accept 和 get 函数进行处理。


是redis 回调accept 和 get函数还是内核回调accept 和 get函数啊？希望老师看到后，有时间解答一下哈</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（3） 💬（0）<div>弄了个随堂测试，希望能帮到大家
【随堂测试：Redis 核心技术与实战 】

# 03 | 高性能IO模型：为什么单线程Redis能那么快？

## 【灵魂问题】该讲对应知识全景图的哪一块？

## 3.1 Redis 是单线程，主要是指？

## 3.2 Redis 为什么用单线程？

## 3.3 单线程 Redis 为什么那么快（两方面）？

### 3.3.1 基本 IO 模型与阻塞点 是什么？

### 3.3.2 非阻塞模式的关键？

### 3.3.3 基于多路复用的高性能 I&#47;O 模型是什么？

## 3.4 每课一问: 在“Redis 基本 IO 模型”图中，你觉得还有哪些潜在的性能瓶颈吗？</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/bd/7fef12c8.jpg" width="30px"><span>张新亮</span> 👍（3） 💬（0）<div>为什么不把io线程和工作线程分开实现？
1，Io线程负责连接和数据读取，读到数据后加入事件队列
2，然后工作线程处理事件，处理后再把结果写到队列中
3，由io线程负责写出
这样不是充分利用多核优势吗？既没有锁，也没有频繁的上下文切换，除非服务器都用单核的CPU。</div>2021-03-18</li><br/>
</ul>