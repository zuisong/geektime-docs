你好，我是吴磊。

对于Spark这样的内存计算引擎来说，内存的管理与利用至关重要。业务应用只有充分利用内存，才能让执行性能达到最优。

那么，你知道Spark是如何使用内存的吗？不同的内存区域之间的关系是什么，它们又是如何划分的？今天这一讲，我就结合一个有趣的小故事，来和你深入探讨一下Spark内存管理的基础知识。

## 内存的管理模式

在管理方式上，Spark会区分**堆内内存**（On-heap Memory）和**堆外内存**（Off-heap Memory）。这里的“堆”指的是JVM Heap，因此堆内内存实际上就是Executor JVM的堆内存；堆外内存指的是通过Java Unsafe API，像C++那样直接从操作系统中申请和释放内存空间。

**其中，堆内内存的申请与释放统一由JVM代劳。**比如说，Spark需要内存来实例化对象，JVM负责从堆内分配空间并创建对象，然后把对象的引用返回，最后由Spark保存引用，同时记录内存消耗。反过来也是一样，Spark申请删除对象会同时记录可用内存，JVM负责把这样的对象标记为“待删除”，然后再通过垃圾回收（Garbage Collection，GC）机制将对象清除并真正释放内存。

![](https://static001.geekbang.org/resource/image/6b/ca/6b7c27e8b2e02e2698a031ff871313ca.jpg?wh=2889%2A883 "JVM堆内内存的申请与释放")

在这样的管理模式下，Spark对内存的释放是有延迟的，因此，当Spark尝试估算当前可用内存时，很有可能会高估堆内的可用内存空间。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/b7/23/ea83d6eb.jpg" width="30px"><span>-.-</span> 👍（19） 💬（6）<div>受益匪浅，开始看第二遍了！有个问题想请教下，spark.executor.memoryOverhead控制的是堆外内存的大小，官方文档解释：This is memory that accounts for things like VM overheads, interned strings, other native overheads, etc.1. 如果设置spark.memory.offHeap.enabled=false，这块内存是不是只是jvm的堆外内存而不是spark管理的堆外内存，不会被用于执行内存和缓存内存？ 2. 如果设置spark.memory.offHeap.enabled=true,这块内存中是不是会包含offHeapSize，其中一部分为JVM堆外内存一部分为offHeap的执行内存和缓存内存？</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（10） 💬（8）<div>堆内内存中：保留内存300M，用户内存为20*0.2=4GB，Storage内存为20*0.8*0.6=9.6GB，Execution内存为20*0.8*0.4=6.4GB
堆外内存中：Storage内存为10*0.6=6G，Execution内存为10*0.4=4G</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b7/94/22121c60.jpg" width="30px"><span>Kendrick</span> 👍（9） 💬（2）<div>有点疑惑，我想知道堆外内存存在的意义是什么，有什么场景是一定需要堆外内存么？</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/e2/0d/d7a012b7.jpg" width="30px"><span>LYL</span> 👍（7） 💬（1）<div>老师，有几个问题我不太明白，
1.tungsten中的page用于同一管理off-heap和on-heap，利用这个机制可否在spark runtime的时候shuffle同时使用堆内和堆外内存？
2.在cache rdd的时候是否能指定StorageLevel为off_heap在spark runtime时使用堆外内存，memory_only的情况下使用堆内内存，或者说在配置开启堆外内存的参数之后，所有内存都是走堆外内存，无法使用堆内内存</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2b/86/318e6ff3.jpg" width="30px"><span>井先生</span> 👍（7） 💬（1）<div>试读了几节果断订阅了。
开启堆外内存后，分配的内存空间是多大？这时候还会分配堆内内存吗？谢谢</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/f1/bb/547b580a.jpg" width="30px"><span>苏子浩</span> 👍（5） 💬（2）<div>老师，您好！我想问一下在文中提到“reduceByKey算子会引入 Shuffle，而 Shuffle 过程中所涉及的内部数据结构，如映射、排序、聚合等操作所仰仗的 Buffer、Array 和 HashMap，都会消耗 Execution Memory 区域中的内存。”上一节说到Shuffle的中间结果会写入磁盘：Shuffle manager通过BlockManager调用DiskStore的putBytes()方法将数据块写入文件。这里的联系是什么呢？在内存和磁盘上有点不理解，不好意思，感谢解答！</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（4） 💬（2）<div>第一题：
缓存rdd：rdd.persist(StorageLevel.OFF_HEAP)

第二题：
因为堆内内存的申请和释放是由JVM来统一管理，对Spark来说是不那么透明可控的；而堆外内存需要调用Unsafe的allocateMemory和freeMemory方法来进行内存的申请和释放，完全由Spark来控制，所以估算会相对更精准。

第三题：
- Reserved：300M
- User：(20GB - 300MB) * (1 - 0.8)
- Execution：(20GB - 300MB) * 0.8 * (1 - 0.6) + 10GB * (1 - 0.6)
- Storage：(20GB - 300MB) * 0.8 * 0.6 + 10GB * 0.6</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/a1/8bc8e7e1.jpg" width="30px"><span>赌神很低调</span> 👍（3） 💬（1）<div>老师好，有几个问题不是很明白想问下:
1、spark中内存划分是逻辑上的，真正的管理还是在jvm。如user memory占用内存超过设定值，还是会占用框架内存。但框架内存会根据设定值让task做一些阻塞或spill操作，所以从这个层面上说，框架内存的值得正确设置，如用户不会用到大的list、map等内存集合，就要把用户内存空间设置得够小，以保证框架内存(执行内存+存储内存)足够大，避免不必要的阻塞或spill操作？
2、如果开启了堆外内存,即使堆外内存不够，堆内内存充足，task也只会用堆外内存而不会用堆内内存？
3、spark 2.x版本中如果开启了堆外内存，并设置了spark.memory.offHeap.size=500mb,在yarn上跑的话spark.executor.memoryOverhead除了默认需要的10%是否还有要加上这500mb，否则container不会分配堆外这500mb的内存？看网上说3.0以上就不用加了。
4、task会在哪些场景申请和释放内存呢？只是shuffle的场景吗？transformer场景会吗？</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（3） 💬（1）<div>从第一章看到了第十一章,在留言去里面学习到了很多,老师对知识的传授也很有技巧,个人也是受益匪浅,随着阅读的慢慢深入的,总结了一些自己理解和疑惑,现在又回到了第七章,总结了一些问题,希望老师可以帮忙解惑,感谢!
1.在缓存rdd时,既然executor memory 和 storage memory 两块内存不可互相share,那是不是可以通过persist来指定呢,一部分rdd使用execm 一部分rdd使用storm呢?
2.只要不开启off heap,spark就无法使用off heap,包括yarn,k8s模式利用off heap提升稳定性也无法体现出来,一旦开启了off heap,执行任务也就是executor memory优先使用off heap,storage memory还是优先堆内内存,可以这样理解吗?
3.例如：spark executor如果配置了堆内和堆外各4GB，executor cores配置为2。那么该executor运行的第一个task只会使用堆外内存？调度来的第二个task，哪怕堆外剩余几十MB，它也会用堆外内存，如果第二个task发现堆外不够用，就会写磁盘,或清除部分堆外内存数据呢
4.shuffle 阶段的稳定性参数 spark.excludeOnFailure.application.fetchFailure.enabled 从官网描述上来看,这个参数对fetch failed会切换到别的节点,结合实际情况,在Map 阶段：Shuffle writer 按照 Reducer 的分区规则将中间数据写入本地磁盘过程中,刚好写人的datanode 的数据卷故障,但是并没有触发重试机制,而是一直runing状态,是不是可以通过启用application.fetchFailure.enabled来识别,目前使用的是物理机,这种情况也是偶尔发生一次,所以很难验证</div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（3） 💬（2）<div>启用off-heap以后，RDD可以直接缓存到off-heap上。</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（3） 💬（5）<div>老师，stage的输入是外部数据源的情况，比如s3的parquet文件，是用哪一块内存来保存读取的数据呀</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（2） 💬（2）<div>老师，怎么知道是堆外用完了才用堆内呢？能指导一下源码的出处么？</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1c/8f/a5e25ee4.jpg" width="30px"><span>豪</span> 👍（1） 💬（2）<div>源码捕捉实力还不够强😂，看了半天没找到 一个job堆外不够用时转用堆内 的源码，老师能指点下吗</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（1） 💬（2）<div>二刷,接上一个留言的问题2:
1.memoryOverhead这个参数不管是作用在堆内还是堆外,都是占用storage memory这部分内存吗,
2.磊哥的回复中提到 &quot;不管堆外还是堆内，开发者用不到，spark也用不到，所以不用关心，千万不指望调这个参数去提升性能，它的目的是保持运行时的稳定性~&quot;,个人不太理解这句话的不用关心,因为有出现过oom overhead的问题,可以理解为是使用到了memoryOverhead,那么就需要去调整对应的memoryOverhead大小,&quot;开发者用不到，spark也用不到&quot;,这句话我还没有get到,斗胆在问一下磊哥,是哪里用到了这个参数,来提升稳定性呢? 
个人理解不够,给磊哥添麻烦了 o(╥﹏╥)o  o(╥﹏╥)o  o(╥﹏╥)o</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/48/ef/4750cb14.jpg" width="30px"><span>🚤</span> 👍（1） 💬（3）<div>老师，cache 之后 再进行count，主要是因为cache不是action算子，所以需要一个action算子来触发缓存的生效。
我这样子理解对么？

回答2：
堆内内存：因为spark只是将无用的对象引用删除，但是无用对象真正的回收还要依赖于JVM来管理。Spark只是做了标记，但是真正什么时候删除spark并不知道，这里存在一个时间差。
相比较堆外内存：spark自己做管理就可以清楚的知道当前还有多少内存空间可以使用。

回答3：
堆内：
Reserved: 300MB
User: 4GB
Execution: 6.4GB
Storage: 9.6GB

堆外：
Execution：6GB
Storage：4GB</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/65/75/f9d7e8b7.jpg" width="30px"><span>L3nvy</span> 👍（1） 💬（1）<div>1. 堆外内存主要分为Execution Memory和Storage Memory两部分，使用场景应该是和堆内内存的使用场景几乎一致。Execution Memory用在Shuffle、Join、Sort、Aggregation计算过程中；Storage Memory用在RDD的缓存、集群中内部数据的传播
2. 堆内内存因为依赖JVM的GC进行内存回收，Spark不能保证内存空间已经被回收；堆外内存因为是手动进行内存的分配和释放，所以Spark能准确预估内存暂用量
3. 
    1. Reserved Memory: 300 MB
    2. User Memory: 20 * 0.2  = 4 GB
    3. Execution Memory: 20 * 0.8 * 0.4 + 10 * 0.4 = 10.4 GB
    4. Storage Memory: 20 * 0.8 * 0.6 + 10 * 0.6  = 15.6 GB</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2d/aa/e33e9edd.jpg" width="30px"><span>陌生的心酸</span> 👍（0） 💬（1）<div>2.通过java UnSafe API 进行内存分配和回收，及时、自行进行对象的引用、回收，及时进行内存的分配和管理，避免像jvm那样进行定时清理，进行标记、清除操作，效率更快，速度更高
3.
堆内内存：
预留内存 : (1-0.8)*20G = 4G ; 执行内存： 0.8*(1-0.6）*20 = 6.4G ,存储内存：0.8*0.6*20 = 9.2G
堆外内存：
执行内存： （1-0.6） * 10G = 4G,存储内存 0.6*10 = 6G
</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2d/aa/e33e9edd.jpg" width="30px"><span>陌生的心酸</span> 👍（0） 💬（1）<div>2.通过java UnSafe API 进行内存分配和回收，及时、自行进行对象的引用、回收，及时进行内存的分配和管理，避免像jvm那样进行定时清理，进行标记、清除操作，效率更快，速度更高
3.
堆内内存：
预留内存 : (1-0.8)*20G = 4G ; 执行内存： 0.8*(1-0.6）*20 = 6.4G ,存储内存：0.8*0.6*20 = 9.2G
堆外内存：
执行内存： （1-0.6） * 10G = 4G,存储内存 0.6*10 = 6G
</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/a3/45/65e7997f.jpg" width="30px"><span>Cellophane</span> 👍（0） 💬（1）<div>感觉土地招租的例子有点绕，没有零基础入门 Spark中那个施工的例子直观</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/78/a0/7a248ddc.jpg" width="30px"><span>福</span> 👍（0） 💬（1）<div>老师，想请问哈您，第2行代码，val words: RDD[String] = sparkContext.textFile(“~&#47;words.csv”)，这个words的数据，是用的哪里的内存，这个也是用户定义的内存，是在userMemory中嘛</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/0b/aa/09c1215f.jpg" width="30px"><span>Sansi</span> 👍（0） 💬（1）<div>为什么我看源码，执行内存+存储每次=(spark.executor.memory-预留内存300m)*spark.memory.fraction</div>2021-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4f/bd/e08af2e9.jpg" width="30px"><span>冷萃浮乐朵</span> 👍（0） 💬（1）<div>想问下这里说的内存管理和BlockManager的MemoryStore有关系吗？</div>2021-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/63/6e/6b971571.jpg" width="30px"><span>Z宇锤锤</span> 👍（0） 💬（1）<div>感觉麻子干不过小艺，小艺的政策太好了，越线的地，小艺需要麻子就要给。当麻子线内的地，小艺种了就不给麻子还了。谁叫小艺的作物经济价值高呢。</div>2021-04-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIiaeebUYxl7e4jicPshDRKMbiculHUjKgZZ2ygDibn2S7bbsjeqYIdsEUdVyoryKNa43ZGnDQmWjv3ibQ/132" width="30px"><span>Geek_d794f8</span> 👍（0） 💬（1）<div>老师cache用的storage memory，count不应该是用的execution memory吗？</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（0） 💬（2）<div>如果没有开启堆外内存spark.memory.offHeap.enabled=false。spark会用堆内内存，那还会用到堆外内存么。怎么感觉一些地方会用到呢。否则也没必要预留堆外内存吧？</div>2021-04-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vH3NV3dCKgCDrxfbwqeaaI3XYpZ6PqAxPQByH0zt6WNMOBoRjg3IvfWDYtib6flCpwqkP5iamd74c3WlM72ydLmw/132" width="30px"><span>Geek_50f808</span> 👍（0） 💬（2）<div>老师，我想请教一下dict会和任务一起发送到executor，这种方式方式和广播变量的方式有什么区别么？</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/6f/b3337e6d.jpg" width="30px"><span>金角大王</span> 👍（0） 💬（2）<div>onHeapStorageRegionSize =
        (maxMemory * conf.getDouble(&quot;spark.memory.storageFraction&quot;, 0.5)).toLong</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/6f/b3337e6d.jpg" width="30px"><span>金角大王</span> 👍（0） 💬（4）<div>老师，能讲解下Spark不同任务在堆内堆外内存的使用选择上的逻辑吗？</div>2021-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/a2/5252a278.jpg" width="30px"><span>对方正在输入。。。</span> 👍（0） 💬（1）<div>老师，第一个问题，我的理解是涉及到io的操作会用到堆外内存，比如shuffle reduce阶段从不同的executor拉取中间数据时；或者rdd使用persist到磁盘时，其他情况我就不得而知了</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/93/2d3d5868.jpg" width="30px"><span>Jay</span> 👍（0） 💬（1）<div>&quot;第四行和第五行用 cache 和 count 对 keywords RDD 进行缓存&quot; -- keywords.cache缓存能理解，keywords.count为啥也可以缓存呢？</div>2021-03-29</li><br/>
</ul>