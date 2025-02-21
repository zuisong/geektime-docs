你好，我是徐文浩。

在上节课里，我们一起了解了Twitter整体搭建数据系统的经验。不过，那一篇论文的主要内容还是在方法论上，一旦我们想要把这个方法论利用到我们当下就在搭建的数据系统里，就有些无从下手的感觉。

不过，好在Twitter还发表了很多有着具体实战经验的论文。那么，今天我就请你一起来学习下《[The Unified Logging Infrastructure for Data Analytics in Twitter](https://arxiv.org/pdf/1208.4171.pdf)》这篇论文。在这篇论文里，Twitter一点儿都没有藏私，而是给出了大量具体的实践技巧，你完全可以用“抄作业”的方式，把里面的做法用到自己的系统里。事实上，在我之前搭建的大数据系统中，就从里面吸取了大量的经验。

希望在学习完这节课之后，你可以直接把所看到的具体实战方法用到实践中去。无论是对你现在已有的系统进行对照改进，还是在建设新系统的时候把Twitter的方法作为模版，都是一个不错的选择。

## 统一的用户行为日志和元数据管理

上节课我们就说过，Twitter为了减少碎片化的日志文件和日志格式，最终在内部启动了一个项目，统一从客户端的视角来记录用户行为日志。这个日志的格式，自然是通过Thrift的Schema来定义的。而有了这个日志之后，所有的工程师和数据分析师，都可以在一个共识下工作。大部分的数据分析工作，也不再需要大量的Join操作，先把数据在Hadoop上搬运一遍。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_88604f</span> 👍（1） 💬（0）<div>这种能力在底层数据格式里默认都支持了吧，像parquet、carbon</div>2022-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/96/60/2c77c899.jpg" width="30px"><span>靴</span> 👍（0） 💬（0）<div>这个埋点设计好妙啊</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（0）<div>是因为这样的索引不方便数据重新分配，代价太大？</div>2022-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>clickhouse 好像也是这样在block级别建立索引</div>2022-01-24</li><br/>
</ul>