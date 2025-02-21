在上第一期的分享中，我们通过一篇经典论文讲了AlexNet这个模型。可以说，这篇文章是深度学习在计算机视觉领域发挥作用的奠基之作。

AlexNet在2012年发表之后，研究界对这个模型做了很多改进工作，使得这个模型得到了不断优化，特别是在ImageNet上的表现获得了显著提升。今天我们就来看看针对AlexNet模型的两个重要改进，分别是VGG和GoogleNet。

## VGG网络

我们要分享的第一篇论文题目是《用于大规模图像识别的深度卷积网络》（Very Deep Convolutional Networks for Large-Scale Image Recognition）\[1]。这篇文章的作者都来自于英国牛津大学的“视觉几何实验室”（Visual Geometry Group），简称VGG，所以文章提出的模型也被叫作 **VGG网络**。到目前为止，这篇论文的引用次数已经多达1万4千次。

首先，我们简单来了解一下这篇论文的作者。

第一作者叫卡伦·西蒙彦（Karen Simonyan），发表论文的时候他在牛津大学计算机系攻读博士学位。之后，西蒙彦加入了谷歌，在DeepMind任职，继续从事深度学习的研究。

第二作者叫安德鲁·兹泽曼（Andrew Zisserman），是牛津大学计算机系的教授，也是计算机视觉领域的学术权威。他曾经三次被授予计算机视觉最高荣誉“马尔奖”（Marr Prize）。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/30/1c/e160955d.jpg" width="30px"><span>sky</span> 👍（4） 💬（0）<div>第一是如何让网络越来越深，参数越来越多，第二是如何优化网络结构，优化网络结构需要对深度神经网络有更基础的理论性理解</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/8e/f4297447.jpg" width="30px"><span>吴文敏</span> 👍（1） 💬（0）<div>更深的模型更少的参数</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（0） 💬（0）<div>VGG：第一个真正意义上达到“深层”的网络架构；
GoogleNet：优化网络架构。</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/1c/e160955d.jpg" width="30px"><span>sky</span> 👍（0） 💬（0）<div>第一是如何让网络越来越深，参数越来越多，第二是如何优化网络结构，优化网络结构需要对深度神经网络有更基础的理论性理解</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/45/abb7bfe3.jpg" width="30px"><span>Andy</span> 👍（0） 💬（0）<div>请问老师计算机视觉会被这些复杂的模型统治吗？</div>2018-09-10</li><br/>
</ul>