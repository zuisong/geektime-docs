你好，我是Tyler！

在上一节中，我们深入探讨了如何利用 LLaMA 3 增强思维链的频率。尽管我们发现频率增强可以在一定程度上提高思维链的有效性，但这种方法存在系统性不足的问题，可能无法充分挖掘思维链的潜力。为了解决这些问题，我们引入了一种更高级的推理方法——“树状思维链”（Tree of Thought，简称 ToT）。

## 什么是树状思维链？

树状思维链常常被误解为对思维链（Chain of Thought，CoT）的简单树状扩展，然而，这种看法忽略了树状思维链的本质和独特性。实际上，树状思维链不仅是思维链的延展，而是引入了一种全新的思维模式，具有显著的区别和优势。

首先，思维链是一种逐步推理的方法，通过线性链的形式展开，每一步推理紧密相连，逐步接近问题的解决方案。这种方法有效地组织了推理过程，但其局限性在于只能按照单一方向推进，难以全面探索所有可能的思维路径。

你在上一节学习的自一致性（Self-Consistency）方法是一种在思维链中进行朴素分支扩展的策略。它通过生成多个不同的推理路径，并将这些路径的结果进行汇总，以提高最终答案的一致性。虽然自一致性方法在某种程度上增强了推理的可靠性，但仍然局限于对现有路径的汇总，而非系统性地探索不同的思维路径。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/27/c27599ae.jpg" width="30px"><span>术子米德</span> 👍（3） 💬（1）<div>疑问：CoT ToT，是否非Llama专属？如果是大模型共享的方法，跟课程主题对起来，总有点变扭啊</div>2024-11-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4OvKiaF14CVnpTUEibC06vyicltuXrXWKB44K1UERgrzJgVShHiaoicBSvWdQFEGqYHEL0k53GeXRKwpCmiaYof4NMTQ/132" width="30px"><span>漠北</span> 👍（3） 💬（0）<div>希望能结合例子给出完整prompt拆解和状态转移过程细节</div>2024-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/fe/31/b2791e76.jpg" width="30px"><span>靠谱的派大星</span> 👍（0） 💬（0）<div>我是不是可以理解成，COT、SC、TOT是一种思维方式或者行为逻辑，不是模型本身独有的特质，更像是赋予并且加强并特地的训练模型的这种表达能力，来追求结果的准确性，在经过训练的模型上进行预测会更贴切问题的答案，同时提问时也可以通过提示词的方式让模型使用这种思维方式，但带来的是不是token成本的增加，在软件开发中是不是要考虑成本和收益的比例</div>2025-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/22/441c4e51.jpg" width="30px"><span>逐書寄年</span> 👍（0） 💬（0）<div>挺簡單易懂的例子
可是衍伸而來的問題就會是：
1. 如果確保我們有辦法列舉出所有問題空間內的實例（instance）？
2. 問題空間的大小如何評估？
3. 同2，如何評估在給定問題空間大小下，使用大型語言模型的運算成本？

</div>2025-01-06</li><br/>
</ul>