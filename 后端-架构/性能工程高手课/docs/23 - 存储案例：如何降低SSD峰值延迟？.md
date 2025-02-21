你好，我是庄振运。

我们之前讲过，存储系统的性能很关键（参见[第17讲](https://time.geekbang.org/column/article/185154)）。我们这一讲就探讨存储方面的优化案例，是关于SSD性能的。

现在很多公司里面的高性能存储系统，一般都是基于SSD的，这主要归功于SSD价格在近几年的大幅度下降。但是，SSD也不是包治百病的灵丹妙药，也有自己的特殊性能问题。我们今天就重点讲述两点：**SSD的损耗**和**IO访问延迟偶尔过大**的问题。

这里的第二个问题可能听起来很让人吃惊：不是说SSD延迟很低吗？

一般情况下，是的。但是特殊情况下就不一定了，这个就说来话长了，它和SSD的内部原理有关。我们会一步步地探讨问题形成的原因和解决的策略。

## SSD为什么会损耗？

我们的[第17讲](https://time.geekbang.org/column/article/185154)是关于存储系统的，讲过SSD的工作原理和性能。为了防止你忘记，我们就在这里快速地回顾一下其中的一个重要概念：**写入放大**。

什么是写入放大呢？当写入SSD的物理数据量，大于应用程序打算写入SSD的逻辑数据量时，就会造成“写入放大”。

如果是传统硬盘HDD，就不会有写入放大的问题。那么SSD为什么会有写入放大呢？这是因为SSD内部的工作原理和硬盘很不一样。

我们知道，HDD是可以直接写入覆盖的。和HDD不同，SSD里面的页面只能写入一次，要重写的话，必须先回收擦除，而且只能在“块”这个级别进行擦除。因此呢，SSD内部就需要不断地移动所存储的数据，来清空需要回收的块。也就是说，SSD内部需要进行块级别的“垃圾回收”。垃圾收集器必须有效地在SSD内部不断地回收块，回收以前使用的页面空间，然后才能在这个块上写入新数据。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/ce/80/f9f950f1.jpg" width="30px"><span>张翠山</span> 👍（0） 💬（1）<div>怎么确认目前系统用的是SSD</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（2）<div>如果在很短时间内写到 SSD 太多数据，就会导致 SSD 损耗太快，有可能过早烧坏 SSD。

请问老师SSD是怎么存储数据的？为什么说在很短的时间内写入到SSD太多数据，就会导致SSD损耗太快，有可能过早烧坏SSD？</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>现在很多都是用的云服务器了，不知道云厂商是怎么来调优的。
我们在使用云服务器的过程中，如果遇到了ssd的间歇性性能问题，有什么好办法来判断是自身程序的问题还是云服务器的问题呢？

之前在使用某云时，遇到过写入一个3M的日志，耗时2分多钟的情况，整个进程就租塞住了。
好在当时是有时间戳，知道是卡在写日志了。</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/9f/71345740.jpg" width="30px"><span>黑崽</span> 👍（0） 💬（1）<div>fstrim挂起之后，有办法干预吗？</div>2020-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/47/ca2d9e0e.jpg" width="30px"><span>logo3755</span> 👍（0） 💬（0）<div>老师，那如果ssd做raid以后是不是可以理解为增加了ssd的io周期呢？那raid模式（例如：0-10）会对trim的优化有影响么？</div>2020-08-30</li><br/>
</ul>