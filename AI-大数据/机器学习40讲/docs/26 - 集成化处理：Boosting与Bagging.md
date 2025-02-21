伊壁鸠鲁（Epicurus）是古希腊一位伟大的哲学家，其哲学思想自成一派。在认识论上，伊壁鸠鲁最核心的观点就是“多重解释原则”（Prinicple of Multiple Explanantions），其内容是当多种理论都能符合观察到的现象时，就要将它们全部保留。这在某种程度上可以看成是机器学习中集成方法的哲学基础。

![](https://static001.geekbang.org/resource/image/fe/f5/fe8297d1f5d3a7e43c0a73df4e121bf5.png?wh=1023%2A356)

集成学习架构图（图片来自Ensemble Methods: Foundations and Algorithms，图1.9）

集成学习的常用架构如上图所示。在统计学习中，集成学习（ensemble learning）是将多个基学习器（base learners）进行集成，以得到比每个单独基学习器更优预测性能的方法。每个用于集成的基学习器都是弱学习器（weak learner），其性能可以只比随机猜测稍微好一点点。

**集成学习的作用就是将这多个弱学习器提升成一个强学习器（strong learner），达到任意小的错误率**。

在设计算法之前，集成学习先要解决的一个理论问题是集成方法到底有没有提升的效果。虽说三个臭皮匠赛过诸葛亮，但如果皮匠之间没法产生化学反应，别说诸葛亮了，连个蒋琬、费祎恐怕都凑不出来。

在计算学习的理论中，这个问题可以解释成**弱可学习问题**（weakly learnable）和**强可学习问题**（strongly learnable）的复杂性是否等价。幸运的是，这个问题的答案是“是”，而实现从弱到强的手段就是**提升方法**。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/88/ec/1460179b.jpg" width="30px"><span>我心飞扬</span> 👍（3） 💬（1）<div>MultiBoosting由于集合了Bagging，Wagging，AdaBoost，可以有效的降低误差和方差，特别是误差。但是训练成本和预测成本都会显著增加。 
Iterative Bagging相比Bagging会降低误差，但是方差上升。由于Bagging本身就是一种降低方差的算法，所以Iterative Bagging相当于Bagging与单分类器的折中。</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/55/16198c08.jpg" width="30px"><span>InsomniaTony</span> 👍（0） 💬（1）<div>如果对基于决策树的方法感兴趣的话，可以看Gilles Louppe的博士毕业论文Understanding Random Forest。个人觉得很有帮助</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（0） 💬（1）<div>MultiBoosting如果不引入有泊松分布的权重来对样本作wagging，不知道在性能和效果上是否能比Adaboost达到更好的平衡。

Iterative Boosting方法的文章不好找，有没有更具体的称呼。

从实践中看，这几年GBDT，XGBoost，Random Forest太好用了。除了它们和基本的几类集成学习方法外，介绍其他的延伸集成学习方法通俗易懂，正确，且不只是概述的中文文章在学术领域之外很少。</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-06-11</li><br/><li><img src="" width="30px"><span>wsstony</span> 👍（0） 💬（0）<div>有没有实际的实战例子，这样结合例子和理论，加深理解。</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/80/52763d62.jpg" width="30px"><span>周平</span> 👍（0） 💬（0）<div>没看太懂，需要多次学习</div>2018-08-03</li><br/>
</ul>