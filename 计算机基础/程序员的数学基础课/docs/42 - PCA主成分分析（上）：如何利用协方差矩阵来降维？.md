你好，我是黄申。

在概率统计模块，我详细讲解了如何使用各种统计指标来进行特征的选择，降低用于监督式学习的特征之维度。接下来的几节，我会阐述两种针对数值型特征，更为通用的降维方法，它们是**主成分分析PCA**（Principal Component Analysis）和**奇异值分解SVD**（Singular Value Decomposition）。这两种方法是从矩阵分析的角度出发，找出数据分布之间的关系，从而达到降低维度的目的，因此并不需要监督式学习中样本标签和特征之间的关系。

## PCA分析法的主要步骤

我们先从主成分分析PCA开始看。

在解释这个方法之前，我先带你快速回顾一下什么是特征的降维。在机器学习领域中，我们要进行大量的特征工程，把物品的特征转换成计算机所能处理的各种数据。通常，我们增加物品的特征，就有可能提升机器学习的效果。可是，随着特征数量不断的增加，特征向量的维度也会不断上升。这不仅会加大机器学习的难度，还会影响最终的准确度。针对这种情形，我们需要过滤掉一些不重要的特征，或者是把某些相关的特征合并起来，最终达到在减少特征维度的同时，尽量保留原始数据所包含的信息。

了解了这些，我们再来看今天要讲解的PCA方法。它的主要步骤其实并不复杂，我一说你就能明白，但是为什么要这么做，你可能并不理解。咱们学习一个概念或者方法，不仅要知道它是什么，还要明白是怎么来的，这样你就能知其然，知其所以然，明白背后的逻辑，达到灵活运用。因此，我先从它的运算步骤入手，给你讲清楚每一步，然后再解释方法背后的核心思想。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/8e/7b6ea886.jpg" width="30px"><span>Joe</span> 👍（4） 💬（1）<div>一直有个问题为什么协方差是除以m-1，而不是m。方差，均方根等公式也是除m-1。好奇怪。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（2） 💬（1）<div>是不是只有方阵才能求特征值和特征向量？特征值和特征向量的个数与矩阵的维度有关系吗？特征向量的维度和矩阵的维度有关系吗？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/c0/d38daa2d.jpg" width="30px"><span>yaya</span> 👍（2） 💬（1）<div>所以上只是讲解pca的步骤吗？非常赞同要明白他是为什么被提出的，怎么来的观点，但是pca如果只是记步骤很容易忘记，觉得还是从如何建模，然后推导而来更有印象。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/45/af/e7b17926.jpg" width="30px"><span>牛奶</span> 👍（1） 💬（0）<div>请问，在解释协方差公式的时候，xbar是不是应该表示的是“m个样本x这个属性的平均值”?还有一个问题就是，关于这句“协方差是用于衡量两个变量的总体误差”，对于协方差的意义我只能理解到，协方差表示的是两个变量之间的相关性，为什么是两个变量的总体误差呢？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（1） 💬（1）<div>这里Xn,1+...... 后面的括号是不是写错了？还是写掉了一部分？黄老师
(x1,1​−λ)(x2,2​−λ)…(xn,n​−λ)+x1,2​x2,3​…xn−1,n​xn,1​+…)−(xn,1​xn−1,2​…x2,n−1​x1,n​)=0
谢谢 因为有点没看懂😂</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（0） 💬（1）<div>|(X-λI)|  那个竖线是什么意思？行列式是什么意思？怎么算的</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（4） 💬（2）<div>markdown 语法支持不是很好

(1) 标准化原始数据
$$
x&#39; = \frac{x-μ}{σ}
$$
第一列 

均值 $μ_1 = 0$ , 方差 ${σ_1}^2 = [(1-0)^2 + (2-0)^2 + (-3-0)^2]&#47;3 = 14&#47;3$ 

第二列 

均值 $μ_2 =1&#47;3 $ , 方差 ${σ_2}^2 = [(3-1&#47;3)^2 + (5-1&#47;3)^2 + (-7-1&#47;3)^2]&#47;3 = 248&#47;9$ 

第三列 

均值 $μ_3 =-19&#47;3 $ , 方差 ${σ_3}^2 = [(-7+19&#47;3)^2 + (-14+19&#47;3)^2 + (2+19&#47;3)^2]&#47;3 = 386&#47;9$ 

则，
$$
\mathbf{X&#39;} = \begin{vmatrix} 0.46291005&amp;0.50800051&amp;-0.10179732\\0.9258201&amp;0.88900089&amp;-1.17066918\\-1.38873015&amp;-1.3970014&amp;1.2724665\\\end{vmatrix}
$$

(2)协方差矩阵
$$
\mathbf{cov(X_{,i}, X_{,j})} = \frac{\sum_{k=1}^m(x_{k,i} - \bar{X_{,i}})(x_{k,j} - \bar{X_{,j}})}{m-1}
$$

$$
\mathbf{X&#39;}.mean(asix=0) = [0,0, -7.401486830834377e-17]
$$

$$
\mathbf{cov(X_{,i}, X_{,j})} = \frac{(\mathbf{X&#39;[:,i-1]} - \mathbf{X&#39;[:,i-1]}.mean()).transpose().dot(\mathbf{X&#39;[:,j-1]} - \mathbf{X&#39;[:,j-1]}.mean())} {m-1}
$$

协方差矩阵(对角线上是各维特征的方差)：
$$
\mathbf{COV} = \begin{vmatrix} \mathbf{cov(X_{,1}, X_{,1})} &amp; \mathbf{cov(X_{,1}, X_{,2})} &amp; \mathbf{cov(X_{,1}, X_{,3})} \\ \mathbf{cov(X_{,2}, X_{,1})} &amp; \mathbf{cov(X_{,2}, X_{,2})} &amp; \mathbf{cov(X_{,2}, X_{,3})} \\ \mathbf{cov(X_{,3}, X_{,1})} &amp;\mathbf{cov(X_{,3}, X_{,2})} &amp;\mathbf{cov(X_{,3}, X_{,3})}\\\end{vmatrix} = \begin{vmatrix} 1.5 &amp; 1.4991357 &amp; -1.44903232 \\ 1.4991357 &amp; 1.5 &amp; -1.43503825 \\ -1.44903232 &amp; -1.43503825 &amp; 1.5 \\\end{vmatrix}
$$
</div>2019-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/c7/8c2d0a3d.jpg" width="30px"><span>余泽锋</span> 👍（3） 💬（1）<div>import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
array = np.array([[1, 3, -7], [2, 5, -14], [-3, -7, 2]])
array = scale(array)
df = pd.DataFrame(array)
df.corr()</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（2） 💬（1）<div>1.标准化

第一步：计算每列平均值：
E(X1) = 0, E(X2) = 1&#47;3, E(X3) = -19&#47;3

第二步：计算每列方差：
D(X1) = 14&#47;3, D(X2) = 248&#47;9, D(X3) = 386&#47;9

第三步：根据标准化公式：[X - E(X)] &#47; SQRT[D(X)]做标准化处理，结果：

X11 = 0.4628,   X12 = 0.508,    X13 = -0.1018 
X21 = 0.9258,   X22 = 0.889,    X23 = -1.1707
X31 = -1.389,   X32 = -1,397,   X33 = 1.2725

2.协方差矩阵

[[  7.        ,  17.        , -20.5       ],
 [ 17.        ,  41.33333333, -49.33333333],
 [-20.5       , -49.33333333,  64.33333333]]</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>最重要的数学推导没有啊</div>2023-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（0） 💬（0）<div>茶艺师学编程

在隔壁《人人都能学会的编程入门课》找虐回来，继续找黄老师找虐。

而且今天作业又是和留言框过不去……

标准化：
[  0.378   0.577   0.083
   0.755   0.577  -0.956
  -1.133  -1.155  1.039  ]

协方差矩阵：
[      1      0.981     -0.934   
   0.981   0.9999   -0.804  
  -0.934  -0.804     1.014  ]</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/bb/7d/26340713.jpg" width="30px"><span>黄振宇</span> 👍（0） 💬（0）<div>有个问题，黄老师能否帮忙解答下。
降维后的特征集合是之前所有特征的子集合吗，是相当于是先对数据的特征向量做了筛选吗？只不过我们把筛选的工作交给了特征值？

还是说降维之后乘以新的特征向量之后，原始数据的意义是否变了呢？</div>2019-11-29</li><br/>
</ul>