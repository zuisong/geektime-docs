你好，我是陈旭。

可视化开发是所有低代码工具/平台（下文简称低代码或Low Code）的标配，是成为低代码工具/平台的一个必要条件。而承载可视化开发的核心基础设施，就是所见即所得的编辑器。

这个编辑器非常重要，它的使用体验、能力和易用性在极大程度上决定了低代码整体的成败。由于编辑器的实现是一个非常大的话题，我们需要分成8讲才能说清楚。所以，今天这节课我们先从编辑器的引擎切入，从架构的角度聊一聊应用代码生成器与编辑器之间的关系。

在[讨论低代码到底是银弹还是行业毒瘤那一讲](https://time.geekbang.org/column/article/495328)中，我们了解到低代码的开发过程就是不停地在描述和细化一个业务最终的样子。这就要求低代码编辑器能实时反馈出开发人员的操作结果，这也就是所见即所得的含义。

而通过模拟，是难以保持“所见”与“所得”的一致性的。为了达到“所见”与“所得”的高度一致，我们就需要实时地把应用创建出来，创建应用的过程就是生成并运行应用代码的过程。显然，生成应用代码是这一切的基础。编辑器在收集到开发人员的操作后，应该立即生成应用的代码。

那么，生成代码的功能在架构上和编辑器可以有什么样的关系呢？不同的关系对低代码长期演进会有什么样的影响呢？不同的组织应该如何选择合适的架构呢？这正是你我今天要探讨的主要内容。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/3e/82b7deca.jpg" width="30px"><span>huangshan</span> 👍（2） 💬（1）<div>老师，有几个问题需要请教一下
1、编辑器中组件和组件之间的事件流如何控制，比如A组件的事件会影响B组件的刷新，是在编辑器页面配置，还是通过写代码的方式
2、低代码的解析引擎，在需要手动开发时，如何做到二次扩展开发。
3、低代码在某些场景下可以做到零代码吗？如果可以转到零代码开发，是不是受众不一定非得是程序员，比如运维人员就可以做到页面开发。</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/70/dafc8858.jpg" width="30px"><span>孟谦</span> 👍（0） 💬（1）<div>Level4 怕不是重新搞个类似React的框架了。学习和开发难度又上去了。</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f5/e9/e03655a1.jpg" width="30px"><span>hungry learner</span> 👍（0） 💬（1）<div>老师你好，我说下我的理解：页面拖拽产出的是协议定义的数据格式，比如jason，这是在编辑器里的逻辑，最后要上线就“编译”成可直接运行的代码，比如把协议里的输入框变成input组件。
我之前看一些资料上的思路是，把编辑器的组件渲染逻辑，跟在线运行时的逻辑统一起来了，也就是做了一个运行时引擎统一了两端。</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/98/fb/aa63be6f.jpg" width="30px"><span>pasico</span> 👍（2） 💬（0）<div>根据抽象程度的不同，应用代码生成器与编辑器之间可以分为几个层级？
4个层次


各个层级的关键特征是什么？
1 简单拖拽，像玩具
2 工具和业务耦合严重
3 成熟分离 编译器，协议，解释器
4 插件，生态圈


不同层级对低代码平台长期演进具有什么样的意义？
1 拖拽只是低代码平台起步的一种方式
2 耦合严重的编辑器，负担太重，难以走得更远（很难找到更多人的合作加入），而且积重难返
3 市场上的成功案例都是协议优先，核心稳定，欢迎合作共赢</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ef/ed/90d0199d.jpg" width="30px"><span>李凯</span> 👍（2） 💬（2）<div>老师,  我们现在用的 json schema来作为编译器和生成器的协议, 但是我们的生成器只是单纯导出了json schema, 最后通过解析器动态执行schema数据完成页面渲染的. 您觉得这个和利用AST直接生成代码的区别或劣势是什么?</div>2022-04-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epgqrqneY3HlSW5qb7Hul6rlGjqwxU52pnSlCDIH1skb073Ts7oo7H5egP4o93TzK11xjPJPLDMGw/132" width="30px"><span>InfoQ_27c14057950d</span> 👍（0） 💬（0）<div>编译器不合适吧,编译器原始含义转成机器可执行代码的,你这样用有歧义</div>2024-11-04</li><br/><li><img src="" width="30px"><span>Geek_12e8fd</span> 👍（0） 💬（0）<div>根据抽象程度的不同，应用代码生成器与编辑器之间的关系可以分为四个层级，每个层级的关键特征以及对低代码平台长期演进的意义如下：

Level 1：基础级
关键特征：

没有明确的代码生成器概念，或者实现非常粗糙。
编辑态和运行态的区分主要依赖于一系列if-else语句。
对低代码平台长期演进的意义：

这一层级缺乏足够的抽象，随着功能的增加，代码将变得难以维护，不利于平台的长期发展。
Level 2：耦合级
关键特征：

有相对独立的模块用于生成代码，但该模块与编辑器耦合严重。
编辑态和运行态的公共部分被抽取出来，通过OOP的多态特性实现。
生成的App仍然只能在编辑器上运行，与应用之间存在耦合。
对低代码平台长期演进的意义：

这一层级虽然引入了代码生成的概念，但由于与编辑器的紧密耦合，限制了平台的扩展性和定制性。长期演进需要解决与应用之间的耦合问题。
Level 3：独立级
关键特征：

代码生成器与编辑器基本相互独立，具有同等地位。
引入协议层，代码生成器负责实现协议，编辑器调用协议层提供的API完成代码生成等活动。
命令行形式的代码生成器易于与DevOps流水线结合使用，实现自动化。
对低代码平台长期演进的意义：

这一层级通过解耦代码生成器与编辑器，为平台提供了良好的扩展性和定制性。独立的代码生成器使得应用可以脱离编辑器独立运行，有利于平台的长期发展。
Level 4：生态级
关键特征：

在Level 3的基础上进一步抽象，形成完备的插件开发能力。
编辑器具备插件系统和周边生态，支持开发者通过插件扩展平台功能。
对低代码平台长期演进的意义：

这一层级通过构建插件系统和生态，极大地增强了平台的灵活性和可扩展性。开发者可以根据需求定制和扩展平台功能，推动平台不断演进和发展。同时，插件系统也为构建生态圈奠定了基础，促进了低代码平台的生态繁荣。
总的来说，随着抽象程度的提高，应用代码生成器与编辑器之间的关系从紧密耦合逐渐发展为相互独立和具备生态支持。这种演进过程不仅提高了低代码平台的扩展性和定制性，还为平台的长期发展奠定了坚实基础。</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK3dicRrv41vMfAxdlW2icmTyG3jicf5iaUTZUStUdG6bUKxK1YjIcY67ciaicCfmZ0hqJ035VBBh80N59w/132" width="30px"><span>kkaaddff</span> 👍（0） 💬（0）<div>老师，你在 Qcon 中的分享在哪里可以回看呢</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/13/cd/a1429abe.jpg" width="30px"><span>快手阿修</span> 👍（0） 💬（0）<div>老师好，有个问题想要请教一下，DSL一般都是一个json对象，本身就是一个结构化数据了，文章里提到的变成结构化的SVD主要是什么操作。DSL和SVD的差异在哪里？</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/73/56/9cfb1e43.jpg" width="30px"><span>sheeeeep</span> 👍（0） 💬（0）<div>请问老师，这种使用协议的架构，具体实现方案有相关资料可以推荐阅读的吗？</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/80/52161b2f.jpg" width="30px"><span>Faith信</span> 👍（0） 💬（0）<div>看了老师的PPT, 解决问题的思路很重要</div>2022-06-29</li><br/><li><img src="" width="30px"><span>Geek_1bcbfe</span> 👍（0） 💬（0）<div>老师，麻烦问一下直接开发不能做pro code和low code混合开发吗？</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（0） 💬（0）<div>间接法就是可以做二次开发，是吗</div>2022-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7d/f7/2fe4c1a1.jpg" width="30px"><span>洛河</span> 👍（0） 💬（0）<div>老师，您好：
问题： 对于直接法还是没有太理解，与间接法在编译流程上的区别。 是指不需要生成AVR的框架代码，直接生成兼容浏览器的JS代码嘛？那是不是就意味着抛弃了AVR框架呢</div>2022-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/cf/60/5adef06a.jpg" width="30px"><span>王盛东</span> 👍（0） 💬（0）<div>老师你好， 代码生成器和编译器是同个概念吧， 用了不同名词阅读上稍微绕了些，不知其他人会不会有这种感觉。</div>2022-04-26</li><br/>
</ul>