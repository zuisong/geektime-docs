你好，我是王喆。

前面两节课，我们一起学习了从Item2vec到Graph Embedding的几种经典Embedding方法。在打好了理论基础之后，这节课就让我们从理论走向实践，看看到底**如何基于Spark训练得到物品的Embedding向量**。

通过特征工程部分的实践，我想你已经对Spark这个分布式计算平台有了初步的认识。其实除了一些基本的特征处理方法，在Spark的机器学习包Spark MLlib中，还包含了大量成熟的机器学习模型，这其中就包括我们讲过的Word2vec模型。基于此，这节课我们会在Spark平台上，完成**Item2vec和基于Deep Walk的Graph Embedding**的训练。

对其他机器学习平台有所了解的同学可能会问，TensorFlow、PyTorch都有很强大的深度学习工具包，我们能不能利用这些平台进行Embedding训练呢？当然是可以的，我们也会在之后的课程中介绍TensorFlow并用它实现很多深度学习推荐模型。

但是Spark作为一个原生的分布式计算平台，在处理大数据方面还是比TensorFlow等深度学习平台更具有优势，而且业界的很多公司仍然在使用Spark训练一些结构比较简单的机器学习模型，再加上我们已经用Spark进行了特征工程的处理，所以，这节课我们继续使用Spark来完成Embedding的实践。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/e4/a1/2f5b9764.jpg" width="30px"><span>你笑起来真好看</span> 👍（30） 💬（5）<div>transitionMatrixAndItemDis 在生成中这样定义的话，会不会造成dirver端oom？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（27） 💬（3）<div>老师，筛选出来的高分电影有900多部，随机游走出来的序列embdding后，只有500多部，这应该和序列数量，序列长度有关，比如序列数量不够，导致没有覆盖到全部高分电影。实际工作中，像序列数量，序列长度是不是要经过筛选，来保证所有item都会被embdding？</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/96/59/d0b69f85.jpg" width="30px"><span>Huntley</span> 👍（12） 💬（1）<div>想请教下老师，user embedding 也可以用相同的方法获得吗？如何构建用户关系图呢？是不是看过同一部电影的两个用户之间由一条无向边进行连接？和item embedding相比，有什么区别或注意事项吗？</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（10） 💬（3）<div>老师请教下，我对item2vec和Graph Embedding的联系理解是否正确：
1. 联系：item2vec和Graph Embedding 都是为了下一步的相关性矩阵，而一段物品序列
2. 不同： item2vec使用同一用户历史时间序列下的滑动窗口， 而Graph embedding在同一用户的时间序列之上，还应用了不同用户，同一物品之间的图联系，所以说graph embedding可以生成更全面的物品与物品的连接。

所以是否可理解为graph embedding比item2vec的复杂，更完善？业界更流行的是不是想deep walk这种graph embedding的算法？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0e/4a/cc6a2478.jpg" width="30px"><span>白夜</span> 👍（9） 💬（2）<div>老师，randomWalk这部在60核的机器上跑的很慢，，慢到无语，可以优化下吗，transitionMatrixAndItemDis._1与_2的size都是300000</div>2020-10-29</li><br/><li><img src="" width="30px"><span>tuomasiii</span> 👍（6） 💬（1）<div>想问一下在item2vec和graph embedding里面ttl都设置成了24小时，也就是说24小时候后这些embedding就会从redis里面evict掉吗？

还有就是如果有new user和new item我们都是需要train from scratch吗？还是说可以增量训练？</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/90/b3/8828caa4.jpg" width="30px"><span>聪聪呀</span> 👍（6） 💬（2）<div>老师，我最近在研究使用graph embedding ，根据网上的git 代码跑了item2vec，EGES代码，我的推荐场景是视频推荐，同样的训练数据，我发现item2vec 推荐效果较好，但我发现EGES推荐效果不好（只用了ID，没有加其他特征）推荐结果相似度很低。所以想请教您，您觉得可能是什么原因引起的呢，您有没有EGES的demo </div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d1/27/68543b66.jpg" width="30px"><span>W</span> 👍（5） 💬（2）<div>老师你好，不知道我是不是哪里理解错了T_T，新手入门。我的问题是：评分低于3.5的电影被过滤了，相当于电影库里没有低于3.5分的电影，那么也就不会有对应低于3.5分的电影的embedding向量，为什么BatMan的推荐结果里还有低于3.5分的推荐结果呢？</div>2021-06-29</li><br/><li><img src="" width="30px"><span>Geek_ee4f14</span> 👍（5） 💬（1）<div>再请问下老师，游走的时候起始点没有做去重，会不会导致某些爆款成为起始点的概率更高，也不容易游走到冷门物品呀？</div>2021-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/4a/fdae1e16.jpg" width="30px"><span>梁栋💝</span> 👍（5） 💬（1）<div>综上，随机游走因为需要完整转移概率矩阵的原因，受限于转移概率矩阵规模能否容纳到内存中。</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/95/ee/062139f0.jpg" width="30px"><span>王发庆</span> 👍（5） 💬（1）<div>老师，您好，请教您一个问题，在生成Embedding的时候我们都是全量生成的，在生产环境下我们能增量的去生成新节点的Embedding么？</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/eb/a74e5ba6.jpg" width="30px"><span>花花花木兰</span> 👍（4） 💬（1）<div>老师，对于非序列数据用spark的word2vec模型是不是不合适？非序列数据用什么方法训练比较好？例如生鲜配送的场景，用户一次会购买很多菜，这些菜在一个订单中是没有先后时序的。</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/0a/c35f9000.jpg" width="30px"><span>WiFeng</span> 👍（4） 💬（3）<div>你们执行都没有问题吗？

&#47;Users&#47;leeco&#47;github&#47;wzhe06&#47;SparrowRecSys&#47;src&#47;main&#47;java&#47;com&#47;wzhe&#47;sparrowrecsys&#47;offline&#47;spark&#47;embedding&#47;Embedding.scala:34:43
No TypeTag available for scala.collection.Seq[String]
    val sortUdf: UserDefinedFunction = udf((rows: Seq[Row]) =&gt; {</div>2020-10-26</li><br/><li><img src="" width="30px"><span>tuomasiii</span> 👍（3） 💬（1）<div>想请问下老师如果新的user&#47;item加入，embedding matrix形状变大。如果每天都end2end train from scratch，是不是太expensive了？
如果是手动扩容embedding再initialize with昨日的checkpoint继续训练新的user-item interactions，然后时间久一点再train from scratch，行得通吗？
</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/f9/c0a6232c.jpg" width="30px"><span>Capricornus</span> 👍（3） 💬（2）<div>userSeq.select(&quot;movieIdStr&quot;).rdd.map(r =&gt; r.getAs[String](&quot;movieIdStr&quot;).split(&quot; &quot;).toSeq)
老师这里为什么需要转陈Seq，而不使用Array？
    val sortUdf: UserDefinedFunction = udf((rows: Seq[Row]) =&gt; {
      rows.map { case Row(movieId: String, timestamp: String) =&gt; (movieId, timestamp) }
        .sortBy { case (movieId, timestamp) =&gt; timestamp }
        .map { case (movieId, timestamp) =&gt; movieId }
    })
老师这里case的作用是什么？不太能理解。</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（3） 💬（2）<div>下午好，请问老师：
作为推荐系统工程师，在学习代码的时候，除了掌握代码实现了什么，还要把每一句代码的意思弄透彻吗？</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（3） 💬（1）<div>embeddding不可以用tf来求么？</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/12/ea/79effe93.jpg" width="30px"><span>tiger</span> 👍（3） 💬（1）<div>老师，用word2vec利用高评分的做出了的模型（相似推荐）有的物品会找不到，能不能把所有物品one hot编码输入里面，这样是不是就会找到所有的物品了？但是这样做有没有意义？</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/90/00/cfc2b463.jpg" width="30px"><span>萬里長空</span> 👍（3） 💬（2）<div>老师，这里想再问个内存的问题，生产环境中，比如2000万的商品，使用spark-word2vec来训练，维度设置为100，这里driver的内存一般要设置多大啊，我用了36g还是会存在内存问题，但是用gensim的单机训练，不到30g就训练好了</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（3） 💬（1）<div>老师，关于随机游走到下一部电影实现，文稿和github上代码不一致。文稿中这种实现，可以保证游走概率大的电影，优先被游走到嘛
文稿中：
&#47;&#47;从curElement到下一个跳的转移概率向量 
val probDistribution = transferMatrix(curElement) 
val curCount = itemCount(curElement) 
val randomDouble = Random.nextDouble() 
var culCount:Long = 0 
&#47;&#47;根据转移概率向量随机决定下一跳的物品 
breakable { for ((item, count) &lt;- probDistribution) { 
culCount += count
 if (culCount &gt;= randomDouble * curCount)
{ curElement = item 
break } }}
github上：
  val probDistribution = transitionMatrix(curElement)
  val randomDouble = Random.nextDouble()
  breakable { for ((item, prob) &lt;- probDistribution) {
  if (randomDouble &gt;= prob){
       curElement = item
       break
    }</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（3） 💬（3）<div>老师，请问我平时工作中是用PySpark，这节课的代码是不是也都可以用python的来写？有什么好的学习资料来学习怎么把他们翻译成python吗？谢谢老师！！</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/0a/c35f9000.jpg" width="30px"><span>WiFeng</span> 👍（3） 💬（2）<div>由于之前没有实际基础过机器学习开发，请问老师，上面这些代码也是在 spark-shell 中执行吗？</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/55/a3/561138f8.jpg" width="30px"><span>Apache-代蒙</span> 👍（2） 💬（2）<div>老师，我注意到里面有两个参数sampleCount、sampleLength是直接下载代码里面的，这两个参数的取值有什么依据吗</div>2021-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/67/68/6c05da27.jpg" width="30px"><span>泷</span> 👍（2） 💬（1）<div>思考题，变为Node2Wec，主要修改随机游走循环中的probDistribution，根据记录的前驱节点进行修正，p,q为修正权重，然后再归一化概率分布，后续步骤多一个prevElement = curElement。
刚接触scala，如有错误请指正。
var probDistribution = mutable.Map[String, Double]()
  if (prevElement != null) {
    val prevProbDis = transitionMatrix(prevElement)  &#47;&#47;获得前驱节点的“邻接矩阵”行
    var accuP:Double = 0
    var nonNormProb = mutable.Map[String, Double]()
    for ((item, prob) &lt;- transitionMatrix(curElement)) {  &#47;&#47;前驱节点可达，那么距离为1
      if (prevProbDis.contains(item)) {
        nonNormProb(item) = prob
        accuP = accuP + prob
      } else if (item == prevElement) {  &#47;&#47;是前驱节点，那么距离为0
        nonNormProb(item) = prob * (1 &#47; p)
        accuP = accuP + prob * (1 &#47; p)
      } else {  &#47;&#47;其他情况，距离为2
        nonNormProb(item) = prob * (1 &#47; q)
        accuP = accuP + prob * (1 &#47; q)
      }
    }
    for ((item, prob) &lt;- nonNormProb) {  &#47;&#47;归一化概率分布
      probDistribution(item) = prob &#47; accuP
    }
  } else {  &#47;&#47;当前为firstItem，不进行概率修正（偷懒）
    probDistribution = transitionMatrix(curElement)
  }</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b2/56/b71ee269.jpg" width="30px"><span>小灵城</span> 👍（2） 💬（1）<div>想请问下老师，对item2vec来说，同一序列的物品可以两两节对生成输入数据。可是对node2vec需要先生成有向图然后再随机游走，如果只有序列数据但是没有先后（一次订单包含很多物品），这种情况下还可以用node2vec吗</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/eb/a74e5ba6.jpg" width="30px"><span>花花花木兰</span> 👍（2） 💬（1）<div>老师，您介绍的这些embedding都是基于行为序列作为训练数据的。
深度学习中，比如TF中可以利用embedding层可以将one-hot向量或者multil-hot向量进行embedding转换，这两个有什么区别吗？是不是可以把TF的embedding层理解为word2vec模型的隐藏层？</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/99/f0/ba3c0208.jpg" width="30px"><span>Geek_63ee39</span> 👍（2） 💬（1）<div>请教一下老师，从效率角度上讲，可以把转移矩阵transferMatrix放在executor端进行分布式随机游走吧，因为这是可以并行计算的。</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/6a/d3/294cb209.jpg" width="30px"><span>FruitDealer</span> 👍（1） 💬（1）<div>王喆老师，想要请教一下有关上下文特征这块的内容，因为没有进行过实际的推荐项目，所以上下文特征的应用上面有些想不明白。

问题是：训练阶段和预测阶段的上下文中的时间应该怎么取？

我的疑点是训练阶段时间应该用户历史点击&#47;订购（假如是一个产品推荐的场景）行为发生的时间，但是在预测阶段，对于召回的那些候选产品，这里的上下文特征中的时间是不是应该取当前用户操作的时间呢？如果是的话，这个时间感觉意义不太大。如果用最后一次点击&#47;订购产品的时间点作为上下文特征的话，预测数据中召回的那些没产生过订购行为的产品中的时间又如何取值呢？感觉训练数据和预测数据中存在一些gap</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e2/4e/c3e86856.jpg" width="30px"><span>笑笑是个好孩子</span> 👍（1） 💬（1）<div>item2vec的序列处理那块 为什么只看一个用户打分比较高的电影作为序列呀 为什么不把电影的rating作为序列呢？ 就是行是uid 列是电影id 具体的数据是某用户对于某电影的打分呢？</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/a6/f7/e434c375.jpg" width="30px"><span>Sean</span> 👍（1） 💬（1）<div>王喆老师你好，想请问Item2vec观念上的问题
根据我的了解，word2vec是藉由大量文章透过上下文来学习每个词的含义，例如「我是一名学生」和「他是一名工程师」，word2vec可以判断这两句有相似的句型，得知（我,他）是相似的，（学生,工程师）是相似的（都是一种职业）。
但是用户的浏览纪录可能是随机的，例如在网路商城的使用情境下，用户A的浏览顺序为(手机、耳机、电脑、保温杯)，用户B的浏览顺序为(手机、耳机、电脑、平底锅)，我们不能说(保温杯,平底锅)是相似的，但在word2vec演算法的逻辑下，因为他们的上下文一样，所以很可能会被模型认为是相似的？
不知道我有没有理解错误，如果是这样的话那该如何保证Item2vec是有效的呢？谢谢老师！</div>2021-04-30</li><br/>
</ul>