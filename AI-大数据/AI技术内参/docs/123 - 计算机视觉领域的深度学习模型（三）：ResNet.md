今天我们继续来讨论经典的深度学习模型在计算机视觉领域应用。今天和你分享的论文是《用于图像识别的深度残差学习》（Deep Residual Learning for Image Recognition）\[1]。这篇论文获得了CVPR 2016的最佳论文，在发表之后的两年间里获得了超过1万2千次的论文引用。

## 论文的主要贡献

我们前面介绍VGG和GoogleNet的时候就已经提到过，在深度学习模型的前进道路上，一个重要的研究课题就是**神经网络结构究竟能够搭建多深**。

这个课题要从两个方面来看：第一个是现实层面，那就是如何构建更深的网络，如何能够训练更深的网络，以及如何才能展示出更深网络的更好性能；第二个是理论层面，那就是如何真正把网络深度，或者说是层次度，以及网络的宽度和模型整体的泛化性能直接联系起来。

在很长的一段时间里，研究人员对神经网络结构有一个大胆的预测，那就是更深的网络架构能够带来更好的泛化能力。但是要想真正实现这样的结果其实并不容易，我们都会遇到哪些挑战呢？

一个长期的挑战就是**模型训练时的梯度“爆炸”（Exploding）或者“消失”（Vanishing）**。为了解决这个问题，在深度学习研究刚刚开始的一段时间，就如雨后春笋般爆发出了很多技术手段，比如“线性整流函数”（ReLu），“批量归一化”（Batch Normalization），“预先训练”（Pre-Training）等等。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/45/abb7bfe3.jpg" width="30px"><span>Andy</span> 👍（2） 💬（0）<div>老师 为什么层数多了之后就不用dropout了呢？</div>2018-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/1c/e160955d.jpg" width="30px"><span>sky</span> 👍（1） 💬（2）<div>我还有个大胆地猜想，在几何领域，有保角映射和等距离映射这样的反应几何特性的映射，如果我想要神经网络提高对这些特征的识别，是否可以把输入做保角映射或者等距离映射，然后作为残差网络的捷径</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/1c/e160955d.jpg" width="30px"><span>sky</span> 👍（1） 💬（1）<div>我能不能这样理解，resnet的捷径其实就是给网络加了一个线性因子，resnet其实就是线性和非线性的组合达到了这样的效果，其实我还是不太明白作者为什么回想到用去逼近残差，逼近残差在其他地方有类似的应用吗</div>2018-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（0） 💬（0）<div>不止层数越来越多，网络架构越来越复杂了，比如GoogleNet新增了平行层，ResNet新增了捷径</div>2020-06-05</li><br/>
</ul>