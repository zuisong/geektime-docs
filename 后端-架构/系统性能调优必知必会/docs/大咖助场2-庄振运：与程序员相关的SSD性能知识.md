你好，我是庄振运。我是[《性能工程高手课》](https://time.geekbang.org/column/intro/100041101)的专栏作者，很荣幸受邀来到陶辉老师的专栏做一期分享。今天我们来讲一点SSD相关的性能知识。SSD（Solid State Drive）是硬盘的一种，有时候也叫Flash或者固态硬盘。

最近几年，SSD的发展和演化非常迅速。随着市场规模的增大和技术的进步，SSD的价格也大幅度降低了。在很多实时的后台系统中，SSD几乎已经成了标准配置了。所以了解它的机制和性能，对你的工作会很有益处的。

相对于传统硬盘HDD（Hard Disk Drive），SSD有完全不同的内部工作原理和全新的特性。有些机制不太容易理解，而且根据你工作的领域，需要理解的深度也不一样。所以，我把这节课的内容按照由浅入深的原则分成了三个层次。

第一个层次是关注SSD的外部性能指标；第二个层次是了解它的内部工作机制；第三个层次是设计对SSD友好的应用程序。

## 比HDD更快的硬盘

很多人对传统硬盘了解较多，毕竟这种硬盘在业界用了好几十年了，很多教科书里面都讲述过。所以，对SSD的性能，我先用对比的方式带你看看它们的外部性能指标和特性。

一个硬盘的性能最主要体现在这三个指标：IOPS，带宽/吞吐率和访问延迟。**IOPS** (Input/Output Per Second) ，即每秒钟系统能处理的读写请求数量。**访问延迟**，指的是从发起IO请求到存储系统把IO处理完成的时间间隔。**吞吐率**（Throughput）或者带宽（Bandwidth），衡量的是实际数据传输速率。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/75/6bf38a1e.jpg" width="30px"><span>坤哥</span> 👍（1） 💬（3）<div>老师，不明白就地更新会引起读取-修改-写入过程，随机更新仅仅写入过程。随机更新不会碰到已写的页面吗？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（2）<div>公司目前kafka使用的就是ssd</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（0）<div>老师，你好，文中的就地更新和随机更新怎么区分，不太理解，能不能举个例子</div>2021-11-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/l4nngwyggBGqeMXC0micwO8bM1hSttgQXa1Y5frJSqWa8NibDhia5icwPcHM5wOpV3hfsf0UicDY0ypFqnQ3iarG0T1w/132" width="30px"><span>Trident</span> 👍（0） 💬（0）<div>之前公司采用SSD存储es的热点数据，但是深层次优化没有做</div>2021-05-11</li><br/>
</ul>