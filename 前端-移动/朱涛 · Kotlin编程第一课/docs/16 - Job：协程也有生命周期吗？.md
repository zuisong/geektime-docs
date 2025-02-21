你好，我是朱涛。今天我们来学习Kotlin协程的Job。

Job其实就是协程的句柄。从某种程度上讲，当我们用launch和async创建一个协程以后，同时也会创建一个对应的Job对象。另外，Job也是我们理解**协程生命周期**、**结构化并发**的关键知识点。通过Job暴露的API，我们还可以让不同的协程之间互相配合，从而实现更加复杂的功能。

虽然前面已经解释过，Job就是协程的句柄，但你可能还是不清楚它到底是什么，因为句柄本身就是一个比较“虚”的概念。所以在这节课中，我们会从使用的角度入手，来看看Job到底能干什么。在充分理解了Job的用法以后，我们再来结合它的源代码进一步分析，这样对Job也会有一个更加清晰的认知。

## Job生命周期

在上节课我们学习launch、async的时候，我们知道它们两个返回值类型分别是Job和Deferred。

```plain
// 代码段1

public interface Deferred<out T> : Job {
    public suspend fun await(): T
}
```

而如果你去看Deferred的源代码，你会发现，它其实也是继承自Job的。对应的，它只是多了一个泛型参数T，还多了一个返回类型为T的await()方法。所以，不管是launch还是async，**它们本质上都会返回一个Job对象**。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/3c/d72b0d26.jpg" width="30px"><span>面无表情的生鱼片</span> 👍（37） 💬（3）<div>思考题：
代码的执行结果是：
&gt; First coroutine start!
&gt; First coroutine end!
&gt; Process end!
可见 job2 的代码块并没有被执行。

分析原因：
分别打印出 job2 在 job2.join() 前后的状态：

job2 before join: isActive === false
job2 before join: isCancelled === true
job2 before join: isCompleted === false
&#47;&#47; job2.join()
job2 after join: isActive === false
job2 after join: isCancelled === true
job2 after join: isCompleted === true

可见 job2 创建后并没有被激活。

val job2 = launch(job) {} 这一行代码指示 job2 将运行在 job 的 CoroutineContext 之下, 而之前的代码 job.join() 时 job 已经执行完毕了，根据协程结构化的特性，job2 在创建后不会被激活，并且标记为Cancelled，然后执行 job2 时，发现 job2 未被激活，并且已经被取消，则不会执行 job2 的代码块，但是会将 job2 标记为 Completed</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/4c/05/4fe55808.jpg" width="30px"><span>没名儿</span> 👍（12） 💬（1）<div>看了大家的留言有个疑点
----很多异步任务之间都是没有互相依赖的，这样的代码结合挂起函数后，再通过 async 并发来执行，是可以大大提升代码运行效率的。----
----如你所说，存在依赖关系的时候，我们就可以挂起函数与async结合了。-----
到底是存在依赖关系用async还是不存在依赖关系用async呢？

</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（7） 💬（1）<div>思考题针对性不强。
因为思考题考察的知识点是 CoroutineContext 上下文，而这一部分是下一节课的内容。</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（6） 💬（1）<div>思考题结果：
First coroutine start!
First coroutine end!
Process end!
没有执行job2的原因是，它的launch中传入了job 作为coroutinecontext，而它已经是complete 状态了，所以不会再执行job2的block 而是直接执行了job2的join ，然后结束。</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/48/c5/3ecc101f.jpg" width="30px"><span>原仲</span> 👍（2） 💬（3）<div>代码片段14 中的执行流程
val result1 = async { getResult1() } 
val result2 = async { getResult2() } 
val result3 = async { getResult3() }
&#47;&#47;调用时机在这
results = listOf(result1.await(), result2.await(), result3.await())
用作者的思维模型，相当于三个钓鱼杆同时拉杆

val result1 = async { getResult1() } 
&#47;&#47;调用时机
result1.await()
val result2 = async { getResult2() } 
&#47;&#47;调用时机
result2.await()
val result3 = async { getResult3() }
&#47;&#47;调用时机
result3.await()
用作者的思维模型，相当于三个钓鱼杆依次拉杆
</div>2022-05-14</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（2） 💬（3）<div>代码段10中【delay(500L)】这一句影响了什么呀？不加的话后边的日志就不打印了</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f0/a0/43168e73.jpg" width="30px"><span>Gavin</span> 👍（2） 💬（1）<div>&quot;First coroutine start!&quot;
&quot;First coroutine end!&quot;
&quot;Process end!&quot;
通过源码可知launch中传入的CoroutineContext会作为parentJob，而job2的parentJob为job，job协程已经处于completed状态，故不执行job2直接跳过</div>2022-02-23</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（1） 💬（1）<div>这里 await() 后面的代码，虽然看起来是阻塞了，但它只是执行流程被挂起和恢复的一种表现。而且如果你仔细思考的话，你会发现上面这个动图，同样也描述了之前 job.join() 的行为模式，在协程执行完毕之前，后面的协程代码都被暂时挂起了，等到协程执行完毕，才有机会继续执行。

——”在协程执行完毕之前“这里的协程指的父级协程，“后面的协程代码都被暂时挂起了“这里的协程代码指的子级协程代码部份。也就是说：如果子级自己有挂起操作，那么子级的代码会被暂时挂起，直到父级的协程代码执行完毕之后再继续执行子级协程代码（前提是父级没有挂起延迟之类的操作）。</div>2022-04-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpF5euTNx3GOkmf515HFh1ahAzogerLfIyLia2AspTIR9fkU6icGbo2ungo23cdM5s9dUjZGMno7ZA/132" width="30px"><span>dawn</span> 👍（1） 💬（1）<div>fun main() = runBlocking {
    val job = launch {
        logX(&quot;Coroutine  start!&quot;)
        delay(1000L)
        logX(&quot;Coroutine  end!&quot;)
    }
    job.log()
    delay(500)
    job.cancel()
    job.log()
    delay(1) &#47;&#47;延时1ms
    job.log()
    delay(2000)
    logX(&quot;Process end!&quot;)
}
为什么取消后输出延时1ms输出job的isCompleted会有false变为true</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/fa/44a3e48a.jpg" width="30px"><span>张国庆</span> 👍（1） 💬（1）<div>最后问题应该是按顺序打印</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/38/aad89fe5.jpg" width="30px"><span>Luckykelan</span> 👍（0） 💬（1）<div>老师你好，请问完善后的思维模型这个例子中，是怎么知道println(&quot;Result = $result&quot;)和logX(&quot;Process end!&quot;)这两段代码是和协程在同一个task 中并一同挂起的呢？</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/37/15baf151.jpg" width="30px"><span>neo</span> 👍（0） 💬（1）<div>Finishing[cancelling=true, completing=false, rootCause=kotlinx.coroutines.JobCancellationException: Parent job is Completed; job=&quot;coroutine#2&quot;:StandaloneCoroutine{Completed}@d6da883, exceptions=null, list=List{Active}[]]
上面cancelling的原因是父job已经被完结</div>2022-04-22</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（0） 💬（1）<div>这里的阻塞和之前的挂起不是一回事把</div>2022-04-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（0） 💬（1）<div>思考题，job与job2存在父子协程关系吗？</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>    val job = launch {
        log(&quot;First coroutine start!&quot;)
        delay(1000L)
        log(&quot;First coroutine end!&quot;)
    }

    job.join()
    val job2 = launch(job) {
        log(&quot;Second coroutine start!&quot;)
        delay(1000L)
        log(&quot;Second coroutine end!&quot;)
    }
    log(&quot;job2: isActivate: ${job2.isActive}, isCompleted: ${job2.isCompleted}, isCancel: ${job2.isCancelled}&quot;)
    job2.join()
    log(&quot;Process end!&quot;)

在示例代码中，加了一个打印 job2 的状态，发现 job2 已经被取消了，是因为绑定了 job 后，运行时认为其已经被执行过了，所以直接将其取消了？</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（2）<div>执行的结果为：
First coroutine start!
First coroutine end!
Second coroutine start!
Second coroutine end!
Process end!

结果分析：
1. 第一个 job.join() 被调用后，当前通过 runBlocking 启动的协程会被挂起，等待当前 job 执行完成。
2. 当第一个 job 执行完成后，会恢复 runBlocking 对应的协程继续执行。
3. 当执行到 job2.join() 后，runBlocking 对应的协程又被挂起，并等待 job2 的执行。
4. 同样的道理，当 job2 执行完成后，会恢复 runBlocking 对应协程的继续执行。
5. 最终打印 “Porcess end!” 后，runBlocking 运行的协程，对应的线程以及进程会相即结束。


</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>执行的结果为：
First coroutine start
First coroutine end!</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（0） 💬（1）<div>由浅入深。学习了~</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/5c/a786deb5.jpg" width="30px"><span>提醒圈圈去看书</span> 👍（0） 💬（1）<div>挂起函数，挂起代码的范围是当前协程对咩？比如说在子协程里执行到了挂起函数，则接下来去执行父协程的代码？和线程会有关系吗？</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/5c/a786deb5.jpg" width="30px"><span>提醒圈圈去看书</span> 👍（0） 💬（1）<div>老师，想要请教一下这样的场景：3个异步请求A,B,C。1、B依赖A结果，C依赖B结果，这时是放一个协程里，依次执行三个挂起函数？2.ABC可以同时请求，则一个父协程，分别用async开启三个子协程来执行ABC？3.AB可以同时请求，C依赖AB的结果，则一个父协程，分别用async开启两个子协程执行AB，C为挂起函数放在父协程里面，在await之后再执行对咩。   </div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/2b/95/ef6b7672.jpg" width="30px"><span>来日可期</span> 👍（1） 💬（1）<div>大佬，我有个疑惑，为什么lauch方法可以传入job参数呢，这个函数参数不是这三个吗
public fun CoroutineScope.launch(
    context: CoroutineContext = EmptyCoroutineContext,
    start: CoroutineStart = CoroutineStart.DEFAULT,
    block: suspend CoroutineScope.() -&gt; Unit
): Job {
    ...
}</div>2022-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/66/54/e6845aa6.jpg" width="30px"><span>Jeffery</span> 👍（0） 💬（0）<div>老师，您讲的太好了，看了这么多课程、博客等，第一次在您这儿懂了协程，太感谢您了。如果可以，希望老师能多多出一些课程，比如Compose、Flutter等当今热门的知识体系，我一定鼎力支持！</div>2024-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/a6/05/34357b55.jpg" width="30px"><span>王亚军</span> 👍（0） 💬（0）<div>关于isCancelled = true
isCompleted = false 和 isCompleted = true的问题，老师这里似乎讲的有点问题。

其实job.cancel()操作就是立即取消协程，不会等待协程完成。取消后没有遇到下一个协程挂起点或取消点，那么isCompleted属性将保持为false。所以如果job.cancel()后面直接打印job.log()，那么isCompleted一定是false。如果job.cancel()后面又执行delay(...)，那么相当于是遇到了下一个协程挂起点，所以isCompleted就会变为true；

另外，job.cancelAndJoin()这个方法会取消协程，并且会等待协程完成，跟上面的job.cancel()刚好相反，这里会等待协程完成，即，执行了job.cancelAndJoin()之后立即执行job.log()，则isCompleted=true，不用等到下一个协程挂起点或取消点。

所以isCompleted等于false还是true，跟操作有关。</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/65/ac/adbda26f.jpg" width="30px"><span>武</span> 👍（0） 💬（0）<div>结构化并发可以理解成树吗？父节点的开始和取消都会通知下面的子节点。</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/0c/c623649c.jpg" width="30px"><span>稚者</span> 👍（0） 💬（0）<div>对于 launch(context) 的参数，除了Job类型外，我都能理解。
因为 参数有个Job，返回值是Job，父Context会包含一个Job，假设参数没有Job还会自己生成一个Job，乱糟糟的，搞不清楚它们之前的关系。</div>2023-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/a6/05/34357b55.jpg" width="30px"><span>王亚军</span> 👍（0） 💬（0）<div>它还会阻塞当前协程的执行流程，直到协程任务执行完毕。

这里的“当前协程”指的是deffered协程还是runBlocking协程？</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/32/27/2e524ac5.jpg" width="30px"><span>L0l@i</span> 👍（0） 💬（0）<div>老师，提个问题

fun main() {
    runBlocking {

        val job = launch(start = CoroutineStart.LAZY) {
            logX(&quot;Coroutine start!&quot;)
            download()
            logX(&quot;Coroutine end!&quot;)
        }
        delay(500L)
        job.log()
        job.start()
        job.log()

        job.join()      &#47;&#47; 等待协程执行完毕

        job.invokeOnCompletion {
            job.log()
        }

        logX(&quot;程序执行结束-Process end!&quot;)


    }

    println(&quot;can can need &quot;)
}

1，这里job挂起的是 val job  还是 runBlocking {} 块里面的
2，为什么【logX(&quot;程序执行结束-Process end!&quot;)】 和 【 println(&quot;can can need &quot;)】 会被卡住呢 （【 println(&quot;can can need &quot;)】是在runBlocking {} 块外的，不应该会被阻塞呀）
</div>2022-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/be/04/2d492543.jpg" width="30px"><span>Maggie</span> 👍（0） 💬（0）<div>想问下，动图里task是怎么定义的呢，runBlocking里定义的任务吗？</div>2022-11-28</li><br/>
</ul>