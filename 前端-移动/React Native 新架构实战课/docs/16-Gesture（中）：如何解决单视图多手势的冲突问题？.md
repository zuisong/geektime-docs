你好，我是蒋宏伟。

通过上节课对轻按手势和拖拽动效这两个基础手势案例的学习，相信你现在已经能够完成一些基本手势需求的开发了。今天这节课，我们就再进一步，聊下怎么解决更进阶的手势问题。

在手势基础的学习中，我们给到的手势案例都是围绕着一个视图、一个手势展开的，处理起来很简单。但在真实的工作中，情况会更加复杂。比如说，我们会有稍微难一点的情况，也就是一个视图同时存在多个手势。还有更复杂的，就是同时有多个视图、多个手势，并且这些视图和手势环环相扣。

当然你也不用担心，这两种复杂的情况，我们的 Gesture 手势库都提供了相关的解决方案。不过俗语也有说，“一口吃不成大胖子。”所以今天这一讲，我们先来聊聊一个视图多个手势如何处理，下一讲再聊聊多个视图、多个手势如何处理。

但在展开讲解手势冲突问题之前，我需要带你补全 Gesture 手势的一些进阶知识。

## 手势进阶

我们要研究多个手势冲突的问题，大体上得遵循这样的流程：

- 首先你得知道 Gesture 手势库都能识别哪些手势；
- 然后手势实际是一系列连续的动作，而这一系列动作大致可以分为几个阶段，比如开始、进行中、完成和中途取消，Gesture 手势库又提供了哪些手势回调来识别手势的不同阶段；
- 最后，不同阶段的回调又都能提供什么参数，能让开发者来使用。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/89/ba/009ee13c.jpg" width="30px"><span>霍霍</span> 👍（0） 💬（1）<div>老师讲的很好，要是能有一些demo代码实例，让我们身临其境学习就更好了</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b9/27/b6d05c82.jpg" width="30px"><span>lcl</span> 👍（0） 💬（0）<div>老师文中的示意图是用什么画的，好好看</div>2024-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJxhkqxtWKQeYrYlVYphlicHXW5KmHAvibx6hmice4NTvmn60ZEfTpLp3480umVEquqPdMfwOnecj6Aw/132" width="30px"><span>焦糖大瓜子</span> 👍（0） 💬（0）<div>点个赞</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>再给老师点个赞。</div>2022-06-08</li><br/>
</ul>