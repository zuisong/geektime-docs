你好，我是邢云阳。

本章的开始，我从设计出发，为你讲解了用自然语言操控 K8s 需要考虑的要点，这些点从技术角度主要分成两类，一类是云原生时代，用命令、代码等等手段与 K8s 集群资源进行交互的手段；第二类是 AI 时代的开发技巧，比如 prompt 工程等等。

AI 时代的开发技巧实际上是重思维，轻代码的，但云原生的开发手段则是实打实的“内功”。因此我在设计篇后，又花了 4 节课的时间，为你讲解了 client-go 的两种进阶用法，如何用 gin 框架封装 API，以及多云管理工具 Karmada。

那有了思维 + 内功的支持后，本节课我们就可以开启实战，真正打通用自然语言操控 K8s 的全流程了。

我们再来回顾一下[第 5 节课](https://time.geekbang.org/column/article/835895)设计的架构：

![图片](https://static001.geekbang.org/resource/image/ba/b3/ba30da253eebdd58f77762cc9216dcb3.jpg?wh=1623x900)

用户会在一个自然语言前端，向 AI Agent 发送一条 操控 K8s 的 prompt。AI Agent 通过工具调用与 K8s 进行交互，在得到结果后，由大模型判断结果准确性并进行自然语言处理后，反馈给用户。

综上所述，设计分为三个部分，分别是自然语言前端、AI Agent 以及工具。自然语言前端我们使用 kubectl 同款的 cobra 来做成一个命令行前端，AI Agent 依然使用 ReAct，工具已经在第 8、9 节完成，分别是对于单集群资源的增删查以及对多集群的获取集群列表操作，本节课我会补充一个人类工具，用于在删除这样的危险操作前做一下确认。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEK2ms7lkhNWeaZLF5cwnEPiadxeNnk5icGx0P6Nfx8U6iaEYicNjrNpjYbib9vOqfMtXIbUZa65wmFoN9A/132" width="30px"><span>luislin</span> 👍（0） 💬（1）<div>老师， 幻觉问题严重啊，思考过程已经知道要调用工具，但是通义仍然给我假设性的回答，一轮就结束。在 though 后加了提示词，让它碰到与 k8s 兼顾问题，就必须使用工具，不可以随便回答。刚调整完，agent 听话了，过一会再调用，又是幻觉了，直接一本正经的给我胡说八道，连假设这种词语都没了🥲🥲 我应该怎么去解决这个问题啊？</div>2025-01-07</li><br/>
</ul>