你好，我是黄鸿波。

上节课我们讲解了基于协同过滤的召回算法，本节课我们来介绍另外一种召回算法：基于Embedding的召回。

我把这节课分成了以下三个部分。

1. 什么是基于Embedding的召回。
2. 基于Embedding的召回算法都有哪几种。
3. DSSM模型。

## 基于Embedding的召回

协同过滤算法是从内容和用户的角度出发，根据用户的历史行为来进行内容推荐。在基于用户的协同过滤中，会认为与用户历史记录相似的其他用户对同一商品也可能感兴趣。而在基于Item的协同过滤中，则会考虑内容之间的相似度以及用户和内容之间的关系，从而计算出用户可能喜欢的内容进行推荐。但不管怎么样，这些内容实际上都是基于关系进行推荐的，并不关心内容的文本语义。

基于Embedding的算法与协同过滤最大的区别在于，它是从内容文本信息和用户查询的角度出发，利用预训练的词向量模型和深度学习模型，将文本信息转换成向量进行表示，通过计算两个向量之间的距离或者相似度来推荐内容。**这种方式主要考虑商品文本信息的语义信息，使推荐的内容更加精准。**

我来通过一个小例子说明下基于Embedding的召回是如何工作的。

假设我们要构建一个商品推荐系统，用户在平台上浏览了几个商品，比如一双运动鞋、一件T恤和一条牛仔裤。系统基于这些商品信息构建商品的Embedding向量表示，以及用户的Embedding向量表示。然后计算用户Embedding向量与所有商品Embedding向量之间的相似度，选取相似度最高的商品进行推荐。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mhSYbmpwSzVIEDu714dQuicXCf4ssKQ3LictIW6VoCFZ17EdanhRnhHEHmReiatJBrkUsfkXl4FsWU1JkoHqDiaxKA/132" width="30px"><span>19984598515</span> 👍（2） 💬（2）<div>老师你好，请问完整源码什么时候放出呢</div>2023-05-31</li><br/><li><img src="" width="30px"><span>Geek_40f5b6</span> 👍（0） 💬（1）<div>老师你好，“User 塔在线计算 User Embedding”是在推荐服务上进行计算吗，还是说会有一个单独的计算服务，为推荐服务提供计算结果</div>2023-06-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUXWqIBiadT4H3XvpcLeOkeocfmpInuhCoHviaUrX7B0N8wnOicnqHZeicKg1SlLk070EFRya1RPQIicw/132" width="30px"><span>爱极客</span> 👍（0） 💬（1）<div>用户Enbeding和商品Enbeding可以直接求相似度吗？</div>2023-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（0）<div>最近这几个章节没有代码实验吗？</div>2023-12-14</li><br/>
</ul>