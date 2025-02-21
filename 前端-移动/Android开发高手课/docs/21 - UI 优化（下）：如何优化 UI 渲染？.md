孔子曰：“温故而知新”，在学习如何优化UI渲染之前，我们先来回顾一下在“卡顿优化”中学到的知识。关于卡顿优化，我们学习了4种本地排查卡顿的工具，以及多种线上监控卡顿、帧率的方法。为什么要回顾卡顿优化呢？那是因为UI渲染也会造成卡顿，并且肯定会有同学疑惑卡顿优化和UI优化的区别是什么。

在Android系统的VSYNC信号到达时，如果UI线程被某个耗时任务堵塞，长时间无法对UI进行渲染，这时就会出现卡顿。但是这种情形并不是我们今天讨论的重点，UI优化要解决的核心是由于渲染性能本身造成用户感知的卡顿，它可以认为是卡顿优化的一个子集。

从设计师和产品的角度，他们希望应用可以用丰富的图形元素、更炫酷的动画来实现流畅的用户体验。但是Android系统很有可能无法及时完成这些复杂的界面渲染操作，这个时候就会出现掉帧。也正因如此我才希望做UI优化，因为我们有更高的要求，希望它能达到流畅画面所需要的60 fps。这里需要说的是，即使40 fps用户可能不会感到明显的卡顿，但我们也仍需要去做进一步的优化。

那么接下来我们就来看看，如何让我们的UI渲染达到60 fps？有哪些方法可以帮助我们优化UI渲染性能？

## UI渲染测量
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/e6/6a88c8a3.jpg" width="30px"><span>刘伟</span> 👍（4） 💬（4）<div>老师你好，有个问题想要请教一下

你在这篇文章里面提到了 异步创建 

我尝试在子线程调用了如下代码，没按照文中的说法替换子线程 Looper的MessageQueue

View v = new View(MainActivity.this);
v.invalidate();
v.setLayoutParams(new ViewGroup.MarginLayoutParams(200, 200)); v.setBackgroundColor(Color.RED);

然后在主线程中添加到LinearLayout ！代码正常运行，界面也正常显示。
查看源码之后，检查线程是在ViewRootImpl中做的，而这个方法会在view invalidate 以后调用，我在子线程中调用的时候，因为还没有添加到 LinearLayout 中，所以不会触发ViewRootImpl 中方法的调用。 (翻了一下 5.0 和 8.0 的源码)

那么你在文章中提到的 替换子线程的消息队列作用是什么呢？

分割线---------------

但是上面不替换消息队列的情况对WebView 不起作用，子线程创建WebView的时候必须替换。
替换成之后，WebView 可以正常创建的了

然而在主线程中添加到布局容器时候还是提示在非UI线程操作了View. 不知道老师使用这种方法的时候有没有遇到类似的问题。

再割-----------------

关于这个问题在stackoverflow上也有个类似的提问~

https:&#47;&#47;stackoverflow.com&#47;questions&#47;5284513&#47;constructing-views-in-a-non-ui-thread-and-consuming-in-the-ui-thread





</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/55/48de9a24.jpg" width="30px"><span>Carlo</span> 👍（1） 💬（1）<div>用flutter痛苦啊。还不如开发native app。各种坑。就一个facebook integration就产生了很多bug。</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/48/03abbbd1.jpg" width="30px"><span>瑞</span> 👍（1） 💬（1）<div>你好，目前应用碰到进入主界面卡顿黑屏现象比较严重，需要怎么定位问题吗，本人已根据排除法去定位相关代码，但是定位到结果存在概率性，需要怎么去定位到真正的问题呢？麻烦帮忙说下处理方案</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/e6/6a88c8a3.jpg" width="30px"><span>刘伟</span> 👍（0） 💬（1）<div>开拓眼界~每一个点深入都是一个大领域</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/c8/68263086.jpg" width="30px"><span>哈珀朋友</span> 👍（0） 💬（2）<div>老哥RenderScript说得太简单了，原本以为会针对后端编译器LLVM做分析呢</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/b0/4e22819f.jpg" width="30px"><span>syz</span> 👍（16） 💬（0）<div>美团关于Litho的一篇文章，推给大家做参考。作为小白觉得看的清晰https:&#47;&#47;tech.meituan.com&#47;2019&#47;03&#47;14&#47;litho-use-and-principle-analysis.html</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/1b/abb7bfe3.jpg" width="30px"><span>venciallee</span> 👍（2） 💬（3）<div>Android RenderScript 简单高效实现图片的高斯模糊效果的链接被劫持跳到Huang色网站了。。</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/ab/dd9ab224.jpg" width="30px"><span>EdwdChen</span> 👍（2） 💬（4）<div>请教一下，文中提及 flutter 是使用 skia 来进行渲染的，但是前一篇文章提到 skia 是软件渲染，这是不是意味着 flutter 虽然方便但是 ui 渲染上性能还是没有原声组件好呢？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/82/f039ae08.jpg" width="30px"><span>gk</span> 👍（1） 💬（0）<div>值得粗读完，精细学习一阵子的高手课。</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（0）<div>存储优化、网络优化、耗电优化到现在的UI优化，深深的把我刺激到了。以前搞的Android都只是为了实现而实现，以后我一定要好好规划规划，把这些优化都用起来。</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（0） 💬（0）<div>怎么没提AsyncInflate 呀？</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/65/f281f579.jpg" width="30px"><span>大鹏鸟</span> 👍（0） 💬（2）<div>flutter集成到native项目中，体积大了18m，问下这是合理的么</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/66/fd/84c3c0d3.jpg" width="30px"><span>Jack</span> 👍（0） 💬（0）<div>View复用这一块 能分享一下怎么做到View的净身出户的吗？</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/27/eb/fdceac5d.jpg" width="30px"><span>人海中一只羊</span> 👍（0） 💬（0）<div>关于UI异步创建会抛出异常的那部分，能否举个例子？</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/06/0e6b6365.jpg" width="30px"><span>ForzaJuve</span> 👍（0） 💬（0）<div>涨见识，开眼界</div>2019-03-19</li><br/>
</ul>