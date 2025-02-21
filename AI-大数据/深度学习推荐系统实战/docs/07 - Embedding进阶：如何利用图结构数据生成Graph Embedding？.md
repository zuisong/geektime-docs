你好，我是王喆。

上一节课，我们一起学习了Embedding技术。我们知道，只要是能够被序列数据表示的物品，都可以通过Item2vec方法训练出Embedding。但是，互联网的数据可不仅仅是序列数据那么简单，越来越多的数据被我们以图的形式展现出来。这个时候，基于序列数据的Embedding方法就显得“不够用”了。但在推荐系统中放弃图结构数据是非常可惜的，因为图数据中包含了大量非常有价值的结构信息。

那我们怎么样才能够基于图结构数据生成Embedding呢？这节课，我们就重点来讲讲基于图结构的Embedding方法，它也被称为Graph Embedding。

## 互联网中有哪些图结构数据？

可能有的同学还不太清楚图结构中到底包含了哪些重要信息，为什么我们希望好好利用它们，并以它们为基础生成Embedding？下面，我就先带你认识一下互联网中那些非常典型的图结构数据（如图1）。

![](https://static001.geekbang.org/resource/image/54/91/5423f8d0f5c1b2ba583f5a2b2d0aed91.jpeg?wh=1920%2A654 "图1 互联网图结构数据")

事实上，图结构数据在互联网中几乎无处不在，最典型的就是我们每天都在使用的**社交网络**（如图1-a）。从社交网络中，我们可以发现意见领袖，可以发现社区，再根据这些“社交”特性进行社交化的推荐，如果我们可以对社交网络中的节点进行Embedding编码，社交化推荐的过程将会非常方便。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（83） 💬（4）<div>王喆老师！我刚刚问了那个deepwalk在原本就是序列数据上的应用的问题，我说我能想到的优势就是扩充样本， 但是通过一系列的尝试，我觉得好像是恰恰相反！用deepwalk的时候生成比原序列样本少，才能降低噪音，抓住主要关联。特别想跟老师探讨一下这个结论。

具体是这样的， 我用我们公司的用户浏览网页的序列数据，来做网页的embedding，原本有 500k条序列，一开始我用deepwalk生成了原数据两倍的样本（1mm）的samples， 结果训练出来的embedding，网页之间的similarity很低 （每个网页跟最近网页的similarity值达到0.5左右， 如果直接用原样本可达0.7）， 接着我试着降低deepwalk生成样本的数量，最后用了跟您同样的20k，通过随机抽查，效果特别的好（可以达到0.9以上，而且结果很make sense）。所以我觉得deepwalk的好处反而是去掉多余噪音信息，关注主要矛盾，所以一般要生成比原样本更少的样本量</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/ab/21/d118e1c4.jpg" width="30px"><span>微波</span> 👍（44） 💬（1）<div>王老师，对于深度学习这块儿我是个新手，查找网上的东西真是太多了，好像说的都有道理，真是不知道该看些啥，能否推荐一些经典papers作为进一步学习的资料吗？十分感谢！</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（43） 💬（4）<div>Embedding预训练的优点：1.更快。因为对于End2End的方式，Embedding层的优化还受推荐算法的影响，这会增加计算量。2.难收敛。推荐算法是以Embedding为前提的，在端到端的方式中，在训练初期由于Embedding层的结果没有意义，所以推荐模块的优化也可能不太有意义，可能无法有效收敛。
Embedding端到端的优点：可能收敛到更好的结果。端到端因为将Embedding和推荐算法连接起来训练，那么Embedding层可以学习到最有利于推荐目标的Embedding结果。</div>2020-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b4/99/79a21147.jpg" width="30px"><span>轩</span> 👍（24） 💬（1）<div>老师您好，关于课后思考题有些疑惑，预训练emb和end2end emb：
首先 预训练emb实现了模型和emb的解耦，解耦之后，模型只需要关注emb即可，emb就是物品的本征表示，线上服务也就是查redis拿emb完成推断。缺点么，感觉有风险？假如emb是由上游提供，上游重train之后，每一维的隐含意义就变化了，下游模型必须重新train，否则不就出错了？

end2end的训练的话，对emb可以finetune，理论性能更高，但是总感觉不甚灵活？对于新的物品不停更新发布，岂不是nn.embedding的vocab需要不停的扩充，模型也需要不停的再次训练？

嗯，感觉在工程落地时，面对非静态的物品集，要么不灵活要么有风险？</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（10） 💬（2）<div>请问老师，有两个问题有点疑惑，第一个问题是采用Node2Vec算法时，当前节点v到下一个节点x的概率在经过进出参数和返回参数调整后是否需要做概率的归一化操作，使节点v到所有下一节点的概率为1呢？第二个问题是既然我们希望网络要么体现“同质性”要么体现“结构性”的特点，那么为什么一定要设定两个参数p和q，而不是仅用一个参数m(打比方)来实现，当m小，就是同质性强，结构性弱，当m大，就是同质性弱，结构性强？</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8c/74/2bbd132d.jpg" width="30px"><span>Dikiwi</span> 👍（8） 💬（3）<div>直观理解，预训练的emb本身因为是有一定意义的，所以喂给mlp之后理论上可以加速收敛，但因为这个emb是通过其他方法训练出来的，本身不是对该模型服务的，所以很可能走到局部最优解？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b7/42/1f44ce49.jpg" width="30px"><span>远方蔚蓝</span> 👍（7） 💬（2）<div>老师后面会介绍一下GraphSAGE和GAT在推荐的应用与实践吗，业界现在用的挺多。</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/99/f0/ba3c0208.jpg" width="30px"><span>Geek_63ee39</span> 👍（7） 💬（5）<div>“首先，为了使 Graph Embedding 的结果能够表达网络的“结构性”，在随机游走的过程中，我们需要让游走的过程更倾向于 BFS（Breadth First Search，宽度优先搜索）”
这里应该是DFS吧？并且同质性是使用BFS</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/42/69/8c56cea0.jpg" width="30px"><span>inkachenko</span> 👍（5） 💬（1）<div>老师，我想问一下deep-walk随机选择起始点的时候，是所有节点等概率选取呢？还是像HMM一样，以原始行为序列中节点出现次数为权重建立一个初始状态概率分布，再随机选取呢？感觉后一种更加合理。。</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（5） 💬（3）<div>老师知道有什么sample code， 可以把转移概率矩阵（项目中的transitionMatrix 和itemDistribution ）生成图5这种graph可视化图吗？感觉在做presentation的时候，人们就认图，没有图感觉说再多也没有热烈的反馈</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/9a/fe/a984c940.jpg" width="30px"><span>雪焰🐻🥑</span> 👍（5） 💬（2）<div>对于文中的:&quot;“预训练应用”指的是在我们预先训练好物品和用户的 Embedding 之后，不直接应用，而是把这些 Embedding 向量作为特征向量的一部分，跟其余的特征向量拼接起来&quot;
请问老师，比如对文本的embedding x和图像的embedding y会是得到不同的维度，这种情况下怎么把x和y拼接起来输入DL 模型呢？直接concatenate么？不知道下节课会不会涉及到具体操作，谢谢老师!</div>2020-10-16</li><br/><li><img src="" width="30px"><span>Wa</span> 👍（4） 💬（2）<div>一直没动手尝试item2vec和graph embedding相关算法，因为对于我们的业务，不同商品之间关系比较独立，不存在“先看了A明星新闻，再看与他有绯闻的B明星新闻，再看他们共同作品的新闻...”这种有时序关系的用户行为序列，所以不确定用类似word2vec这种作用于文本（文本天然具有强前后相关性）的模型是否有效。我们的用户依次点击A - B - C - D可能仅仅是因为展示列表时这个顺序，而不存在A离B近而离D远这种信息，不知道老师怎么看。</div>2021-01-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKS70PShNZaxpibFc1gWuvibbg3hXR4YKm3MkNgX0n56hWUicN0JfB2GQ6I9UicBfKABH6dkfVDPohA6Q/132" width="30px"><span>香格里拉飞龙</span> 👍（3） 💬（2）<div>老师，关于同质性和结构性及其表达，不知这样理解是否可行呢？
1.倾向于广度优先搜索时（p越小），节点更容易在起始点周围跳转，而且经常会返回前一节点，反应微观的、局部的关系。
比如起始点为图3中节点u，游走长度设为4。所以游走序列可能是u s1 u s1，u s1 u s2，u s1 s2 s1，u s1 s2 u，……，经过许多次游走后，会发现游走序列大部分都在u及其相邻点s1、s2、s3、s4之间转悠，而且其中会有一部分序列在转悠一圈后又回到u。于是可以稍微推断出u是中心节点，且s6的情况与之类似。
而如果起始点设为s9，虽然也有一部分游走序列中多次出现s9，但是若序列从s9到s6，之后又跳转到了s5或s7，就无法再回到s9。在广度优先中，s9为起始点无法返回自身的概率显然比u为起始点无法返回自身的概率大。
故广度优先倾向于表现结构性。
2.倾向于深度优先搜索时（q越小），节点更容易跳转至更远处节点，反应宏观的节点关系。
依然以起始点u举例，游走长度为4。深度优先下更能游走至更远更新的节点，游走序列可能是u s1 s2 s4，u s1 s3 s4，u s1 s2 u，u s1 s2 s5，……，游走序列在更大的概率上游走至s5、s6，并且因为s1和s3并没有外部的节点与之相连，会有一部分序列依然在u和其相邻节点中转悠。所以表现出同质性，与同一节点距离相近的，高度互联且属于相似社区。
还有一种理解。如果一个节点a及其四个相邻节点高度互联，与上图中u极其邻点相似，然而这四个邻点又各自与其他点相连，这些更远处点距离a点为2。于是在游走过程中，有一部分游走序列在a点及其邻点间转悠，也有一部分游走至更远点，不再回来。但是因为a与邻点高度互联，在a与邻点间游走的概率更大。此也能表达同质性。
</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/de/3b/c15d2d9f.jpg" width="30px"><span>DAMIAN</span> 👍（3） 💬（1）<div>课后思考：
1. pre-training 优点：embedding泛化能力强，即使后接不同的任务，也都可以work，bp的层数很少，收敛比较快
缺点：精度一般比较低，不能针对特定任务优化
2. end2end: 优点：一般精度比前者高，embedding可以针对特定任务优化
缺点：训练慢，embedding几乎不可能用来做其他的任务，泛化能力比较差

想请问老师，按照迁移学习的思路，将预训练的embedding放到end2end模型中fine-tuning会不会有好的效果呢？</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/e6/c3/35099b03.jpg" width="30px"><span>褚江</span> 👍（3） 💬（4）<div>王老师，我想请问， embedding层可以加入到树模型中吗？很多时候在比较小的样本上训练，感觉Lgbm会好很多，但好像没有人这样做是吗？
</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7d/15/c099a439.jpg" width="30px"><span>Dive</span> 👍（3） 💬（2）<div>王老师，好多论文里介绍完自己的深度学习推荐模型A都会加一个预训练嵌入的对比。我理解是将预训练得到的嵌入作为深度学习推荐系统模型A的嵌入的初始化；我其实很疑惑，实际中应该是情况①还是情况②呢？感谢老师~
①这些嵌入在深度学习模型中就固定住，不会更新
②这些嵌入仅仅是初始化作用，在模型中还会更新</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/72/73/d707c8be.jpg" width="30px"><span>MutouMan</span> 👍（2） 💬（1）<div>End2end的方法肯定能够得到更精确的表达：1. 数据的时效性； 2. 和其它特征共同训练，还可以学习到交叉后的效果； 3. 根据我们设定的目标（loss function），得到的embedding会更趋向于我们想要的结果，可能会损失些generalization，但是bias会减少。但是end2end明显就是要花很多时间了，不可能做到线上训练和推荐都在ms级。
预训练：最大的好处就是模型上线后，可以快速抽取特征进行召回然后排序。当然就是会有时间上的滞后，推荐的效果是会比理论上差。</div>2021-04-27</li><br/><li><img src="" width="30px"><span>Geek_fdb832</span> 👍（2） 💬（1）<div>想求教一下王老师，graph embedding只是embedding了graph有关的信息 (node之间的关系) 吗？如果一个item有些其他的性质，比如price, name, category, 这方面的信息能也能在随机游走的过程中放在graph embedding里吗？</div>2021-04-25</li><br/><li><img src="" width="30px"><span>Sanders</span> 👍（2） 💬（1）<div>结合Word2Vec这样理解对不对？
1. Random Walk和Node2Vec实际上是构建语料-训练样本的过程，Graph Embedding结构和之前Word2Vec是一样的
2. Word2Vec中会将相邻词的label值设为1，Node2Vec会用跳转概率作为相邻节点的label值</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（2） 💬（3）<div>Node embedding 的最终结果看起来看起来更像聚类结果。
是否可以利用聚类算法来实现Node embedding的过程呢？</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（1） 💬（1）<div>老师，有基于地图的推荐系统案例介绍吗？</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/18/84/2f950e5e.jpg" width="30px"><span>乔伊波伊</span> 👍（1） 💬（1）<div>老师你好，请问像xgboost等树模型适合使用embedding出来的特征作为输入吗，这样在树分裂的时候会不会更倾向于embedding特征而弱化原始特征如年龄、点击率等</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/4d/d7/5f835e27.jpg" width="30px"><span>温华</span> 👍（1） 💬（1）<div>Embeddding预训练

优点：embeddding训练与模型训练解耦，训练后的embedding再喂给推荐模型，可以加速收敛

缺点：工程实现上更复杂，因为解耦，需要训练两个模型，embedding模型产生的embedding向量需要刷到线上特征库进行存储，然后才能给模型输入时使用

E2E

优点：embeddding训练包含在推荐模型训练过程中，体现了端到端，流程上更容易，不用再额外考虑embedding训练

缺点：embedding层包含大量参数，训练可能难以收敛，甚至可能因为embedding矩阵过大，计算资源不够导致无法训练</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/17/43/928d89a7.jpg" width="30px"><span>Geek_elpkc8</span> 👍（1） 💬（1）<div>你能尝试对比一下 Embedding 预训练和 Embedding End2End 训练这两种应用方法，说出它们之间的优缺点吗？
预训练：
优点；更容易实现，实现更快，且不需要标注数据
缺点：学习出的向量仅有数据的结构距离特性，无法进一步完成具体任务。
e2e：
优点：可以完成更多的任务，由于是监督学习，可以获得更高的任务指标。
缺点：需要标注数据，成本高</div>2021-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（1） 💬（2）<div>老师， 用deep walk解决原本就是graph的结构数据很有道理，但是像我们电影推荐这正，原本是序列的数据，通过建图，然后在生成序列数据，这样用deepwalk，相比于直接用原有序列样本直接导入word2vec的有什么优势呢？我唯一能想到的好处就是生成比原有序列更多的样本，来扩充样本数量防止过拟合。 但是如果原有序列数据已经足够大，是不是deepwalk就没有意义了。</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7c/5b/7a8d842c.jpg" width="30px"><span>Lucifer</span> 👍（1） 💬（1）<div>图5实验中，上图：采用bfs构图，近的emb相似同色，体现同质性；下图：采用dfs构图，远的emb相似同色，体现同构性。跟下文以及答疑中的bfs对应同构，dfs对应同质是不是有些矛盾。</div>2020-11-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erUKWZy1fBBcJncWRNh9M3TkjThqgsIIpmGOTCyg2IN80IDf3COkeWyTLHliczAppIkfBgCJTsUn1g/132" width="30px"><span>马龙流</span> 👍（0） 💬（1）<div>在这边，边和边的权重怎么确定呢？</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c7/21/6a8e267a.jpg" width="30px"><span>β</span> 👍（0） 💬（1）<div>你好，结构性通过BFS随机游走搜索一个中心节点和它周围的节点建立，结构性关系。但同质性为啥是DFS随机游走？比如你随机游走的结果是u和s6，它们应该是同结构性的，和u同质的应该还是它周围那些节点，就是之前结构性随机游走建立的。？？？</div>2021-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（0） 💬（3）<div>你能尝试对比一下 Embedding 预训练和 Embedding End2End 训练这两种应用方法，说出它们之间的优缺点吗？
Embedding 预训练
优点：
1. 更容易实现，实现更快，且不需要标注数据；
缺点：
1. 难以收敛；
2. 较于End2End，预训练可能损失一些效果；

Embedding End2End 训练
优点：
1. 能够找到embedding层在这个模型结构下的最优解。
2. 收敛速度快；
缺点：
1. 需要标注数据，成本高；
2. End2End训练在实际的应用中没有发现效果有明显提高。

王老师，您好！~ 请问： 
有向有权图：N+(v_i) 是节点 v_i所有的出边集合，这里的“出边”是指哪些边呢？
无向无权图：N+(v_i) 是节点 v_i所有的边集合，这里的 “边” 是指哪些边呢？</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1d/bfd0a242.jpg" width="30px"><span>辛湛</span> 👍（0） 💬（1）<div>老师问一下一般word2vec这种都是预训练作为特征用到推荐精排或粗排模型的,那么word2vec如何更新呢 怎么能确定更新后特征分布还是相似的。尤其是特征是打印的，是否要进行离线的特征回滚?谢谢</div>2020-12-16</li><br/>
</ul>