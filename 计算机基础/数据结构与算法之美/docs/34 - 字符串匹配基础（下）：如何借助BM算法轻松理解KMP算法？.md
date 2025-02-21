上一节我们讲了BM算法，尽管它很复杂，也不好理解，但却是工程中非常常用的一种高效字符串匹配算法。有统计说，它是最高效、最常用的字符串匹配算法。不过，在所有的字符串匹配算法里，要说最知名的一种的话，那就非KMP算法莫属。很多时候，提到字符串匹配，我们首先想到的就是KMP算法。

尽管在实际的开发中，我们几乎不大可能自己亲手实现一个KMP算法。但是，学习这个算法的思想，作为让你开拓眼界、锻炼下逻辑思维，也是极好的，所以我觉得有必要拿出来给你讲一讲。不过，KMP算法是出了名的不好懂。我会尽力把它讲清楚，但是你自己也要多动动脑子。

实际上，KMP算法跟BM算法的本质是一样的。上一节，我们讲了好后缀和坏字符规则，今天，我们就看下，如何借助上一节BM算法的讲解思路，让你能更好地理解KMP算法？

## KMP算法基本原理

KMP算法是根据三位作者（D.E.Knuth，J.H.Morris和V.R.Pratt）的名字来命名的，算法的全称是Knuth Morris Pratt算法，简称为KMP算法。

KMP算法的核心思想，跟上一节讲的BM算法非常相近。我们假设主串是a，模式串是b。在模式串与主串匹配的过程中，当遇到不可匹配的字符的时候，我们希望找到一些规律，可以将模式串往后多滑动几位，跳过那些肯定不会匹配的情况。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/da/7f/8069035d.jpg" width="30px"><span>ZX</span> 👍（272） 💬（17）<div>最难理解的地方是
k = next[k]
因为前一个的最长串的下一个字符不与最后一个相等，需要找前一个的次长串，问题就变成了求0到next(k)的最长串，如果下个字符与最后一个不等，继续求次长串，也就是下一个next(k)，直到找到，或者完全没有
</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/50/c23cf47d.jpg" width="30px"><span>李</span> 👍（40） 💬（5）<div>百度了下，终于搞明白了，回答自己前面一个问题。
关键是要搞明白k值是啥东西。
比如求aba  每个前缀最长可匹配前缀子串的结尾字符下标
这句话很容易引起歧义。
aba的前缀有a,ab,   后缀有ba,a    只有a与a匹配。 所以匹配的结尾下标是0.
abab     显然ab和ab可以匹配，所以匹配的结尾下标是1
abaaba   下标是2
ababa    下标是2
aaaa  下标是2




</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（29） 💬（1）<div>一个双休，加上好几个早上的时间，这两篇关于字符串匹配，弄明白了，代码我自己也实现了一遍，就论代码实现来说，KMP算法比BM算法要简单一点，这个BM算法，一个双休送给了他，慢慢的一点点理解规则，然后再一点点的，按照自己所理解的思想来实现，虽然觉得这样子慢，但能学到的会更多，要论最难理解的地方，这个ＢＭ的算法的计算next数组，这脑子绕了好久！</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/34/5dee4f70.jpg" width="30px"><span>P@tricK</span> 👍（11） 💬（2）<div>最难理解的就是kmp的next数组的这个求法了，思路本身就难，几个边界情况靠自己理清写出来没BUG更是难。
自己想到的一个简单点的解法，就是先将所有模式串的前缀子串全列出来，然后用哈希表存储，key是串，value是串长度，求解next数组值的时候将后缀子串从长到短去哈希表里找。</div>2018-12-10</li><br/><li><img src="" width="30px"><span>suke</span> 👍（9） 💬（2）<div>这些对什么最长前缀后缀字符串变量的描述能不能不要加那么多形容词？用一个字符变量不就描述了么，整那么多形容词不把人搞晕才怪，自己百度一下，全明白了，相比之下，你这个描述真的是徒然增加读者的阅读障碍</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/ea/6ad346c1.jpg" width="30px"><span>煦暖</span> 👍（6） 💬（1）<div>老师你好，第二幅图的上半部分的模式串前缀子串画错了，应该从a开始，abab，而不是baba。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/34/5dee4f70.jpg" width="30px"><span>P@tricK</span> 👍（5） 💬（1）<div>如果 next[i-1]=k-1，也就是说，子串 b[0, k-1] 是 b[0, i-1] 的最长可匹配前缀子串。如果子串 b[0, k-1] 的下一个字符 b[k]，与 b[0, i-1] 的下一个字符 b[i] 匹配，那子串 b[0, k] 就是 b[0, i] 的最长可匹配前缀子串。所以，next[i-1] 等于 k。

---------------

末尾应该是 next[i] 等于 k</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/d2/3d88cb8e.jpg" width="30px"><span>NeverMore</span> 👍（4） 💬（1）<div>学习啦，next数组一开始没明白，看了几次终于看懂啦。
思考了下字符串匹配，最重点的就是多移动几位，但是又不要移动过多，同时记录历史数据，以空间换时间！</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/9d/b1305f4d.jpg" width="30px"><span>文祥</span> 👍（2） 💬（1）<div>第一个程序里面的 while (j &gt; 0 &amp;&amp; a[i] != b[j]) 可以改成if吧
</div>2019-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/3b/e56ff0a9.jpg" width="30px"><span>Pan^yu</span> 👍（1） 💬（1）<div>看了三遍总算看懂了，靠@ZX的留言，然后回去在梳理才看懂</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/7e/0cc5a187.jpg" width="30px"><span>narcos</span> 👍（1） 💬（1）<div>&quot;我们只需要拿好前缀本身，在它的后缀子串中，查找最长的那个可以跟好前缀的前缀子串匹配的。假设最长的可匹配的那部分前缀子串是{v}，长度是 k。我们把模式串一次性往后滑动 j-k 位，相当于，每次遇到坏字符的时候，我们就把 j 更新为 k，i 不变，然后继续比较。&quot;
老师，这里的 j 和 i 分别是什么，没有交代</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/be/9a083ea1.jpg" width="30px"><span>景页</span> 👍（1） 💬（1）<div>getNexts函数的while循环两行代码很妙，还没理解，虽然文字部分看懂了。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/10/b6bf3c3c.jpg" width="30px"><span>纯洁的憎恶</span> 👍（1） 💬（1）<div>上一节课计算suffix数组与prefix数组也可以使用动态规划么？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/d0/7e18e9a2.jpg" width="30px"><span>Tenderness</span> 👍（1） 💬（1）<div>分开看是差不多看懂了，看了这篇后，貌似前面的代码实现也ok了。估计明天又不会写了，😂</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/00/ea/6ad346c1.jpg" width="30px"><span>煦暖</span> 👍（1） 💬（1）<div>老师你好，文中“假设最长的可匹配的那部分前缀子串是{v}，长度是 k。我们把模式串一次性往后滑动 j-k位...”这个地方结合下面图看，应该是往后移动j-k+1位吧？？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6a/fe/7566542f.jpg" width="30px"><span>布衣</span> 👍（0） 💬（1）<div>有点太惜笔墨了, 最难的地方讲的不透彻, 需要看半天才搞明白,多画几张图不好吗?</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/96/9571fa3d.jpg" width="30px"><span>青青子衿</span> 👍（0） 💬（1）<div>作者写的确实有点绕，结合这篇确实更好理解，https:&#47;&#47;www.zhihu.com&#47;question&#47;21923021?utm_source=wechat_search&amp;utm_medium=organic</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/4b/99d67d3d.jpg" width="30px"><span>oh..</span> 👍（0） 💬（1）<div>老师，我想问下像svn、git这些版本管理工具的代码校验比对是怎么实现的？想了解具体操作是怎样实现的</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/a2/c7a3758d.jpg" width="30px"><span>漏网之渔</span> 👍（0） 💬（1）<div>个人认为这一章节图和文字描述KMP过于抽象了，沿用BM算法来讲述KMP过于繁琐，推荐阅读：http:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2013&#47;05&#47;Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/c9/75c9002e.jpg" width="30px"><span>Shawn</span> 👍（0） 💬（1）<div>理解了原理和写出完美的代码还差了一个宇宙，哈哈。</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/73/b5158f6c.jpg" width="30px"><span>笙南</span> 👍（0） 💬（1）<div>王争老师你好，您上边的例子中 e 是坏字符，按照 KMP 的匹配规则，模式串需要移动 3 次，走到最后；但是如果是 BM 的坏字符规则，发现 e 是坏字符，并且不再模式串中出现，模式串应该直接移动 5 + 1 位，越过坏字符，移动 1 次，走到最后；这样 BM 的模式串移动次数比 KMP 的少。请问老师，我上面的理解对吗 ？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/99/454b17c1.jpg" width="30px"><span>他在她城断了弦</span> 👍（104） 💬（7）<div>关于求next数组这部分写的太不好懂了，建议作者别用太多长句，切换成短句，方便大家理解。。</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/d9/db957e30.jpg" width="30px"><span>algo</span> 👍（78） 💬（8）<div>推荐读者先去看下这篇文章，然后再来看看，理解next会比较有帮助。
https:&#47;&#47;www.zhihu.com&#47;question&#47;21923021，逍遥行 的回答</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/50/c23cf47d.jpg" width="30px"><span>李</span> 👍（77） 💬（4）<div>终于看明白了，感觉设置了很多干扰项。其实用迭代思想解释就能理解了。
这个算法本质是找相等的最长匹配前缀和最长匹配后缀。
有两种情况，
（1）如果b[i-1]的最长前缀下一个字符与b[i]相等，则next[i]=next[i-1]+1.
（2）如果不相等，则我们假设找到b[i-1]的最长前缀里有b[0,y]与后缀的子串b[z,i-1]相等，然后只要b[y+1]与b[i]相等，那么b[0,y+1]就是最长匹配前缀。这个y可以不断的通过迭代缩小就可以找到
</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/54/deb19880.jpg" width="30px"><span>slvher</span> 👍（56） 💬（6）<div>「我们假设 b[0, i] 的最长可匹配后缀子串是 b[r, i]。如果我们把最后一个字符去掉，那 b[r, i-1] 肯定是 b[0, i-1] 的可匹配后缀子串，但不一定是最长可匹配后缀子串。」

========= 手动分割线 ========

对文中这句话，我的理解如下：

因为 b[i] 的约束可能导致 r 靠近 i，故去掉 b[i] 字符后，b[r, i-1] 虽然肯定是 b[0, i-1] 的可匹配后缀子串，但不一定是其中最长的。

例如：设模式串好前缀为 &quot;abxabcabxabx&quot;，其最长可匹配后缀子串为 &quot;abx&quot;，去掉最后的字符 &#39;x&#39; 后，虽然 &quot;ab&quot; 还是好前缀的可匹配后缀子串，但 &quot;abxab&quot; 才是最长可匹配后缀子串。

这句话虽然本身逻辑上是正确的，与上下文逻辑衔接性不强，感觉去掉这句更有利于对 next 数组第二种情况的理解。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0e/69/0d17f102.jpg" width="30px"><span>niulixin</span> 👍（35） 💬（2）<div>我觉得bm算法倒是好理解但是kmp的算法的next数组我感觉不太好理解啊</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/c3/e4ba51d5.jpg" width="30px"><span>Flash</span> 👍（23） 💬（1）<div>
最难理解的是KMP算法了。
总体上，KMP算法是借鉴了BM算法本质思想的，都是遇到坏字符的时候，把模式串往后多滑动几位。
1.但是这里要注意一个细节，不然容易被前面学的BM算法给误导，导致难以理解。
BM算法是对模式串从后往前比较，每次是将主串的下标 ”i“ 往后移动多位。(这符合我们正常的思维，所以好理解)
KMP虽然也是往后移动多位，但是比较时，是对模式串从前往后比较；
对于主串已经比较过的部分，保持主串的 ”i“ 指针(即下标)不回溯。
而是通过修改模式串的”j“指针，变相地让模式串移动到有效的位置。(这里修改&quot;j&quot;，是让&quot;j&quot;变小了，我们说的还是将模式串往后移动，所以不太好理解)

2.KMP算法中不好难理解的，构建next数组，其实很简单，要多下自己的脑筋，不要被带偏了，就好理解了。就是求next[i](动态规划的思想，根据前面已经计算好的结果next[0]...next[i-1]来得到next[i])，前一个的最长串的下一个字符与最后一个相等，那next[i]就=next[i-1]+1；否则就需要找前一个的次长串，递归这个过程，直到找到或没有。</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（19） 💬（1）<div>「那 b[r, i-1] 肯定是 b[0, i-1] 的可匹配后缀子串，但并不一定是最长可匹配后缀子串。」后半句不是很理解，如果模式串是 b[0, i-1]，i-1 已经是最后一个字符了，那么为什么 b[r, i-1] 不一定是 b[0, i-1] 的最长可匹配后缀子串呢？
</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/9d/a3706e4f.jpg" width="30px"><span>饺子</span> 👍（17） 💬（6）<div>😂😂😂讲移动那幅图是不是写错了 j=j-k
不应该是j=k嘛</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/46/2850b4a9.jpg" width="30px"><span>luo</span> 👍（12） 💬（0）<div>3遍才理解了差不多，还有一句话之前留言的还是木有理解，BM是去滑动主串，KMP是利用模式串的好前缀规则去跳过模式串（相当于滑动模式串）主串递增的形式。最难理解的就是next数组中的求解，如果b[0,i-1]的最长前缀是k-1 那b[0,k-1]就是最长的前缀 这里开始分两种情况，
第一种情况：b[0,k-1]的下一个字符b[k]=b[i],则最长前缀子串就变成b[0,k]，最长后缀就变成b[i-k,i]。next[i]=next[i-1]+1
第二种情况：b[0,k-1]的下一个字符b[k]≠b[i]，这时候我们要去寻找的就是b[0,i-1]中的最长前缀子串（最长匹配前后缀子串b[0,y] 和b[i-y-1,i-1]这两本身就是一一匹配的，而next数组记录的只有前缀我们仍然利用现有条件做推断）的最长可匹配前缀子串（必然跟后缀子串一致），就是b[0,i-1]的次长可匹配子串（划重点）（因为b[0,i-1]的最长可匹配子串c因为c这个串接下来一个字符跟b[i]不等，求取c它的最长可匹配子串一直到下个字符b[x+1]与b[i]相等递归求取）。
可能我说的跟理解的有点问题，举个例子： abeabfabeabe(主串) abeabfabeabc（模型串） 到e处不能匹配，最长可匹配子串就是 abeab接下来发现f与e不一致然后再求取abeab的最长可匹配子串 ， 为ab接下去的e刚好跟e匹配。</div>2019-01-10</li><br/>
</ul>