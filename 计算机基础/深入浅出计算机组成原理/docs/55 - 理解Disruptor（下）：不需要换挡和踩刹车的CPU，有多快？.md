上一讲，我们学习了一个精妙的想法，Disruptor通过缓存行填充，来利用好CPU的高速缓存。不知道你做完课后思考题之后，有没有体会到高速缓存在实践中带来的速度提升呢？

不过，利用CPU高速缓存，只是Disruptor“快”的一个因素，那今天我们就来看一看Disruptor快的另一个因素，也就是“无锁”，而尽可能发挥CPU本身的高速处理性能。

## 缓慢的锁

Disruptor作为一个高性能的生产者-消费者队列系统，一个核心的设计就是通过RingBuffer实现一个无锁队列。

上一讲里我们讲过，Java里面的基础库里，就有像LinkedBlockingQueue这样的队列库。但是，这个队列库比起Disruptor里用的RingBuffer要慢上很多。慢的第一个原因我们说过，因为链表的数据在内存里面的布局对于高速缓存并不友好，而RingBuffer所使用的数组则不然。

![](https://static001.geekbang.org/resource/image/9c/69/9ce732cb22c49a8a26e870dddde66b69.jpeg?wh=2566%2A2059)

LinkedBlockingQueue慢，有另外一个重要的因素，那就是它对于锁的依赖。在生产者-消费者模式里，我们可能有多个消费者，同样也可能有多个生产者。多个生产者都要往队列的尾指针里面添加新的任务，就会产生多个线程的竞争。于是，在做这个事情的时候，生产者就需要拿到对于队列尾部的锁。同样地，在多个消费者去消费队列头的时候，也就产生竞争。同样消费者也要拿到锁。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIaOAxRlZjFkGfRBn420LuAcyWkMrpq5iafGdqthX5icJPjql0ibZOAdafaqbfvw4ZpVzDmsaYglVXDw/132" width="30px"><span>唐朝农民</span> 👍（30） 💬（1）<div>ReentrantLock内部不也是CAS实现的吗</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/9c/73e76b19.jpg" width="30px"><span>姜戈</span> 👍（20） 💬（3）<div>课后问题：
对比了Sequence与AtomicLong源码，在于CAS之前，Disruptor直接取原有值，做CAS操作；而AtomicLong使用了getLongVolatile获值。
两者value都用了Volatile来修饰，这点是共同的；但在于获值时，AtomicLong又再次使用volatile(getLongVolatile), 由于Volatile会在内存中强行刷新此值，相比这样就会增加一次性能的消耗，另外还有Spinlock（自旋锁），这两点都会带来性能消耗。
为什么Disruptor可以这样做，免掉getLongVolatile操作，我猜想应该是缓存行的填充，避免了伪共享（False Sharing）的问题，线程对value值的修改，不会出现不同线程同时修改同一缓存行不同变量的问题，所以不需要再次强行刷内存的步骤。

请老师指正！！！

 &#47;**    Sequence关于取值是直接Get(), 查看内部方法直接返回value
     *
     * Atomically add the supplied value.
     *
     * @param increment The value to add to the sequence.
     * @return The value after the increment.
     *&#47;
    public long addAndGet(final long increment)
    {
        long currentValue;
        long newValue;

        do
        {
            currentValue = get();
            newValue = currentValue + increment;
        }
        while (!compareAndSet(currentValue, newValue));

        return newValue;
    }

&#47;**    AtomicLong关于取值时使用getLongVolatile，查看其源码，增加了Volatile和自旋锁
     *
     * getAndAddLong
     *
*&#47;
public final long getAndAddLong(Object var1, long var2, long var4) {
        long var6;
        do {
            var6 = this.getLongVolatile(var1, var2);
        } while(!this.compareAndSwapLong(var1, var2, var6, var6 + var4));

        return var6;
    }

&#47;**    getLongVolatile源码（C++）
   *
   *   1. volatile, 刷新内存
   *   2.Spinlock, 自旋锁
   *&#47;
jlong
sun::misc::Unsafe::getLongVolatile (jobject obj, jlong offset)
{
  volatile jlong *addr = (jlong *) ((char *) obj + offset);
  spinlock lock;
  return *addr;
}</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（14） 💬（7）<div>极客时间买了13个专栏，终于完成了一个专栏的所有笔记
专栏所有笔记如下：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;10496701.html</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（11） 💬（1）<div>    专栏最开始就订阅了，看到了这篇专栏目录中的这篇文档标题，当时就想着要从底层了解disruptor的原理，也一篇一篇认真的跟了下来，不知不觉就到了今天，虽然有很多后续还是要回去时常翻阅的知识点，但是也庆幸自己能一路跟着老师到现在。
     课后思考题会去翻源码再回来补充</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/0c/f39f847a.jpg" width="30px"><span>D</span> 👍（8） 💬（2）<div>看了下jdk 1.8的 AtomicLong 和disruptor的sequence， 个人认为有两点不同：
1. disruptor 加了上一讲里面的padding, 以进一步利用缓存。
2. Atomiclong 里面提供了更多的方法，并且判断cpu是否支持无锁cas
相同点，底层都是调用unsafe类实现硬件层面的操作，以跳过jdk的限制。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/28/9c/73e76b19.jpg" width="30px"><span>姜戈</span> 👍（5） 💬（1）<div>LinkedBlockingQueue源码（JDK1.8）看了一下, 使用的是ReentrantLock和Condition来控制的，没发现老师说的synchronized关键字, 是不是哪里我忽略掉了？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/aa/abb7bfe3.jpg" width="30px"><span>免费的人</span> 👍（3） 💬（1）<div>Cas仍然会涉及到内存读取，老师能否介绍下rcu锁？</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（3） 💬（2）<div>       学习中一步步跟进：越来越明白其实真正弄明白为何学习的中间层其实是操作系统和计算机原理；就像老师的课程中不少就和操作系统相关，而在此基础上可以衍生出一系列相关的知识。
       就像老师的2个TOP：存储与IO系统，应用篇分别就是一个向下一个向上；代码题对于不做纯代码超过5年的来说有点难，跟课再去学Java有点难且时间实在不够-毕竟运维的coding能力都偏差，不过大致能明白原理，从原理层去解释一些问题的根源原因，以及某些场合下那些可能更加适用。
      其实通过操作系统和组成原理会衍生出很多知识：选择合适的方向专攻确实不错。向老师提个小的要求：希望在最后一堂课可以分享老师在做这个专栏所查阅的主要书籍，毕竟没人可以学完一遍就基本掌握的；老师所看的核心资料是我们后续再看课程提升自己的一个辅助手段吧。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/ad/52df3832.jpg" width="30px"><span>逍遥法外</span> 👍（3） 💬（1）<div>ReentrantLock内部也有CAS的操作，只不过也会有Lock的操作。Disruptor直接使用CAS，是简化了操作。</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（4） 💬（1）<div>文章中加锁和不加锁性能比较的case老师的数据是差了50倍，我在intel E5 v4和鲲鹏920下跑出来都是查了80倍。
不过其中的原因不是因为加锁，而是lock.lock() 函数自身包含了几十条指令，而++只有简单的几个指令，也就是两者指令数就差了1个数量级。
例子中不加锁性能好的另外一个原因是 ++指令 对流水线十分友好，基本能跑满流水线（IPC 跑到4)；而lock()那堆指令只能把IPC跑到0.5-0.8之间。

在只有一个线程的情况下加锁中的&quot;锁&quot;对性能是没有任何影响的，比如假设你的业务逻辑几万个指令，加上lock()多出来的几十个指令基本，基本是没有啥影响的。只有一个线程不会真正发生切换、等锁的糟心操作。只需要考虑实际指令量和对pipeline的友好程度</div>2021-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gmP4Yh00MZPwNvr4UQdLeXaX3TVyZEEp195S3vD3Sfl1xz5jBr1474Mt6w5OPr0KsrnQObfLRy5PkKNFjSBiasA/132" width="30px"><span>大头爸爸</span> 👍（3） 💬（0）<div>runIncrementWithLock()里面对每个counter++执行lock和unlock操作，可是就只有一个线程用到这个reentrantlock，那么这个lock()和unlock()应该花不了多少时间啊，也不会有多少context switch操作啊?</div>2020-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/50/26/0e9e87af.jpg" width="30px"><span>陈冰清</span> 👍（1） 💬（0）<div>老师 你有没有兴趣去量化私募行业做CTO呢 或者架构系统优化之类的岗位呢？</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/72/1f/9ddfeff7.jpg" width="30px"><span>文进</span> 👍（1） 💬（0）<div>老师，此处Java锁的例子不太准确，因为你是在单线程下获取以及释放锁，其实并没有产生锁竞争，并不会有线程上下文切换问题。所以对吧cas的程序差距不大，如果改成几个线程一起执行，抢夺一个锁，效果会更明显</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（2）<div>how  激动 ，第一遍花了大半年，终于撸完了</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/a7/16/b2ff3f70.jpg" width="30px"><span>信长</span> 👍（1） 💬（0）<div>你说到序号的时候，我以为假如有两个消费者，这两个消费者一个按着奇数的序列号消费，另一个按着偶数消费，类似这种思维，想多了吗</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（1） 💬（0）<div>compxchg [ax] ,[bx], [cx]和 UNSAFE.compareAndSwapLong(this, VALUE_OFFSET, expectedValue, newValue)d对应关系没搞明白。jdk源码到compareAndSwapLong，只有
@HotSpotIntrinsicCandidate
public final native boolean compareAndSetLong(Object o, long offset,long expected,long x);
不知道compxchg的[ax] ,[bx], [cx]和compareAndSetLong方法有什么对应关系</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/36/a7adc2dd.jpg" width="30px"><span>JaredLuo</span> 👍（0） 💬（0）<div>老师推荐阅读里的各种英文论文资料，这些论文资料都是去哪里找的？</div>2022-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKyNezT33TyZdPI8DtRe7LzV9geutjMkaNNByOkyMXhNQVia5CJE54lWrBpicftq7jdo8bCcXhokjUQ/132" width="30px"><span>Geek_337e21</span> 👍（0） 💬（0）<div>老师，有没有C++代码的例子啊？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/45/74/7a82eebb.jpg" width="30px"><span>Ins</span> 👍（0） 💬（0）<div>Ringbuffer无锁化没明白，compareAndSet可以线程安全执行，但是外面的newValue = currentValue + increment;语句（或实际的生产消费代码）不还是会出现多线程竞争吗？</div>2021-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师，锁在硬件层面的实现有相关资料推荐吗？</div>2021-04-07</li><br/><li><img src="" width="30px"><span>Geek_428412</span> 👍（0） 💬（0）<div>进一步，为什么cas还是比原始loop慢一个数量级？</div>2021-03-29</li><br/><li><img src="" width="30px"><span>Geek_428412</span> 👍（0） 💬（0）<div>为什么第一种情况下 编译器不会做常量折叠呢？</div>2021-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gmP4Yh00MZPwNvr4UQdLeXaX3TVyZEEp195S3vD3Sfl1xz5jBr1474Mt6w5OPr0KsrnQObfLRy5PkKNFjSBiasA/132" width="30px"><span>大头爸爸</span> 👍（0） 💬（0）<div>像这种用ringBuffer的基于write pointer和read pointer的模型好像不需要定义head和tail啊，producer写就更新write pointer，consumer读就更新read pointer。看了一下“Implement Lock-Free Queues”，好像搞得很复杂。不知道为什么要搞这么复杂。</div>2020-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gmP4Yh00MZPwNvr4UQdLeXaX3TVyZEEp195S3vD3Sfl1xz5jBr1474Mt6w5OPr0KsrnQObfLRy5PkKNFjSBiasA/132" width="30px"><span>大头爸爸</span> 👍（0） 💬（1）<div>RingBuffer都是用数组实现，而&quot;Implement Lock-Free Queues&quot;是基于链表，两者的原理是否一样？</div>2020-03-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gmP4Yh00MZPwNvr4UQdLeXaX3TVyZEEp195S3vD3Sfl1xz5jBr1474Mt6w5OPr0KsrnQObfLRy5PkKNFjSBiasA/132" width="30px"><span>大头爸爸</span> 👍（0） 💬（1）<div>这种ring buffer是基于write pointer和read pointer，是不是只适合一个生产者和一个消费者的情况？如果有多个生产者和消费者那就有多个write pointer和read pointer，那岂不乱了套？</div>2020-03-31</li><br/>
</ul>