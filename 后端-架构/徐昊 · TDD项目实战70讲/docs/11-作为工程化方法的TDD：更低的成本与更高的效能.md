你好，我是徐昊。在了解了测试驱动开发中的“测试”，和测试驱动开发中的“驱动”之后。让我们重新复盘一下作为工程化方法的TDD。

## TDD的流程

在[第一讲](https://time.geekbang.org/column/article/494207?utm_term=zeus7J9ZC&utm_source=pcweb&utm_medium=geektime&utm_campaign=100109401&utm_content=pcweb)中，我曾给出了一张任务分解法的流程图。用以在TDD演示过程中，帮助我们把握整体流程的走向。由于是在课程刚开始给出的，很多内容我们尚未澄清，无法给出更细致的描绘，只能看做对于TDD流程大略的描述。

那么在学习了什么是TDD中的测试，和什么是TDD中的驱动之后，我们将会怎么描述TDD的流程呢？

![](https://static001.geekbang.org/resource/image/a5/9c/a5a74d26cf9581064420d81cff7da89c.jpg?wh=2284x1285)

如上图所示，使用TDD的核心流程为：

- 首先将需求分解为**功能点**，也就是将需求转化为一系列**可验证的里程碑点**；
- 如果已经存在架构或架构愿景，则依据架构中定义的**组件与交互**，将功能点分解为不同的**功能上下文**；
- 如果尚不存在架构愿景，则可以将功能点作为功能上下文；
- 将功能点按照功能上下文，分解为**任务项**。也就是进一步将可验证的里程碑点，分解为功能上下文中可验证的任务项；
- 将任务项转化为**自动化测试**，进入红/绿/重构循环，驱动功能上下文内的功能实现；
- 如果重构涉及功能上下文的重新划分，即**提取/合并组件**，即视作对于架构的重构与梳理。需调整后续功能点中对于功能上下文以及任务项的划分。
- 如此往复，直到所有功能完成。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>1.  从认可 TDD 的员工开始推行最容易入手
2. 从想不加班但又想通过技术手段提升效率的员工入手
3. 从不想花费大量时间在线上找 Bug 的员工入手</div>2022-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rAqwExT20D9WdnlEmZpzXp9HrorvyeGOdpicPCwfAREPJuM1F5I3A8cTbCg2LwggfxdEP0qPwCuAWjrIRiaNj4MQ/132" width="30px"><span>夏天</span> 👍（0） 💬（1）<div>TDD带来的是工程效率的提升，是降本增效的方法。所以在团队中推行TDD，要先说服sponsor。sponsor愿意买单，才能推行TDD。</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（5） 💬（0）<div>老师，后面会去讲如何在项目型的工程实践中，Restful接口，数据库模型。项目为典型的三层架构，或DDD分层架构。这样的场景下，如何进行TDD，以及在需求大量变动的情况下，保证项目的质量？</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/31/91cc9c3c.jpg" width="30px"><span>汗香</span> 👍（3） 💬（0）<div>与客户交流的过程中以测试代替文档，先得到客户的对需求列表方式的认可</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/ab/caec7bca.jpg" width="30px"><span>humor</span> 👍（2） 💬（0）<div>从自己开始入手，自己在做项目的过程中实践TDD，并取得一定的成果，进而在组内及团队内推广</div>2022-04-17</li><br/><li><img src="" width="30px"><span>Geek_b11f27</span> 👍（0） 💬（0）<div>从我自己入手，一个人如果不知道一件事情的好处就不会去做，不做就不知道这个好处，这样形成了一个死循环。我自己先试着打破循环，别人看到了了效果也相当于打破了他们的认知，从而有可能打破他们的认知上的死循环。</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/df/90/0d8864db.jpg" width="30px"><span>少晴</span> 👍（0） 💬（2）<div>我目前是项目TDD的推动负责人，我现在很困惑，对于团队成员能力的参差不齐，推动TDD的过程非常困难，很难让团队成员接受TDD思想。很主要的一点是不会写测试代码是他们一直吐槽的点，甚至很多人认为写测试代码所投入的精力远大于功能实现。所以这个如何解决呢</div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（0）<div>在团队中从哪里开始推行 TDD 最容易入手？

从正在需要重构的项目入手容易些吧，但是往往这样的项目都有工期，和领导的KPI。敢于推行TDD需要莫大的勇气，感觉又是个一把手工程。</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（0）<div>1. 从工程管理的角度，“判断一个人是否理解了需求”的成本极高。
2. 从工程管理的角度，“判断哪个需求应该从工程化方式交付模式进入探索模式”的成本极高。
3. 从工程管理的角度，“判断团队是否对架构达成了共识”的成本极高。
4. 从工程管理的角度，“发现当前架构愿景不容易实现的需求”成本极高。

感觉自己不懂工程管理，如何补足这方面的知识呢？</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/b1/bb5126fc.jpg" width="30px"><span>宁</span> 👍（0） 💬（0）<div>通过提交代码时检查代码测试覆盖率来推动TDD：前期可以覆盖率较低，但是一旦增加了检查，代码提交失败（红），增加测试代码使其通过检查并提交代码（绿），逐步提高测试覆盖率（重构），整个推动过程也可以保持TDD的节奏。——有种俄罗斯套娃的感觉，手动狗头</div>2022-04-11</li><br/>
</ul>