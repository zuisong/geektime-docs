互联网发展到现在，搜索引擎已经非常好用，基本上输入关键词，都能找到匹配的内容，质量还不错。但在1998年之前，搜索引擎的体验并不好。早期的搜索引擎，会遇到下面的两类问题：

1. 返回结果质量不高：搜索结果不考虑网页的质量，而是通过时间顺序进行检索；
2. 容易被人钻空子：搜索引擎是基于检索词进行检索的，页面中检索词出现的频次越高，匹配度越高，这样就会出现网页作弊的情况。有些网页为了增加搜索引擎的排名，故意增加某个检索词的频率。

基于这些缺陷，当时Google的创始人拉里·佩奇提出了PageRank算法，目的就是要找到优质的网页，这样Google的排序结果不仅能找到用户想要的内容，而且还会从众多网页中筛选出权重高的呈现给用户。

Google的两位创始人都是斯坦福大学的博士生，他们提出的PageRank算法受到了论文影响力因子的评价启发。当一篇论文被引用的次数越多，证明这篇论文的影响力越大。正是这个想法解决了当时网页检索质量不高的问题。

## PageRank的简化模型

我们先来看下PageRank是如何计算的。

我假设一共有4个网页A、B、C、D。它们之间的链接信息如图所示：

![](https://static001.geekbang.org/resource/image/81/36/814d53ff8d73113631482e71b7c53636.png?wh=1472%2A1007)  
这里有两个概念你需要了解一下。

出链指的是链接出去的链接。入链指的是链接进来的链接。比如图中A有2个入链，3个出链。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（25） 💬（2）<div>pagerank算法就是通过你的邻居的影响力来评判你的影响力，当然然无法通过邻居来访问你，并不代表你没有影响力，因为可以直接访问你，所以引入阻尼因子的概念。现实生活中，顾客比较多的店铺质量比较好，但是要看看顾客是不是托。</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（17） 💬（1）<div>复习感悟：
1.PageRank算法，有点像
海纳百川有容乃大（网页影响力=所有入链集合的页面的加权影响力之和）
像我汇聚的东西，越多，我就越厉害。

2.随机访问模型
有点像下雨。
海洋除了有河流流经，还有雨水，但是下雨是随机的（网页影响力=阻尼影响力+所有入链集合页面的加权影响力之和）</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（9） 💬（1）<div>作业
1.原理
1）基础：网页影响力=所有入链集合的页面的加权影响力之和

2）拉里佩奇加入随机访问模型，即有概率用户通过输入网址访问
网页影响力=阻尼影响力+所有入链集合页面的加权影响力之和

2.应用场景：
评估某个新行业怎么样，通过计算涌入这个行业的人的智力和数量。
如果这个行业，正在有大量的聪明人涌入，说明这是一个正在上升的行业。

作业及问题
转移矩阵
第一列是A的出链的概率
A0B1&#47;3C1&#47;3D1&#47;3
第二列是B的的出链的概率
A1&#47;2B0C0D1&#47;2
第三列是C的出链概率
A1B0C0D0
第四列是D的出链概率
A0B1&#47;2C1&#47;2D0

等级泄露的转移矩阵应该是
M=[0 0 1&#47;2 0]   
     [1 0  0   0]
     [0 0 1&#47;2 0]
     [0 1 0    0]

还是
M=[0 0 0 1&#47;2]   
     [1 0 0  0 ]
     [0 0 0 1&#47;2]
     [0 1 0  0  ]

假设概率相同，都为1&#47;4
进行第一次转移之后，会发现，后面的
W1=[1&#47;8]
[1&#47;4]
[1&#47;8]
[1&#47;4]

总和已经小于1了，在不断转移的过程中，会使得所有PR为0

等级沉没的转移矩阵怎么写？
M=[0 0 1 0]   
     [1 0  0 0]
     [0 0 0 0]
     [0 1 0  0]
</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cb/07/e34220d6.jpg" width="30px"><span>李沛欣</span> 👍（6） 💬（1）<div>有人的地方，就有入世和出世
有网络和地方，就有入链和出链

入世的人，链接的大牛越多，越有影响力，
对网站而言，链接出去的网页越多，说明网站影响力越大，但是越多链接进来你这里的网页，也直接影响到网站的价值。

出链太多，如同出世一样，耗散内力，排名等级越来越低，最终江湖再见。
入链太多，就可能成为流量黑洞，如同涉世太深的人一样走火入魔。

谷歌创始人拉里佩奇则力图破解等级泄露和等级沉没困境，创造了随机浏览模型。</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/42/aeb79b35.jpg" width="30px"><span>Ling</span> 👍（4） 💬（1）<div>其实提出阻尼系数，还是为了解决某些网站明明存在大量出链（入链），但是影响力却非常大的情形。比如说 www.hao123.com 一样的导航网页，这种网页就完全是导航页，存在极其多出链；还有各种搜索引擎，比如 www.baidu.com、www.google.com 这种网站，基本不存在出链，但是入链可能非常多。这两种网站的影响力其实非常大。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/d2/2cf975ea.jpg" width="30px"><span>S.Mona</span> 👍（3） 💬（1）<div>PageRank和机器学习和数据分析的关系是怎样的？</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（3） 💬（1）<div>1.把影响力转化为每日使用时间考虑。
在感兴趣的人或事身上投入了相对多的时间。对其相关的人事物也会投入一定的时间。
那个人或事，被关注的越多，它的影响力&#47;受众也就越大。而每个人的时间有限，一般来说最多与150人保持联系，相当于最多有150个出链。
其中，一部分人，没人关注，只有出链没有入链，他们就需要社会最低限度的关照，这个就是社会福利（阻尼）。
2.矩阵以前学了一直不知道在哪里可以应用，今天学了用处感觉还蛮爽的。</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（3） 💬（1）<div>一、学完今天的内容，你不妨说说 PageRank 的算法原理？
1、PageRank 的算法原理核心思想：
-如果一个网页被很多其他网页链接到的话说明这个网页比较重要，也就是PageRank值会相对较高；
-如果一个PageRank值很高的网页链接到一个其他的网页，那么被链接到的网页的PageRank值会相应地因此而提高。
2、公式
PR(u)=PR(v1)&#47;N1+PR(v2)&#47;N2+……
其中PR(u), PR(v1) 为页面影响力。N1, N2是v1, v2页面对应的出链总数。
3、算法过程
1）给每个页面分配相同的PR值，比如PR(u)=PR(v1)=PR(v2)=……=1
2）按照每个页面的PR影响力计算公式，给每个页面的PR值重新计算一遍
3）重复步骤2，迭代结束的收敛条件：比如上次迭代结果与本次迭代结果小于某个误差，我们结束程序运行；或者比如还可以设置最大循环次数。

二、你还能说一些 PageRank 都有哪些应用场景吗？
引用链接：https:&#47;&#47;36kr.com&#47;p&#47;214680.html
1、研究某段时间最重要的文学作品
2、研究与遗传有关的肿瘤基因
3、图书馆图书推荐
</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/53/23/5d081efe.jpg" width="30px"><span>梁智行</span> 👍（2） 💬（1）<div>用网络科学来理解算法就是，网页的影响力（中心度），体现在：很多人说这网页好（度中心度），说这网页好的网页也要好（特征向量中心度），就好像一个人牛不牛逼，首先他自己要很牛逼，然后很多人说他牛逼，最后说他很牛逼的人也要很牛逼。
</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/52/10c4d863.jpg" width="30px"><span>FeiFei</span> 👍（2） 💬（1）<div>PageRank原理：
通过聚合入链和出链的权重，来判断自身的排序。
因为可能没有入链或者外链，因此加入阻尼因子d，来将这种情况规避。</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b4/3a/02ea71fa.jpg" width="30px"><span>sunny</span> 👍（2） 💬（1）<div>这个计算PR权重的时候，是计算对象的每个入链的权重除以出链数量的之和，那从一开始计算的时候每个页面需要有个原始的权重值才行，这个原始权重是否就是1</div>2019-02-27</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ENStdZ2o72F2wqqWVcCnQ6EpLhOo3qohvibXCVQUrhXAnZxUHMpwyfs9oXHrCdSQ4byuVicMX2UbeiavFCib15wakw/132" width="30px"><span>Geek_34dbb7</span> 👍（1） 💬（1）<div>淘宝商品流量，某件商品流量越大，销量也会越好，但也要排除刷单</div>2020-05-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ziaN7rOONp15HJm6A9JoAYicJL8VA59x10DX4JZyvcfqmmpCnumXgAkNn37aFoALftyTaQNlUF7te54LibvVm20TQ/132" width="30px"><span>Geek_c9fa4e</span> 👍（1） 💬（1）<div>PageRank算法原理：
   一个网页的影响力=所有入链集合页面的加权影响力之和。
  简单来说，根据你周围的人来去判断你这个人得影响力。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/36/88/20b6a6ee.jpg" width="30px"><span>Simon</span> 👍（1） 💬（1）<div>为什么Rank Leak会造成PR为0，怎么算的？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4d/62/0fe9cbb3.jpg" width="30px"><span>William～Zhang</span> 👍（1） 💬（1）<div>老师，在计算一个网页u的影响力的时候，用到v的影响力，这是怎么得到的？</div>2019-11-14</li><br/><li><img src="" width="30px"><span>吃饭睡觉打窦窦</span> 👍（1） 💬（3）<div>为啥等级泄露，我的代码跑出来4个点的pr值没有出现0的情况</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dc/ce/03fdeb60.jpg" width="30px"><span>白色纯度</span> 👍（6） 💬（0）<div>转移矩阵用到了Marcov过程的部分知识，转移概率矩阵并不一定收敛，需满足条件：不可约，平稳（可逆）。等级泄露和等级沉没都是破坏了不可约的情况，使得马氏矩阵不具备平稳概率。而解决该问题的思想又与朴素贝叶斯的平滑处理相似，浅见，若老师有时间还望指正。</div>2019-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/50/91/0dd2b8ce.jpg" width="30px"><span>听妈妈的话</span> 👍（3） 💬（0）<div>有个人博客的人互互相交换友链，也是为了提高搜索引擎收录的rank吗？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8f/84/2c2d8c47.jpg" width="30px"><span>lipan</span> 👍（1） 💬（0）<div>最后图解。早期搜索引擎问题，写的是k-means算法的流程。</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（0） 💬（0）<div>PageRank算法的原理：PageRank算法首先根据不同网页节点的出链数量计算出它们的跳转概率并构成转移矩阵，然后指定各个节点的初始影响力，两个矩阵相乘形成第一次转移，之后不断用
转移矩阵乘以新形成的影响力矩阵，反复迭代，直至第n次后影响力矩阵不再发生变化，各个网页的影响力趋于平衡。
实际例子：一个演员如果都是与知名导演合作，并且演的都是重要角色，说明这个演员在圈内的影响力较高。</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0a/83/f916f903.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>PageRank感觉跟机器学习没什么关系，PageRank的模型建立以后，只能用来评价现有的网络里结点的影响力而已。而不会后续拿这个模型和新的数据去预测未来</div>2020-11-05</li><br/>
</ul>