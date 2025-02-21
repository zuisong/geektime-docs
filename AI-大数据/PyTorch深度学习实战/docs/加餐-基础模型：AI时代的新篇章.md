你好，我是方远。

好久不见，我想最近我们每个人都可以感受到AI行业发生着巨大的变化，似乎有点当年iPhone4问世的那种感觉。在这次行业变迁的主角就是最近被提出的基础模型。我们现在聊得最多的ChatGPT，就是一个典型的代表。

如果我们把ChatGPT比作一款应用软件的话，那么基础模型就相当于运行它的操作系统。这次加餐，我们就来聊聊基础模型以及它的代表模型。了解了这些，你将会对新的AI研究有更加宏观深入的理解。

# 基础模型Foundation model

在2021年，斯坦福大学的学者在论文 [On the Opportunities and Risks of Foundation Models](https://arxiv.org/pdf/2108.07258.pdf) 中，以基础模型（Foundation Model）来命名这样的模型。

论文中给出的定义是这样的。

> A foundation model is any model that is trained on broad data (generally using self-supervision at scale) that can be adapted (e.g., fine-tuned) to a wide range of downstream tasks

意思就是说，基础模型是利用大量数据进行训练，可以在广泛的下游任务中通过微调等手段进行应用的模型。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（2）<div>老师好,想问下一个不太专业的问题,就是chatpt这类模型出现之后,与pytorch和tensorflow这些框架的关系是怎样的呢</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/fb/37/791d0f5e.jpg" width="30px"><span>Monin</span> 👍（0） 💬（1）<div>方老师  关于“未来畅想”这部分  作为一名业务开发程序员  深度研究哪块可以更好的抓住未来的大模型趋势 ？ </div>2023-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-16</li><br/>
</ul>