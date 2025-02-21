平时的工作中，不知道你有没有遇到过这样的场景，一条SQL语句，正常执行的时候特别快，但是有时也不知道怎么回事，它就会变得特别慢，并且这样的场景很难复现，它不只随机，而且持续时间还很短。

看上去，这就像是数据库“抖”了一下。今天，我们就一起来看一看这是什么原因。

# 你的SQL语句为什么变“慢”了

在前面第2篇文章[《日志系统：一条SQL更新语句是如何执行的？》](https://time.geekbang.org/column/article/68633)中，我为你介绍了WAL机制。现在你知道了，InnoDB在处理更新语句的时候，只做了写日志这一个磁盘操作。这个日志叫作redo log（重做日志），也就是《孔乙己》里咸亨酒店掌柜用来记账的粉板，在更新内存写完redo log后，就返回给客户端，本次更新成功。

做下类比的话，掌柜记账的账本是数据文件，记账用的粉板是日志文件（redo log），掌柜的记忆就是内存。

掌柜总要找时间把账本更新一下，这对应的就是把内存里的数据写入磁盘的过程，术语就是flush。在这个flush操作执行之前，孔乙己的赊账总额，其实跟掌柜手中账本里面的记录是不一致的。因为孔乙己今天的赊账金额还只在粉板上，而账本里的记录是老的，还没把今天的赊账算进去。

**当内存数据页跟磁盘数据页内容不一致的时候，我们称这个内存页为“脏页”。内存数据写入到磁盘后，内存和磁盘上的数据页的内容就一致了，称为“干净页”**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（49） 💬（29）<div>关于粉板和redo log的类比我觉得有一点不太合适：redo log记录的是实时欠款，比如账本中是10文，又欠了9文，此时redo log 记录的是19；而粉板的话，只会追加某人欠款+9文，不会关注原来已欠款多少（不然某人赊账时，我还需要找到账本中的这个人，才知道他之前欠款多少，我觉得这个场景跟MySQL中的场景还是有区别的）
</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/59/b457f370.jpg" width="30px"><span>yesir</span> 👍（58） 💬（9）<div>我观察了下公司的数据库确实发现了抖动现象，有几个问题，
1）Innodb_buffer_pool_pages_total这个值很大，百万级别的，而且数值不像是人为设置上去的，是怎么来的呢？
2）Innodb_buffer_pool_pages_dirty达到4万多的时候就开始flush了，脏页比例是75，这肯定是远达不到的，ssd磁盘，innodb_io_capacity是200，肯定可以提高。文章中说flush的触发条件有2个，一个是内存不够了，一个是redo log 满了，那么我这个场景是哪种情况呢 </div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/70/f3a33a14.jpg" width="30px"><span>某、人</span> 👍（224） 💬（15）<div>redo log是关系型数据库的核心啊,保证了ACID里的D。所以redo log是牵一发而动全身的操作
按照老师说的当内存数据页跟磁盘数据页不一致的时候,把内存页称为&#39;脏页&#39;。如果redo log
设置得太小,redo log写满.那么会涉及到哪些操作呢,我认为是以下几点:
1.把相对应的数据页中的脏页持久化到磁盘,checkpoint往前推
2.由于redo log还记录了undo的变化,undo log buffer也要持久化进undo log
3.当innodb_flush_log_at_trx_commit设置为非1,还要把内存里的redo log持久化到磁盘上
4.redo log还记录了change buffer的改变,那么还要把change buffer purge到idb
以及merge change buffer.merge生成的数据页也是脏页,也要持久化到磁盘
上述4种操作,都是占用系统I&#47;O,影响DML,如果操作频繁,会导致&#39;抖&#39;得向现在我们过冬一样。
但是对于select操作来说,查询时间相对会更快。因为系统脏页变少了,不用去淘汰脏页,直接复用
干净页即可。还有就是对于宕机恢复,速度也更快,因为checkpoint很接近LSN,恢复的数据页相对较少
所以要控制刷脏的频率,频率快了,影响DML I&#47;O,频率慢了,会导致读操作耗时长。
我是这样想的这个问题,有可能不太对,特别是对于第4点是否会merge以及purge,还需要老师的解答</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/bd/6c7d4230.jpg" width="30px"><span>Tony Du</span> 👍（460） 💬（47）<div>当内存不够用了，要将脏页写到磁盘，会有一个数据页淘汰机制（最久不使用），假设淘汰的是脏页，则此时脏页所对应的redo log的位置是随机的，当有多个不同的脏页需要刷，则对应的redo log可能在不同的位置，这样就需要把redo log的多个不同位置刷掉，这样对于redo log的处理不是就会很麻烦吗？（合并间隙，移动位置？）
另外，redo log的优势在于将磁盘随机写转换成了顺序写，如果需要将redo log的不同部分刷掉（刷脏页），不是就在redo log里随机读写了么？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/1d/ec173090.jpg" width="30px"><span>melon</span> 👍（164） 💬（28）<div>又思考了一下，请老师帮忙看一下理解的对不对：buffer pool里维护着一个脏页列表，假设现在redo log 的 checkpoint 记录的 LSN 为 10，现在内存中的一干净页有修改，修改后该页的LSN为12，大于 checkpoint 的LSN，则在写redo log的同时该页也会被标记为脏页记录到脏页列表中，现在内存不足，该页需要被淘汰掉，该页会被刷到磁盘，磁盘中该页的LSN为12，该页也从脏页列表中移除，现在redo log 需要往前推进checkpoint，到LSN为12的这条log时，发现内存中的脏页列表里没有该页，且磁盘上该页的LSN也已经为12，则该页已刷脏，已为干净页，跳过。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/2b/2702fcbe.jpg" width="30px"><span>jimmy</span> 👍（130） 💬（11）<div>老师，我想问一下，innodb是如何知道一个页是不是脏页的，是有标记位还是通过redolog的ckeckpoint来确定的？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/3d/51762e76.jpg" width="30px"><span>大白给小白讲故事</span> 👍（81） 💬（11）<div>“内存不够用了，要先将脏页写到磁盘“和“redo log 写满了，要 flush 脏页”可以理解为一个脏页本身占用内存，释放内存需要将脏页写入到磁盘才能释放。而redo log写满只有当redo log对应的脏页flush到磁盘上才能释放对应空间。有几个问题：
1、“内存不够用了，要先将脏页写到磁盘“redo log对应的空间会释放嘛？“redo log 写满了，要 flush 脏页”对应的内存页会释放嘛？
2、将脏页flush到磁盘上是直接将脏页数据覆盖到对应磁盘上的数据？还是从磁盘上取到数据后取根据redo log记录进行更新后再写入到磁盘？
3、redo log是怎么记录对应脏页是否已经flush了？如果断电了重启导致内存丢失，前面几章说通过redo log进行数据恢复那redo log又怎么去释放空间？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9c/9c/e02a0daf.jpg" width="30px"><span>运斤成风</span> 👍（69） 💬（2）<div>老师好，flush和purge是不是还是有区别的？flush主要指刷新脏页，和clean进程相关？而purge是清理不再被使用的undo信息。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（59） 💬（3）<div>100M的redo很容易写满，系统锁死，触发检查点推进，导致写操作卡住。由于主机IO能力很强，检查点会很快完成，卡住的写操作又很快可以执行。循环往复，现象就是写操作每隔一小段时间执行就会变慢几秒。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/e7/4ce5ed27.jpg" width="30px"><span>lunung</span> 👍（51） 💬（1）<div>很多测试人员再做压力测试的时候 出现刚开始 insert update 很快 一会 就出现很慢,并且延迟很大，大部分是因为redo log 设置太小 引起的,完美诠释</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/12/a169bdcd.jpg" width="30px"><span>Geek_477c02</span> 👍（33） 💬（1）<div>InnoDB 认为这个系统的能力就这么差，所以刷脏页刷得特别慢，甚至比脏页生成的速度还慢，这样就造成了脏页累积，影响了查询和更新性能。为什么会影响性能，是因为要读取的数据不在内存中，但是脏页过多导致新页必须等待脏页刷盘导致的么？</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/bd/6c7d4230.jpg" width="30px"><span>Tony Du</span> 👍（26） 💬（11）<div>当内存不够用了，要将脏页写到磁盘，会有一个数据页淘汰机制（最久不使用），假设淘汰的是脏页，则此时脏页所对应的redo log的位置是随机的，当有多个不同的脏页需要刷，则对应的redo log可能在不同的位置，这样就需要把redo log的多个不同位置刷掉，这样对于redo log的处理不是就会很麻烦吗？（合并间隙，移动位置？）
另外，redo log的优势在于将磁盘随机写转换成了顺序写，如果需要将redo log的不同部分刷掉（刷脏页），不是就在redo log里随机读写了么？

作者回复
好问题。 

其实由于淘汰的时候，刷脏页过程不用动redo log文件的。

这个有个额外的保证，是redo log在“重放”的时候，如果一个数据页已经是刷过的，会识别出来并跳过。

我的回复
这个额外保证是如何做到的？能不能稍微解释下
通过刷脏页时数据页更新的timestamp来对比redo log的timestamp？</div>2018-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq46o2L7ibj1L7Uh44pLTgJrsnRezptClG1HD1PdGImspBLvFcsp0l1Wp8WDVt6sN7NUKC8aqKXnJA/132" width="30px"><span>老鱼头</span> 👍（22） 💬（3）<div>那个说fio命令会破坏硬盘的兄弟，是没用对命令。估计把-filename=&#47;dev&#47;sdb1 。。。这个的意思是从 分区 sdb1 的第一个扇区开始写入随机数据，去判断这个磁盘的写入速度。如果指定路径+文件名就不会出这事了~比如老师给的例子~</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/cb/6bc95e09.jpg" width="30px"><span>喔～</span> 👍（21） 💬（3）<div>老师，请问下访问某条记录时，存储引擎是如何判断这条记录所在的数据页是否在内存当中，这个查内存机制是如何实现的？</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/6a/3c618346.jpg" width="30px"><span>二桃杀三士</span> 👍（15） 💬（4）<div>老师您好，请教一个问题：

当内存不够用了，要将脏页写到磁盘，会有一个数据页淘汰机制（最久不使用），假设淘汰的是脏页，则此时脏页所对应的redo log的位置是随机的，
当有多个不同的脏页需要刷，则对应的redo log可能在不同的位置，这样就需要把redo log的多个不同位置刷掉，
这样对于redo log的处理不是就会很麻烦吗？（合并间隙，移动位置？）
另外，redo log的优势在于将磁盘随机写转换成了顺序写，如果需要将redo log的不同部分刷掉（刷脏页），不是就在redo log里随机读写了么？
作者回复: 好问题。 

其实由于淘汰的时候，刷脏页过程不用动redo log文件的。

这个有个额外的保证，是redo log在“重放”的时候，如果一个数据页已经是刷过的，会识别出来并跳过。

在这个问题中关于您说的淘汰脏页过程中是不用动redo log的。
老师可以先看一下链接https:&#47;&#47;www.cnblogs.com&#47;f-ck-need-u&#47;archive&#47;2018&#47;05&#47;08&#47;9010872.html#commentform中的1.7章节
我的理解是：
可能是这个意思。此时脏页占缓冲池75%时，进行fuzzy checkpoint（一次只刷一小部分的日志到磁盘，而非将所有脏日志刷盘）方式中的dirty page too much checkpoint，逐渐推进的时候，若此时业务压力增大，脏页占缓冲池比例增加，此时内存不足，需要淘汰脏页，在淘汰的过程中，因为部分脏页不是顺序的，那此时淘汰的过程中刷脏页是不用动redo log的，在redo log“重放”的时候，如果一个数据页已经是刷过的，会识别出来并跳过。重点是淘汰脏页。相当于兜底方案，脏页占75%的时候，强制触发检查点；当脏页比例继续增大时，内存撑不住了，启用兜底方案，开始淘汰脏页，而这个过程，就如上所说。
所以我有两个问题：
1.就是系统正常刷脏页（比如这种方式dirty page too much checkpoint）会推进checkpoint，而因淘汰脏页的刷脏页并不会推进checkpoint？
2.关于链接中1.7章节的数据页刷盘规则其实也是触发checkpoint推进的方式？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（15） 💬（1）<div>redo日志设置太小，内存又比较大，导致innodb缓存的脏页还没多少就开始大量flush，刷写频率增大。感觉有点像jvm中，年轻代内存设置小点，导致频繁younggc。当然这就是个权衡，毕竟redo和内存不能无限大。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/ab/1aac53bf.jpg" width="30px"><span>董航</span> 👍（14） 💬（3）<div>怎么说呢，越看越明白，哈哈，前面不懂的，后面就懂了</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/20/a02c4f61.jpg" width="30px"><span>didiren</span> 👍（12） 💬（1）<div>用fio压测的结果，读写的iops是一样的，那么io_capacity按照这个值设，还是设为读写相加</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bd/da/3d76ea74.jpg" width="30px"><span>看不到de颜色</span> 👍（11） 💬（2）<div>看完这一章明白了原来数据落盘不仅仅只是定时刷redo log及快写满是才会进行。当内存不足要淘汰掉的数据页为脏页时会直接将内存中脏页的数据刷入磁盘。不过此时产生了几个疑问。
1、如果直接将内存中的数据页刷入磁盘，那redo log中的数据怎么办，会去删除吗？如果是那redo log岂不就不连续了。如果不是的话当刷redo log时又该怎么判断此时硬盘中的数据已经是最新的数据了呢。
2、在执行DML操作时应该是总共有两处写磁盘是吗？先是innodb层的redo log落盘，紧接着MySQL server层的bin log落盘。这两处写磁盘都是同步写操作吗？
还望老师可以在百忙之中不吝赐教，感激不尽*^o^*</div>2019-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKWBSfZTcUiaJ0Rxibe9VSDSBDEhM8lNjrTiahUrDibboxW1M8JQc7M9QevUZdVXI8N10BWpEsKc2bPKQ/132" width="30px"><span>克己过</span> 👍（9） 💬（2）<div>老师！！！fio这条命令是会破坏硬盘的！而且百度搜出来不加硬盘坏关键词去搜，搜出来的文章没有一篇会告诉你这个事情！！！不说了，我去恢复数据了😭</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/61/691e2936.jpg" width="30px"><span>算不出流源</span> 👍（7） 💬（1）<div>思考题:redo log较小，此时F2(N)就容易较大，后台刷脏页的速度就会较快，但是机器iops很高，所以即使在mysql负载较高的情况下，也不会造成redo log写满，因为innodb会照着最大iops的目标去请求io，而读写数据库的业务请求也机器朝最大iops能力去挤，最终两类io需求相互竞争达到一个动态平衡，redo log不会被灌满，但业务请求也没有空闲的时候执行速度快。
    所以我认为应该不是造成抖动，而是业务负载较大的情况下，完成业务请求的平均时间会较系统空闲时加倍。不知道理解有没有问题，请老师指正</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/b6/f404b490.jpg" width="30px"><span>我是小队长</span> 👍（6） 💬（2）<div>mysql&gt; select VARIABLE_VALUE into @a from global_status where VARIABLE_NAME = &#39;Innodb_buffer_pool_pages_dirty&#39;;
1146 - Table &#39;mysql.global_status&#39; doesn&#39;t exist

为啥会出现表不存在呢？</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/5d/f4d789cc.jpg" width="30px"><span>极客童</span> 👍（5） 💬（2）<div>梳理一下之前的知识，存储引擎接到一个更新操作时，操作过程是：
1、引擎将这行新数据更新到change buffer中，同时将这个更新操作记录到redo log 里面；
2、此时 redo log 处于 prepare 状态，再生成写入binlog；
3、最后把redo log commit。change buffer找时机merge到buffer pool。

对本题目，如果redo log过小，会频繁触发purge操作，purge操作即buffer pool刷脏页的同时把redolog的checkpoint往前移动，导致频繁的磁盘io，结果就是mysql频繁的抖动。我的理解对吗？
</div>2018-12-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（3） 💬（1）<div>
老师请问下 innodb_io_capacity我们默认是200,在高并发插入场景下,cpu使用率很低,但是cpu iowait高,这种情况下 调大  innodb_io_capacity 是否有用呢,我用了您的测试方法,iops随机读写都为1K
</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/41/b868f086.jpg" width="30px"><span>小确幸</span> 👍（3） 💬（1）<div>有两个疑问：
1、数据库的页，与书本的页在概念上是类似的吗？
2、在内存中的页数据，与查询缓存有什么区别？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2b/fd/7013289d.jpg" width="30px"><span>温故而知新可以为师矣</span> 👍（2） 💬（1）<div>最近做日报表采用的就是年与日用&quot;int&quot;来存储，只是没想到“这就是简单的hash“，瞬间高大上，哈哈哈。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/fe/04f56d1e.jpg" width="30px"><span>learn more</span> 👍（2） 💬（1）<div>老师你好，请问如何才能判断出，当前的MySQL是否正在刷脏页，或说是因为刷脏页影响到了MySQL性能？
如果发现是在刷脏页，又如何判断MySQL是因为内存不足导致的还是redo log 满了导致的呢？
看完这篇文章我知道了刷脏页会影响性能，也知道为什么会刷脏页，但是我却没有手段知晓线上是因为刷脏页才影响到MySQL性能。</div>2019-12-25</li><br/><li><img src="" width="30px"><span>700</span> 👍（2） 💬（1）<div>利用 WAL 技术，数据库将随机写转换成了顺序写，大大提升了数据库的性能。
----
老师，您好。这句话不懂？
随机写是指脏页写磁盘吗？
顺序写是指写 redo log 吗？

如果没有 WAL 技术，数据库是怎样更新数据的？
</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/43/38f6f7a1.jpg" width="30px"><span>tc_song</span> 👍（2） 💬（1）<div>老师，我这边遇到一个问题，生产系统突然出现pager_cleaner了七百多秒，但是业务系统中应该没有大sql,slow log中也没有长sql记录，这个时候业务系统的查询全部被卡住，十几分钟后才执行完毕。这个是啥方面问题呢？
2018-12-20
 作者回复
是不是之前刚刚做了大量更新？或者近期做了大量更新，然后系统突然闲下来了？

业务上没什么特别，没有大量更新，运行了一年多第一次出现，而且一天之内出现两三次</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/b2/ca764e25.jpg" width="30px"><span>假装有网名</span> 👍（2） 💬（1）<div>我们现在数据由于近期一直在做老数据割接，频繁事务同步数据，一天一个库要被重新刷N次，结果在不执行数据割接时候mysql瞬间cpu就很高，影响了正常的访问，这会不会是由于系统处理脏页完成的？今天刚看到文章，还没看配置，望老师指点。</div>2018-12-18</li><br/>
</ul>