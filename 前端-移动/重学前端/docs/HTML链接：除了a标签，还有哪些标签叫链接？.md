你好，我是winter。

在前面的课程中，我讲到了HTML的语义和元信息标签，今天这一课，我们来讲另一类HTML元素：链接。

链接这种元素可以说是占据了整个互联网。也正是因为无处不在的超链接，才让我们的万维网如此繁荣。没有了超链接的HTML，最多可以称为富文本，没法称作超文本（hyper text）。

我想，作为互联网从业者，我们一定对链接都非常熟悉了。链接能够帮助我们从一个网页跳转到另一个网页。

不过，除了肉眼可见的这些链接，其实HTML里面还规定了一些不可见链接的类型，这节课，我就来给你介绍链接家族的全员，让你对它们有一个完整的认识。

链接是HTML中的一种机制，它是HTML文档和其它文档或者资源的连接关系，在HTML中，链接有两种类型。一种是超链接型标签，一种是外部资源链接。

链接的家族中有a标签、area标签和link标签。今天，我会逐一对它们进行介绍。

![](https://static001.geekbang.org/resource/image/ca/51/caab7832c425b3af2b3adae747e6f551.png?wh=702%2A1100)

## link 标签

提到链接，我们都知道a标签可以成为超链接，但是我们今天的内容，要从一个大家不太熟悉的标签开始，也就是link标签。

我们已经介绍过元信息类标签。实际上，我们并没有介绍完全，有些link标签也是元信息类标签的一种。

我们已经讲过，HTML标准并没有规定浏览器如何使用元信息，我们还讲到了元信息中有不少是被设计成“无需被浏览器识别，而是专门用于搜索引擎看的”。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（0） 💬（2）<div>&quot;opener 打开的网页可以使用 window.opener 来访问当前页面的 window 对象，这是 a 标签的默认行为。&quot;   
老师，这句话没看明白， opener 是需要和 window.open 方法配合使用的，这个和 a 标签有什么关系呢？</div>2019-07-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kB4swUuCyMiciaFuXxnUx2VFurJ0gvxkRlwSuHP85nQDzyGT2EyTiaoYF3Jia3ufecH0dYrWMIuIPbDE9MfKooVpDA/132" width="30px"><span>心雨</span> 👍（86） 💬（1）<div>有很多链接类型都没有用过,老师就这样点到为止我们也不知道能用来干什么,如果您能举例说平时哪些场景用哪些标签更好,这样就不会过目就忘,也容易理解记忆,在工作中也能有很大帮助,这样也能帮助我们买了课程的这些小伙伴省很多时间.</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/ae/6d8c3c4f.jpg" width="30px"><span>cmyh</span> 👍（25） 💬（0）<div>老师您好，我有几点困惑，望您能指点迷津
1.基本数据类型存放于栈空间中，对象存放于堆空间中，堆空间在内存里的存放是以链表的形式吗，物理地址不连续，但是逻辑地址是连续的？
2.声明一个基本数据类型，存放于栈空间，但是使用的时候，又把它进行一次对象的转化，例如：var a=&quot;1&quot;，实际操作的时候它又创建了一个String对象，那么这个基本数据类型a字符串_去哪了，它就没有用了吗？
3.JavaScript中的null，是一个值还是一个地址，如果是值的话，那null是否有很多个，是地址的话，那说明null是指向一个唯一的一个地方？
4.原型链中的prototype和__proto__，它们是指针吗，我认为它是指针，但是有前端小伙伴说它是一块连续的空间，每次声明一个变量都从object开始开辟一整套的空间，也就是说堆空间中可能会有很多的object
5.最后一个问题是js垃圾回收机制标记清除算法中，它说从根节点出发进行可达节点遍历标记，那么这个根节点是从什么地方开始呢？是从全局的window或者global出发吗？如果null是一个唯一的空间，那么清除一个对象其实是把对象的值指向这块空间吗？</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/11/5c/9f6827cc.jpg" width="30px"><span>以勒</span> 👍（15） 💬（0）<div>link主要用来引入外部静态资源 和 记录标记页面的元信息帮助浏览器优化

a 主要用在 页面内可见的 超链接

area + map 用在 一张图片中部分区域需要做跳转时的情况。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（13） 💬（4）<div>服了！
我能说我之前听都没听说过area和map标签吗...
真没想到小小链接竟然有这么多学问...
且不说用不用得到，对整个知识体系有了一定的认识和了解。
winter老师的课从来都是点到为止，而不是把所有东西都告诉我们。我们有了方向，就不怕迷路，自然胸有成竹。</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/fc/0b324280.jpg" width="30px"><span>Semantha</span> 👍（8） 💬（1）<div>自从用了vue，项目中貌似没用过链接标签</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/19/69f6e2ec.jpg" width="30px"><span>王大可</span> 👍（6） 💬（0）<div>记得早年都是使用dreamweaver生成area和map代码，然后用在淘宝店铺上</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/ca/9661e38f.jpg" width="30px"><span>王文银</span> 👍（4） 💬（0）<div>作为一个菜鸟，平时只用到了link
链接样式和a标签跳转😂 😂 😂 </div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AcJM5WNhE05rzaVzeL9ia4QSnibd0ibbKNdIbySj2ibhj2xFRHibdhOX9fBEB5HMS1bbOt0tXcxwKur2gPdVaZpcIZw/132" width="30px"><span>子非鱼</span> 👍（3） 💬（0）<div>项目中使用了modulepreload，效果还是挺明显的</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（3） 💬（0）<div>我好像只用过引入css标签，，。感觉自己菜到抠脚</div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ26xdibLibk37rdrIA3zStsayOo9b0SGiasibNGfic6n2EIJiba1ptZOtWqV797wkszdjDM8aQkz1A2vibw/132" width="30px"><span>jacklovepdf</span> 👍（2） 💬（0）<div>把链接分为超链接类和外部资源类是作者自己的理解么，还是官方有这种分类呀，我没找到。</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/41/a5/16c615cc.jpg" width="30px"><span>乃乎</span> 👍（2） 💬（0）<div>加一个 manifest 吧</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/78/a9/d0209735.jpg" width="30px"><span>海的对岸</span> 👍（0） 💬（0）<div>以前玩dw的时候，有个工具，就是在图片上画圆，然后给这个圆设置属性，现在想来，应该就是area标签了。然后真的从事前端行业，基本开发都是vscode，从来都不用dw</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/0c/bcd2b32b.jpg" width="30px"><span>青鸟</span> 👍（0） 💬（0）<div>HTML的链接，要么就是常用的要么就是索性不用，那么对于不用的只是暂时的，例如map和area配合，不是特定情况是不需要考虑的。
area标签和a标签中的coords属性语义是一样的吗？
为什么HTML5不支持a标签中的coords属性呢？</div>2020-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDSY5xBJ2PH4lqNtWJqhe1HcYkP7S9ibAXChONgCBX5pJ2gaU3icXhltQgqhzDyML3EzFicxPeE4Tiag/132" width="30px"><span>Geek_0bb537</span> 👍（0） 💬（1）<div>link预加载是开启单独一个线程加载的还是跟其它普通link一起排队一个一个加载</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/29/6fbe6d66.jpg" width="30px"><span>Mr.杨</span> 👍（0） 💬（0）<div>area可以在项目太紧的情况下用，不过不推荐用</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/f5/6821ac5f.jpg" width="30px"><span>ezra.xu</span> 👍（0） 💬（0）<div>请问老师，页面资源的预加载是不是可以用link标签实现，还有其他的方式吗？</div>2019-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/13/3e/f350a41b.jpg" width="30px"><span>田野的嘴好冰</span> 👍（0） 💬（0）<div>area没听说过，link方便搜索之类的也是第一次听说，还有a标签的rel 属性也是第一次看全</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/db/4e658ce8.jpg" width="30px"><span>继业(Adrian)</span> 👍（0） 💬（0）<div>感谢作者。提神醒脑</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/4b/7ccd2499.jpg" width="30px"><span>F.</span> 👍（0） 💬（0）<div>老师， script 标签算不算半个链接标签呢</div>2019-03-15</li><br/><li><img src="" width="30px"><span>fape</span> 👍（0） 💬（0）<div>想起table时代用Dreamweaver可以在img上画热区能生成area，现在也就地图用这个标签了吧？
使用link预加载感觉很有用，老师能结合实例多讲讲吗？</div>2019-03-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（0） 💬（0）<div>好多标签听都没停过，我感觉我只用到了html的一个子集</div>2019-03-12</li><br/>
</ul>