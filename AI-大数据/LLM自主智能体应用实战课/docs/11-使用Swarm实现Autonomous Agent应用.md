你好，我是李锟。

在上节课中，我们安装好了 Swarm，运行了第一个例子，然后一起学习了 Swarm 的官方文档。这节课我们把上节课学到的新知识投入实战，基于 Swarm 开发我们的 24 点游戏智能体应用。

我们之前已经基于 MetaGPT、AutoGPT 实现过两次这个应用，这节课要做的工作就是将之前的设计移植到 Swarm。

## 角色建模和工作流设计

首先我们要做的工作还是针对 Swarm 来做角色建模和工作流设计。

从概念上讲，Swarm 应用中的概念其实更接近 AutoGPT。Swarm 的两个核心概念是 Agent（智能体）和 Handoff（移交），Agent 与 AutoGPT 的 Agent 对应，Handoff 对应着 AutoGPT Builder 图形界面中两个 Agent 之间的那些连接关系（连接线以及相关的输入、输出数据）。因此 Swarm 版 24 点游戏智能体应用的角色建模和工作流设计与 AutoGPT 版完全相同，同样也划分为 4 个 Agent：**GameDealer**、**MathProdigy**、**GameJudger**、**GamePlayer**。

我直接把 08 课中的流程图复制过来。

![图片](https://static001.geekbang.org/resource/image/bc/84/bc46948cd46f8529ea921f306374c584.png?wh=878x932)

因为 Swarm 的每一个 Agent 在运行 client.run() 时都需要访问 LLM，而我们之前在实现 MetaGPT、AutoGPT 版的 24 点游戏智能体应用时，MathProdigy 和 GamePlayer 这两个 Agent（或 Role）是没有访问 LLM 的。对于 MathProdigy 和 GamePlayer，貌似最直接的方式是不使用 Swarm 的 Agent，而是用自定义的类来实现。这样做确实也能实现 24 点游戏智能体应用，不过为了展示 Swarm 调用外部函数（外部工具）的能力，也为了代码的一致性，我决定把它们 4 个全部实现为 Swarm 的 Agent。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（1） 💬（2）<div>老师您好，请问这是什么原因造成的呢？
定义玩家 agent, 有函数 get_human_reply_func获取 用户输入。
```python
agent_david = Agent(
    name=&quot;GamePlayer&quot;,
    instructions=get_instruction,
    model=&quot;qwen2.5&quot;,
    functions=[get_human_reply_func],
)
``` 

运行agent 这里，这里有 user_prompt.
```python
    response = client.run(
        agent=agent_david,
        messages=[{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: get_user_prompt(context_var_dict)}],
        context_variables=context_var_dict
    )
    for message in response.messages:
        print(f&quot;message is: {message}&quot;)
    human_reply = response.messages[-1][&quot;content&quot;]
    print(human_reply)
    return human_reply
```
是 client.run() 运行后，是先运行的 get_human_reply_func 吗？ 然后再去获取 user_prompt?  为什么response 会有好几个呢（数学表达式也捕获了，deal 也错误捕获了）？</div>2025-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/79/f098c11d.jpg" width="30px"><span>YX</span> 👍（0） 💬（2）<div>在使用GamePlayer的时候，发现不知道什么原因，当输入算术表达式的时候，模型最后会返回deal，我稍微把提示词改了下：
What&#39;s the human reply of {last_cards_posted}? Just return the human reply itself and do not add anything else, such as &#39;The human reply ...&#39;. If the input is an arithmetic expression, return it as is.</div>2025-02-01</li><br/>
</ul>