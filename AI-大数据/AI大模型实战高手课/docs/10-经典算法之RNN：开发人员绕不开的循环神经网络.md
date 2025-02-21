你好，我是独行。

上一节课的最后我们介绍了神经网络，神经网络有很多种，包括前馈神经网络（FNN）、卷积神经网络（CNN）、循环神经网络（RNN）、图神经网络（GNN）、自注意力机制模型Transformer等。

这节课我们就来学习其中的RNN，它主要用来处理序列数据，为什么我们要学习RNN呢？实际上目前大部分大语言模型都是基于Transformer的，通过学习RNN，我们可以理解神经网络如何处理序列中的依赖关系、记忆过去的信息，并在此基础上生成预测的基本概念，尤其是几个关键问题，比如梯度消失和梯度爆炸等，为我们后面进一步理解Transformer打下基础。

## 循环神经网络

循环神经网络（RNN）是一类用于处理序列数据的神经网络。不同于传统的前馈神经网络，RNN能够处理序列长度变化的数据，如文本、语音等。RNN的特点是在模型中引入循环，使得网络能够保持某种状态，从而在处理序列数据时表现出更好的性能。我们看一下下面的图片。

![图片](https://static001.geekbang.org/resource/image/8a/45/8a7b7d8b1fb825e8a3056efd58037545.png?wh=795x319 "图片源于网络")

左边简单描述RNN的原理，x是输入层，o是输出层，中间s是隐藏层，在s层进行一个循环，右边表示展开循环看到的逻辑，其实是和时间t相关的一个状态变化，也就是说神经网络在处理数据的时候，能看到前一时刻、后一时刻的状态，也就是我们常说的上下文。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/32/c2/ffa6c819.jpg" width="30px"><span>冰冻柠檬</span> 👍（4） 💬（1）<div>独行老师，提个建议哈，示例代码可以换成pytorch吗？</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（1） 💬（1）<div>既然引入 LSTM 可以解决一系列问题，那目前主流的大语言模型为什么没有使用 RNN 架构呢？
原因在于训练效率低。RNN是串行计算，当前计算的输出依赖于前一次计算的隐藏层结果</div>2024-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/78/b0/13b19797.jpg" width="30px"><span>潇洒哥66</span> 👍（0） 💬（1）<div>有一个疑问哈，RNN第一个计算的例子，是不是简化了，感觉矩阵乘法有些问题。</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（13） 💬（0）<div>第10讲打卡~
思考题：主流的大语言模型没有采用RNN，而是采用了Transformer，主要是因为RNN没法处理长序列。由于文中提到的梯度消失和梯度爆炸等问题，RNN模型没法捕捉到距离较远的文本之间的依赖关系，但是这并不符合人类的语言习惯。比如这样一段话：&quot;我喜欢旅行，并不喜欢上班，因为这能让我感受到自由&quot;，里面的&quot;这&quot;实际上指代的是&quot;旅行&quot;，而并不是距离它更近的&quot;上班&quot;。</div>2024-06-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/bJjBw4nJOV2VFDibH86RicG3tA92ngUH7R0PRx5yZqhGmcWv5QPjWNFPafOIpDlHZ5BMnQH9a7r0S3Xhqa9w36NA/132" width="30px"><span>wlih45</span> 👍（0） 💬（2）<div>大家rnn部分最终的输出是什么呀？</div>2024-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/70/0b67addb.jpg" width="30px"><span>行者无疆</span> 👍（0） 💬（0）<div>自然界中的许多关系都是非线性的，若是模型只能学习线性关系，也就无法准确地拟合这些数据。RNN的输入主要是序列数据，这些数据展示的更多的就是线性关系。激活函数（例如ReLU）用于为序列中每个位置的词元（输入向量）单独添加非线性变换，增加模型的深度，从而让其学习到更复杂的特征，提高模型的性能。</div>2024-09-24</li><br/>
</ul>