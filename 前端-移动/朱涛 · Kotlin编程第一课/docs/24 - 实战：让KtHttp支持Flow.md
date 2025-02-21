你好，我是朱涛。又到了熟悉的实战环节，这一次我们接着来改造KtHttp，让它能够支持协程的Flow API。

有了前面两次实战的基础，这次我们应该就轻车熟路了。在之前的[4.0版本](https://time.geekbang.org/column/article/488985)中，为了让KtHttp支持挂起函数，我们有两种思路，一种是**改造内部**，另一种是**扩展外部**。同理，为了让KtHttp支持Flow，这次的实战也是这两种思路。

因此，这节课我们仍然会分为两个版本。

- 5.0版本，基于4.0版本的代码，从KtHttp的**外部扩展**出Flow的能力。
- 6.0版本，**修改KtHttp内部**，让它支持Flow API。

其实在实际的工作中，我们往往没有权限修改第三方提供的SDK，那么这时候，如果想要让SDK获得Flow的能力，我们就只能借助Kotlin的扩展函数，为它**扩展**出Flow的能力。而对于工程内部的代码，我们希望某个功能模块获得Flow的能力，就可以**直接修改它的源代码**，让它直接支持Flow。

那么在这节课里，我会同时用这两种手段来扩展并改造KtHttp，为你演示其中的关键步骤。在这个过程中，我也会为你讲解其中的常见误区和陷阱，这样一来，你就可以放心地将Flow应用到你的实际工作中了。

OK，让我们正式开始吧！

## 5.0版本：Callback转Flow
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/07/6d/4c1909be.jpg" width="30px"><span>PoPlus</span> 👍（5） 💬（1）<div>网络请求是一次性事件，我都改用 Flow 的话合适吗？</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（1） 💬（2）<div>awaitClose感觉有等待协程执行结束的作用，等待老师的专业解答</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/93/b4791ee3.jpg" width="30px"><span>白泽丶</span> 👍（0） 💬（1）<div>是不是和 delay() 一样，在外部取消时抛出 CancellationException 异常并从而让协程退出呢</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（0） 💬（1）<div>去掉awaitClose后程序有异常了。
java.lang.IllegalStateException: &#39;awaitClose { yourCallbackOrListener.cancel() }&#39; should be used in the end of callbackFlow block.
Otherwise, a callback&#47;listener may leak in case of external cancellation.
See callbackFlow API documentation for the details.
原因还不清楚。。。</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（0） 💬（1）<div>为什么第5版中的程序要等一会儿才会退出呢？</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4b/b9/44443af4.jpg" width="30px"><span>漱口杯</span> 👍（1） 💬（0）<div>注释调awaitClose可能会发生内存泄漏，官方文档里是这样写的：
使用awaitClose是强制性的，以防止取消流量收集时发生内存泄漏，否则即使流量收集器已经完成，回调也可能继续运行。为避免此类泄漏，如果块返回但通道尚未关闭，此方法将抛出IllegalStateException </div>2023-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/be/661f406b.jpg" width="30px"><span>彭Kai.</span> 👍（0） 💬（0）<div>挂起当前的协程，好让flow里的代码执行，要不然不会执行</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（0） 💬（0）<div>awaitClose内部实现是suspendCancellableCoroutine。 所以它可以支持结构化的取消，比如从parent job来的取消请求。</div>2022-08-20</li><br/>
</ul>