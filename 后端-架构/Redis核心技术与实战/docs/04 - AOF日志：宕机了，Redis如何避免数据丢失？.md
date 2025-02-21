你好，我是蒋德钧。

如果有人问你：“你会把Redis用在什么业务场景下？”我想你大概率会说：“我会把它当作缓存使用，因为它把后端数据库中的数据存储在内存中，然后直接从内存中读取数据，响应速度会非常快。”没错，这确实是Redis的一个普遍使用场景，但是，这里也有一个绝对不能忽略的问题：**一旦服务器宕机，内存中的数据将全部丢失。**

我们很容易想到的一个解决方案是，从后端数据库恢复这些数据，但这种方式存在两个问题：一是，需要频繁访问数据库，会给数据库带来巨大的压力；二是，这些数据是从慢速数据库中读取出来的，性能肯定比不上从Redis中读取，导致使用这些数据的应用程序响应变慢。所以，对Redis来说，实现数据的持久化，避免从后端数据库中进行恢复，是至关重要的。

目前，Redis的持久化主要有两大机制，即AOF（Append Only File）日志和RDB快照。在接下来的两节课里，我们就分别学习一下吧。这节课，我们先重点学习下AOF日志。

## AOF日志是如何实现的？

说到日志，我们比较熟悉的是数据库的写前日志（Write Ahead Log, WAL），也就是说，在实际写数据前，先把修改的数据记到日志文件中，以便故障时进行恢复。不过，AOF日志正好相反，它是写后日志，“写后”的意思是Redis是先执行命令，把数据写入内存，然后才记录日志，如下图所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/8a/288f9f94.jpg" width="30px"><span>Kaito</span> 👍（1354） 💬（156）<div>问题1，Redis采用fork子进程重写AOF文件时，潜在的阻塞风险包括：fork子进程 和 AOF重写过程中父进程产生写入的场景，下面依次介绍。

	a、fork子进程，fork这个瞬间一定是会阻塞主线程的（注意，fork时并不会一次性拷贝所有内存数据给子进程，老师文章写的是拷贝所有内存数据给子进程，我个人认为是有歧义的），fork采用操作系统提供的写实复制(Copy On Write)机制，就是为了避免一次性拷贝大量内存数据给子进程造成的长时间阻塞问题，但fork子进程需要拷贝进程必要的数据结构，其中有一项就是拷贝内存页表（虚拟内存和物理内存的映射索引表），这个拷贝过程会消耗大量CPU资源，拷贝完成之前整个进程是会阻塞的，阻塞时间取决于整个实例的内存大小，实例越大，内存页表越大，fork阻塞时间越久。拷贝内存页表完成后，子进程与父进程指向相同的内存地址空间，也就是说此时虽然产生了子进程，但是并没有申请与父进程相同的内存大小。那什么时候父子进程才会真正内存分离呢？“写实复制”顾名思义，就是在写发生时，才真正拷贝内存真正的数据，这个过程中，父进程也可能会产生阻塞的风险，就是下面介绍的场景。

	b、fork出的子进程指向与父进程相同的内存地址空间，此时子进程就可以执行AOF重写，把内存中的所有数据写入到AOF文件中。但是此时父进程依旧是会有流量写入的，如果父进程操作的是一个已经存在的key，那么这个时候父进程就会真正拷贝这个key对应的内存数据，申请新的内存空间，这样逐渐地，父子进程内存数据开始分离，父子进程逐渐拥有各自独立的内存空间。因为内存分配是以页为单位进行分配的，默认4k，如果父进程此时操作的是一个bigkey，重新申请大块内存耗时会变长，可能会产阻塞风险。另外，如果操作系统开启了内存大页机制(Huge Page，页面大小2M)，那么父进程申请内存时阻塞的概率将会大大提高，所以在Redis机器上需要关闭Huge Page机制。Redis每次fork生成RDB或AOF重写完成后，都可以在Redis log中看到父进程重新申请了多大的内存空间。

问题2，AOF重写不复用AOF本身的日志，一个原因是父子进程写同一个文件必然会产生竞争问题，控制竞争就意味着会影响父进程的性能。二是如果AOF重写过程中失败了，那么原本的AOF文件相当于被污染了，无法做恢复使用。所以Redis AOF重写一个新文件，重写失败的话，直接删除这个文件就好了，不会对原先的AOF文件产生影响。等重写完成之后，直接替换旧文件即可。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（106） 💬（3）<div>什么时候会触发AOF 重写呢？</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/0c/f39f847a.jpg" width="30px"><span>D</span> 👍（16） 💬（5）<div>AOF 是什么的缩写， 还是说就是这个名字？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（12） 💬（3）<div>图是不是画错了。为什么主线程和AOF重写缓冲连起来了呢？不是应该bgrewriteaof来写吗？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/eb/30864e40.jpg" width="30px"><span>漂泊者及其影子</span> 👍（9） 💬（1）<div>问个问题：redis同时开启RDB和AOF，redis重启基于哪个文件进行数据恢复</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/ce/bc/8177eef4.jpg" width="30px"><span>五角场撸个串</span> 👍（3） 💬（1）<div>一口气看了好多节课，感谢老师的用心准备。老师的课从问题出发，从表面到原理，循序渐进，通俗易懂。对比其他有些课程，要么浮于表面，要么晦涩难懂。希望老师能够再出更多课程，谢谢。</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（116） 💬（3）<div>1，作者讲了什么？
本章讲了Redis两种持久化机制之一：AOF机制原理
aof日志记录了redis所有增删改的操作，保存在磁盘上，当redis宕机，需要恢复内存中的数据时，可以通过读取aop日志恢复数据，从而避免因redis异常导致的数据丢失

2，作者是怎么把这事给讲明白的？
（1）作者先讲述redis宕机会导致内存数据丢失，需要有一种机制在redis重启后恢复数据。
（2）介绍了AOF通过记录每一个对redis数据进行增删改的操作日志，可以实现这种功能
（2）介绍了AOF的运行机制，数据保存机制，以及由此带来的优点和缺点
3，为了讲明白，作者讲了哪些要点，有哪些亮点？
（1）亮点：记录操作的时机分为：“写前日志和写后日志”，这个是我之前所不知道的
（2）要点1：AOF是写后日志，这样带来的好处是，记录的所有操作命令都是正确的，不需要额外的语法检查，确保redis重启时能够正确的读取回复数据
（3）要点2：AOF日志写入磁盘是比较影响性能的，为了平衡性能与数据安全，开发了三种机制：①：立即写入②：按秒写入③：系统写入
（4）要点3：AOF日志会变得巨大，所以Redis提供了日志重整的机制，通过读取内存中的数据重新产生一份数据写入日志
4，对于作者所讲，我有哪些发散性的思考？
作者说系统设计“取舍”二字非常重要，这是我之前未曾意识到的。作者讲了fork子进程机制，是Linux系统的一个能力，在刘超的课中讲过，这鼓舞了我继续学习的信心
5，将来有哪些场景，我可以应用上它？
目前还没有机会直接操作生产的redis配置，但现在要学习，争取将来可以直接操作
</div>2020-08-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLZ09TltdQiboR0kc1Kzp4X7ul2t01sWMG3cA7kT4X1Uvibes5bAEXx72veJ6uEMmUFq8FtEQvwl6FQ/132" width="30px"><span>GEEKBANG_3036760</span> 👍（77） 💬（1）<div>为了减小aof文件的体量，可以手动发送“bgrewriteaof”指令，通过子进程生成更小体积的aof，然后替换掉旧的、大体量的aof文件。

也可以配置自动触发

　　1）auto-aof-rewrite-percentage 100

　　2）auto-aof-rewrite-min-size 64mb

　　这两个配置项的意思是，在aof文件体量超过64mb，且比上次重写后的体量增加了100%时自动触发重写。我们可以修改这些参数达到自己的实际要求</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/30/4be78ce7.jpg" width="30px"><span>徐鹏</span> 👍（49） 💬（13）<div>有几个问题想请教一下：
1、文中多处提到bgrewriteaof 子进程，这个有点迷糊，主线程fork出来的bgrewriteaof是子线程还是子进程？
2、AOF重写会拷贝一份完整的内存数据，这个会导致内存占用直接翻倍吗？
3、如果一个key设置了过期时间，在利用AOF文件恢复数据时，key已经过期了这个是如何处理的呢？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（47） 💬（7）<div>AOF工作原理：
1、Redis 执行 fork() ，现在同时拥有父进程和子进程。
2、子进程开始将新 AOF 文件的内容写入到临时文件。
3、对于所有新执行的写入命令，父进程一边将它们累积到一个内存缓存中，一边将这些改动追加到现有 AOF 文件的末尾,这样样即使在重写的中途发生停机，现有的 AOF 文件也还是安全的。
4、当子进程完成重写工作时，它给父进程发送一个信号，父进程在接收到信号之后，将内存缓存中的所有数据追加到新 AOF 文件的末尾。
5、搞定！现在 Redis 原子地用新文件替换旧文件，之后所有命令都会直接追加到新 AOF 文件的末尾。

试着讨论下留言童鞋的几个问题

一、其中老师在文中提到：“因为主线程未阻塞，仍然可以处理新来的操作。此时，如果有写操作，第一处日志就是指正在使用的 AOF 日志，Redis 会把这个操作写到它的缓冲区。这样一来，即使宕机了，这个 AOF 日志的操作仍然是齐全的，可以用于恢复。”
这里面说到 “Redis 会把这个操作写到它的缓冲区，这样一来，即使宕机了，这个 AOF 日志的操作仍然是齐全的”，其实对于有些人有理解起来可能不是那么好理解，因为写入缓冲区为什么还不都是数据；

我的理解其实这个就是写入缓冲区，只不过是由appendfsync策略决定的，所以说的不丢失数据指的是不会因为子进程额外丢失数据。

二、AOF重新只是回拷贝引用(指针)，不会拷贝数据本身，因此量其实不大，那写入的时候怎么办呢，写时复制，即新开辟空间保存修改的值，因此需要额外的内存，但绝对不是redis现在占有的2倍。

三、AOF对于过期key不会特殊处理，因为Redis keys过期有两种方式：被动和主动方式。
	当一些客户端尝试访问它时，key会被发现并主动的过期。
	
	当然，这样是不够的，因为有些过期的keys，永远不会访问他们。 无论如何，这些keys应该过期，所以定时随机测试设置keys的过期时间。所有这些过期的keys将会从删除。
	具体就是Redis每秒10次做的事情：
		测试随机的20个keys进行相关过期检测。
		删除所有已经过期的keys。
		如果有多于25%的keys过期，重复步奏1.

至于课后问题，看了 @与路同飞 童鞋的答案，没有更好的答案，就不回答了</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（18） 💬（5）<div>问题一:在AOF重写期间，Redis运行的命令会被积累在缓冲区，待AOF重写结束后会进行回放，在高并发情况下缓冲区积累可能会很大，这样就会导致阻塞，Redis后来通过Linux管道技术让aof期间就能同时进行回放，这样aof重写结束后只需要回放少量剩余的数据即可

问题二：对于任何文件系统都是不推荐并发修改文件的，例如hadoop的租约机制，Redis也是这样，避免重写发生故障，导致文件格式错乱最后aof文件损坏无法使用，所以Redis的做法是同时写两份文件，最后通过修改文件名的方式，保证文件切换的原子性

这里需要纠正一下老师前面的口误，就是Redis是通过使用操作系统的fork()方式创建进程，不是线程，也由于这个原因，主进程和fork出来的子进程的资源是不共享的，所以也出现Redis使用pipe管道技术来同步主子进程的aof增量数据</div>2020-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WtHCCMoLJ2DvzqQwPYZyj2RlN7eibTLMHDMTSO4xIKjfKR1Eh9L98AMkkZY7FmegWyGLahRQJ5ibPzeeFtfpeSow/132" width="30px"><span>脱缰的野马__</span> 👍（13） 💬（4）<div>文章前面说到redo log日志记录的是修改后的数据，但是在丁奇老师的MySQL实战中讲解的是redo log记录是对数据的操作记录，修改后的数据是保存在内存的change buffer中的</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2d/0f/a00f2a32.jpg" width="30px"><span>Archer30</span> 👍（10） 💬（4）<div>问题1回答：如果子进程写入事件过长，并且这段事件，会导致AOF重写日志，积累过多，当新的AOF文件完成后，还是需要写入大量AOF重写日志里的内容，可能会导致阻塞。

问题2回答：我觉得评论区里的大部分回答 防止锁竞争 ，应该是把问题理解错了，父子两个进程本来就没有需要竞争的数据，老师所指的两个日志应该是“AOF缓冲区”和&quot;AOF重写缓冲区&quot;，而不是磁盘上的AOF文件，之所有另外有一个&quot;AOF重写缓冲区&quot;，是因为重写期间，主进程AOF还在继续工作，还是会同步到旧的AOF文件中，同步成功后，“AOF缓冲区”会被清除，会被清除，会被清除！</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（8） 💬（3）<div>Always，everysec，No，这三种模式就是 CAP 理论的体现。</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/66/7a2313ba.jpg" width="30px"><span>ruier</span> 👍（7） 💬（0）<div>有个Django写的Redis管理小系统，有兴趣的朋友可以看一看，名字叫repoll
https:&#47;&#47;github.com&#47;NaNShaner&#47;repoll</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/25/ca/96734ade.jpg" width="30px"><span>随机漫步的傻瓜</span> 👍（6） 💬（0）<div>感觉老师没有刻意把进程和线程分的特别清楚</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/60/4f/db0e62b3.jpg" width="30px"><span>Daiver</span> 👍（6） 💬（2）<div>AOF重写过程，主线程接收到了新的请求，并将日志写入缓冲区，如果宕机了，缓冲区的内容还是会丢失的。子进程在写日志时，重写缓冲区也是可能会丢失的，为啥说AOF日志还是齐全的，怎么可以用于恢复呢？</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/8e/a6/c3286b61.jpg" width="30px"><span>Java垒墙工程师</span> 👍（6） 💬（0）<div>试听完了，彻底入坑</div>2020-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIL1K9WKIkvsdWBwthxz7M08hvqrbeibtzq9rKreZ8wEtHJa2F6x8C1f0dicibMOH6FUW2ayrBYlsEqQ/132" width="30px"><span>杨小羊快跑</span> 👍（5） 💬（3）<div>开启AOF，有可能导致Redis hang住。日志里也有体现：Asynchronous AOF fsync is taking too long (disk is busy?). Writing the AOF buffer without waiting for fsync to complete, this may slow down Redis 
主要原因：Linux规定执行write(2)时，如果对同一个文件正在执行fdatasync(2)将kernel buffer写入物理磁盘，或者有system wide sync在执行，write(2)会被Block住，整个Redis被Block住。（注：Redis处理完每个事件后都会调用write(2)将变化写入kernel的buffer）</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/85/f72f1d94.jpg" width="30px"><span>与路同飞</span> 👍（5） 💬（6）<div>1.子线程重新AOF日志完成时会向主线程发送信号处理函数，会完成 （1）将AOF重写缓冲区的内容写入到新的AOF文件中。（2）将新的AOF文件改名，原子地替换现有的AOF文件。完成以后才会重新处理客户端请求。
2.不共享AOF本身的日志是防止锁竞争，类似于redis rehash。</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/64/be/12c37d15.jpg" width="30px"><span>CityAnimal</span> 👍（4） 💬（0）<div>笔记打卡

    * [ ] 原理
        * [ ] 写后日志
            * [ ] 好处：
                * [ ] 避免出现记录错误命令的情况
                * [ ] 不会阻塞当前的写操作
            * [ ] 风险
                * [ ] 执行完命令后宕机 =&amp;gt; 数据丢失
                * [ ] 给下一个操作带来阻塞风险
                    * [ ] AOF 日志也是在主线程中执行的
        * [ ] 内容：收到的每一条命令，以文本形式保存
            * [ ] 命令：set testkey testvalue
            * [ ] aof: *3\n$3\nset\n$7\ntestkey\n$9\ntestvalue
                * [ ] *3 : 当前命令有三个部分
                * [ ] 每部分都是由“$+数字”开头，后面紧跟着具体的命令、键或值
    * [ ] 写回策略 &amp;lt;= 配置项 appendfsync
        * [ ] Always(同步写回)
            * [ ] 基本不丢数据
            * [ ] 影响主线程性能
        * [ ] Everysec(每秒写回)
            * [ ] 性能适中
            * [ ] 如果发生宕机，上一秒内未落盘的命令操作仍然会丢失
        * [ ] No(操作系统控制的写回)
            * [ ] 性能好
            * [ ] 一旦宕机前AOF 记录没有落盘，对应的数据就丢失了
    * [ ] AOF 文件过大
        * [ ] 性能问题
            * [ ] 文件系统对文件大小有限制
            * [ ] 追加命令记录效率低
            * [ ] 故障恢复非常缓慢
        * [ ] 方案：AOF 重写机制
            * [ ] 原理：根据redis的现状创建一个新的 AOF 文件
            * [ ] !!! 非常耗时 (不阻塞主线程)
                * [ ] 由后台子进程 bgrewriteaof 来完成的
                * [ ] 一个拷贝
                    * [ ] 主线程 fork 出 bgrewriteaof 子进程，并将内存拷贝给 bgrewriteaof
                * [ ] 两处日志
                    * [ ] 正在使用的 AOF 日志
                    * [ ] 新的 AOF 重写日志</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/cd/52753b9e.jpg" width="30px"><span>Anony</span> 👍（4） 💬（3）<div>上节说redis单线程处理网络IO和键值对的读写，持久化是由额外线程处理的。那AOF由额外线程处理的话，为什么会影响主线程呢？和主线程之间是什么关系？</div>2020-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3f/ec/00904faa.jpg" width="30px"><span>连长</span> 👍（3） 💬（0）<div>AOF持久化机制
1、不进行数据校验，直接操作内存，成功后记录日志；
2、主线程把日志记录到AOF缓存区中，不进行持久化磁盘。

刷盘策略，都由子线程执行
1、Always，每执行一条写入操作，刷新缓存区到磁盘；
2、Everysec，每秒刷新缓存区到磁盘；
3、No，由操作系统决定何时将缓存区内存写回磁盘。
三种写回策略都有可能导致数据丢失

AOF重写
1、一个拷贝，两处日志；
2、bgrewriteaof子进程，复制内存数据，把内存数据写入重写日志；
3、AOF重写缓存，保证数据一致；
4、替换AOF日志，完成重写。</div>2021-04-16</li><br/><li><img src="" width="30px"><span>pippin</span> 👍（2） 💬（1）<div>想知道，停电会导致aof日志损坏，需要使用redis-check-aof修复，在哪个环节会导致aof日志损坏</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/11/89ba9915.jpg" width="30px"><span>永远的草莓地</span> 👍（2） 💬（5）<div>redis AOF  appendfsync 选择 always 模式时，是等 fsync 完成之后，才返回成功，还是说先返回成功，之后 再 fsync ？</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（2）<div>老师好，本文循序渐进，线路清晰，实属深度好文，但如“AOF非阻塞的重写过程”图，有几个问题，望回复，谢谢。
1、如果写回策略是Always，是没有AOF缓冲的。是怎么做AOF重写呢？
2、图右边部分有四个日志：两个日志，两个重写日志，请问“一个拷贝，两个日志”中的“日志”是指四个中的哪两个？
3、aof缓冲没有线连到最下面的磁盘吗？</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（2） 💬（0）<div>aof重写，我理解按如下操作也行：

bgrewriteaof线程直接操作磁盘的aof文件，主线程还是写原来的缓存。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（0）<div>appendfsync: no 是系统控制进行写磁盘，这里是利用文件系统的机制吗？ 如果是利用的文件系统的哪个功能， 一般多久进行持久化写磁盘呢？</div>2020-08-14</li><br/><li><img src="" width="30px"><span>你4885</span> 👍（1） 💬（0）<div>有个问题请教一下：
在子进程未完成rewrite操作，且aof rewrite buffer触发写磁盘时，这个时候redis是怎么处理的

我理解的：rewrite操作时将内存中的数据以AOF格式写到新的AOF文件，这个时候aof rewrite buffer触发写磁盘操作应该不能直接插入到新的AOF文件，否则可能会出现旧数据覆盖新数据情况</div>2024-03-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mno5Csic4tevfH5icPib8MOR4DyYpujr3Gls6gibNHZChyDF4rTykdHxBDBssWHGNgwpAhvS90WLCOBbCNSQSgs9pw/132" width="30px"><span>tong96</span> 👍（1） 💬（1）<div>bgrewriteaof是子进程还是子线程啊</div>2022-08-20</li><br/>
</ul>