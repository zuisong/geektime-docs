你好，我是金伟。

上节课说的Transformer模型是ChatGPT的基础算法，这节课我们来看看ChatGPT在这个基础上做了哪些工程创新。这些工程创新，才是让ChatGPT成名的关键。

大模型领域有一个词叫智能涌现，指的是当模型数据和参数达到一定规模时，大模型自发出现新的能力或行为。这些能力或行为并不是在模型设计初期就有过明确计划或预测的，ChatGPT就是一个典型的例子。

ChatGPT使用了约45TB的训练数据，生成的模型有1750亿个参数，发布时间是在2022年底。在它推出之后，人们惊奇地发现它已经具备了程序员级别的编程能力，以至于很多人都说第一个被AI替代的工种将是程序员。除了编程能力，ChatGPT还涌现了可以媲美人类的其他智能，这也是2023年初AI爆火，各大模型厂商疯狂卷算力和参数的原因。

**那究竟是什么推动了这种智能涌现呢？**目前还没有非常明确的科学解释。这多少有点像古代的“炼丹”故事，现在的大模型厂商只是把数据和参数扔进“炼丹炉”，希望自己成为第一个炼出AGI（通用人工智能）的人。

虽然底层原理尚不清楚，但是从工程上来说，ChatGPT却提供了一份可参考的“炼丹术”，这也正是本节课我想提炼出来分享给你的。大模型的三大核心创新点，Transformer、数据与训练、算力。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（1）<div>业内一直有一些吐槽的声音，说OpenAI就是“大力出奇迹”，只会用更大规模的参数和训练数据来卷大模型，但是实际上，OpenAI在大模型的pre-training、fine-tuning、in-content-learning和AI工程等领域，做出了非常多创新的成果！</div>2024-08-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM59PTNiaDASVicbVaeWBU1WKmOgyHcqVtl85nDwAqDicib1EUKE2RRoU0x0vZctZO4kbPDUTTke8qKfAw/132" width="30px"><span>binzhang</span> 👍（1） 💬（1）<div>copilot may improve 33% coding efficiency; but coding is only a part of software development lifecycle. although it can help write test case and some documentation, software engineer still need to spend lots of time on design, implementation, integration etc.. </div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/57/1cebae66.jpg" width="30px"><span>YOUNG</span> 👍（0） 💬（1）<div>第一次学习还在更新中的可成，希望自己能坚持下去</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/67/94d80726.jpg" width="30px"><span>vincent</span> 👍（0） 💬（1）<div>大模型编程不靠谱我觉得还是因为模型对项目细节需求理解方面</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/99/5038d0a1.jpg" width="30px"><span>黄海洲</span> 👍（0） 💬（1）<div>讲得太好了，追更追更~</div>2024-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（3）<div>ChatGPT预训练阶段怎么是有监督学习？没有搞错吧</div>2024-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>追更，第一时间看完。看完后更好的理解了大模型。然后，边睡边思考。</div>2024-08-09</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkwbyTYtSCx6Qc7cQPnnRWv38Jybh3etziaPmuP8gHcgS6FMxcdftrKgWiamH6fc2iciaicDKDVEwcEibQ/132" width="30px"><span>sami</span> 👍（2） 💬（0）<div>
### 金字塔结构
1. ChatGPT核心工程创新
   1.1 Transformer模型
      1.1.1 Decoder架构
   1.2 数据与训练
      1.2.1 预训练 (45TB数据，1750亿参数)
      1.2.2 模型微调 (指令微调)
      1.2.3 强化学习
   1.3 算力

## 核心概念解释

### 1. Transformer模型

专业解释：Transformer是一种基于自注意力机制的神经网络架构，最初由Google团队在2017年提出，用于自然语言处理任务。

5W2H分析：
- What：一种革命性的深度学习模型架构
- Why：为了提高自然语言处理任务的性能
- Who：由Google研究团队提出
- When：2017年
- Where：在机器学习和自然语言处理领域
- How：使用自注意力机制来处理序列数据
- How much：显著提高了多项NLP任务的性能

生活类比：想象Transformer是一个超级高效的会议记录员。在一个大型会议中，普通记录员可能只能记录下说话最多的几个人的内容。但Transformer能同时关注所有与会者，理解每个人说的话及其上下文关系，最后形成一个全面而连贯的会议纪要。

### 2. Decoder架构

专业解释：ChatGPT采用了Transformer的Decoder部分，专注于生成连贯的、上下文相关的文本。

生活类比：如果把完整的Transformer比作一个翻译公司，有人负责理解外语（Encoder），有人负责写出中文（Decoder）。ChatGPT就像只保留了写中文的部分，但这个&quot;写手&quot;异常厉害，不仅能写出流畅的中文，还能根据上下文创造性地延伸内容。

## 技术原理简述

### 预训练过程

专业解释：ChatGPT的预训练过程是将大量文本数据输入Transformer模型，通过&quot;文字接龙&quot;游戏不断调整模型参数。

生活类比：想象一个超级学霸正在阅读世界上所有的书籍和网页。它不仅记住了内容，还理解了各种知识之间的联系。这个过程就像是从幼儿园到高中的学习阶段，建立了对世界的基本认知。

### 模型微调

专业解释：在预训练模型基础上，使用特定任务的数据集进行进一步训练，以获得专业能力。

生活类比：如果说预训练是上完高中，那么模型微调就像上大学选择专业。例如，给模型&quot;喂&quot;大量翻译数据，就能让它成为翻译高手；输入大量编程代码，它就能成为编程高手。</div>2024-08-16</li><br/>
</ul>