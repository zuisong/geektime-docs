你好，我是月影。

上节课，我们从宏观上了解了各个图形系统在性能方面的优劣，以及影响性能的要素。实际上，想要解决性能问题，我们就必须要知道真正消耗性能的点，从而结合项目需求进行有针对的处理，否则性能优化就是纸上谈兵、空中楼阁。

所以这节课，我们就深入讨论一下影响Canvas绘图性能的因素，一起来分析几个不同类型的Canvas项目，找到的性能瓶颈以及对应的解决办法，从而学会对大部分Canvas项目进行性能优化。

我们知道，Canvas是指令式绘图系统，它有状态设置指令、绘图指令以及真正的绘图方法（fill和stroke）等各类API。通常情况下利用Canvas绘图，我们要先调用状态设置指令设置绘图状态，然后用绘图指令决定要绘制的图形，最后调用真正的fill()或stroke()方法将内容输出到画布上。

那结合上节课的实验我们知道，影响Canvas性能的两大因素分别是图形的数量和图形的大小。它们都会直接影响绘图指令，一个决定了绘图指令的多少，另一个决定了绘图指令的执行时间。通常来说，绘图指令越多、执行时间越长，渲染效率就越低，性能也就越差。

因此，我们想要对Canvas性能进行优化，最重要的就是优化渲染效率。常用的手段有5种，分别是优化Canvas指令、使用缓存、分层渲染、局部重绘和优化滤镜。此外，还有一种手段叫做**多线程渲染**，是用来优化非渲染的计算和交互方面导致的性能问题。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/32/ef42b1c1.jpg" width="30px"><span>嗨小二</span> 👍（5） 💬（1）<div>“因为不使用缓存直接绘制的是矢量图，而通过缓存 drawImage 绘制出的则是位图“，我怎么记得canvas绘制的都是位图，因为使用canvas绘制图形，放大后就会失真，为什么这里会说”不使用缓存直接绘制的是矢量图“，麻烦解释下</div>2020-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLqNxFYmldFiaT0180Po2TEbPuB3l0uZIqKb9sPWO97XicgDlaSIbkggq9yXv1vd1l7DXR4BjuqN76w/132" width="30px"><span>Mingzhang</span> 👍（5） 💬（2）<div>在屏幕上显示主 Canvas，利用 transferControlToOffscreen 将绘制交由 offScreen canvas 来绘制，而主 Canvas 负责监测鼠标在其上的 move 事件，然后将 event 的坐标 postMessage 给 Web Worker。请问月影这种方法可行吗？</div>2020-08-28</li><br/>
</ul>