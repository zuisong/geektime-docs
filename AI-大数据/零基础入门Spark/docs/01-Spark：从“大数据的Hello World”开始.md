你好，我是吴磊。

从这节课开始，我们先来学习Spark的“基础知识”模块，对Spark的概念和核心原理先做一个整体的了解。我并不会从RDD、DAG这些基本概念给你讲起。坦白地说，这些抽象的概念枯燥而又乏味，对于刚开始接触Spark的你来说，很难学进去。因此，我们不妨反其道而行之，先从实战入手，用一个小例子来直观地认识Spark，看看Spark都能做些什么。

这就好比我们学习一门新的编程语言，往往都是从“Hello World”开始。我还记得，刚刚学编程那会，屏幕上打印出的“Hello World”，足足让我兴奋了一整天，让我莫名地有一种“I can change the world”的冲动。

今天这一讲，我们就从“大数据的Hello World”开始，去学习怎么在Spark之上做应用开发。不过，“大数据的Hello World”并不是把字符串打印到屏幕上这么简单，而是要先对文件中的单词做统计计数，然后再打印出频次最高的5个单词，江湖人称“Word Count”。

之所以会选择Word Count，作为我们迈入Spark门槛的第一个项目，主要有两个原因，一是Word Count场景比较简单、容易理解；二是Word Count麻雀虽小，但五脏俱全，一个小小的Word Count，就能够牵引出Spark许多的核心原理，帮助我们快速入门。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/75/ec/c60b29f5.jpg" width="30px"><span>Alvin-L</span> 👍（21） 💬（6）<div>在Python中运行:
``` 
from pyspark import SparkContext

textFile = SparkContext().textFile(&quot;.&#47;wikiOfSpark.txt&quot;)
wordCount = (
    textFile.flatMap(lambda line: line.split(&quot; &quot;))
    .filter(lambda word: word != &quot;&quot;)
    .map(lambda word: (word, 1))
    .reduceByKey(lambda x, y: x + y)
    .sortBy(lambda x: x[1], False)
    .take(5)
)
print(wordCount)
#显示: [(&#39;the&#39;, 67), (&#39;Spark&#39;, 63), (&#39;a&#39;, 54), (&#39;and&#39;, 51), (&#39;of&#39;, 50)]
``` 
</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/81/63/2ceecb43.jpg" width="30px"><span>liugddx</span> 👍（44） 💬（4）<div>我是一个大数据小白，我想咨询下spark和hadoop在大数据体系下的关系？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5e/b2/aceb3e41.jpg" width="30px"><span>Neo-dqy</span> 👍（26） 💬（5）<div>老师好！wordCounts.map{case (k, v) =&gt; (v, k)}.sortByKey(false).take(5)这行代码我还存在疑问，为什么这里的map函数使用了花括号{ }而不是上面一些算子的( )，同时这个case又是什么意思？这一行代码非常像我曾经在Python中使用字典数据结构，然后根据字典值的升序排序。最后，貌似Scala语言本身就可以实现wordcount案例，那么它本身的实现和spark实现相比，spark有什么优势呢？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/36/ccf3b5d1.jpg" width="30px"><span>Vic</span> 👍（8） 💬（9）<div>遇到这个问题
scala&gt; val rootPath: String = _
&lt;console&gt;:24: error: unbound placeholder parameter
       val rootPath: String = _
网上搜一下，说这是汇编错误。
要把val 改成var , 但会遇到&quot;_&quot;这default值是null。
org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:&#47;Users&#47;vic&#47;src&#47;data&#47;null&#47;wikiOfSpark.txt
这一段就先跳过root_path，直接给file一个路径，是可以成功运行&quot;word count&quot;,得到和老师一样的结果:
[Stage 0:&gt;                                                          (0 + 2) &#47;                                                                               res0: Array[(Int, String)] = Array((67,the), (63,Spark), (54,a), (51,and), (50,of))</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5e/b2/aceb3e41.jpg" width="30px"><span>Neo-dqy</span> 👍（6） 💬（1）<div>老师我可以再问一下，如果我是用IDEA创建Spark项目，是不是只要配置好Scala的SDK，然后在pom文件中加入对应版本号的spark依赖，就会自动下载spark包了？这个时候不需要再去官网下载spark了吗，同时也不再需要使用spark-shell了吗？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/bd/95/882bd4e0.jpg" width="30px"><span>Abigail</span> 👍（6） 💬（1）<div>前排占座！三年前接触过 Spark 今天从头再学！</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/31/85/5fd92ebe.jpg" width="30px"><span>浮生若梦</span> 👍（4） 💬（4）<div>Java实现：

SparkConf sparkConf = new SparkConf().setAppName(&quot;Test&quot;).setMaster(&quot;local[*]&quot;);
        JavaSparkContext JSC = new JavaSparkContext(sparkConf);

        &#47;&#47; 读取文件内容
        JavaRDD&lt;String&gt; lineRDD = JSC.textFile(&quot;wikiOfSpark.txt&quot;);
        &#47;&#47; 以行为单位做分词
        JavaRDD&lt;String&gt; wordRDD = lineRDD.flatMap(new FlatMapFunction&lt;String, String&gt;() {
            @Override
            public Iterator&lt;String&gt; call(String s) throws Exception {
                return  Arrays.asList(s.split(&quot; &quot;)).iterator();
            }
        });
        JavaRDD&lt;String&gt; cleanWordRDD = wordRDD.filter(new Function&lt;String, Boolean&gt;() {
            @Override
            public Boolean call(String s) throws Exception {
                return !s.equals(&quot;&quot;);
            }
        });

        &#47;&#47; 把RDD元素转换为（Key，Value）的形式
        JavaPairRDD&lt;String, Integer&gt; kvRDD = cleanWordRDD.mapToPair(new PairFunction&lt;String, String, Integer&gt;() {
            @Override
            public Tuple2&lt;String, Integer&gt; call(String s) throws Exception {
                return new Tuple2&lt;String, Integer&gt;(s,1);
            }
        });
        &#47;&#47; 按照单词做分组计数
        JavaPairRDD&lt;String, Integer&gt; wordCounts = kvRDD.reduceByKey(new Function2&lt;Integer, Integer, Integer&gt;() {
            @Override
            public Integer call(Integer integer, Integer integer2) throws Exception {
                return integer+integer2;
            }
        });
        &#47;&#47; 打印词频最高的5个词汇(先将元组的key value交换一下顺序，然后在调用sortByKey())
        wordCounts.mapToPair((row)-&gt;  new Tuple2&lt;&gt;(row._2,row._1)).sortByKey(false).foreach(new VoidFunction&lt;Tuple2&lt;Integer, String&gt;&gt;() {
            @Override
            public void call(Tuple2&lt;Integer, String&gt; stringIntegerTuple2) throws Exception {
                System.out.println(stringIntegerTuple2._1 + &quot;:&quot; + stringIntegerTuple2._2);
            }
        });

        &#47;&#47;关闭context
        JSC.close();</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3a/83/74e3fabd.jpg" width="30px"><span>火炎焱燚</span> 👍（3） 💬（2）<div>Python版代码为：

file=&#39;~~~&#47;wikiOfSpark.txt&#39;
lineRDD=sc.textFile(file)
lineRDD.first() # 会打印出lineRDD的第一行： u&#39;Apache Spark&#39;，如果出错则不打印
wordRDD=lineRDD.flatMap(lambda line: line.split(&quot; &quot;))
cleanWordRDD=wordRDD.filter(lambda word: word!=&#39;&#39;)
kvRDD=cleanWordRDD.map(lambda word:(word,1))
wordCounts=kvRDD.reduceByKey(lambda x,y:x+y)
wordCounts.map(lambda (k,v):(v,k)).sortByKey(False).take(5)</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（3） 💬（1）<div>问下执行 val lineRDD: RDD[String] = spark.sparkContext.textFile(file) 报错error: not found: value spark是怎么回事？</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e6/94/98f30daf.jpg" width="30px"><span>国度</span> 👍（2） 💬（1）<div>2022年2月5号学习打卡记录
机器环境：ROG14
操作系统：win11 + wsl Ubuntu20.04
环境变量：
----------------------------

export SPARK_HOME=&#47;mnt&#47;c&#47;spark&#47;spark-2.4.8-bin-hadoop2.7
export JAVA_HOME=&#47;mnt&#47;c&#47;linux_environment&#47;jdk&#47;jdk1.8.0_321
export M2_HOME=&#47;mnt&#47;c&#47;linux_environment&#47;apache-maven-3.8.4
export SCALA_HOME=&#47;mnt&#47;c&#47;linux_environment&#47;scala3-3.1.1

export PATH=$SPARK_HOME&#47;bin:$SCALA_HOME&#47;bin:$M2_HOME&#47;bin:$JAVA_HOME&#47;bin:$PATH

---------------------------
希望帮助和我一样从零开始一起学习的同学躲避一些坑：

坑1：jdk版本不兼容：
一开始使用jdk17版本，在启动过程中一直报错，降为1.8后启动成功；

坑2：hadoop版本问题：
hadoop3.2.1 逐步使用Dataset，报错类型转换异常；
由于scala经验不足，暂时无法大规模改写老师的代码，降低版本为spark2.4.8
下载地址：https:&#47;&#47;dlcdn.apache.org&#47;spark&#47; 可以选择适合的版本下载

原理性的还没有搞懂，目前在第一阶段，读懂，简单改写为主；

感谢吴磊老师的课</div>2022-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/76/51/96291466.jpg" width="30px"><span>猫太太</span> 👍（2） 💬（1）<div>请问在本地部署spark环境不需要先安装hadoop么</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/46/4a/b0cd391e.jpg" width="30px"><span>巴普洛夫的</span> 👍（1） 💬（2）<div>wordCounts.map{case (k, v) =&gt; (v, k)}.sortByKey(false) 
这一步是做了什么呢，没有见过的语法</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/17/ef/d0a1a069.jpg" width="30px"><span>Z</span> 👍（1） 💬（1）<div>为啥我的结果是单个字母呢？</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（1） 💬（1）<div>注意空格“ ”，和空字符串“”，前者有空格，后者没有

书写的时候，根据自己的文件所在目录来，比如我的是 &#47;input&#47;wikiOfSpark.txt
不要遗漏后缀名。

学习的过程，需要给自己一些耐心和鼓励，一起加油把！</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（1） 💬（1）<div>Spark RDD算子分为Transformation算子和Action算子，Transformation算子基本上都是延迟计算，需要通过调用Action算子进行触发。</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/75/09/464ade1e.jpg" width="30px"><span>Luke Skywalker</span> 👍（0） 💬（1）<div>老师，请问我运行spark-shell总是报这个警告是什么问题呢？搜了好多解决办法也没去掉WARN ProcfsMetricsGetter: Exception when trying to compute pagesize, as a result reporting of ProcessTree metrics is stopped</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（4）<div>关于前几天问的 执行 val lineRDD: RDD[String] = spark.sparkContext.textFile(file) 报错error: not found: value spark 的问题，我确实是在spark-shell执行的，应该不需要显式创建spark-session吧</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/29/8d/2869a10b.jpg" width="30px"><span>zhihui</span> 👍（0） 💬（1）<div>1.
val lineRDD: RDD[String] = spark.sparkContext.textFile(file)
idea中，sparkContext报红，提示 “value sparkContext is not a member of spark”。
但是复制到spark-shell却可以执行。
我是写java的，总觉的这是导包问题，但又找不到这个包。一脸懵。
2. 我按照老师代码写的，一摸一样。执行结果是Array[(Int, String)] = Array((79,&quot;&quot;), (67,the), (63,Spark), (54,a), (51,and))</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/bd/02b20ca1.jpg" width="30px"><span>undefined</span> 👍（0） 💬（1）<div>WordCount中有涉及两类算子，首先是map、filter、flatMap、 reduceByKey、sortByKey、sortBy等转换算子，属于延迟执行，需要另一种行动算子进行触发，行动算子包括：take、count、foreach、collect、first; </div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/83/36ab65ec.jpg" width="30px"><span>keke</span> 👍（0） 💬（3）<div>报错“此时不应有 \spark-3.1.2-bin-hadoop3\bin\..&#39;。”是啥问题呢？</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/c7/66f5fcea.jpg" width="30px"><span>大志</span> 👍（0） 💬（1）<div>Win10系统又装了Hadoop，并下载了winutils.exe这个文件放到Hadoop bin目录下，换成了spark-2.4.6-bin-hadoop2.7运行spark-shell终于不报错了。Windows下文件路径写法val file: String = s&quot;file:&#47;&#47;&#47;D:&#47;wikiOfSpark.txt&quot;</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/15/f7/aba61f1b.jpg" width="30px"><span>JavaXu</span> 👍（0） 💬（1）<div>在macOS上，似乎默认安装了scala。
总之我安装了spark之后，spark-shell，然后键入代码，可以执行并得到结果。

或者是我安装的spark包，里面自带了scala？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/a3/af469d27.jpg" width="30px"><span>Qilin Lou</span> 👍（0） 💬（1）<div>我其实比较喜欢用filterNot，这样里面的函数就不用取反，不过Spark里居然没有提供</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/a3/af469d27.jpg" width="30px"><span>Qilin Lou</span> 👍（0） 💬（1）<div>大意了，没想到用的是一台新电脑，还得先装Java Runtime</div>2021-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/15/39/095dc1c2.jpg" width="30px"><span>Stéphane 胡</span> 👍（0） 💬（5）<div>您好老师，请问一下多久会更新一讲呢？</div>2021-09-06</li><br/><li><img src="" width="30px"><span>杨帅</span> 👍（8） 💬（0）<div>老师，spark-3.2.1 默认从hdfs读取文件，所以rootPath需要加上协议 file:&#47;&#47;.</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/87/669263b4.jpg" width="30px"><span>陈金鑫</span> 👍（4） 💬（0）<div>又学了一遍，wordcount一句话实现：
spark.sparkContext.textFile(file).flatMap(_.split(&quot; &quot;)).filter(!_.equals(&quot;&quot;)).map((_, 1)).reduceByKey(_ + _).map(t =&gt; (t._2, t._1)).sortByKey(false).take(5)</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/c2/33/bd212cb1.jpg" width="30px"><span>ZJ</span> 👍（1） 💬（0）<div>Java Version:

public static void main(String[] args) {
        System.setProperty(&quot;hadoop.home.dir&quot;, &quot;C:\\hadoop&quot;);
        SparkConf conf = new SparkConf().setAppName(&quot;spark-in-Java&quot;).setMaster(&quot;local[*]&quot;);
        JavaSparkContext sc = new JavaSparkContext(conf);
        JavaRDD&lt;String&gt; lineRdd = sc.textFile(&quot;src&#47;main&#47;resources&#47;sparkDev.txt&quot;);
        lineRdd.flatMap(k -&gt; Arrays.asList(k.split(&quot; &quot;)).iterator())
                .mapToPair(k -&gt; new Tuple2&lt;&gt;(k, 1))
                .reduceByKey((k1, k2) -&gt; k1 + k2)
                .mapToPair(tuple -&gt; new Tuple2&lt;&gt;(tuple._2, tuple._1))
                .sortByKey(false).take(10)
                .forEach(k -&gt; System.out.println(k._2 + &quot; has &quot; + k._1));

        sc.close();
    }</div>2023-11-25</li><br/><li><img src="" width="30px"><span>Geek_f09cec</span> 👍（1） 💬（0）<div>将“${解压目录}&#47;bin”配置到 PATH 环境变量。这一步不懂，在哪儿配置，怎么配置呢？</div>2022-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ad/46/f3c56862.jpg" width="30px"><span>🌈你是人间四月天💫</span> 👍（1） 💬（2）<div>像我这种零基础的，看到很懵，第一个demo代码是spark，这个变量怎么来的？这个真的适合零基础？</div>2022-07-04</li><br/>
</ul>