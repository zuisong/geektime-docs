你好，我是朱涛。这节课，我们来学习协程的挂起函数。

挂起函数，是Kotlin协程当中最基础、最重要的知识点。如果对协程的挂起函数没有足够的认识，我们后续的学习将会困难重重。如果不理解挂起函数，我们将无法理解协程的非阻塞；如果不了解挂起函数，我们将无法掌握Channel、Flow等API；如果不理解挂起函数，我们写出来的代码也会漏洞百出，就更别提优化软件架构了。

相反，如果能将挂起函数理解透彻，我们后面的学习也会更加轻松一些。所以这节课，我会从应用和原理两个角度，来带你理解挂起函数，包括如何使用挂起函数来优化异步任务，以及挂起函数的CPS当中的Continuation到底是什么。通过对这两个维度的学习，你在更轻易地掌握挂起函数应用场景的同时，对它的底层原理也会有一定认识。

那么接下来，你一定要打起精神，我们一起来攻克这个关键的知识点！

## 挂起函数：Kotlin协程的优势

通过前面课程的学习，我们已经知道了：协程就像是轻量级的线程一样。用线程能实现的功能，我们借助launch和async也同样可以做到。

不过你可能会好奇，如果只是把thread{} 替换成launch{}，那协程比起线程也没什么特殊的优势吧？**仅仅只是因为“轻量”“非阻塞”，我们就应该放弃线程，拥抱协程吗？**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（23） 💬（2）<div>public interface Continuation&lt;in T&gt; {
    &#47;**
     * The context of the coroutine that corresponds to this continuation.
     *&#47;
    public val context: CoroutineContext

    &#47;**
     * Resumes the execution of the corresponding coroutine passing a successful or failed [result] as the
     * return value of the last suspension point.
     *&#47;
    public fun resumeWith(result: Result&lt;T&gt;)
}
suspend函数的入参Continuation，看源码可以知道需要有一个协程上下文CoroutineContext信息，只有在协程作用域里才能传递。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/a6/18c4f73c.jpg" width="30px"><span>Airsaid</span> 👍（22） 💬（1）<div>老师您好，为什么 Kotlin 选择使用关键字来定义挂起函数而不是使用注解呢？（例如 Compose 就使用的是注解的方式）</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c4/bd/44757daf.jpg" width="30px"><span>墨方</span> 👍（19） 💬（1）<div>被调用的挂起函数需要传入一个Continuation(当然这个传入也是幕后编译做的), 没有被suspend修饰的函数是没有Continuation参数的,所以被调用的挂起函数没有办法从普通函数中获取一个Continuation。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/27/6c/5abd5e9f.jpg" width="30px"><span>AKEI</span> 👍（5） 💬（1）<div>所以kotlin的挂起函数只是相当于让回调函数更简洁，相当于封装了线程池，并没有任何更高效的性能优化是吗？</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/ca/50c1fd43.jpg" width="30px"><span>colin</span> 👍（5） 💬（2）<div>挂起函数本身并不支持挂起，所以它没法在普通函数中调用，而它之所以能在挂起函数中调用，是因为挂起函数最终都是在协程中被调用，是协程提供了挂起函数运行的环境。</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/38/aad89fe5.jpg" width="30px"><span>Luckykelan</span> 👍（4） 💬（7）<div>老师您好，有个问题不太清楚
val user = getUserInfo()
val friendList = getFriendList(user)
val feedList = getFeedList(friendList)
这段代码和协程思维模型那张动图一起看，代码执行到getUserInfo()函数时，这个函数就被挂起了，不是应该继续执行val friendList = getFriendList(user)吗？为什么实际上在这里没有继续执行而是等待了getUserInfo()的返回呢？</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/59/f2/ef476ddc.jpg" width="30px"><span>的的喀喀湖</span> 👍（3） 💬（1）<div>讲的确实不错，之前看了好多文章没看懂挂起的概念，跟着这两篇文章自己走了一遍代码终于能理解了</div>2022-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（2） 💬（1）<div>图文说明，写的真好。</div>2022-02-21</li><br/><li><img src="" width="30px"><span>InfoQ_0880b52232bf</span> 👍（1） 💬（1）<div>关于思考题，我想可以尝试逆向思考一下，假如普通函数可以调用挂起函数，那么会出现什么情况呢？
比如：我们在main方法里可以直接调用这三个挂起函数（实际不能直接调用），我们预期的结果是同步方式实现异步请求（这也是协程的特点之一），但其实按照非阻塞挂起的特点，main方法会直接打印“main end”，无法满足我们的预期：
fun main() {
    val userInfo = getUserInfo()
    val friendList = getFeedList(userInfo)
    val feedList = getFeedList(friendList)
    println(&quot;main end&quot;)
}

suspend fun getUserInfo(): String {
    withContext(Dispatchers.IO) { delay(1000L) }
    return &quot;BoyCoder&quot;
}

suspend fun getFriendList(user: String): String {
    withContext(Dispatchers.IO) { delay(1000L) }
    return &quot;Tom, Jack&quot;
}

suspend fun getFeedList(list: String): String {
    withContext(Dispatchers.IO) { delay(1000L) }
    return &quot;{FeedList..}&quot;
}</div>2022-04-18</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（1） 💬（1）<div>suspend -&gt; Continuation -&gt;CoroutineContext + resumeWith
协程上下文才是挂起和回调的幕后黑手，😀，也就是说所有的挂起函数调用的时候最终都要依托于某个协程。
</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e5/e1/a5064f88.jpg" width="30px"><span>Geek_Adr</span> 👍（1） 💬（1）<div>我理解 挂起函数（suspend 关键字）就类似于 注解，协程包含是具体解析与实现</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/d2/204edd23.jpg" width="30px"><span>WWWarmFly</span> 👍（1） 💬（2）<div>请教老师，文中有一句话     “你可能觉得，既然协程和挂起函数都是支持挂起和恢复的，那它们两个是不是同一个东西呢？”

这里说的协程支持挂起和恢复，是不是说多个协程间的？挂起函数的挂起和恢复是不是说一个协程内的？

但是多个协程间也是可以阻塞的，之前就有协程中调用sleep的例子。协程间的非阻塞其实是借助于delay，这是一个挂起函数。


那“你可能觉得，既然协程和挂起函数都是支持挂起和恢复的，那它们两个是不是同一个东西呢？” 是不是可以认为是同一个东西。
</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/ea/373d8e6b.jpg" width="30px"><span>夜班同志</span> 👍（1） 💬（1）<div>挂起函数才有恢复的&quot;callback&quot;，普通函数没有</div>2022-02-18</li><br/><li><img src="" width="30px"><span>20220106</span> 👍（0） 💬（4）<div>小问题：挂起函数，被挂起后（被抓手）的挂起函数去干嘛了，就是暂停运行了嘛，看单词意思是这个意思。</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>suspend 函数经过 CPS 转换，参数会多一个 Continuation 参数，其表示协程体，同时挂起函数内部会创建一个 SafeContinuaton 实例，将协程体的 continuation 保存到内部，SC 的作用是确保 resumeWith 只调用一次。</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（2）<div>我觉得是协程体 block 才是 cotinuation 回调，suspend 函数严格意义上不是回调。</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/93/b4791ee3.jpg" width="30px"><span>白泽丶</span> 👍（0） 💬（1）<div>加了 suspend 关键字的函数，才会被进行 CPS 转换，也就是说挂起函数在未编译时表现的只是表面的函数类型，最后会被翻译成另一种类型；而普通函数则一直是原来的类型，为了防止开发者误调，编译器才加了这个错误提示。suspend 应该也只是一个标记的作用，不知道这样理解对不对...</div>2022-03-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vpHvsPl7ffl3ECrKxH1j0R1W8lYWc8svvlz0cahq8KZpNYMHicWiaTGJLWFyQsy8rTJcGAAVDhKCAeHRkTPKeqTQ/132" width="30px"><span>kevintcl24</span> 👍（0） 💬（1）<div>问题描述：
continuation后面的要执行的代码，看CPS 转换动画效果，相当于被移动到Continuation接口的resumeWith函数中。
我的问题是：
在上一个执行动画中，getUserInfo在子线程执行的。然后切换到了主线程返回结果。我想问resumeWith
函数的调用就已经被kotlin 切换到了主线程了吗？如果是，大概切换的外代码是怎么样的哟。
协程这个有点烧脑壳</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/10/fc/213c381f.jpg" width="30px"><span>请叫我潜水员</span> 👍（0） 💬（2）<div>是不是因为只有协程才有恢复能力，所以挂起函数只能在协程中调用</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/d3/e25d104a.jpg" width="30px"><span>êｗěｎ</span> 👍（0） 💬（2）<div>问题：continuation后面的要执行的代码，这里得代码是指有上下文关联的吗？比如后面代码要用到前面的返回值。
问题2: 挂起函数会主动开启新协程吗？</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（1） 💬（0）<div>挂起函数有回复点，普通函数没有恢复点。挂起函数无法在普通函数中返回。</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/bd/f3977ebb.jpg" width="30px"><span>John</span> 👍（0） 💬（0）<div>如果suspend函数里需要调用一个long running的函数 比如在Service里的suspend method去调用一个传统Spring Data JPA(而非R2DBC)的普通method 该怎么办呢? 是用那个在withContext里的Dispatcher.IO么?</div>2024-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（2）<div>也就是说，挂起函数至少需要两个参数才能正常使用：CoroutineScope 和 Continuation。
其中CoroutineScope持有一个CoroutineContext，而Continuation需要一个CoroutineContext，它将提供给Continuation使用。</div>2023-12-31</li><br/><li><img src="" width="30px"><span>RETR0</span> 👍（0） 💬（3）<div>朱老师你好，关于这段话：

另外，表面上看起来是同步的代码，实际上也涉及到了线程切换，一行代码，切换了两个线程。比如“val user = getUserInfo()”，其中“=”左边的代码运行在主线程，而“=”右边的代码运行在 IO 线程。

请问挂起函数的调用就一定会涉及到线程的切换吗？难道不应该是协程的切换吗？等号左右两边的代码应该只是位于不同的协程中而已吧？</div>2023-04-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1CHiaNHUWw45OWIbjom5EPjQqiauqoZROdU3Qibh8vA2zrhia7icxkVmibekXTicU2X8ceBdaqrS36bpLa6oE9jsqnNCw/132" width="30px"><span>菜鸡皮</span> 👍（0） 💬（2）<div>老师请问一下：一个协程是否就是一个动图中的task？如果不是的话，怎么创建第二个task呢？还有挂起的是指不会阻塞主线程还是网络请求的子线程呢？</div>2023-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhhu1P5vUiagyT97qwPyNTcuIBE0b325DKIkBfeI0Xr6gyUZC7aWA1qP6IJicReEfqpv1wxylwbJzA/132" width="30px"><span>wangfeng</span> 👍（0） 💬（0）<div>挂起函数在调用时包含协程挂起的语义，在返回时包含协程恢复的语义。在无栈协程中，挂起点状态通过闭包或对象保存。而kotlin的挂起点状态保存在Continuation 中。在非挂起函数中没有Continuation这个对象。</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/e6/b626aa9c.jpg" width="30px"><span>Lindroid</span> 👍（0） 💬（0）<div>动画真的做得太赞了！</div>2022-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/f4/6bd66c0e.jpg" width="30px"><span>Jevan Wu</span> 👍（0） 💬（0）<div>老师您好，如果协程的挂起和恢复其实是切换线程运行，那这个过程会导致频繁线程切换，这在某些情况下会导致更多的时间和资源消耗吧？</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/88/81511d7b.jpg" width="30px"><span>湘良君</span> 👍（0） 💬（0）<div>请教下，有点困惑协程和suspend的关系。到底是协程的挂起能力依赖suspend来实现？还是说suspend挂起函数的实现依托于协程？</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/09/2e/4badf056.jpg" width="30px"><span>余先声</span> 👍（0） 💬（2）<div>老师，问个问题，如果suspend里头并没有切换线程，也就是调用suspend的线程和执行suspend函数的线程是同一线程，那么suspend方法依然会阻塞当前调用线程，是这样的么？</div>2022-06-13</li><br/>
</ul>