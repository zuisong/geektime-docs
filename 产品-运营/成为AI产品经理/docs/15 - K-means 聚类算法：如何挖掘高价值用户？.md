你好，我是海丰。

在前面的课程中，我们学习了分类算法：K 近邻、逻辑回归、朴素贝叶斯、决策树，以及支持向量机，也学习了回归算法：线性回归。它们有一个共同点，都是有监督学习算法，也就是都需要提前准备样本数据（包含特征和标签，即特征和分类）。

但有的情况下，我们事先并不能知道数据的类别标签，比如在[第8讲](https://time.geekbang.org/column/article/326965)智能客服的例子中，因为事先并不知道用户的咨询问题属于什么类别，所以我们通过层次聚类算法把相似度比较高的用户咨询问题进行了聚类分组，然后把分析出的常见高频问题交由机器人回复，从而减轻人工客服的压力。

聚类算法是无监督学习算法中最常用的一种，无监督就是事先并不需要知道数据的类别标签，而只是根据数据特征去学习，找到相似数据的特征，然后把已知的数据集划分成不同的类别。

不过，因为第 8 讲中的层次聚类算法在实际工业中的应用并不多。所以今天，我们就来讲一种应用最广泛的聚类算法，它就是 K 均值（ K-means ）算法。

## 如何理解 K-means 算法？

每次大学开学的时候都会迎来一批新生，他们总会根据自己的兴趣爱好，自发地加入校园一个个小社团中。比如，喜欢音乐的同学会加入音乐社，喜欢动漫的同学会加入动漫社，而喜欢健身的同学会加入健身社等等。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/5d/1c/f2d45010.jpg" width="30px"><span>橙gě狸</span> 👍（8） 💬（0）<div>在给销售人员提供个性化培训的这个场景上，使用聚类算法。
可以先根据销售人员能力模型内的几大标签作为聚类算法的特征，通过算法将销售人员划分为2的n次方个群体，并根据最终聚类结果推送不同的培训课程。</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3c/fd/7f9ab528.jpg" width="30px"><span>汉堡吃不饱</span> 👍（5） 💬（4）<div>老师，不明白的一点:
既然都已经分成8类了，且知道每一类的特征与类别了，那这不是有监督学习吗？
聚类按照8类出结果后，如果这8类不符合之前定义的8类的标准，怎么办？</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e6/37/74ec8fbb.jpg" width="30px"><span>小太白</span> 👍（2） 💬（0）<div>应用场景：差异化教学。通过对学生多维数据进行标签，分组，聚类，对学生进行愈发精细的画像，给老师教学决策和差异化教学提供依据和抓手。</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/4e/f42d27e8.jpg" width="30px"><span>Rosa rugosa</span> 👍（2） 💬（0）<div>在股票软件中，判断资讯发布在那个类别下适合用K-means聚类。K-means聚类适合用在文本分类和精细化运行中的用户分层中。</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/28/5f/3f40169c.jpg" width="30px"><span>Yesss!</span> 👍（2） 💬（0）<div>我暂时接触过环保业务，R：最近一次扔垃圾的频率 F：扔垃圾的频率 M：扔垃圾的重量。在后台得到样本数据，并用K-means。分析出哪一些人员是相似性最大的。从而决定人员相似性最高的楼栋作为标准（实行奖惩等制度）。
银行借贷业务也是相似的：R：最近一次借贷频率，F：借贷的频率次数 M：借贷的金额。分析出哪一些人员是最接近老赖的
保险业务、电商、社交同理</div>2021-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/19/2f33b810.jpg" width="30px"><span>加菲猫</span> 👍（1） 💬（0）<div>聚类算法可以用在社区运营和内容推荐上，例如B站、视频网站的内容推荐，电商社区不同用户群的内容、商品推荐；腾讯视频号的内容推荐。</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/33/5d8a5a90.jpg" width="30px"><span>文杰</span> 👍（1） 💬（3）<div>客户分层，通过聚类后怎么对应到那8个分类去？用户数据是每天变的，每天都要全量数据跑下聚类？还有一个用户今天被分到类1，明天分到类2，前端营销怎么搞？</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/4f/50/d62f24f2.jpg" width="30px"><span>熊猫要吃酒</span> 👍（1） 💬（1）<div>RFM模型中，R的值越低越好，但是F和M越高越好，怎么看权重呢？</div>2021-01-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJvs3Bz46PKSC4hvPUt0wbZo1iaKIbEt6UDe8SeqpyLJnaauadIIWLycHMVhTibmMDibgXribwxNNibk0g/132" width="30px"><span>Geek_ac620e</span> 👍（0） 💬（0）<div>hhh
</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（0）<div>老师，“第三步，在划分好的每一个组内，我们计算每一个数据到质心的距离，取均值，用这个均值作为下一轮迭代的中心点。”这里没看明白，是不是应该是取每个组的所有点的坐标的平均值作为新的质点呀</div>2022-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKGNb0iaXNtliaO2UYrzn6j7DgoH4PC9UCQ1euV7xuI92GQ779IIBhI99GCDASBQ1C7RE7dz2nMPibLg/132" width="30px"><span>AsyDong</span> 👍（0） 💬（0）<div>质心位置的选择是随机的话，对结果会有影响吧。比如数据在第一象限，然后2个质心，一个随机放在第三象限，一个随机放在第一象限，那第三象限的质心岂不是成了摆设，这样分出来的类不精准吧。</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（0） 💬（0）<div>这些算法在落地时是用啥技术实现的啊</div>2021-01-15</li><br/>
</ul>