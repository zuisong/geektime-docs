你好，我是朱涛。

通过前面课程的学习，我们知道CoroutineScope是实现协程结构化并发的关键。使用CoroutineScope，我们可以批量管理同一个作用域下面所有的协程。那么，今天这节课，我们就来研究一下CoroutineScope是如何管理协程的。

## CoroutineScope VS 结构化并发

在前面的课程中，我们学习过CoroutineScope的用法。由于launch、async被定义成了CoroutineScope的扩展函数，这就意味着：在调用launch之前，我们必须先获取CoroutineScope。

```plain
// 代码段1

public fun CoroutineScope.launch(
    context: CoroutineContext = EmptyCoroutineContext,
    start: CoroutineStart = CoroutineStart.DEFAULT,
    block: suspend CoroutineScope.() -> Unit
): Job {}

public fun <T> CoroutineScope.async(
    context: CoroutineContext = EmptyCoroutineContext,
    start: CoroutineStart = CoroutineStart.DEFAULT,
    block: suspend CoroutineScope.() -> T
): Deferred<T> {}

private fun testScope() {
    val scope = CoroutineScope(Job())
    scope.launch{
        // 省略
    }
}
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（11） 💬（1）<div>思考题：SupervisorJob 重写了childCancelled方法，当异常发生，错误在整个树中传递，调用到​​cancelParent会调用parent.childCancelled，这个时候就会直接返回false而不是调用cancelImpl，错误传递就会终止，父协程不会被cancle掉。执行的路径其实和CancellationException异常类似，区别是cancelParent的返回值。</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（7） 💬（1）<div>CancellationException 引起的异常，会传递给兄弟节点吗？</div>2022-04-13</li><br/><li><img src="" width="30px"><span>辉哥</span> 👍（1） 💬（1）<div>原文: 另外，由于 CoroutineScope 当中的 Job 是我们手动创建的，并不需要执行任何协程代码，所以，它会是 true。也就是说，这里会执行注释 2 对应的代码

涛哥,结合上下文的意思,这里应该是会执行注释1对应的代码吧</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4a/5a/14eb7973.jpg" width="30px"><span>杨小妞</span> 👍（0） 💬（2）<div>环境：implementation &#39;org.jetbrains.kotlinx:kotlinx-coroutines-core:1.5.0&#39;
问题1：“而代码段 5 当中的 CoroutineScope(Job())，改成 CoroutineScope() 也是完全没问题的”，这里参数是不能为空的吧？
问题2：在创建CoroutineScope的时候，即使外部不传入Job，内部也会自己创建一个Job，那么JobSupport.initParentJob判断parent == null是否就多余了？
问题3：SupervisorJob可以阻断异常传递给父协程，它自己本身的子协程也是能接收到异常的吧。
</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>代码段4，假设launch是普通顶层函数，那么job应该取消不了里面的两个子协程吧了？</div>2023-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（0） 💬（0）<div>既然协程是结构化，有方法类似于tree命令，来dump协程的树形结构吗？</div>2022-06-24</li><br/>
</ul>