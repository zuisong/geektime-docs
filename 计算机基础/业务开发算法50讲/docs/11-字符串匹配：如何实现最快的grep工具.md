你好，我是微扰君。

grep命令，相信使用过Linux的同学都会非常熟悉，我们常常用它在Linux上进行文本搜索操作，具体来说就是从一段文本中查找某个字符串存在的行。下面一个典型的grep的使用例子，比如我可以用它来看看自己在LeetCode上用Java做了多少题：

![图片](https://static001.geekbang.org/resource/image/9b/aa/9b96f1b08a964ba051681c05dc3f8faa.png?wh=866x268)

GNU Grep 则是 grep 命令的一个工业级实现，在项目官方 Readme 中作者是这样介绍它的：

> This is GNU grep, the “fastest grep in the west” (we hope).

其实就是在说这是世界上最快的grep程序。当然，这款从上世纪就诞生的软件，敢这么说自己也是因为它有着十足的底气。

GNU Grep 确实是将“文本搜索”这一简单的功能做到了极致。作者 Mike Haertel 自己写了[一封邮件](https://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html)解释 GNU Grep 为什么这么快，主要有两点：

1. 它避免了检查每一个byte
2. 对于被检查的byte，只需要执行非常少的指令

**第一点的主要优化就在于 GNU Grep 用到了非常知名的字符串匹配算法：Boyer Moore 算法**，也就是我们常说的 BM 算法，它是目前已知的在大多数工业级应用场景中最快的字符串匹配算法，因而被广泛应用在各种需要搜索关键词的软件中，许多文档编辑器快捷键 `ctrl+f` 对应的搜索功能都是基于这个算法实现的。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（7） 💬（1）<div>BM算法和KMP算法是类似的，都是采用了预处理来加快查询，区别是KMP扫描和匹配方向是相同的，都是从左到右，BM扫描从左到右，匹配从右到左，在字符串差异比较大的情况，可以跳过更多，这也是坏字符算法的作用，但是仅仅凭着坏字符算法处理两个字符串比较接近的情况，复杂度就会退化为O(m*n),这个时候引入KMP类似的子串跳转算法，避免了最差的情况，可以取得O(m+n)。坏字符类似于粗调，只用到了当前不匹配的字符，好后缀类似于精调，用到了不包括当前字符所有已经匹配的字符串。BM和KMP算法和红黑树算法一样，属于我一看就忘的类型,:）。</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/1a/367ebeac.jpg" width="30px"><span>Jump</span> 👍（0） 💬（2）<div>str = AMPLEMABCABCMABC，pattern = ABCABCMABC，示例代码有点问题。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/85/d2/045c63fb.jpg" width="30px"><span>王建新</span> 👍（0） 💬（1）<div>leetcode好像有类似很多的字符串匹配题目 思路就是这样的</div>2022-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a8/b2/5acb4806.jpg" width="30px"><span>Daneil</span> 👍（0） 💬（1）<div>不好意思，刚才看错了</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a8/b2/5acb4806.jpg" width="30px"><span>Daneil</span> 👍（0） 💬（0）<div>好后缀计算的代码中，14-17行后缀的遍历有误。应当让后缀从小到大去进行遍历，而不是让后缀从大到小，一旦有一个大的后缀在gs表中，那么他的所有子后缀都不需要遍历，一定在gs表中。</div>2022-01-06</li><br/>
</ul>