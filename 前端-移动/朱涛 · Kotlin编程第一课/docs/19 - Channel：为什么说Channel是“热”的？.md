你好，我是朱涛。

前面我们学习的挂起函数、async，它们一次都只能返回一个结果。但在某些业务场景下，我们往往需要协程返回多个结果，比如微信等软件的IM通道接收的消息，或者是手机GPS定位返回的经纬度坐标需要实时更新。那么，在这些场景下，我们之前学习的协程知识就无法直接解决了。

而今天我要讲解的Kotlin协程中的Channel，就是专门用来做这种事情的。类似的需求，如果我们不使用Channel而是用其他的并发手段配合集合来做的话，其实也能实现，但复杂度会大大增加。那么接下来，我们就一起来学习下Channel。

## Channel就是管道

顾名思义，Channel就是一个管道。我们可以用这个概念，先来建立一个思维模型：

![](https://static001.geekbang.org/resource/image/6e/e7/6e3884f46932e80f080191d20cc26be7.gif?wh=1080x270)

Channel这个管道的其中一端，是发送方；管道的另一端是接收方。而管道本身，则可以用来传输数据。

所以，我们根据上面的思维模型，很容易就能写出下面的代码。

```plain
// 代码段1

fun main() = runBlocking {
    // 1，创建管道
    val channel = Channel<Int>()

    launch {
        // 2，在一个单独的协程当中发送管道消息
        (1..3).forEach {
            channel.send(it) // 挂起函数
            logX("Send: $it")
        }
    }

    launch {
        // 3，在一个单独的协程当中接收管道消息
        for (i in channel) {  // 挂起函数
            logX("Receive: $i")
        }
    }

    logX("end")
}

/*
================================
end
Thread:main @coroutine#1
================================
================================
Receive: 1
Thread:main @coroutine#3
================================
================================
Send: 1
Thread:main @coroutine#2
================================
================================
Send: 2
Thread:main @coroutine#2
================================
================================
Receive: 2
Thread:main @coroutine#3
================================
================================
Receive: 3
Thread:main @coroutine#3
================================
================================
Send: 3
Thread:main @coroutine#2
================================
// 4，程序不会退出
*/
```
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（16） 💬（1）<div>Channel 是“热”的可能会导致一下几个问题：
1. 可能会导致数据的丢失。
2. 浪费不必要的程序资源，类似于非懒加载的情况。
3. 如果未及时 close 的话，可能会导致内存泄露。</div>2022-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Urc67zDC8R6dh9U1ZFTF36icXewM1seehvOUYUs4hyWSsFzS5WQc2RcrE1Mzs8qtgib5SM5wFrVh22QcQd0JUUBw/132" width="30px"><span>jim</span> 👍（5） 💬（1）<div>Channel平时工作中有 哪些使用场景？？？</div>2022-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（3） 💬（1）<div>1、最开始  channel.receive () 先调用，但是 channel 没有 item，所以挂起；

2、协程启动要时间，send(it) 后调用，发送 item，然后 输入 “send1”；

3、 协程循环再调用 send(it)，此时队列已经满了，所以挂起，并唤起接收协程，然后 输入 “receive1”；

3、接收协程... ... ...</div>2022-04-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL11eYiaBo5voEzTIEkNgOgZ0KSsMw9UeStPgfEUVEndUhG2nxL5WnLaQ9sEDWctVZJ9Lgyn9iaCh1A/132" width="30px"><span>Geek_8a5ee1</span> 👍（3） 💬（1）<div>可以讲一下viewModelScope的区别吗</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/d3/e25d104a.jpg" width="30px"><span>êｗěｎ</span> 👍（3） 💬（2）<div>Recieve的cancel是清空channel中的消息，但不会close吧？ 像go中如果在consumer 中关闭，会导致sender的panic。感觉kotlin也有这种陷阱。</div>2022-03-02</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（2） 💬（1）<div>对于接收方而言，热的Channel状态是时刻改变的，数据之间是强依赖。简单的情况还好，如果Channel的数据级联了几次之后，调试就成了噩梦，这和滥用EventBus一样。
</div>2022-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（2） 💬（1）<div>以上代码看起来是可以正常工作了。但是，我仍然不建议你用这种方式。因为，当你为管道指定了 capacity 以后，以上的判断方式将会变得不可靠！原因是目前的 1.6.10 版本的协程库，运行这样的代码会崩溃，如下所示：

-------------

这是现象，而不是原因呀，具体原因是什么呢？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（1） 💬（2）<div>为什么例子中是ReceiveChannel 在send？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/b8/c887a5ea.jpg" width="30px"><span>Xs.Ten</span> 👍（0） 💬（1）<div>老师好，请问Channel 里面 Sender 和 Receiver 的身份可以发生互换么？</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（0） 💬（3）<div>public fun &lt;E&gt; Channel(
    capacity: Int = RENDEZVOUS,
    onBufferOverflow: BufferOverflow = BufferOverflow.SUSPEND,
    onUndeliveredElement: ((E) -&gt; Unit)? = null
): Channel&lt;E&gt;

Channel居然也是个方法，为啥方法名是大写字母开头的? 难道是因为它是顶层方法?</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（0） 💬（2）<div>val channel: ReceiveChannel by ::_channel
 private val _channel: Channel = Channel()

Channel既然是个接口，为啥还能直接实例化？</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/31/76/8e3347a1.jpg" width="30px"><span>学习中...</span> 👍（0） 💬（1）<div>协程库最新不是1.6.0吗，怎么有1.6.10呢
https:&#47;&#47;github.com&#47;Kotlin&#47;kotlinx.coroutines&#47;releases</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（0） 💬（2）<div>老师好，我又重新发了一遍哈

代码段12
发送【奇数】条数据的时候正常，发送【偶数】条数据的时候就会异常崩溃
例如   (1..2)   (1..4)   (1..6) 都会异常
这是什么原因呢？

fun main() = runBlocking {
    val channel: ReceiveChannel&lt;Int&gt; = produce {
        (1..2).forEach { &#47;&#47; 发送【奇数】条数据时是正常的，发送【偶数】条数据时就会崩溃
            send(it)
            println(&amp;#34;Send: $it&amp;#34;)
        }
    }
    while (!channel.isClosedForReceive) {
        val i = channel.receive()
        println(&amp;#34;Receive: $i&amp;#34;)
    }
    println(&amp;#34;end&amp;#34;)
}

代码接报错信息如下图：
https:&#47;&#47;gitee.com&#47;baiqiantao&#47;blogPic&#47;raw&#47;master&#47;img&#47;2020&#47;20220314204734.png</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（0） 💬（1）<div>老师你好，能举几个实际场景中channel使用例子吗？什么时候需要使用这种双向数据流呢？</div>2022-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epW39iazElic8B436AHhEePqOibvHr2lSXJ0LMwiavicmCPtXwXxBuxyy6l7pEiblo198fTpFiayCoyoj8Jw/132" width="30px"><span>tedzyc</span> 👍（0） 💬（1）<div>老师能有空能讲讲Android Jetpack的paging3这个库吗？里面用BroadcastChannel通信那块能否帮着分析一下。</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ef/c0/537b3905.jpg" width="30px"><span>L先生</span> 👍（0） 💬（1）<div>个人理解。因为是热管道，如果开发者不注意或者因为某些意外原因，可能会导致挂起，或者队列过大的情况。参考eventbus,除非是sticky状态，否则没有注册接受事件的话，是发不出去的</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（0） 💬（3）<div>Channel是“热”的，导致想接收数据时会接收到之前的旧数据，而可能只希望接收当前开始发送的数据。</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/8a/f7a3d5e6.jpg" width="30px"><span>Allen</span> 👍（0） 💬（4）<div>涛哥，我有几个问题问一下哈：
1. send 函数是如何挂起的？虽然它是一个 suspend 函数，但它可以连续发多个数据（容量足够的情况下），直到数据发送完后才被挂起？
2. 当 send 函数被挂起后，是如何恢复的？
3.代码段 1 的例子，打印的结果为什么不是交替的，而是乱序的？</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（0） 💬（1）<div>一直没懂“冷”和“热”的概念，今天似乎明白了。

思考题：
有坏处。因为不管有没有接受都在一直工作，那么势必会造成资源的浪费。</div>2022-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/ae/e5/e910c716.jpg" width="30px"><span>lopy</span> 👍（0） 💬（0）<div>    runBlocking {
        val channel = Channel&lt;Int&gt;(onBufferOverflow = BufferOverflow.DROP_OLDEST)
        &#47;&#47;代码块1
        launch {
            println(&quot;send：${Thread.currentThread().name}&quot;)
            (1..3).forEach {
                println(&quot;before send  $it&quot;)
                channel.send(it)
                println(&quot;after send $it&quot;)
            }
        }

        &#47;&#47;代码块2
        launch {
            for (i in channel){
                println(&quot;before receive $i&quot;)
                println(&quot;result == $i&quot;)
                println(&quot;after receive $i&quot;)
            }
        }

    }
老师你好，按照这段代码接收端只会收到数据3，为什么我把代码块1、2互换以后接收端会接受到数据1、3，一直没弄明白</div>2023-02-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er7DPjeHkPLcAJYvlhTjezPfj8sw8ZJAM93ZMSIERVUvLs0K5qSZzZJhtar1mp7tN4GdLkyCfpmbg/132" width="30px"><span>Geek_b8faf4</span> 👍（0） 💬（1）<div>```
fun main() = runBlocking {
    val channel = Channel&lt;Int&gt;(
        capacity = Channel.RENDEZVOUS
    ) {
        println(&quot;Undelivered: $it&quot;)
    }
    launch {
        (1..3).forEach {
            channel.send(it)
            println(&quot;Send: $it&quot;)
        }

        channel.close()
    }

    println( channel.receive() )
    channel.cancel()
    println(&quot;end&quot;)
}

Send: 1
1
Undelivered: 2
end
```
3没有Undelivered我可以理解，因为onUndeliveredElement只有在Element进入了管道，但是没有被接收的时候触发，3没有机会进入管道。我不太理解2为什么能进入管道。我的管道capacity是RENDEZVOUS，只调用了一次receive，1进入了管道并且被接收了，2应该没有机会进入管道啊，为什么会触发onUndeliveredElement？</div>2022-06-22</li><br/>
</ul>