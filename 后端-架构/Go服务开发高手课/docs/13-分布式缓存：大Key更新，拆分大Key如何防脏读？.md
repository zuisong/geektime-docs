你好，我是徐逸。

在上一节课中，我们深入探讨了如何应对Redis中的热Key问题，并掌握了多种解决方案。然而，在面对高并发的挑战时，我们不仅要关注热Key问题，还必须关注另一个可能影响Redis性能的因素——大Key问题。

今天这节课，我们就来聊聊Redis大Key问题和相应的解决方案。

## 什么是大Key问题

Redis 作为单线程应用程序，它的请求处理模式类似排队系统，就像下面的图一样，所有请求只能依序逐个处理。一旦处于队列前面的请求处理时间过长，后续请求的等待时间就会被迫延长。

![](https://static001.geekbang.org/resource/image/30/92/3021ff0023b5b504d877f3f76ee2fc92.jpg?wh=3242x872 "图1 Redis 请求排队处理")

在请求处理过程中，若涉及的键（Key）或键关联的值（Value）数据量过大，Redis 针对这个请求的 I/O 操作耗时以及整体处理时间都将显著增加。

**倘若这种情况频繁发生，不仅Redis的吞吐会下降，而且大量后续请求都会因长时间得不到响应，而导致延迟上涨，甚至引发超时。在实际应用场景中，这种现象被定义为 “大 Key 问题”，而那些数据量过大的键（Key）与值（Value）则被称为 “大 Key”**。

当然，要判断什么是“大Key”，我们得综合考虑两个因素：**Key的大小和Key中包含的成员数量**。

不过，对于 Key 究竟要达到多大规模或者包含的成员数量具体为多少才能够被认定为大 Key，实际上并没有一个统一的标准，这个标准得根据你的Redis配置来定。接下来，我给你分享一些[阿里云](https://www.alibabacloud.com/help/zh/tair/user-guide/identify-and-handle-large-keys-and-hotkeys)提供的关于大Key的参考标准，这些标准可以作为你判断和处理大Key问题的参考。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/19/fe/d31344db.jpg" width="30px"><span>lJ</span> 👍（1） 💬（1）<div>1. 《阿里云》文档提到了四点，对大Key进行拆分、对大Key进行清理、监控实例的内存水位、对过期数据进行定期清理。
2. 提前规划数据结构，从系统设计阶段开始优化数据结构，避免产生大 Key。
3. 为大 Key 设置合理的过期时间，确保无用数据及时清理。
4. 将数据分片存储到多个 Redis 实例中，避免单个实例中的大 Key 问题。
5. 避免直接删除大 Key，通过异步任务分批删除其数据，减少阻塞。通过 UNLINK 命令替代 DEL。</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/a0/085f8747.jpg" width="30px"><span>『WJ』</span> 👍（0） 💬（1）<div>你这里大Key 的判断标准和阿里云写的不一样，5M和500M来说大太多了，是不是弄错了</div>2025-01-06</li><br/>
</ul>