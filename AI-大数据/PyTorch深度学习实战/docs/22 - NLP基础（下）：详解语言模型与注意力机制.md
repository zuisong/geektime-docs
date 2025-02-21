你好，我是方远。

在上节课中，我们一同了解了NLP任务中的几个经典问题，这些方法各有千秋，但是我们也发现，有的方法并不能很好地将文本中单词、词组的顺序关系或者语义关系记录下来，也就是说，不能很好地量化表示，也不能对语言内容不同部分的重要程度加以区分。

那么，有没有一种方法，可以把语言变成一种数学计算过程，比如采用概率、向量等方式对语言的生成和分析加以表示呢？答案当然是肯定的，这就是这节课我们要讲到的语言模型。

那如何区分语言不同部分的重要程度呢？我会从深度学习中最火热的注意力机制这一角度为你讲解。

## 语言模型

语言模型是根据语言客观事实而进行的语言抽象数学建模，是一种对应关系。很多NLP任务中，都涉及到一个问题：对于一个确定的概念或者表达，判断哪种表示结果是最有可能的。

我们结合两个例子体会一下。

先看第一个例子，翻译文字是：今天天气很好。可能的结果是： res1 = Today is a fine day. res2 = Today is a good day.那么我们最后要的结果就是看概率P(res1)和P(res2)哪个更大。

再比如说，问答系统提问：我什么时候才能成为亿万富翁。可能的结果有：ans1 = 白日做梦去吧。ans2 = 红烧肉得加点冰糖。那么，最后返回的答案就要选择最贴近问题内容本身的结果，这里就是前一个答案。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="" width="30px"><span>赵心睿</span> 👍（3） 💬（1）<div>方老师讲得很好，对小白来说浅显易懂，希望看到您更多课程。</div>2022-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（1） 💬（1）<div>方老师，&quot;我爱极客&quot;的注意力机制的例子，顺着你的思路，如何分析出这几个词的权重是多少呢？</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（0） 💬（1）<div>之前看这篇文章的时候，是字都认识，但是连起来就是不懂。前两天学习了transformers，再看这篇文章，终于能够看懂一点了。文章里提供的案例特别的形象！</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/a7/ba/66b4aebe.jpg" width="30px"><span>南风北巷</span> 👍（0） 💬（2）<div>老师您好，我复现过transformer，但是有一点不明白，Q矩阵当中的一个向量要与K矩阵相乘，进而得到一个向量，那么得到的这个向量它的意义是什么呢？简单来说我想问，词向量点积的意义是什么呢？谢谢老师。</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/e4/7bbec200.jpg" width="30px"><span>董义</span> 👍（0） 💬（1）<div>老师好,我对文中提到的注意力机制可以区分一句话中的重点部分和非重点部分很感兴趣,那么这种机制有哪些现实的成熟应用呢?想深入了解的话可以从哪里入手?</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/52/cb97162e.jpg" width="30px"><span>Sarai李</span> 👍（0） 💬（1）<div>LM从统计模型过渡到神经网络，终于在这里明白了
</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/54/d5e7d56c.jpg" width="30px"><span>Kinvo</span> 👍（2） 💬（0）<div>这篇文章，每个字都是认识的</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/02/2a/90e38b94.jpg" width="30px"><span>John(易筋)</span> 👍（2） 💬（0）<div>翻译: 详细图解Transformer多头自注意力机制 Attention Is All You Need
https:&#47;&#47;blog.csdn.net&#47;zgpeace&#47;article&#47;details&#47;126635650</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/cd/b7/6efa2c68.jpg" width="30px"><span>李雄</span> 👍（1） 💬（0）<div>真得很精炼</div>2021-12-31</li><br/><li><img src="" width="30px"><span>Geek_a26208</span> 👍（1） 💬（0）<div>太长的话，会引入大量的计算量吧，太短的话好像学习的内容就比较少了</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-11</li><br/>
</ul>