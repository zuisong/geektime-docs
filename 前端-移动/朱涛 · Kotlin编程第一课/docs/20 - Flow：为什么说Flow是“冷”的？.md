你好，我是朱涛。今天我们来学习Kotlin协程Flow的基础知识。

Flow，可以说是在Kotlin协程当中自成体系的知识点。**Flow极其强大、极其灵活**，在它出现之前，业界还有很多质疑Kotlin协程的声音，认为Kotlin的挂起函数、结构化并发，并不足以形成核心竞争力，在异步、并发任务的领域，RxJava可以做得更好。

但是，随着2019年Kotlin推出Flow以后，这样的质疑声就渐渐没有了。有了Flow以后，Kotlin的协程已经没有明显的短板了。简单的异步场景，我们可以直接使用挂起函数、launch、async；至于复杂的异步场景，我们就可以使用Flow。

实际上，在很多技术领域，Flow已经开始占领RxJava原本的领地，在Android领域，Flow甚至还要取代原本LiveData的地位。因为，Flow是真的香啊！

接下来，我们就一起来学习Flow。

## Flow就是“数据流”

Flow这个单词有“流”的意思，比如Cash Flow代表了“现金流”；Traffic Flow代表了“车流”；Flow在Kotlin协程当中，其实就是“数据流”的意思。因为Flow当中“流淌”的，都是数据。

为了帮你建立思维模型，我做了一个动图，来描述Flow的行为模式。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（15） 💬（1）<div>思考题:flow本身已经提供了线程切换的中间操作符flowOn和launchIn，来确定不同部分的线程边界并优化，withContext要再次切换线程，势必打破flow规划好的线程边界，估计要出错，抛出异常来提前报错。</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（4） 💬（1）<div>以下代码，为啥没有任何日志输出？
而且，为啥程序不会结束？

fun main() = runBlocking {
    withContext(dispatcher) {
        flow { log(&quot;emit&quot;); emit(1) }
            .flowOn(Dispatchers.Main)
            .filter { log(&quot;filter&quot;); it &gt; 0 }
            .collect { log(&quot;collect&quot;) }
    }
}</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/8f/d0874a01.jpg" width="30px"><span>曾帅</span> 👍（4） 💬（1）<div>关于思考题，翻了一下 emit() 的代码，发现里面有说到这一点。
里面说不允许在 withContext 里 调用 emit() 是因为 emit() 默认不是线程安全的，而且还给出了一种解决方案，那就是使用 channel 来处理。</div>2022-03-10</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（1）<div>原来在使用Rxjava还是Coroutine的时候，我还是支持使用Rxjava的，Flow出来之后，我就倒向Coroutine Flow。</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（2） 💬（3）<div>Flow 跟RxJava 的使用方式太像了</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f0/01/fd1c2548.jpg" width="30px"><span>pengzhaoyang coder</span> 👍（0） 💬（2）<div>发送的数据必须来自同一个协程内，不允许来自多个CoroutineContext，所以默认不能在flow{}中创建新协程或通过withContext()切换协程。如需切换上游的CoroutineContext，可以通过flowOn()进行切换</div>2022-04-01</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>Flow也有热的SharedFlow，还支持一对多的服务，我自己的经验是，Channel在具体场景中基本可以被Flow替代，而且更方便更安全。</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（0） 💬（1）<div>大佬，能结合几个服务端的例子讲讲不，其实协程的主要发挥场景还是在服务端，就像gorouting一样</div>2022-03-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpF5euTNx3GOkmf515HFh1ahAzogerLfIyLia2AspTIR9fkU6icGbo2ungo23cdM5s9dUjZGMno7ZA/132" width="30px"><span>dawn</span> 👍（0） 💬（2）<div>大佬，为什么下面的代码没法结束
fun main() {
    val asCoroutineDispatcher = Executors.newSingleThreadExecutor().asCoroutineDispatcher()
    val scope = CoroutineScope(asCoroutineDispatcher)
    runBlocking {
        flow {
            emit(1f)
            emit(&quot;s&quot;)
            kotlinx.coroutines.delay(2000)
            emit(2f)
            emit(3f)
&#47;&#47;            throw NullPointerException()
            emit(4f)
            emit(5f)
            logX(&quot;emit&quot;)
        }.filter {
            logX(&quot;filter&quot;)
            it is Float
        }.onStart {
            logX(&quot;onStart&quot;)
        }.onCompletion {
            logX(&quot;onCompletion&quot;)
        }.catch {
            logX(&quot;catch $it&quot;)
        }.onEach {
            logX(it)
        }.launchIn(scope)

        logX(&quot;end&quot;)
    }
}</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（0） 💬（3）<div>为啥下面代码中的 emit 也执行在 IO 线程？

fun main() = runBlocking {
    val flow = flow { log(&quot;emit&quot;); emit(1) }
    withContext(Dispatchers.IO) {
        flow.filter { log(&quot;filter&quot;); it &gt; 0 }
            .collect { log(&quot;collect&quot;) }
    }
}</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（0） 💬（1）<div>我猜是避免withContext和flowOn、launchIn的冲突，主动抛出一个异常对业务进行提示。</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/ed/80/157c58a9.jpg" width="30px"><span>从心所欲</span> 👍（0） 💬（1）<div>怎样在onCompletion的时候拿到flow的内容呢？</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（0） 💬（1）<div>既然 launchIn 也是用 collect 实现的，那么为什么需要在程序末尾 delay 一下呢？</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/0c/c623649c.jpg" width="30px"><span>稚者</span> 👍（1） 💬（0）<div>协程和Channel都有讲取消操作，那Flow有取消操作吗？</div>2023-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b7/0e/f7b48767.jpg" width="30px"><span>钟意</span> 👍（1） 💬（0）<div>作者的课程源代码，在哪里下载呢？</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>这不就是类似 Java8 的 Stream API？</div>2023-08-24</li><br/><li><img src="" width="30px"><span>Geek_416c20</span> 👍（0） 💬（0）<div>fun main() = runBlocking {
    launch {
        listOf&lt;Int&gt;(1, 2, 3)
            .asFlow()
            .onCompletion {
                println(&quot;onCompletion first: $it&quot;)
            }
            .collect {
                println(&quot;collect: $it&quot;)
                if (it == 2) {
                    cancel() &#47;&#47; 1
                    println(&quot;cancel&quot;)
                }
            }
    }
返回的结果，跟例子有所不同，这是为什么？
&#47;*
collect: 1
collect: 2
cancel
collect: 3
onCompletion first: null
*&#47;</div>2023-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/a1/3c/e415fa49.jpg" width="30px"><span>NormanYonng</span> 👍（0） 💬（1）<div>我作为稍微有java基础的感觉老师讲到java的对比时还是感觉到能很快深入理解，但是有个问题就是，实例代码有时候用高阶函数和kotlin标准函数的时候我就会一脸懵逼，去查这个函数作用。这个真的是这个课程很大的缺点，特别是没有编程经验的人来说，代码一般般解析需要理解代码的每一个字符作用及函数作用。希望老师能在第一课加个kotlin标准函数讲解，还有讲解代码时，使用的标准函数，讲解一下标准函数的作用</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（0） 💬（0）<div>withContext() 太具有侵入性。可能破坏flowOn和launchIn的逻辑。</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/98/c5/a0ca3e05.jpg" width="30px"><span>小人物</span> 👍（0） 💬（0）<div>老师关于launchIn的表述似乎比较模糊，launchIn的设计我觉得主要还是用于在一个新的协程中启动flow，从而避免阻塞外面的协程，因为collect操作符是挂起的。当我们有多个flow任务并发需求时，就可以用launchIn来方便的处理。至于collect代码的线程切换实际也不是一个问题，因为collect的执行环境就是所在协程的环境</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/2b/446ef7b6.jpg" width="30px"><span>许先森</span> 👍（0） 💬（0）<div>协程1.4之前cancel不成功，3还是会打印。1.4之后正常
collect: 1
collect: 2
cancel
collect: 3
onCompletion first: null
collect: 4
onCompletion second: null</div>2022-06-23</li><br/>
</ul>