你好，我是程远。今天我想聊一聊平均负载（Load Average）的话题。

在上一讲中，我们提到过CPU Cgroup可以限制进程的CPU资源使用，但是CPU Cgroup对容器的资源限制是存在盲点的。

什么盲点呢？就是无法通过CPU Cgroup来控制Load Average的平均负载。而没有这个限制，就会影响我们系统资源的合理调度，很可能导致我们的系统变得很慢。

那么今天这一讲，我们要来讲一下为什么加了CPU Cgroup的配置后，即使保证了容器的CPU资源，容器中的进程还是会运行得很慢？

## 问题再现

在Linux的系统维护中，我们需要经常查看CPU使用情况，再根据这个情况分析系统整体的运行状态。有时候你可能会发现，明明容器里所有进程的CPU使用率都很低，甚至整个宿主机的CPU使用率都很低，而机器的Load Average里的值却很高，容器里进程运行得也很慢。

这么说有些抽象，我们一起动手再现一下这个情况，这样你就能更好地理解这个问题了。

比如说下面的top输出，第三行可以显示当前的CPU使用情况，我们可以看到整个机器的CPU Usage几乎为0，因为"id"显示99.9%，这说明CPU是处于空闲状态的。

但是请你注意，这里1分钟的"load average"的值却高达9.09，这里的数值9几乎就意味着使用了9个CPU了，这样CPU Usage和Load Average的数值看上去就很矛盾了。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIYdf5Z0Iicn5mGECKewrGxaY3sPlTEk3PcjImA7as2H7n7L6Krly8dzjwfOQIUYaZwdBBtfCuc0Sg/132" width="30px"><span>garnett</span> 👍（18） 💬（2）<div>请问老师，引入为 TASK_UNINTERRUPTIBLE 状态的进程的案例，top 输出中为什么wa使用率这一项没有增长？</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（12） 💬（4）<div>推荐 stress 压测工具：stress -c 1 -t 600

平均负载计算公式（nr_active 表示单位时间内平均活跃进程个数，每个 CPU 对应一个 运行队列 rq，rq-&gt;nr_running、rq-&gt;nr_uninterruptible 分别表示该运行队列上可运行进程、不可中断进程的个数。累积的 nr_active 再进行指数衰减平均得到最终的平均负载）

&#47;* 
* The global load average is an exponentially decaying average of nr_running +
 * nr_uninterruptible.
 *&#47;
nr_active = 0;
for_each_possible_cpu(cpu)
    nr_active += cpu_of(cpu)-&gt;nr_running + cpu_of(cpu)-&gt;nr_uninterruptible;</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/08/0287f41f.jpg" width="30px"><span>争光 Alan</span> 👍（9） 💬（4）<div>感谢分享

我想问下
1.如果出现就D进程，我为什么好的故障方法排查在等待什么吗？
2.一直有个疑问，是不是linux的进程数不能太多？太多会有很多的调度时间造成很卡？
3.容器目前每个节点官方推荐是110个pod，openshift是250个，能问下你们这边的最佳实践不引起性能下降的前提下节点最大pod是多少个吗？</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/86/fe/0fb57311.jpg" width="30px"><span>游离的鱼</span> 👍（6） 💬（2）<div>首先很感谢老师，然后我还是有一些些不太明白，第一个: 处于task_interruptible的进程，虽然它在等信号量和等待io上，但是我理解这个时候其实cpu是空闲的，为什么不把cpu资源让出来，等io完成或者有信号量时再把它放入可运行的队列中去等待调用呢，类似于回调函数那样的思想。第二个: 如果是我的机器长期平均负载过高，是不是一定是D状态的进程或线程引起的。 第三个: 我有四个cpu的机器，现有五个进程，有四个在cpu中运行，其中三个是处于运行状态，另一个是处于task_interruptable状态，也就是D状态，还有一个在排队，那这个时候的负载是不是就是5？如果除了刚刚的D状态的进程其他的进程都运行完了，负载是不是又变成1了。 第四个: 根据老师的定义和公式，平均负载是...的平均进程数，我感觉平均进程数是一个整数，为什么我们看到的平均负载都是带小数的。希望老师帮忙解答一下，帮我解除疑惑。万分感谢</div>2020-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/40/e592d386.jpg" width="30px"><span>Jackson Wu</span> 👍（3） 💬（1）<div>老师好，一个CPU只能同时处理一个进程，为什么还能把CPU分为0.5C的单位呢，这个cpu的单位是怎么理解的呢</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/4d/bbfda6b7.jpg" width="30px"><span>笃定</span> 👍（2） 💬（1）<div>文中的第二个实验，四个cpu的系统，运行六个进程。理论上六个进程同一时刻不可能都处于R状态吧？一个cpu同一时刻不是只能处理一个进程吗？我的理解top输出应该是四个R状态两个S状态</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d5/d1/42de06de.jpg" width="30px"><span>Harold</span> 👍（2） 💬（1）<div>对于 load average 的值还是有些模糊，不考虑 D 进程的情况下，1台8核的机器有 16个 running 的进程，cpu并没有占满100%的情况下，load average取的值是 16*(1 - cpu idle) 还是 16？换句话说，是不是只要 cpu idle 不是0，取的都是 cpu usage 的值。望解答。</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（2） 💬（9）<div>有事，好几天没来留言了，我有个确认点：
1. 如果一台2个cpu的机器，跑了8个进程，每个进程使用一个cpu的10%，那么load average应该是0.8吧？
2. 平常说的物理机CPU，比如2核4线程，这个在Linux里面看是几个cpu呢？</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/97/9a7ee7b3.jpg" width="30px"><span>Geek4329</span> 👍（2） 💬（2）<div>感谢老师，受益匪浅！

有一点不是很懂，想请教下：
“这里我们做一个kernel module，通过一个 &#47;proc 文件系统给用户程序提供一个读取的接口，只要用户进程读取了这个接口就会进入 UNINTERRUPTIBLE。”

老师上面给的kernel module中，我的理解是只调用sleep，然后用户调用这个接口就进入D state，算是模拟DISK IO状态时获取不到资源时的状态吗？老师能不能给个参考，用户进程读是如何取了这个接口呢？</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/f6/e39d5af1.jpg" width="30px"><span>钱米</span> 👍（1） 💬（1）<div>请问老师，我的宿主机的memory cgroup很多，处于上升趋势，未下降
 ~# cat &#47;proc&#47;cgroups
#subsys_name	hierarchy	num_cgroups	enabled
cpuset	3	30	1
cpu	2	101	1
cpuacct	2	101	1
blkio	6	99	1
memory	7	1013	1
devices	4	99	1
freezer	9	30	1
net_cls	10	30	1
perf_event	8	30	1
net_prio	10	30	1
pids	5	100	1
这个影响了api对容器的创建和启动，改如何处理呢？</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/ed/56731acd.jpg" width="30px"><span>瑞</span> 👍（1） 💬（1）<div>文首提到的Cgroup无法限制LoadAverage，从而可能导致整个系统性能下降。指的是处于D状态进程的性能下降，而D状态进程对同一资源的竞争越来越多，整体表现出来就是系统性能下降。这样理解对吗？</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（1） 💬（2）<div>“在 Linux 的系统维护中，我们需要经常查看 CPU 使用情况，再根据这个情况分析系统整体的运行状态。有时候你可能会发现，明明容器里所有进程的 CPU 使用率都很低，甚至整个宿主机的 CPU 使用率都很低，而机器的 Load Average 里的值却很高，容器里进程运行得也很慢。”

老师，这个问题，我是不是可以这么理解

    假设系统4CPU，平均负载很高为8，每个任务使用100% CPU可发挥最高性能
        1. 如果都是CPU密集型负载，那么CPU使用率不超过50%，应用性能肯定下降
        2. 如果全部是IO密集型负载，那么都在竞争IO资源，应用性能肯定下降
        3. 假设有小于4个的CPU密集型负载，其他都是IO密集型负载，那么CPU密集型负载的性能应该不受影响。</div>2020-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9b/08/27ac7ecd.jpg" width="30px"><span>水蒸蛋</span> 👍（0） 💬（1）<div>老师cpu平均是活动进程&#47;cpu核数，sleep平均也是sleep&#47;CPUcore数量？</div>2020-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/7e/c0/1c3fd7dd.jpg" width="30px"><span>朱新威</span> 👍（22） 💬（1）<div>做个不太恰当的比喻：

cpu：比做一条高速公路

进程占用：比做一辆辆汽车

高速公路上的拥堵情况（load average）= 正在跑的汽车 + 收费站排队等待进入的汽车 + 服务站加油、吃饭的汽车（D进程）；

把D进程考虑进去是因为，服务站里的汽车随时可能进入高速公路，造成拥堵程度增加</div>2021-01-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpibfWGQ563ARjRF6yGa7XoWOMn1ZmVyNldafdzZzvOOqf9gmhacx0utXu12BsGB0w22VSlXTInPg/132" width="30px"><span>InfoQ_09e721f0120c</span> 👍（0） 💬（0）<div>mac上man top对load average的解释：

     LoadAvg     Load average over 1, 5, and 15 minutes.  The load average is the average number of jobs in the run queue.
</div>2024-07-07</li><br/><li><img src="" width="30px"><span>Geek_0a0c33</span> 👍（0） 💬（0）<div>这一讲感觉和容器的关系并不大，更像是排查如果主机的负载升高的原因，不过还是感谢老师对load average这个概念做了更加清楚的介绍。</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（0） 💬（0）<div>请问下：  D状态进程如何监控和分析呢？</div>2022-09-04</li><br/><li><img src="" width="30px"><span>Geek4437</span> 👍（0） 💬（1）<div>老师你好，结合上一节我有个疑问：容器中 top&#47;uptime 中的 load average 是宿主机的还是容器的呢？</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（0） 💬（0）<div>老师，我想问一下“休眠队列中不可打断的进程平均数”虽然会影响系统的负载，但是对系统的性能影响会非常大吗，它们之前有什么样的关系，因为在线上看到过一些机器确实有D进程出现，甚至负载达到了上千但是系统在正常运行，业务进程并不受影响。</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2a/ff/a9d72102.jpg" width="30px"><span>BertGeek</span> 👍（0） 💬（0）<div>原来Load Average 是这么统计的
第一种是 Linux 进程调度器中可运行队列（Running Queue）一段时间（1 分钟，5 分钟，15 分钟）的进程平均数。
第二种是 Linux 进程调度器中休眠队列（Sleeping Queue）里的一段时间的 TASK_UNINTERRUPTIBLE 状态下的进程平均数。</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c5/d5/90ca8efe.jpg" width="30px"><span>拉可里啦</span> 👍（0） 💬（0）<div>老师，我使用top命令后，进程状态是S，但是为什么还占用CPU呢</div>2021-05-31</li><br/>
</ul>