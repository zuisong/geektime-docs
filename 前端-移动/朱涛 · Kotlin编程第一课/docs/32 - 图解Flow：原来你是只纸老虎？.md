你好，我是朱涛。今天我们来研究Flow的源代码。

经过前面的学习，我们已经知道了，Channel和Flow都是数据流，Channel是“热”的，Flow则是“冷”的。这里的冷，代表着Flow不仅是“冷淡”的，而且还是“懒惰”的。

除了“冷”这个特性以外，Flow从API的角度分类，主要分为：构造器、中间操作符、终止操作符。今天这节课，我们将会从这几个角度来分析Flow的源码，来看看它的这几类API是如何实现的。

经过这节课的学习，你会发现：虽然Flow的功能看起来非常高大上，然而它的原理却非常的简单，是一只名副其实的“纸老虎”。

## Flow为什么是冷的？

在正式开始研究Flow源代码之前，我们首先需要确定研究的对象。这里，我写了一段Demo代码，接下来我们就以这个Demo为例，来分析Flow的整个执行流程：

```plain
// 代码段1

fun main() {
    val scope = CoroutineScope(Job())
    scope.launch {
        testFlow()
    }

    Thread.sleep(1000L)

    logX("end")
}

private suspend fun testFlow() {
    // 1
    flow {
        emit(1)
        emit(2)
        emit(3)
        emit(4)
        emit(5)
    }.collect {      // 2
            logX(it)
        }
}

/**
 * 控制台输出带协程信息的log
 */
fun logX(any: Any?) {
    println(
        """
================================
$any
Thread:${Thread.currentThread().name}
================================""".trimIndent()
    )
}

/*
输出结果
================================
1
Thread:DefaultDispatcher-worker-1
================================
================================
2
Thread:DefaultDispatcher-worker-1
================================
================================
3
Thread:DefaultDispatcher-worker-1
================================
================================
4
Thread:DefaultDispatcher-worker-1
================================
================================
5
Thread:DefaultDispatcher-worker-1
================================
================================
end
Thread:main
================================
*/
```
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="" width="30px"><span>Paul Shan</span> 👍（11） 💬（1）<div>Flow 接口引用了FlowCollector接口，并封装了一段调用逻辑，作为将来FlowCollector使用的来源。FlowCollector，带有emit函数的接口，统一了上游的发送方的数据输出和下游接收方的数据输入。FlowCollector的做法和通常扩展函数不太一样，通常的扩展函数是先有核心类，然后扩展函数扩充核心类的功能。FlowCollector是先在上游的构造器里构建了高阶的扩展函数，然后在下游collect里实现了带有emit的核心类。下游collect触发流程，然后上游的emit驱动下游的emit。这么设计原因应该是上游的构造器，相对复杂，而且是推迟执行的，需要给开发人员以足够的灵活性，所以采用了扩展函数的格式，下游接受数据相对固定，而且是同步执行的，采用固定的FlowCollector接口。
</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（1）<div>老师，下节课的目录得改下。。。应该是Android开发者还有未来吗？市场基本都没需求了</div>2022-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/00/da/790e0a76.jpg" width="30px"><span>zyaire</span> 👍（1） 💬（2）<div>老师，“Flow 上游与下游的协程上下文就会不一致，它们整体的结构也会被破坏，从而导致“结构化并发”的特性也被破坏。”这句话不是很能理解，以代码11来说，即使在flow中调用withContext切换了上下文，当外部协程取消时，不也是会响应取消操作吗</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/34/abb7bfe3.jpg" width="30px"><span>再前进一点</span> 👍（1） 💬（1）<div>同问：为啥transform{}这方法在IDE里点击跳转到的源码是unsafeTransform这个方法呢</div>2022-04-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpF5euTNx3GOkmf515HFh1ahAzogerLfIyLia2AspTIR9fkU6icGbo2ungo23cdM5s9dUjZGMno7ZA/132" width="30px"><span>dawn</span> 👍（1） 💬（3）<div>@PublishedApi
internal inline fun &lt;T, R&gt; Flow&lt;T&gt;.unsafeTransform(
    @BuilderInference crossinline transform: suspend FlowCollector&lt;R&gt;.(value: T) -&gt; Unit
): Flow&lt;R&gt; = unsafeFlow { &#47;&#47; Note: unsafe flow is used here, because unsafeTransform is only for internal use
这里的作用域应该是FlowCollector，为什么可以调用collect函数
    collect { value -&gt;
        &#47;&#47; kludge, without it Unit will be returned and TCE won&#39;t kick in, KT-28938
        return@collect transform(value)
    }
}

@PublishedApi
internal inline fun &lt;T&gt; unsafeFlow(@BuilderInference crossinline block: suspend FlowCollector&lt;T&gt;.() -&gt; Unit): Flow&lt;T&gt; {
    return object : Flow&lt;T&gt; {
        override suspend fun collect(collector: FlowCollector&lt;T&gt;) {
            collector.block()
        }
    }
}</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>&#47;&#47; 2
internal inline fun &lt;T, R&gt; Flow&lt;T&gt;.unsafeTransform(
    crossinline transform: suspend FlowCollector&lt;R&gt;.(value: T) -&gt; Unit
): Flow&lt;R&gt; = unsafeFlow { 
    &#47;&#47; 6
    collect { value -&gt;
        &#47;&#47; 7
        return@collect transform(value)
    }
}

老师，可以解答下么：

1、transform 的接受者是哪个实例呢？是 flow {}.filter {}.collect {} 中终止操作符号  collect 传入的 FlowCollector

还是注释 6 处  collect 传入的 FlowCollector 实例呢？

按照逻辑的话，应该是终止操作符号 collect {} 传入的 FlowCollector。

但是看逻辑，注释 6 处的 collect 的参数也是个 FlowCollector 实例，那么 transform 的接受者应该是它？？</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>&#47;&#47; 2
internal inline fun &lt;T, R&gt; Flow&lt;T&gt;.unsafeTransform (
    crossinline transform: suspend FlowCollector&lt;R&gt;.(value: T) -&gt; Unit
): Flow&lt;R&gt; = unsafeFlow { 
    &#47;&#47; 6
    collect { value -&gt;
        &#47;&#47; 7
        return@collect transform (value)
    }
}</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>
&#47;&#47; 代码段8

&#47;&#47; 1
inline fun &lt;T&gt; Flow&lt;T&gt;.filter(
    crossinline predicate: suspend (T) -&gt; Boolean
): Flow&lt;T&gt; = transform { value -&gt;
    &#47;&#47; 8
    if (predicate(value)) return@transform emit(value)
}

&#47;&#47; 2
internal inline fun &lt;T, R&gt; Flow&lt;T&gt;.unsafeTransform(
    crossinline transform: suspend FlowCollector&lt;R&gt;.(value: T) -&gt; Unit
): Flow&lt;R&gt; = unsafeFlow { 
    &#47;&#47; 6
    collect { value -&gt;
        &#47;&#47; 7
        return@collect transform(value)
    }
}

&#47;&#47; 3
internal inline fun &lt;T&gt; unsafeFlow(
    crossinline block: suspend FlowCollector&lt;T&gt;.() -&gt; Unit
): Flow&lt;T&gt; {
    &#47;&#47; 4
    return object : Flow&lt;T&gt; {
        &#47;&#47; 5
        override suspend fun collect(collector: FlowCollector&lt;T&gt;) {
            collector.block()
        }
    }
}

老师好，想在问一个问题：
 
unsafeTransform  中的 collect 参数是一个 FlowCollector 匿名内部类实例

那 return@collect transform(value) 中的  transform 的接收者是这个 FlowCollector 匿名内部类实例

还是 flow{}.filter{}.collect{} 中，终止操作符传入的 FlowCollector 匿名内部类实例呢？？</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>老师好，对于 Flow 的 fliter 的源码，确实没看懂，可以详细讲下么？？

直接看源码不直观，反编译看 java 有很凌乱

&#47;&#47; unsafeTransform
&#47;&#47; 2
inline fun &lt;T&gt; Flow&lt;T&gt;.unsafeTransform(
    crossinline transform: suspend FlowCollector&lt;T&gt;.(value: T) -&gt; Unit &#47;&#47; FlowCollector.transform
): Flow&lt;T&gt; {
    return unsafeFlow { 
        &#47;&#47; 这里的作用域应该是 FlowCollector，为什么可以调用 collect 函数
        collect(object : FlowCollector&lt;T&gt; { 
            override suspend fun emit(value: T) {
                &#47;&#47; 7
                transform(value)
            }
        })
        &#47;&#47; 6
&#47;&#47;        collect { value -&gt;
&#47;&#47;            &#47;&#47; 7
&#47;&#47;            return@collect transform(value)
&#47;&#47;        }
    }
}</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（2）<div>难道说是因为 unsafeFlow 创建的是一个匿名内部类的实例，匿名内部类的实例是持有外部对象 SafeFlow 的引用？？？</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>filter(..）貌似是新建了一个 FLow，flow {... ... ...} 创建  SafeFlow 貌似没用到呀

老师解答下呀，谢谢。。

</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/75/4e0d7419.jpg" width="30px"><span>飓风</span> 👍（0） 💬（3）<div>“它的类型是Function3, Any?, Continuation, Any?&gt;” 这个怎么理解？</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c6/78/9b1e4b15.jpg" width="30px"><span>ZircoN</span> 👍（0） 💬（1）<div>1. 为啥transform{}这方法在IDE里点击跳转到的源码是unsafeTransform这个方法呢
2. SharedFlow等是否准备讲一下呢</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>扁平化后的filter函数：
inline fun &lt;T&gt; Flow&lt;T&gt;.filter(
    crossinline predicate: suspend (T) -&gt; Boolean
): Flow&lt;T&gt; = object : Flow&lt;T&gt; {
    override suspend fun collect(collector: FlowCollector&lt;T&gt;) {
        this@filter.collect { value -&gt;
            if (predicate(value)) {
                collector.emit(value)
            }
        }
    }
}
</div>2024-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUXpvIbKKeXfHv2xS2aUJYCLlNsmIQUicTicSuRqWQeicrput3ytRIgbM3tErHRJrorCiaS9u6lqZUrg/132" width="30px"><span>Geek_3074ac</span> 👍（0） 💬（0）<div>“Flow 上游与下游的协程上下文就会不一致，它们整体的结构也会被破坏，从而导致“结构化并发”的特性也被破坏。”

老师我想问下，假设我维持了父子关系，从理论来说是不是就没问题了

lifecycleScope.launch {
            flow&lt;Int&gt; {
                emit(1)
                emit(2)
                emit(3)
                withContext(Job(parent = currentCoroutineContext()[Job])) {

                }
            }
                .filter { it &lt; 2 }
                .collect { }
        }

限制的原因是因为使用成本太高，要懂得 Job 的结构化并发，所以禁止这样使用吗
</div>2023-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2e/08e6ce7c.jpg" width="30px"><span>薄荷</span> 👍（0） 💬（0）<div>我的理解是：
flow这个顶层函数生成Flow的过程其实就是携带了block块中的数据，按照我的理解我写了下面这样一个类
class MFlow&lt;T&gt;(vararg elements: T) {
    private val list: List&lt;T&gt;

    init {
        list = elements.asList()
    }

    suspend fun collect(collector: FlowCollector&lt;T&gt;) {
        for (element in list) {
            collector.emit(element)
        }
    }
}
而FlowCollector的emit方法其实是对数据的具体处理逻辑，
Flow的collect函数调用会传入一个FlowCollector对象，同时用具体逻辑处理之前保存的数据</div>2022-07-21</li><br/>
</ul>