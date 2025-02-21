从今天开始，我们就进入案例分析模块了。 这个模块我们将分析四个经典的开源框架，看看它们是如何处理并发问题的，通过这四个案例的学习，相信你会对如何解决并发问题有个更深入的认识。

首先我们来看看**Guava RateLimiter是如何解决高并发场景下的限流问题的**。Guava是Google开源的Java类库，提供了一个工具类RateLimiter。我们先来看看RateLimiter的使用，让你对限流有个感官的印象。假设我们有一个线程池，它每秒只能处理两个任务，如果提交的任务过快，可能导致系统不稳定，这个时候就需要用到限流。

在下面的示例代码中，我们创建了一个流速为2个请求/秒的限流器，这里的流速该怎么理解呢？直观地看，2个请求/秒指的是每秒最多允许2个请求通过限流器，其实在Guava中，流速还有更深一层的意思：是一种匀速的概念，2个请求/秒等价于1个请求/500毫秒。

在向线程池提交任务之前，调用 `acquire()` 方法就能起到限流的作用。通过示例代码的执行结果，任务提交到线程池的时间间隔基本上稳定在500毫秒。

```
//限流器流速：2个请求/秒
RateLimiter limiter = 
  RateLimiter.create(2.0);
//执行任务的线程池
ExecutorService es = Executors
  .newFixedThreadPool(1);
//记录上一次执行时间
prev = System.nanoTime();
//测试执行20次
for (int i=0; i<20; i++){
  //限流器限流
  limiter.acquire();
  //提交任务异步执行
  es.execute(()->{
    long cur=System.nanoTime();
    //打印时间间隔：毫秒
    System.out.println(
      (cur-prev)/1000_000);
    prev = cur;
  });
}

输出结果：
...
500
499
499
500
499
```

## 经典限流算法：令牌桶算法

Guava的限流器使用上还是很简单的，那它是如何实现的呢？Guava采用的是**令牌桶算法**，其**核心是要想通过限流器，必须拿到令牌**。也就是说，只要我们能够限制发放令牌的速率，那么就能控制流速了。令牌桶算法的详细描述如下：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（71） 💬（7）<div>re：为什么令牌是从令牌桶中出的，那么 next 就无需增加一个 interval？

next 变量的意思是下一个令牌的生成时间，可以理解为当前线程请求的令牌的生成时刻，如第一张图所示：线程 T1 的令牌的生成时刻是第三秒。

线程 T 请求时，存在三种场景：
1. 桶里有剩余令牌。
2. 刚创建令牌，线程同时请求。
3. 桶里无剩余令牌。

场景 2 可以想象成线程请求的同时令牌刚好生成，没来得及放入桶内就被线程 T 拿走了。因此将场景 2 和场景 3 合并成一种情况，那就是桶里没令牌。即线程请求时，桶里可分为有令牌和没令牌。

“桶里没令牌”，线程 T 需要等待；需要等待则意味着 now(线程 T 请求时刻) 小于等于 next(线程 T 所需的令牌的生成时刻)。这里可以想象一下线程 T 在苦苦等待令牌生成的场景，只要线程 T 等待那么久之后，就会被放行。放行这一刻令牌同时生成，立马被线程拿走，令牌没放入桶里。对应到代码就是 resync 方法没有进入 if 语句内。

“桶里有令牌”，线程 T 不需要等待。说明线程 T 对应的令牌已经早早生成，已在桶内。代码就是：now &gt; next（请求时刻大于对应令牌的生成时刻）。因此在分配令牌给线程之前，需要计算线程 T 迟到了多久，迟到的这段时间，有多少个令牌生成¹；然后放入桶内，满了则丢弃²；未来的线程的令牌在这个时刻已经生成放入桶内³（即 resync 方法的逻辑）。线程无需等待，所以不需要增加一个 interval 了。

角标分别对应 resync 方法内的代码：
¹: long newPermits=(now-next)&#47;interval;
²: storedPermits=min(maxPermits, 
        storedPermits + newPermits);
³: next = now;</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/8c/d9330d2b.jpg" width="30px"><span>花儿少年</span> 👍（27） 💬（7）<div>很精髓的就是reserve方法，我来试着稍微解释一下
首先肯定是计算令牌桶里面的令牌数量
然后取令牌桶中的令牌数量storedPermits 与当前的需要的令牌数量 1 做比较，大于等于 1，说明令牌桶至少有一个令牌，此时下一令牌的获取是不需要等待的，表现为 next 不需要变化；而当令牌桶中的令牌没有了即storedPermits等于 0 时，next 就会变化为下一个令牌的获取时间，注意 nr 的值变化</div>2019-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（19） 💬（4）<div>有个疑问：高并发情况下单独一个线程维护一个队列放令牌，性能上扛不住，那么获取令牌时每次加锁去计算性能就可以抗的主？是根据什么依据来判断性能的呢？</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（17） 💬（2）<div>老师，请教一下，限流器和信号量为什么感觉一样的，那为什么2个还都存在？是因为业务场景不同吗？请老师解惑下</div>2019-05-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epLhKkTgowm9PqUwP9k90DecpOU7HQ0IRuAp515kIonbfyqYm6ME7s2bmaPX0sSA14micZ2DAfLLibw/132" width="30px"><span>zsh0103</span> 👍（8） 💬（1）<div>老师好，问个问题。文中代码b=3，r=1&#47;s时，如果在next之后同时来了3个请求，应该时都可以获得令牌的对吧。就是说这3个请求都可以执行。那岂不是违背了r=1&#47;s的限制吗。
</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/8c/97b2f2ba.jpg" width="30px"><span>刘鸿博</span> 👍（5） 💬（2）<div>newPermits, storePermits, fb, nr 都应该是double, 而不是long. </div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（5） 💬（1）<div>还有就是老师我问一下因为我不是在互联网公司工作接触高并发场景少，我又喜欢学习研究提高自己，是不是得多看多练，实战</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/cb/f8157ad8.jpg" width="30px"><span>爱吃回锅肉的瘦子</span> 👍（4） 💬（1）<div>老师，有没什么资料推荐关于guava预热功能呢？主要网上资料太繁杂，不知道要如何甄别哪些是比较经典的</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/77/5c/5d6fb47b.jpg" width="30px"><span>小强（jacky）</span> 👍（3） 💬（1）<div>老师请教个问题，maxPermits&#47;next 的变量在程序里面，不同线程之间存在依赖关系，这不是数据竞争吗？为啥这里没有加对应的锁？</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（3） 💬（2）<div>很精彩！老师应该去讲数据结构与算法:)</div>2019-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（1） 💬（1）<div>不知道课程结束后，老师还会出来答疑不？</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/75/e346e04e.jpg" width="30px"><span>一个慢慢爬行的普通人</span> 👍（1） 💬（1）<div>老师，我刚刚应该是想错了，线程池任务提交频繁是不是导致线程池存储任务队列不断扩大，从而可能会导致系统不稳定，但是这方面线程池也可以用有界队列来控制，所以不太清楚是什么能够导致系统不稳定</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/68/a05fb728.jpg" width="30px"><span>韩大</span> 👍（1） 💬（1）<div>guava的ratelimit好像是阻塞的，而不是抛弃请求，这样会不会导致用户响应时间过长的问题？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/76/89/3b15e9e6.jpg" width="30px"><span>一一</span> 👍（0） 💬（1）<div>老师你好，请问在高并发场景下定时器与线程睡眠的差距是怎样的？</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/95/6d/bc01fdf7.jpg" width="30px"><span>白</span> 👍（0） 💬（1）<div>令牌桶的平滑特性这里怎么体现呢？
比如1秒钟10个令牌这个算法里会在第一毫秒耗尽，而不是平滑的分散在1秒里吧？</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/1f/8e304ec0.jpg" width="30px"><span>卖火柴的托儿索</span> 👍（0） 💬（1）<div>老师，请问您用的是什么画图工具？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7c/63/115a4b23.jpg" width="30px"><span>静海</span> 👍（0） 💬（3）<div>老师，请教下接收rocketmq消息，能否采用限流器Guava RateLimiter进行限流? 要怎么做?</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/a3/d7e5fe8a.jpg" width="30px"><span>0xABC</span> 👍（0） 💬（1）<div>限流器老师讲的浅显易懂，发现有些同学有些疑问，试着解答一下。

1. 是否会有并发问题？
并发问题应该是不存在的，限流器的竞争资源是令牌（permit），实现中令牌是动态计算出来的，增加了并发访问控制，synchronized reverse()，这里的同步仅仅是加在了预占令牌上，非常好的设计
2. maxPermits 大于1的代码没看懂？
分了两种情况，下一个令牌产生时间落后于当前时间时，需要重置下一次令牌产生时间和计算令牌桶中可用的令牌；然后，所有的请求都按照相同的令牌获取算法，代码中在计算能获得令牌的时间时，又分了两种情况，令牌桶中有令牌和没有令牌，没有令牌的时候需要计算下一次产生令牌的时间，有令牌的时候需要减去令牌桶中的令牌，这就是那几行比较晦涩一些代码要做的事情

自己的浅显理解</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（0） 💬（1）<div>guava ratelimiter 容量上限在哪个参数中体现或者在哪设置这个。比如我们设置的流速是 2&#47;s,当100s之内都没有请求到来，是不是会往令牌桶中持续放入200个令牌， 而这这时候突然来了一波300个并发请求，是不是200个请求可以被调用，剩下100个请求被阻塞慢慢释放。是这样的？</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/99/42929758.jpg" width="30px"><span>andy</span> 👍（0） 💬（1）<div>我有个疑问，这个令牌桶算法，多线程当中不会有问题么？还是我认为的使用场景不对，有点蒙</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7c/b5/4a7a2bd4.jpg" width="30px"><span>Sunqc</span> 👍（0） 💬（1）<div>皮一下，老王，这一节挺深奥的，哈哈哈</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/37/12e4c9c9.jpg" width="30px"><span>高源</span> 👍（0） 💬（2）<div>老师想请教个实际问题，假设单机做服务器端win和下面Linux应用程序实时socket通信，每个消息交互时间大概10毫秒，我现在想提速，想把交互时间变成0.1毫秒，有啥方法解决此问题，服务器端承载业务处理逻辑和数据库读写操作，谢谢，我现在不清楚这个问题如何解决，我想法是更换网络框架，例如换成netty框架</div>2019-05-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz3icr3mGs5ib8FbSPQZ2ic3ib90mHkd1btQrmGacZjJxfYXrerIdaTxglKyCicFzLcEAb6deC2cWjE5Q/132" width="30px"><span>the geek</span> 👍（5） 💬（5）<div>老师，当b&gt;1时的reserve方法写的有问题吧，long at = next;不应该是第一行，而应该在&#47;&#47; 重新计算下一令牌产生时间
    next = next + nr*interval;
这行代码之后吧</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/c8/bed1e08a.jpg" width="30px"><span>辣椒</span> 👍（5） 💬（10）<div>&#47;&#47; 令牌净需求：首先减掉令牌桶中的令牌
    		long nr = 1 - fb;
    		&#47;&#47; 重新计算下一令牌产生时间
    		next = next + nr*interval;
    		&#47;&#47; 重新计算令牌桶中的令牌
    		this.storedPermits -= fb;

老师这儿没有看懂，能不能解释一下？</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/4f/ff1ac464.jpg" width="30px"><span>又双叒叕是一年啊</span> 👍（5） 💬（2）<div>long interval = 1000_000_000;
这是什么写法</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/14/c2/46ebe3a0.jpg" width="30px"><span>侧耳倾听</span> 👍（4） 💬（0）<div>时间那个其实就是当前请求时间超过上次令牌的取得时间，我就发令牌，令牌满了就不发只取，有空间了继续发，总之就是一秒一个，通过时间差算出，来一个请求就算一次时间，没必要通过定时器去实现</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/8c/ff48ece3.jpg" width="30px"><span>小乙哥</span> 👍（2） 💬（0）<div>http:&#47;&#47;ifeve.com&#47;guava-ratelimiter&#47;
RateLimiter的文档翻译，mark一下</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/c7/d66952bc.jpg" width="30px"><span>Happy</span> 👍（2） 💬（1）<div>老师，经过单元测试后，个人感觉 resync 方法有bug。resync 的功能仅仅是将时间转换为令牌的操作，并更新下一次产生令牌的时间。不消耗令牌。
resync 方法中 &#47;&#47;新产生的令牌数
long newPermits = (now - next) &#47; interval; 这一步中，假如 now - next 为 1.9 秒，interval 为1秒，那么除法后，会将 0.9 秒丢弃，长期这种操作，会导致错误越来越多。我这边做了一个补偿操作：
long diff = (now - next) % interval;
 &#47;&#47; 将下一个令牌发放时间重置为当前时间
next = now - diff;

单元测试在 https:&#47;&#47;github.com&#47;1996fanrui&#47;fanrui-learning&#47;blob&#47;755cb85bfc84981ba3a0309cc4fee91035e7ee25&#47;module-juc&#47;src&#47;test&#47;java&#47;com&#47;dream&#47;juc&#47;ratelimiter&#47;RateLimiterTest.java

虽然课程早就结束了，但还是非常期待老师的反馈。</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/40/e0/2f1816a8.jpg" width="30px"><span>speedy9</span> 👍（2） 💬（2）<div>老师，前一个桶大小为1的代码是不是写错了，&#47;&#47; 返回线程需要等待的时间 应该是return Math.max(at-now,0)吧
</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（2） 💬（0）<div>桶容量为1的时候，我能理解。但是桶容量为多个的时候，就不理解了，比如
&#47;&#47; 新产生的令牌数
      long newPermits=(now-next)&#47;interval;
这句，不应该1秒生成桶的总容量吗？假设now为2，next为1。interval也为1。那么一个周期也就产生一个令牌啊？</div>2019-05-25</li><br/>
</ul>