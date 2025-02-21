你好，我是蔡元楠。

今天我要与你分享的主题是“WordCount Beam Pipeline实战”。

前面我们已经学习了Beam的基础数据结构PCollection，基本数据转换操作Transform，还有Pipeline等技术。你一定跃跃欲试，想要在实际项目中使用了。这一讲我们就一起学习一下怎样用Beam解决数据处理领域的教科书级案例——WordCount。

WordCount你一定不陌生，在[第18讲](https://time.geekbang.org/column/article/97658)中，我们就已经接触过了。WordCount问题是起源于MapReduce时代就广泛使用的案例。顾名思义，WordCount想要解决的问题是统计一个文本库中的词频。

比如，你可以用WordCount找出莎士比亚最喜欢使用的单词，那么你的输入是莎士比亚全集，输出就是每个单词出现的次数。举个例子，比如这一段：

```
HAMLET

ACT I

SCENE I	Elsinore. A platform before the castle.

	[FRANCISCO at his post. Enter to him BERNARDO]

BERNARDO	Who's there?

FRANCISCO	Nay, answer me: stand, and unfold yourself.

BERNARDO	Long live the king!

FRANCISCO	Bernardo?

BERNARDO	He.

FRANCISCO	You come most carefully upon your hour.

BERNARDO	'Tis now struck twelve; get thee to bed, Francisco.

FRANCISCO	For this relief much thanks: 'tis bitter cold,
	And I am sick at heart.

BERNARDO	Have you had quiet guard?

FRANCISCO	Not a mouse stirring.

BERNARDO	Well, good night.
	If you do meet Horatio and Marcellus,
	The rivals of my watch, bid them make haste.

FRANCISCO	I think I hear them. Stand, ho! Who's there?
```

在这个文本库中，我们用“the: 数字”表示the出现了几次，数字就是单词出现的次数。

```
The: 3
And: 3
Him: 1
...
```

那么我们怎样在Beam中处理这个问题呢？结合前面所学的知识，我们可以把Pipeline分为这样几步：

1. 用Pipeline IO读取文本库（参考[第27讲](https://time.geekbang.org/column/article/102578)）；
2. 用Transform对文本进行分词和词频统计操作（参考[第25讲](https://time.geekbang.org/column/article/101735)）；
3. 用Pipeline IO输出结果（参考[第27讲](https://time.geekbang.org/column/article/102578)）；
4. 所有的步骤会被打包进一个Beam Pipeline（参考[第26讲](https://time.geekbang.org/column/article/102182)）。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（1）<div>如何用Apache Beam求word count TopK问题呢？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（1）<div>如果要按word出现次数从大到小排序应该怎么写？</div>2019-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqEacia8yO1dR5Tal9B7w8PzTRrViajlAvDph96OqcuBGe29icbXOibhibGmaBcO7BfpVia0Y8ksZwsuAYQ/132" width="30px"><span>杰洛特</span> 👍（6） 💬（4）<div>前两章还在说不要使用任何 DoFnTester 进行测试，这边怎么又来写 DoFnTester 了？感觉这专栏像是很多人写了拼起来的，有很多前后矛盾的地方</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（4） 💬（0）<div>Beam的函数确实难用，不像spark和scala collection那样用起来直观. 
sc.textFile(&quot;file:&#47;&#47;&#47;your-input.txt&quot;).flatMap(_.split(&quot;[^\\p{L}]+&quot;)).map((_,1)).reduceByKey(_+_).map(_.swap).sortByKey(false).map(_.swap).collect</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/b0/77e5f8c8.jpg" width="30px"><span>李孟聊AI</span> 👍（1） 💬（0）<div>这还是比较重，spark求同样的需求几个函数就搞定了</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a0/f4/7e122a67.jpg" width="30px"><span>之渊</span> 👍（0） 💬（0）<div>实例代码 https:&#47;&#47;gitee.com&#47;oumin12345&#47;daimademojihe&#47;blob&#47;e20d60b93113d2537f4bd2e7f38b23ac17d4c3c0&#47;cloudx&#47;bigdata&#47;src&#47;main&#47;java&#47;test&#47;beam&#47;WordCountBeam.java
从我这个新人角度来看。虽然代码可能看起来没有spark 那些那么简洁。但是编程思想就是全部都是transform 。而且都是 链式调用，apply(xx).apply(xx) 其实没有差到哪里去。
1. 上手难得大大减低。spark 太多算子了，什么并发算子，什么action类的啊，等等。概念太多了。而beam 帮我们自动优化了。就好像在写很传统的java 代码一样。而且也非常易于理解。
2. 如果要类比的话，就好像 Apache beam 就是mybatis ， 而 spark ,flink 就是 hibernate了。</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/86/d689f77e.jpg" width="30px"><span>Hank_Yan</span> 👍（0） 💬（0）<div>还是spark方便一些。。。beam看了这么多节，只能感受到其出发点，问题抽象的独到之处，很难感受实际工作中会带来什么益处，文中例子不太容易领悟到这点。</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/7b/45/871a64fb.jpg" width="30px"><span>jeeeeeennnny</span> 👍（0） 💬（1）<div>Sideinput 可以根据业务逻辑新增数据吗？</div>2020-03-24</li><br/>
</ul>