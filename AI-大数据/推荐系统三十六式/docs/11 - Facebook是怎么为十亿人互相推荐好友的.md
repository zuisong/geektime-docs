上一篇中，我和你专门聊到了矩阵分解，在这篇文章的开始，我再为你回顾一下矩阵分解。

## 回顾矩阵分解

矩阵分解要将用户物品评分矩阵分解成两个小矩阵，一个矩阵是代表用户偏好的用户隐因子向量组成，另一个矩阵是代表物品语义主题的隐因子向量组成。

这两个小矩阵相乘后得到的矩阵，维度和原来的用户物品评分矩阵一模一样。比如原来矩阵维度是m x n，其中m是用户数量，n是物品数量，再假如分解后的隐因子向量是k个，那么用户隐因子向量组成的矩阵就是m x k，物品隐因子向量组成的矩阵就是n x k。

得到的这两个矩阵有这么几个特点：

1. 每个用户对应一个k维向量，每个物品也对应一个k维向量，就是所谓的隐因子向量，因为是无中生有变出来的，所以叫做“隐因子”；
2. 两个矩阵相乘后，就得到了任何一个用户对任何一个物品的预测评分，具体这个评分靠不靠谱，那就是看功夫了。

所以矩阵分解，所做的事就是矩阵填充。那到底怎么填充呢，换句话也就是说两个小矩阵怎么得到呢？

按照机器学习的套路，就是使用优化算法求解下面这个损失函数：

$$ \\min\_{q^{* },p^{* } } \\sum\_{(u,i) \\in \\kappa }{(r\_{ui} - p\_{u}q\_{i}^{T})^{2} + \\lambda (||q\_{i}||^{2} + ||p\_{u}||^{2})} $$

这个公式依然由两部分构成：加号左边是误差平方和，加号右边是分解后参数的平方。

这种模式可以套在几乎所有的机器学习训练中：就是一个负责衡量模型准不准，另一个负责衡量模型稳不稳定。行话是这样说的：一个衡量模型的偏差，一个衡量模型的方差。偏差大的模型欠拟合，方差大的模型过拟合。

有了这个目标函数后，就要用到优化算法找到能使它最小的参数。优化方法常用的选择有两个，一个是随机梯度下降（SGD），另一个是交替最小二乘（ALS）。

在实际应用中，交替最小二乘更常用一些，这也是社交巨头Facebook在他们的推荐系统中选择的主要矩阵分解方法，今天，我就专门聊一聊交替最小二乘求矩阵分解。

## 交替最小二乘原理 (ALS)

交替最小二乘的核心是交替，什么意思呢？你的任务是找到两个矩阵P和Q，让它们相乘后约等于原矩阵R：

$$ R\_{m \\times n} = P\_{m \\times k} \\times Q^{T}\_{n \\times k} $$

难就难在，P和Q两个都是未知的，如果知道其中一个的话，就可以按照线性代数标准解法求得，比如如果知道了Q，那么P就可以这样算：

$$ P\_{m \\times k} = R\_{m \\times n} \\times Q^{-1}\_{n \\times k}$$

也就是R矩阵乘以Q矩阵的逆矩阵就得到了结果。

反之知道了P再求Q也一样。交替最小二乘通过迭代的方式解决了这个鸡生蛋蛋生鸡的难题：

1. 初始化随机矩阵Q里面的元素值；
2. 把Q矩阵当做已知的，直接用线性代数的方法求得矩阵P；
3. 得到了矩阵P后，把P当做已知的，故技重施，回去求解矩阵Q；
4. 上面两个过程交替进行，一直到误差可以接受为止。

你看吧，机器就是这么单纯善良，先用一个假的结果让算法先运转起来，然后不断迭代最终得到想要的结果。这和做互联网C2C平台的思路也一样，告诉买家说：快来这里，我们是万能的，什么都能买到！

买家来了后又去告诉卖家们说：快来这里开店，我这里掌握了最多的剁手党。嗯，雪球就这样滚出来了。

交替最小二乘有这么几个好处：

1. 在交替的其中一步，也就是假设已知其中一个矩阵求解另一个时，要优化的参数是很容易并行化的；
2. 在不那么稀疏的数据集合上，交替最小二乘通常比随机梯度下降要更快地得到结果，事实上这一点就是我马上要说的，也就是关于隐式反馈的内容。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/27/e1/cbedb320.jpg" width="30px"><span>王掌柜家的小二</span> 👍（3） 💬（3）<div>有个问题没想明白的，上网找了下也没明白的：在交替最小二乘法的原理中，既然已经是随机初始化了矩阵P，求得Q就是一个确定的结果了，那么这时候用Q反过来求P的意义何在呢？得到不也是同一个P吗？既然两个值是确定的，又何来迭代一说？
知道自己理解的肯定有问题，忘老师回复。</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/f1/e4fc57a3.jpg" width="30px"><span>无隅</span> 👍（0） 💬（2）<div>无反馈的样本评分是0，然后被采样到的负样本评分，设为-1吗？</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3d/5e/75563f01.jpg" width="30px"><span>瑞雪</span> 👍（10） 💬（3）<div>你好，请问如果选取一部分为负样本，其他的缺失值在矩阵分解时是直接使用NaN吗，有点对正负样本分不太清:D</div>2018-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（5） 💬（0）<div>1. 既然可以根据物品的热门程度选择负样本，是不是类似也可以根据用户的活跃程度选择负样本?
2. 是不是可以借鉴之前基于内容推荐的方法，先找出和当前用户或场景类似内容的用户或场景中的热门物品的交互作为负样本？这里用户或场景可以用各种距离度量的方式选出k个最相邻的。基于内容相似度找和正样本最相邻的物品作为负样本可能也可以。
3. 负样本从概率分布中采样，概率分布的参数让整体的期望值和真实值尽可能接近。这样交互次数多的有更大概率被选中，或者可以看成赋予了更大权重。
4. 引入一个概率参数变量，有交互的概率为p(i, j)，预测交互值为1；无交互的概率为p(i, j)，预测交互值为0。除了计算用户和物品隐变量外，把用户和物品隐变量固定后再估算这个概率参数。</div>2018-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（3） 💬（0）<div>负样本构建方法：
1、通过页面或APP曝光，用户没有反应的
2、告知用户有优惠活动或优惠券，用户无动于衷的
3、根据用户画像，以及物品标签，用户不需要的物品
4、用户明确标记不感兴趣的物品或不认识的人
5、普遍有差评的人或物品</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/ca/8d103e9a.jpg" width="30px"><span>yalei</span> 👍（3） 💬（0）<div>通常用户需要一个“入口”才能浏览商品详情，这个入口可大部分情况下是搜索结果和算法推荐。可以设置曝光埋点，再结合点击埋点来找到真正的负样本（有曝光而无点击的样本）</div>2018-04-10</li><br/><li><img src="" width="30px"><span>Drxan</span> 👍（2） 💬（0）<div>大神，如果要对负样本进行采样的话，是不是就无法用矩阵分解了</div>2018-03-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（1） 💬（0）<div>负样本采样最最精准的应该是曝光而无行为的那些用户sku对，即对该用户来说该sku曝光了，但是用户对该sku没有行为，但是这个量会很大，可以从中抽样得到负样本</div>2019-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq7G29kbKiaJKMDClWibNjMb7BzHEVXRicfBUbW1icyx7TjZPcXFgUGrquqfzPDepWQX7YSdkuYlf9ZeA/132" width="30px"><span>cl</span> 👍（1） 💬（1）<div>还是没有明白，矩阵分解前提是需要分数矩阵，针对没有评分体系的应用从隐式反馈数据中构建这个分数矩阵，就是上一章遗留的问题，能否结合实例说一下？？</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/30/9dcf35ff.jpg" width="30px"><span>森林</span> 👍（1） 💬（0）<div>目标函数里置信度C是1+aC，如果我们挑负样本的话，负样本的次数是啥？</div>2018-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/7c/39ea8a23.jpg" width="30px"><span>曾阿牛</span> 👍（1） 💬（0）<div>在构建点击率预估模型时，仅将正样本附近未点击的样本视为负样本。样本量大时，剔除一段时间内没有转化行为的用户数据（包括正负样本）</div>2018-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4d/a0/e547b7a1.jpg" width="30px"><span>许勇</span> 👍（0） 💬（0）<div>请问如何根据用户向量推荐物品向量呢？除了用聚类算法</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b3/6a/eb6f9010.jpg" width="30px"><span>当下</span> 👍（0） 💬（0）<div>请问怎么确定负样本个数，正负样本的比例多少合适？</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（0） 💬（0）<div>居然能够想到物品向量做聚类，然后逐一计算用户与每个类的推荐分数，这种方法，我大吃一惊！~~</div>2021-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/e7/eb5aea59.jpg" width="30px"><span>山药</span> 👍（0） 💬（0）<div>Faiss用的不是ball tree吧，是Product Quantization吧</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/37/a14bffa6.jpg" width="30px"><span>白木其尔_Grace</span> 👍（0） 💬（0）<div>矩阵初始化是否是常规的初始化方法（Q&#47;|Q|），您的初始化方法是什么？</div>2020-04-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK6mh3xlaMoGtWjmVJh2LutdLcQcPbKNjRlVru3bx8ynPhgwuGhhdzTkwEMoXbvBtgkcDSfom1kZg/132" width="30px"><span>夜雨声烦</span> 👍（0） 💬（0）<div>c2c平台的例子太形象了 ..</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/92/0b/c86a7500.jpg" width="30px"><span>陈朋</span> 👍（0） 💬（0）<div>ALS算法没有讲好，连接https:&#47;&#47;blog.csdn.net&#47;antkillerfarm&#47;article&#47;details&#47;53734658</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/0f/e8d0d8cc.jpg" width="30px"><span>lazytortoise</span> 👍（0） 💬（0）<div>老师，加权的最小二乘公式中 rui 是不是 pui？ 是rui下的二元变量，当rui&gt;0时候，pui=1 ,当rui=0,pui=0.</div>2019-08-01</li><br/><li><img src="" width="30px"><span>赖春苹</span> 👍（0） 💬（0）<div>有个很不明白的地方就是，隐式反馈的代价函数第一项，也是均方误差么？均方误差一般用于评分预测这种回归问题吧？隐式反馈对应的“点击”、“收藏”、“加购物车”这类的操作不是有限个状态么，不应该是分类问题吗？</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/e7/be5d09ae.jpg" width="30px"><span>real</span> 👍（0） 💬（2）<div>这个 根本就不是矩阵分解 好伐。你可以理解为 userid 和itemid的embedding。实现组织为onehot，在embedding到低纬度。两个field的embedding就对应的 p u，然后去采样。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/b4/9a6c44cd.jpg" width="30px"><span>戏入蝶衣</span> 👍（0） 💬（2）<div>老师，上一堂课讲到的预测评分的svd模型不需要负样本，为什么行为预测套用svd就需要负样本呢？如果我们只在用户有过行为的样本上训练模型，会有什么疏忽呢？</div>2019-05-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（0） 💬（0）<div>老师，我理解矩阵分解中，应该是我们对于其中好多元素是未知的，这个未知不代表为0，而负样本其实对应的矩阵中的元素应该确认为0或者定义的负数是么？我们矩阵分解的目的是把矩阵中未知的元素计算出来</div>2019-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（0） 💬（0）<div>老师，您好，在您介绍算法的时候是否也推荐下其对应的python或者spark的包，方便我们实践起来</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3f/f4/c3b50e6c.jpg" width="30px"><span>易初</span> 👍（0） 💬（0）<div>用户 和 物品 是一个pair ， 用dssm 深度语意匹配网络是不是更好</div>2018-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/31/0fbadaff.jpg" width="30px"><span>哎哎哎</span> 👍（0） 💬（0）<div>用户向量存在内存中的话，如何存的下呢？还有就是这种方式对用户向量的更新如果不是实时的话，是否线上服务的用户miss会很高啊，这种情况应该怎么处理呢？</div>2018-03-31</li><br/><li><img src="" width="30px"><span>Drxan</span> 👍（0） 💬（0）<div>大神，如果要对负样本进行采样的话，是不是就无法用矩阵分解了</div>2018-03-28</li><br/>
</ul>