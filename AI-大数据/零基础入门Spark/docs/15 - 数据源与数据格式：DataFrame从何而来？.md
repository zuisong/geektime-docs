你好，我是吴磊。

在上一讲，我们重点讲解了DataFrame与Spark SQL的渊源，并提到，DataFrame是Spark SQL的重要入口。换句话说，通过创建DataFrame并沿用DataFrame开发API，我们才能充分利用Spark SQL优化引擎提供种种“性能红利”。显然，对于初学者来说，第一步的创建DataFrame就变得至关重要。

之前 [第13讲](https://time.geekbang.org/column/article/424550)，我们做小汽车摇号倍率分析时，用了SparkSession的read API从Parquet文件创建DataFrame，其实创建DataFrame的方法还有很多。毫不夸张地说，DataFrame的创建途径异常丰富，为什么这么说呢？

如下图所示，Spark支持多种数据源，按照数据来源进行划分，这些数据源可以分为如下几个大类：Driver端自定义的数据结构、（分布式）文件系统、关系型数据库RDBMS、关系型数据仓库、NoSQL数据库，以及其他的计算引擎。

![图片](https://static001.geekbang.org/resource/image/f9/f6/f99dae173ba0268a8bd486ab200ecdf6.jpg?wh=1920x696 "Spark支持的数据源")

显然，要深入地介绍Spark与每一种数据源的集成并不现实，也没必要，咱们只需要把注意力放在那些最常用、最常见的集成方式即可。

这一讲，我会从Driver、文件系统与RDBMS三个方面，为你讲解5种常见的DataFrame创建方式，然后带你了解不同方式的使用场景跟优劣分析。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/65/4c/f7f86496.jpg" width="30px"><span>welldo</span> 👍（3） 💬（1）<div>老师,
对于 max=“male”同时 min=“male”的 gender 文件来说
这句话没有读懂,求解释.</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（3） 💬（1）<div>Python 代码：
# 下面是我在notebook上运行的，可以得到结果，拿出来分享

from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
sc = SparkContext()
spark = SparkSession(sc)

seq=[(&#39;Bob&#39;,14),(&#39;Alice&#39;,18)]
rdd=sc.parallelize(seq)
column = [&#39;name&#39;,&#39;age&#39;]
dataframe=spark.createDataFrame(seq,column)


seq=[(&#39;Bob&#39;,14),(&#39;Alice&#39;,18)]
rdd=sc.parallelize(seq)
column = [&#39;name&#39;,&#39;age&#39;]
df2=rdd.toDF(column)  

csvFilePath=&#39;file:&#47;&#47;&#47;home&#47;ray&#47;DataSet&#47;learn-spark&#47;chapter15&#47;info.txt&#39;
df=spark.read.format(&#39;csv&#39;).option(&#39;header&#39;,True).load(csvFilePath)

from pyspark.sql.types import (StringType,StructField,StringType,IntegerType)
schema = StructType([
    StructField(&quot;name&quot;, StringType(), True),
    StructField(&quot;age&quot;, IntegerType(), True),
])

df2=spark.read.format(&#39;csv&#39;).option(&#39;header&#39;,True).load(csvFilePath)

df3=spark.read.format(&#39;csv&#39;).schema(schema).option(&#39;header&#39;,True).option(&#39;mode&#39;,&#39;dropMalformed&#39;).load(csvFilePath)

parquetFilePath=&#39;file:&#47;&#47;&#47;home&#47;RawData&#47;lucky&#47;batchNum=201705&#47;part-00000-a4ecpy.parquet&#39;
df1=spark.read.format(&#39;parquet&#39;).load(parquetFilePath)
# or
df2=spark.read.parquet(parquetFilePath)

from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
sc = SparkContext()
spark = SparkSession(sc)

df=spark.read.format(&quot;jdbc&quot;).option(&quot;driver&quot;, &quot;com.mysql.cj.jdbc.Driver&quot;).option(&quot;url&quot;, &quot;jdbc:mysql:&#47;&#47;localhost:3306&#47;DBName&quot;).option(&quot;user&quot;, &quot;username&quot;).option(&quot;password&quot;,&quot;password&quot;).option(&quot;numPartitions&quot;, 20).option(&quot;dbtable&quot;, &quot;tableName&quot;).load()

sqlQuery=&#39;(select * from django_content_type where app_label = &quot;auth&quot;)T&#39;
df2=spark.read.format(&quot;jdbc&quot;).option(&quot;driver&quot;, &quot;com.mysql.cj.jdbc.Driver&quot;).option(&quot;url&quot;, &quot;jdbc:mysql:&#47;&#47;localhost:3306&#47;DBName&quot;).option(&quot;user&quot;, &quot;username&quot;).option(&quot;password&quot;,&quot;password&quot;).option(&quot;numPartitions&quot;, 20).option(&quot;dbtable&quot;, sqlQuery).load()</div>2021-10-23</li><br/><li><img src="" width="30px"><span>姚礼垚</span> 👍（2） 💬（1）<div>老师，RDD[Row]怎么理解，和RDD[String]这些有啥区别呢</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（1） 💬（1）<div>老师，感觉最近更新的Spark SQL没有Spark core有深度了？是我直觉性错误，还是我没有get到老师聊的点呢</div>2021-10-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/H8NxrljQXlibw5tznwNYgqp9WSJicDIB8Bn9MygzFD0jn6ycBfkPDnDEcoEbuh2C3N6fCSAlvWV9wuA5KFa5yMuQ/132" width="30px"><span>Geek_f09d5e</span> 👍（0） 💬（1）<div>发现小失误，CSV文件分隔列数据的分隔符不是“seq”，是“sep”</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（0） 💬（1）<div>老师,我连接oracle时dbtable选项指定表名成功了,指定的是个sqlquery报错:表名无效</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7d/57/c94b6a93.jpg" width="30px"><span>王璀璨</span> 👍（0） 💬（1）<div>老师 sql语句查询后面默认加where 1=0的报错:
java.sql.SQLSyntaxErrorException: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;select * from HaoDF_article limit 2000 WHERE 1=0&#39; at line 1</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7d/57/c94b6a93.jpg" width="30px"><span>王璀璨</span> 👍（0） 💬（3）<div>老师，sql语句后面默认加where 1=0的报错
java.sql.SQLSyntaxErrorException: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near &#39;select * from HaoDF_article limit 2000 WHERE 1=0&#39; at line 1</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7d/57/c94b6a93.jpg" width="30px"><span>王璀璨</span> 👍（0） 💬（1）<div>老师请问一下spark.default.parallelism和numPartitions分别是什么意思，我看都有分块的意思，但是不懂其中的原理。</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ba/c6/10448065.jpg" width="30px"><span>东围居士</span> 👍（0） 💬（1）<div>我在 spark-shell 中使用 failFast 模式的时候，并不会在 load 语句处出错，而是在执行 df.show 的时候才会报错</div>2021-10-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（0） 💬（1）<div>老师，我在用spark sql 读取mysql数据的时候，会在sql后默认加 where 1=0语句，导致程序报错，这个怎么解决呢？</div>2021-10-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIQpPwtelwwDve2HDXszyDMR4e9iaw9mVJ1EdQy6WQO9pQibZ43TO7KE6wdo5n6lMXNRxqLRAjgP1Ng/132" width="30px"><span>czuo03</span> 👍（0） 💬（1）<div>permissive会将six替换为null
val df: DataFrame = spark.read.format(&quot;csv&quot;).schema(schema).option(&quot;header&quot;, true).option(&quot;mode&quot;, &quot;permissive&quot;).load(csvFilePath)
+------+----+
|  name| age|
+------+----+
| alice|  18|
|   bob|  14|
|cassie|null|
+------+----+

dropMalFormed跳过cassie, six这条记录
val df: DataFrame = spark.read.format(&quot;csv&quot;).schema(schema).option(&quot;header&quot;, true).option(&quot;mode&quot;, &quot;dropMalFormed&quot;).load(csvFilePath)
+-----+---+
| name|age|
+-----+---+
|alice| 18|
|  bob| 14|
+-----+---+

failFast无法生成DataFrame并提示SparkException
val df: DataFrame = spark.read.format(&quot;csv&quot;).schema(schema).option(&quot;header&quot;, true).option(&quot;mode&quot;, &quot;failFast&quot;).load(csvFilePath)
org.apache.spark.SparkException: Malformed records are detected in record parsing. Parse Mode: FAILFAST. To process malformed records as null result, try setting the option &#39;mode&#39; as &#39;PERMISSIVE&#39;.</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（0） 💬（0）<div>老师有没有什么资料或者学习方法来学习实现自己的数据源connector</div>2024-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d8/e5/bb87e21f.jpg" width="30px"><span>穌滂</span> 👍（0） 💬（0）<div>请问老师，read是actions算子还是transformations算子？</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/36/1c/adfeb6c4.jpg" width="30px"><span>爱学习的王呱呱</span> 👍（0） 💬（0）<div>老师我想问下，我的parquet文件过大，被切分成了若干个小文件，这些小文件都在同一个hdfs目录下。这种情况下怎么读取呢？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/d2/f12dd0ac.jpg" width="30px"><span>翡翠小南瓜</span> 👍（0） 💬（0）<div>jdbc的numPartitions有什么作用，最大分区啥意思？数据库的表不是分区表，它有用吗</div>2022-04-14</li><br/>
</ul>