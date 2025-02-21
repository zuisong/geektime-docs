你好，我是王喆。

互联网中到处都是图结构的数据，比如我们熟悉的社交网络，最近流行的知识图谱等等，这些数据中包含着大量的关系信息，这对推荐系统来说是非常有帮助的。

为了能更好地利用这些信息进行推荐，各大巨头可谓尝试了各种办法，比如我们之前学过的DeepWalk、Node2Vec这些非常实用的Graph Embedding方法。但是技术的发展永无止境，最近两年，GNN（Graph Nerual Netwrok，图神经网络）毫无疑问是最火热、最流行的基于图结构数据的建模方法。严格一点来说，图神经网络指的就是可以直接处理图结构数据的神经网络模型。

在诸多GNN的解决方案中，著名的社交电商巨头Pinterest对于GraphSAGE的实现和落地又是最为成功的，在业界的影响力也最大。所以，这节课我们就学一学GraphSAGE的技术细节，看一看Pinterest是如何利用图神经网络进行商品推荐的。

## 搭桥还是平推？技术途径上的抉择

在正式开始GraphSAGE的讲解之前，我想先给你讲一讲DeepWalk、Node2vec这些Graph Embedding方法和GNN之间的关系，这有助于我们理解GNN的原理。

我们这里简单回顾一下DeepWalk和Node2vec算法的基本流程，如下面的图1所示。它们在面对像图1b这样的图数据的时候，其实没有直接处理图结构的数据，而是走了一个取巧的方式，先把图结构数据通过随机游走采样，转换成了序列数据，然后再 用诸如Word2vec这类序列数据Embedding的方法生成最终的Graph Embedding。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（19） 💬（1）<div>思考题：1）能否在第一阶聚合的时候，就把物品的其他特征拼接起来，作为节点的初始embedding呢？2）也可以在k阶聚合完成后，像wide&amp;deep钟一样，将节点的embedding和物品其他特征拼接后接入全连接层和softmax层得到embedding</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/8f/ccce7df1.jpg" width="30px"><span>小匚</span> 👍（13） 💬（1）<div>我觉得目的导向，以目的来决定要不要更多的特征。资源允许情况下，特征越多越好。喂给机器，由模型来判断哪些特征是重要的，哪些是不重要的。
“这个 CONVOLVE 操作是由两个步骤组成的：第一步叫 Aggregate 操作，就是图 4 中 gamma 符号代表的操作，它把点 A 的三个邻接点 Embedding 进行了聚合，生成了一个 Embedding hN(A)；第二步，我们再把 hN(A) 与点 A 上一轮训练中的 Embedding hA 连接起来，然后通过一个全联接层生成点 A 新的 Embedding。”
如果要加，我觉得要加在和上一轮连接起来这里，每次再多加上去这个特征的embedding。这样能保证最原始的数据放进去，保留原始特征，而不会被二次聚合。</div>2020-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YWmHBH11GBpLibqaluLEz53qNHAdcF64pCibYuicofDw09mu0Mnv0cmKia5OBAVbbLZ7UUYS8PhrtbmFHkgN97kKNw/132" width="30px"><span>jalief</span> 👍（4） 💬（1）<div>在实际公司推荐场景中如果要应用这个算法，数据是通过图数据库来存储吗？希望老师能推荐一个生产环境适合的图数据库</div>2021-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（3） 💬（2）<div>思考题：第k阶节点emb初始化时怎么做的，如果是基于节点id类特征通过word2vec生成id_emb，那么还可以基于同样方法，生成对应category_emb，brand_emb，price_emb，然后avg pooling。类似前面讲物品冷启动中提到的EGES模型。
提问：感觉如果综合物品所有相关属性生成的物品emb，已经能很好包含了物品所属特征，包括了属性和行为特征，这样生成的emb在输入GraphSAGE得到物品emb，还能得到更强的物品表达嘛</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/72/73/d707c8be.jpg" width="30px"><span>MutouMan</span> 👍（1） 💬（1）<div>那graphsage是不是本质属于i2i推荐呢？这里用户行为只是不同物品的边，没有说怎么学习用户的embedding。之前的模型大多着眼于u2i推荐。
关于思考题，几位同学都说的很好了，aggregate前加入或者之后都可以吧。还是老师的那句话，怎么做得测试。</div>2021-07-22</li><br/><li><img src="" width="30px"><span>努力学习</span> 👍（1） 💬（1）<div>老师 请问 使用两个GCN网络直接替换到嵌入层，分别用于学习用户的嵌入向量q 和 物品的嵌入向量p，假设对p·q点积使用softmax函数来获得下一项的概率，那是不是用一个损失函数就学习训练了两个GCN网络？而不是用两个损失函数联合训练吗？</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/cb/18/0139e086.jpg" width="30px"><span>骚动</span> 👍（1） 💬（1）<div>老师，还有个问题：GraphSAGE是否有像Node2vec一样考虑了图的结构性和同质性？如果有的话是怎么体现的，如果没有的话后续是否有相应的改进？</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/28/a1/fd2bfc25.jpg" width="30px"><span>fsc2016</span> 👍（1） 💬（1）<div>提问2：既然GraphSAGE是为了直接处理图结构数据生成物品emb，而不需要把图数据转为行为序列。那输入的第k阶物品初始化emb，还是通过转为序列数据进行word2vec得到的。那也就是说GraphSAGE还是避免不了图数据转为序列生成物品emb的过程吗</div>2020-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d1/27/68543b66.jpg" width="30px"><span>W</span> 👍（0） 💬（1）<div>第k阶节点的embedding生成了第k-1阶节点的新embedding，那第k-1阶原始embedding还需要一起使用吗？</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/94/cf/06bad5fc.jpg" width="30px"><span>麦兜</span> 👍（0） 💬（0）<div>图神经网络只聚合了节点信息，如果有边的信息，该如何聚合</div>2024-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/cb/18/0139e086.jpg" width="30px"><span>骚动</span> 👍（0） 💬（0）<div>老师，怎么感觉和Node2vec采样的方式差不多？？2阶我就对应Node2vec 用DFS采样2阶？？</div>2021-01-18</li><br/>
</ul>