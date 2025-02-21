你好，我是王磊，你也可以叫我Ivan。

在上一讲的开头，我提了一个问题：对分布式数据库来说，“强一致性”意味着什么？我们经过分析后得出的结论是这个强一致性，包括数据一致性和事务一致性两个方面。然后，我们介绍了数据一致性是怎么回事儿。那么，今天我们会继续这个话题，谈谈事务一致性。

每次，我和熟悉NoSQL同学聊到事务这个话题时，都会提到ACID和BASE。甚至，不少同学会觉得ACID有些落伍了，以BASE为理论基础的NoSQL，才是当下的潮流。

那我们来看看BASE是什么？其实，它代表了三个特性，BA表示基本可用性（Basically Available），S表示软状态（Soft State），E表示最终一致性（Eventual Consistency）：

- 基本可用性，是指某些部分出现故障，那么系统的其余部分依然可用。
- 软状态或柔性事务，是指数据处理过程中，存在数据状态暂时不一致的情况，但最终会实现事务的一致性。
- 最终一致性，是指单数据项的多副本，经过一段时间，最终达成一致。这个，我们在第2讲已经详细说过了。

总体来说，BASE是一个很宽泛的定义，所做的承诺非常有限。我认为，BASE的意义只在于放弃了ACID的一些特性，从而更简单地实现了高性能和可用性，达到一个新的平衡。但是，架构设计上的平衡往往都是阶段性的，随着新技术的突破，原来的平衡点也自然会改变。你看，不用说分布式数据库，就连不少NoSQL也开始增加对事务的支持了。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/e0/d856f5a4.jpg" width="30px"><span>余松</span> 👍（43） 💬（9）<div>这篇文档是我见到少有提到写倾斜关于隔离的文档了，（实际上大部分人对事物的了解都是面试前背一背4中隔离级别)。喜欢这篇文档的同学强烈建议看一看《数据密集型系统设计》这本书，它虽然没直接提到Critique的六种隔离级别，但是详细介绍了快照级别的隔离和写倾斜的例子。看评论，很多同学对写倾斜不太明白，我解释一下：写倾斜其实更像是业务应该考虑的事情，就是你要做一件事（修改数据A），依赖于目前已经存在其他数据B。但是你修改数据A的时候是不锁定数据B的，你修改的过程中，A被另外一个用户修改了，造成你最终目的的没达到（一致性)。常见的场景，如用户余额减扣，排班等等。
要规避写倾斜的措施有多种，我列举一下，其中前两种是老师提到的：
1.实际串行执行（典型的就是redis）
2.SSI（实际上是一个学生的论文得到的)，就是乐观锁的原理
3.基于两阶段加锁锁定读数据（简言之就是对读到的不需要修改的数据也加锁 for update）
4.实体化冲突（这个参考mysql45讲，林老师的方案）
5.业务上控制（我觉得工作中用的比较多，比如电商的余额锁定和优惠券锁定类似于TCC吧）

</div>2021-01-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJqUkoCXOxRraVNVg1fTm4O892WFVCjeL9pS8kUX2nEeTEcaS6k0kP25h3rRKtUCwSoUrY6dvP43w/132" width="30px"><span>赵见跃</span> 👍（30） 💬（13）<div>写的太好了！！！
当初就是学习了林晓斌老师《MySQL 实战 45 讲》，使我认识了极客时间，课程非常好！
随后又买了几个课程，可惜都没有达到林晓斌老师的高度，曾经一度对极客时间产生了怀疑，
还好，幸运的是今天看到了王磊的课程，感觉又有希望了。王老师的课程客观理性、深入浅出！
收获满满，谢谢老师。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/16/40/c1d71b93.jpg" width="30px"><span>过</span> 👍（11） 💬（1）<div>老师，我的观察点和大家不太一样，我想请问 比如&quot;A Critique of ANSI SQL Isolation Levels“这样的论文，在国外是发布在哪里的，以及 数据库方面相关的论文或一手资源 有哪些值得关注的信息源。（说白点就是，在信息渠道获取方面，我应该怎么让自己混得6一点）</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/85/f72f1d94.jpg" width="30px"><span>与路同飞</span> 👍（7） 💬（1）<div>老师每节课的思维导图很赞</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/97/f1a3d398.jpg" width="30px"><span>张永志</span> 👍（6） 💬（8）<div>有关MVCC我发表一下自己的认识：
MySQL下 RR与RC隔离级别的操作都分当前读和快照读，当前读才会加锁，快照读都是不加锁的。RR 快照读是可以消除幻读的，因为这是事务开始时的快照一致性读，而RC是语句快照一致性读。
有关本课的问题：
数据块未能及时落盘，重新启动数据库会进行实例恢复，从最后的检查点开始将redo进行前写和回滚，这样就能保证数据块与redo一致了，实例恢复后，数据库就可以对外访问了。
</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f2/66/b16f9ca9.jpg" width="30px"><span>南国</span> 👍（4） 💬（6）<div>首先回答问题，其实对此方面了解不多，强答一下：其实预写日志在我看来就是redo日志，如果redo日志已经成功证明已经落盘，此时数据可以根据redo日志异步的刷回磁盘，写数据表失败应该就是后面异步写回出现问题，我们只需要重演redo日志就可以了。当然这只是最简单的过程，细节还是看其他留言和老师的解答啦

其实我感觉这一章中既然是说分布式数据库的事务，我觉得也应该说说分布式事务，毕竟我们定义了数据库是分片的，如果事务涉及到多个机器就得上分布式事务了呀。

还有确实很巧，以前我写过一篇关于事务的博客，里面有几个例子都非常直观，理解起几个文中的概念也更简单些：https:&#47;&#47;blog.csdn.net&#47;weixin_43705457&#47;article&#47;details&#47;105443927</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/e2/297518ab.jpg" width="30px"><span>佳佳的爸</span> 👍（3） 💬（1）<div>解决写倾斜主要就是加上写锁，但是这样会严重影响并发性能。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（1） 💬（1）<div>&quot; 数据一致性关注的是单对象、单操作在多副本上的一致性，事务一致性则是关注多对象、多操作在单副本上的一致性，分布式数据库的一致性是数据一致性与事务一致性的融合。&quot; 
老师，分布式数据肯定也要支持分布式事务，那分布式事务是多对象、多操作在多副本上的实现吗？有点混了。</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（1）<div>我之前的发言有些误解，我再阐述一下：
SI隔离级别是MVCC，实际上RR也可以用MVCC，不过之前没有这种技术，都用的是2PL。SI主要通过Gap lock来解决RR的幻读？因为光一个MVCC是解决不了幻读的。</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（2）<div>有点问题：
快照隔离相当于是比可重复读解决了幻读的问题，文章中说是MVCC的功能特性，但是MVCC并不能解决幻读呀，真正解决幻读的是Gap Lock（Mysql）？

而且可重复读也可以使用MVCC来实现吧？</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/0e/9ce05946.jpg" width="30px"><span>distdev</span> 👍（1） 💬（1）<div>关于redo log有一个问题， 就是何时同步到磁盘？完全同步太慢，如果成批处理又有可能丢数据， 老师能否谈谈经验？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/97/dfadcc92.jpg" width="30px"><span>Kang</span> 👍（0） 💬（1）<div>老师，单对象，单操作和多对象，多操作是指在一个事物内，对多个表或者库（单个表单个库）进行的dml或者ddl这样理解吗</div>2021-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（0） 💬（1）<div>真的是好的课程，谢谢老师了，希望在文章后面增加一些理论的引用链接。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/df/9d/0d334026.jpg" width="30px"><span>胡须老爹</span> 👍（0） 💬（1）<div>这课程太好了，非常清晰的脉络，看得停不下来。</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/9a/4231fb93.jpg" width="30px"><span>nemo</span> 👍（0） 💬（1）<div>老师，citus可以加入讲讲么</div>2020-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a5/5b/e1ffd5e4.jpg" width="30px"><span>纸君</span> 👍（2） 💬（0）<div>参考mysql设计:  redo log成功后，假如未完成落盘，则下次启动时检测并重新落盘。   落盘是按照数据库逻辑页大小落盘的，且redo log是页增量日志，这里可能有两种情况:  
1. 逻辑页和数据页大小相等， 则从未入库部分开始继续入库。  

2.当逻辑页 与 磁盘数据页大小不相等时， 查看double write 在磁盘的内容确定是否出现了页断裂，修复页断裂部分后，走1逻辑</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（2） 💬（0）<div>老师，你好，这个写倾斜还是不太明白。</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/0e/9ce05946.jpg" width="30px"><span>distdev</span> 👍（2） 💬（3）<div>关于幻读， 一直不明白实际工程中幻读在哪种情况下会有问题？似乎绝大多数情况一个事务看见其他的事务的创建或者删除记录都不是问题。老师能否给举个例子？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/e0/d856f5a4.jpg" width="30px"><span>余松</span> 👍（1） 💬（2）<div>在没有MVCC的情况下，使用读写锁+范围锁是否也可以解决幻读问题。</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（1）<div>老师，你在文中说ANSI SQL 92没有考虑快照隔离的原因是MVCC技术的不广泛？为什么MVCC使用不广泛就不能考虑SI呢？这之间的推导关系能再阐述一下吗？

另外答个题：
一般事务操作流程是WAL+内存写。WAL是持久化的，也就是说硬件无故障的话上不会丢失。如果在内存写的时候崩溃了，那么数据库重启的时候就要检查日志，如果日志表明已提交，而真正的数据还没有写完，则要重放。需要一套机制来判断日志中的事务是否已提交等等。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>对于文章那个写倾斜的图不是很理解，老师可以解释下执行过程吗？ 方便更好的理解</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/39/4089c9b5.jpg" width="30px"><span>胖子罗</span> 👍（0） 💬（0）<div>还是没看明白什么是写倾斜 什么是快照隔离？</div>2023-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7d/ac/a9cd5ff0.jpg" width="30px"><span>w⃰e⃰i⃰</span> 👍（0） 💬（0）<div>有个错别字：小结里面的图片，未提交读，写成了未提交都</div>2023-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/70/f59db672.jpg" width="30px"><span>槑·先生</span> 👍（0） 💬（0）<div>老师讲的很清晰，不考虑再出一个课程吗？</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（0）<div>赞一个，跟《数据密集型应用系统设计》上说的对上了</div>2021-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/40/c0/18066d53.jpg" width="30px"><span>早睡早起</span> 👍（0） 💬（0）<div>老师您好，请教个问题，Strict Serializable解决了SSI哪些未能解决的问题呢？</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c2/fc/1bae4cdc.jpg" width="30px"><span>我要打十个</span> 👍（0） 💬（0）<div>单对象，多对象，单操作，多操作，单副本，多副本这些概念能否具体介绍下，感觉有点混乱😂</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/b2/274a4192.jpg" width="30px"><span>漂泊的小飘</span> 👍（0） 💬（2）<div>我记得之前看Mysql的课 ，里面介绍可重复读的实现就是靠的快照。这个和快照隔离的快照有什么区别吗？</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/32/1fd102ec.jpg" width="30px"><span>真名不叫黄金</span> 👍（0） 💬（0）<div>我想，日志落盘后即可根据日志进行数据表的重写，因此只要日志在，那么数据表可以根据最近的checkpoint进行恢复</div>2020-08-20</li><br/>
</ul>