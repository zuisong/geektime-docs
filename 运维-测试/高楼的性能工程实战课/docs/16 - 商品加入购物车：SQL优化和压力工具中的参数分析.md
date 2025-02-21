你好，我是高楼。

今天这节课，我用商品加入购物车接口，来给你讲一讲SQL优化和压力工具中的参数分析。

对于SQL的优化，很多人一看到数据库资源使用率高，就猜测是SQL有问题。这个方向看起来没错，但是，具体是哪个SQL有问题，以及有什么样的问题，往往回答不出来。因此，这节课我会教你怎么根据资源使用率高，快速定位到有问题的SQL，并做出相应的调整。此外，你还将看到，当压力工具的参数使用不合理时，我们应该如何处理由此产生的数据库锁的问题。

现在，我们就开始这节课的分析。

## 压力数据

对于商品加入购物车这个接口，我们第一次运行的性能场景结果如下：

![](https://static001.geekbang.org/resource/image/f8/8c/f871d42d3e4528def48fe1202e219a8c.png?wh=1789%2A789)

看着有一种想哭的感觉，有没有？从这张图来看，问题不止一个。我用自己在有限的职业生涯中吸收的天地之灵气，打开天眼一看，感觉这里有两个问题：

- TPS即使在峰值的时候，也不够高，才50左右；
- TPS在峰值的时候，有大量的错误产生。

那哪个问题更重要呢？有人可能说，明显应该处理错误呀，有错误看着不眼晕吗？如果你是有强迫症的人，那没办法，可以先处理错误。

不过，在我看来，先处理TPS不高的问题也是可以的。因为虽然有错误产生，但并不是全错呀，只有5%的错，你着个啥急。

可是，不管怎么着，我们都要走性能分析决策树的思路。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/30/4c/ebe9a2b7.jpg" width="30px"><span>馒头大王</span> 👍（9） 💬（1）<div>根据系统指标现象看问题

一、TPS低&#47;响应耗时长
1、分析链路-推荐skywalking
2、发现service-MySQL耗时较长
3、确定慢SQL
	方法1：MySQL Report-pt-query-digest（解析慢日志）
	方法2：RDS→日志管理
	注：一般伴随着DB CPU高
4、”执行计划“分析慢SQL
	（执行 explain 或 desc  + SQL）
5、添加相关索引
	无法通过索引解决的根据业务优化代码
6、问题解决

二、报错&#47;错误率高
1、查日志
2、具体问题具体分析
	譬如：
	1）参数
	2）主键冲突
	3）超时
	4）服务降级
	~~~~</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9f/0a/611030c3.jpg" width="30px"><span>同心飞翔</span> 👍（3） 💬（3）<div>老师，是否可以推荐个有各种性能问题的开源系统，大家来练手。还是要自己实践</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/f1/6b/a8dae12f.jpg" width="30px"><span>z-Amy</span> 👍（0） 💬（1）<div>老师你好，请问MySQL Report 是什么命令打印出来的？</div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（1）<div>为什么是Cart - MySQL影响最大，看图上才113ms。User - Gateway，Gateway - Cart平均响应时间也很大呀，这块是怎么回事？</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/93/38/efb7eb38.jpg" width="30px"><span>安静。。。</span> 👍（0） 💬（1）<div>2. 你能画出在第二阶段分析中的逻辑吗？
因为错误数量随着请求数量的增加而增加
查看错误的日志，确定代码是在add的时候报错
那么同时请求add的场景，跟实际的场景有关系
实际上可能不会有多个用户同时请求的场景，需要修改压测数据</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e4/e1/d1bf83c9.jpg" width="30px"><span>公瑾</span> 👍（0） 💬（1）<div>老师，慢日志阈值一般设置成多少，100ms左右吗？</div>2021-06-17</li><br/>
</ul>