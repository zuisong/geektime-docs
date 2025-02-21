你好，我是徐昊。今天我们来回顾一下第二个实战项目的整个过程。

## 最终的完成形态

首先，让我们来看一下最终的完成形态：

## 项目回顾与总结

首先是任务分解。在项目刚开始的时候，我们没有构想任何的架构愿景，而是直接采用经典模式，从功能点出发进行TDD开发。一开始进展是很顺利的，从任务列表上看，除了偶有遗落的功能点，基本上是按照任务列表顺畅进行的。

第一个转折点出现在我们第一次重构之后，我们将InjectionProvider从ContextConfig中分离了出来。并将依赖的检查从运行期检查，变成了在ContextConfig.getContext时预先检查。

也就是说，我们的**架构愿景**在此时发生了改变：只要Context能够被构建出来，其中就不存在无效组件和无效的组件关系（循环依赖、依赖缺失）。

这个架构愿景改变的直接影响，就是让我们**分解任务的方式**发生了变化。体现在任务列表上为：

- 方法注入（改变前）
  
  - 通过Inject标注的方法，其参数为依赖组件
  - 通过Inject标注的无参数方法，会被调用
  - 按照子类中的规则，覆盖父类中的Inject方法
  - 如果组件需要的依赖不存在，则抛出异常
  - 如果方法定义类型参数，则抛出异常
  - 如果组件间存在循环依赖，则抛出异常
- 方法注入（改变后）
  
  - 通过Inject标注的方法，其参数为依赖组件
  - 通过Inject标注的无参数方法，会被调用
  - 按照子类中的规则，覆盖父类中的Inject方法
  - 如果方法定义类型参数，则抛出异常
  - 依赖中应包含Inject Method声明的依赖
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/22/7606c6ba.jpg" width="30px"><span>张铁林</span> 👍（2） 💬（1）<div>主要还是开阔了眼界，用TDD来做一个相对复杂的功能，不像很多kata那样，短短几十行代码量，体会不到不断的重构和深进。</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>这次要求中最容易做到的就是为自己点个赞，我已经点了！
最开始学习 TDD 相比：学会使用 @Nested 标签；学会了泛型中 ?、T 之类的含义；有测试做保障想重构就重构</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/93/0f1cbf44.jpg" width="30px"><span>枫中的刀剑</span> 👍（2） 💬（0）<div>第一次静距离观察一个完整项目的TDD过程，感受还是挺深的。特别是第一次接触到测试重组、测试文档化的时候有种眼前一亮的感觉。而其中ComponentRef 模型和 Qualifier 模型调整的重构过程更加让人赏心悦目。新的模型引入拓展了知识，带来个更加明确的功能上下文划分。而原有整体的结构却没有发生太多的变化。这种一点点进步是能够很清楚的感受到的。

最后在附上项目链接：https:&#47;&#47;github.com&#47;maplestoryJin&#47;DiContainer  
包括 static 注入实现。</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（0） 💬（0）<div>有个关于bind的实现问题，一般情况都是bind(Component.class, Instance.class)或者bind(Component.class, Provider&lt;Instance.class&gt;)。如果直接bind(Instance.class, Instance.class)，那么get(Component.class)还能找到吗？
另外，无论bind的是Intance还是Provider，当需要注入Provider类型的时候，是都需要支持吗？
这些规范的东西我可以去哪里找到，希望老师能解答一下。</div>2022-06-06</li><br/>
</ul>