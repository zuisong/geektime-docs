你好，我是蔡元楠。

今天我要与你分享的主题是“横看成岭侧成峰：再战Streaming WordCount”。

在上一讲中，我们学习了Beam窗口（Window）的概念。当时，我们提到窗口技术的产生是因为我们想要根据时间戳去分组处理一个PCollection中的元素。

我们也提到了在“统计莎士比亚文集词频”这个例子中，如果莎士比亚穿越到了现代，成了一名极客时间的专栏作家，我们就可能需要根据他文章的写作时间来统计词频了。

举个具体的例子的话，就是我们能不能灵活地得到莎士比亚在2017年9月使用的高频词汇？或者是他在2018年第7个周五偏爱使用的高频词汇呢？

时效性是数据处理很重要的一部分，类似上面这样的问题还有很多。

比如，能不能根据实时交通数据，得到最近24小时之内拥堵的道路？能不能根据所有微信分享文章的点击数据，得到过去一周最热门的文章？这些问题都是可以用窗口技术来解决。

所以今天这一讲，我们就来看看怎样在WordCount这个例子中使用窗口技术。我会介绍怎样在Beam中实现以下六个问题：

1. 怎样区分有界数据还是无界数据？
2. 怎样读取无边界数据？
3. 怎样给PCollection数据添加时间戳？
4. 怎样在PCollection应用窗口？
5. 怎样复用之前的DoFn和PTransform？
6. 怎样存储无边界数据？
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/70/6411282d.jpg" width="30px"><span>陈</span> 👍（3） 💬（1）<div>老师，窗口的跨度能多大，比如我想计算每天用户访问量？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/21/eb/bb2e7a3b.jpg" width="30px"><span>Ming</span> 👍（1） 💬（2）<div>假如要给一个流处理的pipeline更换计算逻辑的话，在Beam层上要做相应处理吗？还是完全由底层的实现来处理的？

Beam虽好，但是似乎，作为开发首当其冲的还是要熟练掌握一个底层计算框架。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/b5/dd0353f4.jpg" width="30px"><span>三水</span> 👍（1） 💬（1）<div>老师，现在使用 Beam 模型的项目中，使用 Python 语言的多吗？如果用 Python 语言的话，Beam 除了Google的 云 Pub&#47;Sub，还不支持 Kafka 类似的，Built-in I&#47;O Transform 也太少了，这些都需要自己实现吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/a2/f70dae3a.jpg" width="30px"><span>端碗吹水</span> 👍（0） 💬（0）<div>请问老师，假设有个报表需求是实时显示从起始至今所有数据的平均值，那么流处理能否实现这种对开始至今的数据求平均值，如果能的话是不是每次新数据到来都得重算数据</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/3d/93aa82b6.jpg" width="30px"><span>Junjie.M</span> 👍（0） 💬（0）<div>老师请问对于PTransform Runner是DIRECT时可以设置并行度吗</div>2020-04-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（0） 💬（1）<div>无界数据中窗口的时间跨度的选择是否可以从下面这些方面考虑：
1. 业务实时性要求
2. 数据量
比如文章中的统计一个月的高频词和某一周的，那么可以选择窗口长度为一周的固定窗口（常用英文单词是有限的，且莎士比亚一周产出的文章数量也是比较有限的。同时也符合业务上的时间要求），后面再设置一个长度为一个月的窗口，将上一个输出的PCollection结果进行合并。</div>2019-07-10</li><br/>
</ul>