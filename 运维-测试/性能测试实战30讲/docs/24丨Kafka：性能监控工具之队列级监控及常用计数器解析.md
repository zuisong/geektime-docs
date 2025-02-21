在我看来队列服务器是最简单的一种组件了。因为队列给我们下手的机会实在是并不多。我们只是用它，如果想改变它就只能去改代码，其他的都只是配置问题。

在当前的市场中，Kafka算是用得非常火的一个队列服务器了，所以今天，我选择它来做一些解读。

虽然我在前面一直在强调分析的思路，但在这一篇中，我打算换个思路，不是像以前那样，直接给你一个结论型的思维导图，而是一起来分析一个组件，让我们看看从哪里下手，来观察一个被分析对象的相关配置。

## 了解Kafka的基本知识

我们先看一下这张图，以便更好地了解一个队列服务器。

![](https://static001.geekbang.org/resource/image/65/87/659043d7a680bd0cb5df070e0ecec687.jpg?wh=1069%2A899)

这是Kafka官网上的一个图。从这个图中可以看到，对Kafka来说，这就像一个典型的集线器。那它里面的结构是什么样子的呢？根据我的理解，我画了一个如下的示意图：

![](https://static001.geekbang.org/resource/image/d5/30/d59231449717009067723332de568130.png?wh=978%2A648)

在这个图中，有三个Broker，也就是三个集群节点。每个消息有一个leader partition，还有两个follower partition。我没有画更多的Producer和Consumer、Consumer Group，是觉得线太多了容易乱。

因为Producer和Consumer肯定会从leader partition中读写数据，而Kafka也保证了leader在不同broker上的均衡，所以Kafka的集群能力很好。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（3） 💬（1）<div>听了这节课 思路清晰了</div>2020-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6Be8vjNk03LEXMl52vONOQvdKTL1MWPR6OsAGEDsHIZXw9FibW8c4YtNL6HAmB8wRkDNIEx15xawJ9PWLW4y1UA/132" width="30px"><span>董飞</span> 👍（2） 💬（2）<div>老师，请教下jmeter测性能时，聚合报告中有一个错误率，具体怎样的请求会被统计成错误？</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/28/8c/c4d33971.jpg" width="30px"><span>GeekS</span> 👍（1） 💬（1）<div>老师，请教下，对于kafka队列这种客户端sdk与服务器对接的应用，用kafka自带性能脚本kafka-producer-perf-test.sh只能做基准性能测试，但是对于多种业务混合场景下的性能测试，有推荐的性能工具吗</div>2020-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er3G5DWFp5PEklibQPYE1m8OxtYqTcryibkcUHpP4ibBicf8OUYHB6V1iaSRaNiaFV8cuNFb0xbOUF7mZhQ/132" width="30px"><span>Duke</span> 👍（1） 💬（1）<div>授人以鱼不如授人以渔！感谢老师，真的受益匪浅</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>还得靠大量的实战经验积累</div>2024-03-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erVRFkhqd8tb8Hq0oFYHd5wfGxROKjg2dOC5KPJicpaSib6BF1cJeR7c7kibvMhdkiazSIygNxTFlaokQ/132" width="30px"><span>Geek_7869f6</span> 👍（0） 💬（1）<div>老师，消息中间件性能测试过程中建议开持久化不？
另外，可以出一期redis性能优化不。</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/71/7c/29f2d5ed.jpg" width="30px"><span>修继伟</span> 👍（0） 💬（1）<div>老师 线程日志里出现大量的 waiting on condition  这个程序会有问题吗</div>2020-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/c3/2c53acd7.jpg" width="30px"><span>雄鹰</span> 👍（0） 💬（1）<div>正好项目组要测试kafka的基准测试，派上用场了，感谢老师o(^o^)o</div>2020-10-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EjMVAocAC3kwH9zWkicAsJ3rFpTwUZFJdPvSs5jYHoOJXktk4AHnlpYgt1arm2gYTmvJqQaQ73MK4QzATNuFFsw/132" width="30px"><span>t6666</span> 👍（0） 💬（1）<div>感觉自己还有很多需要学习，如果是我拿到未知组件应该先去看他的文档然后理清楚运行逻辑然后再分析吧，后面那个，我觉得我还是滚去看书了</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（0） 💬（1）<div>老师打开kafka-exporter 一堆的计数器，怎么确定哪个重要，哪个不重要</div>2020-04-25</li><br/>
</ul>