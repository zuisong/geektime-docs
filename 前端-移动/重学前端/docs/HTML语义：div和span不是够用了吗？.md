你好，我是winter。

今天这篇是我们正式开篇的第一篇文章，我想和你聊聊HTML。

我猜屏幕那一边的你估计会说：“HTML我很熟悉了，每天写，这不是初级程序员才学的内容么，这我还能不会吗？”

其实在我看来，HTML并不简单，它是典型的“入门容易，精通困难”的一部分知识。深刻理解HTML是成为优秀的前端工程师重要的一步。

我们在上一篇文章中讲到了，HTML的标签可以分为很多种，比如head里面的元信息类标签，又比如img、video、audio之类的替换型媒体标签。我今天要讲的标签是：语义类标签。

## 语义类标签是什么，使用它有什么好处？

语义类标签也是大家工作中经常会用到的一类标签，它们的特点是视觉表现上互相都差不多，主要的区别在于它们表示了不同的语义，比如大家会经常见到的section、nav、p，这些都是语义类的标签。

语义是我们说话表达的意思，多数的语义实际上都是由文字来承载的。语义类标签则是纯文字的补充，比如标题、自然段、章节、列表，这些内容都是纯文字无法表达的，我们需要依靠语义标签代为表达。

在讲语义之前，我们来说说为什么要用语义。

现在我们很多的前端工程师写起代码来，多数都不用复杂的语义标签， 只靠div 和 span 就能走天下了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（74） 💬（1）<div>老师也有看炮姐吗？(〃•⊖•〃)</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（42） 💬（7）<div>我们是做业务系统的，团队中有一个同事（纯前端偏UI）特别喜欢使用语义化标签，但是我们在维护他的代码时总感觉他的代码乱糟糟的不好维护，很多样式就直接写标签来定义；而我们其他人（擅长做后台的）则喜欢用div，然后通过有业务含义的class来定义样式。
个人觉得做业务系统，特别是团队一起协作开发，还是尽量少用语义化标签，这样能减少后期维护的成本。</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/37/68/b37d27f6.jpg" width="30px"><span>Mowtwo</span> 👍（19） 💬（2）<div>虽然文章确实讲了很多有用的东西，但是对于hgroup的例子我觉得还是可以得到一些指正。
至少到目前为止，我尝试了一下，hgroup已经不再可以在网页上有人和作用了...而我搜索以后，也找到了一篇关于hgroup已经在HTML5.1标准下被取消的信息。所以文章中所提出的部分内容已经不再有效，希望重视。</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/0f/9c572b5e.jpg" width="30px"><span>@Listener</span> 👍（5） 💬（1）<div>老师，看了之后有几个问题：
1. 我看到有的语义化文章说的一个页面最好只有一个h1标签，所以一般除了页面的主标题之外通常我都会用h2-h6去做，不知道这样用对不对？
2. article和section嵌套的正确使用方式是什么，用于页面布局是不是一般不用article？
3. 日常我们的页面都是软件界面类的，是不是没必要用这些复杂的语义化标签？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ff/1f/4f927519.jpg" width="30px"><span>渭河</span> 👍（4） 💬（1）<div> &lt;hgroup&gt;&lt;h1&gt;今天吃什么&lt;&#47;h1&gt;&lt;h2&gt;吃肉&lt;&#47;h2&gt;&lt;&#47;hgroup&gt;
 
为什么写出来没有出现和老师一样的效果
我这么写还是分成两行
和用hgroup包裹前没区别</div>2019-02-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlgFmOLogkNRwKVyYbNzu79k2Y8k9d3AEiaIDmQWI3c7YNEw1RYPGmQteibthXTnwoSqBj0aibZhmfw/132" width="30px"><span>吴前端</span> 👍（3） 💬（1）<div>老师 我想问个具体问题 图文列表用section来划分的话算正确使用嘛 正确的话 列表标题必须用h1嘛</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（2） 💬（2）<div>读的人水平一般, </div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/8c/d91b01a6.jpg" width="30px"><span>zhangbao</span> 👍（2） 💬（1）<div>老师，您好。关于“给所有并列关系的元素都套上 ul”的误用情况，我有点疑惑，希望得到老师的解答。

1. 

我现在使用 ul 的地方：网站导航栏，网页底部的相关链接部分还有文章侧边栏的相关文章部分。

我是否误用了呢？

2. 

老师您说的“如果所有并列关系都用 ul，会造成大量冗余标签”，是不是比如下面的例子

···
&lt;nav&gt;
  &lt;ul&gt;
    &lt;li&gt;&lt;a href=&quot;...&quot;&gt;...&lt;a&gt;&lt;&#47;li&gt;
    ...
  &lt;&#47;ul&gt;
&lt;nav&gt;
···

就是冗余了，本来可以写成

···
&lt;nav&gt;
  &lt;a href=&quot;...&quot;&gt;...&lt;a&gt;
  ...
&lt;nav&gt;
···

不知道我这样理解对吗？



</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/0d/caab8ba1.jpg" width="30px"><span>孤独的二向箔</span> 👍（1） 💬（1）<div>「还有一种情况是，HTML 的有些标签实际上就是必要的，甚至必要的程度可以达到：如果没有这个标签，文字会产生歧义的程度。」
反对winter大大这句话，我钻下牛角尖，实际上并不是必要的。比如温大的例子，用&lt;div class=&quot;em&quot;&gt;&lt;&#47;div&gt;也是可以的。

我觉得语义标签用途的本质是「简化和统一了（一种特定用途的标签的）表达方式」。

比如&lt;div class=&quot;emphasis&quot;&gt;xxx&lt;&#47;div&gt; 这个也能表示&lt;em&gt;的含义，但是由于每个人对同一种用途的标签，用class会有不同的表述方式，比如小明就写&lt;div class=&quot;highlight&quot;&gt;xxx&lt;&#47;div&gt;。如此一来，当其他人来理解你这段代码的含义时，认知成本就会提高，机器就更难理解了。

从上面这个例子，简化在于em 比 class=&quot;highlight&quot; 更简单；统一在于消除了不同人不同的表达方式，这样更有利于人和机器的阅读。

而方便了机器的阅读，还可以获得一些好处：
1.生成目录
2.SEO优化

所以，遇到用语义标签的时候，一定用语义标签，至少为了SEO吧:D</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f4/0d/827a3541.jpg" width="30px"><span>是方旭啊</span> 👍（1） 💬（1）<div>1、footer 也可以和 aside , nav , section 相关联（header 不存在关联问题）
2、address 明确地只关联到 article 和 body。
这两句话中的关联，具体指的是什么？有点不太理解，望解答。</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/61/aa/4d1e4085.jpg" width="30px"><span>metthew😀</span> 👍（0） 💬（1）<div>em 标签告诉浏览器把其中文本表示强调，strong 告诉用户加强语气
section用的比较广泛</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a6/ac/1b3ea381.jpg" width="30px"><span>青云</span> 👍（0） 💬（2）<div>em和strong的区别，我百度了一下就是‘强调’和‘更强烈的强调’区别？？？</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/0a/07844962.jpg" width="30px"><span>梦丹</span> 👍（0） 💬（1）<div>工作中遇到一个问题：引入icon图标的时候可以使用i标签，也可以使用span，使用的时候他们两个有性能上的区分吗</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/cc/b6/b1137e76.jpg" width="30px"><span>阿诺韩·史瓦辛倩</span> 👍（0） 💬（1）<div>老师您好，感觉您说的。。。都对，只是觉得您针对这部分知识的讲解出发点是什么呢？为了让大家养成好习惯还是针对seo比较友好，如果是针对seo友好的话，确实觉得这部分都是说友好，但是怎么友好我们就不知道了，用的时候就比较被动。希望老师解惑</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ff/4f/df4027ba.jpg" width="30px"><span>清原小宁</span> 👍（0） 💬（1）<div>之前我也追求语义化的，但现在看有些ul，em可能用的不恰当。不过我之前我参加峰会的时候，听过一个盲人讲如何用读屏软件来上网，所以我想我们还是应该有些语义化的，那现在流行的react怎么语义呢</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/de/086971ba.jpg" width="30px"><span>y.c</span> 👍（0） 💬（1）<div>嗯 这么说吧 假设页面只有一个大主题，再细分几个小标题，
&lt;main&gt;
        &lt;h1&gt;一级标题&lt;&#47;h1&gt;
        &lt;section&gt;
            &lt;h1&gt;二级标题&lt;&#47;h1&gt;
            &lt;section&gt;
                &lt;h1&gt;三级标题&lt;&#47;h1&gt;
            &lt;&#47;section&gt;
        &lt;&#47;section&gt;
    &lt;&#47;main&gt;
您的意思应该是这样写吧？百度和谷歌能否支持这种写法？因为对于他们来说h1后面跟h2，h2后面再跟h3才是正确的吧
</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0f/de/086971ba.jpg" width="30px"><span>y.c</span> 👍（0） 💬（1）<div>语义化标签更多是用在需要SEO的网站，但是文中说的“section 的嵌套会使得其中的 h1-h6 下降一级”，然后代码中出现多个H1，一个页面不是应该至多一个h1吗？您这种写法会不会影响到优化</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fa/8c/af35dd30.jpg" width="30px"><span>Shmily</span> 👍（0） 💬（1）<div>语义是只是为了方便开发阅读和浏览器渲染吗？执行了一下文章中的代码，发现展示效果没什么区别</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/43/b6/69ded917.jpg" width="30px"><span>milanaries</span> 👍（0） 💬（1）<div>老师 不打算讲一下 关于http相关的知识点吗？</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/11/94/016f470a.jpg" width="30px"><span>ZainYi</span> 👍（0） 💬（1）<div>怎么看 dl dd dt，一些自定义列表里面，我常使用这组标签</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/62/28cf26d4.jpg" width="30px"><span>韩风枫</span> 👍（0） 💬（1）<div>aside 和 header 中都可能出现导航（nav 标签），二者的区别是，header 中的导航多数是到文章自己的目录，而 aside 中的导航多数是到关联页面或者是整站地图。我觉得这里不对，或者说正好相反，header中的导航是整站地图，aside中是文章目录，具体参照vue，react，antd，echarts都是类似的结构。</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/ea/16291abc.jpg" width="30px"><span>better man</span> 👍（0） 💬（1）<div>表达一定的结构的场景，和Ruby的例子有什么关系？没看懂٩😐ི۶</div>2019-01-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Zb5XAibrJOtgL4EMIhUu8CL0Cwf6BoZHau7n03LK91BTswcBicU8K8wlO79Q9YGAy593fYofe08ymuiaYxxibsBMYQ/132" width="30px"><span>武瑶</span> 👍（0） 💬（1）<div>今天我吃了一个苹果。这个谁看懂了？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/6a/b6f6810c.jpg" width="30px"><span>简单</span> 👍（0） 💬（1）<div>实际开发中没有很刻意使用语义标签，都是div解决😂不过觉得用了语义标签可以使代码结构没那么单一。老师在说到h1标题标签的时候，想到这些标签都自带了样式，但是有时候开发会把样式清除掉，那清除样式不是跟普通div标签一样了吗？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/00/62/7df9bb08.jpg" width="30px"><span>Icobe</span> 👍（0） 💬（1）<div>有些标签都没见过，请问老师那些网站能看到比较全的，有比较紧跟更新步伐的手册可以查询？w3c吗？
</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/96/e051b906.jpg" width="30px"><span>Storm</span> 👍（0） 💬（1）<div>语义化很多时候都是考虑设备功能简陋的情况，比如没有css的情况下，还要展示个结构啦什么的。。就现在这个趋势，根本没必要考虑这个，还有什么针对盲人友好之类的，如果不是你的目标客户，做这些只是增加无谓的工作量而已。多数时候所谓的语义化并没有用，还不如干脆放开结合使用xml标准，在xml标准内，除了文档特定意义的标签比如head,body,a,form...，你愿意定义什么标签就定义什么标签；比如address这种标签，我用&lt;addr&gt;&lt;&#47;addr&gt;也能表示。</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2b/d6/945f0d82.jpg" width="30px"><span>_(:з」∠)_</span> 👍（0） 💬（1）<div>版权信息应该怎么写？代表了什么含义？我国有相应的规定吗？国际标准有相应的规定吗？</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（142） 💬（3）<div>我写前端时间不长，写的都是小东西，确实觉得div和span够用

我认为html标签和自然语言的演化肯定会是一种逻辑：

汉语中「地」「的」「得」的正确用法今天大部分中国人根本不会，都只用「的」字，也不影响表达。另外很多字的读音标准都变了，英语也有类似的历史，都是人民的选择成了标准

所以我的观点是：html也一样，设计者的初衷有他自己的思考，但最后开发者的习惯会成为标准（微信小程序最基本的标签不就是view和text嘛），除非这些标签会影响人数更广大的普通用户</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/30/4a/bcc3f82a.jpg" width="30px"><span>人艰不拆</span> 👍（106） 💬（4）<div>老夫写页面就是一把梭，div，div，div，什么都是div，display改一改什么都能写</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/13/d720d077.jpg" width="30px"><span>馒头小哥</span> 👍（64） 💬（2）<div>其实语义化更重要的是在于规范，渲染出来的网页是给大多数用户看的。还有一小部分用户比如 程序员、机器人、视障用户。

如果一个页面只有 span 和 div，视障软件如果把这个网页读给用户？ 读 “ div 开始 class=&quot;tile&quot; 今天天气很好 div 结束” 还是读 “标题：今天天气很好” 那个方式更好呢？

就好比家里的排插，有做得精致美观的、也有简约朴素的，但是大家都是遵循统一插座规范，所以都能正常插上家电使用。

无规矩不成方圆，语义化能更好的帮助到这些用户去读取、去认知、去使用，这是我所理解的语义化好处。</div>2019-01-22</li><br/>
</ul>