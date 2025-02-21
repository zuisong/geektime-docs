你好，我是胡夕。今天我要和你分享的主题是：Kafka中的高水位和Leader Epoch机制。

你可能听说过高水位（High Watermark），但不一定耳闻过Leader Epoch。前者是Kafka中非常重要的概念，而后者是社区在0.11版本中新推出的，主要是为了弥补高水位机制的一些缺陷。鉴于高水位机制在Kafka中举足轻重，而且深受各路面试官的喜爱，今天我们就来重点说说高水位。当然，我们也会花一部分时间来讨论Leader Epoch以及它的角色定位。

## 什么是高水位？

首先，我们要明确一下基本的定义：什么是高水位？或者说什么是水位？水位一词多用于流式处理领域，比如，Spark Streaming或Flink框架中都有水位的概念。教科书中关于水位的经典定义通常是这样的：

> 在时刻T，任意创建时间（Event Time）为T’，且T’≤T的所有事件都已经到达或被观测到，那么T就被定义为水位。

“Streaming System”一书则是这样表述水位的：

> 水位是一个单调增加且表征最早未完成工作（oldest work not yet completed）的时间戳。

为了帮助你更好地理解水位，我借助这本书里的一张图来说明一下。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/e2/dbc4a5f2.jpg" width="30px"><span>朱东旭</span> 👍（17） 💬（5）<div>胡老师您好，在您讲的leader epoch机制案例中，在我看来最关键的操作是broker重启后先向leader确认leo,而不是直接基于自己的高水位截断数据，来防止数据不一致。。可是有无leader epoch都可以做这个操作呀，我看不出leader epoch必要性在哪。。
</div>2019-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/6e/0a300829.jpg" width="30px"><span>李先生</span> 👍（13） 💬（3）<div>胡哥，有两个问题：
1:为什么broker重启要进行日志截断，触发日志截断的前提是什么？目的是什么？
2:acks=all,是代表同步到所有isr中broker的pagecache中还是磁盘？min.insync.replicas是配合acks=all来使用的，是一个保证消息可靠性的配置，比如设置为2，是代表在isr中至少两个broker上写入消息，这个写入是写入pagecache中还是磁盘中？如果都是写入pagecache中，kafka是有异步线程来定时从pagecache中拉消息写入磁盘吗？</div>2020-04-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/SM4fwn9uFicXU8cQ1rNF2LQdKNbZI1FX1jmdwaE2MTrBawbugj4TQKjMKWG0sGbmqQickyARXZFS8NZtobvoWTHA/132" width="30px"><span>td901105</span> 👍（9） 💬（6）<div>老师您好,我怎么感觉只需要在副本拉取Leader的LOG就不会产生日志截断的问题了,感觉不需要Leader Epoch?</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/27/385b3e33.jpg" width="30px"><span>Johnson</span> 👍（8） 💬（2）<div>老师您好，有个疑问，leader epoch怎么做到像hw里的数据可见性的，比如hw可以保证消费端只能消费hw之前提交的消息，leader epoch如何保证这点，谢谢！</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/7d/112bc7e1.jpg" width="30px"><span>faunjoe</span> 👍（7） 💬（1）<div>多个broker 中的leader epoch 他们是版本号是怎么保持累加的</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（7） 💬（2）<div>倘若此时副本 B 所在的 Broker 宕机，当它重启回来后，副本 B 会执行日志截断操作，将 LEO 值调整为之前的高水位值，也就是 1。
-------------------------------------------------------------&gt;
老师，请问为什么要将LE0的值设置为HW的值。LEO的值是消息写入磁盘后才被更新的，也就是数据已经落地。重启后继续用LEO的值会有什么问题吗</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/87/b32dc1ea.jpg" width="30px"><span>😈😈😈😈😈</span> 👍（7） 💬（2）<div>这个是我理解的HW和LEO更新的机制步骤，有错误的话请大神指明下，非常感谢
更新对象 更新时机
Broker1上Follower副本 Follwer会从Leader副本不停的拉取数据，但是Leader副本现在的没有数据。所以Leader副本和Follower副本的高水位值和LEO值都是0
Broker0上的Leader副本 生产者向Leader副本中写入一条数据，此时LEO值是1,HW值是0。也就是说位移为0的位置上已经有数据了
Broker1上Follower副本 由于Leader副本有了数据，所以Follower可以获取到数据写入到自己的日志中，且标记LEO值为1，此时在Followe位移值为0的位置上也有了数据，所以此时Follower的HW=0，LEO=1
Broker1上Follower副本 获取到数据之后，再次向Leader副本拉数据，这次请求拉取的数据是位移值1上的数据
Broker0上的远程副本 Leader收到Follower的拉取请求后，发现Follower要拉取的数据是在位移值为1的位置上的数据，此时会更新远程副本的LEO值为1。所以所有的远程副本的LEO等于各自对应的Follower副本的LEO值
Brober0上的Leader副本 Broker0上的远程副本的LEO已经更新为1了。所以开始更新Leader副本的HW值。HW=max{HW,min(LEO1,LEO2,LEO3......LEON)},更新HW值为1，之后会发送Follower副本请求的数据（如果有数据的话，没有数据的话只发送HW值）并一起发送HW值
Broker1上Follower副本 Follwer副本收到Leader返回的数据和HW值（如果Leader返回了数据那么LEO就是2，没有数据的话LEO还是1），用HW值和自己的LEO值比较选择较小作为自己的HW值并更新HW值为1（如果俩个值相等的话HW=LEO）
一次副本间的同步过程完成 </div>2019-10-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELbKf55SEo9bZ30GAIA09AaaoGvAIibEjNC0rsxpP7r1z4jUUBFz3xepso6CK8bYia6n5wcAyOQUfibA/132" width="30px"><span>Geek_0819</span> 👍（6） 💬（4）<div>胡老师有个疑问：生产者同步发送消息时指定同步到所有副本，生产者是等待所有副本的LEO都写入成功才返回吗？如果是这样Follower副本从Leader上拉取LEO是有时间间隔的，这样生产者都在这里等待很久吗？还是其他方式的交互？</div>2020-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/e9/95ef44f3.jpg" width="30px"><span>常超</span> 👍（6） 💬（3）<div>请问老师，与 Leader 副本保持同步的两个判断条件，是OR还是AND的关系？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（5） 💬（3）<div>“当获知到 Leader LEO=2 后，B 发现该 LEO值不比它自己的 LEO 值小，而且缓存中也没有保存任何起始位移值 &gt; 2 的 Epoch 条目”是什么意思？
如果follower B重启回来之后去取Leader A的LEO，但是此时Leader A已经挂了，这套机制不就玩不转了吗？</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（4） 💬（4）<div>1.该远程 Follower 副本在 ISR 中。

如果 Kafka 只判断第 1 个条件的话，就可能出现某些副本具备了“进入 ISR”的资格，但却尚未进入到 ISR 中的情况。

————————
这里是不是把条件的编号写反了？
</div>2019-08-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo7R9LibMTe6CF9sVIcZUee5xCVEAxiava7CUb37V3ic6eFYuWBgFelDqeA0wekG2ibA3HFic94PYJHWlA/132" width="30px"><span>山里小龙</span> 👍（3） 💬（1）<div>”当它重启回来后，副本 B 会执行日志截断操作，将 LEO 值调整为之前的高水位值，也就是 1。这就是说，位移值为 1 的那条消息被副本 B 从磁盘中删除，此时副本 B 的底层磁盘文件中只保存有 1 条消息，即位移值为 0 的那条消息。”
这里有点不明白，主从的高水位都是1了，说明数据1已经成功同步了，为什么要把1给截断删除呢？follower重启只需要把leo值设置为1就行了，hw不用动了吧！</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/41/ad/4ccf4238.jpg" width="30px"><span>店小二#2</span> 👍（3） 💬（1）<div>引用一下@thomas与老师交流。

thomas
iii. 更新 currentHW = max{currentHW, min（LEO-1, LEO-2, ……，LEO-n）}
-------------------------------------------------------------------------------&lt;
老师， LEO-1,LEO-2...LEO-n 都是在ISR集合中的，我认为 currentHW= min（LEO-1, LEO-2, ……，LEO-n就可以，请问在什么场景下currentHW 会大于 min(LEO-1, LEO-2, ……，LEO-n）
作者回复: 有些落后很多的follower可能出现这种情况

====================================================
老师的解答的场景我理解了。但是不明白的是，该场景下，恢复过来的follower副本replica.lag.time.max.ms &lt; 10s，且还未到ISR中时，此时的分区高水位不是也大于LEO了么？
</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（3） 💬（3）<div>我还奇怪为什么老师讲的和Apache kafka实战这部分内容差不多，还以为是抄袭，后来一看，原来老师就是我看的这本书的作者，😂</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（3） 💬（2）<div>原文中“如果 Kafka 只判断第 1 个条件的话”--这里应该是：第2个条件？评论区其他人也有提到
对这块的个人理解：
两个条件之间的关系是与不是或
这里想表达的应该是--这个即将进入isr的副本的LEO值比分区高水位小，但满足条件2；
文中对条件2的描述好像有点歧义，以下是网上找的一段：
假设replica.lag.max.messages设置为4，表明只要follower落后leader不超过3，就不会从同步副本列表中移除。replica.lag.time.max设置为500 ms，表明只要follower向leader发送请求时间间隔不超过500 ms，就不会被标记为死亡,也不会从同步副本列中移除。 </div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/3e/8a813e51.jpg" width="30px"><span>被歌唱拯救中</span> 👍（2） 💬（3）<div>“引用 Leader Epoch 机制后，Follower 副本 B 重启回来后，需要向 A 发送一个特殊的请求去获取 Leader 的 LEO 值。”
假如这个时候，副本A所在broker宕机怎么做呢？</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（1）<div>老师好，有个问题请教一下：
日志段文件在删除时，先被标记为deleted，然后延迟默认1分钟后删除，如果此时我的客户端要访问这个日志文件，那么这个被标记为deleted的日志文件还会被删除吗？物理文件和内存中的文件分别是怎样的？也就是说会不会导致openfiles由于客户端的访问而不被释放掉？</div>2020-07-06</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz3icr3mGs5ib8FbSPQZ2ic3ib90mHkd1btQrmGacZjJxfYXrerIdaTxglKyCicFzLcEAb6deC2cWjE5Q/132" width="30px"><span>the geek</span> 👍（2） 💬（1）<div>看这篇文章的时候一直有个疑惑，follower的HW究竟有什么作用？
是版本的遗留吗？原来的追随者HW是用来截断日志的。现在有了Leader Epoch后，其实完全没必要在follower上保存HW。可以这样理解吗？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/5e/b8fada94.jpg" width="30px"><span>Ryoma</span> 👍（2） 💬（1）<div>1、Leader 副本处理生产者请求时，为什么会更新分区高水位值？理论上这个时候没有必要更新高水位吧（因为领导者的 Leo 是最大的，取 Min 值 HW 不会变化）？除非副本只有1个，那这种应该按特例分析吧，因为也不会有 follow 副本的存在了；
2、既然不更新远程副本中 HW 值，那为什么还会存储在那呢？岂不是很浪费空间
3、Leader Epoch 是存储在哪的呢？如何保证某个 Broker 挂了之后还能正常处理，是 ZK 么？</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/db/51457469.jpg" width="30px"><span>Keep</span> 👍（2） 💬（1）<div>文中说: 分区高水位值就可能超过 ISR 中副本 LEO，而高水位 &gt; LEO 的情形是不被允许的。这段话是不是有误？因为在生产者设置acks=1时，只要leader副本写入磁盘就算提交，不用等follower同步消息。是有可能存在分区高水位&gt;ISR中的LEO的吧</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/18/b9/d74477d1.jpg" width="30px"><span>Flee</span> 👍（1） 💬（1）<div>针对“每次有 Leader 变更时，新的 Leader 副本会查询这部分缓存，取出对应的 Leader Epoch 的起始位移，以避免数据丢失和不一致的情况。”
如果原始 Leader 已经挂了, 那么如何拿到这个 Leader Epoch 信息呢？</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（1） 💬（1）<div>老师，在启用了Leader Epoch机制后，Follower副本B重启回来后，是如何知道Leader得LEO值?这也是Leader Epoch 机制里面得吗？</div>2020-08-25</li><br/><li><img src="" width="30px"><span>Vector</span> 👍（1） 💬（1）<div>副本同步机制解析开头的例子并不能说明“Leader 副本高水位更新和 Follower 副本高水位更新在时间上是存在错配的。”吧，因为两者都是在同一次FETCH请求内更新的，如果说在时间上存在错配的话，也应该是FETCH请求在leader副本处理成功，但follower副本所在broker宕机未能处理。但感觉这里表述的不太明确，不知道老是说的时间错配指的是不是在min.insync.replicas=1的情况下发生的。</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（1） 💬（1）<div>在isr同步后就是已提交的消息，isr未同步就是未提交的消息。也就是说必须满足2个条件的原因，让高水位一定小于LEO。也就是使用默认的acks可能丢失数据的原因。这里理解对不对？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/41/ad/4ccf4238.jpg" width="30px"><span>店小二#2</span> 👍（1） 💬（1）<div>iii. 更新 currentHW = max{currentHW, min（LEO-1, LEO-2, ……，LEO-n）}，是修改后的。那么表格中leader副本高水位更新时机的算法描述也需要改为max{HW,min(LEO-1……LEO-N)}吧？</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/e2/28aa8e6c.jpg" width="30px"><span>会玩code</span> 👍（1） 💬（1）<div>老师，有个疑问想请教下，假如有3个副本，leader发生异常后，较为落后的那个副本当选了新的leader，这时候获取epoch的时候发现offset比新leader的leo还高，那这种情况是怎么处理之后的写入呢？</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（2）<div>iii. 更新 currentHW = max{currentHW, min（LEO-1, LEO-2, ……，LEO-n）}
-------------------------------------------------------------------------------&gt;
老师， LEO-1,LEO-2...LEO-n 都是在ISR集合中的，我认为 currentHW= min（LEO-1, LEO-2, ……，LEO-n就可以，请问在什么场景下currentHW 会大于 min(LEO-1, LEO-2, ……，LEO-n）</div>2020-05-20</li><br/><li><img src="" width="30px"><span>Cv</span> 👍（1） 💬（1）<div>看到文中一直说是所有远程副本, 是指保持同步的follower的,还是包括不满足同步2个条件的不同步的也算?
如果不同步的也算的话, 那么有一个follower同步的很慢, 不就拖累了整个集群吗?
还要一个问题, 提交成功=可以被消费=高水位, 提交成功之前的章节是可以配置几个副本同步完成就算提交成功的, 但是高水位计算时又是所有副本, 这里是不是矛盾了呢?</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（1） 💬（1）<div>请问老师：副本B重启的时候，为什么副本A的图片里有个红色的叉？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（1） 💬（1）<div>“当获知到 Leader LEO=2 后，B 发现该 LEO值不比它自己的 LEO 值小，而且缓存中也没有保存任何起始位移值 &gt; 2 的 Epoch 条目”是什么意思？

老师，leo值不比自己leo知道说明意思，但是后面epoch这句话不理解，如果起始值大于2意味着什么呢？
如果大于2，不是应该说follower当前的日志更老吗，更不应该截断日志。麻烦解答下，谢谢，很疑惑
</div>2019-08-03</li><br/>
</ul>