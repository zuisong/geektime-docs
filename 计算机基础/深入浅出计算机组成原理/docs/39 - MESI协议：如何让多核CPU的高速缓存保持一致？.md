你平时用的电脑，应该都是多核的CPU。多核CPU有很多好处，其中最重要的一个就是，它使得我们在不能提升CPU的主频之后，找到了另一种提升CPU吞吐率的办法。

不知道上一讲的内容你还记得多少？上一节，我们讲到，多核CPU里的每一个CPU核，都有独立的属于自己的L1 Cache和L2 Cache。多个CPU之间，只是共用L3 Cache和主内存。

我们说，CPU Cache解决的是内存访问速度和CPU的速度差距太大的问题。而多核CPU提供的是，在主频难以提升的时候，通过增加CPU核心来提升CPU的吞吐率的办法。我们把多核和CPU Cache两者一结合，就给我们带来了一个新的挑战。因为CPU的每个核各有各的缓存，互相之间的操作又是各自独立的，就会带来[**缓存一致性**](https://en.wikipedia.org/wiki/Cache_coherence)（Cache Coherence）的问题。

![](https://static001.geekbang.org/resource/image/07/41/0723f72f3016fede96b545e2898c0541.jpeg?wh=1546%2A1126)

## 缓存一致性问题

那什么是缓存一致性呢？我们拿一个有两个核心的CPU，来看一下。你可以看这里这张图，我们结合图来说。

![](https://static001.geekbang.org/resource/image/a6/da/a6146ddd5c78f2cbc1af56b0ee3292da.jpeg?wh=2236%2A1066)

在这两个CPU核心里，1号核心要写一个数据到内存里。这个怎么理解呢？我拿一个例子来给你解释。

比方说，iPhone降价了，我们要把iPhone最新的价格更新到内存里。为了性能问题，它采用了上一讲我们说的写回策略，先把数据写入到L2 Cache里面，然后把Cache Block标记成脏的。这个时候，数据其实并没有被同步到L3 Cache或者主内存里。1号核心希望在这个Cache Block要被交换出去的时候，数据才写入到主内存里。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/e1/d4/1b5ac51e.jpg" width="30px"><span>山间竹</span> 👍（20） 💬（5）<div>既然有了MESI协议，是不是就不需要volatile的可见性语义了？当然不是，还有三个问题：

并不是所有的硬件架构都提供了相同的一致性保证，JVM需要volatile统一语义（就算是MESI，也只解决CPU缓存层面的问题，没有涉及其他层面）。
可见性问题不仅仅局限于CPU缓存内，JVM自己维护的内存模型中也有可见性问题。使用volatile做标记，可以解决JVM层面的可见性问题。
如果不考虑真·重排序，MESI确实解决了CPU缓存层面的可见性问题；然而，真·重排序也会导致可见性问题。</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/fd/ec24cba7.jpg" width="30px"><span>fcb的鱼</span> 👍（3） 💬（1）<div>老师好，问下：在多核cpu里边,某个cpu更新了数据，再去广播其他cpu。怎么保证其他cpu一定是操作成功的呢？</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c2/21/a8ef82ac.jpg" width="30px"><span>炎发灼眼</span> 👍（47） 💬（21）<div>老师，有个问题，如果说一个核心更新了数据，广播失效操作和地址，其他核心的缓存被更新为失效，那更新数据的那个核心什么时候把数据再次写入内存呢，按照上一讲，在下次更新数据的时候才会写入，那如果在这个之间，别的核心需要用到这部分数据，看到失效，还是从内存读，这不是还是读不到最新的数据么。</div>2019-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/60/0403b575.jpg" width="30px"><span>林三杠</span> 👍（29） 💬（3）<div>涉及到数据一致性的问题，cpu层，单机多线程内存层，分布式系统多台机器层，处理办法都差不多，原理是相通的</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/54/c9990105.jpg" width="30px"><span>bro.</span> 👍（18） 💬（1）<div>Java中volatile变量修饰的共享变量在进行写操作时候会多出一行汇编**
    ```
    0x01a3de1d:movb $0×0，0×1104800（%esi）;0x01a3de24:lock addl $0×0,(%esp);
    ```
lock前缀的指令在多核处理器下会:
        1. 将当前处理器缓存行的数据写回到系统内存
        2. 这个写回内存的操作会使其他CPU里缓存了改内存地址的数据无效
多处理器总线嗅探:
        1. 为了提高处理速度,处理器不直接和内存进行通信,而是先将系统内存的数据读到内部缓存后在进行操作,但**写回操作**不知道这个更改何时回写到内存
        2. 但是对变量使用volatile进行写操作时,JVM就会向处理器发送一条lock前缀的指令,将这个变量所在的缓存行的数据写回到系统内存
        3. 在多处理器中,为了保证各个处理器的缓存一致性,每个处理器通过嗅探在总线上传播的数据来检查自己的缓存值是不是过期了,如果处理器发现自己缓存行对应的内存地址被修改,就会将当前处理器的缓存行设置为无效状态,就相当于**写回时发现状态标识为0失效**,当这个处理器对数据进行修改操作时,会重新从系统内存中读取数据到CPU缓存中</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（16） 💬（0）<div>MSI 缓存一致性协议没有E这个状态，也就是没有独享的状态。
如果块尚未被装入缓存(处于“I”状态)，则在装入该块之前，必须先要保证该地址的数据不会在其他缓存的缓存块中处于“M”状态。如果另一个缓存中有处于“M”状态的块，则它必须将数据写回后备存储，并回到“S”状态。
MESI 多了E状态（独享状态），如果当前写入的是E，则可直接写入，提高了性能。</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/94/cefb8a05.jpg" width="30px"><span>。。。</span> 👍（7） 💬（0）<div>老师我想问下：mesi默认一直运行的， 还是说加了lock才会采用锁总线或者msei协议</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（4） 💬（1）<div>MESI 协议对于“锁”的实现是机制是RFO（Request For Ownership），也就是获取当前对应 Cache Block 数据的所有权吗？ 如果是的话，多核cpu下，同时RFO会发生死锁呀，还有你RFO结束后，还没有执行完指令去更新缓存行，但是别的cpu又发起RFO了，此时感觉还是不安全的呀？是不是我理解的不对？期望老师和大神帮忙解答下，🙏</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（4） 💬（2）<div>我编译了volatile相关的代码，在Win10 64位下，将java代码转换成字节码，再转换成机器码，发现是由lock cmpxchg两个指令实现的。 </div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（2） 💬（0）<div>对于MESI协议，当对一个值进行修改时，会需要通过总线广播给其他核，这个时候是需要进行等待其他核响应，这里会有性能的差异吧。记得看过一些资料，有通过写寄存器和无效队列来进行优化，但是优化又会出现可见性和有序问题。最后底层是通过内存屏障来解决加入写寄存器和无效队列的可见性和有序性问题，希望老师能讲下这块</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/15/9c/575cca94.jpg" width="30px"><span>LearnAndTry</span> 👍（2） 💬（0）<div>看到了另一篇讲的不错的文章https:&#47;&#47;blog.csdn.net&#47;reliveIT&#47;article&#47;details&#47;50450136</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（2） 💬（1）<div>1、有人成功，有人普通，到底是什么原因导致的？

我们想成功，我们个人的水平必须是足够高的

2、那么我们的水平高来源于哪里？

来源于我们获得的知识，生活中每一天工作、上班、路上、回家获取的信息

day39 笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11358997.html</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b4/f6/735673f7.jpg" width="30px"><span>W.jyao</span> 👍（2） 💬（3）<div>没明白，其他cpu收到写失效之后把自己的cache置位失效状态，然后还做其他什么处理吗？</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（0）<div>MESI的状态是在cache blockd的哪里做标识？ 是否是脏数据，是通过有效位来标识的吗？</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/6a/3c618346.jpg" width="30px"><span>二桃杀三士</span> 👍（1） 💬（2）<div>老师你好，有个疑问。
修改数据之前：
    RFO 的目的是要先获得要修改的 cache block 的所有权，那就要先发出无效化指令来无效化其他核对应的这个 cache line，其他核再发出无效化确认。

修改数据之后：写失效协议要去广播一个“失效”请求告诉所有其他的 CPU 核心。其他的 CPU 核心，只是去判断自己是否也有一个“失效”版本的 Cache Block，然后把这个也标记成失效的就好了。


疑问 1：修改数据之前已经无效化其他核的 cache 了，当前 CPU 已经获得所有权了，为什么修改数据之后还要再次无效化其他核呢？岂不是多此一举了。     

当前 CPU 的这个 cache 状态是 M&#47;E 都不需要发出无效化指令，说明当前 CPU 已经拥有了相应数据的所有权，直接修改就完事了；当前 CPU cache 状态为 S 才需要无效化其他核对应的 cache 并接收无效化确认指令。


疑问 2：难道写失效协议是应用在 CPU 获取 cache 所有权时发出的无效化指令吗？但和文中描述的又有差异，写失效就是使用在修改数据之后发出的，而获取 cache 所有权却是在修改数据之前发生的。


疑问 3：《Java 并发编程的艺术》P9 上说

“在多处理器下，为了保证各个处理器的缓存是一致的，就会实现缓存一 致性协议，每个处理器通过嗅探在总线上传播的数据来检查自己缓存的值是不是过期了，当处理器发现自己缓存行对应的内存地址被修改，就会将当前处理器的缓存行设置成无效状态，当处理器对这个数据进行修改操作的时候，会重新从系统内存中把数据读到处理器缓存里。”

这里又说明了修改数据之后，回写到主存，处理器嗅探到了总线上传播的数据，就会无效化其 cache。这里的无效化又是否与写失效协议相关？为什么这里又来一次无效化呢？按我的理解，获得 cache 所有权的时候一次无效化就足够了的。不是很明白。</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（1） 💬（0）<div>在看《Java并发编程实战》这门课的时候介绍到了并发编程的可见性问题，回过头来再看这篇文章加深理解。</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/64/64/865c1eb4.jpg" width="30px"><span>劳码识途</span> 👍（1） 💬（2）<div>我了解mesif和moesi多一些，但是大体思想都是在进行源头cc流量的过滤，有一个问题我一直没有想明白，如果存在两个核心上两个s态的缓存行同时被进行了写操作，这时候会出现数据丢失吗？</div>2020-01-02</li><br/><li><img src="" width="30px"><span>Geek_103f3f</span> 👍（1） 💬（0）<div>比编译原理课程那老师讲的好多了</div>2019-12-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/f7wZYyMpQ58So4fzM8U4BIa3koXsax1O5VbISXpJtAlPZB16B2HWd8jrTO2KOE4O22UpWeKgEOsk9GSBrGocbw/132" width="30px"><span>Geek_1e090c</span> 👍（0） 💬（0）<div>独占模式也会有总线写么？</div>2024-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>### MSI 协议
- 三种状态：Modified（修改）、Shared（共享）、Invalid（无效）
- 用于多处理器系统中维护缓存一致性
- 写入Shared状态的缓存行时，需将其他核心中该缓存行置为Invalid
### MESI 相对于 MSI 的优化
- 增加了Exclusive（独占）状态
- 减少了总线通信
- 提高了缓存利用率
- 优化了写回操作，减少通知其他核心的需求
- 更高效地维护缓存一致性
</div>2024-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/bd/aa670a70.jpg" width="30px"><span>赵</span> 👍（0） 💬（0）<div>缓存一致性协议中失效状态的处理

在MESI协议中，如果CPU B试图读取一个缓存行，而该缓存行的状态为I（Invalid，失效），那么CPU B将无法从缓存中获取有效的数据。因此，CPU B需要采取以下步骤来获取所需的数据：

1. **缓存行状态检查**:
   - CPU B检查缓存行的状态，发现状态为I（失效）。

2. **从内存读取数据**:
   - 由于缓存行无效，CPU B会发出一个内存读取请求，通过系统总线从主内存中读取最新的数据。

3. **缓存行更新**:
   - CPU B从主内存中获取到最新的数据后，将该数据存储到自己的缓存行中。
   - 根据MESI协议，该缓存行的状态会设为S（Shared，共享），因为此时的数据可能也被其他处理器共享使用。

状态转换过程示意

以下是详细的状态转换过程：

1. **CPU A修改缓存行**:
   - CPU A的缓存行从E（独占）变为M（修改）。

2. **CPU A使CPU B的缓存行失效**:
   - CPU A通过总线发出失效信号，使CPU B的相应缓存行变为I（失效）。

3. **CPU A写回内存（可选）**:
   - 如果需要，CPU A将修改后的数据写回内存，缓存行状态可能从M变为E（独占），视具体情况而定。

4. **CPU B读取缓存行（发现状态为I）**:
   - CPU B试图读取数据时，发现缓存行状态为I（失效）。

5. **CPU B从内存读取数据**:
   - CPU B发出内存读取请求，通过总线从主内存中读取数据。

6. **CPU B缓存行更新**:
   - CPU B将读取到的数据存入缓存，并将缓存行状态设为S（共享）。

总结

当CPU B发现缓存行的状态为I（失效）时，会触发以下过程：
- 通过总线从主内存读取最新的数据。
- 将数据存储到缓存中，并将缓存行状态设为S（共享）。

这一过程确保CPU B能够获取最新的有效数据，并保持系统中的数据一致性。</div>2024-07-19</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>CPU高速缓存机制与业务数据库+redis机制的区别:
    1.总线的传输机制可靠性要远高于网络
    2.CPU的回写机制逻辑比较复杂，在硬件层面可以高速运转；数据库+redis的架构中如果也采用这种机制可能没有收益
    3.CPU高速缓存机制可以保证数据一致；数据库+redis在某些场景下可以容忍短暂的不一致
    4.CPU高速缓存机制在断电后内存和缓存都是空的；数据库+redis的架构在断电后，通常需要进行缓存预加载</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/64/457325e6.jpg" width="30px"><span>Sam Fu</span> 👍（0） 💬（0）<div>MESI 协议，是一种叫作写失效（Write Invalidate）的协议。在写失效协议里，只有一个 CPU 核心负责写入数据，其他的核心，只是同步读取到这个写入。
------------------------
这里应该是说同一时间，只有一个 CPU 核心在写吧。而一段时间内每个 CPU 都是可以写的？</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（0）<div>就应该把基础专栏刷几遍，总看博客连贯不起来</div>2023-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/67/aa52812a.jpg" width="30px"><span>stark</span> 👍（0） 💬（0）<div>老师写的太棒了！</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/f9/af581a47.jpg" width="30px"><span>k</span> 👍（0） 💬（0）<div>mesi和msi协议  e独占状态  不同于s共享状态需要在更新时通知其他核心，节省了写入效率</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（0）<div>请问一下，Cache line和Cache Block有什么区别呢？</div>2022-09-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mQddXC7nRiaKHTwdficicTB3bH0q5ic5UoSab51Omic7eyLBz0SNcvbLpQnNib7zP1yJFm7xxx4ia81iahfibRVnbTwHmhw/132" width="30px"><span>浮石沉木</span> 👍（0） 💬（0）<div>这一章的评论是我点赞最多的。</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/96/a0132d15.jpg" width="30px"><span>范超</span> 👍（0） 💬（0）<div>老师，这一讲的Cache Block和Cache Line是同一个东西吗</div>2022-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b6/d9/4d8a4d4c.jpg" width="30px"><span>红豆成香</span> 👍（0） 💬（0）<div>MESI和MESA有联系吗</div>2022-05-11</li><br/>
</ul>