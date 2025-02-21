你好，我是徐昊，今天我们来继续学习AI时代的软件工程。

在上一节课，我们介绍了如何构建反馈循环，并使用大语言模型（Large Language Model，LLM）反馈模型的缺失，然后再使用LLM进行模型展开，完成对模型的验证。构造有效的反馈循环，并使用LLM对其加速，这是一种利用LLM加速知识学习的通用模式。

然而在实际的应用的过程中，很少会出现不提供业务上下文，仅仅通过LLM反馈辅助建模这样的情况，而且这样的做法实际效率也不高。今天，我们来讨论一下使用LLM辅助建模的其他方法。

## 通过概念字典辅助建模

我们知道在建模的过程中，最重要的就是发掘系统中的存在的概念，并建立概念与概念之间的关联。那么在实际建模的过程中，对于概念的提炼就是重中之重了。

通常在建模的过程中，我们会维护一个**概念字典（Glossary）**，其中包含对于系统非常重要的业务概念，以及对于这些概念的基本解释。举个例子，在上节课中，当我们收到LLM给出的反馈后，我们对于建模任务给出了这样的调整：

```plain
这是一个教学学籍管理系统。系统中应该包含以下的核心概念：
- 教学计划：一系列相关课程和活动，这些课程和活动旨在培养特定领域的知识和技能。比如，计算机科学与技术学士学位教学计划，或是计算机科学与技术硕士学位教学计划
- 录取通知：学生需要根据录取通知注册学籍。录取通知应该包含学生被录取的信息，如录取的教学计划
- 学籍：当学生注册之后，学籍记录学生在校将按照哪个教学计划学习
- 学生
```
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e8/c9/59bcd490.jpg" width="30px"><span>听水的湖</span> 👍（1） 💬（0）<div>第二章学习反馈持续收集中，链接在这里：https:&#47;&#47;jinshuju.net&#47;f&#47;YzTEQa[社会社会] 期待你们的反馈！</div>2024-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（2） 💬（3）<div>原文：我们通常使用 Epic 用户故事提取模型。

为什么呢？翻了一下User story applied，没什么收获。我想到两个原因：
1、一开始粒度可以先粗一点，需要的时候再细化（比较敏捷？）
2、用epic的粒度描述feature的话，story数量比较少，比较方便</div>2024-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（1）<div>2024年05月03日14:17:27
到了这里留言越来越少了</div>2024-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（1）<div>勘误：

原文：然后，我们可以修改建模的任务模板：用户故事======{story}概念提取的方法============{modeling_method}任务===请根据上面描述的业务场景，按照提取概念的方法，提取其中的业务概念。并给出每个概念的定义。并以表格形式给出Glossary，并标注对应的archtype

======

这个不是建模任务模板，这个是提取glossary的模板，建模模板会让生成mermiad</div>2024-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（3） 💬（0）<div>第二次学习收获：

1. 将概念字典（Glossary）加入 CoT 中可以增强 AI 辅助建模
2. 如果没有概念字典，可以通过用户故事让 AI 提取
3. CoT 越完善 AI 生成的结果越准确，当缺少某项概念时，可以先通过 AI 获取，然后再加入 CoT，让 AI 越来越强</div>2024-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>在文章最后突然来了个“领域字典”，这个领域字典和概念字典是同一个东西嘛？</div>2024-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（0）<div>先epic 然后用细粒度的用户故事验证。
这和TDD很像，先AT再UT。</div>2024-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（0） 💬（0）<div>10 | LLM辅助建模（二）：构造思维链
🤔☕️🤔☕️🤔
【R】建模中发掘概念，建立观念间关联，维护成概念词典（Glossary）。
开始为复杂认知模式（Complex），当发现LLM给出的反馈，可以有效构成概念字典时，即从探测性模型生成、转向针对性的知识生成（Generated Knowledge），由此逐渐进入到庞杂认知模式（Complicated），提效就靠构造思维链（CoT）的发挥，再借助四色法、催化剂法、实体目标法、事件风暴法。
【.I.】概念，最容易建立，是因为脑子里会自动浮现出来，最难以共识，即使看着相同的词典，在没有一起摩擦过几次之前，面对相同的名词，大概率9个人有11种以上的概念解释，包括某些人前后解释还矛盾的情况。容易和困难，同时在概念上表现得如此突出。
概念，举个例子，立刻应付道，噢，这样呀，加点操作，嗯，知道啦，来个状态，啊，至于嘛，再来辨析分类抽象，这，清晰到繁复，繁复到简化，得多来几遍，才能体验到概念之魔力，也真正需要概念它老人家的存在。
【Q】用户故事，主要来自社会化活动，逻辑上它不该来自LLM的生成？
    —  by 术子米德@2024年4月2日</div>2024-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（0） 💬（1）<div>老师，我注意到建模的任务模板只有context 和 glossary 这两个 variable 。既然我们在提取glossary 的任务模板里有 modeling_method 这个variable，那么建模的任务模板是不是也加上modeling_method呢？还是这里面有什么不加的考量？</div>2024-04-02</li><br/>
</ul>