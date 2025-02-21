你好，我是独行。

上节课我向你介绍了模型的内部结构，为了理解模型的内部结构，我们又顺带回顾了一下模型的实现原理，其中我讲过一句话：模型的训练过程就是不断调整权重的过程，准确一点还应该加上偏置，**模型的训练过程就是不断调整权重和偏置的过程**，调整的过程依赖反向传播、损失函数等等。

前面我们没有详细讲解这方面的细节，这节课我们再通过一个简单的例子，把预训练的过程完整细致地串一遍。我们将使用一个三层神经网络结构的模型来进行数据分类的展示。这个模型接收两个输入变量：学习时间和睡眠时间，并基于这些输入预测一个学生是否能够通过考试。

我们还是按照常规的模型训练步骤来进行，但前面讲过的内容这节课就不细说了。

## 网络结构设计

模型网络结构的定义，你可以参考[手敲Transformer那节课](https://time.geekbang.org/column/article/787626?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)的代码。

```python
import torch
from torch import nn

# 定义一个只包含解码器的Transformer模型
class TransformerDecoderModel(nn.Module):
    def __init__(self, vocab_size, embed_size, num_heads, hidden_dim, num_layers):
        super(TransformerDecoderModel, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.positional_encoding = nn.Parameter(torch.randn(embed_size).unsqueeze(0))
        decoder_layer = nn.TransformerDecoderLayer(d_model=embed_size, nhead=num_heads, dim_feedforward=hidden_dim)
        self.transformer_decoder = nn.TransformerDecoder(decoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(embed_size, vocab_size)
    def forward(self, src):
        src = self.embed(src) + self.positional_encoding
        src_mask = self.generate_square_subsequent_mask(src.size(0))
        output = self.transformer_decoder(src, src, src_mask)
        output = self.fc(output)
        return output
    def generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask
        
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（12） 💬（1）<div>现在还跟着学的，点个赞让我看看。</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/58/b3/abb3256b.jpg" width="30px"><span>枫树_6177003</span> 👍（5） 💬（1）<div>如果发现模型在训练集上的表现远远好于在验证集上，可能是过拟合导致。可以使用dropout来提高模型的泛化能力</div>2024-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/1a/12/da1ca5ea.jpg" width="30px"><span>希</span> 👍（2） 💬（1）<div>过拟合，可能是模型结构过于复杂、训练样本不足、训练样本不平衡导致，可以减少神经网络的层数、使用dropout、增加数据量、数据增强、集成模型来缓解过拟合</div>2024-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（6） 💬（0）<div>如果模型在训练集上的表现明显好于在验证集上的表现，这通常意味着模型出现了过拟合（overfitting）的现象。过拟合是指模型在训练数据上表现得很好，但是在未见过的数据（验证集或测试集）上表现较差。这是因为模型学到了训练数据中的噪声和细节，而不是数据的实际模式或一般规律。

过拟合的原因
1. 模型复杂度过高：模型的参数太多（例如，神经网络的层数和神经元数量过多），导致其能够学习训练数据中的噪声。
2. 训练数据不足：训练数据样本过少，导致模型对训练数据的依赖过大。
3. 数据不平衡或噪声数据：训练数据中存在噪声或异常数据，导致模型学习到不具备普遍性的模式。
4. 训练时间过长：模型训练的轮次太多，导致它过度拟合训练数据。

改善过拟合的措施
1. 减少模型复杂度：
减少神经网络的层数或神经元数量：简单的模型更不容易过拟合。
使用较小的模型架构：选择参数更少的模型。
2.  增加训练数据：
收集更多的数据：更多的数据可以帮助模型学习更普遍的特征。
数据增强（Data Augmentation）：通过旋转、翻转、缩放等方式生成新的训练数据，增加数据量。
3. 正则化（Regularization）：
L1&#47;L2 正则化：在损失函数中添加权重惩罚项，限制模型参数的大小，防止模型学习到过多的特征。
Dropout：在每个训练步骤中随机丢弃一部分神经元，防止模型过度依赖某些路径。
4. 提前停止（Early Stopping）：
在验证集损失开始上升时停止训练。这样可以防止模型在训练集上过拟合。
5. 集成方法（Ensemble Methods）：
Bagging：例如，随机森林通过结合多棵树的结果来降低过拟合风险。
Boosting：如 XGBoost，通过顺序训练多个弱分类器，每个分类器弥补前一个分类器的不足。
6. 使用更好的数据预处理和清洗：
去除异常值和噪声数据，确保数据的质量。
标准化和归一化数据，使不同特征具有相同的尺度。
7. 使用验证数据进行模型选择和超参数调优：
使用交叉验证（cross-validation）来评估模型性能，确保模型在不同的数据子集上表现一致。
调整超参数（如学习率、正则化强度等）来找到最佳参数设置。</div>2024-09-05</li><br/>
</ul>