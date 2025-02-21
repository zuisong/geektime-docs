你好，我是叶伟民。

上一节课我们看到，使用RAG改造之后的MIS系统，从以前的通过增删改查界面与数据交互变成了通过一问一答的对话模式交互。是的，所有RAG应用本质上都是通过对话模式交互的，即使少数看起来不是对话模式的RAG应用（例如后面几节提到的返回结构化数据的应用），其底层也是通过对话模式交互的。

今天我们就来深入探索上一节课的基础对话模式，为后面的实现环节打好基础。

## 对话模式以及相关概念

对话模式顾名思义，就是两个角色进行对话。体现在RAG里面，就是用户与AI进行对话。例如：

```sql
用户：客户A的款项到账了多少？
AI：已到账款项为57980。
```

### 用户、AI与系统

在RAG里面，以上例子中的用户一般称为**user**（就是用户的英文），但是AI一般称为 **assistant**（助理的英文）。

比较特殊的是，从ChatGPT（GPT3.5）开始，OpenAI新增了一个角色——**system**（系统的英文），这个角色有助于设置助理的行为。你可以在system角色里面，描述助理在整个对话过程中应该如何表现。于是如果你使用OpenAI的大模型，上述用例就会变成这样：

```sql
系统：你是一个ERP MIS系统
用户：客户A的款项到账了多少？
AI：已到账款项为57980。
```
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（8） 💬（2）<div>第2讲打卡~
思考题：这种多轮对话的场景，通常需要系统支持Memory记忆功能，简单来说就是将用户与LLM的聊天记录保存下来，并在下次生成内容时传递给LLM。常用的记忆模式包括缓冲记忆、摘要记忆、混合记忆、向量数据库记忆等等，这些功能在LangChain中大多包含了内置的组件。关于Memory系统的实现，感兴趣的同学可以参考下我的文章：https:&#47;&#47;blog.csdn.net&#47;weixin_34452850&#47;article&#47;details&#47;141716143</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c5/76/e269369e.jpg" width="30px"><span>明辰</span> 👍（2） 💬（1）<div>老师，我仔细看了您的课，有3个问题想请教一下
1、对话中输入的内容，我们一般全部放到role里，但是OpenAI额外增加了system，哪些指令应该放到system中，哪些放到role中
2、您提到编码、融合过程，是不是可以理解为这部分已经由基座模型实现了，一般我们不需要太多关注
3、您提到的“外部知识组装”环节应该怎么理解，是说检索到的信息需要改写成固定的格式再给到模型嘛
期待老师的解答～</div>2024-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/dd/61/544c2838.jpg" width="30px"><span>kevin</span> 👍（2） 💬（1）<div>在编码阶段，将历史问答进行压缩</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/89/2e2211d3.jpg" width="30px"><span>NEO</span> 👍（1） 💬（1）<div>提问--&gt;LLM对问题进行完善丰富--&gt;向量数据库根据完善后的提问进行检索---&gt;编码--&gt;融合--&gt;生成--&gt;prompt反馈--&gt;优化......</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（1） 💬（1）<div>请教两个问题：
1. 系统角色在其他主流LLM支持吗 比如claude&#47;gemini&#47;grok
2. 超长窗口的LLM不断出现，会给RAG带来任何影响吗，比如https:&#47;&#47;magic.dev&#47;blog&#47;100m-token-context-windows</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/36/0a/a14b6af4.jpg" width="30px"><span>叶绘落</span> 👍（0） 💬（1）<div>将一万次对话进行切片，如每 10 、100 次对话为一个切片（每个切片进行持久化存储），将前一个切片交给 LLM 归纳总结，归纳结果作为下一个切片的上下文，以此类推，最终得到一万次对话的最终归纳结果，并将其持久化存储。

如有新提问，就以最终归纳结果和最近的一个对话切片作为上下文，结合新提问，交给 LLM 处理。</div>2024-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QD6bf8hkS5dHrabdW7M7Oo9An1Oo3QSxqoySJMDh7GTraxFRX77VZ2HZ13x3R4EVYddIGXicRRDAc7V9z5cLDlA/132" width="30px"><span>爬行的蜗牛</span> 👍（0） 💬（1）<div>方式一：对一万次会话进行总结，提取要点再作为Memory.
方式二：切片去最近的部分。</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/94/9c/0af40494.jpg" width="30px"><span>Geek小马哥</span> 👍（0） 💬（0）<div>这个老师讲得好: 假传万卷书, 真传一案例.</div>2025-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/16/cf/bfde35d6.jpg" width="30px"><span>alue</span> 👍（0） 💬（0）<div>请问老师，RAG的能力是不是受限于推理上下文的大小？如果本地部署一个大模型，例如Qwen2.5-7b, 推理上下文大小是受限于硬件资源呢还是受限于模型本身？
</div>2025-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（0）<div>长期记忆压缩存储关键信息。</div>2024-09-25</li><br/>
</ul>