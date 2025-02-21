你好，我是胡夕。今天我要和你分享的主题是：Apache Kafka的副本机制。

所谓的副本机制（Replication），也可以称之为备份机制，通常是指分布式系统在多台网络互联的机器上保存有相同的数据拷贝。副本机制有什么好处呢？

1. **提供数据冗余**。即使系统部分组件失效，系统依然能够继续运转，因而增加了整体可用性以及数据持久性。
2. **提供高伸缩性**。支持横向扩展，能够通过增加机器的方式来提升读性能，进而提高读操作吞吐量。
3. **改善数据局部性**。允许将数据放入与用户地理位置相近的地方，从而降低系统延时。

这些优点都是在分布式系统教科书中最常被提及的，但是有些遗憾的是，对于Apache Kafka而言，目前只能享受到副本机制带来的第1个好处，也就是提供数据冗余实现高可用性和高持久性。我会在这一讲后面的内容中，详细解释Kafka没能提供第2点和第3点好处的原因。

不过即便如此，副本机制依然是Kafka设计架构的核心所在，它也是Kafka确保系统高可用和消息高持久性的重要基石。

## 副本定义

在讨论具体的副本机制之前，我们先花一点时间明确一下副本的含义。

我们之前谈到过，Kafka是有主题概念的，而每个主题又进一步划分成若干个分区。副本的概念实际上是在分区层级下定义的，每个分区配置有若干个副本。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/a0/cb/aab3b3e7.jpg" width="30px"><span>张三丰</span> 👍（70） 💬（6）<div>replica.lag.time.max.ms，感觉老师对这个参数的解释有歧义。

应该是如果leader发现flower超过这个参数所设置的时间没有向它发起fech请求（也就是复制请求），那么leader考虑将这个flower从ISR移除。
而不是连续落后这么长时间</div>2021-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/70/a874d69c.jpg" width="30px"><span>Mick</span> 👍（35） 💬（8）<div>老师，LEO和HW这两个概念不理解，能不能详细说下，谢谢</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/c9/57d571a3.jpg" width="30px"><span>凯</span> 👍（35） 💬（4）<div>请问一下，producer生产消息ack=all的时候，消息是怎么保证到follower的，因为看到follower是异步拉取数据的，难道是看leader和follower上面的offset吗？</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/76/abb7bfe3.jpg" width="30px"><span>ideal sail</span> 👍（30） 💬（3）<div>老师，假设一个分区有5个副本，Broker的min.insync.replicas设置为2，生产者设置acks=all，这时是有2个副本同步了就可以，还是必须是5个副本都同步，他们是什么关系。</div>2019-12-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLl9nj9b6RydKADq82ZwOad0fQcvXWyQKk5U5RFC2kzHGI4GjIQsIZvHsEm7mFELgMiaGx3lGq9vag/132" width="30px"><span>咸淡一首诗</span> 👍（21） 💬（3）<div>老师，“这个标准就是 Broker 端参数 replica.lag.time.max.ms 参数值。这个参数的含义是 Follower 副本能够落后 Leader 副本的最长时间间隔，当前默认值是 10 秒” 这句话中的最长时间间隔是怎么计算的，以什么时间为基准？</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5f/b2/c4780c10.jpg" width="30px"><span>曹伟雄</span> 👍（18） 💬（2）<div>老师你好，有个问题请教一下，麻烦抽空看看，谢谢。
生产环境，因磁盘满了，所有broker宕机了，重启集群后，主题中的部分分区中，有1个副本被踢出ISR集合，只剩下leader副本了。

试了以下几种方法都没有自动加入进来：
1、等了3天后还是没有加入到ISR；
2、然后重启kafka集群；
3、用kafka-reassign-partitions.sh命令重新分配分区；

针对此情况，请问一下有什么办法让它自动加入进来？  或者手工处理加入进来也可以。
有什么命令可以查看follower落后多少吗？  麻烦老师给点建议或解决思路，谢谢。</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（13） 💬（1）<div>ack=all时候，生产者向leader发送完数据，而副本是异步拉取的，那生产者写入线程要一直阻塞等待吗</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/6e/0a300829.jpg" width="30px"><span>李先生</span> 👍（10） 💬（3）<div>胡哥：分区选举leader，是通过抢占模式来选举的。如果不开启unclean.leader.election.enable，是只能isr集合中的broker才能竞争吗？这个竞争的过程能具体说下是如何实现的吗？</div>2020-04-13</li><br/><li><img src="" width="30px"><span>Cv</span> 👍（9） 💬（2）<div>生产者acks=all使用异步提交, 如果ISR副本迟迟不能完成从leader的同步, 那么10s过后, 生产者会收到提交失败的回调吗? 还是一直不会有回调</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（9） 💬（6）<div>老师好，请问ISR中的副本一定可以保证和leader副本的一致性吗？如果有一种情况是某个ISR中副本与leader副本的lag在ISR判断的边界值，这时如果leader副本挂了的话，还是会有数据丢失是吗？谢谢老师</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/77/ce921ed4.jpg" width="30px"><span>球球</span> 👍（8） 💬（4）<div>胡夕老师好，replica.lag.time.max.ms配置follower是否处于isr中，那么是否存在，在这个时间段内数据写完leader，follower还没有完全同步leader数据，leader宕机，isr中follower提升为新leader，那这一部分数据是否就丢失呢？该如何避免呢？谢谢</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/9c/b457a937.jpg" width="30px"><span>不能扮演天使</span> 👍（6） 💬（1）<div>老师，ack=all,是保证ISR中的follower同步还是所有的follower同步，还有消费者是只能消费到ISR中的HW处的offset么？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/3d/4ac37cc2.jpg" width="30px"><span>外星人</span> 👍（6） 💬（2）<div>请问，关闭unclean后，有哪些方法可以保证available啊？谢谢</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/55/8ac4f169.jpg" width="30px"><span>陈国林</span> 👍（5） 💬（1）<div>老师好，我觉得是否可以这样分场景。对于读新的数据可以从 leader replica 读取，对于老一些的数据从follower replica 读取，这样不懂是否可行</div>2020-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/7b/f720c935.jpg" width="30px"><span>易程</span> 👍（5） 💬（4）<div>老师好，想请教您两个问题，如下：
如果某个follower副本同步持续慢于leader副本写入速度，repkica.lag.time.max.ms 是对于二者的同步时间做的判断，我理解就是如果一直检查10s follower都赶不上leader副本的进度！
但是，这个同步进度是用哪一块进行判别的呢？是通过index值吗？
另外，如果某个follower不在ISR中了，kafka如果维持副本数均衡呢？比如设置了副本数为3，其中一个副本不在ISR集合中了，那么就一直少了一个副本吗？前提是这个副本一直没有跟上leader的同步进度！
谢谢！
</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（4） 💬（1）<div>ack=all时候，生产者向leader发送完数据，而副本是异步拉取的，那生产者写入线程要一直阻塞等待吗
老师这个问题您是说不会阻塞,可以认为是生产会不断地轮询状态
那是否可能存在发送了两条消息,可能导致后发送的先写入分区(设置max.in.flight.requests.per.connection),如果不可能的话,此时生产者是否处于阻塞模式,无法再次发送消息</div>2020-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（4） 💬（1）<div>老师，请问以replica.lag.time.max.ms=10s为副本机制的判断依据，遇到以下场景的话，是如何解决？

比如 Leader-A LEO=1000  Follower-B LEO=800,  他们的差值是200， 那如何判断这200条消息是否会在10s内同步完？</div>2020-04-30</li><br/><li><img src="" width="30px"><span>Cv</span> 👍（4） 💬（1）<div>ISR中的数据也会落后leader, 那么leader挂了之后的重新选举, 一样会造成数据丢失, 为了避免这种请问, 我们是否需要把replica.lag.time.max.ms设置为0呢?</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（3） 💬（1）<div>谢谢老师的讲解！
这里有两个问题想请教一下老师：
1.kafka使用replica.lag.max.time.ms来判断是否保留replica在ISR里，那么问题来了，在吞吐量较高的场景下，replica满足这个时间限制，但是LEO相差比较大，leader这时候挂掉，这个replica被选举为新leader，这个时候是不是有一部分数据丢失了？
2.如果问题1确实存在，目前是怎样处理的呢？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（3） 💬（1）<div>在“无消息丢失配置怎么实现？”中有两个配置项，acks=all这里的all是指所有的isr的副本还是所有的副本,如果是所有的副本，那副本同步都是通过拉取实现的，那这个等待时间就是最慢的那个副本了，也就是消费者端等待时间&gt;replica.lag.time.max.ms；min.insync.replicas这个参数是表示isr的最小副本数？</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（2） 💬（1）<div>1、ack=all时,生产者向leader发送完数据,副本拉取失败,这样生产者持续轮询得到的结果是发送失败吗？如果是的话,生产者重发消息,是不是就可能存在两条一样的消息(就发送的内容而言，不考虑时间戳),还是说kafka内部有机制会把第一条消息删除？
2、原来问过老师一个问题：ack=all时候，生产者向leader发送完数据，而副本是异步拉取的，生产会不断地轮询状态
那是否可能存在发送了两条消息,可能导致后发送的先写入分区(设置max.in.flight.requests.per.connection),您的回答是可能出现乱序
这个我不太理解,第一条消息发送到leader后就已经占用了消息位移,再来一条消息不是会记录在后面吗？麻烦老师解释下,最好可以举例说明下什么场景下会发生乱序  谢谢
</div>2020-11-27</li><br/><li><img src="" width="30px"><span>13761642169</span> 👍（2） 💬（1）<div>配置是 unclean.leader.election.enable=false
1个分区有2个副本，r1 和 r2，isr 中只有 r1，r1 所在机器崩溃后，并且日志数据也丢失了，这种情况怎样操作让分区恢复服务？</div>2019-10-18</li><br/><li><img src="" width="30px"><span>giantbroom</span> 👍（2） 💬（1）<div>请教2个问题：
1. 之前介绍过副本的ack设置，0，1和all，以及设置最大写入副本的数量（具体参数名忘了）。这些设置(ack为1或all)跟unclean.leader.election.enable在语义上是不是互斥的？
2. 在设置ack为1或all的情况下，如果发生网络分区，使得ack的条件不满足，kafka会怎么处理？
3. 在默认设置下，kafka是AP还是CP？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/b4/d5d9e4fb.jpg" width="30px"><span>爱学习的小学生</span> 👍（1） 💬（1）<div>老师麻烦问一下，三台kafka分区配置多大比较合适！</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/79/df384bdc.jpg" width="30px"><span>修愿三秋</span> 👍（1） 💬（2）<div>老师你好，acks=all是保证isr列表中的副本同步，如果长时间的大吞吐量，致使isr中只剩下leader，那acks=all实际起到的效果就是只同步leader一个副本，如果此时leader挂掉，那是不是会丢数据？</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/0d/fb77a32c.jpg" width="30px"><span>Tim</span> 👍（1） 💬（2）<div>老师好，请教2个问题，感谢老师：
1、它要比较的是Follower 副本落后 Leader 副本的时间是否超过10秒，那这个10s这个时间单位和LEO&#47;HW这种度量单位是如何比较的呢？
2、老师，follow副本是何时fetch一次leader的呢，多久fetch一次呢？有配置么？</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/cf/ec335526.jpg" width="30px"><span>jc9090kkk</span> 👍（1） 💬（1）<div>感谢老师的分享，对于这一章节的内容有两个疑问，希望老师能抽时间回复下：
1.follower落后leader超过特定的时间，也就是超过replica.lag.time.max.ms的值，就会被踢出isr集合，那么这个时间差是如何算出来的，是通过LEO和HW计算出来的么？具体的计算细节能否简单介绍下？如果是落后特定的某个数据量阈值很容易理解，但是换成落后多少秒让我有点难以理解？
2.ISR集合是动态的，如果后面发现被踢出的follower又追上leader，还会重新回归到ISR集合，这个里面有个矛盾的点，把落后的follower踢出去后，我个人的理解，这个follower不就变成僵尸副本了吗？因为它不是任何一个leader的follower了呀，哪里还有机会继续从leader那同步数据，然后再重新回归到ISR集合中去呢？麻烦老师解答下，谢谢</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/5d/ac666969.jpg" width="30px"><span>miwucc</span> 👍（1） 💬（1）<div>ISR中进行选组也可能有10s的消息丢失?</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d1/22/706c492e.jpg" width="30px"><span>Algoric</span> 👍（1） 💬（2）<div>老师，请问下leader副本所在broker挂掉，重新恢复后上线，成为follower，后面会因为与AR中的优先副本的指定不一致，重新被选为leader副本？</div>2019-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUJKviaecwxpAZCAnHWap86kXUichv5JwUoAtrUNy4ugC0kMMmssFDdyayKFgAoA9Z62sqMZaibbvUg/132" width="30px"><span>Geek_edc612</span> 👍（1） 💬（3）<div>kafak不会像hdfs那样自己再找个分区备份损坏磁盘副本吗？</div>2019-08-22</li><br/>
</ul>