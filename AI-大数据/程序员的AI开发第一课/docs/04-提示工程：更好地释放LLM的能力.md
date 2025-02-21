你好，我是郑晔！

上一讲，我们讨论了站在用户角度怎么写提示词。从使用的角度来说，提示词公式基本上涵盖了日常使用的大多数场景。但是，仅仅掌握提示词公式，对于开发一个大模型应用而言，这个公式就显得有些不够了。为了开发大模型应用，我们需要进一步扩展自己对于提示词的理解，掌握更多关于提示词的知识，这就是我们这一讲要来讨论的内容——提示工程。

## 提示词工程

提示工程，顾名思义，就是研究怎么写提示词。之所以有提示工程，很重要的原因就是大模型在不同人眼中做的事情差异很大。普通用户只是把大模型当作一个聊天机器人，他们的关注点是大模型能否给予及时且正确的反馈，我们上一讲提到的提示词公式就足以应付绝大多数的使用场景。

而在开发者眼中，我们需要的是**大模型处理复杂任务场景的能力**，比如，现在很多 Agent 背后的技术就是让大模型推断出下一步的行为，这是利用大模型的推理能力，而这依赖于提示词的编写。

大多数人是先知道 ChatGPT，然后知道提示词，再知道提示工程。但其实提示工程并不是在 GPT 流行之后才诞生的技术。提示工程最早是诞生于自然语言处理（Natural Language Processing，简称 NLP），人们发现，在任务处理过程中，如果给予 AI 适当的引导，它能更准确地理解我们的意图，响应我们的指令。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（3） 💬（1）<div>提示词有推荐的认证考试吗？或者说如何提高自己的编写能力？</div>2024-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（3） 💬（1）<div>思维链，把思考的过程链接起来，有理有据，顺便把正确率提升了，只不过响应会慢一点，并且多费点精力（成本高一点）。我们人类也是：背答案很快，但把答案推导一遍就慢了。</div>2024-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（1）<div>1. ReAct 框架看不太懂，后面有项目细讲嘛？
2. 最近Anthropic推出的computer use，跟ReAct有什么关系吗？https:&#47;&#47;www.anthropic.com&#47;news&#47;3-5-models-and-computer-use. 都是操作“工具”？
3. 文中说ReAct“具备了实现一个 Agent 的基础”, 还有没有其他主流的实现agent的框架？（除了ReAct）</div>2024-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（1） 💬（2）<div>是否可以这么理解:  ai应用工程师  = system提示词工程师. 😃. </div>2024-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/e0/3db22579.jpg" width="30px"><span>技术骨干</span> 👍（0） 💬（1）<div>提示工程释放大模型的能力，如虎添翼可以这么讲吧</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（1） 💬（0）<div>GPT-4o mini
免费
3.11 比 3.8 大。虽然它们的整数部分相同，但小数部分的比较中，0.11 大于 0.8，因此 3.11 大于 3.8。</div>2024-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第4讲打卡~</div>2024-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/c8/1ccbb110.jpg" width="30px"><span>淡漠尘花划忧伤</span> 👍（0） 💬（0）<div>笔记：提示工程是为了引导大模型给出更好的答案：
零样本提示：用于通用的任务。
少样本提示：用于特定的简单任务。
思维链提示：引入推理过程，可以与零样本提示和少样本提示结合。
ReAct 框架：将大模型推理和一些行动能力结合起来，超越大模型自身的限制。</div>2025-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a6/3bddb98c.jpg" width="30px"><span>大叶枫</span> 👍（0） 💬（0）<div>极客AI总结的不错哦“1. 提示工程是研究如何写提示词的技术，旨在扩展对提示词的理解，以更好地释放大模型的能力。
2. 零样本提示（Zero-Shot Prompting）利用大模型的丰富知识，无需过多信息提示即可完成通用任务，适用于简单查询等场景。
3. 少样本提示（Few-Shot Prompting）通过给出一些例子，帮助大模型理解特定工作内容，适用于简单分类场景。
4. 思维链提示（Chain-of-Thought Prompting）旨在让大模型慢下来，进行推理和思考，提升在数学、推理等问题上的表现。
5. ReAct 框架结合了推理和行动，超越大模型自身的限制，使其能够更多地参与实际行动。”</div>2025-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（0） 💬（0）<div>提示工程是研究如果写好提示词的技术</div>2024-11-16</li><br/>
</ul>