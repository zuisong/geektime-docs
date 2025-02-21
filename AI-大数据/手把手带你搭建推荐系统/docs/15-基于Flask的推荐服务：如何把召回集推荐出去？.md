你好，我是黄鸿波。

在前面的课程中，我们搭建了一个简单的Flask服务，并且已经可以通过Postman来进行调用，这节课我们将在此基础上，把基于规则的召回集成进来并推荐给用户。这节课你会学到下面的内容。

1. 写一个基于时间的召回，并存储到Redis数据库中。
2. 编写一个翻页查询服务，能够进行翻页查询。
3. 编写Service服务，将基于时间的召回推荐给用户。

## 编写基于时间的召回

推荐系统如果想要将内容推荐给用户，首先要做的就是要找到合适的内容，然后将这些内容通过一定的整理和排序，按照一定的规则推荐给用户。这些规则可能是时间、热度、相似度以及一些用于特征的评分，也可以是这些中一个或者多个算法的结合。在这节课里，我们就先用简单的基于时间的召回算法来做。

首先，我们来回顾一下我们之前的内容画像，下图是内容画像其中的一条数据。

![图片](https://static001.geekbang.org/resource/image/b5/ac/b5dfdc8ac8f03980aebe4de0ba3017ac.png?wh=1920x254)

我们可以看到，我们的用户画像实际上是由10个字段组成，在这10个字段中，第一个字段 \_id 是MongoDB数据库为我们生成的一个唯一的id值，我们可以用其作为索引，来标记其唯一性。

与时间相关的字段有2个，一个是news\_date，另一个是create\_time。在这两个字段中，news\_date表示的是新闻发布的时间，create\_time指的是这个新闻的入库时间（也就是爬虫爬取的时间），这两个时间作为特征数据在不同的算法中有不同的用处。我们目前是想要基于时间来进行召回，这个时间最好使用新闻的发布时间，因为新闻发布时间属于新闻本身的一个特征，可以防止“时间穿越”事件的发生。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/ba/42/5ca553bd.jpg" width="30px"><span>Weitzenböck</span> 👍（0） 💬（1）<div>这个代码到底在哪里啊？学了那么久了都没有看到</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>Q1：源码链接已经提供了吗？
Q2：百度首页会提供推荐列表，估计是什么算法？
Q3：本文开始的“分数”，是根据什么确定的？某一个值可能选一个特殊值，比如特别大的数值，那其他的分数呢？</div>2023-05-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/EaBxhibOicZe9L7z2icbU4W462l543drFWYqibqczTicj4Msyb2g9pDSGmFTiafW9jibwib7jG6hpAdPMcCowdCiaxHaOdA/132" width="30px"><span>Geek_ccc0fd</span> 👍（0） 💬（1）<div>从mongodb获取排序数据报错：pymongo.errors.OperationFailure: FieldPath field names may not start with &#39;$&#39;.
发现不需要带$,我的pymongo版本4.3.3，正确代码：
data = self.collection_test.find().sort([{&quot;$news_date&quot;, -1}])
</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/8a/be3b7ae6.jpg" width="30px"><span>叶圣枫</span> 👍（0） 💬（0）<div>StrictRedis 构造的时候要指定本地的db id，不一定是db=10. 
我的本地是0。</div>2024-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/67/fe/5d17661a.jpg" width="30px"><span>悟尘</span> 👍（0） 💬（1）<div>文稿中的代码示例和github里的代码不一样呀，有点出入，应该以哪个为准？</div>2023-12-13</li><br/>
</ul>