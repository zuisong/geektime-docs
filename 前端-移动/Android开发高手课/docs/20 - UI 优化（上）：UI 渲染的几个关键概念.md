在开始今天的学习前，我祝各位同学新春快乐、工作顺利、身体健康、阖家幸福，绍文给您拜年啦！

> 每个做UI的Android开发，上辈子都是折翼的天使。

多年来，有那么一群苦逼的Android开发，他们饱受碎片化之苦，面对着各式各样的手机屏幕尺寸和分辨率，还要与“凶残”的产品和UI设计师过招，日复一日、年复一年的做着UI适配和优化工作，蹉跎着青春的岁月。更加不幸的是，最近两年这个趋势似乎还愈演愈烈：刘海屏、全面屏，还有即将推出的柔性折叠屏，UI适配将变得越来越复杂。

UI优化究竟指的是什么呢？我认为所谓的UI优化，应该包含两个方面：一个是效率的提升，我们可以非常高效地把UI的设计图转化成应用界面，并且保证UI界面在不同尺寸和分辨率的手机上都是一致的；另一个是性能的提升，在正确实现复杂、炫酷的UI设计的同时，需要保证用户有流畅的体验。

那如何将我们从无穷无尽的UI适配中拯救出来呢？

## UI渲染的背景知识

究竟什么是UI渲染呢？Android的图形渲染框架十分复杂，不同版本的差异也比较大。但是无论怎么样，它们都是为了将我们代码中的View或者元素显示到屏幕中。

而屏幕作为直接面对用户的手机硬件，类似厚度、色彩、功耗等都是厂家非常关注的。从功能机小小的黑白屏，到现在超大的全面屏，我们先来看手机屏幕的发展历程。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="" width="30px"><span>ekkoLee</span> 👍（22） 💬（1）<div>您好 我们的项目也有很多libhwui的崩溃，占jni的35%以上，可以分享下大概的解决思路和方向吗</div>2019-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/0lTtM624ia8QlghIm9yfGLvjFltC03TgWlfuNC8vLibnuD8sosTcb3ynR5F2gANq1fwMPh4EiakbRVT8I59YKYjCg/132" width="30px"><span>Geek_2d38e3</span> 👍（0） 💬（1）<div>张老师您好，我们的应用也遇到了hwui的问题且占比很高，能简单分享一下思路吗，不胜感激</div>2019-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erybSCGfl8xiaN0nSa4BwfNJlI7bicXxPMQDOiaY2r1toC0lTeTqUJPLmsKdGWZ416cricibOtpEHwQPbg/132" width="30px"><span>Geek_ax6y3f</span> 👍（0） 💬（1）<div>非常希望可以分享如何解决libhwui的崩溃，我们项目中也有很多</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/34/10cca5eb.jpg" width="30px"><span>韩增波</span> 👍（0） 💬（1）<div>您好 我们的项目也有很多libhwui的崩溃，不知是否可以帮忙提供一下解决思路。多谢。</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/c8/68263086.jpg" width="30px"><span>哈珀朋友</span> 👍（12） 💬（0）<div>老哥Android显示系统说得不错。老哥的风格，由浅入深，授人以渔，非常像一个优秀的学院派教授说课风格，很喜欢，相信其他人也很容易看懂</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/00/fbf5a3c3.jpg" width="30px"><span>辉   哥</span> 👍（1） 💬（0）<div>张哥，新年快乐！</div>2019-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9c/96/abb7bfe3.jpg" width="30px"><span>啊 菠萝</span> 👍（0） 💬（0）<div>看文章链接里的头条方案代码似乎并没有用到反射而是直接赋值？</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5f/e9/41b6b116.jpg" width="30px"><span>Geek_258277</span> 👍（0） 💬（0）<div>您好，关于libhwui的崩溃问题，想问下您主要hook了哪些点呢？</div>2020-07-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N0NACGUr8dNAbN6BdiagPHBaB0EnyDsI9zWpwJteqTY38apOEnTOA7JkBAQnzYKJBgxu3Q8YMUILwLAB6camn4w/132" width="30px"><span>Swing</span> 👍（0） 💬（1）<div>“对于不支持的 API，我们需要使用软件绘制模式，渲染的性能将会大大降低。”
是说 开发人员 主动切换成 软件绘制 还是 会自动切换呢？
如果不自动切换。也不支持。会crash吗？？？</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/49/418a9486.jpg" width="30px"><span>Neil</span> 👍（0） 💬（0）<div>libhwui我们也经常遇到这个怎么解决</div>2019-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/e6/6a88c8a3.jpg" width="30px"><span>刘伟</span> 👍（0） 💬（0）<div>目前遇到问题优化的时候，有些阶段发生的事情感觉有点无从下手去解决，比如命令问题和交换缓冲区</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/4e/95017299.jpg" width="30px"><span>(ㄒoㄒ)</span> 👍（0） 💬（0）<div>过年好，老哥</div>2019-02-05</li><br/>
</ul>