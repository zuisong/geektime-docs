你好，我是Tyler。

在上节课，我们一起学习了 OpenAI GPT 1-3 系列的发展历程，你掌握得如何？

目前大部分人都对 GPT-1 到 GPT-3 的工作都比较熟悉，因为它们之间有很清晰的发展脉络，但是对 OpenAI 之后的工作内容却是一头雾水。

我们的认知似乎也停留在 GPT-3 上，因为在我们的印象里，自从GPT-3 问世之后，LLM 的生成内容已经开始变得真假难辨，很难区分出后续模型的细微差别了。

## 达文西诞生

然而，实际情况是，在 GPT-3（Davinci）之后，OpenAI 内部存在着众多不同的“内部版本”。你可能已经非常熟悉像 text-davinci-xxx 这样的 OpenAI API 选项。其实每一个代号的都代表着OpenAI的一次尝试，是大语言模型发展过程中积累的宝贵财富。

所以其实我们今天看到的很多能力，并不是一蹴而就的，背后藏着许多不可忽视的细节。在今天的课程中，我将会带你深入理解 OpenAI 是怎么逐步“试”出 ChatGPT 的，让你从这个经典的颠覆式创新里面得到一些启示。

正如下图所示，自GPT-3之后，OpenAI的发展经历了几个关键阶段，主要包括 CodeX、WebGPT 和 ChatGPT。

![](https://static001.geekbang.org/resource/image/c4/cf/c452febeb3999d1137a4d2faba6f56cf.jpg?wh=1867x948)

## Codex models
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（5） 💬（1）<div>sft model 相对于pretrained model 或base model，有一定的指令识别和意图识别能力，但是产生的内容可能不符合人类期待，所有有一个对齐的过程，因此，我们要如何优化sft model，尤其是符合人类期待的方式优化sft model，这就是reward model 所起的作用。从这个视角看，其实再多找一些“问题-回答对”来微调 sft model 应该也关系不大，但这样成本就比较高了，所以干脆造一个工具 reward model 给 sft model  的产出打分也是个不错的方向。就好比家长、老师会教你说话做事的正确答案，但教的总是有限的，也不一定对，到社会上没人教你，你只能通过别人的脸色、反应来判断做的好或不好。</div>2023-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/d2/a8/194d33ed.jpg" width="30px"><span>lw</span> 👍（1） 💬（2）<div>webgpt是需要手动标注吗，这样工作量太大了</div>2023-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/9d/0f4ea119.jpg" width="30px"><span>周晓英</span> 👍（3） 💬（1）<div>自我循环问题:

如果模型主要依赖自身生成的数据进行训练和优化，可能会出现自我循环（或称为自我确认偏误）的问题。这种情况下，模型可能会在一些错误或偏见上不断自我强化，而不是学习到新的、正确的或更有用的信息。
近亲繁殖的数据问题:

这种情况是指模型主要依赖与原始训练数据非常相似或重复的数据进行训练，可能会导致过拟合和泛化能力的降低。如果模型不断地只看到它自己生成的数据，它可能无法学习到新的知识或改进它的表现。
RLHF（Reinforcement Learning from Human Feedback）与 SFT（Supervised Fine-Tuning）:

RLHF 和 SFT 是两种不同的训练策略。RLHF 通常是通过从人类反馈中学习，以优化模型的性能，而 SFT 是通过有监督的方式，使用标签数据对模型进行微调。
在 RLHF 中，通常会收集人类对模型生成内容的反馈，然后利用这些反馈来指导模型的优化。而 SFT 则是基于一个预先标注的数据集来进行的，通常会有一个明确的损失函数来指导优化。
RLHF 更依赖于模型与环境的交互，而 SFT 更依赖于预先准备好的训练数据。
两者可以结合使用，以提高模型的性能和泛化能力。例如，可以首先使用 SFT 微调模型，然后使用 RLHF 进一步优化模型，或者相反。
为了解决自我循环和近亲繁殖的数据问题，通常需要确保模型在训练过程中有足够多样化的数据，并且有时会结合人类的反馈和外部数据来指导模型的训练和优化。</div>2023-10-02</li><br/>
</ul>