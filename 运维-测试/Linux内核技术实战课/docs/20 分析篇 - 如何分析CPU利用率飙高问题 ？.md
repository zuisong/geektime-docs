你好，我是邵亚方。

如果你是一名应用开发者，那你应该知道如何去分析应用逻辑，对于如何优化应用代码提升系统性能也应该有自己的一套经验。而我们这节课想要讨论的是，如何拓展你的边界，让你能够分析代码之外的模块，以及对你而言几乎是黑盒的Linux内核。

在很多情况下，应用的性能问题都需要通过分析内核行为来解决，因此，内核提供了非常多的指标供应用程序参考。当应用出现问题时，我们可以查看到底是哪些指标出现了异常，然后再做进一步分析。不过，这些内核导出的指标并不能覆盖所有的场景，我们面临的问题可能更加棘手：应用出现性能问题，可是系统中所有的指标都看起来没有异常。相信很多人都为此抓狂过。那出现这种情况时，内核到底有没有问题呢，它究竟在搞什么鬼？这节课我就带你探讨一下如何分析这类问题。

我们知道，对于应用开发者而言，应用程序的边界是系统调用，进入到系统调用中就是Linux内核了。所以，要想拓展分析问题的边界，你首先需要知道该怎么去分析应用程序使用的系统调用函数。对于内核开发者而言，边界同样是系统调用，系统调用之外是应用程序。如果内核开发者想要拓展分析问题的边界，也需要知道如何利用系统调用去追踪应用程序的逻辑。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（11） 💬（2）<div>邵老师，你好，有个负载高的问题，我判断是因为开的线程数过多导致的，我想请教一下是下面的这些数据是不是有说服力或者有什么手段进一步确认? 谢谢！
top
top - 18:46:33 up 186 days,  4:31,  3 users,  load average: 67.47, 55.78, 61.19
Tasks: 377 total,   1 running, 376 sleeping,   0 stopped,   0 zombie
%Cpu(s): 51.0 us, 30.2 sy,  0.0 ni,  8.0 id,  0.0 wa,  0.0 hi, 10.8 si,  0.0 st
KiB Mem : 13173332+total, 21147572 free,  6840020 used, 10374573+buff&#47;cache

grep procs_running &#47;proc&#47;stat
procs_running 70
grep procs_running &#47;proc&#47;stat
procs_running 90
grep procs_running &#47;proc&#47;stat
procs_running 119

 perf top -U
   4.41%  [kernel]          [k] system_call_after_swapgs
   3.49%  [kernel]          [k] do_select
   3.23%  [kernel]          [k] copy_user_enhanced_fast_string
   2.98%  [kernel]          [k] sysret_check
   2.78%  [kernel]          [k] __schedule
   1.82%  [kernel]          [k] __check_object_size
   1.67%  [kernel]          [k] fget_light
   1.22%  [kernel]          [k] tcp_ack
   1.21%  [kernel]          [k] __audit_syscall_exit
   1.16%  [kernel]          [k] __x86_indirect_thunk_rax
   1.15%  [kernel]          [k] tcp_poll
   1.13%  [kernel]          [k] _raw_spin_lock_irqsave
   1.12%  [kernel]          [k] __switch_to
 


 perf stat
 Performance counter stats for &#39;system wide&#39;:

     376801.028719      cpu-clock (msec)          #   31.997 CPUs utilized          
         7,323,807      context-switches          #    0.019 M&#47;sec                  
           824,699      cpu-migrations            #    0.002 M&#47;sec                  
           100,337      page-faults               #    0.266 K&#47;sec                  
   808,730,622,944      cycles                    #    2.146 GHz                    
   429,965,110,114      instructions              #    0.53  insn per cycle         
    90,908,416,046      branches                  #  241.264 M&#47;sec                  
     2,554,107,830      branch-misses             #    2.81% of all branches        

      11.776125779 seconds time elapsed
</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（3） 💬（2）<div>推荐使用 ftrace 前端 trace-cmd，直接操作 tracefs 文件略显繁琐。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（1）<div># 老师文中提到的`查看 Page Cache 的组成`这个功能,感觉很吸引人啊!

# 根据老师的提示,也只找到了这两个方式:
## [Is it possible to list the files that are cached?](https:&#47;&#47;serverfault.com&#47;a&#47;782640)
原理也比较简单:
借助`ps`找出`rss`的top10进程,然后根据`lsof`找出进程引用的文件,最后借助`linux-fincore`查看这些文件在PageCache中的信息.

感觉这个脚本也有局限性.
由于`linux-fincore`只能查看列出的文件,所以是无法查看已经不被进程占用的`Page Cache`中的文件及大小的.

## [pcstat](https:&#47;&#47;github.com&#47;tobert&#47;pcstat)
这个工具是借助`mincore`来查看的Page Cache信息,但是也是需要列出具体的文件名.

# 疑问
还是老师的这个方法好,不需要提供文件列表,也可以查看内存中都有哪些文件以及这些文件的大小.
请问,老师的这个工具有开源版本么?
</div>2020-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/6b/a52282b8.jpg" width="30px"><span>会飞的鱼</span> 👍（2） 💬（1）<div>老师好，我的服务器内核空间的cpu使用率达到了100%，重启了几次依然没有解决，然后我用top查看，没有发现cpu占用很高的进程，用execsnoop也没发现异常，然后用pidstat -w查看，发现rcu_sched的上下文切换很频繁，而且是自愿上下文切换，然后我再用perf top -g -p 9追踪，发现有schedule,finish_task_switch等系统调用，但我还是不清楚是什么原因导致的内核空间cpu使用率高，服务器上也没跑什么程序，这种情况怎么进一步解决呢？ 可以加您微信进一步求教下吗？</div>2020-11-25</li><br/><li><img src="" width="30px"><span>Geek_9bf0b0</span> 👍（1） 💬（1）<div>邵老师，关于在 sysrq 里实现显示出系统中所有 R 和 D 状态的任务的功能，我的想法是将

show_state_filter()接口的state_filter参数改成指针类型，传递参数NULL时表示显示所有进程信息，
这样避免与TASK_RUNNING冲突，代码修改量也小，也相对优雅。

-extern void show_state_filter(unsigned long state_filter);
+extern void show_state_filter(unsigned long *state_filter);

 static inline void show_state(void)
 {
- show_state_filter(0);
+ show_state_filter(NULL);
 }

 static void sysrq_handle_showstate_blocked(int key)
 {
- show_state_filter(TASK_UNINTERRUPTIBLE);
+ unsigned long filter = TASK_UNINTERRUPTIBLE;
+
+ show_state_filter(&amp;filter);
 }


然后调用unregister_sysrq_key()移除sysrq_showstate_blocked_op，
接着register_sysrq_key()接口注册定制化的op，
定制化的回调函数handle可以实现如下：
static void sysrq_handle_showstate_load(int key)
{
    unsigned long filter;

    filter = TASK_RUNNING;
    show_state_filter(&amp;filter);

    filter = TASK_UNINTERRUPTIBLE;
    show_state_filter(&amp;filter);
}

关于注册定制化的sysrq，可以通过early_param或者模块的方式。
以模块的方式注册定制化的sysrq时需要导出内核符号show_state_filter。</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/cc/0947ff0b.jpg" width="30px"><span>nestle</span> 👍（0） 💬（1）<div>老是，IO排队是不是应该看avgqu-sz这个字段？</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（1） 💬（0）<div>iotop 没有发现写 I&#47;O 的用户进程，觉得可以往上走，在文件系统层面做些分析，page 紧张的情况下，文件读写操作会变得相对慢一些。借助 BCC 现有工具 ext4slower、ext4dist（假设是 ext4 fs）分析，应该可以看到具体的用户进程。</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（1） 💬（0）<div>我是一名系统运维工程师，对内核还不太了解。但感觉这节课还是收货了很多，尤其是如何借助ftrace去做进一步分析，以及如何查看page cache中都是哪些文件及文件大小。之前只知道使用cachestat和cachetop去查看缓存命中情况。希望以后工作中能够运用上。</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/13/fb/7f31dfd4.jpg" width="30px"><span>Bin</span> 👍（0） 💬（1）<div>你好，邵老师， 这篇文文章标题写的 cpu利用率高因为系统调用的问题，而这个系统调用主要卡在io wait上，但io wait 跟cpu利用率没关系吧，cpu利用率(用户态加系统态)应该不受影响才对</div>2023-01-09</li><br/>
</ul>