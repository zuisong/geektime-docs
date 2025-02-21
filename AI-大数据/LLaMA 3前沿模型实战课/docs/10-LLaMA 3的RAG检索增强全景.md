你好，我是Tyler！

从这节课开始，我们正式讨论RAG（检索增强生成）相关的知识，这是当前大模型应用优化中最频繁使用的技术之一。

首先我们来区分一下搜索增强和检索增强，我们前面学习的搜索增强是在模型的推理过程中对不同可能的生成路径进行搜索，以达到最优的生成效果。而**检索增强则是通过外部知识辅助大语言模型回答复杂问题。**

在检索增强的过程中有一个常见误区，那就是很多人常常对向量数据库过于重视，认为仅依靠“老三样”：文章分割、向量模型和向量数据库，就能够解决检索问题。然而，这种思路虽然有其价值，但如果通过充分利用LLaMA 3的能力，我们能够将索引、检索和内容生成的过程变得更加智能化。在深入探讨之前，首先让我们了解朴素RAG的基本流程。

## 朴素RAG的基本流程

由于我们的课程没有设置RAG的前序知识要求，所以我们首先来看朴素 RAG 的构建过程。朴素RAG（Retrieval-Augmented Generation）的基本流程分为五个主要步骤，分别是文档分割、嵌入生成、向量存储、检索过程和内容生成。以下是相关的代码逻辑分解介绍，文末提供了更紧凑的完整代码示例。

![图片](https://static001.geekbang.org/resource/image/1d/52/1d1c476be5d5d3fd9700a9d26aac0552.png?wh=1342x650 "Llama-index High-Level Concepts https://docs.llamaindex.ai/en/stable/getting_started/concepts/")

### 文档分割

文档分割是RAG流程的起点，其目标是将大块的文档拆分成可管理的小片段。分割方式通常基于文本长度、段落、句子结构或者逻辑结构。例如：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（0） 💬（0）<div>课程代码地址：https:&#47;&#47;github.com&#47;tylerelyt&#47;LLaMa-in-Action</div>2024-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/65/2fb5c4ce.jpg" width="30px"><span>旅梦开发团</span> 👍（1） 💬（0）<div>上面的代码缺少了依赖安装，补下：
pip install llama_index 
pip install llama-index-embeddings-huggingface
pip install ollama
pip install llama-index-llms-ollama
pip install chromadb
pip install llama-index-vector-stores-chroma</div>2024-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7d/2a/d40e1145.jpg" width="30px"><span>🌞</span> 👍（1） 💬（0）<div>后续有graphrag的专门介绍和实践吗？</div>2024-11-06</li><br/><li><img src="" width="30px"><span>無鄉</span> 👍（0） 💬（0）<div>引入 LLaMA 3 后，RAG 系统在多个方面有了显著提升？ 如何理解文中这句话？</div>2024-11-16</li><br/>
</ul>