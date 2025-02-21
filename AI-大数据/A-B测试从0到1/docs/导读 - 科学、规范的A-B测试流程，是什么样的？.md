你好，我是博伟。

前面两节课啊，我们花了很大力气去学习做A/B测试的理论前提，这也是为了让你夯实理论基础。不过啊，除非你是统计科班出身，否则我都会推荐你，在学习实战的时候呢，也要不断温习统计篇的内容，把理论与实践结合起来。如果觉得有必要，也可以把我在统计篇讲的统计概念和理论延伸开来，通过查看相关统计专业书籍来加深理解。

学完了统计理论，接下来就要开始设计实现做A/B测试了。不过在我总结A/B测试的流程之前呢，我要简单介绍下在实践中做A/B测试的准备工作，主要有两部分：**数据**和**测试平台**。

一方面，我们要有数据，包括用户在我们产品和业务中的各种行为，营销广告的表现效果等等，以便用来构建指标。因为A/B测试是建立在数据上的分析方法，正如“巧妇难为无米之炊”，没有数据的话，我们就不能通过A/B测试来比较谁好谁坏。

一般来说，只要是公司的数据基础架构做得好，埋点埋得到位的话，基本的常用指标都是可以满足的。

如果说我们要进行的A/B测试的指标比较新、比较特别，或者数据库没有很全面，没有现成的数据可以用来计算相应的指标，那么可以和数据团队进行协商，看能不能在现有的数据中找出可以替代的指标计算方法。

如果找不到相近的替代指标，那么就要和数据工程团队协商，看能不能构建这个数据，可能需要新的埋点，或者从第三方获得。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/5d/e071d7a3.jpg" width="30px"><span>梅不烦</span> 👍（1） 💬（2）<div>老师您的思维导图用的什么软件啊，很美观。我用的那个呈现比较丑😿</div>2020-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b0/da/afd19d47.jpg" width="30px"><span>Marrbor</span> 👍（0） 💬（1）<div>第二步中的bootstrapping 目的是什么？验证AA吗？还是其它？</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/4a/a145c675.jpg" width="30px"><span>张浩_house</span> 👍（0） 💬（1）<div>做AB测试后，是不是需要根据选择的不通流量针对性的埋点了？通常实验是随机分配的流量，在统计指标的时候能够区分哪些统计指标是A实验的效果，哪些指标是B时刻的实验效果？</div>2020-12-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKpXQ37ZYMatZVBib4G4nEF4uBqYg2e3q8AEkokKBdG1rV0UGqvicwL2bXeEoJC3hq0W1eZaaAicZtYg/132" width="30px"><span>18041177287</span> 👍（0） 💬（0）<div>做数据分析统计方面的书籍或课程有推荐的吗？</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b0/da/afd19d47.jpg" width="30px"><span>Marrbor</span> 👍（0） 💬（2）<div>统计学的教程有推荐吗？</div>2021-08-09</li><br/>
</ul>