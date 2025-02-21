在前面的文章中，我介绍过GUI自动化测试的页面对象模型和业务流程封装等相关知识，也提到过大型全球化电商网站的GUI自动化测试，那如何把已经学到的GUI测试理论知识用到大型全球化电商网站的测试中呢？

今天，我的分享就从“实战”这个角度展开，带你看看实际的大型全球化电商网站的GUI自动化测试如何开展。这场实战，我将从以下两个方面展开：

1. 测试策略如何设计？这一点，我会根据亲身经历的实际项目，和你探讨GUI测试的分层测试策略。
2. 测试用例脚本如何组织？需要注意的是，对于这个问题，我不是要和你讨论测试用例的管理，而是要讨论测试用脚本的管理。比如，当需要组装上层的端到端（E2E）测试时，如何才能最大程度地重用已有的页面对象以及业务流程（business flow）。

如果你所在的企业或者项目正在大规模开展GUI测试，并且准备使用页面对象模型以及业务流程封装等最佳实践的话，那么，你很可能会遇到本文所描述的问题并且迫切需要相应的解决办法。

## 大型全球化电商网站的前端模块划分

在正式讨论大型全球化电商网站的GUI自动化测试策略设计之前，我先简单介绍一下电商网站的前端架构，为避免过多的技术细节引起不必要的干扰，我只会概要性地介绍与GUI自动化测试密切相关的部分。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（7） 💬（1）<div>1. 理论上完全符合 Unit &gt; Integration &gt; E2E 的理论模型，而且很好的应用到实践，赞，不知道这套实现的投入产出比如何？目前使用过程中是否出现过什么问题？是否还有可以改进的地方？

2. 对于持续迭代的大型 web 站，看起来这套实现已经被实践验证，可以推广使用，但是目前我们这，有很多简单 web 站的修改需求，正在考虑如何提取共性关键点来推进自动化，不知茹老师在这方面是否有建议？抑或这种情况就不适合自动化……

以上，欢迎沟通交流，公众号「sylan215」</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/05/c3873f46.jpg" width="30px"><span>on the way</span> 👍（2） 💬（1）<div>目前公司还没有实行E2E GUI 测试</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/35/2c56c29c.jpg" width="30px"><span>arthur</span> 👍（23） 💬（0）<div>茹老师您好，我想请教几个问题：
1. 你们团队会写手工测试用例吗？如果写，是怎么写的呢？如果不写，回归测试完全自动化覆盖吗？还是只能熟悉功能的同学进行探索测试？
2. 你们测试团队人员组成是什么样的呢？测试分功能测试组，自动化测试组，E2E组，性能，安全测试组，还是测试组内的人员所有事情都需要做？
3. 你们组内UT是开发做还是测试做？测试会对UT评审或者review吗？覆盖率有强制要求吗？
期待老师解答</div>2018-08-19</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（4） 💬（0）<div>老师你说不偏向于任何语言…但我就看到基于Java的实现方式…请问版本依赖管理在python中如何实现呢</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/cc/50fa3518.jpg" width="30px"><span>hohofugao</span> 👍（3） 💬（0）<div>用pom维护不同案例的依赖关系，但是怎么保证不同案例数据前后一致？比如登陆用户用A，后面注销用户如果数据是B呢</div>2018-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（2） 💬（0）<div>学习文章后，有疑问：是把所有的前端模块各自独立的代码库放在一起就是公共组件的代码库吗？

学习完这篇文章后，了解了GUI自动化测试的总体策略，在自己心目中的GUI自动化测试，就是E2E的GUI自动化测试，按照老师本文所说，还有JavaScript单元测试、前端组件集成测试，是自己之前没了解的。

自己之前做GUI自动化测试工作，上来就直接做端到端的GUI自动化测试，我想这也是做不好的原因之一吧。

JavaScript单元测试、前端组件集成测试，还得另外学习，文中老师没有提到具体的细节。
</div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d9/3b/8c0134be.jpg" width="30px"><span>丹丹兒🍥</span> 👍（2） 💬（0）<div>GUI 的 E2E ，应该可以把平时积累的手工冒烟测试用例转化为自动化测试</div>2018-08-16</li><br/><li><img src="" width="30px"><span>klxiaoqi</span> 👍（2） 💬（0）<div>老师后面可不可以出python示例</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/00/c00ddb9d.jpg" width="30px"><span>Geek_Dream</span> 👍（1） 💬（0）<div>目前所在公司还没有进行E2E GUI测试，看了本小节专栏知识，使我明白了在大型项目中使用GUI自动化测试策略的思维模式，通过模块依赖继承关系，解决模块之间相互依赖的资源组件问题</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（0）<div>1、ebay是优化过的selenium 进行GUI测试还是用UTF？
2、你经常说大型商务网站一天两个版本。这里又说通过版本号来管理。请问一天两个版本有专门的版本号吗？若有，与自动化测试脚本通过版本号管理有关系吗？</div>2018-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/fe/26/feda16aa.jpg" width="30px"><span>Herbert</span> 👍（0） 💬（0）<div>对于大型网站的GUI测试，是如何做分布式GUI测试呢，毕竟测试集很大的时候，肯定是要做分发，多机器测试的。</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（0）<div>学了个新词happy path
这节内容我看了好几遍，但还是不太理解...</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/9f/94128044.jpg" width="30px"><span>lerame</span> 👍（0） 💬（1）<div>老师，可以这么理解吗：模块就是指注册、登录、加入购物车、付费这种。而e2e是指一个用户注册——登录——浏览——加入购物车——付费这一整个流程的任何正向或异常操作？另外，happy path具体怎么理解，是指容易实现的流程路径吗？</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/a7/c4de1048.jpg" width="30px"><span>涅槃Ls</span> 👍（0） 💬（0）<div>打卡19，加油</div>2018-08-14</li><br/>
</ul>