你好，我是王喆。今天我们聊聊Embedding。

说起Embedding，我想你肯定不会陌生，至少经常听说。事实上，Embedding技术不仅名气大，而且用Embedding方法进行相似物品推荐，几乎成了业界最流行的做法，无论是国外的Facebook、Airbnb，还是在国内的阿里、美团，我们都可以看到Embedding的成功应用。因此，自从深度学习流行起来之后，Embedding就成为了深度学习推荐系统方向最火热的话题之一。

但是Embedding这个词又不是很好理解，你甚至很难给它找出一个准确的中文翻译，如果硬是翻译成“嵌入”“向量映射”，感觉也不知所谓。所以索性我们就还是用Embedding这个叫法吧。

那这项技术到底是什么，为什么它在推荐系统领域这么重要？最经典的Embedding方法Word2vec的原理细节到底啥样？这节课，我们就一起来聊聊这几个问题。

## 什么是Embedding？

简单来说，**Embedding就是用一个数值向量“表示”一个对象（Object）的方法**，我这里说的对象可以是一个词、一个物品，也可以是一部电影等等。但是“表示”这个词是什么意思呢？用一个向量表示一个物品，这句话感觉还是有点让人费解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/22/36/59/010b3e60.jpg" width="30px"><span>神经蛙</span> 👍（60） 💬（1）<div>最近刚好看了看Word2Vec,先列一下看了的资料：
    1.Numpy实现的基础版 Word2vec https:&#47;&#47;github.com&#47;YelZhang&#47;word2vec_numpy&#47;blob&#47;495c2bce99fcdfe281bce0918a6765efd3179b07&#47;wordtovec.py
    2.公式推导 https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;136247620    https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;108987941
    3.Google Word2vec c源码详解  https:&#47;&#47;blog.csdn.net&#47;jeryjeryjery&#47;article&#47;details&#47;80245924    https:&#47;&#47;blog.csdn.net&#47;google19890102&#47;article&#47;details&#47;51887344   https:&#47;&#47;github.com&#47;zhaozhiyong19890102&#47;OpenSourceReading&#47;blob&#47;master&#47;word2vec&#47;word2vec.c

**理解有问题的话，麻烦大家指出来，互相进步~**

说一下看了的理解，Google的源码中Skip-gram,中间词预测周围词是一个循环，每次的优化目标词只有一个周围词中的一个。CBOW是将周围词的向量加和求平均作为上下文词向量，来预测中心词。

为什么会出现层次Softmax和负采样的优化方法？ 
需要先摆一下前向传播和反向传播公式：
-- 略去了下标，以及矩阵乘法的先后。
词表长度V，Embedding长度N
输入：X(shape:(1,V))，输入到隐层矩阵W1(shape: V,N), 隐层到输出矩阵W2(shape: N,V)
前向传播：
H=X * W1    (shape:1,N)
U=H * W2    (shape:1,V)
Y=softmax(U)

这里计算Softmax，参与计算的是V个元素。

反向传播：
Loss= -sum(y * logY)

Loss对W2偏导=(Y-1)*H
Loss对W1偏导=(Y-1)*W2*x    (由于X是one-hot向量,相乘后实际只有一行是非0)

W1更新时只更新一行,W2更新时更新整个矩阵。

原因：
    1.前向传播时计算softmax开销大
    2.反向传播时更新W2矩阵开销大

于是就有了对Sofmax这里的优化。最近主要看了负采样。

负采样：
每次训练时，需要预测的目标词给分成2类。一类是目标词，另一类是非目标词（个数可人工指定）（负采样而来，采样词频高的词，TensorFlow里面是这样，与原论文不同）。此时就是个二分类问题，Loss就变了。变成了Sigmod的形式。这样在前向传播不用计算Softmax，反向传播时将每次更新的向量变成了很少的几个，而不是原始的V。降低开销。

关于W1和W2哪被用来做词向量，一般是W1。
这里我有点疑惑，用层次Softmax或者负采样优化方法会不会对W2的效果产生影响？因为更新时没有用到所有数据，所以用W1作为词向量？</div>2020-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0d/da/8a744899.jpg" width="30px"><span>wolong</span> 👍（28） 💬（9）<div>老师您好，我这边有个问题。假如我们是做商品推荐，假如商品频繁上新，我们的物品库会是一个动态的，Embedding技术如何应对？</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（26） 💬（2）<div>计算向量间相似度的常用方法：https:&#47;&#47;cloud.tencent.com&#47;developer&#47;article&#47;1668762</div>2020-10-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLaoiaerNMy7eoSA5yfibPNhta51jkhPTTL1dD1HGlnjaGnFQ6Uzbbce82Kpnic3g1JlD7rtm41Y83PA/132" width="30px"><span>Geek_3c29c3</span> 👍（12） 💬（1）<div>老师，想问一下，业界利用embedding召回时：
1、是用用户embedding与item embedding的相似性召回还是先计算用户之间的相似性TOPN，然后生成一个user-item矩阵，看看最相似的用户买的多的item得分就更高？；
2、业界用embedding召回如何评价优劣？数据集会划分训练集和验证集吗，来验证购买率，召回率等指标；如果划分，是按照时间划分还是按照用户来划分啊？</div>2020-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b2/cb/9c6c7bf7.jpg" width="30px"><span>张弛 Conor</span> 👍（11） 💬（7）<div>老师，有两个问题想请教一下：
1.为什么深度学习的结构特点不利于稀疏特征向量的处理呢？
2.既然输出向量是Multi-hot，那用softmax这种激活函数是否不太好呢？Softmax有输出相加和为一的限制，对于一对多的任务是不是不太合适呢？</div>2020-10-15</li><br/><li><img src="" width="30px"><span>夜枭</span> 👍（9） 💬（1）<div>王老师，关于item2vec有一些业务上的疑问，比如用户的点击item序列，这个item的候选集大概得是一个什么规模才能够线上推荐使用呢，目前在做的item量级比较大的话利用spark处理时耗时也会时间长，导致召回的文章并不能很快的更新，几乎是天级别的，不知道您做业务时是怎么权衡更新的频率和数据量这样一个关系的</div>2021-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/8a/e8/a7ff6230.jpg" width="30px"><span>阳光明媚</span> 👍（9） 💬（1）<div>常用的相似度度量有余弦距离和欧氏距离，余弦距离可以体现数值的相对差异，欧式距离体现数值的绝对差异；例如，衡量用户点击次数的相似度，欧氏距离更好，衡量用户对各类电影的喜好的相似度，用余弦距离更好。</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/93/06/0cb4257e.jpg" width="30px"><span>Vinny</span> 👍（9） 💬（2）<div>老师你好，想请教您个可能与这张内容关联不太大的问题，我是搞nlp的，但是之前在知乎上面看推荐的 user embedding lookup表问题。
像 user id 可能有很多 上千万个，lookup 表的维度就会特别大，而且一些长尾的id 出现交互的次数过少，可能学不到什么好的embedding。
那么工业界是怎么解决这个问题的呢？
之前在知乎上面看一些笼统的说法，比如用hash 让多个id对应一个embdding之类的（但是没有解释这么做的合理性），想请教一下这方面有没有什么推荐的好论文，想去研究下
谢谢！</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8c/74/2bbd132d.jpg" width="30px"><span>Dikiwi</span> 👍（8） 💬（1）<div>相似性一般用欧式距离，cosine距离; 
线上快速召回一般有用ANN，比如LSH算法进行近似召回。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（7） 💬（2）<div>业界常用 余弦相似度方式，文本相似度TD-IDF方式，
想了解更多：https:&#47;&#47;cloud.tencent.com&#47;developer&#47;article&#47;1668762

对word2vec的学习
Word2Vec是词嵌入模型之一，它是一种浅层的神经网络模型，它有两种网络结构：CBOW和Skip-gram。
CBOW：根据上下文出现的词语预测当前词的生成概率；
Skip-gram：根据当前词预测上下文各个词的概率。
注意：在CBOW中，还需要将各个输入词所计算出的隐含单元求和。
Softmax激活函数
输出层使用Softmax激活函数，可以计算出每个单词的生成概率。具体公式f(x) = e^x &#47; sum( e^x_i )，它运用的是极大似然。
由于Softmax激活函数种存在归一化项的缘故，从公式可以看出，需要对词汇表中的所有单词进行遍历，使得每次迭代过程非常缓慢，时间复杂度为O(V)，由此产生了Hierarchical Softmax（层次Softmax） 和 Negative Sampling（负采样）两种改进方法。
Negative Sampling（负采样）：
每次训练时，需要预测的目标词给分成2类。一类是目标词，另一类是非目标词（个数可人工指定）（负采样而来，采样词频高的词，TensorFlow里面是这样，与原论文不同）。此时就是个二分类问题，Loss就变了。变成了Sigmod的形式。这样在前向传播不用计算Softmax，反向传播时将每次更新的向量变成了很少的几个，而不是原始的V，降低开销。（详细可见评论区）
Hierarchical Softmax（分层Softmax）：
它不需要去遍历所有的节点信息，时间复杂度变为O(log(V))。
基本原理：根据标签（label）和频率建立霍夫曼树；（label出现的频率越高，Huffman树的路径越短）；Huffman树中每一叶子结点代表一个label；
参考：https:&#47;&#47;blog.csdn.net&#47;qq_35290785&#47;article&#47;details&#47;96706599
embedding和PCA的本质区别：
引用老师的留言：我觉得理解非常正确，embedding虽然有降维的目的，但初衷是希望在最终的vector中保存物品相关性的信息，甚至依次进行运算。而PCA就是单纯找出主成分进行降维，二者的设计动机差别是比较大的。</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（7） 💬（3）<div>请问下老师，同样作为降维的手段，embedding和PCA的本质区别，可不可以理解为， embedding可以得到更为稠密的向量，并且降维后的各维度没有主次排序之分， 而PCA降维后的向量稠密度并不会增加， 而是得到主成分的排序。 所以如果为了提高模型计算的聚合的速度，就要选择embedding， 如果想降低模型的复杂度和防止过拟合，应该选择PCA。</div>2020-10-29</li><br/><li><img src="" width="30px"><span>AstrHan</span> 👍（6） 💬（4）<div>物品embedding和用户embedding如何一起训练，让他们在同一个空间里呢，我理解这样才可以进行物品和用户的相似度计算。</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/57/ee02ef41.jpg" width="30px"><span>大龄小学生</span> 👍（6） 💬（3）<div>老师，维度过高为什么不用降维，而用embedding</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/ca/6c4010cc.jpg" width="30px"><span>Jay Kay</span> 👍（5） 💬（1）<div>老师有个问题，item2vec所谓的相似性是拟合的一种隐式的共现么？毕竟感觉通过行为序列得到的embedding没有办法反应语义上的相似性。不知道这样的理解对不对。</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b4/99/79a21147.jpg" width="30px"><span>轩</span> 👍（4） 💬（3）<div>老师您好，昨天的提出的一些问题都得到了您的回复，非常感谢。
关于冷启动物品的embedding，我有一些思路，不知是否可行？可业界中也没看到类似做法？

具体而言，拿冷启动物品的标题描述等文字信息喂进rnn吐出embedding，训练好这个rnn之后，就可以冷启动物品入库之时，通过模型获得embedding了，不依赖于用户行为。
至于论据，搜索等都是基于标签标题描述所做，这些文字信息是人类语言关于物品的编码，转换成embedding编码也是可行的？
训练的话，end2end训练，拿点击序列去预测下一个点击。或是拿有充分历史行为的物品训练，预测cosine similarity，应该都可以train这个rnn吧？

之前我负责的业务场景是新闻视频类信息流推荐，内容都很新，大量的冷启动，这是一直以来的一个想法。
由于种种原因，短时间内我没有实践机会了，可经过一段时间的学习，发现对于冷启动好像业界并没有这样做？或是这个想法有些问题？</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/24/13/8fb0424b.jpg" width="30px"><span>follow-fate</span> 👍（4） 💬（1）<div>老是您好，在对物品序列做embeding的时候，物品序列对应的标签序列是什么呢？word2vec预测的输出,skip-gram是根据中心词预测周边词，那物品序列做embeding时也是预测序列中的某个特征吗？</div>2020-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/plh3lengbMHg0qdGHxX3lJzKaJhh0BAXOqBe1mdmoBVk00NsQfC7HNlhTPRuvlXNDblibcwK3fPZjNicRO73Oibtg/132" width="30px"><span>wanlong</span> 👍（4） 💬（1）<div>老师您好，非常棒的文章，请教一个问题：
如果要往更深部分的学习，除了朝您说的算法细节，还有对应各个环节实现遇到的工程挑战，并设计相对的优化方向，这样算一个靠谱的掌握了吧？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/71/8e/31458837.jpg" width="30px"><span>时不时充充电</span> 👍（3） 💬（1）<div>老师，想问个问题，工程实践中，如何评价一个embedding向量的好坏？有没有统一的方法论指导？</div>2021-03-06</li><br/><li><img src="" width="30px"><span>Geek_1d26c5</span> 👍（3） 💬（1）<div>老师您好，我注意到word2vec模型在生成训练样本的时候跳过了&quot;的&quot;和&quot;了&quot;这样的停用词。请问这样做的原因是因为停用词和附近单词的语义关系不大吗?</div>2021-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/39/99/6ae63d8a.jpg" width="30px"><span>努力思考小白菜</span> 👍（3） 💬（1）<div>老师你好！我想不太明白的地方是word2vec的输入层维度是词汇库的大小V。word2vec里词汇库的大小V是不怎么会变的。但如果是经常会加新物品进来的item2vec V会动态的变大。item2vec要随着V变大不断变动神经网络的结构并重新训练么？</div>2020-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Y5U2ADUvruWhziaB4tSyiaAN7h9OcHMGj6X6nAeqJyJvrqWs8JmyO6yOTBziatAEIG6gHRic0jvT3d0hxNhiaAUVYkw/132" width="30px"><span>傻</span> 👍（3） 💬（5）<div>如果是线上用到的实时特征，重新计算embedding的话，响应时间是否能满足要求呢？</div>2020-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI0LeXiaibibS5ENlib4ibibDUZ1DDPqTojcvlmdhCqdZEiareLw3SJzPcVPN1LPqr13WrZ9REG1tZSEQcIQ/132" width="30px"><span>Soulmate</span> 👍（2） 💬（1）<div>老是您好，基于 word2vec 跑出来物品向量太少，导致召回率低，会是哪些原因造成的，基础的ratings数据在1600W左右。</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/23/d0/b72a900b.jpg" width="30px"><span>At sei ni</span> 👍（2） 💬（1）<div>老师您好，我看了一些论文，有很多论文是通过autoencoder来extract每一个user和item的特征的，这跟您本节将的word2vec等方法有何优劣或者不同？</div>2020-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/0a/c35f9000.jpg" width="30px"><span>WiFeng</span> 👍（2） 💬（3）<div>其实，它就藏在输入层到隐层的权重矩阵 WVxN 中。我想看了下面的图你一下就明白了。

这个愣是没明白。</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fd/83/b432b125.jpg" width="30px"><span>鱼_XueTr</span> 👍（2） 💬（1）<div>1.向量投影，即余弦相似度，2.计算模比较大小，各种距离，比如欧式距离，3.KNN</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e7/b4/79ea288d.jpg" width="30px"><span>Mobs</span> 👍（1） 💬（1）<div>我自己总结了四大相似性计算公式：1. Cosine vector similarity 2.Pearson correlation coefficient ( PCC )
3. Euclidean distance similarity 4.Tanimoto coefficient  (  Jaccard similarity coefficient 雅卡尔指数  ) 
本人倾向于使用cosine公式进行计算</div>2021-04-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ3q0LkadjOv4zicr7xQufgXyh8o1Usno8RZdeBPOqzsoH8DRiaMdYjs0OyEuTknHwHxfQ4AnBHdBCA/132" width="30px"><span>Geek_f676f3</span> 👍（1） 💬（1）<div>向量计算相似度：https:&#47;&#47;www.milvus.io&#47;cn&#47; 工业界实践</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/46/f4/93b1275b.jpg" width="30px"><span>Alan</span> 👍（1） 💬（1）<div>课后思考：
1、其实很多，大家也都知道！业界常用计算Cosine Similarity余弦相似度方式，文本相似度TD-IDF方式</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e1/f4/456752ac.jpg" width="30px"><span>DUO2.0</span> 👍（1） 💬（1）<div>在你觉得skip gram的中文例子里面，怎么知道“深度学习”是一个词，而不是四个词呢？在英文下 deep learning因为有空格作为自然的separator，我们一般是把deep 跟learning分开处理的。</div>2021-02-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK8hCUT5psspwxiaAiarTRZ4icOg4KpzFnw68ib2VqN6F5sra4GnBiaT3aSptvVKQe9sFNhzjCQG1ib1tPQ/132" width="30px"><span>wangyunyy</span> 👍（1） 💬（6）<div>老师你好，您在Netflix的电影推荐中提到 ： “具体来说就是，我们直接找出某个用户向量周围的电影向量，然后把这些电影推荐给这个用户就可以了”
按照这个说法应该是通过用户向量和电影向量的相似度来推荐，但是矩阵分解中最后的推荐排序是通过用户向量和电影向量的内积，这两种方式应该是不一样的，而且用户向量和电影向量应该是没有可比性的，不知道我理解是否正确？谢谢</div>2021-02-23</li><br/>
</ul>