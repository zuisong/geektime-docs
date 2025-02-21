你好，我是徐文浩。

在上节课里，我们看到了Dremel这个系统的数据存储是怎么回事儿的。不过，只是一个支持复杂嵌套结构的列存储，还没有发挥Dremel百分之百的威力。像Hive也在2011年推出了自己的列存储方案RCFile，并在后续不断改进提出了ORC File的格式。

列存储可以让一般的MapReduce任务少扫描很多数据，让很多MapReduce任务执行的时间从十几分钟乃至几个小时，下降到了几分钟。更短的反馈时间，使得数据分析师去探索数据，根据拿到的数据反馈不断从不同的角度去尝试分析的效率大大提高了。

不过，人们总是容易得陇望蜀的。当原先需要花几天时间写MapReduce程序才能分析数据的时候，我们希望能够通过写SQL跑分析数据。当原先SQL运行要30分钟、一个小时的时候，我们通过列存储把SQL执行的时间缩短到5分钟。但是在这5分钟里，我们的数据分析师该干嘛呢？只能去倒杯咖啡发个呆么？所以，我们自然希望SQL在大数据集上，也能在几十秒，甚至是十几秒内得到结果。

所以Google并没有在列存储上止步，而是借鉴了多种不同的数据系统，搭建起了整个Dremel系统，真的把在百亿行的数据表上，常见OLAP分析所需要的时间，缩短到了10秒这个数量级上。那么，这节课我们就来看看Dremel是通过什么样的系统架构，做到这一点的。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（25） 💬（1）<div>徐老师好，我想Dremel一开始把数据放在硬盘上，是因为当时“计算和存储分离”还不是大数据领域的主流思想，MPP数据库把计算和存储放在一起的思路，在过去证明是有效的，Dremel借鉴过去的成功经验是理所当然的。在Dremel 2020年的论文的第3.1节提到“At the time, it seemed the best way to squeeze out maximal performance from an analytical system was by using dedicated hardware and direct-attached disks. As Dremel’s workload grew, it became increasingly difficult to manage it on a small fleet of dedicated servers”。也就是说，那个时候大家都认为把计算和存储放在一起才是最佳的方法，但是随着数据规模和查询负载的增加，服务器管理越来越困难。

在今天看来把数据放在GFS上，一定比放在本地好，但是这中间其实经过了很多优化，一开始的时候选择把数据放在本地是更好的选择，因为相关的技术都是很成熟的，把数据放在GFS上需要解决很多未知的问题。把数据放在GFS上有很多好处，第一，数据扩容方便，管理简单；第二，数据拥有多个副本，对容灾友好；第三，数据可以被Dremel之外的工具使用，也方便和其他团队共享。</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/f0/0bbb0df5.jpg" width="30px"><span>乐天</span> 👍（10） 💬（0）<div>分开存储的好处：计算和存储分离，可以提供资源的利用率，数据量大就单纯增加存储节点，计算量大就增加计算节点，能更好的利用资源。同时任务调度时不用综合考虑节点的性能和数据的位置。
坏处：增加了网络传输的时间。
这样做是因为硬件性能特别是网络传输设备的提升很大，大数据量的传输已经不是大问题了，数据传输的时间可能比任务等待调度执行的时间还要短。</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（3） 💬（0）<div>尝试回答思考题：采用GFS最明显的好处是，存储扩展容易！
分片存储存本地硬盘，不可避免的、由于本地硬盘存不下了，要人肉做数据搬迁 或者 加一个元数据层进行管理，这不就是GFS么
另外，Dremel这个多层树状汇聚，很拉风！！</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/13/31ea1b0b.jpg" width="30px"><span>峰</span> 👍（3） 💬（0）<div>好处：不用管存储的高可用，解决struggle的问题。
坏处：打破了数据计算在同节点的设计，造成一定网络开销，解决方法：gfs能够提供固定block位置的api。
问题：开源OLAP系统中，有像dremel这样可以加入中间层（层数&gt; 1）的OLAP引擎吗? 以及如何确定中间层数。</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（1） 💬（0）<div>老师好，感觉Dremel的这种计算方式只适合简单计算，如果涉及join操作的话还如何通过这种树形服务拆分呢？</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ea/9a/02d589f9.jpg" width="30px"><span>斜面镜子 Bill</span> 👍（1） 💬（0）<div>好处理解是本地访问性能和数据质量相对好保证，处理逻辑也相对简单。坏处就是弹性和IO的吞吐会比较限制。当然也想听听作者的解答。</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4f/40/6cfa75cb.jpg" width="30px"><span>哈达syn$</span> 👍（0） 💬（0）<div>分开存储的好处：计算和存储分离，可以提供资源的利用率，数据量大就单纯增加存储节点，计算量大就增加计算节点，能更好的利用资源。同时任务调度时不用综合考虑节点的性能和数据的位置。

坏处：增加了网络传输的时间。

这样做是因为硬件性能特别是网络传输设备的提升很大，大数据量的传输已经不是大问题了，数据传输的时间可能比任务等待调度执行的时间还要短</div>2023-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/75/82/72398a60.jpg" width="30px"><span>?</span> 👍（0） 💬（0）<div>我觉得这个趋势是因为基础设施的发展，最开始数据和代码在一起是因为那时候网络的带宽有限。从远程读取数据对整个系统的性能影响较大。随着网络的发展，网络的开销逐渐不是影响架构的决定性的因素。其他的因素『扩容方便』『容灾恢复更快』占了决定性因素。</div>2022-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>思考题的那里，问题就是以前存储和计算是不分离的，但是放在了GFS上面，那么数据的容错管理那些就交给了GFS了。但是这里也有一个潜在的问题，数据倾斜问题。不知道多少朋友遇到过。以前使用spark计算的时候，调度算法中如果优先在数据节点计算，那么当该节点中的数据很多都是热数据时，那么就容易出现问题了。当时还出现过生产事故，后面改了调度算法为公平调度才解决的。

所以如果避免存储系统的数据倾斜问题，一直以来都是一个痛点和难点，哈希算法目前来说，已经真的快走到头了。</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>clickhouse 做到秒级别</div>2022-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/55/c2/7c0c5fa2.jpg" width="30px"><span>Jensen</span> 👍（0） 💬（0）<div>请问老师，Dremel不使用mr进行计算，那么它底层是如何进行计算的呢？</div>2021-11-28</li><br/>
</ul>