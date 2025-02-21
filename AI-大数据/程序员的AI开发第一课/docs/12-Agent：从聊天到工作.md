你好，我是郑晔！

经过前面几讲内容的介绍，相信你已经能做出一个带有自己业务特点的聊天机器人了。在很多场景下，聊天机器人已经完全能够满足我们的需要了，比如智能客服。我们只要把恰当的业务数据提供给聊天机器人，这个智能客服甚至可以表现得比大多数人类都要好。

不过，聊天机器人的能力也仅限于陪你聊天，如此强大的大模型如果只能起到聊天的作用，显然是无法满足人们对 AI 能力的想象。所以，有人就开始思考，如何将大模型的能力与真实工作结合起来，于是，Agent 开始在行业里流行起来。

这一讲，我们就来说说 Agent。

## Agent

我们这里讨论的 Agent 概念最初来自于人工智能领域，人们往往叫它智能代理（Intelligent Agent），所以，许多人把 Agent 翻译成了智能体。Agent 到底是什么呢？

下面这张图来自《人工智能：现代方法》一书，它可以帮我们理解 Agent 的概念。

![](https://static001.geekbang.org/resource/image/fe/34/febc3404c63f919b6937dafcb0469f34.jpg?wh=3000x1654)

在这张图里，智能体通过传感器从外界感知环境，并将接收到的信息交给中央的“大脑”处理，然后，“大脑”做出决策，让执行器执行相应的动作，对环境产生影响。

根据书里的定义，任何通过**传感器（sensor）感知环境（environment）**，并通过**执行器（actuator）作用于该环境的事物都可以视为智能体（agent）**。按照这个理解，人是一种智能体，眼睛、耳朵等器官是我们的传感器，手、腿等器官是我们的执行器；机器人是一种智能体，摄像头、红外线测距仪是传感器，各种电机是执行器。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（3） 💬（1）<div>第12讲打卡~
业界很多大佬预测，2025年会是“AI Agent 元年”，我们拭目以待！</div>2025-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/32/3de6a189.jpg" width="30px"><span>范</span> 👍（0） 💬（1）<div>翻译为智能体，比“代理”更好理解了</div>2024-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（0） 💬（0）<div>老师 请教一个问题：前两天Anthropic发布了MCP &lt;https:&#47;&#47;www.anthropic.com&#47;news&#47;model-context-protocol&gt;, 请问这个东西和agent有多大关系？这个MCP当前是否有竞争产品？对程序员的参考价值有多大？

---
思考题答案在此：https:&#47;&#47;www.perplexity.ai&#47;search&#47;llm-ai-agent-shi-yi-ge-peng-bo-0nk8rr6nRmyvXEzl3JY1sg</div>2024-11-27</li><br/>
</ul>