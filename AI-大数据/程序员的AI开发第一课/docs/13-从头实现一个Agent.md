你好，我是郑晔！

上一讲，我们已经从概念上了解了 Agent。你现在知道 Agent 其实也是一个软件系统，只不过，因为有了大模型的加持，它有了一个可以做“自主”推理的大脑，完成很多“智能”的工作。

这一讲，我们来实现一个 Agent。不同于之前借助 LangChain，这次我们会用更底层的方式实现一个 Agent，帮助你更好地理解 Agent 的运作原理。

我们构建这个 Agent 会基于 ReAct 来实现，我们在 [04 讲](https://time.geekbang.org/column/article/822235)介绍过，ReAct 表示 Reasoning + Acting，也就是推理和行动。采用这个模式，要经历思考（Thought）、行动（Action）、观察（Observation）三个阶段。

大模型会先思考要做什么，决定采用怎样的行动，然后在环境中执行这个行动，返回一个观察结果。有了这个观察结果，大模型就会重复思考的过程，再次考虑要做什么，采用怎样的行动，这个过程会持续到大模型决定这个过程结束为止。

我们的实现代码参考了 Simon Willison 的一篇[文章](https://til.simonwillison.net/llms/python-react-pattern)，这篇文章介绍了如何用 Python 实现 ReAct 模式。

## 基础的聊天机器人

我们先来实现一个基础的聊天机器人：

```python
from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"
client = OpenAI()

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def invoke(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=self.messages,
            temperature=0
        )
        return completion.choices[0].message.content
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/87/c1/e9e688c2.jpg" width="30px"><span>hellotong</span> 👍（1） 💬（1）<div>深入浅出👍</div>2024-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/c4/5a3686af.jpg" width="30px"><span>kergee</span> 👍（0） 💬（1）<div>和 Function Calling 的区别呢？</div>2025-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（0）<div>挺好玩的：
```
query(&quot;三公斤苹果和两公斤香蕉的总价？&quot;)
---
Thought: To calculate the total price of three kilograms of apples and two kilograms of bananas, I first need to know the unit price of each fruit.

Action: ask_fruit_unit_price: apple
PAUSE
 -- running ask_fruit_unit_price apple
Observation: Apple unit price is 10&#47;kg
Thought: Now that I have the price of apples, I need to ask for the price of bananas to proceed with the calculation.

Action: ask_fruit_unit_price: banana
PAUSE
 -- running ask_fruit_unit_price banana
Observation: Banana unit price is 6&#47;kg
Thought: I now have the unit prices for both apples and bananas. I can calculate the total price by multiplying the quantity of each fruit by its unit price and then summing these amounts.

Action: calculate: 3 * 10 + 2 * 6
PAUSE
 -- running calculate 3 * 10 + 2 * 6
Observation: 42
Answer: 三公斤苹果和两公斤香蕉的总价是42元。
```

本节代码在此：https:&#47;&#47;github.com&#47;groklab&#47;misc&#47;blob&#47;main&#47;geektime-llm-zhengye-column&#47;lec13.ipynb</div>2024-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第13讲打卡~</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/7f/7b1f3f68.jpg" width="30px"><span>willmyc</span> 👍（1） 💬（0）<div>老师，您好有几个问题 1.query(&quot;What is the total price of 3kg of apple and 2kg of banana?&quot;)这个prompt和输出的不匹配 2.re.compile 需要导入包，import re 3.为了方便理解，老师后续的代码是否可以增加一点注释，谢谢您！</div>2024-11-29</li><br/>
</ul>