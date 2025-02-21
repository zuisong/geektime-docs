你好，我是南柯。

时隔一年半，在2023年9月OpenAI “悄悄”发布了DALL-E 3这个AI绘画模型。相比Midjourney V5.2、SDXL等时下最强模型，DALL-E 3在长文本文生图、图中写入文字（也就是我们常说的Text-in-Image）等方面优势非常明显。

就在这个月（10月份），OpenAI相继放出了DALL-E 3的[安全审核方案](https://cdn.openai.com/papers/DALL_E_3_System_Card.pdf)和[技术方案](https://cdn.openai.com/papers/dall-e-3.pdf)。它背后所用的技术方案也终于公之于众，刷新了算法工程师对于AI绘画模型的理解。接下来的两讲内容，我们就一起探秘DALL-E 3，带你搞清楚它的技术方案、局限性以及发展趋势。

在我看来，DALL-E 3有两方面的探索最值得我们关注。**一个是如何用生成数据来训练模型，另一个是如何将各种AI绘画模型训练技巧有机地组合起来。**这节课，我会先为你分享DALL-E 3的使用体验，然后结合论文为你深入解读DALL-E 3如何用OpenAI的方式生成数据。

这两年，技术圈围绕能否使用生成数据训练大模型的话题一直争论不休。使用BLIP这类模型为图像生成的描述，无论是用于训练文生图模型，还是训练类似GPT-4 Vision这样的图文问答模型，都没有带来显著的收益。**如今DALL-E 3的成功无疑证实了生成数据用于模型训练的可行性，也将引领下一波用生成数据优化AI绘画模型的趋势**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>沐瑞Lynn</span> 👍（0） 💬（1）<div>极客时间能不能把更新的通知发一下，很多人估计都还不知道有更新吧</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（1）<div>太棒啦，期待下一讲</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（1）<div>分析的很巧妙，感谢加餐</div>2023-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/83/f0/9f063379.jpg" width="30px"><span>我听着呢</span> 👍（0） 💬（1）<div>前排打卡，终于等到了更新</div>2023-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f6/5d/32d96b26.jpg" width="30px"><span>Grace</span> 👍（0） 💬（0）<div>没有用GPT 4 Vison训练所有的数据，是因为GPT 4 Vison，太！贵！啦！</div>2024-02-01</li><br/>
</ul>