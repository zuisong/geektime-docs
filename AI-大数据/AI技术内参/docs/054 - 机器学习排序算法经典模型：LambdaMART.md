在这周的时间里，我们讨论机器学习排序算法中几个经典的模型。周一我们分享了排序支持向量机（RankSVM），这个算法的好处是模型是线性的，容易理解。周三我们聊了梯度增强决策树（Gradient Boosted Decision Tree），长期以来，这种算法被用在很多商业搜索引擎当中来作为排序算法。

今天，我们来分享这一部分的最后一个经典模型：**LambdaMART**。这是微软在Bing中使用了较长时间的模型，也在机器学习排序这个领域享有盛誉。

## LambdaMART的历史

LambdaMART的提出可以说是一个“三步曲”。

这里有一个核心人物，叫克里斯多夫⋅博格斯（Christopher J.C. Burges）。博格斯早年从牛津大学物理学毕业之后，又于布兰戴斯大学（Brandeis University）获得物理学博士学位，他曾在麻省理工大学做过短暂的博士后研究，之后来到贝尔实验室，一待14年。2000年，他来到微软研究院，并一直在微软研究院从事机器学习和人工智能的研究工作，直到2016年退休。可以说，是博格斯领导的团队发明了微软搜索引擎Bing的算法。

**LambdaMART的第一步来自于一个叫RankNet的思想**\[1]。这个模型发表于ICML 2005，并且在10年之后获得ICML的时间检验奖。这也算是在深度学习火热之前，利用神经网络进行大规模商业应用的经典案例。

RankNet之后，博格斯的团队很快意识到了RankNet并不能直接优化搜索的评价指标。因此他们根据一个惊人的发现，**提出了LambdaRank这一重要方法**\[2]。LambdaRank的进步在于算法开始和搜索的评价指标，也就是NDCG挂钩，也就能够大幅度提高算法的精度。

LambdaRank之后，博格斯的团队也认识到了当时从雅虎开始流行的使用“梯度增强”（Gradient Boosting），特别是“梯度增强决策树”（GBDT）的思路来进行排序算法的训练，于是他们就把LambdaRank和GBDT的思想结合起来，**开发出了更加具有模型表现力的LambdaMART**\[3]。LambdaMART在之后的雅虎排序学习比赛中获得了最佳成绩。

## RankNet的思想核心

要理解LambdaMART，我们首先要从RankNet说起。其实，有了排序支持向量机RankSVM的理论基础，要理解RankNet就非常容易。RankNet是一个和排序支持向量机非常类似的配对法排序模型。也就是说，RankNet尝试正确学习每组两两文档的顺序。那么，怎么来定义这个所谓的两两文档的顺序呢？
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/89/5b/cc06e436.jpg" width="30px"><span>yaolixu</span> 👍（1） 💬（0）<div>会不会出现梯度消失的情况？如果出现了，怎么破？</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/8e/f4297447.jpg" width="30px"><span>吴文敏</span> 👍（0） 💬（0）<div>这样会影响模型的收敛速度吧</div>2018-01-31</li><br/>
</ul>