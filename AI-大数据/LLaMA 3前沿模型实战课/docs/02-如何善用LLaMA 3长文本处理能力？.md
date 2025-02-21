你好，我是Tyler。

在之前的课程中，我们深入探讨了如何利用 LLaMA 模型进行对话，并明确了LLaMA 在多轮对话中的核心机制。这一机制通过存储历史对话内容，将无状态的大模型推理服务转变为有状态的多轮对话服务。

这一机制显著提升了对话系统在处理复杂对话情境时的能力，但也带来了新的挑战：随着历史对话轮次的增加，模型的输入长度也随之增长。为应对这一挑战，大模型必须具备处理长文本输入的能力，这不仅是对现有技术的扩展，也是长文本处理能力发展的关键驱动力。

本节课我们将深入探讨处理长文本输入时的关键技术工作，包括当前的解决方案、优势及其局限性。我们将系统性地分析如何优化长文本输入的处理，以满足大规模对话系统对长文本的需求，并评估这些技术方案在实际应用中的表现和潜在改进方向。

## 长文本处理的发展与现状

LLaMA 模型的长文本处理能力有了显著提升。从 LLaMA 2 的 2048 个 token 扩展到 4096 个 token，再到 LLaMA 3 支持的 8000 个 token，甚至通过进一步微调可以处理更长的文本。这意味着这些模型现在可以处理更长的文本，理解能力也得到了增强，生成的回应更加连贯，相关性也更强。图表展示了不同模型在长文本处理方面的进展。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（1） 💬（0）<div>课程代码地址：https:&#47;&#47;github.com&#47;tylerelyt&#47;LLaMa-in-Action</div>2024-11-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iaK3hr7TO6WRFgmFkia0Q75ThkpyIOQtnXSttpI1ib8ianXxbb6LlPgPLZNOj5niaZnBt6Htps2Jia11v9l2VeL7EPibw/132" width="30px"><span>午夜修铃</span> 👍（0） 💬（0）<div>Windows本地模型，使用ollama时如何调用本地显卡？</div>2024-12-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iaK3hr7TO6WRFgmFkia0Q75ThkpyIOQtnXSttpI1ib8ianXxbb6LlPgPLZNOj5niaZnBt6Htps2Jia11v9l2VeL7EPibw/132" width="30px"><span>午夜修铃</span> 👍（0） 💬（0）<div>生成的结果： 根据给出的数据，合同中的主要义务包括：

1. 付款义务
2. 商品交付义务
3. 相关服务的提供
Exception ignored in: &lt;function AbsEmbedder.__del__ at 0x00000174DDF64540&gt;
Traceback (most recent call last):
  File &quot;C:\Users\xxx\miniconda3\Lib\site-packages\FlagEmbedding\abc\inference\AbsEmbedder.py&quot;, line 270, in __del__
  File &quot;C:\Users\xxx\miniconda3\Lib\site-packages\FlagEmbedding\abc\inference\AbsEmbedder.py&quot;, line 89, in stop_self_pool
TypeError: &#39;NoneType&#39; object is not callable

这里报错了。
flagembedding             1.3.3                   </div>2024-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/e0/c20f2457.jpg" width="30px"><span>江慧明</span> 👍（0） 💬（0）<div>具备长文本处理能力，也意味着需要更多资源，显存资源，CPU资源，也意味着回答用户问题需要更长时间，所以具备长文本处理能力模型，在具体实践中也不能毫无节制使用，而是充分有理由使用，为取得速度、资源、上下文的平衡，我们需要充分设计，利用langchain工具，可以把问题拆分多个聚焦点，然后用LLM快速获得答案，然后再讲问题组合</div>2024-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c1/65/2fb5c4ce.jpg" width="30px"><span>旅梦开发团</span> 👍（0） 💬（0）<div>在合同RAG的案例中 我安装FlagEmbedding报错了，可能是python版本的问题。 我使用nomic-embed-text:latest 嵌入模型代替， 大家也可以试试。 我的完整代码如下
```python
# 向量数据库
import chromadb
# Settings 配置
from chromadb.config import Settings
# 生成器嵌入 图像处 自然语言处理
# from FlagEmbedding import BGEM3FlagModel
import ollama

chroma_client = chromadb.PersistentClient(path=&quot;.&#47;chromadb&quot;)
# document, metadata embedding
documents = [
...
]

documentation_collection = chroma_client.get_or_create_collection(name=&quot;legal_docs&quot;)

for doc in documents:
  embedding = ollama.embeddings(model=&#39;nomic-embed-text:latest&#39;,prompt=doc[&#39;page_content&#39;])
  # print(embedding.get(&#39;embedding&#39;))
  # id, embedding, 原内容
  documentation_collection.add(
    ids=[doc[&#39;metadata&#39;][&#39;id&#39;]],
    embeddings=embedding.get(&#39;embeddings&#39;),
    documents=[doc[&#39;page_content&#39;]]
  )

query = &quot;合同是什么？&quot;
query_embedding = ollama.embeddings(model=&#39;nomic-embed-text:latest&#39;, prompt=query)
query_embedding = query_embedding.get(&#39;embedding&#39;)[:384] 
# print(query_embedding.get())
# # # 根据embedding 查询
results = documentation_collection.query(
  query_embeddings = query_embedding,
  n_results=1
)
# # # # 取出原内容
data = results[&#39;documents&#39;][0]
document_content = data

prompt = f&quot;根据一下信息， 请回答：{query}&quot;

output = ollama.chat(model=&#39;qwen2.5:latest&#39;, messages=[
  {
    &#39;role&#39;: &#39;user&#39;,
    &#39;content&#39;: f&quot;使用一下数据：{document_content},响应这个提示：{prompt}&quot;
  }
])

print(&quot;生成的结果：&quot;, output[&#39;message&#39;][&#39;content&#39;])
```</div>2024-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/7f/7b1f3f68.jpg" width="30px"><span>willmyc</span> 👍（0） 💬（0）<div>超长文本是否应该考虑跟llama3多轮对话的情况，llama3如何处理，可否介绍一下，谢谢！</div>2024-10-22</li><br/>
</ul>