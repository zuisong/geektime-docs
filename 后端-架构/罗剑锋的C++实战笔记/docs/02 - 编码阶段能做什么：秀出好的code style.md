你好，我是Chrono。

上节课我介绍了C++程序的生命周期和编程范式，今天我就接着展开来讲，看看在编码阶段我们能做哪些事情。

在编码阶段，我们的核心任务就是写出在预处理、编译和运行等不同阶段里执行的代码，还记得那句编程格言吗：

“**任何人都能写出机器能看懂的代码，但只有优秀的程序员才能写出人能看懂的代码。**”

所以，我们在编码阶段的首要目标，不是实现功能，而是要写出清晰易读的代码，也就是要有好的code style。

怎么样才能写出human readable的好代码呢？

这就需要有一些明确的、经过实践验证的规则来指导，只要自觉遵守、合理运用这些规则，想把代码写“烂”都很难。

在此，我强烈推荐一份非常棒的[指南](http://openresty.org/cn/c-coding-style-guide.html)，它来自OpenResty的作者章亦春，代码风格参照的是顶级开源产品Nginx，内容非常详细完善。

不过有一点要注意，这份指南描述的是C语言，但对于C++仍然有很好的指导意义，所以接下来我就以它为基础，加上我的工作体会，从**代码格式**、**标识符命名**和**注释**三个方面，讲一下怎么“秀出好的code style”。

## 空格与空行

当我们拿到一份编码风格指南的时候，不论它是公司内部的还是外部的，通常第一感觉就是“头大”，几十个、上百个的条款罗列在一起，规则甚至细致到了标点符号，再配上干巴巴的说明和示例，不花个半天功夫是绝对看不完的。而且，最大的可能是半途而废，成了“从入门到放弃”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/04/89cc31ab.jpg" width="30px"><span>嵇斌</span> 👍（39） 💬（3）<div>分享我的一些实践：
1. 匈牙利命名真心不推荐了，参考《clean code》中关于avoid encoding的说明。
2. 如果是存现代c++工程，不考虑兼容C的话. Header guards可以使用#pragma once替代。
3. 避免注释，最好使用代码来阐述。很多信息可以通过代码仓库来表达，比如commit message。
4. m_，g_ 等前缀如果使用现代化的ide的话，也可以考虑省略，因为ide的高亮能够区分。
5. 如果不是在写类库，比如开发应用程序，最好命名规则能快速区分这个是你的代码，还是标准库、知名类库的代码，可能这也是大厂流行CamalCase的缘由。
6. Google的style guide是个不错的参考，但是也有很多不可取的规则，感觉原因：Google出这个guide的时候modern c++还没有流行，Google当时内部还有很多技术债，Google想把c++写的像java。所以Google后来在golang里面....
7. 如果是参与现有项目，无论现有规则多么的不爽，都先遵循现有的规则。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/e4/e7471344.jpg" width="30px"><span>jxon-H</span> 👍（17） 💬（1）<div>磨刀不误砍柴工，编码风格我觉得不仅是软件开发行业的共识，更是一种软件开发的文化。回顾我自己写过的代码，简直惨不忍睹。罗老师这节内容让我收获极大，也让进一步加深了以下认识：

1、之所以讲究编码风格，因为软件的规模越大，协作性要求就越高，软件开发是一件群体性的智力活动，每个人的代码都只有自己懂，每段代码都将成为一个信息孤岛，没法让代码变得可交流、可复用、可维护。

2、一段代码的功能，不仅仅是完成一个任务，也是一种思想的传播，因此注释担当着传递信息的功能，要养成良好的注释习惯和明了易懂注释风格。

3、留白的艺术深受启发，既给代码空间留下了闲余，给视觉留下了美感，也给代码的阅读增添了节奏，更是给大脑腾出足够的思考空间。
</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/5b/8e321b62.jpg" width="30px"><span>Carlos</span> 👍（15） 💬（4）<div>哈哈, 容我先说一句题外话, 我作为一个 c++ 入门新手, 昨天和前天还真的读了一份 &quot;公司色彩很重&quot; 的 code style guide 😂(虽然没完全读懂). 

1. 今天文章中的 &quot;留白&quot;, 和 &quot;命名&quot; 我倒是注意到了, 但是可能因为我目前写的 c++ 代码基本上都是不超过 50 行的练习文件, 所以注释这一点我没有注意到, 从现在开始注意. 
2. 我觉得另一个重要的用法是把一些代码备注掉. 可能是为了 debug 方便(如果新代码错了, 换回旧代码, 程序还能运行), 也可能是为了以后功能拓展方便(直接把相关模块取消备注就能用了). 

补充一条我前天刚学会的 code style: 

All header files should have #define guards to prevent multiple inclusion. The format of the symbol name should be &lt;PROJECT&gt;_&lt;PATH&gt;_&lt;FILE&gt;_H_</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/69/c2/519723fb.jpg" width="30px"><span>winsummer</span> 👍（12） 💬（1）<div>老师，函数的注释是写在声明处还是写在定义处好呢</div>2020-05-09</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erD9YTBibqNvibwp8mTWQMjgkenv0MWM1iaOhDiaC99noFm95UWISibzOgZf9kELlktJJcnvnXT9B24wRw/132" width="30px"><span>Yaxe</span> 👍（7） 💬（1）<div>昨天上github看cpp_study这个仓库的时候 发现头像莫名熟悉，才知道之前star的注释版nginx也是罗大写的  十分有缘 学习学习！</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/32/8d/91cd624b.jpg" width="30px"><span>幻境之桥</span> 👍（7） 💬（1）<div>在此基础上使用 clang-format 统一并减少大部分手工格式化的工作</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/85/c1/d94111b4.jpg" width="30px"><span>湫兮如风</span> 👍（5） 💬（2）<div>看完一节的内容一定一定要阅读大家的评论！罗老师这个专栏的氛围真好、质量真高!师生共进!</div>2020-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVAVOYIoohh3bCdgErne0VHtoPorcrtmOAR45rsWPmJsLkzlvqMulbRyv0Skj8JHajrA9bPia3Lxw/132" width="30px"><span>Geek_0315ca</span> 👍（5） 💬（1）<div>我比较喜欢变量名使用m和g前缀，说明变量的作用域范围；todo注释标注自己未实现的功能和想法💡 ；函数体内部使用空行分离不同的代码片段</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/9c/46/a2c1a99f.jpg" width="30px"><span>yelin</span> 👍（4） 💬（1）<div>特别喜欢匈牙利命名法里的类型前缀，不过现在使用的也基本就是m和g前缀了。我个人特别喜欢空格！很多CPP check，没有空格是会报错的，所以不能说习惯啦，这是规则。
</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/78/84e3433a.jpg" width="30px"><span>hb</span> 👍（4） 💬（1）<div>其实各个语言都有自己的code style， 例如OC就是习惯驼峰命名，基本不用加 &quot;_&quot;</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/75/7f76341b.jpg" width="30px"><span>c1rew</span> 👍（3） 💬（1）<div>代码统一规范，推荐一个工具，astyle，命令行或者vscode也有插件，大家提交代码前一键格式化，风格还可以根据配置自定义。</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/9f/bce7b518.jpg" width="30px"><span>虎皮青椒</span> 👍（3） 💬（1）<div>我觉得如果代码自己把自己写清楚了，比如清晰的布局，贴切的函数和变量名，适当的空行分割等等，注释就不必了。这是上策。

如果不行，那尽量写上规整周全的注释，帮助其他人维护。这是中策。

如果代码写得不行，注释也没有就太糟糕了。</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（2） 💬（1）<div>code style 从开始学写代码就注意起来了，之前看初学者的代码都是没有换行或者空格，真的读起来难受。优秀的代码都是可以阅读的，这种代码从结构到逻辑都是让人感觉眼前一亮，而不是一脸懵逼。
代码除了注释之外，我觉得会写log也比较重要，很多程序不仅仅是再运行前审查代码，还有就是出错时候返回来看代码，这时候你的code style和log里面的内容就为精确排查错误剩下一大笔时间！！！</div>2020-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（2） 💬（1）<div>我在实践中有几个疑惑，想请教一下老师：
1. 函数参数也是变量，该怎么命名能够直观地知道这个变量是入参，而不是局部变量？
2. 匈牙利命名法：string str_value;不是更能表示该变量是个字符串吗？
3. member fucntion要注释的话，建议采用单行&#47;&#47;……， 还是多行 &#47;* @param ……   @return…… *&#47;？</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/9c/46/a2c1a99f.jpg" width="30px"><span>yelin</span> 👍（2） 💬（2）<div>非常认同本文提到的很多观念啊，取百家之长，不过有些公司单位强制使用谷歌规范或者公司规范，对于这一类和自己理念冲突的问题，老师怎么解决</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（2） 💬（1）<div>There are 2 hard problems in computer science: cache invalidation, naming things, and off-by-1 errors.

团队英文水平有限，试过直接用中文来命名一些业务上较难翻译成英文或翻译后较繁琐的概念，用作变量名和函数名，反而没那么纠结，代码review或接手一看就懂</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c6/f1/aac154fe.jpg" width="30px"><span>wuwei</span> 👍（2） 💬（1）<div>留白的习惯我一直都有。命名倒是有点问题，member_function没有加m_的习惯。注释只做了代码说明和注释实验代码，文件开头、函数和类的说明一直没做，要改改了。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/80/e409fff6.jpg" width="30px"><span>Sochooligan</span> 👍（2） 💬（1）<div>还没看完，“20%的留白”，观点非常启发人。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/ae/3b101c00.jpg" width="30px"><span>fl260919784</span> 👍（2） 💬（1）<div>Facebook的命名方式也很赞，类JAVA风格；除了函数、变量、类的命名，还有文件夹、文件、namespace的命名也很重要</div>2020-05-09</li><br/><li><img src="" width="30px"><span>201201782</span> 👍（1） 💬（1）<div>留白确实是以前没怎么注意到的点，一开始以为公司不允许留白。。。感觉之后写代码一定要注意这个问题
注释里的TODO确实是非常重要，因为很多开发都是迭代式的，写在代码中也能保证以后能快速想起要做的关键事项，可以提升效率同时最重要的是尽早发现以及避免错误</div>2021-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/2c/06375913.jpg" width="30px"><span>宇天飞</span> 👍（1） 💬（1）<div>你用过哪些好的 code style，你最喜欢今天介绍的哪几条？
总则：“任何人都能写出机器能看懂的代码，但只有优秀的程序员才能写出人能看懂的代码。”，让我确定了要写达到什么目的。当人都能看懂的时候，bug有没有也很容易看出来。
1、用好空格和空行，多留白，让写代码就像写诗一样；让我坚定了code style的可践行性。
2、给变量、函数、类起个好名字，你的代码就成功了一半；code style非常简短，非常好。


注释在代码里通常的作用是“说明文档”，但它还有另外一个重要的用法，你知道吗？
1、多人协作
2、未来继续开发

评论区学到了：clang-format这个工具</div>2020-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/d5/b439fe35.jpg" width="30px"><span>ericluo</span> 👍（1） 💬（1）<div>很赞同留白的艺术
个人觉得留白主用于分割逻辑段，让别人或自己去阅读时不会那个累，逻辑也很容易理解</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/bc/791d0f5e.jpg" width="30px"><span>杜现有</span> 👍（1） 💬（3）<div>我对大括号用法有个疑惑，以前写C的时候，都是上下对称的写法，如下，
if(xx)
{

}
但是看java代码大部分人都是下面这样的，
if(xx){

}
感觉还是上面的看着舒服一些，下面这种用法有啥好处呢？是为了节省空间？</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4d/0b/ac1f7fec.jpg" width="30px"><span>章大蒜📍</span> 👍（1） 💬（1）<div>修改代码时要更新注释，不要出现牛头不对马嘴的情况，很容易误导别人，时间长了甚至自己都会被误导</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/93/af/54e2a654.jpg" width="30px"><span>无为而立</span> 👍（1） 💬（1）<div>我的code style和老师说的几乎一样，类用驼峰，变量和函数名用snake case。就是感觉注释说明有时候写的不好。</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/ee/33ef689b.jpg" width="30px"><span>土土人</span> 👍（1） 💬（1）<div>关于文件名的规范有没有什么建议呀？</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/39/85/c6110f83.jpg" width="30px"><span>黄骏</span> 👍（1） 💬（1）<div>觉得linux内核的代码注释值得学习，很详细。工作中读了一些开源代码，读注释少的代码会很痛苦，比如，ceph，哈哈</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/71/4f/bce0d5bc.jpg" width="30px"><span>哈哈</span> 👍（1） 💬（1）<div>喜欢老师说的写好注释应该换位思考。

还有就是我觉得团队英语水平不行时候还是应该写汉字注释，要比蹩脚的英文注释更好一些。

网上还有种说法是，不要留注释的代码，一是交给git来管理历史，这样文件更干净；
另外是过几天返回来看注释掉的代码可能有更简洁的实现，而不是放开原来的注释</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d6/67/5e0cac1b.jpg" width="30px"><span>Tedeer</span> 👍（1） 💬（2）<div>用过较好的codestyle是《阿里java开发手册》中的介绍，vscode中prettier代码格式化工具，最喜欢今天介绍留白（清爽）和命名，以前在开发中遇到过long a = 10l的情况，被坑了。我觉得注释写的好也是代码协同者的交流语言，节约时间成本。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/48/2d/1c05cf04.jpg" width="30px"><span>William Wang</span> 👍（0） 💬（1）<div>P1:
在过去工作的过程中我主要使用google code style进行代码的编写，但是其中也有一些问题，比如类的数据成名命名使用名字+_的方式，有点过于奇怪，所以我还是习惯使用m_名字来对类的成员函数命名。
P2:
注释除了作为函数和代码的解释，还有备注的作用，比如使用todo来提醒开发人员还有哪些地方没有做，或者fix来表示哪部分代码有bug需要修理，使用不同的关键字来做不同类型的备注。</div>2024-10-23</li><br/>
</ul>