你好，我是微扰君。

上一讲，我们讲到如何利用散列表解决类似“文档中不同单词计数”的问题，并以JDK中HashMap的实现为例讲解了散列表背后的思想。

单词计数这个问题最基本的解决思路就是建立一个线性的符号表，每次计数的时候，遍历符号表就可以找到对应单词的计数器，做相应的累计计数操作就可以了。

为了更快地查找到单词的计数器，有两种优化思路，一种是我们上一讲学习的基于哈希表的思想，直接将符号表映射到一个连续线性的数组空间，从而获得O(1)的访问时间复杂度；**另外一种思路就需要维护一个有序排列的符号表，JDK中的TreeMap就是基于这种思路**。

试想，如果能够让符号表是有序排列的，我们查找的时候是不是就不用遍历每一个元素，而可以采用二分查找之类的手段了呢？当然也要尽量降低维护这个有序排列的数据结构所花费的代价。

那一种常见的用于实现有序集的数据结构就是红黑树，这也是JDK中TreeMap中Tree的意思。如果你有一定的Java开发经验，相信你一定会知道相比于HashMap，**基于红黑树的TreeMap的一个显著特点就是其维护的键值对是有序排列的**。

如果你一听到红黑树这个词，就有点慌张，觉得这不是自己能驾驭的，今天这节课就来帮你打消这个顾虑。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（7） 💬（2）<div>红黑树每次看的时候都好像明白了，过一段时间就会忘记旋转细节。但是，红黑树确实是工程实现的典范，为了让完全二叉树容纳各种数量的节点，引入了2，3树的概念，也就是保持树的形状为完全二叉树，让树的节点容纳一个或者两个元素来承载变化。有了这个灵活性，平衡二叉树的实现就方便很多，而且也高效不少（半数插入不用调整树的结构）。增加节点的颜色来代替异构节点简化了实现。引入了根节点为黑色和红色节点只出现在左侧的约束，在没有降低红黑树表达功能和性能的前提下，进一步简化实现。
</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/74/cd80b9f4.jpg" width="30px"><span>友</span> 👍（5） 💬（1）<div>红黑看过几个版本 一个是算法4 一个是邓公的 关于旋转操作我看过邓公的那个 connect34方法  我惊了我根本没想到可以这样通过打散然后组合的方式</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（4） 💬（1）<div>左偏红黑树和算法4作者的亲自讲解

https:&#47;&#47;www.coursera.org&#47;lecture&#47;algorithms-part1&#47;red-black-bsts-GZe13</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（2） 💬（3）<div>avl 实现更简单，比红黑树性能并没有差多少，为什么应用场景没有红黑树那么广呢</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/38/f1/996a070d.jpg" width="30px"><span>LW</span> 👍（1） 💬（1）<div>第一次看懂了红黑树实现</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/62/28/0356880b.jpg" width="30px"><span>.</span> 👍（0） 💬（1）<div>这个比另一个专栏红黑树讲得好。。。。那个专栏红黑树我直接放弃了</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/34/5c/c60b30c0.jpg" width="30px"><span>这是白猫</span> 👍（0） 💬（1）<div>HashMap 和 TreeMap 都是使用红黑树实现的，区别是HashMap多了外面的基于hashCode的有序链表，因此在重复数据较多时使用Treemap，反之大量不重复数据时使用 HashMap，是不是这样呢老师</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（0）<div>1、应该再说明下 为什么同样是平衡二叉树的AVL树没有被选中
2、红黑树严格意义上应该是等价2-3-4树而不是2-3树</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/8a/4bef6202.jpg" width="30px"><span>大叮当</span> 👍（0） 💬（1）<div>老师好，请教个问题，完全二叉树为啥要规定可以有左叶子节点没有右叶子节点，这个规定的原因是什么呢？</div>2022-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（3）<div>这一点不是很明白：
2-3 树上，每个节点到叶子节点的数量一定是一样的</div>2022-07-02</li><br/>
</ul>