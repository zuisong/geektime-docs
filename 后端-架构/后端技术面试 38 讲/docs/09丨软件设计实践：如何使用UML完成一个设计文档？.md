在上一篇文章中，我们讨论了为什么要建模，以及建模的4+1视图模型，4+1视图模型很好地向我们展示了如何对一个软件的不同方面用不同的模型图进行建模与设计，以完整描述一个软件的业务场景与技术实现。但是软件开发是有阶段性的，在不同的开发阶段用不同的模型图描述业务场景与设计思路，在不同阶段输出不同的设计文档，对于现实的开发更有实践意义。

软件建模与设计过程可以拆分成需求分析、概要设计和详细设计三个阶段。UML规范包含了十多种模型图，常用的有7种：类图、序列图、组件图、部署图、用例图、状态图和活动图。下面我们讨论如何画这7种模型图，以及如何在需求分析、概要设计、详细设计三个阶段使用这7种模型输出合适的设计文档。

## 类图

类图是最常见的UML图形，用来描述类的特性和类之间的静态关系。

一个类包含三个部分：类的名字、类的属性列表和类的方法列表。类之间有6种静态关系：关联、依赖、组合、聚合、继承、泛化。把相关的一组类及其关系用一张图画出来，就是类图。

类图主要是在**详细设计阶段**画，如果类图已经设计出来了，那么开发工程师只需要按照类图实现代码就可以了，只要类方法的逻辑不是太复杂，不同的工程师实现出来的代码几乎是一样的，这样可以保证软件的规范、统一。在实践中，我们通常不需要把一个软件所有的类都画出来，把核心的、有代表性的、有一定技术难度的类图画出来，一般就可以了。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/97/ae/08eb3aad.jpg" width="30px"><span>To be is to do</span> 👍（16） 💬（5）<div>老师,可以推荐一下 mac上做UML,时序图的软件吗?</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/39/9b/fc21f943.jpg" width="30px"><span>睡浴缸的人</span> 👍（6） 💬（2）<div>以前做业务开发的时候被业务逼着走，没有什么意识。后来做独自坐通用模块时，感觉这样不行，看了点软件工程的书，慢慢开始画UML图进行设计，设计完后有时候写代码简直如尿奔~</div>2020-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OgopVGSkwlFuyHV0hWtzxjEAQ8qhwQuTeY9BdvXDDTj2JH5d9ZI1hJBnlgaoUcKtrceWVlUejJEUdjCjoKSUAQ/132" width="30px"><span>golangboy</span> 👍（6） 💬（2）<div>老师，
1.设计模式的图例只适合画静态类图？
2.详细设计阶段是要确定软件的细节和逻辑的基本框架，用设计模式可以提高程序的扩展性，我这样理解对吗？
3.实际开发中，有很多都是那种需求都不明确，探索性的，随时要变，甚至推倒重来。像这种情况，我也不可能一开始就有全局的视野，有啥好的实践经验或者推荐？</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/d4/1e0bb504.jpg" width="30px"><span>Peter</span> 👍（4） 💬（1）<div>一直有个问题没搞清楚，就是关联关系和组合关系之间的关系区别是什么，我怎么觉得都是类A中包含一个成员变量类B</div>2021-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/06/08/855abb02.jpg" width="30px"><span>Seven.Lin澤耿</span> 👍（3） 💬（1）<div>我们会画图，但是没按照规范，应该是四不像，但是也能用😂</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/4f/ff04156a.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（1）<div>部署图主要用在概要设计阶段，请问有推荐的工具吗？</div>2023-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/ad/5020a8c5.jpg" width="30px"><span>Farewell丶</span> 👍（0） 💬（1）<div>&quot;流程图也比较有普适性，可以在需求分析阶段描述业务流程，也可以在概要设计阶段描述子系统和组件的交互，还可以在详细设计阶段描述一个类方法内部的计算流程。&quot; 应该是“活动图”，写错了。</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/3c/a595eb2a.jpg" width="30px"><span>台风骆骆</span> 👍（15） 💬（0）<div>本章学习总结：
1、基本上开发分为需求分析、概要设计、详细设计阶段。
2、常用的UML图有类图、时序图、活动图、用例图、组件图、部署图、状态图七种。
     类图是用来描述类之间的关系以及类中包含的属性和方法的，可以在需求分析阶段的领域模型用简化的类图来表示，详细设计阶段详细描述类图。
     时序图是用来描述类、组件、模块之间的调用关系的，可以在需求分析、概要设计、详细设计都用得到。
     活动图则是表达了过程和业务逻辑的，有点像流程图，在三个阶段都可以应用。
     用例图是用来表达用户与软件系统的交互，用来表达这个软件系统的功能需求。一般用于需求分析。
     组件图是表达了各个组件之间的关系，一般是依赖关系，是静态的，如果要表达调用关系需要用时序图或活动图，一般用于概要设计阶段。
     部署图是用于表达物理上面的软件部署情况，一般用于概要设计阶段。
     状态图则是表达某个组件或某个类的状态迁移情况。可以用于详细设计和需求分析阶段。
3、不同阶段需要描述的东西不一样，用的图也不一样相同。</div>2019-12-09</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（11） 💬（0）<div>我现在自己写代码基本不画图，主要因为写的软件不够复杂（Android开发）。
我画类图和时序图主要是用来分析别人写的代码，画得过程中往往能搞清楚代码的意图。</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（3） 💬（0）<div>我感觉类图不太实用，如果能够画出类图来，那么基本上代码也就写的差不多了。而且可能会遇到代码已经修改，但是设计文档中的类图已经过时的问题。好像也够工具可以直接从代码生成类图，以前 Visual Studio 就可以生成类图。

部署图估计是每一分架构设计里面都会有的，不过专栏里面画了两个立方体有点奇怪，我之前看到的至少会把数据库画成圆柱体。

用例图是我认为最有用的，特别是在需求分析，以及概要设计阶段。做一个项目，不论大小，至少应该先有一个用例图吧。

在我看来，序列图和状态图只有在遇到比较复杂的情况下，对于沟通或者整理思路很有用。但是如果用 Visio 或者其他工具可能会比较复杂，把时间都花在做图上，如果有可能，我倾向于手工或者白板画图，比较简单，并且利于修改。当然如果最后形成正式文档的时候，也可以花一些时间，美化一下。

UML 中没有流程图，但是有活动图，在我看来，活动图有点像“立体”的流程图。

估计最终在架构设计文档中还是会有流程图的，否则感觉缺了点什么。

之前的项目，在架构设计文档里面，为了撑门面，一般都会尽可能多的画图；在方案评审的时候，评委很多时候也会对图比较重视。但是也有一些项目，是先撸代码搞起来，在最后评审的时候才去补各种设计图。

如果让我来做架构师，那么用例图（场景）、组件图（逻辑）、部署图（物理）、活动图（过程）应该会有，好像还缺一个开发视图的。</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/8b/32a8c5a0.jpg" width="30px"><span>卡特</span> 👍（3） 💬（0）<div>小结一下
uml图主要有7类
我用的mac,工具astash 或者planuml
从需求分析，概要设计，详细设计依次画这些图
1，用例图 体现角色和软件系统的功能
2，活动图 体现核心流程
3， 状态图 体现核心状态变化
4，部署图 软件的物理结构
5，组件图 软件的模块结构
6，时序图 核心和逻辑
7，类图 领域模型和具体功能设计

可以比较好的为软件建模</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（2） 💬（0）<div>太多的细节，没法用这些来描述。往往是客户在反复使用后调整出来的。</div>2020-10-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo435IStLENgDxYPDykxxE9CP6Tye3xPQ584UeNqW21pU62ic6vibrGpNjKVbhulVehVG5IGvicSTaZg/132" width="30px"><span>alex</span> 👍（2） 💬（1）<div>活动图跟时序图这两个有点分不清，老师能给讲下区分么？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/10/5a/3411221e.jpg" width="30px"><span>Heidi</span> 👍（2） 💬（2）<div>计算机类专业大一大二内容</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d8/5d/07dfb3b5.jpg" width="30px"><span>杯莫停</span> 👍（1） 💬（0）<div>设计一个东西，先画出图，按照流程去实现。有些像逻辑判断，结果导向会清晰很多。Bug多都是因为没有一个全局概念，写代码耦合性越来越高。还有就是画图比较有说服力。</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d8/5d/07dfb3b5.jpg" width="30px"><span>杯莫停</span> 👍（1） 💬（0）<div>我们一般都是架构师一个PPT上面画些流程图，然后粗略讲讲，然后我们开发的时候就靠自己想象力了。</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（1） 💬（0）<div>思考题
你现在开发的软件是否会用到 UML 建模呢？如果没有，你觉得应该画哪些 UML 模型？又该如何画呢？
----
我的回答：目前在工作中基本用不到UML建模。这可能是因为我目前的开发任务比较简单，都是基于现有的大项目框架来进行新增需求或修改需求开发。系统部署的建模也暂时没有涉及到。
但我相信，随着工作的深入，我接触到的工作将会更上层，到时候，面对复杂业务场景，我只有提前做好软件建模设计工作，才能进一步着手的实际开售。</div>2020-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJowicLVgt4uscjBFa2jG7WyBZ0G9ID9JibHdCiafpl7j01txMMXlEiayQjNkw70QKtJAtJ35XAI5voCg/132" width="30px"><span>realwuxing</span> 👍（1） 💬（0）<div>李老师您好，请问架构设计中一般会有的总体设计分层图，技术架构分层图以及逻辑架构图(系统之间的关系) ，这些所起的主要作用？</div>2020-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/5d/69170b96.jpg" width="30px"><span>灰灰</span> 👍（1） 💬（0）<div>打卡</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（1） 💬（0）<div>这个我最常用序列图设计功能和UML设计数据库来着。。。。
总算有一份把把UML说的全一点文章了，最开始不怎么画图，但是设计到一个稍微复杂点的和别的系统有交互的功能从0到1，画一下序列图什么确实有帮助。把这个过程能梳理清楚一些，比直接写代码要头脑更清楚。</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/fb/872e2cf1.jpg" width="30px"><span>秦凯</span> 👍（1） 💬（2）<div>接触到的项目基本都没有这样全面可以窥探系统全貌的架构设计文档。而且实际工作中，项目组小伙伴们接到各自的需求都是在各自的点上做开发，很少从面或体上面去考虑需求、设计和实现，这样就导致判断分支、冗余代码、不必要的复杂逻辑越来越多。大家有没有好的办法走出这种困境？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（0）<div>业务架构图，时序图，泳道图</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/01/95/fd09e8a8.jpg" width="30px"><span>布拉姆</span> 👍（0） 💬（0）<div>组件是系统中遵循一组接口且提供实现的一个物理部件，通常指开发和运行时类的物理实现。表示实际存在的、物理的物件，可以是：源代码、子系统、动态链接库等，组件一般都包含很多类并实现很多接口。

子系统是组件，通常包括许多更小的组件，是一个大的组件。
 
包多用于将类分组。类似于命名空间，在同一包中名字唯一。</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/49/2b938b4f.jpg" width="30px"><span>北极的大企鹅</span> 👍（0） 💬（0）<div>嗯不错啊
draw.io
processon都用过
现在用语雀文档画流程</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/57/3ffdfc8d.jpg" width="30px"><span>vigo</span> 👍（0） 💬（1）<div>活动图 和 时序图 很相似</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/88/bf/16ce4410.jpg" width="30px"><span>苍茫</span> 👍（0） 💬（0）<div>听了大有收获</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>登录了下 draw.io 确实是一个画图利器，业务中如果涉及到很复杂的功能需求，确实是需要画出UML图的，团队基于UML很容易达成共识，还可以指导开发。</div>2019-12-09</li><br/>
</ul>