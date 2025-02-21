你好，我是黄鸿波。

上节课里我们讲了非常经典的GBDT+LR模型，虽说GBDT+LR的组合能够解决很大一部分问题，但是对于高阶的特征组合仍然缺乏良好的应对能力。因此就迎来了本节课要学习的内容：DeepFM。我会先从FM的概念入手，然后进一步讲解DeepFM的模型结构。

## FM算法概述

在讲解DeepFM之前，我们先来了解一下FM。FM（Factorization Machines，因子分解机）是广义线性模型（GLM）的变种，是一种基于矩阵分解的机器学习算法。

当我们面对推荐系统时，数据可能是一个高维的稀疏矩阵。我们希望从这个矩阵中提取出有用的特征，并用这些特征来进行预测和推荐。常见的做法是使用矩阵分解算法（例如SVD和ALS），但这种算法的计算复杂度很高，不太适用于大规模的数据集。为了解决这个问题，可以使用FM算法。

在一般的模型下，各个特征之间都是独立的（例如年龄和文章类别、性别和文章长度等），我们并没有考虑到特征与特征之间的相互关联。但是在实际的推荐系统中，大量的特征之间是有关联关系的，放大了来说，就是内容画像之间的各个特征其实相互关联，内容画像与用户画像之间也存在着很大的关联性。如果能够把这些特征与特征之间的关联性找到，然后挖掘其背后的关系，显然对于推荐系统来说非常有意义。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/b9/c3d3a92f.jpg" width="30px"><span>G小调</span> 👍（3） 💬（1）<div>老师，你代码，在github上哪里</div>2023-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/64/79f2b7e7.jpg" width="30px"><span>曾超</span> 👍（3） 💬（1）<div>希望老师每节课都能给到参考代码，比如这节课，太理论没有代码不好吸收。</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/43/64/79f2b7e7.jpg" width="30px"><span>曾超</span> 👍（1） 💬（1）<div>老师没有参考的代码么
</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>这节课没看懂，完全没理解</div>2023-12-18</li><br/>
</ul>