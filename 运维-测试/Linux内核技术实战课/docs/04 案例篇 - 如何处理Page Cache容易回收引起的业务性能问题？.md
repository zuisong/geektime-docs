你好，我是邵亚方。我们在前一节课讲了Page Cache难以回收导致的load飙高问题，这类问题是很直观的，相信很多人都遭遇过。这节课，我们则是来讲相反的一些问题，即Page Cache太容易回收而引起的一些问题。

这类问题因为不直观所以陷阱会很多，应用开发者和运维人员会更容易踩坑，也正因为这类问题不直观，所以他们往往是一而再再而三地中招之后，才搞清楚问题到底是怎么回事。

我把大家经常遇到的这类问题做个总结，大致可以分为两方面：

- 误操作而导致Page Cache被回收掉，进而导致业务性能下降明显；
- 内核的一些机制导致业务Page Cache被回收，从而引起性能下降。

如果你的业务对Page Cache比较敏感，比如说你的业务数据对延迟很敏感，或者再具体一点，你的业务指标对TP99（99分位）要求较高，那你对于这类性能问题应该多多少少有所接触。当然，这并不意味着业务对延迟不敏感，你就不需要关注这些问题了，关注这类问题会让你对业务行为理解更深刻。

言归正传，我们来看下发生在生产环境中的案例。

## 对Page Cache操作不当产生的业务性能下降

我们先从一个相对简单的案例说起，一起分析下误操作导致Page Cache被回收掉的情况，它具体是怎样发生的。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（10） 💬（0）<div>课后作业答案：
- 进程调用 mlock() 来保护内存，然后进程没有运行 munlock() 就退出了，在进程退出后，这部分内存还被保护吗，为什么？
这部分内容就不被保护了，评论区里有人已经给出了文档里的解释：
 Memory locks are not inherited by a child created via fork(2) and are
       automatically removed (unlocked) during an execve(2) or when the
       process terminates.
https:&#47;&#47;man7.org&#47;linux&#47;man-pages&#47;man2&#47;mlock.2.html
</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/83/abb7bfe3.jpg" width="30px"><span>奔跑的熊</span> 👍（20） 💬（2）<div>老师您好，如何观察单个应用的page cache?</div>2020-10-02</li><br/><li><img src="" width="30px"><span>Geek_162e2a</span> 👍（9） 💬（2）<div>思考题：
在进程退出之后，此部分内存不会再被保护
为什么呢，文档是这么说的������
       Memory locks are not inherited by a child created via fork(2) and are
       automatically removed (unlocked) during an execve(2) or when the
       process terminates.
https:&#47;&#47;man7.org&#47;linux&#47;man-pages&#47;man2&#47;mlock.2.html</div>2020-08-28</li><br/><li><img src="" width="30px"><span>ray</span> 👍（4） 💬（1）<div>老师您好，请问
如果使用echo 2 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches释放slab objects (includes dentries and inodes)也会释放掉page cache，那这条指令和单纯释放page cache的echo 1 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches指令的区别又在哪里呢？

谢谢老师的解答^^</div>2020-08-28</li><br/><li><img src="" width="30px"><span>从远方过来</span> 👍（4） 💬（1）<div>老师，我有几个疑问：
1. 扫描比例是怎么设置的？和zoneinfo里面的min，low，high有什么的联系么？
2. “回收到足够的内存” 是指回收到high水位还是满足这一次内存分配就停止了？</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（1） 💬（2）<div>请问一下邵老师，我看memory cgroup中相关的参数是这些  memory.kmem.limit_in_bytes,memory.kmem.max_usage_in_bytes,memory.usage_in_bytes,memory.soft_limit_in_bytes,memory.memsw.usage_in_bytes.memory.memsw.max_usage_in_bytes请问跟文章中memory.max, memory.high这些是怎么对应的呢？</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（1） 💬（1）<div>老师，你好，有个疑问，memory cgroup 来对它们进行保护，如何保证我要保护的数据是放在里面的呢？</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d0/d0/a6c6069d.jpg" width="30px"><span>坚</span> 👍（1） 💬（1）<div>老师好，我查看了一下 zoneinfo 其中   pages free=4497，但是min   low hight 分别为5 6 7 ，三者设置得这么接近，有这么小，是否会有什么问题呢？</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/95/a362f01b.jpg" width="30px"><span>Geek1560</span> 👍（1） 💬（1）<div>老师好，请教一个问题，当内核分配内存时，如果没有空闲页，其中slab&#47;slub部分的匿名页会调用shrink_inactive_list 函数会扫描inactive list，将不活跃的page置换到swap分区。但是swap有时几M、几百M甚至几个G，这个内核置换的机制或算法逻辑是啥？(PS本身应用程序或内核不会一次性申请几个G的内存)</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（1）<div>①”pginodesteal 是指 kswapd 之外其他线程在回收过程中，因为回收 inode 而释放的 pagecache page 个数。“------这里的”kswapd 之外其他线程“有可能就是用户业务线程吧？？
②对于java工程师，完全不懂memory cgroup 为何物。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/8b/2c81a375.jpg" width="30px"><span>好说</span> 👍（1） 💬（1）<div>老师，对于io密集型的业务，基本上大部分都是读磁盘，当带宽达到一定量级之后服务器的load会很高，但是当我执行echo &quot;1&quot;&gt;&#47;proc&#47;sys&#47;vm&#47;drop_caches后，服务器load会非常明显的下降，然后过一会就又会升上去，请问老师造成这种现象的原因是什么呢，或者老师可以提示一些排查思路吗</div>2020-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJpJXWFP3dNle88WnTkRTsEQkPJmOhepibiaTfhEtMRrbdg5EAWm4EzurA61oKxvCK2ZjMmy1QvmChw/132" width="30px"><span>唐江</span> 👍（0） 💬（1）<div>inode被回收是什么意思？</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/c5/3cdf2390.jpg" width="30px"><span>洛戈</span> 👍（0） 💬（1）<div>请问老师，使用memory cgroup怎么保护指定的关键数据呢？只能设置min来保留最小的page cache呀，那并不一定能确保关键数据在min之内吧</div>2021-04-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqtXSgThiaEiaEqqic5YIJ7v469nCM3VXiccOJ4SxbYjW91ciczuYYEzcTVtYWaWXaokZqShuLdKsXjnFA/132" width="30px"><span>Geek_b85295</span> 👍（0） 💬（1）<div>老师，关于swap请教一个问题，调整swappiness参数可以控制系统使用swap的情况。我把这个参数改成了0，也就是尽量让机器不使用swap，在echo 1 &gt; &#47;proc&#47;sys&#47;vm&#47;drop_caches 得到大量free内存的情况下，用vmstat -w 1 指标中的swap信息，还是可以看到很多的换进换出，这是为什么，谢谢老师答疑</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f2/fc/316fdc18.jpg" width="30px"><span>王一怂</span> 👍（0） 💬（1）<div>inode本身也是文件系统的概念，这里的inode应该是内存中的inode，感觉还是区分一下比较好</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/53/5c19021b.jpg" width="30px"><span>梁鹏</span> 👍（0） 💬（1）<div>邵老师 能否简单的概括一下 page cache 和 slab cache 的 关系，或者推荐一些资料</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/00/bfc101ee.jpg" width="30px"><span>Tendrun</span> 👍（0） 💬（0）<div>想到一个问题，有没有办法针对某个进程进行page cache回收呢，这样就不会影响到其他进程的性能了</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ec/ce/3ec9f1a8.jpg" width="30px"><span>颜卫</span> 👍（0） 💬（0）<div>老师，你好。看内核代码，memory.high好像不是优先回收，而是在达到这个水位后，每次申请增加一定的时延

&#47;*
 * Scheduled by try_charge() to be executed from the userland return path
 * and reclaims memory over the high limit.
 *&#47;
void mem_cgroup_handle_over_high(void)
{
    unsigned long penalty_jiffies;
    unsigned long pflags;
    unsigned int nr_pages = current-&gt;memcg_nr_pages_over_high;
    struct mem_cgroup *memcg;
    u64 start;

    if (likely(!nr_pages))
        return;

    sli_memlat_stat_start(&amp;amp;start);
    memcg = get_mem_cgroup_from_mm(current-&gt;mm);
    reclaim_high(memcg, nr_pages, GFP_KERNEL);
    current-&gt;memcg_nr_pages_over_high = 0;

    &#47;*
     * memory.high is breached and reclaim is unable to keep up. Throttle
     * allocators proactively to slow down excessive growth.
     *&#47;
    penalty_jiffies = calculate_high_delay(memcg, nr_pages);

    &#47;*
     * Don&#39;t sleep if the amount of jiffies this memcg owes us is so low
     * that it&#39;s not even worth doing, in an attempt to be nice to those who
     * go only a small amount over their memory.high value and maybe haven&#39;t
     * been aggressively reclaimed enough yet.
     *&#47;
    if (penalty_jiffies &lt;= HZ &#47; 100)
        goto out;

    &#47;*
     * If we exit early, we&#39;re guaranteed to die (since
     * schedule_timeout_killable sets TASK_KILLABLE). This means we don&#39;t
     * need to account for any ill-begotten jiffies to pay them off later.
     *&#47;
    psi_memstall_enter(&amp;amp;pflags);
    schedule_timeout_killable(penalty_jiffies);
    psi_memstall_leave(&amp;amp;pflags);

out:
    sli_memlat_stat_end(MEM_LAT_MEMCG_DIRECT_RECLAIM, start);
    css_put(&amp;amp;memcg-&gt;css);
}

是不是我少找了一些地方，回收的时候也会考虑memory.high啊？</div>2022-01-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erWEJ05DJylAxYQeo2Ua6GlPkto2uice4WD9vu9wCwBsqV1zXM8DMKMib3SlOc5L348bPHoZIOZ3zibA/132" width="30px"><span>Geek_1piyxf</span> 👍（0） 💬（0）<div>老师好，想请教下slab scanned对应用抖动的问题，生产上8C24G的机器，slab经常用到8G多，其中dentry用掉了4G左右，kmalloc-192使用了3G左右，SReclaimable占了8G的2&#47;3左右，经常看到应哟给你抖动都会伴随着很高的slab scanned值，高达100w数值，这块cache引起的问题一般如何分析？</div>2021-12-31</li><br/><li><img src="" width="30px"><span>Geek_c1d00e</span> 👍（0） 💬（0）<div>老师，我在多线程的应用里，在mmap后，用mlock锁定，可是在&#47;proc&#47;meminfo中看到的Mlocked项的大小并没有增加；这是为啥呢？</div>2021-12-08</li><br/>
</ul>