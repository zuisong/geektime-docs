你好，我是戴铭。

手机设备电量有限，App 开发时如不注意电量的的消耗，当用户发现你的 App 是耗电大户时，就会毫不犹豫地将其抛弃。所以，每次开发完，我们都需要去检查自己的App有没有耗电的问题。

耗电的原因有千万种，如果每次遇到耗电过多的问题，我们都从头查找一番的话，那必然会效率低下。

就比如说，测试同学过来跟你说“某个页面的前一个版本还好好的，这个版本的耗电怎么多了那么多”，那么你首先想到可能就是这个页面有没有开启定位，网络请求是不是频繁，亦或是定时任务时间是不是间隔过小。接下来，你会去查找耗电问题到底是怎么引起的。你去翻代码的时候却发现，这个页面的相关功能在好几个版本中都没改过了。

那么，到底是什么原因使得这一个版本的耗电量突然增加呢？不如就使用排除法吧，你把功能一个个都注释掉，却发现耗电量还是没有减少。这时，你应该怎么办呢？接下来，我就在今天的文章里面和你详细分享一下这个问题的解法吧。

我们首先需要明确的是，只有获取到电量，才能够发现电量问题。所以，我就先从如何获取电量和你讲起。

## 如何获取电量？

在iOS中，IOKit framework 是专门用于跟硬件或内核服务通信的。所以，我们可以通过IOKit framework 来获取硬件信息，进而获取到电量消耗信息。在使用IOKit framework时，你需要：
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/42/0e/21b8025f.jpg" width="30px"><span>月落泉</span> 👍（0） 💬（2）<div>smStackOfThread这个方法哪有啊</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/10/2d673601.jpg" width="30px"><span>好饿早知道送外卖了</span> 👍（0） 💬（1）<div>QOS_CLASS_UTILITY指定block的Qos，是不是和设置队列优先级效果一样？</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2f/27/9a606b3e.jpg" width="30px"><span>泽七</span> 👍（40） 💬（2）<div>获取电量为什么不用 [[UIDevice currentDevice] batteryLevel] 呢？</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/9a/78f2af55.jpg" width="30px"><span>包罗万象</span> 👍（7） 💬（0）<div>iokit已经无法导入了，请问老师这种情况你是怎们处理的？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/35/51/ed895596.jpg" width="30px"><span>繁星mind</span> 👍（3） 💬（0）<div>电量优化 https:&#47;&#47;www.jianshu.com&#47;p&#47;bd2c1ce5c02a</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/bf/5f4681b6.jpg" width="30px"><span>cp_kong</span> 👍（3） 💬（2）<div>IOKit Frameworks 目前在iOS项目中无法导入了，要自己新建一个mac项目，然后从那个项目导入，再拷到iOS项目中</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/91/53/ebf6a6ac.jpg" width="30px"><span>cocoakc</span> 👍（3） 💬（0）<div>IOKit framework 是Mac 的框架？参考的这个吗？https:&#47;&#47;blog.csdn.net&#47;uxyheaven&#47;article&#47;details&#47;38167509</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d7/4d/d74ffb1f.jpg" width="30px"><span>黄昏</span> 👍（1） 💬（0）<div>cpu使用量确实是耗电的重大原因。不合理的动画可能导致cpu暴涨，电量损耗巨大。</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/16/ca250e8c.jpg" width="30px"><span>王木公</span> 👍（0） 💬（0）<div>有个问题可能没有讲到，如何发现电量消耗太大的问题？参考指标、阈值有什么？一个App开发、测试、发布过程中，在哪一步去监控或排查有无耗电量的问题？</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/77/67/10063e76.jpg" width="30px"><span>星辰</span> 👍（0） 💬（0）<div>老师你好，IOKit中拿到的电池电量与UIDevice中获取到的电池电量相比谁的精度更高呢</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/46/45/570163e0.jpg" width="30px"><span>Alexander</span> 👍（0） 💬（0）<div>获取电量的for循环直接return了。</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/76/ad/1dbf46f5.jpg" width="30px"><span>do .利军</span> 👍（0） 💬（1）<div>Stack of thread: 771:
CPU used: 34.0 percent
user time: 542025 second
libsystem_kernel.dylib         0x111e6617a mach_msg_trap + 10
libsystem_kernel.dylib         0x111e696a2 thread_get_state + 421
Stock                          0x102e35f7e smStackOfThread + 878
Stock                          0x102f0fea8 +[SMCPUMonitor updateCPU] + 296
Stock                          0x1038d097f -[AppDelegate updateCPUInfo] + 47
Foundation                     0x10bd2a135 __NSFireTimer + 83
CoreFoundation                 0x10a8613e4 __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__ + 20
CoreFoundation                 0x10a860ff2 __CFRunLoopDoTimer + 1026
CoreFoundation                 0x10a86085a __CFRunLoopDoTimers + 266
CoreFoundation                 0x10a85aefc __CFRunLoopRun + 2220
CoreFoundation                 0x10a85a302 CFRunLoopRunSpecific + 626
GraphicsServices               0x1127d52fe GSEventRunModal + 65
UIKitCore                      0x11b5dfba2 UIApplicationMain + 140
Stock                          0x103ff37d0 main + 112
libdyld.dylib                  0x111b48541 start + 1

我检测到的信息如上，+后边的数字是什么意思呢？数值越=大，表示占用越多？</div>2019-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/suDu7BaYWwk1ucZW2EYmVDCNCia7TcBzOHp2Qb9NDjcjhw6XIxMn7owaM7mTfnPibsFapdlug8Wg2UiaWgaPTbWyg/132" width="30px"><span>Geek_rnkwl4</span> 👍（0） 💬（0）<div>iOS需要强制导入IOKit框架吗</div>2019-04-28</li><br/><li><img src="" width="30px"><span>Calabash_Boy</span> 👍（0） 💬（0）<div>获取电量方法里,为什么循环里有个return呢?那就没有必要写循环了吧</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/31/87/1a0377fa.jpg" width="30px"><span>赫小僧</span> 👍（0） 💬（0）<div>请教个问题, dispatch_block_create_with_qos_class 这种方式创建出的队列进行复杂计算的时候对电量有优化. 相关信息可以去哪查看呢?

</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/90/abb7bfe3.jpg" width="30px"><span>Geek_8iv7s5</span> 👍（0） 💬（0）<div>请问老师一个问题，下面这段代码如何在断点时插入到有问题的方法中：
thread_act_array_t threads;
mach_msg_type_number_t threadCount = 0;
const task_t thisTask = mach_task_self();
kern_return_t kr = task_threads(thisTask, &amp;threads, &amp;threadCount);
</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（0） 💬（0）<div>受教了</div>2019-04-21</li><br/>
</ul>