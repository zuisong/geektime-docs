你好，我是朱涛。今天我们来学习Kotlin协程的Context。

协程的Context，在Kotlin当中有一个具体的名字，叫做CoroutineContext。它是我们理解Kotlin协程非常关键的一环。

从概念上讲，CoroutineContext很容易理解，它只是个[上下文](https://zh.wikipedia.org/zh-hans/%E4%B8%8A%E4%B8%8B%E6%96%87_%28%E8%AE%A1%E7%AE%97%E6%9C%BA%29)而已，实际开发中它最常见的用处就是切换线程池。不过，CoroutineContext背后的代码设计其实比较复杂，如果不能深入理解它的设计思想，那我们在后面阅读协程源码，并进一步建立复杂并发结构的时候，都将会困难重重。

所以这节课，我将会从应用的角度出发，带你了解CoroutineContext的使用场景，并会对照源码带你理解它的设计思路。另外，知识点之间的串联也是很重要的，所以我还会带你分析它跟我们前面学的Job、Deferred、launch、async有什么联系，让你能真正理解和掌握协程的上下文，并建立一个**基于CoroutineContext的协程知识体系**。

## Context的应用

前面说过，CoroutineContext就是协程的上下文。你在前面的第14~16讲里其实就已经见过它了。在[第14讲](https://time.geekbang.org/column/article/486305)我介绍launch源码的时候，CoroutineContext其实就是函数的第一个参数：
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（16） 💬（1）<div>suspend方法需要在协程中执行，协程又一定有上下文，所以可以访问的到哈~ 也就是在suspend方法中可以访问当前协程上下文，并且拿到一些有用的信息</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/ea/373d8e6b.jpg" width="30px"><span>夜班同志</span> 👍（11） 💬（1）<div>挂起函数的Continuation就有CoroutineContext</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/93/b4791ee3.jpg" width="30px"><span>白泽丶</span> 👍（6） 💬（4）<div>如果为协程作用域创建时传入多个CoroutineContext，比如 Job() + Dispatcher.IO + Dispatcher.Main ，那么携程最终会在哪个线程池中执行呢</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（5） 💬（3）<div>1、思考题中的方法为什么要加 suspend，加不加有什么区别吗？
2、为什么代码打印的都是 EmptyCoroutineContext，且没有 name？


import kotlinx.coroutines.*
import kotlinx.coroutines.GlobalScope.coroutineContext

fun main() = runBlocking {
    printInfo(1) &#47;&#47; 1 - EmptyCoroutineContext - null
    CoroutineScope(Dispatchers.IO + Job() + CoroutineName(&quot;bqt&quot;)).launch {
        printInfo(2) &#47;&#47; 2 - EmptyCoroutineContext - null
    }
    delay(100L)
}

suspend fun printInfo(text: Any) = println(&quot;$text - $coroutineContext - ${coroutineContext[CoroutineName]?.name}&quot;)</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（4） 💬（2）<div>如果你理解了第 14 讲的内容，那你一定能分析出它们的运行顺序应该是：1、4、2、3。

也有可能是1、2、4、3吧？  这个得看CPU的调度了，也有可能子协程的2线运行吧？</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（3） 💬（1）<div>思考题代码可以运行。coroutineContext方法是返回当前的CoroutineContext，因为runBlocking是CorouScope，CorouScope具有成员CoroutineContext，所以coroutineContext方法可以返回runBlocking的CoroutineContext。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/3c/d72b0d26.jpg" width="30px"><span>面无表情的生鱼片</span> 👍（3） 💬（2）<div>请教老师，经常看到 Job() + Dispatcher ，这么做是什么原因呢</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/d2/204edd23.jpg" width="30px"><span>WWWarmFly</span> 👍（2） 💬（1）<div>请教老师，
Dispatcher 内部成员的类型是CoroutineContext，这里怎么推出

Dispatcher 确实就是 CoroutineContext</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/27/a3737d61.jpg" width="30px"><span>Shanks-王冲</span> 👍（1） 💬（1）<div>Kotlin1.6源码package kotlin.coroutines中找到了这个，public suspend inline val coroutineContext: CoroutineContext，成员定义成suspend了，我不知道该怎么解释，贴出试试</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/a6/679b3c6b.jpg" width="30px"><span>Renext</span> 👍（0） 💬（1）<div>代码段6报错：  Cannot access &#39;ExecutorCoroutineDispatcherImpl&#39;: it is private in file</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（5）<div>代码是可以运行的，coroutineContext 的作用是获取当前运行作用域所对应协程的上下文信息。

这里打印出来的信息就是 runBlocking 所运行的协程所对应上下文的信息。

[CoroutineId(1), &quot;coroutine#1&quot;:BlockingCoroutine{Active}@759ebb3d, BlockingEventLoop@484b61fc]</div>2022-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIJ9Kyict83d8Y95iavUqHsiaJVKbHdcTEKdsubAYvBr6FkzNicS3hGd2MRclrG2XZ0KGcgtHsCPluaNA/132" width="30px"><span>Geek_48edaa</span> 👍（1） 💬（0）<div>&#47;&#47; 代码段7

fun main() = runBlocking {
    logX(&quot;Before launch.&quot;) &#47;&#47; 1
    launch {
        logX(&quot;In launch.&quot;) &#47;&#47; 2
        delay(1000L)
        logX(&quot;End launch.&quot;) &#47;&#47; 3
    }
    logX(&quot;After launch&quot;)   &#47;&#47; 4
}
“如果你理解了第 14 讲的内容，那你一定能分析出它们的运行顺序应该是：1、4、2、3。”
这段代码的执行顺序是不可控的，可能是1243、也可能是1423.因为2 4 分别运行在不同线程
</div>2023-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/0c/c623649c.jpg" width="30px"><span>稚者</span> 👍（1） 💬（0）<div>ExceptionHandler这段代码要把人折磨疯，我看过的一堆博客说的是，异常会被传递到顶层Context的exceptionHandler处理，
我的理解是：
scope = CoroutineScope(Job() + Dispatcher + ExceptionHandler)
scope.launch {}
这样才算顶层； 
而：scope = CoroutineScope(Job() + Dispatcher)
scope.launch(exceptionHandler) {} 中的 exHandler 是属于子协程的，不是顶层Context，所以不可能被捕获到。 </div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>以下为AI给出的withContext函数的简化实现：
public suspend fun &lt;T&gt; withContext(
    context: CoroutineContext,
    block: suspend CoroutineScope.() -&gt; T
): T {
    &#47;&#47; 暂停当前协程，切换到指定的上下文中执行挂起函数
    return suspendCoroutineUninterceptedOrReturn { cont -&gt;
        val oldContext = cont.context
        &#47;&#47; 创建新的 CoroutineContext，合并指定的 context 和当前的上下文
        val newContext = oldContext + context
        &#47;&#47; 创建一个新的协程
        val newContinuation = CoroutineCotinuation(cont)
        &#47;&#47; 切换到新的上下文中执行挂起函数
        block.startCoroutineCancellable(newContinuation)
        COROUTINE_SUSPENDED
    }
}
</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>老实说，我觉得不是Dispatchers.Unconfined 的错。谁规定子协程里的代码就一定要比父协程发起子协程之后的代码晚一点执行？编码不该指望这种未定义的巧合来保证代码执行顺序。真要对执行顺序有严格要求，就应该在编码时通过手段体现出来。如果对异步顺序没有要求，也就不必去在乎。</div>2023-12-09</li><br/><li><img src="" width="30px"><span>Geek_416c20</span> 👍（0） 💬（0）<div>fun main() = runBlocking(mySingleDispatcher) {

    val myExceptionHandler = CoroutineExceptionHandler{_,throwable -&gt;
        println(&quot;catch exception: $throwable&quot;)
        }
   val scope = CoroutineScope(Job()+ mySingleDispatcher)
    val job = scope.launch(myExceptionHandler) {
        logX(&quot;Second&quot;)
        val s:String? = null
        s!!.length
    }
&#47;&#47;    job.join()
&#47;&#47;    val user = getUserInfo()
&#47;&#47;    logX(user)
}
代码段20 ，我将 job.join() 注释掉，代码能够执行，但是不会有Catch exception: java.lang.NullPointerException的输出结果。runBlocking 不是会等所以子协程运行结束才会结束的吗？照理说，没有 job.join()  也能输出异常的结果，但是没有欸。</div>2023-01-15</li><br/><li><img src="" width="30px"><span>Geek_fd59dd</span> 👍（0） 💬（0）<div>老师请教一下，本文中代码段2，打印结果依次是：Before IO Context-&gt; In IO Context. -&gt; After IO Context.   不应该是 Before IO Context-&gt; After IO Context. -&gt; In IO Context 吗</div>2022-10-10</li><br/>
</ul>