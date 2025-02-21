你好，我是徐文浩。

上一讲里，我们通过一个简单的统计广告点击率和广告计费的Storm Topology，看到了第一代流式数据处理系统面临的三个核心挑战，分别是：

- 数据的正确性，也就是需要能够保障“正好一次”的数据处理。
- 系统的容错能力，也就是我们不能因为某一台服务器的硬件故障，就丢失掉一部分数据。
- 对于时间窗口的正确处理，也就是能够准确地根据事件时间生成报表，而不是简单地使用进行处理的服务器的本地时间。并且，还需要能够考虑到分布式集群中，数据的传输可能会有延时的情况出现。

这三个能力，在我们之前介绍的Kafka+Storm的组合下，其实是不具备的。当然，我们也看到了，这些问题并不是解决不了，我们也可以在应用层撰写大量的代码，来进行数据去重、状态持久化。但是，一个合理的解决方案，**应该是在流式计算框架层面就解决这些问题**，而不是把这些问题留给应用开发人员。

围绕着这三个核心挑战，在2013年，Google的一篇论文《MillWheel: Fault-Tolerant Stream Processing at Internet Scale》给我们带来了一套解决方案。这个解决方案，在我看来可以算是第二代流式数据处理系统。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（15） 💬（1）<div>徐老师好，在MillWheel中为了保证消息处理至少一次的语义，Computation的每条消息在发送之后都需要应答，收不到应答就会不断重试。String Production的做法是，下游Computation收到消息后存起来，然后立即应答上游的Computation。Weak Production的做法是，不保存消息，不保存消息就必须等整个链路处理完再逐层应答，链路越长，遇到故障的可能性越大，故障会导致消息从头消费，整个系统的延迟就变大了。解决方法就是Computation在发出消息一段时间后收不到应答，就把消息存起来，并应答上游的Computation。这样如果下游链路出问题，只需要从当前的Computation开始重试，而不用从头开始。</div>2021-12-31</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJGg1LEZBInwiaZAEwichicXUTxXCtLw9xwpicftueOJPjrXAuiaAzTsSeib48jiaXZXnAibSHkn9ALjsuGIg/132" width="30px"><span>InfoQ_cdca53d71446</span> 👍（2） 💬（1）<div>&quot;网络传输是乱序的，我们其实并不知道是 X 会先到下游，还是 Y 会先到下游.&quot;
这里有点歧义.  tcp传输已经解决了包乱序的问题.  这里的乱序, 应该是两个并发tcp连接,发送的包谁先到服务端不确定的意思.</div>2022-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eomCrCRrLAWib0gMI2L2NbicMummlxOY6nVmphsDO0J3xx7OygNd8wJicc88RbNoHrcuXBsKLtCMvgFQ/132" width="30px"><span>zart</span> 👍（2） 💬（1）<div>徐老师好，每一个 Computation + Key 的组合，在接收到一条消息的处理过程的第一步，消息去重，使用分段的 BloomFilter 来解决，不是会有小概率的误判，导致非重复的消息也会判断为重复，这样就会导致丢数据。请问会有这种情况么？MillWheel如果允许这种情况就做不到ExactlyOnce了吧</div>2022-01-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epWuRmpg9jWibtRH3mO9I0Sc9Y86fJpiaJDdLia39eib89R1raTkxMg9AOkjb0OTRkmXiaialJgHC5ve59g/132" width="30px"><span>Geek_64affe</span> 👍（1） 💬（0）<div>因为没有Checkpoint，所以只能通过不断重试来确保消息不丢失，并且重试的粒度是整个计算过程，如果计算过程比较深，每一个Computation都需要重新计算，很可能会慢于Checkpoint机制</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（0） 💬（2）<div>不是很明白保存状态和checkpoint的区别是什么，就像文章说的，如果一个computation已经通过timer发送了消息x，按道理如果故障重启后不会有相同时间窗口的消息才对。</div>2022-01-09</li><br/>
</ul>