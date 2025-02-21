在[上一篇文章](https://time.geekbang.org/column/article/132931)中我们介绍了页面中的事件和消息队列，知道了**浏览器页面是由消息队列和事件循环系统来驱动的**。

那在接下来的两篇文章中，我会通过**setTimeout**和**XMLHttpRequest**这两个WebAPI来介绍事件循环的应用。这两个WebAPI是两种不同类型的应用，比较典型，并且在JavaScript中的使用频率非常高。你可能觉得它们太简单、太基础，但有时候恰恰是基础简单的东西才最重要，了解它们是如何工作的会有助于你写出更加高效的前端代码。

本篇文章主要介绍的是**setTimeout**。其实说起setTimeout方法，从事开发的同学想必都不会陌生，它就是一个**定时器，用来指定某个函数在多少毫秒之后执行**。它会返回一个整数，表示定时器的编号，同时你还可以通过该编号来取消这个定时器。下面的示例代码就演示了定时器最基础的使用方式：

```
function showName(){
  console.log("极客时间")
}
var timerID = setTimeout(showName,200);
```

执行上述代码，输出的结果也很明显，通过setTimeout指定在200毫秒之后调用showName函数，并输出“极客时间”四个字。

简单了解了setTimeout的使用方法后，那接下来我们就来看看浏览器是如何实现定时器的，然后再介绍下定时器在使用过程中的一些注意事项。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（109） 💬（5）<div>我没有太理解这个异步延迟队列，既然是队列，但好像完全不符合先进先出的特点。在每次执行完任务队列中的一个任务之后都会去执行那些已经到期的延迟任务，这些延迟的任务具体是如何取出的呢。</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（60） 💬（3）<div>requestAnimationFrame 提供一个原生的API去执行动画的效果，它会在一帧（一般是16ms）间隔内根据选择浏览器情况去执行相关动作。
setTimeout是在特定的时间间隔去执行任务，不到时间间隔不会去执行，这样浏览器就没有办法去自动优化。

今日得到
浏览器的页面是通过消息队列和事件循环系统来驱动的。settimeout的函数会被加入到延迟消息队列中，
等到执行完Task任务之后就会执行延迟队列中的任务。然后分析几种场景下面的setimeout的执行方式。
1. 如果执行一个很耗时的任务，会影响延迟消息队列中任务的执行
2. 存在嵌套带调用时候，系统会设置最短时间间隔为4s（超过5层）
3. 未激活的页面，setTimeout最小时间间隔为1000ms
4. 延时执行时间的最大值2147483647，溢出会导致定时器立即执行
5. setTimeout设置回调函数this会是回调时候对应的this对象，可以使用箭头函数解决</div>2019-09-11</li><br/><li><img src="" width="30px"><span>moss</span> 👍（21） 💬（8）<div>这一节学习到了不少setTimeout的知识。不过关于消息队列我有不同的理解。
1. 关于任务优先级。whatwg标准里，“An event loop has one or more task queues”。消息队列其实不算是队列，因为有很多个task queue。“a task queue is a set of tasks”。每一个task queue才是一个队列。而对于每一个task queue里的task，其task source是一致的，或者说不同的task source会被推入到不同的task queue。就是规范里说的“every task source must be associated with a specific task queue”。而task sources都有哪些呢？比如DOM操作，UI事件，网络事件等。这个setTimout应该也算是一种task source吧？会放到专门的队列里。上一轮事件循环结束后，会先选择一个高优先级的task queue，然后取出task queue的第一个task，也因此而有了事件的优先级，老师将的延时队列我有点不太知道怎么融入我现有的知识体系。
2. “重新布局”是task吗？
老师说“重新布局”的事件会被放到消息队列。我的理解是task -&gt; microtask -&gt; update the rendering。当然不是每次循环都走渲染过程，因为每次循环都特别快不可能每次都走一次渲染，浏览器会遵循17ms一桢的原则走一次update the rendering，其中rAF也在此阶段执行，也是老师题目里rAF更流畅的原因。而重新布局也是在update the rendering阶段执行的，resize和onscroll都是在update the rendering阶段。标准里在update the rendering阶段，会有“run the resize steps”，“run the scroll steps”，这也是为啥scrolling自带节流效果最多17ms触发一次回调的原因，所以我认为连续事件（resize，scroll）既然都不是task -&gt; microtask -&gt; update the rendering里的task，而是update the rendering阶段，应该不会推送到某一个task queue才对。</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（12） 💬（6）<div>老师，你好。
请问微任务的执行是在延迟队列任务执行之前吗？</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/72/b7083420.jpg" width="30px"><span>Zzzrd</span> 👍（11） 💬（4）<div>看完还是很迷惑：
1. setTimeout是宏任务，宏任务应该放在消息队列中，文中说是放在延迟队列中，为什么？延迟队列和消息队列的区别是什么？
2. 延迟队列的任务是在当前宏任务执行完之后执行，微任务队列是在当前宏任务将要结束时执行对吗？
</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/dd/f2e79297.jpg" width="30px"><span>Djan Unchained</span> 👍（11） 💬（1）<div>requestAnimationFrame 也是在主线程上执行吗？如果当前任务执行时间过久，也会导致 requestAnimationFrame 被延后执行吗？</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（10） 💬（3）<div>1.执行延迟队列的任务，是一次循环只取出一个，还是检查只要时间到了，就执行？
2.微任务是在宏任务里的，是执行完一个宏任务，就去执行宏任务里面的微任务？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e6/06/2045daa5.jpg" width="30px"><span>Wlt</span> 👍（8） 💬（1）<div>老师，您好，延迟队列和消息队列是什么关系，怎么配合工作的？</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（6） 💬（1）<div>老师，您这里未激活的页面是什么意思？</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c6/e0/d2360a29.jpg" width="30px"><span>纪年</span> 👍（4） 💬（1）<div>如果 setTimeout 设置的延迟值大于 2147483647 毫秒时就会溢出，这导致定时器会被立即执行。
问题：这里的立即执行其实是不是相当于setTimeout（fun, 0）的意思？</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/08/36/401ce5e8.jpg" width="30px"><span>follaw</span> 👍（4） 💬（2）<div>系统如何筛选出到期的任务，如果有10000个呢，是循环一万次？这个系统内部怎么处理的呢？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/eb/c092f833.jpg" width="30px"><span>晓东</span> 👍（3） 💬（1）<div>老师，对processDelayTask这块有个疑惑。这里会把所有的到期任务都执行完才会开始下一个while循环吗？</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（3） 💬（1）<div>&#39;32bit 最大只能存放的数字是 2147483647 毫秒&#39;,最大能存放的数字不是2^32-1吗？4294967295，为什么是 2147483647 毫秒</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/b3/b6e1817a.jpg" width="30px"><span>趁你还年轻233</span> 👍（1） 💬（1）<div>虽然老师的英语发音很不标准···
但是技术原理讲得还是不错的。</div>2020-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLReFZCZAq532WRg5Bjabx1WX997t0EVnsrLYcBnsNZDaDjk5jHvKDfRibjwibVjqtlm7S3eBJkwPtg/132" width="30px"><span>海之蓝心</span> 👍（0） 💬（2）<div>老师，如果setInterval是怎么执行，是在延时队列还是微任务</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/28/17/2ee45db9.jpg" width="30px"><span>abson</span> 👍（0） 💬（2）<div>老师讲一下宏任务和微任务呗</div>2019-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（114） 💬（10）<div>使用 requestAnimationFrame 不需要设置具体的时间，由系统来决定回调函数的执行时间，requestAnimationFrame 里面的回调函数是在页面刷新之前执行，它跟着屏幕的刷新频率走，保证每个刷新间隔只执行一次，内如果页面未激活的话，requestAnimationFrame 也会停止渲染，这样既可以保证页面的流畅性，又能节省主线程执行函数的开销</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c8/e9/c7c5cbf5.jpg" width="30px"><span>l1shu</span> 👍（17） 💬（4）<div>为什么有些文章说渲染进程中有一个定时器线程用来计时的 到时间后会把回调函数塞到消息队列  而没有提到延迟队列这个说法  求老师解答</div>2019-10-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（16） 💬（4）<div>请问老师不是说settimeout属于宏任务不，不应该属于在上节课讲的消息队列中么
怎么这次有跑到延时队列中了呢，这两个队列有什么关系呢，延时队列也分宏任务和微任务？</div>2019-09-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo2GMhevabZrribH3tMFmIuLialgyyictMg1N3ZPPMjmGOdlZ3KXjzPBLWw2dhgR9UGtAXsmKaHCqicew/132" width="30px"><span>吴海燕</span> 👍（15） 💬（0）<div>老师有空的时候能否画一个包含延时队列和微任务，宏任务，消息队列关系运行图</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b3/2f/867b94d8.jpg" width="30px"><span>4!!</span> 👍（6） 💬（2）<div>传入requestAnimationFrame的回调并不会添加到消息队列或延迟队列中，传入requestAnimationFrame的回调会在页面下次重绘之前被调用，可以保证动画更实时准确。与setTimeout相比还有几个优点：1.当页面不可见或未被激活时，requestAnimationFrame的回调不会被调用；2.requestAnimationFrame的循环调用会有个自动节流处理，使得动画足够流畅，而函数不被过于频繁调用。</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（5） 💬（4）<div>评论好多说延迟队列得，其实就是一个定时器线程吧，定时器线程负责计时，到点了就把回掉push到消息队列中。</div>2020-04-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/deFp0jnQdc8uyhBsMdBAqiaL3T2SoE2QD5d9nw7V97QFsrmrAEgFiaQz3CHAWxwdehGR9m5uAgtf9VzDUUEStlOA/132" width="30px"><span>Geek_z46e7g</span> 👍（2） 💬（1）<div>怎么优化setTimeout 时间值不准的问题呢？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/dd/f2e79297.jpg" width="30px"><span>Djan Unchained</span> 👍（2） 💬（1）<div>setTimeout是在普通队列的当前一个任务结束之后，才去延迟队列查询并执行到期任务？还是在本轮事件循环的所有同步任务执行完？另外，怎么确定一轮事件循环是从哪儿到哪儿？</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/1f/97011d77.jpg" width="30px"><span>Debugger</span> 👍（2） 💬（0）<div>请问老师，系统每隔16ms去刷新页面，那刷新页面这个操作是不是也是消息队列中的一个任务</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/e7/227ee616.jpg" width="30px"><span>阿桐</span> 👍（2） 💬（0）<div>老师，假设在执行延迟队列中到期的任务时产生了新的到期任务如 setTimeout(foo, 0)，新的到期任务是在本次循环中执行还是推迟到下个循环中执行呢？

“如果 setTimeout 存在嵌套调用，那么系统会设置最短时间间隔为 4 毫秒”，基于此，我猜测新产生的到期任务不超过5个的话，会在本次循环中执行</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/01/aa7562e4.jpg" width="30px"><span>zy</span> 👍（1） 💬（0）<div>有问题希望老师回答，setTimeOut是放在所谓的延迟队列里还是单独一个定时器线程，到期了就把任务放回任务队列，还是老师说的单独的队列，每次执行完任务队列的一个任务就去延迟队列里找到到期的任务</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d6/25/a95a2064.jpg" width="30px"><span>luwei</span> 👍（1） 💬（1）<div>老是说的&quot;比如有五个定时的任务到期了,那么会分别把这个五个定时器的任务执行掉，再开始下次循环过程！&quot;这个是不是不太对呢？在node环境下是这样的，但是在浏览器环境下不是这样的。
在浏览器环境下的事件循环机制是：一个task执行完毕，然后再执行所有的micro-task，一次事件循环就结束了。然后继续循环....
```
while (true) {
  宏任务队列.shift()
  微任务队列全部任务()
}
```
在node环境下的事件循环机制是：
```
while (true) {
  loop.forEach((阶段) =&gt; {
    阶段全部任务()
    nextTick全部任务()
    microTask全部任务()
  })
  loop = loop.next
```

以下代码
```
setTimeout(() =&gt; {
  console.log(&#39;setTimeout 1&#39;)
  Promise.resolve().then(() =&gt; {
    console.log(&#39;promise 1&#39;)
  })
}, 0)
setTimeout(() =&gt; {
  console.log(&#39;setTimeout 2&#39;)
  Promise.resolve().then(() =&gt; {
    console.log(&#39;promise 2&#39;)
  })
}, 0)
```
在node环境下的打印结果是：
setTimeout 1
setTimeout 2
promise 1
promise 2
但在浏览器环境下是
setTimeout 1
promise 1
setTimeout 2
promise 2</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（1） 💬（0）<div>浏览器每秒执行60帧，大概一帧16ms，并且浏览器在每一帧都会去执行requestAnimationFrame函数，而setTimeout定时器存在不准时的情况，所以绘制动画选择requestAnimationFrame更好</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（1） 💬（1）<div>感觉浏览器得事件循环架构和node得架构很相似，都说渲染线程是单线程架构，但是也会有一些其它线程来帮助它执行一些任务，比如定时器线程，请求线程等等。这些在node里面都有对应得线程。不知道理解得对不对</div>2020-04-16</li><br/>
</ul>