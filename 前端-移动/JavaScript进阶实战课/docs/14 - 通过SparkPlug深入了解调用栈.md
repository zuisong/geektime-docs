你好，我是石川。

在[第11讲](https://time.geekbang.org/column/article/580014)的时候，我们通过函数中的闭包了解了栈和堆这两种数据结构。在[12讲](https://time.geekbang.org/column/article/580442)中，我们通过递归了解了函数在调用栈中的循环执行。那么今天，我们再通过V8的Sparkplug编译器来深入的了解下JavaScript引擎中的调用栈，其中**栈帧（stack frame）**，**栈指针（stack pointer）和帧指针（frame pointer）的概念**。

![图片](https://static001.geekbang.org/resource/image/cb/a9/cb4080b43440b5a9b7fb2acbeb3d28a9.png?wh=1488x336)

这里，可能有不太了解V8的同学，我们来简单看一下Sparkplug的前世今生。最开始的时候啊，V8用的是一个相对比较快的Full-codegen编译器生成未优化的代码，然后通过Crankshaft这个及时（JIT）编译器对代码进行优化和反优化。但是随着更多人浏览网页的习惯从PC端转向移动端，性能问题变得更加重要了。而这个流水线既没能对ES6之前的，也没能对ES6之后版本的JS做到理想的优化。

![图片](https://static001.geekbang.org/resource/image/ff/7e/ff50ae5effb4cd6467a8fda8b8252a7e.png?wh=1838x516)

所以随之而来的，V8就引入了Ignition解释器和TurboFan的优化编译器以**移动优先**为目的的流水线。它最大的特点呢，就是通过Ignition最终生成**字节码**，之后再通过TurboFan生成优化后的代码，和做相关的反优化。

![图片](https://static001.geekbang.org/resource/image/70/a2/708801965f3459116da926829c6dd4a2.png?wh=1908x586)

可是这个时候，问题又来了，TurboFan和Crankshaft比起来，有时也有不足。所以为了解决这个问题，V8又创建了一个把Full-codegen，Crankshaft，Ignition和TurboFan整合起来的“全家桶”的流水线。这显然让问题显得更复杂了。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（1）<div>这节课对我来说太硬了  先放下   后面学学编译相关的知识</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/3b/7933fc58.jpg" width="30px"><span>魏志鹏</span> 👍（0） 💬（1）<div>看不懂汗 流汗</div>2022-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/69/30/d4db99b2.jpg" width="30px"><span>真嗣</span> 👍（1） 💬（0）<div>这节课过于硬核了...</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/07/99/2c12c56c.jpg" width="30px"><span>浩然</span> 👍（0） 💬（0）<div>汗流浃背了属于是</div>2024-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（0） 💬（0）<div>这个差的东西有点多呀</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>那个图的指针方向是不是错的？？？</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/14/2a08a0c8.jpg" width="30px"><span>度衡</span> 👍（0） 💬（0）<div>图里面的虚线&#39;反优化&#39;干啥呢？不应该只优化吗，怎么还反优化？</div>2023-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/3b/7933fc58.jpg" width="30px"><span>魏志鹏</span> 👍（0） 💬（0）<div>不懂啊</div>2022-11-13</li><br/>
</ul>