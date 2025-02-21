搜索引擎的搜索关键词提示功能，我想你应该不陌生吧？为了方便快速输入，当你在搜索引擎的搜索框中，输入要搜索的文字的某一部分的时候，搜索引擎就会自动弹出下拉框，里面是各种关键词提示。你可以直接从下拉框中选择你要搜索的东西，而不用把所有内容都输入进去，一定程度上节省了我们的搜索时间。

![](https://static001.geekbang.org/resource/image/ce/9e/ceb8738453401d5fc067acd513b57a9e.png?wh=1228%2A962)

尽管这个功能我们几乎天天在用，作为一名工程师，你是否思考过，它是怎么实现的呢？它底层使用的是哪种数据结构和算法呢？

像Google、百度这样的搜索引擎，它们的关键词提示功能非常全面和精准，肯定做了很多优化，但万变不离其宗，底层最基本的原理就是今天要讲的这种数据结构：Trie树。

## 什么是“Trie树”？

Trie树，也叫“字典树”。顾名思义，它是一个树形结构。它是一种专门处理字符串匹配的数据结构，用来解决在一组字符串集合中快速查找某个字符串的问题。

当然，这样一个问题可以有多种解决方法，比如散列表、红黑树，或者我们前面几节讲到的一些字符串匹配算法，但是，Trie树在这个问题的解决上，有它特有的优点。不仅如此，Trie树能解决的问题也不限于此，我们一会儿慢慢分析。

现在，我们先来看下，Trie树到底长什么样子。

我举个简单的例子来说明一下。我们有6个字符串，它们分别是：how，hi，her，hello，so，see。我们希望在里面多次查找某个字符串是否存在。如果每次查找，都是拿要查找的字符串跟这6个字符串依次进行字符串匹配，那效率就比较低，有没有更高效的方法呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（246） 💬（14）<div>找到了一个Trie树的开源库：Apache Commons，里面有关于Trie的实现</div>2018-12-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/tRDAHK9WKQXOIJUP0WBJeR4mmjkXtMgtsTPcprqGzc1SqNWAnkREicvOWvM24YF9D7Ric7C4BEGoloPdOibaaq0hQ/132" width="30px"><span>kepmov</span> 👍（29） 💬（1）<div>trie树实际项目中由于内存问题用的不是很多，老师可以讲解下DAT（双数组trie树）的具体实现吗</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/96/3162d51f.jpg" width="30px"><span>雨天</span> 👍（19） 💬（2）<div>if (p.isEndingChar == false) return false; &#47;&#47; 不能完全匹配，只是前缀
else return true; &#47;&#47; 找到 pattern 
这小段代码有点不大牛.^_^
return p.isEndingChar;就好了</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/7f/8069035d.jpg" width="30px"><span>ZX</span> 👍（17） 💬（4）<div>老师，字符串匹配这里，还差后缀树没讲，很多场合需要用到这种结构，希望老师可以讲一讲</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/89/1b/7974e215.jpg" width="30px"><span>忽忽</span> 👍（15） 💬（1）<div>请问下老师，这些图是什么工具画的呀？</div>2018-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（11） 💬（1）<div>老师 红黑树  如何实现字符串查找  方便王老师稍微点拨下吗</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/52/f07e9001.jpg" width="30px"><span>想当上帝的司机</span> 👍（10） 💬（1）<div>26个字符的话TrieNode不要data也可以吧 数组下标就是data</div>2018-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/87/0491e9e5.jpg" width="30px"><span>Lisa Li</span> 👍（6） 💬（2）<div>“而 Trie 树中用到了指针，所以，对缓存并不友好，性能上会打个折扣。” 可以解释一下为什么吗？</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/aa/db213a66.jpg" width="30px"><span>莫弹弹</span> 👍（6） 💬（1）<div>想起来上一次需求是做敏感词检测，需要匹配到指定动词和指定名词才会触发屏蔽，经过实验，暴力for循环是最快的(&quot;▔㉨▔) trie太复杂了写完怕别人看不懂</div>2018-12-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjUDIRQ0gRiciax3Wo78c5rVjuWDiaw4ibcCiby8xiaMXJh5ibjU5242vfCGOK4ehibe1IKyxex2A4IX4XSA/132" width="30px"><span>追风者</span> 👍（4） 💬（3）<div>王老师，关于Trie树有两点疑问。
1.文中用‘he’和‘her’构建Trie树，当我要查询‘he’的时候怎么办？
2.像jieba分词这种切词工具，为什么要用Trie树呢？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f4/26b95f0b.jpg" width="30px"><span>TryTs</span> 👍（4） 💬（1）<div>老师，麻烦请问一下您请问一下对于一些新的领域，没有现成的书，教程你会通过什么方法跟途径或者说平台去体系的学习？还有我就是想请教一下老师您对AR的看法？</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/4a/2f81b0f5.jpg" width="30px"><span>freeland</span> 👍（4） 💬（1）<div>以太坊上header里的transaction .root ,state root,receipt root用的是Merkle-PatriciaTrie(MPT)，和今天的这个是一个么</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/a2/9450ef89.jpg" width="30px"><span>刘涛涛</span> 👍（2） 💬（1）<div>请问老师，如何删除trie中的字符串呢</div>2019-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK7lrNkubM9GZyvcaaJ4PxeRw6LGnsHxJ9hvNEK6KToxF5VFOFia1bUZQpia9fMgERUyRc85Jk4vV8A/132" width="30px"><span>lm</span> 👍（2） 💬（1）<div>这种树结构是不是匹配到前缀后还得继续遍历前缀的子节点？这样提示字符串才能显示全</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/6e/60680aa4.jpg" width="30px"><span>Li Yao</span> 👍（2） 💬（1）<div>p = p.children[index];
p.isEndingChar = true;
是不是应该放到for循环外面？ 否则每个节点都会被标记为endingChar?</div>2018-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLlztvlBgajZMEph8AvkP2pfoqNCGtYSalIKgrCbCg0MWDZJgJwqVRfWA6cgIoZicL6dKibfK0zjsWg/132" width="30px"><span>Geek_18b741</span> 👍（1） 💬（1）<div>老师好，关于本课程我写了一些博客笔记在CSDN，https:&#47;&#47;blog.csdn.net&#47;flying_all&#47;article&#47;details&#47;97097870。博客中有这里的图，也有文字。我在文章开始有申明。这侵权吗？如果侵权，我就把文章改为私有的，仅供自己复习使用。</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4d/a2/9450ef89.jpg" width="30px"><span>刘涛涛</span> 👍（1） 💬（1）<div>hey和he都放到trie树里面如何放置呢，如果先放he，那么e被标记为ending，再放入hey的时候，会发生什么呢，e的endiing是否有效？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/7e/0cc5a187.jpg" width="30px"><span>narcos</span> 👍（1） 💬（2）<div>老师，下一节是 AC 自动机吗？什么时候发？</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/a2/c30ac459.jpg" width="30px"><span>hughieyu</span> 👍（1） 💬（1）<div>if (i == text.length-1) {
          newNode.isEndingChar = true;
     }

这一段代码是不是应该拿到上一层判断是否存在的if外面去 比如先走hello 再有he e就不是endchar了</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（1）<div>这篇的留言只有66个，我就来一条吧！</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6f/96/4d340fc4.jpg" width="30px"><span>淘林</span> 👍（0） 💬（1）<div>老师，问一下，如果hi和hill都存在，那么第二个字符应该怎么存储啊</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/30/4ae82e16.jpg" width="30px"><span>wordMan</span> 👍（0） 💬（1）<div>“public class TrieNode { p..public TrieNode[] children = new TrieNode[26]... ”
是不是在真的有子节点插入的时候再分配长度26的数组给到children更好呢？
</div>2019-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/dc/32e78f02.jpg" width="30px"><span>乐凡</span> 👍（0） 💬（1）<div>老师，上面说的用有序数组代替存储子节点我有点不理解，因为就算是有序数组，在初始化的时候也不确定一个节点的子节点到底有多少啊，若初始化小了，后续添加的子节点数超过了有序数组的长度，需要进行扩容，得再生成一个数组，还要数据迁移。希望老师看到帮忙回答下</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（65） 💬（4）<div>思考题：

依次读取每个字符串的字符构建 Trie 树，用散列表来存储每一个节点。每一层树的所有散列表的元素用一个链表串联起来，
求某一长度的前缀重合，在对应树层级上遍历该层链表，求链表长度，除以字符集大小，值越小前缀重合率越高。

遍历所有树层级的链表，存入散列表，最后散列表包含元素的个数，就代表字符集的大小。</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（46） 💬（7）<div>如何统计字符串的字符集大小，以及前缀重合的程度呢？

统计字符集的大小，这个问题，其实就是在求字符的最小值以及最大值的问题。
我的解决办法
1，遍历字符串集合
2，将每个字符转化为int数字
3，设置最小以及最大的变量，当字符中比最大字符的变量大的时候，将最大字符变量改为当前字符，或者比最小字符小，就修改最小字符
4，遍历完成后，所求得的最大值与最小值的差，就是字符集的大小

前缀重合的程度，这个问题的求解，其实就是做字符的统计问题
我的解决办法：
使用哈希表来记录下统计数，key为字符，value为统计计数
遍历每条记录，假如每条记录中仅包含一个单词（如果多单词，多一步分隔操作，分隔成一个一个的单词）
统计计数算法，就是从前到后遍历，遇到存在的，加1，不存在，则存入hash表
比如hello这个单词，在哈希表中存储就为
h      1
he     1
hel    1
hell   1
hello  1
当再将出现，比如he
就会变成
h      2
he     2
hel    1
hell   1
hello  1

统计数据完成后，对这个结果计算重合的字符数与整个字符的占比，
具体计算公式为: count(value &gt; 1) &#47; count(all) 
但我的算法复杂度有点高，是m*n,m表示整个字符的长度，n表示单个单表的长度。

</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/dc/9408c8c2.jpg" width="30px"><span>ban</span> 👍（36） 💬（1）<div>上面代码里： p.isEndingChar = true; 应该是放在for循环的外面吧？
不然如果hello，那不就变成 h e l l o 都是叶子节点？</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（36） 💬（2）<div>今天的课程比上两节的课程理解起来容易多了 总体觉得就像是构造出来的多叉树，相同的前缀字符串就是同一棵树下来的不同分之</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/31/96b76ca8.jpg" width="30px"><span>起点·终站</span> 👍（33） 💬（5）<div>看完后发现我们项目的屏蔽字检测就是用trie树写的。。666</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/4f/4d5efcf9.jpg" width="30px"><span>k</span> 👍（16） 💬（3）<div>用户单词拼写错误的情况下，可以用贝叶斯去纠错，详见Peter Norvig大牛的几十行py教做人 https:&#47;&#47;norvig.com&#47;spell-correct.html</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d9/e9/eaa1222d.jpg" width="30px"><span>qazwsx</span> 👍（15） 💬（0）<div>力扣 第820题 </div>2019-10-21</li><br/>
</ul>