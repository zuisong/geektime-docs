你好，我是独行。

上一节课我们讲解了编码器各层的数据处理逻辑，这节课我们进入解码器。先来看一个更加细化的架构图，解码器多了一层：编码-解码注意力层（Encoder-Decoder Attention），我们依次来看一下。

![图片](https://static001.geekbang.org/resource/image/4d/84/4d6c6cbaa5a9754c6976ae4a6af62e84.png?wh=1415x804 "图片来源于网络")

## Transformer架构原理

### 自注意力层处理（解码器）

解码器的自注意力层设计得比较特别，与编码器的自注意力层不同，解码器的自注意力层需要处理额外的约束，即保证在生成序列的每一步仅依赖于之前的输出，而不是未来的输出。这是通过一个特定的掩蔽（masking）技术来实现的。接下来我详细解释一下解码器自注意力层的几个关键点。

1. **处理序列依赖关系**，解码器的自注意力层使每个输出位置可以依赖于到目前为止在目标序列中的所有先前位置。这允许模型在生成每个新词时，综合考虑已生成的序列的上下文信息。
2. **掩蔽未来信息**，为了确保在生成第 $t$ 个词的时候不会使用到第 $t+1$ 及之后的词的信息，自注意力层使用一个上三角掩蔽矩阵，在实现中通常填充为负无穷或非常大的负数。这保证了在计算Softmax时未来位置的贡献被归零，从而模型无法“看到”未来的输出。
3. **动态调整注意力焦点**，通过学习的注意力权重，模型可以动态地决定在生成每个词时应更多地关注目标序列中的哪些部分。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3c/1a/12/da1ca5ea.jpg" width="30px"><span>希</span> 👍（1） 💬（1）<div>self-attention对抓取关键信息起决定性作用，可以增加head数量、编码器的数量、其他attention来尝试提高效果</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（1） 💬（1）<div>思考题答案可以给一下吗</div>2024-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKug7j7FSiaWwGzQKWXPbHA9teGtx4TncVUyxbSUTgxVXH1jESD44FRQJZspF5CrvU7ib0tNJ7Stoag/132" width="30px"><span>Geek_de5d8e</span> 👍（0） 💬（1）<div>没点基础完全听不下去了</div>2024-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（3） 💬（0）<div>这些底层逻辑好难理解。建议大家结合AI来学习，这样会更容易理解一点。

思考题：
影响 Transformer 模型抓取关键信息的主要部分是注意力机制。通过调整注意力权重、增强输入处理、引入预训练模型或领域知识，模型可以更好地捕捉文章的关键信息，从而生成更准确的摘要。</div>2024-09-05</li><br/>
</ul>