你好，我是李玥。

我们在上节课中提到过，用于解决消息队列一些常见问题的知识和原理，最终落地到代码上，都包含在收、发消息这两个流程中。对于消息队列的生产和消费这两个核心流程，在大部分消息队列中，它实现的主要流程都是一样的，所以，通过这两节课的学习之后，掌握了这两个流程的实现过程。无论你使用的是哪种消息队列，遇到收发消息的问题，你都可以用同样的思路去分析和解决问题。

上一节课我和你一起通过分析源代码学习了RocketMQ消息生产的实现过程，本节课我们来看一下Kafka消费者的源代码，理清Kafka消费的实现过程，并且能从中学习到一些Kafka的优秀设计思路和编码技巧。

在开始分析源码之前，我们一起来回顾一下Kafka消费模型的几个要点：

- Kafka的每个Consumer（消费者）实例属于一个ConsumerGroup（消费组）；
- 在消费时，ConsumerGroup中的每个Consumer独占一个或多个Partition（分区）；
- 对于每个ConsumerGroup，在任意时刻，每个Partition至多有1个Consumer在消费；
- 每个ConsumerGroup都有一个Coordinator(协调者）负责分配Consumer和Partition的对应关系，当Partition或是Consumer发生变更时，会触发rebalance（重新分配）过程，重新分配Consumer与Partition的对应关系；
- Consumer维护与Coordinator之间的心跳，这样Coordinator就能感知到Consumer的状态，在Consumer故障的时候及时触发rebalance。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/57/f6/2c7ac1ad.jpg" width="30px"><span>Peter</span> 👍（24） 💬（2）<div>课后作业，希望老师指正。
在基础篇03的时候讲过消费位置是消息队列服务器针对每个消费组和每个队列维护的一个位置变量。那么也就是说最终真正更新这个位置变量应该是交由服务器去执行的，而Consumer只是发送一个请求。那么顺着这个思路，我猜应该是在更新元数据的时候就应该发送这个请求，原因很简单：消费者需要知道“从哪发起”并且“发多少”，因此这时就已经知道了应该将消费位置更新为多少了，所以这时候就可以发送这个请求了。至于服务器最终会将消费位置更新为多少，还取决于客户端返回的结果。
在方法updateAssignmentMetadataIfNeeded中，最后一行return updateFetchPositions(timer);
从updateFetchPositions这个方法点进去，看到coordinator.refreshCommittedOffsetsIfNeeded(timer)
这个方法点进去之后会看到fetchCommittedOffsets方法，进这个方法，找到sendOffsetFetchRequest，点进去，最终会发现  client.send(coordinator, requestBuilder)</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/14/f1532dec.jpg" width="30px"><span>鲁班大师</span> 👍（7） 💬（3）<div>老师，kafak consumer 在reblance期间，如何实现不重复消费</div>2020-06-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（6） 💬（4）<div>老师，你好，broker和消费端都重启了，消费端还知道从哪个offset开始消费吗</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（4） 💬（1）<div>老师您好：
          kafka consumer中没有分析到心跳线程是怎么处理的，我看源代码上写的是单独开了一个后台线程负责心跳，这样处理的优势是什么啊？</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/14/f1532dec.jpg" width="30px"><span>鲁班大师</span> 👍（3） 💬（1）<div>每个 ConsumerGroup 都有一个 Coordinator(协调者）负责分配 Consumer 和 Partition 的对应关系，当 Partition 或是 Consumer 发生变更时，会触发 rebalance（重新分配）过程，重新分配 Consumer 与 Partition 的对应关系；……在rebalance期间应该是不能消费的吧</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f8/3a/e0c14cb3.jpg" width="30px"><span>lizhibo</span> 👍（1） 💬（4）<div>老师好，kafka消息要是在消费端消费出现异常了怎么办，他没有再次消费的机制，比如1分之后再去消费，这个怎么实现</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/85/e9/3854e59a.jpg" width="30px"><span>SKang</span> 👍（1） 💬（1）<div>老师 我看完之后 可以理解为 消费组A 消费一个cc主题的消息，然后过程中我将消费组A 的名字改成消费组B后，不会出现重复消费，只会接着A的 继续消费剩下的吧 我认为毕竟A已经成功消费了 偏移量已经成功被更新了吧</div>2020-03-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（1） 💬（5）<div>消费者如何从服务端拉取消息的，用for循环效率太低吧，能否说说实际的代码</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/47/7c3baa15.jpg" width="30px"><span>蛤蟆先生</span> 👍（0） 💬（1）<div>有个问题请教一下老师，目前我们公司某个应用在生产环境一共有两台机器，这时候有一台机器挂了，但是某个消息还是会经常消费到这台挂的机器上，导致消息没有消费成功，这是为什么呢？</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fe/14/f1532dec.jpg" width="30px"><span>鲁班大师</span> 👍（0） 💬（3）<div>多个consumer消费同一个partition会有什么问题么</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6e/a8/ee6bc8a5.jpg" width="30px"><span>LY</span> 👍（0） 💬（1）<div>当 Partition 或是 Consumer 发生变更是，会触发 reblance（重新分配）过程。
这句话有两个错别字。。。</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（0） 💬（1）<div>上一节课我和你一起通过分析源代码学习了 RocketMQ 消息生产的实现过程，本节课我们来看一下 Kafka 消费者的源代码，理清 Kafka 消费的实现过程，并且能从中学习到一些 Kafka 的优秀设计思路和编码技巧。

老师，为什么上一讲是Rabbit这一讲是kafka?</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（0） 💬（5）<div>老师好，看了Rocketmq consumer源码，为啥启动consumer实例的时候也会初始化producer，是为了提交消费位点吗？</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/25/31/1ee460ab.jpg" width="30px"><span>米兰铁匠</span> 👍（0） 💬（1）<div>用代码跟类图来讲解一个系统的实现还是太过于抽象，难以把握住，最好的方式是用老师理解的东西然后转换成通俗易懂的原理图来讲解</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（48） 💬（5）<div>我们需要一些速成的实战经验，比如消息队列突然延迟2个小时该如何解决？
希望带着这些类似的问题，结合设计原理，帮助我们层层解析。。。</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/29/1b1234ed.jpg" width="30px"><span>DFighting</span> 👍（8） 💬（0）<div>offset的提交不知道是不是在kafkaConsumer.commitAsync中调用coordinator.commitOffsetsAsync(offsets,callback)
1、这里设计成异步方式一开始我是比较奇怪的，他是如何保证offset不丢失呢？看了代码才知道在异步返回前会等待ConcurrentLinkQueue&lt;offsetCommitCompletetion&gt;中没有其他的待处理的其他的offset的commit后，才会返回，这里的非阻塞队列是线程安全的，可以避免当前提交冲掉其他的offset的提交
2、真正进行提交的时候也不是调用什么具体操作net的接口，而是向另一个ConcurrentLinkedQueue中注册了一个RequestFutureListener的监听者，当然注册之前使用了AtomicInteger来保证并发安全。
3、每个监听者应该都会由相应的Coordinator轮询处理队列中的待提交请求，将offset提交从具体的Consumer中解耦到每个组的Coordinator中。
当然以上只是个人理解，如有不当欢迎指正。
读完这个代码，我发现kafka在这里保证并发数据一致性时，使用了安全的数据结构+CAS的数据访问，灵活且大大降低了锁机制的粗粒度带来的性能损耗，只是这个代码真不容易写好，真是大牛作品！！</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/51/4155b021.jpg" width="30px"><span>于成龙</span> 👍（3） 💬（1）<div>分析了下acquireAndEnsureOpen如何加锁，供大家参考

private void acquireAndEnsureOpen() {
    acquire();
    &#47;&#47;KafkaConsumer成员变量，初始值为false，调用close(Duration)方法后才会置为true
    if (this.closed) {
        release();
        throw new IllegalStateException(&quot;This consumer has already been closed.&quot;);
    }
}

&#47;&#47;变量声明
private static final long NO_CURRENT_THREAD = -1L;

private void acquire() {
    &#47;&#47;拿到当前线程的线程id
    long threadId = Thread.currentThread().getId();
    &#47;*if threadId与当前正执行的线程的id不一致（并发，多线程访问）&amp;&amp; threadId对应的线程没有争抢到锁
    	 then 抛出异常
   	举例：
   		现在有两个KafkaConsumer线程，线程id分别是thread1, thread2，要执行acquire()方法。
		thread1先启动，执行完上面这条语句、赋值threadId后， thread1栈帧中threadId=thread1，此时CPU线程调度、执行thread2，
		thread2也走到if语句时，在thread2的栈帧中，threadId已经赋值为thread2，走到这里，currentThread作为成员变量，初始值为NO_CURRENT_THREAD（-1），因此必然不相等，继续走第二判断条件，即利用AtomicInteger的CAS操作，将当前线程id threadId(thread2)赋值给currentThread这个AtomicInteger，必然返回true，因此会继续执行，使得refcount加1；
		接着，此时执行thread1，那么再继续执行if，threadId(thread1) != currentThread.get() (thread2)能满足，但是currentThread的CAS赋值将会失败，因此此时currentThread的值并不是NO_CURRENT_THREAD。
		
		refcount用于记录重入锁的情况，参见release()方法，当refcount=0时，currentThread将重新赋值为NO_CURRENT_THREAD，保证彻底解锁。
    *&#47;
    if (threadId != currentThread.get() &amp;&amp; !currentThread.compareAndSet(NO_CURRENT_THREAD, threadId))
        throw new ConcurrentModificationException(&quot;KafkaConsumer is not safe for multi-threaded access&quot;);
    refcount.incrementAndGet();
}</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（0）<div>   先打卡：代码慢慢研究；老师今天讲述了研究代码的目的：
   1.消息队列实现的主要流程都一样，掌握流程的实现过程；遇到收发消息的问题，都可以用同样的思路去分析和解决问题。
   2.看一下源代码，理清消费生产的实现过程，从中学习一些优秀的设计思路和编码技巧。
   这个算是一个小的总结吧：明天中秋休息刚好可以啃代码，好好研究代码去体会。
   明天是中秋佳节：愿老师节日快乐^_^</div>2019-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XeGpHsAib2ZBic8PsR7z18plF2AccJ6Op5WmRDnv4Y9Vkmdiba9ibbcQSPGLJ1yuACAhkLQVQZHSz9WUcNj7UKSw6Q/132" width="30px"><span>Geek_ba3598</span> 👍（0） 💬（0）<div>对于pollForFetches方法，在执行client.poll的时候，如果是异步架构，不应该是只发送请求然后就返回吗？response由回调线程来处理，结果放到completedFetches中，然后下次再调用pollForFetches方法时，通过fetcher.fetchedRecords方法就可以获取到上一次请求的数据了。如果在当前线程中发送请求并处理响应，那不是同步逻辑吗？因为不是得等待broker返回响应吗</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/f6/b5394713.jpg" width="30px"><span>小杨</span> 👍（0） 💬（0）<div>我有个疑问，1个topic，3个partition，增加consumer数量能提升消费速度么？或者说kafka应该如何提升消费能力。期待老师解答。</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/03/c5/600fd645.jpg" width="30px"><span>tianbingJ</span> 👍（0） 💬（0）<div>大部分内容都在讨论网络、CAS、异步啊等等知识对于实现一个系统多么重要；但是，各种框架实现的场景都会用到这些内容，总不能所有的课程都先罗列一遍这些内容吧。
即使介绍，花个两三节课差不多就行了，占比过大；结果就是跑题了，没有聚焦在MQ上。</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/64/457325e6.jpg" width="30px"><span>Sam Fu</span> 👍（0） 💬（0）<div>老师 我最近看了rocketmq消费的源码，您看看我的理解对不对。
rocketmq consumer消费完消息后，其实不管成功或失败都会提交这批信息的最大位移。 如果存在失败的消息，则会将整个这一批消息全部发到重试队列去。这样的话，之前消费过的消息就会重复消费了。
所以每批拉取的消息设置的不能太大，否则有一条失败整个都得重试，重试率会增高</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/aa/6b/ab9a072a.jpg" width="30px"><span>对与错</span> 👍（0） 💬（1）<div>请问kafka消费者使用手动提交位移的方式，当前消费进度为10，,然后消费几条失败之后，提交位移失败，后面消费新的消息成功之后，当前消费进度被更新为15，那中间消费失败的几条消息会随着重启消费者而重新消费吗？位移主题里面的消费进度会随着重启消费者而被删除吗?如果不被删除，那应该不会重新消费失败的那几条消息吧？</div>2020-10-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rHcOA80Xqhe4PJ9S38AzqD2zhrMjK92D7lvH8D3feuHkjiaHTIks5LQvOYjLWZr9mjFklv04jI2Wciahk7x2o8YA/132" width="30px"><span>Geek_411c57</span> 👍（0） 💬（0）<div>老师您好，我想问下: 客户端拉取消息的时候是同步拉取吗？如果是同步拉取的话应该会占用连接吧？为什么不是用异步监听io事件呢？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/43/50/abb4ca1e.jpg" width="30px"><span>凡</span> 👍（0） 💬（0）<div>提交位置是在ConsumerCoordinator类提供了同步异步提交方法，具体提交位置可以查看到调用这几个方法的位置 </div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/06/f5979d65.jpg" width="30px"><span>亚洲舞王.尼古拉斯赵四</span> 👍（0） 💬（0）<div>这篇文章真的好深，看了好几遍才明白，异步的设计好复杂，现在明白前面为什么老师讲那些基础了</div>2019-10-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（0） 💬（0）<div>消费端重启的时候，他会从哪里拿offset呢？他是从头还是拿消息还是从上次消费的地方？这个offset能讲讲吗？</div>2019-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（0） 💬（0）<div>老师，主题和分区，以及分区和ConsumerGroup到底是几对几的关系</div>2019-09-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQ0NueqD3LTRravKIH2DgtqFKLqgjZQicDZtibdTqJ8pBRjNwlKornibGj2qibPdsgLXh2xQ3MesQ7q2JyATIEBphVHpcS2iaboZqATms4IDUibes/132" width="30px"><span>山头</span> 👍（0） 💬（0）<div> ConsumerGroup，和分区什么关系，有多少个ConsumerGroup呢</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/17/8763dced.jpg" width="30px"><span>微微一笑</span> 👍（0） 💬（1）<div>老师好，先祝您节日快乐！！！您辛苦了~
有几个疑问需要老师解答一下：
①今天在看rocketMq源码过程中，发现DefaultMQProducer有个属性defaultTopicQueueNums，它是用来设置topic的ConsumeQueue的数量的吗？我之前的理解是，consumeQueue的数量是创建topic的时候指定的，跟producer没有关系，那这个参数又有什么作用呢？
②在RocketMq的控制台上可以创建topic，需要指定writeQueueNums，readQueueNums，perm，这三个参数是有什么用呢？这里为什么要区分写队列跟读队列呢？不应该只有一个consumeQueue吗？
③用户请求--&gt;异步处理---&gt;用户收到响应结果。异步处理的作用是：用更少的线程来接收更多的用户请求，然后异步处理业务逻辑。老师，异步处理完后，如何将结果通知给原先的用户呢？即使有回调接口，我理解也是给用户发个短信之类的处理，那结果怎么返回到定位到用户，并返回之前请求的页面上呢？需要让之前的请求线程阻塞吗？那也无法达到【用更少的线程来接收更多的用户请求】的目的丫。
望老师能指点迷津~~~</div>2019-09-12</li><br/>
</ul>