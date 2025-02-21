你好，我是郑晔！

上一讲，我们抛开了 LangChain，基于 OpenAI Python 程序库实现了一个 Agent，主要是为了让你更好地理解 Agent 的运作机理。其中最核心的部分就是一个循环，不断地执行各种动作，直到判断运行的结果是停下来。

现在，你已经知道了 Agent 是怎样运作的，这一讲，我们再回来看看如何用 LangChain 实现一个 Agent，相信有了之前的铺垫，这一讲的代码就比较容易理解了。

## 基于LangChain实现的Agent

从实现的功能上讲，我们这一讲要实现的功能和上一讲是完全相同的，只不过我们采用了 LangChain 的基础设施，代码如下所示：

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def calculate(what: str) -> float:
    """Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary"""
    return eval(what)

@tool
def ask_fruit_unit_price(fruit: str) -> str:
    """Asks the user for the price of a fruit"""
    if fruit.casefold() == "apple":
        return "Apple unit price is 10/kg"
    elif fruit.casefold() == "banana":
        return "Banana unit price is 6/kg"
    else:
        return "{} unit price is 20/kg".format(fruit)


prompt = PromptTemplate.from_template('''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}''')

tools = [calculate, ask_fruit_unit_price]
model = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = agent_executor.invoke({
    "input": "What is the total price of 3 kg of apple and 2 kg of banana?"
})
print(result)
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>AI是自动识别需要调用哪个tool以及需要传入什么作为参数？</div>2025-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（6） 💬（1）<div>我用的grok2，本节代码跑不通。需要清理输入。改动如下：
```
def clean_tool_input(func):
    &quot;&quot;&quot;装饰器：清理传递给工具函数的输入&quot;&quot;&quot;
    @wraps(func)  # 这会保留原始函数的元数据，包括 docstring
    def wrapper(input_str: str, *args, **kwargs):
        # 清理输入，只取第一行并去除空白字符
        cleaned_input = input_str.split(&#39;\n&#39;)[0].strip()
        return func(cleaned_input, *args, **kwargs)
    return wrapper

@tool
@clean_tool_input
def calculate(what: str) -&gt; float:
    &quot;&quot;&quot;Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary&quot;&quot;&quot;
    return eval(what)

@tool
@clean_tool_input
def ask_fruit_unit_price(fruit: str) -&gt; str:
    &quot;&quot;&quot;Asks the user for the price of a fruit&quot;&quot;&quot;
    if fruit.casefold() == &quot;apple&quot;:
        return &quot;Apple unit price is 10&#47;kg&quot;
    elif fruit.casefold() == &quot;banana&quot;:
        return &quot;Banana unit price is 6&#47;kg&quot;
    else:
        return &quot;{} unit price is 20&#47;kg&quot;.format(fruit)
```

完整代码在此：https:&#47;&#47;github.com&#47;groklab&#47;misc&#47;blob&#47;main&#47;geektime-llm-zhengye-column&#47;lec14.ipynb</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（4） 💬（0）<div>第14讲打卡~
LangChain 内置了大量开箱即用的工具，可以参考：https:&#47;&#47;python.langchain.com&#47;docs&#47;integrations&#47;tools&#47;</div>2025-01-24</li><br/>
</ul>