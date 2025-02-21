你好，我是王喆。

上两节课，我们学习了离线评估的主要方法以及离线评估的主要指标。那这些方法和指标具体是怎么使用的，会遇到哪些问题呢？我们之前实现的深度学习模型的效果怎么样呢？

这节课，我们直接进入实战，在TensorFlow环境下评估一下我们之前实现过的深度学习模型。一方面这能帮助我们进一步加深对离线评估方法和指标的理解，另一方面，也能检验一下我们自己模型的效果。

## 训练集和测试集的生成

离线评估的第一步就是要生成训练集和测试集，在这次的评估实践中，我会选择最常用的Holdout检验的方式来划分训练集和测试集。划分的方法我们已经在[第23讲](https://time.geekbang.org/column/article/317114)里用Spark实现过了，就是调用Spark中的randomSplit函数进行划分，具体的代码你可以参考 FeatureEngForRecModel对象中的splitAndSaveTrainingTestSamples函数。

这里我们按照8:2的比例把全量样本集划分为训练集和测试集，再把它们分别存储在`SparrowRecSys/src/main/resources/webroot/sampledata/trainingSamples.csv`和`SparrowRecSys/src/main/resources/webroot/sampledata/testSamples.csv`路径中。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epWOEWQYu9icQR8iaiayXyeJpzzrZIF6S4NdkrAGYELyrpnh4GxOicjcj6ZG9PnuuYfzEwMMGB0J1z9Tg/132" width="30px"><span>Geek_e642b8</span> 👍（21） 💬（1）<div>第二个问题是FM部分使用两两点积的缘故吗？</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/42/2d91f663.jpg" width="30px"><span>老庄</span> 👍（4） 💬（1）<div>请教老师，这个wide&amp;deep的ROC和PR AUC的数值，如果使用不同的epochs，得到的结果差别很大。

为什么这里没有把train_dataset分为train和validate两部分，也没有配置EarlyStopping，感觉会一直跑。

这样的结果对比，会不会不大对？

</div>2021-03-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIs6dlFP2kRCS2wLkial1ag8R6K133bHNeCZMRmlQMKgVEAuhyGz9eibGzLv8mjTe939YqJpbAxnMV9jxFsXqsd3amanAqVqXyyzX0w6fMibJJicw/132" width="30px"><span>Geek_b6c3b5</span> 👍（0） 💬（0）<div>为什么emp我没有上线默认是emb计算猜你喜欢？ 而neuralCF我上线了还需要手动输出model=neuralCF
</div>2024-03-13</li><br/>
</ul>