你好，我是吴磊。

在上一讲，我们学习了创建DataFrame的各种途径与方法，那么，有了DataFrame之后，我们该如何在DataFrame之上做数据探索、数据分析，以及各式各样的数据转换呢？在数据处理完毕之后，我们又该如何做数据展示与数据持久化呢？今天这一讲，我们就来解答这些疑问。

为了给开发者提供足够的灵活性，对于DataFrame之上的数据处理，Spark SQL支持两类开发入口：一个是大家所熟知的结构化查询语言：SQL，另一类是DataFrame开发算子。就开发效率与执行效率来说，二者并无优劣之分，选择哪种开发入口，完全取决于开发者的个人偏好与开发习惯。

与RDD类似，DataFrame支持种类繁多的开发算子，但相比SQL语言，DataFrame算子的学习成本相对要高一些。因此，本着先易后难的思路，咱们先来说说DataFrame中SQL语句的用法，然后再去理解DataFrame开发算子。

## SQL语句

对于任意的DataFrame，我们都可以使用createTempView或是createGlobalTempView在Spark SQL中创建临时数据表。

两者的区别在于，createTempView创建的临时表，其生命周期仅限于SparkSession内部，而createGlobalTempView创建的临时表，可以在同一个应用程序中跨SparkSession提供访问。有了临时表之后，我们就可以使用SQL语句灵活地倒腾表数据。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（11） 💬（3）<div>explode 不会引入shuffle,因为shuffle是在众多计算节点进行数据传输，explode虽然会导致数据条数变多但是都是在一台节点上的</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（2） 💬（1）<div>python 代码为：

# 1-SQL语句：
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
sc = SparkContext()
spark = SparkSession(sc)

seq=[(&#39;Alice&#39;,18), (&#39;Bob&#39;,14)]
column = [&#39;name&#39;,&#39;age&#39;]
df=spark.createDataFrame(seq,column)
df.createTempView(&#39;t1&#39;)
query=&quot;select * from t1&quot;
result=spark.sql(query)
result.show()

# 2-探索类算子：
employees=[(1, &quot;John&quot;, 26, &quot;Male&quot;), (2, &quot;Lily&quot;, 28, &quot;Female&quot;), (3, &quot;Raymond&quot;, 30, &quot;Male&quot;)]
employeesDF=spark.createDataFrame(employees,[&#39;id&#39;,&#39;name&#39;,&#39;age&#39;,&#39;gender&#39;])
employeesDF.printSchema()
employeesDF.show() 
age_df=employeesDF.describe(&#39;age&#39;)
age_df.show()

# 3-清洗类算子：
# 删除某一列数据
employeesDF.drop(&#39;gender&#39;).show()
# distinct对所有数据去重，注意无法设置列名
employeesDF.distinct().show()
# dropDuplicates可以对某几列去重，灵活性更高
employeesDF.dropDuplicates([&#39;gender&#39;]).show()

# 4-转换类算子
# 选择某几列组成新的df
employeesDF.select([&#39;name&#39;,&#39;gender&#39;]).show()
employeesDF.select(&#39;name&#39;).show()
# selectExpr用选择表达式来组成新的df
employeesDF.selectExpr(&quot;id&quot;, &quot;name&quot;, &quot;concat(id, &#39;_&#39;, name) as id_name&quot;).show()
# where选择满足条件的内容
employeesDF.where(&quot;gender=&#39;Male&#39;&quot;).show()
# 对列名重命名：将gender重命名为sex
employeesDF.withColumnRenamed(&#39;gender&#39;,&#39;sex&#39;).show() 
# 在原列进行修改后组成新的一列，将age都+10岁
employeesDF.withColumn(&quot;crypto&quot;, employeesDF[&#39;age&#39;]+10).show()
# drop删除某一列
employeesDF.withColumn(&quot;crypto&quot;, employeesDF[&#39;age&#39;]+10).drop(&#39;age&#39;).show()

# explode拆分list
seq2 =[(1, &quot;John&quot;, 26, &quot;Male&quot;,[&quot;Sports&quot;, &quot;News&quot;]),
(2, &quot;Lily&quot;, 28, &quot;Female&quot;, [&quot;Shopping&quot;, &quot;Reading&quot;]),
(3, &quot;Raymond&quot;, 30, &quot;Male&quot;, [&quot;Sports&quot;, &quot;Reading&quot;])]
employeesDF2=spark.createDataFrame(seq2,[&#39;id&#39;,&#39;name&#39;,&#39;age&#39;,&#39;gender&#39;,&#39;interests&#39;])
from pyspark.sql.functions import explode
employeesDF2.withColumn(&#39;interest&#39;,explode(employeesDF2[&#39;interests&#39;])).show()</div>2021-10-23</li><br/><li><img src="" width="30px"><span>Geek_935079</span> 👍（1） 💬（2）<div>val aggResult = fullInfo.groupBy这里是不是要改为val aggResult = jointDF.groupBy</div>2021-11-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iaQgtbE98VGIVIyribdo6dgLOnaNoe7ZdUuPr60ibsduibscrzQCTzdW2AfL9nxwe8YlSK75gOnK3YbAJKTaFPxibdg/132" width="30px"><span>小李</span> 👍（0） 💬（1）<div>请问一下：df.select().groupBy().count()与df.select().groupBy().agg(count(lit(1)))内部处理逻辑会不一样吗，还是会都会经过spark sql优化引擎优化成map阶段预聚合？比如会不会像rdd的aggregateByKey或者reduceByKey一样在shuffle write阶段做partition内的预聚合。</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（0） 💬（1）<div>
# 5-分析类算子
# 创建员工df
seq=[(1,&#39;Mike&#39;,28,&#39;Male&#39;),
     (2, &quot;Lily&quot;, 30, &quot;Female&quot;),
     (3, &quot;Raymond&quot;, 26, &quot;Male&quot;)]
employees=spark.createDataFrame(seq,[&#39;id&#39;,&#39;name&#39;,&#39;age&#39;,&#39;gender&#39;])
employees.show()

# 创建薪水df
seq2=[(1, 26000), (2, 30000), (4, 25000), (3, 20000)]
salaries=spark.createDataFrame(seq2,[&#39;id&#39;,&#39;salary&#39;])
salaries.show()

# 将员工df和薪水df进行合并，inner方式：
joinDF=salaries.join(employees,&#39;id&#39;,&#39;inner&#39;)
joinDF.show()

# 按照性别统计出薪水之和，平均值
from pyspark.sql import functions as f
aggResult=joinDF.groupBy(&#39;gender&#39;).agg(f.sum(&#39;salary&#39;).alias(&#39;sum_salary&#39;),f.avg(&#39;salary&#39;).alias(&#39;avg_salary&#39;))
aggResult.show()

# 排序，sort方法和orderBy方法一样
aggResult.sort(f.desc(&#39;sum_salary&#39;),f.asc(&#39;gender&#39;)).show()
aggResult.orderBy(f.desc(&#39;sum_salary&#39;),f.asc(&#39;gender&#39;)).show()</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3d/08/fcf92621.jpg" width="30px"><span>小玲铛🍯</span> 👍（0） 💬（1）<div>自己开发的时候createTempView会在内存中创建临时表,重新运行的话会报table is exist 错误,建议使用 createOrReplaceTempView</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>Spark中Shuffle算子的分类：重分区算子、ByKey算子、Join算子</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（2） 💬（0）<div>Java代码实现
https:&#47;&#47;github.com&#47;Spoon94&#47;spark-practice&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;spoon&#47;spark&#47;sql&#47;DataFrameOperatorJob.java</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/eb/24e0ac9c.jpg" width="30px"><span>嬴梦川</span> 👍（0） 💬（0）<div>从我的开发经验发现explode不会引入shuffle</div>2023-09-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIw0Nnvrrt9fV1wHVfBlPzrZmxNCRTbWPfNEbCEMtuoj6gw0LlMbbS3gtRLgLMfCoAV3TXsk5giavw/132" width="30px"><span>Geek_b2839b</span> 👍（0） 💬（0）<div>老师请问一下，使用spark同步hive数据到Oracle的时候，由于executor失败重试，导致偶尔出现同步时hive数据和Oracle数据不一致的情况，这个该怎么解决呢</div>2022-05-28</li><br/>
</ul>