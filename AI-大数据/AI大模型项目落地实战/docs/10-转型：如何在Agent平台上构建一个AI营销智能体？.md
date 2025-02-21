你好，我是金伟。

上节课说的AI营销功能还是微信单点能力，在现实营销项目中，还需要“化零为整”，把更多的功能及合成一个智能体。

从整个系统的角度来看，就是通过Agent智能体升级我们原来的营销平台，即**原有广告平台 + AI = 营销平台 2.0。**

这节课，我就带你开发几个营销领域的Agent智能体，让你从零开始，学会Agent智能体开发。

## 营销Agent开发思路

Agent平台应用的范式说来并不复杂，交互上，是聊天机器人为基础的交互界面，架构上，支持低成本开发和分享新的AI智能体应用，也可以快速复用原有的成熟应用逻辑。

市场上有一些低代码的Agent开发平台，比如[斑头雁](https://www.betteryeah.com/?channel=feizhuke)、[扣子](https://www.coze.cn/?ref=openi.cn)等等。我们基于这些平台就可以开发自己的Agent智能体应用，也可以直接把这些应用分享给用户。

![图片](https://static001.geekbang.org/resource/image/f5/4f/f5yy53c16791701a0d206cb6fc38344f.png?wh=1920x990)

我们的目标是把原有营销平台的工具全都转换成Agent智能体，同时，把Agent智能体的开发能力分享给我们的客户。具体选型上，一方面基于成本考量，另一方面团队也抱着学习的态度，我们选择在扣子Agent平台上，开发1-2个Agent智能体，组合完成一个完整的业务逻辑。

![](https://static001.geekbang.org/resource/image/58/45/588850d66e32c3c5bc6ca017c2f3a345.jpg?wh=3546x1832)

在做单个的工具之前，我们最大的挑战就是理解、适应Agent平台的开发模式。

我先从Agent平台的**助理**这个概念入手分析。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/3a/407930cc.jpg" width="30px"><span>jerremyZhang</span> 👍（1） 💬（1）<div>非常期待后续</div>2024-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/f8/b4da7936.jpg" width="30px"><span>大魔王汪汪</span> 👍（1） 💬（0）<div>想问下，现在对于Agent的定义，如果实现一个基于用户问题+简单的function call+答案生成的功能可以叫做Agent，那如果后面是一个复杂的工作流也可以叫Agent，所以从功能复杂度角度来说应该怎么定义一个Agent呢？</div>2024-12-30</li><br/>
</ul>