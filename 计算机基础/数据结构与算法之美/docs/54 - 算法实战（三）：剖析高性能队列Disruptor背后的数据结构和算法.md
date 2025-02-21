Disruptor你是否听说过呢？它是一种内存消息队列。从功能上讲，它其实有点儿类似Kafka。不过，和Kafka不同的是，Disruptor是线程之间用于消息传递的队列。它在Apache Storm、Camel、Log4j 2等很多知名项目中都有广泛应用。

之所以如此受青睐，主要还是因为它的性能表现非常优秀。它比Java中另外一个非常常用的内存消息队列ArrayBlockingQueue（ABS）的性能，要高一个数量级，可以算得上是最快的内存消息队列了。它还因此获得过Oracle官方的Duke大奖。

如此高性能的内存消息队列，在设计和实现上，必然有它独到的地方。今天，我们就来一块儿看下，**Disruptor是如何做到如此高性能的？其底层依赖了哪些数据结构和算法？**

## 基于循环队列的“生产者-消费者模型”

什么是内存消息队列？对很多业务工程师或者前端工程师来说，可能会比较陌生。不过，如果我说“生产者-消费者模型”，估计大部分人都知道。在这个模型中，“生产者”生产数据，并且将数据放到一个中心存储容器中。之后，“消费者”从中心存储容器中，取出数据消费。

这个模型非常简单、好理解，那你有没有思考过，这里面存储数据的中心存储容器，是用什么样的数据结构来实现的呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKYfcUOVhf3vhEBUNGHgtIcw8ujMZnkabicLzzjn3xwdeeic2PJSe7ibJgMx2UjF0d7L4B4gsRpaqe2A/132" width="30px"><span>郭小菜</span> 👍（16） 💬（8）<div>一直追老师的课程，每期的质量都很高，收获很多。但是这期确实有点虎头蛇尾，没有把disruptor的实现原理讲得特别明白。不是讲得不好，只是觉得结尾有点突兀，信息量少了。但是瑕不掩瑜，老师的课程总体质量绝对是杠杠的！</div>2019-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/7d/800888a3.jpg" width="30px"><span>belongcai蔡炳榕</span> 👍（10） 💬（4）<div>看完还是有很多困惑（可能跟我不了解线程安全有关）
一是申请一段连续存储空间，怎么成为线程独享的呢？生产者ab分别申请后，消费者为啥无法跨区域读取呢
二是这种方法应该是有实验证明效率高的，私下去了解下。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/4a/7e3d158d.jpg" width="30px"><span>沉睡的木木夕</span> 👍（1） 💬（1）<div>还是没说加存储单元是干嘛的啊，为什么在往队列添加元素之前申请存储单元就不用加锁了？能说的在详细点么</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/14/e9ca2d09.jpg" width="30px"><span>小予</span> 👍（0） 💬（1）<div>一个线程一次读取n个元素，那另外一个线程想要读取元素时，必须等前一个线程的n个元素读取完，本质上读取还是单线程的，不明白这样为何能提高性能，希望老师能解释一下其原理。🙏🙏</div>2019-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BpprxVMjsB0Ok4wGunDLHOLEI9wJX5HIEVsqs2EaXpuODfM7tuiaNfjPcxKWc60TwTaJnTuSicGMicib4r4um02qicQ/132" width="30px"><span>Geek_c33c8e</span> 👍（0） 💬（1）<div>老师，线程池的实现是单个线程往队列插入任务，单个线程去队列去任务吗，所以不会处理并发控制吗</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/d7/a09ef784.jpg" width="30px"><span>Tattoo</span> 👍（0） 💬（1）<div>这就是面试中考的消息队列吗？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/f7/3a493bec.jpg" width="30px"><span>老杨同志</span> 👍（99） 💬（9）<div>尝试回答老师的思考题

1）分库分表也可以使用自增主键，可以设置增加的步长。8台机器分别从1、2、3。。开始，步长8.
     从1开始的下一个id是9，与其他的不重复就可以了。
2）上面同学说的redis或者zk应该也能生成自增主键，不过他们的写性能可能不能支持真正的高并发。
3）开放独立的id生成服务。最有名的算法应该是snowflake吧。snowflake的好处是基本有序，每秒钟可以生成很大的量，容易水平扩展。
    也可以把今天的disrupt用上，用自己生成id算法，提前生成id存入disrupt，预估一下峰值时业务需要的id量，比如提前生成50万；
</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/aa/ee/15c328ca.jpg" width="30px"><span>ɴɪᴋᴇʀ</span> 👍（43） 💬（6）<div>我看到很多读者对文中这段话”3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的“这句话都不是理解，我仔细看了下disruptor的设计方案，统一来回答一下：
每个线程都是一个生产者。对于其中一个生产者申请写入n个元素，则返回列队中对应的最大下标位置(比如当前申请写入3个，从下标3开始，返回的最大下标就是6)，456就是这个生产者所申请到的独享空间。生产者同时会带有一个标记，记录当前写入成功的下标(比如当前写入到5，标记的值就为5，用来标记自身是否全部写入完成)，这是对于单独的一个生产者。对于多个生产者来说，都是如此的，比如有两个生产者，A申请了456，B申请了789，此时A写入到了5，A的标记是5，B写入到了8，B的标记是8，队列中对应6和9的位置是没有数据的。这样是没有问题的，此刻暂停，来看下多消费者同时读数据。消费者A*申请到读取3个元素，消费中B*申请读到了3个元素，那么要申请的连续最大元素个数就是6，对应此刻的下标就是9，这里会触发disruptor的设计机制，从3开始，会依次检测对位置的元素是否生产成功，此刻这里A写到了5，B写到了8，6位置还没有生产成功的，那么机制就会返回可消费的最大下标，也就是5，然后消费者只会读取下标4到5两个元素进行消费。也就是文中小争哥所说的”3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的“-&gt;其实就是disruptor找到了还没有生产出的元素，后面的数据都是无法读取的，其实很简单。不知道这里的解释看懂了没有，有兴趣的话可以自己去看下disruptor的设计实现，而且图片会比文字更加直观。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（37） 💬（6）<div>没有读过 Disruptor 的源码，从老师的文章理解，一个线程申请了一组存储空间，如果这组空间还没有被完全填满之前，另一个线程又进来，在这组空间之后申请空间并添加数据，之后第一组空间又继续填充数据，那在消费时如何保证队列是按照添加顺序读取的呢？

即使控制读取时前面不能有空闲空间，是为了保证能按内存空间顺序消费，但是如果生产的时候没有保证顺序存储，似乎就不满足队列的条件了。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/52/f07e9001.jpg" width="30px"><span>想当上帝的司机</span> 👍（21） 💬（10）<div>为什么3到6没有完全写入前，7到9无法读取，不是两个写入操作吗</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（15） 💬（2）<div>思考题：加锁批量生成ID，使用时就不用加锁了</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/00/791d0f5e.jpg" width="30px"><span>忍者无敌1995</span> 👍（11） 💬（1）<div>项目中有使用过分布式id生成器，但是不知道具体是怎么实现的，参考今天的Disruptor的思路：
1. id生成器相当于一个全局的生产者，可以提前生成一批id
2. 对于每一张表，可以类似于Disruptor的消费者思路，从id生成器中申请一批id，用作当前表的id使用，当然申请一批id对于id生成器来说是需要加锁操作的</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（10） 💬（3）<div>后面有补充这门课的内容吗？我看到老师回复说会补充，为何没有在评论区中反馈呢？对后面学习这门课的学生很困惑啊

“生产者申请连续空间后，后续往队列添加元素就不需要加锁了，因为这个存储单元是这个线程独享的”

这个不好理解，添加元素的不是有可能多个线程吗？那不是会产生竞争资源吗？

希望得到解惑

</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/95/f3283c31.jpg" width="30px"><span>彳</span> 👍（10） 💬（1）<div>disruptor使用环的数据结构，内存连续，初始化时就申请并设置对象，将原本队列的头尾节点锁的争用转化为cas操作，并利用Java对象填充，解决cache line伪共享问题</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（7） 💬（0）<div>雪花算法可以根据不同机子生成不同的id</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/eb/e7127bb8.jpg" width="30px"><span>，</span> 👍（6） 💬（0）<div>感觉Disruptor 其实就是把锁的粒度减小了,原来只要写入和读取都得加锁,锁的是整个数组,现在是只锁数组中的某组连续的下标
</div>2019-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjUDIRQ0gRicmicHclt9KDXCVbqjQVYEtibs4mWcsd13Z1ibqPNb1dSkNAu6Znfak0nyUibOvRD07UfZw/132" width="30px"><span>futute</span> 👍（6） 💬（0）<div>弱弱地问一下，后来老师补充过这节课的内容吗？我看完后，跟以前留言的同学有相同的感觉。
</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/78/3ee39415.jpg" width="30px"><span>M.Y</span> 👍（5） 💬（0）<div>课后思考。 
如果不是分布式应用：
1.用JDK自带的AtomicLong
2.用Oracle数据库中的Sequence
如果是分布式应用：
1.用zookeeper生成全局ID
2.用Redis中的Redlock 生产全局ID</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fd/fd/326be9bb.jpg" width="30px"><span>注定非凡</span> 👍（4） 💬（1）<div>Disruptor是一种内存消息队列，功能上类似 Kafka， 不同的是Disruptor 是线程之间用于消息传递的队列。在 Apache Storm、Camel、Log4j 2 等很多知名项目中都有广泛应用。

它的性能表现非常优秀，比 Java 中另一个非常常用的内存消息队列 ArrayBlockingQueue（ABS）的性能，要高一个数量级，可以算得上是最快的内存消息队列。

Disruptor 是如何做到如此高性能的？其底层依赖了哪些数据结构和算法？

基于循环队列的“生产者 - 消费者模型”
“生产者 - 消费者模型”，“生产者”生产数据，并且将数据放到一个中心存储容器中。“消费者”从中心存储容器中，取出数据消费。

实现中心存储容器的数据结构是队列。队列支持数据的先进先出，使得数据被消费的顺序性可以得到保证

队列有两种实现思路。一种是基于链表实现的链式队列，另一种是基于数组实现的顺序队列

如果实现一个无界队列，适合选用链表来实现队列，因为链表支持快速地动态扩容

相较于无界队列，有界队列的应用场景更加广泛。机器内存是有限的，无界队列占用的内存数量是不可控的，有可能因为内存持续增长，而导致 OOM（Out of Memory）错误。

循环队列是一种特殊的顺序队列。非循环的顺序队列在添加、删除数据时涉及数据的搬移操作，导致性能变差。而循环队列可以解决数据搬移问题，所以性能更加好。所以大部分用顺序队列中的循环队列。

循环队列这种数据结构，就是内存消息队列的雏形

基于加锁的并发“生产者 - 消费者模型”
在多个生产者或者多个消费者并发操作队列的情况下，主要会有下面两个问题：

多个生产者写入的数据可能会互相覆盖；
多个消费者可能会读取重复的数据。

如何解决这种线程并发往队列中添加数据时，导致的数据覆盖、运行不正确问题？

最简单的处理方法就是给代码加锁，同一时间只允许一个线程执行 add() 函数，由并行改成了串行



Disruptor 的基本思想是换了一种队列和“生产者 - 消费者模型”的实现思路。
	* 生产者：往队列中添加数据之前，先批量地申请连续的 n 个（n≥1）可用空闲存储单元。这组存储单元是这个线程独享的，后续往队列中添加元素可以不用加锁了。申请存储单元的过程是需要加锁的

	* 消费者：处理的过程跟生产者是类似的。先申请一批连续可读的存储单元（申请的过程也是要加锁），当申请到这批存储单元之后，后续的读取操作就不加锁

	* Disruptor 实现思路的一个弊端：如果生产者 A 申请到了一组连续的存储单元，假设是下标为 3 到 6 的存储单元，生产者 B 紧跟着申请到了下标是 7 到 9 的存储单元，在 3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的

	* Disruptor 采用的是 RingBuffer 和 AvailableBuffer 这两个结构，来实现功能

总结引申

	* 多个生产者同时往队列中写入数据时，存在数据覆盖的问题。多个消费者同时消费数据，会存在消费重复数据的问题
	* 为了保证逻辑正确，尽可能地提高队列在并发情况下的性能，Disruptor 采用了“两阶段写入”的方法。
	* 在写入数据之前，先加锁申请批量的空闲存储单元，之后往队列中写入数据的操作就不需要加锁了，写入的性能因此就提高了
	* Disruptor 对消费过程的改造，跟对生产过程的改造是类似的。它先加锁申请批量的可读取的存储单元，之后从队列中读取数据的操作也就不需要加锁了，读取的性能因此也就提高了

</div>2020-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/c9/9f51fd27.jpg" width="30px"><span>编程界的小学生</span> 👍（4） 💬（0）<div>我们用的百度的uid生成器，底层是雪花算法，有那么几段规则，根据机器ip和时间进行唯一性</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/23/5df1f341.jpg" width="30px"><span>且听疯吟</span> 👍（4） 💬（0）<div>__sync_fetch_and_add操作即可实现原子自增的操作。</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8e/0b/89055f4c.jpg" width="30px"><span>cn</span> 👍（4） 💬（1）<div>申请了一段空间之后，只有写完才能够读取这段空间和后续空间，如果生产者挂了，是不是读取就阻塞了？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/d4/abb7bfe3.jpg" width="30px"><span>神盾局闹别扭</span> 👍（4） 💬（1）<div>有个问题，按照老师所说，a线程只写1-3区块，b线程只写4-6块，假设a线程先写了块1，切换到线程b，b写块4，然后再切回线程a，a写块2。虽然没有数据覆盖问题，但是最终块1-6的顺序不是按写入先后顺序排布的，读取不是乱套了吗，怎么解决这个问题？求老师能说的详细点。</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/a7/3e6fee86.jpg" width="30px"><span>K战神</span> 👍（4） 💬（1）<div>而是采用了“当队列满了之后，生产者就轮训等待；当队列空了之后，消费者就轮训等待”这样的措施。～是不是有错别字？轮询？</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（2） 💬（0）<div>这种方式本质是让临界区变小。 再一个就是批量。</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/aa/ee/15c328ca.jpg" width="30px"><span>ɴɪᴋᴇʀ</span> 👍（2） 💬（0）<div>我看到很多读者对文中这段话”3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的“这句话都不是理解，我仔细看了下disruptor的设计方案，统一来回答一下：
每个线程都是一个生产者。对于其中一个生产者申请写入n个元素，则返回列队中对应的最大下标位置(比如当前申请写入3个，从下标3开始，返回的最大下标就是6)，456就是这个生产者所申请到的独享空间。生产者同时会带有一个标记，记录当前写入成功的下标(比如当前写入到5，标记的值就为5，用来标记自身是否全部写入完成)，这是对于单独的一个生产者。对于多个生产者来说，都是如此的，比如有两个生产者，A申请了456，B申请了789，此时A写入到了5，A的标记是5，B写入到了8，B的标记是8，队列中对应6和9的位置是没有数据的。这样是没有问题的，此刻暂停，来看下多消费者同时读数据。消费者A*申请到读取3个元素，消费中B*申请读到了3个元素，那么要申请的连续最大元素个数就是6，对应此刻的下标就是9，这里会触发disruptor的设计机制，从3开始，会依次检测对位置的元素是否生产成功，此刻这里A写到了5，B写到了8，6位置还没有生产成功的，那么机制就会返回可消费的最大下标，也就是5，然后消费者只会读取下标4到5两个元素进行消费。也就是文中小争哥所说的”3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的“-&gt;其实就是disruptor找到了还没有生产出的元素，后面的数据都是无法读取的，其实很简单。不知道这里的解释看懂了没有，有兴趣的话可以自己去看下disruptor的设计实现，而且图片会比文字更加直观。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6b/bb/10aaf123.jpg" width="30px"><span>王世林</span> 👍（1） 💬（0）<div>解决思路类似于ConcurrentHashMap 16个分段锁，可以搞个final ReentrentLock数组，大小为8.对要插入的数据按照某种规则对8取余，看下插入哪个分表中，然后获取对应下标的锁即可</div>2020-10-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（1） 💬（0）<div>如果对disruptor还有疑问的可以看看这个https:&#47;&#47;tech.meituan.com&#47;2016&#47;11&#47;18&#47;disruptor.html</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/19/19/d82e24fb.jpg" width="30px"><span>李润东</span> 👍（1） 💬（0）<div>实在是理解不了这句：3 到 6 没有完全写入数据之前，7 到 9 的数据是无法读取的。。。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/0c/0a6a0d5e.jpg" width="30px"><span>蜗牛</span> 👍（1） 💬（0）<div>雪花算法。一层层划分：机房-&gt;服务器-&gt;...</div>2020-04-02</li><br/>
</ul>