你好，我是陈现麟。

通过学习分布式场景下面临的新挑战，你已经了解了从集中式系统演进到分布式系统时，分布式系统在部分故障、异步网络、时钟同步和共识协调这四个方面的新挑战，以及它们对分布式系统设计原则的影响。了解了这些之后，当你在面对分布式系统各种实现的时候，能更深刻地思考这些系统的取舍与权衡了。

经过不断地思考，人们在实践分布式系统架构的时候，从系统可用性和数据一致性的权衡中总结出来了 CAP 理论，它是指导人们在面对架构分布式系统时，进行取舍的设计原则。同时，CAP 理论深刻影响着分布式系统的设计与发展，是我们在学习分布式系统时不能绕过的知识。

所以在这节课中，我将和你一起来讨论什么是 CAP 理论以及它产生的影响，并且我们还会讨论在当前这个时间点，业界对于 CAP 理论的重新思考与理解。

## 什么是 CAP 理论

CAP 理论是加州理工大学伯克利分校的 Eric Brewer 教授在 2000 年 7 月的 ACM PODC 会议上首次提出的，它是 Eric Brewer 在 Inktomi 期间研发搜索引擎、分布式 Web 缓存时得出的关于数据一致性（ C：Consistency ）、服务可用性（ A：Availability ）、分区容错性（ P：Partition-tolerance ）的一个著名猜想：
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（27） 💬（1）<div>cap从每一个定义来说并不是说牺牲了第三者吧，而是尽量保证第三者</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/f7/d6547adb.jpg" width="30px"><span>努力努力再努力</span> 👍（13） 💬（1）<div>1 一致性 （C）一致性级别 是 从高到低
     1.1 强一致性
     1.2 单调一致性
     1.3 会话一致性
     1.4 序列一致性
     1.5 最终一致性
2 可用性 （A）
       关键字： 100%可用 有限时间内 返回结果
3 分区容错性 （P）
      3.1 网络分区
      3.2 网络丢包导致的网络不通 （包含节点宕机）
对可用性的重新思考与理解
基于Raft 算法实现的etcd 属于CP模型，但是也尽量保持了可用性

对一致性的重新思考与理解
就算选择了 AP，哪怕出现网络分区 也要尽量保证高的 一致性级别
 结论：
开发一个分布式系统的时候 系统正常情况 CAP 都要，等到 出现网络分区的时候 再选择放弃 部分A 或者C
尽可能互相满足

自己的思考：
1 上面的每一点 如果是我 有什么方案解决呢？ 
思考题：
大部分时间都是 无问题的，可以保证CAP 共存
只是需要 添加几个方法 
   1. 探知 分区发生问题
   2. 进入显式的分区模式以限制某些操作
   3 启动恢复过程以 恢复数据一致性并补偿分区期间发生的错误
猜测： 可以 先存到本地 ，等分区恢复 ，带着 offset 进行比较 恢复数据</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（12） 💬（1）<div>分布式场景下，站在用户角度思考CAP理论，用户发送一条请求，在正确的时间响应正确的结果，可以被视为同时满足三者的系统设计。站在系统设计者的角度思考CAP理论，同时满足两者而第三者则是努力的方向，先让系统能够用起来，然后迭代优化。这也满足现在常说的“小步子快跑”的说法。</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/63/cd/fd2778c0.jpg" width="30px"><span>leitiannet</span> 👍（9） 💬（1）<div>Redis有主从架构，哨兵架构和集群架构，分别属于什么模型（AP还是CP）？</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d2/a0/c8714628.jpg" width="30px"><span>独一无二</span> 👍（7） 💬（1）<div>文中有一句很有概括性的句子：&quot;在满足分区容错的前提下，没有算法能同时满足数据一致性和服务可用性，只能在数据一致性和服务可用性之间二选一&quot;。也就是未发生p，则ca都可以满足，发生p后，才会选择一个。并不是软件设计之初就必需要舍弃一个。</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/59/91/fa2d8bb2.jpg" width="30px"><span>不吃辣👾</span> 👍（3） 💬（2）<div>老师，我发现人工可以弥补CAP中的任何一项，达到接近100%水平。😅</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a0/59/86073794.jpg" width="30px"><span>Hello,Tomrrow</span> 👍（2） 💬（1）<div>CAP理论只是给我们提供了分布式系统设计的边界，这是好事，避免追求一些极致的尝试。系统设计不像是盖房子，主体结构确定后就不能改变了。系统设计要有灵活性，在不同的业务场景下，微调系统，以便更好的服务业务。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（2） 💬（1）<div>作者您好，关于p，我听到最多的是数据在不同集群中复制。如果一个集群的话，是不是不存在p的问题，即使一个集群中有很多的服务而且这些服务可能会宕机</div>2022-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/af/16/51149d2b.jpg" width="30px"><span>葡萄糖sugar</span> 👍（2） 💬（3）<div>作者你好，cp 我能理解为系统在达到强一致性以及网络分区容忍性，与此同时我们还能够尽力达到可用性，并且依旧保持强一致性吗？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6b/6c/3e80afaf.jpg" width="30px"><span>HappyHasson</span> 👍（1） 💬（4）<div>既然说CAP中的A是100%可用，100%是一个理想值，那说明A是一个不可能达到的方向，AP这个组合不应该存在，理论上只存在CP？</div>2022-02-13</li><br/><li><img src="" width="30px"><span>三毛</span> 👍（1） 💬（1）<div>关于P的重新理解这块，没出问题的时候先上CA，也就是确保强一致性和服务高可用，当出问题的时候再改成CP或者AP，但是架构上不能同时满足吧？除非之前的CA也是尽量CA。</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/35/be8372be.jpg" width="30px"><span>quietwater</span> 👍（0） 💬（1）<div>必须点赞，这是我迄今为止看过的关于CAP理论讲述最透彻的文章，没有之一。问个题外话，对于分布式数据库，老师最看好哪个或哪几个？MongoDB可以替代MySQL吗？</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d2/a0/c8714628.jpg" width="30px"><span>独一无二</span> 👍（0） 💬（1）<div>太好了，老师3月份还在回复评论呢，老师辛苦了。</div>2022-03-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKib3vNM6TPT1umvR3TictnLurJPKuQq4iblH5upgBB3kHL9hoN3Pgh3MaR2rjz6fWgMiaDpicd8R5wsAQ/132" width="30px"><span>陈阳</span> 👍（0） 💬（1）<div>老师，能举个例子吗？ google中spanner的ca是怎样程度的ca， 大概设计是啥？</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a9/99/0002556f.jpg" width="30px"><span>XingAn</span> 👍（1） 💬（0）<div>服务A调用服务B，由于服务B响应超时（原因可能是多样的）导致服务调用失败，可以认为此时发生了分区错误。
如果我们直接将明确的错误提示给用户，我理解是采用了AP设计方案，用户得到了明确但不一定正确的响应，最起码服务是可用的，我们可以采用对账的方式保证数据的最终一致性；
如果我们在服务B超时的情况下，不计时间代价的去不断地查询服务B的处理结果，并在得到明确的结果后选择继续往下执行或者回滚数据，并最终返回结果给用户（很大可能用户此时已经等不耐烦退出页面了），我理解采用的是CP的方案；
不知道这样的理解是否正确？还请陈老师帮忙解答</div>2022-08-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKEDxLO0wLibic5WkVl1x7TIL0fsxX1zl2GbRjutYQ89fGRrv2VKJtNmmJb32iarbcHROlmW8SOQsHag/132" width="30px"><span>X</span> 👍（0） 💬（0）<div>学到了，不是选择题，是多选题</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（0） 💬（0）<div>1 什么是分布式系统？
2 什么是 BASE 理论？
3 经过了黄金十年的 NoSQL 现在怎么样了？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>对于思考题，CAP正确描述的应该是，当P必定出现的时候，优先保证的是A还是C，并不是说CP的时候就没有A，AP的时候就没有C，只是相对于另一个而言，优先级更高而已，这其实也是分布式设计过程中的一个权衡之策。其实对于大部分场景来说，其实正如老是上述所说，网络分区发生的概率很低，可以近似的将系统看成是CA系统，只是现实情况是P必然存在，所以导致A与C的优先级需要在设计之初划定。</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e4/e7/31944ee7.jpg" width="30px"><span>千军万马万马@</span> 👍（0） 💬（0）<div>对于 CAP 理论，我们真的只能三选二吗？</div>2022-03-12</li><br/>
</ul>