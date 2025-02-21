你好，我是Tyler。

在上一节课中，我们深入探讨了大模型在处理长文本方面的能力。这一能力让我们在面对长篇代码文件或大量文字资料时，能够借助大模型进行高效的分析和处理。然而，即便如此，LLaMA 3 的能力在传统的“对话框”中仍然受到一定的限制。

## 从“对话框”到更广阔的世界

我们都知道，像 ChatGPT 这样的工具最早其实只是一个对话机器人，主要是跟人聊天，功能相对简单。但随着技术的进步，它不再局限于“对话框”里，变成了现在多功能的智能助手。能有这么大的进步，关键在于大模型具备了指令跟随的能力（Instruction Following）。简单说，指令跟随能力就是大模型可以根据用户的指令，通过使用特定的工具，完成一些比较复杂的任务。

比如，现在的 ChatGPT 插件功能就是一个很好的例子。以前 ChatGPT 主要是靠输入输出文本进行对话，而插件功能让它可以调用外部工具，去执行各种任务。不管是查找信息、进行计算，还是和其他软件协同工作，都是可以的。

**指令跟随能力是 LLaMA 3 打破“对话框”限制的核心。**这种能力使模型不仅能理解用户的指令，还能通过调用特定的工具或模块来执行复杂的任务。通过提升指令跟随能力，LLaMA 3 可以实现从简单对话机器人到多功能智能助手的转变。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（1） 💬（0）<div>课程代码地址：https:&#47;&#47;github.com&#47;tylerelyt&#47;LLaMa-in-Action</div>2024-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f8/21/3fa228e6.jpg" width="30px"><span>悟光</span> 👍（3） 💬（0）<div>格式化（如 JSON）的大语言模型输出我觉得会很好和现有的系统集成，标准的输出格式类似一个接口，这个接口已经被现有的系统广泛使用，理想情况下大模型可以应用到现有系统的任何一个模块里面</div>2024-12-09</li><br/><li><img src="" width="30px"><span>edward</span> 👍（2） 💬（0）<div>请问老师 大模型是如何判断什么时候该调用什么工具的。</div>2024-10-18</li><br/><li><img src="" width="30px"><span>Geek_820805</span> 👍（1） 💬（0）<div>改成 prompt = hub.pull(&quot;hwchase17&#47;react&quot;)
tools=[city_code_tool, weather_tool]
agent=create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent,
            tools=tools, verbose=True,
            agent_kwargs={&quot;handle_parsing_errors&quot;: True}
)好用了</div>2024-10-23</li><br/><li><img src="" width="30px"><span>Geek_820805</span> 👍（1） 💬（0）<div>运行代码，最后出现 ValueError: An output parsing error occurred. In order to pass this error back to the agent and have it try again, pass `handle_parsing_errors=True` to the AgentExecutor. This is the error: Could not parse LLM output: `The weather in Beijing is晴 (sunny) with a temperature of 15°C and humidity of 47%.`
看起来tool已经返回结果了，但是llm解析结果出问题了，应该如何解决呢？</div>2024-10-23</li><br/>
</ul>