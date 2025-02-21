你好，我是王健伟。

上节课我带你学习了串的朴素模式匹配算法，这种算法思想简单，执行效率不高。为什么这么说呢？我带你仔细分析一下。

## 朴素模式匹配算法的问题

串的朴素模式匹配算法经常可以看到主串的指针point1回退的情形。导致匹配时间增加。看一下图1：

![](https://static001.geekbang.org/resource/image/13/4d/1391e6b5b8987f8b6088d874a935714d.jpg?wh=2187x583 "图1 串的朴素模式匹配算法【步骤1】")

图1中，在主串中寻找子串“google”内容，开头的“googl”都相同，但比较到第6个字符时，主串内容为‘o’，子串内容为‘e’，此时情形如图2所示：

![](https://static001.geekbang.org/resource/image/1a/89/1af58c98eb19587a6fe92a98f565a789.jpg?wh=2154x555 "图2 串的朴素模式匹配算法【步骤2】")

那么point1指针就要从下标为5的位置回退到下标为1的位置，为什么回退到下标为1的位置呢？其实很容易看得出来，只需要把子串位置向右移动一个位置，而后子串的开头字符对应的是哪个下标，主串的指针point1就回退到哪个下标位置，下一次比较就是主串中下标1位置的字符o与子串的开头位置的字符g作比较。如图3所示：

![](https://static001.geekbang.org/resource/image/80/1a/808e995f766ae7b16d832110ff14891a.jpg?wh=2187x612 "图3 串的朴素模式匹配算法【步骤3】")

其实，整个串的朴素模式匹配算法的执行过程也可以看作是子串不断右移与主串对应位置字符逐个比较的过程。这个过程中，point1指针在字符比较失败的情况下往往需要回退（左移）若干位置来重新与子串的各个字符比较，整个算法的执行效率显然不会很高。

正是因为串的朴素模式匹配算法是比较低效的，所以又提出了KMP算法。KMP算法是一种改进的字符串匹配算法，由D.E.Knuth，J.H.Morris和V.R.Pratt三位大神提出的，因此人们称它为克努特—莫里斯—普拉特算法（简称KMP算法）。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>老师会讲next数组的构造吗？</div>2023-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f0/82/f235d91d.jpg" width="30px"><span>Yj.yolo</span> 👍（1） 💬（0）<div>图16下图应该是错了吧，point2应该指向位置2，但是图中指向位置3了</div>2023-06-28</li><br/>
</ul>