你好，我是郑晔！

上一讲，我们用了一讲的篇幅介绍了一下 RAG。你现在已经对 RAG 有了一个初步的了解，这一讲，我们就要动手实现一个 RAG 应用了。

我们知道 RAG 有两个核心的过程，一个是把信息存放起来的索引过程，一个是利用找到相关信息生成内容的检索生成过程。所以，我们这个 RAG 应用也要分成两个部分：**索引和检索生成**。

RAG 是为了让大模型知道更多的东西，所以，接下来要实现的 RAG 应用，用来增强的信息就是我们这门课程的内容，我会把开篇词做成一个文件，这样，我们就可以和大模型讨论我们的课程了。LangChain 已经提供了一些基础设施，我们可以利用这些基础设施构建我们的应用。

我们先从索引的过程开始！

## 索引

我们[上一讲](https://time.geekbang.org/column/article/827289)已经讲过了索引的基本过程，你可以先回顾一下，这样结合代码看起来就比较容易理解了：

![](https://static001.geekbang.org/resource/image/bd/a2/bdba19e4bbcd2d5bc548cd23372a86a2.jpg?wh=2202x471)

下面是实现这个索引过程的代码：

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("introduction.txt")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma(
    collection_name="ai_learning",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="vectordb"
)
vectorstore.add_documents(splits)
```
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/31/48/e7/958b7e6c.jpg" width="30px"><span>高并发</span> 👍（2） 💬（1）<div>关于embeddings的替换,可以参考这个文章: https:&#47;&#47;www.langchain.com.cn&#47;docs&#47;integrations&#47;vectorstores&#47;chroma&#47;</div>2024-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（2） 💬（2）<div>不需要先安装Chroma数据库吗? </div>2024-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（1）<div>跑例子总是遇到库不存的报错，用pip 安装库后还是不行，大家有遇到类似的问题吗，Macbook Pro M4芯片 。  from langchain_chroma import Chroma
ModuleNotFoundError: No module named &#39;langchain_chroma&#39; 

执行 pip3 install chromadb安装后仍然报错。

这是版本
Name: langchain
Version: 0.3.14
Summary: Building applications with LLMs through composability
Home-page: https:&#47;&#47;github.com&#47;langchain-ai&#47;langchain
Author:
Author-email:
License: MIT
Location: &#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.12&#47;lib&#47;python3.12&#47;site-packages
Requires: aiohttp, langchain-core, langchain-text-splitters, langsmith, numpy, pydantic, PyYAML, requests, SQLAlchemy, tenacity
Required-by: langchain-community
</div>2025-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（0） 💬（1）<div>感觉Text split的chunk size是个很有意思的东西。太小太碎了检索的时候容易漏东西。太大了又容易让generation吃的context太多，浪费token。</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（0） 💬（2）<div>每次从chroma里检索，也要消耗embedding model的token吗？如果是的话，这个消耗量和chroma里存储的数据总量呈正相关吗？</div>2025-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/32/3de6a189.jpg" width="30px"><span>范</span> 👍（0） 💬（1）<div>对于OpenAI兼容性的向量接口，可以参考如下：
embeddings=OpenAIEmbeddings(
   openai_api_key=os.getenv(&#39;OPENAI_API_KEY&#39;),
    openai_api_base=os.getenv(&#39;OPENAI_API_BASE&#39;),
    model=&quot;BAAI&#47;bge-large-zh-v1.5&quot;
)

vector_store = Chroma(
    collection_name=&quot;example_collection&quot;,
    embedding_function=embeddings,
    persist_directory=&quot;.&#47;chroma_langchain_db&quot;,  # Where to save data locally, remove if not necessary
)
</div>2024-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（0） 💬（1）<div>经过Retriever加持的prompt，是否会容易超长？</div>2024-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（5） 💬（0）<div>本节代码在此：https:&#47;&#47;github.com&#47;groklab&#47;misc&#47;blob&#47;main&#47;geektime-llm-zhengye-column&#47;lec11.ipynb</div>2024-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第11讲打卡~
实现了一个增强版的RAG应用，主要功能包括:
1. 使用Pinecone向量数据库，持久化向量。
2. 实现了文档加载器的映射，可以根据文件的扩展类型，选择对应的加载器。
3. 采用关键词+语义相似度结合的混合检索方式，提升检索的准确率。
4. 实现了重排序机制，将权重较高的检索结果优先返回。

完整代码：
https:&#47;&#47;gitee.com&#47;zhangshenao&#47;happy-rag&#47;tree&#47;master&#47;RAG%E5%BF%AB%E9%80%9F%E5%BC%80%E5%8F%91%E5%AE%9E%E6%88%98&#47;1-%E5%BF%AB%E9%80%9F%E6%90%AD%E5%BB%BARAG%E5%BA%94%E7%94%A8</div>2025-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（1） 💬（0）<div>还是建议作者把完整可运行例子全部提供下，统一可以放在仓库里。对新手友好一些。</div>2025-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/29/2478f7d0.jpg" width="30px"><span>CPF</span> 👍（1） 💬（0）<div>评论区不能贴图，那放链接吧 https:&#47;&#47;askurl.cn&#47;qjK8W3ot</div>2025-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/47/41e4bada.jpg" width="30px"><span>XXL</span> 👍（0） 💬（0）<div>老师提供一下代码仓库吧，这个成本应该不高，不然对新手很不友好</div>2025-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（0）<div>有没有把老师的例子都跑通的大佬，联系我，可以有偿</div>2025-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（0）<div>import chromadb
from langchain.vectorstores import Chroma

# 使用 Chroma 初始化存储
client = chromadb.Client()
vector_store = Chroma(client=client)


这个才是对的</div>2025-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（0）<div>LangChain 的声明式编程体现了软件设计是一门艺术，很美～</div>2025-01-10</li><br/>
</ul>