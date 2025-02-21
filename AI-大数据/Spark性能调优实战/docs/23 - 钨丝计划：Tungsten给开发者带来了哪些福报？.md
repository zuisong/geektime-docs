你好，我是吴磊。

通过前两讲的学习，我们知道在Spark SQL这颗智能大脑中，“左脑”Catalyst优化器负责把查询语句最终转换成可执行的Physical Plan。但是，把Physical Plan直接丢给Spark去执行并不是最优的选择，最优的选择是把它交给“右脑”Tungsten再做一轮优化。

Tungsten又叫钨丝计划，它主要围绕内核引擎做了两方面的改进：数据结构设计和全阶段代码生成（WSCG，Whole Stage Code Generation）。

今天这一讲，我们就来说说Tungsten的设计初衷是什么，它的两方面改进到底解决了哪些问题，以及它给开发者到底带来了哪些性能红利。

## Tungsten在数据结构方面的设计

相比Spark Core，Tungsten在数据结构方面做了两个比较大的改进，一个是紧凑的二进制格式Unsafe Row，另一个是内存页管理。我们一个一个来说。

### Unsafe Row：二进制数据结构

Unsafe Row是一种字节数组，它可以用来存储下图所示Schema为（userID，name，age，gender）的用户数据条目。总的来说，所有字段都会按照Schema中的顺序安放在数组中。其中，定长字段的值会直接安插到字节中，而变长字段会先在Schema的相应位置插入偏移地址，再把字段长度和字段值存储到靠后的元素中。更详细的例子我们在[第9讲](https://time.geekbang.org/column/article/357342)说过，你可以去看看。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/22/f04cea4c.jpg" width="30px"><span>Fendora范东_</span> 👍（18） 💬（4）<div>有个地方没理解
1.onheap内存寻址所说的内存页表，保存的是对象引用到jvm对象地址的映射，那它应该也是一个map结构，它是不是用下面所说的Tungsten.hashmap实现的？
2.我理解不是，下面说的Tungsten.hashmap实例，我理解它是一个完整查询结构:要查某条数据，先计算key的hashcode，然后拿到128位内存地址，然后高64位(堆内对象引用)用于在「内存页表」中查询jvm对象地址，低64位用于在查到的jvm对象中进行偏移计算拿到具体某行数据。
3.如果2我没分析错，那「内存页表」是怎么实现的呢？</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（13） 💬（1）<div>老师，tungsten内存页这块还是看得我很迷糊。我试着用我自己的语言复述下你看下对不对。

假设我有一张一百万行的表，用Tungsten内存，那就是会把这一百万分散到几十个内存页里去是吗，也就是一个内存页存了几万行？
其次，这几十个内存页里前64位都存着key value的键值对(共一百万个)，后64位存偏移指针。其中key就是每一行的hash，row就是表的每一行对吗？
最后，如果我想找id=3的那行数据(假设id唯一)，那就再去内存页的后64位找偏移量为3，也就是指针挪动3个单位，来确定最终要找的那一行是吗？

感觉自己都不能自圆其说了，要是面试这么回答估计得挂，求老师帮忙看看错在哪里…</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/d6/b9513db0.jpg" width="30px"><span>kingcall</span> 👍（6） 💬（2）<div>哈哈，昨天看了一遍没懂，然后去补了点知识 1 java unsafe 2 虚拟内存管理 3 spark 官网关于Tungsten的介绍，今天又来了！
回答：关于sort 为了更好的利用CPU 的多级缓存，Tungsten 做了关于类似pointer-key 作为元素的数组，从而避免在主存里面随机读取数据进行排序，从而可以更好的利用缓存，其实这就是Tungsten 的第二点，然而这一点老师没有介绍，估计是在这等着的吧，哈哈！</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/00/3f/a0f84788.jpg" width="30px"><span>Sean</span> 👍（4） 💬（1）<div>老师提到,开启了堆外之后，Spark在运行时会优先使用堆外，堆外不够再回退到堆内。我理解为这个任务一共生成了1000个task,每个task100m,堆外内存是6G,堆内2G,在执行到第50个task时,发现堆内还剩下40m,则剩下的所有task,960个都会走堆内内存,即时堆外50个task占用的内存已经释放,依然不会被使用,不知道这样理解对不对</div>2021-09-04</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJO944A1HeBCrewW7YHE1Ha3OVWDEz8iaXwD23iczWrG9eG6deJ0dK5qD1qJuLB0u7LnU4ujtokvjAg/132" width="30px"><span>keeprun</span> 👍（2） 💬（1）<div>老师好，最近在看groupBy的Aggregation策略的选择，包含Hash-based Aggregation（spark 2.2.0后增加了Object-Hash-based Aggregation）和Sort-based Aggregation。其中能否使用Hash-based Aggregation的判断条件主要是UnsafeRow.isMutable(field.dataType())，主要是定长的数据类型，看到注释中提到，数据能够就地更新（Field types that can be updated in place in UnsafeRows）。是否主要是效率考虑（之前第9节有说明UnsafeRow的存储方式，定长的数据按顺序存储在字节数组中，而变长的字段需要通过offset来记录。）还是其他有其他原因？麻烦解惑。</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/20/9f31c4f4.jpg" width="30px"><span>wow_xiaodi</span> 👍（2） 💬（1）<div>老师，有个问题，java的hashmap对于哈希冲突的元素可以通过遍历链表来定位到目标对象，那么tungsten.hashmap的value存放的却是一个128位内存地址，那么此时遇到哈希冲突，他是怎么解决的呢？是先根据128位的内容去寻址内存页的开始位置，然后一直遍历下去吗？</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/9d/daad92d2.jpg" width="30px"><span>Stony.修行僧</span> 👍（2） 💬（2）<div>学到很多，也参照了 《learn spark》，性能优化提高了不少，从好几个个小时job 优化到5分钟</div>2021-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（2） 💬（1）<div>问题二：Spark SQL 解析为语法树后，在不使用 Expression Codegen 的情况下，表达式节点每次执行都需要进行 Spark 内部的一些相关操作（如做一些操作类型匹配），那么 Spark 自身机制的开销可能大于我们需要执行的计算的开销，因此需要 Expression Codegen 对表达式进行代码生成，此时侧重于对表达式自身的优化；而 WSCG 则侧重与多个函数之间的合并，两者侧重点并不相同。

这里有几个疑问想请教下老师：
1. Tungsten 在堆内采用了 8 字节表示 Java Object，这跟 64 位 JVM 可以对应上，但 64 位 JVM 是有指针压缩机制的，这个对于 Tungsten 是否生效
2. Tungsten 在堆外有 64 位空间浪费了，为何 Spark 社区不针对堆内堆外区分处理，而是采用统一管理的方式？</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/78/66b3f2a2.jpg" width="30px"><span>斯盖丸</span> 👍（2） 💬（1）<div>老师，请问On heap寻址里的Object引用和偏移地址分别对应的是什么？Object引用是一条Row，偏移地址里是Row的一个字段或者说是列吗？</div>2021-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（1） 💬（1）<div>老师问下投影是什么？我看执行计划里好像就是选出需要的字段？</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（1） 💬（1）<div>老师，tungsten的hashmap我看应该在shufflehashjoin的时候会用到，broadcasthashjoin也用这个结构了么？</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/f3/e945e4ac.jpg" width="30px"><span>sparkjoy</span> 👍（1） 💬（1）<div>老师，在内存页表中，怎么知道一个unsafe row的结束位置呢？</div>2021-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/df/e5/65e37812.jpg" width="30px"><span>快跑</span> 👍（1） 💬（2）<div>1、内存页也是Java Object，所以内存页也存储在堆内内存On Heap? 
内存页是一个连续内存空间，通过内存页+偏移量来定位一个数据元素；相比之前，每个数据元素都要生成对象，并且每个对象位置在内存中分散，属于随机访问

2、虽然Tungsten有管理 Off Heap 和 On Heap 内存空间，但是如果要使用Off Heap的情况，也是需要开启堆外内存spark.memory.offHeap.enabled=true，这个前提是没有改变的吧 

3、开启堆外内存spark.memory.offHeap.enabled=true，所有的数据都存到堆外了么，还是有区分。</div>2021-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/37/d0/26975fba.jpg" width="30px"><span>西南偏北</span> 👍（1） 💬（1）<div>花了一个五一的时间，从第一篇追上了老师的更新进度哈哈！老师厉害，学到了很多，尤其Spark SQL这块，还是要对着老师讲的东西，再去认真的读下源码才能有更深的理解</div>2021-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9X140JXPuaDB8PibXpwFWds6mZvg1w7THkyB6NjBkP7x4HqSk2wuUvcmDb9O2l0fCkxvB3ibL0L2A/132" width="30px"><span>科学养牛</span> 👍（0） 💬（1）<div>没选过计算机原理，感觉这讲完全听不懂了😭</div>2021-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/f2/32/ea5b24da.jpg" width="30px"><span>MuJp</span> 👍（0） 💬（1）<div>老师，设置10 executor、5 core数和5 executor、10 core数分别提交500M、1T的数据，四个任务执行性能排序，那个最快呢</div>2022-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/ee/0ce82b15.jpg" width="30px"><span>糍粑</span> 👍（0） 💬（0）<div>WSCG对于VI的优势没有看懂。那段WSCG的代码，使用foreach写的，本质上也是个iterator。这里的优势就是把几个操作符（filter, aggregator）连成一个语句了。背后还是有对操作符对next()的调用。
为什么说“不仅消除了操作符，也消除了操作符的虚函数调用，更没有不同算子之间的数据交换，计算逻辑完全是一次性地应用到数据上。”呢？</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/ee/0ce82b15.jpg" width="30px"><span>糍粑</span> 👍（0） 💬（0）<div>prod上报错ERROR CodeGenerator:91 - failed to compile:...grows beyond 64 KB
查看了spark UI的SQL tab，发现physical plan很大。但神奇的是，spark UI显示job&#47;task依旧完成了，没有错误。这是因为尝试WSCG失败了之后，系统自动fail back to Volcano model了么？
对于这类错误，第一反应是把query改小，但是query是user填写的，不受我的控制。这种是不是可以当warning直接忽略呢？</div>2022-07-05</li><br/>
</ul>