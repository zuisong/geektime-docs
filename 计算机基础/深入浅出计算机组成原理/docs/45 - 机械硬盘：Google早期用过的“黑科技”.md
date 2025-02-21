在1991年，我刚接触计算机的时候，很多计算机还没有硬盘。整个操作系统都安装在5寸或者3.5寸的软盘里。不过，很快大部分计算机都开始用上了直接安装在主板上的机械硬盘。到了今天，更早的软盘早已经被淘汰了。在个人电脑和服务器里，更晚出现的光盘也已经很少用了。

机械硬盘的生命力仍然非常顽强。无论是作为个人电脑的数据盘，还是在数据中心里面用作海量数据的存储，机械硬盘仍然在被大量使用。不仅如此，随着成本的不断下降，机械硬盘还替代掉了很多传统的存储设备，比如，以前常常用来备份冷数据的磁带。

那这一讲里，我们就从机械硬盘的物理构造开始，从原理到应用剖析一下，看看我们可以怎么样用好机械硬盘。

## 拆解机械硬盘

上一讲里，我们提到过机械硬盘的IOPS。我们说，机械硬盘的IOPS，大概只能做到每秒100次左右。那么，这个100次究竟是怎么来的呢？

我们把机械硬盘拆开来看一看，看看它的物理构造是怎么样的，你就自然知道为什么它的IOPS是100左右了。

我们之前看过整个硬盘的构造，里面有接口，有对应的控制电路版，以及实际的I/O设备（也就是我们的机械硬盘）。这里，我们就拆开机械硬盘部分来看一看。

![](https://static001.geekbang.org/resource/image/51/14/5146a2a881afb81b3a076e4974df8614.jpg?wh=1561%2A1005%3Fwh%3D1561%2A1005)

[图片来源](https://www.symantec.com/connect/articles/getting-hang-iops-v13)

一块机械硬盘是由盘面、磁头和悬臂三个部件组成的。下面我们一一来看每一个部件。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/11/0a/59639f1f.jpg" width="30px"><span>penbox</span> 👍（97） 💬（7）<div>这个解决方案真的太妙了，简单有效又容易操作。有点编程珠玑里面的位图排序算法的感觉。
机械硬盘分区是由外到内的，C盘在最外侧依次类推，所以机械硬盘里面C盘的性能是所有分区里最好的。
要想只用最外侧1&#47;4的磁道，只需要简单地把C盘分成整个硬盘1&#47;4的容量，剩下的容量弃而不用就可以达到文章里面的效果了！</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（44） 💬（1）<div>老师，Partial Stroking技术不就是用空间换时间吗，原来计算机优化的本质都是一样的。
5400 转的硬盘，只使用一半的硬盘空间，我们的 IOPS 能够提升多少呢？
每分钟5400转，每秒可以转180个半圈，平均延时就是5.5ms
只使用一半硬盘空间，平均寻道时间就是9ms&#47;2=4.5ms
总体IOPS就是1s &#47; (5.5ms + 4.5ms) = 100 IOPS</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（16） 💬（1）<div>HDD 硬盘通常有个磁盘清理的操作，有什么用？</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ee/e7/4375e97c.jpg" width="30px"><span>雲至</span> 👍（11） 💬（4）<div>也许可以用另外一方法   就是多加几个磁头   每个负责一部分就快了   就好像几个人一块找东西</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e1/d4/1b5ac51e.jpg" width="30px"><span>山间竹</span> 👍（3） 💬（2）<div>文中“实践当中，我们可以只用 1&#47;2 或者 1&#47;4 的磁道，也就是最外面 1&#47;4 或者 1&#47;2 的磁道。这样，我们硬盘可以使用的容量可能变成了 1&#47;2 或者 1&#47;4。”
这个容量计算有误吧，现在硬盘大体实现了等密度了，不是正比例关系。</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（3） 💬（1）<div>本科的操作系统课程上还有一个电梯算法,  操作系统对于无重叠的磁盘IO操作进行排序, 然后在单向的寻道行程里完成这些数据的访存。 就像电梯一样, 从1层到100层, 按一个顺序送所有乘客, 而不是先来先送让电梯往复运动。 个人感觉在高并发的数据中心上, 这个方案要比谷歌的做法更高效。</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/1e/2a40a5ca.jpg" width="30px"><span>大明</span> 👍（3） 💬（1）<div>老师，是不是漏了一节了呢，dma，kafka为什么快。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（2） 💬（1）<div>99IOPS左右，大概也就是100
草稿纸上算的，计算过程就不写了！不知道结果对不对</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（2） 💬（1）<div>老师，Partial Stroking技术不就是用空间换时间吗，按照老师的推算公式。
5400 转的硬盘，只使用一半的硬盘空间，我们的 IOPS 能够提升多少呢？
每分钟5400转，每秒可以转180个半圈，平均延时就是5.56ms

优化前 1000&#47;（5.56+9）= 68.68

优化后 1000&#47;（5.56+9&#47;2）= 99.4

提升了 (99.4-68.68)&#47;68.68*100=44.7%</div>2019-08-12</li><br/><li><img src="" width="30px"><span>haer</span> 👍（1） 💬（1）<div>如果是用更慢的 5400 转的硬盘
平均延时：
1s &#47; 180 = 5.56 ms
优化前：
1s &#47; (5.56ms + 9ms) = 68.7 IOPS
优化后：
1s &#47; (5.56ms + 9ms&#47;2) = 99.4 IOPS
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f8/49/0c3a380d.jpg" width="30px"><span>Geek_aeeb45</span> 👍（0） 💬（1）<div>&quot;读取数据，其实就是两个步骤。一个步骤，就是把盘面旋转到某一个位置。在这个位置上，我们的悬臂可以定位到整个盘面的某一个子区间。这个子区间的形状有点儿像一块披萨饼，我们一般把这个区间叫作几何扇区（Geometrical Sector），意思是，在“几何位置上”，所有这些扇区都可以被悬臂访问到。另一个步骤，就是把我们的悬臂移动到特定磁道的特定扇区，也就在这个“几何扇区”里面，找到我们实际的扇区。找到之后，我们的磁头会落下，就可以读取到正对着扇区的数据。&quot;，老师，那写入数据，又是什么样的过程呢？</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/54/c9990105.jpg" width="30px"><span>bro.</span> 👍（0） 💬（1）<div>5400转&#47;1min = 90转&#47;s ，所以平均延迟为 1000 &#47; 180半转 = 5.56ms , 使用 1&#47;4的硬盘 为 9&#47;4 = 2.25ms,则总体IOPS为 1000 ms &#47;( 5.56 + 2.25) = 128 IOPS</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/25/23d2af5d.jpg" width="30px"><span>miyan</span> 👍（0） 💬（1）<div>5400rpm=90r&#47;s，也就是每s180个半圈

平均延时 1s &#47; 180 = 5.56ms

IOPS:

优化前 1000&#47;（5.56+9）= 68.68

优化后 1000&#47;（5.56+9&#47;2）= 99.4</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/f0/678e6643.jpg" width="30px"><span>赵捌玖</span> 👍（0） 💬（1）<div>5400 转的硬盘，一秒钟可以转180个半圈（5400rpm&#47;60*2）,平均时延约5.56ms(1000ms&#47;180),如果寻道时间为9ms，那么原本 IOPS 为68.7（1000ms&#47;(5.56+9)ms)；如果只用1&#47;2的磁道，那么IOPS约为99.4(1000ms&#47;(5.56+9&#47;2)ms)，提升大约1.4倍。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（0） 💬（1）<div>64-100iops
</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/06/72b01bb7.jpg" width="30px"><span>美美</span> 👍（17） 💬（0）<div>文中柱面的说法有误，文中“上下平行的盘面上相同的扇区”是柱面，应该是多个盘面上相同磁道组成的圆柱是柱面。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/f0/6c34b90f.jpg" width="30px"><span>David</span> 👍（7） 💬（0）<div>5400&#47;60=90圈=180半圈
1s&#47;180=5.55ms 平均延时
4-10ms 平均寻道时间
全部空间：
1s&#47;9.55 = 104 iops，1s&#47;15.55 =64 iops
一半空间：
1s&#47;7.55 = 132 iops，1s&#47;10.55 = 94 iops</div>2019-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（5） 💬（3）<div>这个只用最外面磁道的方法还真是奇思妙想，不过老师，实际上能用什么软件通过格式化的方式屏蔽内侧磁道，只保留外部磁道呢？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a8/3d/652e0b46.jpg" width="30px"><span>表酱紫嘛</span> 👍（3） 💬（0）<div>很奇怪磁盘旋转和寻道不能同时进行？</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（3） 💬（2）<div>扇区的大小是固定的，但是越在外面的扇区面积越大，感觉可以比里面的扇区多存储数据。那么扇区的面积跟能存储多小数据有无关系？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/d6/f66133b4.jpg" width="30px"><span>吴贤龙</span> 👍（2） 💬（1）<div>老师，请教一下，我理解的是，机械硬盘在开机通电以后，应该是一直在高速转动，所以这么理解的话，这个文章里描述的读写扇区的逻辑，我梳理不通呢？磁盘再转动，存储数据的扇区也在转动，怎么定位呢？我是不是哪里的理解有误？</div>2020-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKj3GbvevFibxwJibTqm16NaE8MXibwDUlnt5tt73KF9WS2uypha2m1Myxic6Q47Zaj2DZOwia3AgicO7Q/132" width="30px"><span>饭</span> 👍（1） 💬（0）<div>老师，看了不少数据库写日志时提到，是顺序读写来提高性能。那程序让日志读写变成顺序写的原理是怎么样的了。网上也没发现有资料介绍。有点好奇</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（1） 💬（0）<div>应该还有一个整页读的知识点，每页4k</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>对于一块5400转的硬盘，其平均延时大约是5.56毫秒（由于计算中的除法，实际值是1&#47;180秒，即每秒180个半圈）。如果我们考虑原本的平均寻道时间是9毫秒，那么这块硬盘原本的IOPS大约是68.7次&#47;秒。

当我们使用Partial Stroking技术，只使用硬盘的一半空间时，平均寻道时间减半，变为4.5毫秒。在这种情况下，IOPS提升到了大约99.45次&#47;秒。

因此，通过只使用硬盘的一半空间，5400转硬盘的IOPS从大约68.7提升到了大约99.45，接近于原来的1.5倍。</div>2024-09-09</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>影响磁盘IOPS的有两个因素，分别是“平均延时 + 寻道时间”。可以通过提高转速减少平均时延;可以通过减少悬臂行程缩短寻道时间，方法是可以只用 1&#47;2 或者 1&#47;4 的磁道，也就是最外面 1&#47;4 或者 1&#47;2 的磁道。这样，硬盘可以使用的容量可能变成了 1&#47;2 或者 1&#47;4。但是寻道时间也变成了 1&#47;4 或者 1&#47;2，因为悬臂需要移动的“行程”也变成了原来的 1&#47;2 或者 1&#47;4</div>2024-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（0） 💬（0）<div>总结:hdd硬盘是如何读取数据的，基本构成，硬盘是由盘面，磁头，悬臂组成，盘面是由金属铝，玻璃，磁作为基础，外面磁性涂层，数据存储到涂层里，硬盘由很多盘面组成，磁头是每个盘面都有对应的磁头，磁头通过放到盘面上，读取数据，悬浮臂是把磁头自动到盘面上磁道上。读取过程:盘面先转到对应的位置上，这叫，悬浮臂把磁头送到几何扇面上，影响读取速度的就是这2个指标。一次随礼访问，由两部分组成，一个是盘面移动到扇面的时间，叫平均延时，一个是悬臂移动到磁道的时间，寻道时间，7200转，240个半圈，1s&#47;240=4ms，寻道时间也是大约4-10ms，也就是一次随机访问的时间8ms，iops=1000&#47;8=125，也就是iops，提升性能有多种方式，一种是顺序读写，减少悬臂寻道的时间，还有一种是减少磁道，用空间换时间。</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/50/aee9fdab.jpg" width="30px"><span>小杰</span> 👍（0） 💬（0）<div>根据老师的方法走了一下。5400原先的IOPS：1&#47;（1 &#47; 5200 &#47; 60 &#47; 2 + 9）= 68.7。只是使用一半磁盘空间，悬臂时间&#47;2: 1&#47;（1 &#47; 5200 &#47; 60 &#47; 2 + 9 &#47;2）= 99.4.
99.4 &#47; 68.7 = 1.45。提升了1.5接近。提升巨大</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ac/bf/f549183e.jpg" width="30px"><span>=</span> 👍（0） 💬（0）<div>比使用全部磁道的IOPS提升144.55%左右</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（0） 💬（0）<div>平均延时这里不太明白，为什么寻找一个几何扇区，需旋转半圈盘面，这是为什么老师，在文章里没找到答案，望老师买忙之中抽出时间回复下。</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7a/e3/145adba9.jpg" width="30px"><span>不一样的烟火</span> 👍（0） 💬（0）<div>老老师讲讲raid0原理</div>2019-10-20</li><br/>
</ul>