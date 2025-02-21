你好，我是黄佳，欢迎来到LangChain实战课！

在深入讲解LangChain的每一个具体组件之前，我想带着你从头完成一个很实用、很有意义的实战项目。目的就是让你直观感受一下LangChain作为一个基于大语言模型的应用开发框架，功能到底有多么强大。好的，现在就开始！

## 项目及实现框架

我们先来整体了解一下这个项目。

**项目名称**：“易速鲜花”内部员工知识库问答系统。

**项目介绍**：“易速鲜花”作为一个大型在线鲜花销售平台，有自己的业务流程和规范，也拥有针对员工的SOP手册。新员工入职培训时，会分享相关的信息。但是，这些信息分散于内部网和HR部门目录各处，有时不便查询；有时因为文档过于冗长，员工无法第一时间找到想要的内容；有时公司政策已更新，但是员工手头的文档还是旧版内容。

基于上述需求，我们将开发一套基于各种内部知识手册的 “Doc-QA” 系统。这个系统将充分利用LangChain框架，处理从员工手册中产生的各种问题。这个问答系统能够理解员工的问题，并基于最新的员工手册，给出精准的答案。

**开发框架**：下面这张图片描述了通过LangChain框架实现一个知识库文档系统的整体框架。

![](https://static001.geekbang.org/resource/image/c6/bf/c66995f1bf8575fb8fyye6293200eabf.jpg?wh=1393x697 "基于数据源的文档问答系统开发框架")

整个框架分为这样三个部分。

- 数据源（Data Sources）：数据可以有很多种，包括PDF在内的非结构化的数据（Unstructured Data）、SQL在内的结构化的数据（Structured Data），以及Python、Java之类的代码（Code）。在这个示例中，我们聚焦于对非结构化数据的处理。
- 大模型应用（Application，即LLM App）：以大模型为逻辑引擎，生成我们所需要的回答。
- 用例（Use-Cases）：大模型生成的回答可以构建出QA/聊天机器人等系统。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/9d/a9/4602808f.jpg" width="30px"><span>黄佳</span> 👍（16） 💬（2）<div>各位同学，好消息，本课代码我已经根据LangChain 0.2版本进行了更新，减少了warning！请大家Clone新的Github Repo参考DocQA_v0.2.py。https:&#47;&#47;github.com&#47;huangjia2019&#47;langchain
</div>2024-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/20/1c/de379ed1.jpg" width="30px"><span>shatu</span> 👍（20） 💬（3）<div>学习小结：
排坑点：
1.文本分割默认采用“utf-8”，中文字符会出错，改为“gbk”后解决
问题点：
1.MultiQueryRetriever在代码中的意义是什么？
2.Langchain中不同Retrievers应该如何选择？
3.对于中文而言，如何判断不同文本分割方法的效果差异？</div>2023-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/h5jfedUT5Sv7ibzM8WNCxoO9c136UUXDroaib2BUVILcZVp0FFBiaDPEbzPVv1J94LhR4oianox3wgyWpUBbtNJs0A/132" width="30px"><span>Geek_ebb87d</span> 👍（15） 💬（3）<div>其实不仅图片，文档中如果有表格，处理问答的效果也不好，表格方面老师是否有思路？
</div>2023-09-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKDZx5XkVZFrlIxDEhWiatEmLLDtD7M5B35rJacp6qMUpdXDZpvpw3o7bCPqcUCWUWXM8q7PRelOZg/132" width="30px"><span>Geek_439927</span> 👍（10） 💬（2）<div>老师，我想通过Langchain +开源大模型搭建一个私有化的知识库GPT，文件内容是文字+图片，图片的内容没有文字，你可以想象成这个文件是一个系统操作手册，手册里面有一些文字描述，以及一步一步地操作截图，这种格式的文档可行吗，在LLM给出的回答中，希望能够显示这些图片</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（9） 💬（1）<div>老师能不能提供一下文章中代码完整源码</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（5） 💬（1）<div>深入浅出，相当清晰</div>2023-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/a4/b060c723.jpg" width="30px"><span>阿斯蒂芬</span> 👍（4） 💬（2）<div>跟着老师代码敲一遍，解决过程中遇到的问题，成功run起来之后，还是小有成就感的😎</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（4） 💬（3）<div>这里切割文本，生成的向量数据库，保存在内存中吗？</div>2023-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/65/6016b046.jpg" width="30px"><span>清风明月</span> 👍（3） 💬（1）<div>如果文档有更新怎么更新索引</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/84/6a/8599e17f.jpg" width="30px"><span>敬</span> 👍（3） 💬（2）<div>我用OpenAIEmbeddings查询出来的结果不对，后来该用text2vec-base-chinese才正常。 </div>2023-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/a7/ba/66b4aebe.jpg" width="30px"><span>南风北巷</span> 👍（3） 💬（2）<div>老师，想问一下文本切割粒度怎样是合适的呢？粗粒度的文本被检索出来之后给大模型参考，大模型总会被文本中的无关信息干扰; 而细粒度的文本，我又怕检索出来的信息不全，缺少上下文信息，导致大模型没法给出正确答案。请问老师是怎么在工程中平衡切割文本的长短的呢？</div>2023-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/f9/352365e3.jpg" width="30px"><span>徐冰</span> 👍（2） 💬（1）<div>黄老师你好，想请教下，我把大模型改成了使用阿里云的灵积大模型平台的通义千问API，同时使用灵积的&quot;text-embedding-v2&quot;的模型做文档的向量化处理。但是 做向量化的时候，发现这个灵积的&quot;text-embedding-v2&quot;这个api单次请求文本最大行数限制为最大25行。
demo中的pdf文档数据， documents.extend(loader.load())这一步是，我看documents列表大小就是35，
后面调整分片大小，text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=10)，chunk_size再大，分片数最小也是35，导致调用api超过最大行数限制。这块有什么办法处理下吗？</div>2024-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（2） 💬（1）<div>如果一个大模型 使用的医学的知识库训练完成的，那我针对这个大模型再对法律经过 数据准备和载入、文本分割、向量数据库存储、相关信息的获取 等本文中的步骤，那这个大模型能提供法律的相关回答吗？该大模型提供的医学的及对法律提供的回答准确度 哪个更高一些？</div>2023-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcFhGY0NV4kFzOSXWDHR2lrI2UbUP4Y016GOnpTH7dqSbicqJarX0pHxMsfLopRiacKEPXLx7IHHqg/132" width="30px"><span>一路前行</span> 👍（2） 💬（2）<div>qdrant，chromadb,fiass老师在这些向量库的选择上有什么建议么</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/fc/147e38d9.jpg" width="30px"><span>Lominnave</span> 👍（2） 💬（2）<div>请问老师，对于DB的结构化数据进行知识库建设，如何进行Embedding设计呢？</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1f/2d/90648df8.jpg" width="30px"><span>进击的矮人</span> 👍（1） 💬（1）<div>老师, 代码还没更新呀</div>2024-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/cb/27b88c1c.jpg" width="30px"><span>风格若干</span> 👍（1） 💬（1）<div>LangChain 官方文档对 Document QA 系统设计及实现的详细说明，v0.1的链接失效了，老师方便帮忙找一下0.2版本的吗？</div>2024-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/b8/0f3bd8ec.jpg" width="30px"><span>曹胖子</span> 👍（1） 💬（1）<div>新的：
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader

from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings</div>2024-05-10</li><br/><li><img src="" width="30px"><span>Geek_094518</span> 👍（1） 💬（1）<div>排坑点2 

要安装 pip install tiktoken

从 langchain 导入向量存储和嵌入式模块的做法已被弃用,将在未来版本中被移除。您需要从 langchain-community 包中导入它们。例如:

from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
</div>2024-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/hllDt1dmuR6iciaahutPe9NjOic5OPMc7fbTysLTn8wgCSPW3zjYvd5rYDWBwQkSmqfsFntK12fLmam63FWpMklfg/132" width="30px"><span>dydcm</span> 👍（1） 💬（1）<div>目前想用langchain知识图谱的图数据库与大模型结合，请问老师有什么建议方案吗？</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（1） 💬（2）<div>老师，ES是向量数据库吗？分割后的文本，能否存储于ES里？</div>2023-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/01/eb3ba274.jpg" width="30px"><span>一面湖水</span> 👍（1） 💬（1）<div>langchain的document_loaders目前都支持哪些文档类型呢？</div>2023-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/56/50/3fdfdceb.jpg" width="30px"><span>张汝成</span> 👍（1） 💬（2）<div>老师请问一下，我想在langchain里调用国产大模型，比如讯飞星火大模型，但我看langchain官网上它还没有被集成进去，那应该如何使用呢？</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/17/796a3d20.jpg" width="30px"><span>言十年</span> 👍（1） 💬（6）<div>embeddings被限流了。大家怎么跑的呢？

&#47;embeddings
Retrying langchain.embeddings.openai.embed_with_retry.&lt;locals&gt;._embed_with_retry in 4.0 seconds as it raised RateLimitError: Rate limit reached for default-text-embedding-ada-002 in organization org-ZK1ptPebNCVCArIQG8s81jxx on requests per min. Limit: 3 &#47; min. Please try again in 20s. Contact us through our help center at help.openai.com if you continue to have issues. Please add a payment method to your account to increase your rate limit. Visit https:&#47;&#47;platform.openai.com&#47;account&#47;billing to add a payment method..</div>2023-09-30</li><br/><li><img src="" width="30px"><span>Geek_144417</span> 👍（0） 💬（1）<div>请问loader = PyPDFLoader(file_path)   documents.extend(loader.load()) 经过这一步，documents存的是什么，或者loader.load()是什么，是pdf的图片还是pdf编码成一段编码还是pdf解析后提取的文字和图片？</div>2024-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/64/7912c306.jpg" width="30px"><span>Amir</span> 👍（0） 💬（4）<div>智谱清言的embedding2 生成embedding效果还行，需要自己根据langchain 的 Embeddings自己实现一下</div>2024-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9doFL0ZzcWf5gkQ10cHsOziamhHicjq1k2KHvJibkicBjHsKyvf9jMepvdgLFiadiaI8PScf73Pl7QK3ibp6MYicWn9BuQ/132" width="30px"><span>Geek_6df977</span> 👍（0） 💬（1）<div>有人遇到这个报错吗
vectorstore = Qdrant.from_documents(
    documents=chunked_documents,  # 以分块的文档
    embedding=OpenAIEmbeddings(),  # 用OpenAI的Embedding Model做嵌入
    location=&quot;:memory:&quot;,  # in-memory 存储
    collection_name=&quot;my_documents&quot;, ) 

    vector_size = len(partial_embeddings[0])
                      ~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range  </div>2024-05-08</li><br/><li><img src="" width="30px"><span>Geek_094518</span> 👍（0） 💬（1）<div>排坑建议:

在您的Python代码中,将从langchain导入文档加载器的语句替换为从langchain-community导入。例如,如果您有以下导入语句:


from langchain import Docx2txtLoader
from langchain import TextLoader
请将它们替换为:

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/45/e9/4947093c.jpg" width="30px"><span>！</span> 👍（0） 💬（1）<div>Traceback (most recent call last):
  File &quot;&#47;Users&#47;wangrui&#47;Documents&#47;dev&#47;project&#47;python&#47;langchain-learning&#47;answer_QA.py&quot;, line 34, in &lt;module&gt;
    vectorstore = Qdrant.from_documents(
  File &quot;&#47;Users&#47;wangrui&#47;anaconda3&#47;envs&#47;py3.9&#47;lib&#47;python3.9&#47;site-packages&#47;langchain_core&#47;vectorstores.py&quot;, line 508, in from_documents
    return cls.from_texts(texts, embedding, metadatas=metadatas, **kwargs)

    return self._request(
  File &quot;&#47;Users&#47;wangrui&#47;anaconda3&#47;envs&#47;py3.9&#47;lib&#47;python3.9&#47;site-packages&#47;openai&#47;_base_client.py&quot;, line 930, in _request
    raise self._make_status_error_from_response(err.response) from None
openai.InternalServerError: Internal Server Error 请问这是啥原因</div>2024-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2a/f5/30d1f7b9.jpg" width="30px"><span>森。</span> 👍（0） 💬（1）<div>老师您好，我在实践中，通过大模型把一个句子转成我想要的结构化json，效果不是很理想，已经输给了几个例子了，但出来的结果不稳定，有哪些优化思路</div>2023-12-25</li><br/>
</ul>