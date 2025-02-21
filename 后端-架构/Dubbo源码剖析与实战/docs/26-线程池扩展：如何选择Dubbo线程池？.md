你好，我是何辉。今天我们继续学习Dubbo拓展的第四篇，线程池扩展。

提到线程池，我们在前面“[异步化实践](https://time.geekbang.org/column/article/611392)”中通过“线程池耗尽”这个现象已经接触到了，Dubbo 采用默认的线程池，也就是 200 个核心线程，来提供服务，其实我们已经用得非常舒服了，业务正常运转没什么阻碍。

不过你知道吗，Dubbo 框架里面其实有 4 种线程池，那其他的线程池存在的意义是什么，我们在使用时该怎么选择呢？

带着这个问题，今天我们来点轻松的，带你掌握 Dubbo 4 种线程池的用法。

## 线程池原理

在具体分析每一种线程池之前，我们还是回忆一下创建线程池的核心代码参数，看一看添加任务到线程池的大致工作原理是什么样的。

```java
///////////////////////////////////////////////////
// java.util.concurrent.ThreadPoolExecutor#ThreadPoolExecutor(int, int, long, java.util.concurrent.TimeUnit, java.util.concurrent.BlockingQueue<java.lang.Runnable>, java.util.concurrent.ThreadFactory, java.util.concurrent.RejectedExecutionHandler)
// 线程池最核心的构造方法
///////////////////////////////////////////////////
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler) {
    // 核心线程数量小于 0，则抛出参数非法异常
    if (corePoolSize < 0 ||
        // 最大线程数量小于等于 0，则抛出参数非法异常
        maximumPoolSize <= 0 ||
        // 最大线程数量小于核心线程数量，则抛出参数非法异常
        maximumPoolSize < corePoolSize ||
        // 非核心线程空闲时的存活时间小于0，则抛出参数非法异常
        keepAliveTime < 0)
        throw new IllegalArgumentException();
    // 没有配置任务队列、没有配置创建线程的工厂、没有配置拒绝策略，一律抛出参数非法异常
    if (workQueue == null || threadFactory == null || handler == null)
        throw new NullPointerException();
    // 剩下的就是一些入参的赋值逻辑了
    this.corePoolSize = corePoolSize;
    this.maximumPoolSize = maximumPoolSize;
    this.workQueue = workQueue;
    this.keepAliveTime = unit.toNanos(keepAliveTime);
    this.threadFactory = threadFactory;
    this.handler = handler;
}
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_b2ac95</span> 👍（0） 💬（1）<div>您好，可以正常留言吗</div>2024-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/b0/17/f3dcd8d1.jpg" width="30px"><span>准时不早退的嘉然</span> 👍（0） 💬（1）<div>老师您好，如果想做线程池隔离要怎么实现呢？现在有个需求，要为不同服务接口分配不同的线程数量</div>2023-03-11</li><br/><li><img src="" width="30px"><span>Geek_b2ac95</span> 👍（0） 💬（0）<div>您好，我执行工程中的案例，使用自定义线程池，发现provider可以正常启动，并且自定义线程池生效了，zk上的服务注册信息也有自定义线程池信息，但是consumer无法正常消费，debug进去发现找不到可用的invoker，应该是过滤掉了，这个怎么解决？</div>2024-12-31</li><br/>
</ul>