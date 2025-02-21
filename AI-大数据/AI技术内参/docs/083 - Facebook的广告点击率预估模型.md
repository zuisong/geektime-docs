上一篇文章我们讲了整个计算广告领域最核心的一个问题：广告回馈预估。广告回馈预估，就是预测“用户与广告的交互以及达成交易这种行为”的概率，也就是点击率预估和转化率预估。广告回馈预估存在着数据稀疏等难点和挑战，目前在这个领域比较流行的模型有对数几率回归和数模型等。

今天，我们就来看一个广告回馈预估的实例：**Facebook的广告点击率预估**。我们会结合2014年发表的一篇论文《Facebook的广告点击率预估实践经验》（Practical Lessons from Predicting Clicks on Ads at Facebook）来进行分析\[1]。

## Facebook广告预估

Facebook的广告不是我们之前介绍过的搜索广告或者展示广告的简单应用，而是**社交广告**。可以说，社交广告是最近10年慢慢崛起的一种新的广告类型。在论文发表的时候，也就是2014年，Facebook有7.5亿“日活跃用户”（Daily Active Users）和超过1百万的广告商，这个数字在当时是相当惊人的。而今天，在Facebook上活跃的大约有14.5亿用户和5百万广告商。因此，广告系统所需要应对的规模是成倍增加的。

我们说Facebook的广告是社交广告，也就是说，这些广告不依赖于用户输入的搜索关键词。从Facebook的角度来说，广告商在其平台上投放广告的巨大优势，在于能够精准地根据用户的地理位置、年龄、性别等重要信息进行有针对性的投放，因此这些信息能够帮助平台选择什么样的广告适合什么样的人群。那这里的难点就是，对于某一个人群来说，可能符合的广告数量是巨大的，这对广告的回馈预估以及整个系统都是一个不小的挑战。

## 广告点击率的评估

在我们详细解释Facebook点击率系统的一些核心组件之前，我们首先来看一看Facebook的研究人员是怎么评测他们的系统的。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/35/df/67f91c36.jpg" width="30px"><span>帅帅</span> 👍（1） 💬（1）<div>反正加个GBDT就是比单纯的LR好就对了</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/b6/fedb6472.jpg" width="30px"><span>艾熊</span> 👍（1） 💬（0）<div>hi，因为这篇论文是2014年发的，想问一下现在Facebook还是基于这个模型来做广告ctr预估吗？这个模型适用和不适用的规模和场景可以分享一下吗？</div>2018-06-20</li><br/><li><img src="" width="30px"><span>星星之火</span> 👍（1） 💬（0）<div>老师能不能讲下具体的实现，架构中的难点</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/41/89/77d3e613.jpg" width="30px"><span>bookchan</span> 👍（0） 💬（0）<div>NCE在训练的时候，相比CE，只是多了个常数项，对求梯度的效果只是多了个系数的作用，可以等同于原来的学习率乘以这个系数，这么看的话对训练其实帮助是不大的，因为不同数据集使用不同学习率常事。但在其他场景下，比如同一个模型，使用不同的训练数据来训练，那么怎么评价不同数据训练出来的模型效果？这时候使用NCE，就能够消除不同数据集自身数据分布对loss的影响(极端假设A数据集正样本偏多，B数据集都是负样本偏多，那么他们的NCE也许会一样，但是模型的效果是不一样的，A随便预测正类就好了，指标就会很高，但是B则难很多)。 </div>2021-01-27</li><br/><li><img src="" width="30px"><span>Geek_fa0c60</span> 👍（0） 💬（0）<div>写的好浅。就是网上的一些文章的堆砌而已。 我们不需要看很多，只希望有一些详细的，深入的介绍</div>2020-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（0） 💬（0）<div>如何了解谷歌的广告模型</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/c3/625eef99.jpg" width="30px"><span>arfa</span> 👍（0） 💬（0）<div>老师，id怎么加进模型？</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（0） 💬（0）<div>老师怎么看待微信广告现状和前景？</div>2018-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/b4/4768f34b.jpg" width="30px"><span>旭</span> 👍（0） 💬（0）<div>无需人工特征工程也是优势，缺点应是gbdt的离线更新以及预测时间消耗</div>2018-06-11</li><br/>
</ul>