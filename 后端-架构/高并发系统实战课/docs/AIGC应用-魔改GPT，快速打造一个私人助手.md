你好，我是徐长龙。

相信最近你一定听到了不少ChatGPT的讨论，甚至自己也体验过了。

不知道你感觉如何？对于ChatGPT，我印象最深刻的就是它仅仅通过多次对话，就可以按我们期望不断优化输出内容的能力。原本令人头大的文本整理工作，现在我们只需要给ChatGPT下达类似编程指令一样的 Promopt 就可以轻松搞定，这帮助我们节约了不少时间和精力。

不过，现在的ChatGPT还是有局限性的，它收集的资料截止到2021年，并没有最新的内容。另外，token字数上的限制也不太方便，在梳理大量文本或者做总结的场景里使用起来很麻烦。

这节课，我就带你一起基于GPT做点“魔改”，做一个更方便我们使用的私人小助手，这是一个嵌入了Faiss 私有数据库的小助手，它能帮你实现知识库、资料整理（突破默认token字数限制）、内容总结和文章润色等功能。

想实现这个小助手，我们需要用到 Python 3.10、LangChain 0.0.145还有OpenAI 0.27.0（由于这几个开发依赖包比较新还在持续迭代，未来可能会因为依赖包升级导致无法使用情况，届时我会再同步更新）。

## 基础知识及对话接口

想要魔改，先得熟悉一下GPT的基础调用方法，所以我们先热热身，看看如何实现基础的对话。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/0c/1c/07610986.jpg" width="30px"><span>希波莱</span> 👍（0） 💬（1）<div>老师如果想做推荐系统和电商，但引入整套llm 的rag工作流，是不是可以淘汰掉传统的mysql，只用elasticsearch + mongdb + redis就足够了</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>老师向量数据库有没有什么好的教程？</div>2023-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>文章的示例代码，向量数据库能否提供一下测试？</div>2023-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（1）<div>1. 就是结合 CHatGPT 和公司或个人数据库或向量数据库其他的，实现智能客服之类的；
2. 老师的文章中还提及了：多种实现方法和技术，我想系统跟着老师的课程学学，开发开放；
3. 公司目前需要这方面的研发客服啥的，市面上没有这类结合私有数据库开发的[流泪]</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/3d/55653953.jpg" width="30px"><span>AI悦创</span> 👍（0） 💬（5）<div>这个有后续吗？快速打造一个私人助手</div>2023-07-29</li><br/>
</ul>