你好，我是徐文浩。

上一讲里，我们已经学会了通过AI来进行语音合成。有了语音识别、ChatGPT，再加上这个语音合成，我们就可以做一个能和我们语音聊天的机器人了。不过光有声音还不够，我们还希望这个声音可以是某一个特定的人的声音。就好像在电影《Her》里面那样，AI因为用了影星斯嘉丽·约翰逊的配音，也吸引到不少观众。最后，光有声音还不够，我们还希望能够有视觉上的效果，最好能够模拟自己真的在镜头面前侃侃而谈的样子。

这些需求结合在一起，就是最近市面上很火的“数字人”，也是我们这一讲要学习的内容。当然，在这么短的时间里，我们做出来的数字人的效果肯定比不上商业公司的方案。不过作为概念演示也完全够用了。

## 制作一个语音聊天机器人

### 从文本ChatBot起步

我们先从最简单的文本ChatBot起步，先来做一个和[第 6 讲](https://time.geekbang.org/column/article/643915)一样的文本聊天机器人。对应的代码逻辑和第6讲的ChatGPT应用基本一样，整个的UI界面也还是使用Gradio来创建。

唯一的区别在于，我们把原先自己封装的Conversation类换成了Langchain的ConversationChain来实现，并且使用了SummaryBufferMemory。这样，我们就不需要强行设定只保留过去几轮对话了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（13） 💬（2）<div>特意赶到最新进度的文章给老师留言咨询个问题：
背景：首先，这个课程真的是干货满满，物超所值，感谢老师的辛苦、认真付出！但是，作为一个10来年经验的老码农（现在是区块链方面的架构、研发）总觉得跟得有点吃力，原因是缺少AI方面的基础知识，对课程中的一些库、算法的原理缺少基本的概念认知。当然如果只局限于”过一遍代码、熟练使用“基本是够了，但是我觉得还达不到入门级。所以，特地来请教下老师哪些可以作为入门的一手知识，越精简越好。
问题：能否请老师推荐或者总结归纳下入门AI或者大语言模型的最小基础知识是哪些？（李笑来老师提过的入门一个新领域的MAKE [Minimal Actionable Knowledge and Experience]) 
可能上面的问题有点大，我再缩小下，我的目的不是转行AI领域开发，而是得心应手的使用AI大语言模型开发自己的应用或者提高工作效率，比如使用AI做些财务建议、投研之类的应用。我总觉得只是会调接口，完全不理解基础概念还是无法游刃有余的使用，离开课程，就很难有思路做自主开发了。

说的有点啰嗦了，感谢老师！
</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cc/1d/3c0272a1.jpg" width="30px"><span>abc🙂</span> 👍（3） 💬（2）<div>老师，如果想要AI学习我的写作风格，按照我的风格写作，要怎么训练呢？</div>2023-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（3） 💬（2）<div>这个paddleBoBo都一年没更新啦 还有没有平替或者潜在新产品呢</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（1） 💬（1）<div>现在HeyGen不错 就是收费不低</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/aa/54/bf64d522.jpg" width="30px"><span>劉仲仲</span> 👍（0） 💬（2）<div>出现error:module &#39;pexpect&#39; has no attribute &#39;spawn&#39;,已经是最新的pexpect</div>2023-04-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/RSBuejSw2icwNxLQeW0Xs6ib9pedqEhB7h6kYbOdaxiaUbLz2xSxE2e7e0yHneLicBCkmnhQ4QSuzKx0K5aUaeyaQQ/132" width="30px"><span>粉墨之下</span> 👍（0） 💬（1）<div>本地运行后，回复时报错：Retrying langchain.llms.openai.completion_with_retry.&lt;locals&gt;._completion_with_retry in 4.0 seconds as it raised APIConnectionError: Error communicating with OpenAI: HTTPSConnectionPool(host=&#39;api.openai.com&#39;, port=443): Max retries exceeded with url: &#47;v1&#47;completions (Caused by NewConnectionError(&#39;&lt;urllib3.connection.HTTPSConnection object at 0x000001F9C7DAD670&gt;: Failed to establish a new connection: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。&#39;)).</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/95/50/01199ae9.jpg" width="30px"><span>一叶</span> 👍（0） 💬（2）<div>刚看了下,这个did的价格不是一般的贵....</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>txt = gr.Textbox(show_label=False, placeholder=&quot;Enter text and press enter&quot;).style(container=False)
官网文档也都没有.style(container=False)</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>audio = gr.Audio(source=&quot;microphone&quot;, type=&quot;filepath&quot;)
老师这段代码没有source属性，这个属性是sources才可以，可能写错了哈哈哈
audio=gr.Audio(sources=&quot;microphone&quot;, type=&quot;filepath&quot;)</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/28/40/82d748e6.jpg" width="30px"><span>小理想。</span> 👍（0） 💬（0）<div>https:&#47;&#47;cdn.discordapp.com&#47;attachments&#47;1065596492796153856&#47;1095617463112187984&#47;John_Carmack_Potrait_668a7a8d-1bb0-427d-8655-d32517f6583d.png
老师这个地址访问不了，是不是我需要把文件下载下来自己映射一下哈</div>2023-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>如果能有一个完整的数字人开源方案就好了</div>2023-07-12</li><br/>
</ul>