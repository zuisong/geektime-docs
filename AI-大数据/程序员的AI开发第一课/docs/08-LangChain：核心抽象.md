你好，我是郑晔！

上一讲，我们知道了 LangChain 是一个 AI 应用开发的生态，包括了开发框架、社区生态和扩展生态。其中，**最重要的，也是构成整个生态基础的就是开发框架**。

开发框架为我们提供了构建大模型应用的基础抽象和 LangChain 表达式语言，其中，LangChain 表达式语言是为了提高代码的表达性，要想理解 LangChain，关键点就是理解其中的基础抽象。这一讲，我们就来讨论一下 LangChain 的基础抽象。

## ChatModel

既然 LangChain 是为了构建大模型应用而生的，其最核心的基础抽象一定就是聊天模型（ChatModel）。如果你去查看 LangChain 的文档，估计第一个让人困惑的问题一定就是为什么 LangChain 中既有 LLM，也有 ChatModel？

它俩的关系其实类似于之前我们说的补全接口和聊天补全接口的关系，LLM 对应的是文本到文本的生成，而 ChatModel 则是对应着由 ChatGPT 带来的聊天模式。大部分情况下，推荐使用 ChatModel，即便对于非聊天应用也是如此，如同聊天补全接口几乎可以替代补全接口，ChatModel 几乎可以完全替代 LLM。所以，我们后面的讨论也集中在 ChatModel 上。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（2）<div>新手两个问题：
1. langchain文档里面的例子, streaming时候, `print(chunk.content, end=&quot;&quot;, flush=True)` -- 这个flush干啥的？
2. PromptTemplate和ChatPromptTemplate啥区别？`from langchain_core.prompts import PromptTemplate, ChatPromptTemplate`

---

perplexity pro每月送5刀API额度，可以拿来做这些练习。本节代码在此：https:&#47;&#47;github.com&#47;groklab&#47;misc&#47;blob&#47;main&#47;geektime-llm-zhengye-column&#47;lec08.ipynb</div>2024-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（1）<div>简单总结：ChatModel是核心，其他都是辅助，原来大模型编程和普通编程没什么区别；真正的区别是模型差异和模型的Prompt优化，怪不得会有“Prompt工程师”这个说法</div>2024-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/bd/cbcdc4a6.jpg" width="30px"><span>rOMEo罗密欧</span> 👍（4） 💬（0）<div>请问一下老师有练习环境提供吗？</div>2024-11-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erD8CwHKGGIia1HwRBxy5GxMLTfGGzOeLjrmZ6ich9Ng7bbPia89iaSibbldnV4uiaKNXFcO2vQ3ztibCrDw/132" width="30px"><span>Williamleelol</span> 👍（1） 💬（0）<div>添加JsonOutputParser后生成的prompt如下：生成的最终提示: 列举3部鲁迅的作品. 

 The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {&quot;properties&quot;: {&quot;foo&quot;: {&quot;title&quot;: &quot;Foo&quot;, &quot;description&quot;: &quot;a list of strings&quot;, &quot;type&quot;: &quot;array&quot;, &quot;items&quot;: {&quot;type&quot;: &quot;string&quot;}}}, &quot;required&quot;: [&quot;foo&quot;]}
the object {&quot;foo&quot;: [&quot;bar&quot;, &quot;baz&quot;]} is a well-formatted instance of the schema. The object {&quot;properties&quot;: {&quot;foo&quot;: [&quot;bar&quot;, &quot;baz&quot;]}} is not well-formatted.

Here is the output schema:
```
{&quot;properties&quot;: {&quot;title&quot;: {&quot;description&quot;: &quot;Title of the work&quot;, &quot;title&quot;: &quot;Title&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;description&quot;: {&quot;description&quot;: &quot;Description of the work&quot;, &quot;title&quot;: &quot;Description&quot;, &quot;type&quot;: &quot;string&quot;}}, &quot;required&quot;: [&quot;title&quot;, &quot;description&quot;]}</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（1） 💬（1）<div>请问老师有完整代码提供吗？例如github 代码仓库， 纯小白，文中只是部分代码， 还需要切出去找教程</div>2024-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第8讲打卡~</div>2024-11-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoHHibbxS2gia8LeibibHcaDkyZ9BjxUQsIg9dIic6JwZPAgKLavjlNljl2etaR2eypN8WOib2Kodicf1DQ/132" width="30px"><span>Geek_803ee3</span> 👍（0） 💬（0）<div>老师要是能提供能跑的代码就更好了</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/a6/1fc5435f.jpg" width="30px"><span>江旭东01</span> 👍（0） 💬（0）<div>直接传入文本和使用提示词模版【{&quot;text&quot;:&quot;Welcome to LLM application development!&quot;}】 的区别是什么？这里最终执行还是把后面要翻译的内容替换到前面占位符 text上了，有什么区别？</div>2025-02-09</li><br/><li><img src="" width="30px"><span>Geek_d4f4e7</span> 👍（0） 💬（0）<div>ChatPromptTemplate用StrOutputParser也可以按json返回，只需要在system中添加提示词约束按json返回</div>2025-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/dc/c1a0c142.jpg" width="30px"><span>schwarzeni</span> 👍（0） 💬（0）<div>我所在的公司为内部员工提供了一个大模型服务接口来访问外部的各模型服务，看了一下文档是符合 openapi 接口的，设置了 OPENAI_API_KEY 和 OPENAI_API_BASE 后 langchain 也可以直接用，可以白嫖了 233</div>2025-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（0） 💬（0）<div>用 PromptTemplate 返回的json格式老是变咋办? </div>2024-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>输入：PromptTemplate，框架的规框架 ，用户的规用户；
业务执行：ChatModel，不同的模型有不同的抽象，所有细节都被封装，用户无感知；
输出：OutputParser，按需获取想要的结果。</div>2024-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/e0/3db22579.jpg" width="30px"><span>技术骨干</span> 👍（0） 💬（0）<div>有没有可以让小白直接跑起来的代码</div>2024-12-08</li><br/>
</ul>