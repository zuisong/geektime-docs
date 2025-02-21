你好，我是戴铭。今天我们来聊聊，临近OOM，如何获取详细的内存分配信息，分析内存问题的话题。

OOM，是Out of Memory的缩写，指的是App占用的内存达到了iOS系统对单个App占用内存上限后，而被系统强杀掉的现象。这么说的话，OOM其实也属于我们在第12篇文章“[iOS 崩溃千奇百怪，如何全面监控？](https://time.geekbang.org/column/article/88600)”中提到的应用“崩溃”中的一种，是由iOS的Jetsam机制导致的一种“另类”崩溃，并且日志无法通过信号捕捉到。

JetSam机制，指的就是操作系统为了控制内存资源过度使用而采用的一种资源管控机制。

我们都知道，物理内存和 CPU 对于手机这样的便携设备来说，可谓稀缺资源。所以说，在iOS 系统的虚拟内存管理中，内存压力的管控就是一项很重要的内容。

接下来，我就跟你介绍一下如何获取内存上限值，以及如何监控到App因为占用内存过大而被强杀的问题？

## 通过 JetsamEvent 日志计算内存限制值

想要了解不同机器在不同系统版本的情况下，对 App 的内存限制是怎样的，有一种方法就是查看手机中以 JetsamEvent 开头的系统日志（我们可以从设置-&gt;隐私-&gt;分析中看到这些日志）。

在这些系统日志中，查找崩溃原因时我们需要关注 per-process-limit 部分的 rpages。rpages 表示的是 ，App 占用的内存页数量；per-process-limit 表示的是，App 占用的内存超过了系统对单个App 的内存限制。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/3f/1b/40293181.jpg" width="30px"><span>鼠辈</span> 👍（3） 💬（2）<div>info.resident_size这个获取的内存和xcode上显示的内存是对不上的。不知道您怎么看这个问题？</div>2019-04-11</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（2） 💬（1）<div>线程使用优先级时，CPU 占用多的线程的优先级会被降低。这句话怎么读不懂呢？

利用didReceivedMemoryWarning 这个代理时间，看得我一愣。。应该是代理事件，我这算不算鸡蛋里面挑骨头？

task_infk的使用需要导入&lt;mach&#47;mach.h&gt; 

最后一段意思是，系统通过malloc_logger来统计并管理内存的分配情况？</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（0） 💬（1）<div>当系统还剩多少内存时，会发出内存不足的通知。</div>2019-06-25</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（0） 💬（1）<div>系统在强杀App前，会先做优先级判断。意思是：如果优先级高的话，本来会强杀的也不强杀了，而去强杀那些没有达到limit的进程？</div>2019-04-13</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（0） 💬（1）<div>didReceivedMemory 动态获取内存值的方法，没有找到啊 大佬能说一下吗？</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/ba/23c9246a.jpg" width="30px"><span>mαnajay</span> 👍（0） 💬（1）<div>hook malloc_logger aop收集日志，然后在OOM那6秒内收集所有内存分配信息，然后在再次启动应用时 上报这两部分日志吗？ 
oom那一刻是指的哪个时机，接受内存警告？ didReceiveMemoryWarning 中判断 是否靠近 limit吗 </div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/a7/374e86a7.jpg" width="30px"><span>欢乐的小马驹</span> 👍（17） 💬（0）<div>我建议，以后写这样的专栏，最后把所有参考的原始资料都下。你觉得呢？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a6/40/6518a188.jpg" width="30px"><span>白开了杯水</span> 👍（16） 💬（1）<div>一直不知道内存分配最大值获取和怎么获取当前内存分配，看了文章豁然开朗，想问的是，老师这些知识都是通过分析源码得来的吗？</div>2019-04-11</li><br/><li><img src="" width="30px"><span>drunkenMouse</span> 👍（10） 💬（0）<div>iOS通过堆栈管理所有的app进程，通过一个优先级最高的线程去监控系统内存的压力，还有一个快速对照表记录所有app的内存使用情况。如果内存有压力了，就按照优先级去释放优先级低还使用内存多的。

所以app得内存阈值是没有固定大小的。我一直以为每个app可以使用的内存大小是固定的。。</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ea/36/7d088c63.jpg" width="30px"><span>D</span> 👍（6） 💬（0）<div>腾讯的OOMDetector就是干这个事的https:&#47;&#47;github.com&#47;Tencent&#47;OOMDetector</div>2021-08-16</li><br/><li><img src="" width="30px"><span>我唔知点死啊</span> 👍（4） 💬（2）<div>fishhook初学者提问：
关于fishhook malloc_logger，在libmalloc中找到malloc_logger是一个结构体：
typedef void(malloc_logger_t)(uint32_t type,
		uintptr_t arg1,
		uintptr_t arg2,
		uintptr_t arg3,
		uintptr_t result,
		uint32_t num_hot_frames_to_skip);

fishhook malloc_logger没有任何作用，然后在_malloc_initialize方法里面，找到这句malloc_logger = __disk_stack_logging_log_stack;
fishhhok __disk_stack_logging_log_stack同样不起作用，现在无从下手，请指教。

我的fishhook方法如下：
static void (*original_disk_stack_logging_log_stack)(uint32_t type_flags,
                               uintptr_t zone_ptr,
                               uintptr_t arg2,
                               uintptr_t arg3,
                               uintptr_t return_val,
                                  uint32_t num_hot_to_skip);
void new_disk_stack_logging_log_stack(uint32_t type_flags,
                               uintptr_t zone_ptr,
                               uintptr_t arg2,
                               uintptr_t arg3,
                               uintptr_t return_val,
                               uint32_t num_hot_to_skip) {
    NSLog(@&quot;========== __disk_stack_logging_log_stack ==========&quot;);
}

        struct rebinding malloc_logger_rebinding = { &quot;__disk_stack_logging_log_stack&quot;, original_disk_stack_logging_log_stack, (void *)&amp;original_disk_stack_logging_log_stack};
        rebind_symbols((struct rebinding[1]){malloc_logger_rebinding}, 1);</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/61/68462a07.jpg" width="30px"><span>无名</span> 👍（3） 💬（2）<div>我问这个问题的原因是看到SDWebImage 2.6版本的源码中释放内存缓存有两种方式：
第一种：监听到内存不足时，释放所有内存缓存；
第二种：当系统剩余内存小于12M时，释放内存缓存。

刚开始版本是没有加第二种判断的。我的疑问是加上第二种判断有必要吗？如果有必要的话，那么就是，当系统只剩12M内存都还没有触发内存不足的通知。

所以说这个内存不足通知是否在应用能给它分配的最大内存都全部使用完了才发出通知还是？
如：当前app能使用的最大内存为2G，系统总共内存为4G。那是否说不管系统是否还剩余多少内存，只要app的内存达到2G就发出内存警告通知？还是说快到2G,如达到最大可用内存的百分之95以上就发出内存警告通知。有哪里可以看到这个值吗？</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3c/b9/42b228f8.jpg" width="30px"><span>徐秀滨</span> 👍（3） 💬（0）<div>老师，我没找到malloc_logger这个方法，没法hook，咋搞？</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/32/f1/54575096.jpg" width="30px"><span>Master</span> 👍（2） 💬（1）<div>有个疑问，就算 hook 了malloc_logger ，知晓了内存分配地址和大小，又如何知道是代码中哪块或者哪个对象申请的呢？望各位大佬不吝赐教！</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4a/51/02678317.jpg" width="30px"><span>Jaker</span> 👍（2） 💬（1）<div>接上面的问题，问一下老师，task_vm_info_data_t的phys_footprint 打印输出的内存值和xcode的显示内存还是不一致啊，这是怎么回事，望解惑，谢谢。</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/38/77/5849fbcf.jpg" width="30px"><span>天空很蓝</span> 👍（1） 💬（1）<div>出现OOM前一定会出现Memory Warning么？这个应该是不一定吧大佬；既然不一定的话那上面三种情况就都不能很好的获取到邻近OOM的时候内存的分配信息吧；还有其他更好的方式吗？还是我理解的有问题呢？麻烦知道的大佬解答一下谢谢！</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/22/c6ff6e02.jpg" width="30px"><span>will</span> 👍（1） 💬（0）<div>监控内存分配的核心，在于使用libmalloc库的malloc_logger指针实现的</div>2020-05-22</li><br/><li><img src="" width="30px"><span>RichardJ</span> 👍（1） 💬（0）<div>小结里说到访问未分配内存、向只读内存进行写操作的问题，戴老师可以举些例子说明下这两种情况怎么排查原因吗？</div>2019-08-20</li><br/><li><img src="" width="30px"><span>Calabash_Boy</span> 👍（1） 💬（2）<div>老师好,读完后有几个问题不得其解:
(1) 在相同的设备和系统版本下,每个App的内存限制是不一样的么?我查看了手机的jetsamEvent,在per-process-limit中发现一个rpages是196.
(2) 在vm_pressure_monitor线程的检测下,发现某App有了内存压力(理解为即将达到内存限制),然后会给该App发通知,然后您又讲到了优先级机制,这就有疑惑了,当某个App有压力的时候,是强杀这个App呢还是根据优先级去强杀后台的App呢?
(3) 在测试struct mach_task_basic_info info;这段代码的时候,编译会报错Definition of &#39;mach_task_basic_info&#39; must be imported from module &#39;Darwin.Mach.task_info&#39; before it is required,是我没有导入某个头文件么?</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/a0/75cdae30.jpg" width="30px"><span>浩</span> 👍（1） 💬（0）<div>一直不知道内存分配最大值获取和怎么获取当前内存分配，看了文章豁然开朗，想问的是，老师这些知识都是通过分析源码得来的吗？</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/0b/2ccf7908.jpg" width="30px"><span>...</span> 👍（0） 💬（0）<div>hook 内存分配的性能开销应该很大 这块线上环境怎么处理呢？</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/30/d3/b3516304.jpg" width="30px"><span>夜空繁星</span> 👍（0） 💬（0）<div>除了膜拜，没别的。</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/dd/5d473145.jpg" width="30px"><span>亡命之徒</span> 👍（0） 💬（0）<div>线上使用这种方式监控内存，苹果审核会通过嘛</div>2019-06-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epzwbJGbUmgEC77J6QY6A5pLPdPbw7sqk4DcsHK8qPw7OiaiaMD7pjzb8uHlkY5uLZRibWVvPDDAgM5A/132" width="30px"><span>mersa</span> 👍（0） 💬（0）<div>怎么知道谁调用了 malloc，来指导对应的堆栈信息</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/43/63bdc516.jpg" width="30px"><span>二木又土</span> 👍（0） 💬（0）<div>JetsamEvent文件中搜索rpages，为什么有很多值，不同app能使用的最大内存大小是不一样的？</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/eb/2394e520.jpg" width="30px"><span>Hy</span> 👍（0） 💬（0）<div>👌</div>2019-04-12</li><br/>
</ul>