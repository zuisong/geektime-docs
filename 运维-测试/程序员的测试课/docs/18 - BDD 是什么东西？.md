你好，我是郑晔！

在扩展篇中，我们要讨论的是在不同方向上的写测试探索。在上一讲里，我给你介绍了 TDD。TDD 是在写测试的时机上进行了不同的探索。这一讲，我们再来讲另一个实践——BDD，它是在写测试的表达方式上进行的不同探索。

我们都知道，在软件开发中最重要的一个概念就是分层，也就是在一些模型的基础上，继续构建新的一些模型。程序员最耳熟能详的分层概念就是网络的七层模型，只要一层模型成熟了，就会有人基于这个模型做延伸的思考，这样的做法在测试上也不例外。

当 JUnit 带来的自动化测试框架风潮迅速席卷了整个开发者社区，成了行业的事实标准，就开始有人基于测试框架的模型进行延伸了。各种探索中，最有影响力的就是 BDD。

## 行为驱动开发

BDD 的全称是 Behavior Driven Development，也就是**行为驱动开发**。BDD 这个概念是2003年由 Dan North 提出来的。

单元测试框架写测试的方式更多的是面向具体的实现，这种做法的层次是很低的，BDD 希望把这个思考的层次拉高。拉到什么程度呢？软件变化的源动力在业务需求上，所以，最好是能够到业务上，而校验业务的正确与否的就是业务行为。这种想法很大程度上是受到当时刚刚兴起的领域驱动设计（Domain Driven Design）中通用语言的影响。在 BDD 的话语体系中，“测试”的概念就由“行为”所代替，所以，这种做法称之为行为驱动开发。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（7） 💬（1）<div>郑大，DDD里面模型与软件实现关联、统一语言与模型关联的思想和BDD也是一脉相承的是嘛，以及现在程序员市场更加普遍要求具备产品思维，能多从业务角度思考设计与实现也是技术与业务更紧密结合的时代所需对不</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/87/8ed5880a.jpg" width="30px"><span>大碗</span> 👍（2） 💬（1）<div>老师的BDD项目例子里，写了一个TodoItemStepDefinitions, 然后调用了多个接口，完成了一个完整的业务功能。相当于验收了一个“需求”</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f7/0b/403fbeba.jpg" width="30px"><span>小凯</span> 👍（0） 💬（1）<div>空手道也是BDD吧？</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/95/4544d905.jpg" width="30px"><span>sylan215</span> 👍（5） 💬（0）<div>如果换个角度来看，BDD 也可以认为是一种集成测试，只不过是按照业务场景进行的，目的更明确的集成。

从另一个角度来说，BDD 和 TDD 的道理是一样的，都是让开发者，不仅仅停留在代码的层面，而是从 B 或 T 的角度进行思考，从而编写&#47;设计出更完整的实现。</div>2021-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>感觉这个在实际场景中很少用到，主要就是单元测试加功能测试，这个度应该去如何控制也是一门学问。。</div>2022-04-14</li><br/>
</ul>