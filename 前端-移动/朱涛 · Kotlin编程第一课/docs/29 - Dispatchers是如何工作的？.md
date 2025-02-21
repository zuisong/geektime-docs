你好，我是朱涛。今天，我们来分析Kotlin协程当中的Dispatchers。

上节课里，我们分析了launch的源代码，从中我们知道，Kotlin的launch会调用startCoroutineCancellable()，接着又会调用createCoroutineUnintercepted()，最终会调用编译器帮我们生成SuspendLambda实现类当中的create()方法。这样，协程就创建出来了。不过，协程是创建出来了，可它是如何运行的呢？

另外我们也都知道，协程无法脱离线程运行，Kotlin当中所有的协程，最终都是运行在线程之上的。**那么，协程创建出来以后，它又是如何跟线程产生关联的？**这节课，我们将进一步分析launch的启动流程，去发掘上节课我们忽略掉的代码分支。

我相信，经过这节课的学习，你会对协程与线程之间的关系有一个更加透彻的认识。

## Dispatchers

在上节课里我们学习过，launch{}本质上是调用了startCoroutineCancellable()当中的createCoroutineUnintercepted()方法创建了协程。

```plain
// 代码段1

public fun <T> (suspend () -> T).startCoroutineCancellable(completion: Continuation<T>): Unit = runSafely(completion) {
    //                                        注意这里
    //                                           ↓
    createCoroutineUnintercepted(completion).intercepted().resumeCancellableWith(Result.success(Unit))
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（10） 💬（1）<div>Kotlin在开启协程状态机之前做了大量的工作，从父协程那里继承了状态，重新设定了子协程运行线程，检查了各种异常情况，区分了程序异常和协程cancel的情况，最终在指定的线程里启动了状态机。协程的重点不在线程，而在线程之外的调度，异常处理和状态机。
</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（4） 💬（1）<div>协程本质上是对线程的封装，我们在使用协程的时候，并不需要直接与线程打交道，直接使用 Coroutine 提供的相关 API 以同步的方式就可以间接完成与线程之间的交互。</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（4） 💬（1）<div>kotlin的协程与java线程密不可分，协程最终是运行在线程中的Task。</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（1）<div>如果挂起后，再恢复，是如何恢复到之前的线程的呢？？

这个线程的是如何保存的呢？？</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>这里，请你留意代码中我标记出的注释，intercepted() 方法首先会判断它的成员变量 intercepted 是否为空，如果不为空，就会调用 context[ContinuationInterceptor]，获取上下文当中的 Dispatcher 对象。以代码段 3 当中的逻辑为例，这时候的 Dispatcher 肯定是 Default 线程池。

涛哥，这里应该是 intercepted 为空才会调用 context[ContinuationInterceptor] 吧？</div>2022-03-30</li><br/>
</ul>