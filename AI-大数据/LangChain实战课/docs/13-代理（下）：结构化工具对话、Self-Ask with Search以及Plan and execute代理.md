你好，我是黄佳，欢迎来到LangChain实战课！

在上一讲中，我们深入LangChain程序内部机制，探索了AgentExecutor究竟是如何思考（Thought）、执行（Execute/Act）和观察（Observe）的，这些步骤之间的紧密联系就是代理在推理（Reasoning）和工具调用过程中的“生死因果”。

现在我们趁热打铁，再学习几种更为复杂的代理：Structured Tool Chat（结构化工具对话）代理、Self-Ask with Search（自主询问搜索）代理、Plan and execute（计划与执行） 代理。

## 什么是结构化工具

LangChain的第一个版本是在 2022 年 11 月推出的，当时的设计是基于 ReAct 论文构建的，主要围绕着代理和工具的使用，并将二者集成到提示模板的框架中。

早期的工具使用十分简单，AgentExecutor引导模型经过推理调用工具时，仅仅能够生成两部分内容：一是工具的名称，二是输入工具的内容。而且，在每一轮中，代理只被允许使用一个工具，并且输入内容只能是一个简单的字符串。这种简化的设计方式是为了让模型的任务变得更简单，因为进行复杂的操作可能会使得执行过程变得不太稳定。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_617b3f</span> 👍（4） 💬（2）<div>老师请问下，ReAct框架的原理是：”大语言模型可以通过生成推理痕迹和任务特定行动来实现更大的协同作用。引导模型生成一个任务解决轨迹：观察环境 - 进行思考 - 采取行动，也就是观察 - 思考 - 行动。那么，再进一步进行简化，就变成了推理 - 行动，也就是 Reasoning-Acting 框架。“ 
那么Plan and execute的方式对做Plan的那个大模型的要求不是更高么？因为做计划的那个大模型，直接就根据问题做计划了，过程中没有接收任何反馈，不像ReAct方式那样，中间是接收一些信息的。
另外这个做计划的过程，不是思维链的过程么，还是有什么区别呢？
所以…… 不是很理解为何Plan and execute是一个更灵活、更新的一种方式。还请老师答疑解惑，谢谢！</div>2023-11-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（4） 💬（1）<div>老师节日快乐。</div>2023-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（2） 💬（4）<div>使用结构化工具对话代理的实例代码报错，请问怎么改？。具体输出如下：
Traceback (most recent call last):
  File &quot;&#47;Users&#47;abc&#47;project&#47;python&#47;learnlangchain&#47;struct_tool.py&quot;, line 17, in &lt;module&gt;
    agent_chain = initialize_agent(
                  ^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;agents&#47;initialize.py&quot;, line 57, in initialize_agent
    agent_obj = agent_cls.from_llm_and_tools(
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;agents&#47;structured_chat&#47;base.py&quot;, line 132, in from_llm_and_tools
    _output_parser = output_parser or cls._get_default_output_parser(llm=llm)
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;agents&#47;structured_chat&#47;base.py&quot;, line 65, in _get_default_output_parser
    return StructuredChatOutputParserWithRetries.from_llm(llm=llm)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;agents&#47;structured_chat&#47;output_parser.py&quot;, line 82, in from_llm
    output_fixing_parser = OutputFixingParser.from_llm(
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;output_parsers&#47;fix.py&quot;, line 45, in from_llm
    return cls(parser=parser, retry_chain=chain)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File &quot;&#47;opt&#47;homebrew&#47;lib&#47;python3.11&#47;site-packages&#47;langchain&#47;load&#47;serializable.py&quot;, line 74, in __init__
    super().__init__(**kwargs)
  File &quot;pydantic&#47;main.py&quot;, line 339, in pydantic.main.BaseModel.__init__
  File &quot;pydantic&#47;main.py&quot;, line 1076, in pydantic.main.validate_model
  File &quot;pydantic&#47;fields.py&quot;, line 860, in pydantic.fields.ModelField.validate
pydantic.errors.ConfigError: field &quot;retry_chain&quot; not yet prepared so type is still a ForwardRef, you might need to call OutputFixingParser.update_forward_refs().
</div>2023-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/8c/791d0f5e.jpg" width="30px"><span>SH</span> 👍（1） 💬（1）<div>老师， 把离散的文档及其他信息做嵌入，存储到向量数据库中，然后再提取的过程。 这类利用大模型的时候（比如：openai 的 api） 这类的数据是否会被大模型 获取到？  导致信息泄露～</div>2023-11-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（1） 💬（1）<div>老师，在使用plan and execute代理时，推理的上下文比较大的时候，结果就不太如意了。例如：一个go项目，我要求给指定的方法增加一个日志输出的代码逻辑，然后代理读取了整个源代码文件，最后代码是加了，但是只有那个方法还保留着是完整的，其他的代码就没了。请问这种情况有什么手段可以优化吗？</div>2023-10-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/YflLdCdbUAkfr9LPzF50EibDrMxBibPicQ5NNAETaPP0ytTmuR3h6QNichDMhDbR2XelSIXpOrPwbiaHgBkMJYOeULA/132" width="30px"><span>抽象派</span> 👍（1） 💬（1）<div>老师，agent可以结合chain来用吗？有示例吗？</div>2023-10-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（1） 💬（1）<div>老师好。您平时的工作业务和业务流是什么？</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/49/9d/3b40bd68.jpg" width="30px"><span>Final</span> 👍（1） 💬（1）<div>中秋快乐 ~</div>2023-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（1） 💬（1）<div>老师提下代码</div>2023-09-28</li><br/><li><img src="" width="30px"><span>Geek2808</span> 👍（0） 💬（1）<div>对于StructedToolChat部分，异步总是有问题，可能是VPN网络的问题，改成同步方式跑起来就可以了：
import os
os.environ[&quot;OPENAI_API_KEY&quot;] = &#39;xxxx&#39;

from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_sync_playwright_browser

sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()
print(tools)

from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI

# LLM不稳定，异步方式总是得不到结果。尝试使用同步方式
llm = ChatOpenAI(temperature=0.5)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)


def main():
    response = agent_chain.run(&quot;What are the headers on python.langchain.com?&quot;)
    print(response)

main()
</div>2024-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/20/1c/de379ed1.jpg" width="30px"><span>shatu</span> 👍（0） 💬（1）<div>Plan and execute受限于大模型的不稳定性，还是可能出错，而且一步错步步错，这对于复杂多步骤流程还是很有挑战性【Thought:To calculate the number of bouquets that can be purchased, you need to divide 100 by the average price of a bouquet of roses in New York.

Action:
```
{
  &quot;action&quot;: &quot;Calculator&quot;,
  &quot;action_input&quot;: &quot;100 &#47; (63.98 + 56.99 + 18.70)&quot;
}
```


&gt; Entering new LLMMathChain chain...
100 &#47; (63.98 + 56.99 + 18.70)```text
100 &#47; (63.98 + 56.99 + 18.70)
```
...numexpr.evaluate(&quot;100 &#47; (63.98 + 56.99 + 18.70)&quot;)...

Answer: 0.7159733657907926】</div>2023-11-17</li><br/><li><img src="" width="30px"><span>Geek_995b81</span> 👍（0） 💬（1）<div>老师，结构化工具那一个demo，比如模型决定使用 PlayWrightBrowserToolkit 中的 get_elements 工具。这里我们没有给他提示，他是怎么知道用get_elements工具的呢？另外，结构化工具还有其他工具吗？</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（0） 💬（3）<div>老师 请教下  Plan and execute和之前说的ReAct感觉很相似  都可以概括为推理+行动？  那两者的区别是啥？  我个人理解是
①Plan and execute可以由两个LLM代理完成   ReAct一般由一个LLM完成整个推理+行动    
②Plan and execute由多个LLM  可以让推理+行动并行操作   实现fork-join操作  缩短执行时间</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/65/2fb5c4ce.jpg" width="30px"><span>旅梦开发团</span> 👍（0） 💬（2）<div>我这里执行 playwright install  报了以下错误：
Downloading Chromium 117.0.5938.62 (playwright build v1080) from https:&#47;&#47;playwright.azureedge.net&#47;builds&#47;chromium&#47;1080&#47;chromium-win64.zip
Error: read ECONNRESET  大家怎么解决的</div>2023-10-03</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div>***** 修订课程中“使用结构化工具对话代理”部分的代码，改为通义千问，将旧版 langchain的改为新版本
## 旧代码1：
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_async_playwright_browser
from langchain.chat_models import ChatAnthropic, ChatOpenAI
## 新代码1：（ 新版本用 langchain_community 代替 旧版本的 langchain ）
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain_openai import ChatOpenAI
----
## 旧代码2：
llm = ChatOpenAI(temperature=0.5)
## 新代码2：（用千问模型代替 OpenAI )
llm = ChatOpenAI(
    api_key=&quot;KEY&quot;, # 用你的DASHSCOPE_API_KEY
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;, 
    model=&quot;qwen-plus&quot;
    )
----
## 旧代码3：
response = await agent_chain.arun(&quot;What are the headers on python.langchain.com?&quot;)
## 新代码3：（Chain.arun&#39; 方法已弃用，改用 ainvoke ）
 response = await agent_chain.ainvoke(&quot;What are the headers on python.langchain.com?&quot;)

****  修订课程中“使用 Self-Ask with Search 代理”部分的中代码，用通义千问 和Perplexity
## 旧代码4
from langchain import OpenAI, SerpAPIWrapper 
## 新代码4
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatPerplexity
----
## 旧代码5
llm = OpenAI(temperature=0)
search = SerpAPIWrapper()
## 新代码5 
# 用千问大模型初始化 
llm = ChatOpenAI(   
    api_key= &quot;key&quot;,  # 你的DASHSCOPE_API_KEY
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;,  
    model=&quot;qwen-long&quot;)

# 新用Perplexity 初始化网络搜索工具
search = ChatPerplexity(    
    temperature=0.3, 
    pplx_api_key= ”key“,  # 你的PPLX_API_KEY
    model=&quot;llama-3-sonar-small-32k-online&quot;)
---
## 旧代码6
func=search.run,
self_ask_with_search.run( &quot;使用玫瑰作为国花的国家的首都是哪里?&quot;  )
## 新代码6 ，将run方法改为invote
func=search.invoke,  
self_ask_with_search_agent.invoke(&quot;使用玫瑰作为国花的国家的首都是哪里?&quot;) </div>2024-08-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKCbnOvEatUNibJ7oSRw2jrKPFh9wxY1xt5Z5bbRu6PO9cgrJXDKHKAo6u7737icrp0r2kiab77ib4H8Q/132" width="30px"><span>Geek_eeff0f</span> 👍（1） 💬（1）<div>老师，请教下使用SerpAPIWrapper运行提示：
    raise ValueError(
ValueError: An output parsing error occurred. In order to pass this error back to the agent and have it try again, pass `handle_parsing_errors=True` to the AgentExecutor. This is the error: Could not parse output:  No.
是什么原因呢？我在self_ask_with_search = initialize_agent(
    tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
)添加了参数handle_parsing_errors=True，尽管不报错，但是得不到结果</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/42/ac/179015d9.jpg" width="30px"><span>LVEli</span> 👍（0） 💬（0）<div>请教老师，在实际使用中，被测网页是https协议，对浏览器做了如下修改：
async_browser = create_async_playwright_browser(args=[&quot;--ignore_https_errors=true&quot;])
无法访问到，仍然报证书错误。单步调试时，发现大模型没有接收到这里的忽略证书，所以执行的动作是这样的：

&gt; Entering new AgentExecutor chain...
Thought: I will need to navigate to the specified IP address and port to find the webpage title.
Action:
```
{
  &quot;action&quot;: &quot;navigate_browser&quot;,
  &quot;action_input&quot;: {
    &quot;url&quot;: &quot;https:&#47;&#47;xx.xxx.xxx.xx:443&quot;
  }
}

这种情况如何处理呢？</div>2025-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e5/64/ac338f9c.jpg" width="30px"><span>温泉</span> 👍（0） 💬（0）<div>SELF_ASK_WITH_SEARCH  这个在0.2版本如何使用，我的一直在报错msg: parameter check failed, stop word range is [1, 20]</div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第13讲打卡~
Agent真的很强大~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/1b/6f/ee41e363.jpg" width="30px"><span>海是蓝天的倒影</span> 👍（0） 💬（0）<div>我理解agentType在不同的代理类型中包装了不同的代理思维方式和代理工具调用的提示词。通过对问题任务的思考分析，调用有用的工具，得出答案结果。我这么理解对吗？</div>2024-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/10/28d5a686.jpg" width="30px"><span>Longerian</span> 👍（0） 💬（0）<div>Plan and execute 代理也没跑通，没计算出平均价格，很奇怪。

</div>2024-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/62/81a5a17d.jpg" width="30px"><span>ManerFan</span> 👍（0） 💬（0）<div>老师好，在构建agent executor时，具体应该如何选择AgentType呢？</div>2024-02-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKCbnOvEatUNibJ7oSRw2jrKPFh9wxY1xt5Z5bbRu6PO9cgrJXDKHKAo6u7737icrp0r2kiab77ib4H8Q/132" width="30px"><span>Geek_eeff0f</span> 👍（0） 💬（1）<div>from langchain.tools.playwright.utils import create_async_playwright_browser
我安装的是langchain是0.1.0
但是提示我找不到utils 这个包是怎么回事呢？
</div>2024-01-19</li><br/>
</ul>