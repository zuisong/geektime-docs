你好，我是LMOS。

在前面的课程中，我们已经写好了Cosmos的进程管理组件，实现了多进程调度运行，今天我们一起探索Linux如何表示进程以及如何进行多进程调度。

好了，话不多说，我们开始吧。

## Linux如何表示进程

在Cosmos中，我们设计了一个thread\_t数据结构来代表一个进程，Linux也同样是用一个数据结构表示一个进程。

下面我们先来研究Linux的进程数据结构，然后看看Linux进程的地址空间数据结构，最后再来理解Linux的文件表结构。

### Linux进程的数据结构

Linux系统下，把运行中的应用程序抽象成一个数据结构task\_struct，一个应用程序所需要的各种资源，如内存、文件等都包含在task\_struct结构中。

因此，task\_struct结构是非常巨大的一个数据结构，代码如下。

```
struct task_struct {
    struct thread_info thread_info;//处理器特有数据 
    volatile long   state;       //进程状态 
    void            *stack;      //进程内核栈地址 
    refcount_t      usage;       //进程使用计数
    int             on_rq;       //进程是否在运行队列上
    int             prio;        //动态优先级
    int             static_prio; //静态优先级
    int             normal_prio; //取决于静态优先级和调度策略
    unsigned int    rt_priority; //实时优先级
    const struct sched_class    *sched_class;//指向其所在的调度类
    struct sched_entity         se;//普通进程的调度实体
    struct sched_rt_entity      rt;//实时进程的调度实体
    struct sched_dl_entity      dl;//采用EDF算法调度实时进程的调度实体
    struct sched_info       sched_info;//用于调度器统计进程的运行信息 
    struct list_head        tasks;//所有进程的链表
    struct mm_struct        *mm;  //指向进程内存结构
    struct mm_struct        *active_mm;
    pid_t               pid;            //进程id
    struct task_struct __rcu    *parent;//指向其父进程
    struct list_head        children; //链表中的所有元素都是它的子进程
    struct list_head        sibling;  //用于把当前进程插入到兄弟链表中
    struct task_struct      *group_leader;//指向其所在进程组的领头进程
    u64             utime;   //用于记录进程在用户态下所经过的节拍数
    u64             stime;   //用于记录进程在内核态下所经过的节拍数
    u64             gtime;   //用于记录作为虚拟机进程所经过的节拍数
    unsigned long           min_flt;//缺页统计 
    unsigned long           maj_flt;
    struct fs_struct        *fs;    //进程相关的文件系统信息
    struct files_struct     *files;//进程打开的所有文件
    struct vm_struct        *stack_vm_area;//内核栈的内存区
  };
```

为了帮你掌握核心思路，关于task\_struct结构体，我省略了进程的权能、性能跟踪、信号、numa、cgroup等相关的近500行内容，你若有兴趣可以自行[阅读](https://elixir.bootlin.com/linux/v5.10.23/source/include/linux/sched.h#L640)，这里你只需要明白，在内存中，**一个task\_struct结构体的实例变量代表一个Linux进程**就行了。

### 创建task\_struct结构
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（6） 💬（1）<div>三、调度器数据结构
sched_class结构，通过一组函数指针描述了调度器；
__end_sched_classes，优先级最高
stop_sched_class，停止调度类
dl_sched_class，最早截至时间调度类
rt_sched_class，实时调度类
fair_sched_class，公平调度调度类
idle_sched_class，空转调度类
__begin_sched_classes，优先级最低

调度器的优先级，是编译时指定的，通过__begin_sched_classes和__end_sched_classes进行定位；

四、CFS调度
cfs调度算法，调度队列为cfs_rq，其整体是一个红黑树，树根记录在tasks_timeline中；
cfs调度器，根据一个进程权重占总体权重的比例，确定每个进程的CPU时间分配比例；而这个权重，开放给程序员的是一个nice值，数值越小，权重越大；

同时，即不能让进程切换过于频繁，也不能让进程长期饥饿，需要保证调度时间：
当进程数小于8个时，进程调度延迟为6ms，也就是每6ms保证每个进程至少运行一次；
当进程数大于8个时，进程延迟无法保证，需要确保程序至少运行一段时间才被调度，这个时间称为最小调度粒度时间，默认为0.75ms；

cfs中，由于每个进程的权重不同，所以无法单纯的通过进程运行时间来对进程优先级进行排序。所以将进程运行时间，通过权重换算，得到了一个进程运行的虚拟时间，然后通过虚拟时间，来对进程优先级进行排序。此时，红黑树的排序特性就充分发挥了，哪个进程的虚拟时间最小，就会来到红黑树的最左子节点，进行调度时，从左到右进行判断就好了。

这个时间又是如何刷新呢：
Linux会有一个scheduler_tick定时器，给调度器提供机会，刷新CFS队列虚拟时间
scheduler_tick-&gt;rq.curr.sched_class.task_tick，对应到CFS调度器，就是task_tick_fair
task_tick_fair-&gt;entity_tick
-&gt;update_curr，更新当前进程调度时间
-&gt;check_preempt_tick，根据实际运行时间、最小调度时间、虚拟时间是否最小等，判断是否要进行调度，如果需要调度则打标记

Linux进行进程调度时，调用schedule-&gt;__schedule
-&gt;pick_next_task
A、首先尝试pick_next_task_fair，获取下一个进程
B、如果获取失败，就按调取器优先级，依次尝试获取下一个进程
C、如果全部获取失败，就返回idel进程
-&gt;context_switch，如果获取到了新的进程，进行进程切换

其中，pick_next_task_fair-&gt;pick_next_entity，其实就是按红黑树从左到右尝试反馈优先级最高的进程；
然后，当前进程被切换时，也会更新虚拟时间，会在CFS红黑数中比较右侧的地方找到自己的位置，然后一直向左，向左，直到再次被调度。</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（5） 💬（1）<div>一、进程数据结构
每个CPU有一个rq结构，描述进程运行队列，其中：
A、cfs_rq、rt_rq、dl_rq，分别包含了公平调度、实时调度、最早截至时间调度算法相关的队列
B、记录了当前CPU的，正在运行的进程、空转进程、停止进程等；
C、每个进程用一个task_struct结构描述；

task_struct结构包括：
sched_entity结构，描述调度实体；
files_struct 结构，描述进程打开的文件；
mm_struct结构，描述一个进程的地址空间的数据结构；其中包括，vm_area_struct 结构，描述一段虚拟地址空间

二、fork创建一个进程
调用fork
-&gt;_do_fork
-&gt;-&gt;_do_fork首先调用复制进程copy_process
-&gt;-&gt;-&gt;调用了一系列的copy和初始化函数：dup_task_struct、copy_creds、copy_semundo、copy_files、copy_fs、copy_sighand、copy_signal、copy_mm、copy_namespaces、copy_io、copy_thread、copy_seccomp
-&gt;-&gt;_do_fork然后调用wake_up_new_task，初始化并准备好第一次启动，进入runqueue

其中，_do_fork-&gt;copy_process-&gt;dup_task_struct
A、alloc_task_struct_node，分配结构体
alloc_task_struct_node-&gt;kmem_cache_alloc_node-&gt;kmem_cache_alloc-&gt;slab_alloc-&gt;接上了之前的内容
B、alloc_thread_stack_node，分配内核栈
alloc_thread_stack_node-&gt;alloc_pages_node-&gt;__alloc_pages_node-&gt;__alloc_pages-&gt;__alloc_pages_nodemask-&gt;接上了之前的内容
C、arch_dup_task_struct复制task_struct
D、setup_thread_stack设置内核栈

其中，_do_fork-&gt;copy_process-&gt;copy_mm-&gt;dup_mm
A、allocate_mm，分配内存
B、memcpy，结构拷贝
C、mm_init，mm初始化
D、dup_mmap，mmap拷贝

其中，_do_fork-&gt;copy_files-&gt;dup_fd
kmem_cache_alloc，分配内存
copy_fd_bitmaps，拷贝fd位图数据</div>2021-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（16） 💬（1）<div>不是一回事。进程优先级由 nice 值表示，nice 值越好，优先级越小，只会导致该进程占用 CPU 的时间越少，而调度优先级则表示该进程获得调度机会的多寡。

这篇 linux 进程调度文章写的实在是太好了，一篇值回票价！</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（9） 💬（1）<div>这俩可不是一个概念：
进程优先级越高，占用CPU时间越长；
调度优先级越高，调度系统选中它的概率就越大。</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/d3/08/ffd93029.jpg" width="30px"><span>太阳</span> 👍（7） 💬（1）<div>linux只有进程没有线程吗？那我们在代码创建线程底层如何实现的？全局变量可以多线程共享。</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ef/fa/5e9f3dc9.jpg" width="30px"><span>驰往</span> 👍（3） 💬（3）<div>进程优先级以cfs为例，nice值越低，优先级越高，vruntime就走的越慢，从而导致实际占用cpu的时间越长；调度器类优先级越高，则调度的时候优先选择优先级高的调度器执行该调度算法找下一个要切换的进程，如果没有找到，就遍历下一个的调度算法。第一次留言写这么多字，不知道这样理解对不对。还望指出不对之处~</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（1） 💬（1）<div>看的书也没这篇文章讲的好， 老师出一本linux相关的书吧</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（0） 💬（1）<div>老师你好，我有关于这么几个关于进程切换的疑问：
一、在linux中，task_struct应该是在进程的内核地址空间中。那么在进程切换的时候，每个进程的task_struct对应的物理页面应该都不一样，所以在内核地址空间中，关于task_struct的页表项也会被切换对吗？但是很多书上都有一个说法：所有进程的内核地址空间的映射都是一样的，这样存在矛盾吗？
二、每个进程的task_struct，都是在内核线性映射对应的物理内存中分配对吗？还是可以在物理内存的任何位置？</div>2021-12-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ia5olchDzerJDeAzoY4XZrEOmqhjDJrO6ZfQU8CjWmkxwhtM6fwc16nq7Jpqr4t9ILlDSQjKHcogBpXiaIuW4IIA/132" width="30px"><span>一君</span> 👍（0） 💬（1）<div>彭老师，文章中提到“Linux是同时支持多个进程调度器的，不同的进程挂载到不同的运行队列中”，那么是由谁决定进程挂载到哪一个运行队列了？</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/d3/a9/2b84cc97.jpg" width="30px"><span>乡村爱情代言人-刘能</span> 👍（0） 💬（2）<div>彭工，学习了王爽的汇编再学c语言基础 能否学习你这门课</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（0） 💬（2）<div>进程的运行时间和调度时间居然是长达微秒级别，我一直以为是比纳秒级更小的时间单位</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/05/b8e95caa.jpg" width="30px"><span>CIH</span> 👍（0） 💬（0）<div>每个核只能从自己的rq中选择一个进程吗，不能从其他核的rq中选择吗？那么有没有可能进程A先运行在0核上，然后又运行在1核上啊？</div>2023-11-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eohMx1lpjJc5aYyM7vJmHbs3T1O7glNkhMESUjeiaCr2GuYdmGB1vKfBqH6V9osDuxwC07cp4ps0eA/132" width="30px"><span>bomber</span> 👍（0） 💬（1）<div>彭老师,CFS 解释的真好能看懂,但是还有一个问题,linux 中是基于进程调度这个概念来实现的算法,那像时间片、短任务优先之类的调度算法实现了吗?</div>2023-02-21</li><br/>
</ul>