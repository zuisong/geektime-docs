你好，我是独行。

上节课我们一起学习了Word2Vec，Word2Vec的主要能力是把词汇放在多维的空间里，相似的词汇会被放在邻近的位置。这节课我们将进入Seq2Seq的领域，了解这种更为复杂且功能强大的模型，它不仅能理解词汇，还能把这些词汇串联成完整的句子。

## Seq2Seq

Seq2Seq（Sequence-to-Sequence），顾名思义是**从一个序列到另一个序列的转换**。它不仅仅能理解单词之间的关系，而且还能把整个句子的意思打包，并解压成另一种形式的表达。如果说Word2Vec是让我们的机器学会了理解词汇的话，那Seq2Seq则是教会了机器如何理解句子并进行相应地转化。

在这个过程中，我们会遇到两个核心的角色：**编码器**（Encoder）和**解码器**（Decoder）。编码器的任务是理解和压缩信息，就像是把一封长信函整理成一个精简的摘要；而解码器则需要将这个摘要展开，翻译成另一种语言或形式的完整信息。这个过程有一定的挑战，比如如何确保信息在这次转换中不丢失精髓，而是以新的面貌精准地呈现出来，这就是我们接下来要探索的内容之一。

## 基本概念

Seq2Seq也是一种神经网络架构，模型的核心由两部分组成：编码器（Encoder）和解码器（Decoder）。你可以看一下这个架构的示意图。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/f1/7d21b2b0.jpg" width="30px"><span>方梁</span> 👍（1） 💬（1）<div>train_1w.zh
train_1w.en
请提供一下哈，谢谢</div>2024-06-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epsRcQM1w3rNleqQ9990hGuRWCrrSvAibzcHyuLBic9XhfvC0KCfyjicaIvMaPDicwrepIY0TiatFRp8ag/132" width="30px"><span>小毛驴</span> 👍（0） 💬（1）<div>老师补充一下：OSError: [E053] Could not read config file from external\en_core_web_sm-2.3.0\config.cfg
从网盘下载的模型加载会报错，在huggingface上引用的模型每次执行pred_token_index = output.argmax(dim=1).item()返回都是0，这是为啥？
</div>2024-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epsRcQM1w3rNleqQ9990hGuRWCrrSvAibzcHyuLBic9XhfvC0KCfyjicaIvMaPDicwrepIY0TiatFRp8ag/132" width="30px"><span>小毛驴</span> 👍（0） 💬（1）<div>老师，请教一下为什么 pred_token_index = output.argmax(dim=1).item()这段代码永远返回都是0，是我引用的模型不对嘛？
</div>2024-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（0） 💬（1）<div>第三章开始的技术原理部分越来越难了。</div>2024-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/54/73cc7f73.jpg" width="30px"><span>王旧业</span> 👍（0） 💬（1）<div>老师请教下文中这种动图咋做的</div>2024-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/f1/7d21b2b0.jpg" width="30px"><span>方梁</span> 👍（0） 💬（1）<div>en_core_web_sm
等文件在哪里下载？
</div>2024-06-26</li><br/><li><img src="" width="30px"><span>Geek_7df415</span> 👍（0） 💬（1）<div>模型训练部分， AIchallenger2017 的链接，AccessDenied</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3d/8e/83/c5eb2649.jpg" width="30px"><span>kiikii</span> 👍（0） 💬（0）<div>反向算法传播过程中，会被更新的参数，是权重和偏置，weights和bais；权重即上下文向量中的每个词和已生成序列，影响到当前要被生成的词的权重、影响力有多大；baises是指一个基础阈值</div>2025-01-19</li><br/>
</ul>