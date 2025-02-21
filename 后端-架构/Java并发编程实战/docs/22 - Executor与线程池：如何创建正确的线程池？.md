虽然在Java语言中创建线程看上去就像创建一个对象一样简单，只需要new Thread()就可以了，但实际上创建线程远不是创建一个对象那么简单。创建对象，仅仅是在JVM的堆里分配一块内存而已；而创建一个线程，却需要调用操作系统内核的API，然后操作系统要为线程分配一系列的资源，这个成本就很高了，所以**线程是一个重量级的对象，应该避免频繁创建和销毁**。

那如何避免呢？应对方案估计你已经知道了，那就是线程池。

线程池的需求是如此普遍，所以Java SDK并发包自然也少不了它。但是很多人在初次接触并发包里线程池相关的工具类时，多少会都有点蒙，不知道该从哪里入手，我觉得根本原因在于线程池和一般意义上的池化资源是不同的。一般意义上的池化资源，都是下面这样，当你需要资源的时候就调用acquire()方法来申请资源，用完之后就调用release()释放资源。若你带着这个固有模型来看并发包里线程池相关的工具类时，会很遗憾地发现它们完全匹配不上，Java提供的线程池里面压根就没有申请线程和释放线程的方法。

```
class XXXPool{
  // 获取池化资源
  XXX acquire() {
  }
  // 释放池化资源
  void release(XXX x){
  }
}  
```

## 线程池是一种生产者-消费者模式

为什么线程池没有采用一般意义上池化资源的设计方法呢？如果线程池采用一般意义上池化资源的设计方法，应该是下面示例代码这样。你可以来思考一下，假设我们获取到一个空闲线程T1，然后该如何使用T1呢？你期望的可能是这样：通过调用T1的execute()方法，传入一个Runnable对象来执行具体业务逻辑，就像通过构造函数Thread(Runnable target)创建线程一样。可惜的是，你翻遍Thread对象的所有方法，都不存在类似execute(Runnable target)这样的公共方法。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/c2/196932c7.jpg" width="30px"><span>南琛一梦</span> 👍（132） 💬（6）<div>回答下Lrwin和张天屹同学的问题：当线程池中无可用线程，且阻塞队列已满，那么此时就会触发拒绝策略。对于采用何种策略，具体要看执行的任务重要程度。如果是一些不重要任务，可以选择直接丢弃。但是如果为重要任务，可以采用降级处理，例如将任务信息插入数据库或者消息队列，启用一个专门用作补偿的线程池去进行补偿。所谓降级就是在服务无法正常提供功能的情况下，采取的补救措施。具体采用何种降级手段，这也是要看具体场景。技术的世界里没有一尘不变的方案。另外，看到很多同学都提到让老师多讲讲源码，其实我觉得真没必要，老师目前的思路起到提纲契领的作用，让我们有大的思路，有全局观，具体细节我觉得大家私下去研究更合适。小弟不才，可以加微信（SevenBlue）一起讨论。</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/89/b0/988921fe.jpg" width="30px"><span>随风🐿</span> 👍（95） 💬（8）<div>老师，有个问题一直不是很明确，①一个项目中如果多个业务需要用到线程池，是定义一个公共的线程池比较好，还是按照业务定义各自不同的线程池？②如果定义一个公共的线程池那里面的线程数的理论值应该是按照老师前面章节讲的去计算吗？还是按照如果有多少个业务就分别去计算他们各自创建线程池线程数的加和?③如果不同的业务各自定义不同的线程池，那线程数的理论值也是按照前面的去计算吗？</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/87/57236a2d.jpg" width="30px"><span>木卫六</span> 👍（44） 💬（2）<div>guava的ThreadFactoryBuilder.setNameFormat可以指定一个前缀，使用%d表示序号；
或者自己实现ThreadFactory并制定给线程池，在实现的ThreadFactory中设定计数和调用Thread.setName</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/ec/dc03f5ad.jpg" width="30px"><span>张天屹</span> 👍（34） 💬（5）<div>老师你好，使用有界队列虽然避免了OOM  但是如果请求量太大，我又不想丢弃和异常的情况下一般怎么实践呢。我对降级这一块没经验，我能直观想到的就是存放在缓存，如果缓存内存也不够了就只能持久化了</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（27） 💬（2）<div>public class ReNameThreadFactory implements ThreadFactory {
    &#47;**
     * 线程池编号（static修饰）(容器里面所有线程池的数量)
     *&#47;
    private static final AtomicInteger POOLNUMBER = new AtomicInteger(1);

    &#47;**
     * 线程编号(当前线程池线程的数量)
     *&#47;
    private final AtomicInteger threadNumber = new AtomicInteger(1);

    &#47;**
     * 线程组
     *&#47;
    private final ThreadGroup group;

    &#47;**
     * 业务名称前缀
     *&#47;
    private final String namePrefix;


    &#47;**
     * 重写线程名称（获取线程池编号，线程编号，线程组）
     *
     * @param prefix 你需要指定的业务名称
     *&#47;
    public ReNameThreadFactory(@NonNull String prefix) {
        SecurityManager s = System.getSecurityManager();
        group = (s != null) ? s.getThreadGroup() :
                Thread.currentThread().getThreadGroup();
        &#47;&#47;组装线程前缀
        namePrefix = prefix + &quot;-poolNumber:&quot; + POOLNUMBER.getAndIncrement() + &quot;-threadNumber:&quot;;
    }


    @Override
    public Thread newThread(Runnable r) {
        Thread t = new Thread(group, r,
                &#47;&#47;方便dump的时候排查（重写线程名称）
                namePrefix + threadNumber.getAndIncrement(),
                0);
        if (t.isDaemon()) {
            t.setDaemon(false);
        }
        if (t.getPriority() != Thread.NORM_PRIORITY) {
            t.setPriority(Thread.NORM_PRIORITY);
        }
        return t;
    }
}</div>2019-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/80/382e46b6.jpg" width="30px"><span>Red Cape</span> 👍（25） 💬（6）<div>请问老师，有界队列的长度怎么确定呢</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/93/098e5ef5.jpg" width="30px"><span>海鸿</span> 👍（21） 💬（1）<div>1.利用guava的ThreadFactoryBuilder
2.自己实现ThreadFactory</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/84/47/1b8b376e.jpg" width="30px"><span>Uncle Drew</span> 👍（20） 💬（4）<div>老师请教一下，如果线上系统宕机了，线程池中的阻塞队列怎么处理才能保证任务不丢失</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（15） 💬（1）<div>老师，有一个问题想问一下:

如果corePoolSize为10，maxinumPoolSize为20，而此时线程池中有15个线程在运行，过了一段时间后，其中有3个线程处于等待状态的时间超过keepAliveTime指定的时间，则结束这3个线程，此时线程池中则还有12个线程正在运行；若有六个线程处于等待状态的时间超过keepAliveTime指定的时间，则只会结束5个线程，此时线程池中则还有10个线程，即核心线程数。

是这样吗？</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/f8/c1a939e7.jpg" width="30px"><span>君哥聊技术</span> 👍（14） 💬（1）<div>我们项目中用了guava的new ThreadFactoryBuilder().setNameFormat()

老师，请教个问题，在工程中，线程池的定义一般是在全局还是局部呢？如果全局的话，是不用shutdown吗？不关闭线程池有没有问题呢？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/8e/cf0b4575.jpg" width="30px"><span>郑晨Cc</span> 👍（9） 💬（2）<div>可参照SDK中的 DefaultThreadFactory 自定义DYIThreadFactory
static class DIYThreadFactory implements ThreadFactory {
        private static final AtomicInteger poolNumber = new AtomicInteger(1);
        private final ThreadGroup group;
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        private final String namePrefix;

        DIYThreadFactory(String diyName) {
            SecurityManager s = System.getSecurityManager();
            group = (s != null) ? s.getThreadGroup() :
                                  Thread.currentThread().getThreadGroup();
            namePrefix = diyName +
                         &quot;-thread-&quot;;
        }

        public Thread newThread(Runnable r) {
            Thread t = new Thread(group, r,
                                  namePrefix + threadNumber.getAndIncrement(),
                                  0);
            if (t.isDaemon())
                t.setDaemon(false);
            if (t.getPriority() != Thread.NORM_PRIORITY)
                t.setPriority(Thread.NORM_PRIORITY);
            return t;
        }
    }
	
	ExecutorService executor = Executors.newFixedThreadPool(4,new DIYThreadFactory(&quot;xxx&quot;));</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/0b/fd18c8ab.jpg" width="30px"><span>大胖子呀、</span> 👍（7） 💬（2）<div>请教一下大家，线程池执行数据更新任务，还能简单的使用事务注解来回滚事务吗？</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/3a/86196508.jpg" width="30px"><span>linqw</span> 👍（7） 💬（1）<div>最近打算分析下Executor系列源码，先分析了下FutureTask源码，https:&#47;&#47;juejin.im&#47;post&#47;5d08be8ce51d455d6c0ad925，老师有空帮忙看下哦</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（4） 💬（1）<div>老师您好，请问有什么推荐的替代 Executors 的方案吗？</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/53/ade0afb0.jpg" width="30px"><span>ub8</span> 👍（3） 💬（2）<div>老师您好，在我们使用线程池时候，如果队列中还有任务未执行，此时重启了服务，那队列中的任务是否会丢。像这样的场景线程池配置的策略应该是什么样的呢</div>2021-08-30</li><br/><li><img src="" width="30px"><span>崛起的小强</span> 👍（3） 💬（1）<div>老师有个问题请教下您。我们一个项目包含若干个业务模块，其中好几个模块都会用到线程池，那使用的时候只创建一个线程池好还是根据项目模块创建多个不同的线程池呢？各个模块的任务也都是各不相同的，有cpu密集型的，有io密集型的，还有rpc调用耗时较长的任务。</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/15/01/927d96e5.jpg" width="30px"><span>随风而逝</span> 👍（3） 💬（1）<div>老师，这里的线程池，和Disruptor是一样的吗？</div>2019-05-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ4vhMGnAfWK7EaNx6lgDAfqLxafxKQoXOgNVfhNxpNMkCL5WQdRlWHicjIqfvY2tvs3gZpicp4lTeQ/132" width="30px"><span>程文</span> 👍（1） 💬（2）<div>老师，线程池创建之后是否有必要关闭</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/c2/bad34a50.jpg" width="30px"><span>张洋</span> 👍（1） 💬（2）<div>老师，我如果要对线程池进行异常处理比如异步任务异常，发送email这种。需要怎么对线程池进行异常的处理呢，线程池提交任务的时候现在代码中都是 submit()进行提交的。
</div>2019-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（1） 💬（1）<div>请问老师linkedBlockQueue默认是无界的，那如果构造函数带上初始容量是不是变成有界的</div>2019-04-19</li><br/><li><img src="" width="30px"><span>Geek_ebabb4</span> 👍（0） 💬（1）<div>我在某个黄色大马褂的IT大厂，公司基础平台部封装了一个线程池管理中心，可以实现在线实时配置线程池的参数，代码只有一行api就可以获取线程池，方便是方便，但也要努力学习原理啊</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/dd/c6035349.jpg" width="30px"><span>Bumblebee</span> 👍（0） 💬（1）<div>老师我想问个问题，同一个服务下面，不同业务进行线程池隔离这样做，能提升性能吗？我认为不能（因为机器的cpu数量是固定的，假设有一台4核的机器，那么最多同时运行4个线程）这样理解的话不论线程池怎么隔离同时最多也就4个线程同时运行。</div>2022-03-05</li><br/><li><img src="" width="30px"><span>Akane</span> 👍（0） 💬（1）<div>老师，请教一下，简化线程池代码中
&#47;&#47;保存内部工作线程 
List threads = new ArrayList&lt;&gt;();
保存内部工作线程有什么作用呀？
后续也只是在构造方法中初始化的时候将线程放到list中，然后就没有对该list做操作了，不太理解</div>2022-02-17</li><br/><li><img src="" width="30px"><span>poordickey</span> 👍（0） 💬（1）<div>老师真的太适合讲课了   思路清奇    有种相见恨晚的感觉</div>2020-12-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erPMtAfnQdpx1yOZQ2ic7icqUs3tvibEjUXQMUXKiaakyuIho6k6vmdl46nrdWjXIjPIRg9Pmco00tR5w/132" width="30px"><span>小氘</span> 👍（0） 💬（1）<div>我在项目中遇到了线程任务抛出空指针异常但没有任何提示我以为任务执行正常但实际却终止了的情况，看完这篇下周上班按规范都catch上运行时异常。</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（0） 💬（4）<div>老师好
Springboot中
使用ThreadPoolExecutor创建线程池
 corePoolSize＝4
 maximumPoolSize＝8
发布到4核服务器上
Jmeter压测，看日志线程最多是4个
不管修改corePoolSize，maximumPoolSize为多少，线程数最多等于corePoolSize，这会是什么原因呢？</div>2019-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJwQvLGE4dMsF4JU0svW3DtGbodpjskbY65FdwF13JdtBYZfgL2IXHlHrdejWzHdjT0RibEIfib4QYA/132" width="30px"><span>知行合一</span> 👍（0） 💬（1）<div>请问老师，自定义线程池，最大线程数设置多少合适呢</div>2019-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，如果队列中任务很少，请问while（true）一句是不是有问题了</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/65/3da02c30.jpg" width="30px"><span>once</span> 👍（0） 💬（1）<div>老师你好,这里感觉还是没有说清楚为什么线程池不采用一般的池化资源的方法? </div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6d/df/dd536ff5.jpg" width="30px"><span>魏斌斌</span> 👍（0） 💬（1）<div>老师，线程池里面用到了阻塞队列，当队列满的时候提交任务，不是会挂起生产者线程吗？</div>2019-06-13</li><br/>
</ul>