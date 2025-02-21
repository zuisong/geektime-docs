你好，我是尹会生。

在涉及运营、市场的工作中，我们经常需要根据产品评论的情感分析，来了解某一产品的口碑。所谓的情感分析，就是指根据用户对产品的评论，分析出用户对产品的喜好程度。

最简单的，我们会**区分产品的评价是正向还是负向**的，然后根据反馈结果改变产品的特性。稍微复杂一点的，我们会**根据情感色彩将产品的评价关键词提取出来，进行统计和分类（用于更深入的分析产品）。**

如果靠人工对产品评价进行辨析，有很大的局限性：一个是不够公平，因为每个人对词语感情色彩的理解并不是完全一致的；另一个是产品评价有很多，而且还会不定期增加，人工分析很难保证及时性。

因此，在进行词语的情感分析时，我通常都会使用Python的jieba库，来自动化实现文本情感分析功能。一般需要经过三个步骤，分别是**分词、优化分词结果和情感分析**。

那我就先带你看看**为什么要进行分词，以及如何进行分词操作。**

# 如何分词？

要想判断一段话表达的情感是正向还是负向，就需要根据这句话中的关键词来得到情感的倾向。例如一段话中出现了“开心”“高兴”“物超所值”等正向的词语，我们就可以认定这条产品的评价是偏正向的。相反，出现“不喜欢”“差”等词语，评价就是偏负向的。

但是，要想从一句话中将这些表达情感的词一个一个找出来，就需要依靠专业的工具把一句话根据语义划分成多个词，再把表达情感的词语提取出来，进行情感分析。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Ge7uhlEVxicQT73YuomDPrVKI8UmhqxKWrhtO5GMNlFjrHWfd3HAjgaSribR4Pzorw8yalYGYqJI4VPvUyPzicSKg/132" width="30px"><span>陈东</span> 👍（2） 💬（2）<div>老师能分享你词性统计的思路吗？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（1） 💬（1）<div>有个问题请教一下老师，我在思考题中用代码统计各种词性的数量，但每次统计的结果都不对，和实际数量相去甚远，不知道是什么原因。</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/27/805786be.jpg" width="30px"><span>笨笨</span> 👍（0） 💬（1）<div>jieba.suggest_freq((&quot;中&quot;, &quot;将&quot;), tune = True)老师这句代码应该放在哪里使用呢？是放在words2=jieba.cut(words1)后使用吗?</div>2023-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-05</li><br/>
</ul>