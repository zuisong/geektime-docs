你好，我是郑晔！

上一讲，我们站在用户视角介绍了LLM，这个视角可以帮助我们更好地理解如何使用大模型。

不过，站在用户视角，我们只能关心到语言输入和输出，而如果要开发一个 AI 应用，我们不可避免地会接触到其它一些概念，比如，Token、Embedding、温度等等，这些概念是什么意思呢？这一讲，我们就从技术的视角看一下大模型，到这一讲的末尾，你也就知道这些概念是怎么回事了。

在出发之前，我要强调一下，我们不是为了打造一个大模型，而是为了更好地理解应用开发中的各种概念。好，我们开始！

## 技术视角的大模型

站在技术视角理解大模型，核心就是搞懂一件事，大模型到底做了些什么。其实，大模型的工作很简单，**一次添加一个词**。

怎么理解这个说法呢？本质上说，ChatGPT做的是针对任何文本产生“合理的延续”。所谓“合理”，就是“人们看到诸如数十亿个网页上的内容后，可能期待别人会这样写”。我们借鉴 Stephen Wolfram 的《这就是 ChatGPT》（What Is ChatGPT Doing … and Why Does It Work?）里的一个例子一起来看一下。

### 选择下一个词

假设我们手里的文本是“The best thing about AI is its ability to”（AI 最棒的地方在于它能）。想象一下，我们浏览了人类编写的数十亿页文本（比如在互联网上和电子书中），找到该文本的所有实例，然后，猜测一下接下来要出现的是什么词，以及这些词出现的概率是多少。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（11） 💬（1）<div>在大型模型中，Embedding 是一种将高维数据（如文本、图像、视频等）转换为低维向量表示的技术。这种技术在自然语言处理（NLP）、计算机视觉等领域有着广泛的应用。Embedding 的核心思想是将离散数据映射到连续的向量空间，使得相似的数据点在向量空间中的距离较近，而不相似的数据点则距离较远。</div>2024-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/b0/6f87ab08.jpg" width="30px"><span>Tony Bai</span> 👍（3） 💬（1）<div>“在大模型的处理中，需要经过 One-Hot 编码，然后，再对 One-Hot 编码之后的结果进行压缩，得到我们最终需要的结果。”  -- 目前词嵌入不会有one-hot这一过程吧？不过从内容讲解的角度来看，以one-hot为例，倒不失为很好的方法😁。</div>2024-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/e0/3db22579.jpg" width="30px"><span>技术骨干</span> 👍（1） 💬（1）<div>token 代表可以生成的内容有多少，温度代表生成内容的随机性，embedding 代表将高维数据转换成向量的技术，极其复杂，看不太懂。</div>2024-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>好像之前了解过一些搜索引擎做搜索的时候会对处理成向量的数据做一个余弦相似度的处理，不知道跟这个文章说的是否类似</div>2025-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（0） 💬（1）<div>还是对AI不大熟悉,  有个问题,  您以上讲的是  训练大模型的过程  还是  用户输入后, 大模型针对用户输入输出的过程? </div>2024-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（1）<div>1、 …… --&gt; 词 --&gt; token --&gt; 稀疏向量 --&gt; 密集向量 --&gt; ……

2、交给 AI 算法处理的前提就是把各种信息转换成向量 ==&gt; 向量是多模态的前提；

3、你看过哪些介绍大模型工作原理的内容呢？推荐一下孙志岗老师的专栏：https:&#47;&#47;note.mowen.cn&#47;note&#47;detail?noteUuid=vKwymX8n5BEpqD5nCZPRo</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/86/dba8214e.jpg" width="30px"><span>星期三。</span> 👍（0） 💬（1）<div>One-Hot 只是针对单个词的，词与词之间的关系，甚至是整个句子，这些是怎么处理的</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/86/dba8214e.jpg" width="30px"><span>星期三。</span> 👍（0） 💬（1）<div>One-Hot是一个很老的技术吧，现在基于transformer架构embedding模型还在用这个吗</div>2024-11-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLm8skz4F7FGGBTXWUMia6qVEc00BddeXapicv5FkAx62GmOnUNEcE4scSR60AmappQoNdIQhccKsBA/132" width="30px"><span>末日，成欢</span> 👍（0） 💬（1）<div>大模型会将&#39;输入&#39;，会被隐射到多维空间的坐标点上，再经过某种压缩机制转化成向量
提示词中的内容词语权重不一样，所以大模型往往根据我们不同的提示词内容可以给出不同的结果，也就是大模型需要理解上下文，完成迁移学习。
预测下一个词我第一次知道，应该也是根据内容词语权重【理解上下文】，找出一堆向量，然后再通过概率找出【最合适】的一个向量</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第2讲打卡~</div>2024-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/c8/1ccbb110.jpg" width="30px"><span>淡漠尘花划忧伤</span> 👍（0） 💬（0）<div>重点总结：
1. 大模型的工作很简单，一次添加一个词。Token 就是我们理解大模型编程的第一个重要概念。这个 Token 可能是我们传统理解的一个完整的单词，可能是一个单词组合，甚至可能是单词的一部分（这就是大模型可以“造出新词”的原因）。有一个很重要的指标就是上下文窗口（Context Window）的大小。这里的上下文窗口，指的就是大模型可以处理 Token 数量，上下文越大，能处理的 Token 越多。
2. 表示随机性强弱的概念：温度它是表示大模型活跃程度的一个参数，通过调节这个参数，大模型变得更加活跃，或是更加死板。
3. 大模型内部处理的并不是字符串，而是向量。之所以要将字符串转换为向量，简单理解，就是现在大部分的 AI 算法只支持向量。</div>2025-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/a6/1fc5435f.jpg" width="30px"><span>江旭东01</span> 👍（0） 💬（0）<div>上下文窗口的大小决定了大模型一次可以处理多少个 Token，什么决定上下文窗口的大小呢？</div>2025-02-07</li><br/><li><img src="" width="30px"><span>Geek_d4f4e7</span> 👍（0） 💬（0）<div>个人理解希望老师和其他同学帮我纠正一下
本章主要大模型的核心，就是选择下一个词，针对回答的创新性更人性化更有温度，和我们讲了一下其中的一个参数叫做温度(随机性)。
其次和我们简单介绍了一下Token，Token是大模型理解的文本的基本单位，在不同大模型中token可以为字符、单词、子词，Token也是大模型计费的标准
其次和我们简单介绍了下字符串到向量的过程，和我们介绍了一下ai算法是基于向量进行运算，大模型会将字符串统一处理为向量，处理步骤有两步，第一步one-hot编码，将字符串处理为离散稀疏的高维向量，第二步把第一步结果进行压缩，将向量通过嵌入层矩阵压缩成低维密集向量</div>2025-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（0） 💬（0）<div>流式输出</div>2024-11-06</li><br/>
</ul>