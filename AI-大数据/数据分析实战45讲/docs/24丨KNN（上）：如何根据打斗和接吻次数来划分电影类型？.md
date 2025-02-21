今天我来带你进行KNN的学习，KNN的英文叫K-Nearest Neighbor，应该算是数据挖掘算法中最简单的一种。

我们先用一个例子体会下。

假设，我们想对电影的类型进行分类，统计了电影中打斗次数、接吻次数，当然还有其他的指标也可以被统计到，如下表所示。

![](https://static001.geekbang.org/resource/image/6d/87/6dac3a9961e69aa86d80de32bdc00987.png?wh=1134%2A440)  
我们很容易理解《战狼》《红海行动》《碟中谍6》是动作片，《前任3》《春娇救志明》《泰坦尼克号》是爱情片，但是有没有一种方法让机器也可以掌握这个分类的规则，当有一部新电影的时候，也可以对它的类型自动分类呢？

我们可以把打斗次数看成X轴，接吻次数看成Y轴，然后在二维的坐标轴上，对这几部电影进行标记，如下图所示。对于未知的电影A，坐标为(x,y)，我们需要看下离电影A最近的都有哪些电影，这些电影中的大多数属于哪个分类，那么电影A就属于哪个分类。实际操作中，我们还需要确定一个K值，也就是我们要观察离电影A最近的电影有多少个。

![](https://static001.geekbang.org/resource/image/fa/cc/fa0aa02dae219b21de5984371950c3cc.png?wh=674%2A388)

## KNN的工作原理

“近朱者赤，近墨者黑”可以说是KNN的工作原理。整个计算过程分为三步：

1. 计算待分类物体与其他物体之间的距离；
2. 统计距离最近的K个邻居；
3. 对于K个最近的邻居，它们属于哪个分类最多，待分类物体就属于哪一类。

**K值如何选择**

你能看出整个KNN的分类过程，K值的选择还是很重要的。那么问题来了，K值选择多少是适合的呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（18） 💬（4）<div>曼哈顿距离写错了吧？ 应该d=|X1-X2|+|Y1-Y2|吧</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（28） 💬（1）<div>老师，能不能推荐一下kaggle上谁的项目能让我们学习。</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（9） 💬（1）<div>k越少就会越拟合，越多则越不拟合。最后就是为了寻找k的数值</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/21/c03839f1.jpg" width="30px"><span>FORWARD―MOUNT</span> 👍（8） 💬（3）<div>KNN回归，既然已经知道某部电影的位置了，也就知道接吻次数和打斗次数。还用相邻的电影做回归求接吻次数和打斗次数？
这个表示没懂。</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（5） 💬（1）<div>KNN 的算法原理和工作流程是怎么样的？KNN 中的 K 值又是如何选择的？
1、kNN算法的核心思想是如果一个样本在特征空间中的k个最相邻的样本中的大多数属于某一个类别，则该样本也属于这个类别，并具有这个类别上样本的特性。
2、整个计算过程分为三步：
1）计算待分类物体与其他物体之间的距离；
2）统计距离最近的 K 个邻居；
3）对于 K 个最近的邻居，它们属于哪个分类最多，待分类物体就属于哪一类。
3、我们一般采用交叉验证的方式选取 K 值。
交叉验证的思路就是，把样本集中的大部分样本作为训练集，剩余的小部分样本用于预测，来验证分类模型的准确性，准确率最高的那一个最终确定作为 K 值。
</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/da/44b9273b.jpg" width="30px"><span>文晟</span> 👍（5） 💬（2）<div>老师，那几个距离公式怎么跟别处的不一样，记得课本上是x1-x2而不是x1-y1这种形式</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（2） 💬（1）<div>跟谁像，就是谁

计算距离
通过交叉验证的方法，找到较小K，准确还较高的
计算K个近邻，
跟谁多</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（2） 💬（1）<div>老师，在实际工作中，我们直接调库和调参就行了吗？</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e2/47/1914418a.jpg" width="30px"><span>贺中堃</span> 👍（1） 💬（1）<div>1.找K个最近邻。KNN分类算法的核心就是找最近的K个点，选定度量距离的方法之后，以待分类样本点为中心，分别测量它到其他点的距离，找出其中的距离最近的“TOP K”，这就是K个最近邻。
2.统计最近邻的类别占比。确定了最近邻之后，统计出每种类别在最近邻中的占比。
3.选取占比最多的类别作为待分类样本的类别。

k值一般取一个比较小的数值，通常采用交叉验证法来选取最优的k值。</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7d/2a/4c7e2e2f.jpg" width="30px"><span>§mc²ompleXWr</span> 👍（1） 💬（1）<div>KNN回归：如果某个特征属性未知，我怎么算距离？</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（1） 💬（1）<div>kd树的简单解释https:&#47;&#47;blog.csdn.net&#47;App_12062011&#47;article&#47;details&#47;51986805</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（1） 💬（1）<div>1. KNN的算法原理
离哪个邻居越近，属性与那个邻居越相似，和那个邻居的类别越一致。
2. KNN的工作流程
首先，根据场景，选取距离的计算方式
然后，统计与所需分类对象距离最近的K个邻居
最后，K个邻居中，所占数量最多的类别，即预测其为该分类对象的类别
3. K值的选取
交叉验证的方式，即设置多个测试集，用这些测试集测试多个K值，那个测试集所预测准确率越高的，即选取其相应的K值。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/1e/0d5f8336.jpg" width="30px"><span>fancy</span> 👍（1） 💬（1）<div>1. KNN的算法原理
离哪个邻居越近，属性与那个邻居越相似，和那个邻居的类别越一致。
2. KNN的工作流程
首先，根据场景，选取距离的计算方式
然后，统计与所需分类对象距离最近的K个邻居
最后，K个邻居中，所占数量最多的类别，即预测其为该分类对象的类别
3. K值的选取
交叉验证的方式，即设置多个测试集，用这些测试集测试多个K值，那个测试集所预测准确率越高的，即选取其相应的K值。</div>2019-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/3b/2d14b5e1.jpg" width="30px"><span>顾仲贤</span> 👍（1） 💬（1）<div>老师，您在KNN做回归时举例说已知分类求属性。问题是，在没有属性只知道分类的情况下，怎么求出k个近邻呢？</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>老师，KNN中的K值选取还是得不断的尝试是吗，只是最终确定K值的选取是以K折交叉验证得出的准确度的高低来确定</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4d/62/0fe9cbb3.jpg" width="30px"><span>William～Zhang</span> 👍（0） 💬（1）<div>老师，请问选取k个最近的领居，看分类最多的那一类，待分类物体就属于哪一类，那请问如果，刚好k个最近领居各一半，分属于不同类，怎么办</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/52/10c4d863.jpg" width="30px"><span>FeiFei</span> 👍（0） 💬（1）<div>1，计算待分类物和其他物体之间的距离；
2，统计距离最近的K的物体；
3，K个邻居最多的分类=待分类物的分类。

分割线

1，太小会过于拟合
2，太大会欠拟合</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/02/ff2e1881.jpg" width="30px"><span>闫伟</span> 👍（0） 💬（1）<div>老师，微信群是多少呀，想进群一起学习，麻烦老师加 下，vx：yw903167000</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（0） 💬（1）<div>KNN工作原理：计算分类物体与其它物体的距离，选取k值，获得k个邻居的属性，哪种属性最多，该类就归属于这种属性。
K值选择：交叉验证选择</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（1） 💬（0）<div>很不错，讲了等于没讲，所以K怎么找？具体教学都没有，怎么实战？</div>2022-11-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAl7V1ibk8gX62W5I4SER2zbQAj3gy5icJlavGhnAmxENCia7QFm8lE3YBc5HOHvlyNVFz7rQKFQ7dA/132" width="30px"><span>timeng27</span> 👍（1） 💬（0）<div>k值的选取是否可以参考样本中的分类比例和个数？比如样本中最少的一个分类是10个，那么k肯定不能取10。回不会有类似的方法取k值？</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/da/2c/783413de.jpg" width="30px"><span>彭涛</span> 👍（0） 💬（0）<div>同样 KNN 也可以用于推荐算法，虽然现在很多推荐系统的算法会使用 TD-IDF、协同过滤、Apriori 算法，不过针对数据量不大的情况下，采用 KNN 作为推荐算法也是可行的。
请问：总结中的 TD-IDF 是否应该为：TF-IDF ？</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（0） 💬（0）<div>KNN算法原理:
1.根据业务场景，选择合适的距离计算公式，计算待分类点与其他样本点之间的距离
2.统计与待分类点距离最近的K个邻居
3.观察K个邻居的分类占比，分类占比最高的即为待分类点所属的类别

K值的选择:
交叉验证法: 选取样本集中的大部分样本为训练集，剩下的样本为测试集，不断训练模型，得到不同的模型准确率，直至得到最高的准确率，此时的K值为最优值

KD树: 待学习</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bf/e3/2aa8ec84.jpg" width="30px"><span>鱼非子</span> 👍（0） 💬（0）<div>KNN算法原理：物以类聚
工作流程：计算一个样本与其它样本的距离，选择最近的k个样本，k个样本中哪种类别最多，这个样本就属于哪种类别
k值选择：利用交叉验证的方法
</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/36/cc/499625d3.jpg" width="30px"><span>学技术攒钱开宠物店</span> 👍（0） 💬（0）<div>回归已经知道值了呀，为什么还计算距离平均</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/8b/35fa42aa.jpg" width="30px"><span>大鱼</span> 👍（0） 💬（0）<div>如果回归的话，怎么找到那k个相邻的点呢？除了类别，是不是还需要其他的特征来辅助，比如我是爱情电影，除了这个分类，还得有我是几级的爱情电影？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/db/21/26ff0240.jpg" width="30px"><span>上善若水</span> 👍（0） 💬（0）<div>请问TD-IDF是什么，为啥我搜的是tf-idf,是不同的命名吗？

</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6d/88/d6e6ddcf.jpg" width="30px"><span>开心</span> 👍（0） 💬（0）<div>预估值就是历史的平均值，这样理解对吗？上一讲的乳腺癌的发病率是不是这样算的</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/be/76/55e5e326.jpg" width="30px"><span>Chen</span> 👍（0） 💬（0）<div>1、K值太小的时候，模型变得复杂，容易发生过拟合，这点怎么理解呢？难道不是K太小，看的邻居太少，学习能力不足，会欠拟合吗，这儿没有理解。
2、当数据量非常大的时候，KNN会面临庞大的存储空间和计算时间问题，我们可以用kd树解决。
当样本类别非常地不均衡的时候，KNN会面临分类准确率很低的问题，我们该怎么解决呢？</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ab/5d/430ed3b6.jpg" width="30px"><span>从未在此</span> 👍（0） 💬（0）<div>欧式距离应该是同坐标轴数字相减吧？跨坐标轴不好计算</div>2019-02-12</li><br/>
</ul>