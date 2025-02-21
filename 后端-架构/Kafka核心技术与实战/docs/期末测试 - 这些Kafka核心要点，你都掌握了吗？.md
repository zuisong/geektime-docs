你好，我是胡夕。

《Kafka核心技术与实战》已经结课一段时间了，你掌握得怎么样了呢？我给你准备了一个结课小测试，来帮助你检验自己的学习效果。

这套测试题有选择题和简答题两种形式。选择题共有 20 道题目，考题范围覆盖专栏的 42 讲正文，题目类型为单选题和多选题，满分 100 分，系统自动评分。简答题共有5道，建议你拿出纸笔，写下你的思考和答案，然后再和文末的答案进行对照。

还等什么，点击下面按钮开始测试吧！

[![](https://static001.geekbang.org/resource/image/28/a4/28d1be62669b4f3cc01c36466bf811a4.png?wh=1142%2A201)](http://time.geekbang.org/quiz/intro?act_id=94&exam_id=190)

## 简答题

1. 如果副本长时间不在ISR中，这说明什么？
2. 谈一谈Kafka Producer的acks参数的作用。
3. Kafka中有哪些重要组件?
4. 简单描述一下消费者组（Consumer Group）。
5. Kafka为什么不像Redis和MySQL那样支持读写分离？

## 答案与解析

1.如果副本长时间不在ISR中，这说明什么？

**答案与解析：**

如果副本长时间不在ISR中，这表示Follower副本无法及时跟上Leader副本的进度。通常情况下，你需要查看Follower副本所在的Broker与Leader副本的连接情况以及Follower副本所在Broker上的负载情况。

2.请你谈一谈Kafka Producer的acks参数的作用。

**答案与解析：**
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qsmAdOC3R3twep9xwiboiaNF6u3fk5jNZGibKrBuILKgyNMH0DAQMg3liaWQ7ntVAFGEBCg5uB9y9KdKrhD65TyGgQ/132" width="30px"><span>镜子中间</span> 👍（9） 💬（1）<div>终于看完了Kafka课程，这是我在极客时间学完的第一门课，也是坚持的最久的，期末测试得了80分，仍有进步的空间，感谢胡夕老师，也感谢坚持下来的自己，Mark一下，准备开始二刷了！</div>2020-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/ce/092acd6a.jpg" width="30px"><span>孙同学</span> 👍（3） 💬（3）<div>做完题 85 哈哈 以为自己都忘了。。</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（1） 💬（1）<div>胡老师，学完源码课然后来的实战课，收获很大。有没有好的讲解分布式的资料呢，能够综合一些学习</div>2020-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLRKgow8PPLLgCqt6ZWiaylrFG1ButvHRSqOZ8hvFZFHoUGaoYCLlasbRiaaM0pTWKeeLbW4xBM4vjg/132" width="30px"><span>执芳之手</span> 👍（1） 💬（1）<div>老师，你好。我的服务运行了一段时间，发送消息报错：Cannot perform operation after producer has been closed。网上说是，KafkaProducer 已经close了。但是，我不知道为什么被关闭的。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/cd/09874b2f.jpg" width="30px"><span>Godning</span> 👍（0） 💬（3）<div>老师，我们在对kafka性能测试时遇到了too many files open问题，单节点服务器是256&#47;48t存储 磁盘做了raid0 集群是三台服务器构成 ，我们对单节点进行测试 启用五个topic 都是单分区 ，写入时带宽几乎占满 。当写入数据量到达3.6t时 系统文件句柄数就超过200w了 导致kafka崩溃 这种情况是kafka本身问题还是系统配置问题还是我们使用的问题呢</div>2021-04-28</li><br/><li><img src="" width="30px"><span>墙角儿的花</span> 👍（0） 💬（1）<div>老师，服务部署在阿里云上，生产者发送消息经常在非上班期间发生超时，如晚8点到第二天8点间出现发送超时(org.apache.kafka.common.errors.TimeoutException)，而且根本就没什么qps，一分钟内都是个位数，白天时有一定的qps，但却不会出现超时，阿里云说网络没问题，请问该如何排查呢，谢谢</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/e9/377a3b09.jpg" width="30px"><span>H.L.</span> 👍（0） 💬（1）<div>kafka集群扩容， reassign主题分区迁移，这个不讲了吗？</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/74/85/9443a0a9.jpg" width="30px"><span>旭旭</span> 👍（0） 💬（1）<div>完整的看了你的这门课 实在不错 有种相见恨晚的感觉 希望老师多推出一些大数据相关的优秀课程！</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/06/66831563.jpg" width="30px"><span>阡陌</span> 👍（0） 💬（3）<div>嗯，很多收货。但是也有很多没理解透彻的，准备从头再来一遍，加深理解和记忆。</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/11/ba/2175bc50.jpg" width="30px"><span>Mr.Brooks</span> 👍（0） 💬（1）<div>虽然工作中从没用过kafka，依然学到很多。准备去追老师下一个源码课了</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/22/26530e66.jpg" width="30px"><span>趁早</span> 👍（0） 💬（1）<div>终于看完了，收货颇多，感谢胡总的辛苦付出</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（0） 💬（1）<div>谢谢老师！
</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f7/51/1bacf04f.jpg" width="30px"><span>Tc</span> 👍（0） 💬（1）<div>老师的解读源码什么时候上</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/57/1b/37a93b76.jpg" width="30px"><span>剑锋所指</span> 👍（2） 💬（0）<div>学完打卡 90分</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（1） 💬（0）<div>补充一下
如果你的Partition只有一个副本，也就是一个Leader，任何Follower都没有，你认为acks=all有用吗？
当然没用了，因为ISR里就一个Leader，他接收完消息后宕机，也会导致数据丢失。
所以说，这个acks=all，必须跟ISR列表里至少有2个以上的副本配合使用，起码是有一个Leader和一个Follower才可以。
这样才能保证说写一条数据过去，一定是2个以上的副本都收到了才算是成功，此时任何一个副本宕机，不会导致数据丢失。</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/09/b7f0eac6.jpg" width="30px"><span>谁都会变</span> 👍（0） 💬（0）<div>kafka不同读写分离，互相主副本野是一个原因吧。它的读写压力本身就是分散的。</div>2023-03-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnv4h4j5tWywnuIKJHXwhkXImSCMsx1CDD2dmoNUjOBACyicHZvuNN125wnDYgnSLyboIfCytEzRw/132" width="30px"><span>杨栋</span> 👍（0） 💬（0）<div>为什么我学完了进度还是显示97% </div>2022-08-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnv4h4j5tWywnuIKJHXwhkXImSCMsx1CDD2dmoNUjOBACyicHZvuNN125wnDYgnSLyboIfCytEzRw/132" width="30px"><span>杨栋</span> 👍（0） 💬（0）<div>很有深度 </div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>选择题90分</div>2021-08-14</li><br/>
</ul>