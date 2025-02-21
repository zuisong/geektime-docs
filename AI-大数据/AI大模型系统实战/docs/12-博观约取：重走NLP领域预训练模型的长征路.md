你好，我是Tyler。

上节课，我们学习了计算机视觉领域预训练模型（PTM）的发展历程和重要成果，了解到CNN的平移不变性和边缘提取能力为视觉任务提供了巨大的帮助。

不过你可能会问，上节课学到的 CNN 是根据生物的视觉结构而设计的，我总不能用 CNN 来处理自然语言问题吧？

虽然这样也不是不行，不过NLP领域确实有自己更偏好的模型结构。在这节课，我将带你解决自然语言处理领域所独有的一些问题，重走NLP “长征路”，看看NLP模型预训练技术在黎明前都经历过哪些考验。

## RNN：生而 NLP 的神经网络

我们第一个要学习的模型是循环神经网络（Recurrent Neural Network，RNN），它是一种用于处理“序列数据”的神经网络模型。

RNN引入了循环结构，如下图所示，在RNN中，每个单元都具有一个隐藏状态来存储之前的信息，并将其传递给下一个节点。

如下图所示，每个单元 i 不仅仅接收自身的输入 $x\_i$ 来获取当前步骤的文本信息，同时还接收前一个单元的输出 $h\_{i-1}$ 作为另一部分输入，获得上下文信息的补充。

![](https://static001.geekbang.org/resource/image/cf/82/cf7034a4994bb4aa55951d0494c5d882.jpg?wh=3900x2194)

就像前面学习CNN的时候一样，从生物尤其是人类的智能中寻找灵感这种做法，在AI领域屡见不鲜。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/01/2c/1ab6258c.jpg" width="30px"><span>perfect</span> 👍（2） 💬（1）<div>你好，Tyler，我是做软件工程的，对模型设计的数学原理不太理解。听前面的课程感觉很有趣也能理解，但涉及到模型和算法后，不懂底层数学原路感觉理解起来很吃力。
想请教几个问题
1、是否可以把AI算法&#47;模型当成一个黑盒使用？业界有没有一些黑盒使用手册
2、如果无法黑盒使用模型，针对非AI专业有什么入门学习路径吗？期望达到会使用会调参的水平，数学需要掌握哪些最少知识？</div>2023-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（3） 💬（1）<div>允许后面的人问前面所有的人？那前面的那么多层存在意义在哪里？那干脆把前面的层都铺平让最后一个人挨个问过去，不是更好？没有研究者考虑过这个方向？</div>2023-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8a/47/82c7c347.jpg" width="30px"><span>跳哥爱学习</span> 👍（3） 💬（1）<div>用这个传声筒游戏解释了自注意力机制 太秒了！</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/9d/0f4ea119.jpg" width="30px"><span>周晓英</span> 👍（3） 💬（0）<div>何为 CNN 添加注意力机制：

1. 设计注意力模块:
设计一个注意力模块，该模块能够为每个特征图分配一个权重。这个权重表示模型应该给予该特征图多少注意力。

常见的注意力模块包括 Squeeze-and-Excitation (SE) 模块、CBAM（Convolutional Block Attention Module）等。

2. 集成注意力模块:
将设计好的注意力模块集成到 CNN 的每一层或某些特定层中。例如，可以在每个卷积层之后添加一个 SE 注意力模块。

3. 注意力权重计算:
在前向传播过程中，计算注意力权重。通常，注意力权重是通过对特征图的全局池化、全连接层和激活函数（如 Sigmoid 函数）计算得到的。

4. 特征重标定:
使用计算得到的注意力权重来重标定特征图。通常，这是通过将注意力权重与原始特征图相乘来实现的。

5. 训练和优化:
训练新的 CNN 模型，并通过反向传播算法优化注意力模块的参数和 CNN 的参数，以最小化目标函数。

6. 评估和调优:
评估模型的性能，如果需要，可以调整注意力模块的设计或参数，以进一步提高模型的性能</div>2023-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c4/9d/0f4ea119.jpg" width="30px"><span>周晓英</span> 👍（1） 💬（0）<div>作弊的可能方式：
1.每个参与者可以使用多种方式传递信息，包含语言，动作，文本，图示等。
2.每个参与者可以设法突出最重要的信息，例如将重要内容高亮或者加上音量。
3.每个参与者身上有一个标记，是他们在历史比赛中传递信息准确度的综合评分，帮助后面的人确定权重。</div>2023-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/b6/c9b56731.jpg" width="30px"><span>St.Peter</span> 👍（0） 💬（0）<div>了解了用于NLP的预训练模型，从RNN、LSTM、Transformer.</div>2024-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/3b/dc11df9d.jpg" width="30px"><span>天之痕</span> 👍（0） 💬（0）<div>老师您好，因为长时间都不在这个领域（在数据库领域），最近想了解一下大模型的知识，坚持看了12节，还会坚持看完，很多脉络性的知识都能够了解，但是很多底层算法确实一知半解，基础太差，不知道有什么算法入门类的课程可以推荐下，比如神经网络具体如何实现的，TensorFlow原理是啥？😂</div>2024-02-16</li><br/>
</ul>