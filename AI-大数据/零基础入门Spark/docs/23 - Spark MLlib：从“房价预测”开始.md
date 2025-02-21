你好，我是吴磊。

从今天这一讲开始，我们进入课程的第三个模块：Spark MLlib机器学习。在数据科学、机器学习与人工智能火热的当下，积累一些机器学习的知识储备，有利于我们拓展视野，甚至为职业发展提供新的支点。

在这个模块中，我们首先从一个“房价预测”的小项目入手，来初步了解机器学习以及Spark MLlib的基本用法。接下来，我们会着重讲解机器学习的两个关键环节：特征工程与模型调优，在深入学习Spark MLlib的同时，进一步优化“房价预测”的模型效果，从而让房价的预测越来越准。

熟悉了关键环节之后，我们再去探讨，在Spark MLlib的框架之下，高效构建机器学习流水线的一般方法。好啦，话不多说，让我们先来一起看看“房价预测”这个小项目吧。

为兼顾项目的权威性与代表性，这里我选择了Kaggle（数据科学竞赛平台）的“[House Prices - Advanced Regression Techniques](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/overview)”竞赛项目。这个项目的要求是，给定房屋的79个属性特征以及历史房价，训练房价预测模型，并在测试集上验证模型的预测效果。

## 数据准备

虽然项目的要求相当清晰明了，不过你可能会说：“我没有机器学习背景，上面提到这些什么特征啊、模型啊，还有测试集、效果验证，我都没有概念，那接下来的课程，要怎么学呢？”别担心，随着课程的推进，我会逐渐把这些概念给你讲清楚。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（5） 💬（1）<div>House Prices - Advanced Regression Techniques 数据需要代理插件才能显示注册码。否则无法注册账号下载数据，数据可在这下载。
链接：https:&#47;&#47;pan.baidu.com&#47;s&#47;1J4LklHyYz5S6d32uZPp6nA 
提取码：xr96</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/08/9fd313d7.jpg" width="30px"><span>markliang</span> 👍（2） 💬（1）<div>看文章学习技术的同时，顺带可以学习文章里的写作方法和学习方法:联想方法，现实生活模型，费曼学习法，等等。学到的远不止是技术。👐格局打开</div>2021-11-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/w74m73icotZZEiasC6VzRUytfkFkgyYCGAcz16oBWuMXueWOxxVuAnH6IHaZFXkj5OqwlVO1fnocvn9gGYh8gGcw/132" width="30px"><span>Geek_995b78</span> 👍（1） 💬（1）<div>老师 可以把相关数据上传到git一份吗，不好下载</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ba/c6/10448065.jpg" width="30px"><span>东围居士</span> 👍（0） 💬（1）<div>老师，数据集上传到哪了呢，在你的 github 里面没找到</div>2021-12-05</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/wgMMrp1hvSB3E30KqZvMsj3KQdAI3T1uQM77LT7hZ65nVSjPGRg3AbUOyiahnssA6AIT5PAkyHFmlTBzUH9gdyQ/132" width="30px"><span>pythonbug</span> 👍（0） 💬（1）<div>老师好，“预测” 体现在哪里呢，是指我给特征向量，然后根据模型算出房价吗</div>2021-11-19</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/wgMMrp1hvSB3E30KqZvMsj3KQdAI3T1uQM77LT7hZ65nVSjPGRg3AbUOyiahnssA6AIT5PAkyHFmlTBzUH9gdyQ/132" width="30px"><span>pythonbug</span> 👍（0） 💬（1）<div>真的蛮好玩的，我迭代10次是40000多，我想试试迭代100次试试，结果43000多</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/f2/a8b0d8a6.jpg" width="30px"><span>千里马</span> 👍（0） 💬（1）<div>老师，数据不好下载，能提供一份么？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/7b/31a6bf42.jpg" width="30px"><span>强</span> 👍（0） 💬（2）<div>从性能调优过来的,打算看完之后。找工作了（被公司裁了）</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（1） 💬（1）<div>在训练集的数据分布中，房价的值域在（34900，755000）之间，因此，45798.86 的预测误差还是相当大的。

45798不是落在上面的区间内吗</div>2022-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLbGiciayvbAatOqQg1yycNxyRw8eqORSvsQrGVTxGjde33YY5Xdg1ddKhL6jWH0pdR2wy2FC0knt1w/132" width="30px"><span>刘英杰</span> 👍（0） 💬（0）<div>准备训练样本的代码改成了这样，样例代码跑下来字段并没有drop掉
&#47;&#47;调用 transform() 生成新 DataFrame
val transformedDF: DataFrame = assembler.transform(typedFields)

&#47;&#47; 显式删除 featureCols 指定的列
val featuresAdded = transformedDF.drop(featureCols: _*)</div>2025-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/jzribKIfoUZ60eibKFgU1zricHFjrJuZZHEtNcrI7SKa5Iz7CahfMDcMmmXUc9f6l9dB7jCiaj1ic1icgibf7vAPqNonQ/132" width="30px"><span>Geek_104e8e</span> 👍（0） 💬（0）<div>老师可以用Python重写一版吗？</div>2025-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3f/9d/c59c12ad.jpg" width="30px"><span>实数</span> 👍（0） 💬（0）<div>sparkml的模型是不是不如原生的python的anaconda算法包</div>2024-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/76/9a/2a8fa5ed.jpg" width="30px"><span>星星📷</span> 👍（0） 💬（0）<div>老师，结果必然是45798.86吗？</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/6f/3a97712e.jpg" width="30px"><span>林Curry</span> 👍（0） 💬（0）<div>代码里好像没有体现验证集的用法呀老师</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/52/f35f5265.jpg" width="30px"><span>空de</span> 👍（0） 💬（0）<div>spark3 的MLlib库有没有提供时序模型，可以处理时序数据的异常检测的需求？在生产中spark MLlib 处理时序异常检测是怎么做的，有没有案例推荐？</div>2022-03-17</li><br/>
</ul>