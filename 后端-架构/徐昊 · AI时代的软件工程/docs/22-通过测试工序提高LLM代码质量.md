你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

上节课，我们讲解了如何将架构模式转化为测试工序，以及工序在架构落地过程中发挥的作用。测试工序有助于将抽象的架构设计转化为具体的开发任务和实际的工作流程，帮助团队有效地实现架构设计，并最终产生质量高、可靠性强的软件系统。

同样，通过测试工序，我们也可以让LLM帮助我们有效地实现架构设计，并提高LLM生成代码的质量。这节课我们就讨论一下如何实现这个目标。

## 将工序转化为提示词模版

首先，我们需要将测试工序转化为CoT（Chain of Thought），通过CoT指导LLM按照测试工序的要求，将给定的需求功能拆分成对应的任务列表。

这里我们使用的测试工序仍然是前面提到的那一个：

![](https://static001.geekbang.org/resource/image/26/ee/26e48c8fc6ca29b39eb57366dbb42fee.jpg?wh=1833x932)

我们将架构组件中的三种不同的组件分别进行测试，其中Persistent层中的组件，使用假对象（Fake，内存数据库）作为测试替身。而HTTP interface和Application Logic层则通过存根（Stub）作为测试替身。最后，再通过功能测试，对整个系统进行验证。

那么让我们来构造CoT的提示词模板：

```plain
架构描述
=======
当前系统技术栈为Spring Boot，Jersey和MyBatis。

当前系统采用典型的三层架构设计，分别为:
- HTTP interface层，负责提供RESTful API，命名规则为XXXAPI，比如OrdersAPI；
  - API通过JAX-RS的Resource实现；
  - HTTP interface层调用Application Logic层的Service，完成功能；
- Application Logic层，负责提供核心逻辑，命名规则为XXXService，比如OrderService；
  - 使用Java实现，Service使用POJO为主的领域对象；
  - Application Logic层调用Persistent层的DAO完成对于数据的访问；
- Persistent层，负责与持久化数据交互，命名规则为XXXDAO，比如OrderDAO；
  - 使用Java实现，DAO使用DTO为主的数据对象；
  - DAO通过MyBatis的Mapper实现
 
工序说明
=======
  - 如果功能要求使用到HTTP interface层，那么：
     - 使用Application Logic层中对应Service的Stub作为测试替身；
     - 列出需求描述的场景使用到HTTP interface组件的功能（HTTP interface层目标功能）；
     - 列出“HTTP interface层目标功能”需要测试的场景（HTTP层目标场景）；

  - 如果功能要求使用到Application Logic层，那么：
     - 使用Persistent层中对应DAO的Stub作为测试替身；
     - 列出需求描述的场景使用到Application Logic组件的功能（Application Logic层目标功能）；
     - 列出“Application Logic层目标功能”要测试的场景（Application Logic层目标场景）；

  - 如果功能要求使用到Persistent层，那么：
     - 使用H2数据库作为fake implementation；
     - 列出需求描述的场景使用到Persistent组件的功能（Persistent层目标功能）；
     - 列出“Persistent层目标功能”要测试的场景（Persistent层目标场景）；

功能需求
=======
{functionalities}

任务
====
首先，列出每一个验收场景以及对应的测试数据；
然后，针对每一个验收场景，按照架构描述和工序说明的指引，列出任务列表。
```
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（1）<div>🤔☕️🤔☕️🤔
【R】列出：验收场景 + 测试数据 -&gt; 任务列表
-》按照任务列表、符合技术要求，编写测试代码。
独立测试工序模板 -&gt; 大模型驱动的自主代理架构（LLM based Autonomous Agent）。
【.I.】课程到这里，似乎越来越淡薄于是否有一只开发团队，这是种错觉、还是种趋势，我不太确定。而且，引入LLM来助推软件开发过程中的这些地方，那么作为具体的人，在哪些地方出现，以及需要具备或需要提升的能力在哪些方面，也得试着辨别明晰出来。
【Q】课程中的CoT，跟业界的CoT的联系与区别是什么？
— by 术子米德@2024年4月26日</div>2024-04-26</li><br/>
</ul>