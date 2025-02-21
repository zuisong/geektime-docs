你好，我是黄佳。

在启程篇的前两课中，我们学习了如何调用Function，以及Thread（线程）和Run（运行交互对话）的来龙去脉，今天我们稍微轻松一下，讲些没有那么烧脑，相对来说比较简单的内容。我们一起来看看，如何使用Assistants中的Code interpreter做数据分析。

## 什么是 Code interpreter

Code interpreter这个工具的名字有点误导，一开始，我以为它是一个强大的代码分析器，是类似于Github Copilot、CodeLlama这样的工具，能够分析、补全或者生成代码，帮助开发者提高编程效率和代码质量。我想，如果我把一堆程序代码丢进去，Code interpreter应该能帮我分析分析吧（其实ChatGPT不调用任何工具，就已经可以胜任这种代码分析和生成的任务了）。

但是，其实不是，Code interpreter当然可以生成代码，但它的主要的目标工作是帮助我们根据数据文件做数据分析。这里所说的数据分析，是从头到尾的一站式服务——**生成数据分析代码的同时，还能直接运行所生成的代码，并呈现结果**。

用官方的话来说，Code interpreter是一款托管在OpenAI服务器的工具，允许用Python代码读取、处理和分析数据文件。它支持多种常见的文件格式，如csv、json、pdf等，可以对数据进行切片、过滤、排序、分组、聚合等多种操作，而且内置了数据可视化功能，可以一键生成折线图、柱状图、饼图等图表。OpenAI对Code interpreter使用按量计费，每个会话收费0.03美元，会话默认持续1小时。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（1）<div>主要还是怕幻觉吧。生成代码五分钟，检查代码五小时，总体上可能还没人写得快。code interpreter是确保代码至少能跑得起来。</div>2024-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（1） 💬（1）<div>以上这些案例分析来自于实际工作吗？老师能否适当增加实际工作要用到的例子？，谢谢。</div>2024-05-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqk7zaqpGsU3icwictRrJtCrWBibsxkDkjRbKFzkaZ402eibxLaxAicvdZmfjMeV4N30DXyJAjTZA4LxyQ/132" width="30px"><span>Geek_6e7726</span> 👍（0） 💬（1）<div>老师提出的这些问题，后面有专门一章统一回复么？</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a3/4d/59390ba9.jpg" width="30px"><span>排骨</span> 👍（0） 💬（1）<div>自然语言处理（NLP）和生成式预训练模型（如GPT-4）的发展确实使得与计算机的交互变得更加直观和自然。然而，这并不意味着编程技能将变得不再重要。相反，编程技能和自然语言交互能力可以互补，共同提升数据分析人员的职业竞争力。</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a1/d3/2f691222.jpg" width="30px"><span>Simon WZ</span> 👍（0） 💬（0）<div>这样子看，其实这Function calling和Code Interpreter的功能在GPT中都也有，那使用Assistants跟直接调用GPT最明显区别是什么？</div>2024-06-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8qibAw4lRCic1pbnA6yzQU3UqtQm3NqV1bUJ5EiaUnJ24V1yf4rtY7n2Wx7ZVvTemqq5a61ERWrrHA/132" width="30px"><span>Alex</span> 👍（0） 💬（0）<div>def create_assistant(instructions, file_path):
    with open(file_path, &quot;rb&quot;) as file:
        file_obj = client.files.create(file=file, purpose=&#39;assistants&#39;)
        file_id = file_obj.id

    assistant = client.beta.assistants.create(
        instructions=instructions,
        model=&quot;gpt-4&quot;,
        tools=[{&quot;type&quot;: &quot;code_interpreter&quot;}],
        file_ids=[file_id]
    )
    return assistant
老师这里的file_ids好像应该去掉吧？ 查看文档 https:&#47;&#47;platform.openai.com&#47;docs&#47;api-reference&#47;assistants&#47;createAssistant  这里如果是tool 为 file_search的场景的话 用tool_resources读取文件向量 
请老师指教下 是不是我理解错了？
</div>2024-06-10</li><br/>
</ul>