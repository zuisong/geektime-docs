你好，我是黄俊彬。

随着项目不断的迭代，新的技术栈也会持续不断地演进。适时使用新的技术栈，可以帮助我们提高效率以及代码质量。这节课，我们就一起来学习如何安全高效地为遗留系统升级技术栈，具体我们会使用新的语言Kotlin以及新的架构模式MVVM，来重构消息组件。

选择Kotlin + MVVM，有两方面考量：一方面，Kotlin从框架层面提供了大量的封装，可以帮我们减少工作量，无需编写大量的模板代码；另一方面，[Kotlin也是官方推荐的开发语言](https://developer.android.com/kotlin)，MVVM框架则是官方推荐的分层架构，为此 [JetPack](https://developer.android.com/jetpack) 也专门提供了相应的框架组件支持快速开发。

不过技术栈不同了，流程方法仍然相同，这里我们会继续使用组件内分层重构的方法。

## 准备：支持Kotlin

对于遗留系统来说，通常使用的开发语言都是Java，那么在选择Kotlin语言时，我们通常会有2种选择：第一种是Kotlin与Java语言混编，另外一种是完全使用Kotlin替换Java。

至于哪种方式更好，它们之间有什么差异？我们结合例子来分析一下。

第一种方法使用Java与Kotlin混编，这个做法的好处是我们不需要改动原来的代码，只需要用Kotlin语言编写扩展的代码就可以了。但是缺点就是由于Kotlin的语言高度依赖编辑器生成转换代码，所以有些语法通过Java来调用Kotlin会比较啰嗦，例如伴生函数的调用。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：第二种方法是怎么转换为kotlin的？
文中开头的例子说到“第二种方法使用 Kotlin 替换 Java 的好处就是，可以减少一些跨语言调用编写问题，但是缺点是需要将原有的代码改动成 Kotlin”。 例子代码中，一个是kotlin，一个是Java，并没有Java转换为kotlin的信息啊。
Q2：假如现在开发APP，用kotlin还是Java？哪个好？如果现在会Java但不会kotlin，需要放弃Java而学习kotlin吗？
Q3：kotlin有协程，安卓用Java开发的话，有协程吗？（印象中是没有的）
Q4：kotlin可以用MVVM，用Java可以采用吗？
Q5：Java和kotlin混合开发，除了调用不太方便，还有什么问题？比如，会有性能问题吗？
Q5：MVVM和MVP都是“业务逻辑和视图分离”，似乎是一样的。那这两种模式有什么区别？
Q6：老师赞成Java和kotlin混合开发吗？</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/b5/a8db0572.jpg" width="30px"><span>永远年轻</span> 👍（0） 💬（1）<div>第五点中，应该是使用了 DataBinding 的单项绑定，数据变动会驱动 UI 变化，而 UI 变化不会驱动数据变化。双向绑定应该是 「@={vm.xxx}」</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（0） 💬（1）<div>项目中是 Kotlin、Java 混编，有个问题想请教一下老师：Kotlin、Java 混编和纯 Kotlin 的编译时间哪个更短呢？</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a1/31/ca97e229.jpg" width="30px"><span>louc</span> 👍（0） 💬（1）<div>不太严谨啊，怎么重构后，getMessageList就在主线程取数据了，之前不是在异步线程么</div>2023-05-05</li><br/>
</ul>