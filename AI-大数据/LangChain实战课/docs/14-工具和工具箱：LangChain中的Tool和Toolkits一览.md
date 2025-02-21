你好，我是黄佳，欢迎来到LangChain实战课！

这节课我们来一起看一看LangChain中各种强大的工具（Tool），以及如何使用它们。

在之前的几节课中，我们深入讲解了LangChain中的代理。未来的AI Agent，应该就是以LLM为核心控制器的代理系统。而**工具，则是代理身上延展出的三头六臂，是代理的武器，代理通过工具来与世界进行交互，控制并改造世界**。

## 工具是代理的武器

LangChain之所以强大，第一是大模型的推理能力强大，第二则是工具的执行能力强大！孙猴子法力再强，没有金箍棒，也降伏不了妖怪。大模型再能思考，没有工具也不行。

工具是代理可以用来与世界交互的功能。这些工具可以是通用实用程序（例如搜索），也可以是其他链，甚至其他的代理。

那么到底什么是工具？在LangChain中，工具是如何发挥作用的？

LangChain通过提供一个统一的框架来集成功能的具体实现。在这个框架中，每个功能都被封装成一个工具。每个工具都有自己的输入和输出，以及处理这些输入和生成输出的方法。

当代理接收到一个任务时，它会根据任务的类型和需求，通过大模型的推理，来选择合适的工具处理这个任务。这个选择过程可以基于各种策略，例如基于工具的性能，或者基于工具处理特定类型任务的能力。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_995b81</span> 👍（3） 💬（1）<div>老师好，那我们可以自定义工具吗？比如某个实际场景，我需要调用到某个内部系统的API，通过API返回的信息我再做提取，然后将提取到的信息重新给LLM推理</div>2023-10-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（2） 💬（1）<div>老师，文中“甚至尝试让大模型自动回答 Issues 中的问题——反正大模型解决代码问题的能力本来就更强。”是怎样实现让大模型理解项目系统代码的？例如：一个web项目，我给出一个接口，大模型能从给定的接口出发自顶向下，分析出每一层的调用关系和依赖关系。</div>2023-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（2） 💬（1）<div>怎么理解Tool和Toolkits 的异同呢？</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/55/b6c9c0f4.jpg" width="30px"><span>liyinda0000</span> 👍（0） 💬（2）<div>老师，你有遇到过这个问题吗？
不使用openai封装agent，使用的是私有模型比如qwen-1.8b时封装的agent不能调用tools，不知道什么原因？</div>2024-05-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epEexjZIhNpYNiaAibdLD0Jsl797U6hianjrDs2QT4Q4HOicIEeILxjOcEF7gXGyQeJRJHaeenibb3N9QQ/132" width="30px"><span>enbool</span> 👍（0） 💬（1）<div>老师，怎么进群啊？</div>2023-10-10</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>不使用openai封装agent，使用的是私有模型比如qwen-1.8b时封装的agent是可以很好调用tools。
将“使用 arXiv 工具开发科研助理”到代码修改、输出如下：

旧代码：
llm = ChatOpenAI(temperature=0.0)
新代码：
llm = ChatOpenAI(
    api_key= &quot;DASHSCOPE_API_KEY&quot;,  #换为你的 key
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;,  # 填写 DashScope base_url
    model=&quot;qwen-1.8b-chat&quot;     # 其他通义模型也可以 &quot;qwen-long&quot; 、&quot;qwen-max&quot; 
)

####  运行结果
&gt;&gt; from langchain.agents import load_tools
with new imports of:
&gt;&gt; from langchain_community.agent_toolkits.load_tools import load_tools
（略）
&gt; Entering new AgentExecutor chain...
 我应该使用arxiv来查找相关信息。
Action: arxiv
Action Input: &quot;2005.14165&quot;
Observation: Published: 2020-07-22
Title: Language Models are Few-Shot Learners
Authors: （略）
Thought: 我现在可以作答了。
Final Answer: 2005年发表的一项研究《语言模型是少样本学习者》对语言模型进行了创新性的研究。研究发现，通过预训练在大量文本数据上进行，以及针对特定任务进行微调的方 法，这些方法通常具有跨任务通用性，但在架构上仍然需要特定的任务强化学习数据集。相比之下，人类可以从少量或简单的指示中完成新的语言任务，而目前的自然语言处理系统在 这方面仍做得不好。研究人员展示了，在少样本情况下，可以极大地提高任务通用性和少样本性能，并有时甚至可以达到与先前的细粒度微调方法相当的竞争力。具体来说，他们训练 了GPT-3，这是一款拥有175亿参数、比以前任何非稀疏语言模型都要多的自注意力语言模型，然后测试其在少数样本设置下的表现。在所有任务上，GPT-3都无需梯度更新或微调即可应用，而是在文本交互的情况下对模型进行指定的任务和少数样本演示。GPT-3在许多NLP任务（包括翻译、问答、缺失填入等）中表现出色，还包括一些需要实时推理或领域适应的任务 ，如解开单词、将一个新词放入句子中或执行三进制算术。同时，研究人员还识别了一些大型Web语料库上的任务，其中GPT-3的少数样本学习仍然存在挑战，以及一些任务中的方法问 题，这些问题与在大型Web语料库上训练算法有关。最后，研究人员发现GPT-3可以在人工评估者难以区分的人类文章中生成样本来。他们讨论了这项发现及其广泛的社会影响，以及GPT-3的一般性影响。
&gt; Finished chain. </div>2024-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第14讲打卡~
通过合理地编排多种Tools，一个多功能的智能助手就出来了~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/60/4fa1f3bd.jpg" width="30px"><span>rs勿忘初心</span> 👍（0） 💬（0）<div>比较好奇自然语言-&gt;参数抽取是哪个环节做的？如果的业务自己开发的API，涉及的参数较多（比如4-5个），能很好的处理么？</div>2024-07-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqt6kWhJMrTD7lMTVYiaRe2ru9ibvScXgxaGgoRKOkmB5kNkQpmhfPYT8yoHG9icM542ttxtKYca39kA/132" width="30px"><span>左可</span> 👍（0） 💬（0）<div>(this Thought&#47;Action&#47;Action Input&#47;Observation can repeat N times)\n——老师，这个可以让模型自主决定回溯多少次，如果稍微复杂的问题，是否有可能模型找不到最终答案？这种情况是如何跳出的？使用者是如何控制这个异常场景处理的？</div>2024-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/10/28d5a686.jpg" width="30px"><span>Longerian</span> 👍（0） 💬（2）<div>I should search for the paper with the identifier &quot;2005.14165&quot; on arxiv to find out its innovative points.
Action: arxiv
Action Input: 2005.14165
Observation: Published: 2020-07-22
Title: Language Models are Few-Shot Learners
Authors: Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, Dario Amodei
Summary: Recent work has demonstrated substantial gains on many NLP tasks and
benchmarks by pre-training on a large corpus of text followed by fine-tuning on
a specific task. While typically task-agnostic in architecture, this method
still requires task-specific fine-tuning datasets of thousands or tens 

为何我执行了搜到的论文和文中的不一样，开始胡说八道了。</div>2024-03-14</li><br/>
</ul>