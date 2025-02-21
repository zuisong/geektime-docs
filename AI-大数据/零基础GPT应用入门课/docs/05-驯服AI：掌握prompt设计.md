你好，我是键盘，我们继续驯服 GPT。

刚开始设计 prompt 的时候，通常会走 2 个极端。要么是缺乏背景的简陋提问，要么是一大段拥挤的描述，结构化和可读性欠佳。这样不仅容易遗漏，交给 GPT 执行的效果也不尽如人意。

其实，这是因为你的需求没有梳理好就开跑了，要不就是缺乏示例，AI 理解不到你要的细节。

想要得到相对合心意的回答，合理的顺序是“先劳心，再劳力”，把更多的精力放在前置的思考环节。

那么，怎么梳理自己的需求呢？从混乱到秩序、从简陋到简洁（未必是简单），怎么将问题设计成清晰、有效的 prompt？

![图片](https://static001.geekbang.org/resource/image/1d/ee/1da09f2400dd20f9558e10d7577abeee.png?wh=1142x272 "简洁是终极的复杂 ——  列昂纳多·达·芬奇")

这节课我们来实操一下。通过让 ChatGPT 扮演一位“重磅好书推荐助手”，掌握需求拆分、prompt 规划方法和 prompt 设计框架参考，帮助你有效提问，在提问过程中使用一些 prompt 工程技巧来提升效果。最后，我们也会针对结果做一个综合评估，完成闭环。

## **什么是清晰、明确的需求？**

“清晰、明确的需求”是指准确地、简洁地描述要解决的问题，有足够的背景信息和细节要求，并且容易被 AI 理解和实现**。**了解这个关键技能，不仅能够让ChatGPT的输出更贴近预期，在向上汇报或工作沟通的时候，都会让你事半功倍。

想要表达出清晰、明确的需求，我们可以分为 3 步走：明确需求并拆分，提供必要背景信息，补充细节约束。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/37/9c/3f/c7a8b950.jpg" width="30px"><span>曾雪姣</span> 👍（4） 💬（1）<div>有图文、excel功能的都需要在GPT4上面实现了吧</div>2023-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/27/b8/33244767.jpg" width="30px"><span>阿白</span> 👍（2） 💬（1）<div>感觉挺难的，大家学的都轻松吗？看完一章，不手写点笔记都感觉抓不住</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/3e/c1725237.jpg" width="30px"><span>楚翔style</span> 👍（2） 💬（1）<div>我用GPT4感觉没必要用prompt,我用大白话讲它也能懂,需要啥再补充迭代    模板化的prompt只不过是输出格式好看点</div>2023-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/be/e7c7bb94.jpg" width="30px"><span>福禄妹妹</span> 👍（1） 💬（1）<div>这些也适用于国产化的产品么：kimi、文心一言 之类的
因为gpt使用门槛有点高</div>2024-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/05/ca/e22f4bf5.jpg" width="30px"><span>神经蛙</span> 👍（1） 💬（1）<div>训练的prompt 能分享下吗？</div>2023-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（1）<div>内容太硬了，准备先通读一遍，再回过头一节一节实践</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（2） 💬（3）<div>老师，荐书助手prompt里的图片![通用](https:&#47;&#47;s.mj.run&#47;eq31FdWhom8) 质量好高啊，有开放接口让GPT根据内容自动去查询么？</div>2023-06-27</li><br/><li><img src="" width="30px"><span>Geek_a9ebb3</span> 👍（0） 💬（0）<div>GPT更新到4o了&#xff0c;你们有更新吗
</div>2024-09-10</li><br/><li><img src="" width="30px"><span>Geek_a9ebb3</span> 👍（0） 💬（0）<div>先全部过一遍&#xff0c;然后仔细听&#xff0c;最后遍跟着练习。
</div>2024-09-10</li><br/>
</ul>