你好，我是吴磊。

在数据源与数据格式，以及数据转换那两讲（第15、16讲），我们介绍了在Spark SQL之上做数据分析应用开发的一般步骤。

这里我们简单回顾一下：首先，我们通过SparkSession read API从分布式文件系统创建DataFrame。然后，通过创建临时表并使用SQL语句，或是直接使用DataFrame API，来进行各式各样的数据转换、过滤、聚合等操作。最后，我们再用SparkSession的write API把计算结果写回分布式文件系统。

实际上，直接与文件系统交互，仅仅是Spark SQL数据应用的常见场景之一。Spark SQL另一类非常典型的场景是与Hive做集成、构建分布式数据仓库。我们知道，数据仓库指的是一类带有主题、聚合层次较高的数据集合，它的承载形式，往往是一系列Schema经过精心设计的数据表。在数据分析这类场景中，数据仓库的应用非常普遍。

在Hive与Spark这对“万金油”组合中，Hive擅长元数据管理，而Spark的专长是高效的分布式计算，二者的结合可谓是“强强联合”。今天这一讲，我们就来聊一聊Spark与Hive集成的两类方式，一类是从Spark的视角出发，我们称之为Spark with Hive；而另一类，则是从Hive的视角出发，业界的通俗说法是：Hive on Spark。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/57/61/369a609c.jpg" width="30px"><span>A</span> 👍（7） 💬（2）<div>不过，相比前者，spark-sql CLI 的集成方式多了一层限制，那就是在部署上，spark-sql CLI 与 Hive Metastore 必须安装在同一个计算节点。换句话说，spark-sql CLI 只能在本地访问 Hive Metastore，而没有办法通过远程的方式来做到这一点。   ---------我试了试是可以的老师，是我对这句话理解有误嘛？三台机器 01、02、03；01、02启动hive metastore，然后在03上启动spark-sql spark:&#47;&#47;bdp-dc-003:7077  同样是可以使用hive的metastore</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（1）<div>老师问下 Beeline + Spark Thrift Server 这种部署方式应该怎么配置spark参数呢？我看我们公司的文件是在hivesql里带上类似 set hive.exec.parallel=true; 这种参数，这和用dataframe api设置参数不太一样啊。。如果在 hive sql里配置的话它的参数和spark的参数的对应关系是怎样的呢？谢谢老师~</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>问题一的执行路径是不是还是先建立dataframe，然后根据sql逻辑完成计算，最后存到hive？虽然是hive on spark但是我理解这种情况下应该没有用到hive的优化引擎吧</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/9a/e1/0867c16b.jpg" width="30px"><span>HHB</span> 👍（0） 💬（1）<div>老师请问，Hive with Spark的方式比直接使用spark sql的性能高吗？</div>2021-11-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（3）<div>老师，我把hive引擎换成spark后，一直出现这个错误，我看了 资源充足呀，您看一下，是什么原因呢

hive (test)&gt; select count(*) from spark_hive group by id;
Query ID = root_20211031144450_fc398bef-8f94-4a07-a678-cdeef464b128
Total jobs = 1
Launching Job 1 out of 1
In order to change the average load for a reducer (in bytes):
  set hive.exec.reducers.bytes.per.reducer=&lt;number&gt;
In order to limit the maximum number of reducers:
  set hive.exec.reducers.max=&lt;number&gt;
In order to set a constant number of reducers:
  set mapreduce.job.reduces=&lt;number&gt;
Starting Spark Job = 75d07aa7-a98f-43b5-8fe5-de4158f454a7
Job hasn&#39;t been submitted after 61s. Aborting it.
Possible reasons include network issues, errors in remote driver or the cluster has no available resources, etc.
Please check YARN or Spark driver&#39;s logs for further information.
Status: SENT
Failed to execute spark task, with exception &#39;java.lang.IllegalStateException(RPC channel is closed.)&#39;
FAILED: Execution Error, return code 1 from org.apache.hadoop.hive.ql.exec.spark.SparkTask. RPC channel is closed.
</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（2）<div>理论上应该可以把HQL转换成Spark SQL吧，那样Hive on Spark是不是性能就会提升了？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/a8/6853ca39.jpg" width="30px"><span>gouge</span> 👍（0） 💬（4）<div>老师，请问为什么会有这个限制？“spark-sql CLI 的集成方式多了一层限制，那就是在部署上，spark-sql CLI 与 Hive Metastore 必须安装在同一个计算节点”。

我实验好像没有发现存在这个“限制”。如下：

我在本地配置 %SPARK_HOME%&#47;conf&#47;hive-site.xml，内容如下：
&lt;configuration&gt;
&lt;property&gt;
  &lt;name&gt;hive.metastore.uris&lt;&#47;name&gt;
  &lt;value&gt;thrift:&#47;&#47;xxx:9083&lt;&#47;value&gt;  
&lt;&#47;property&gt;
&lt;&#47;configuration&gt;

其中xxx:9083为远程服务器上部署的hive metastore。通过这样的配置，再执行%SPARK_HOME%&#47;bin&#47;spark-sql，是可以查询到hive的元数据信息的。

谢谢！

</div>2021-10-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5dE76DFqQlkTdseGfAKdcb7XSpS8eOlJ5W0g5jJxWe8EoBb5Yz4JGZU6zPFosonSibudko7yDgfiaw/132" width="30px"><span>Geek_e2be2a</span> 👍（5） 💬（0）<div>官方的Spark Thriftserver功能比较弱，可以试一下Apache Kyuubi</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/99/4bdadfd3.jpg" width="30px"><span>Chloe</span> 👍（0） 💬（0）<div>请问可以简单讲一下hive和iceberg的区别吗？两者和Spark的结合，各有什么应用场景呢？谢谢！</div>2024-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b2/9c/b7b9896c.jpg" width="30px"><span>王云峰</span> 👍（0） 💬（0）<div>HBase是按照列族聚集的还是按照列聚集的？就是磁盘上顺序扫是只扫某一列还是会列族所有列一起扫？</div>2023-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（0） 💬（0）<div>Spark是计算引擎，而Hive是开发侧实现业务逻辑的入口
Hive的设计优势在于兼容，不同于以往的pig，他只需要写sql
同时也能优化计算逻辑，最终将计算过程放在map—reduce上</div>2022-11-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/zWLzhGrHubcMJnNFz0s0akeMpefNBVy2jic3rxetxHIjy1icPjJBXFQc78AW10icVN47BLrWicHcSm9MOfG38J2kKw/132" width="30px"><span>Geek_278a2c</span> 👍（0） 💬（0）<div>1，请问可以通过hive sql create table并插入数据，然后通过spark sql访问吗？（配置同一个hive metastore）
2，类似的，请问可以通过hive sql create udf，然后通过spark sql使用udf吗？
</div>2022-03-15</li><br/>
</ul>