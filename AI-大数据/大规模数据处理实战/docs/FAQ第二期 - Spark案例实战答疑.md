你好，我是蔡元楠。

这里是第二期答疑，上周我们结束了Spark部分的内容，时隔一周，我们的Spark案例实战答疑终于上线了。

通过10讲的Spark学习，相信你已经对Spark的基本特性有了深入的了解，也基本掌握了如何使用各类常用API，如RDD、DataSet/DataFrame、Spark Streaming和Structured Streaming。今天我将针对模块三中提出的一些共性留言做一个集中答疑。

我首先要为积极留言的同学们点个赞，感谢同学们亲自动手实践，有的同学还通过查阅官方API文档的形式找出了正确的实现方式，这非常值得鼓励。

## 第18讲

![](https://static001.geekbang.org/resource/image/87/81/871a0e71b4bc152a33bc4429b1ce1881.jpg?wh=1125%2A1228)

在第18讲中，kylin同学留言问到，为什么用我们通篇用的是DataFrame API而不是DataSet。这是因为PySpark的SQL库只有DataFrame，并没有DataSet。不过在Scala和Java中，DataSet已经成为了统一的SQL入口。

![](https://static001.geekbang.org/resource/image/f0/2d/f02f83eb7122e419a80467465d7f4f2d.jpg?wh=1125%2A1144)

斯盖丸同学问道，第18讲代码中groupBy(‘value’)中value是什么意思？

这里我说一下，SparkSession.read.text()读取文件后生成的DataFrame只有一列，它的默认名字就是“value”。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（4） 💬（0）<div>老师,请教个问题:
1.spark多表做join,表里的数据都要加载到内存的吗?
2.假设都是上亿条数据,每张表有500+字段;导致内存不足,除了硬件角度处理,代码角度能否解决?</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/34/f41d73a4.jpg" width="30px"><span>王盛武</span> 👍（2） 💬（0）<div>想听老师讲讲storm与其它大数据框架的差异</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/79/d55044ac.jpg" width="30px"><span>coder</span> 👍（1） 💬（0）<div>老师，再问两个问题：
1、&gt; PySpark 现在不支持 DataSet，只有 Scala 和 Java 支持。这是由语言特性决定的，Python 是动态类型的语言，而 DataSet 是强类型的，要求在编译时检测类型安全。所以，在所有用 Python 的代码例子中，我用的都是 DataFrame。

怎么理解动态类型的语言不支持强类型的数据结构，编译时检测类型安全都在检测类型哪些方面的安全性？强类型和弱类型这种概念出现了很多次，但是一直不理解它们的含义，怎么从编译原理的角度去理解强类型和弱类型？

2、流数据确实是无边界的，所以它们算出来的结果背后应该会有一套概率理论模型做支撑，准确说应该是一套基于局部时间窗口和全局数据概率统计模型的。也就是说我想得到最大值，这个最大值往往是局部时间窗口的，但是我如果想得到全局的最大值，岂不是要从流数据的源头就开始统计？
基于局部时间窗口算出来的一般不是最准确的，那么对于那些需要非常精确处理结果的应用场景，流处理框架是不是就不适用了，或者需要结合其它技术来完善？
流数据框架在哪些场景中是不适用的？</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/51/7773d421.jpg" width="30px"><span>FengX</span> 👍（1） 💬（0）<div>^_^谢谢老师答疑解惑</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（0）<div>多谢老师的答疑</div>2019-06-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/HGP7ltMMgX6RtZa1SEe9epzjtiaiaDN9pkjdrPy9LwvBTH8I0VELzEqEUMib3CgWuZPvMJ3MOB7KedVkXvpCGgILQ/132" width="30px"><span>Geek_f89209</span> 👍（0） 💬（1）<div>老是，能介绍一下pyspark处理hbase数据源的方案吗，happybase虽然流行，但限制很多，无法批量按照每个row特定的前缀过滤数据？我们目前的方案是用java原生这个处理hbase的进程，用py4j和这个进程通信</div>2019-06-14</li><br/>
</ul>