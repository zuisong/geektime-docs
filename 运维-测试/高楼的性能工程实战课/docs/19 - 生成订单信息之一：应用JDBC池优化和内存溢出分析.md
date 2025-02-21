你好，我是高楼。

在这节课中，我们来看一下生成订单接口的基准场景是什么结果。

你将看到一些重复的问题，比如SQL的问题定位，虽然具体的问题不同，但我们的分析逻辑没有区别，我会简单带过。同时，你也会看到一些新的问题，比如JDBC池增加之后，由于数据量过大导致JVM内存被消耗光；批量业务和实时业务共存导致的锁问题等。这节课，我们重点来看看这样的问题如何进一步优化。

话不多说，开整！

## 场景运行数据

对于生成订单接口，我们第一次试执行性能场景的结果如下：

![](https://static001.geekbang.org/resource/image/dc/6a/dcbed4b3bc53be11f7d18280b8f1d16a.png?wh=1830%2A831)

从场景执行的结果来看。40个压力线程只跑出来50多的TPS，响应时间也蹭蹭蹭地跑了近700ms。这显然是一个非常慢的接口了。

从这样的接口来看，我们选择这个项目算是选择对了，因为到处都是性能问题。

下面我们就来一步步分析一下。

## 架构图

前面我们做过多次描述，画架构图是为了知道分析的路径。所以按照惯例，我们仍然把架构图列在这里。

![](https://static001.geekbang.org/resource/image/89/5f/8973byyed69dec259cb6f7d4bf3f4b5f.png?wh=1215%2A731)

由于这个接口比较复杂，架构图看起来有点乱，我又整了一个简化版本：

![](https://static001.geekbang.org/resource/image/c9/aa/c95c8daab26ca52fb2df688986a1c0aa.png?wh=894%2A736)

Order服务是这个接口的核心，因此，你可以看到我把Order相关的服务都筛选了出来，这样我们就能很清楚地知道它连接了哪些东西。

下面我们来拆分响应时间。

## 拆分响应时间

因为在场景运行的时候，我们看到响应时间比较长，所以我们用APM工具来拆分一下：
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/e4/a8fe6d0d.jpg" width="30px"><span>张东炫</span> 👍（5） 💬（1）<div>1.VM Thread 线程消耗 CPU 高的异常，查看JAVA gc 是否合理
2.innodb_trx表提供了当前innodb引擎内每个事务的信息（只读事务除外），包括当一个事务启动，事务是否在等待一个锁，以及交易正在执行的语句</div>2021-05-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（3） 💬（1）<div>老师你好，查了下资料，bulk_insert_buffer_size是用于myisam存储引擎，我看你的建表sql，是innodb，请确认下呢？</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/35/50a6adc3.jpg" width="30px"><span>阿嬷</span> 👍（0） 💬（1）<div>老师，架构图是用什么画的？</div>2022-02-14</li><br/><li><img src="" width="30px"><span>steve</span> 👍（0） 💬（1）<div>aix服务器的java路径下没找到jstack</div>2021-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（1）<div>1、第二阶段里面
在查看 Order 服务的 top 时，占用cpu最多的是pid 29349 ，为什么后面是jstack -l 1，而不是jstack -l  29349？


2、“当批量业务和实时业务同时出现在同一个数据库中，并且是对同样的表进行操作，这时，你就得考虑一下架构设计是否合理了。”
请问下应该如何设计架构呢？

谢谢</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/33/cdea4bca.jpg" width="30px"><span>zwm</span> 👍（0） 💬（1）<div> 从上图来看，系统资源并没有完全用起来，这个接口显然还有优化的空间

老师这个是怎么看出来的，就通过TPS和响应时间？</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/5e/fa1b9072.jpg" width="30px"><span>Hant</span> 👍（0） 💬（1）<div>高老师，怎么判断GC正不正常呀？</div>2021-06-27</li><br/>
</ul>