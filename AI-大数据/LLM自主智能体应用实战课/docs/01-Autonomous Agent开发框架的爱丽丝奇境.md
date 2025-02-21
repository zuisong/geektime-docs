你好，我是李锟。

在开篇词中，我们已经了解了大语言模型应用开发框架可划分为 ChatBot 和 Autonomous Agent（自主型智能体）两大类。虽然 ChatBot 开发框架的生态已经非常繁荣，但我们这门课只会关注 Autonomous Agent 开发框架。不过这两大类开发框架之间的界限并非泾渭分明，例如 LangChain 也具有一些开发 Autonomous Agent 应用的能力，而 AutoGPT、MetaGPT 其实也可以用来开发 ChatBot。

不过我们还是应该根据特定 LLM 应用的业务需求优先选择最适合的**轻量级开发框架**。一来学习门槛会比较低（不必学习很多多余的知识），二来也能充分挖掘所用基础 LLM 的一些新的能力。如果一味偷懒，直接选择貌似最省事的**重量级低代码开发框架**，这类框架往往存在大量的过度封装，会导致大语言模型应用开发陷入到一个死胡同之中，一些较为复杂的需求，甚至完全无法实现。

## 常见 ChatBot 开发框架的局限性

那么常见的 ChatBot 开发框架有哪些局限性呢？我们以两个最有代表性的开发框架 LangChain 和 Dify 作为例子，来看看它们的局限性。

LangChain 是目前最流行的大语言模型应用开发框架，然而它有以下局限性：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/e8/d01b90c3.jpg" width="30px"><span>种花家</span> 👍（6） 💬（1）<div>以下是对指定内容的处理：

### Autonomous Agent 应用的运行环境与 ChatBot 应用的运行环境的区别
- **交互方式**：ChatBot 应用通常以文本或语音交互为主，用户通过输入问题或指令来获取回复，交互相对简单直接。而 Autonomous Agent 应用则可能涉及多种交互方式，如视觉识别、语音交互、物理操作等，需要处理更复杂的多模态信息.
- **任务范围**：ChatBot 的任务通常较为单一，主要集中在对话和信息查询，如答疑解惑、提供信息等。Autonomous Agent 的任务则更加广泛和多样化，包括但不限于导航、决策制定、任务执行等，需要具备更全面的能力来应对各种复杂场景.
- **自主性和决策能力**：ChatBot 的自主性相对较低，主要依赖预设的规则和知识库来生成回复，决策能力有限。Autonomous Agent 则需要具备较高的自主性和决策能力，能够在没有人类干预的情况下，根据环境变化和任务需求做出合理的决策和行动.

### 开发 Autonomous Agent 有更高复杂度的原因
- **技术要求更高**：Autonomous Agent 的开发需要融合多种先进技术，如机器学习、计算机视觉、自然语言处理、传感器融合等，这些技术本身都具有较高的复杂性，且需要相互配合才能实现 Autonomous Agent 的功能.
- **环境适应性挑战**：Autonomous Agent 需要在复杂多变的环境中运行，如不同的物理环境、社会环境等，需要具备强大的环境适应能力，能够准确感知和理解环境信息，并做出相应的调整和决策，这对开发提出了更高的要求.
- **安全性和可靠性要求**：由于 Autonomous Agent 可能涉及到物理操作和决策制定等关键任务，其安全性和可靠性至关重要。开发过程中需要充分考虑各种潜在的风险和异常情况，设计出更加健壮和可靠的系统，以确保 Autonomous Agent 在各种情况下都能安全稳定地运行.
- **多学科知识融合**：Autonomous Agent 的开发涉及多个学科领域的知识，如计算机科学、人工智能、控制理论、心理学等，需要开发者具备跨学科的知识储备和综合运用能力，这也增加了开发的复杂度.</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/98/d5e08eb7.jpg" width="30px"><span>yangchao</span> 👍（1） 💬（1）<div>自治代理和聊天机器人在运行环境上的主要区别在于：自治代理需要在复杂、动态的环境中自主运行并优化其行为，而聊天机器人则主要依赖于用户与机器人之间的交互界面进行对话和信息提供。开发Autonomous Agent相比开发ChatBot具有更高的复杂度，这主要体现在任务分解与规划、多方案选择与优化、外部模块与工具的使用、自主性与互动性以及系统集成与部署等方面</div>2025-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/47/3f/51708649.jpg" width="30px"><span>Blow</span> 👍（1） 💬（1）<div>老师，有没有交流群呢</div>2025-01-07</li><br/><li><img src="" width="30px"><span>Geek_c680d7</span> 👍（1） 💬（2）<div>感觉这门课会很有用，我们目前就是遇到了一些低代码平台&#47;langchain都解决不了的问题，应用还停留在chatbot，没有升级为agent，催更催更~</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/94/ae6dcfb9.jpg" width="30px"><span>I. Z.</span> 👍（1） 💬（1）<div>请问LangGraph 和CrewAI 框架如何</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/c7/9c8647c8.jpg" width="30px"><span>鐘</span> 👍（0） 💬（1）<div>chatbot 和 agent 在輸出的要求上自己感覺會不太一樣：
chatbot 的服務對象是人, 獲取的輸出大多是一次性 問題也不太會重複
agent 的服務對象是排程任務, 期望有穩定一致的輸出</div>2025-02-09</li><br/>
</ul>