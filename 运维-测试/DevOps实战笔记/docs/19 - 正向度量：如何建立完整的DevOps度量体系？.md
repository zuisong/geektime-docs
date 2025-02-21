你好，我是石雪峰。到今天为止，我用14讲的篇幅给你通盘梳理了DevOps的工程实践，基本涵盖了工程实践的方方面面。但是，就像那句经典的“不仅要低头看路，还要抬头看天”说的一样，我们花了这么大的力气投入工程实践的建设，结果是不是符合我们的预期呢？

所以，在工程实践的最后两讲，我想跟你聊聊度量和持续改进的话题，今天先来看看DevOps的度量体系。

我相信，对于每个公司来说，度量都是必不可少的实践，也是管理层最重视的实践。在实施度量的时候，很多人都把管理学大师爱德华·戴明博士的“If you can’t measure it, you can’t manage it”奉为实践圭臬。

但是，回过头来想想，有多少度量指标是为了度量而度量的？花了好大力气度量出来的数据会有人看吗？度量想要解决的，到底是什么问题呢？

所以，**度量不是目的，而是手段，也就是说度量的目标是“做正确的事”，而度量的手段是“正确地做事”**。

那么，什么才是度量领域正确的事情呢？如果想要弄清楚DevOps中的度量长什么样子，关键就是要回到**DevOps对于软件交付的核心诉求**上。

简而言之，对于IT交付来说，DevOps希望做到的就是**持续、快速和高质量的价值交付**。价值可以是一个功能特性，可以是用户体验的提升，也可以是修复阻塞用户的缺陷。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（6） 💬（1）<div>    正向管理：觉得老师今天的课程就是在讲项目管理。&lt;落地实践篇&gt;开始就明显的感觉到了，故而在老师开始的其实就去补充了其相关的课程强化自身。
    老师的今天的课程中这块其实完全体现了DevOps其实就是一个项目一个产品：想有效发挥DevOps就必须让其贯穿整个过程，早期的进销存去替换全手工记账同样如此。做好一个DevOps可以大幅提升软件内部的效率，就像上次DevOps大会时网易的于旭东曾经做的分享更让我感受到这点。
     软件是一把双刃剑，诸多的关键环节同样如此：用好了大幅提升效率，过于刻板的为了规范而规范，可能受伤害的不只是软件本身，而是整个企业。谢谢老师今天的分享，期待后续的课程。</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（5） 💬（2）<div>老师您好，在统计指标的时候我们一般会以人的纬度或者以部门的纬度来进行统计，比如会统计一个部门的前置时间，一个小组的前置时间，一个人的前置时间。那我们在做系统设计时这些数据是如何与组织架构关联呢，特别是这个人在组织机构中产生了变化又如何保证数据的准确呢？</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（1）<div>关于数据的准确性这段时间很有感触。公司今年新上了一个缺陷管理系统，用来替换原先的老系统。新系统功能和使用习惯和老系统差异很大，大家都很不习惯，经常出现代码已经部署到生产环境了，但是对应的ticket还是显示正在开发的状态。我的应对方式是，一看到错误就追踪落实到个人，确保他意识到问题出在哪里，我们制定的新规则是什么，还有也要解释为什么我们制定这样的规则（我觉得规则的制定还是要以效率为准，没缘由的规则自己都说服不了自己，更不要想着让别人遵守）。然后总结一些常见的问题，以checklist的形式附加给所有程序员，作为提醒。感觉现在的自己就像个老母亲，一遍又一遍教导纠错，心累…</div>2019-12-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJYRZy0TDUsnolSVgRgRNiamraQiby8bpicAXno0CWC3WicftyRDt9QacLQzPhicBTd055yjMKW4Lbuf0w/132" width="30px"><span>Geek_nai6tk</span> 👍（1） 💬（1）<div>老师您好，当前业界有比较流行好用的度量平台的开源工具或者开源框架吗？</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（1） 💬（1）<div>请问老师“交付吞吐量”是否可以辅助团队敏捷开发时设置每个冲刺的任务点数？避免出现工作量闲置或者产生过多挤压？</div>2019-11-23</li><br/><li><img src="" width="30px"><span>工画师</span> 👍（1） 💬（1）<div>感谢老师的分享，对于我们正在建设DevOps度量指标阶段受益匪浅，还是应该回归本质，宜少不宜多，宜精不宜烂，达成共识，构建多维度视角的可视化，才能使度量变得真正有效。</div>2019-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK134043CpGAlWGcszSme7Zia5Yv4mpj1LltFk0JZiboYU4rD5K0CZeicPUCRbP4rtr6AsyZb6BO8aKw/132" width="30px"><span>倪倪</span> 👍（0） 💬（1）<div>有的需求很大，有的需求很小，那开发前置时间是否就没有意义了</div>2020-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/ce/abb7bfe3.jpg" width="30px"><span>张瑞霞</span> 👍（0） 💬（2）<div>这些指标需要区分阶段嘛？  如开发阶段是在开发环境，测试阶段是在测试环境</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/65/bf57c323.jpg" width="30px"><span>Pyel</span> 👍（0） 💬（0）<div>“度量不是目的，而是手段，也就是说度量的目标是“做正确的事”，而度量的手段是“正确地做事”。”</div>2020-03-29</li><br/>
</ul>