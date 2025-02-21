你好，我是吴磊。

在数据分析领域，大表Join小表的场景非常普遍。不过，大小是个相对的概念，通常来说，大表与小表尺寸相差3倍以上，我们就将其归类为“大表Join小表”的计算场景。因此，大表Join小表，仅仅意味着参与关联的两张表尺寸悬殊。

对于大表Join小表这种场景，我们应该优先考虑BHJ，它是Spark支持的5种Join策略中执行效率最高的。**BHJ处理大表Join小表时的前提条件是，广播变量能够容纳小表的全量数据。**但是，如果小表的数据量超过广播阈值，我们又该怎么办呢？

今天这一讲，我们就结合3个真实的业务案例，来聊一聊这种情况的解决办法。虽然这3个案例不可能覆盖“大表Join小表”场景中的所有情况，但是，分析并汇总案例的应对策略和解决办法，有利于我们在调优的过程中开阔思路、发散思维，从而避免陷入“面对问题无所适从”的窘境。

## 案例1：Join Key远大于Payload

在第一个案例中，大表100GB、小表10GB，它们全都远超广播变量阈值（默认10MB）。因为小表的尺寸已经超过8GB，在大于8GB的数据集上创建广播变量，Spark会直接抛出异常，中断任务执行，所以Spark是没有办法应用BHJ机制的。那我们该怎么办呢？先别急，我们来看看这个案例的业务需求。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（12） 💬（5）<div>问题回答
1.给join keys每个字段维护一个字典，每个字段值在字典内对应一个唯一的整数。拿到每个字段指定的种整数，然后组装起来，作为新的join key。
 2.把维度表查询sql单独拿出来，缓存其df，查看其屋里计划，可以知道它结果集大小。
3.参考AQE的自动倾斜处理特性，把数据倾斜的分区拆分开，然后再进行SHJ</div>2021-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（4） 💬（2）<div>问题回答。

第一题：
对每个字段的值生成一个独热编码，以字典来维护，然后再组合各个字段的独热编码，形成一个新的join key。当然这里不一定用独热编码，也能用二进制编码，如果想更加节省空间更加折腾，可以使用 哈夫曼编码，哈夫曼编码 从本质上讲，是将最宝贵的资源（最短的编码）给出现概率最大的信息。

第二题：
先 Cache，再查看执行计划，有示例代码，在第17篇内存视角（三）：OMM都是谁的锅？怎么破？

第三题：
AQE的自动倾斜处理，在 Reduce 阶段，当 Reduce Task 所需处理的分区尺寸大于一定阈值时，利用 OptimizeSkewedJoin 策略，AQE 会把大分区拆成多个小分区。（阀值可自行设置的）</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（2） 💬（1）<div>老师，SHJ 要求小表数据均匀，防止某一分区OOM，是因为小表hash 后，会把相同的key, reduce到一个分区吗？那么这样SMJ 同样也会在shuffle 后有oom 的风险呀？</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d6/66/62206d01.jpg" width="30px"><span>超级丹</span> 👍（2） 💬（3）<div>老师，我有个疑问，dpp，不会导致inode过高吗？ 特别是在用户上做分区这种。。。</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（1） 💬（1）<div>第一题首先打开aqe，对基表df.dropDupilcates(***).withColumn(&quot;code&quot;, monotonically_increasing_id())，这样就完成全局编码了。然后驱动表和基表都join上这个字典表，将组合join keys转换为字典值</div>2021-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a1/2d/599e9051.jpg" width="30px"><span>CycleGAN</span> 👍（1） 💬（1）<div>我们生产端用的2.4也没有AQE机制，但是我觉得减小维度表的大小也能模拟出来，要在维度表上做设计，最有效的还是分区做好，比如我们按时间分区，每个分区的数据局小很多，然后摘出来需要的列，列上的长str做编码，再反映射，列上的长join key做编码等。感觉把维表做小还是值得的，性价比很高。
然后分析大小的话，一是看cache后看大小，主要还是ui页面里的sql计划里看是不是Broadcast，倒是也不需要非常精准。
</div>2021-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/26/db/27724a6f.jpg" width="30px"><span>辰</span> 👍（1） 💬（1）<div>老师，这些都是基于spark3.0的新特性，那对于3.0之前的版本又该怎么解决呢，毕竟3.0版本是新出的，对于大多数公司不一定使用了该版本</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（1） 💬（2）<div>老师我想请问下，在第二个案例中，如果我将 join 条件写成 on orders.userId = users.id and users.type = ‘Head User’  ，是否能实现维度表提前过滤并达到 Broadcast 的要求？</div>2021-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师您好 您在评论 @陈威洋 对问题3的回答时说 &quot;AQE是需要Shuffle才能生效的，因此，要想利用AQE消除数据倾斜，得先对小表做repartition才行&quot;，但是问题3的背景已经是小表尺寸大于广播阈值 因此必须走shuffle了呀，那AQE在这个shuffle的map文件输出之后进行分区倾斜处理不就可以了吗？为什么要额外对小表进行一次 repartition 呢？谢谢老师~</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（0） 💬（1）<div>老师，对于哈希处理join keys或许要考虑基表的列数量和每列数据类型，因为毕竟两个哈希函数计算出来的结果再拼接，长度不下于32甚至大于64。假如原始列内容大部分都是英文和数字，而且大小或长度都不厉害，哈希处理后存储开销会不会更加大了呢？最后有一个问题需要确认下，在tungsten的数据结构里，一个整形数据，是否用到了32bit的存储空间呢？一个utf-8编码的中文是否占用2-4个字节？</div>2021-08-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/z2z2OI0z9rbCngwkzrnP8mmUOXqDjS5I2u4ibfbb2eyvLicFwiclymCYFduU7gtksO6aAvSkbkfEhqCM4fXXQwCsg/132" width="30px"><span>siys</span> 👍（0） 💬（2）<div>案例2中orders_new如果采用分区加分桶的方式能够触发DPP吗，采用userid分的太细了</div>2021-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/8d/27db1e0f.jpg" width="30px"><span>姚先生</span> 👍（0） 💬（1）<div>个人感觉，案例2的解决方案略显牵强。不知道是不是想错了，分享一下。orders表的分区键改为userId，hdfs文件会有count(distinct userId)个文件夹，可能的问题：1.小文件过多造成扫描文件的task数目过多进而增大调度开销;2.hdfs namenode负载问题</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/44/23/8f5d80ad.jpg" width="30px"><span>林红波 :)</span> 👍（1） 💬（0）<div>老师，第二个案例不是通过谓词下推，维表的数据量已经降下来了吗？为什么还要开启AQE？AQE不是通过判断shuffle map输出的中间文件来执行的吗？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/20/c9058450.jpg" width="30px"><span>DarrenChan陈驰</span> 👍（0） 💬（0）<div>老师，我还是觉得第二个例子有点问题，这个明显是可以通过谓词下推来缩减数据量的，谓词下推在逻辑执行计划阶段，join策略选择在物理执行计划阶段，肯定是获取谓词下推以后的结果。我理解AQE适用于比如多join或者子查询这种没办法直接估计数据大小的场景，一个简单的where为啥不能谓词下推呢？</div>2024-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/20/c9058450.jpg" width="30px"><span>DarrenChan陈驰</span> 👍（0） 💬（0）<div>第三个例子，添加Join hints之后的查询语句，是不是写错了？应该&#47;*+ shuffle_hash(users) *&#47;才对吧，users是小表</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2d/aa/e33e9edd.jpg" width="30px"><span>陌生的心酸</span> 👍（0） 💬（0）<div>有个疑问，对于方案二，如果维表【用户表】本身userID超大，还用来建分区表，这个是不是会导致hdfs namenode负载过重，甚至导致超过hive限制的分区数量，创建失败？</div>2022-03-12</li><br/>
</ul>