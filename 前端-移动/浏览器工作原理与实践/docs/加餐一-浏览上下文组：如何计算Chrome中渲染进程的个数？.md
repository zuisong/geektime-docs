你好，我是李兵。

在留言区，经常有朋友问到如何计算Chrome中渲染进程个数的问题，那么今天我就来完整地解答这个问题。

在前面“[04 | 导航流程](https://time.geekbang.org/column/article/117637)”这一讲中我们介绍过了，在默认情况下，如果打开一个标签页，那么浏览器会默认为其创建一个渲染进程。不过我们在“[04 | 导航流程](https://time.geekbang.org/column/article/117637)”中还介绍了同一站点的概念，如果从一个标签页中打开了另一个新标签页，当新标签页和当前标签页属于同一站点的话，那么新标签页会复用当前标签页的渲染进程。

具体地讲，如果我从极客邦(www.geekbang.org) 的标签页中打开新的极客时间(time.geekbang.org) 标签页，由于这两个标签页属于同一站点(相同协议、相同根域名)，所以他们会共用同一个渲染进程。你可以看下面这张Chrome的任务管理器截图：

![](https://static001.geekbang.org/resource/image/f8/5c/f87168a79df0b87a08b243937f53545c.png?wh=1540%2A712)

多个标签页运行在同一个渲染进程

观察上图，我们可以看到，极客邦官网和极客时间标签页都共用同一个渲染进程，该进程ID是84748。

不过如果我们分别打开这两个标签页，比如先打开极客邦的标签页，然后再新建一个标签页，再在这个新标签页中打开极客时间，这时候我们可以看到这两个标签页分别使用了两个不同的渲染进程。你可以参看下图：

![](https://static001.geekbang.org/resource/image/34/f9/34815ee3a8d5057d39ebb6f871fbf0f9.jpg?wh=4752%2A2973)

多个标签页运行在不同的渲染进程中
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJS0jwYKhjm1hq96go05J4R7XDd5FFXXaoyIfX9TgoI3mLURAu2ET72SvYGM2iaET7IV3WDvMibAVfw/132" width="30px"><span>tokey</span> 👍（74） 💬（2）<div>老师，阿里为什么要把同一站点的tab签做成无连接的，会避免什么安全隐患啊？</div>2019-11-20</li><br/><li><img src="" width="30px"><span>Geek_177f82</span> 👍（43） 💬（3）<div>老师之前知否自己出过课程？或者书籍，博客之类的。希望老师提供下。
</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（23） 💬（1）<div>同源要求协议、域名以及端口均一样才行；同一站点只要求协议，根域名相同即可。也就是同源的要求太严格，导致复用同一渲染进程的条件比较难满足，所有条件放宽至同一站点？</div>2019-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/D5lTKlxYlRfWBl8ye0JvdfmVo0Ykibt7QhDf1A3g8L66lL36xFkHKUIicCia8dz2Y2mU5qG1OJLdfOvQSoD6svib2Q/132" width="30px"><span>Geek_259055</span> 👍（8） 💬（3）<div>老师期待你的Proformance加餐哦</div>2019-11-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJXFU47jt2Phr9DAlzyZyKSA5oDEiaiaBsaLUoVQfBEic9ON6vOrO4NJL7icq7QIFje5DV2IBFJDGbTicg/132" width="30px"><span>梦已沉沦</span> 👍（3） 💬（1）<div>是不是在多标签页时，同一站点比同源能有效节约进程</div>2019-11-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSGtKFrlXheKwAse0KO8lz9r8nj6AHibmSetJ4natNicUwNTp78nm9aMibPcibCn9qxmK9MxKMeQ1mRg/0" width="30px"><span>冯建俊</span> 👍（0） 💬（4）<div>我用的搜索引擎是必应：
搜索瓜子二手车 -&gt; 点击跳转到瓜子二手车页面，我查看chorme浏览器任务管理,发现必应和瓜子同用一个渲染进程，然后我又从必应搜索列表点击跳转到另外一个网站，发现他们三个同用一个渲染进程，为什么呢？他们有浏览上下文的关系，但是主域都不同，它们不是应该各自用各自的渲染进程吗？不知道这么描述清晰吗？
</div>2019-12-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSGtKFrlXheKwAse0KO8lz9r8nj6AHibmSetJ4natNicUwNTp78nm9aMibPcibCn9qxmK9MxKMeQ1mRg/0" width="30px"><span>冯建俊</span> 👍（0） 💬（1）<div>老师我在必应搜索列表中打开一个A网站链接，再打开B网链接，任务管理器查看，发现必应 A网B网同用一个渲染进程，这怎么回事呢？</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（9） 💬（1）<div>可能在编写“阿里云lot”这个项目是配置了eslint，所有的a标签必须加上 rel=&#39;noopener noreferrer&#39;</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（6） 💬（0）<div>同源要求协议、域名以及端口均一样才行；
同站点只要协议、根域名相同就行
这样子相比较下同源的要求比较难满足，通常情况下同站一点就可以保障安全性，并且条件低就更容易满足渲染进程的资源复用，提高性能，减少不必要的开销</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/2e/332fee49.jpg" width="30px"><span>刘弥</span> 👍（6） 💬（0）<div>反过来思考的话，不同站点的应用不放在同一个渲染进程的原因可能是出于不信任的因素吧。

那么大致可以认为同站点下的不同源是该公司的各个子应用，所以从安全可信的角度来讲，放在同一个渲染进程是没有问题的。

但由于本质上是不同源的，所以不可以操作对方站点的 DOM。
</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/1b/bcabd223.jpg" width="30px"><span>Snow同學</span> 👍（4） 💬（1）<div>希望老师能出一篇，如何监测收集线上用户使用网站时的性能数据。
觉得虽然开发时进行了页面性能测试，但是用户使用时，可能还会出现很多我们的盲点未考虑到。
线上监测感觉还是很有必要的</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（3） 💬（0）<div>老师你好，我有一个疑问。

在课程中，网络一直是当做一个进程来看待（network process）。

但是在查询资料的过程中，看到一篇 Google 的文章，作者说网络是浏览器进程内的一个线程（network thread）。文章附在最后。

这篇文章是 2018 年 9 月写的，是因为现在 Chromium 把网络线程从浏览器进程中拆分出来了吗？

提前谢谢老师。

文章：
Inside look at modern web browser (part 2)
https:&#47;&#47;developers.google.com&#47;web&#47;updates&#47;2018&#47;09&#47;inside-browser-part2</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/29/c8/3d6597b1.jpg" width="30px"><span>Jimmy</span> 👍（2） 💬（0）<div>老师，想请教一个chrome内存的问题, 就是我开了chrome 的任务管理器，我有看到内存占用空间远大于js内存，和GPU内存还有图片，css, js cache 之和，那要如何排查总内存是因为什么影响呢？。具体的场景就是，我有一个登录页面，本来内存大概150M, js 内存大概60M, 我登录到主页面使用一段时间，退出登录，但是我看到js 内存已经恢复了60M 左右，说明js 是没用内存泄漏的，不过问题是主内存显示确实500M, 并没有恢复到150M， 放了三个小时候依旧如何，但我看GPU内存， js 内存，图片cache 这些都已经正常了， 所以如何排查这500M 总内存到底是如何来的呢 ？</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/27/1f/42059b0f.jpg" width="30px"><span>HXL</span> 👍（1） 💬（0）<div>老师，为什么我在 https:&#47;&#47;www.geekbang.org&#47; 中点击标签 打开  https:&#47;&#47;time.geekbang.org&#47; , 在任务管理器中显示的是两个渲染进程呢, 通过 open 方法则属于一个. 而且我看跳转的 a 标签上面页面 rel属性. 有点奇怪</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/00/e1/6538ec45.jpg" width="30px"><span>狂躁小胖</span> 👍（1） 💬（2）<div>李老师，我最近刚好有一个项目用到了iframe，iframe与父文档属于同一站点，但是我想能不能强制让iframe使用新的渲染进程，这样的话是否对页面性能会有提升，同时还能使用postMessage 在父文档和iframe之间进行通信。不知道行不行的通，请李老师指点</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/db/0b/f0ded153.jpg" width="30px"><span>江谢木</span> 👍（1） 💬（1）<div>老师，我在当前页面的控制台输入window.open(&#39;www.baidu.com&#39;)没有输入协议名，为啥会打开极客时间首页的新标签。</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/f0/cae1fd01.jpg" width="30px"><span>苹果澳门app</span> 👍（0） 💬（0）<div>老师，请教个当前困扰的问题。我们线上用的是chrome浏览器，运行在win7操作系统，使用vue框架开发的应用，会出现部分设备在运行一两天（给客户办理业务的自助设备终端），发现出现页面显示文字不全的情况（实际html文字是有的，就是文字间显示一个空白占位），请问对于这种现象有什么分析和解决问题的思路？</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/cb/d4/7c494c9e.jpg" width="30px"><span>「或許」</span> 👍（0） 💬（0）<div>我验证的是：
1. 极客时间官网（https:&#47;&#47;time.geekbang.org&#47;）点击某个课程详情（https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;165897）。属于同源也是属于同一站点吧=====&gt;同一个渲染进程。

2. 极客邦科技（https:&#47;&#47;www.geekbang.org&#47;）点击页面某个标签到（https:&#47;&#47;time.geekbang.org&#47;）。属于同一站点吧=====&gt;竟然是在两个渲染进程中。
和讲义中的不太一样呀？哪里出错了吗</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6a/22/527904b2.jpg" width="30px"><span>hao-kuai</span> 👍（0） 💬（0）<div>总结:
1. a 标签和window.open 相同点是都有opener属性指向父标；不同点是后者在父标签上有new_window属性
2. 满足同一站点（协议和根域名相通，区别于同源策略的协议、域名、端口相同）和opener 即可复用同一渲染进程
3. 可以通过 a 标签设置ref 的值为 noopener 使得新标签的opener 属性为 null ，来阻止复用渲染进程</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/8f/16/e6903aad.jpg" width="30px"><span>Eval</span> 👍（0） 💬（2）<div>老师，知乎首页的每个问题的a标签并没有使用rel属性为什么不是共用一个渲染进程</div>2021-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（0） 💬（0）<div>补充：
1、右键，在其他tab或其他window打开，会被视为不是一个浏览上下文组，会用不同的浏览进程
2、tab是否在同一个window下，不会影响渲染进程的拆分及合并</div>2020-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/yicicolgdxU2vTP6ExtAf6NicvFicuAfM0tL7bOoPDMZa0bYVa8wkV10DgnpobHX9blmIicdL6zFS76Dq40Rm8xt21g/132" width="30px"><span>Geek_baa4ad</span> 👍（0） 💬（0）<div>非常负责，居然还有加餐的。大赞</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（0） 💬（0）<div>老师，能简单说下同一站点河同源站点吗区别吗？</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/d3/55afabca.jpg" width="30px"><span>YElllllOW</span> 👍（0） 💬（0）<div>老师简直牛逼！期待加餐结束后的详细资料！</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/90/ae39017f.jpg" width="30px"><span>爱吃锅巴的沐泡</span> 👍（0） 💬（0）<div>老师在第5节课中说布局计算太复杂，要放在后面说，是不是在加餐中？很期待呀</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/d9/83d1346c.jpg" width="30px"><span>Lx</span> 👍（0） 💬（0）<div>1、业务场景的需求
实际的复杂业务场景中，经常会不同的站点提供不同的业务功能。他们同属于同一公司主域，但却分属不同部门子域。同一站点策略即保持统一也能保证各自独立。且同公司场景有交互的场景需求。
2、同源策略从安全角度考虑没问题，但对于各系统通信未免严格了些。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>加餐来了，老师太棒了</div>2019-11-16</li><br/>
</ul>