你好，我是陈航。

在上一篇文章中，我与你分享了如何捕获Flutter应用的未处理异常。所谓异常，指的是Dart代码在运行时意外发生的错误事件。对于单一异常来说，我们可以使用try-catch，或是catchError去处理；而如果我们想对异常进行集中的拦截治理，则需要使用Zone，并结合FlutterError进行统一管理。异常一旦被抓取，我们就可以利用第三方数据上报服务（比如Bugly），上报其上下文信息了。

这些线上异常的监控数据，对于开发者尽早发现线上隐患，确定问题根因至关重要。如果我们想进一步评估应用整体的稳定性的话，就需要把异常信息与页面的渲染关联起来。比如，页面渲染过程是否出现了异常，而导致功能不可用？

而对于以“丝般顺滑”著称的Flutter应用而言，页面渲染的性能同样需要我们重点关注。比如，界面渲染是否出现会掉帧卡顿现象，或者页面加载是否会出现性能问题导致耗时过长？这些问题，虽不至于让应用完全不能使用，但也很容易引起用户对应用质量的质疑，甚至是反感。

通过上面的分析，可以看到，衡量线上Flutter应用整体质量的指标，可以分为以下3类：

- 页面异常率；
- 页面帧率；
- 页面加载时长。

其中，页面异常率反应了页面的健康程度，页面帧率反应了视觉效果的顺滑程度，而页面加载时长则反应了整个渲染过程中点对点的延时情况。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/1c/ec/d9af0dc9.jpg" width="30px"><span>！_新起点</span> 👍（3） 💬（2）<div>如果页面渲染依赖单个或多个网络接口回调，那么我们需要减去用单个或者多个接口请求后，成功或者失败后的最后的回调里加载时间的时长。</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/37/aa04f997.jpg" width="30px"><span>和小胖</span> 👍（0） 💬（1）<div>老师，如果一个 App 只有一个继承 StatelessWidget 的页面，那么在不用原生配合的情况下如何得知页面退出了呢？NavigatorObserver 的 didPush 可以知道页面进入了，但是没有页面退出或者销毁的回调。</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/74/e0b9807f.jpg" width="30px"><span>小米</span> 👍（0） 💬（1）<div>页面加载时长，一般超过多少毫秒算不正常呢？</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/02/9a/3b44f43d.jpg" width="30px"><span>find</span> 👍（4） 💬（3）<div>当升级到Flutter 1.12.x 之后，onReportTimings应该改成SchedulerBinding的addTimingsCallback,SchedulerBinding.instance.addTimingsCallback(_onReportTimings);</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/cb/5e79c6ed.jpg" width="30px"><span>(Jet)黄仲平</span> 👍（0） 💬（1）<div>老师好，在真实运用中这个帧率和界面异常率，是会设定一个阀值，当超出这个值的时候就上报。是吗？</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/2a/7e/6d2e703b.jpg" width="30px"><span>小何</span> 👍（0） 💬（1）<div>return lastFrames.length&#47;sum * 60; 这里写是写反了嘛 不应该是return sum * 60&#47;lastFrames.length;嘛</div>2021-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/02/9a/3b44f43d.jpg" width="30px"><span>find</span> 👍（0） 💬（0）<div>那个帧率是怎么打印出来的，什么时机打印，上报呢</div>2021-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/e8/d1e52dbb.jpg" width="30px"><span>IF-Processing</span> 👍（0） 💬（1）<div>两个问题：
1. 下面这段怎么保留的原始回调，没看懂。。保留引用就能保留原始回调了吗？这个调用是链式的？
void main()
 { runApp(MyApp()); 
&#47;&#47;设置帧回调函数并保存原始帧回调函数 
 orginalCallback = window.onReportTimings;
 window.onReportTimings = onReportTimings;}
2.咱们统计出来这3个指标之后，通过什么手段上报呢？也使用类似bugly这种异常上报的机制吗？什么情况下使用，如何使用呢？</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/24/4005d4c8.jpg" width="30px"><span>Fun</span> 👍（0） 💬（1）<div>请问计算FPS的时候为什么要乘60</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/05/3e2b8688.jpg" width="30px"><span>时光念你</span> 👍（0） 💬（0）<div>如果接口是when整合过的，取第二次的addPostFrameCallback时间作为Endtime。如果每个接口单独请求，取接口数量➕1的回调次数时间作为Endtime。</div>2019-12-26</li><br/>
</ul>