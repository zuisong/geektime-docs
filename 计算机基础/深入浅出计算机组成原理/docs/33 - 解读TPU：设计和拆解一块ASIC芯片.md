过去几年，最知名、最具有实用价值的ASIC就是TPU了。各种解读TPU论文内容的文章网上也很多。不过，这些文章更多地是从机器学习或者AI的角度，来讲解TPU。

上一讲，我为你讲解了FPGA和ASIC，讲解了FPGA如何实现通过“软件”来控制“硬件”，以及我们可以进一步把FPGA设计出来的电路变成一块ASIC芯片。

不过呢，这些似乎距离我们真实的应用场景有点儿远。我们怎么能够设计出来一块有真实应用场景的ASIC呢？如果要去设计一块ASIC，我们应该如何思考和拆解问题呢？今天，我就带着你一起学习一下，如何设计一块专用芯片。

## TPU V1想要解决什么问题？

黑格尔说，“世上没有无缘无故的爱，也没有无缘无故的恨”。第一代TPU的设计并不是异想天开的创新，而是来自于真实的需求。

从2012年解决计算机视觉问题开始，深度学习一下子进入了大爆发阶段，也一下子带火了GPU，NVidia的股价一飞冲天。我们在[第31讲](https://time.geekbang.org/column/article/105401)讲过，GPU天生适合进行海量、并行的矩阵数值计算，于是它被大量用在深度学习的模型训练上。

不过你有没有想过，在深度学习热起来之后，计算量最大的是什么呢？并不是进行深度学习的训练，而是深度学习的推断部分。

所谓**推断部分**，是指我们在完成深度学习训练之后，把训练完成的模型存储下来。这个存储下来的模型，是许许多多个向量组成的参数。然后，我们根据这些参数，去计算输入的数据，最终得到一个计算结果。这个推断过程，可能是在互联网广告领域，去推测某一个用户是否会点击特定的广告；也可能是我们在经过高铁站的时候，扫一下身份证进行一次人脸识别，判断一下是不是你本人。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/4f/3a89d29a.jpg" width="30px"><span>J.D.Chi</span> 👍（19） 💬（1）<div>曼昆的《经济学原理》里十大原理的一条：人们总是面临权衡取舍。</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（12） 💬（1）<div>进入每个字都认识系列了，硬着头皮看</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/3e/885ec1d2.jpg" width="30px"><span>宋不肥</span> 👍（8） 💬（0）<div>训练的话，大量的池化卷积，而且很多网络都是对称的，反向传播损失。虽然矩阵乘法可以并行但一层一层的训练迭代的参数更新的考虑时序信息，可以考虑之前处理进位的方法，在硬件上实现，减少等待前面运算的时间，加快它参数更新吧</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/3e/885ec1d2.jpg" width="30px"><span>宋不肥</span> 👍（6） 💬（1）<div>信息时代，数据的爆炸增长，使得深度学习的方法开始发挥作用，反过来又push计算能力的提升，对于计算的实现，由于大量简单重复，直接搭为固定的电路结构（其实就是之前讲的各种门电路，寄存器的组合加上时钟信号和控制信号），就像微机原理里面提到的 硬件软化和软件硬化，按需求，资源稀缺和收益比决定是硬件实现还是软件实现，但在硬件的改进的过程中还得考虑市场的情况，毕竟要落地之后有收益才能存活下去</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（4） 💬（0）<div>---问题---
请问下老师是怎么做到对一个事务的发展历程和最新动态如此了解的？平时会刻意关注一些东西吗？盼老师有空解答？
还有就是感觉自己在看到行业新动态时只能跟着发布动态的文章的思路走，无法形成自己的判断，是否是因为基础仍然比较薄弱导致？</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（3） 💬（0）<div>突然想起来，前一阵挖矿潮，当时候退出的一些挖矿机就是AISC的，就是对挖矿专门处理的TPU，现在深度学习这方面有没有类似专门的比较出名的TPU，感觉现在大多数还是用显卡来跑深度学习。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/96/251c0cee.jpg" width="30px"><span>xindoo</span> 👍（2） 💬（0）<div>训练和推断最大的不同就是训练需要大量的迭代，所以针对训练的tpu肯定是优化迭代，但我具体想不出如何在硬件层面优化迭代。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/78/7b/09defb8d.jpg" width="30px"><span>Yongtao</span> 👍（1） 💬（0）<div>推理主要有前向传播计算，主要是矩阵。训练有前向传播和反向传播计算，其中，反向传播计算包含一些微分计算。所以支持训练的TPU需要计算矩阵计算和微分计算。</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/24/b8/d084eff6.jpg" width="30px"><span>Alan</span> 👍（1） 💬（0）<div>那这么看来的感觉，从技术难度上讲 TPU &lt; GPU &lt; CPU</div>2021-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/76/45/8ff9317c.jpg" width="30px"><span>滕伟峰</span> 👍（1） 💬（0）<div>不错不错，第二次学习</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（1） 💬（1）<div>“Google在TPU的论文里面给出了答案。一方面，在性能上，TPU比现在的CPU、GPU在深度学习的推断任务上，要快15～30倍。而在能耗比上，更是好出30～80倍。
另一方面，Google已经用TPU替换了自家数据中心里95%的推断任务，可谓是拿自己的实际业务做了一个明证。”这一段很精彩

day33 天笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11424820.html</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/89/65ca6878.jpg" width="30px"><span>missingmaria</span> 👍（1） 💬（0）<div>搜了一下，竟然没有搜到第二代TPU的技术细节介绍。但是新闻里开发者透露了一句话，“在芯片进行学习训练的过程中，只需要采用固定的模型即可，不需要变动算法”，猜测二代TPU是针对固定算法开发的，在训练具体模型的时候，将几个算法搭载在一起即可</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/f5/6821ac5f.jpg" width="30px"><span>ezra.xu</span> 👍（1） 💬（0）<div>除了响应时间，效能比，还有就是兼容性，尺寸，成本……</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>训练模型还需要做反向传播、损失函数、更新权重、图像转换等计算。反向传播也是矩阵乘法计算，但需要至少fp16的精度，另外，因为需要保存前向传播计算出来的中间结果，因此需要加大统一存储器的容量。损失函数、更新权重这些计算都需要增加相应的电路模块。</div>2020-07-10</li><br/>
</ul>