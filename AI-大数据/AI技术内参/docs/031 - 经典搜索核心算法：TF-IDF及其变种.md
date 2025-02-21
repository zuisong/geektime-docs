从本周开始我们进入人工智能核心技术模块，本周我会集中讲解经典的搜索核心算法，今天先来介绍TF-IDF算法。

在信息检索（Information Retrieval）、文本挖掘（Text Mining）以及自然语言处理（Natural Language Processing）领域，TF-IDF算法都可以说是鼎鼎有名。虽然在这些领域中，目前也出现了不少以深度学习为基础的新的文本表达和算分（Weighting）方法，但是TF-IDF作为一个最基础的方法，依然在很多应用中发挥着不可替代的作用。

了解和掌握TF-IDF算法对初学者大有裨益，能够帮助初学者更快地理解其它更加深入、复杂的文本挖掘算法和模型。今天我就来谈谈TF-IDF的历史、算法本身的细节以及基于TF-IDF的几个变种算法。

## TF-IDF的历史

把查询关键字（Query）和文档（Document）都转换成“向量”，并且尝试用线性代数等数学工具来解决信息检索问题，这样的努力至少可以追溯到20世纪70年代。

1971年，美国康奈尔大学教授杰拉德·索尔顿（Gerard Salton）发表了《SMART检索系统：自动文档处理实验》（The SMART Retrieval System—Experiments in Automatic Document Processing）一文，文中首次提到了把查询关键字和文档都转换成“向量”，并且给这些向量中的元素赋予不同的值。这篇论文中描述的SMART检索系统，特别是其中对TF-IDF及其变种的描述成了后续很多工业级系统的重要参考。

1972年，英国的计算机科学家卡伦·琼斯（Karen Spärck Jones）在《从统计的观点看词的特殊性及其在文档检索中的应用》（A Statistical Interpretation of Term Specificity and Its Application in Retrieval） 一文中第一次详细地阐述了IDF的应用。其后卡伦又在《检索目录中的词赋值权重》（Index Term Weighting）一文中对TF和IDF的结合进行了论述。可以说，卡伦是第一位从理论上对TF-IDF进行完整论证的计算机科学家，因此后世也有很多人把TF-IDF的发明归结于卡伦。

杰拉德本人被认为是“信息检索之父”。他1927年出生于德国的纽伦堡，并与1950年和1952年先后从纽约的布鲁克林学院获得数学学士和硕士学位，1958年从哈佛大学获得应用数学博士学位，之后来到康奈尔大学参与组建计算机系。为了致敬杰拉德本人对现代信息检索技术的卓越贡献，现在，美国计算机协会ACM（Association of Computing Machinery）每三年颁发一次“杰拉德·索尔顿奖”（Gerard Salton Award），用于表彰对信息检索技术有突出贡献的研究人员。卡伦·琼斯在1988年获得了第二届“杰拉德·索尔顿奖”的殊荣。

## TF-IDF算法详解

要理解TF-IDF算法，第一个步骤是理解TF-IDF的应用背景。TF-IDF来源于一个最经典、也是最古老的信息检索模型，即“**向量空间模型**”（Vector Space Model）。

简单来说，**向量空间模型就是希望把查询关键字和文档都表达成向量，然后利用向量之间的运算来进一步表达向量间的关系**。比如，一个比较常用的运算就是计算查询关键字所对应的向量和文档所对应的向量之间的“**相关度**”。

因为有了向量的表达，相关度往往可以用向量在某种意义上的“**相似度**”来进行近似，比如**余弦相似性**（Cosine Similarity）或者是**点积**（Dot Product）。这样，相关度就可以用一个值来进行表达。不管是余弦相似度还是点积都能够从线性代数或者几何的角度来解释计算的合理性。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/62/b874af21.jpg" width="30px"><span>颛顼</span> 👍（22） 💬（1）<div>中文首先要分词，分词后要解决多词一义，以及一词多义问题，这两个问题通过简单的tf-idf方法不能很好的解决，于是就有了后来的词嵌入方法，用向量来表征一个词</div>2017-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/17/1cce757b.jpg" width="30px"><span>张岩kris</span> 👍（1） 💬（1）<div>文档到词向量的转换，语言先进行中文分词吧，不同分词算法，可能对最终的结果产生一定影响</div>2017-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6f/53/2e05d320.jpg" width="30px"><span>东辉  (●---●)</span> 👍（1） 💬（1）<div>是否需要先分词</div>2017-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/b4/abb7bfe3.jpg" width="30px"><span>霸气芝士草莓</span> 👍（18） 💬（0）<div>能不能加上一些公式，用公式和文字结合来表达，感觉更清晰直观</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/b4/abb7bfe3.jpg" width="30px"><span>lyhbit</span> 👍（5） 💬（0）<div>讲TF-IDF的四种变种、如果加一些图片或者例子会更好理解些</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cb/07/e34220d6.jpg" width="30px"><span>李沛欣</span> 👍（4） 💬（0）<div>TF词频：某一单词出现在某文档的次数
IDF逆文档频率：多个文档都出现同一单词的概率之倒数

二者向量化的乘积，能够反映出某词对整个文章的重要性。

采用余弦相似度等算法，能反映出多篇文章文章的相似性。

个人以为，这大概也是论文查重的原理</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/80/6ff7ea5f.jpg" width="30px"><span>guoguo 👻</span> 👍（2） 💬（0）<div>第一个变种那里是ln(tf)吧，log(tf)算的话值明显不对</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/52/1c/e902de0f.jpg" width="30px"><span>追逐繁星的孩纸~</span> 👍（1） 💬（0）<div>思考题，如果要把 TF-IDF 应用到中文环境中，是否需要一些预处理的步骤？
答：要的。TF表示单词频率，对中文来说，首先就需要分句，分词，分词涉及的东西就多了，准确的分词需要涉及上下文理解，歧义词、多义词、词语搭配等处理。此外，为了统一处理，可能还会涉及简繁转换。暂时只能想到这些。</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/3f/eabd0cb1.jpg" width="30px"><span>Yang</span> 👍（0） 💬（0）<div>分词，有时候为了提高模型的效果，可能既要分词，也要分字。</div>2019-09-09</li><br/><li><img src="" width="30px"><span>庄小P</span> 👍（0） 💬（0）<div>学习了，了解这些算法是怎么改进的，才会有自己改进的空间</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/1d/9cc0e453.jpg" width="30px"><span>willow990</span> 👍（0） 💬（0）<div>你好，下面这句话我理解我点问题，能否再具体解释下，谢谢
“还有一个重要的 TF-IDF 变种，则是对查询关键字向量，以及文档向量进行标准化，使得这些向量能够不受向量里有效元素多少的影响，也就是不同的文档可能有不同的长度”</div>2018-02-17</li><br/>
</ul>