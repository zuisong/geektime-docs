> 本门课程为精品小课，不标配音频

你好，我是常扬。

本节课将深入探讨RAG索引（Indexing）流程中的**分块（Chunking）策略和嵌入（Embedding）技术。**

文档数据（Documents）经过解析后，通过分块技术将信息内容划分为适当大小的文档片段（chunks），从而使RAG系统能够高效处理和精准检索这些片段信息。分块的本质在于依据一定逻辑或语义原则，将较长文本拆解为更小的单元。分块策略有多种，各有侧重，**选择适合特定场景的分块策略**是提升RAG系统召回率的关键。

嵌入模型（Embedding Model）负责将文本数据映射到高维向量空间中，将输入的文档片段转换为对应的嵌入向量（embedding vectors）。这些向量捕捉了文本的语义信息，并被存储在向量库（VectorStore）中，以便后续检索使用。用户查询（Query）同样通过嵌入模型的处理生成查询嵌入向量，这些向量用于在向量数据库中通过向量检索（Vector Retrieval）匹配最相似的文档片段。根据不同的场景需求，**评估并选择最优的嵌入模型**，以确保RAG的检索性能符合要求。

![图片](https://static001.geekbang.org/resource/image/c2/d0/c2eea144d5e3ffd46fb18fe11fb069d0.jpg?wh=1920x1603)

## 为什么说分块很重要？

文档通常包含丰富的上下文信息和复杂的语义结构，通过将文档分块，模型可以更有效地提取关键信息，并减少不相关内容的干扰。分块的目标在于确保每个片段在**保留核心语义**的同时，具备**相对独立的语义完整性**，从而使模型在处理时不必依赖广泛的上下文信息，**增强检索召回的准确性**。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/83/4a/3e08427e.jpg" width="30px"><span>药师</span> 👍（6） 💬（1）<div>这个课真不错，看了好几个了，这个是最落地且含金量高的</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（5） 💬（1）<div>第4讲打卡~
请教老师一个问题：我一直有个困惑，将文本、图片或者视频这类非结构化信息，转换成高维向量的过程，叫做Embedding嵌入，那么“嵌入”这个词的由来是什么呢？是指将语义信息内化到高维向量空间中了吗？</div>2024-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（4） 💬（2）<div>这门课很有含金量，每节课都有代码和注释，而且还是独立的，能看到整个框架起来的过程，赞👍</div>2024-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/66/d0/2fb761be.jpg" width="30px"><span>Jaycee-张少同</span> 👍（2） 💬（1）<div>对于思考问题1我没有实战经验，目前一切凭感觉。固定字符分块这种好理解，但是略显笨，比较起来似乎重叠分块更好一些；如果在资源足够的情况下，是否语义分块是比较理想的分块方式。</div>2024-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6c/36/2b368544.jpg" width="30px"><span>魏士祥</span> 👍（0） 💬（1）<div>原以为是个“水”课，没想到这么干。物超所值。</div>2025-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/46/42c2e559.jpg" width="30px"><span>煜寶</span> 👍（0） 💬（1）<div>请问下老师，如果是想要基于RAG来增强底座模型在特定领域里的编码理解能力的，比如我就希望通过描述一个特定框架对应的功能需求信息，然后模型可以根据相关的代码框架知识库来输出结果，这个比较推荐用哪种分块策略和嵌入模型呢？</div>2024-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>在选择嵌入模型时，你如何在模型大小与延迟、精度与效率之间做出权衡？分享你在实际项目中平衡这些因素的经验，或探讨在不同业务场景下的最佳平衡点。
答：够用就好，如果小模型够用，一定用小模型。</div>2024-11-10</li><br/>
</ul>