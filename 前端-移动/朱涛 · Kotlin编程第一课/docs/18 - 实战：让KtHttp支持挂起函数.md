你好，我是朱涛。今天这节实战课，我们接着前面[第12讲](https://time.geekbang.org/column/article/481787)里实现的网络请求框架，来进一步完善这个KtHttp，让它支持挂起函数。

在上一次实战课当中，我们已经开发出了两个版本的KtHttp，1.0版本的是基于命令式风格的，2.0版本的是基于函数式风格的。其中2.0版本的代码风格，跟我们平时工作写的代码风格很不一样，之前我也说了，这主要是因为业界对Kotlin函数式编程接纳度并不高，所以这节课的代码，我们将基于1.0版本的代码继续改造。这样，也能让课程的内容更接地气一些，甚至你都可以借鉴今天写代码的思路，复用到实际的Android或者后端开发中去。

跟往常一样，这节课的代码还是会分为两个版本：

- 3.0 版本，在之前1.0版本的基础上，扩展出**异步请求**的能力。
- 4.0 版本，进一步扩展异步请求的能力，让它**支持挂起函数**。

好，接下来就正式开始吧！

## 3.0 版本：支持异步（Call）

有了上一次实战课的基础，这节课就会轻松一些了。关于动态代理、注解、反射之类的知识不会牵涉太多，我们今天主要把精力都集中在协程上来。不过，在正式开始写协程代码之前，我们需要先让KtHttp支持异步请求，也就是Callback请求。

这是为什么呢？别忘了[第15讲](https://time.geekbang.org/column/article/487085)的内容：**挂起函数本质就是Callback！**所以，为了让KtHttp支持挂起函数，我们可以采用迂回的策略，让它先支持Callback。在之前1.0、2.0版本的代码中，KtHttp是只支持同步请求的，你可能对异步同步还有些懵，我带你来看个例子吧。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/c5/0a/c7267f5b.jpg" width="30px"><span>迩、卜懂莪</span> 👍（4） 💬（1）<div>Kthttp系列实战 像是简易版的retrofit2 对学习 retrofit的源码有很大帮助</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/8c/06f3aef0.jpg" width="30px"><span>神秘嘉Bin</span> 👍（3） 💬（3）<div>思考题：
（1）执行async可认为一瞬间就到了suspendCancellableCoroutine的await扩展方法，即协程被挂起。
（2）执行deferred.cancel()，可以使得挂起函数立刻返回并抛出协程cancel异常
（3）协程取消了，但网络请求还是发出去了，（因为网络请求有自己的线程）也会回来，调用continuation.resume，发现协程被取消了，抛出协程已经被取消的异常
（4.1）网络IO比deferred.await()早，那么deferred.await()会拿到异常，并catch
（4.2）网络IO比deferred.await()晚，那么deferred.await()会立刻返回，没有异常


以上都是我猜的，没有实际运行  -.- </div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/83/dd/e0f79039.jpg" width="30px"><span>荒原</span> 👍（1） 💬（1）<div>KtHttpV3.invoke()方法返回值这样写会将同步请求的返回值转成了一个异步的KtCall
return if (isKtCallReturn(method)){
            KtCall&lt;T&gt;(
                client.newCall(request),
                gson,
                getTypeArgument(method)
            )
        }else{
            val response = client.newCall(request).execute()
          &#47;&#47;这里转成了一个KtCall对象
            gson.fromJson(
                response.body?.string(),
                method.genericReturnType
            )
        }
而这样写就不会
if (isKtCallReturn(method)){
            return KtCall&lt;T&gt;(
                client.newCall(request),
                gson,
                getTypeArgument(method)
            )
        }else{
            val response = client.newCall(request).execute()

            return gson.fromJson(
                response.body?.string(),
                method.genericReturnType
            )
        }
这是为什么呢</div>2022-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/29/21/d90429b1.jpg" width="30px"><span>王安泽</span> 👍（1） 💬（1）<div>请问为什么Async的写法response返回后程序没有结束呢？ </div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/a7/ac23f5a6.jpg" width="30px"><span>better</span> 👍（1） 💬（1）<div>第一，它可以避免不必要的挂起，提升运行效率 ；请问老师，这一条指的是？
思考题：
网络请求还是会执行，第一点避免了，但是二点没有避免。</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（1） 💬（1）<div>问题二：像 suspendCoroutine 这一类系统所提供的挂起函数底层到底实现了什么，才使得其具有挂起的功能？是内部自己实现了 Callback 吗？为啥我们自己实现的 suspend 函数必须调用系统提供的挂起函数才能生效？</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>涛哥，问两个问题哈。如果上面例子中的网络请求是运行在当前线程，是不是这里的挂起实际上也没有什么用，因为其还是会阻塞当前线程（像下面的代码一样）？

suspend fun testSuspendFunc() {
    suspendCancellableCoroutine&lt;Unit&gt; {
        &#47;&#47; stimulate the network request
        Thread.sleep(5000)
        it.resumeWith(Result.success(Unit))
    }
}</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（3）<div>思考题的执行结果和 suspendCoroutine 的执行结果是一样的。取消了监听 invokeOnCancellation 的方法后，suspendCancellableoroutine 和 suspendCoroutine 本质上是一回事。</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/99/f133c8ff.jpg" width="30px"><span>梦佳</span> 👍（0） 💬（0）<div>已经实践于项目，协程包装原来网络请求，一行代码获取数据</div>2024-03-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/jibauP3icEFic4w56L2ddVghL7h2gGKhFdW8lBfE9rpwwRgzUKkLFY9wb4w70AXz7retME96a6EBRTA0LvSLn0ib8A/132" width="30px"><span>jack</span> 👍（0） 💬（0）<div>思考题的运行结果参考：
Time cancel: 697
invokeOnCompletion!
Time exception: 702
Catch exception:kotlinx.coroutines.JobCancellationException: DeferredCoroutine was cancelled; job=DeferredCoroutine{Cancelled}@25084a1e
Time total: 703
Request success!</div>2023-10-13</li><br/><li><img src="" width="30px"><span>常正午</span> 👍（0） 💬（0）<div>和retrofit2 源码相比，文章的代码质量差太远，还不如自己直接学习retrofit2如何支持suspend</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/99/f133c8ff.jpg" width="30px"><span>梦佳</span> 👍（0） 💬（0）<div>已经用起来了</div>2022-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（0） 💬（0）<div>思考题：

1. 除非没有Line 12 delay(50L) 或者 delay(0L)， 网络请求总是被发送出去，并返回结果。因为请求没有被取消。
2. 取消协程不一定能catch到cancel exception。
3. 如果网络请求在defer.await()之前返回，则协程正常返回，没有异常。否则，协程被取消的异常被catch。


注意两点
1. 本课的协程输出受delay时间影响。出现了request未被发送， request发送未返回和request发送返回 多种不同状态。
2. main函数执行完成后，process不能马上exit。因为okhttp创建了一个非daemon的线程。在timeout结束后process可以正常结束。</div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/0e/8d/d8f3298d.jpg" width="30px"><span>银河</span> 👍（0） 💬（0）<div>思考题结果：
Time cancel: 301
invokeOnCompletion!
Time exception: 301
Catch exception:kotlinx.coroutines.JobCancellationException: DeferredCoroutine was cancelled; job=DeferredCoroutine{Cancelled}@41c2284a
Time total: 301
Request success!

不难看出，suspendCancellableCoroutine函数是asyc被cancel后await立即恢复，不阻塞了，监听的是外部async的生命周期，而suspendCoroutine靠手动也就是监听网络请求call的返回结果</div>2022-08-01</li><br/>
</ul>