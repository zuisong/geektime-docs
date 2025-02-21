你好，我是蔡元楠。

今天我要与你分享的主题是“Beam Window：打通流处理的任督二脉”。

在上一讲中，我们一起用Beam编写了第一个完整的WordCount项目，我们所用的例子是统计莎士比亚的文集中最常使用到的一些单词。

这里我们所用到的“莎士比亚文集”这种类型的数据集是一个静态的数据集。也就是说，我们在生成输入数据集的时候，就已经知道了这个数据集是完整的，并不需要再等待新的数据进来。

根据前面的内容，我们可以把这种数据集归类为有界数据集（Bounded Dataset）。这里我们的数据流水线就是一个批处理的数据流水线。

这个时候你可能会有一个疑问，如果我们想要统计的内容是一个正在连载的小说，我们在编写数据流水线的时候，这个小说还并没有完结，也就是说，未来还会不断有新的内容作为输入数据流入我们的数据流水线，那我们需要怎么做呢？

这个时候我们就需要用到窗口（Window）这个概念了。

## 窗口

在Beam的世界中，窗口这个概念将PCollection里的每个元素根据时间戳（Timestamp）划分成为了不同的有限数据集合。

当我们要将一些聚合操作（Aggregation）应用在PCollection上面的时候，或者我们想要将不同的PCollections连接（Join）在一起的时候，其实Beam是将这些操作应用在了这些被窗口划分好的不同数据集合上的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/1b/e88e33ba.jpg" width="30px"><span>Chang</span> 👍（4） 💬（2）<div>老师，我对会话窗口的理解不知道对不对：像文中的例子gap是5 min的话，假设有一个数据流每4分钟一个流入一个数据，是不是只需要一个窗口？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（3） 💬（1）<div>老师，文章读完有两点疑惑的地方：
1、文中滑动窗口样例，窗口大小1小时，滑动周期30分钟：
[July 8, 2019 0:00:00 AM, July 8, 2019 1:00:00 AM)
[July 8, 2019 0:30:00 AM, July 8, 2019 1:30:00 AM)
[July 8, 2019 1:00:00 AM, July 8, 2019 1:30:00 AM)
[July 8, 2019 1:30:00 AM, July 8, 2019 2:00:00 AM)
……
最后两条是否笔误了？窗口大小固定是1小时，我的理解应该是下面这样：
[July 8, 2019 1:00:00 AM, July 8, 2019 2:00:00 AM)
[July 8, 2019 1:30:00 AM, July 8, 2019 2:30:00 AM)
2、会话窗口是否可以这么理解：指定一段时间，在这段时间范围圈定的数据集上去应用固定窗口。
请老师指教，谢谢！
</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（2）<div>beam支持动态session gap定义吗？全局窗口的作用和使用场景是什么？beam支持自定义窗口吗？</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/79/f098c11d.jpg" width="30px"><span>YX</span> 👍（1） 💬（0）<div>在 Beam 的世界中，窗口这个概念将 PCollection 里的每个元素根据时间戳（Timestamp）划分成为了不同的有限数据集合。
--------------------------
请问下老师，是否支持按照元素个数设置窗口呢？</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/49/51/dbb22af1.jpg" width="30px"><span>理性的执着</span> 👍（0） 💬（0）<div>另外还有一个问题，会话窗口的静态时间间隔和固定窗口的静态时间大小的区别是什么，都是设置一个时间。这块理解不过去了</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/49/51/dbb22af1.jpg" width="30px"><span>理性的执着</span> 👍（0） 💬（0）<div>固定窗口由一个静态窗口大小定于，那么一个元素只属于一个窗口。
滑动窗口由一个静态窗口大小和一个滑动周期定义，一个元素可以属于多个窗口。
这两个能理解，不太理解会话窗口，
老师，我这么理解对吗？
会话窗口是由一个静态的时间间隔定义，那么一个元素应该只属于一个窗口吗？这样理解对吗？
会话窗口的时间间隔跟滑动窗口的滑动周期好像呀</div>2020-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/3d/93aa82b6.jpg" width="30px"><span>Junjie.M</span> 👍（0） 💬（0）<div>老师问下，流和批的区别就是看其使用那种窗口吗？那么这个窗口在哪里设置，input transform时吗？</div>2020-04-14</li><br/>
</ul>