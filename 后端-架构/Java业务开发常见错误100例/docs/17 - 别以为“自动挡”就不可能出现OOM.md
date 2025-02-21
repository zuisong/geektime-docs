你好，我是朱晔。今天，我要和你分享的主题是，别以为“自动挡”就不可能出现OOM。

这里的“自动挡”，是我对Java自动垃圾收集器的戏称。的确，经过这么多年的发展，Java的垃圾收集器已经非常成熟了。有了自动垃圾收集器，绝大多数情况下我们写程序时可以专注于业务逻辑，无需过多考虑对象的分配和释放，一般也不会出现OOM。

但，内存空间始终是有限的，Java的几大内存区域始终都有OOM的可能。相应地，Java程序的常见OOM类型，可以分为堆内存的OOM、栈OOM、元空间OOM、直接内存OOM等。几乎每一种OOM都可以使用几行代码模拟，市面上也有很多资料在堆、元空间、直接内存中分配超大对象或是无限分配对象，尝试创建无限个线程或是进行方法无限递归调用来模拟。

但值得注意的是，我们的业务代码并不会这么干。所以今天，我会从内存分配意识的角度通过一些案例，展示业务代码中可能导致OOM的一些坑。这些坑，或是因为我们意识不到对象的分配，或是因为不合理的资源使用，或是没有控制缓存的数据量等。

在[第3讲](https://time.geekbang.org/column/article/210337)介绍线程时，我们已经看到了两种OOM的情况，一是因为使用无界队列导致的堆OOM，二是因为使用没有最大线程数量限制的线程池导致无限创建线程的OOM。接下来，我们再一起看看，在写业务代码的过程中，还有哪些意识上的疏忽可能会导致OOM。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/f3/8b/a629f9d4.jpg" width="30px"><span>一个汉子~</span> 👍（27） 💬（3）<div>针对第二点，可以先compile，然后在内存中保存，脚本内容的hash作为key，compile结果作为value，用ConcurrentReferenceHashMap保存
同样的风险还出现在表达式框架aviator中</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（12） 💬（3）<div>试着回到下问题：
第一个：
肯定是软引用，因为弱引用是只要GC执行，扫描到就被回收，缓存的作用是为了提高速度，要有一定的存在周期；如果是弱引用，每次GC执行，缓存被回收，缓存命中率超低，完全达不到缓存的作用，而又要维护缓存和DB的数据一致性问题，得不偿失。
第二个：
第一种不完美的方案：GroovyShell不要设置成全局的，每次运行时，都创建一个GroovyShell，然后限制元数据区大小，当元数据回收时，GroovyShell和该GroovyShell加载的类一起被回收；
第二种方法：GroovyShell设置为全局的，然后使用缓存，每次都是先从缓存中获取，获取不到了，在加载，然后更新缓存。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/2a/33441e2b.jpg" width="30px"><span>汝林外史</span> 👍（12） 💬（1）<div>1. 对于老师说的autoComplete的场景是不是Trie树更适合一些？
2. 这个WeakReference可能导致内存溢出的典型就是ThreadLocal，虽然ThreadLocalMap的entry的key是weakReference，但是value是强引用，当用线程池的时候，就会内存溢出，还是要自己remove才行。
3. 对于问题1，应该是用软引用更好一些，用弱引用总是被gc回收就失去了缓存的意义。对于问题2不是很了解。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（9） 💬（2）<div>应该用哪种引用，首先考虑的肯定是四大引用的区别。
1.强引用：最常见的一种，只要该引用存在，就不会被GC。
2.软引用：内存空间不足时，进行回收。
3.弱引用：当JVM进行GC时，则进行回收，无论内存是否充足。
4.虚引用：这个不提了，因为我也完全不懂。

软引用和弱引用，这两个，让我选，肯定是选软引用。因为弱引用，被回收的频率更高。缓存，如果经常被回收的话，就达不到最大利用率。

但是这里又要说点额外的，单说缓存设计，还要涉及其他的因素。包括缓存大小，缓存的过期时间等。让我来说的话，我可能会考虑使用现有的缓存实现，或者是redis。自己实现一套缓存，成本略高。</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f3/8b/a629f9d4.jpg" width="30px"><span>一个汉子~</span> 👍（8） 💬（3）<div>之前还遇到一个，一个导出功能，拥有管理员权限的人几乎没有限制，造成了全表查，再加上框架禁止join，所以又把外键拉出来做了一次in查询，也是全表扫，大量的Bo对象和超长sql，直接把系统oom了</div>2020-04-18</li><br/><li><img src="" width="30px"><span>不能忍的地精</span> 👍（7） 💬（1）<div>我遇到一个OOM,是这样的
1. 首先有一个线程池,线程数量是20个,但是线程队列容器的数量是Integer的最大值,所以拒绝策略几乎无效,大概没过3秒往线程池提交3个任务
2. 任务里面有一个Restemplate,没有设置超时时间,超时时间为-1,并且里面维护的连接池是5个,小于线程池数量
3. 出现5个连接都超时,任务卡住了,但是还是不断的往任务队列里面添加任务,最终导致OOM</div>2020-04-24</li><br/><li><img src="" width="30px"><span>ddosyang</span> 👍（2） 💬（1）<div>老师想问一下，在WeakHashMap的那个例子里，可不可以直接用String name当作Key，而不是用User做Key。这样是不是也可以解决问题？</div>2020-04-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLwTZdUafC5YM7bCASt8icUnoyYfV4hUHulexibDI7B4eaokTxYXHFtoic97DBlCAU9j5Jw4QUuGhyZQ/132" width="30px"><span>Carisy</span> 👍（1） 💬（1）<div>老师请教一个问题，在使用CompletableFuture的时候出现了很奇怪的场景，就是buffers飙升出现oom，应用程序使用内存并不多，处理逻辑也相对简单就是调用接口通过http上传下载文件</div>2020-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（1） 💬（2）<div>有点没懂 java.lang.IllegalArgumentException: Request header is too large 的意思不就是request header过大了么 为什么开发人员还设置的那么大？</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（3）<div>问题一，弱引用是在内存不足时被 gc 掉，而软引用是只要 gc 就回收掉，自然就不能用来做缓存，否则动不动就缓存失效，数据库怕是要被玩坏哦，因为适合做缓存的是弱引用。
问题二，没用过 groovy，希望看到别人的解答。😄</div>2020-04-18</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（2） 💬（1）<div>周六第一件事跟上老师进度</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/95/3b/a7c94a53.jpg" width="30px"><span>自由港</span> 👍（2） 💬（0）<div>关于第二个向题限制了metadata的堆大小，发现就可自动回收了</div>2020-04-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ZJjl8bEt5zdqufZ304Ra0eibWtJPoVqpMjhu5xgd0o2oAj1ib6MBBWicHzTSFkEPiahxWwiaGsPib4S6N38kCFF0pDDg/132" width="30px"><span>Geek_d432e7</span> 👍（0） 💬（0）<div>专栏内容非常具有参考价值，希望能够多推送此类专栏。</div>2023-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/93/7e/4f9a11af.jpg" width="30px"><span>子陌.</span> 👍（0） 💬（0）<div>享元模式</div>2023-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/ca/86d58e40.jpg" width="30px"><span>yang</span> 👍（0） 💬（0）<div>技术方案也够奇葩的------------怎么设计出来的-----~-~----</div>2020-04-20</li><br/>
</ul>