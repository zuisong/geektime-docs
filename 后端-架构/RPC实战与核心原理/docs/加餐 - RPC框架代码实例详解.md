你好，我是何小锋，好久不见！咱们专栏结课有段时间了，这期间我和编辑冬青一起对整个课程做了复盘，也认真挨个逐字看了结课问卷中的反馈，其中呼声最高的是“想看RPC代码实例”，今天我就带着你的期待来了。

还记得我在[\[结束语\]](https://time.geekbang.org/column/article/226573)提到过，我在写这个专栏之前，把公司内部我负责的RPC框架重新写了一遍。口说无凭，现在这个RPC框架已经[开源](https://github.com/joyrpc/joyrpc)，接受你的检阅。

下面我就针对这套代码做一个详细的解析，希望能帮你串联已学的知识点，实战演练，有所收获。

## RPC框架整体结构

首先说我们RPC框架的整体架构，这里请你回想下[\[第 07 讲\]](https://time.geekbang.org/column/article/207137)，在这一讲中我讲解了如何设计一个灵活的RPC框架，其关键点就是插件化，我们可以利用插件体系来提高RPC的扩展性，使其成为一个微内核架构，如下图所示：

![](https://static001.geekbang.org/resource/image/a3/a6/a3688580dccd3053fac8c0178cef4ba6.jpg?wh=3084%2A2183 "插件化RPC")

这里我们可以看到，我们将RPC框架大体分为了四层，分别是入口层、集群层、协议层和传输层，而这四层中分别包含了一系列的插件，而在实际的RPC框架中插件会更多。在我所开源的RPC框架中就超过了50个插件，其中涉及到的代码量也是相当大的，下面我就通过**服务端启动流程、调用端启动流程、RPC调用流程**这三大流程来将RPC框架的核心模块以及核心类串联起来，理解了这三大流程会对你阅读代码有非常大的帮助。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/51/9d5cfadd.jpg" width="30px"><span>好运来</span> 👍（5） 💬（1）<div>太干货了，准备以项目为中心，重新过一遍前面的文章。</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/60/4888d3dc.jpg" width="30px"><span>HIYO</span> 👍（1） 💬（1）<div>赞，期待结合JoyRPC讲解对之前技术点技术选型的思考，比如说咱们的流量隔离实现方式是什么，分组与统一入口是如何平衡的？我了解到netty有过回退版本的过程，是因为AIO在性能上并没有比NIO有明显的提高，还导致代码过于复杂。那咱们选择纯异步和纯插件化又是基于什么样的考虑呢？</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（13） 💬（0）<div> 好早以前就购买课程了，但当时没有更完。所以就没追，其实我的学习方式跟追剧是一样的。更完后在一段时间内看完，思路会比较完整。利用五一假期把整个课程看完了，重新理解了rpc框架各个组件的设计原理，收获很大。后续根据这些原理再去看一遍dubbo的源码，会有更深的认识。感谢老师👨‍🏫</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（6） 💬（0）<div>感谢老师的加餐，把专栏的内容根据项目结合起来，一起看，收获肯定会更大</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（5） 💬（1）<div>喜欢这个加餐，JSF也终于开源了，不知道是不是还是熟悉了味道😄</div>2020-05-17</li><br/><li><img src="" width="30px"><span>Geek_09d497</span> 👍（2） 💬（0）<div>花了5个小时，终于看完了。对rpc和微服务有了一个宏观的认识，后面的路就是看具体的源码了。</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/05/c8/2f849dfb.jpg" width="30px"><span>山顶的洞</span> 👍（2） 💬（0）<div>假期也出货，赞</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/40/23/deccfba5.jpg" width="30px"><span>WLB</span> 👍（0） 💬（0）<div>为什么这个我运行不了，谁能教教我
</div>2023-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/e8/aa60f7f1.jpg" width="30px"><span>赵存金</span> 👍（0） 💬（0）<div>干货满满。</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>感谢老师的加餐</div>2021-02-02</li><br/>
</ul>