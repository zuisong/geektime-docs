你好，我是蔡元楠。

今天我们来从零开始运行你的第一个Spark应用。

我们先来回顾一下模块三的学习路径。

首先，我们由浅入深地学习了Spark的基本数据结构RDD，了解了它这样设计的原因，以及它所支持的API。

之后，我们又学习了Spark SQL的DataSet/DataFrame API，了解到它不仅提供类似于SQL query的接口，大大提高了开发者的工作效率，还集成了Catalyst优化器，可以提升程序的性能。

这些API应对的都是批处理的场景。

再之后，我们学习了Spark的流处理模块：Spark Streaming和Structured Streaming。两者都是基于微批处理（Micro batch processing）的思想，将流数据按时间间隔分割成小的数据块进行批处理，实时更新计算结果。

其中Structured Streaming也是使用DataSet/DataFrame API，这套API在某种程度上统一了批处理和流处理，是当前Spark最流行的工具，我们必需要好好掌握。

虽然学习了这么多API以及它们的应用，但是大部分同学还没有从零开始写一个完整的Spark程序，可能更没有运行Spark程序的经历。纸上谈兵并不能帮助我们在工作生活中用Spark解决实际问题。所以，今天我就和你一起做个小练习，从在本地安装Spark、配置环境开始，为你示范怎样一步步解决之前提到数次的统计词频（Word Count）的问题。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（2） 💬（1）<div>.groupBy(&quot;Value&quot;)这个value是什么意思？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（1） 💬（2）<div>python 直接安装
pip install pyspark
pip帮你搞定一切安装配置问题。
参考资料：
https:&#47;&#47;pypi.org&#47;project&#47;pyspark&#47;</div>2019-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（1）<div>实践成功
demo.txt:
I hava a dog
He has a Dog
RDD写法：
[(&#39;I&#39;, 1), (&#39;hava&#39;, 1), (&#39;a&#39;, 2), (&#39;dog&#39;, 1), (&#39;He&#39;, 1), (&#39;has&#39;, 1), (&#39;Dog&#39;, 1)]
[(&#39;a&#39;, 2), (&#39;I&#39;, 1), (&#39;hava&#39;, 1), (&#39;dog&#39;, 1), (&#39;He&#39;, 1), (&#39;has&#39;, 1), (&#39;Dog&#39;, 1)]
DF写法：
[Row(word=&#39;dog&#39;, count=1), Row(word=&#39;He&#39;, count=1), Row(word=&#39;Dog&#39;, count=1), Row(word=&#39;I&#39;, count=1), Row(word=&#39;a&#39;, count=2), Row(word=&#39;hava&#39;, count=1), Row(word=&#39;has&#39;, count=1)]
[Row(word=&#39;a&#39;, count=2), Row(word=&#39;I&#39;, count=1), Row(word=&#39;Dog&#39;, count=1), Row(word=&#39;hava&#39;, count=1), Row(word=&#39;dog&#39;, count=1), Row(word=&#39;has&#39;, count=1), Row(word=&#39;He&#39;, count=1)]

从启动到出结果，DF写法速度要比rdd慢。</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/9f/460284b9.jpg" width="30px"><span>Qi Liu 刘祺</span> 👍（0） 💬（1）<div>继续学习~</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（20） 💬（0）<div>java万金油，什么都可以干，人好招，特别是我们这种偏远地区，scala，虽然开发效率高，但是人少，难招，所以我们大数据团队选择了java。至于运行效率，py是最慢的，java和scala应该半斤八俩吧</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（9） 💬（2）<div>女同学看完2015年出的spark快速大数据分析这本书以后，再来看老师写的这些文字，觉得言简意赅，印象深刻，至于用什么语言倒无所谓了，主要是思路。后期希望老师能多说一些案例和处理中需要注意的技巧。</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/8e/6e4c7509.jpg" width="30px"><span>一</span> 👍（7） 💬（0）<div>看了这一讲意识到之前对Python欠缺了重视，现在明白Python在大数据处理领域是很有竞争力的，因为Spark和众多的库的原因，甚至超越Java，所以现在要重新重视起来Python的学习了</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（6） 💬（0）<div>【以下代码可以运行，但对df格式的操作是借助二楼的网址去找的，具体含义也不太清楚，只是可以运行出来】

#python前运行调用包
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

#初始化SparkSession程序入口
spark = SparkSession.builder.appName(&quot;WordCount&quot;).getOrCreate()
#读入文档
ds_lines = spark.read.text(&quot;&#47;Users&#47;apple&#47;code_tool&#47;spark&#47;WordCount&#47;demo.md&quot;)
#针对df特定的计算格式
words = ds_lines.select(
   explode(
       split(ds_lines.value, &quot; &quot;)
   ).alias(&quot;word&quot;)
)
#返回的RDD进行计数
wordCounts = words.groupBy(&quot;word&quot;).count()
#展示
wordCounts.show()
#关闭spark
spark.stop()</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/1f/343f2dec.jpg" width="30px"><span>9527</span> 👍（6） 💬（1）<div>spark_session = SparkSession.builder.appName(&quot;PySparkShell&quot;).getOrCreate()
ds_lines = spark_session.read.textFile(&quot;README.md&quot;)
ds = ds_lines.flatMap(lambda x: x.split(&#39; &#39;)).groupBy(&quot;Value&quot;).count()
ds.show()

我执行这段的时候报错了
AttributeError: &#39;DataFrameReader&#39; object has no attribute &#39;textFile&#39;
如果把textFile()改成text()就对了
再执行flatMap那段，也报错了
AttributeError: &#39;DataFrame&#39; object has no attribute &#39;flatMap&#39;
是不是API变动了，我用的是2.4.3版本单机执行的</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/8c/f029535a.jpg" width="30px"><span>hallo128</span> 👍（4） 💬（1）<div>“虽然 Spark 还支持 Java 和 R，但是我个人不推荐你使用。用 Java 写程序实在有些冗长，而且速度上没有优势。”
推荐使用，还是应该详细说明对比下，不能只因为自己偏好某种工具给出建议。对于spark原生来说，速度和库同步更新更快的是Scala，如果你想随时用到spark最新功能库的话，就应该选择Scala，同时速度也是最快的。
至于Python，R，Java，一方面和你的熟悉程度有关，另一方面也与你到底准备用spark来做什么的目的有关。是集群控制，还是数据分析，还是建模，来选择合适的编程语言与spark进行连接编写。</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/39/ac/d185d0e5.jpg" width="30px"><span>Quincy</span> 👍（3） 💬（0）<div>Spark 不应该是首选Scala 么</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（3） 💬（0）<div>#!&#47;usr&#47;bin&#47;python3

import os
from pyspark import SparkContext, SparkConf


os.environ[&#39;SPARK_HOME&#39;] = &#39;&#47;usr&#47;local&#47;spark&#39;
os.environ[&#39;HADOOP_HOME&#39;] = &#39;&#47;usr&#47;local&#47;hadoop-2.7.7&#39;

conf = SparkConf().setAppName(&#39;WordCount&#39;).setMaster(&#39;local&#39;)
sc = SparkContext(&#39;local&#39;, &#39;pyspark&#39;, conf=conf)

text_file = sc.textFile(&#39;file:&#47;&#47;&#47;Users&#47;albert.ming.xu&#47;Downloads&#47;text.txt&#39;)

counts = text_file.filter(lambda x: len(x.strip()) &gt; 0).flatMap(lambda x: x.split(&#39; &#39;)).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).sortBy(lambda x: x[1], ascending=False)

print(&#39;|{0: ^20}|{1: ^20}|&#39;.format(&#39;Word&#39;, &#39;Count&#39;))
for (word, num) in counts.take(10):
    print(&#39;|{0: ^20}|{1: ^20}|&#39;.format(word, num))

</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/1b/7f34b19b.jpg" width="30px"><span>Geek_4ldh1g</span> 👍（3） 💬（0）<div>用java写 有点冗长  我不敢苟同，因为java8 已经是函数编程了！而且spark开发我觉得大部分还是spark  sql多点！这样基本没啥区别  </div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/89/78/311dbb8b.jpg" width="30px"><span>这个名字居然都有</span> 👍（3） 💬（1）<div>老师，你给一个完整的案例吧，</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/c7/66f5fcea.jpg" width="30px"><span>大志</span> 👍（2） 💬（1）<div>老师，本地已经安装了Spark，有Demo吗，只看代码片段的话还是无从下手啊</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/cc/fac12364.jpg" width="30px"><span>xxx</span> 👍（1） 💬（0）<div>文中的示例是可以运行的，稍微改改：

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

if __name__ == &quot;__main__&quot;:
    spark = SparkSession.builder.appName(&#39;WordCount&#39;).getOrCreate()
    lines = spark.read.text(&quot;wikiOfSpark.txt&quot;)
    wordCounts = lines.select(explode(split(lines.value, &quot; &quot;)).alias(&quot;word&quot;)).groupBy(&quot;word&quot;).count().sort(desc(&quot;count&quot;))
    wordCounts.show()

    spark.stop()</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2a/fb/e2b29825.jpg" width="30px"><span>Bing</span> 👍（1） 💬（0）<div>flatMap是rdd的算子，df不能直接用，可以explode行转列</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/7c/25abe455.jpg" width="30px"><span>stars</span> 👍（0） 💬（0）<div>前面还好，到这里看不懂了，环境搭建完成，代码怎么执行，完全走不下去，是不是简单说一下</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/ac/a7da8788.jpg" width="30px"><span>黑黑白</span> 👍（0） 💬（0）<div>from operator import add

from pyspark.sql import SparkSession

if __name__ == &quot;__main__&quot;:
    spark = SparkSession.builder.appName(&quot;rdd&quot;)\
        .config(&quot;spark.driver.bindAddress&quot;, &quot;127.0.0.1&quot;)\
        .getOrCreate()
    lines = spark.read.text(&quot;file:&#47;&#47;&#47;mnt&#47;d&#47;playground&#47;bigdata&#47;spark001&#47;sample.txt&quot;)\
        .rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(&#39; &#39;)).map(lambda x: (x, 1)).reduceByKey(add)
    output = counts.collect()

    for (word, count) in output:
        print(&quot;%s: %i&quot; % (word, count))
    spark.stop()</div>2021-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/a8/10/ee8b8c0b.jpg" width="30px"><span>whatever</span> 👍（0） 💬（0）<div>给所有小白到我这个程度踩了初级坑的人：

如果运行pyspark报错 ERROR SparkContext: Error initializing SparkContext，说明需要修改主机名
vim ~&#47;.bash_profile
添加
export SPARK_LOCAL_HOSTNAME=localhost
编辑完后重新加载，执行
source ~&#47;.bash_profile
再运行pyspark试试</div>2020-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/6f/3d4f7e31.jpg" width="30px"><span>娄江国</span> 👍（0） 💬（0）<div>在pyspark中执行的程序，为什么在spark的管控台上，看不到对应的Application呢？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/4c/a51ece16.jpg" width="30px"><span>刘润森</span> 👍（0） 💬（0）<div>我在centos搭建Spark集群，怎么用Pyspark在window连接spark集群</div>2020-03-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdpKbFgRLnicjsr6qkrPVKZcFrG3aS2V51HhjFP6Mh2CYcjWric9ud1Qiclo8A49ia3eZ1NhibDib0AOCg/132" width="30px"><span>西北偏北</span> 👍（0） 💬（0）<div>对于词频统计的场景，除了用map reduce的方式，对应到sql就是group by，基于每个单词分组然后统计每个分组的大小</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（0）<div>老师我想问一下，如果大数据学习用python、java、还是Scala？
python虽然代码少，但不是说性能上，运行速度上不及java和go吗？</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/9d/25650474.jpg" width="30px"><span>fresh</span> 👍（0） 💬（0）<div>能用java 写代码吗？</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>环境搭好了，下一步不知道怎么操作了。</div>2019-05-29</li><br/>
</ul>