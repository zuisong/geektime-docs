你好，我是吴磊。

在日常的开发工作中，我发现有个现象很普遍。很多开发者都认为Spark的执行性能已经非常强了，实际工作中只要按部就班地实现业务功能就可以了，没有必要进行性能调优。

你是不是也这么认为呢？确实，Spark的核心竞争力就是它的执行性能，这主要得益于Spark基于内存计算的运行模式和钨丝计划的锦上添花，以及Spark SQL上的专注与发力。

但是，真如大家所说，**开发者只要把业务逻辑实现了就万事大吉了吗**？这样，咱们先不急于得出结论，你先跟着我一起看两个日常开发中常见的例子，最后我们再来回答这个问题。

在数据应用场景中，ETL（Extract Transform Load）往往是打头阵的那个，毕竟源数据经过抽取和转换才能用于探索和分析，或者是供养给机器学习算法进行模型训练，从而挖掘出数据深层次的价值。我们今天要举的两个例子，都取自典型ETL端到端作业中常见的操作和计算任务。

## 开发案例1：数据抽取

第一个例子很简单：给定数据条目，从中抽取特定字段。这样的数据处理需求在平时的ETL作业中相当普遍。想要实现这个需求，我们需要定义一个函数extractFields：它的输入参数是Seq\[Row]类型，也即数据条目序列；输出结果的返回类型是Seq\[(String, Int)]，也就是（String, Int）对儿的序列；函数的计算逻辑是从数据条目中抽取索引为2的字符串和索引为4的整型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/42/6e3be953.jpg" width="30px"><span>Will</span> 👍（19） 💬（5）<div>第二个例子，可以利用map join，让小数据分发到每个worker上，这样不用shuffle数据</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（18） 💬（4）<div>请问磊哥，spark里面nested loop join和cartesian product jion有什么区别？</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（13） 💬（3）<div>1. 其实有很多，比如用foreach算子将数据写入到外部数据库，导致每条数据的写入都会建立连接，另外单条写入也比批量写入的性能差很多。建议使用foreachPartition()，每个分区建立一个连接，同时可以批量写入，性能会好很多。
2. 一般来讲，小表与大表的关联操作，首先要考虑Broadcast Join


另外，关于Nested Loop Join的原理：https:&#47;&#47;www.geeksforgeeks.org&#47;join-algorithms-in-database&#47;amp&#47;
</div>2021-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/80/59f1886d.jpg" width="30px"><span>TaoInsight</span> 👍（12） 💬（6）<div>如果pai rDF的startDate和endDate范围有限，可以把日期范围展开，将非等值join转成等值join</div>2021-03-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IcDlyK6DaBrssVGlmosXnahdJ4bwCesjXa98iaapSDozBiagZTqSCok6iaktu2wOibvpNv9Pd6nfwMg7N7KTSTzYRw/132" width="30px"><span>慢慢卢</span> 👍（7） 💬（3）<div>老师，我把第二个例子自己试了一遍，有个问题不理解：两个df都只有一条数据，sparkui上第二个stage有200个task，为什么shuffle之后的stage的task有200个，虽然说shuffle之后reduce默认并行度是200，但我只有一条数据，实际上只需要一个task啊，其他的task是怎么产生的？</div>2021-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/b7/abb7bfe3.jpg" width="30px"><span>Elon</span> 👍（5） 💬（1）<div>函数式的副作用指的是不修改入参吧？在函数内部是可以定义变量、修改变量的。因此fields变量在函数内部，应该不算副作用吧？</div>2021-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6uQj0EmXTGstVxNicLWqJhGvY0tavWvxK5RwgxjaMK1rNB9Rf7kAdnzBnG7YOicHjTibOf6G6HEFwonRFXDN3Pp8A/132" width="30px"><span>葛聂</span> 👍（4） 💬（4）<div>Case 1为什么性能差一倍呢</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（3） 💬（6）<div>请问老师，这个课程需要哪些基础，我平时使用过pysaprk 做过一些机器学习相关数据处理练习，对于我这种使用spark不多的，可以消化吸收嘛</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/8e/a7/92d1b90e.jpg" width="30px"><span>浩然</span> 👍（2） 💬（1）<div>简单啊。那个时间区间的，罗列出来，广播一下就完事了。从nest loop到hash join的跨越。
我之前做Oracle优化的，所以第一反应是哈希join，第二反应是不等值到等值。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（2） 💬（2）<div>可以先将pairdf collect到driver，再将数组按照startdate排序，然后再将其广播。然后在factdf.map里面实现一个方法来从广播的数组里面二分查找到eventdate所属的时间对子。最后就可以根据这个时间对子以及其他的维度属性进行分组聚合了</div>2021-03-15</li><br/><li><img src="" width="30px"><span>Geek_92df49</span> 👍（2） 💬（10）<div>四个维度分组为什么要加上开始时间和结束时间？
.groupBy(&quot;dim1&quot;, &quot;dim2&quot;, &quot;dim3&quot;, &quot;event_date&quot;, &quot;startDate&quot;, &quot;endDate&quot;)</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f5/d9/345d743d.jpg" width="30px"><span>刘吉超</span> 👍（1） 💬（2）<div>我们每天有9T数据，用如下代码做ETL  json平铺，花很长时间
val adArr = ArrayBuffer[Map[String, String]]()
if (ads != null) {
  val adnum = ads.length
  for (i &lt;- 0 until adnum) {
    val addObj = ads.getJSONObject(i)
    val adMap = THashMap[String, String]()
    addObj.entrySet().foreach(x =&gt; adMap += (x.getKey -&gt; (if(x.getValue==null) &quot;&quot; else x.getValue.toString )  ))
    adArr += adMap.toMap
  }
}
基于老师讲的，避免副作用，改为如下代码
import org.apache.flink.streaming.api.scala._
import scala.collection.JavaConversions._
 val adArr = (0 until ads.size()).map(i =&gt; ads.getJSONObject(i).toMap.map(entry =&gt; entry._1 -&gt; (if(entry._2==null) &quot;&quot; else entry._2.toString)))
尝试后没啥效果，希望老师指导一下</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（1）<div>同一个application如果action多的话一定会影响效率吗？</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（4）<div>老师我把所有课程看了一遍还是不太理解为什么例2 正例的性能更高（捂脸）；如果spark不能根据日期范围对fairDF做过滤提前去掉一部分的话 不管是fairDF left join factDF还是factDF left join fairDF还是反例的代码，感觉时间复杂度都是 size(fairDF)*size(factDF) 啊。。。虽然数据是分布在不同节点中但是NLJ的算法不是对于factDF中每条记录都遍历一遍fairDF吗？希望老师能解答一下嘤嘤嘤</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/4b/16ea3997.jpg" width="30px"><span>tiankonghewo</span> 👍（0） 💬（2）<div>&quot;尽管 Nested Loop Join 是所有 Join 实现方式（Merge Join，Hash Join，Broadcast Join 等）中性能最差的一种，而且这种 Join 方式没有任何优化空间，但 factDF 与 pairDF 的数据关联只需要扫描一次全量数据&quot;, 
对于这一段话,感觉解释的不好, Nested Loop Join 是两个for循环, 时间复杂度应该也是M*N, 如果factDF只需要扫码一遍全量数据,那么pairDF需要扫描的次数也不会少,
两个for循环,时间复杂度怎么都是M*N, 那么节约下来的时间,相比第一种foreach方式,应该是从磁盘中拉取的时间

</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/1a/f2c8988b.jpg" width="30px"><span>萝莉巴索小布丁</span> 👍（0） 💬（1）<div>老师，我看了下nested loop join的原理，查找次数应该为外层循环的次数呀，为什么你说只全表扫描一次呢？</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/eb/b6/e7f8956a.jpg" width="30px"><span>雁归来🍁</span> 👍（0） 💬（1）<div>我有2个问题想请教一下老师：
第一个：我们现在生产用sparkSQL去做SQL分析，一张4千万数据左右的表去left join 一张50万的表和几张几万数据的表，要花费半个小时，这个正常吗？然后把得到的近800万的数据写入TIDB又花费半个小时，这个是不是正常的时效啊？，但是用MPP数据库如impala,hive等几分钟就全搞定了。
第二个：有5张700万左右数据的表做left join的话sparkSQL经常会OOM，然后调大内存后要跑1个小时才能出结果，是不是sparkSQL在大表关联大表方面性能很差啊？</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/39/68/56dfc8c0.jpg" width="30px"><span>子兮</span> 👍（0） 💬（1）<div>老师，案例二，正例中用的join，会做shuffle ,反例是做遍历，大数据下，会不会不做shuffle 更好？</div>2021-10-09</li><br/><li><img src="" width="30px"><span>边边爱学习</span> 👍（0） 💬（2）<div>(1) select partition_col from table1 where partition_col in (select partition_col from table2 where partition_col between 1 and 10)
(2) select partition_col from table1 inner join (select partition_col from table2 where partition_col between 1 and 10) r on table1.partition_col = r.partition_col
（1）全表scan，没有非常慢
（2）指定分区scan
为啥会这样呢</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/2c/900cb4f0.jpg" width="30px"><span>方得始终</span> 👍（0） 💬（1）<div>错过了老师上星期的直播，请问在哪里可以看到回放吗？</div>2021-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/2c/900cb4f0.jpg" width="30px"><span>方得始终</span> 👍（0） 💬（3）<div>代码会集中放到GitHub上面吗？这样方便于以后学习查找。我主要用 pyspark, 这个课程只用Scala吗？请问有关于Scala spark的入门教程吗？</div>2021-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrZb9pm07aicqH4rErIanMN5owmsBO6rWa6VSkpFMFjVRKOKkNM6JEf2gvQ2g23xUiammg7PUykJFA/132" width="30px"><span>天渡</span> 👍（0） 💬（1）<div>可否将小表进行broadcast，将reduce端join变为map端join。</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/47/ba/d36340c1.jpg" width="30px"><span>Shockang</span> 👍（0） 💬（1）<div>Case1里面除了老师讲的副作用外，我认为Scala在处理闭包时也会存在一定的性能损耗，Case2里面把大变量广播出去是一种常见的操作，另外，filter之后加上coalesce 也是比较常见的优化手段</div>2021-03-16</li><br/><li><img src="" width="30px"><span>rb@31</span> 👍（0） 💬（1）<div>另外，不知道老师的更新频率。大概多久能全部更新好？</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/53/d6a1f585.jpg" width="30px"><span>光羽隼</span> 👍（1） 💬（0）<div>1、case 2 问题的关键应该是在于计算发生位置在哪里，反例中逻辑计算发生的位置是driver端，pairDF每循环一次都要把factDF拉到driver遍历一遍，一个factDF很大，拉取一遍就是一次IO的开销。正例中如果把pairdf广播到多个executor中，让计算发生在executor中，那么io开销就变小了。即时NLJ不是一个好的join实现机制，但是在次之前优化已经实现了。
2、TaoInsight：如果pai rDF的startDate和endDate范围有限，可以把日期范围展开，将非等值join转成等值join；
    以文中的例子，如果pairDF的一条记录是(startDate, endDate) = (&quot;2021-01-01&quot;, &quot;2021-01-31&quot;)，explode成31条，(startDate, endDate, eventDate) = (&quot;2021-01-01&quot;, &quot;2021-01-31&quot;), &quot;2021-01-01&quot;),(&quot;2021-01-01&quot;, &quot;2021-01-31&quot;, &quot;2021-01-02&quot;), ... ,(&quot;2021-01-01&quot;, &quot;2021-01-31&quot;, &quot;2021-01-31&quot;), 这样就可以基于eventDate字段进行等值关联。
数据会有N倍的膨胀，不过只要N不太大，也可以这么搞 
这位大佬的思路很厉害，将pairdf每条数据按照时间范围扩大，pairDF一张表几百条数据，扩大几百倍也就几万几十万的数据，也是可以实现广播的。而且将数据扩大的另一个好处就是避免了NLJ，就可以实现等值i关联，那么1中说的NLJ性能不好的问题也解决了。</div>2024-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/97/2e/c2b19350.jpg" width="30px"><span>LeoJC</span> 👍（0） 💬（0）<div>晚来的学习，感谢有你！针对第二个例子，如果pairDF数据过大，我有个想法是：把pairDF中时间转成时间戳再排序，然后按照某个阈值大小分桶，最终转换成map数据结构（key表示bucket index，value则记录原始日期段）再广播出去，fackDF每条记录遍历时按照同样的分桶算法拿到bocket index,就可以快速进行关联碰撞了。这样子一来，降低了参与计算的数据量。....不知道这想法中，有没有什么隐藏的性能问题呢？望指导</div>2023-07-24</li><br/><li><img src="" width="30px"><span>Geek_6bf244</span> 👍（0） 💬（0）<div>我有个最近有个地方用了nested loop join，跑得有点慢，不用的话sql会写的非常长，真的一点优化空间没有吗</div>2023-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/16/bedf7932.jpg" width="30px"><span>阿奎</span> 👍（0） 💬（0）<div>老师您好，我最近遇到一个奇怪的问题。我直接登录终端去执行spark submit任务可以执行成功，我在项目里是模仿的小海豚调度器在程序里去拼接的spark submit脚本然后生成的shell脚本，通过sudo -u  hadoop集群的租户  sh command去执行的，这种方式提交的任务如果任务数据量小可以执行成功，任务数据量大就会失败，提示applicationmaster 接受到了kill的信号</div>2022-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ugib9sF9icd9dhibQoAA025hibbD5zgZTiaddLoeEH457hrkBBhtQK6qknTWt270rHCtBZqeqsbibtHghgjdkPx3DyIw/132" width="30px"><span>唐方刚</span> 👍（0） 💬（1）<div>弱弱的问个问题，val extractFields: Seq[Row] =&gt; Seq[(String, Int)] = {}，一般定义方法，冒号后面不是返回值么，怎么这里冒号后面参数和返回值都有</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/1f/a2/0ac2dc38.jpg" width="30px"><span>组织灵魂 王子健</span> 👍（0） 💬（0）<div>看到一个数据量大另一个数据量小，立刻马上就会想到广播变量。还有优化部分write用到了partitionBy这个细节必须注意</div>2022-06-20</li><br/>
</ul>