你好，我是鸟窝，一位沉浸于编程世界20余年的 hacker。在公司内同级别的程序员早就不写代码了，可是我依然奋战在编程的第一线，是部门内同级别编码最多的人。

我也是你们的老朋友了，很久以前我研究Scala的时候出过一本书《Scala集合编程手册》，几年前我在极客时间出过[《Go 并发编程实战课》](https://time.geekbang.org/column/intro/100061801?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search&tab=catalog)的专栏，去年的时候也基于这个专栏出版了《深入理解Go并发编程》一书，承蒙厚爱，这两本书也在我们的台湾岛出版了繁体版。

与其说多年的编程经验给了我更多的写作经验，还不如说我可能更善于将开发编程的经验进行挖掘、整理和总结，能够更加系统和全面地介绍某一个垂直方向的知识，让你理解、贯通、深入、全面地掌握和巩固某个方面的知识点。《Scala集合编程手册》是针对Scala集合类的全面介绍，《Go并发编程实战课》是对Go并发编程深入且全面的剖析，而今天这门课程，是对Rust并发编程的一次全面介绍。

未来，我还有更宏大的计划，想推出C/C++并发编程、Python并发编程、 Zig并发编程等姊妹篇，让学习各种编程语言的同学没有编程的困惑，我提前整理好相应的学习资料，你只需买杯奶茶轻轻松松地学习即可。

## 并发编程的本质与挑战

在我看来，并发编程的本质是**如何有效地管理和协调多个执行单元（例如线程、协程）共享的资源，以实现高效的程序执行**。并发编程的挑战在于两点：如何避免数据竞争、死锁、活锁等问题，同时最大程度地利用硬件资源，提高程序的性能。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/34/b0/8d14a2a1.jpg" width="30px"><span>大布丁</span> 👍（0） 💬（1）<div>支持！</div>2025-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7a/73/f221efee.jpg" width="30px"><span>Porter Zhang</span> 👍（0） 💬（1）<div>老师能给一些并发环境下写rust单测的例子吗，如果有的话，这块比较碎片化，所以想看看老师平时怎么做的。</div>2025-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2giaUb5iczia7HciagrnDoo4hSSZKFQT0VXKyjE9eBb2FzBGvD2qoU0icS3WYRvN15BM6iaicW9cOTmewDHrDvFPIIcLQ/132" width="30px"><span>Shopman</span> 👍（0） 💬（1）<div>统计单元测试覆盖率很不方便系统范围内缺少单测的执行顺序功能给测试环准备带来了不方便，pprof支持不如golang，并发代码的基准测试也不方便，希望老师在后面提一嘴</div>2025-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/89/34/cd862ef6.jpg" width="30px"><span>Vincent_Li</span> 👍（0） 💬（1）<div>惊喜，前几天还在看老师的Rust并发编程文档。这会已经上新了课程</div>2025-02-16</li><br/>
</ul>