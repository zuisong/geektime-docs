MapReduce是Google大数据处理的三驾马车之一，另外两个是GFS和Bigtable。它在倒排索引、PageRank计算、网页分析等搜索引擎相关的技术中都有大量的应用。

尽管开发一个MapReduce看起来很高深，感觉跟我们遥不可及。实际上，万变不离其宗，它的本质就是我们今天要学的这种算法思想，分治算法。

## 如何理解分治算法？

为什么说MapRedue的本质就是分治算法呢？我们先来看，什么是分治算法？

分治算法（divide and conquer）的核心思想其实就是四个字，分而治之 ，也就是将原问题划分成n个规模较小，并且结构与原问题相似的子问题，递归地解决这些子问题，然后再合并其结果，就得到原问题的解。

这个定义看起来有点类似递归的定义。关于分治和递归的区别，我们在排序（下）的时候讲过，**分治算法是一种处理问题的思想，递归是一种编程技巧**。实际上，分治算法一般都比较适合用递归来实现。分治算法的递归实现中，每一层递归都会涉及这样三个操作：

- 分解：将原问题分解成一系列子问题；
- 解决：递归地求解各个子问题，若子问题足够小，则直接求解；
- 合并：将子问题的结果合并成原问题。

分治算法能解决的问题，一般需要满足下面这几个条件：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/87/57/e28ba87b.jpg" width="30px"><span>Williamzhang</span> 👍（46） 💬（1）<div>第一个留言有问题可以再理解一下，不要误导后边人，作者的num+=语句位置正确</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（149） 💬（1）<div>在统计方面比较多，比如统计我国人口，要知道我国人口就要先知道每个省人口，要知道省人口就要知道每个市人口，要知道市人口就要知道每个区县人口，直到村社区，然后汇总求的总人数。</div>2018-12-19</li><br/><li><img src="" width="30px"><span>Yves</span> 👍（39） 💬（1）<div>代码略有问题：1，num += (q - i + 1)，应该是在 a[i] &lt;= a[j] 这个条件分支里面；2，while (i &lt;= q) 里面不应该有 num += (q - i + 1)，3，最后的修改原数组迭代条件应该是  i &lt; r - p + 1 而不是  i &lt; r - p 。

private void merge(int[] a, int p, int q, int r) {
        int i = p, j = q + 1, k = 0;
        int[] tmp = new int[r - p + 1];
        while (i &lt;= q &amp;&amp; j &lt;= r) {
            if (a[i] &lt;= a[j]) {
                tmp[k++] = a[i++];
            } else {
                num += (q - i + 1);
                tmp[k++] = a[j++];
            }
        }
        while (i &lt;= q) {
            tmp[k++] = a[i++];
        }
        while (j &lt;= r) {
            tmp[k++] = a[j++];
        }
        for (i = 0; i &lt; r - p + 1; ++i) {
            a[p + i] = tmp[i];
        }
    }</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/7b/7c043069.jpg" width="30px"><span>h…</span> 👍（36） 💬（12）<div>王争老师，我是后台开发，想换算法类工作，能不能给我点建议</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/44/1588e8b6.jpg" width="30px"><span>刘文坛</span> 👍（25） 💬（6）<div>分治算法本质上就是利用多核cpu并行计算能力，如果只是单核cpu，分治算法是不是就不可行了？</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（7） 💬（2）<div>老师，请问我做java但是不从事算法岗位，这门课需要学习到什么程度呢？总觉得心里有目标会更好点。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/7a/31328704.jpg" width="30px"><span>wo</span> 👍（3） 💬（1）<div>if (a[i] &lt;= a[j]) {
      num += (j - q - 1);
      tmp[k++] = a[i++];
    } else {
      tmp[k++] = a[j++];
    }
我想了想，这段代码应该求的是有序对而不是逆序对吧</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/0a/fa152399.jpg" width="30px"><span>wahaha</span> 👍（1） 💬（1）<div>老师，求有(逆)序对只需一遍扫描即可，O(n)就能解决，所以用归并排序求解的这个例子并不太合适。</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/b9/00b35168.jpg" width="30px"><span>行者</span> 👍（0） 💬（1）<div>老师，我前两个留言想说的是您文中说到的两个经典的分治算法的例子，不是思考题。一方面想问一下在您的github上有没有代码实现（这个您在回复我上一条留言中已经给了github地址了），另一方面是想问一下3×3阶矩阵相乘的话，可不可以用分治的思想去做呢？您的例子是n×n，n不必是2的倍数吗？如果可以的话，您能不能详细讲一讲3×3阶矩阵相乘怎么做。
我同学面试的时候面试官问到了这个问题，但他当时除了3个for循环，也没想出什么比较好的方法。我们讨论的时候，也没想出来</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/b9/00b35168.jpg" width="30px"><span>行者</span> 👍（0） 💬（1）<div>3x3阶矩阵怎么用分治做呢？nxn阶，是要求n必须为2的整数倍吗
</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/b9/00b35168.jpg" width="30px"><span>行者</span> 👍（0） 💬（1）<div>老师，这节课的思考题很有价值，但是想了半天没有好的思路啊，你的GitHub上有代码实现吗？有时间的话，还请老师亲自做一下这两个题目</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIahDan9ibN8uCqDo8WY1Nb9vJd9yrUtmC9XHibSO1PichUaPWR8sIjfdNvSpOqN28Cw1ibYztoZF10ibg/132" width="30px"><span>龙须子</span> 👍（0） 💬（1）<div>很好奇，10G的文件，内存只有2G或者3G，怎样做到提前扫描一遍订单金额区间？</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（0） 💬（1）<div>王老师，我觉得利用merge sort找逆序对个数的代码，最后3行，就是讲tmp[]拷贝回a[]这个操作，应该是不需要的。在排序过程中，tmp[]是有序的，a[]是不变的。那么partition之后，应该使用原始的数组一份而二的2个子数组来分别找各自的逆序对。应该用原始的数据。tmp[]拷贝之后，对有序的做判断，值为0。实际上，我觉得根本就不需要tmp[]这个辅助数组。
不知道我的理解是否正确，还请王老师看一下。谢谢！</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/38/c7819759.jpg" width="30px"><span>哈哈</span> 👍（0） 💬（2）<div>快排算不算分治呢? 好像只有分, 没有合</div>2019-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/49/898cb635.jpg" width="30px"><span>LEO</span> 👍（0） 💬（1）<div>老师，10g订单那个例子我有一个疑问，就是文中提到先扫描10g订单并按区间将订单分在不同的小文件中，我想请问这个过程怎么在内存只有2-3g的机器上进行的呢？还是说您指得不是在单机上，而是在集群上进行的？麻烦老师解答一下</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/df/6e6a4c6b.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>为什么需要创建tmp数组来存储原数据，并在后面复制回去； 其实原数组数据并没有被修改过</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/44/1588e8b6.jpg" width="30px"><span>刘文坛</span> 👍（0） 💬（1）<div>对10G大文件拆分成若干小文件分别排序，在合并有序文件时，如何对两个5G有序文件进行内存排序？内存放不下啊</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/46/2850b4a9.jpg" width="30px"><span>luo</span> 👍（0） 💬（1）<div>老师 你说的转算法，岁数不大愿意学习的岁数不大应该是小于多少岁为好</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/15/5dabb390.jpg" width="30px"><span>Geek_fbe6fe</span> 👍（0） 💬（1）<div>老师，使用归并排序算有序度，分成两个小数组必须是有序的，是吗？好疑惑这样子应用场景不是很小？</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（0） 💬（1）<div>老师 一开始逆序度不是4吗，最后怎么成了6了</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/09/13f8a4ab.jpg" width="30px"><span>杨槐</span> 👍（0） 💬（1）<div>老师，普通本科生学这个算法，数据结构可以拓展自己的思维，有较大的机会以后能转算法或者大数据呢？看完你的专栏，刷刷leetcode，还需要哪些书看呢</div>2018-12-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIcMfFBhXflsHhW5HV9EGFLJe21f5MP5qGzdHAgSficFP04WrnGwcmg1Ix4j74VImJphH17kehuibjg/132" width="30px"><span>李盏</span> 👍（0） 💬（1）<div>老师，是不是每课都有代码放git上了，地址是啥</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（0） 💬（1）<div>老师这个分治算法我理解了，但在加入统计逆序对个数的代码的后，我有一点没有理解，就是逆序对的个数的加法，为什么是当前中间值下标减开始下标加1，这是为什么？我本来的想法是当左边大于右边就加1，但这样是不对的，所以请老师帮我解释下，谢谢！</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/4d/9ce28826.jpg" width="30px"><span>luxinfeng</span> 👍（0） 💬（1）<div>老师，分治算法求逆序度比时间复杂度是O（n^2）的算法高效在什么地方啊？为什么我推算的分治算法的时间复杂度并不比O（n^2）高效呢？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e8/f4/6cca0aac.jpg" width="30px"><span>浩</span> 👍（0） 💬（1）<div>为什么那个逆序对的个数要减1呀？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/e2/e5110db5.jpg" width="30px"><span>MIAN-勉</span> 👍（86） 💬（3）<div>把归并排序merge方法的参数列表 由merge(int[] a, int p, int q, int r) 改为 merge(int[] a, int low, int middle, int high) 更容易理解😂，小细节，哈哈</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（60） 💬（2）<div>「创新并非离我们很远，创新的源泉来自对事物本质的认识。无数优秀架构设计的思想来源都是基础的数据结构和算法，这本身就是算法的一个魅力所在。」 

这句话讲的太好啦。各种前端框架层出不穷，本质的东西，也是基本都没有变。

与其最新，不如求本。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（51） 💬（2）<div>采用分治思想的算法包括：
1.快速排序算法
2.合并排序算法
3.桶排序算法
4.基数排序算法
5.二分查找算法
6.利用递归树求解算法复杂度的思想
7.分布式数据库利用分片技术做数据处理
8.MapReduce模型处理思想</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/bb/c488d5db.jpg" width="30px"><span>刘远通</span> 👍（44） 💬（3）<div>第一个求最近的点对
分成两块 单独求其中一块点对最小距离 
然后求这两块之间点对的最小距离 通过一些排序和删除 可以减少到6个点之间比较 很神奇

第二个矩阵计算
v.斯特拉森提出了2*2分块矩阵的计算公式 从原来的8次乘法 缩减到了7次
当n规模很大的时候 缩减效果就很明显 （7&#47;8）^(logn)</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/d4/b71779ff.jpg" width="30px"><span>Jiemr</span> 👍（27） 💬（7）<div>老师，我有两个疑问：
给 10GB 的订单排序，我们就可以先扫描一遍订单
-------------------------------------
1.场景中描述的机器内存只有2、3GB，我理解的是直接加载文件内存应该不够用来扫描一次10GB订单文件，对吗？如果不能，那应该怎么扫描呢？
2.如果用buffer来缓存扫描结果的话，即使能扫描完成，又该怎么对文件根据金额区间进行分割呢？</div>2019-01-11</li><br/>
</ul>