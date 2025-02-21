你好，我是吴磊。

在上一讲的最后，我们用一张表格整理了Spark[官网](https://spark.apache.org/docs/latest/rdd-programming-guide.html)给出的RDD算子。想要在Spark之上快速实现业务逻辑，理解并掌握这些算子无疑是至关重要的。

因此，在接下来的几讲，我将带你一起梳理这些常见算子的用法与用途。不同的算子，就像是厨房里的炒勺、铲子、刀具和各式各样的锅碗瓢盆，只有熟悉了这些“厨具”的操作方法，才能在客人点餐的时候迅速地做出一桌好菜。

今天这一讲，我们先来学习同一个RDD内部的数据转换。掌握RDD常用算子是做好Spark应用开发的基础，而数据转换类算子则是基础中的基础，因此我们优先来学习这类RDD算子。

在这些算子中，我们重点讲解的就是map、mapPartitions、flatMap、filter。这4个算子几乎囊括了日常开发中99%的数据转换场景，剩下的mapPartitionsWithIndex，我把它留给你作为课后作业去探索。

![图片](https://static001.geekbang.org/resource/image/a3/88/a3ec138b50456604bae8ce22cdf56788.jpg?wh=1599x1885 "RDD算子分类表")

俗话说，巧妇难为无米之炊，要想玩转厨房里的厨具，我们得先准备好米、面、油这些食材。学习RDD算子也是一样，要想动手操作这些算子，咱们得先有RDD才行。

所以，接下来我们就一起来看看RDD是怎么创建的。

## 创建RDD

在Spark中，创建RDD的典型方式有两种：
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（45） 💬（11）<div>不是很懂spark。mapPartitions()那里，光从代码上来看的话，在map()的闭包里可以访问到外面mapPartitions()闭包里的同一个md5实例，从而达到共享实例的效果。那么有没有可能在最外层创建一个全局的md5实例，这样就算只用map()，在闭包里访问的也是这同一个实例？这样会有什么问题吗？或者说在这种情况下mapPartitions()相比map()还有什么优势？</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（22） 💬（1）<div>老师您回答一楼的问题时提到的序列化意思是不是对象在不同节点间传输的时候只能序列化为字符串传输？如果是的话那我觉得 在mapPartitions里面创建MD5实例，map引用这个对象，Spark却没有报“Task not Serializable”错误 是因为driver把这段代码分发到了各个executor，而创建对象这个工作是由executor完成的，所以不会报错？</div>2021-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKw8ictgYcqf6iaicPTOyZ2CR7iaVeeztZLZrLdrvuJib46ibZgibkhSYg85xZAglBhhsO7bY4fz5YQ8icbMA/132" width="30px"><span>Geek_eb2d3d</span> 👍（8） 💬（1）<div>老师，我在 map 里面使用 SparkContext 或 SparkSession 创建新的 RDD，这样是可以的么？</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/ec/c60b29f5.jpg" width="30px"><span>Alvin-L</span> 👍（7） 💬（3）<div>Python版,虽然能跑,但是不知道对不对:
#哈希值计数
``` 
from hashlib import md5
from pyspark import SparkContext


def f(partition):
    m = md5()
    for word in partition:
        m.update(word.encode(&quot;utf8&quot;))
        yield m.hexdigest()


lineRDD = SparkContext().textFile(&quot;.&#47;wikiOfSpark.txt&quot;)
kvRDD = (
    lineRDD.flatMap(lambda line: line.split(&quot; &quot;))
    .filter(lambda word: word != &quot;&quot;)
    .mapPartitions(f)
    .map(lambda word: (word, 1))
)

kvRDD.foreach(print)

``` 

#相邻+过滤特殊字符
``` 
from pyspark import SparkContext

# 定义特殊字符列表
special_char_list = [&quot;&amp;&quot;, &quot;|&quot;, &quot;#&quot;, &quot;^&quot;, &quot;@&quot;]
# 定义判定函数f
def f(s):
    words = s.split(&quot;-&quot;)
    b1 = words[0] in special_char_list
    b2 = words[1] in special_char_list
    return (not b1) and (not b2)


# 定义拼接函数word_pair
def word_pair(line):
    words = line.split(&quot; &quot;)
    for i in range(len(words) - 1):
        yield words[i] + &quot;-&quot; + words[i + 1]


lineRDD = SparkContext().textFile(&quot;.&#47;wikiOfSpark.txt&quot;)
cleanedPairRDD = lineRDD.flatMap(word_pair).filter(f)
cleanedPairRDD.foreach(print)

``` </div>2021-09-21</li><br/><li><img src="" width="30px"><span>Geek_a30533</span> 👍（4） 💬（1）<div>对scala的函数定义格式不是很清楚，那边绕了好几次，有一个小疑问，在flatMap里的匿名函数f

line =&gt; {  
			val words: Array[String] = line.split(&quot; &quot;)  
			for (i &lt;- 0 until words.length - 1) yield words(i) + &quot;-&quot; + words(i+1)
		}

只定义了形参是line，那出参是整个花括号么？主要是没有return，让我一下迷了，难道是最后一个是Array[String]所以返回值就是这个？不用声明吗？</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（4） 💬（1）<div>老师，请问，一个变量m被filter 算子内部计算时使用，若m定义在了filter算子所在函数内，也就是变量和算子在同一个函数里，就不会报序列化问题，若定义在了函数之外就会报序列化问题，这是为什么？看了一些解释，说是函数闭包，也不是很理解</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5d/e2/1587b1b3.jpg" width="30px"><span>木之上</span> 👍（3） 💬（1）<div>老师，在学习这些算子的时候，像map，flatmap是否可以类比JAVA8的lambda表达式+stream流去学习</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/73/791d0f5e.jpg" width="30px"><span>DMY</span> 👍（3） 💬（3）<div>数据做map映射是以元素为粒度，执行f函数；
这里业务场景中，f函数需要调用rpc，每个数据调一次rpc+数据量大就会非常耗时。
所以想把一组数据打包成一个list减少rpc调用，来提高效率，这里要怎么处理呢</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（3） 💬（4）<div>同问老师,AIK问的问题，什么时候用小括号什么时候用花括号啊，感觉scala实在有点过于灵活</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/77/08ee51cb.jpg" width="30px"><span>孙浩</span> 👍（2） 💬（1）<div>有疑问，吴老师，PariedRDD中的（K，V），1.对应的数据类型应该是scala中的元组吧？2.reduceByKey为啥不支持元素是map类型？或者如果我存在一个RDD[Map[String,Int]]，我想做reduceByKey操作，应该怎么实现？</div>2021-11-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGiaLDlazWNmLnB7nGbHdH3g4Akx1LxJAjx4zrriaS7AWdUXfCzy2pyfhibJ4Z0LNnSOgcSvA39LuOQ/132" width="30px"><span>Geek_390836</span> 👍（2） 💬（1）<div>参考map和mapPartitions，为什么mapPartitions中的map，是对record进行getbytes而不是word.getbytes操作，刚学spark，求老师解答</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（1） 💬（1）<div>mapPartitionsWithIndex  需要结合分区索引使用
map filter flatMap mapPartitions mapPartitionsWithIndex  通过函数，传递参数，返回新的RDD
mapPartitions 采集系统中，只需实例化一次电表号，可读其他各类读数</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（0） 💬（1）<div>&#47;&#47; 相邻词汇计数统计
package com.shouneng

import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

object NeighboringWordCount {
  def main(args: Array[String]) {
    try {
      val conf =
        new SparkConf().setAppName(&quot;NeighboringWordCount&quot;).setMaster(&quot;local[1]&quot;)
      val sparkContext = new SparkContext(conf)
      val rootPath: String = &quot;file:&#47;&#47;&quot;
      val file: String =
        s&quot;${rootPath}&#47;home&#47;shouneng&#47;geektime&#47;Getting_Started_with_Spark&#47;chapter01&#47;wikiOfSpark.txt&quot;

      &#47;&#47; 读取文件内容
      val lineRDD: RDD[String] = sparkContext.textFile(file)
      &#47;&#47;   val wordRDD: RDD[String] = lineRDD.flatMap(line =&gt; line.split(&quot; &quot;))
      &#47;&#47;   val cleanWordRDD: RDD[String] = wordRDD.filter(word =&gt; !word.equals(&quot;&quot;))

      val wordPairRDD: RDD[String] = lineRDD.flatMap(line =&gt; {
        val words: Array[String] =
          line.split(&quot; &quot;).filter(word =&gt; !word.equals(&quot;&quot;))
        for (i &lt;- 0 until words.length - 1) yield words(i) + &quot;-&quot; + words(i + 1)
      })
      val kvRDD: RDD[(String, Int)] = wordPairRDD.map(wordPair =&gt; (wordPair, 1))
      val wordCounts: RDD[(String, Int)] = kvRDD.reduceByKey((x, y) =&gt; x + y)

      wordCounts
        .map { case (k, v) =&gt; (v, k) }
        .sortByKey(false)
        .take(5)
        .foreach(println)
    } catch {
      case ex: Exception =&gt; {
        ex.printStackTrace() &#47;&#47; 打印到标准err
        System.err.println(&quot;exception===&gt;: ...&quot;) &#47;&#47; 打印到标准err
      }
    }
  }
}</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/a8/77/08ee51cb.jpg" width="30px"><span>孙浩</span> 👍（0） 💬（1）<div>吴老师，mapPartitions的是不是也避免了对象锁的问题，因为partitions对应的也是任务数。</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/97/c4/6c92c78a.jpg" width="30px"><span>小强</span> 👍（0） 💬（1）<div>import org.apache.spark.rdd.RDD
 
&#47;&#47; 这里的下划线&quot;_&quot;是占位符，代表数据文件的根目录
val rootPath: String = &quot;&#47;home&#47;gxchen&#47;Spark&#47;01-wordCount&quot;
val file: String = s&quot;${rootPath}&#47;wikiOfSpark.txt&quot;
 
&#47;&#47; 读取文件内容
val lineRDD: RDD[String] = spark.sparkContext.textFile(file)
 
&#47;&#47; 以行为单位做分词
val wordPairRDD: RDD[String] = lineRDD.flatMap(line =&gt; {
	val words: Array[String] = line.split(&quot; &quot;)
	for (i &lt;- 0 until words.length - 1) yield words(i) + &quot;-&quot; + words(i+1)
})



&#47;&#47; 定义特殊字符列表
val list: List[String] = List(&quot;&amp;&quot;, &quot;|&quot;, &quot;#&quot;, &quot;^&quot;, &quot;@&quot;)
 
&#47;&#47; 定义判定函数f
def f(s: String): Boolean = {
	val words: Array[String] = s.split(&quot;-&quot;)
	val b1: Boolean = list.contains(words(0))
	val b2: Boolean = list.contains(words(1))
	return !b1 &amp;&amp; !b2 &#47;&#47; 返回不在特殊字符列表中的词汇对
}
 
&#47;&#47; 使用filter(f)对RDD进行过滤
val cleanWordPairRDD: RDD[String] = wordPairRDD.filter(f)

&#47;&#47; 把RDD元素转换为（Key，Value）的形式
val kvRDD: RDD[(String, Int)] = cleanWordPairRDD.map(wordPair =&gt; (wordPair, 1))
&#47;&#47; 按照单词做分组计数
val wordPairCounts: RDD[(String, Int)] = kvRDD.reduceByKey((x, y) =&gt; x + y)
 
&#47;&#47; 打印词频最高的5个词汇
wordPairCounts.map{case (k, v) =&gt; (v, k)}.sortByKey(false).take(5)


运行了以上代码后，报错。想了半天也没弄明白，求助一下！
21&#47;10&#47;24 04:58:42 ERROR Executor: Exception in task 1.0 in stage 2.0 (TID 3)
java.lang.ArrayIndexOutOfBoundsException: 1
        at $line33.$read$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$iw.f(&lt;console&gt;:29)
        at $line34.$read$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$iw$$iw.$anonfun$cleanWordPairRDD$1(&lt;console&gt;:27)

21&#47;10&#47;24 04:58:42 WARN TaskSetManager: Lost task 1.0 in stage 2.0 (TID 3) (localhost executor driver): java.lang.ArrayIndexOutOfBoundsException: 1

21&#47;10&#47;24 04:58:42 ERROR TaskSetManager: Task 1 in stage 2.0 failed 1 times; aborting job
21&#47;10&#47;24 04:58:42 ERROR Executor: Exception in task 0.0 in stage 2.0 (TID 2)

21&#47;10&#47;24 04:58:42 WARN TaskSetManager: Lost task 0.0 in stage 2.0 (TID 2) (localhost executor driver): java.lang.ArrayIndexOutOfBoundsException: 0</div>2021-10-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/hSGZCTvHTKaJH5WibTcC15qDKYpGdgdMFEV6mwcslOFoADP6skWCpBiae2ykkaBFDaexEY9xXBPhZMAGmj1nW8vA/132" width="30px"><span>进</span> 👍（0） 💬（1）<div>期待下一讲....</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/f7/a6f40eee.jpg" width="30px"><span>求索</span> 👍（0） 💬（3）<div>请教个问题，spark sql执行缓慢，然而资源却闲置状态，这是何解</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（0） 💬（1）<div>1、mapPartitionsWithIndex的应用场景：获取数据所在的分区并对特定分区数据进行特定处理。
2、这些算子首先都是惰性算子，又都使用函数作为参数传入，达到一对一的效果。
3、在mapPatitions中只创建过连接数据库的共享对象，其他的没有遇到过，还请老师能不能多给几个实际案例，提高一下对mapPatitions的认知。
还想向老师提个问题：scala编程spark什么时候用小括号,什么时候用用花括号？
wordCount.map{case (k, v) =&gt; (v, k)}.sortByKey(false).take(5)
这段代码对于为什么使用花括号，不是很清晰，尝试过用小括号，但是无法调用sortByKey。</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/bd/95/882bd4e0.jpg" width="30px"><span>Abigail</span> 👍（0） 💬（5）<div>遇到一个关于filter 函数的 bug on reduceByKey。
我运行第一个例子代码如下可以得到正确的结果：
...
 val cleanedPairRDD: RDD[String] = wordPairRDD.filter(word =&gt; !word.equals(&quot;&quot;)) 
...
可以输出结果：
scala&gt; :load WordCount03.scala
Loading WordCount03.scala...
import org.apache.spark.rdd.RDD
rootPath: String = .
file: String = .&#47;wikiOfSpark.txt
lineRDD: org.apache.spark.rdd.RDD[String] = .&#47;wikiOfSpark.txt MapPartitionsRDD[274] at textFile at WordCount03.scala:80
wordPairRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[275] at flatMap at WordCount03.scala:80
cleanedPairRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[276] at filter at WordCount03.scala:80
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[277] at map at WordCount03.scala:80
wordCounts: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[278] at reduceByKey at WordCount03.scala:80
res66: Array[(Int, String)] = Array((10,Apache-Software), (8,Apache-Spark), (7,can-be), (7,-&quot;Spark), (7,of-the))

修改代码，添加filter函数后，代码报错：
代码：
...
&#47;&#47; 定义特殊字符列表
val list: List[String] = List(&quot;&amp;&quot;, &quot;|&quot;, &quot;#&quot;, &quot;^&quot;, &quot;@&quot;, &quot;\&quot;&quot;,&quot;-&quot;)
def f(s: String): Boolean = {
    val words: Array[String] = s.split(&quot;-&quot;)
    val b1: Boolean = list.contains(words(0))
    val b2: Boolean = list.contains(words(1))
    return !b1 &amp;&amp; !b2}  
val cleanedPairRDD: RDD[String] = wordPairRDD.filter(f)  
...
输出报错：
scala&gt; :load WordCountDebug.scala
Loading WordCountDebug.scala...
...
list: List[String] = List(&amp;, |, #, ^, @, &quot;, -)
f: (s: String)Boolean
cleanedPairRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[286] at filter at WordCountDebug.scala:84
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[287] at map at WordCountDebug.scala:82
wordCounts: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[288] at reduceByKey at WordCountDebug.scala:82
21&#47;09&#47;15 09:51:42 ERROR Executor: Exception in task 1.0 in stage 108.0 (TID 141)
java.lang.ArrayIndexOutOfBoundsException: 1
...
</div>2021-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（3） 💬（0）<div>最后filter更建议用Set这种数据结构进行contain查询，set的算法复杂度为O(1)
本节内容Java版本实现
https:&#47;&#47;github.com&#47;Spoon94&#47;spark-practice&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;spoon&#47;spark&#47;core&#47;TransformOpJob.java</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/58/a1/6e33ffc7.jpg" width="30px"><span>请输入昵称</span> 👍（1） 💬（0）<div>课后回答
第一题：应用为按照分区索引做定制化操作
第二题：共性为都是转换算子，并非行动算子
第三题：之前没用过 mapPartitions 算子，也不知道，看来下代码，发现了可以很多用这个算子做优化的地方</div>2022-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIxKpBQJbxHFG9Wjk73WkbqcGeDrjzwjPSDzLlm8C80U9dVmByrrmBa3LmIoCYUW2H3thj5VfMvGQ/132" width="30px"><span>jasonde</span> 👍（0） 💬（0）<div>老师，麻烦咨询一下用map， mappartition， 是否也可以实现flatmap 的结果呢，劳烦指导，谢谢了</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/f9/1dcffdc0.jpg" width="30px"><span>Geek_919d2f</span> 👍（0） 💬（0）<div>为什么不可以把val md5 = MessageDigest.getInstance(&quot;MD5&quot;) 这一段，提取到方法外面，这样就可以不使用mapPartitions，不用再套一层逻辑了</div>2023-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d3/0a/92640aae.jpg" width="30px"><span>我爱夜来香</span> 👍（0） 💬（1）<div>老师,map算子针对一个个元素进行f操作,这个元素是咋定义的,一行?</div>2022-04-13</li><br/>
</ul>