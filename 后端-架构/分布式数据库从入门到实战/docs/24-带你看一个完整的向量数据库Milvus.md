你好，我是彭旭。

前面几节课我们介绍了Faiss，学习了使用Faiss构建索引与向量化检索，也用Faiss来搭建了一个简单的人脸识别应用。

通过对Faiss的介绍，你应该知道，Faiss不像数据库一样持久化存储向量化数据，而是每次使用之前，都需要从硬盘等持久化设备读取数据，加载索引。并且Faiss也没有一个数据库所需要的数据管理功能。所以 [DBRanking](https://db-engines.com/en/ranking/vector+dbms) 对向量数据库的排名，并没有将Faiss包括在内。

那有没有一个具备完整的数据存储、管理功能的向量数据库产品呢？

有，就是我们这节课要介绍的Milvus。

## Milvus是什么？

Milvus其实是基于Faiss、HNSW、DiskANN、SCANN（Scalable Approximate Nearest Neighbor）等这些向量检索库构建的，被设计用来做稠密向量的相似性检索。它可以支持十亿，甚至万亿以上向量化数据的存储检索。

Milvus支持数据分片、动态Schema、单向量检索、多向量检索、向量与标量混合检索以及许多其他高级功能。

与StarRocks类似，Milvus也支持存算分离。因为Milvus使用MinIO对象存储来存储日志文件的快照、索引文件、数据以及一些查询的中间结果，所以能够快速地部署在兼容MinIO协议的AWS S3和Asure Blob上。