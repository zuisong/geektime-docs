你好，我是柳胜。

我们前面用了4讲篇幅，讨论ROI模型和由此衍生出来的一套实践原则，从分层测试、选型思路和具体代码多个角度探索提升ROI的方法。

这些方法还都是基于常规的自动化测试开发流程，先有测试需求，再设计测试案例，然后做自动化。以登录测试为例，我画了一张流程图做说明。

![图片](https://static001.geekbang.org/resource/image/e5/82/e524642fdd13d88e63de2900325f5e82.jpg?wh=1920x462)

自动化测试的开发成本，就是把测试需求转变成自动化测试代码这个过程花费的时间。在我们的图里，它是从左向右，所以我管它叫做**水平开发成本**。

![图片](https://static001.geekbang.org/resource/image/5f/98/5fcyy4827fff8970ef6dc39aeb0ca598.jpg?wh=1920x709)

当登录功能测试需求发生变化时，就会重新走一遍这个流程，出现了多个版本的测试需求，也会带来多个版本的自动化测试案例。从下图可见，这个版本是自上向下增加，所以我管它叫做**垂直维护成本**。

![图片](https://static001.geekbang.org/resource/image/ab/e4/ab257d846526c1e731da9812c9cd08e4.jpg?wh=1920x781)

我们现在可以直观地看到开发成本和维护成本了。好，问题来了，有没有办法**从流程上动手术，来降低这两个成本呢**？

这就是我们今天要讲的Automation Generate Automation，也叫自动化产生自动化测试代码，为了方便起见，下面的篇幅用缩写Auto Gen Auto来指代。

## Auto Gen Auto 技术

常规的自动化测试，是指用代码实现设计好的TestCase，而Auto Gen Auto的目的是让Test Case生成也自动化，如下图所示。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5GQZCecntmOibVjWkMWVnibqXEZhAYnFiaRkgfAUGdrQBWzfXjqsYteLee6afDEjvBLBVa5uvtWYTTicwO2jKia0zOw/132" width="30px"><span>Geek_a4cca6</span> 👍（4） 💬（1）<div>我做了5年以上自动化，思路是非常好的，但是在实际实施过程中由于很多的业务线规范并不统一，有的是mardown,有的是openapi规范，所以推动开发设计API规范也是件不容易的事情，目前我的解决方案和老师的思想差不多，我是先定义模板，针对不规划的API设计需要大家把API信息手工录入，然后我再针对模板自动生成脚本用例，回头再套用老师用的公式计算下ROI，相信产出比会很明显，因为我们的设计用例要遍历所有字段异常边界等场景，一个接口下来上百条用例都正常。</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/a9/ee6c8c9d.jpg" width="30px"><span>dakangz</span> 👍（3） 💬（1）<div>大多数小公司都很难落地这么成熟的方案，假如开发都没有单元测试的习惯，这些斗工作太难展开了</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/65/9f/217346ce.jpg" width="30px"><span>清风明月</span> 👍（3） 💬（1）<div>请教一个问题：一般做自动化测试的话，是需要自己写测试覆盖率的工具，还是用开源的？有什么好的思路吗？
最近一直在研究测试覆盖率，之前也用过一些统计测试覆盖率的工具，感觉不是很好用，希望老师能在后期的文章里面讲解 “测试覆盖率的工具”  非常感激！</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d6/09/e9bfe86f.jpg" width="30px"><span>夜歌</span> 👍（2） 💬（1）<div>学了这节课受益匪浅，没想到openapi还可以这么用，真是开拓眼界了。平时老想着自己写代码，以后要多探索探索开发技术，看看能用什么了</div>2022-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw3jpao45frZibQIAicWBfc7ofgrm5gJLiaFQSj5u2DDvkjy3ia5goicJLJlgVtZ0HryiaXb2VqpTSQT5Q/132" width="30px"><span>lisa</span> 👍（1） 💬（1）<div>这块我理解从业务落地的角度来说还不是很成熟，一方面API规范落地成本比较大，可能需要测试团队将测试契约补充完整。其次从投入产出比上，这里可以发一些一些边界的问题，但是后期的维护成本会比较大，不太确定投入产出比怎么样。从自动生成API自动化测试框架代码的角度我觉得可以从垂类业务（根据业务的API类型或者rpc框架）的角度会有收获。
整体来说，我非常赞同这个思路：所有的测试工作即代码。</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e0/e5/91175e2f.jpg" width="30px"><span>北冥</span> 👍（0） 💬（1）<div>老师，如果被测接口需要 前置造数，造数有可能是通过业务接口来造也可能是通过 sql 来造数，那这些前置造数的行为 和 后置清理数据的行为 在用例里怎么设计 才能更好的 达到接口 test case 生成自动化呢</div>2022-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5GQZCecntmOibVjWkMWVnibqXEZhAYnFiaRkgfAUGdrQBWzfXjqsYteLee6afDEjvBLBVa5uvtWYTTicwO2jKia0zOw/132" width="30px"><span>Geek_a4cca6</span> 👍（0） 💬（1）<div>试了下生成go的代码中，没有看到有体现字段的长度定义及边界等信息</div>2022-03-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5GQZCecntmOibVjWkMWVnibqXEZhAYnFiaRkgfAUGdrQBWzfXjqsYteLee6afDEjvBLBVa5uvtWYTTicwO2jKia0zOw/132" width="30px"><span>Geek_a4cca6</span> 👍（0） 💬（1）<div>目前我这边是自己手工写代码去解析的，需要引用需要递归解析，这个库回头也试下看行不，谢谢老师</div>2022-03-31</li><br/><li><img src="" width="30px"><span>woJA1wCgAA3aj6p1ELWENTCq8KX2zC2w</span> 👍（0） 💬（1）<div>意犹未尽，老师快更新</div>2022-03-30</li><br/><li><img src="" width="30px"><span>Geek_1bb348</span> 👍（0） 💬（0）<div>老师您好，用了您提供的user.yaml并没有生成您文中的几个等价测试类。我是需要修改什么配置吗</div>2024-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGXndj5N66z9BL1ic9GibZzWWgoVeWaWTL2XUnCYic7iba2kAEvN9WfjmlXELD5lqt8IJ1P023N5ZWicg/132" width="30px"><span>Geek_f93234</span> 👍（0） 💬（0）<div>柳胜老师讲的真是超级的棒，第一次觉得自动化测试这么的很有意思，自动化测试，不是仅仅当作一份工作</div>2023-09-16</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKubuofHB43wdIwvnWSIdL6YzfGZhic7abWu06ia8BwnMBDCbCFDIF1RQB4nN46Ldv6ALQf025E2mRA/132" width="30px"><span>Geek_palmlan</span> 👍（0） 💬（0）<div>openapi 的spec规范，其实也是一种领域特定的建模语言。也属于开发工作。有没有可能通过大语言模型，输入需求文档，输出符合某个spec的yaml呢？</div>2023-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/a1/4150f41d.jpg" width="30px"><span>杜兴文</span> 👍（0） 💬（0）<div>老师能否分享一下这个解析方案，将这个规则作为我们 Auto Gen Auto 的输入。然后经过加载，解析，最后输出测试案例</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/57/9f/94128044.jpg" width="30px"><span>lerame</span> 👍（0） 💬（0）<div>这个业务规则有时候在需求层面也会频繁变动吧？而且跨团队的时候，有关联的业务，有时候规则限制是不一样的。</div>2022-12-09</li><br/>
</ul>