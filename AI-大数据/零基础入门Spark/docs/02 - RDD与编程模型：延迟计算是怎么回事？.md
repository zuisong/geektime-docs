你好，我是吴磊。

在上一讲，我们一起开发了一个Word Count小应用，并把它敲入到spark-shell中去执行。Word Count的计算步骤非常简单，首先是读取数据源，然后是做分词，最后做分组计数、并把词频最高的几个词汇打印到屏幕上。

如果你也动手实践了这个示例，你可能会发现，在spark-shell的REPL里，所有代码都是立即返回、瞬间就执行完毕了，相比之下，只有最后一行代码，花了好长时间才在屏幕上打印出the、Spark、a、and和of这几个单词。

针对这个现象，你可能会觉得很奇怪：“读取数据源、分组计数应该是最耗时的步骤，为什么它们瞬间就返回了呢？打印单词应该是瞬间的事，为什么这一步反而是最耗时的呢？”要解答这个疑惑，我们还是得从RDD说起。

## 什么是RDD

为什么非要从RDD说起呢？首先，RDD是构建Spark分布式内存计算引擎的基石，很多Spark核心概念与核心组件，如DAG和调度系统都衍生自RDD。因此，深入理解RDD有利于你更全面、系统地学习 Spark 的工作原理。

其次，尽管RDD API使用频率越来越低，绝大多数人也都已经习惯于DataFrame和Dataset API，但是，无论采用哪种API或是哪种开发语言，你的应用在Spark内部最终都会转化为RDD之上的分布式计算。换句话说，如果你想要对Spark作业有更好的把握，前提是你要对RDD足够了解。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/48/fb/7b27bccb.jpg" width="30px"><span>cfwseven</span> 👍（37） 💬（3）<div>作者大大能说一下，为什么action算子要设置成延迟计算吗</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（21） 💬（1）<div>从两者的整体流程来看，结果都是不可逆的，但是WordCount可以设置Cache和Checkpoint，方便加速访问和故障修复，而土豆加工流程却不可以。土豆加工流程是DAG的概图。</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/1c/92/dcbad687.jpg" width="30px"><span>宇</span> 👍（14） 💬（4）<div>怎样知道程序里哪个算子最耗时，现在薯片生产速度很慢，我想知道最耗时生产环节是哪个（清洗，切割，还是烘烤）？</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（5） 💬（1）<div>Action中漏了一个reduce，今天才注意到reduceByKey是transformation而reduce是action</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/82/3afc0b3c.jpg" width="30px"><span>Geek_dcxai9</span> 👍（5） 💬（2）<div>从两者不同点看，workdcount切切实实为延迟计算，而土豆工坊的流程为切实发生的。</div>2021-09-16</li><br/><li><img src="" width="30px"><span>zx</span> 👍（4） 💬（1）<div>计算wordcount的时候文件路径写错了，但是却是在reduceByKey这一步报错，这步并不是action算子，这是和partitions属性有关吗</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/65/4c/f7f86496.jpg" width="30px"><span>welldo</span> 👍（4） 💬（3）<div>&quot;我们再来看 RDD 的 partitioner 属性，这个属性定义了把原始数据集切割成数据分片的切割规则。在土豆工坊的例子中，“带泥土豆”RDD 的切割规则是随机拿取，也就是从麻袋中随机拿取一颗脏兮兮的土豆放到流水线上。后面的食材形态，如“干净土豆”、“土豆片”和“即食薯片”，则沿用了“带泥土豆”RDD 的切割规则。换句话说，后续的这些 RDD，分别继承了前一个 RDD 的 partitioner 属性。&quot;
-----------------------
老师, 看完这段话和土豆流水线的图片, 我有几个疑问.

1. rdd分为&lt;value&gt;类型和&lt;key,value&gt;类型，数据分区方式只作用于&lt;Key，Value&gt;形式的数据。
并且刚开始没有任何分区方式，直到遇到包含shuffle的算子时，才会使用“分区方式”，比如hash分区。

问题1：那么，一坨数据，在成为&lt;key,value&gt;类型的rdd的时候（假如4片），分片方式，是不是平均分成4份呢？

2. &lt;value&gt;类型的rdd，没有分区器，那么它刚刚生成的时候，也是平均分吗？</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/27/15/abf4f787.jpg" width="30px"><span>田大侠</span> 👍（2） 💬（1）<div>作者大大有个问题问一下
这里的依赖关系有个比较明显的差别
1.map计算是一个数据分片依赖于前一个RDD“数据分片”，就是说在同一个分片上可以连续计算直到reduce之前
2.reduce计算是依赖关系前面一个RDD的所有的数据集 spark实际计算的时候要等前面所有的map计算完成才能进行reduce操作

上面的我的两个理解是否有偏差？</div>2022-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bmgpp5wc8GLmOdHNQccSgrunK0VdIicB6rpTHXCTF5xEkm2YvPHOX2DwNt2EqTzJ70JD41h0u5qW4R0yXRY1ZCg/132" width="30px"><span>Eazow</span> 👍（0） 💬（2）<div>请问土豆工坊图是用什么画滴那？</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d3/82/c3e57eb3.jpg" width="30px"><span>xuchuan</span> 👍（0） 💬（1）<div>都是来料加工，目标都是高效率生产。</div>2021-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKXgGEaR08MWXP13HdKiaOaSH8ejETGnB2r9AibLWic2ibqeicspnWYbF7P0ZIF6KAYN6nFDhm0QVjushw/132" width="30px"><span>小马哥</span> 👍（0） 💬（0）<div>老师，打扰想问下action算子，最终收集任务结果，然后计算是在driver中执行吗？</div>2024-10-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKXgGEaR08MWXP13HdKiaOaSH8ejETGnB2r9AibLWic2ibqeicspnWYbF7P0ZIF6KAYN6nFDhm0QVjushw/132" width="30px"><span>小马哥</span> 👍（0） 💬（0）<div>想问下action算子，怎么收集每个任务的执行结果？是在哪里收集的？</div>2024-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b8/52/5ab04f5d.jpg" width="30px"><span>廖子博</span> 👍（0） 💬（0）<div>Java代码

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.sql.SparkSession;
import scala.Tuple2;
 
import java.util.Arrays;
import java.util.List;
 
public class WorkCount {
    public static void main(String[] args) {
        SparkSession spark = SparkSession.builder()
                .appName(&quot;WorkCount&quot;)
                .getOrCreate();
        JavaRDD&lt;String&gt; lines = spark.read().textFile(&quot;&#47;Users&#47;liaozibo&#47;code&#47;demo&#47;spark-demo&#47;spark-readme.md&quot;).javaRDD();
        JavaRDD&lt;String&gt; words = lines.flatMap(line -&gt; Arrays.asList(line.split(&quot;\\s+&quot;)).iterator()).filter(word -&gt; !word.isEmpty());
        List&lt;Tuple2&lt;Integer, String&gt;&gt; top5 = words.mapToPair(word -&gt; new Tuple2&lt;&gt;(word, 1))
                .reduceByKey(Integer::sum)
                .mapToPair(Tuple2::swap)
                .sortByKey(false)
                .take(5);
        top5.forEach(System.out::println);
    }
}

打包执行
$SPARK_HOME&#47;bin&#47;spark-submit \
--class &quot;WorkCount&quot; \
--master local[4] \
target&#47;spark-demo-1.0-SNAPSHOT.jar</div>2024-09-05</li><br/><li><img src="" width="30px"><span>Geek_5bd5c5</span> 👍（0） 💬（0）<div>不是，买了复制还是乱码啊</div>2024-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（0）<div>老师好，如果说rdd的单元是partition的话，那map函数的作用为啥是元素，而mapPartitions作用是partition内所有元素呢</div>2023-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（1）<div>老师好，这里的“同一种食材形态在不同流水线上的具体实物，就是 RDD 的 partitions 属性；” 指的是在水平处理的逻辑上，例如带泥巴的土豆、干净的土豆和土豆切片都是同一个rdd上的不同partition嘛</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师，你好，为什么foreach也是action算子呢，foreach跟map其实很像，只不过foreach不需要返回值</div>2023-08-02</li><br/><li><img src="" width="30px"><span>Geek_a25305</span> 👍（0） 💬（0）<div>大神你好 我有个问题:


如果把“带泥土豆”看成是 RDD 的话，那么 RDD 的 partitions 属性，囊括的正是麻袋里那一颗颗脏兮兮的土豆。同理，流水线上所有洗净的土豆，一同构成了“干净土豆”RDD 的 partitions 属性。

这句话, 是不是要改成:

囊括的正是麻袋里每一颗脏兮兮的土豆。</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>RDD这种抽象，平时在IDEA这种开发环境中，小批量数据应该可以debug 吧</div>2022-06-17</li><br/><li><img src="" width="30px"><span>Geek_757cbc</span> 👍（0） 💬（1）<div>既然spark的transformation不会立即计算为什么会立即返回，还是不太理解，难道返回的结果不是计算之后的结果吗</div>2022-05-23</li><br/>
</ul>