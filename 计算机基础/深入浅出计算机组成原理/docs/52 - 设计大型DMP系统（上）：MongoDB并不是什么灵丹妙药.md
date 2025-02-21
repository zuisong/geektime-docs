如果你一讲一讲跟到现在，那首先要恭喜你，马上就看到胜利的曙光了。过去的50多讲里，我把计算机组成原理中的各个知识点，一点一点和你拆解了。对于其中的很多知识点，我也给了相应的代码示例和实际的应用案例。

不过呢，相信你和我一样，觉得只了解这样一个个零散的知识点和案例还不过瘾。那么从今天开始，我们就进入应用篇。我会通过两个应用系统的案例，串联起计算机组成原理的两大块知识点，一个是我们的整个存储器系统，另一个自然是我们的CPU和指令系统了。

我们今天就先从搭建一个大型的DMP系统开始，利用组成原理里面学到的存储器知识，来做选型判断，从而更深入地理解计算机组成原理。

## DMP：数据管理平台

我们先来看一下什么是DMP系统。DMP系统的全称叫作数据管理平台（Data Management Platform），目前广泛应用在互联网的广告定向（Ad Targeting）、个性化推荐（Recommendation）这些领域。

通常来说，DMP系统会通过处理海量的互联网访问数据以及机器学习算法，给一个用户标注上各种各样的标签。然后，在我们做个性化推荐和广告投放的时候，再利用这些这些标签，去做实际的广告排序、推荐等工作。无论是Google的搜索广告、淘宝里千人千面的商品信息，还是抖音里面的信息流推荐，背后都会有一个DMP系统。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e2/e9/5be2a24c.jpg" width="30px"><span>胖头小C</span> 👍（66） 💬（1）<div>SSD硬盘好处是读写更快，但是使用寿命不长，在Kafka经常擦除情况下，机械盘更耐用，经济，而且是顺序读写，机械盘也是很快的，综合还是机械盘更好</div>2019-09-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/IPdZZXuHVMibwfZWmm7NiawzeEFGsaRoWjhuN99iaoj5amcRkiaOePo6rH1KJ3jictmNlic4OibkF4I20vOGfwDqcBxfA/132" width="30px"><span>鱼向北游</span> 👍（34） 💬（1）<div>不差钱可以用ssd呀 ssd的顺序写速度更快
但是 kafka这种应该会频繁擦写 ssd的寿命扛不住
对于存档 hdd普遍容量大 存档成本低 组raid价格也便宜
对于和ssd顺序读写的性能差距 可以用扩大partition数量来做些弥补
怎么感觉说到底最后是钱的问题呢</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（16） 💬（1）<div>我觉得没有必要使用SSD，Kafka主要利用PageCache来提高系统写入的性能，而且Kafka对磁盘大多是顺序读写，在磁盘上提高IOPS，并不能显著的提升Kafka的性能。</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（12） 💬（2）<div>Kafka使用SSD硬盘：
好处：
Kafka是顺序追加写，比较适合SSD硬盘的特性；
坏处：
Kafka的落盘数据类似于日志，顺序追加写SSD比机械硬盘没有太多的优势，再者擦写太频繁SSD硬盘有擦写寿命，使用SSD的性价比不如机械硬盘。</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（7） 💬（3）<div>	以下是个人对此的理解：希望老师可以在下节课把这节课的答案公布。
分成两部分分别阐述个人对此的理解
一．机械硬盘
	机械硬盘的好处是寿命：不过机械硬盘的问题在于速度，不同的机械硬盘有不一样的特性，即使用机械硬盘也要选择缓存偏大且读性能较好的蓝盘。由于kafka是充分利用缓存，毕竟kafka只是消息队列-只是中间件，我们不可能把数据放在kafka中，还是会使用的NOSQL数据库，故而其实际需求是对读性能要求较高的存储设备。
二．SSD
SSD读写性能比其实是相对固定的：无论是哪个厂商，其实最终发现这是一个定值；有能力其实SSD确实是一个不错的选择。不过我们在讨论SSD的寿命时其实忽略了一个问题，什么操作影响SSD的寿命？SSD存在的硬件条件和场景是什么？
1.SSD的寿命问题：其实这个问题就像早期说液晶屏一样，额定寿命大概是3年左右，其实大多数实际情况都在5年左右；真正影响SSD寿命的不是读，而是写，这个问题其实机械硬盘同样有。
2.SSD存在的硬件条件是什么：服务器、PC；现在一台PC或者服务器基本上5-6年就各种硬件出现问题，SSD如果使用场景和HDD类似其实寿命是几乎一样的；我们不太可能在服务器都出问题的情况下还去使用使用吧。我自己笔记本电脑是单双硬盘：不过由于市场提供的尺寸不一样，大小略有区别，使用场景几乎完全一样，都各自有一个300G的空间跑虚机做测试，目前已经使用了4年多了，性能和4年前没区别，唯一的区别是当时HDD的代价是SSD的一半左右；现实中服务器的使用也就不超过5-6年，此时其实主板、电源、CPU的散热系统已经基本出问题且厂家和市场都没有相应可换的硬件配件了。
综上所述：故而个人觉得Kafka场景其实资金允许的情况下还是SSD，因为它的坏处其实传统硬盘同样有，这是我们不能回避HDD的硬件问题去说SSD的问题。即使使用HDD其实我们还是要选取读性能强于写性能且缓存偏大的硬盘，况且其实SSD的读写速度方面同样是读方面更好。严重写&gt;读的场景下其实HDD的损坏速度同样非常快，只不过硬件代价低一些而已，但是耗时同样高许多。
      期待老师的下节课：谢谢老师的教诲。
</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/60/049a20e9.jpg" width="30px"><span>吴宇晨</span> 👍（3） 💬（1）<div>成本的问题ssd顺序读速度能更快，但是价格贵了很多，还有大概kafka主要读写是利用pagecache</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（26） 💬（0）<div>1.重视底层知识，核心知识，万丈高楼平地起。
2.使用场景。没有一招鲜，吃遍天的技术。
3.要有量级的概念。kv数据库，数据管道，数据仓库，就根本不是一个量级的事情，每个量级都应该有自己的最优方案。

刚工作一年多一点，不对之处请老师指出
</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/ad/52df3832.jpg" width="30px"><span>逍遥法外</span> 👍（11） 💬（1）<div>看的真过瘾</div>2019-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK7OIm3bNZ5X3Hgukib14xfrEmvVVkpdahJ1sicWI6X8vZeqHcCYk5ayeHODsjmUWsfMf7LiaE29wptg/132" width="30px"><span>李伟</span> 👍（2） 💬（0）<div>读到这里，为我打开了一个世界大门，我知道原来这才是设计和技术选型，而不是以前的bug少，维护快。</div>2021-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（2） 💬（0）<div>工作中一直在用MongoDB但是并没有想过它不适合那些场景、今天老师从底层原理给我们刨析了个究竟

day52 笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11510567.html</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（2） 💬（0）<div>满满的干货，我先干为敬</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/93/365ba71d.jpg" width="30px"><span>陈德伟</span> 👍（1） 💬（0）<div>图里kv数据库的读写比例是不是写错了，应该读多写少</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5f/e6/19778e70.jpg" width="30px"><span>Mr.埃克斯</span> 👍（1） 💬（0）<div>数据密集型应用系统设计 这本书挺不错，有空二刷一下。</div>2020-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/f7/abb7bfe3.jpg" width="30px"><span>刘冲</span> 👍（1） 💬（0）<div>数据仓库可以用elasticsearch</div>2019-11-22</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>mongodb的使用场景是初创业务，需求不稳定需要灵活应对，schema less，对事务性要求不高，没有文档之间join的情形。适合做业务数据库，不适合做分析性数仓</div>2024-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/cf/21bea6bb.jpg" width="30px"><span>衣舞晨风</span> 👍（0） 💬（0）<div>kv数据库为什么没有选用elasticsearch呢？</div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f8/49/0c3a380d.jpg" width="30px"><span>Geek_aeeb45</span> 👍（0） 💬（0）<div>“因为低延时、高并发、写少读多的 DMP 的 KV 数据库，最适合用 SSD 硬盘”，这里的“写少读多”，在表格中是“写多读少”，希望老是能解惑一下</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/23/18/4284361f.jpg" width="30px"><span>易飞</span> 👍（0） 💬（0）<div>太牛了</div>2021-10-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（0） 💬（1）<div>老师，为什么没有考虑用redis做kv呀？</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e1/7a/b206cded.jpg" width="30px"><span>人在江湖龙在江湖</span> 👍（0） 💬（0）<div>DMP系统讲的真的很好，受益匪浅。</div>2020-11-11</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>如果Kafka 用了SSD硬盘估计响应时间会减少不少，尤其考虑PCI Express对于串行读写的优化更是如此，但是数据管道解决方案，响应时间要求不高，这个时候HDD硬盘寿命长价格低的的特点可能更重要一些。</div>2020-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（0） 💬（1）<div>老师好，一般好多应用严格要求响应都是几ms，比如文章说的1ms，这种一般是怎么做到的呢，需要怎么优化，因为我感觉随便处理个什么逻辑或者查询缓存或者远程调用就不止1ms了。。</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/b5/4dc0c109.jpg" width="30px"><span>Cyril</span> 👍（0） 💬（0）<div>干活慢慢，受益匪浅</div>2020-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLRwYJzyB6pdy4NANXiaxBEibOOHBa8KC0pQC8AGveDYloW4rfM42E4rEO6ohhQSiciaMGdDNBrkJkYtA/132" width="30px"><span>谢军</span> 👍（0） 💬（1）<div>那么一共我们需要 10 亿 x 500 x (4 + 4) Bytes = 400 TB 的数据了</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（0） 💬（0）<div>hive on mapreduce太慢了，推荐用spark sql。</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/f0/6c34b90f.jpg" width="30px"><span>David</span> 👍（0） 💬（0）<div>👍</div>2019-10-16</li><br/>
</ul>