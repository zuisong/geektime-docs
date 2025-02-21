你好，我是李锟。

在上节课中，我们学习了 MetaGPT 的基础概念，并且初步体验了 MetaGPT 的使用方法。在第一课中我们已经讨论过待开发的第一个 Autonomous Agent 应用的需求，即一个陪伴用户玩24点游戏的智能体应用。在这一课中我们把这个需求实现为可运行的代码。按照魔术师刘谦老师的话说：见证奇迹的时刻到了！

## 角色建模和工作流设计

从上一课中我们已经了解到，多 Agent 应用是基于 Role Playing 来实现的。为了实现这个应用的需求，我们首先需要思考的是，在这个应用中我们最少需要创建几个角色。这里我出于方便借用了软件工程中的“**角色建模**”这个术语，不过两者概念还是有些差异的。

- 因为这个游戏是提供给人类用户使用的，首先要有一个人类用户作为游戏玩家，我们给这个角色 (Role子类) 取名 GamePlayer，其 name 属性设置为 David。
- 这个游戏确实有较高难度，人类用户很多时候自己搞定比较困难，因此需要求助于一个程序实现的角色。这个程序角色擅长给出满足24点游戏规则的表达式，我们给这个角色 (Role子类) 取名 MathProdigy (数学神童)，其 name 属性设置为 Gauss (高斯)。
- 系统还需要有一个游戏裁判，负责发牌和对上述两个角色给出的表达式做检查，并且控制流程的顺利进行。人类用户只是游戏的玩家，并不是游戏的裁判，否则就不公平了。我们给这个角色 (Role子类) 取名 GameJudger，其 name 属性设置为 Peter。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>mxzjzj</span> 👍（2） 💬（1）<div>有没有交流群啊</div>2025-01-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKicUXKVXIQAmToH3CkpQGjjDHRGSh0RjBpUf82r9WibfrrJMHxZXcuNVgCy8icpI9Mo4He8umCspDDA/132" width="30px"><span>Geek_8cf9dd</span> 👍（0） 💬（1）<div>老师，完整源代码在哪里可以下载</div>2025-02-21</li><br/><li><img src="" width="30px"><span>mxzjzj</span> 👍（0） 💬（1）<div>学完这课，不知道从哪里开始下手，需要本地先部署大模型吗</div>2025-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwViav94kcF53iaAmWUpmicVQAFudhLLadoRdl2JEAE9Bv1rzpXhx1KlrMFddmMgOCx0XXprOyaYDaA/132" width="30px"><span>Geek_30bdf2</span> 👍（0） 💬（1）<div>我发现一个问题，如果让它不返回步骤只返回结果，则很容易出现错误答案，但是如果有步骤，那就会计算正确了，这是什么原因?
### 分析步骤

1. LLM的计算行为差异分析：
   - 无步骤时：可能使用快速直觉判断
   - 有步骤时：被迫进行详细计算

2. 这种现象的原因：
   - 链式思考(Chain-of-Thought)效应
   - 当需要展示步骤时，LLM被迫进行更严谨的思考
   - 类似人类解题：写出步骤会更仔细

### 改进建议

```python


class CheckExpression(Action):
    PROMPT_TEMPLATE: str = &quot;&quot;&quot;
    你是一个精确的计算器。请按以下格式回答：
    
    步骤：
    1. 计算 {expression} = [你的计算过程]
    2. 计算 |结果 - 24| = [差值计算]
    3. 判断差值是否 &lt; 0.1
    
    答案：[只返回True或False]
    &quot;&quot;&quot;
```

关键点：
- 强制LLM展示计算步骤
- 在最后单独返回True&#47;False
- 计算过程和结果分离

这样设计可以：
1. 确保LLM进行完整计算
2. 保持最终输出简洁
3. 便于调试和验证</div>2025-02-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwViav94kcF53iaAmWUpmicVQAFudhLLadoRdl2JEAE9Bv1rzpXhx1KlrMFddmMgOCx0XXprOyaYDaA/132" width="30px"><span>Geek_30bdf2</span> 👍（0） 💬（1）<div>在v2版本输入后中出现了
Traceback (most recent call last):
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;utils&#47;common.py&quot;, line 664, in wrapper
    return await func(self, *args, **kwargs)
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;roles&#47;role.py&quot;, line 551, in run
    rsp = await self.react()
AttributeError: &#39;NoneType&#39; object has no attribute &#39;group&#39;

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;utils&#47;common.py&quot;, line 650, in wrapper
    result = await func(self, *args, **kwargs)
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;team.py&quot;, line 134, in run
    await self.env.run()
Exception: Traceback (most recent call last):
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;utils&#47;common.py&quot;, line 664, in wrapper
    return await func(self, *args, **kwargs)
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;roles&#47;role.py&quot;, line 551, in run
    rsp = await self.react()
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;roles&#47;role.py&quot;, line 520, in react
    rsp = await self._react()
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;MetaGPT&#47;metagpt&#47;roles&#47;role.py&quot;, line 475, in _react
    rsp = await self._act()
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;learn_metagpt&#47;autonomous_agent&#47;lesson_04&#47;game_judger_v2.py&quot;, line 92, in _act
    check_result = await todo.run(msg.content)
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;learn_metagpt&#47;autonomous_agent&#47;lesson_04&#47;game_judger_v2.py&quot;, line 69, in run
    check_result = extract_result(rsp)
  File &quot;&#47;root&#47;autodl-tmp&#47;work&#47;learn_metagpt&#47;autonomous_agent&#47;lesson_04&#47;game_judger_v2.py&quot;, line 32, in extract_result
    result = eval(search_obj.group(1))
AttributeError: &#39;NoneType&#39; object has no attribute &#39;group&#39;
的情况，请问是什么原因呢</div>2025-01-30</li><br/>
</ul>