你好，我是石川。

今天我们来看下图（graph）这种数据结构，图是一个抽象化的网络结构模型。你可能会问有什么算法应用会用到图这种结构吗？其实很多，像我们经常用的社交媒体（比如国内的微博、微信，或者国外的脸书、领英）中的社交图谱，都可以通过图来表达。另外，图也能用来表达现实世界中的路网、空网以及虚拟的通信网络。

图在JS引擎的编译器中作用是非常大的。如果说整个V8的编译器TurboFan都基于图也毫不夸张。我们既可以通过图这种数据结构，对编译的原理有更深的理解，在我们了解编译的同时，又可以对相关的数据结构和算法有更深入的认识。

## 图的结构

下面我们先来看一下图的结构吧。图就是由边（edge）连接的节点（vertax），任何一个二分的关系都可以通过图来表示。

![图片](https://static001.geekbang.org/resource/image/dd/7f/dd449c673188afaf677a5d127f3ce07f.png?wh=1346x732)

那我们说的TurboFan是怎么利用图来做编译的呢？在开始前，我们先来了解下编译流程和中间代码。

## 编译流程：中间代码

IR，也就是中间代码（Intermediate Representation，有时也称 Intermediate Code，IC）。从概念层面看，IR可以分为HIR（Higher IR）、MIR（Middle IR）和LIR（Lower IR），这几种高、中、低的中间代码的形式。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（1） 💬（0）<div>phi 指令 太抽象，没看懂他的具体意思</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/1c/7899bab4.jpg" width="30px"><span>南城</span> 👍（0） 💬（0）<div>硬，啃不动，然后买了一个编译的书，老子就不信了！</div>2023-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（2）<div>过分了，这文章。。</div>2023-03-21</li><br/>
</ul>