你好，我是李锟。

在开篇词中，我们已经了解了大语言模型应用开发框架可划分为 ChatBot 和 Autonomous Agent（自主型智能体）两大类。虽然 ChatBot 开发框架的生态已经非常繁荣，但我们这门课只会关注 Autonomous Agent 开发框架。不过这两大类开发框架之间的界限并非泾渭分明，例如 LangChain 也具有一些开发 Autonomous Agent 应用的能力，而 AutoGPT、MetaGPT 其实也可以用来开发 ChatBot。

不过我们还是应该根据特定 LLM 应用的业务需求优先选择最适合的**轻量级开发框架**。一来学习门槛会比较低（不必学习很多多余的知识），二来也能充分挖掘所用基础 LLM 的一些新的能力。如果一味偷懒，直接选择貌似最省事的**重量级低代码开发框架**，这类框架往往存在大量的过度封装，会导致大语言模型应用开发陷入到一个死胡同之中，一些较为复杂的需求，甚至完全无法实现。

## 常见 ChatBot 开发框架的局限性

那么常见的 ChatBot 开发框架有哪些局限性呢？我们以两个最有代表性的开发框架 LangChain 和 Dify 作为例子，来看看它们的局限性。

LangChain 是目前最流行的大语言模型应用开发框架，然而它有以下局限性：

- code base 很大，存在很多过度封装，有很多容易混淆的概念，这使得开发人员很难理解和使用它。当应用代码运行时出错，不容易快速排查错误原因。
- 首要支持的应用类型为 ChatBot + RAG 应用，对需要自主运行、高度自动化的 Autonomous Agent 应用的支持很少。
- 严重依赖预先写好的大量手工提示词。会导致脆弱性和不灵活，无法适应基础大语言模型的升级或变更。

Dify 是一个流行的大语言模型应用低代码开发框架，它有以下局限性：

- **高度依赖算法和预训练语言模型**：Dify 的核心功能基于智能化算法实现。一旦算法出现问题或不适用于某些特定场景，Dify 的效果将大打折扣。Dify 依赖预训练的语言模型，虽然它们足够强大，可以应对一般性的文本生成和理解任务，但面对一些特定领域的应用时，它们的表现往往不足以令人满意。使用 Dify 的开发者无法控制底层的模型结构、训练过程和优化策略，尤其是在需要进一步优化模型性能的时候。
- **无法替代专业技能**：虽然 Dify 能够简化技术流程，但它并不能完全替代专业技能。在涉及高度专业化和复杂度的任务时，专业人士的经验和判断仍然不可或缺。Dify 提供的预设API或预先训练好的模型并不能满足复杂的业务需求，例如某些需要特定领域知识或语言风格的生成任务，开发者无法针对性地进行深度优化。
- **应用场景有很大的局限性**：Dify 的适用场景较为有限，在某些特定领域或需求下，Dify 无法提供有效的解决方案。Dify 主要支持的应用类型也是 ChatBot + RAG 应用，对需要自主运行、高度自动化的 Autonomous Agent 应用的支持很少。
- **存在隐私泄露的风险**：许多 LLM 应用涉及到的用户数据需要严格保护，而 Dify 因为会依赖第三方平台，所以数据传输和存储环节上存在一定的隐私泄露风险。

Dify 只是 LLM 应用低代码开发框架中一个有代表性的例子，上述问题在其他低代码开发框架中其实都有 (抱歉，我不是针对你，我是说…)。Dify 起码是开源的，完全支持本地部署。那些云端的商业低代码开发框架，例如 OpenAI GPTs、字节跳动的扣子（国际版叫 Coze）、百度文心智能体开发平台（AgentBuilder）等等，想要私有化部署的成本非常高昂。

既然如此，我们可以完全忽略上述这些 ChatBot 开发框架，把关注点聚焦在我们最关心的 Autonomout Agent 开发框架上面。

## Autonomous Agent 的发展历史

Autonomous Agent 其实并非是一个新的概念，可以说开发 Autonomous Agent 伴随着 AI 技术发展的全过程。早在 1991 年，AI 技术的发展尚处在步履维艰的阶段，就有人写过如何设计 Autonomous Agent 的书，书名叫 Designing Autonomous Agents，作者是 Pattie Maes。

![图片](https://static001.geekbang.org/resource/image/a6/a7/a65b9820d776ac19c3be0325aab881a7.png?wh=1920x964)

但是因为当时的 AI 技术发展程度太低，计算机的算力也太低，这本书只能局限在一些理论的探讨上。一直到了 Hinton 教授等人发明了深度学习，特别是诞生了强化学习之后，开发高度灵敏、可靠的 Autonomous Agent 在工程上才成为了现实。所以现代**深度强化学习**（Deep Reinforcement Learning, 简称 DRL）是开发 Autonomous Agent 必需的基础技术，而基于 DRL 发展起来的大语言模型则可以让 Autonomous Agent 如虎添翼。

这类自主型智能体应用通常应用在 BPA 场合，甚至还应用在一些环境要求非常苛刻的工业场景（工厂、油田、煤矿等等）。微软公司有一个专门的自主人工智能部门，这个部门专门与一些大型工业企业合作，设计开发各种复杂的**工业大脑**。微软公司的自主人工智能应用总监 Kence Anderson（相当于首席产品经理）总结了自己十余年为大型企业设计自主决策 AI 系统的经验，写了一本设计此类应用的专著：Designing Autonomous AI。此书 2022 年上市，刚好是大模型时代的元年。

![图片](https://static001.geekbang.org/resource/image/42/f3/42c417bbed18a491f603a610f6d950f3.png?wh=1920x964)

新的这本书主要是面向 **AI 产品经理**和 **AI 业务架构师**的，并没有涉及到底层的任何具体的 AI 算法，但是这本书中提出的一套完整的方法论对于设计开发自主型智能体应用非常有指导性。我强烈建议渴望深入学习的同学课后把这本书找来一读。具体的技术容易学会，我们这门课程正是讲解具体的技术。但是深入掌握方法论层面的东西，就需要靠很强的领悟能力了。一个是术，另一个是道，两者缺一不可。涉及到“道”的内容，我们会在学习了足够多的“术”之后再来集中介绍。因为没有足够的“术”的积累，是不可能领悟“道”的。

与 Autonomous Agent 类似，多 Agent 的 AI 应用也不是一个新的概念，伴随着 AI 技术的发展也是由来已久。多 Agent 应用适用于更加复杂的业务流程和自动化场景，在这些场景中，仅有完成单一任务的 Agent 是不够的，需要将很多 Agent 组合在一起，实现复杂的工作流，才能完成目标。当然，实现多 Agent 应用的基础还是能够实现很多高度灵敏、可靠的单 Agent。

## Autonomous Agent 开发框架的历史

2023 年 ChatBot 开发框架占据着大语言模型应用开发的舞台中央，到了 2024 年，舞台中央已经退让给 Autonomous Agent 开发框架。最早出现的 Autonomous Agent 开发框架是 AutoGPT，最初名叫 EntreprenurGPT，由英国游戏开发者 Toran Bruce Richards 开发，于 2023年3月16日在 GitHub 上发布。

AutoGPT 结合了 GPT-4 和 GPT-3.5 模型，通过 API 来创建完整的项目。它可以根据用户给定的目标，自动生成所需的提示词，并执行多步骤任务，不需要人类的干预和指导。AutoGPT 弥补了 GPT-4 的缺点，实现了任务执行的自动化，这也是 AutoGPT 能在短时间内爆火的原因。AutoGPT相当于给了GPT-4一个“身体”，充当了它的“四肢”，从而对大语言模型生成的内容实现了更深层次的应用。

AutoGPT 的诞生轰动了整个大语言模型应用开发社区，甚至让当时的明星开发框架 LangChain 黯然失色。随后在很短时间内，开源社区涌现出大量类似 AutoGPT 这样的 Autonomous Agent 开发框架，例如 Camel、BabyAGI、MetaGPT、AutoGen（微软）、AutoAgents、AgentGPT、Swarm（OpenAI）等等。随着这些开发框架的发展壮大，它们都已经能够支持开发复杂的多 Agent 应用，多 Agent 应用通常都是基于角色扮演（role playing）来实现的，即每个 Agent 扮演一个角色（或岗位），仅完成这个角色（或岗位）需要完成的工作，通过事先定义的工作流相互协作。

## 我们的选择——轻量级 Autonomous Agent 开发框架

上述这些 Autonomous Agent 开发框架的功能、成熟度（完成度）各异，本课程将会按照它们的成熟度顺序来分别介绍。这个清单还在快速成长中，我们无法面面俱到。我对这些框架的排序为：MetaGPT、AutoGPT、Swarm、Auto Agents、AutoGen……

把 MetaGPT 放在最前面，因为 MetaGPT 是由我们的同胞吴承霖老师开创的，于2023年6月开源，至今已有将近一年半的时间，发展迅速，社区非常繁荣。MetaGPT 无论在成熟度，还是文档的质量上都是首屈一指，已经后来居上超越了 AutoGPT。

AutoGPT的核心开发团队不大稳定，管理略显混乱。重新设计开发的新版本 AutoGPT Platform 与老版本 AutoGPT Classic 相比变化巨大，完全没有向后兼容。过去为 AutoGPT Classic 写的那些文档全部不适用于 AutoGPT Platform，而且 AutoGPT Platform 的文档的组织和丰富程度也很不理想。所以目前阶段，要把 AutoGPT 应用在对可靠性要求很高的生产环境，需要做一些权衡。然而我仍然把 AutoGPT 放在第二位来讲解，是因为 AutoGPT 有很多开创性的设计，对其他 Autonomous Agent 开发框架的设计产生了巨大影响。而且这个新版本的 AutoGPT Platform 的设计正是为了更好地支持多 Agent 协作，未来的前途也很光明（当然团队也不差钱 :) ）。

把 Swarm 放在第三位，一方面是 Swarm 系出名门，是来自 OpenAI 内部开发人员的贡献，未来会得到长期的支持。另一方面是 Swarm 易学易用，很轻量，非常适合用来试验各种多 Agent 应用，同时充分挖掘底层基础大语言模型的潜力。

Autonomous Agent 开发框架最好是轻量级的，不要过度封装。我们不需要重量级开发框架，特别不需要那种**要么全有、要么全无**的开发框架。过犹不及，一旦过度封装，当基础 LLM 的新版本提供了一些全新功能时，通过重量级开发框架往往难以及时利用这些新功能。

除了 Autonomous Agent 开发框架外，我们还很有必要学习一类自动提示词工程开发框架。这类开发框架可以缓解并解决复杂手工提示词工程中存在的工作繁重、脆弱、不可移植、技能难以在团队中传播等等严重问题。我将选择此类开发框架中诞生最早的 DSPy 来做讲解。DSPy 也可以被集成在 Autonomous Agent 开发框架之中。

## 即将开发的 Autonomous Agent 应用的需求

我们这套课程在实战部分，将会始终坚持由可运行的例子驱动的原则。我们都是实用主义者，对长时间沉溺于理论探讨或者畅想未来兴趣不大。通过可运行的例子来学习，对于程序员来说是最为高效的学习方式，同时也会充满趣味。

我们接下来讨论一个能体现多 Agent 协作的应用场景和需求。这里要先说明一下，在课程的入门篇学习具体框架的过程中，我们的案例不会太复杂，否则会喧宾夺主，失去焦点。在课程的进阶篇还会有一个真实的行业级应用案例，带你把前面学到的知识都实战演练一遍。

玩游戏是大家都喜闻乐见的，我们也可以设计一个能够陪我们玩游戏的 Autonomous Agent 应用。那么玩什么游戏呢？

24点是一种非常流行的游戏，玩家拿到 4 个整数，每个整数都落在 \[1, 13] 的区间上，玩家需要通过四则运算，将这 4 个整数组合成一个算式，并且这个算式的计算结果是整数 24。算式中可以有加减乘除，以及括号（用于改变运算符号的计算优先顺序）。24点游戏的规则，详见[百度百科](https://baike.baidu.com/item/24%E7%82%B9%E7%89%8C/4133244)。

我们可以使用上述不同的 Autonomous Agent 开发框架，分别来实现一个陪用户玩24点游戏的智能体应用。每个应用的实现中至少有两个角色（两个Agent），共同协作来完成任务。

上述这些是简单的功能性需求，我们还希望这个应用能满足一些非功能性需求。

- 很好地支持本地部署的开源大语言模型。这样可以节省调用商业大语言模型的费用，同时还能提高响应速度，而且还更容易做平行扩展（假设我们想把这个应用做成一个在线服务，提供给很多用户并行使用）。
- 能够在较低的硬件配置下流畅运行。除了完成基本的功能性需求外，我们还需要对开源大语言模型做性能测试和优化，让它们在较低的硬件配置下也能流畅运行。

讨论完了上述需求，估计你已经跃跃欲试了。且慢，工欲善其事，必先利其器。我们下一课中，需要理解一些与开源大语言模型相关的基础概念，并且做一些开发之前的准备工作。敬请期待！

## 总结时刻

最后我们来总结一下。开发优秀的大语言模型应用，选择最适合的开发框架和开发工具至关重要，也是需要首先解决的问题。

技术选型和架构设计，永远都是一种**权衡的艺术**，权衡的首要依据是待开发应用的**业务需求**和**运行环境**。脱离具体的业务需求和运行环境，大谈特谈某种技术或架构的优势，其实就是在耍流氓。

大语言模型应用的范围非常广阔，也因此诞生了很多不同的开发框架。不同的开发框架各自有自己主要面向的应用领域，这一点需要特别注意。如果我们只是开发一个常见的 ChatBot，例如一个旅游景区的导游机器人，那么 LangChain 是一个正确的选择。但是当我们开发的是工作环境中的另一类智能体应用——Autonomous Agent，而且需要通过多 Agent 来实现复杂的协作，那么就应该选择另外一类开发框架。

另外基础大语言模型仍然在快速发展的过程中，在一些大语言模型应用开发框架中存在很多过度封装，既不利于简单直接实现业务需求，也不利于当切换到大语言模型的新版本时，充分利用新版本大语言模型的最新功能，因为尚未被封装。我们需要的是灵活的**轻量级开发框架**，而不是学习门槛很高的**重量级开发框架**。同样，我们也需要对很多所谓的低代码甚至无代码大语言模型应用开发框架保持足够的警惕。世上没有免费的午餐，大语言模型仍然不是软件行业的银弹，冷静的现实主义者才能走得更远。

在本节课的最后，我们还讨论了一个即将实现的 24 点游戏的具体需求。这个智能体应用就是我们在后续的入门篇中学习各个开发框架的应用需求。既不过分复杂，也不过分简陋，足以展示各个开发框架的核心功能。

## 思考题

Autonomous Agent 应用的运行环境，与 ChatBot 应用的运行环境有哪些区别？与开发 ChatBot 相比，为何开发 Autonomous Agent 有更高的复杂度？

期待你的分享。如果今天的内容对你有所帮助，也期待你转发给你的同事或者朋友，大家一起学习，共同进步。我们下节课再见！
<div><strong>精选留言（6）</strong></div><ul>
<li><span>种花家</span> 👍（6） 💬（1）<p>以下是对指定内容的处理：

### Autonomous Agent 应用的运行环境与 ChatBot 应用的运行环境的区别
- **交互方式**：ChatBot 应用通常以文本或语音交互为主，用户通过输入问题或指令来获取回复，交互相对简单直接。而 Autonomous Agent 应用则可能涉及多种交互方式，如视觉识别、语音交互、物理操作等，需要处理更复杂的多模态信息.
- **任务范围**：ChatBot 的任务通常较为单一，主要集中在对话和信息查询，如答疑解惑、提供信息等。Autonomous Agent 的任务则更加广泛和多样化，包括但不限于导航、决策制定、任务执行等，需要具备更全面的能力来应对各种复杂场景.
- **自主性和决策能力**：ChatBot 的自主性相对较低，主要依赖预设的规则和知识库来生成回复，决策能力有限。Autonomous Agent 则需要具备较高的自主性和决策能力，能够在没有人类干预的情况下，根据环境变化和任务需求做出合理的决策和行动.

### 开发 Autonomous Agent 有更高复杂度的原因
- **技术要求更高**：Autonomous Agent 的开发需要融合多种先进技术，如机器学习、计算机视觉、自然语言处理、传感器融合等，这些技术本身都具有较高的复杂性，且需要相互配合才能实现 Autonomous Agent 的功能.
- **环境适应性挑战**：Autonomous Agent 需要在复杂多变的环境中运行，如不同的物理环境、社会环境等，需要具备强大的环境适应能力，能够准确感知和理解环境信息，并做出相应的调整和决策，这对开发提出了更高的要求.
- **安全性和可靠性要求**：由于 Autonomous Agent 可能涉及到物理操作和决策制定等关键任务，其安全性和可靠性至关重要。开发过程中需要充分考虑各种潜在的风险和异常情况，设计出更加健壮和可靠的系统，以确保 Autonomous Agent 在各种情况下都能安全稳定地运行.
- **多学科知识融合**：Autonomous Agent 的开发涉及多个学科领域的知识，如计算机科学、人工智能、控制理论、心理学等，需要开发者具备跨学科的知识储备和综合运用能力，这也增加了开发的复杂度.</p>2025-01-06</li><br/><li><span>yangchao</span> 👍（1） 💬（1）<p>自治代理和聊天机器人在运行环境上的主要区别在于：自治代理需要在复杂、动态的环境中自主运行并优化其行为，而聊天机器人则主要依赖于用户与机器人之间的交互界面进行对话和信息提供。开发Autonomous Agent相比开发ChatBot具有更高的复杂度，这主要体现在任务分解与规划、多方案选择与优化、外部模块与工具的使用、自主性与互动性以及系统集成与部署等方面</p>2025-01-08</li><br/><li><span>Blow</span> 👍（1） 💬（1）<p>老师，有没有交流群呢</p>2025-01-07</li><br/><li><span>Geek_c680d7</span> 👍（1） 💬（2）<p>感觉这门课会很有用，我们目前就是遇到了一些低代码平台&#47;langchain都解决不了的问题，应用还停留在chatbot，没有升级为agent，催更催更~</p>2025-01-07</li><br/><li><span>I. Z.</span> 👍（1） 💬（1）<p>请问LangGraph 和CrewAI 框架如何</p>2025-01-07</li><br/><li><span>鐘</span> 👍（0） 💬（1）<p>chatbot 和 agent 在輸出的要求上自己感覺會不太一樣：
chatbot 的服務對象是人, 獲取的輸出大多是一次性 問題也不太會重複
agent 的服務對象是排程任務, 期望有穩定一致的輸出</p>2025-02-09</li><br/>
</ul>