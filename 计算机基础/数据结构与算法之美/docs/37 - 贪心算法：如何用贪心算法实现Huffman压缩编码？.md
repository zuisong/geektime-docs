基础的数据结构和算法我们基本上学完了，接下来几节，我会讲几种更加基本的算法。它们分别是贪心算法、分治算法、回溯算法、动态规划。更加确切地说，它们应该是算法思想，并不是具体的算法，常用来指导我们设计具体的算法和编码等。

贪心、分治、回溯、动态规划这4个算法思想，原理解释起来都很简单，但是要真正掌握且灵活应用，并不是件容易的事情。所以，接下来的这4个算法思想的讲解，我依旧不会长篇大论地去讲理论，而是结合具体的问题，让你自己感受这些算法是怎么工作的，是如何解决问题的，带你在问题中体会这些算法的本质。我觉得，这比单纯记忆原理和定义要更有价值。

今天，我们先来学习一下贪心算法（greedy algorithm）。贪心算法有很多经典的应用，比如霍夫曼编码（Huffman Coding）、Prim和Kruskal最小生成树算法、还有Dijkstra单源最短路径算法。最小生成树算法和最短路径算法我们后面会讲到，所以我们今天讲下霍夫曼编码，看看**它是如何利用贪心算法来实现对数据压缩编码，有效节省数据存储空间的**。

## 如何理解“贪心算法”？

关于贪心算法，我们先看一个例子。

假设我们有一个可以容纳100kg物品的背包，可以装各种物品。我们有以下5种豆子，每种豆子的总量和总价值都各不相同。为了让背包中所装物品的总价值最大，我们如何选择在背包中装哪些豆子？每种豆子又该装多少呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>开心小毛</span> 👍（229） 💬（14）<div>找零问题不能用贪婪算法，即使有面值为一元的币值也不行：考虑币值为100，99和1的币种，每种各一百张，找396元。
 动态规划可求出四张99元，但贪心算法解出需三张一百和96张一元。</div>2018-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/fa/8a5167cd.jpg" width="30px"><span>Jalyn</span> 👍（73） 💬（11）<div>想知道目前没掉队的有多少 哈哈</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/5c/8d53165e.jpg" width="30px"><span>bingo</span> 👍（67） 💬（5）<div>@吴：wiki上的哈夫曼树是标准的生成步骤，老师这里举的例子是一种特殊情况，哈夫曼树构建的一般性方法在本科的教程上就写的很通俗了。
我用wiki里的值举个例子吧：原始集合的值是[2,3,4,4,5,7]
第一步：从原始集合中取出最小的两个值并将这两个值从原始集合中剔除，这两个最小的值相加得到一个新的值并加入原始集合，这两个小值作为这个新值的树叶，新值当然就是树根了。这一步执行之后原始集合就变成了这样：
       [ ⑤,  4,4,5,7]
	&#47; \
      2   3

第二步：从更新后的集合中再取最小的两个值并剔除，同样相加得到新值加入到集合。这一步执行之后集合就变成了
       [⑤,          ⑧  ,5,7]
	&#47; \          &#47;\
      2   3       4  4

第三步，重复以上步骤，你懂得。结果是：
       [ ⑩,          ⑧,    7]
	 &#47; \          &#47; \
        5   ⑤       4  4
	    &#47; \  
	   2  3
第四步，结果是：
       [ ⑩,          15,]
	&#47; \            &#47; \
      5   ⑤         7   ⑧
	   &#47;\              &#47; \
	  2 3           4  4
最后一步，结果是：
               (25)           (打不出圆圈了，用这个代替，应该不难理解，嗯)
              &#47;    \
         ⑩          15
	&#47; \           &#47; \
      5   ⑤        7   ⑧
	  &#47;\              &#47; \
	  2 3           4  4

wiki哈夫曼树链接：https:&#47;&#47;zh.wikipedia.org&#47;wiki&#47;%E9%9C%8D%E5%A4%AB%E6%9B%BC%E7%BC%96%E7%A0%81
ps:大半夜手打，排版扎心</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（15） 💬（7）<div>老师 区间覆盖的问题， (1-5) 和 (2-4) 中为什么选(2-4)  方便老师解释下吗， 贪心不能全局最优 用贪心 如何在这个问题上全局最优呢</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/43/223c5435.jpg" width="30px"><span>发飙的蜗牛</span> 👍（11） 💬（1）<div>个人觉得分糖果不能使用贪心算法，如果使用可以加个条件一个孩子只能分一个糖果，因为可能存在孩子的满意度大于最小的糖果，但是最小的两个的和刚好满足。这个情况贪心就无法满足了。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/6a/b0d7987b.jpg" width="30px"><span>天，很蓝 ～</span> 👍（2） 💬（5）<div>如果文档中只有4个字符，分别是a，b，c，d出现的频率相等，都是100次。如果用00，01，10，11分别表示a，b，c，d的话，总共需要800bit就可以了。但是如果用霍夫曼编码的话，用1，01，001，000分别表示a，b，c，d的话反而需要900bit。这个是不是说明霍夫曼编码有时候是起不到压缩作用的？望老师解答</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/dc/32e78f02.jpg" width="30px"><span>乐凡</span> 👍（2） 💬（3）<div>老师，我觉得那个霍夫曼编码可能有点缺陷，就是不同字符在字符串中出现的频率很接近，那如果还是按照给每个字符用不同长度的二进制码表示，很有可能会比前面用相同二进制码表示耗费的空间多（亲自测过）。我觉得每一个字符在字符串中出现的频率需要满足一定的大小差距，这样使用空间才会比使用相同数量的二进制码更少。这个大小差距点的公式不太好算，笨一点的办法就是用两种方式比较下占用空间大小。</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（2）<div>霍夫曼编码原理 , 不是要求左子树小于右子树么, 按照您的写法, 都依次排列在了右子树啊. 

</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/a0/f03d20cd.jpg" width="30px"><span>likun</span> 👍（0） 💬（1）<div>老师 你给的钱币找零的例子是可以用贪心回去到最优解 但存在其他面额的例子对于贪心是获取不到最优解的 为什么你给的例子用贪心就能获取到最优解呢？</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（1）<div>上面霍夫曼编码构造出的那个树形结构，是不是解码也可以用？？</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/a2/9450ef89.jpg" width="30px"><span>刘涛涛</span> 👍（0） 💬（1）<div>请问老师，区间覆盖那道题是不是应该每次选取剩余区间最大的呢，也就是每次排序需要按照end由小到大，然后在判断他是否和前面有重叠呢</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/e4/a79531ad.jpg" width="30px"><span>GJ</span> 👍（0） 💬（2）<div>分糖果：从最大的开始，分配给需求最大的小孩，也可以满足最多的小孩数。这逻辑没错吧</div>2019-03-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqPn4U0Ix3eB0Cguuw5qmDPGDQODMXH5BcoJEBe1QHJ1709xBfK7q9JePCXdHhvuMAicBAh3GpPe3A/132" width="30px"><span>ddsoma</span> 👍（0） 💬（2）<div>老师关于这个区间覆盖“我们按照起始端点从小到大的顺序对这 n 个区间排序。”

能不能按照终点从小到大来排序，然后检查的活动i的开始时间starti小于最近选择的活动j的结束时间endj，则不选择活动i，否则选择活动i加入集合中。</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/08/d2/83bdc5dd.jpg" width="30px"><span>若星</span> 👍（0） 💬（1）<div>不能在留言下回复，就整个踩的功能，让点赞数减去踩的数，决定排序。现在，错的答案，误导大家，都可以审核通过😒</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（0） 💬（1）<div>表示第二个思考题怎么安排都是一样的吧，一个窗口是串行的，只能一个个的服务</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/9d/30c79c4b.jpg" width="30px"><span>程序员联盟</span> 👍（0） 💬（1）<div>请问老师会不会有关于“并查集”（Union-Find）的课？谢谢。LeetCode好多题目用到这个</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（0） 💬（1）<div>老师，我也不知道怎么描述，其实这个哈夫曼编码困惑了我许久，我也不知到怎么描述，现在您描述的这种状态是一直在原有基础上叠加，没有与一个节点跟两个节点组成的新节点在同一层的，维基百科上有个动图描述2，3，4，4，5，7这几个节点，恩 感觉构建有点不一样，这最后虽然编码结果不一样，效果一样吗？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（0） 💬（1）<div>老师的霍夫曼编码是不是不完整，只是一个简介？感觉多一种字符，编码就多一位，如果一个文档里字符种类比较多，出现概率又相当，压缩效果是不是不太好。</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（1）<div>区间覆盖那个例子 是不是应该取的是 startIndex + range 的最小值，而不是单纯的区间最小</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/b0/9d11054a.jpg" width="30px"><span>smarttime</span> 👍（0） 💬（1）<div>希望老师在理论方面还是深入些，在掌握多个案例后理解理论，指导解决更多的问题。既然贪心选择不能总得出最优解，满足什么特征的问题可以什么样的不可以，不能全靠题目量凭经验感觉吧！最优子结构和贪心选择性质拿一个案例介绍一下总是好的，另外希望老师多讲讲自己在知识上的理解！</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d3/a8/fedf0141.jpg" width="30px"><span>cirno</span> 👍（339） 💬（44）<div>1、由最高位开始，比较低一位数字，如高位大，移除，若高位小，则向右移一位继续比较两个数字，直到高位大于低位则移除，循环k次，如：
4556847594546移除5位-》455647594546-》45547594546-》4547594546-》4447594546-》444594546

2、由等待时间最短的开始服务</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/d0/49b06424.jpg" width="30px"><span>qinggeouye</span> 👍（61） 💬（10）<div>1、在一个非负整数 a 中，希望从中移除 k 个数字，让剩下的数字值最小，如何选择移除哪 k 个数字呢？

整数 a，由若干位数字组成，移除 k 个数字后的值最小。从高位开始移除：移除高位数字比它低位数字大的那个；K 次循环。

也可以用 Top K 排序，求出 K 个最大的数字，移除。

2、假设有 n 个人等待被服务，但是窗口只有一个，每个需要被服务的时间长度是不同的，如何安排被服务的先后顺序，才能让这 n 个人总的等待时间最短？

每个人需要被服务的时间不一样，但所有人加起来总的被服务时间是固定的。

题意是求 n 个人总的等待时间，每个人在被服务之前，所经过的等待时间是不同的。

而当前被服务的人所需的服务时间，会累加到剩下的那些等待被服务人的等待时间上。

要使 n 个人总的等待时间最短，那么每次安排服务时间最短的那个人被服务：堆排序（小顶堆）。


另外，@Alexis何春光 的留言，第一句话表示赞同。</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0a/dd/88fa7b52.jpg" width="30px"><span>Geek_41d472</span> 👍（40） 💬（0）<div>霍夫曼编码，用一个树来避免某个字符的编码是另一个字符编码的前缀，真的是好巧妙</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/dd/b201cf13.jpg" width="30px"><span>Alexis何春光</span> 👍（38） 💬（12）<div>留言里feifei说的两种解决思路都是错的，给的链接也失效了.... 老师可以回复一下防止误导后来的同学呀！
以及没有看出来霍夫曼算法和贪心算法有什么联系，求详细讲解</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（34） 💬（13）<div>1，在一个非负整数 a 中，我们希望从中移除 k 个数字，让剩下的数字值最小，如何选择移除哪 k 个数字呢？
对于此题，我的求解思路是每次选择数据的最高位的数据值进行移除，这样我们每次选择的移除的数值都是最大的，剩下的数值也是最小的。
比如，数据5892，将数据拆成5000,800,90,2，然后使用大顶堆来进行存储，然后每次移除大顶堆中堆顶最大的元素。

2，假设有 n 个人等待被服务，但是服务窗口只有一个，每个人需要被服务的时间长度是不同的，如何安排被服务的先后顺序，才能让这 n 个人总的等待时间最短？
对于此问题，我的求解思路是让待时间最长的来安排先后顺序
比如，现在有3个人，a、b、c,a等待了10分钟，b待待了20分钟，c待待了30分钟
同样使用大顶堆来进行存储等待时间，堆顶的元素就是当前等待时间最长的人
然后每次从堆拿出堆顶元素的人来进行服务，这样就可以让这n个人的总的等待时间最短。




对于学习的贪心算法，老师虽然只进行了理论讲解，但我看完了老师所讲的，我对贪心算法的理解有了一定的认识，我就试着把贪心算法的内容中涉及的东西，都翻译成了代码，
感觉收获良多，也把这个分享给童鞋，希望对他们有帮助。
1，这是第一个示例，背包中豆子的最大价值的问题
https:&#47;&#47;github.com&#47;kkzfl22&#47;datastruct&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;com&#47;liujun&#47;algorithm&#47;greedyAlgorithm&#47;case1
2，这是孩子分糖果的问题
https:&#47;&#47;github.com&#47;kkzfl22&#47;datastruct&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;com&#47;liujun&#47;algorithm&#47;greedyAlgorithm&#47;case2
3，这是钱币支付的问题
https:&#47;&#47;github.com&#47;kkzfl22&#47;datastruct&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;com&#47;liujun&#47;algorithm&#47;greedyAlgorithm&#47;case3
4，这是区间覆盖的问题
https:&#47;&#47;github.com&#47;kkzfl22&#47;datastruct&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;com&#47;liujun&#47;algorithm&#47;greedyAlgorithm&#47;case4
5，这是霍夫漫编码的实现
https:&#47;&#47;github.com&#47;kkzfl22&#47;datastruct&#47;tree&#47;master&#47;src&#47;main&#47;java&#47;com&#47;liujun&#47;algorithm&#47;greedyAlgorithm&#47;huffman

欢迎大家与我交流，也欢迎老师给我指正，谢谢</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/e0/9a79ddac.jpg" width="30px"><span>🐱您的好友William🐱</span> 👍（23） 💬（0）<div>给大家提个醒，货币找零问题如果没有C1货币的话得用动态规划去解，如果出现{C2，C7，C10}货币找零11块的时候使用greedy就会出现找不开的情况。。。。有C1就不会出现找不开的情况且多个C1可以构成任何面值，所以这种情况下使用greedy是对的！（leetcode322题调了一下午的路过。。。）</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（19） 💬（0）<div>打个卡，我还在</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/e2/0e1c6c5a.jpg" width="30px"><span>CathyLin</span> 👍（17） 💬（0）<div>课后思考：
1. 第一道题一开始没有想到...以为直接删除最大的那 k 个数字就好了，后来举了几个样例发现是错的。然后看了评论区小伙伴们的留言，太奇妙了！！！我是真的没有想到这种思路😫 
1) 从高位往低位走，删掉高位比低位大的数；为什么这样子是好的呢？试想:
4596743 如果我们只能删一位，我们会删第三位的 9，因为这样就相当于是把高位给减少了，变成了456743，但是如果删 6，变成了 459743 则没有之前那个优。删后面的数更起不到高位的那种作用。
2) 如果所有数字都是递增的，那么我们删除倒数 k 个数字就好了。

2. 想让所有人的等待时间最短，那么我们得先处理服务时间短的，尽快把他们处理完了才能够处理后面的人！

贪心反思：有些时候思路还是难以打开，可能还是跟老师说的那样，多练习、多积累才是最好的学习方法！</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/84/d0ec0064.jpg" width="30px"><span>睡痴儿😑</span> 👍（17） 💬（0）<div>第一个题，可以反着来想。给定另一个数组，怎么从中原本的中挑出n-k个，使其值最小。
首先第一位必须要是最小的一个，但是因为有顺序，所以只能是从0到n-1-k个中挑一个最小的，下标为m。以后依次类推，从m到n-k中挑一个最小的。如果有相等的情况，以下标小的为准。
第二个，就是从小到大排序即可。</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（15） 💬（1）<div>区间覆盖问题，把区间按照结束时刻排序，每次选择最早结束且没有冲突的区间即可</div>2019-04-15</li><br/>
</ul>