你好，我是彭旭。

在上一讲中，我们探讨了人工智能领域对于数据的向量化表达以及相应的存储和检索需求，这极大地促进了向量数据库技术的发展。

自从2017年FaceBook开源了Faiss后，从2019年到2020年，市场上诞生了许多优秀的向量数据库，据 [DBRanking](https://db-engines.com/en/ranking/vector+dbms) 对向量数据库的排名所示，最新流行的纯向量数据库排名靠前的包括如Pingcone、Chroma、Weaviate、Milvus等。

让人奇怪的是，这个榜单竟然没有把Faiss包含在内。在我看来，这是因为Faiss其实不能算是一个完整的数据库。

为什么呢？

我们先来看一下Faiss提供了什么能力。

## Faiss是什么？

官方对Faiss的介绍是“Faiss是一个用于高效相似性搜索和密集向量聚类的库”。注意，这里说Faiss是一个库，而没有说是一个数据库。

事实上，Faiss是用C++编写的，并提供了一个Python的封装，而Faiss对外提供的服务就是一个Python的依赖库，所以它并不具备一个完整的数据库的功能，甚至不具备数据的持久化能力、数据的管理能力。

比如说Faiss每次在程序中访问之前，都需要重新加载数据，然后基于这些数据在内存中构建索引。但是程序一旦结束，这些数据就在内存中消亡了，并不会被持久化存储。除非手动调用Faiss的API将构建好的索引数据，以文件的形式存储到磁盘。但是，就算存储下来，也没有一个管理工具可以查看这些数据，只能在Faiss重新启动后，再去加载这个文件。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyhbzdkFM64Npva5ZKf4IPwhy6rDAX0L77QNESbalnXhnGKibcTbwtSaNC0hO6z0icO8DYI9Nf4xwg/132" width="30px"><span>eriklee</span> 👍（0） 💬（1）<div>请问老师，faiss与其他向量数据库检索相比有什么优势呢？是检索速度更快，还是有其他优点呢？</div>2024-08-11</li><br/>
</ul>