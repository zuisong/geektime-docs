你好，我是吴磊。

前面我们一起学习了如何在Spark MLlib框架下做特征工程与模型训练。不论是特征工程，还是模型训练，针对同一个机器学习问题，我们往往需要尝试不同的特征处理方法或是模型算法。

结合之前的大量实例，细心的你想必早已发现，针对同一问题，不同的算法选型在开发的过程中，存在着大量的重复性代码。

以GBDT和随机森林为例，它们处理数据的过程是相似的，原始数据都是经过StringIndexer、VectorAssembler和VectorIndexer这三个环节转化为训练样本，只不过GBDT最后用GBTRegressor来做回归，而随机森林用RandomForestClassifier来做分类。

![图片](https://static001.geekbang.org/resource/image/51/0b/51a23f4c00c6048f262eb6006f66600b.jpg?wh=1920x585 "重复的处理逻辑")

不仅如此，在之前验证模型效果的时候我们也没有闭环，仅仅检查了训练集上的拟合效果，并没有在测试集上进行推理并验证。如果我们尝试去加载新的测试数据集，那么所有的特征处理过程，都需要在测试集上重演一遍。无疑，这同样会引入大量冗余的重复代码。

那么，有没有什么办法，能够避免上述的重复开发，让Spark MLlib框架下的机器学习开发更加高效呢？答案是肯定的，今天这一讲，我们就来说说Spark MLlib Pipeline，看看它如何帮助开发者大幅提升机器学习应用的开发效率。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/58/52/f35f5265.jpg" width="30px"><span>空de</span> 👍（0） 💬（1）<div>Spark 搞时序异常分析，用什么库比较好？</div>2022-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLKk5aS61o1afOibKYKwKKpIiaKCw65oIg8QrnT9G54klTjkZ6JnqzQvaY5tAv2sF7WvicicorlW2S41w/132" width="30px"><span>Geek_fe18e0</span> 👍（1） 💬（0）<div>老师好，以现在的职场环境，如果校招生以大数据开发为目标的话，将来能慢慢历练为大数据全栈吗（包括大数据算法）？似乎现在大数据行业都是以数仓开发为主。</div>2022-07-23</li><br/>
</ul>