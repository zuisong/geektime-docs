你好，我是朱涛。

在前面的课程里，我们一直在研究如何使用Kotlin协程，比如，如何启动协程，如何使用挂起函数，如何使用Channel、Flow等API。但到目前为止，我们只知道该怎么用协程，对它内部的运行机制并没有深究。

现在我们都知道，launch、async可以创建、启动新的协程，但我们只能通过调试参数，通过log看到协程。比如我们可以回过头来看下[第13讲](https://time.geekbang.org/column/article/485632)当中的代码：

```plain
// 代码段1

// 代码中一共启动了两个协程
fun main() = runBlocking {
    println(Thread.currentThread().name)

    launch {
        println(Thread.currentThread().name)
        delay(100L)
    }

    Thread.sleep(1000L)
}

/*
输出结果：
main @coroutine#1
main @coroutine#2
*/
```

现在回过头来看，这段代码无疑是非常简单的，runBlocking{} 启动了第一个协程，launch{} 启动了第二个协程。可是，有一个问题，我们一直都没有找到答案：**协程到底是如何创建的？它对应的源代码，到底在哪个类？具体在哪一行？**

我们常说Java线程的源代码是Thread.java，这样说虽然不一定准确，但我们起码能看到几个暴露出来的方法。那么，在Kotlin协程当中，有没有类似Coroutine.kt的类呢？对于这些问题，我们唯有去阅读Kotlin协程的源码、去分析launch的启动流程，才能找到答案。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="" width="30px"><span>辉哥</span> 👍（5） 💬（1）<div>startCoroutine -&gt; createCoroutineUnintercepted -&gt; createCoroutineFromSuspendFunction,最终返回一个RestrictedContinuationImpl对象,然后调用其resume方法,从而调用block的invoke方法.最终调起协程.</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4a/5a/14eb7973.jpg" width="30px"><span>杨小妞</span> 👍（1） 💬（1）<div>createCoroutineUnintercepted这个函数的JVM实现在哪个包，哪个类下呢？</div>2022-04-06</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（1） 💬（1）<div>思考题：调试了一下，结果是一样的。唯一的区别可能在于block原来被反编译成一个函数对象直接用实现状态机的Continuation对象赋值。加入函数赋值以后，block对象被实现为一个简单的内部类，这个内部类的invoke函数再去调用Continuation对象。</div>2022-03-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqQVYE1EfqibdyNsnjFibHW4jee0Q3qMMeRhqqVQUn5Ix9fFl3Zfzf0xpdrGypxHUmBCyiczfyEaPoWA/132" width="30px"><span>ACE_Killer09</span> 👍（0） 💬（1）<div>代码段16中，
我理解resume 之后 会回到 LaunchUnderTheHoodKt$testLaunch$1 # invoke ，再进一步到invokeSuspend 进入状态机的流程。那么 Continuation#resume -&gt; invoke这个过程是怎么调用过来的？</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ef/c0/537b3905.jpg" width="30px"><span>L先生</span> 👍（0） 💬（1）<div>反编译了一下，block最终会转成function1。(this as Function1, Any?&gt;).invoke(it)中的invoke是指的这个Function1中的invoke吗</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ef/c0/537b3905.jpg" width="30px"><span>L先生</span> 👍（0） 💬（2）<div>打印没啥区别啊。应该是走这里了。createCoroutineFromSuspendFunction(probeCompletion) { (this as Function1, Any?&gt;).invoke(it) }。但是我看不太懂。this指什么，it又指什么参数</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>关于思考题的思考：

我认为执行流程及结果和代码段 3 中是完全一样的。因为 
private suspend fun func(): String { 
    println(&quot;Hello!&quot;) 
    delay(1000L) 
    println(&quot;World!&quot;) 
    return &quot;Result&quot;
} 和

val block = suspend {
    println(&quot;Hello!&quot;)
    delay(1000L)
    println(&quot;World!&quot;)
    &quot;Result&quot;
}

完全是等价的写法。
</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（1） 💬（0）<div>深层认识：
suspend function type 底层被实现为Continuation。所以协程启动就是Continuation的resume。协程的启动实际上是Continuation的一个应用。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（2）<div>start(block, receiver, this)是三个参数，是怎么跳转到只有两个参数的
public operator fun invoke(block: suspend () -&gt; T, completion: Continuation): Unit
的？</div>2024-04-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eyKgpIVFSDQBia7SJRVUKFh5qgwc3ohzEPSKvchLf9ZvwIO9CrS470ER7OhNzWTs0svECHCBiarQTa41BO3Hf0DA/132" width="30px"><span>Temme</span> 👍（0） 💬（1）<div>”注释 2 处的 (this is BaseContinuationImpl) 条件一定是为 true 的“
这句话好像是错的SuspendLambda并不是BaseContinuationImpl的子类</div>2024-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>完了，现在编译后没有block这个类</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>为什么调用resume(Unit)就是启动协程？怎么启动的？
这个方法不是直接返回异步执行结果的吗？</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>前排提醒，本课程的一个重要基础：学会invoke操作符和Function系列接口</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（1）<div>在看的过程中我的想法一直在变。我在想，coroutine到底是什么？
是coroutinecontext？是cotinuation？是job？是挂起函数？</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/23/65/39d789a8.jpg" width="30px"><span>zs</span> 👍（0） 💬（0）<div>BaseContinuationImpl 里面的resumeWith()方法里面会判断 completion 是不是 BaseContinuationImpl，在挂起函数恢复的实话都是调用的suspendLambda的 resumeWith方法，所以才会调用suspendLambda 的invokeSuspend方法，那什么时候调用AbstractCoroutine()的resumeWith方法恢复整个协程呢</div>2022-09-19</li><br/>
</ul>