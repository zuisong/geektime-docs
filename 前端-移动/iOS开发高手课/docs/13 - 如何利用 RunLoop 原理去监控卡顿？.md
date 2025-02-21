你好，我是戴铭。今天，我来和你说说如何监控卡顿。

卡顿问题，就是在主线程上无法响应用户交互的问题。如果一个 App 时不时地就给你卡一下，有时还长时间无响应，这时你还愿意继续用它吗？所以说，卡顿问题对App的伤害是巨大的，也是我们必须要重点解决的一个问题。

现在，我们先来看一下导致卡顿问题的几种原因：

- 复杂 UI 、图文混排的绘制量过大；
- 在主线程上做网络同步请求；
- 在主线程做大量的IO 操作；
- 运算量过大，CPU持续高占用；
- 死锁和主子线程抢锁。

那么，我们如何监控到什么时候会出现卡顿呢？是要监视 FPS 吗？

以前，我特别喜欢一本叫作《24格》的杂志，它主要介绍的是动画片制作的相关内容。那么，它为啥叫24格呢？这是因为，动画片中1秒钟会用到24张图片，这样肉眼看起来就是流畅的。

FPS 是一秒显示的帧数，也就是一秒内画面变化数量。如果按照动画片来说，动画片的 FPS 就是24，是达不到60满帧的。也就是说，对于动画片来说，24帧时虽然没有60帧时流畅，但也已经是连贯的了，所以并不能说24帧时就算是卡住了。

由此可见，简单地通过监视 FPS 是很难确定是否会出现卡顿问题了，所以我就果断弃了通过监视FPS 来监控卡顿的方案。

那么，我们到底应该使用什么方案来监控卡顿呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（15） 💬（2）<div>PLCrashReporter怎么和卡顿检测结合起来呢？我理解它是收集崩溃信息的，但卡顿又不是一定会崩溃</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e1/c4/15f70de2.jpg" width="30px"><span>Wechat Team</span> 👍（3） 💬（1）<div>文章提到可以『直接调用系统函数』来获取堆栈，但是通过注册那几个信号的方式获取堆栈，一般不是在闪退的情况下才可以触发回调吗？
请老师指点</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/11/37ec1136.jpg" width="30px"><span>鹏哥</span> 👍（2） 💬（1）<div>老师，请问下，如果我在用户滑动界面的时候不去加载图片，等停止滑动的时候再去加载图片，这个场景用runloop或者scrollview的代理来实现，和使用sdwebimage异步下载图片有什么区别，这几种方式貌似都没有影响用户滑动体验！</div>2019-04-09</li><br/><li><img src="" width="30px"><span>Xcode</span> 👍（1） 💬（2）<div>谢谢老师的文章，受益匪浅，尽管好多RunLoop的代码没怎么看懂，但是会去啃的，眼前有个问题想请教下：关于现在跨平台混合开发，怎么看待？基本都不用原生代码了，我现在的团队都是用ionic+Cordova，每天都是用前端Angular写代码，我担心这样下去会废了，谢谢老师</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/12/de485542.jpg" width="30px"><span>庞佳星</span> 👍（1） 💬（1）<div>老大，啥时候讲讲，resct native  和iOS的关系。谢谢啦，</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5d/5a/152d792e.jpg" width="30px"><span>茄菲</span> 👍（0） 💬（2）<div>&quot;将那些繁重而不紧急会大量占用 CPU 的任务（比如图片加载）放到空闲的 RunLoop 模式里执行就可以避开在 UITrackingRunLoopMode这个 RunLoop 模式时是执行&quot;
这样和将任务放置在异步线程里执行有什么区别呢？或者是这样有什么好处吗</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e5/d6/37a1be71.jpg" width="30px"><span>凡</span> 👍（0） 💬（1）<div>您好，我请教一个问题，我看好像大多数监控卡顿都是UI主线程上，我想知道音视频播放以及直播的这种卡顿能否用这种方式监测到！通常直播这种流畅程度都是通过服务器端监控的，但是对于小公司来说，对接的直播基本都是第三方的库和服务平台，所以不太好太太去三方服务平台拉日志！所以如果我这种对接第三方直播库的app，如果我想把这种监控放到客户端来做，应该如何处理呢？谢谢，期待您解决我的疑问</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/43/63bdc516.jpg" width="30px"><span>二木又土</span> 👍（0） 💬（1）<div>刚IM项目中遇到一个实际卡顿的情景，程序启动后，需要从服务端获取3w条会话列表，web收到数据后，需要排序后显示，排序操作需要700ms，加上列表显示大概要2秒的时间，想过排序放子线程操作，又要处理多线程的问题，很纠结。
</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/39/1b/bcabd223.jpg" width="30px"><span>Snow同學</span> 👍（0） 💬（1）<div>觉得使用：02 | App 启动速度怎么做优化与监控？  讲的内容，设置方法的执行最短时间，也是可以查找那些在主线程长时间执行的方法的</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（1）<div>今天没作业真是爽歪歪</div>2019-04-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aiaSrhS44dUCfpycicJ6UWANe3aEkdibMFOOX2oXRo0amNwYxQM1dCKZpzfMdy3Z2ibwSSPu6ibFxnTvuDGzKiaLIClA/132" width="30px"><span>Geek_cc73f2</span> 👍（0） 💬（1）<div>老师你好，从文章真的受益匪浅，以前只会用第三方的，现在能从本质看出端倪，另外能不能从源头给一些建议呢，比如怎么避免卡顿，哪些操作容易卡顿，然后怎么处理呢，感谢</div>2019-04-09</li><br/><li><img src="" width="30px"><span>Geek_a03ab1</span> 👍（52） 💬（10）<div>为什么监控 kCFRunLoopBeforeSources、kCFRunLoopAfterWaiting这两个事件就能判断出卡顿呢？为什么不是kCFRunLoopBeforeWaiting、kCFRunLoopAfterWaiting这两个事件呢？没想明白，老师能展开说下吗？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/cc/5ff05eb3.jpg" width="30px"><span>WeZZard</span> 👍（23） 💬（0）<div>單純監控 FPS 確實不行，因為很多卡頓其實是 FPS 變化率的大幅變化（既 FPS 一階導數的波動）所造成的。

比如說點 A 花一秒匀速位移至點 B，秒間平均幀率 60FPS，但是前 59&#47;60 秒才跑了一幀出來，剩下 59 幀都在後 1&#47;60 秒跑出來，那麼用戶必然看到的是點 A 花了 59&#47;60 秒停在 A + ((B - A)&#47;60) 這個位置上，然後突然「飛」到了 B 點上。

所以監控 FPS &gt; 24 的同時還要監控 FPS 變化率的波動。而這個波動的成因其實就是主線程上計算任務的性能衝擊。</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/33/6b9a7719.jpg" width="30px"><span>金阳</span> 👍（22） 💬（0）<div>https:&#47;&#47;blog.ibireme.com&#47;2015&#47;05&#47;18&#47;runloop&#47;  这篇文章讲的更清晰些</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/1b/40293181.jpg" width="30px"><span>鼠辈</span> 👍（17） 💬（0）<div>这个3秒是不是太长了，1秒60帧，每帧16.67ms。runlooo会在每次sleep之前去刷新ui，这样的话如果掉了30帧，就是500ms左右，用户的体验就已经下去了，能感觉到卡顿了.
</div>2019-04-09</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（6） 💬（0）<div>想起以前遇到过的卡顿效果，真的是坑啊。

印象最深的一次卡顿：在TableView的Cell里访问了数据库。

其次是在一个答题系统里，多选单选与判断题，一个Cell从最少两个选项、一个选项三到N行，到最多九个选项。然后使用了TableViewCell的高度自动计算，后来换成了自己手动计算并缓存。

还有Cell的样式太多，后来把尽可能相同的都放到一个Cell里，也就是：一个Cell有七行，如果有四行不显示，那就移除四行，如果需要九行就再加两行。还有就是网络请求同步操作，结果数据过大，然后就做了异步和无数据的默认显示。

其实我就是从这几个方面下手的：页面重叠部分、简单的动画与显示用CALayer自己画、对象释放与创建的次数、高度自动缓存、autoRelease使用、static使用部分（如单列对象）、UI刷新前的数据处理部分、页面刷新次数、通知和监听的移除、数据的不合理读取、复杂操作尽量异步、

最后想说下：线程的消息传递依赖于NSRunLoop，函数的调用依赖runtime。感觉二者挺像的。</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/05/b2776d73.jpg" width="30px"><span>Geek</span> 👍（5） 💬（4）<div>卡顿的原因讲的可以，但是讲的RunLoop让我听的头大，有几个疑问请教老师，
1，线程与run loop是什么关系。
2，mach_port是什么，第一次进入runloop，也是mach_port触发的吗，
3.进入休眠状态的runloop为什么要等mach_port.
4,系统会有多个runloop吗，不同runloop之间是串行还是并行执行的？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/4e/ef406442.jpg" width="30px"><span>唯她命</span> 👍（4） 💬（1）<div>点击事件超时，kCFRunLoopBeforeSources、kCFRunLoopAfterWaiting  监控不了</div>2020-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/4e/5095f5b6.jpg" width="30px"><span>董仕卿</span> 👍（4） 💬（0）<div>你这不是在讲runloop的源码嘛</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/f7/12a952a0.jpg" width="30px"><span>天涯</span> 👍（3） 💬（2）<div>runloop监听kCFRunLoopBeforeSources做ui刷新，为什么还需要监听kCFRunLoopAfterWaiting来判定卡顿</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/41/9c/f4f22c62.jpg" width="30px"><span>菲夜</span> 👍（2） 💬（0）<div>作者认为并不能说 24 帧时就算是卡住了，确实 24 帧确实算不上卡，但是24 帧是用在观看电影上的，而APP或者游戏因为显示机制并不一样，24 帧在视觉观感其实还是会感觉有卡顿，用户体验不佳。

</div>2019-05-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUmLkzxSWpS3I74CcHegN1SRQ3L000oUazjnk7KGwJN98vmibZkpogxiaqYoEEJ5zFfWXSwXjAw4Uw/132" width="30px"><span>Geek_a6d9b0</span> 👍（1） 💬（2）<div> 戴老大， CFRunLoopObserverCreate 创建观察者的时候 order 传 0 对于点击 tableViewCell 造成的卡顿检测不到，要改成LONG_MAX 才以后可以检测到了。 </div>2021-06-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLDW0y0ZHYVRgkrGt16ylsklKoZEGiaalibWBjIDUKZtY3PeMpZckTsoKEetWRSkxrS2fLgibxJA4WtIw/132" width="30px"><span>夏至</span> 👍（1） 💬（0）<div>swift 版本CFRunLoopObserver创建，通过runloopObserverHandle处理超时判断
        self.runloopObserver = CFRunLoopObserverCreateWithHandler(kCFAllocatorDefault, CFRunLoopActivity.allActivities.rawValue, true, 0, { [weak self] (observer, activity) in
            guard let strongSelf = self else {
                return
            }
            
            strongSelf.runloopObserverHandle(observer: observer, activity: activity)
        })
        
        CFRunLoopAddObserver(CFRunLoopGetMain(), self.runloopObserver, CFRunLoopMode.commonModes)
</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2e/d5/fa9300aa.jpg" width="30px"><span>小宇</span> 👍（1） 💬（0）<div>为什么监控 kCFRunLoopBeforeSources、kCFRunLoopAfterWaiting这两个事件就能判断出卡顿呢？kCFRunLoopBeforeWaiting不是也做一些UI的刷新吗，这个时间过长不也是会造成卡顿吗</div>2019-12-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK9ma0nrF2yicbQ079mTDd6RdN6hOEnLL1ePEY3arqxQSc1EAGQTJjqSHaFlRtnB3YzXpp8kPdXu9w/132" width="30px"><span>Geek__b82782469097</span> 👍（1） 💬（1）<div>请问swift是如何检测卡顿的呢？也是runloop么？</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/99/918e9b2a.jpg" width="30px"><span>三刀流剑客</span> 👍（1） 💬（1）<div>看了老师讲的 runloop 的原理 , runloop 有不同的mode,当需要切换mode 的时候,我不明白的是不同mode 的任务状态是如何记录呢?</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/9e/7a6e6442.jpg" width="30px"><span>一纸丶荒年</span> 👍（0） 💬（0）<div>讲实话。 有写 看不明白 😄 。</div>2022-12-29</li><br/><li><img src="" width="30px"><span>Geek_ea2f98</span> 👍（0） 💬（0）<div>大佬你好，我试过写一个tableview列表，然后cell加载上面写sleep(1)来模拟卡顿问题，他这样确实也导致了FPS帧率下降了很多，保持在10-20帧率，很卡，但是activity太的枚举一直在kCFRunLoopBeforeWaiting上面，kCFRunLoopBeforeSources和kCFRunLoopAfterWaiting这两个枚举根本就没走，这是为何呢，我查阅了好些博客，对比了跟别人写的代码，甚至拷贝别人代码出来，结果都是一样的。</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/65/fc/a2247327.jpg" width="30px"><span>Evan</span> 👍（0） 💬（0）<div>我在看源码的同时看你的这章课程，有一个疑惑，你把do while保活线程的执行顺序放在了进入loop之后。但是源码中CFRunLoopRun函数里执行了第一个do while，条件是不等于stop后者finish。然后在__CFRunLoopRun函数执行了第二个do while()，条件是等于0，在__CFRunLoopRun函数即将走完的时候可能会更新这个retVal值，跳出第二个循环，然后来到第一个循环里继续执行。按照代码的执行逻辑，是否可以说先开启do while保活线程，然后开始进入loop；</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ea/36/7d088c63.jpg" width="30px"><span>D</span> 👍（0） 💬（0）<div>第四步里面的被调用者唤醒，这里的调用者指的是什么呢？</div>2021-07-09</li><br/>
</ul>