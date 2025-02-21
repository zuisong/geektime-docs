你好，我是金伟。

相信很多同学都看到过类似下面的GPT介绍。

> GPT-3是强大的生成式语言模型，拥有1750亿个参数。它使用Transformer架构，通过大规模的无监督学习从海量文本数据中学习了语言的统计规律和语义表示。GPT-3可以应用于多种自然语言处理(NLP)任务，包括文本生成、文本分类、问答系统等……

你有没有想过，为什么这里面的概念不管在哪种介绍里都会被反复提及？它们是什么意思？每个概念之间有什么关系？如果我们想入局大模型，需要搞清楚这些概念吗？

我的答案是，需要。想学习大模型开发的朋友，只有通盘搞清楚这些问题，才能把概念落实到程序中。

接下来，我会从一个典型的例子出发，采用抽丝剥茧的方式，分析这个例子在Transformer架构下的具体程序流程以及数据结构。

相信通过这节课，你一定能达成三个目标。

1. 跟着这个Transformer程序流程图，把所有Transformer里的概念串联起来，并理解清楚流程。
2. 理解Token，Embedding和Self-Attention这3个最核心的算法和数据结构，解释Transformer为何可以达到人类智力级别。
3. 从业务层看待Transformer程序流程图，理解上述所有大模型的相关概念。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/5b/ff28088f.jpg" width="30px"><span>郑大钱</span> 👍（14） 💬（1）<div>第一次听懂Transformer了，不得不叹一句牛逼！</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（11） 💬（1）<div>自己总结下LLM生成内容的流程：

1. 输入层：对用户输入进行分词，转换成Token列表，列表长度为N；
2. 输入层：针对每个Token，逐个在Token词表中查询Embedding向量表示，生成一个NxM维的矩阵，其中M为Embedding的维度；
3. 输入层：将NxM维矩阵传递给编解码层处理；
4. 编解码层：拿到NxM维矩，基于Transformer算法，采用Q、K、V权重矩阵计算，生成每个Token的注意力分数；
5. 编解码层：根据注意力分数，计算生成下一个Token的概率，传递给输出层；
6. 输出层：根据生成的Token概率，以及预设的随机性策略，到Token词表中获取下一个生成的Token；
7. 输出层：将生成的Token，与用户的原始输入一起，作为下一轮的输入，传递给输入层，重复上述步骤。</div>2024-08-20</li><br/><li><img src="" width="30px"><span>8000tank</span> 👍（6） 💬（2）<div>https:&#47;&#47;bbycroft.net&#47;llm，这里可以看到多个LLM内部原理的 可视化3D图像演示细节，强烈推荐</div>2024-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8qibAw4lRCic1pbnA6yzQU3UqtQm3NqV1bUJ5EiaUnJ24V1yf4rtY7n2Wx7ZVvTemqq5a61ERWrrHA/132" width="30px"><span>Alex</span> 👍（2） 💬（1）<div>最后的思考题 
- 有部分是根据模型的初始值有关就像针对各个行业的不同模型 其实也就是模型的训练的语料不同
- 就像文中说的注意力的机制也是动态的 下一次的注意点不一定就是上一次的值 也许也有上下文的问题 问了多次模型会调整回答
- 随机的问题 就是openai的tempatrue 越高越随机性就越高 自然语言本身就是模糊的 模型的回答自然也会带入一定的随机性</div>2024-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/40/1c/19fea99b.jpg" width="30px"><span>我爱学习</span> 👍（1） 💬（3）<div>每一个词的概率 P(wn|wi)，[0, 0, 0, 0.6, 0.3, 0.1]，这个是怎么计算出来的？</div>2024-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIofiaCAziajdQnbvrfpEkpCKVFgO62y6zicamhjF1BAWZSRcCVaTBXLIerLsGeZCic7XS7KOEkTN4fRg/132" width="30px"><span>zahi</span> 👍（1） 💬（2）<div>Self-Attention 算法计算出来的向量Z, 是代替N x M矩阵计算吗？</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/8a/f4/149802dd.jpg" width="30px"><span>Chris_zhengbin</span> 👍（1） 💬（1）<div>看了很多关于Transformer的文章和视频，就这一篇讲的最透彻最实用，看完这篇再看其他的就简单多了。</div>2024-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b4/99/353fe94e.jpg" width="30px"><span>luminais</span> 👍（1） 💬（1）<div>”第二步，Token ti 拿着自己的 Q 向量去询问每个 Token，并得到自己的重要性分数 Score”
这里的“每个 Token”是指自己本次输入语句被拆分的所有Token吗，这里没有理解到为啥要询问自己输入的Token？</div>2024-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/1b/32/cbfdf1f4.jpg" width="30px"><span>Geek_11d2d2</span> 👍（1） 💬（1）<div>思考题: 首先不是总是从预测的最高概率取 token, 还有温度等参数, 还有就是, 是不是在一次会话中, 即使问了重复的问题, token 计算的注意力值就会变化? 跟现实中人的对话一样, 问了相同问题, 也会有可能得到不一样描述的回答.</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/cb/27b88c1c.jpg" width="30px"><span>风格若干</span> 👍（1） 💬（3）<div>老师，我想问一下，文稿中这段话，抽取的为什么是一个 3 x M 的矩阵呀？

假设词表总长度是 L，比如“我”这个 Token 的 Embedding 就可以直接从词表里取出来，这个例子输入的总 Token 数量 N = 4，Embedding 向量的维度是 M，此时抽取的矩阵是一个 3 x M 的矩阵。</div>2024-08-11</li><br/><li><img src="" width="30px"><span>8000tank</span> 👍（0） 💬（1）<div>最后的2个流程图（同一个），下方的“模型参数”中，有个“M=Token词表”，是不是应该改为“M=Token维度”？</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/57/1cebae66.jpg" width="30px"><span>YOUNG</span> 👍（0） 💬（1）<div>老师讲的真好，我基本看懂了</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/36/b4a4e6fb.jpg" width="30px"><span>Edon du</span> 👍（0） 💬（2）<div>gpt3文本嵌入的默认向量维度不是1536吗，有点不太理解的是，我们拿到一个文本，先分段，不管某一段的文本多长，只要不超过最大token数，拿到的向量化都是一个指定维度的一维数组。

文中的&quot;我爱你&quot; 为什么会拆字转换成向量矩阵呢，如果转化了，那向量矩阵和我们调用向量化得到的一维数组有什么关联呢，希望老师解惑</div>2024-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/db/ec/d5638e84.jpg" width="30px"><span>麦克范儿</span> 👍（0） 💬（1）<div>想问下，当output部分得出parameters概率向量后，大模型是通过概率随机的方式来选择具体产生哪个token吗？还是输出最大概率的token呢？如果输出最大概率的话会不会很多次相同提问的回复都是一样的值？谢谢！</div>2024-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/f7/0645cb4a.jpg" width="30px"><span>西雨ζ๓㎕东晴</span> 👍（0） 💬（2）<div>预测下一个最高概率的字是从token词表中来的吗？</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/27/11/07d2455b.jpg" width="30px"><span>黄武</span> 👍（0） 💬（1）<div>这个是每天一讲吗
如何学习下一节课程</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/cd/c21a01dd.jpg" width="30px"><span>W-T</span> 👍（0） 💬（2）<div>思考题，是不是内部会包含多套模型权重参数，有时候会选择不同的权重参数，所以会产生不一样的结果</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/58/b3/abb3256b.jpg" width="30px"><span>枫树_6177003</span> 👍（0） 💬（1）<div>老师讲的透彻，太棒了</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/a9/903cc835.jpg" width="30px"><span>blue mountain</span> 👍（0） 💬（0）<div>有个问题，什么时候跳出循环呢，就是怎么判定我这个问题已经回答出来了，不需要继续生成</div>2025-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3f/9d/c59c12ad.jpg" width="30px"><span>实数</span> 👍（0） 💬（0）<div>有学习群吗 老师</div>2025-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0a/a417ec1c.jpg" width="30px"><span>南瓜</span> 👍（0） 💬（0）<div>高手就是把复杂的东西弄简单</div>2024-10-29</li><br/>
</ul>