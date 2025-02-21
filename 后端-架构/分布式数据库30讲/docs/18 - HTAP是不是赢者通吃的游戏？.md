你好，我是王磊，你也可以叫我Ivan。

这一讲的关键词是HTAP，在解释这个概念前，我们先要搞清楚它到底能解决什么问题。

有关OLTP和OLAP的概念，我们在[第1讲](https://time.geekbang.org/column/article/271373)就已经介绍过了。OLTP是面向交易的处理过程，单笔交易的数据量很小，但是要在很短的时间内给出结果；而OLAP场景通常是基于大数据集的运算。

![](https://static001.geekbang.org/resource/image/38/1a/382508db9c5e251760d2eb443ebcc41a.jpg?wh=2700%2A1180)

OLAP和OLTP通过ETL进行衔接。为了提升OLAP的性能，需要在ETL过程中进行大量的预计算，包括数据结构的调整和业务逻辑处理。这样的好处是可以控制OLAP的访问延迟，提升用户体验。但是，因为要避免抽取数据对OLTP系统造成影响，所以必须在日终的交易低谷期才能启动ETL过程。这样一来， OLAP与OLTP的数据延迟通常就在一天左右，习惯上大家把这种时效性表述为T+1。其中，T日就是指OLTP系统产生数据的日期，T+1日是OLAP中数据可用的日期，两者间隔为1天。

你可能已经发现了，这个体系的主要问题就是OLAP系统的数据时效性，T+1太慢了。是的，进入大数据时代后，商业决策更加注重数据的支撑，而且数据分析也不断向一线操作渗透，这都要求OLAP系统更快速地反映业务的变化。

## 两种解决思路

说到这，你应该猜到了，HTAP要解决的就是OLAP的时效性问题，不过它也不是唯一的选择，这个问题有两种解决思路：
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/71/3d/da8dc880.jpg" width="30px"><span>游弋云端</span> 👍（4） 💬（0）<div>可以后台启动一个轮询日志增量的线程，当差异大于一定量的时候触发实际的数据同步。或者在心跳包中增加一个版本用于比对，当差异大的时候，触发主动同步。这样不用等到请求到达时触发，省掉这个等待时延。但是由于是Raft的非成员节点，怎么做都会有一定的数据差异，单对于大多OLAP分析场景应该是足够使用了。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（2） 💬（0）<div>没有接触过OLAP。

是不是可以不用每次都去请求“最新”的日志增量，而是按需请求数据：本地保存一个数据新旧的时间戳，如果早于读请求的时间戳，就不用去请求了；

或者设置一个质量因子，可以做到分配请求数据，采用类似滑动平均的算法，动态计算目标指标，达到质量要求后就停止请求数据。</div>2020-09-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLia17ibYsLic20bEFNkvObLpXicfUpYd9OeWvKxml0rNic3NDyRQ6KHl7wtEp0x993tJsTDsLHX2UHRYw/132" width="30px"><span>Geek_761876</span> 👍（1） 💬（0）<div>有人说两份数据的做法是&quot;缝合怪&quot;，老师怎么看这个问题？</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a2/46/6721d8bf.jpg" width="30px"><span>iswade</span> 👍（1） 💬（1）<div>可以通过读一致的旧版本来实现吧，对于OLAP也完全满足要求了。</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（0） 💬（0）<div>最近Snowflake也公布了进军HTAP</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（0） 💬（0）<div> 我看好多其他开源写的db 项目，delta Tree</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/b8/81/a0afe928.jpg" width="30px"><span>杜思奇</span> 👍（0） 💬（0）<div>我认为OLAP相当于一艘大轮船（技术上追求高吞吐 QPS）而OLTP相当于一辆小轿车（技术追求高并发
、低延迟）</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/cf/43f201f2.jpg" width="30px"><span>幼儿编程教学</span> 👍（0） 💬（0）<div>pax格式其实没太看懂。特别是和dsm的区别。老师能否再详细介绍下？谢谢！</div>2020-11-22</li><br/><li><img src="" width="30px"><span>myrfy</span> 👍（0） 💬（0）<div>当客户请求的时间戳可以确信小于服务端的时间戳时。难点应该就是如何保证客户端和服务端在时间上的同步。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/47/46da4585.jpg" width="30px"><span>Fan()</span> 👍（0） 💬（0）<div>受益匪浅</div>2020-09-18</li><br/>
</ul>