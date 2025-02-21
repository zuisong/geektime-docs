你好，我是黄佳，欢迎来到LangChain实战课！

在[第2课](https://time.geekbang.org/column/article/699436)中，我曾经带着你完成了一个基于本地文档的问答系统。用当下时髦的话说，你实现了一个RAG 应用。

什么是RAG？其全称为Retrieval-Augmented Generation，即检索增强生成，它结合了检索和生成的能力，为文本序列生成任务引入外部知识。RAG将传统的语言生成模型与大规模的外部知识库相结合，使模型在生成响应或文本时可以动态地从这些知识库中检索相关信息。这种结合方法旨在增强模型的生成能力，使其能够产生更为丰富、准确和有根据的内容，特别是在需要具体细节或外部事实支持的场合。

RAG 的工作原理可以概括为几个步骤。

1. **检索：**对于给定的输入（问题），模型首先使用检索系统从大型文档集合中查找相关的文档或段落。这个检索系统通常基于密集向量搜索，例如ChromaDB、Faiss这样的向量数据库。
2. **上下文编码：**找到相关的文档或段落后，模型将它们与原始输入（问题）一起编码。
3. **生成：**使用编码的上下文信息，模型生成输出（答案）。这通常当然是通过大模型完成的。

RAG 的一个关键特点是，它不仅仅依赖于训练数据中的信息，还可以从大型外部知识库中检索信息。这使得RAG模型特别适合处理在训练数据中未出现的问题。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_f55576</span> 👍（3） 💬（1）<div>老师如果对文件切片时候，文件中的的问题和回答被切成2个不同的chunck那么经常会无法检索到答案，这种场景有什么优化方法吗？</div>2023-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8e/c1/ab1110f8.jpg" width="30px"><span>万万没想到</span> 👍（2） 💬（3）<div>还是不能明白gpt这样的语言模型在RAG中的作用、不是直接在向量数据库中就查出来了么、最后一步为什么要丢给gpt输出、而不是直接输出</div>2024-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/fc/147e38d9.jpg" width="30px"><span>Lominnave</span> 👍（2） 💬（1）<div>老师可以介绍下稀疏向量么，另外稀疏-密集向量结合如何提高召回效果？</div>2023-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（2） 💬（3）<div>【第二种是 embed_query 方法，为查询创建嵌入】一直有个疑问，如果query是需要“复杂理解”的，那么是怎么通过“相似度”去match到文档内容的呢。比如文档是一片小说，而query是：请解读文中描写主人翁心理活动的部分？这里面 LangChain 是否做了特殊处理？</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/15/84/2734c72c.jpg" width="30px"><span>zjl</span> 👍（1） 💬（2）<div>langchain有没有调用本地检索的tool呢？或许可以尝试用本地检索去做reAct</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/b6/43/8ee89342.jpg" width="30px"><span>感性即自然的理性</span> 👍（1） 💬（1）<div>希望老师可以最后的内容里面涉及到相关交互页面的内容，就是图形页面的内容</div>2023-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/aa/b6/9d021ab4.jpg" width="30px"><span>日暮途远</span> 👍（0） 💬（1）<div>embed_documents和embed_query这一块的文档是不是写错了？出现了2次「embed_documents 方法的示例代码如下：」</div>2023-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/02/cb050516.jpg" width="30px"><span>qkyong</span> 👍（0） 💬（1）<div>检索时为啥要指定text-splitter？理论上直接计算向量距离呀</div>2023-10-30</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（2） 💬（0）<div>用百川智能嵌入模型改写文本嵌入、存储嵌入

## 旧代码1：
from langchain.embeddings import OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings()
## 新代码1：
from langchain_community.embeddings import BaichuanTextEmbeddings  # 导入百川模型
embeddings_model = BaichuanTextEmbeddings(baichuan_api_key=&quot;key&quot;) # 初始化百川模型。KEY 用你的key代替

## 旧代码2：
underlying_embeddings = OpenAIEmbeddings()
namespace=underlying_embeddings.model 
## 新代码2：
underlying_embeddings=embeddings_model
namespace=&quot;baichuan_embeddings&quot;   # 用自定义命名嵌入缓存的命名空间

### 新代码3：采用其他文本分割器、向量数据库、检索器的的代码

# 导入文档
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader(&#39;.&#47;建筑垃圾处理技术标准.docx&#39;)

# 导入初始化百川模型
from langchain_community.embeddings import BaichuanTextEmbeddings
embeddings_model = BaichuanTextEmbeddings(baichuan_api_key=&quot;KEY&quot;) #此处用你的key代替

# 从加载器创建索引
from langchain.indexes import VectorstoreIndexCreator
index = VectorstoreIndexCreator(embedding=embeddings_model).from_loaders([loader])

# llm用阿里千问大模型替换
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    api_key=&quot;key&quot;, # 用您的KEY替换
    base_url=&quot;https:&#47;&#47;dashscope.aliyuncs.com&#47;compatible-mode&#47;v1&quot;, 
    model=&#39;qwen-long&#39; 
    )

# 替换文本分割器 
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

# 替换向量存储 
from langchain_community.vectorstores import LanceDB
embeddings = embeddings_model

# 从加载器创建索引 
index_creator = VectorstoreIndexCreator(
    vectorstore_cls= LanceDB, # 使用LanceDB向量存储替换
    embedding=embeddings, # 使用百川智能嵌入模型替换
    text_splitter=text_splitter # 使用RecursiveCharacterTextSplitter文本分割器
)

query = &quot;各类建筑垃圾如何处理？&quot;
index = index_creator.from_loaders([loader])
# 在query需要增加大语言模型llm
result = index.query(llm = llm, question = query)
print(result)</div>2024-08-17</li><br/><li><img src="" width="30px"><span>yanyu-xin</span> 👍（1） 💬（0）<div># 文档加载器列表的图片表格中，示例代码的显示出现一些小错误。应该分隔的代码没有用空格分隔，单词连接在一起。如加载文本文档的代码：
from langchain.document_loaders import TextLoaderloader =
Textloader(&quot;example_data&#47;index.md&quot;)data = loader.load()

代码显示错误，应该在其中增加空格的，和增加换行：
from langchain.document_loaders import TextLoader
loader = Textloader(&quot;example_data&#47;index.md&quot;) 
data= loader.load()

# 文档加载和文本分割的示例代码都存在类似分隔、换行显示问题，建议修订。</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第15讲打卡~
一个典型的RAG系统的核心处理流程：Loading -&gt; Transform(Splitting) -&gt; Embedding -&gt; Store -&gt; Retrieving</div>2024-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/62/81a5a17d.jpg" width="30px"><span>ManerFan</span> 👍（1） 💬（0）<div>相比 langchain的Retrival和llama index，应该如何选择呢？</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（0） 💬（0）<div>想问下老师，RAG 如何与 Agent 结合呢？比如要做一个较通用的 Agent，对于用户的一些请求，可能并不需要查询数据，直接请求大模型即可，这种怎么处理？</div>2025-01-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erodJv4qrfPuPODosGMgKicodLr6tE8icXql5ks2tnp81FmNNkNdk7f0iclKdBUGAE197azmeGDSxs9g/132" width="30px"><span>Geek_2d85f8</span> 👍（0） 💬（0）<div>由于langchain的更新，课程里的VectorstoreIndexCreator使用时需要增加embedding，如：
index = VectorstoreIndexCreator(embedding=OpenAIEmbeddings()).from_loaders([loader])
同时在index.query中，也需要增加大语言模型llm（需提前创建），如：
index.query(llm = llm, question = query)</div>2024-07-11</li><br/>
</ul>