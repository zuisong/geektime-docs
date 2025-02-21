你好，我是徐昊。从今天开始，我们就来使用TDD的方式实现RESTful Web Services。

在上节课，我们展示了需要完成的几大功能块。我们很容易可以发现，RESTful Web Services需要多模块协同完成。而不是像DI Container那样，可以从单一模块入手，在完成几个功能之后再进行重构。

那么我们可以先简单地规划一下架构愿景（Architecture Vision），以简化后续的工作。

## 规划架构愿景

首先，我们需要明确的是，我们将以Servlet的方式来实现RESTful Web Services框架。也就是说，我们将提供一个Servlet作为主入口，在其中完成对资源对象（Resources）的派分，并根据不同的超媒体选择对应的reader和writer进行输入输出处理。大致结构如下图所示：

![](https://static001.geekbang.org/resource/image/f5/6e/f531cdc180da287d25244d5ea711f36e.jpg?wh=8000x4500)

然而仅仅如此，还不足以让我们顺滑地进入伦敦学派的流程（如果你足够自信，已经可以开始经典学派TDD了），我们需要进一步细化ResourceServlet中的组件与交互：

![](https://static001.geekbang.org/resource/image/fe/b2/fe218e684cba33a63fa004c76f1ea3b2.jpg?wh=7493x3969)

如上图所示，为大致的组件划分：

- ResourceDispatcher管理所有的Root Resource，并根据Root Resource的标注形成路由表。它可以根据路由表，生产对应的ResourceLocator。
- ResourceLocator表示与URI中某一段相匹配的资源方法（Resource Method），并负责调用它。
- ResourceContext表示Resource上下文，包含所有可注入的组件（通过@Context标注）。
- BodyReader聚合了所有的MessageBodyReader，可以根据所需的类型，从HttpServletRequest中读取对象。
- BodyWriter聚合了所有的MessageBodyWriter，可根据提供的类型，将信息写回到HttpServletResponse中。
- ExceptionMapping聚合了所有的ExceptionMapper，可根据提供的异常，将信息写回到HttpServletResponse中。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/22/7606c6ba.jpg" width="30px"><span>张铁林</span> 👍（0） 💬（1）<div>https:&#47;&#47;github.com&#47;vfbiby&#47;tdd-restful
开始提交作业，这次把中间记的操作步骤一起放在项目doc下，还有小步提交，尽量，把每一个改变都提交上来，然后，每一章完成时，再做一个大提交。可以check到小提交处来练习。</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/fa/2a046821.jpg" width="30px"><span>人间四月天</span> 👍（5） 💬（0）<div>非常喜欢这个spike方法，在产品需求领域，叫做mvp最小可行产品，这个应该叫做最小可行设计，对于复杂需求，需求不清晰，或者复杂设计，通过这个方法验证架构愿景的可行性非常好，也能增强前期架构规划的信心。
</div>2022-06-02</li><br/><li><img src="" width="30px"><span>Geek_dcb102</span> 👍（1） 💬（0）<div>spike的过程:
1. spike过程 需要能够快速反馈结果 所以建议从一个开始可运行的小型框架 逐步替换成自己的代码 
2. spike中 是需要自己认为的组件 尤其是大的组件 都全员参与的 确定组件之间的关系是否合理
3. spike中 需要参考现成的规约api 让组件更内聚合理 保证后续的复杂升级的可能性 也可以更好的观察组件的理解和划分是否合理.防止因为一开始的用例简单 造成很多组件相互耦合 职责不清 没有复杂升级的方向 进而没有达到spike应有的效果</div>2023-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0d/fe/4e5ba578.jpg" width="30px"><span>Jason</span> 👍（1） 💬（0）<div>第一次直观的感受spike方法</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/93/0f1cbf44.jpg" width="30px"><span>枫中的刀剑</span> 👍（1） 💬（0）<div>最大收获是Spike的方式也可以采取类似TDD的方式，甚至对于暂不关心的细节部分可以使用stub。</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/87/8ed5880a.jpg" width="30px"><span>大碗</span> 👍（0） 💬（0）<div>通过实现“现有的接口”去了解组件交互的细节</div>2022-09-05</li><br/>
</ul>