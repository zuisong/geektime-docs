你好，我是戴铭。今天，我来和你聊聊iOS原生、大前端和Flutter分别是怎么渲染的。

用户在使用 App 时，界面的设计、流畅程度是最直接的体验。为此，苹果公司提供了各个层级的库，比如 SwiftUI、UIKit、Core Animation、Core Graphic、OpenGL ，以方便App界面的开发。

说起来，即使你不了解这些库的实现原理，也可以通过它们提供的易用接口上手去开发 App，特别是 SwiftUI 大大简化了界面的开发，也确实能够解决大部分问题。但是，一旦遇到性能问题，完全依靠搜索获得的不完整的、拼凑来的知识，大概率只能解一时之需，要想系统地解决问题，还是要知道这些库的实现原理。

而这些与界面相关的库，背后的知识其实就是渲染。接下来，我就和你说说渲染的原理。

## 渲染原理

我们看到的 App 界面，都是由 CPU 和 GPU 共同计算处理的。

CPU 内部流水线结构拥有并行计算能力，一般用于显示内容的计算。而 GPU的并行计算能力更强，能够通过计算将图形结果显示在屏幕像素中。内存中的图形数据，经过转换显示到屏幕上的这个过程，就是渲染。而负责执行这个过程的，就是GPU。

渲染的过程中，GPU需要处理屏幕上的每一个像素点，并保证这些像素点的更新是流畅的，这就对 GPU 的并行计算能力要求非常高。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/15/9b/a988aea2.jpg" width="30px"><span>🚲 刘大欢</span> 👍（4） 💬（0）<div>斗胆尝试回答一下楼上同学的问题 屏幕开始渲染的时候 cpu会做包括视图创建 布局计算 图层绘制 图像解码等一系列事情 等构件好图层树 渲染层拿到并反序列化后成为渲染树调用openGL操作gpu指令时 其实在序列化完成 这个事务已经完成了 剩下的就是屏幕上绘制这一帧的显示了 你说的改变位置应该是下帧的事情了 不可能在在中间还有穿插一次提交这么一说吧 </div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/af/b8/458866d3.jpg" width="30px"><span>Bo</span> 👍（2） 💬（0）<div>好像没有人讨论课后作业，暂且放上自己搜索资料后得到的回答：
Google起初使用Webkit作为Chrome浏览器的引擎，后来以Webkit引擎为基础创造了Blink引擎，它针对Webkit内核，去掉了几十万行不相关的复杂代码，让效率更高。然后针对未来的网页格式，做了进一步优化，和效率提升的处理。
所以Chrome的Blink内核可以看成是Webkit的精简高效强化版。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（0）<div>能答疑吗 我想问</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/af/b8/458866d3.jpg" width="30px"><span>Bo</span> 👍（0） 💬（0）<div>Chrome渲染引擎Blink：https:&#47;&#47;www.chromium.org&#47;blink&#47;</div>2022-02-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epa5lcfaxArmZI1upDsVh9zmFdefuN79Lkox5fEVMhd5ANEfWtHStbONwvKKc1sL6tHX9iaFpNEyDQ/132" width="30px"><span>Geek_54260c</span> 👍（0） 💬（2）<div>原生每一帧的渲染不也是通过ipc传递给render server的嘛？core animation 和render server 也是独立进程，为什么这块会比webview快呢？</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/4b/328b1c57.jpg" width="30px"><span>Schrödinger</span> 👍（0） 💬（1）<div>原生渲染那部分感觉写得有些问题</div>2020-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rWMGIQG1z13nekorr9I4PY1w7rlskssf949IQ24SvIewpM7mmZoH2QEZ2aKHu5tkmicGQ7KTGrN9vFYhrDsdp9w/132" width="30px"><span>Geek_9dbcb4</span> 👍（0） 💬（1）<div>flutter是有UI局部刷新的功能，来提高渲染效率。iOS的渲染，没有这方面的优化吧？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/e1/fa7fd9f3.jpg" width="30px"><span>方金峰</span> 👍（0） 💬（1）<div>老师，问一下啊！iOS的图层树经过序列化发送到渲染服务进程，渲染服务进程反序列化得到图层树，然后生成渲染树，这里如果当前只改动了一个图层的位置，app当前进程也会将整颗图层树序列化发送到渲染服务进程？如果是整颗图层树这样设计的好处是什么，因为进程和进程之间的通讯，数据传输是一个制约效率的因素，这里能否请老师帮忙解答下，或是指明下哪里有这方面材料，可以研究下。麻烦了啊！</div>2019-07-02</li><br/>
</ul>