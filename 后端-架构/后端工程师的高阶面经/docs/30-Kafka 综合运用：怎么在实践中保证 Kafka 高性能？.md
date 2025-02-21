你好，我是大明。今天我们来聊 Kafka 的最后一个话题——怎么在实践中保证 Kafka 高性能？也可以说，怎么在业务里面优化使用 Kafka 的性能。

在前面微服务部分，我就说高并发可遇不可求，而高可用和高性能是可求的。在追求高性能的时候，Kafka 自然也是一个绕不开的环节。那么今天这节课我就带你深入讨论怎么优化发送者和 broker，结合消息积压中优化消费者性能的知识，你就掌握了一条消息从生产出来到消费完成整个环节上优化性能的方法。

## 如何选择压缩算法？

不管是 Kafka 还是别的中间件，你在选择压缩算法的时候，首先要考虑的就是压缩比和压缩速率。压缩比主要是为了节省网络带宽和磁盘存储空间，而压缩速率主要影响吞吐量。

一般来说，压缩比越高，压缩速率越低；压缩比越低，压缩速率越高。

![图片](https://static001.geekbang.org/resource/image/40/7f/408fc97ddb65b6059b83213f0402897f.png?wh=1920x825)

所以选择压缩算法就是看自己的业务场景究竟是偏向压缩比还是偏向压缩速率。不过在真实环境下，一切都要以性能测试为准，而不能仅仅依赖于原理分析。

## 操作系统交换区

在现代操作系统中，基本都支持交换区，也叫做 swap 分区。当操作系统发现可用的物理内存不足的时候，就会把物理内存里的一部分页淘汰出来，放到磁盘上，也就是放到 swap 分区。

![图片](https://static001.geekbang.org/resource/image/71/e8/71475610yye35c73c46222147911b3e8.png?wh=1920x703)

你也可以把 swap 分区看作是“虚拟内存”。那么你可以想到，如果触发了这种交换，性能就会显著下降。交换越频繁，下降越快。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="" width="30px"><span>kai</span> 👍（3） 💬（1）<div>请问一下老师：

问题1：这几个参数的修改是指修改 linux 系统的参数吗？
net.core.rmem_default 和 net.core.wmem_default：Socket 默认读写缓冲区大小。
net.core.rmem_max 和 net.core.wmem_max：Socket 最大读写缓冲区。
net.ipv4.tcp_wmem 和 net.ipv4.tcp_rmem：TCP 读写缓冲区。它们的值由空格分隔的最小值、默认值、最大值组成。可以考虑调整为 4KB、64KB 和 2MB。

问题2：
Kafka 客户端 receive.buffer.bytes 也是修改 TCP receive buffer 的值，请问一下这个参数的修改和上述 linux 系统的修改是什么关系呢？

谢谢老师</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/02/8863cb1b.jpg" width="30px"><span>王韬</span> 👍（1） 💬（1）<div>优化主从那里，如果acks设置为all的话，是不是这两部分是不是相反的影响啊？</div>2024-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/44/cf/791d0f5e.jpg" width="30px"><span>ZhiguoXue_IT</span> 👍（1） 💬（1）<div>请教一下， 优化jvm，g1性能好只是因为g1的垃圾回收算法，多cms标记整理吗，还有哪些点呢</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：缓冲池太小为什么会阻塞发送者？
文中有这样一句话：“发送者被阻塞也可能是因为缓冲池太小”，缓冲池小，很快就会装满，就可以发送，这样发送速度更快啊。缓冲池大才会阻塞发送者吧。
Q2：atime禁用怎么理解？
不让kafka使用文件的atime属性？还是从操作系统层面上禁止给忘记设置atime属性？
Q3：Redis性能和TCP参数有关吗？</div>2023-08-25</li><br/>
</ul>