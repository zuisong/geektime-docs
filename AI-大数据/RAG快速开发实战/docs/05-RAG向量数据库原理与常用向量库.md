> 本课程为精品小课，不标配音频。

你好，我是常扬。

在前面的课程中，我们已经学习了RAG检索流程中如何将文档数据解析、分块并转换为嵌入向量的操作。本节课将进一步掌握如何存储这些向量及其文档元数据，并高效地进行相似度检索。

![图片](https://static001.geekbang.org/resource/image/91/19/9110ece16990bf06ed1ddb60c9989a19.jpg?wh=1920x572)

在人工智能（AI）主导的时代，文字、图像、语音、视频等多模态数据的复杂性显著增加。由于这些数据具有非结构化和多维特征，向量表示能够有效表示语义和捕捉其潜在的语义关系，促使向量数据库成为存储、检索和分析高维数据向量的关键工具。

下图展示了向量数据库的分类，依据是否开源与是否为专用向量数据库，将其分为四类。

1. 第一类是**开源的专用向量数据库**，如 Chroma、Vespa、LanceDB、Marqo、Qdrant 和 Milvus，这些数据库专门设计用于处理向量数据。
2. 第二类是**支持向量搜索的开源数据库**，如 OpenSearch、PostgreSQL、ClickHouse 和 Cassandra，它们是常规数据库，但支持向量搜索功能。
3. 第三类是**商用的专用向量数据库**，如Weaviate和Pinecone，它们专门用于处理向量数据，但属于商业产品或通过商业许可获得源码。
4. 第四类是**支持向量搜索的商用数据库**，如Elasticsearch、Redis、Rockset和SingleStore，这些常规数据库支持向量搜索功能，同时属于商业产品或可通过商业许可获得源码。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/d0/e676ac19.jpg" width="30px"><span>梦典</span> 👍（7） 💬（2）<div>个人感受哈
首先，数据隐私安全要求高的场景，比如要求内网环境，优先选择开源向量数据库；
在此场景下，如果客户需求超出开源向量数据库的功能表现，需要加强或者定制，可以考虑商业许可并获得官方的技术支持；
其次，数据隐私安全要求不高的场景，优先选择开源向量数据库，以节约成本；
项目比较小考虑Chroma、Qdrant；项目比较大就Milvus；
如果LLM应用在无服务器环境比如lambda，优先选择Zilliz或者Pinecone；</div>2024-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/66/d0/2fb761be.jpg" width="30px"><span>Jaycee-张少同</span> 👍（3） 💬（1）<div>为了学习这节课恶补了向量、余弦相似、欧几里得距离等概念，哈哈哈。个人学习，我选择开源数据库，毕竟成本低；对于内网企业，是否基于闭源国产向量数据库更能保证数据安全性？</div>2024-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（2） 💬（2）<div>第5讲打卡~
关于向量数据库，我们项目中Pinecone和PGVector都在用，这两款各有优缺点，Pinecone成熟稳定，但是成本很高，而且无法支持业务自定义扩展；而PGVector使用起来比较方便，但是在存储空间和检索性能的优化上比Pinecone差一些。目前我们正在调研Zilliz Cloud，看看是否能与项目进行更好地适配~</div>2024-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/01/38/5daf2cfb.jpg" width="30px"><span>吴军旗^_^</span> 👍（0） 💬（1）<div>老师可以贴一下你 linux 的环境吗？</div>2024-12-23</li><br/>
</ul>