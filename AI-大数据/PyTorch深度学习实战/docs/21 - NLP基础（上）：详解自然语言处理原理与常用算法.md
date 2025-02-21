你好，我是方远。

在之前的课程中，我们一同学习了图像分类、图像分割的相关方法，还通过实战项目小试牛刀，学完这部分内容，相信你已经对深度学习图像算法有了一个较为深入的理解。

然而在实际的项目中，除了图像算法，还有一个大的问题类型，就是文字或者说语言相关的算法。这一类让程序理解人类语言表达的算法或处理方法，我们统称为自然语言处理（Natural Language Processing, NLP）。

这节课，我们先来学习自然语言处理的原理和常用算法，通过这一部分的学习，以后你遇到一些常见的NLP问题，很容易就能想出自己的解决办法。不必担心原理、算法的内容太过理论化，我会结合自己的经验从实际应用的角度，为你建立对NLP的整体认知。

## NLP的应用无处不在

NLP研究的领域非常广泛，凡是跟语言学有关的内容都属于NLP的范畴。一般来说，较为多见的语言学的方向包括：词干提取、词形还原、分词、词性标注、命名实体识别、语义消歧、句法分析、指代消解、篇章分析等方面。

看到这里，你可能感觉这些似乎有点太学术、太专业了，涉及语言的结构、构成甚至是性质方面的研究了。没错，这些都是NLP研究在语言学中的应用方面，就会给人一种比较偏研究的感觉。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2c/8d/70/b0047299.jpg" width="30px"><span>Zeurd</span> 👍（5） 💬（2）<div>TF-IDF因为各种问题，比如文章长度问题，长的文章一个词出现的次数肯定比短的来的多，又比如都是经济学的文章，一个出现80次，一个出现100次，不能代表100次的那个比80次的有用25%，存在边际效用递减的问题，所以一般会对文章数量做指数化以及归一化处理，尽可能减小误差</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（3） 💬（1）<div>tf-idf的理论依据及不足
编辑
tf-idf算法是建立在这样一个假设之上的：对区别文档最有意义的词语应该是那些在文档中出现频率高，而在整个文档集合的其他文档中出现频率少的词语，所以如果特征空间坐标系取tf词频作为测度，就可以体现同类文本的特点。另外考虑到单词区别不同类别的能力，tf-idf法认为一个单词出现的文本频数越小，它区别不同类别文本的能力就越大。因此引入了逆文本频度idf的概念，以tf和idf的乘积作为特征空间坐标系的取值测度，并用它完成对权值tf的调整，调整权值的目的在于突出重要单词，抑制次要单词。但是在本质上idf是一种试图抑制雜訊的加权，并且单纯地认为文本頻率小的单词就越重要，文本頻率大的单词就越无用，显然这并不是完全正确的。idf的简单结构并不能有效地反映单词的重要程度和特征词的分布情况，使其无法很好地完成对权值调整的功能，所以tf-idf法的精度并不是很高。

此外，在tf-idf算法中并没有体现出单词的位置信息，对于Web文档而言，权重的计算方法应该体现出HTML的结构特征。特征词在不同的标记符中对文章内容的反映程度不同，其权重的计算方法也应不同。因此应该对于处于网页不同位置的特征词分别赋予不同的系数，然后乘以特征词的词频，以提高文本表示的效果。
-- 维基百科</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/48/3a981e55.jpg" width="30px"><span>林于翔</span> 👍（1） 💬（1）<div>from nltk import word_tokenize
from nltk import TextCollection

sents=[&#39;i like jike&#39;,&#39;i want to eat apple&#39;,&#39;i like lady gaga&#39;]
# 首先进行分词
sents=[word_tokenize(sent) for sent in sents]

# 构建语料库
corpus=TextCollection(sents)

# 计算IDF
idf=corpus.idf(&#39;like&#39;)  
print(idf)#0.4054651081081644
请问这个idf值应该怎么算呢？如果按照公式，文档总数为3, 包含词条‘like’的文档数为2，分母再加上1，那么idf=ln(3&#47;(2+1)=0?? 为什么会跟结果不符合呢？</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（1）<div>方老师，最后一段代码有误，for少了in， input_content 应该是texts。修正后如下

from gensim import corpora, models
import jieba.posseg as jp
import jieba

texts = [line.strip() for line in open(&#39;input.txt&#39;, &#39;r&#39;)]
# 老规矩，先分词
words_list = []
for text in texts:
  words = [w.word for w in jp.cut(text)]
  words_list.append(words)

# 构建文本统计信息, 遍历所有的文本，为每个不重复的单词分配序列id，同时收集该单词出现的次数
dictionary = corpora.Dictionary(words_list)

# 构建语料，将dictionary转化为一个词袋。
# corpus是一个向量的列表，向量的个数就是文档数。你可以输出看一下它内部的结构是怎样的。
corpus = [dictionary.doc2bow(words) for words in words_list]

# 开始训练LDA模型
lda_model = models.ldamodel.LdaModel(corpus=corpus, num_topics=8, id2word=dictionary, passes=10)</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/ed/1176932f.jpg" width="30px"><span>思勇</span> 👍（0） 💬（1）<div>LDA模型示例无法跑通，从网上找了一个，可以跑： https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;134161509</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（1）<div>nltk 计算TF-IDF的时候，如果是无限个文档或是很大量的文档，这改怎么玩类</div>2022-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e3/d7/d7b3505f.jpg" width="30px"><span>官</span> 👍（5） 💬（0）<div>只用TF-IDF的话，在不设置停用词的情况，有很多常见的冠词还有谓语动词出现的次数会非常高，比如 is the ，或者汉语“是”，“我”等。而在研究段落主题或者文章含义的时候，这些词实际含义并不大，所以在使用TF-IDF之前需要对文本进行一些预处理。</div>2021-11-30</li><br/><li><img src="" width="30px"><span>Sam Wang</span> 👍（2） 💬（0）<div>TFIDF缺少了semantic meaning </div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKSVuNarJuDhBSvHY0giaq6yriceEBKiaKuc04wCYWOuso50noqDexaPJJibJN7PHwvcQppnzsDia1icZkw/132" width="30px"><span>Matthew</span> 👍（0） 💬（0）<div>离线下载安装NLTK的nltk_data数据包：
https:&#47;&#47;blog.csdn.net&#47;qq_43140627&#47;article&#47;details&#47;103895811

其中，tokenizers&#47; 下的 punkt.zip 需要解压缩</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（0） 💬（0）<div>翻译: 词频逆文档频率TF-IDF算法介绍及实现 手把手用python从零开始实现
https:&#47;&#47;blog.csdn.net&#47;zgpeace&#47;article&#47;details&#47;126596077</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>nltk需要下载data有点慢</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（0） 💬（0）<div>tf-idf算法是创建在这样一个假设之上的：对区别文档最有意义的词语应该是那些在文档中出现频率高，而在整个文档集合的其他文档中出现频率少的词语，所以如果特征空间坐标系取tf词频作为测度，就可以体现同类文本的特点。另外考虑到单词区别不同类别的能力，tf-idf法认为一个单词出现的文本频数越小，它区别不同类别文本的能力就越大。因此引入了逆文本频度idf的概念，以tf和idf的乘积作为特征空间坐标系的取值测度，并用它完成对权值tf的调整，调整权值的目的在于突出重要单词，抑制次要单词。但是在本质上idf是一种试图抑制噪声的加权，并且单纯地认为文本频率小的单词就越重要，文本频率大的单词就越无用，显然这并不是完全正确的。idf的简单结构并不能有效地反映单词的重要程度和特征词的分布情况，使其无法很好地完成对权值调整的功能，所以tf-idf法的精度并不是很高。

此外，在tf-idf算法中并没有体现出单词的位置信息，对于Web文档而言，权重的计算方法应该体现出HTML的结构特征。特征词在不同的标记符中对文章内容的反映程度不同，其权重的计算方法也应不同。因此应该对于处于网页不同位置的特征词分别赋予不同的系数，然后乘以特征词的词频，以提高文本表示的效果。（By维基百科）</div>2022-05-30</li><br/>
</ul>