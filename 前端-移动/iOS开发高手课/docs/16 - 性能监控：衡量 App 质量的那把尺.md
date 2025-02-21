你好，我是戴铭。

通常情况下，App 的性能问题虽然不会导致 App不可用，但依然会影响到用户体验。如果这个性能问题不断累积，达到临界点以后，问题就会爆发出来。这时，影响到的就不仅仅是用户了，还有负责App开发的你。

为了能够主动、高效地发现性能问题，避免App质量进入无人监管的失控状态，我们就需要对App的性能进行监控。目前，对App的性能监控，主要是从线下和线上两个维度展开。

今天这篇文章，我就从这两个方面来和你聊聊如何做性能监控这个话题。接下来，我们就先看看苹果官方的线下性能监控王牌 Instruments。

## Instruments

关于线下性能监控，苹果公司官方就有一个性能监控工具Instruments。它是一款被集成在 Xcode 里，专门用来在线下进行性能分析的工具。

Instruments的功能非常强大，比如说Energy Log就是用来监控耗电量的，Leaks就是专门用来监控内存泄露问题的，Network就是用来专门检查网络情况的，Time Profiler就是通过时间采样来分析页面卡顿问题的。

如下图所示，就是Instruments的各种性能检测工具。

![](https://static001.geekbang.org/resource/image/08/e9/087ddcf91e5c222804f753389edf2de9.png?wh=1690%2A3410)

图1 Instruments 提供的各种性能检测工具
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVegfjqa0gM4hcRrBhZkIf7Uc5oeTMYsg6o5pd76IQlUoIIh2ic6P22xVEFtRnAzjyLtiaPVstkKug/132" width="30px"><span>xilie</span> 👍（4） 💬（1）<div>要不还是介绍下第三方的监控平台，小公司，监控后台都没人做啊</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7f/d8/36512951.jpg" width="30px"><span>小阳哥</span> 👍（4） 💬（2）<div>每2s去遍历线程 这个不会有问题吗？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fc/da/1f1254e6.jpg" width="30px"><span>小城</span> 👍（1） 💬（1）<div>内存线上监控，不是针对多个线程，而是直接从结构体里面取出phys_footprint就可以？</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/b0/b91fc19b.jpg" width="30px"><span>异界</span> 👍（1） 💬（1）<div>图片名字，使用中文，会影响性能吗（项目中90％以上使用的中文命名图片）？</div>2019-05-05</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（20） 💬（0）<div>CADisplayLink:与屏幕刷新频率的计时器同步，每次屏幕刷新都会调用一次，所以可以获取到一秒钟屏幕刷新的次数。
线下监控：Instrument，一个工具检测所有。
线上监控：CPU使用直接获取所有线程的cpu_usage计算综合，内存消耗使用task_basic_info的phys_footprint，FPS用CADisplayLink。</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/73/aa/442e9eb1.jpg" width="30px"><span>李大江</span> 👍（3） 💬（0）<div>对于性能的监控有没有衡量标准，如何衡量优劣？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c6/30/55a03b70.jpg" width="30px"><span>Onion</span> 👍（3） 💬（0）<div>监控起来如何分析，有实践方案嘛</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/92/78e66924.jpg" width="30px"><span>一代真龙</span> 👍（2） 💬（0）<div>线上电量监控是监控不了的。现有的方案都是不可行的，没有参考价值。</div>2019-04-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PjTbTVicNs9wpgmmpxvSK6orvN2E4wOmQ1ukSNMd5icoFEulcA21QaQvtp6ADvgOicnibPLZQop91ISU6cyQmfKJwg/132" width="30px"><span>CoderY</span> 👍（1） 💬（0）<div>文中提到“集成多个公司 SDK 的情况，所以我们就需要以黑盒的方式来进行性能监控”，请问大佬这块具体怎么监控？</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/6c/29d8075b.jpg" width="30px"><span>Geek_rvf9xm</span> 👍（1） 💬（0）<div>time profile 工具再最新的xcode版本上收集不到数据，作者你有遇到过吗？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/78/f6/231cb5cd.jpg" width="30px"><span>drq</span> 👍（1） 💬（3）<div>app耗电量怎么监控呢</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/0b/2ccf7908.jpg" width="30px"><span>...</span> 👍（0） 💬（0）<div>内存泄露线上监控如何做呢</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/80/3f/bc65b009.jpg" width="30px"><span>Yest</span> 👍（0） 💬（2）<div>戴老师。cpu_usage是千分比吗？我打印的最高是1000
(lldb) p threadBaseInfo-&gt;cpu_usage
(integer_t) $10 = 965

看原文解释 是百分比啊
integer_t       cpu_usage;      &#47;* scaled cpu usage percentage *&#47;</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/59/b607b8c0.jpg" width="30px"><span>毛成方</span> 👍（0） 💬（0）<div>threadBaseInfo = (thread_basic_info_data_t)threadInfo;
xcode8.2 无法强制转换
请问得更新xcode？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/42/0e/21b8025f.jpg" width="30px"><span>月落泉</span> 👍（0） 💬（2）<div>mach_task_self()这个函数报错Implicit declaration of function &#39;mach_task_self&#39; is invalid in C99，如何处理</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/d0/259e7ce3.jpg" width="30px"><span>政</span> 👍（0） 💬（0）<div>有个问题，就是用instrument的leak功能的时候，app运行起来会比较卡。不知道自定义的instrument会不会也有这个问题。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（0）<div>Xcode 还有这么牛的功能</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/21/b20b2f44.jpg" width="30px"><span>国朋</span> 👍（0） 💬（0）<div>老哥，询问个问题，APP第一次安装，安装后会提示网络权限，提示权限时APP有什么活动吗，触发网络访问的代码后面的程序是出于等待状态，还是已经执行了呢</div>2019-04-17</li><br/>
</ul>