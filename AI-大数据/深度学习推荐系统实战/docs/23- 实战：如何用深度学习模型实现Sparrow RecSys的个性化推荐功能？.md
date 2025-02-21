你好，我是王喆。

今天又是一堂实战课。在这节课里，我会带你利用我们现阶段掌握的所有知识，来实现SparrowRecSys中“猜你喜欢”的功能。具体来说，我们会根据一位用户的历史行为，为TA推荐可能喜欢的电影。这个功能几乎会用到所有的推荐系统模块，包括离线的特征工程、模型训练以及线上的模型服务和推荐逻辑的实现。

如果说完成了[第14讲](https://time.geekbang.org/column/article/303641)的“相似电影”功能，还只是你“武功小成”的标志，那啃透了这节课的实践，就代表你掌握了推荐系统技术框架中的大部分内容，你就能在推荐系统的实际工作中做到“驾轻就熟”啦。

## “清点技能库”，看看我们已有的知识储备有哪些

正式开始实践之前，我们还是先来清点一次自己的技能库。看看经过推荐模型篇的学习，我们技能库中的“兵器”又增加了多少，哪些可以用来实现“猜你喜欢”这个功能。下面，我就按照从离线到线上，由数据到模型的顺序，为你依次梳理一下特征工程、模型离线训练、模型服务、推荐服务器逻辑这四大部分的技能点。

### 1. 模型特征工程

特征工程是所有机器学习项目的起点，咱们的推荐模型也不例外。为了训练推荐模型，我们需要准备好模型所需的样本和特征。此外，在进行模型线上推断的时候，推荐服务器也需要线上实时拼装好包含了用户特征、物品特征、场景特征的特征向量，发送给推荐模型进行实时推断。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/7c/5b/7a8d842c.jpg" width="30px"><span>Lucifer</span> 👍（24） 💬（1）<div>思考题：推荐服务器内部专门开发特征加工模块，进行一些人工的处理。比如点击率特征，实际上“点击”会包含多种点击行为，各种行为如何融合，需要灵活配置。既不能放在离线存（更新不便），也不能放在tf serving里（逻辑多了太慢）
1、tf serving只负责简单的模型运算；
2、离线redis等负责通用特征数据的存储；
3、推荐系统服务器进行数据加工</div>2020-12-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/55lYKUdcPFgUHibRYmaRiaBdrsmnLGOHdPp4OicjBh197X0vyGa9qAwruEqicAPuUgibXO4Lz5jLudlcbtsqq2p3CpA/132" width="30px"><span>Sebastian</span> 👍（9） 💬（4）<div>思考题：特征分为静态特征和动态特征。对于静态特征，基本长时间不会变更，这块直接从特征池（可以是Redis）里取。但是对于动态特征，比如用户实时行为的特征，这种会通过流式处理（比如spark streaming或者flink）后，直接落盘，同时可以避免特征穿越。特征实时更新后，线上服务阶段，模型的输入就是未进行处理的原格式数据，tf serving 接受请求后，在模型里进行特征预处理，比如使用tf.feature_column进行处理，转为one hot和embedding格式。

但是在QPS很高的场景下，这种处理可能达不到上线要求，想问老师有什么好的解决方案？</div>2020-12-04</li><br/><li><img src="" width="30px"><span>tuomasiii</span> 👍（6） 💬（1）<div>想问下老师图1里，“候选物品库”里是放的embeddings还是actual data？ 
因为我们召回层用embedding来算similarity的话，到底是从redis里读还是到候选物品库拿？</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6d/c5/c0665034.jpg" width="30px"><span>Wiiki</span> 👍（5） 💬（1）<div>非常感谢王老师的细心分享，让我们从零到一建立起推荐系统的概念和实践经验~  谢谢~</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6d/c5/c0665034.jpg" width="30px"><span>Wiiki</span> 👍（3） 💬（5）<div>王老师，您好。更新了你最近的工程代码，发现新增了pyspark推荐系统的工程实现部分，想请教一下：对于大数据量的特征工程处理，选择用scala还是python版的spark实现有没有什么建议？ 谢谢~</div>2020-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/5d/562e90d6.jpg" width="30px"><span>金鹏</span> 👍（3） 💬（1）<div>王喆老师好，请教个问题，现在边缘计算或端智能，多大程度解决了用户特征更新的问题，端智能的应用前景如何？</div>2020-12-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEINKG7h0MpuMdBncDnl8Hv9RtX4OTs6Wg3O7ibs2AOch14SwVecEWmGkmnHouIEsgJjoDe1D7LSHqg/132" width="30px"><span>Berton</span> 👍（3） 💬（1）<div>特征处理这部分，应该是离线计算好得到每个特征的map数据，在推荐服务器内部加载这些map数据，直接将原始特征映射成深度学习需要的向量，将得到的向量送入Tensorflow Serving得到推荐结果
如果在Tensorflow Serving做特征预处理的工作，会导致推荐服务的响应时间边长</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ee/9c/abb7bfe3.jpg" width="30px"><span>abc-web</span> 👍（2） 💬（1）<div>王老师请问一下，在线推断需要拼装数据提交请求，但数据量大的情况下会影响效率，那除了拼装还有没有其他的方式可用</div>2021-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9e/2e/ad69bd71.jpg" width="30px"><span>liuqqwwe</span> 👍（1） 💬（1）<div>王老师，如果想要结合移动端上实时反馈信息，比如迅速划过以及短播这种隐式负反馈，长播、点赞这些正反馈，结合后端下发的用户和部分物品的embedding信息对缓存内容进行前端重排序，这种场景选用什么模型合适呢，如何合并新操作产生的输入呢</div>2021-07-19</li><br/><li><img src="" width="30px"><span>tuomasiii</span> 👍（1） 💬（1）<div>想问下图中Redis到排序层的线上特征具体是指的哪些特征？ 
是像geographic和current timestamp这些feature吗？

还有就是排序层模型的loss都是使用entropy的loss？
像warp loss和bpr这些能被使用到吗？

谢谢！</div>2021-01-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/55lYKUdcPFgUHibRYmaRiaBdrsmnLGOHdPp4OicjBh197X0vyGa9qAwruEqicAPuUgibXO4Lz5jLudlcbtsqq2p3CpA/132" width="30px"><span>Sebastian</span> 👍（1） 💬（1）<div>老师，我想问下关于“推荐服务器内部专门开发特征加工模块”：如果不单独做特征加工模块，而是把特征做预处理后弄一张编码表，10秒更新一次编码表，在线请求过来后直接读这张编码表的特征，这种方案是否可行？这样是不是也同时避免了线上线下特征处理不一致的问题？</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/5d/75/57b77cdb.jpg" width="30px"><span>masiwei</span> 👍（0） 💬（2）<div>想请教下大家，我理解是online&#47;recprocess&#47;RecForYouProcess.java文件里，召回是通过电影评分高低，排序是通过embedding或者nerualCF，而老师讲的召回是用embedding，排序是用nerualCF。不知道我理解的对不对？那种方式，是代码里的方式还是老师讲义里的方式，在实际产品中更合理和普遍呢？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e5/fb/b2c82caa.jpg" width="30px"><span>X.G</span> 👍（0） 💬（3）<div>基础架构篇里说，最终的系统会有这个功能：随着当前用户不断为电影打分，系统会对首页的推荐结果进行个性化的调整，比如电影类型的排名会进行个性化调整，每个类型内部的影片也会进行个性化推荐。请问这个打分功能也是在后期课程中增加吗？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b5/8b/92549066.jpg" width="30px"><span>Geek_8183d5</span> 👍（8） 💬（1）<div>如果是M1芯片的mac，官方 tensorflow-serving 镜像并不支持。您可以在docker中导入模型时通过如下命令使用第三方镜像：（记得把路径$YOUR PATH$替换为您自己的哦）
docker run -t --rm -p 8501:8501     -v &quot;$YOUR PATH$&#47;neuralcf:&#47;models&#47;recmodel&quot;     -e MODEL_NAME=recmodel     emacski&#47;tensorflow-serving:2.6.0  &amp;</div>2022-04-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIAovgSHkL6KXasuk093J0JYOLPVicsI9Wrv9pj3ACsMorBpIOzOVNXfauvibicDml7nCv7zuWtqLlsA/132" width="30px"><span>Geek_471665</span> 👍（0） 💬（0）<div>请问docker部署Tensorflow Serving后，为什么只能本地访问呢？外部访问curl、restful api均失败，已经配置了8501防火墙</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/58/ce/1d069c94.jpg" width="30px"><span>wjc</span> 👍（0） 💬（0）<div>tf1的模型能部署吗？</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7a/cf/c42dd74e.jpg" width="30px"><span>sky</span> 👍（0） 💬（0）<div>这里的最开始的触发输入是什么呢？？感觉没有搜索那么明确</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b7/42/1f44ce49.jpg" width="30px"><span>远方蔚蓝</span> 👍（0） 💬（0）<div>请问一下怎么保存和查看tensorflow serving接收请求的log日志</div>2021-06-19</li><br/>
</ul>