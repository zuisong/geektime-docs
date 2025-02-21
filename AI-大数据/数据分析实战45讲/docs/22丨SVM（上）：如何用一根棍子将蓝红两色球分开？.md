今天我来带你进行SVM的学习，SVM的英文叫Support Vector Machine，中文名为支持向量机。它是常见的一种分类方法，在机器学习中，SVM是有监督的学习模型。

什么是有监督的学习模型呢？它指的是我们需要事先对数据打上分类标签，这样机器就知道这个数据属于哪个分类。同样无监督学习，就是数据没有被打上分类标签，这可能是因为我们不具备先验的知识，或者打标签的成本很高。所以我们需要机器代我们部分完成这个工作，比如将数据进行聚类，方便后续人工对每个类进行分析。SVM作为有监督的学习模型，通常可以帮我们模式识别、分类以及回归分析。

听起来，是不是很高大上。我先带你做个小练习。

练习1：桌子上我放了红色和蓝色两种球，请你用一根棍子将这两种颜色的球分开。

![](https://static001.geekbang.org/resource/image/21/88/210bc20b5963d474d425ad1ca9ac6888.jpg?wh=1726%2A1063)  
你可以很快想到解决方案，在红色和蓝色球之间画条直线就好了，如下图所示：

![](https://static001.geekbang.org/resource/image/ec/bb/ec657a6d274b5afb4d8169df9c248abb.jpg?wh=1846%2A1389)  
练习2：这次难度升级，桌子上依然放着红色、蓝色两种球，但是它们的摆放不规律，如下图所示。如何用一根棍子把这两种颜色分开呢？

![](https://static001.geekbang.org/resource/image/b4/a3/b4b9793cdec47d0ea1528ff1922973a3.jpg?wh=1790%2A1085)  
你可能想了想，认为一根棍子是分不开的。除非把棍子弯曲，像下面这样：

![](https://static001.geekbang.org/resource/image/14/eb/144d72013a808e955e78718f6df3d2eb.jpg?wh=1710%2A1050)  
所以这里直线变成了曲线。如果在同一个平面上来看，红蓝两种颜色的球是很难分开的。那么有没有一种方式，可以让它们自然地分开呢？
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2DyBmGYZYz2rgfdR3OMAletl16fZ9VZ9znkaJQSDny4bpcKLsmKMEUdbP4hDBm1f8jIOAfS1NZoYeYGMfgH7WQ/132" width="30px"><span>captain</span> 👍（60） 💬（1）<div>老师好，最近几期的算法课内容量比较大，麻烦推荐一些相关的理论或案例的书籍，谢谢</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（45） 💬（1）<div>有监督学习，就是告诉他这个是红的那个是蓝的。你给我分出红蓝
无监督，自己学会认识红色和蓝色，然后再分类

硬间接，就是完美数据下的完美情况，分出完美类
软间隔，就是中间总有杂质，情况总是复杂，分类总是有一点错误
核函数，高纬度打低纬度，</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cb/07/e34220d6.jpg" width="30px"><span>李沛欣</span> 👍（18） 💬（3）<div>核函数，是一种格局更高的分类模式。通过它我们可以把原本混沌的一堆数据映射到高维，从上帝视角来对这些数据进行线性分类。

来，扔个二向箔🤣</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/1e/0d5f8336.jpg" width="30px"><span>fancy</span> 👍（10） 💬（1）<div>1. 有监督学习and无监督学习
有监督学习，即在已有类别标签的情况下，将样本数据进行分类。
无监督学习，即在无类别标签的情况下，样本数据根据一定的方法进行分类，即聚类，分类好的类别需要进一步分析后，从而得知每个类别的特点。
2. 硬间隔、软间隔、核函数
使用SVM算法，是基于数据是线性分布的情况，这时使用硬间隔的方法分类数据即可。但实际情况下，大部分数据都不属于线性分布，即通过软间隔、核函数处理后，使得数据可以利用SVM算法进行分类。软间隔是通过允许数据有误差，不是绝对的线性分布；核函数是通过将非线性分布的数据映射为线性分布的数据。</div>2019-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/73JN7HxoDAxjPmSWlaGydX6Cpico0aWNIP6mHYibB5BsYcLRt3f7Lm3ZgvtLYWTnBKm9D8bicZI7Q02UTicTiaXycLA/132" width="30px"><span>霸蛮人</span> 👍（6） 💬（2）<div>核函数，是使用变换思维，当数据从一个角度无法进行分类，就变换一个角度来分。就比如，两个人的声音混在一起，要区分开来的话，从时域的角度去看，互相叠加，根本就无法区分，但通过傅里叶变换到频域之后，通过频率的不同就能轻松地区分开来了。在这里，傅里叶变换就相当于核函数的作用。面对不同的数据常见，需要使用不同的变换角度，也就是不同的核函数。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（5） 💬（1）<div>硬间隔，我认为就像线性回归一样，一条直线粗暴的画出边界，然后回答YES OR NO。
软间隔，我认为类似逻辑回归，会绕一下弯子，最后给出的答案是一个概率。
以上两种方式都是处理线性可分的数据，但碰到线性完全分布开的非线性数据的时候，就需要用到核函数，核函数主要是通过把低维的数据映射到高纬，产生一个落差，并给出一个超平面来划分。

不知道我理解的对不对，希望老师回答YES OR NO</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/89/a01375a1.jpg" width="30px"><span>林</span> 👍（3） 💬（1）<div>老师好，这一块的数学原理讲的有点少了吧，能不能讲讲拉格朗日对偶和kkt</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/26/53/60fe31fb.jpg" width="30px"><span>深白浅黑</span> 👍（3） 💬（1）<div>核心在于数据是否线性可分，以及容错能力强弱。
硬间隔和软间隔都是处理线性可分的情况，区别在于容错能力。
核函数用于处理线性不可分情况，将现有数据进行升维，达到线性可分，再进行类别划分处理。</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/52/c6/8eb48963.jpg" width="30px"><span>一纸书</span> 👍（2） 💬（1）<div>那句&quot;灵机一动,猛拍一下桌子&quot;真的是神来一笔,哈哈哈哈哈哈
</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（2） 💬（1）<div>告诉机器，给它一些数据，这部分数据一些是数据集合A，一部分是属于集合B，然后让机器去把数据往集合A和集合B里去划分，这是有监督学习；同样的数据给机器，只是告诉它去做划分和归类，这是无监督学习，类似于孩子的放养。   
硬间隔：表示得到的分类间隔即超平面 能完美的划分数据，不存在划分错误的情况，即零误差
软间隔：表示得到的分类间隔，没有达到完美的程度，对数据划分存在一定的误差
核函数：在数据分布无法用线性函数来表示的时候，需要对数据进行划分的标准变成来非线性的，这个时候就需要用到一种函数名叫核函数，核函数要做的工作是将原来的映射关系在更高维度的空间重新映射，使得新的映射关系变得线性可分。</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/27/74e152d3.jpg" width="30px"><span>滨滨</span> 👍（2） 💬（1）<div>有监督学习和无监督学习的根本区别，就是训练数据中是否有标签。监督学习的数据既有特征又有标签，而非监督学习的数据中只有特征而没有标签。
监督学习是通过训练让机器自己找到特征和标签之间的联系，在以后面对只有特征而没有标签的数据时可以自己判别出标签。
非监督学习由于训练数据中只有特征没有标签，所以就需要自己对数据进行聚类分析，然后就可以通过聚类的方式从数据中提取一个特殊的结构。
2、硬间隔、软间隔和核函数
硬间隔指的就是完全分类准确，不能存在分类错误的情况。软间隔，就是允许一定量的样本分类错误。
线性不可分的情况下，可以使用核函数将样本从原始空间映射到一个更高维的特质空间中，使得样本在新的空间中线性可分。</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/05/4bad0c7c.jpg" width="30px"><span>Geek_hve78z</span> 👍（2） 💬（1）<div>1、有监督学习和无监督学习的理解
有监督学习和无监督学习的根本区别，就是训练数据中是否有标签。监督学习的数据既有特征又有标签，而非监督学习的数据中只有特征而没有标签。
监督学习是通过训练让机器自己找到特征和标签之间的联系，在以后面对只有特征而没有标签的数据时可以自己判别出标签。
非监督学习由于训练数据中只有特征没有标签，所以就需要自己对数据进行聚类分析，然后就可以通过聚类的方式从数据中提取一个特殊的结构。
2、硬间隔、软间隔和核函数
硬间隔指的就是完全分类准确，不能存在分类错误的情况。软间隔，就是允许一定量的样本分类错误。
它可以将样本从原始空间映射到一个更高维的特质空间中，使得样本在新的空间中线性可分。</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/17/01/1c5309a3.jpg" width="30px"><span>McKee Chen</span> 👍（1） 💬（1）<div>1.有监督的学习模型和无监督的学习模型
  有监督的学习模型：事先对数据打上分类标签，机器知道数据的分类
  无监督的学习模型：没有对数据打上分类标签，机器不知道数据的分类

2.硬间隔、软间隔、核函数
  硬间隔：对数据进行分类，不存在分类错误的情况
  软间隔：允许存在一定数据分类错误的情况
  核函数：对于非线性数据，通过核函数让原始的样本空间投射到一个高位的空间，使数据变得线性可分</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/da/df/4ea7b148.jpg" width="30px"><span>Prometheus</span> 👍（0） 💬（1）<div>有监督学习和无监督学习的根本区别，由这个知识点，我想起了统计学基础中，K聚类与判别聚类的知识点。不知道是否想歪了？求教老师，与各位同学。谢谢。</div>2020-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJGXItsGm9EEgVzURZ5iae2T0SLyic5LPzuhsjgu9nvbgne7qIINWkNd1LIVuav1GschBVGj1guLCYg/132" width="30px"><span>Daniel的爹</span> 👍（1） 💬（0）<div>有监督学习就是在训练组中已知数据的结果，可以对模型的训练进行Supervise监督。无监督就是拿到手的训练集并不知道分类情况，要根据算法来区分并生成对应的结果。
硬间隔是理想化的世界，非红即白，不允许出错。软间隔有容错率更现实点，包容性强，更有普适性。核函数可以在原本训练集中多加一维，让分类更容易。</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/79/9a/4f907ad6.jpg" width="30px"><span>Python</span> 👍（1） 💬（0）<div>老师，多分类器用的是集成法吗？</div>2019-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Lop0uAwiawHbqgRFYqIZv2YbFMJSeDePB0fia3j6joQQ3sddhvgpic6ibXLkva572O6dWS3QzicOibJGjr4QjrNXEgwg/132" width="30px"><span>忙了你个狗</span> 👍（0） 💬（0）<div>核函数的作用我可以理解就是一拍桌子球弹了起来这个时候可以找到一个平面把球分开的过程吗</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/88/4c/2c3d2c7d.jpg" width="30px"><span>小强</span> 👍（0） 💬（0）<div>其中||w||为超平面的范数，di 的公式可以用解析几何知识进行推导，这里不做解释。这是能否学下去的精神支柱，被老师放弃讲解了</div>2020-09-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAl7V1ibk8gX62W5I4SER2zbQAj3gy5icJlavGhnAmxENCia7QFm8lE3YBc5HOHvlyNVFz7rQKFQ7dA/132" width="30px"><span>timeng27</span> 👍（0） 💬（0）<div>svm “超平面”将样本分为两份。它是二分类器，最大化最小距离。硬间隔，将两个完全分开；软间隔，可以存在误差；非线性可分的，就需要使用到核函数，可以理解为将坐标转换，比如直角坐标转成极坐标，或者理解为投影到某个平面。
如果要多分类，可以1对多，过1对1。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4d/62/0fe9cbb3.jpg" width="30px"><span>William～Zhang</span> 👍（0） 💬（1）<div>老师 有个问题 关于文中最大间隔 指的其中分界线c 距离左侧点的最大距离还是右侧点？</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（0） 💬（1）<div>硬间隔：需要完全分开
软间隔：允许有个别点分类错误
核函数：转换到更高维度来达到分类效果
还有想问下为什么说落在超平面上的点就是支持向量？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（1）<div>老师，这里面用二分类算法实现多分类怎么用，比如一对多分类，一个测试样本分别用这几个训练模型去匹配，的到的结果难道是百分比吗？哪个大属于哪个分类？</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/0d/b4258141.jpg" width="30px"><span>姜泮昌</span> 👍（0） 💬（0）<div>老师，能不能讲讲这些分类算法的区别？尤其是二分类算法，在使用时怎样进行选择呢？谢谢</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/76/6d55e26f.jpg" width="30px"><span>张晓辉</span> 👍（0） 💬（0）<div>监督学习适用于打标签的数据。无监督学习适于用没有标签的数据。
SVM的硬间隔是指线性分类器完全线性可分，软间隔是指允许线性分类器有一定的分类错误。核函数是针对非线性可分的情况提出来的，可以利用核函数把样本空间投射到高维空间，然后再利用线性分类器进行分类。</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/ec/985675c8.jpg" width="30px"><span>小高</span> 👍（0） 💬（0）<div>有点烧脑了，慢慢消化，感觉一篇文章要花几个小时才能消化。</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/31/f0a884a3.jpg" width="30px"><span>Geek_dancer</span> 👍（0） 💬（0）<div>SVM如何与回归应用联系起来？</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/97/77/a01ebefc.jpg" width="30px"><span>Wei_强</span> 👍（0） 💬（0）<div>能讲解一下什么叫做“线性不可分”么？对这个知识点不是很了解，结果导致文章后面的知识点没有怎么理解</div>2019-02-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wJphZ3HcvhjVUyTWCIsCugzfQY5NAy6VJ0XoPLibDlcHWMswFmFe678zd0lUjFETia80NQhyQcVnGDlKgKPcRGyw/132" width="30px"><span>JingZ</span> 👍（0） 💬（0）<div>监督学习和无监督学习根本区别在于是否有标签，核心分别是分类和聚类、同维和降维等~

硬间隔、软间隔、核函数是适用于线性可分、不完全可分、不可分等不同情况下的分类思想</div>2019-02-12</li><br/>
</ul>