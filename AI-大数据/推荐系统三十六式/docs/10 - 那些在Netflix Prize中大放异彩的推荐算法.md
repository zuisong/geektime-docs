早在前几篇务虚的文章中，我就和你聊过了推荐系统中的经典问题，其中有一类就是评分预测。

让我摸着自己的良心说，评分预测问题只是很典型，其实并不大众，毕竟在实际的应用中，评分数据很难收集到，属于典型的精英问题；与之相对的另一类问题行为预测，才是平民级推荐问题，处处可见。

## 缘起

评分预测问题之所以“虽然小众却十分重要”，这一点得益于十多年前 Netflix Prize 的那一百万美元的悬赏效应。

公元2006年10月2号，对于很多人来说，这只是平凡了无新意的一天，但对于推荐系统从业者来说，这是不得了的一天，美国著名的光盘租赁商 Netflix 突然广发英雄帖，放下“豪”言，这个就是土豪的“豪”，凡是能在他们现有推荐系统基础上，把均方根误差降低10%的大侠，可以瓜分100万美元。消息一出，群贤毕至。

Netflix放出的比赛数据，正是评分数据，推荐系统的问题模式也是评分预测，也就是为什么说，评价标准是均方根误差了。

这一评分预测问题在一百万美元的加持下，催生出无数推荐算法横空出世，其中最为著名的就是一系列矩阵分解模型，而最最著名的模型就是SVD以及其各种变体。这些模型后来也经受了时间检验，在实际应用中得到了不同程度的开枝散叶。

今天我就来和你细聊一下矩阵分解，SVD及其最有名的变种算法。

## 矩阵分解

### 为什么要矩阵分解

聪明的你也许会问，好好的近邻模型，一会儿基于用户，一会儿基于物品，感觉也能很酷炫地解决问题呀，为什么还要来矩阵分解呢？

刨除不这么做就拿不到那一百万的不重要因素之外，矩阵分解确实可以解决一些近邻模型无法解决的问题。

我们都是读书人，从不在背后说模型的坏话，这里可以非常坦诚地说几点近邻模型的问题：

1. 物品之间存在相关性，信息量并不随着向量维度增加而线性增加；
2. 矩阵元素稀疏，计算结果不稳定，增减一个向量维度，导致近邻结果差异很大的情况存在。

上述两个问题，在矩阵分解中可以得到解决。矩阵分解，直观上说来简单，就是把原来的大矩阵，近似分解成两个小矩阵的乘积，在实际推荐计算时不再使用大矩阵，而是使用分解得到的两个小矩阵。

具体说来就是，假设用户物品的评分矩阵A是m乘以n维，即一共有m个用户，n个物品。我们选一个很小的数k，这个k比m和n都小很多，比如小两个数量级这样，通过一套算法得到两个矩阵U和V，矩阵U的维度是m乘以k，矩阵V的维度是n乘以k。

这两个矩阵有什么要求呢？要求就是通过下面这个公式复原矩阵A，你可以点击文稿查看公式。

$$ U\_{m\\times{k}}V\_{n\\times{k}}^{T} \\approx A\_{m\\times{n}}$$

类似这样的计算过程就是矩阵分解，还有一个更常见的名字叫做SVD；但是，SVD和矩阵分解不能划等号，因为除了SVD还有一些别的矩阵分解方法。

### 1 基础的SVD算法

值得一说的是，SVD全称奇异值分解，属于线性代数的知识;然而在推荐算法中实际上使用的并不是正统的奇异值分解，而是一个伪奇异值分解（具体伪在哪不是本文的重点）。

今天我介绍的SVD是由Netflix Prize中取得骄人成绩的Yehuda Koren提出的矩阵分解推荐算法。

按照顺序，首先介绍基础的SVD算法，然后是考虑偏置信息，接着是超越评分矩阵增加多种输入，最后是增加时间因素。好，一个一个来。

前面已经从直观上大致说了矩阵分解是怎么回事，这里再从物理意义上解释一遍。矩阵分解，就是把用户和物品都映射到一个k维空间中，这个k维空间不是我们直接看得到的，也不一定具有非常好的可解释性，每一个维度也没有名字，所以常常叫做隐因子，代表藏在直观的矩阵数据下面的。

每一个物品都得到一个向量q，每一个用户也得到一个向量p。对于物品，与它对应的向量q中的元素，有正有负，代表着这个物品背后暗藏的一些用户关注的因素。

对于用户，与它对应的向量p中的元素，也有正有负，代表这个用户在若干因素上的偏好。物品被关注的因素，和用户偏好的因素，它们的数量和意义是一致的，就是我们在矩阵分解之处人为指定的k。

举个例子，用户u的向量是pu，物品i的向量是qi，那么，要计算物品i推荐给用户u的推荐分数，直接计算点积即可：

$$ \\hat{r}\_{ui} = p\_{u}q\_{i}^{T}$$

看上去很简单，难在哪呢？难在如何得到每一个用户，每一个物品的k维向量。这是一个机器学习问题。按照机器学习框架，一般就是考虑两个核心要素：

1. 损失函数；
2. 优化算法。

SVD的损失函数是这样定义的：

$$ \\min\_{q^{* },p^{* } } \\sum\_{(u,i) \\in \\kappa }{(r\_{ui} - p\_{u}q\_{i}^{T})^{2} + \\lambda (||q\_{i}||^{2} + ||p\_{u}||^{2})} $$

理解SVD的参数学习过程并不是必须的，如果你不是算法工程师的话不必深究这个过程。

由于这个公式略复杂，如果你正在听音频，就需要自己看一下图片。这个损失函数由两部分构成，加号前一部分控制着模型的偏差，加号后一部分控制着模型的方差。

前一部分就是：用分解后的矩阵预测分数，要和实际的用户评分之间误差越小越好。

后一部分就是：得到的隐因子向量要越简单越好，以控制这个模型的方差，换句话说，让它在真正执行推荐任务时发挥要稳定。这部分的概念对应机器学习中的过拟合，有兴趣可以深入了解。

整个SVD的学习过程就是：

1. 准备好用户物品的评分矩阵，每一条评分数据看做一条训练样本；
2. 给分解后的U矩阵和V矩阵随机初始化元素值；
3. 用U和V计算预测后的分数；
4. 计算预测的分数和实际的分数误差；
5. 按照梯度下降的方向更新U和V中的元素值；
6. 重复步骤3到5，直到达到停止条件。

过程中提到的梯度下降是优化算法的一种，想深入了解可以参见任何一本机器学习的专著。

得到分解后的矩阵之后，实质上就是得到了每个用户和每个物品的隐因子向量，拿着这个向量再做推荐计算就简单了，哪里不会点哪里，意思就是拿着物品和用户两个向量，计算点积就是推荐分数了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>Dan</span> 👍（11） 💬（1）<div>請問老師隱性因子k的個數通常如何決定？</div>2018-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/b4/9a6c44cd.jpg" width="30px"><span>戏入蝶衣</span> 👍（3） 💬（1）<div>在最基础的svd模型里，如果不添加用户和物品的评分bias，会有什么影响？</div>2019-05-07</li><br/><li><img src="" width="30px"><span>愚公移山</span> 👍（2） 💬（1）<div>老师，在SVD++分解中，用户的隐式反馈数据和用户属于是怎样加入到用户物品评分矩阵中的呢？损失函数应该需要这部分数据做监督训练的</div>2018-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/40/c8fad3f7.jpg" width="30px"><span>185</span> 👍（2） 💬（1）<div>根据我的理解，损失函数对行为数据是有用的，例如购买物品的数量、观看或者收听的时长、每天打开app的次数等都是和评分类似的数据。
我理解的对吗？</div>2018-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJYWib1hZibEMrCawHUDp3VzEj5uRERX7I4sIjyOSKKNuV8XqSoNRbPTjvd1Bz3DniaLtGecvJDgg9xg/132" width="30px"><span>nebula</span> 👍（1） 💬（1）<div>请问SVD分解，针对新用户、新物品，怎么做更新呢</div>2018-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/fd/56c4fb54.jpg" width="30px"><span>Skye</span> 👍（1） 💬（1）<div>老师，我想问一下，SVD++对于隐式反馈数据，损失函数拟合的rui值是0吗？还有用户行为向量x和用户属性y这个迭代初始值是什么，加上这两个向量，可是损失函数拟合的还是评分，这两个向量好像有点捉摸不透，意义在哪，能否细讲一下</div>2018-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/7c/932aca3d.jpg" width="30px"><span>leoplodchang</span> 👍（0） 💬（1）<div>老师你好，我想请问下，在假如历史行为的那个章节中，你给出了r的公式，那么损失函数的公式是什么样的呢？直接将r套入么？损失函数的后一部分是什么样的呢？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/fd/56c4fb54.jpg" width="30px"><span>Skye</span> 👍（0） 💬（1）<div>行为次数可以作为评分，使用损失函数，但是基础的SVD模型缺少负样本，用户没有行为的记录不作为样本计算在内，在隐式反馈场景应该不行。SVD++加入了隐式反馈信息，在这个场景效果就好了。老师，这样理解对吗？</div>2018-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/26/a7/177581b8.jpg" width="30px"><span>jt120</span> 👍（0） 💬（1）<div>行为和评分，只是y不同，公式一样</div>2018-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/38/4f89095b.jpg" width="30px"><span>写点啥呢</span> 👍（0） 💬（1）<div>请问老师，前面提到的SVD后利用有监督机器学习来得到用户和物品的隐因子向量，那么训练样本是如何获取的呢？有一点疑惑，训练样本已经是用户和物品之间的关系反应，还需要做机器学习么？</div>2018-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（5） 💬（0）<div>老师，您好，我之前用过spark的ALS，我负责的项目中没有显示反馈，全部是隐式反馈，比如点击、点赞、收藏这种，所以我是对每种行为定义了分数，比如点击是3分，点赞4分，收藏或分享是5分这样，然后使用的矩阵分解，上线效果并不理想，我不知道这样是不是不合适？正好您也留了这个思考作业，所以希望您能指点下</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（4） 💬（1）<div>行为数据对于每个用户每个物品已经不是一个数值。这时候预测的还是评分吗？我觉得数值处理过程和目标很可能不同，损失函数需要做一些修改。</div>2018-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVUskibDnhMt5MCIJ8227HWkeg2wEEyewps8GuWhWaY5fy7Ya56bu2ktMlxdla3K29Wqia9efCkWaQ/132" width="30px"><span>衬衫的价格是19美元</span> 👍（2） 💬（1）<div>1.用户物品评分矩阵中某个特定用户一般只给其中的部分物品有评分，那么如何计算该用户对未评分物品的推荐分呢？
2.通过分解用户物品评分矩阵得到隐式因子，这是隐藏在用户物品中的不为人直观理解的影响因子，却又能深刻揭示用户物品的关系
3.因此，从用户物品评分矩阵分解得到隐式因子是关键，一般用SVD方法</div>2019-02-19</li><br/><li><img src="" width="30px"><span>sangyongjia</span> 👍（1） 💬（1）<div>用户物品评分矩阵中某个特定用户一般只给其中的部分物品有评分，评分矩阵是极度稀疏的，但是在矩阵分解时需要使用到评分矩阵。问题是：这些未评分的位置如何填充呢？</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/1a/645ab65b.jpg" width="30px"><span>全</span> 👍（0） 💬（0）<div>1.物品之间存在相关性，信息量并不随着向量维度增加而线性增加；
2.矩阵元素稀疏，计算结果不稳定，增减一个向量维度，导致近邻结果差异很大的情况存在。

老师说的邻居模型这两个弊端真的没想通，可以举个例子吗</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/47/24/de13e1c6.jpg" width="30px"><span>小栗Aili</span> 👍（0） 💬（0）<div>行为数据的话这几个方面因素依然存在，只是行为的话估计得有权重了</div>2020-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f7/88/da243c77.jpg" width="30px"><span>大魔王</span> 👍（0） 💬（0）<div>老师用了矩阵分解就不能用协同过滤了吧？这俩是完全不一样的解法是吗？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/0b/d2335912.jpg" width="30px"><span>kissingurami</span> 👍（0） 💬（0）<div>行为数据(例如点击或不点击，收藏或不收藏...）可以使用均方差作为损失函数，来预测0，或者1；但是奖励和惩罚的力度不够，应该不如交叉熵(或者negitive log likelihood)效果好。不知道对不对？</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/8f/23e9c701.jpg" width="30px"><span>ljinshuan</span> 👍（0） 💬（0）<div>老师我这样理解不知道对不对，假设有10w商品，1w用户。原始svd需要分解的矩阵是1w*10w，如果加入用户行为，比如点击行为。这个矩阵就变成了1w*20w？因为没个商品对象的行为都是一个特征？</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/dd/318c6d52.jpg" width="30px"><span>范蠡</span> 👍（0） 💬（0）<div>SVD 的损失函数公式，您能详细解释下吗？看不明白</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（0） 💬（0）<div>试着回答一下老师的问题：
由于行为数据是离散值，不是连续值，所以损失函数在没有修改的情况下，应该不适用。
而且，离散数据的话，好像也不适合梯度下降算法。
如果是离散数据，做聚类会不会更简单一些呢？</div>2019-12-04</li><br/><li><img src="" width="30px"><span>Geek_86533a</span> 👍（0） 💬（0）<div>请问SVD++中的x和y如何生成，随机吗？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/be/25919d4b.jpg" width="30px"><span>FF</span> 👍（0） 💬（0）<div>偏置值，就是任性值哈哈哈</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/7e/c38ac02f.jpg" width="30px"><span>北冥Master</span> 👍（0） 💬（1）<div>SVD++公式中，Nu -0.5,为什么是这个参数呢？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/b2/274a4192.jpg" width="30px"><span>漂泊的小飘</span> 👍（0） 💬（0）<div>呃……学习AI的时候一直不知道奇异值分解的方法，原来是这样啊。。。感谢</div>2019-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icicSvapqLfCWmIofXILE3b20RVDicQvooGnbksVNgz7wSzEfCKtibhIVMwibf778E39fF9hAa1EFMCFyhgljkwicicXg/132" width="30px"><span>张贝贝</span> 👍（0） 💬（0）<div>svd＋＋中的item向量q和隐士反馈的item向量x是独立的吗？</div>2019-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（0） 💬（0）<div>老师，我还有个疑问就是基于矩阵分解的协同过滤和这节课讲的矩阵分解是不是就是一套算法啊？</div>2019-04-29</li><br/><li><img src="" width="30px"><span>杜骞</span> 👍（0） 💬（0）<div>伪体现在伪逆吧</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/67/4008d168.jpg" width="30px"><span>蘑菇酱</span> 👍（0） 💬（0）<div>物品之间存在相关性，信息量并不随着向量维度增加而线性增加；

老师 这句话能举个具体的例子吗</div>2018-09-29</li><br/><li><img src="" width="30px"><span>lmmcuc</span> 👍（0） 💬（0）<div>老师，您讲关于行为数据的了吗</div>2018-05-15</li><br/>
</ul>