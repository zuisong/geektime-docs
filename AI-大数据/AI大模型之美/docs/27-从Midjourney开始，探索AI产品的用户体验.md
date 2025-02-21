你好，我是徐文浩。

学到这里，这个课程终于到了尾声。过去的二十多讲里，我们围绕着文本、语音、视频、图像体验了大量的AI应用场景。不过在这些场景里，我们还只是通过撰写代码体验了AI的能力。那么，如果我们今天想通过学习到的这些知识，开发一个真正的AI应用，需要注意些什么呢？我们是只需要简单地给我们的Python代码封装一个对话框一样的用户界面就可以了吗？

如果你有这样的疑惑，那请一定要坚持学完这最后一讲。我们一起来看看Midjourney这个AI画画的应用是怎么做的。它在整个应用的体验里考虑了哪些设计原则？毕竟，Midjourney在过去一年里可谓是创造了一个AI产品的奇迹。它没有独立的App，完全依赖Discord这个语音社区聊天工具和用户交互。团队只有十几个人，但是出图的质量始终领先于有整个开源社区支持的Stable Diffusion。没有外部融资，却完全靠用户订阅获取了1亿美元的年收入。

无论从哪个角度来看，Midjourney都是一个值得研究的AI产品。在它所有的产品设计里，我认为有三个要点是今天所有的AI应用都应该借鉴的，那就是**以用户社区作为入门教程、给用户即时反馈以及搭建数据飞轮以迭代模型**。下面我们一个一个来看。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（22） 💬（1）<div>今天的第27课是徐文浩老师的 &quot;AI 大模型之美&quot;系列讲座的收官之作，感觉来得很突然，都因心中还有期待。徐老师用短短的27讲，通过精心的安排，将 AI世界的各个触角展现在我们眼前，直接上手的实例体验更有拨云见日之功效。当我们亲手推开那一扇扇大门时，神秘变成自然。

Embedding 是一条线，它将大数据，多模态，深度学习，神经网络，机器学习，大语言模型都串了起来; 随之而来的各类算法，分类，递归，决策，都在忙着处理这些 Embedding，&quot;跳出来&quot;的情感分析，广告推送，&quot;智能&quot;聊天就是再自然不过的事了。

老师在&quot;上手课&quot;之后的第二节就引出了 OpenAI 的 Embedding，寥寥几行代码，其在零启动情感分析上的威力就显露无疑。

Embedding 将&quot;万事万物&quot;映射到高维空间，维数的增加标志着对事物描述得更细，但带来的是对算力需求的急剧增加，处理过程变慢。再经过多层迭代，反馈激励，最后连 AI 自己都说不清是怎么 Embedding的了。

既然是 Embedding, AI 就不可能做到尽善尽美，理解。人也无完人，更不要说一个&quot;失败的触痛&quot;极有可能成为另一个成功的&quot;触发器&quot;。

感谢徐文浩老师的这门课，给出了很多实例，包括对开源库的介绍，及相关重要论文的索引，同时还引发了更多的思考，再次感谢。</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ef/2d/757bb0d3.jpg" width="30px"><span>Toni</span> 👍（10） 💬（1）<div>当ChatGPT4 还在玩waitlist, 新的挑战者已横空出世(https:&#47;&#47;www.anthropic.com&#47;index&#47;100k-context-windows)。
Claude-100k 以一次性读取10万个token，将GPT4甩开3倍有余。这意味着什么呢?

在第六课时我们学的聊天机器人，为了让它记住之前聊的问题，要将以前的聊天内容当作下一轮对话的prompt，再喂给OpenAI，但很快prompt 中的 token 数就超过了最高限制，我们只能裁去之前的内容，或小结，以满足token 数限制的要求，一般几轮对话下来聊天机器人就忘了之前的内容了，这就是应用中的痛点。第七节给文章做总结，第十六节用Langchain 给AI上手段使其&quot;记忆力&quot;变长，到第十九节用Whisper 语音转文字，将大段的录音裁成几段才能处理，都是那个痛点: token 数限制。

Claude-100k 一次性读取10万个token，意味着聊天机器人通天聊几天的内容都记得，7，8万字的书一次性提取中心思想，6小时的音频文件无须裁成数个小文件了。

&quot;好事者&quot;已经在用 Claude-100k 分析拆解 ChatGPT4，看看它到底是个什么&quot;鬼&quot;，因为 ChatGPT4 也无法了解其自身。

我们在见证历史。</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（1）<div>谢谢徐老师，墨问西东集训班再见。</div>2023-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/b3/40e8fa1d.jpg" width="30px"><span>风的叹息</span> 👍（0） 💬（1）<div>确实很棒的课程，意犹未尽啊，老师后续可否对关键的某些技术节点可以加更一二，期待解读</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/82/5b/df97e03c.jpg" width="30px"><span>Santiago</span> 👍（3） 💬（0）<div>感谢老师的课程，极大的拓宽了我的知识面，也对AIGC有了一个很好的认识与理解，再次感谢徐老师！</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/c1/e7a0f04d.jpg" width="30px"><span>JonSlow</span> 👍（1） 💬（0）<div>微软这几天刚发布的 bing.com&#47;create，体验也挺不错，推荐各位同学上手试试</div>2023-05-12</li><br/><li><img src="" width="30px"><span>Geek_d54869</span> 👍（0） 💬（0）<div>感谢精彩课程讲解和分享，产品人收益良多~</div>2023-10-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTILhR0NtpB4fGSHwNG2bnDYohLYtRMAogpOfmuHPhLaqC9GaoB0GtIYPlQzxlEO5icicAQIEVcbzLfQ/132" width="30px"><span>Geek_f92fa7</span> 👍（0） 💬（0）<div>搭建数据飞轮这里，个人部署模型后，也可以收集使用日志数据，来获取优质图片数据来迭代模型呀。</div>2023-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7c/12/7b9a2efb.jpg" width="30px"><span>胡萝卜</span> 👍（0） 💬（1）<div>qq频道接入了midjourney</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（0） 💬（0）<div>课程学完了，感谢徐老师带我进入AI这扇神秘的大门，感谢老师为我解惑</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/fa/7f76ddc2.jpg" width="30px"><span>昱宇</span> 👍（0） 💬（0）<div>非常感谢徐文浩老师带我们进入了AIGC的大门！受益良多！</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a1/6b/f5f94a6f.jpg" width="30px"><span>唐国强</span> 👍（0） 💬（0）<div>感谢徐文浩老师的这门课</div>2023-05-12</li><br/>
</ul>