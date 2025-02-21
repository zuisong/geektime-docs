你好！我是郑晔。

在上一讲中，我以Spring的DI容器为例，给你讲解了如何理解一个项目的模型。在模型之后，下一步就该是接口了。

在任何一个项目中，接口的数量都不是一个小数目。仅仅一个普通的程序库，里面的接口少则几十个，多则成百上千。难道我们理解接口，就是要一个一个地读这些接口吗？

显然，你不太可能把所有的接口细节都记住。我写Java程序差不多 20 年了，但很多JDK里的类我都不了解。甚至有时候，还没有等我去了解这个类，它就过时了。

那么，如何才能从纷繁复杂的接口中，披荆斩棘而出呢？我给你个方法：**找主线，看风格**。

**找主线**的意思是，你需要找到一条功能主线，建立起对这个项目结构性的认知，而不是一上来就把精力放在每一个接口的细节上。你对细节部分的了解会随着你对项目的深入而逐渐增加。而有了主线后，你就有了着力点，就可以不断深入了。

但是，我们要学习的不只是这些接口的用法，要想从项目的接口设计上学到更多，这就需要你关注它所引导的**风格**，换句话说，就是它希望你怎样使用它，或是怎样在上面继续开发。

从一个项目的接口风格中，我们不难看出设计者的品位。我们常把编程视为一种艺术，而在接口的设计上就能窥见一二。这些内容是我们在学习软件设计时，应该慢慢品味的。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/86/d689f77e.jpg" width="30px"><span>Hank_Yan</span> 👍（20） 💬（3）<div>找主线，看风格。找主线看文章，看风格看接口。从上到下，从整体到局部。不过这也是正常读源码的一个步骤。</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（16） 💬（2）<div>1.最早自学的就是ruby，要不是因为找不到工作，可能就做不成javaer了。论快速搭建一个web项目，至今依旧是ruby on rails。一个多小时从无到有搭建一个博客系统的时候，信心爆棚。

2.本篇，明天得再看看。get不到点。只能理解风格应该是说设计偏好。至于主线，从ruby这个demo里没能get到。


3.spring。兼容（老版本以及各种场景），开放（提供规范和基础工具，方便各种“实现”自己写插件接入spring），与时俱进（springboot的推出，算得上破而后立），追求卓越（在迭代中改变接口命名，只为让原本达意的命名更达意）</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（7） 💬（2）<div>Ruby on Rails这个设计在当时感觉很超前,也不知道现在的SpringBoot是不是借鉴了,感觉从SpringBoot上能看倒Ruby on Rails的身影, SpringBoot的约定大于配置,还SpringBoot把命简洁的页面,勾选之后就可以创建一个简单的SpringBoot项目等等,Ruby on Rails的设计在现在看来可能确实没什么,但在当时感觉这个设计就太超前了.</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/63/7eb32c9b.jpg" width="30px"><span>捞鱼的搬砖奇</span> 👍（7） 💬（1）<div>在 Spring 的源码中 接口 -&gt; 抽象类-&gt;实现类，如 BeanDefinition -&gt; AbstractBeanDefinition -&gt; RootBeanDefinition。这样的设计风格。顶层接口规定定义，抽象类提供部分实现。用户需要扩展，可以选择从抽象类进行扩展，或从接口扩展。
</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/f2/2a9a6e9a.jpg" width="30px"><span>行与修</span> 👍（6） 💬（1）<div>好的设计要多从使用者角度考虑，是否有助于释放程序员精力，是否易用，是否有良好的可读性和可扩展性。自己先用，并在开始时就设定好边界，即使先只在一点上有所突破也比全面开花哪哪不灵要好。</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/3d/928b41f1.jpg" width="30px"><span>六一王</span> 👍（5） 💬（1）<div>接触的第一个框架就是 rails，用起来确实很爽，今天看到此篇文章，让我对它更有敬意，而不会因为现在不就行，或者性能不够好，就看不起它，没有东西是绝对的好，或者绝对不好，今天全是对这个道理有更深层的理解了。
我之后学习了JavaScript，转了前端，学习 Vue 框架，它使用虚拟dom将组件高度抽象化，使页面组件可以多端运行，比如node端，如此可以前后端同构，解决单页面应用的劣势，而保留其优势。
模块如何拆解然后又如何组装，逻辑清晰。
提供了很多全局组件和生命周期函数，以及其他方法，这些就是给程序员提供的接口，可以让我们在特定的场景让你更加关注功能需求的实现，而不是代码的实现细节，会自动帮你做好很多事情。
并且使用了很多高阶函数，化繁为简，最终返回一个干净的只有核心逻辑的函数。即大量使用了函数式编程。
学习的过程就是写一段简单的，特定场景代码，然后进行断点测试，看看源码中主要会走那些流程。然后大概就有了一条小主线。
好的框架理解起来应该是容易的，清晰的。而那些不假思索写出来的面向过程的代码，如果不一行一行去看的话，就不知道问题出在哪里，甚至以后回过来看，都不知道自己是怎么写出这种代码的，就像写正则表达式一样，写完之后，自己都看不懂了。
</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/ee/96a7d638.jpg" width="30px"><span>西西弗与卡夫卡</span> 👍（5） 💬（1）<div>怀念RoR，起初用过，后来因为性能，我们都替换成Java了</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（5） 💬（1）<div>最早接触BDD是cucumber，当时觉得简直是magic。整个RoR框架也到处给人magic的感觉。但是软件开发不应该有magic，否则容易失控。RoR式微部分原因可能也是Ruby过于灵活了，印象中RoR有些严重的安全漏洞就是由此引发。此外Ruby的执行效率也逐渐落后于时代了。近年来有Crystal语言借由llvm复兴Ruby，加入了很多现代语言的特性，希望能有好结果。</div>2020-06-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/sWJX4YJIuhibOOScX09NbBp2Fn0lItp1a2iaIQQWV5MfULria4jByUlsq4FDsxI9JNEXJibCcNLLib5cPRd4fh8zJ4A/132" width="30px"><span>jakimli</span> 👍（4） 💬（3）<div>问个问题，如果说rails落伍的原因是因为Javascript，为什么没有演变成 javascript + rails后端服务这样的组合呢？</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（4） 💬（1）<div>理解软件中的接口设计，要抓住主线，可以从文档开始入手，了解软件设计者的风格品味，看看作者希望我们是如何使用这些接口的。
我没用过Ruby，但是通过分析之后，其实它的接口设计中，整合了许多极佳的工程实践，提高编码效率，解放生产力，这些思想在软件设计的时候是可以学习和参考的</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（3） 💬（2）<div>“优雅的编程接口，顺畅的开发过程”，虽然我也非常的喜欢 Ruby on Rails，却没有办法像老师这样精辟的总结提升。

给我的感觉，RoR 在设计的时候非常的体贴程序员，并且采用了一大堆优秀的设计范式。

看了文中对于 Rails 接口的分析，感觉更喜欢 Rails 了，可惜的确如同留言里面 @Jxin 说的那样，工作不好找，另外薪水不高。

如果按照开发模式的变迁，那么现在是不是应该学习 Deno ? 请老师推荐一个比较有潜力的语言或者框架，Go 或者 TypeScript ？</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/89/4fda09bd.jpg" width="30px"><span>舀点米 | Titus Mi</span> 👍（2） 💬（1）<div>那python的Django是不是也有rails的问题？那flask呢？java的spring boot是更好的实践吗？
另外rails应该也可以使用前后端分离吗？老师是否还可以再分享下，spring具体是如何越来越强大，使得rails落伍？spring和node如何联手超越rails的？</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/cc/ca22bb7c.jpg" width="30px"><span>蓝士钦</span> 👍（2） 💬（1）<div>关于接口想请教一下老师，我们平时在公司内部的二方库，是不是应该拆分成两个jar包，分为api模型包和一个实现包。对于大多数开发业务我们只关心一个系统的模型以及提供什么样的功能接口。拆分成不同包可以根据需要引入不同的实现包，而api和模型是共用的。 比如最近有个项目需要把查数据湖的报表改成差数据库，如果封装的足够好应该只要替换实现就可以不改一行代码达到目标。</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（2） 💬（0）<div>今天熊大在群里说了“没用过 rails 就不足以聊 DDD”、“我以为玩玩 rails 是程序员的基本要求呢”，同时也推荐了一本书《Agile Web Development with Rails》。特地再来复习复习。</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>这一章的内容，读起来并没有 get 到内容，先继续向下看</div>2023-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cb/93/124d8cd8.jpg" width="30px"><span>努力努力再努力</span> 👍（0） 💬（0）<div>不知道是不是3年经验问题……感觉好难get到老师想表达的设计点在哪</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>理解一个项目的接口，先找主线，再看风格。--记下来</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（0）<div>现在对模型的理解，依然是很懵懂～</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/5a/6033b9f0.jpg" width="30px"><span>阿彪</span> 👍（0） 💬（0）<div>模型是指MVC?  我还以为是我们建的各种自定义业务模型</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/d3/67bdcca9.jpg" width="30px"><span>林铭铭</span> 👍（0） 💬（0）<div>找主线识别整体流程，看风格识别编程习惯。</div>2021-04-23</li><br/>
</ul>