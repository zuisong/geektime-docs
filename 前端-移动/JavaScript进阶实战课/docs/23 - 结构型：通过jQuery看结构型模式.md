你好，我是石川。

今天，我带你顺着上一节的内容，再来看看在GoF（四人组）的[《设计模式：可复用面向对象软件的基础》](https://book.douban.com/subject/34262305/)这本书中介绍的另外几种经典的结构型设计模式。我们可以通过jQuery来看看结构型的设计，说到这里，你可能会说jQuery可以算是被吐槽比较多的一个框架了，它有什么参考价值呢？但是我认为用户是用脚投票的，虽然很多人在骂着jQuery，但是同时也在用着。这也证明了它从开发上提供给人们的便捷，作为优点要大于它的缺点。其实，它的很多让人们“恨不释手”的设计背后都能看到结构型的设计模式。今天，我们就一起来看看吧。

## 几种经典的结构型模式

我们先来看看几种经典的结构型模式。分别是享元、门面和组合模式。

### 享元模式（flyweight）

享元模式（flyweight）的核心思想是**通过减少对象的创建数量来节约内存**。

享元模式最早是保罗·考尔德和马克·林顿在 1990 年提出的。喜欢看拳击的朋友可能知道享元的英文单词flyweight，其实是拳击里面的一个重量等级，叫做“特轻量”，也就是重量低于112磅的拳手。我们来看一个UFC比赛画面，一个重量级（heavy weight）和特轻量级 （flyweight）的选手放在一起对比，感受就更直观了。所以顾名思义，该模式旨在帮助我们实现轻量级的内存占用。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/73/8079d3fd.jpg" width="30px"><span>郭慧娟</span> 👍（0） 💬（1）<div>Facebook ... 减少一层抽象，或避说呢，免创建新的 jQuery 对象。这里文案有问题</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/3a/35/ea6fde99.jpg" width="30px"><span>FSS</span> 👍（0） 💬（0）<div>&#47;&#47; 如果车型已知，就返回vin；未知就创建var createCar = (model, maker, isbn) =&gt; {
形参isbn是否应该为vin</div>2023-12-12</li><br/>
</ul>