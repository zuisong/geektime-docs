你好，我是吴磊。

积累了一定的理论基础之后，今天我们继续来学习RDD常用算子。在[RDD常用算子（一）](https://time.geekbang.org/column/article/418079)那一讲，我们讲了四个算子map、mapPartitions、flatMap和filter，同时留了这样一道思考题：“这些算子之间，有哪些共同点？”

今天我们就来揭晓答案。首先，在功能方面，这4个算子都用于RDD内部的数据转换，而学习过Shuffle的工作原理之后，我们不难发现，这4个算子当中，没有任何一个算子，会引入Shuffle计算。

而今天我们要学习的几个算子则恰恰相反，它们都会引入繁重的Shuffle计算。这些算子分别是groupByKey、reduceByKey、aggregateByKey和sortByKey，也就是表格中加粗的部分。

我们知道，在数据分析场景中，典型的计算类型分别是分组、聚合和排序。而groupByKey、reduceByKey、aggregateByKey和sortByKey这些算子的功能，恰恰就是用来实现分组、聚合和排序的计算逻辑。

![图片](https://static001.geekbang.org/resource/image/c9/fc/c97a717512897749d5db659fb583c8fc.jpg?wh=1597x1977 "RDD算子分类表")

尽管这些算子看上去相比其他算子的适用范围更窄，也就是它们只能作用（Apply）在Paired RDD之上，所谓Paired RDD，它指的是元素类型为（Key，Value）键值对的RDD。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epGTSTvn7r4ibk1PuaUrSvvLdviaLcne50jbvvfiaxKkM5SLibeP6jibA2bCCQBqETibvIvcsOhAZlwS8kQ/132" width="30px"><span>Geek_2dfa9a</span> 👍（21） 💬（3）<div>最近公司在搞黑客马拉松，我忙于做一个数仓血缘图计算的项目来晚啦。
reduceByKey和aggregateByKey底层使用了同一个方法实现：combineByKeyWithClassTag，该方法是将KV型的RDD[(K, V)]转换为RDD[(K, C)]，
类似于分组聚合，既然要找到reduceByKey和aggregateByKey的联系那肯定要从下至上由共性开始分析，combineByKeyWithClassTag方法声明如下：
  def combineByKeyWithClassTag[C](
      createCombiner: V =&gt; C,
      mergeValue: (C, V) =&gt; C,
      mergeCombiners: (C, C) =&gt; C,
      partitioner: Partitioner,
      mapSideCombine: Boolean = true,
      serializer: Serializer = null)(implicit ct: ClassTag[C]): RDD[(K, C)] = self.withScope {
  }
字数限制了，我把方法实现放在下面评论。
首先讲三个高阶函数入参：createCombiner，mergeValue，mergeCombiners数，在方法里组成了Aggregator对象，Aggregator
其实就是spark对分组聚合（Shuffle）操作的抽象，如果不清楚spark分组聚合的过程这三个高阶函数不好理解，简单点讲，RDD按照Key分组后因为
不同Partition里会有相同Key，因此对于Key=k1这个大组会有多个小组（k11,k12...k1n）,首先createCombiner会给k11,k12...k1n）
每个小组赋一个初始值C0，然后mergeValue把小组内的每个记录叠加给初始值得到一个小组值C00（其实就是map端聚合），最后再把所有小组的
小组值合并成一个KV型RDD（注意这里V已经变成了C类型）。
再讲参数partitioner，了解RDD的话应该清楚，就是这个RDD的分区规则，这里的入参就是聚合后RDD的分区规则，如果相同的话，那Shuffle就完全不需要了，
直接task本地聚合一下就好了，源码里也就直接mapPartitions就结束了，如果聚合前后分区规则不相同的话，那么就会返回一个ShuffledRDD。
最后讲下参数mapSideCombine和serializer，mapSideCombine就是是否在map端聚合，方法开头的校验可以看到keyClass是数组时不支持
map端聚合和哈希分区，这里是为什么呢？不太熟悉scala的我查了下stackoverflow，原来scala里的数组和Java的一样，hashcode只是数组对象本身的
hashcode，和内容没关系，那自然没办法map端聚合了，
这里请问老师，那数组作为KVRDD的时候，reduce端的聚合是怎么完成判等的呢？
serializer是指出数据如何序列化的，序列化就先不说了，不然又要讲好多。

最后总结下，reduceByKey和aggregateByKey底层实现完全相同，都是combineByKeyWithClassTag，只不过reduceByKey调用
combineByKeyWithClassTag的入参mergeValue和mergeCombiners是相等的，aggregateByKey是用户指定可以不等的，也就是说
reduceByKey是一种特殊的aggregateByKey。</div>2021-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKIkpsQkTyLtfxgib35o0ho9nWmCHwJL8BYibJPPT22fkT1aTwHhwQc0krINWjTVRjibF1bMTgia5mflg/132" width="30px"><span>Geek_2a0deb</span> 👍（2） 💬（1）<div>reduceByKey 和 aggregateByKey的区别在于reduceByKey在map端和reduce时的聚合函数一致，而aggregateByKey在map端和reduce端聚合函数可以不一致，联系就是reduceByKey可以认为是一种特殊的aggregateByKey（map和reduce是同一个函数）如果用算子来描述:reduceByKey(f)=aggregateByKey(初始值) (f,f)</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8e/d3/1a3bb2cc.jpg" width="30px"><span>Botanic</span> 👍（0） 💬（1）<div>```
# 使用 aggregateByKey 来实现 reduceByKey
def f1(x, y):
    # 显示定义Map阶段聚合函数f1，求加和
    return x+y

import random
# 实验3：aggregateByKey 使用说明
textFile = SparkContext().textFile(&quot;..&#47;wikiOfSpark.txt&quot;)
wordCount = (
            textFile.flatMap(lambda line: line.split(&quot; &quot;))
                .filter(lambda word: word != &quot;&quot;)
                    .map(lambda word: (word, 1))
                        .aggregateByKey(0, f1, f1)
                            .sortBy(lambda x: x[1], False)
                                .take(5))
print(wordCount)
```</div>2021-12-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/wgMMrp1hvSB3E30KqZvMsj3KQdAI3T1uQM77LT7hZ65nVSjPGRg3AbUOyiahnssA6AIT5PAkyHFmlTBzUH9gdyQ/132" width="30px"><span>pythonbug</span> 👍（0） 💬（1）<div>我感觉aggregateByKey直接作用在刚刚读取数据的RDD上的情况很少，因为刚刚从数据源读取出来的数据分区大多数时候是没啥业务含义的，所以Map阶段的聚合也没有太大意义。所以猜测，aggregateByKey可能大多数情况是跟在reduceByKey之后，那个时候已经对数据按照业务分区好了。那个时候Map阶段的聚合才有一些意义，不知道猜的对不对</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/06/9d/3c121a1c.jpg" width="30px"><span>十年</span> 👍（0） 💬（2）<div>请问老师，aggregateByKey的初始值有什么作用？</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（0） 💬（1）<div>reduceByKey 和 aggregateByKey的联系：将相同的key值进行聚合。不同点：reduceByKey()采用的是相同的func，在map阶段使用sum操作，reduce阶段采用max操作就不满足。
aggregateByKey可以看做是更一般的reduceByKey，
</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/b3/931dcd9e.jpg" width="30px"><span>J</span> 👍（1） 💬（0）<div>讲解aggregateByKey计算过程时，图例错写成了“reduceByKey计算过程”</div>2022-08-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIxKpBQJbxHFG9Wjk73WkbqcGeDrjzwjPSDzLlm8C80U9dVmByrrmBa3LmIoCYUW2H3thj5VfMvGQ/132" width="30px"><span>jasonde</span> 👍（0） 💬（0）<div>能否帮忙举个例子，什么情况可以用reduce by key， 什么情况只能用aggregate by key ，用python 代码，劳烦了</div>2024-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/52/9c/8a60675c.jpg" width="30px"><span>睿晞</span> 👍（0） 💬（0）<div>aggregateByKey算子中第一个默认参数的使用方法是什么啊？是直接参与到第二个聚合函数（reduce端）里面运算吗？比如，默认参数是0，然后如果第二个聚合函数是max求最大值，初始默认参数是参与比较的，用0和每个字段中的值比较，是这个意思吗？</div>2022-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（0） 💬（1）<div>Java实现代码
https:&#47;&#47;github.com&#47;Spoon94&#47;spark-practice&#47;blob&#47;master&#47;src&#47;main&#47;java&#47;com&#47;spoon&#47;spark&#47;core&#47;AggOpJob.java</div>2022-03-27</li><br/>
</ul>