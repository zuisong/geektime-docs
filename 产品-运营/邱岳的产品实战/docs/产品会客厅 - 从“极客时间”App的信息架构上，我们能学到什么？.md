## 写在前面的话

极客时间的专栏读者你好，我是邱岳。

我们在之前的产品会客厅中，分享了产品经理如何从一个App入手，去研究和学习。有朋友给我们留言，说希望可以用一个App从头演示一下。这次我们用“极客时间”App作为例子，一起研究一下。

由于篇幅有限，我们就不按照之前说的整体逻辑全部过一遍了，我们着重来看信息架构方面的拆解和分析，其他的部分就留给你自己来发挥。

## 邱岳分享

首先我们打开极客时间的App，这个结构大家应该都已经非常熟悉了，共有三个Tab页。

第一个是首屏，它是一个根据运营属性的一个页面，第二个是知识产品的一个索引和列表，它就是一个跟信息架构直接相关的一个结构，第三个是个人中心。

我们直接从第二个Tab页看，因为它背后的东西，就是极客时间App里的所有的概念实体。

在App里面，其实有四种不同的知识性产品，它们是文字专栏，视频课程，每日一课和微课，接下来我们去看每种知识产品的信息结构，以及它的设计是怎样承载信息结构的。

## 文字专栏的信息架构

首先我们来看文字专栏。如果我们来看一个没有买过的文字专栏，可以发现一个信息页面，我们可以在这里进行订阅，通过信息页可以进到免费试读，通过免费试读，可以再进入到Detail页，在Detail页我们可以完成订阅。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_ol8mqs</span> 👍（9） 💬（0）<div>产品目前对已购内容学习场景设计的特别不友好，路径过长</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/79/a74d1e60.jpg" width="30px"><span>代码丸子</span> 👍（8） 💬（0）<div>要实现结构清晰、重点突出的界面设计方案，你必须首先梳理出结构清晰、重点突出的信息架构。作为产品设计师，我们需要在这里承担思考与分析的责任，否则这一重担势必会落到用户身上。

在思考信息架构时，出现在我们头脑中的应该是一系列抽象的信息单元，包括名词与动词等等，而非具体的像素、组件或页面。这样，你很快便会发现，任何产品无法只是信息的集合；而用户怎样理解和使用产品，最终将取决于我们以怎样的方式将这些信息进行整合。

这就像在造句 – 各种名词、动词的组合方式决定着最终能够传达出怎样的信息。

产品也是如此。一个app可以抽象成若干名词与动词的组合，包括“事物”以及“我能对这个事物执行的行为”。其中的名词非常重要，app的信息世界正是由它们组成的大体上讲，app界面当中存在着这样一种比例关系 – 绝大多数的界面元素（约80%）用于呈现“名词”；一小部分用于呈现“动词”，即用户可以对那些名词进行的操作。</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8b/38b93ca0.jpg" width="30px"><span>听天由己</span> 👍（2） 💬（0）<div>还是看视频舒服，可能文字看久了，总会想着有画面更有温度。

今天主题的确适合视频切入，能够顺着思路去思考这样的信息架构是如何产生、设计并且交互的。

我对信息架构不敏感，但通过多次的首页设计，也慢慢领悟了一些原则：我们每个页面想要为用户传递的内容是什么？在不同场景下，这些信息是否足够且唯一？

二爷提了很多次概念实体，这是我们理解产品和内部沟通的关键一环，基于同样的话语才能建立概念与观念。</div>2018-12-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/NYfjRelia7DOibtRycUN7jY2ibiboQNhcLzHqUZgTqCwPTUaYYLV4N8iaosvxUXXaibdkV1aa1sBz2PCYtD3ANYlicb0g/132" width="30px"><span>咋个学才快</span> 👍（1） 💬（0）<div>这么快就结束了。。其中还是学到了很多，不仅是专栏，还有些留言也对我的认知有帮助的。
另外看这个才知道有社群，有时间上app再看下。。</div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/23/27ab9782.jpg" width="30px"><span>向茂遥</span> 👍（1） 💬（0）<div>视频结尾突然伤感了一下……</div>2018-11-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er57GdibI3V84D4EdJUXe2dmNprumibCwGCH4ibF8OcNr79cmCteNpD4eicJbaIQAtrS5GAPxDzLpB23Q/132" width="30px"><span>Geek_57b0e3</span> 👍（0） 💬（0）<div>学习方法很好，挺受用的</div>2023-06-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqAVNKZWBEnEf0Qz4SG3ZkkfYsia1L429N64XicGgYiak3jnKaFibibiclNEibWiatJUK5ywTicCsDpPZ1toaw/132" width="30px"><span>杜微</span> 👍（0） 💬（0）<div>很不错</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1c/85/22a6124d.jpg" width="30px"><span>青川</span> 👍（0） 💬（0）<div>获益匪浅</div>2021-11-12</li><br/>
</ul>