你好，我是蔡元楠。

上一讲中，我们介绍了Spark中的流处理库Spark Streaming。它将无边界的流数据抽象成DStream，按特定的时间间隔，把数据流分割成一个个RDD进行批处理。所以，DStream API与RDD API高度相似，也拥有RDD的各种性质。

在第15讲中，我们比较过RDD和DataSet/DataFrame。你还记得DataSet/DataFrame的优点吗？你有没有想过，既然已经有了RDD API，我们为什么还要引入DataSet/DataFrame呢？

让我们来回顾一下DataSet/DataFrame的优点（为了方便描述，下文中我们统一用DataFrame来代指DataSet和DataFrame）：

- DataFrame 是**高级API**，提供类似于**SQL**的query接口，方便熟悉关系型数据库的开发人员使用；
- **Spark SQL执行引擎会自动优化DataFrame程序**，而用RDD API开发的程序本质上需要工程师自己构造RDD的DAG执行图，所以依赖于工程师自己去优化。

那么我们自然会想到，如果可以拥有一个基于DataFrame API的流处理模块，作为工程师的我们就不需要去用相对low level的DStream API去处理无边界数据，这样会大大提升我们的开发效率。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/2b/3ab96998.jpg" width="30px"><span>青石</span> 👍（14） 💬（0）<div>watermark，process time - event time &gt; watermark则直接丢失，process time - event time 
&lt; watermark则接收数据处理，更新结果表。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/ff/2a27214e.jpg" width="30px"><span>se7en</span> 👍（12） 💬（2）<div>同样都是微批处理，为什么spark streaming 就不能处理微秒，而structure streaming就可以</div>2019-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/89/29/1fba918b.jpg" width="30px"><span>彭琳</span> 👍（10） 💬（0）<div>关于思考题……据说是有水印机制，跟踪数据的事件时间，阈值内的延迟数据将会被聚合，比阈值更延迟的数据将被删除，在内存中留有一个中间状态。若有不对，请指正；不过推荐看一下这篇文章《Spark 2.3.0 Structured Streaming详解》，相当于官网翻译：https:&#47;&#47;blog.csdn.net&#47;l_15156024189&#47;article&#47;details&#47;81612860</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/71/a52ac5c1.jpg" width="30px"><span>大大丸子🍡</span> 👍（8） 💬（0）<div>1、Structured Streaming是基于事件事件处理，而不是处理事件，所以，延迟接收的数据，是能被统计到对应的事件时间窗口的
2、设定数据延迟的窗口时间阈值，通过判断阈值来决定延迟数据是否需要纳入统计；这个阈值的设定可以避免大量数据的延迟导致的性能问题</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/a0/f83416e9.jpg" width="30px"><span>向黎明敬礼</span> 👍（4） 💬（0）<div>withWatermark函数第一个参数是 数据表中的时间戳字段的字段名，第二个参数是延迟的时间阈值</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（4） 💬（0）<div>我不确定有没有完全理解问题..

我想大概是因为，输出时间所对应的窗口可以故意设置的比输出时间稍微早一点，这样可以对数据延迟有一定的抗性。不然例子中的1:09分的数据就没机会被使用了。

不过相应的，这样的机制似乎终究是个妥协，妥协的越大，实时性就越差。</div>2019-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mHibFJhnKJC5wRazXPevbWoRbMkCaJibzSekf3DoJAGygHgXKVIO6zK37e1LVLzpUI7iaER8W93dqyTmQmmuIC4rg/132" width="30px"><span>Geek_86e573</span> 👍（3） 💬（1）<div>用过才知道，这个东西目前坑还挺多</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（2） 💬（0）<div>各个类的继承关系最好画一个图，不然在这几个章节打转搞得有点晕</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（2） 💬（0）<div>spark structure streaming有没有类似flink的sideOutput机制？支持超过watermark的事件被处理到</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/49/e94b2a35.jpg" width="30px"><span>CoderLean</span> 👍（1） 💬（0）<div>最后的思考题只知道flink有一个watermark机制可以保证</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（0）<div>一般是处理滞后一定时间的数据，超过了这个时间范围，就会舍弃</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/29/56db1441.jpg" width="30px"><span>兴趣 e 族</span> 👍（1） 💬（0）<div>我知道在flink中可以通过watermark来处理这样的场景，在Structured Streaming中应该也是这样的方式来处理吧。</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/05/67aae6c8.jpg" width="30px"><span>Rainbow</span> 👍（1） 💬（0）<div>10分钟统计一次，按照处理时间分1:00-1:10，1:10-1:20；所以单词的处理时间位于第二个区间会被第二次统计到；如果按照事件时间，sql里time&gt;1:00 and time&lt;1:10就可以把单词归类到第一个区间，这么理解对吗，老师？</div>2019-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（0）<div>选择更新模式是不是就可以解决解决这个问题呢， </div>2020-03-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJtr0Mee6woib9x0EHPEXh7Or4ZSUicVJgBfskSZZ3zrxAeCqcAselFIZk8uAmSNVDiadBSWyhMiaqL6Q/132" width="30px"><span>.</span> 👍（0） 💬（0）<div>各位大佬好，流式处理应该消息应该只被消费一次吧，waterMark机制可以确保在1:20输出，什么情况下在1:10输出了对应的结果呢？求解。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/ad/faf1bf19.jpg" width="30px"><span>windcaller</span> 👍（0） 💬（0）<div>我用那个withWaterMark限制时间窗口进行思考题中的数据过滤时候，就感觉怪怪的，有时候放弃掉，有时候就怎么都不放弃，一直不太理解这块内容
</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b6/2e/096790e1.jpg" width="30px"><span>淹死的大虾</span> 👍（0） 💬（0）<div>structure streaming相当于一直在更新输出一个表，这个表有事件时间信息，所以可以按事件时间处理；spark streaming只能按处理时间来的rdd处理，缺少一个汇总</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/b6/3d8fcc2c.jpg" width="30px"><span>张凯江</span> 👍（0） 💬（0）<div>输出模式支持呀。
完全模式和更新模式哈。</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（0） 💬（0）<div>我觉得可能是通过冗余计算上一个时间窗口中的数据来实现的。
局限性就是不支持迟到太久的数据</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/69/3dea1b7d.jpg" width="30px"><span>周凯</span> 👍（0） 💬（0）<div>程序在1:10处理的是1:09之前生成的数据，往后推10分钟，那1:20处理的是1:19之前生成的数据</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/77/45e5e06d.jpg" width="30px"><span>胡鹏</span> 👍（0） 💬（0）<div>老师, 我最近遇到个问题还望帮忙提点一下:
1. 需求: 统计实时订单量(类似)
2. 通过maxwell读取binlog数据同步到kafka
3. spark-streaming处理kafka里面的数据
4. spark-sql定义不同的实时报表

这样做的时候, 对于不同sql定义的报表我就懵了, 
   假如昨天需求方写了10个SQL放到数据库, 然后我们启动流计算, 提交job到spark, 那么10个实时的报表就开始变动起来了
   但是今天需求方说, 这里还有两个指标需要统计一下, 就给我了2条SQL,

(先说明下前提, maxwell把mysql的数据提取出来提交到了一个kafka的topic里面)
疑问点出来了: 
    1. 如果从新提交一个2条sql的job, 就得独立消费kafka数据, 否则数据有遗漏,  (相当于一条河流, 做了多个截断),     与其对比的是: 在之前提交10个SQL的job中, 先写好SQL来源是动态从某个数据库某张表取出来的, 然后数据流来了直接共享server进行计算,    (相当于一条河流一次截断, 多个筛选, 复用了job的提交和kafka消费这一步),  不知道后者是否可行, 或是有什么坑? 
    2. 假如选择了问题1 的第一种情况, 且假如重复消费很消耗新能,  然后我想到了替代方案,不同的数据库binlog放到不同的kafka的topic中,  计算出结果之后再聚合, (这样做缺点是不是就是开发程序非常麻烦呢)?

目前存在如上两个疑问, 我目前觉得第一个问题的第二种情况比较靠谱, 希望可以求证, 或者我原本思考方向就是错的,     还望老师帮忙指点一下</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/18/3596069c.jpg" width="30px"><span>RocWay</span> 👍（0） 💬（0）<div>我的理解是：虽然设立了窗口，但是有些事件可能由于网络或其他原因迟到了，这些迟到的事件也要被计算在内。否则这段窗口内的数据计算就会“不准”。当然也不能无限允许迟到，所以Spark也设立了watermark。如果窗口的结束时间减去watermark，比某个事件的时间还“晚”，那这个事件就不能算在这个窗口里。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ec/ef/99f8dc7b.jpg" width="30px"><span>安</span> 👍（0） 💬（0）<div>因为1:20是处理时间，1:09是事件时间，1点20输出数据的事件时间还没到1点20。是这样吗？不太确定</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/5e/79dd13b5.jpg" width="30px"><span>Cyber_Derek</span> 👍（0） 💬（0）<div>不知道老师能否也讲解一些关于flink方面的东西呢？</div>2019-05-27</li><br/>
</ul>