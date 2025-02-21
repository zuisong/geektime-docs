你好，我是陈皓，网名左耳朵耗子。

在了解了前面几篇文章中提的这些问题以后，我们需要思考一下该怎样解决这些问题。为了解决这些问题，请先允许我来谈谈软件工程的本质。

我认为，一家商业公司的软件工程能力主要体现在三个地方。

**第一，提高服务的SLA。**

所谓服务的SLA，也就是我们能提供多少个9的系统可用性，而每提高一个9的可用性都是对整个系统架构的重新洗礼。在我看来，提高系统的SLA主要表现在两个方面：

- 高可用的系统；
- 自动化的运维。

你可以看一下我在CoolShell上写的《[关于高可用系统](https://coolshell.cn/articles/17459.html)》这篇文章，它主要讲了构建高可用的系统需要使用的分布式系统设计思路。然而这还不够，我们还需要一个高度自动化的运维和管理系统，因为故障是常态，如果没有自动化的故障恢复，就很难提高服务的SLA。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>delete is create</span> 👍（31） 💬（1）<div>耗子哥   这些主流技术是你所在工作中用到的还是下班写写demo学到的呢？</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/e0/3e636955.jpg" width="30px"><span>李博越</span> 👍（23） 💬（1）<div>目前工作在搞这些，不过是用的swarm，估计过两年就会被淘汰吧</div>2018-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ee/2e/9ac22d45.jpg" width="30px"><span>噜啦</span> 👍（4） 💬（1）<div>需要好好品味，刚入paas这个坑，看来还需要修炼啊。
耗叔，你觉得k8s的官方文档和网上的、社区上的讨论哪个更容易让新手对整个k8s+docker的生态有一个了解？
求翻牌</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/c9/90c8a53e.jpg" width="30px"><span>missa</span> 👍（2） 💬（1）<div>耗子叔你在做apm，gateway等的时间，有遇到什么坑，或者做的时候有需要注意的地方，以后的文章中方便讲讲？</div>2018-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（13） 💬（0）<div>知识密度比较大，需要更多时间消化，读起来相当畅快，但实际下手又不知从何下手。这是个大工程，个人感觉只能有个整体认知，需要组织的力量去驱动。</div>2018-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（12） 💬（1）<div>耗子叔能否这一个JVM优化的系列专题，这一块现在网络上虽资源很多，但都不像您这样直达本质的讲法，期待！</div>2018-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（6） 💬（0）<div>IAAS是基础设施，如服务器，网络
paas是软件基础设施，以平台形式对外提供服务，提供软件开发的部署，运维能力，客户只要关注业务软件开发既可。
SAAS是开箱即用的服务，如物流助手，电商网站
典型的，salesforce是paas平台，供不同的ISV去定制提供SAAS服务</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/60/0403b575.jpg" width="30px"><span>林三杠</span> 👍（6） 💬（1）<div>这个系列真是干货啊，信息量巨大。对应的看自己单位的系统，简直千疮百孔，无法直视，在任何一个单点上都没做好，整体就更不用说了。</div>2018-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/fc/d1dd57dd.jpg" width="30px"><span>ipofss</span> 👍（3） 💬（0）<div>我还没接触过分布式，日常开发中没有应用场景，这一系列文章，让我对分布式有了高纬度的理解，然后再去扎进去学单块知识时感觉效果会更好</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/52/97f59d07.jpg" width="30px"><span>。。。。</span> 👍（3） 💬（0）<div>浩哥请教个问题，我看谷歌那篇spanner论文的描述，它完成一个事务的时间大致需要两个truetime api返回的时间误差值，大致可以推导出大概是8毫秒完成一个事务，这种情况下咋应付高并发的读写呢</div>2018-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（2） 💬（0）<div>对消息治理有一定的研究，如何保障消息不丢，消息达到率，消息幂等，server端的高可用部署与架构，server过载防护，发布失败补偿，消费失败重试等</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/81/92d01e3a.jpg" width="30px"><span>Sean</span> 👍（2） 💬（0）<div>openshift怎么样？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/44/1d63fc03.jpg" width="30px"><span>刘宗尧</span> 👍（2） 💬（0）<div>写了服务端的，会不会写一下客户端的架构设计?比如说移动客户端的架构设计?</div>2017-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e1/bb/02f9023b.jpg" width="30px"><span>胡明</span> 👍（2） 💬（0）<div>整个系统的层次模块划分方式有没有经典的书或者论文可以参考啊</div>2017-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6d/41/256f7238.jpg" width="30px"><span>GZC</span> 👍（1） 💬（2）<div>一入分布式系统，不回头，等我开源nodejs版微服务</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a6/3bddb98c.jpg" width="30px"><span>大叶枫</span> 👍（1） 💬（0）<div>读了好几遍，信息量很大，影响巨大。再核对思考下提问题。</div>2018-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>不知道有没有人注意到，专栏的这一篇，增加了一位作者。

高可用系统需要自动化的运维和管理。

软件生产流水线 + 运维自动化，仅这两条，估计就难倒了国内大部分的开发团队。

PaaS：服务化、分布式、自动化

如果一个运营级CA，是否可以考虑做成 PaaS 平台？

专栏提供的这个 PaaS 平台总体架构，估计可以复用到很多项目中去。</div>2023-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/b5/137f25a9.jpg" width="30px"><span>kkllor</span> 👍（0） 💬（0）<div>太干了，每一篇都需要深入了解总结</div>2023-03-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/gGOGcSH4AcC6iaeVcibEsuKdkRMPWia5G1OQY9Bm5n9pR7HFWEmtWeK9S3RhibDf8ePibx7RsCRl2Ng6MOPL0ry9vHA/132" width="30px"><span>Geek_71d8b8</span> 👍（0） 💬（0）<div>分布式系统是一整套浩大的工程，就像是在建造一座摩天大厦</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/a7/b8eadbdc.jpg" width="30px"><span>郭子</span> 👍（0） 💬（0）<div>细节都是魔鬼👹，谢谢您的专栏。我学到了很多</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（0）<div>第二遍看～记得第一遍时看的云里雾里，不知道在讲什么，额外补了其他的知识，现在感觉好一些了～</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/d5/73c75eb3.jpg" width="30px"><span>夜行观星</span> 👍（0） 💬（0）<div>比较喜欢看旧文，随着时间的沉淀，可以看到哪些是真干货，一滴水都没有的</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/f5/6cdbfa90.jpg" width="30px"><span>刘匿名</span> 👍（0） 💬（0）<div>很多部分的知识只是有所了解，作为业务方的开发很多底层实现和架构都被运维部门隐藏了，只能主动多学多问了</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f1/12/7dac30d6.jpg" width="30px"><span>你为啥那么牛</span> 👍（0） 💬（0）<div>就从这三张图来说，就甩出平常公司几条街。一些公司，只是表达了我有什么，而不说我怎么用</div>2020-08-02</li><br/><li><img src="" width="30px"><span>Geek_130e9e</span> 👍（0） 💬（0）<div>此节信息量巨大，干货满满啊。只有组织的力量才能驱动Paas大工程。k8s是赢家，docker官网支持，Swarm肯定被淘汰。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/86/20/ee7d32e0.jpg" width="30px"><span>许光伟</span> 👍（0） 💬（0）<div>之前一直在用，今天终于高纬度了解了下，受益匪浅</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/bb/7afd6824.jpg" width="30px"><span>闫冬</span> 👍（0） 💬（0）<div>运维自动化
开发流水化
模块复用化
系统高可用
</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/37/4b12b4cc.jpg" width="30px"><span>ZYCHD(子玉)</span> 👍（0） 💬（0）<div>有所收获，还要再看几遍</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/8f/ad6039b6.jpg" width="30px"><span>沫沫（美丽人生）</span> 👍（0） 💬（0）<div>老师好，能否把PaaS专门作为一个课程来讲讲呢，现在很多SaaS公司都在向PaaS转型。</div>2020-01-05</li><br/><li><img src="" width="30px"><span>Geek_110</span> 👍（0） 💬（0）<div>为什么服务编排也放在paas调度上呢。服务编排不是根据业务进行编排么，还有服务调度不是就保护服务的scale为什么还要加上服务伸缩呢</div>2019-12-27</li><br/>
</ul>