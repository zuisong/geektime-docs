在[上篇文章](https://time.geekbang.org/column/article/118205)中，我们介绍了渲染流水线中的**DOM生成、样式计算**和**布局**三个阶段，那今天我们接着讲解渲染流水线后面的阶段。

这里还是先简单回顾下上节前三个阶段的主要内容：在HTML页面内容被提交给渲染引擎之后，渲染引擎首先将HTML解析为浏览器可以理解的DOM；然后根据CSS样式表，计算出DOM树所有节点的样式；接着又计算每个元素的几何坐标位置，并将这些信息保存在布局树中。

## 分层

现在我们有了布局树，而且每个元素的具体位置信息都计算出来了，那么接下来是不是就要开始着手绘制页面了？

答案依然是否定的。

因为页面中有很多复杂的效果，如一些复杂的3D变换、页面滚动，或者使用z-indexing做z轴排序等，为了更加方便地实现这些效果，**渲染引擎还需要为特定的节点生成专用的图层，并生成一棵对应的图层树**（LayerTree）。如果你熟悉PS，相信你会很容易理解图层的概念，正是这些图层叠加在一起构成了最终的页面图像。

要想直观地理解什么是图层，你可以打开Chrome的“开发者工具”，选择“Layers”标签，就可以可视化页面的分层情况，如下图所示：

![](https://static001.geekbang.org/resource/image/e2/c0/e2c917edf5119cddfbec9481372f8fc0.png?wh=1142%2A1075)

渲染引擎给页面多图层示意图

从上图可以看出，渲染引擎给页面分了很多图层，这些图层按照一定顺序叠加在一起，就形成了最终的页面，你可以参考下图：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（212） 💬（16）<div>减少重排重绘, 方法很多：
1. 使用 class 操作样式，而不是频繁操作 style
2. 避免使用 table 布局
3. 批量dom 操作，例如 createDocumentFragment，或者使用框架，例如 React
4. Debounce window resize 事件
5. 对 dom 属性的读写要分离 
6. will-change: transform 做优化</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（124） 💬（1）<div>关于浏览器渲染的知识点讲的很细致，我想问下，关于浏览器的渲染细节的知识老师是从哪里学到的？，是通过研究源码学习的吗？有没有一些好的学习资料或者学习方法推荐？能否专门出一篇“授人以渔”的文章，谢谢！</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/0c/03bd4b4e.jpg" width="30px"><span>朙</span> 👍（63） 💬（6）<div>渲染进程里的帧的概念是什么样子的呢？一个page是一帧吗</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（42） 💬（3）<div>减少重排重绘，相当于少了渲染进程的主线程和非主线程的很多计算和操作，能够加快web的展示。
1 触发repaint reflow的操作尽量放在一起，比如改变dom高度和设置margin分开写，可能会出发两次重排
2 通过虚拟dom层计算出操作总得差异，一起提交给浏览器。之前还用过createdocumentfragment来汇总append的dom,来减少触发重排重绘次数。
</div>2019-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXKSvfaeicog2Ficx4W3pNeA1KRLOS7iaFy2uoxCDoYpGkGnP6KPGecKia6Dr3MtCkNGpHxAzmTMd0LA/132" width="30px"><span>Geek_East</span> 👍（29） 💬（8）<div>渲染流程的最后，应该是浏览器进程将Compositor Frame发送到GPU, GPU进行显示吧？</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/e9/1f95e422.jpg" width="30px"><span>杨陆伟</span> 👍（25） 💬（1）<div>最后的一段话非常经典，赞！大道至简，这真是做软件该秉持的原则，如果实现功能时感受到复杂和无序，那一定是那里错了</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（19） 💬（6）<div>请教下老师，canvas的渲染流程是什么样的呢？它不涉及dom，也就不涉及dom树、样式计算、布局、分层，canvas的绘制过程也是在渲染进程中进行的吗？</div>2019-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJS0jwYKhjm1hq96go05J4R7XDd5FFXXaoyIfX9TgoI3mLURAu2ET72SvYGM2iaET7IV3WDvMibAVfw/132" width="30px"><span>tokey</span> 👍（11） 💬（4）<div>老师您好！
我想问以下两个问题：
问题1：手机端开发，body 被内容撑开了，超过一屏，在滑动的过程中会不会触发重排，为什么？
问题2：如果 body 高度设置了100%</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2a/bc/03c2c8cf.jpg" width="30px"><span>不存在的</span> 👍（9） 💬（1）<div>什么叫既不要布局也不要绘制的属性呢?</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d1/ee/96fcadbc.jpg" width="30px"><span>Warrior</span> 👍（5） 💬（1）<div>重排是否只在当前分层中，会不会影响其他分层的重排？</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/f7/abb7bfe3.jpg" width="30px"><span>帅气小熊猫</span> 👍（4） 💬（1）<div>这里的合成线程属于哪个进程？浏览器进程是指主进程吗？前面进程线程那块没有啊</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3c/c1/30a7efa3.jpg" width="30px"><span>frankh</span> 👍（3） 💬（2）<div>transform为什么可以避免重排和重绘啊</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/32/1d/d4e03718.jpg" width="30px"><span>Rahim</span> 👍（2） 💬（3）<div>http:&#47;&#47;www.chromium.org&#47;developers&#47;design-documents&#47;gpu-accelerated-compositing-in-chrome?spm=taofed.bloginfo.blog.1.19585ac8aQLUrh
你好，源码中到RenderLayer跟教程中到图层树是同一个意思吗？那后续GraphicsLayer是什么意思</div>2019-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/eb/c092f833.jpg" width="30px"><span>晓东</span> 👍（1） 💬（1）<div>老师，关于视口附近的图块会优先生成位图这块有点疑惑。因为当所有图块都栅格化后，才会通知浏览器进程去合成图层并显示，那么视口图块优先栅格化的意义体现在哪里？</div>2019-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/7b/bd2d9d0c.jpg" width="30px"><span>(ಡωಡ)hahaha</span> 👍（1） 💬（1）<div>老师，你好，我想请教一下，渲染进程中，有哪些线程，以及各线程的作用，可以讲解一下吗</div>2019-11-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJS0jwYKhjm1hq96go05J4R7XDd5FFXXaoyIfX9TgoI3mLURAu2ET72SvYGM2iaET7IV3WDvMibAVfw/132" width="30px"><span>tokey</span> 👍（1） 💬（1）<div>老师的课程可以加个浏览器中的事件循环和js的事件机智么？</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（1） 💬（2）<div>重排和重绘都是渲染进程的主线程中进行的，减少这类操作可以减少主线程的资源占用，提高主线程绘制效率。在编写js时尽量减少dom操作或合并dom操作，dom操作需要重新生成dom树，如果影响布局就需要重新生成布局树，再重新生成分层树，再进行绘制。ps：感觉生成个页面好复杂呀，另外，以前从没注意过chrome开发者工具还有个Layers标签，chrome开发者工具真是一堆宝呀。</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/d9/83d1346c.jpg" width="30px"><span>Lx</span> 👍（0） 💬（2）<div>老师，简单页面，只有一个div。我想问下是会产生一个分层吗？光栅化的过程会利用gpu吗？因为我记得gpu处理3d</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/8d/d381883a.jpg" width="30px"><span>漠</span> 👍（0） 💬（4）<div>老师，为什么我的devtool里面没有layer这个面板</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b4/61/1db459e5.jpg" width="30px"><span>哎姆哦剋</span> 👍（0） 💬（2）<div>请问老师，我改变了宽高，是不是只对同一图层有影响，其他图层不会重排？</div>2019-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZbPA5RQ2mjUjd571jUXUcBCE7lY5vSMibWn8D5S4PzDZMaAhRPdnRBqYbVOBTJibhJg/132" width="30px"><span>ヾ(◍°∇°◍)ﾉﾞ</span> 👍（0） 💬（1）<div>减少重排重绘可以减少gpu等的调用频次，gpu调用本身开销不小</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/f4/a40453e7.jpg" width="30px"><span>man-moonth</span> 👍（0） 💬（2）<div>请教老师，因为重绘(paint)的输入是图层树，“重绘省去了布局和分层阶段”是否可以理解为：因为修改绘制属性并不改变元素的布局计算，所以重绘渲染的布局(layout)、分层(layer)两个阶段处理得非常快以至于可以忽略不计。</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/1d/c7586cfc.jpg" width="30px"><span>Snail</span> 👍（223） 💬（4）<div>浏览器工作流程『从输入 URL 到页面展示』学习笔记

导航

用户输入

1. 用户在地址栏按下回车，检查输入（关键字 or 符合 URL 规则），组装完整 URL；
2. 回车前，当前页面执行 onbeforeunload 事件；
3. 浏览器进入加载状态。

URL 请求

1. 浏览器进程通过 IPC 把 URL 请求发送至网络进程；
2. 查找资源缓存（有效期内）；
3. DNS 解析（查询 DNS 缓存）；
4. 进入 TCP 队列（单个域名 TCP 连接数量限制）；
5. 创建 TCP 连接（三次握手）；
6. HTTPS 建立 TLS 连接（client hello, server hello, pre-master key 生成『对话密钥』）；
7. 发送 HTTP 请求（请求行[方法、URL、协议]、请求头 Cookie 等、请求体 POST）；
8. 接受请求（响应行[协议、状态码、状态消息]、响应头、响应体等）；
   - 状态码 301 &#47; 302，根据响应头中的 Location 重定向；
   - 状态码 200，根据响应头中的 Content-Type 决定如何响应（下载文件、加载资源、渲染 HTML）。

准备渲染进程

1. 根据是否同一站点（相同的协议和根域名），决定是否复用渲染进程。

提交文档

1. 浏览器进程接受到网路进程的响应头数据，向渲染进程发送『提交文档』消息；
2. 渲染进程收到『提交文档』消息后，与网络进程建立传输数据『管道』；
3. 传输完成后，渲染进程返回『确认提交』消息给浏览器进程；
4. 浏览器接受『确认提交』消息后，移除旧文档、更新界面、地址栏，导航历史状态等；
5. 此时标识浏览器加载状态的小圆圈，从此前 URL 网络请求时的逆时针选择，即将变成顺时针旋转（进入渲染阶段）。

渲染

渲染流水线

构建 DOM 树

1. 输入：HTML 文档；
2. 处理：HTML 解析器解析；
3. 输出：DOM 数据解构。

样式计算

1. 输入：CSS 文本；
2. 处理：属性值标准化，每个节点具体样式（继承、层叠）；
3. 输出：styleSheets(CSSOM)。

布局(DOM 树中元素的计划位置)

1. DOM &amp; CSSOM 合并成渲染树；
2. 布局树（DOM 树中的可见元素）；
3. 布局计算。

分层

1. 特定节点生成专用图层，生成一棵图层树（层叠上下文、Clip，类似 PhotoShop 里的图层）；
2. 拥有层叠上下文属性（明确定位属性、透明属性、CSS 滤镜、z-index 等）的元素会创建单独图层；
3. 没有图层的 DOM 节点属于父节点图层；
4. 需要剪裁的地方也会创建图层。

绘制指令

1. 输入：图层树；
2. 渲染引擎对图层树中每个图层进行绘制；
3. 拆分成绘制指令，生成绘制列表，提交到合成线程；
4. 输出：绘制列表。

分块

1. 合成线程会将较大、较长的图层（一屏显示不完，大部分不在视口内）划分为图块（tile, 256*256, 512*512）。

光栅化（栅格化）

1. 在光栅化线程池中，将视口附近的图块优先生成位图（栅格化执行该操作）；
2. 快速栅格化：GPU 加速，生成位图（GPU 进程）。

合成绘制

1. 绘制图块命令——DrawQuad，提交给浏览器进程；
2. 浏览器进程的 viz 组件，根据DrawQuad命令，绘制在屏幕上。

相关概念

重排

1. 更新了元素的几何属性（如宽、高、边距）；
2. 触发重新布局，解析之后的一系列子阶段；
3. 更新完成的渲染流水线，开销最大。

重绘

1. 更新元素的绘制属性（元素的颜色、背景色、边框等）；
2. 布局阶段不会执行（无几何位置变换），直接进入绘制阶段。

合成

1. 直接进入合成阶段（例如CSS 的 transform 动画）；
2. 直接执行合成阶段，开销最小。
</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/32/0d/9ffc70dd.jpg" width="30px"><span>番茄</span> 👍（13） 💬（1）<div>最后一部分，合成和显示讲的太模糊的，不是很理解。</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（10） 💬（2）<div>老师，你好，我有几个问题一直都很很困惑，也没找到答案，希望老师能解惑一下，感谢！
1、图层、图块与BFC有什么区别联系吗？为什么BFC内元素的变动不会对BFC外的元素产生任何影响？是因为BFC会产生一个独立的图层或图块，渲染的时候只用重新渲染这一个图层或图块吗？BFC的原理是什么？
2、在划分图层的时候，每个图层都会生成一系列的绘制指令，而在划分图块的时候，一个图块可能包含多个图层，一个图层也可能分成多个图块，那么在将图块绘制成位图的时候，是如何执行绘制指令的？需要将绘制指令再划分到不同的图块中吗？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/e9/072b33b9.jpg" width="30px"><span>splm</span> 👍（8） 💬（4）<div>在GPU进程完成栅格化，并把结果保存在GPU内存中，此时的结果仍然保存在独立进程中。那么从渲染进程的合成线程发送Drawquad命令到浏览器主线程调用Viz组件，主进程是在什么时候拿到之前存在GPU内存中的位图结果的？是Viz主动去GPU内存获取这部分结果进行合成的吗？这里没太看懂。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/31/72/817e88b4.jpg" width="30px"><span>Fred 鱼</span> 👍（6） 💬（1）<div>对于使用transform的元素，要事先定义好will-change:transform; ，才能避免layout 和paint。</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（6） 💬（7）<div>老师文中说需要剪裁（clip）的地方也会被创建为图层，但是我复制了老师的代码后，发现需要剪裁的地方并没有单独的被创建为图层，难道是最新版本的谷歌浏览器改了渲染规则？
我的浏览器版本是 76.0.3809.100（正式版本） （64 位）
</div>2019-08-26</li><br/><li><img src="" width="30px"><span>Geek_a4a510</span> 👍（5） 💬（0）<div>Chrome原版文档里说合成compositing是分割成layer的过程，而不是图块。这个更能解释transform只调用合成线程，因为一个layer挪来挪去就行了

Compositing is a technique to separate parts of a page into layers, rasterize them separately, and composite as a page in a separate thread called compositor thread.

https:&#47;&#47;developer.chrome.com&#47;blog&#47;inside-browser-part3&#47;</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（4） 💬（0）<div>“栅格化过程都会使用 GPU 来加速生成”，请问下老师，如果用户的电脑没有GPU，栅格化就使用CPU吗</div>2020-05-19</li><br/>
</ul>