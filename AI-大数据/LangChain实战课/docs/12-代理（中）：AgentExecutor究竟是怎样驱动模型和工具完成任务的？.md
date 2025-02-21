你好，我是黄佳，欢迎来到LangChain实战课！

上节课中，你了解了ReAct框架的原理，最后我给你留了一道思考题，让你说一说LangChain中的“代理”和“链”的差异究竟是什么。

我的答案是：**在链中，一系列操作被硬编码（在代码中）。在代理中，语言模型被用作推理引擎来确定要采取哪些操作以及按什么顺序执行这些操作。**

下面这个图，就展现出了Agent接到任务之后，自动进行推理，然后自主调用工具完成任务的过程。

![](https://static001.geekbang.org/resource/image/ae/e3/aeb7497d833b0b3188fbc7152282b0e3.jpg?wh=10666x5260)

那么，你看LangChain，乃至整个大模型应用开发的核心理念就呼之欲出了。这个核心理念就是**操作的序列并非硬编码在代码中，而是使用语言模型（如GPT-3或GPT-4）来选择执行的操作序列**。

这里，我又一次重复了上一段话，显得有点啰嗦，但是这个思路真的是太重要了，它也凸显了LLM作为AI自主决定程序逻辑这个编程新范式的价值，我希望你仔细认真地去理解。

## Agent 的关键组件

在LangChain的代理中，有这样几个关键组件。

1. **代理**（Agent）：这个类决定下一步执行什么操作。它由一个语言模型和一个提示（prompt）驱动。提示可能包含代理的性格（也就是给它分配角色，让它以特定方式进行响应）、任务的背景（用于给它提供更多任务类型的上下文）以及用于激发更好推理能力的提示策略（例如ReAct）。LangChain中包含很多种不同类型的代理。
2. **工具**（Tools）：工具是代理调用的函数。这里有两个重要的考虑因素：一是让代理能访问到正确的工具，二是以最有帮助的方式描述这些工具。如果你没有给代理提供正确的工具，它将无法完成任务。如果你没有正确地描述工具，代理将不知道如何使用它们。LangChain提供了一系列的工具，同时你也可以定义自己的工具。
3. **工具包**（Toolkits）：工具包是一组用于完成特定目标的彼此相关的工具，每个工具包中包含多个工具。比如LangChain的Office365工具包中就包含连接Outlook、读取邮件列表、发送邮件等一系列工具。当然LangChain中还有很多其他工具包供你使用。
4. **代理执行器**（AgentExecutor）：代理执行器是代理的运行环境，它调用代理并执行代理选择的操作。执行器也负责处理多种复杂情况，包括处理代理选择了不存在的工具的情况、处理工具出错的情况、处理代理产生的无法解析成工具调用的输出的情况，以及在代理决策和工具调用进行观察和日志记录。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/78/36/76defa45.jpg" width="30px"><span>刘旺旺</span> 👍（18） 💬（1）<div>各位同学可以尝试在测试脚本中添加一段代码:
```python
import langchain
langchain.debug = True
```
这样可以看到大部分思考过程！</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（12） 💬（1）<div>感觉能多能力 不管是chain还是代理,本质上都是给大模型完善的提示词呢, 并且langchain在适当的环节,内置了很多适当的提示词,结合上下文,觉得下一步做什么,引导大模型完成对应的需求, langchain本质上还是提供了默认的提示词,不知道理解的对不对</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/6e/efb76357.jpg" width="30px"><span>一只豆</span> 👍（4） 💬（3）<div>在最近比较火的Agent综述文章中，Agent被概括为：Profile Memory Plan Tool这四个模块。结合老师这讲前半部分说的“LLM编程新范式”：不是把操作序列硬编码进去，而是让GPT3&#47;4这样的模型去选择这些操作序列。
可不可以理解为：所谓 Plan，就是定义了“操作序列”（？）；所谓Profile，就是提供了“选择操作序列”时推理所需的高层次背景信息？ 反思Reflect，是引导LLM生成推理需要的中观信息？
Memory和Tool是基于此的支撑？
提问心态：我已经通过prompt engineering验证了某个业务领域的多层次复杂问题框架，现在需要使用Agent思想工程化。所以在试着塞进去，还请老师明示！多谢！</div>2023-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（3） 💬（1）<div>先打卡学习。

人类一思考，上帝就发笑。大模型一循环思考，我就忍俊不住要惊呼点赞！

话说第一张图Tack是写错了吗？应该是Task？</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/aa/a2/c7a3758d.jpg" width="30px"><span>漏网之渔</span> 👍（2） 💬（1）<div>agent执行的过程中，prompt是不断累计的么，会出现token上限的情况吗</div>2023-10-08</li><br/><li><img src="" width="30px"><span>Geek_085d59</span> 👍（1） 💬（2）<div>请问调用数学计算工具时，为什么是llm在做计算，我理解的不应该是让大模型返回工具名称和参数，然后langchain本地调用python工具计算吗</div>2023-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/f5/96/4e3dd4e1.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（1）<div>debug的详细过程能不能也专门出一节课，整个判断的思路形成过程特别重要，谢谢啦~</div>2023-09-29</li><br/><li><img src="" width="30px"><span>Geek_339c29</span> 👍（0） 💬（1）<div>大佬，我们公司现在在计划做一个AI产品核心，形成自己的core产品，后续接到具体的客户订单的时候，可以直接基于core做一些定制化的开发以此来快速完成各种项目。不知道我理解的对不对，目前有个fastgpt开源项目，是不是做了可视化的chain组装最后生成的是agent？ 如果我们要做这样的一个core产品，是不是也是这样一个类似的东西，有哪些东西值得做在这个core里面？</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/8c/791d0f5e.jpg" width="30px"><span>SH</span> 👍（0） 💬（4）<div>老师， 看你本次的分析中，都会重复的出现 那个 思考-行动-观察的步骤，每一轮得到一个结果，再重复执行之前的步骤时，把上一步的结果代入到新的任务，有点不理解， 在这里为什么基于上次的逻辑里面，在需要的结果处继续往下执行的呢？而且重新思考一轮呢？  这样是不是会很浪费 token ?</div>2023-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（0） 💬（1）<div>chain中决策走哪一个分支,和代理中选择用哪一个代理, 本质上是一回事吗</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（1）<div>从  AgentType.ZERO_SHOT_REACT_DESCRIPTION  可以看到，不同的 AgentType 实质是prompt 不同？</div>2023-09-27</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>运行了课程代码，测试了 LangChain的Debug和Verbose 的不同：

* 设置为 langchain.verbose = True ：
重要事件记录：Verbose模式会记录“重要”事件的输入和输出，而不是所有事件。这使得开发者可以看到应用程序执行的关键步骤，而不被过多的信息淹没。
用途：适用于需要监控应用程序运行过程的场景，帮助开发者理解代理如何处理请求，并在必要时进行性能优化。

* 设置为 langchain.debug = True ：
Debug 模式
详细日志记录：Debug模式是最详细的日志记录设置，会记录所有事件的输入和输出。这包括所有链、模型、代理、工具和检索器的详细信息。
用途：适用于需要全面了解应用程序执行的每一个细节的场景，尤其是在复杂应用程序中进行问题诊断时。</div>2024-08-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/270T9KAFd4oCxXXB1giaMDaJuTQVib8gPt77VkM5dbS3hW60kwTNnxMYpVibwWVdnASCrymBbwT7HI77URia0KUylw/132" width="30px"><span>Geek_7ee455</span> 👍（1） 💬（0）<div>如果我想新增一个工具,有办法吗</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6a/a1/6270eeb7.jpg" width="30px"><span>极客星星</span> 👍（0） 💬（0）<div>“是以最有帮助的方式描述这些工具”
想问下，这个体现在代码里哪一步？比如langchain怎么知道serpapi是搜索引擎?下面这个代码里，并没有告诉langchain这个i信息？
tools = load_tools([&quot;serpapi&quot;, &quot;llm-math&quot;], llm=llm)</div>2024-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第12讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/56/ff7a9730.jpg" width="30px"><span>许灵</span> 👍（0） 💬（0）<div>感觉这个与routeChain很像，只是把分支的llm进行了扩展与插件化</div>2024-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1d/fa/89d625ed.jpg" width="30px"><span>滴滴答滴滴答</span> 👍（0） 💬（0）<div>为什么我跑出来总是会加上12.5？并且+12.5还会报错
[llm&#47;start] [1:chain:AgentExecutor &gt; 7:tool:Calculator &gt; 8:chain:LLMMathChain &gt; 9:chain:LLMChain &gt; 10:llm:OpenAI] Entering LLM run with input:
{
  &quot;prompts&quot;: [
    &quot;Translate a math problem into a expression that can be executed using Python&#39;s numexpr library. Use the output of running this code to answer the question.\n\nQuestion: ${Question with math problem.}\n```text\n${single line mathematical expression that solves the problem}\n```\n...numexpr.evaluate(text)...\n```output\n${Output of running the code}\n```\nAnswer: ${Answer}\n\nBegin.\n\nQuestion: What is 37593 * 67?\n```text\n37593 * 67\n```\n...numexpr.evaluate(\&quot;37593 * 67\&quot;)...\n```output\n2518731\n```\nAnswer: 2518731\n\nQuestion: 37593^(1&#47;5)\n```text\n37593**(1&#47;5)\n```\n...numexpr.evaluate(\&quot;37593**(1&#47;5)\&quot;)...\n```output\n8.222831614237718\n```\nAnswer: 8.222831614237718\n\nQuestion: 80.16 * 0.15&quot;
  ]
}
[llm&#47;end] [1:chain:AgentExecutor &gt; 7:tool:Calculator &gt; 8:chain:LLMMathChain &gt; 9:chain:LLMChain &gt; 10:llm:OpenAI] [3
。。。。。。
。。。。。。
[chain&#47;error] [1:chain:AgentExecutor] [12.06s] Chain run errored with error:
&quot;ValueError(&#39;unknown format from LLM: + 12.5\\n```text\\n80.16 * 0.15 + 12.5\\n```\\n...numexpr.evaluate(\&quot;80.16 * 0.15 + 12.5\&quot;)...&#39;)Traceback (most recent call last):\n\n\n  File \&quot;D:\\workspace\\python\\awesome-python3-webapp\\.venv\\lib\\site-packages\\langchain\\chains\\base.py\&quot;, line 156, in invoke\n    self._call(inputs, run_manager=run_manager)\n\n\n  File </div>2024-02-01</li><br/>
</ul>