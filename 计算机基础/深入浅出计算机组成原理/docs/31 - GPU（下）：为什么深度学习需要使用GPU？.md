上一讲，我带你一起看了三维图形在计算机里的渲染过程。这个渲染过程，分成了顶点处理、图元处理、 栅格化、片段处理，以及最后的像素操作。这一连串的过程，也被称之为图形流水线或者渲染管线。

因为要实时计算渲染的像素特别地多，图形加速卡登上了历史的舞台。通过3dFx的Voodoo或者NVidia的TNT这样的图形加速卡，CPU就不需要再去处理一个个像素点的图元处理、栅格化和片段处理这些操作。而3D游戏也是从这个时代发展起来的。

你可以看这张图，这是“古墓丽影”游戏的多边形建模的变化。这个变化，则是从1996年到2016年，这20年来显卡的进步带来的。

![](https://static001.geekbang.org/resource/image/1d/c3/1d098ce5b2c779392c8d3a33636673c3.png?wh=1200%2A520)

[图片来源](http://www.gamesgrabr.com/blog/2016/01/07/the-evolution-of-lara-croft/)

## Shader的诞生和可编程图形处理器

不知道你有没有发现，在Voodoo和TNT显卡的渲染管线里面，没有“顶点处理“这个步骤。在当时，把多边形的顶点进行线性变化，转化到我们的屏幕的坐标系的工作还是由CPU完成的。所以，CPU的性能越好，能够支持的多边形也就越多，对应的多边形建模的效果自然也就越像真人。而3D游戏的多边形性能也受限于我们CPU的性能。无论你的显卡有多快，如果CPU不行，3D画面一样还是不行。

所以，1999年NVidia推出的GeForce 256显卡，就把顶点处理的计算能力，也从CPU里挪到了显卡里。不过，这对于想要做好3D游戏的程序员们还不够，即使到了GeForce 256。整个图形渲染过程都是在硬件里面固定的管线来完成的。程序员们在加速卡上能做的事情呢，只有改配置来实现不同的图形渲染效果。如果通过改配置做不到，我们就没有什么办法了。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（70） 💬（6）<div>CPU：在电脑里面起着控制运算的作用，是电脑的中央处理器
GPU:  主要是处理计算机中图形的有关计算，是一个附属形的处理器
只有CPU和GPU配合，才能充分的发挥计算机的性能！

学到了31讲，个人觉得，其实真的记不住什么东西，也不可能记得住，但是对某些知识的理解更加深刻了，不要放弃，先统一的学完一遍，对有的知识点有个映象，学习是一辈子的事情，后面再一遍一遍的把它当做读物来学习，一点点的弄！不慌！

专科大二，朝着自己的目标继续努力！</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/95/d1/7d3834ef.jpg" width="30px"><span>笑若海</span> 👍（14） 💬（0）<div>由此看出，CPU适合做逻辑复杂、小量数据、IO密集这三类运算。
只要数据量大，即使逻辑复杂，还是值得研究可编程的专门硬件来提高效率，正如GPU的出现。
IO密集型的场景，由于内存、网卡、硬盘与CPU之间的速率差异，更适合借助中断机制用异步方式实现，提高总体的吞吐率。并借助高速缓存和超线程，进一步提升吞吐率，Web服务就是这种场景。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（9） 💬（1）<div>算了一下，大概是 16 * 5G = 0.8TFLOPS
</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（8） 💬（1）<div>1、以前只知道深度学习、大数据需要GPU但是底层的原理并不知道？
2、也不知道GPU的硬件组成和CPU有什么不同？
听完来时的讲解一下感觉都明白了

day31天笔记: https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11417549.html</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e0/29/60a814e0.jpg" width="30px"><span>清秋（翟浩）</span> 👍（3） 💬（0）<div>这份讲义都是2011年的了，近8年的GPU发展如何呢，这八年没有任何变化么？</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（1） 💬（0）<div>原来着色器，ALU和cuda core其实是同一个东西。那个ppt很给力，谢谢</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>Intel i9 9900K 的理论浮点运算性能大约是 0.64 TFLOPS。这个计算是基于每个核心有 8 个执行单元，最大主频为 5.0 GHz，以及假设的 IPC 值为 2 进行的</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（0）<div>（SM * Cuda Core + TMU）* 主频(Boost) * 指令数(每个时钟周期)</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e0/c5/c324a7de.jpg" width="30px"><span>jorin@zou</span> 👍（0） 💬（0）<div>cpu和GPU是怎么协同工作的，就是两者的pipeline过程。</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/d8/2bacd9bb.jpg" width="30px"><span>GEEK_jahen</span> 👍（0） 💬（0）<div>这章真好，通俗地讲出了GPU硬件发展以及为什么适合深度学习应用。对体系结构只有一些概念性理解的软件工程师，也能很好地接收Get到。</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/e8/d01b90c3.jpg" width="30px"><span>种花家</span> 👍（0） 💬（1）<div>（2944 + 184）× 1700 MHz × 2  = 10.06  TFLOPS
为什么乘以2呢？</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/78/7b/09defb8d.jpg" width="30px"><span>Yongtao</span> 👍（0） 💬（0）<div>Intel i9 9900k
售价：500美元
最高主频：5GHz
核心数：8核16线程
浮点数运算能力：16*5GHz=0.08TFLOPS</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/ba/43/ab9bca4b.jpg" width="30px"><span>黄奇就💤</span> 👍（0） 💬（2）<div>GPU挖矿</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/22/b8c596b6.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>GPU 一开始是没有“可编程”能力的，程序员们只能够通过配置来设计需要用到的图形渲染效果。随着“可编程管线”的出现，程序员们可以在顶点处理和片段处理去实现自己的算法。为了进一步去提升 GPU 硬件里面的芯片利用率，微软在 XBox 360 里面，第一次引入了“统一着色器架构”，使得 GPU 变成了一个有“通用计算”能力的架构。</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fe/2d/e23fc6ee.jpg" width="30px"><span>深水蓝</span> 👍（0） 💬（0）<div>同样时代的AMD显卡，内核的数量好像比NVIDIA的要多不少，但为什么AMD在通用计算领域没有什么影响力呢？</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（1）<div>徐老师，我理解GPU【执行上下文】的组件多是由于GPU的超线程的数量比CPU多而造成的
那么你的这句话【最后，为了能够让 GPU 不要遭遇流水线停顿，我们又在同一个 GPU 的计算核里面，加上了更多的执行上下文】是不是指的就是GPU超线程多，可以避免流水线的停顿？</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（0） 💬（0）<div>最新版的GPU Turing架构，加入了Tensor Core，面向深度学习，直接支持矩阵乘法这种相对复杂的运算🌝🌝🌝</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>技术都是螺旋式发展的，正如 :游戏的发展
—&gt; GPU技术升级—&gt;深度学习发展</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（0） 💬（1）<div>徐老师能把haifux.org中的ppt链接贴出来吗，客户端上加载不出来:D</div>2019-07-05</li><br/>
</ul>