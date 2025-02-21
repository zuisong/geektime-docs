你好，我是朱涛。这节课我们来学习Kotlin协程的异常处理。

其实到这里，我们就已经学完所有Kotlin协程的语法知识了。但在真正把Kotlin协程应用到生产环境之前，我们还需要掌握一个重要知识点，那就是异常处理。

比起Kotlin协程的语法知识点，协程的异常处理，其实更难掌握。在前面的课程中，我们已经了解到：**协程就是互相协作的程序，协程是结构化的**。正因为Kotlin协程有这两个特点，这就导致它的异常处理机制与我们普通的程序完全不一样。

换句话说：**如果把Java里的那一套异常处理机制，照搬到Kotlin协程里来，你一定会四处碰壁**。因为在普通的程序当中，你使用try-catch就能解决大部分的异常处理问题，但是在协程当中，根据不同的协程特性，它的异常处理策略是随之变化的。

我自己在工作中就踩过很多这方面的坑，遇到过各种匪夷所思的问题：协程无法取消、try-catch不起作用导致线上崩溃率突然大增、软件功能错乱却追踪不到任何异常信息，等等。说实话，Kotlin协程的普及率之所以不高，很大一部分原因也是因为它的异常处理机制太复杂了，稍有不慎就可能会掉坑里去。

那么今天这节课，我们就会来分析几个常见的协程代码模式，通过解决这些异常，我们可以总结出协程异常处理的6大准则。掌握了这些准则之后，你在以后遇到异常问题时，就能有所准备，也知道该怎么处理了。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（24） 💬（1）<div>（1）Cancel依赖Cancel异常。
（2）SupervisorJob重写了childCancelled=false，导致取消不会向上和兄弟传播。
（3）异常的传播应该是先向上传播，然后都没人处理才会触发协程的CoroutineExceptionHandler，在触发全局默认的CoroutineExceptionHandler。
（4）ExceptionHandler代替try catch不合理，无法清晰的对业务异常有一个认知，不知道是哪里来的，只能通用处理；同时我认为ExceptionHandler或者作为兜底策略也是合理的，子协程对自己的业务进行异常处理，同时顶层协程有一个兜底策略，上报后需要及时让子协程进行处理；这个问题就像Java线程要不要加UnCauthedExceptionHandler【协程也可以加默认的】。</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（15） 💬（2）<div>老师，我实验了 CoroutineExceptionHandler ，貌似可以用在局部，还是我哪里搞错了，关键点 + 了一个 Job() 就可以了；
环境：JDK: 11 , Kotlin: 1.6.10,  Kotlin coroutine-core: 1.6.0
代码如下：
  launch {
                delay(100L)

                launch(exceptionHandler + Job() ) { &#47;&#47;
                    delay(100L)
                    1 &#47; 0       &#47;&#47; Cause Exp
                }
            }</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（7） 💬（1）<div>由于 Coroutine 是结构化的，当一个子 job 出现异常会导致其他协程都停止运行，在一些场景下并不是我们想要的。我们需要使用 try catch 来将异常捕获在发生异常的地方。

如果使用 supervisorJob 来阻止异常传递的话，CoroutineExceptionHandler 又无法接收到异常，导致我们无法知道哪一个 Job由于什么原因被中止了。这时使用 try catch 可以捕获到对应的异常信息。

言而总之，try catch 在处理协程异常时，还是很有必要的。</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（5） 💬（1）<div>思考题：
全部用ExceptionHandler 替代try catch是不合理的，因为在实际编码过程中，我们有时需要在当前上下文合适地处理异常，比如兜底操作，重试等，并不是一味的把异常抛出去，如果都交给顶层就无法很好地处理这些case。类似于Java的UnCauthedExceptionHandler 。</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/d3/e25d104a.jpg" width="30px"><span>êｗěｎ</span> 👍（3） 💬（1）<div>思考题: 个人理解，看场景。有些业务是可以把异常当作分支处理，这种情况，handler就不适合了。</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/7b/c0b0c86d.jpg" width="30px"><span>dashingqi</span> 👍（0） 💬（1）<div>请问，文章中的动画是怎么做的啊？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/b0/4e22819f.jpg" width="30px"><span>syz</span> 👍（0） 💬（1）<div>准则二例子
val job1 = Job()
val pJob: Job = launch(myFixedThread) {
            launch(job1) {&#47;&#47;coroutine#3}
            launch{&#47;&#47;CoroutineId(4)}
}
照搬的例子，测试时发现job1下的协程也停止了打印
检查发现
&quot;coroutine#3&quot;:StandaloneCoroutine{Active}@543fc144,
&quot;coroutine#4&quot;:StandaloneCoroutine{Cancelling}@32e5773b
问题：打破协程父子结构的子协程coroutine#3（父协程是job1，当前处于Active状态）停止了打印？pJob的cancel没有影响到job1的Active状态，但是coroutine#3不再打印数据

</div>2022-04-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（0） 💬（2）<div>代码段2：
launch(Dispatchers.Default)
这里为什么必须使用Default线程池？</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/f3/5e4b0315.jpg" width="30px"><span>追梦小乐</span> 👍（0） 💬（1）<div>关于异常要写对应的异常，不要用父类的Except ion，在使用快捷键给一点代码加上try-catch后，出来的就是父类的题材，那老师我们在编写代码的时候，怎么判断是属于某一个具体的异常？！</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（0） 💬（2）<div>以下代码，&quot;End&quot; 都打印了，子 Job 也停止了，为啥程序不能停止？

fun main() = runBlocking {
    val dispatcher = Executors.newFixedThreadPool(2) { Thread(it, &quot;bqt&quot;) }.asCoroutineDispatcher()
    val pJob = launch(dispatcher) {
        launch {
            var i = 0
            while (true) {
                delay(500)
                i++
                println(&quot;cJob - $i&quot;)
            }
        }
    }

    delay(2000L)
    pJob.cancel()
    pJob.join()
    println(&quot;End&quot;)
}</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（0） 💬（2）<div>代码段3，为啥使用 Dispatchers.IO&#47;Default 就没问题，使用自定义线程池就有问题？</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（0） 💬（1）<div>有点复杂，感觉需要结合着源码看可能才会明了</div>2022-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/47/b0/8c301d00.jpg" width="30px"><span>H.ZWei</span> 👍（0） 💬（0）<div>    val exceptionHandler = CoroutineExceptionHandler { _, throwable -&gt;
        println(&quot;exception handler: ${throwable.message}&quot;)
    }
    val dispatcher = Executors.newSingleThreadExecutor().asCoroutineDispatcher()
    val scope = CoroutineScope(Job()   + exceptionHandler )
    scope.launch {
        println(&quot;launch run&quot;)
        1&#47; 0
    }

文档说CoroutineExceptionHandler 在顶层协程中才会生效，但我测试了在顶层协程中也不生效，上面代码创建了一个CoroutineScope中不传入dispatcher 启动协程（默认情况下会使用Dispatchers.Default），异常发生后CoroutineExceptionHandler 不会生效，需要把dispatcher 传入才会生效，对CoroutineExceptionHandler 还是不太理解，看官网例子的测试用例都是GlobalScope</div>2023-08-20</li><br/>
</ul>