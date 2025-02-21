你好，我是吴磊。

好久不见了，距离专栏结束有不少时间了，不过这期间我一直在关注着同学们的留言。今天我就带着你的期待又来了。

在性能调优的本质那一讲（[第2讲](https://time.geekbang.org/column/article/352577)），我们说过性能调优方法论。

其中的第一条，就是根据专家经验或是运行时的诊断，来定位性能瓶颈。作为Spark内置的运行时监控界面，Spark UI是我们必须要掌握的重要工具。而且随着课程的推进，有不少同学在后台反馈，希望我补充Spark UI的课程内容。

鉴于以上两点，我用加餐的形式，把Spark UI的内容补充到课程中，希望对你有所帮助。

在日常的开发工作中，我们总会遇到Spark应用运行失败、或是执行效率未达预期的情况。对于这样的问题，想找到根本原因（Root Cause），就可以通过Spark UI来获取最直接、最直观的线索，在全面地审查Spark应用的同时，迅速定位问题所在。

如果我们把失败的、或是执行低效的Spark应用看作是“病人”的话，那么Spark UI中关于应用的众多度量指标（Metrics），就是这个病人的“体检报告”。结合多样的Metrics，身为“大夫”的开发者即可结合经验来迅速地定位“病灶”。

今天这一讲，让我们以小汽车摇号中“倍率计算”的应用（详细内容你可以回顾[第30讲](https://time.geekbang.org/column/article/374776)）为例，用图解的方式，一步步地去认识Spark UI，看一看它有哪些关键的度量指标，这些指标都是什么含义，又能为开发者提供哪些洞察（Insights）？
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/e7/45d9e964.jpg" width="30px"><span>Hiway</span> 👍（17） 💬（2）<div>第一问：我的理解是RDD Blocks表示的是读入数据集时的分区数，而Complete Tasks则表示整个job完成时该Executor完成的Task数。我觉得原因有二：
一是spark在划分DAG时，遇到shuffle便会断开产生新的Stage，一个task只是对应一个stage里的一个partition。
二是如果未修改spark.sql.shuffle.partitions配置，在join的时候就会自动修改为200的并行度，对应的下一个Stage也就产生了200个task

第二问：从Executors界面看，应该是两个Executor在跑。因为是分布式所以在最后write的时候，两个Executor都进行了save操作。至于为什么是两台Executor跑，应该这样计算出来的：executor 数量 = spark.cores.max&#47;spark.executor.cores

老师，是这样吗？可以发一下你的spark-submit命令嘛?</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/76/3db69173.jpg" width="30px"><span>onepieceJT2018</span> 👍（6） 💬（1）<div>不知道为什么 hive on spark的话 ui里面storage 这个面板是空白</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/8d/c6a2a048.jpg" width="30px"><span>Reiser</span> 👍（5） 💬（1）<div>周末回看之前的文章，看到这篇加餐有点感动。太走心了，磊哥！</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/77/78/e241fe80.jpg" width="30px"><span>LR.яг ®</span> 👍（2） 💬（2）<div>有一个别的组同事，每次启动spark都会把资源申请完，他的部分启动命令如下： --executor-memory 6G --num-executors 2000 --executor-cores 4。导致我每次都要去kill掉他的application。
请问老师，有没有什么方法可以限制启动时不允许申请这么多资源？</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（4）<div>老师我的executors页面为什么rdd blocks都是0？</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9d/6a/9158f399.jpg" width="30px"><span>保护</span> 👍（1） 💬（1）<div>Job Id 为 7存在的原因 是因为保存了文件嘛</div>2021-11-22</li><br/><li><img src="" width="30px"><span>Geek_18fe90</span> 👍（1） 💬（1）<div>解决了我的一块心病</div>2021-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo2GMhevabZrjINs2TKvIeGC7TJkicNlLvqTticuM5KL8ZN80OC2CnrsUyzPcZXO4uptj4Q1S4jT2lQ/132" width="30px"><span>jerry guo</span> 👍（1） 💬（1）<div>spark sql job的Storage页面怎么是空白的呢？是只有运行的时候才有数据吗</div>2021-10-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ia89MwaRSP6iaeQB4789roUntH7tia9EXyoDOnlibE8ABibAzFPiamP0SAU54NNTRiaVtkOtmLaWRH5OXbTOhUZl46scw/132" width="30px"><span>Geek_01fccd</span> 👍（1） 💬（2）<div>多个job公用一个executer，是按照executer纬度，计算的完成的task数吗？</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（0） 💬（1）<div>抢个沙发先🤯🤯🤯</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/36/42/70d01532.jpg" width="30px"><span>苏文进</span> 👍（1） 💬（0）<div>老师好，我用代码算了一下storageMemory和SparkUI上的对不上，我的spark版本是3.0.0：
```
def calculateStorageMemory(
      executorMemory: Long = Runtime.getRuntime.maxMemory
  ): Unit = {
    val systemMemory = executorMemory
    val reservedMemory = 300 * 1024 * 1024
    &#47;&#47; User Memory 用于存储开发者自定义的数据结构，例如 RDD 算子中引用的数组、列表、映射等等。
    val userMemory = (systemMemory - reservedMemory) * 0.4
    &#47;&#47; Storage Memory 用于缓存分布式数据集，比如 RDD Cache、广播变量等等
    val storageMemory = (systemMemory - reservedMemory) * 0.6 * 0.5
    val storageMemoryAsMb = JavaUtils.byteStringAsMb(storageMemory.toLong + &quot;b&quot;)
    println(&quot;actual storageMemory is %d MB&quot;.format(storageMemoryAsMb))
  }

  calculateStorageMemory()
  calculateStorageMemory(1*1024*1024*1024) &#47;&#47; spark.executor.memory默认: 1g
```
打印结果：
actual storageMemory is 1002 MB
actual storageMemory is 217 MB
而SparkUI上显示的是2GiB.
我找了一下答案：
有的对不上是因为开了堆外内存，但是默认情况堆外内存是关闭的，这个原因排除。
有的对不上是SparkUI上字节到GB的换算是用的1000而不是1024，这个bug已经被修复了（https:&#47;&#47;issues.apache.org&#47;jira&#47;browse&#47;SPARK-25696），所以也被排除。
还有的对不上是JVM实际可用内存比spark.executor.memory的值小，而我情况是默认1g，JVM可用的内存是3个多g.
</div>2022-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDgV2qia6eAL7Fb4egX3odViclRRwOlkfCBrjhU9lLeib90KGkIDjdddSibNVs47N90L36Brgnr6ppiag/132" width="30px"><span>ddww</span> 👍（0） 💬（1）<div>想请教一个问题，Executors页面下，Storage Memory 4.3G是怎么算出来的，这个是集群FrameWork Memory的总和吗？如果是的话，我只算出来3.1G。</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/f9/92/f9e3e023.jpg" width="30px"><span>Van</span> 👍（0） 💬（0）<div>好东西</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（0）<div>请问下，spark 有没有类似prometheus metric 监控呢</div>2022-05-04</li><br/>
</ul>