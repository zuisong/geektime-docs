你好，我是戴铭。

我在前面的第12、13和14三篇文章中，和你分享了崩溃、卡顿、内存问题的监控。一旦监控到问题，我们还需要记录下问题的详细信息，形成日志告知开发者，这样开发者才能够从这些日志中定位问题。

但是，很多问题的定位仅靠问题发生的那一刹那记录的信息是不够的，我们还需要依赖更多的日志信息。

在以前公司还没有全量日志的时候，我发现线上有一个上报到服务器的由数据解析出错而引起崩溃的问题。由于数据解析是在生成数据后在另一个线程延迟执行的，所以很难定位到是谁生成的数据造成了崩溃。

如果这个时候，我能够查看到崩溃前的所有日志，包括手动打的日志和无侵入自动埋点的日志，就能够快速定位到是由谁生成的数据造成了崩溃。这些在 App 里记录的所有日志，比如用于记录用户行为和关键操作的日志，就是全量日志了。

有了更多的信息，才更利于开发者去快速、精准地定位各种复杂问题，并提高解决问题的效率。那么，**怎样才能够获取到 App 里更多的日志呢**？

你可能会觉得获取到全量的日志很容易啊，只要所有数据都通过相同的打日志库，不就可以收集到所有日志了吗？但，现实情况并没有这么简单。

一个 App 很有可能是由多个团队共同开发维护的，不同团队使用的日志库由于历史原因可能都不一样，要么是自己开发的，要么就是使用了不同第三方日志库。如果我们只是为了统一获取日志，而去推动其他团队将以前的日志库代码全部替换掉，明显是不现实的。因为，我们谁也无法确定，这种替换日志库的工作，以后是不是还会再来一次。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_97bcf5</span> 👍（17） 💬（2）<div>一般大厂的app都不会用NSLog来打印日志的，我不知道滴滴打车是否用NSLog来打印日志，所以，本文的方案并不符合生产环境。日志是需要分类的，需要压缩，需要加密，实时染色等。NSLog根本不可能完成这些功能，所以，大厂的app都有专门的日志框架。各个模块中也不会用NSLog来输出日志。</div>2019-04-13</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（2） 💬（1）<div>ASL在iOS10.0之后没法用了。所以CocoaLumberJack无法获取到所有的日志，但除了NSLog日志外，别的日志都能获取到吗？</div>2019-04-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/b4oNLTaYfCBibPibneZVz8GqiciavzhbloQicwoIMz8E9cJibjLpOmibOrWYiamKXXwqDWicWwgCZOawlOte6icJkn3iby8GQ/132" width="30px"><span>lhjzzu</span> 👍（1） 💬（1）<div>上周才第一次用CocoaLumberjack做了日志系统，并且看了fishhook的原理，这次看这篇文章就全用上了，太nice了，对两者的使用和理解更深了。哈哈😄</div>2019-04-14</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（1） 💬（1）<div>所以，几个人的小团队直接使用统一的日志库就可以了？

syslogd是一个进程，保护系统接收分发日志消息的进程？

CocoaLumberJack这段有点乱，整理了一下：

captureAslLogs方法对ASL日志的处理措施是：将日志消息转换成char * 字符串类型，然后再转成NSString类型，随后将其记录。 
记录使用DDLog：log：message：方法。
记录时需要将NSString转成DDLogMessage类型，而DDLogMessage设置了日志级别，所以转换类型后也要设置日志级别。

NSLog的日志级别是Verbose。

最后，iOS10之后，为了兼容新的统一日志系统，需要对NSLog日志的输出进行重定向。iOS10之后CocoaLumberJack获取不到NSLog的日志了？</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e9/58/397a4ab2.jpg" width="30px"><span>daniel</span> 👍（8） 💬（0）<div>static void(*orig_nslog) (NSString *format,...); 这里声明的时候是*号不是&amp;号，声明是一个对象，估计老师那边打错了
还有下面这段代码
va_list va;
    va_start(va,format);
    NSLogv(format, va);
    va_end(va);
可以换成orig_nslog(format) ，这时候我们的orig_nslog就是原来NSLog在Mach-o中的地址了，这时候可以直接拦截使用了，老师希望课里面代码可以检查仔细点再发出来，好多次直接报错，然后又找不到原因，这样挺打击人的。。。还有注释可以再清楚点</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/0b/4346a253.jpg" width="30px"><span>Ant</span> 👍（6） 💬（0）<div>温故而知新， 对我来说是反过来说的， 知新而温故。
main函数执行之前  
加载可执行文件、
加载动态链接库rebase指针调整和bind符号绑定、
运行时开始处理，
objc类注册，category注册，selector唯一性检查，
load方法，attribute修饰函数调用，
创建c++静态全局变量</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/31/db/77251f31.jpg" width="30px"><span>jimbo</span> 👍（3） 💬（0）<div>static void (&amp;orig_nslog)(NSString *format, ...); 这里是不是应该变成 static void (*orig_nslog)(NSString *format, ...);  不然报错</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cd/ff/b001b578.jpg" width="30px"><span>小赢一场</span> 👍（2） 💬（0）<div>不太明白，获取日志，怎么上传，什么时候上传日志到后台</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/8b/4c/ff8c53dc.jpg" width="30px"><span>jiang</span> 👍（1） 💬（0）<div>完成第一次作业，这样便可以无侵入的实现日志上报惹
- (void)viewDidLoad {
    [super viewDidLoad];
    [self outLog];
    [self writeMsg];

}

- (void)outLog{
    self.filePath = [NSString stringWithFormat:@&quot;%@&#47;Documents&#47;LOG&quot;, NSHomeDirectory()];
    [[NSFileManager defaultManager] createDirectoryAtPath:self.filePath  withIntermediateDirectories:YES attributes:nil error:nil];
    self.filePath = [self.filePath stringByAppendingString:@&quot;&#47;log.txt&quot;];
    [[NSFileManager defaultManager] createFileAtPath:self.filePath contents:nil attributes:nil];
    self.fileHandle =  [NSFileHandle fileHandleForWritingAtPath:self.filePath];
    int fileDesc = self.fileHandle.fileDescriptor;
    dup2(fileDesc, STDERR_FILENO);
}

int count = 0;

- (void)writeMsg{
    count ++;
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(2 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
        NSString *str = [NSString stringWithFormat:@&quot;+%d&quot;,count];
        [self writeMsg];
        NSLog(@&quot;%@&quot;,str);
    });
    
}
</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/58/f0cb60be.jpg" width="30px"><span>zhonglaoban</span> 👍（1） 💬（0）<div>所以nslog能输出日志到console.app里面是因为用了asl？</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ad/8d/3b2ac759.jpg" width="30px"><span>大年初一</span> 👍（1） 💬（0）<div>微信的 xlog 也不错</div>2019-12-21</li><br/><li><img src="" width="30px"><span>dingdongfm</span> 👍（1） 💬（0）<div>如果需要获取最终用户手机上的日志来定位问题的话，一般怎么获取日志？</div>2019-06-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epzwbJGbUmgEC77J6QY6A5pLPdPbw7sqk4DcsHK8qPw7OiaiaMD7pjzb8uHlkY5uLZRibWVvPDDAgM5A/132" width="30px"><span>mersa</span> 👍（1） 💬（0）<div>写文件不是耗电，还有影响app运行性能么。这个产线情况怎么能够保存全量日志同时性能和耗电都能最低</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/43/63bdc516.jpg" width="30px"><span>二木又土</span> 👍（1） 💬（0）<div>对App来说，网络请求使用AFNetworking，怎么把网络请求的log优雅点的过滤打印出来？另外log，在控制台还会遇到字符串太长显示被截断的问题</div>2019-04-25</li><br/><li><img src="" width="30px"><span>Geek_ecfaae</span> 👍（0） 💬（0）<div>iOS10之后，ASL已经被取代了。那磁盘监控就不能用kNotifyVFSLowDiskSpace了吧？</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/5c/ab80250d.jpg" width="30px"><span>lianleven</span> 👍（0） 💬（0）<div>老师问个问题:如果服务端几乎同时到达客户端1000条消息，这个时候该如何用多线程处理</div>2019-04-19</li><br/><li><img src="" width="30px"><span>James</span> 👍（0） 💬（1）<div>因为团队不大,项目日志采用的方式为freopen重定向stderr类型的日志到本地文件的方式,并没有引入三方库,请问这种方式有什么缺点?
另外大厂的所谓日志框架具体是怎么记录日志的?难道底层实现完全不用NSLog或print吗?</div>2019-04-18</li><br/>
</ul>