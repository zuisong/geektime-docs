时间是一个客观存在的物理属性，很多数据都有时间属性，只不过大多时候都把它忽略掉了。前面讲到的绝大多数推荐算法，也都没有考虑“用户在产品上作出任何行为”都是有时间先后的。

正是认识到这一点，有一些矩阵分解算法考虑了时间属性，比如Time-SVD；但是，这种做法只是把时间作为一个独立特征加入到模型中，仍然没有给时间一个正确的名分。

## 时间的重要性

时间属性反应在序列的先后上，比如用户在视频网站上观看电视剧会先看第一集再看第二集，股市数据先有昨天的再有今天的，说“我订阅了《推荐系统36式》专栏”这句话时，词语也有先后，这种先后的关系就是时间序列。

具体到推荐系统领域，时间序列就是用户操作行为的先后。绝大数推荐算法都忽略操作的先后顺序，为什么要采取这样简化的做法呢？因为一方面的确也能取得不错的效果，另一方面是深度学习和推荐系统还迟迟没有相见。

在深度学习大火之后，对时间序列建模被提上议事日程，业界有很多尝试，今天以Spotify的音乐推荐为例，介绍循环神经网络在推荐系统中的应用。

## 循环神经网络

循环神经网络，也常被简称为RNN，是一种特殊的神经网络。再回顾一下神经网络的结构，示意图如下：

![](https://static001.geekbang.org/resource/image/61/c6/61177f813f5f493966f8f9beaa395dc6.png?wh=1064%2A826)

普通神经网络有三个部分，输入层x，隐藏层h，输出层o，深度神经网络的区别就是隐藏层数量有很多，具体多少算深，这个可没有定论，有几层的，也有上百层的。

把输入层和隐藏层之间的关系表示成公式后就是：

$$h = F(Wx) $$

就是输入层x经过连接参数线性加权后，再有激活函数F变换成非线性输出给输出层。

在输出层就是：

$$O = \\phi(Vh) $$

隐藏层输出经过输出层的网络连接参数线性加权后，再由输出函数变换成最终输出，比如分类任务就是Softmax函数。

那循环神经网络和普通神经网络的区别在哪？

区别就在于：普通神经网络的隐藏层参数只有输入x决定，因为当神经网络在面对一条样本时，这条样本是孤立的，不考虑前一个样本是什么，循环神经网络的隐藏层不只是受输入x影响，还受上一个时刻的隐藏层参数影响。

我们把这个表示成示意图如下：  
![](https://static001.geekbang.org/resource/image/28/71/285fdbb62e517ddb2099d3b6c87f8371.png?wh=1920%2A886)

解释一下这个示意图。在时刻t，输入是xt，而隐藏层的输出不再是只有输入层xt，还有时刻t-1的隐藏层输出h(t-1)，表示成公式就是：

$$h\_{t} = F(Wx\_{t} + Uh\_{t-1})$$

对比这个公式和前面普通神经网络的隐藏层输出，就是在激活函数的输入处多了一个 $Uh\_{t-1}$ 。别小看多这一个小东西，它背后的意义非凡。

我一直在传递一个观点，隐藏层的东西，包括矩阵分解和各种Embedding得到的隐因子，是对很多表面纷繁复杂的现象所做的信息抽取和信息压缩。

那么上一个时刻得到的隐藏层，就是对时间序列上一个时刻的信息压缩，让它参与到这一个时刻的隐藏层建设上来，物理意义就是认为现在这个时刻的信息不只和现在的输入有关，还和上一个时刻的状态有关。这是时间序列本来的意义，也就是循环神经网络的意义。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/67/31/0fbadaff.jpg" width="30px"><span>哎哎哎</span> 👍（10） 💬（0）<div>请问一下，能分享一下rnn在业界的应用效果吗？Spotify真的用rnn了吗？相比较线上效果如何呢？如何部署上线呢？老师，希望多来一些业界应用和经验分享啊</div>2018-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/74/56/b26b9772.jpg" width="30px"><span>Jun60</span> 👍（5） 💬（0）<div>感觉这部分说的有点虚，对于的RNN实际应用没有具体的讲解，过于概括</div>2019-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibXzoEYHwV5Sc79EL58ZeBn8yZIkdVBGniabydtfhFqe76IDNQ95miaiawEm79HlE6icTA/132" width="30px"><span>寒玉阳</span> 👍（4） 💬（0）<div>哎，我不知道这个东西老师在实际中有无落地，但你说的这些东西很虚，基本就是些rnn的原理和链式求导仅此而已，这课从我这不会在传到其他人手里了
</div>2021-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/MdKiauCwb4CJMa3sbQyrjSKceWicHSf81Typ7Hia6ZrArtCQtd3Ezetu8TJnHmianJV2Aq9Lic7YNSdEq2R2F3EH7WQ/132" width="30px"><span>异尘</span> 👍（4） 💬（0）<div>有个问题请教下老师，我的理解，这个RNN模型考虑了用户的历史播放行为来做预测，应该是针对某个特定用户的，如果我们需要给每个用户做个性化推荐，岂不是需要训练非常多的RNN模型？（每个用户一个）</div>2018-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI643alLPLydkjGwXqsnVxppsRpYu2HrtegQfcicSqGJf2ZEkD79LShZoUyCWAhHyiavtA91yzMcTsA/132" width="30px"><span>Geek_nmrdkh</span> 👍（2） 💬（0）<div>我感觉这个很难工程化落地，效果应该也一般吧</div>2020-04-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（1） 💬（0）<div>这里是否跟上一张youTube存在一样的问题，分类的类别可能上亿，效率如何？是否可以把歌曲进行分类，把输入歌单也映射成类别，用类别序列预测类别，不过往往用户听歌喜欢听一某个特定类别的序列。
老师，训练样本选取以及处理的时候是不是先对每个歌曲进行embedding，然后将用户形成的歌曲列表中每首歌的embedding向量相加，或者取平均，然后塞入模型中？RNN是否换成lstm或者GRU来试下，效果如何？有单独介绍这个实践的文章吗？</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2a/d4/c324a7de.jpg" width="30px"><span>风</span> 👍（1） 💬（0）<div>有实际例子？</div>2018-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/9e/dc53669e.jpg" width="30px"><span>zc</span> 👍（1） 💬（0）<div>就是输入层 x 经过连接参数线性加权后，再有激活函数 F 变换成非线性输出给输出层。

看公式，是不是应该 输出给隐藏层？
</div>2018-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/e0/9a79ddac.jpg" width="30px"><span>🐱您的好友William🐱</span> 👍（0） 💬（0）<div>这个只是最简单的版本吧，只考虑每个歌单的顺序，并没有结合不同用户的feature之类的。assumption是大家听了这个歌之后都听了下一个歌，那么你一定喜欢下一个歌。现实有点差距啊。 </div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（0） 💬（0）<div>有些好奇对于无标注或少标注的时间序列数据有没有什么RNN的无监督深度学习变体可以处理，而且有开源或成熟的工具可以落地。我之前遇到过一个被叫作Nonlinear Autoregressive Network(NAN)的算法用来处理时间序列数据，没搜索到这种名字的算法的在时间序列数据上的计算应用细节。</div>2018-04-19</li><br/>
</ul>