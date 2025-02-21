你好，我是独行。

在过去的几年里，Transformer模型在自然语言处理领域占据了主导地位。自从2017年谷歌提出Transformer以来，BERT、GPT-3等基于Transformer的模型取得了巨大的成功。

然而技术的进步从未停止，最近出现了一种新型模型——**Mamba，被认为是 Transformer 的最强挑战者。**那么，Mamba凭什么能与Transformer一较高下呢？这节课我就来带你看看Mamba的过人之处。

## Transformer的局限

Transformer功能很强，但并不完美，尤其是在处理长序列方面，**Transformer模型中自注意力机制的计算量会随着上下文长度的增加呈平方级增长**，比如上下文长度增加32倍时，计算量可能会增长1000倍，计算效率非常低。为什么会这样？因为Transformer 模型在计算自注意力时，每个输入元素都要与序列中的其他元素进行比较，导致总体计算复杂度为$O(n^2\*d)$，其中$n$是序列长度，$d$是元素表示的维度。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/52/56dbb738.jpg" width="30px"><span>牙小木</span> 👍（6） 💬（2）<div>从小学数学直接蹦到微积分了吗</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（5） 💬（1）<div>虽然有些原理没太理解，但是直观上感觉Mamba相较于Transformer而言，可以支持更长的上下文。现在Transformer在一些文生漫画、文生视频的场景下，还是没办法特别好地解决“时序”问题，导致会出现一些情节不连贯、甚至前后矛盾的情况，这在很大程度上是因为Transformer没法处理特别长的上下文。感觉Mamba在这类场景下可能更有优势~</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f1/31/5001390b.jpg" width="30px"><span>Lonely绿豆蛙</span> 👍（3） 💬（1）<div>看懂了&lt;50%，不过有个肤浅的疑问：为什么Mamba计算量更小、训推更加高效，反而说缺点之一是资源需求大呢？是因为需要更多的资源用于调参吗？</div>2024-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/48/7dbd183b.jpg" width="30px"><span>zMansi</span> 👍（2） 💬（1）<div>这节课好有深度哈，很多知识点不懂。但是看下来mamba需要更多算力来支撑，期待有更多对应的开源产品可以提供试验</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/f2/25cfa472.jpg" width="30px"><span>寒溪</span> 👍（1） 💬（1）<div>请教一下老师画图用的什么工具</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（1） 💬（0）<div>在Mamba走向成熟的道路上，可能面临的最大挑战是适应性和通用性。具体来说：
a) 任务适应性：
虽然Mamba在某些任务上表现出色，但它可能难以在所有类型的任务上都超越Transformer。不同任务可能需要不同的模型特性，Mamba需要证明它能在广泛的应用场景中保持竞争力。
b) 预训练和迁移学习：
Transformer模型（如BERT、GPT等）的一大优势是其强大的预训练和迁移学习能力。Mamba需要开发类似的范式来实现在大规模数据上的预训练，并能够有效地将这些知识迁移到下游任务。
c) 工具生态系统：
Transformer模型拥有丰富的工具、库和优化技术。Mamba需要建立类似的生态系统以支持其广泛应用。
d) 训练稳定性：
新的架构可能面临训练不稳定或收敛困难的问题，特别是在扩展到更大规模模型时。

可能的解决方案：
a) 混合架构：
开发Mamba和Transformer的混合模型，结合两者的优势。这可能涉及在模型的不同部分使用不同的架构，或者开发能够动态选择最佳计算方法的模型。
b) 改进预训练方法：
设计专门针对Mamba架构的预训练任务和方法，可能需要重新思考自监督学习的范式。
c) 投资工具和框架：
大力投资开发支持Mamba的工具、库和框架，使其易于使用和优化。
d) 持续的理论研究：
深入研究Mamba的理论基础，以更好地理解其性能特征和局限性，从而指导进一步的改进。
e) 跨领域合作：
促进机器学习研究者与各个应用领域专家的合作，以发现Mamba的独特优势和潜在应用场景。
f) 优化训练算法：
开发专门针对Mamba架构的优化器和训练技巧，提高其训练稳定性和效率。</div>2024-09-08</li><br/>
</ul>