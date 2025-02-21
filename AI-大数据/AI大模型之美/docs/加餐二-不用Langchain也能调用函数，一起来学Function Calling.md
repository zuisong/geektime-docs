你好，我是徐文浩。

在去年的课程里，我们就说过，像GPT这样的大语言模型，其实并不是全知全能的。无论是简单的算术题，还是想要获取实时的外部信息，如果直接让GPT给出答案，往往会得到错误的结果。

对于这类问题，一个常见的解决方案就是**把大语言模型和自己撰写的程序代码结合起来**。让程序代码解决获取外部的实时信息和精确的数学计算问题，让大语言模型解决语言理解和内容生成问题。然后通过大语言模型的逻辑推理能力，把两者结合起来，通过对用户输入内容的理解，去调用不同的程序代码，最终完成用户的需求。

在前面第14～17课里，我们就介绍过如何使用 Langchain 这个开源框架来做到这一点。而正因为这种方式非常有效，OpenAI 直接在后续的模型里内置了这个能力，也就是我们今天要介绍的 Function Call。

## 通过 Function Call 来计算数学题

### 定义工具方便 Function Call 的调用

我们先通过一个最简单的四则运算的例子，看看怎么使用ChatGPT 的 **Function Call** 的能力。想让 ChatGPT 能够使用“按计算器”的方式，就需要先定义一些“按计算器”的 Function。

```python
import json
def add(x, y):
    return json.dumps({"result" : x + y})

def subtract(x, y):
    return json.dumps({"result" : x - y})

def multiply(x, y):
    return json.dumps({"result" : x * y})

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return json.dumps({"result" : x / y})

def get_tools_definition(function_name, description):
    return {
            "type": "function",
            "function": {
                "name": function_name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "number",
                            "description": "The first number",
                        },
                        "y": {
                            "type": "number",
                            "description": "the second number",
                        },
                    },
                    "required": ["x", "y"],
                },
            },
        }

tools = [
    get_tools_definition("add", "add x to y"),
    get_tools_definition("subtract", "subtract y from x"),
    get_tools_definition("multiply", "x multiply y"),
    get_tools_definition("divide", "x divide y"),
]

```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（3） 💬（0）<div>谢谢徐文浩老师的加餐，并在思考题里提出“连环调用”Function Call的问题。

让AI解决一个比较复杂的工作流程，包括自动规划分割子任务，自动生成子任务调动的排序，执行各个子任务并将结果汇总保存最终反馈给用户，可以考虑使用plan-and-excute框架，参考: https:&#47;&#47;blog.langchain.dev&#47;planning-agents&#47;</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/82/438c8534.jpg" width="30px"><span>longslee</span> 👍（1） 💬（0）<div>思考题：是不是递归场景呀？以前编码时需要程序员设定边界和退出条件，现在把要求提给 ChatGPT 让它去调用。当然它会不会产生递归的调用，我也不清楚哈哈，猜测。</div>2024-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/4c/da/cb29f794.jpg" width="30px"><span>twintel</span> 👍（0） 💬（0）<div>这个是不是可以用来解决最近比较火的9.8和9.11比大小的问题</div>2024-07-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIXat0F1n3doFkZDXiaEqIiaJWKf8zOlbU8MSlLgMGGKufopLib21qeBqficic8viaTxKTglxwgKBevwC1w/132" width="30px"><span>Geek_aecc52</span> 👍（0） 💬（0）<div>良心作者呀，又加餐了</div>2024-06-13</li><br/>
</ul>