你好，我是韩健。

咱们都知道，系统在运行中，不可避免会出现各种各样的问题，比如进程崩溃了、服务器死机了，这些问题会导致很严重的后果，让系统没办法运行。学完了15讲后，你应该还记得，在ZAB中，写请求是必须在主节点上处理的，而且提案的广播和提交，也是由主节点来完成的。既然主节点那么重要，如果它突然崩溃宕机了，该怎么办呢？

答案是选举出新的领导者（也就是新的主节点）。

在我看来，领导者选举，关乎着节点故障容错能力和集群可用性，是ZAB协议非常核心的设计之一。你想象一下，如果没有领导者选举，主节点故障了，整个集群都无法写入了，这将是极其严重的灾难性故障。

而对你来说，理解领导者选举（也就是快速领导者选举，Fast Leader Election），能更加深刻地理解ZAB协议，并在日常工作中，游刃有余地处理集群的可用性问题。比如如果写请求持续失败，可以先排查下集群的节点状态。

既然领导者选举这么重要，那么ZAB是如何选举领导者的呢？带着这个问题，我们进入今天的学习。

## ZAB如何选举领导者？

既然要选举领导者，那就涉及成员身份变更，那么在ZAB中，支持哪些成员身份呢？

### 有哪些成员身份？

ZAB支持3种成员身份（领导者、跟随者、观察者）。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJExu8mFzkasuz32FLic5HaYMXicEBnpl63CxZoyYywLY3c59uGicCr9FmWicqKfEA73rmYgtglc1ztAg/132" width="30px"><span>Geek_yuanhe</span> 👍（24） 💬（4）<div>韩老师您好，raft算法跟zab的选举区别，可以理解为比较大的区别就是zab是有leader PK，而raft只是先来先得，一旦该节点已经确认投票，后面即使比他任期编号大的选票再来请求投票，也会拒绝，这样理解对么？</div>2020-05-11</li><br/><li><img src="" width="30px"><span>zyz</span> 👍（15） 💬（2）<div>根据获取选举票数过半机制的原则，同时服务器数量为奇数，不会出现选举失败的情况</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/14/099742ae.jpg" width="30px"><span>xzy</span> 👍（9） 💬（2）<div>你好，请问投票的结果如何同步的呢？当选节点知道自己是 leader，怎么让其他节点也知道呢？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（7） 💬（1）<div>不会选举失败。假设要瓜分的节点是2个，那么最终这2个还是需要pk一轮。关键是zab的选票不是一张，是改变就可以投出去。</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（6） 💬（5）<div>老师，我想问一下 &quot;选举出了新领导者，它是不是就可以处理写请求了呢？答案是不行的，比如这个时候各节点的数据副本还不一致呢，这就需要对数据做取舍，解决冲突，实现数据副本的一致&quot;
那是不是raft也是如此呢? 就是说raft选出的新的leader也不能立即响应写请求~ 对吗?</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/92/9c/1312b3ca.jpg" width="30px"><span>小波菜</span> 👍（5） 💬（2）<div>“逻辑时钟（logicclock）（也就是选举的轮次），会影响选票的有效性，具体来说，逻辑时钟大的节点不会接收来自值小的节点的投票信息。比如，节点 A、B 的逻辑时钟分别为 1 和 2，那么，节点 B 将拒绝接收来自节点 A 的投票信息。”
老师我想请教下，
1:逻辑时钟具体工作原理是什么，这边如果A的事务id大于B,B也直接拒绝吗?
2:事务id是如何保证全局单调递增的，类似雪花算法吗？</div>2020-05-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4uiaFspOvPSF8tzalkP0DvCDme7v53eDGkDMsZsibcm31W99Sib2thFe9m3714d4t7qtIcSeyuR1HiaTXZs4TG8enQ/132" width="30px"><span>钟友兵</span> 👍（4） 💬（1）<div>韩老师，如果说投票时，因为网络问题，可能出现接收到的选票出现延迟，比如，节点A只接受到自身的票，没有接收到其他节点的票，其他节点也可能出现接收到的票数不一致的情况，这种情况是如何处理，设置超时时间吗？如果是超时时间，这个值的选取一般有什么原则</div>2020-05-10</li><br/><li><img src="" width="30px"><span>宋菁</span> 👍（3） 💬（2）<div>在网络通讯正常情况下，各个节点都能够收到其他节点的选票，此时必然会选出最终领导者，不会出现选票瓜分的情况，因为即便是两个节点的任期编号和事物标识符一样，集群ID大的仍然会当选，集群ID小的根据规则会选举集群ID大的节点为领导者。</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（2）<div>ZAB协议中,ZAB协议是通过快速领导者选举,来选举出新的领导者的,那么会出现选票会瓜分的情况吗?
必然可能啊,ZAB是一种脱胎于Multi-Paxos的算法,其本质上也是一种投票选举,那么对于这种投票选举,设置不同的选举时间是一种相对较好的选择
看到这个选举突然想到了网络环路中STP的算法解决</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（2） 💬（1）<div>逻辑时钟到底是什么作用呢？我看到源码有这个东西，但是一直把他当做其他的判断条件，既然和选票PK类似，为什么不把逻辑时钟比较的逻辑加入到选票PK的逻辑totalOrderPredicate中呢？还是说这个逻辑时钟只是代表了机器的标识？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/f6/3f8f6775.jpg" width="30px"><span>arun20350130</span> 👍（1） 💬（0）<div>老师,逻辑时钟和epoch是同一个么,他们的关系是什么呢?逻辑时钟可以理解为每次leader挂掉重新选举时,逻辑时钟会重置为0,而epoch是每次触发选举都会加1,不知道理解的时候正确,谢谢老师解答</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/65/06/9d997340.jpg" width="30px"><span>西瓜</span> 👍（0） 💬（0）<div>“ZooKeeper 会将所有未提交提案提交，并使用 lastProcessedZxid 表示节点上提案（包括刚提交的提案）的事务标识符的最大值”

查了很多书籍和文献，对这段话更加质疑了。如果将所有未提交的提案提交，那么这里面肯定包含未被大部分节点热认可，leader也没提交的提案。如果follower提交了这种未被共识的提案，在后续leader崩溃进行选主时将会占有先机，拥有最大的zxid，并将这条记录复制到其他机器上。这样相当于提交了一条未被共识的提案，难到没问题吗？</div>2023-07-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnywjwpeXxRz0ibZS0ibmhVytkVnXiaTjPuicicWNcjiaUsiaicTEGQgtR4bj3ddMnUOKUiau2zcb1UG1R99g/132" width="30px"><span>Geek_c89d45</span> 👍（0） 💬（0）<div>不会出现选票瓜分的情况，因为领导者pk总能比较出优劣，即使epoch相同、zxid相同，最终还有myid兜底，myid是一定不同的。</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/cd/3819726f.jpg" width="30px"><span>徐同学呀</span> 👍（0） 💬（1）<div>原文：当跟随者检测到异常，退出跟随者状态时（在 follower.shutdown() 函数中），ZooKeeper 会将所有未提交提案提交

但是我并没有在源码中找到（3.7.0），哪位大佬找到了可以贴一下局部代码吗</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/c7/a7a5df8b.jpg" width="30px"><span>达子不一般</span> 👍（0） 💬（0）<div>为什么需要领导者pk，pk结果再进行广播？

第一轮投票广播后，每个节点可以从其他节点的response中知道自己是否是数据最完备的节点及数据最完备的节点是谁，此时可以直接更新LEADING和FOLLOWING状态了</div>2021-10-05</li><br/><li><img src="" width="30px"><span>Jia Tiancai</span> 👍（0） 💬（0）<div>1. 领导者选举的目标，是选举出大多数节点中数据最完整的节点，也就是大多数节点中事务标识符值最大的节点。
问题1：如果只有少数节点数据更新，选举出来的主节点数据可能不是最完整的吧？
问题2：一个任期内节点可以响应多次，那么就会存在多个节点都获取大多数选票，出现这种情况怎么处理呢？</div>2021-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e2/c7/f671bd93.jpg" width="30px"><span>amy</span> 👍（0） 💬（1）<div>韩老师，也就是在 follower 检测到 leader 崩溃退出后，follower 切换状态为选举状态并生成初始投票时，选取的事务 zxid 是所有接收到的 proposal 中最大的 zxid，尽管这个 proposal 可能还没有被 commit。 比如，除了原来旧的 leader 外，一个 proposal 仅仅只被集群中的一个 follower 收到，在重新选 leader 时，拥有这个 proposal 的 follower 会被选为新的 leader ，因为事务id zxid 最大，然后这个 proposal 会被同步到整个集群。</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>
epoch和逻辑时钟是什么关系？zookeeper的paper中的伪代码用round这个变量来代表逻辑时钟，其判断逻辑和文章中说的是一样的。那epoch还有什么用处？能否起到raft中term类似的作用？有点糊涂了。逻辑时钟知否只有在lookForLeader方法中才会+1？</div>2021-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（2）<div>感觉这个选举算法好慢，中间有不少通讯其实是可以省略的，过多的通讯在网络较差的情况下必然减慢选举速度，而根据我的理解，迟迟选不出领导者，整个系统就不能写入了，也就是虽然有半数以上节点存活，系统事实上不可用。</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（0）<div>是怎么计算选票的了。每个looking节点是要记录投票信息吗？那looking节点怎么知道投票数超过大多数节点。也就是它怎么知道当前参与所有选举所有节点个数。</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>逻辑时钟怎么理解，不是应该所有节点都参与选举吗，选举一次逻辑时钟加1，那所有节点的逻辑时钟不是应该相同吗</div>2020-08-10</li><br/>
</ul>