你好，我是独行。

前面几节课我们学习了机器学习和NLP的基本理论，相信你对人工智能已经有了初步的认识。这节课我们学习Word2Vec，顾名思义就是**词语 to 向量**。我们上一节课学习的NLP过程，在文本预处理之后，有一个特征提取，其中就涉及到将词语转化成数值形式，以便计算机能够理解，指的就是Word2Vec的过程。

为什么要学习Word2Vec？还是为了理解大模型的原理打基础，我们整个课程的目的之一就是弄懂大语言模型的原理，所以在正式学习Transformer之前，我会为你介绍一些前置知识，除了之前讲解的ML和NLP的基本概念外，还包括Word2Vec以及后面的Seq2Seq等。下面我们开始由浅入深学习下Word2Vec。

## Word2Vec

Word2Vec是一种广泛使用的NLP技术，目的是将词语转换成向量形式，使计算机能够理解。它通过学习大量文本数据，捕捉到词语间的上下文关系，进而生成词的高维表示，即词向量。

Word2Vec有两种主要模型：Skip-Gram和CBOW，Skip-Gram的目标是根据目标词预测其周围的上下文词汇，与之相反，CBOW模型的目标是根据周围的上下文词汇来预测目标词。Word2Vec的优点是能够揭示词与词之间的相似性，比如通过计算向量之间的距离来找到语义上相近的词。Word2Vec的应用非常广泛，包括但不限于情感分析、机器翻译和推荐系统等。尽管非常有用，但是它也有局限性，比如无法处理多义词，因为每个词仅被赋予一个向量，不考虑上下文中的多种含义。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（6） 💬（1）<div>第12讲打卡~
思考题：实现新闻推荐系统，一个简单的思路是，将每个用户的浏览、搜索、评论等历史记录，通过Embedding向量化后，存储在向量数据中；同时将新闻的文本也向量化入库。在做相关推荐时，可以基于向量数据库的索引能力，利用余弦距离等，计算相关度最高的几条新闻，给用户推荐。</div>2024-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/dd/f2/3513c633.jpg" width="30px"><span>张 ·万岁！</span> 👍（0） 💬（1）<div>关于这个xml文件无法正常读取的问题，主要是因为xml默认没有预定义HTML中的 &amp;brvbar; 实体，还有存在某些不能编码的字符串。我的解决方案是直接简单暴力的字符串替换
import os

path1 = &#39;data.xml&#39;
path2 = &#39;data1.xml&#39;
with open(path1, &#39;r&#39;, encoding=&#39;utf-8&#39;,) as f1:
    with open(path2, &#39;a+&#39;, encoding=&#39;utf-8&#39;) as f2:
        line = f1.readline()
        while line:
            # print(line.strip())
            f2.write(line.replace(&#39;&amp;brvbar;&#39;, &#39;¦&#39;).replace(&#39;￿&#39;,&#39;&#39;))
            line = f1.readline() </div>2024-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/d9/9058e13c.jpg" width="30px"><span>黄蓉 Jessie</span> 👍（0） 💬（2）<div>对于&amp;brvbar;无法解析的问题，可以用代码将其替换为｜。然后还会遇到一个报错，xml.etree.ElementTree.ParseError: not well-formed (invalid token): line 411575, column 19。这个是因为xml文件里有特殊字符，找到对应行411575，复制这个字符批量替换掉就可以运行成功。
实测能运行起来的预处理代码如下（替换特殊字符后）
```python
import jieba
import xml.etree.ElementTree as ET
import re

# 预处理步骤
# 读取XML文件并解析
file_path = &#39;data.xml&#39;

# 读取XML文件内容
with open(file_path, &#39;r&#39;, encoding=&#39;utf-8&#39;) as file:
    content = file.read()

# 替换特殊实体，这里将 &amp;brvbar; 替换为相应的符号（¦）
content = content.replace(&#39;&amp;brvbar;&#39;, &#39;¦&#39;)

# 使用ET.fromstring解析字符串，而不是直接解析文件
root = ET.fromstring(content)

# 获取所有&lt;article&gt;标签的内容
texts = [record.find(&#39;article&#39;).text for record in root.findall(&#39;RECORD&#39;)]
print(len(texts))

# 停用词列表，实际应用中需要根据实际情况扩展
stop_words = set([&quot;的&quot;, &quot;了&quot;, &quot;在&quot;, &quot;是&quot;, &quot;我&quot;, &quot;有&quot;, &quot;和&quot;, &quot;就&quot;])

# 分词和去除停用词
processed_texts = []
for text in texts:
    if text is not None:
        words = jieba.cut(text)
        processed_text = [word for word in words if word not in stop_words]
        processed_texts.append(processed_text)

# 打印预处理后的文本
for text in processed_texts:
    print(text)</div>2024-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/19/b3403815.jpg" width="30px"><span>Juha</span> 👍（0） 💬（4）<div>这个xml文件，不知道有没有一样无法正常读取的，如果换了lxml的话，数据会变得很多，结果不准确</div>2024-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师，你好，基于Word2Vec是怎么实现情感分析的呢？是预先定义一些比如负面情绪的词语，计算拿到一组向量。然后输入一个词，计算出向量，跟预先定义好负面情绪的向量计算相似度，判断是否为负面情绪吗？
</div>2024-12-22</li><br/>
</ul>