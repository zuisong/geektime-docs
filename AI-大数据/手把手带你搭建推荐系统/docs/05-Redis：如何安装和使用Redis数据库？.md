你好，我是黄鸿波。

上节课，我们了解了MongoDB数据库的概念，并学习了MongoDB数据库的搭建和基础使用方法。

这节课，我们来学习另一个常用到的数据库：Redis数据库。我们会从Redis数据库的概念入手，为你讲解Redis数据库的特性、应用场景以及安装和使用方法。

## 什么是Redis数据库？

Redis（Remote Dictionary Server）是一个开源的日志型 Key-Value 数据库。它由ANSI C语言编写，支持网络，可基于内存亦可持久化，还可以提供多种语言的API。它的读写速度快、性能好，支持久化，具有丰富的数据类型，并且使用起来非常简单。我们来详细看一下。

![](https://static001.geekbang.org/resource/image/ce/df/ceef01e19bdc713961a382yy9776dddf.png?wh=3000x1196)

Redis数据库的最大特点就是它是一个内存数据库。Redis主要是使用内存存储的，当用户需要提取数据时，Redis可以直接将数据从内存中提取出来，不必再经过磁盘的IO操作，这就让它的读取效率非常高，可以达到毫秒级别。一般来讲，像Redis这样基于内存存储的数据库，通常用于缓存常用且需要快速检索到的数据进行存储，让效率最大化。

Redis数据库还支持多种计算机编程语言。例如Java、Python、C、C++等，因此，几乎所有的编程语言都能很轻易地操作它。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：Redis是分布式系统，那么有多个节点时，会有一个中心节点吗？还是各节点平等？
Q2：Redis速度快，支持高达每秒 10 万次的并发请求，原因是什么？是因为单线程吗？ 另外，支持每秒 10 万次并发请求这个指标，对硬件有要求吗？（即，在一定的机器配置下才能达到这个指标）
Q3：AOF方式，是即时写入吗？还是按一定的时间间隔写入（比如间隔10秒写入）？还是按照一定的数据数量写入（比如每100条数据写入）？
Q4：Redis的同类产品有哪些？
Q5：Redis经常受黑客攻击吗？
Q6：记得Redis有一个GUI客户端，需要安装此客户端吗？
Q7：Redis中选定一个数据库后，一直往里面添加数据，会溢出吗？如果会溢出，溢出后怎么处理？是存到下一个数据库吗？</div>2023-04-19</li><br/><li><img src="" width="30px"><span>Geek9469</span> 👍（0） 💬（2）<div>有遇到过redis里面的画像太大，导致redis cpu经常告警的吗？</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/60/ecdb8ff9.jpg" width="30px"><span>云中君</span> 👍（4） 💬（0）<div>好着急…</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（1） 💬（0）<div>Mac（intel CPU）安装 Redis 可以看下这个：https:&#47;&#47;blog.csdn.net&#47;realize_dream&#47;article&#47;details&#47;106227622</div>2023-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>这个Redis和上一节的MongoDB其实能合成一个章节的。</div>2023-12-11</li><br/><li><img src="" width="30px"><span>Geek9469</span> 👍（0） 💬（0）<div>有遇到过redis里面的画像太大，导致读取的时候经常告警的吗？或者是你们的redis里面一般都存什么数据？有用L1本地缓存解决不？</div>2023-05-19</li><br/><li><img src="" width="30px"><span>Geek9469</span> 👍（0） 💬（0）<div>有遇到过redis 里面的画像太大，读取的时候，导致经常告警的吗？</div>2023-05-19</li><br/>
</ul>