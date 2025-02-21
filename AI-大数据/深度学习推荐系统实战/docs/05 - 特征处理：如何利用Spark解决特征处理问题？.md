你好，我是王喆。

上节课，我们知道了推荐系统要使用的常用特征有哪些。但这些原始的特征是无法直接提供给推荐模型使用的，因为推荐模型本质上是一个函数，输入输出都是数字或数值型的向量。那么问题来了，像动作、喜剧、爱情、科幻这些电影风格，是怎么转换成数值供推荐模型使用的呢？用户的行为历史又是怎么转换成数值特征的呢？

而且，类似的特征处理过程在数据量变大之后还会变得更加复杂，因为工业界的数据集往往都是TB甚至PB规模的，这在单机上肯定是没法处理的。那业界又是怎样进行海量数据的特征处理呢？这节课，我就带你一起来解决这几个问题。

## 业界主流的大数据处理利器：Spark

既然要处理海量数据，那选择哪个数据处理平台就是我们首先要解决的问题。如果我们随机采访几位推荐系统领域的程序员，问他们在公司用什么平台处理大数据，我想最少有一半以上会回答是Spark。作为业界主流的大数据处理利器，Spark的地位毋庸置疑。所以，今天我先带你了解一下Spark的特点，再一起来看怎么用Spark处理推荐系统的特征。

Spark是一个分布式计算平台。所谓分布式，指的是计算节点之间不共享内存，需要通过网络通信的方式交换数据。Spark最典型的应用方式就是建立在大量廉价的计算节点上，这些节点可以是廉价主机，也可以是虚拟的Docker Container（Docker容器）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（78） 💬（5）<div>Normalizer、StandardScaler、RobustScaler、MinMaxScaler 都是用让数据无量纲化
Normalizer:  正则化；（和Python的sklearn一样是按行处理，而不是按列[每一列是一个特征]处理，原因是：Normalization主要思想是对每个样本计算其p-范数，然后对该样本中每个元素除以该范数，这样处理的结果是使得每个处理后样本的p-范数(l1-norm,l2-norm)等于1。）针对每行样本向量：l1: 每个元素&#47;样本中每个元素绝对值的和，l2: 每个元素&#47;样本中每个元素的平方和开根号，lp: 每个元素&#47;每个元素的p次方和的p次根，默认用l2范数。

StandardScaler：数据标准化；(xi - u) &#47; σ 【u:均值，σ：方差】当数据(x)按均值(μ)中心化后，再按标准差(σ)缩放，数据就会服从为均值为0，方差为1的正态分布（即标准正态分布）。

RobustScaler: (xi - median) &#47; IQR 【median是样本的中位数，IQR是样本的 四分位距：根据第1个四分位数和第3个四分位数之间的范围来缩放数据】

MinMaxScaler：数据归一化，(xi - min(x)) &#47; (max(x) - min(x)) ;当数据(x)按照最小值中心化后，再按极差（最大值 - 最小值）缩放，数据移动了最小值个单位，并且会被收敛到 [0,1]之间
</div>2020-10-12</li><br/><li><img src="" width="30px"><span>李@君</span> 👍（27） 💬（5）<div>对训练数据进行平方或者开方，是为了改变训练数据的分布。训练数据的分布被改变后，训练出来的模型岂不是不能正确拟合训练数据了。</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（18） 💬（3）<div>Multiple编码
顾名思义，Multiple编码特征将多个属性同时编码到一个特征中。在推荐场景中，单个用户对哪些物品感兴趣的特征就是一种Multiple编码特征，如，表示某用户对产品1、产品2、产品3、产品4是否感兴趣，则这个特征可能有多个取值，如用户A对产品1和产品2感兴趣，用户B对产品1和产品4感兴趣，用户C对产品1、产品3和产品4感兴趣，则用户兴趣特征为
用户	UserInterests
A	[1, 2]
B	[1, 4]
C	[1, 3, 4]

Multiple编码采用类似oneHot编码的形式进行编码，根据物品种类数目，展成物品种类数目大小的向量，当某个用户感兴趣时，对应维度为1，反之为0，如下
用户	UserInterests
A	[1, 1, 0, 0]
B	[1, 0, 0, 1]
C	[1, 0, 1, 1]

如何使用Multiple编码呢？
我们将多个属性同时编码到同一个特征中，目的就是同时利用多个属性的特征。经过Multiple编码后的特征大小为[batch_size, num_items]，记作U，构建物品items的Embedding矩阵，该矩阵维度为[num_items, embedding_size]，记作V，将矩阵U和矩阵V相乘，我们就得到了大小为[batch_size， embedding_size]的多属性表示。
参考资料：https:&#47;&#47;www.codeleading.com&#47;article&#47;97252516619&#47;#_OneHot_19</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/4d/06bf7890.jpg" width="30px"><span>twzd</span> 👍（13） 💬（3）<div>老师请教一下，movieIdVector列输出结果中(1001,[1],[1.0])，每一列表示什么含义啊</div>2020-11-10</li><br/><li><img src="" width="30px"><span>Geek_ddf8b1</span> 👍（10） 💬（1）<div>老师 我看您FeatureEngForRecModel.scala代码中将特征写入redis是以哈希表的格式写入的，而且有些特征直接是类别型的文本数据。 
       这种方式线上读取特征再后续处理输入排序模型预估的时候会不会效率很低，预估打分时间较长？比如取出文本特征做onehot 或者multihot变换等等，是否可以将文本特征onehot 或者multihot处理后再写入redis？ 
     还有特征除了以hash表形式还可以以其它数据结构存到redis，比如以probuf对象、libsvm数据格式的特征索引：特征值的字符串存到redis 您对这几种存储方式怎么看？哪种更好？</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/f9/c0a6232c.jpg" width="30px"><span>Capricornus</span> 👍（6） 💬（1）<div>我使用的spark3.0的环境，脱离老师的项目，单独建立的用来学习。
1. 下载Scala支持，[下载链接](https:&#47;&#47;www.scala-lang.org&#47;download&#47;2.12.12.html)
2. 解压后放在指定的目录
    ```bash
    vi ~&#47;.bash_profile
    export PATH=&quot;$PATH:&#47;Library&#47;Scala&#47;scala-2.12.12&#47;bin&quot;
    ```
3. 在IDEA的项目中引入，点击“+”号，根据路径添加
4. 右键项目的目录，添加框架支持
5. 添加IDEA的插件，preferences中


6. porm.xml的环境依赖

    ```xml
    &lt;dependencies&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.apache.spark&lt;&#47;groupId&gt;
        &lt;artifactId&gt;spark-core_2.12&lt;&#47;artifactId&gt;
        &lt;version&gt;3.0.0&lt;&#47;version&gt;
    &lt;&#47;dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.apache.spark&lt;&#47;groupId&gt;
        &lt;artifactId&gt;spark-mllib_2.12&lt;&#47;artifactId&gt;
        &lt;version&gt;3.0.0&lt;&#47;version&gt;
    &lt;&#47;dependency&gt;
    &lt;dependency&gt;
        &lt;groupId&gt;org.apache.spark&lt;&#47;groupId&gt;
        &lt;artifactId&gt;spark-sql_2.12&lt;&#47;artifactId&gt;
        &lt;version&gt;3.0.0&lt;&#47;version&gt;
    &lt;&#47;dependency&gt;
    &lt;&#47;dependencies&gt;
    ```
    **注意：路径中不要包括中文，否则可能会出现路径不存在的问题。**

然后有两处需要更改
    val oneHotEncoder = new OneHotEncoder()
      .setInputCols(Array(&quot;movieIdNumber&quot;))
      .setOutputCols(Array(&quot;movieIdVector&quot;))
      .setDropLast(false)
&#47;&#47; 官网的说法：OneHotEncoder which is deprecated in 2.3,is removed in 3.0 and OneHotEncoderEstimator is now renamed to OneHotEncoder.

    val movieFeatures = samples.groupBy(col(&quot;movieId&quot;))
      .agg(count(lit(1)).as(&quot;ratingCount&quot;),
        avg(col(&quot;rating&quot;)).as(&quot;avgRating&quot;),
        functions.variance(col(&quot;rating&quot;)).as(&quot;ratingVar&quot;))
      .withColumn(&quot;avgRatingVec&quot;, double2vec(col(&quot;avgRating&quot;)))</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（6） 💬（2）<div>请教老师，像在电影评分这样的离散数值(且比较稀疏)例子中，如果需要取得分桶数较多，而导致分位数附近均是同一数值的情况下，如何使用分桶的方法呢？
比如按照分桶法首先排序得到评分为5,5,4,4,4,4,4,4,3,3,3,3,2,2,1(共15个)。取桶数为3时，第一个桶内有前两个5，而后面的6个4中应该选择哪3个来分到第一个桶呢？</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/36/59/010b3e60.jpg" width="30px"><span>神经蛙</span> 👍（4） 💬（2）<div>--- 看了几位同学的留言，受益匪浅啊。希望大家多多交流~

1.请你查阅一下 Spark MLlib 的编程手册，找出 Normalizer、StandardScaler、RobustScaler、MinMaxScaler 这个几个特征处理方法有什么不同。

Normalizer
是规范化，根据所传的p值，做p范数归一化(默认p=2)。它是作用在每个样本的向量内部的。无需训练。
eg:x:[v1,v2,v3],p1=sum(abs(vi)), 经过normalizer, x:[v1&#47;p1,v2&#47;p1,v3&#47;p1]

StandardScaler
标准化，将样本的每个特征的标准差变为1.或者可以设置将均值变换为0(默认setMean是False)。这里计算标准差（计算均值）是样本集的每个维度单独计算。所以需要fit操作。计算后保存每个样本标准差、均值后。对每个样本第i个维度除以第i个维度的标准差（如此计算后,该维度均值也会自动被除以标准差，经过标准差公式，则新的标准差为1）。如果setMean == True, 则在变幻是需要先减去均值之后再除以标准差。

RobustScaler
我看spark3才有,具体没弄出来,看文档大概意思是将数据变换到1&#47;4~3&#47;4分为之间。好像是让数据变得稠密了。

MinMaxScaler
将数据变为到[0,1]之间，也需要训练，得到每个维度的最大最小值。然后变化Y= (X-X_min)&#47;(X_max-X_min)


2.你能试着运行一下 SparrowRecSys 中的 FeatureEngineering 类，从输出的结果中找出，到底哪一列是我们处理好的 One-hot 特征和 Multi-hot 特征吗？以及这两个特征是用 Spark 中的什么数据结构来表示的呢？

处理好的One-hot特征
movieIdVector

处理好的Multi-hot特征
vector

数据结构：
SparseVector

其中的数据分别是：（类别数量，索引数组，值数组）。索引数组长度必须等于值数组长度。 </div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（4） 💬（2）<div>第二个问题：
One-hot特征是调用OneHotEncoderEstimator对movieId转换，生成了特征movieIdVector
Multi-hot 特征是调用Vectors.sparse方法，对处理后的genreIndexes转换，生成vector。
这俩个特征都是稀疏向量表示，不是稠密向量
</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/93/d6cd8897.jpg" width="30px"><span>liput</span> 👍（3） 💬（2）<div>请问老师，看到课程里面特征构造都是在offline批量计算得到特征，而在online再另外计算特征，这里经常会出现不一致的情况。想问下，在工业实践中，有什么好的方法去保证这两个地方的一致性呢？</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/54/3d/366462d0.jpg" width="30px"><span>Yvonne</span> 👍（3） 💬（1）<div>谢谢老师！在读youtube论文的时候，当时没有特别理解为什么要将原值，开方，平方都放进去，解释是：In addition to the raw normalized feature ˜x, we also input powers ˜x2 and √x˜, giving the network more expressive power by allowing it to easily form super- and sub-linear functions of the feature. Feeding powers of continuous features was found to improve offline accuracy.…… 当时没能理解为什么。您提到可以用于改变分布特征，突然就理解了XD</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/f9/c0a6232c.jpg" width="30px"><span>Capricornus</span> 👍（3） 💬（1）<div>+-------+-----------+-----------------+
|movieId|ratingCount|ratingCountBucket|
+-------+-----------+-----------------+
|    296|      14616|             13.0|
|    356|      14426|             12.0|
|    318|      13826|             12.0|
|    593|      13692|             12.0|
|    480|      13033|             12.0|
|    260|      11958|             12.0|
|    110|      11637|             12.0|
|    589|      11483|             12.0|
|    527|      11017|             12.0|
|      1|      10759|             12.0|
|    457|      10736|             12.0|
|    150|      10324|             12.0|
|    780|      10271|             12.0|
|     50|      10221|             12.0|
|    592|      10028|             12.0|
|     32|       9694|             12.0|
|    608|       9505|             12.0|
|    590|       9497|             12.0|
|    380|       9364|             12.0|
|     47|       9335|             12.0|
+-------+-----------+-----------------+
老师我设置的分桶数是20，为什么最大的桶标号不是19啊？</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3a/53/ec2c6c55.jpg" width="30px"><span>杨佳亦</span> 👍（3） 💬（2）<div>MinMaxScaler: 
记录数据整体的最大&#47;最小值为max&#47;min, 对于Feature E，若Emax!=Emin, 则rescale后值=(Ei - Emin) &#47; (Emax - Emin) * (max - min) + min. 若Emax == Emin, 则rescale后值=0.5*(min + max). 

Normalizer: 
参考了其他留言才看懂了：这步做的是正则化。正则化将向量的范数缩放到单位1，即可对「样本」也可对「特征」，此处是对样本的正则化，即求样本在所有特征下的取值的P范数(l1, l2). 用通俗的话解释，l1范数计算的是每个元素在同一样本的所有特征取值之和下占的比例，l2范数计算的是每个元素与P维空间中欧氏距离的比值。

StandardScaler: 
常用的数据标准化方法，即计算样本在所有特征下的均值和标准差，用数据减均值以中心化，再除以标准差以缩放至单位1. 就是一个把分布未知（通常情况下）的数据拉回到正态分布的函数。

RobustScaler：
新学到的一个方法，之前没用过。和minmaxScaler类似，即使用大、小值进行数据的缩放。具体为(x - median) &#47; (localUpper - localLower). 其中的localLower, median, localUpper分别为数据的第一、二、三分位点。名字中带有robust，是强调用四分位点而非最大最小值等极端值可以加强模型对噪音的抗干扰力。</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/6e/f5ee46e8.jpg" width="30px"><span>海滨</span> 👍（2） 💬（1）<div>Normalizer，是范式归一化操作，保证归一化之后范式为1
StandardScaler，是标准差归一化操作，保证归一化之后均值为0标准差为1
RobustScaler，是使用分位数进行鲁棒归一化操作，可以有效减少异常值的干扰
MinMaxScaler，是使用最大值和最小值进行归一化操作</div>2021-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ye1IU6yGTuKULCqUlNoDCqvRwQ3FbLJHuBNw6l0lTicz4h9IUDH4JOSPyH2KsKzAEqznhdO29JB4OsibEdUjxl2Q/132" width="30px"><span>清晨</span> 👍（2） 💬（1）<div>standscalar 不是改变了数据的分布吗 处理后的特征为均值为0，方差为1 为什么说没有呢？</div>2020-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GomQuKMYYNX7aMCNt4Ut8YyBrzVM71fgly5l1jykTFic8iaqCTG5ELnsIqlhwgG7ibCCxpODn6PzfVaSicrDub6t5Q/132" width="30px"><span>smjccj</span> 👍（2） 💬（2）<div>Normalizer： 转化为方差为1，不影响数据分布
StandardScaler： 将数据转化为 variance= 1，mean =0(unit variance and&#47;or zero mean)
RobustScaler： 中位数或四分位数进行缩放，处理异常值带来的影响
MinMaxScaler: 将特征缩放至0-1之间</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（1） 💬（2）<div>老师，晚上好！~ 请问一个问题哦，我使用multiHotEncoderExample()函数生成的新的表，表中有一个字段：indexSize，这个字段描述是什么数据？怎么来的？期待老师的回答~^^</div>2021-02-27</li><br/><li><img src="" width="30px"><span>Geek_36ba7d</span> 👍（1） 💬（2）<div>用ES来代替spark可以吗？一个特征就是ES里得keyword呗？</div>2021-02-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/TYeIuNZlibjr0eCvnCCTkYnFEgc8t7BialET3Bnsrbv9micpGIvbhwQrw7Zvt9BicThAEPPXojibVteAvQLb0eTO3DA/132" width="30px"><span>cymx66688</span> 👍（1） 💬（2）<div>OneHot代码中setDropLast(false)让1000列字段变成了1001列，按理说不应该是删除最后一列为999列吗？新增的一列有什么作用？
val oneHotEncoder = new OneHotEncoderEstimator()
      .setInputCols(Array(&quot;movieIdNumber&quot;))
      .setOutputCols(Array(&quot;movieIdVector&quot;))
      .setDropLast(false)</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8c/c4/aba3ee31.jpg" width="30px"><span>卓别林先森</span> 👍（1） 💬（1）<div>王老师您好，关于推荐系统 特征的衍生，应用您都讲很细致，特征决定了整个推荐系统的推荐效果的高度，至关重要。所以特征的质量也尤为重要，请问有关于特征质量，监控方面的比较好的资料推荐吗，谢谢了。</div>2020-12-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DPAiarROoO4JCGLRjyNefCicAZYepFickI1nOyKb6lz476tlYe1S6n5k7iaeicK0AOGn2AAJCvn7qBO8Zp98tDtM4zQ/132" width="30px"><span>Geek_99db42</span> 👍（1） 💬（1）<div>老师你好，我使用了一个其他数据集，这个数据集的ID比较大，在做OneHot时出现了 OneHotEncoder only supports up to 2147483647 的错误，请问对于这种情况该如何处理，通过谷歌没有找到好的解决方法，也许是搜索的方法有错误</div>2020-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FnAia4oNWqvspqYZ8LxpUMh3J6oDxZHR6N8hut8HnywonBaP06dQkwFcqzslPTkMpqzlyDJ3vuOvwmUMx07psoQ/132" width="30px"><span>流年不流梦</span> 👍（1） 💬（1）<div>老师好，想问下分桶后的特征还有必要做特征归一化吗？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/99/f0/ba3c0208.jpg" width="30px"><span>Geek_63ee39</span> 👍（1） 💬（1）<div>思考2：movieIdVector是处理好的One-hot 特征；vector是处理好的Multi-hot 特征；这两个特征是使用Vector表示的</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/3d/07/e2fffa6a.jpg" width="30px"><span>吴波</span> 👍（1） 💬（8）<div>想问下为什么右键运行FeatureEngineering会报错，提示 错误: 找不到或无法加载主类 com.wzhe.sparrowrecsys.offline.spark.featureeng.FeatureEngineering
</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2a/f8/1af3bba6.jpg" width="30px"><span>m-rui</span> 👍（0） 💬（1）<div>请教下老师，一直对分桶有个疑惑，虽然业界实践是对skewed distribution进行分桶，但是这样从信息论的角度看不会丢掉一部分信息么？而且从您的例子来说，大家评分都集中在3.5是不是本身就代表了一种普遍偏好呢？如何保证分桶增加离散度就能增加模型收益呢？有没有啥理论支撑还是这只是个经验结果？</div>2021-11-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/fo79zus88qcdVNuibzPEwKyUuoVx7TozoxgViaYnbYUCFZtdj97Os59EUIBoeiaheuYLib2Suo1YgJCtL4N7XcfzIg/132" width="30px"><span>Geek_69905b</span> 👍（0） 💬（1）<div>代码里这些处理完的特征好像是保存到csv里边了吧  有HDFS吗</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（0） 💬（2）<div>喆哥，您好，为什么要分100个桶，依据是从方差那里得来的吗？如果不是，那么为什么要计算方差？百思不得其解！~~~对不起喆哥，我很死扣....</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（0） 💬（3）<div>喆哥，晚上好！~

我是正转型推荐算法工程师，请问：

文章的数据分布图，喆哥是用什么工具计算出来哦？有推荐吗？</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/09/23/615b56d2.jpg" width="30px"><span>发财了带带捉狗</span> 👍（0） 💬（1）<div>小白来请教一下老师，Spark是一个分布式计算的平台，那我git clone下来的项目是在我自己的windows机器上，只有一台机器，那这里scala的代码是怎么工作的呢？</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/c2/be/1a4598e0.jpg" width="30px"><span>苍绮皓</span> 👍（0） 💬（1）<div>老师请问，离线时电影库中有1000部电影，如果线上上线了一部新电影，它不在库中，那它做ID的Embedding怎么办？</div>2021-05-06</li><br/>
</ul>