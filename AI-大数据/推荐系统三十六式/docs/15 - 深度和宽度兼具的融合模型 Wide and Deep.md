我在前面已经提到过一个事实，就是推荐系统的框架大都是多种召回策略外挂一个融合排序。召回策略的姿势繁多，前面的专栏文章已经涉及了一部分内容。今天我们继续说融合排序。

## 要深还是要宽

融合排序，最常见的就是CTR预估，你一定不要把自己真的只局限在C上，这里说的CTR预估的C，可以是产品中的任何行为，视频是不是会看完，看完后是不是会收藏，是不是会分享到第三方平台，查看的商品是不是会购买等等，都可以看成那个可以被预估发生概率的CTR。

CTR预估的常见做法就是广义线性模型，如 Logistic Regression，然后再采用特征海洋战术，就是把几乎所有的精力都放在搞特征上：挖掘新特征、挖掘特征组合、寻找新的特征离散方法等等。

这种简单模型加特征工程的做法好处多多：

1. 线性模型简单，其训练和预测计算复杂度都相对低；
2. 工程师的精力可以集中在发掘新的有效特征上，俗称特征工程；
3. 工程师们可以并行化工作，各自挖掘特征；
4. 线性模型的可解释性相对非线性模型要好。

特征海洋战术让线性模型表现为一个很宽广（Wide）的模型，可以想象逻辑回归中那个特征向量在特征工程的加持下，越来越宽的样子。

最近十年，是深度学习独步天下的十年，犹如异军突起，一路摧城拔寨，战火自然也烧到了推荐系统领域，用深度神经网络来革“线性模型+特征工程”的命，也再自然不过。

用这种“深模型”升级以前的“宽模型”，尤其是深度学习“端到端”的诱惑，可以让每天沉迷搞特征无法自拔的工程师们主动投怀送抱。

深度学习在推荐领域的应用，其最大好处就是“洞悉本质般的精深”，优秀的泛化性能，可以给推荐很多惊喜。

硬币总有正反面，深度模型的泛化强于线性模型，也会导致推荐有时候看上去像是“找不着北”，就是大家常常自问的那句话：“不知道这是怎么推出来的？”用行话说，就是可解释性不好。

以前全面搞特征时，你叫人家“宽模型”小甜甜，现在新模型换旧模型，“深模型”一出，就叫“宽模型”牛夫人，这样不好，还是要两者合作，才能最大限度地发挥效果。

因此，Google在2016年就发表了他们在Google Play应用商店上实践检验过的CTR预估方法：Wide &amp; Deep模型，让两者一起为用户们服务，这样就取得了良好效果。

下面，我就为你详细介绍一下这个深宽模型。

## Wide &amp; Deep模型

一个典型的推荐系统架构，其实很类似一个搜索引擎，搜索由检索和排序构成。推荐系统也有召回和排序两部构成，不过，推荐系统的检索过程并不一定有显式的检索语句，通常是拿着用户特征和场景特征去检索召回，其中用户特征也就是在前面的专栏中提到的用户画像。

示意图如下.

![](https://static001.geekbang.org/resource/image/7e/e1/7e3c2abe330e98829c01a73b0f7125e1.png?wh=620%2A289)

简单描述一下这个示意图。

首先使用用户特征和上下文场景特征从物品库中召回候选推荐结果，比如得到100个物品，然后用融合模型对这100个物品做最终排序，输出给用户展示。

同时开始记录展示日志和用户行为日志，再把收集到的日志和用户特征、上下文场景特征、物品特征拉平成为模型的训练数据，训练新的模型，再用于后面的推荐，如此周而复始。

今天要说的深宽模型就是专门用于融合排序的，分成两部分来看。一部分是线性模型，一部分是深度非线性模型。整个示意图如下：  
![](https://static001.geekbang.org/resource/image/5c/20/5ca21e4b2511cd4567fb630db5b14520.png?wh=641%2A199)

我来解释一下这个示意图，这个示意图有三部分。最左边是宽模型，中间是深宽模型，最右边是纯的深度模型。

首先，线性模型部分，也就是“宽模型”，形式如下：

![](https://static001.geekbang.org/resource/image/ea/3f/ea301585c357cbfc77aba992048a103f.png?wh=143%2A35)

再次强调一下，这是线性模型的标准形式，逻辑回归只是在这基础上用sigmoid函数变换了一下。

模型中的X是特征，W是权重，b是模型的偏置，也是线性模型的截距。线性模型中常用的特征构造手段就是特征交叉。

例如：“性别=女 and 语言=英语。”就是由两个特征组合交叉而成，只有当“性别=女”取值为1，并且“语言=英语”也取值为1时，这个交叉特征才会取值为1。线性模型的输出这里采用的Logistic Regression。

好，现在把头转到右边，看看深度模型。深度模型其实就是一个前馈神经网络。

深度模型对原始的高维稀疏类别型特征，先进行嵌入学习，转换为稠密、低维的实值型向量，转换后的向量维度通常在10-100这个范围。

这里的嵌入学习，就是先随机初始化嵌入向量，再直接扔到整个前馈网络中，用目标函数来优化学习。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="" width="30px"><span>王王王</span> 👍（1） 💬（1）<div>越来越难了，很多技术概念需要慢慢消化</div>2018-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/7c/39ea8a23.jpg" width="30px"><span>曾阿牛</span> 👍（1） 💬（1）<div>AUC值衡量的是整体排序，但对前N1个物品排越前对用户影响越大，跟AUC值是有一定出入</div>2018-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/d3/1a98a899.jpg" width="30px"><span>江枫</span> 👍（9） 💬（0）<div>老师好，特征embedding也是和模型训练过程一起进行的吗？如果提前做好embedding，比如用word2vec，效果如何？另外，对于新物品，新特征，可能没有embedding结果，怎么处理？谢谢。</div>2018-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/a7/5e66d331.jpg" width="30px"><span>林彦</span> 👍（6） 💬（0）<div>AUC 的不足之处有：(1)反映的是模型的整体性能，看不出在不同点击率区间上的误差情况。有可能线上实际用户点击多的那部分物品误差低，点击少的那部分物品误差高。与线下对所有物品的整体误差评估有差异；(2)只反映了排序能力，沒有提现精确度。比如，训练出的模型的点击率对所有物品同时乘以一个常数，AUC值不会改变，而模型对于点击率的预测值和真实值的差距肯定有变化。我的理解就是新的模型可能对于排名高，排名低，点击率高，点击率低等的某一类物品的点击率提升较大，但对排名本身的顺序影响不大。

不足之处是参考了网上一篇不错的综述文章得到的，非原创。</div>2018-04-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/iatlKgvFoZibEvUUH0RgpB1CWtDLMB2icn8SkG4dJI2O6VgAd5PzwC1FEw4CdPab7v8v8vPWnksBbuJ3P62o7zWjg/132" width="30px"><span>@lala0124</span> 👍（3） 💬（0）<div>老师，您好，这个wide&amp;deep模型我之前有了解过，tensorflow的实现版本也很简洁，我想问一下deep模型中的embedding向量是否只能来自分类特征</div>2018-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（1） 💬（0）<div>我补充下@江枫的问题，老师，有时候embedding的参数需要随着整个模型一起调优，有时候又说要先进行embedding，即embedding的参数不随着整个模型一起调优，什么场景下要一起，什么场景下不一起呢？</div>2019-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qRjoqWIGC6tpmKZBGTxjQKC9cbz9XLhw2nF1c74R4icFOYOdVO4iaeQEQDqEvmbicxn6HEc4SU8kpkwVaO5nABMug/132" width="30px"><span>shangqiu86</span> 👍（0） 💬（0）<div>用过wide&amp;deep模型，效果 并不太理想，是在资讯推荐中，把资讯内容先做了word2vec，再加上一些其他特征，准确率就比随机高一点点，老师，不知道这种还怎么调优</div>2019-04-30</li><br/><li><img src="" width="30px"><span>Dan</span> 👍（0） 💬（0）<div>老師您好，想請教您，在paper表示，深模型的optimizer 用adagrad，寬模型用FTRL。在joint training的階段是使用前面兩個學習完的權重做為initial，使用mini batch 的sgd做joint train嗎？還是說是分開使用不同的optimizer ,只是使用相同的 logistic loss?</div>2018-04-22</li><br/><li><img src="" width="30px"><span>Dan</span> 👍（0） 💬（0）<div>老師您好，請教您，在深模型的embedding 層的dense vector長度通常是如何setting 或者 tuning ？作者設32 - 1200 - 1024 - 512 - 256，有什麼涵意嗎？感謝您</div>2018-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/31/cbef8d5d.jpg" width="30px"><span>半瓶墨水</span> 👍（0） 💬（0）<div>昨天刚搞明白这篇论文，就是TensorFlow的函数名称太复杂了</div>2018-04-13</li><br/><li><img src="" width="30px"><span>会飞的牛</span> 👍（0） 💬（0）<div>刑老师，有什么方法可以快速搭建一个抓取数据的推荐系统吗？</div>2018-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2a/d4/c324a7de.jpg" width="30px"><span>风</span> 👍（0） 💬（0）<div>有没有推荐系统的实例，可以测试</div>2018-04-08</li><br/>
</ul>