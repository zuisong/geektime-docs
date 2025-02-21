你好， 我是李锟。

在上节课中，我们通过 DSPy 的官方入门教程的 [Learn DSPy](https://dspy.ai/learn/) 栏目学习了 DSPy 的核心概念，并且通过一些简单的例子代码展示了 DSPy 的基本用法。除了入门教程外，DSPy 团队还在 [Tutorials](https://dspy.ai/tutorials/) 栏目下给出了一些更为详细的例子，以便开发者全面体验使用 DSPy 的开发过程。在这节课中，我们将带着要解决的业务需求，有针对性地学习 Tutorials 栏目下的例子。

在前面的课程中，我们已经分别使用 MetaGPT、AutoGPT、Swarm 三种开发框架实现了 24 点游戏智能体应用。在这三个实现中，有一个遗留的难题始终未能解决，那就是通过所使用的基础 LLM 直接给出满足 24 点游戏要求的表达式。

之前未能解决这个问题的根本原因在于，为了让基础 LLM 直接给出 24 点表达式，手工编写的提示词需要使用 CoT (思维链)、ToT (思维树) 等模式，写起来会非常复杂。而且这样的提示词还很脆弱，并非一直能够稳定工作 (稳定给出符合要求的表达式)。有一种拳头打在棉花上面，使不上力气的感觉。因此我们放弃了走这条路，而是使用自己手写的函数库给出 24 点表达式。

通过上节课的学习，我们已经理解到：DSPy 率先开创的**自动提示词工程**开发方法，正是为了解决上述手工提示词工程存在的这些问题而产生的。那么有人肯定会自然地想到，使用 DSPy 的自动提示词工程，也许有可能解决这个长时间未能解决的遗留问题。这个想法是正确的，下面我们就着手使用 DSPy 来解决这个问题。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/51/23bfc6d1.jpg" width="30px"><span>夏一行</span> 👍（1） 💬（1）<div>用中文的数据集训练后，中文问题的回答会不会更好？</div>2025-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c7/2d/9929cbb9.jpg" width="30px"><span>Shepard</span> 👍（0） 💬（1）<div>我把上面的例子投给了deepseek-r1, 也返回了正确的答案，其中还有流式输出的推理思考过程，这感觉，真像一个推理的人啊。

query:Use the following four natural numbers 1,3,7,13 to form a four-rule operation expression. This expression calculates a value equal to 24, where only the four natural numbers and add, subtract, multiply, divide symbols and parentheses. The expression can only have four natural numbers given in the expression, and all four natural numbers must be included. Please simply return an expression that meets the above requirements, don&#39;t include &#39;= 24&#39;.
结果：
The expression that meets the requirements is:
(13 - 7) * (3 + 1)
</div>2025-02-11</li><br/>
</ul>