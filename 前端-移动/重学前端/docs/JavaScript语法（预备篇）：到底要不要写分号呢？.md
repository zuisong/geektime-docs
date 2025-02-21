你好，我是winter。

在我们介绍JavaScript语法的全局结构之前，我们先要探讨一个语言风格问题：究竟要不要写分号。

这是一个非常经典的口水问题，“加分号”党和“不写分号”党之间的战争，可谓是经久不息。

实际上，行尾使用分号的风格来自于Java，也来自于C语言和C++，这一设计最初是为了降低编译器的工作负担。

但是，从今天的角度来看，行尾使用分号其实是一种语法噪音，恰好JavaScript语言又提供了相对可用的分号自动补全规则，所以，很多JavaScript的程序员都是倾向于不写分号。

这里要特意说一点，在今天的文章中，我并不希望去售卖自己的观点（其实我是属于“加分号”党），而是希望比较中立地给你讲清楚相关的知识，让你具备足够的判断力。

我们首先来了解一下自动插入分号的规则。

## 自动插入分号规则

自动插入分号规则其实独立于所有的语法产生式定义，它的规则说起来非常简单，只有三条。

- 要有换行符，且下一个符号是不符合语法的，那么就尝试插入分号。
- 有换行符，且语法中规定此处不能有换行符，那么就自动插入分号。
- 源代码结束处，不能形成完整的脚本或者模块结构，那么就自动插入分号。

这样描述是比较难以理解的，我们一起看一些实际的例子进行分析：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/17/a5/7a0cbb55.jpg" width="30px"><span>本末倒置っ</span> 👍（107） 💬（6）<div>几年前，各种各样的书大致上都推荐你加分号。
几年前，曾经由于构建工具有一些问题，导致不加分号可能会出问题。
jquery依然留着分号，vue源码不用分号。

尤雨溪曾经在知乎说：真正会导致上下行解析出问题的 token 有 5 个：括号，方括号，正则开头的斜杠，加号，减号。我还从没见过实际代码中用正则、加号、减号作为行首的情况，所以总结下来就是一句话：一行开头是括号或者方括号的时候加上分号就可以了，其他时候全部不需要。
哦当然再加个反引号。

可是写分号已经习惯了，又何必花力气改习惯去掉它。不加只要不写出bug，也很好。
反正分号有和没有，对eslint fix来说，只是瞬间的事。。。</div>2019-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ26xdibLibk37rdrIA3zStsayOo9b0SGiasibNGfic6n2EIJiba1ptZOtWqV797wkszdjDM8aQkz1A2vibw/132" width="30px"><span>jacklovepdf</span> 👍（21） 💬（5）<div>总结一下，不加分号可能会有问题，加分号一定不会有问题。那为什么不加?</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（14） 💬（1）<div>写了几年一直不写分号。。。等出了问题再说吧。。。我懒。。</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/10/fb/c054968d.jpg" width="30px"><span>Rock</span> 👍（12） 💬（2）<div>一直有加分号的习惯，一是不写分号我有强迫症，二是不写分号webstorm会提示</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（7） 💬（3）<div>另外我个人也是不写分号，然后使用的是双引号，诸位不写分号党，如果想要写上分号，用的eslint和vs code那么可以这么搞：
1. eslintrc中加入这条规则：&quot;semi&quot;: [&quot;error&quot;, &quot;always&quot;]
2. vsc中设置一下：&quot;eslint.autoFixOnSave&quot;: true
此时，你保存的时候，vsc会自动帮你在需要加分号的地方加上分号</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/e6/2cff4a89.jpg" width="30px"><span>醉月</span> 👍（7） 💬（0）<div>用了cli写vue以后就很少用分号了
以前学js写原生的时候强迫症一样写分号
这东西就是见仁见智
前端真的是娱乐圈，，
为个分号还能争起来。</div>2019-03-25</li><br/><li><img src="" width="30px"><span>Dylan-Tseng</span> 👍（7） 💬（0）<div>个人觉得还是加分号比较好，至少能保证加上去之后今天老师说的问题都能够得到我们想要的答案。</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/3a/2f/70c1007f.jpg" width="30px"><span>梦星魂</span> 👍（5） 💬（0）<div>加封号更好看一点，更有终止感。而且能明显和if else 这样的语句区分开来。</div>2020-07-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDSY5xBJ2PH4lqNtWJqhe1HcYkP7S9ibAXChONgCBX5pJ2gaU3icXhltQgqhzDyML3EzFicxPeE4Tiag/132" width="30px"><span>Geek_0bb537</span> 👍（5） 💬（0）<div>自动补齐和自动驾驶一样 不特么靠谱！稳妥点 养成写分号的习惯！</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/eb/7e6898af.jpg" width="30px"><span>行则将至</span> 👍（4） 💬（0）<div>采用eslint是不会写的，不采用会写上</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/f7/1150bedc.jpg" width="30px"><span>陆同春</span> 👍（3） 💬（0）<div>react源码规范需要分号</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/72/31/06f8ada8.jpg" width="30px"><span>WoodyYip鲜森</span> 👍（2） 💬（0）<div>同意winter老师的观点，除非团队每位成员永远都是高水平的存在，否则我们就不能自己想当然，因为自己知道特殊情况不代表所有人都知道，不代表所有人都不会出上述不抛错的隐匿bug，工程化的时候要考虑团队所有人的平均水平，我们庙小，团队技术水平不高，而且有时也会有新人，所以我们还是倾向于约定俗成要求大家养成靠自己加分号的好习惯，虽然我们的eslint也配成了需要加分号，但这只是辅助手段，很容易就能想到，假如eslint都能正确插入分号，浏览器肯定也能，反之，如果像老师所说的会出问题的地方，eslint同样会抓瞎。 </div>2021-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/73/317ea03c.jpg" width="30px"><span>joker</span> 👍（2） 💬（0）<div>现在的编程环境根本不需要担心。格式代码化或eslint 都可以避免这些问题。</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（2） 💬（0）<div>写了几年一直不写分号。。。等出了问题再说吧。。。我懒。。</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7a/aa/a90ec203.jpg" width="30px"><span>四叶草</span> 👍（2） 💬（1）<div>启用了eslint检查都会要把分号去掉，这样编译后不是可能有问题？</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/dd/5a482cab.jpg" width="30px"><span>杜森垚</span> 👍（1） 💬（0）<div>不写分号需要注意的情况，第三种，以正则表达式开头的语句，那个例子会报错，正则的第一个斜杠被理解成除号，后面小括号中的a，会被理解为普通标识符，会报： a is not defined</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/22/dd505e6d.jpg" width="30px"><span>Yully</span> 👍（1） 💬（0）<div>vue没有分号，react有分号。对于是不是加分号，个人服从集体，代码服从项目，主要看项目的eslint配置，如果项目中设置的有分号，那就加，如果没有分号，那就不加。可无缝切换。主要还是项目的代码风格统一。</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/1c/2a78a51a.jpg" width="30px"><span>千虑必有一得</span> 👍（1） 💬（0）<div>swift中不写分号，到了js自然也习惯不写分号</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/57/ce27b9ad.jpg" width="30px"><span>昔忆落落</span> 👍（1） 💬（0）<div>感觉加分号好看一点，读起来也方便一点，所以一直保留着加分号的习惯</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/c7/cb93c786.jpg" width="30px"><span>Ranjay</span> 👍（1） 💬（0）<div>eslint是你自己配置的。。。</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d1/97/3abdd9cd.jpg" width="30px"><span>stanny</span> 👍（1） 💬（0）<div>antd源码有分号  两个空格缩进</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d1/97/3abdd9cd.jpg" width="30px"><span>stanny</span> 👍（1） 💬（0）<div>koa源码有分号</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/07/36/d677e741.jpg" width="30px"><span>黑山老妖</span> 👍（0） 💬（0）<div>真正会导致上下行解析出问题的 token 有 5 个：括号，方括号，正则开头的斜杠，加号，减号。</div>2022-11-27</li><br/><li><img src="" width="30px"><span>程序员讲道理</span> 👍（0） 💬（0）<div>我是不加分号党。如果某些情况不加分号有问题，为什么不去设置编辑工具、流水线的警告，而是要求所有的都要加上分号？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/dd/970e7b4a.jpg" width="30px"><span>锐锐爱南球</span> 👍（0） 💬（0）<div>最新版的JavaScript权威指南和JavaScript高级程序设计都建议能加分号就尽量加，然后自己也一直都是加分号的，习惯了</div>2022-03-29</li><br/><li><img src="" width="30px"><span>程序员讲道理</span> 👍（0） 💬（0）<div>如果不加分号，可能会有问题，那么可以配置插件检测出来。

如果能检测出来，为什么不直接在编译时直接插入分号？</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/65/69/5681895c.jpg" width="30px"><span>樱桃dady</span> 👍（0） 💬（0）<div>if(&#39;a&#39;) console.log(&#39;a&#39;);else console.log(&#39;b&#39;);</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/84/bda2b034.jpg" width="30px"><span>aaron</span> 👍（0） 💬（0）<div>就为这事我还傻呵呵的去尤大知乎去问了，虽然第二天就删了，哈哈，我还是加了分号</div>2021-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/1e/a2/083412c6.jpg" width="30px"><span>疯羊先生</span> 👍（0） 💬（0）<div>对于不加分号，JS机制本身就不能完美处理，所以不加分号的人士只能自动严格要求代码不能出现非法情况。不过重点是加个分号怎么了，手更容易累？影响性能了？恐怕影响的只有某种美观不美观吧，我认为加分号非常符合自然语言的感觉，我还是喜欢自然的，就像难以想象书面语言没有句号一样。</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8d/0e/5e97bbef.jpg" width="30px"><span>半橙汁</span> 👍（0） 💬（0）<div>单双引号同样会引发一些的问题，没有约束的情况下单双混搭的代码格式真的会令人发狂~</div>2020-10-24</li><br/>
</ul>