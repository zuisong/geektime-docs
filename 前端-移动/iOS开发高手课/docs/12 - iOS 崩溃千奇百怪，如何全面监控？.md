你好，我是戴铭。今天我要跟你说的是崩溃监控。

App上线后，我们最怕出现的情况就是应用崩溃了。但是，我们线下测试好好的App，为什么上线后就发生崩溃了呢？这些崩溃日志信息是怎么采集的？能够采集的全吗？采集后又要怎么分析、解决呢？

接下来，通过今天这篇文章，**你就可以了解到造成崩溃的情况有哪些，以及这些崩溃的日志都是如何捕获收集到的。**

App 上线后，是很脆弱的，导致其崩溃的问题，不仅包括编写代码时的各种小马虎，还包括那些被系统强杀的疑难杂症。

下面，我们就先看看几个常见的编写代码时的小马虎，是如何让应用崩溃的。

- 数组越界：在取数据索引时越界，App会发生崩溃。还有一种情况，就是给数组添加了 nil 会崩溃。
- 多线程问题：在子线程中进行 UI 更新可能会发生崩溃。多个线程进行数据的读取操作，因为处理时机不一致，比如有一个线程在置空数据的同时另一个线程在读取这个数据，可能会出现崩溃情况。
- 主线程无响应：如果主线程超过系统规定的时间无响应，就会被 Watchdog 杀掉。这时，崩溃问题对应的异常编码是0x8badf00d。关于这个异常编码，我还会在后文和你说明。
- 野指针：指针指向一个已删除的对象访问内存区域时，会出现野指针崩溃。野指针问题是需要我们重点关注的，因为它是导致App崩溃的最常见，也是最难定位的一种情况。关于野指针等内存相关问题，我会在第14篇文章“临近 OOM，如何获取详细内存分配信息，分析内存问题？”里和你详细说明。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI643alLPLydjib7OdVw87Q7Zx7O2tc1FYLpHKDO2QsK5bZul6ILNiamqANSgN4JdXzAhehKEKzO9jA/132" width="30px"><span>Geek_hercwz</span> 👍（26） 💬（5）<div>文中所讲的crash捕获只说了针对信号的，基本都是需要内核操作的一些才会以信号的形式给到进程，而oc自己也有定义一些并没深入到内核的一些exception，这些是通过注册exceptionhandle来进行捕获的，所以crash的收集应该是分两块，只说信号这一种是不够完整的</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2d/e8/d53cc6ee.jpg" width="30px"><span>Lotty周小鱼</span> 👍（9） 💬（1）<div>有个小小的建议，希望戴老师以后贴出的代码片段写一下来源或者源码链接，这样方便查看的时候快速翻阅上下文。</div>2019-04-25</li><br/><li><img src="" width="30px"><span>Hiuzi</span> 👍（3） 💬（1）<div>戴老师，有没有办法在一个项目了集成某个第三方sdk的两个版本？最近被admob sdk坑惨了，一个月发了4个版本都是修复bug的，我想更新下如果有闪退只能回退老版本了，回退老版本只能发版解决了，有没有不发版的方案解决这个问题呢？</div>2019-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoYBX95GZxEdKz9LQJVwohUiaRxNge5WpHRbeOC2tGc2rsdpfYKCTKdQicBn8MvSrlZTX7HY2jS3YFA/132" width="30px"><span>青冈</span> 👍（2） 💬（3）<div>戴老师，bugly针对应用进入后台被系统强杀也算是一种crash。您告诉我是后台工作超时，那这种情况的话我是应该在DidEnterBackground这种函数中做什么处理；还是在bugly中做什么配置，不捕捉把这种情况下的crash呢?  app进入后台之后，bugly抓捕crash的名称是 SEGV 是 segmentation violation 的缩写，是当一个进程执行了一个无效的内存引用，或发生段错误时发送给它的信号。这种的话，我应该</div>2019-04-12</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（1） 💬（1）<div>“先要找到它们的阈值，然后在临近阈值时还在执行的后台程序”其实不一定非要是在后台吧？
</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（0） 💬（2）<div>crash中是否有明确的标识显示是由于哪个三方库引起的吗？</div>2019-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoYBX95GZxEdKz9LQJVwohUiaRxNge5WpHRbeOC2tGc2rsdpfYKCTKdQicBn8MvSrlZTX7HY2jS3YFA/132" width="30px"><span>青冈</span> 👍（0） 💬（1）<div>Bugly中，针对应用进入后台被系统强杀也算是一种crash。这种怎么处理呢？</div>2019-04-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLB4OXWgz6l6IiaXKjABEU1iagBItV04ZnLicm4Aczxme80y2NFhdyn71x9VGyN7oXAQfVyPzY3c4ibYQ/132" width="30px"><span>王强😄😄😄😁</span> 👍（0） 💬（1）<div>戴铭老师，主线程无响应 这个可以提前讲吗，最近工程需要到这个地方的知识，谢谢戴铭老师。</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/66/57/f76f20b6.jpg" width="30px"><span>小前端</span> 👍（0） 💬（3）<div>文中说Crash率一般是crash次数与启动次数的比值？是说我一天打开100次app，crash了两次，所以是2个点？我觉得是不是用DAU作为分母更合适？</div>2019-04-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqzYdgPK7wApOch4BlROWdiarexic8KmhqBEH2IicFj93HzqcwPSn5KpKjptraCVZ4AMs9bWeQglIorQ/132" width="30px"><span>Dude</span> 👍（0） 💬（1）<div>Bugly中在哪可以看到异常编码？</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/cc/5ff05eb3.jpg" width="30px"><span>WeZZard</span> 👍（12） 💬（1）<div>爆棧也可以引起崩潰。看了很多 iOS 面試的鏈表題答案都是單純用的自動引用計數管理後繼節點，這種做法下鏈表長到數萬後一析構就會崩，原因就是自動引用計數引起的鏈錶各節點鏈式析構所導致的爆棧。</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（10） 💬（1）<div>老师，我是做SDK，要如何从捕获的日志中区分出来哪些是我的SDK的，哪些是主端APP的，哪些是其他Framwork。目前了解的，动态库收集的日志会有库信息，静态库收集到的信息都是APP的名字。。拜求老师指导下。</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0e/a7/9b79c245.jpg" width="30px"><span>null</span> 👍（7） 💬（0）<div>1. 测试后台执行联调时间时，不能是调试状态。必须断开xcode
2. beginBackgroundTaskWithExpirationHandler与endBackgroundTask是成对出现的。如果不成对出现，5s app会被杀掉。
3.正确写法:yourTask应该放在beginBackgroundTaskWithExpirationHandler前调用,而不是block块
 [self yourTaskWithApplication:application];
    self.backgroundTaskIdentifier = [application beginBackgroundTaskWithExpirationHandler:^(void) {
        [application endBackgroundTask:self.backgroundTaskIdentifier];
        self.backgroundTaskIdentifier = UIBackgroundTaskInvalid;
    }];
4. 我们可以借助 控制台 来判断app是否还在执行，日志是否还在打印
</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/ba/cae2ed38.jpg" width="30px"><span>yehot</span> 👍（7） 💬（6）<div>使用 registerSignalHandler 和handleSignalHandler 是能够捕获到异常。
但是，这个时候 app 已经立即要 crash 了。捕获的异常怎么才能确保能够持久化到沙盒呢？写入文件的代码是没法保证在 crash 前正常执行完的吧！</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/37/a2/045733b3.jpg" width="30px"><span>Adam</span> 👍（6） 💬（0）<div>@Mhy
1. ‘If your app targets iOS 9.0 and later or OS X v10.11 and later, you don&#39;t need to unregister an observer in its deallocation method。’ 在9.0之前需要手动remove 观察者，如果没有移除会出现观察者崩溃情况。
2. NSNotification 有同步、异步、聚合发送等线程问题，不同的线程处理不好就可能出现崩溃，情况比较多可以参考一些资料。</div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a6/5e/0d0a21c4.jpg" width="30px"><span>Mhy</span> 👍（5） 💬（1）<div>请问关于NSNotification线程问题能大致的讲一下吗 </div>2019-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/9e/7a6e6442.jpg" width="30px"><span>一纸丶荒年</span> 👍（4） 💬（1）<div>老师 您好 , 我 想知道的是  你讲这一篇文章 没有确切的解决问题吖, 我想了解的是  怎么来解读那些 堆栈信息. 那些崩溃日志, 都看不懂的.</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/22/c6ff6e02.jpg" width="30px"><span>will</span> 👍（3） 💬（0）<div>老师，我这个对吗，我看了，系统刚好在快3分钟到时候执行打印线程堆栈信息
- (void)applicationDidEnterBackground:(UIApplication *)application {
    UIApplication  *app = [UIApplication sharedApplication];
    __block UIBackgroundTaskIdentifier bgTask = 0;
    
    NSLog(@&quot;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&quot;);
    
    
    bgTask = [app beginBackgroundTaskWithExpirationHandler:^{
        NSLog(@&quot;&lt;&lt;&lt;&lt;&lt;&lt;&quot;);
        NSLog(@&quot;线程堆栈信息：%@&quot;,[NSThread callStackSymbols]);
        if (bgTask != UIBackgroundTaskInvalid) {
            [app endBackgroundTask:bgTask];
            bgTask = UIBackgroundTaskInvalid;
        }
        
    }];
}</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/1b/40293181.jpg" width="30px"><span>鼠辈</span> 👍（3） 💬（0）<div>- (void)applicationDidEnterBackground:(UIApplication *)application {
    self.backgroundTaskIdentifier = [application beginBackgroundTaskWithExpirationHandler:^( void) {
        [self yourTask];
    }];
}
这个代码中的yourTask，是后台申请3分钟之后，才会调用的吧，这个时候如果没有执行完,我试了不会崩溃。求解释</div>2019-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mJsLrs6JP47z0lZCsPKyIicWYcolVZ0ZuMicsefoiaFfPbf5zcsV2vtOw7zHsgq4UzZqwpSRdwJB6ic102icm9m824Q/132" width="30px"><span>小敏</span> 👍（2） 💬（0）<div>老师，Pl和友盟冲突怎么解决？</div>2020-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/45/aaad1f9a.jpg" width="30px"><span>周小明</span> 👍（2） 💬（4）<div>打印到了 1000+ 超过了10 分钟都没有 kill。请问是怎么回事呢？

```` objc
- (void)applicationDidEnterBackground:(UIApplication *)application {
    [application beginBackgroundTaskWithExpirationHandler:^{
        __block int i = 1;
        dispatch_source_t timer = dispatch_source_create(DISPATCH_SOURCE_TYPE_TIMER, 0, 0, dispatch_get_main_queue());
        dispatch_source_set_timer(timer, DISPATCH_TIME_NOW, 1ull * NSEC_PER_SEC, 0 * NSEC_PER_SEC);
        dispatch_source_set_event_handler(timer, ^{
            NSLog(@&quot;%d&quot;,i);
            i++;
            if (i &gt; 60*100 + 5) {
                dispatch_source_cancel(timer);
            }
            
        });
        dispatch_resume(timer);
        
    }];
}

````</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/2c/b0793828.jpg" width="30px"><span>ssala</span> 👍（2） 💬（0）<div>我们采用的fabric监控APP crash问题，但是有些crash的堆栈完全看不出头绪，千奇百怪。</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6b/b1/32cb2393.jpg" width="30px"><span>小袋子</span> 👍（1） 💬（0）<div>建议要自己实现 crash 日志采集系统的同学可以参考 KSCrash，另外做 SDK 的同学要实现一套收集 SDK 相关的 crash，真的是世纪难题，我能想到的方法就是用 hook 的方式实时记录 SDK 的调用栈， crash 的时候上传，辅助排查。另外可以将 SDK 的业务都放在一个带有 SDK 标识的 GCD 队列中，这样崩溃日志会明确指向 SDK，省得无法确定问题的归属方。（找客户要符号表真的很困难）</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/cb/5e79c6ed.jpg" width="30px"><span>(Jet)黄仲平</span> 👍（1） 💬（2）<div>戴老师好，我最近有一个困惑，就是我们公司计划做一个自己的“crash监控系统”。其中有一个很重要的目标是要实现crash日志，能定位到责任人，然后进行快速响应。
目前我个人对这件事的解决思路如下：
1. 收集crash日志，并上传日志到服务器上；
2. 通过解析git 库的提交日志，对代码文件与作者与进行关连并把日志提交到服务器；
3.  发生crash时，通过把错误堆栈信息与符号表(dysm)进行匹配，找到堆栈信息里含特定前缀的文件名。进行责任人匹配；
第一个问题：以上是我的解决思路。不知道戴老师是否也是这种思路？
第二个问题：在上面的第一步日志收集时是通过 文中“handleSignalException”方法来收集？还是通过PLCrashReporter 来进行收集？
第三个问题：dysm 在解析堆栈信息时的工作原理有无相关文章 进行介绍；

望老师百忙之中帮忙答复，不胜感激。
</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/d6/abb7bfe3.jpg" width="30px"><span>易若风云</span> 👍（1） 💬（1）<div>戴老师，问一下，oc引起的崩溃，如数组越界，为什么没有信号产生呢？那这个崩溃是从哪里发出的？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/93/28bbf22e.jpg" width="30px"><span>CoderJJMa</span> 👍（1） 💬（0）<div>- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    _timer = [NSTimer scheduledTimerWithTimeInterval:1 target:self selector:@selector(repeater) userInfo:nil repeats:YES];
    return YES;
}

-(void)repeater{
    
    NSLog(@&quot;%s&quot;,__func__);
    
}

- (void)applicationDidEnterBackground:(UIApplication *)application {
    
    NSLog(@&quot;===== : applicationDidEnterBackground&quot;);
    NSLog(@&quot;begin=============&quot;);

  self.bgIdentify = [application beginBackgroundTaskWithExpirationHandler:^{
        [self endBack];
    }];
}

-(void)endBack{
    
    NSLog(@&quot;end=============&quot;);
    NSLog(@&quot;callStackSymbols : %@&quot;,[NSThread callStackSymbols]);

    [[UIApplication sharedApplication] endBackgroundTask:self.bgIdentify];
    self.bgIdentify = UIBackgroundTaskInvalid;
}</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ab/e5/b272c773.jpg" width="30px"><span>Damon</span> 👍（0） 💬（0）<div>上面有说使用Background Task监控后台崩溃，那如果不用Background Task的话，如何监控是否后台崩溃呢？</div>2023-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f7/43/7e9c6434.jpg" width="30px"><span>mk_objc</span> 👍（0） 💬（0）<div>没讲到重点</div>2022-08-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKyibtHpR7gUQwQyDnbQO5pODsRumWTMfyCeP0SyIJicJxNggANSGXibYJia35n2a4Xayb8LpicyPIicERQ/132" width="30px"><span>NPC</span> 👍（0） 💬（0）<div>戴铭老师，我想请教一下，目前bugly有什么crash是无法捕获到的</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/88/e3/1fb72807.jpg" width="30px"><span>sky</span> 👍（0） 💬（0）<div>完整的异常编码 老师，文中这个链接打不开了，其他地方还可以看吗</div>2021-07-01</li><br/>
</ul>