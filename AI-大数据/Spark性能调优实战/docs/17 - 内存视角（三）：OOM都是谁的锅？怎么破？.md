你好，我是吴磊。

无论是批处理、流计算，还是数据分析、机器学习，只要是在Spark作业中，我们总能见到OOM（Out Of Memory，内存溢出）的身影。一旦出现OOM，作业就会中断，应用的业务功能也都无法执行。因此，及时处理OOM问题是我们日常开发中一项非常重要的工作。

但是，Spark报出的OOM问题可以说是五花八门，常常让人找不到头绪。比如，我们经常遇到，数据集按照尺寸估算本该可以完全放进内存，但Spark依然会报OOM异常。这个时候，不少同学都会参考网上的做法，把spark.executor.memory不断地调大、调大、再调大，直到内心崩溃也无济于事，最后只能放弃。

那么，当我们拿到OOM这个“烫手的山芋”的时候该怎么办呢？我们最先应该弄清楚的是“**到底哪里出现了OOM**”。只有准确定位出现问题的具体区域，我们的调优才能有的放矢。具体来说，这个“**哪里**”，我们至少要分3个方面去看。

- 发生OOM的LOC（Line Of Code），也就是代码位置在哪？
- OOM发生在Driver端，还是在Executor端？
- 如果是发生在Executor端，OOM到底发生在哪一片内存区域？

定位出错代码的位置非常重要但也非常简单，我们只要利用Stack Trace就能很快找到抛出问题的LOC。因此，更**关键的是，我们要明确出问题的到底是Driver端还是Executor端，以及是哪片内存区域**。Driver和Executor产生OOM的病灶不同，我们自然需要区别对待。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（16） 💬（1）<div>老师，从第一讲看到这里，貌似有个东西还没介绍，假设并行度、executor core和每个core均摊的execution memory都估算好了，那么我要几个executor，每个executor几个core好呢，就是说我executor多，然后每个executor的core少点，还是反过来好呢，是否有经验之谈？</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f1/bb/547b580a.jpg" width="30px"><span>苏子浩</span> 👍（16） 💬（2）<div>老师好，我有一下三个问题：
(i)关于Task获取内存方面中“每个线程分到的可用内存有一定的上下限，下限是 M&#47;N&#47;2，上限是 M&#47;N，也就是属于[M&#47;(2*N), M&#47;N].”,同时注意到上述的M和N其实是随着Executor中task的状态动态变化的，根据前文提到的“执行内存总量M动态变化，由于Execution Memory可以占用Storage Memory以及抢占的优先级，所以ExecutionMemory的下限是 Execution Memory初始值，上限是 spark.executor.memory * spark.memory.fraction”和“N~是Executor 内当前的并发度”。但是在具体的例子中怎么task的内存分配我不是很理解。比如本文中提到的“实例 1：数据倾斜”所提到的“Executor 线程池大小为 3，因此每个 Reduce Task 最多可获得 360MB * 1 &#47; 3 = 120MB 的内存空间。Task1、Task2 获取到的内存空间足以容纳分片 1、分片 2，因此可以顺利完成任务。”我不理解的是，此时的Task是以“一批”的形式同时进入Executor吗？所以是“360MB&#47;3=120MB”。为什么不是Task1‘到的早’，它刚来的时候N=1，所以它最多可以拿到整个执行内存，即360MB呢？但是Task1实际只需要100MB，所以分100MB给Task1。此时可用的‘动态执行内存总量’变成260MB（如果是这样，那么接着的内存构成是：(1)80MBStorage Memory + 180Execution Memory还是(2)180MBStorage Memory + 80MBExecution Memory？i.e.其实我想问的是在内存分配上的优先级是怎么分配？先去‘贪心’地抢先占用Storage Memory等用完以后再使用Execution Memory还是分配Execution Memory再开始用Execution Memory？根据您的黄小己招租种地的规则应该是先去占用自己所属的部分的内存吧？）
(ii)同时，实例二：数据膨胀例子中，“task1之所以能拿到300MB，是因为它“到的早”，它刚来的时候N=1，所以它最多可以拿到整个执行内存。“那么task1实际是拿到了多少内存呢？是300MB还是360MB？是按需分配还是给360MB？如果是分配了300MB，那么此时“动态执行内存总量”变成了多少呢，是60MB吗？那么此时Task2进入时，假设Task3还没有进入，N等于2了，所以Task2分配到的执行是60 &#47; 2 = 30MB吗？
(iii)Executor中的Task是同时进入的吗？我的意思是Driver是否会一次性生成所有的的Task，并将Task全部都发送到Executor去执行？还是Driver不完全发送所有Task，根据Executor的并发度（基本上取决于Executor的cores个数）去发送，按照Executor的执行情况去发送Task，执行完一个Task再发送一个Task？虽然之前有提到其实Task本身是自带任务调度意愿的。
打了很多字，确实自己没有想明白，麻烦老师了，不好意思！谢谢！</div>2021-04-27</li><br/><li><img src="" width="30px"><span>王天雨</span> 👍（9） 💬（4）<div>1、执行内存总量是动态变化的，最大是spark.executor.memory * spark.memory.fraction
本例中最大360M。
其次并发度N是固定不变，但是Executor中当前并行执行的任务数是小于等于N的，
上下限公式的计算是根据Executor中当前并行执行的并发度来计算的。
因此先拿到任务的线程能够申请更多的资源，极端情况下，本例单个Task可享受360M内存。</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/09/7f2bcc6e.jpg" width="30px"><span>sky_sql</span> 👍（8） 💬（1）<div>老师好！麻烦问下 Shuffle 文件寻址有个参数spark.reducer.maxSizeInFlight 默认48m，这个buffer缓冲每次拉取48m数据。是Execution Memory剩余部分不够48m就会oom吗？这个和1&#47;N的有啥关联？</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/f6/d75afb79.jpg" width="30px"><span>在路上</span> 👍（6） 💬（1）<div>老师好，请教下关于driver端oom问题，生产中遇到过这样问题，数据表数据量大，每次扫描近一年分区，几十个表关联场景，每次任务启动都一直初始化，有的时候还超时失败，任务一只run不起来，我记得没修改逻辑的时候是把driver调到100多g解决的。后续把代码扫描分区缩短了没有了，想问一下这种情况driver在计算分片吗？为啥这么久啊。</div>2021-12-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qmdZbyxrRD5qQLKjWkmdp3PCVhwmWTcp0cs04s39pic2RcNw0nNKTDgKqedSQ54bAGWjAVSc9p4vWP8RJRKB6nA/132" width="30px"><span>冯杰</span> 👍（4） 💬（1）<div>老师好，文章中提到：“Task3 的数据分片大小远超内存上限，即便 Spark 在 Reduce 阶段支持 Spill 和外排，120MB 的内存空间也无法满足 300MB 数据最基本的计算需要，如 PairBuffer 和 AppendOnlyMap 等数据结构的内存消耗，以及数据排序的临时内存消耗等等。”

关于上述这段话有点疑问：
1、shuffle read 阶段，reduce task去fetch数据时，是可以支持spill到磁盘的。  但在实际工作中，经常出现fetch fail的异常，增加内存后或者同等内存下换为堆外内存也可以解决问题；
2、为什么支持spill操作，还会导致OOM呢？     看老师的解答是需要一个最基础的内存需求，比如：300MB的数据需要120M+50M内存，这块儿不是很明白</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（4） 💬（2）<div>老师好！
实例1中
1、为什么提到“线程池大小设置为 1 是不可取的”？

2、假如spark.executor.cores设置成 1 ，有3个Task，串行。  
第一个Task执行完成后，360M的内存会全部都释放么？会不会有垃圾还没有回收的情况，导致Task2的内存没有360M可以</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f1/bb/547b580a.jpg" width="30px"><span>苏子浩</span> 👍（3） 💬（1）<div>老师，我想问一下，数据膨胀导致 OOM 的例子中，一定会出现OOM吗？既然Task1 能获取到 300MB 的内存空间，那么挂起Task2线程和Task3线程，等待Task1内存释放，然后依次完成3个Task呢？</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（2） 💬（1）<div>老师您好，我有几个问题：
（1）文章中举的例子，“每个 core 有两个线程”是怎么设置的？spark.task.cpus=0.5吗？
（2）我看官方文档对于spark.executor.cores的定义是The number of cores to use on each executor. 现在spark.executor.cores=3但是一个机器上只有两个core，那这时候创建executor的资源好像不够？另外您说spark.executor.cores=1就失去并行的意义了，但是我们目前spark.executor.cores就设置的是1（捂脸）运维说这是经过慎重考虑的默认参数，在 https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;gNxQKTH9JkNsDaBKttvAsQ 这篇文章的 06 规范优化 =&gt; 03 参数滥用问题 有提到，不知道老师对这个设置怎么看呢？
（3）您对 To_Drill 和 狗哭 两位同学的问题回答感觉有一点矛盾呢~在 狗哭 的问题的回答中您说 “task申请不到额外内存，不得不进入waiting list，等待别的task把内存释放，这个时候，CPU也会挂起”，也就是说task开始计算之后发现内存不够但是又申请不到额外内存就会被挂起，但是在 To_Drill 的问题的回答中您说 “task为了容纳整个数据分片，需要不停地申请内存，如果内存不够，任务不能再挂起了，因为挂起来，内存也不能释放，别的task也进不来，挂起没有意义，所以只能硬着头皮往下执行，直到把内存撑爆为止”，意思应该是task开始计算之后发现内存不够但是又申请不到额外内存这时就直接抛oom？不知道是不是我没理解对...
谢谢老师！！</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（2） 💬（2）<div>1.task1首先运行的，拿到自己1&#47;N发现还不够，就继续申请内存。task2&#47;task3后面运行，发现可用内存满足下限，就跑去运行了，结果task1抢先申请到300M，task2,task3在运行时需要更多内存，不能得到满足，导致OOM。
2.driver端oom:
遇到过执行查询SQL，结果集太大，oom。通过调maxResultSize大小来解决。   
executor端oom:
之前没细究过，oom了就给executor调大内存就完了。。。。😅</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/98/4d/582d24f4.jpg" width="30px"><span>To_Drill</span> 👍（1） 💬（1）<div>老师，对下边这个描述我有个疑问，既然内存是陆续分配的，申请不到内存时会挂起，那些OOM的case为啥没有挂起呢？
2）再一个，就是随着task的进展，task对于内存的持续申请，得不到满足，注意，是持续申请，Spark根据task的计算需要，陆续给task分配内存，并不是一下子就提前allocate一定量的内存，这个是很多同学困惑的地方~ 就是大家一开始可能申请的都不多，但是随着各自task计算的进展，大家申请的内存量会陆续增大，慢慢的，就会出现有些task申请不到额外内存，不得不进入waiting list，等待别的task把内存释放，这个时候，CPU也会挂起，造成CPU资源的浪费</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/78/a0/7a248ddc.jpg" width="30px"><span>福</span> 👍（1） 💬（2）<div>老师好，关于苏子浩的提问的。。。。。(ii)同时，实例二：数据膨胀例子中，“task1之所以能拿到300MB，是因为它“到的早”，它刚来的时候N=1，所以它最多可以拿到整个执行内存。“那么task1实际是拿到了多少内存呢？是300MB还是360MB？是按需分配还是给360MB？如果是分配了300MB，那么此时“动态执行内存总量”变成了多少呢，是60MB吗？那么此时Task2进入时，假设Task3还没有进入，N等于2了，所以Task2分配到的执行是60 &#47; 2 = 30MB吗？
我的理解是这样的，，，tast1 分走了 300M，tast2 进来了，此时N=2，我觉得应该是 task1 和task2 来分一共的 360M (两个任务最大的上限（360&#47;2）180M),此时task2只需要100M，那么task2可以运行，task1 应该只能分到360-100等于260M，但是因为task1 本身需要 300，所以oom，，，， 不理解 为什么task2是分到60&#47;2=30M</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b5/88/477e7812.jpg" width="30px"><span>RespectM</span> 👍（1） 💬（3）<div>老师数据膨胀如何监控，怎么看是否是数据膨胀导致的oom，还是shuffle的时候netty导致的堆外内存oom？</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f1/bb/547b580a.jpg" width="30px"><span>苏子浩</span> 👍（1） 💬（1）<div>老师，您好。关于文中在“case1: 数据倾斜”部分提到的“针对以这个案例为代表的数据倾斜问题，我们至少有 2 种调优思路：1. 消除数据倾斜，让所有的数据分片尺寸都不大于 100MB；2. 调整 Executor 线程池、内存、并行度等相关配置，提高 1&#47;N 上限到 300MB”。我有两点疑问：
（1）这里提到的数据分片尺寸100MB是怎么定的呢？为什么不是120MB呢？本例子中Executor 线程池大小为 3，每个 Reduce Task 最多可获得 360MB &#47; 3 = 120MB 的内存空间。以及关于留言关于“spark.reducer.maxSizeInFlight“的回复：”这部分buffer也算作Execution Memory的一部分，也会记到Execution Memory的“账上”。“那么保证数据分片尺寸低于120MB或者100MB此时有效吗？

（2）调整 Executor 线程池、内存、并行度等相关配置，提高“ 1&#47;N ”上限到 300MB，这里为什么是“1&#47;N”而不是14讲中的“动态实时变化的 Execution Memory &#47; N～”呢？文中所举的例子“维持并发度、并行度不变，增大执行内存设置，提高 1&#47;N 上限到 300MB”，这里我的理解变化的是Execution Memory ，和“1&#47;N”这个本身有关系吗？
谢谢老师！</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（1） 💬（1）<div>有个疑问
collect是把executor所有数据全部拉回来，但是他是一次性全放到driver端吗？如果是，那fetchsize的大小只是为了分批输出吗，是不是调的越大输出就越快了;如果不是，那就不应该出现driver端oom吧
按照文中分析来看，collect就是把所有数据一次性拉到driver端了吧？</div>2021-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/54/05b7341b.jpg" width="30px"><span>毕务刚</span> 👍（0） 💬（2）<div>老师好：

将HDFS的json文件导入到hive表时，出现java.lang.OutOfMemoryError: GC overhead limit exceeded，
并且在log中，可以看到WARN MemoryManager: Total allocation exceeds 95.00% (906,992,014 bytes) of heap memory

代码很简单
spark.read.json(&quot;**&quot;).write.mode(&quot;overwrite&quot;).saveAsTable(&quot;**&quot;)

这个问题是哪部分内存出现了问题呢？ 
如果不增加内存， 还可以如何优化？</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/96/17/200c21f0.jpg" width="30px"><span>狗哭</span> 👍（0） 💬（1）<div>老师您好，接着上面苏子浩的第二问的回答我有点不太明白了。前面cpu那一讲线程挂起这个问题里面有这样一段：M 的下限是 Execution Memory 初始值，上限是 spark.executor.memory * spark.memory.fraction 划定的所有内存区域。那这样的话task2进来时给它的内存不应该是（360&#47;2&#47;2，360&#47;2）吗？如果是60&#47;2的话，那线程挂起只有一种情况了，就是这个线程一点内存也没抢占到，也不存在因为分配的内存大于0小于M&#47;N&#47;2而挂起这种情况了吧。请老师指点</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师 问下数据倾斜的第二种解决方法“维持并发度、执行内存不变，使用相关配置项来提升并行度将数据打散，让所有的数据分片尺寸都缩小到 100MB 以内”感觉不能解决本质问题吧，发生数据倾斜应该是因为某个分区数据量太大了，但是分区不管打的多散，这些数据在reduce阶段都会汇集到一个节点吧？</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（0） 💬（1）<div>磊哥好,磊哥上文提到的案例中采用默认配置,源码里面是这样描述的:
&quot;The region shared between execution and storage is a fraction of (the total heap space - 300MB) configurable through `spark.memory.fraction` (default 0.6). The position of the boundary within this space is further determined by `spark.memory.storageFraction` (default 0.5). This means the size of the storage region is 0.6 * 0.5 = 0.3 of the heap space by default&quot;
1.总的堆内存没有提到user memory,只有storage + execution + reserved
2.默认配置fraction:0.5,storagefraction:0.6,storage=(900-300)*0.3=180m,execution=(900-300)*0.6*(1-0.5)=180m
3.没有缓存这里理解为没有使用到storage memory缓存RDD,广播变量等数据,为0M,则execution可以额外占用180M,xecution = 360M
4.反推900M= reserved300m+storage180M+execution180M+240M,可以理解为240M是预留的给user memory的内存吗?</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（0） 💬（1）<div>老师的案例中没有涉及到 --num-executors 配置,看源码里面默认是2,所以实际计算内存分配时,总的堆内内存因该executors-memory*num-executors,每个executor的并发executors-memory*num-executors&#47;executor-cores这样理解对吗
</div>2021-08-29</li><br/><li><img src="" width="30px"><span>王天雨</span> 👍（0） 💬（1）<div>
val df: DataFrame = _
df.cache.count
val plan = df.queryExecution.logical
val estimated: BigInt = spark
.sessionState
.executePlan(plan)
.optimizedPlan
.stats
.sizeInBytes


我是spark2.2  stats方法需要传SQLConf类型的参数进去，不知道传什么呀</div>2021-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（0） 💬（1）<div>老师，针对第一题，有一个疑问，一般来讲，如果数据分片&#47;partition有3个，spark.executor.cores也大于等于3个的时候，很难会出现任务先来后到的情况吧？网络延迟会造成这种情况？我能想到的出现这种情况场景可能是：比如有100个分区待处理，spark.executor.cores为50，这样只能是先执行50个task，然后执行完task的core空闲下来之后，就可以执行pending的tasks了，那么这个时候就会出现task先来后到的情况了。</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（0）<div>老师，我在公司做AI云平台相关工作，AI云平台的工作流里面有很多spark 任务，这个任务可能跑一天的数据，也可能跑一个月的，但是算法工程师不会调节 spark 参数，就导致 任务的运行时间不可控，所以，我们想做一个 配置建议的工具，告诉算法人员这次提交任务，cpu 和 mem 最好配多大。请问下，spark 有人开展类似工作嘛？</div>2022-05-05</li><br/>
</ul>