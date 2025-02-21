你好，我是赵成，欢迎回来。

前面几节课，我们按照层层递进的思路，从可用性讲到SLI和SLO，再到SLO所对应的Error Budget策略。掌握了这些内容，也就为我们建设SRE体系打下了一个稳固的基础。

今天，我用一个电商系统的案例，带着你从头开始，一步一步系统性地设定SLO，一方面巩固我们前面所学的内容，另一方面继续和你分享一些我在实践中总结的注意事项。

## 案例背景

我先来给你介绍下电商系统案例的基础情况，框定下我们今天要讨论的内容范围。

一般来说，电商系统一定有一个或几个核心服务，比如要给用户提供商品选择、搜索和购买的服务等。但我们知道，大部分用户并不是上来就购买，而是会有一个访问的过程，他们会先登录，再搜索，然后访问一个或多个商品详情介绍，决定是放到购物车候选，还是选择物流地址后直接下单，最后支付购买。

这条从登录到购买的链路，我们一般称之为系统的**核心链路**（Critical Path），系统或网站就是依靠这样一条访问链路，为用户提供了购买商品的服务能力。

至于电商系统的其它页面或能力，比如网站政策、新手指导、开店指南等等，这些对用户购买服务不会造成太大影响的，相对于核心链路来说，它的重要性就相对低一些。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（8） 💬（1）<div>老师在课程中讲到了生产压测，其实压测同样可以放在测试环境或者非核心业务中去测试；这其实就是结合DevOps方面的知识。之前学习时有被推荐此书，不过精力有限尚未来的及去增加书库。
DevOps&#47;敏捷讲的是突出效果必然要用典型系统：SRE的不少操作完全可以反其道而行之；故而个人意志觉得DevOps和SRE是互补的，如何合理使二者发挥功效这其实是我们一直要努力去探索的。</div>2020-03-30</li><br/><li><img src="" width="30px"><span>自行车</span> 👍（5） 💬（1）<div>很有启发，为公司部署了很多监控系统和告警策略，但是总感觉大部分的告警都是无用的，现在想想就是没有制定明确的slo，感谢老师</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2c/62/94688493.jpg" width="30px"><span>摇滚诗人M</span> 👍（5） 💬（1）<div>游戏（吃鸡）业务：
1.核心链路：登录，玩家组队及匹配，道具购买（非核心链路，但是对公司收益直接影响，故也应保障），进行游戏，游戏结算（经验值等）。
2. 除了valet维度的SLO，还需招募人员，内测游戏中的各种场景下可能出现的bug。（bug budget）
3. 压测，混沌工程同样适合。（特殊节日预演）
</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（3） 💬（2）<div>期待老师分析全链路跟踪的相关实践。😬</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/62/0a4e5831.jpg" width="30px"><span>soong</span> 👍（2） 💬（1）<div>电商类应用，比较明显的限制因素，是像大促活动一类！对于ToB的SaaS类应用，月末、月初的结转、盘点，也是一个相对集中的时间点，对于这些时间点上的保障和策略要非常清晰！</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（1） 💬（1）<div>很难想象现在的传统企业应用运维碰到故障就是重启。</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（1） 💬（1）<div>感觉现在的运营评判标准都是靠个人感觉，也没有SLO，连主线业务都没有确定清晰，搞什么都是东施效颦</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（2） 💬（0）<div>给力，运维需要系统的学习</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（0） 💬（0）<div>我对混沌工程这部分感到困惑。文中提到“对于一个模拟策略上线实施，一定是在一个隔离的环境中经过了大量反复验证，包括异常情况下的恢复预案实施，确保影响可控之后，在经过多方团队评审或验证，才最终在线上实施。”。这样和现有的灾难演练有什么区别呢，现有的灾难演练，就是模拟故障，然后进行抢救，经过几年的模拟，老员工不看手册都能默写有哪些故障。甚至不排查问题都能熟练操作应多措施。但面对未知的突发问题，还是不能应对，依旧存在时长不可控的抢修。
我对这部分感到困惑，我以前以为混动工程就是引入不确定的因素，让内部在混乱中发现问题，不断打补丁完善整体。</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/17/0b5aad57.jpg" width="30px"><span>Marx</span> 👍（0） 💬（0）<div>slo需要区分强弱依赖：
1. 核心应用对非核心应用弱依赖（自动降级）
2. 非核心应用对核心应用弱依赖（可限流）
3. 核心应用对核心应用强依赖（共享错误预算）</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/c9/f83b0109.jpg" width="30px"><span>罗琦</span> 👍（0） 💬（0）<div> “比如下单的 Buy 应用要依赖 Coupon 这个促销应用，我们要求下单成功率的 SLO 要 99.95%，如果 Coupon 只有 99.9%，那很显然，下单成功率是达不成目标的，所以我们就会要求 Coupon 的成功率 SLO 也要达到 99.95% 。”
感觉这里的Coupon的SLO应该要高于99.95%，因为Buy还依赖其他应用，其他应用无法保证100%的话，那么在Coupon不出问题的情况下可能也会导致Buy失败</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>“如何验证核心链路SLO”，觉得改成 “如何验证核心链路SLO保障的有效性” 更合适。下面给了容量压测，混沌工程的实践来检验保障手段的有效性</div>2020-10-26</li><br/>
</ul>