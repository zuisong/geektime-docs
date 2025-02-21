写这篇文章的时候，我想起来一句似乎无关紧要的话：“我离你如此之近，你却对我视而不见。”

在性能测试中，参数化数据是少有的每个性能测试工程师都会用得到，却经常出现问题的技术点之一。从我的角度来说，究其原因，大部分是因为对性能参数化数据的理解不足。导致的结果就是用了参数化，但和真实的用户场景不一致，从而使得整个性能测试场景都失去了意义。

这样的例子不在少数。

一个项目开始之初，由于没有历史沉淀的数据，所以我们需要造一些数据来做性能测试。造多少呢？并不是按未来生产的容量来造，而是按性能场景中需要的数据量级来造。这种错误的做法是很多项目中真实出现的事情。

这并不止是性能测试工程师之过，还有很多其他的复杂原因，比如时间不够；经验不足，只能造重复的数据等等。

那么性能测试参数化数据的获取逻辑到底是什么呢？我们来看一个图吧。

![](https://static001.geekbang.org/resource/image/6b/ca/6bc265c84949230ec7f028e2de3fa1ca.jpg?wh=1476%2A396)

在这个图中，我用不同的颜色表示不同组件中的数据。压力工具中的参数化数据有两种，这一点，我们前面有提到过，参数化数据有两大类型：

1. 用户输入的数据同时在后台数据库中已存在。
2. 用户输入的数据同时在后台数据库中不存在。

当我们使用数据库中已存在的数据时，就必须考虑到这个数据是否符合真实用户场景中的数据分布。当我们使用数据库中不存在的数据时，就必须考虑输入是否符合真实用户的输入。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/02/e0/5e11188d.jpg" width="30px"><span>坚持半途而废</span> 👍（5） 💬（2）<div>这个问题，我们一般是查日志，多执行几次，看看是不是同样的时间段波动。把响应时间长的流水打印出来，看日志主要时间消耗在哪，定位是应用还是数据库问题。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（1） 💬（1）<div>经常通过tcpdump抓包了，不过老师这次抓的包，竟然能分析出db慢，太强了</div>2020-04-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUHvicvia3fpBfsNh78uuUIhsLyrk0AwSN1Dau7pR3hrEsERANT6UyrSd3gIBVyQibD2nPRzkibJLxibA/132" width="30px"><span>Geek_8e5c47</span> 👍（1） 💬（1）<div>数据分布和生产不一致，压出来性能结果很难预估生产真实性能的情形</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/85/e2/540b91fa.jpg" width="30px"><span>凯耐</span> 👍（0） 💬（1）<div>亲身经历造的数据有问题导致TPS突然下降（一个用户下面造了1w多张不符合业务场景的数据，导致优惠券查询列表接口rt特别慢），切记造的数据一定要符合生产环境的业务场景</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/24/73/91ef894b.jpg" width="30px"><span>kaixin</span> 👍（0） 💬（1）<div>老师，第一张图应用服务器查看top 时，一共120任务，119sleep 不用管吗？</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（0） 💬（1）<div>抓包就只会用fillder，拿到接口基本数据，但是老师我还是不明白为什么抓包可以判断出响应时间？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/36/fc9e80c4.jpg" width="30px"><span>啊啊</span> 👍（0） 💬（2）<div>现在我只能看到压测工具上的响应时间，如果链路较长，通过什么手段可以准确麻烦每个链路的响应时间？
目前做法:可以从最后面的链路一层层压上来，再计算每一层的响应时间。有没有其他的监控工具可以直接把每一层的时间拿到？</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>最好可以从线上釆集测试数据</div>2020-03-25</li><br/>
</ul>