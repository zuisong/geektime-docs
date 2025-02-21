这周我们分享的内容是如何理解网页和网页之间的关系。周一我们介绍了用图（Graph）来表达网页与网页之间的关系并计算网页的重要性，就是经典算法PageRank。今天我来介绍一下PageRank的姊妹算法：**HITS算法**。

## HITS的简要历史

HITS是Hypertext-Induced Topic Search算法的简称。这个算法是由康奈尔大学计算机科学教授乔·克莱恩堡（Jon Kleinberg）于1998年发明的，正好和我们周一讲的布林和佩奇发表PageRank算法是同一年。

这里有必要简单介绍一下乔这个人。乔于1971年出生在马萨诸塞州波士顿。1993年他毕业于康奈尔大学获得计算机科学学士学位，并于1996年从麻省理工大学获得计算机博士学位。1998的时候，乔正在位于美国西海岸硅谷地区的IBM阿尔玛登（Almaden）研究院做博士后研究。HITS的工作最早发表于1998年在旧金山举办的第九届ACM-SIAM离散算法年会上（详细论述可参阅参考文献）。

乔目前是美国国家工程院（National Academy of Engineering）和美国自然与人文科学院（American Academy of Arts and Sciences）院士。顺便提一下，乔的弟弟罗伯特·克莱恩堡也在康奈尔大学计算机系任教职。

## HITS的基本原理

在介绍HITS算法的基本原理之前，我们首先来复习一下网页的网络结构。每一个网页都有一个“输出链接”（Outlink）的集合。输出链接指的是从当前网页出发所指向的其他页面，比如从页面A有一个链接到页面B，那么B就是A的输出链接。根据这个定义，我们来看“输入链接”（Inlink），指的就是指向当前页面的其他页面，比如页面C指向页面A，那么C就是A的输入链接。

要理解HITS算法，我们还需要引入一组概念：**“权威”（Authority）结点**和**“枢纽”（Hub）结点**。这两类结点到底是什么意思呢？
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/8f/f9999406.jpg" width="30px"><span>xxw</span> 👍（4） 💬（0）<div>感觉可以适量列些公式。用文字表达公司有点闷逼</div>2018-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/9f/0343d633.jpg" width="30px"><span>黄德平</span> 👍（3） 💬（0）<div>理一下思路，L表示连接矩阵，Lij是矩阵i行j列的元素，这个值取1当且仅当节点有链接指向节点j，否则为0。L的转置用M表示，根据权威值X和枢纽值Y的定义，我们可以得到
X=MY
Y=LX
进一步可以得到
X=MLX
Y=LMY
LM和ML分别是两个矩阵的乘积，X和Y
可以迭代求解了。

真是费劲。。。
极客时间的回复是否可以支持latex公式渲染，或者图片</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/72/76838c57.jpg" width="30px"><span>白杨</span> 👍（1） 💬（0）<div>某种意义上，可以把权威理解为精度，枢纽理解为广度，然后用F值的思想去合并</div>2018-05-16</li><br/>
</ul>