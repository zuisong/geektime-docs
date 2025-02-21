你好，我是Tyler。

在今天的课程中，我们将深入探讨GPT 1-3的发展历程。GPT的主要内容其实已经体现在它的名字中，它的全称是Generative Pre-trained Transformer，其中集合了我们大模型关注的各种要素，包括预训练大模型（Pre-trained Transformer）和 生成式AI（Generative AI）。

通过上节课的学习，你已经理解了Transformer的工作原理，有了这个基础，我们再来学习GPT系列就相对轻松了。接下来，我们就从GPT-1开始说起。

## GPT-1：学会微调（Finetune）

GPT-1 符合我们之前对预训练模型的美好幻想，就像 CV 领域的预训练模型一样，首先在大规模的数据上进行学习，之后在具体的任务上继续微调。

不过，你可能会问，之前不是说过因为缺乏合适的数据集，所以一直无法制作出适合用在自然语言处理的预训练模型吗。那么，GPT-1 的训练数据是从哪里获取的呢？

这是一个非常好的问题！在这里，我们所说的不是ImageNet那样有标签的数据集，而是 Common Crawl 这类大规模的无标签数据集。

GPT-1 是基于海量的无标签数据，通过对比学习来进行训练的。这个思路来源于从 Word2Vec 到 ELMo 的发展过程中积累的经验。它们都通过在大规模文本数据上进行无监督预训练，学习到了丰富的语言知识。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（2） 💬（1）<div>1. GPT-1先于Bert出现，预训练+微调
2. GPT-2，在训练样本里加入一些特定格式的样本，使用提示来完成下游任务。但此时的提示的任务类型比如是训练样本里已经包含的？
3. GPT-3，训练样本更大，使用提示+少量示例，可以完成训练样本里没见过的下游任务？</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/64/b2/18005d2a.jpg" width="30px"><span>Leo Zhao</span> 👍（0） 💬（1）<div>
ChatGPT 支持多轮对话 能把多轮对话当做上下文 知道下一轮生成  . GPT-3 只是针对当前一轮输入生成输出。</div>2023-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/9d/0f4ea119.jpg" width="30px"><span>周晓英</span> 👍（2） 💬（0）<div>首先，GPT3是一个基座大模型，而ChatGPT是一个应用系统，基于基座大模型可以诞生无数的应用系统，同时应用系统也可以使用不同的基座大模型。此外，目前我用的ChatGPT是基于GPT4的，和3相比，推理能力更强，在用户界面端也做了一定的优化处理（比如用ChatGPT和直接调用GPT公布的API，同一个问题的回答质量是可能存在差异的），GPT4还具备多模态能力。</div>2023-10-02</li><br/>
</ul>