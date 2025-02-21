你好，我是独行。

前两节课，我从理论层面向你介绍了Transformer的架构原理，到现在为止，我们所有介绍基础理论知识的部分基本结束了。从这节课开始，我们会进入实战环节，对模型的设计、构建、预训练、微调、评估等进行全面的介绍，所以接下来的课程会越来越有意思。这节课，我们先来学习下，如何从0到1构建基于Transformer的模型。

## 选择模型架构

Transformer架构自从被提出以来，已经演化出多种变体，用来适应不同的任务和性能需求。以下是一些常见的Transformer架构方式，包括原始的设计以及后续的一些创新。

![图片](https://static001.geekbang.org/resource/image/e3/ba/e3b3f87c7cf8298f70f760d8eca979ba.jpg?wh=2082x964)

我们熟知的GPT系列模型，使用的是Decoder-only架构，Google的Bert模型使用的是Encoder-only架构。GPT系列模型之所以选择使用Decoder-only架构，主要出于以下几点考虑：

1. GPT是语言模型，根据给定的文本预测下一个单词，而解码器就是用来生成输出序列的。
2. Decoder-only模型采用自回归方式进行训练，在生成每一个新词时，都会利用之前所有已生成的词作为上下文。这种自回归的特性使得GPT能够在生成文本时保持内容的连贯性和逻辑性。
3. 与编码器-解码器结构相比，Decoder-only架构简化了模型设计，专注于解码器的能力。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/25/36/cc/f3bc7bbf.jpg" width="30px"><span>newCheng</span> 👍（7） 💬（1）<div>老师，帮忙推荐一台深度学习的电脑配置呗，或者有没有合适的云平台？</div>2024-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（6） 💬（1）<div>第16讲打卡~
这里简单补充一下GPT和Bert这两种模型的差异：GPT是Decoder-only架构，并且采用单向注意力机制，这意味着在生成文本时，它只考虑前面的上下文信息；而Bert是Encoder-only架构，并且采用双向注意力机制，也就是可以同时考虑上文和下文的信息。这两种结构的差别，也就决定了GPT和Bert有各自擅长的应用场景：GPT更擅长文本生成，也就是“续写”，即根据上文生成下文；而Bert可以被应用于更广泛的NLP任务中，如文本分类、情感分析、命名实体识别等。</div>2024-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/c3/c5db35df.jpg" width="30px"><span>石云升</span> 👍（4） 💬（1）<div>C ≈ 8.64 * 10^17 FLOPs
A100-80G的理论峰值性能是312 TFLOPS，即每秒可以进行：
312 * 10^12 = 3.12 * 10^14 FLOPs&#47;s
理论上最快完成时间：
时间 = 总FLOPs &#47; 每秒FLOPs
= (8.64 * 10^17) &#47; (3.12 * 10^14)
≈ 2,769 秒
≈ 46 分钟

所以，理论上使用一张A100-80G显卡，最快约46分钟就能完成训练。</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/dd/f2/3513c633.jpg" width="30px"><span>张 ·万岁！</span> 👍（1） 💬（1）<div>参数量1.2亿，要训练的词元数
理论上，如果光看模型的内存，一张a100 80gb完全可以容纳得下来，因为120,000,000×4÷1,024÷1,024=457.763671875MB，绰绰有余。

算力上来看的话，我没太懂这个问法。按照我的理解来算，12gb的训练文本一共大概800万条样本，每个样本50个词元，词元数D=4亿。再算上参数量1.2亿。那么总的计算量就是C=2.88*10^17。  英伟达的a100 80gb的32位浮点运算的峰值是19.5tflops，也就说1.95*10^13。
那么有(2.88×10^(17))÷(1.95×10^(13))=14769.23
也就说等于14769张a100的算力？
总感觉我算的一点也不对。。。</div>2024-07-25</li><br/><li><img src="" width="30px"><span>Geek_f80ce5</span> 👍（0） 💬（1）<div>老师，完整代码能分享下吗？根据课程中的代码，执行到中间会一直等待。不知道为什么</div>2024-12-28</li><br/><li><img src="" width="30px"><span>Geek_f80ce5</span> 👍（0） 💬（1）<div>这个源代码有吗？</div>2024-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/81/ad80f427.jpg" width="30px"><span>Lane</span> 👍（0） 💬（1）<div>collate_fn应该怎么实现呢</div>2024-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/81/ad80f427.jpg" width="30px"><span>Lane</span> 👍（0） 💬（1）<div>代码缺失的地方呢</div>2024-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/85/b3af5d54.jpg" width="30px"><span>就在这儿💋</span> 👍（0） 💬（2）<div>老师,有没有完整的代码文件呀,课程里的示例代码缺了一些内容, DataLoader的 collect_fn是没有的</div>2024-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/a3/4bcf1b59.jpg" width="30px"><span>大宽</span> 👍（0） 💬（1）<div>老师 大模型训练都用哪些框架呢，pytorch 吗，还有其他工具不 ，或者咱国内的一些大模型都用什么框架训练的呢。老师可否整体介绍一下，一个模型从训练到推理 做成 api 需要的步骤及其对应的技术工具哈？</div>2024-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2d/86/07a10be2.jpg" width="30px"><span>Lee</span> 👍（0） 💬（1）<div>老师  能说说训练时间怎么预估吗</div>2024-07-08</li><br/><li><img src="" width="30px"><span>翔</span> 👍（0） 💬（1）<div>课程到这里，没人互动了，是不是都掉队了😟</div>2024-07-02</li><br/><li><img src="" width="30px"><span>翔</span> 👍（0） 💬（1）<div>训练模型必须要用显卡吗，跑一丢丢测试数据，用 cpu 不行吗</div>2024-07-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/MpKow66ExJ0y3G471ql99hxqcdQ7RF0M7XBnN38uIvhK3bIxadn3W8KPnlbExTBgmAMhAsRnfkC0TsqKrNicnGg/132" width="30px"><span>乔克哥哥</span> 👍（0） 💬（0）<div>自注意力参数的计算是不是直接把多头的参数合并一起算了，刚开始看没反应过来</div>2025-02-07</li><br/><li><img src="" width="30px"><span>Geek_4d9162</span> 👍（0） 💬（0）<div>老师  求助，中文 wiki 数据集下载页面打不开， 能否上传一个阿里云盘或者腾讯云盘的，百度网盘下载太慢了。</div>2024-12-07</li><br/>
</ul>