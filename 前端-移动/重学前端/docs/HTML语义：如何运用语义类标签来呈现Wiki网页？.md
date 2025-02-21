你好，我是winter，今天我们继续来聊聊HTML模块的语义类标签。

在上一篇文章中，我花了大量的篇幅和你解释了正确使用语义类标签的好处和一些场景。那么，哪些场景适合用到语义类标签呢，又如何运用语义类标签呢？

不知道你还记不记得在大学时代，你被导师逼着改毕业论文格式的情景，如果你回想一下，你在论文中使用的那些格式，你会发现其实它们都是可以用HTML里的语义标签来表示的。

这正是因为HTML最初的设计场景就是“超文本”，早期HTML工作组的专家都是出版界书籍排版的专家。

所以，在这一部分，我们找了个跟论文很像的案例：Wikipedia文章，这种跟论文相似的网站比较适合用来学习语义类标签。通过分析一篇Wiki的文章用到的语义类标签，来进一步帮你理解语义的概念。

你可以在电脑上，打开这个页面：

- [https://en.wikipedia.org/wiki/World\_Wide\_Web](https://en.wikipedia.org/wiki/World_Wide_Web)

为了防止这个页面被修改，我们保存了一个副本：

- [http://static001.geekbang.org/static/time/quote/World\_Wide\_Web-Wikipedia.html](http://static001.geekbang.org/static/time/quote/World_Wide_Web-Wikipedia.html)

这是一篇我们选择的Wiki文章，虽然在原本的Wikipedia网站中，也是大量使用了div和span来完成功能。在这里，我们来尝试分析一下，应该如何用语义类标签来呈现这样的一个页面/文章。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/3b/85738679.jpg" width="30px"><span>wangzy</span> 👍（43） 💬（1）<div>语义化标签的一些点可能会降低开发者的使用欲望
1.有些标签可能还不知道就已经过时了
2.很多语义标签自带样式，而这些样式我们并不需要，所以还要先取消默认样式。
3.现代网页已经不再是按照书籍排版的结构来的，很多页面元素并不容易明确应该使用哪个语义标签。</div>2019-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dTyEibufUO2hbfC5vibTTJlXEw86MKQ8lzkE6LiaAfHmkWkSVJeMmrgPo0Tnm2fXyEKRicKBpBu05Kvyia7LnTKJv7Q/132" width="30px"><span>silver6wings</span> 👍（4） 💬（1）<div>在未来高度自动化后，设计师编辑好的矢量图文件可以自动生成前端代码的技术产生之后，这门手艺是否还会需要，还是会变得像手工刺绣一样仅仅是一项娱乐运动，这点大佬您怎么看？</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/c7/0f3b699f.jpg" width="30px"><span>朋克是夏天的冰镇雪碧</span> 👍（0） 💬（1）<div>看到文中说 cite 标签表示引述的作品名，一下子有点没理解这句话是什么意思，然后自己去搜了搜，看到有人说可以把 cite 标签理解为书名号，豁然开朗。</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fd/86/861cfc30.jpg" width="30px"><span>Anoxia.苏</span> 👍（0） 💬（1）<div>两个wiki的页面，一个无法打开，一个打开后显示not found

极客时间版权所有: https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;78168</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/fc/0b324280.jpg" width="30px"><span>Semantha</span> 👍（0） 💬（1）<div>这篇文章中的好多标签都没用过。。。</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/20/2e/8751620e.jpg" width="30px"><span>孤舟【Evelyn】</span> 👍（0） 💬（1）<div>请问是几个模块交叉来讲的吗？还是html部分已经结束？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/78/a6/706f8dd9.jpg" width="30px"><span>一直都在</span> 👍（0） 💬（1）<div>老师，html5的新的标签兼容都不是很好，很多低版本的浏览器都不支持（那应该如何去语义化文本文档结构呢，我一般是写注释，您有什么好的建议呢？）</div>2019-02-15</li><br/><li><img src="" width="30px"><span>扇子</span> 👍（0） 💬（1）<div>winter老师能不能提供下与课程对应的实际的源码供我们进一步详细学习呢？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/87/8e3297a3.jpg" width="30px"><span>ClarenceC</span> 👍（0） 💬（1）<div>突然觉得 html 语义标签，有点像 markdown 语法，都是用一个标签去表达一个文本的意思和作用。请求一下 winter 大大，因为现在我们一般都是使用 div span 搭建结构，语义标签的实用场景在那里呢？移动端和 pc端会不会有所不同啊？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/8e/4860b6b5.jpg" width="30px"><span>LeonZhang</span> 👍（0） 💬（1）<div>最后的表格当中date写错成data了</div>2019-01-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIfI4IVbPPia88MPBgyC74duA452vcNaibnD7N1rK0YEdmOSHMCtpDCFwR3goZeIph7icSiazSNsWSGqg/132" width="30px"><span>进啊进</span> 👍（0） 💬（1）<div>如果是用百度搜索，如果严格的按照语义化的标签去写html,也不清楚在哪一页出现。所以觉得语义化是给开发者看的，对国内seo来说可能微乎其微。</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（182） 💬（2）<div>就擅长div span a标签😂</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fb/3c/16a1127b.jpg" width="30px"><span>鱼膩</span> 👍（73） 💬（0）<div>进入wiki点开控制台，发现很多地方wiki本身并没有严格地按照win大说的来， 大部分也是did, span一把梭，有顺序的nav直接用的ul, 文中说的code, sample这些也都没有用。。是不是可以理解成其实很多时候我们为了实现样式的完全控制，降低了对HTML本身语义化的要求； 或者说在大部分条件下，快速还原设计稿比语义化本身更重要</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/16/6f/9f30a9e0.jpg" width="30px"><span>咖飞的白</span> 👍（63） 💬（0）<div>看懂之后，果断敲出一个wiki页面来，才是最好得学习。</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（43） 💬（0）<div>由于项目的关系，大部分时候是制作品牌网站和软件界面的场景，因此我最擅长的语义标签是「作为整体结构」的语义类标签。

在这两个场景中，一般不会有大段的阅读文字（即使是 FAQ，也避免大段文字，毕竟没人喜欢读字）。

深度了解语义类标签使用的一个技巧，就是去了解爬虫是如何理解自己的网站，从而逆向理解标签是否使用得当。

这篇文章最大的收获，就是认识到自己对「自然语言延伸」和「标题摘要」的语义类标签理解不足。比如 pre 和 samp，让我有”居然是这样使用“的感觉。

现在知道，如果遇到内容网站的场景（比如博客），我就应该复习一次「自然语言延伸」和「标题摘要」的语义类标签文档，确保正确使用。

谢谢 winter 老师。
</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/30/13e42374.jpg" width="30px"><span>Yancey</span> 👍（31） 💬（3）<div>维基百科毕竟太老，div span一把梭也很正常，看一下苹果的页面，你就会很有收获</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/06/4e/501a528c.jpg" width="30px"><span>木子烁束岸</span> 👍（27） 💬（0）<div>简历上写精通html的，脸疼了</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/44/d5cf762b.jpg" width="30px"><span>段先森</span> 👍（18） 💬（0）<div>瑟瑟发抖</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/e0/cc542398.jpg" width="30px"><span>张张张小烦</span> 👍（14） 💬（0）<div>只想说， 好多标签都没见过，更别说用过， 惭愧惭愧</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/f5/1fa34f88.jpg" width="30px"><span>润曦</span> 👍（13） 💬（3）<div>这里的 hgroup标签需要说明一下，早期在HTML5规格尚未发布正式版的时候，当时是有hgroup标签的，但HTML5工作小组在2013年4月2日的一次会议结论中决定从规格中移除hgroup元素，因此请大家不要再用这个hgroup元素。我在使用angular的时候，用hgroup无法正常执行的 ，要执行需要加入NO_ERRORS_SCHEMA到ngModule的schemas中</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/00/245bf3cb.jpg" width="30px"><span>鱼竿</span> 👍（12） 💬（0）<div>涨知识了，虽然在开发中最常用到的还是div和span，但是换一种思路，了解了语义的概念之后，麻麻再也不用担心我的classname造不出名字了，将这些语义化的表达方式融入到样式的命名中，也是提高代码可读性的方法吧

感谢win大</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/9a/c03bea17.jpg" width="30px"><span>金子菇凉的铁粉小逗</span> 👍（11） 💬（0）<div>微信小程序的wiki适配性很好，能简单说一下怎么实现的吗？</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/80/07de6693.jpg" width="30px"><span>叫我大胖就好了</span> 👍（10） 💬（0）<div>我听哭了，感觉自己啥也不会了</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fa/bf/04eac201.jpg" width="30px"><span>Sylvia</span> 👍（9） 💬（0）<div>不求多，只求精，除了上一篇的标签，此篇文章的abbr pre code figcaption  site time dfn，我能说这些标签我几年前就用过，但后来见几乎没人用，也舍弃了，有些东西还是需要多坚持呀∑(´△｀)？！</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/e7/2df279fd.jpg" width="30px"><span>反 面 典 型</span> 👍（9） 💬（0）<div>曾经做过whatwg文档的中文翻译工作，那里面的语义化在我看来是做到了极致</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5e/27/a871073d.jpg" width="30px"><span>小M</span> 👍（7） 💬（0）<div>果真需要重学前端</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/a3/378d8207.jpg" width="30px"><span>五线青年水煮饺</span> 👍（7） 💬（0）<div>我只会div套div。还在努力学习。</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（6） 💬（0）<div>1通过wiki的例子发现真实的网页中还是有使用语义化的，之前以为现实应用中很少。

2看来有必要优化下我们网页的布局模板了。

3hr标签语义是话题的转向，学习了。之前以为就是一条横线，学习了。</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/ff/ae800f6b.jpg" width="30px"><span>我叫张小咩²⁰¹⁹</span> 👍（5） 💬（0）<div>学语义，上wiki😂

读到这，暂时把语义化标签分两类：
结构类 header footer ……
文本标记类 em b q s u ……

之后把所有的标准读完，总结成自己的知识，可以用逻辑推理出来的知识脉络。
</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/70/7d736d5f.jpg" width="30px"><span>小动物很困</span> 👍（5） 💬（0）<div>1.标题+列表 dl&gt;dt&gt;dd
2.普通列表 ul&#47;ol &gt;li
3.header section footer nav等整体布局语义
4.div+span大法
别的不会了....</div>2019-01-28</li><br/>
</ul>