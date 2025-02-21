今天我们要讲的大数据公司叫作Confluent，这个公司是前LinkedIn员工出来后联合创办的，而创业的基础是一款叫作Apache Kafka的开源软件。

在整个Hadoop的生态圈里，Kafka是一款非常特殊的软件。它由LinkedIn于2011年开源，并在2012年底从阿帕奇孵化器里面毕业，正式成为阿帕奇的顶级项目。

Kafka和其他的大数据平台都不同，它的主要目的不是数据的存储或者处理，而是用来做数据交换的。要更好地理解它是干什么的，我先谈一下数据库的日志文件。

数据库系统需要保证数据的稳定性，为了确保修改的数据能够写入库，通常会在更改数据之前先在磁盘里写一条日志文件，大致上的格式是“时间戳：做了什么操作”。如果此后因为故障导致数据本身没有被更改，系统可以根据日志文件一条一条地重新执行操作，让数据恢复到应该恢复的状态。

后来有人意识到，这个日志的恢复功能还可以充当数据复制。简单来说，如果两个数据库的初始状态相同，又按照同样的顺序执行了一系列操作，那么最后的状态也相同...
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>天舟</span> 👍（3） 💬（1）<div>大部分企业都不可能只有一个数据源，当然谷歌这样的企业除外。—为什么谷歌这样的企业除外？</div>2018-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（2） 💬（0）<div>明明是一个消息交互的中间件，硬生生的玩成了一个可以支持流计算的大数据平台!</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/32/800a2bfd.jpg" width="30px"><span>安乐天</span> 👍（2） 💬（0）<div>慢慢来好文章是需要时间的</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（0） 💬（0）<div>kafka有好多课程了，本文可谓抛砖引玉</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/f9/f1074095.jpg" width="30px"><span>天华</span> 👍（0） 💬（0）<div>徐老师，能讲一讲Freewheel企业吗？</div>2018-06-24</li><br/>
</ul>