你好，我是方远。

在第22节课我们一起学习了不少文本处理方面的理论，其实文本分类在机器学习领域的应用也非常广泛。

比如说你现在是一个NLP研发工程师，老板啪地一下甩给你一大堆新闻文本数据，它们可能来源于不同的领域，比如体育、政治、经济、社会等类型。这时我们就需要对文本分类处理，方便用户快速查询自己感兴趣的内容，甚至按用户的需要定向推荐某类内容。

这样的需求就非常适合用PyTorch + BERT处理。为什么会选择BERT呢？因为BERT是比较典型的深度学习NLP算法模型，也是业界使用最广泛的模型之一。接下来，我们就一起来搭建这个文本分类模型，相信我，它的效果表现非常强悍。

## 问题背景与分析

正式动手之前，我们不妨回顾一下历史。文本分类问题有很多经典解决办法。

开始时就是最简单粗暴的关键词统计方法。之后又有了基于贝叶斯概率的分类方法，通过某些条件发生的概率推断某个类别的概率大小，并作为最终分类的决策依据。尽管这个思想很简单，但是意义重大，时至今日，贝叶斯方法仍旧是非常多应用场景下的好选择。

之后还有支持向量机（SVM），很长一段时间，其变体和应用都在NLP算法应用的问题场景下占据统治地位。

随着计算设备性能的提升、新的算法理论的产生等进步，一大批的诸如随机森林、LDA主题模型、神经网络等方法纷纷涌现，可谓百家争鸣。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j24oyxHcpB5AMR9pMO6fITqnOFVOncnk2T1vdu1rYLfq1cN6Sj7xVrBVbCvHXUad2MpfyBcE4neBguxmjIxyiaQ/132" width="30px"><span>vcjmhg</span> 👍（3） 💬（1）<div>1.截断法
截断法是非常常用办法，大致分为三种，head截断，tail截断，head+tail 截断。
head截断即从文本开头直到限制的字数。
tail截断是从结尾开始往前截断。
head+tail 截断，开头和结尾各保留一部分，比例参数是一个可以调节超参数。
缺点:处理方法较为暴力，不是太长的文本
2.Pooling法，缺点性能较差
3.压缩法，提取文本中有限segment，但压缩效果可能会很有限。</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/7e/3afb669f.jpg" width="30px"><span>Qwen</span> 👍（2） 💬（1）<div>才入行新人，文章读了好几遍，还有很多问题点不能理解。
希望大佬能否考虑整理一份完整的训练代码，在参照您的文档去理解，应该能帮助到很多像我这样的新人。</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/8a/0b/ac84669e.jpg" width="30px"><span>(●—●)</span> 👍（1） 💬（3）<div>请问怎么转换模型？</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/b5/12c67a82.jpg" width="30px"><span>xiaolan</span> 👍（1） 💬（1）<div>请问bert模型的用处是不是跟word2vec一样？</div>2022-01-24</li><br/><li><img src="" width="30px"><span>Geek_1e9742</span> 👍（0） 💬（1）<div>你文章里的多语言bert模型的链接已经失效不能使用了</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>预训练模型地址失效了：
https:&#47;&#47;github.com&#47;google-research&#47;bert&#47;blob&#47;master&#47;multilingual.md</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>上一节提到的pipelines能否解决长文本的办法</div>2022-06-02</li><br/><li><img src="" width="30px"><span>Geek_709f77</span> 👍（0） 💬（1）<div>“转换完模型之后，你会发现你的本地多了三个文件”这个转换完成模型是怎么做的？另外，老师给的链接有的打开后跟文章中内容不一样，代码下载也不对，能不能把所有代码放在一个地方，让我们下载运行？</div>2022-04-15</li><br/><li><img src="" width="30px"><span>向坤</span> 👍（0） 💬（1）<div>请问有完整的训练代码链接吗</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（1） 💬（0）<div>我觉得这篇的主角是huggingface</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/51/72/16b13cd4.jpg" width="30px"><span>Beyond myself</span> 👍（0） 💬（1）<div>convert_BERT_original_tf2_checkpoint_to_PyTorch.py 和 modeling_BERT.py两个文件不存在了，全局搜索BERTForSequenceClassification也没有找不到。</div>2023-08-27</li><br/>
</ul>