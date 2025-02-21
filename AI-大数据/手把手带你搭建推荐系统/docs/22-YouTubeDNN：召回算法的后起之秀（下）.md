你好，我是黄鸿波。

上节课我们讲了关于YouTubeDNN的召回模型，接下来，我们来看看如何用代码来实现它。

我们在做YouTubeDNN的时候，要把代码分成两个步骤，第一个步骤是对数据的清洗和处理，第二个步骤是搭建模型然后把数据放进去进行训练和预测。

## 数据的清洗和处理

先来讲数据部分。

按照YouTubeDNN论文来看，输入的数据是用户的信息、视频的ID序列、用户搜索的特征和一些地理信息等其他信息。到了基于文章内容的信息流产品中，就变成了用户ID、年龄、性别、城市、阅读的时间戳再加上视频的ID。我们把这些内容可以组合成YouTubeDNN需要的内容，最后处理成需要的Embedding。

由于前面没有太多的用户浏览数据，所以我先造了一批数据，数据集我会放到GitHub上（后续更新），数据的形式如下。

![图片](https://static001.geekbang.org/resource/image/ea/0a/eaeef45b0eb7e64c3f11c4a252f8120a.png?wh=1379x1424)

接下来我们就把这批数据处理成YouTubeDNN需要的形式。首先在recommendation-class项目中的utils目录下建立一个preprocess.py文件，作为处理数据的文件。

我们要处理这一批数据，需要下面五个步骤。

1. 加载数据集。
2. 处理数据特征。
3. 特征转化为模型输入。
4. 模型的搭建和训练。
5. 模型评估。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（1）<div>有两个问题没弄明白，请老师指点：
1、embedding_dim的大小是如何确定的？
2、什么时候用离散特征，什么时候用变长特征？</div>2023-09-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUXWqIBiadT4H3XvpcLeOkeocfmpInuhCoHviaUrX7B0N8wnOicnqHZeicKg1SlLk070EFRya1RPQIicw/132" width="30px"><span>爱极客</span> 👍（1） 💬（2）<div>老师，后面会出一篇课后答疑的文章吗？</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/d3/2bbc62b2.jpg" width="30px"><span>alexliu</span> 👍（0） 💬（1）<div>老师，faiss.IndexFlagIP这个应该是faiss.IndexFlatIP吧？另外index.add(n,x)有两个参数，为什么在代码里只有item_embs一个参数？
ps：add源码如下：
    def add(self, n, x):
        r&quot;&quot;&quot; default add uses sa_encode&quot;&quot;&quot;
        return _swigfaiss.IndexFlatCodes_add(self, n, x)</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>YoutubeDNN是拿来就能用吗？类似于工具软件那种，不需要开发。</div>2023-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2c/bc/5311e976.jpg" width="30px"><span>Emma</span> 👍（1） 💬（0）<div>请问老师，youtubeDNN的排序部分的代码有吗</div>2024-09-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUXWqIBiadT4H3XvpcLeOkeocfmpInuhCoHviaUrX7B0N8wnOicnqHZeicKg1SlLk070EFRya1RPQIicw/132" width="30px"><span>爱极客</span> 👍（0） 💬（1）<div># 定义模型
        model = YoutubeDNN(self.user_feature_columns, self.item_feature_columns, num_sampled=100,
                           user_dnn_hidden_units=(128, 64, self.embedding_dim))  

这个参数 num_sampled=100 在新版的模型API里面是没有的，希望老师解答</div>2024-06-30</li><br/>
</ul>