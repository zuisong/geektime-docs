今天我来带你进行关联规则挖掘的学习，关联规则这个概念，最早是由Agrawal等人在1993年提出的。在1994年Agrawal等人又提出了基于关联规则的Apriori算法，至今Apriori仍是关联规则挖掘的重要算法。

关联规则挖掘可以让我们从数据集中发现项与项（item与item）之间的关系，它在我们的生活中有很多应用场景，“购物篮分析”就是一个常见的场景，这个场景可以从消费者交易记录中发掘商品与商品之间的关联关系，进而通过商品捆绑销售或者相关推荐的方式带来更多的销售量。所以说，关联规则挖掘是个非常有用的技术。

在今天的内容中，希望你能带着问题，和我一起来搞懂以下几个知识点：

1. 搞懂关联规则中的几个重要概念：支持度、置信度、提升度；
2. Apriori算法的工作原理；
3. 在实际工作中，我们该如何进行关联规则挖掘。

## 搞懂关联规则中的几个概念

我举一个超市购物的例子，下面是几名客户购买的商品列表：

![](https://static001.geekbang.org/resource/image/f7/1c/f7d0cc3c1a845bf790b344f62372941c.png?wh=468%2A195)  
**什么是支持度呢？**

支持度是个百分比，它指的是某个商品组合出现的次数与总次数之间的比例。支持度越高，代表这个组合出现的频率越大。

在这个例子中，我们能看到“牛奶”出现了4次，那么这5笔订单中“牛奶”的支持度就是4/5=0.8。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（16） 💬（1）<div>我也是自己的理解，不知道是否正确，给大家参考一下

构建子树
1.假设已经完成创建项头表的工作，省略count+1
2.扫描数据集，按照项头表排列好的结果，一次创建节点
3.因为尿布出现在所有订单中，没有例外情况，所以这只有一个子节点
4.因为牛奶出现在尿布中的所有订单里，所以只有一个子节点
5.由表中数据可得，在出现牛奶的订单中，面包出现的情况，分为两种，
1）出现3次面包，出现在有牛奶的订单中
2）出现一次面包，出现在没有牛奶的订单中
故，生成两个子节点
6.后续内容属于迭代内容，自行体会


3.创建条件模式集
是一个减掉子树过程。将祖先节点的支持度，记为叶子节点之和，减少频繁项集。
简单理解，就是有几个叶子，说明最开始的节点，怀了几个孩子，怀几个生几个
理解
1.创建含有啤酒的FP树，只有订单中含有啤酒的频繁项集才存在


2.去掉啤酒节点，品酒节点为空，得到，两个频繁项集
见图可理解



作业
1.工作原理
1）K=1，计算支持度
2）筛选小于最小支持度的项集
3）判断如果项集项集为空，K-1项集为最终结果
4）判断失败，K=K+1，重复1-3
2.优化
1）利用FP树和项头表，减少频繁项集的数量存储和计算</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/a0/f12115b7.jpg" width="30px"><span>Sam.张朝</span> 👍（9） 💬（1）<div>https:&#47;&#47;www.ibm.com&#47;developerworks&#47;cn&#47;analytics&#47;library&#47;machine-learning-hands-on2-fp-growth&#47;index.html    FP 还是这里说的清楚</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/d1/076482f3.jpg" width="30px"><span>白夜</span> 👍（4） 💬（1）<div>Apriori 的工作原理：
0.设置一个最小支持度，
1.从K=1开始，筛选频繁项集。
2.在结果中，组合K+1项集，再次筛选
3.循环1、2步。直到找不到结果为止，K-1项集的结果就是最终结果。

FP-Growth相比Apriori的优点：
降低了计算复杂度，只要遍历两次数据集。可以直接得到指定商品的条件模式基。</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>老师，想问下那置信度和提升度在Aproiri和FP-Growth算法中应用在哪了</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/be/1f2409e8.jpg" width="30px"><span>梁林松</span> 👍（1） 💬（1）<div>Apriori算法工作原理是通过计算子集的置信度来寻找频繁项集，从而确立关联。
PF-Growth算法是改进的 Apriori, 改进之处在于它是按照明确品类去计算频繁项目集的，而不是去求全部数据集的频繁项集。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a6/7c/fc571405.jpg" width="30px"><span>ken</span> 👍（1） 💬（1）<div>Apriori挖掘频繁项集，那么置信度和提升度是对得出的频繁项集进行验证的是吧？如得出了啤酒的频繁项集后是对每个结果计算提升度，怎么选择最优的组合呢？是否会出现提升度大而置信度下降的情况？</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（0） 💬（1）<div>Apriori算法的原理：
1. 输入数据集合D，支持度阈值α
2. 扫描整个数据集，得到所有出现过的数据，作为候选频繁1项集。K=1，频繁0项集为空集
3. 扫描数据计算候选频繁K项集的支持度
4. 去除候选频繁K项集中支持度低于阈值的数据集，得到频繁K项集。如果得到的频繁K项集为空，则直接返回频繁K-1项集的集合作为算法结果，算法结束。否则继续对K项进行计算，直到没有更新的频繁项集

Apriori算法和FP-Growth算法的区别：
1. Apriori算法需要对数据集进行多次扫描，而FP-Growth只需要扫描数据集两次
2. Apriori算法可能产生大量的候选集。而FP-Growth只需要创建FP树来储存频繁项集，并在创建前对不满足最小支持度的项进行删除</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（2）<div>在这个基础上，我们将商品两两组合，得到 k=2 项的支持度
上面这句话下面的表，商品1，2的置信度应该为4&#47;5，表里面列的1&#47;5
我数了同时有商品1，2的订单有4个。
希望核实一下。</div>2020-04-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKerOHGs8VAMWj0ysxZpTPcARHEITiaH8YDJR7aoDNYhRpbLsZ0pJdJXIfzvR7u06iaKPBUoWfic5Zww/132" width="30px"><span>Geek_qsftko</span> 👍（0） 💬（1）<div> K=3 项的商品组合 是不是少了一个 1，3，5 组合啊</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/80/382e46b6.jpg" width="30px"><span>Red Cape</span> 👍（0） 💬（2）<div>构造FP树的过程这里看不懂，面包，啤酒为什么会拆分呢</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（67） 💬（7）<div>简述FP-Growth 算法创建过程：
【1】创建项头表。
 项     支持度
尿布  5
牛奶  4
面包  4
啤酒  3
【2】将数据集按照【尿布-牛奶-面包-啤酒】进行排序，得到
1）尿布、牛奶、面包
2）尿布、面包、啤酒、可乐
3）尿布、牛奶、啤酒、鸡蛋
4）尿布、牛奶、面包、啤酒
5）尿布、牛奶、面包、可乐
【3】构造FP树
1）遍历第1条数据，得到
尿布1 |牛奶1 |面包1
2）遍历第2条数据，得到
尿布2 |面包1 |啤酒1
         |牛奶1 |面包1
3）遍历第3条数据，得到
尿布3 |面包1 |啤酒1
         |牛奶2 |面包1
                  |啤酒1
4）遍历第4条数据，得到
尿布4 |面包1 |啤酒1
         |牛奶3 |面包2 |啤酒1
                  |啤酒1
5）遍历第5条数据，得到
尿布5 |面包1 |啤酒1
         |牛奶4 |面包3 |啤酒1
                  |啤酒1
【4】寻找条件模式基
1）以‘啤酒’为节点的链条有3条
-尿布1 |面包1 |啤酒1
-尿布1 |牛奶1 |面包1 |啤酒1 
-尿布1 |牛奶1 |啤酒1
2）FP子树
尿布3 |面包1 |啤酒1
        |牛奶2 |面包1 |啤酒1 
                 |啤酒1

3）“啤酒”的条件模式基是取以‘啤酒’为节点的链条，取‘啤酒’往前的内容，即
-尿布1 |面包1 
-尿布1 |牛奶1 |面包1 
-尿布1 |牛奶1 
</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（16） 💬（7）<div>使用步骤图来解释FG-Growth算法https:&#47;&#47;www.cnblogs.com&#47;zhengxingpeng&#47;p&#47;6679280.html</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8f/84/2c2d8c47.jpg" width="30px"><span>lipan</span> 👍（12） 💬（1）<div>k=2时，商品项集1,3的支持度是4&#47;5啊</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/a0/f12115b7.jpg" width="30px"><span>Sam.张朝</span> 👍（7） 💬（2）<div>构造FP 树，看不懂</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f0/16/76a08ec5.jpg" width="30px"><span>曹恒源</span> 👍（7） 💬（0）<div>您好，陈哥，在文章中，k=2,（1,3）的支持度，不应该是4&#47;5么？这部分的计算方式，不是（1,3）在总的购买的商品出现的次数除以总次数所得到的最后结果？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/0d/c4afec40.jpg" width="30px"><span>leestar54</span> 👍（5） 💬（4）<div>为啥“啤酒“的条件模式基为空呢？图上祖先节点尿布:3的支持度=3&#47;5大于0.5，这样啤酒的频繁项集可以得到{尿布，啤酒}</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c6/85/ef27e5ae.jpg" width="30px"><span>Kai</span> 👍（2） 💬（0）<div>这篇文章只介绍了计算频繁项集的算法呀，具体提升度在计算完频繁项集后该怎么用能进一步解释一下吗</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/47/6c2a60ee.jpg" width="30px"><span>Sniper</span> 👍（2） 💬（1）<div>这个支持度  不应该是个小于1的百分比么，怎么到输出结果里面都变成具体的数字了，这些数字的大小怎么理解呢  </div>2019-08-16</li><br/><li><img src="" width="30px"><span>lemonlxn</span> 👍（1） 💬（0）<div>商品相集 itemset，1、3 同时出现的支持度为 4&#47;5，不是1&#47;5，你把这个item给过滤了</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（1） 💬（0）<div>Apriori 的工作原理是根据排列组合来计算频繁项集，去掉低于阈值的，然后继续排列组合，直到频繁项集为空。FP-Growth 算法就是利用树来减少查询遍历的次数。</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cb/07/e34220d6.jpg" width="30px"><span>李沛欣</span> 👍（1） 💬（0）<div>支持度：购买ABC这一商品组合，在所有商品组合中的出现概率

置信度：购买A商品的条件下，购买B商品的概率

提升度：购买A商品又购买B商品的概率，与所有购买了B商品的概率之比。也就是购买A商品对购买B商品的可能性提升能力。

提升度＞1，说明相互促进
等于1，没影响，
＜1，相互排斥</div>2019-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/CqF8eiaanNteyu2U7FibYicjnw99VXZST61vvMpQKSd5iaLNW6EicLeFYyDOKJmg9rNx6KW90DwpPMKNxiben6fQeZjA/132" width="30px"><span>Geek_24abc6</span> 👍（0） 💬（0）<div>为什么没有使用提升度？</div>2023-03-24</li><br/><li><img src="" width="30px"><span>开心小毛</span> 👍（0） 💬（0）<div>请问老师：在“啤酒”的条件模式基中祖先节“尿布”的support为3，为啥“尿布”会被剪枝呢？3&#47;5的订单数是大于0.5的最小支持度要求的不是么？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/10/28d5a686.jpg" width="30px"><span>Longerian</span> 👍（0） 💬（0）<div>Apriori 算法咋看上去没有用到置信度，提升度这些指标，那前文介绍这些概念的目的是啥</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/35/87465798.jpg" width="30px"><span>成军</span> 👍（0） 💬（1）<div>(1.3)的支持度是4&#47;5，老师，有另外两个同学也提出来了</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/f1/0e934ca8.jpg" width="30px"><span>Maybrittnelson</span> 👍（0） 💬（0）<div>在Apriori的改进算法中，面包的条件模式基，应该只有{尿布，牛奶，面包}吧？因为{尿布，面包}中的面包为1，小于最小支持度的项可乐为2，得删除。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/65/91540892.jpg" width="30px"><span>Kery</span> 👍（0） 💬（0）<div>在创建FP子树前，提醒大家记得删除订单中不满足最小支持度的商品，再按照项头表对每个订单从高到底排序来依次构造FP树。</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（0） 💬（0）<div>1、Apriori 的工作原理吗？
Apriori算法的关键是频繁项集。
Apriori算法的基本过程是：
1、扫描一遍数据库，得到一阶频繁项集；
2、用一阶频繁项集构造二阶候选项；
3、扫描数据库对二阶候选项进行计数，删除其中的非频繁项，得到二阶频繁项；
4、然后构造三阶候选项，以此类推，直到无法构造更高阶的候选项，或到达频繁项集的最大长度限制。

2、相比于 Apriori，FP-Growth 算法都有哪些改进？
通过创建FP树存储频繁项集。减少存储空间。
整个生成过程只遍历数据集2次，减少计算量。

</div>2019-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a9/32/eb71b457.jpg" width="30px"><span>Grandia_Z</span> 👍（0） 💬（0）<div>1 2 5在k=2时就被筛选剔除了</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（0） 💬（0）<div>提升度 (A→B)= 置信度 (A→B)&#47; 支持度 (B)
那么：
当K=3时，提升度怎么求取？
当K&gt;3时，提升度怎么求取？</div>2019-02-20</li><br/>
</ul>