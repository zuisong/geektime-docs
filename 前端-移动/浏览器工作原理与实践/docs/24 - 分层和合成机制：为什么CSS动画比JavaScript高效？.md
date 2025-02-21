在[上一篇文章](https://time.geekbang.org/column/article/140703)中我们分析了CSS和JavaScript是如何影响到DOM树生成的，今天我们继续沿着渲染流水线向下分析，来聊聊DOM树之后所发生的事情。

在前面[《05 | 渲染流程（上）：HTML、CSS和JavaScript文件，是如何变成页面的？》](https://time.geekbang.org/column/article/118205)文章中，我们介绍过DOM树生成之后，还要经历布局、分层、绘制、合成、显示等阶段后才能显示出漂亮的页面。

本文我们主要讲解渲染引擎的分层和合成机制，因为分层和合成机制代表了浏览器最为先进的合成技术，Chrome团队为了做到这一点，做了大量的优化工作。了解其工作原理，有助于拓宽你的视野，而且也有助于你更加深刻地理解CSS动画和JavaScript底层工作机制。

## 显示器是怎么显示图像的

每个显示器都有固定的刷新频率，通常是60HZ，也就是每秒更新60张图片，更新的图片都来自于显卡中一个叫**前缓冲区**的地方，显示器所做的任务很简单，就是每秒固定读取60次前缓冲区中的图像，并将读取的图像显示到显示器上。

**那么这里显卡做什么呢？**

显卡的职责就是合成新的图像，并将图像保存到**后缓冲区**中，一旦显卡把合成的图像写到后缓冲区，系统就会让后缓冲区和前缓冲区互换，这样就能保证显示器能读取到最新显卡合成的图像。通常情况下，显卡的更新频率和显示器的刷新频率是一致的。但有时候，在一些复杂的场景中，显卡处理一张图片的速度会变慢，这样就会造成视觉上的卡顿。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（100） 💬（9）<div>请问老师：既然css动画会跳过重绘阶段，则意味着合成阶段的绘制列表不会变化。但是最终得到的相邻两帧的位图是不一样的。那么在合成阶段，相同的绘制列表是如何绘制出不同的位图的？难道绘制列表是有状态的？还是绘制列表一次能绘制出多张位图？</div>2019-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7WkTI1IicbKvsPJng5vQh5qlrf1smbfl2zb7icHZfzcAk1k4lr8w8IDEAdrqq1NHW5XZMPXiaa1h7Jn1LGOWOCkIA/132" width="30px"><span>早起不吃虫</span> 👍（36） 💬（3）<div>这篇文章信息量巨大，需要很多的知识储备，老师能不能提供一些课外阅读帮助理解呢，谢谢</div>2019-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKf9xWMCV4ic5dsKyroQpGkYGZ32IPicVPVsF1TPENeTcspd6HhhaciaHCCmzeicaiaItZS3DahASFovJQ/132" width="30px"><span>bai</span> 👍（28） 💬（4）<div>关于css动画和js动画效率的问题应该有点武断了，will-change只是优化手段，使用js改变transform也能享受这个属性带来的优化。既然css动画和js动画都能享受这个优化，那就不能说明css动画比js动画效率高</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（23） 💬（12）<div>文中这段话中的“帧”应该改为“层”：
这段代码就是提前告诉渲染引擎 box 元素将要做几何变换和透明度变换操作，这时候渲染引擎会将该元素单独实现一帧，等这些变换发生时，渲染引擎会通过合成线程直接去处理变换，这些变换并没有涉及到主线程，这样就大大提升了渲染的效率。</div>2019-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/60/82/1d8c8c27.jpg" width="30px"><span>钓人的鱼</span> 👍（0） 💬（1）<div>希望老师就 重排、重绘、合成这一块弄个加餐，我自己测试出来感觉没什么变化，不知道为什么，也不知道怎么进行有针对性的分析</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/01/ac/0a84e410.jpg" width="30px"><span>Crack</span> 👍（0） 💬（1）<div>compositing layer中不会进行重绘重排这些操作吗？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/2e/332fee49.jpg" width="30px"><span>刘弥</span> 👍（20） 💬（2）<div>设置了 will-change :

- Layers 中会看到 document 下为每一个 .box 都创建了一个 layer，每个节点占用了 15KB 的内存。
- Performance 看不太懂，大致说一下直观感受
  - FPS 约 60、稳定
  - CPU 低、偶有突然增高
  - GPU 使用频率非常低
  - Chrome_ChildOThread 任务非常少
  - Compositor 任务密集

关闭 will-change：

- Layers 中就只剩下 document 层了。
- Performance 30s
  - FPS 约 60、稳定，但相对于开启 will-change不稳定
  - CPU 相对更低、偶有突然增高
  - GPU 使用频率很高
  - Raster 有 2 个光栅线程
  - Chrome_ChildOThread 任务密集
  - Compositor 任务非常密集

另外关于 Memory 中进行内存快照和 Heap，虽然第一次确实开启了 will-change 后更高，但多测试了几次发现差不多...</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（7） 💬（3）<div>题设的问题答案会不会很牵强？因为使用will-change渲染引擎会通过合成线程去处理元素的变化，所以CSS动画比JavaScript高效？不是应该从CSS动画的原理实现层面去解释吗，will-change只是让CSS动画更高效的一个API，就像JavaScript中的requestAnimationFrame也只是一个优化方案而已。</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a7/a4/da2e300b.jpg" width="30px"><span>风里有诗句</span> 👍（4） 💬（0）<div>老师，想听您讲解一下这道题目的分析</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（4） 💬（5）<div>老师，分成这个概念是不是和CSS里面的BFC这个概念相关?</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/f9/8221aac3.jpg" width="30px"><span>王妍</span> 👍（3） 💬（1）<div>Performance面板：
使用了will-change后帧率能达到60fps左右。不使用则30～50fps之间。
内存面板：
内存方面没看出明显区别。
分层面板：
使用will-change，每个box有一个单独的层。不使用则整个document是一层。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/4b/ab/220aa56c.jpg" width="30px"><span>时光逆行</span> 👍（3） 💬（0）<div>使用 will-change 掉帧情况几乎没有，内存占用比不用will-change会减少三分之二左右，这个属性给力</div>2020-01-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（2） 💬（0）<div>如果样式里面使用了will-change, 样式中涉及到的动画操作就会在合成线程中执行，将旋转后的图层和图层合成一张新的图片，这个就是最终输出的一帧，因为动画过程在合成线程中实现，没有占用主线程，因此渲染速度大大提高</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（2） 💬（2）<div>Performance：使用‘ will-change: transform, opacity;‘后，主线程均匀分布，密集棱状性；GPU均匀稀疏，平均500ms一条棱;rasterizer thread1 持续paint;Summery中GPU占用一小点其它98%以上都是idle;FPS,CPU都很稳定。去掉‘ will-change: transform, opacity;‘后，主线程均匀分布，密集棱状性；GPU密集棱状形；rasterizer thread1 和 thread2 持续paint；Summery中rendering和paint占用约20%时间；FPS，CPU略微不稳定。结论：will-change可以减轻GPU负担（为什么？合成线程不用GPU？），可以减轻rasterizer 线程负担（是因为减少重绘和重排吗），减少重绘和重排，动画的针率更稳定，cpu计算更少（为什么？计算分配给别的核了？）。。。。Layers: ：使用‘ will-change: transform, opacity;‘后，会合成新的层，不使用‘ will-change: transform, opacity;‘后，没有新的层。结论：不使用‘ will-change: transform, opacity;‘由于没有新的层生成，更改都会在一个层改变，所以会涉及到更多重绘和重排。Memory： 使用‘ will-change: transform, opacity;‘这个后System会更少，应该是占有系统内存会更少吧。那就尴尬了，will-change会有新图层，应该内存会增加。</div>2019-12-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLzSRrK59sydknSSYZdeTww3Cgib9Gy9N4BJGgSXMYdmVIxJYwDXPsLCIE68AbwTkgUct8J4iboAqicA/132" width="30px"><span>罗武钢</span> 👍（1） 💬（0）<div>太棒了，老师这套课程真得很受用</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/70/dafc8858.jpg" width="30px"><span>孟谦</span> 👍（1） 💬（0）<div>开启了will-change, 在performance &gt; setting 中开启 Advance Paint 之后, 点击某一个frame的时候可以, 可以看到. 渲染引擎为每一个标记了 CSS: will-change 开了新的layer, 用来叠加动画. 来减少重绘

&lt;a href=&quot;https:&#47;&#47;ibb.co&#47;4Y343hq&quot;&gt;&lt;img src=&quot;https:&#47;&#47;i.ibb.co&#47;SdGVGFj&#47;Clean-Shot-2020-12-13-at-14-37-02-2x.png&quot; alt=&quot;Clean-Shot-2020-12-13-at-14-37-02-2x&quot; border=&quot;0&quot;&gt;&lt;&#47;a&gt;</div>2020-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/8c/d91b01a6.jpg" width="30px"><span>zhangbao</span> 👍（1） 💬（1）<div>浏览器的 分层 依据是什么呢，就是如何决定哪些元素使用的是单独图层？我开始把 CSS 中的 层叠上下文 看成是一个图层，但观察发现好像并不是这样的。 </div>2020-04-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yicibWmBIDaSpBYI5wCBDQcYu6mxjvz3XZzBibxSNXFfqCS6OJOjvy2Nc2lyDicZfmneW9ZY4KbicA1sNgLktVSicgkw/132" width="30px"><span>老余</span> 👍（1） 💬（1）<div>加will-change：开启动画后整个过程帧率在59.9。图层由60个排列的变为1个重叠的60层。load时间在80ms左右，fp时间在200ms左右。内存方面为2m左右。
不加will-change：透明度变为0的时候帧率会变成40左右，随后增加到60。图层由60个排列。load时间在80ms左右，fp时间在100ms左右。内存方面为2m左右。</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/f5/1fa34f88.jpg" width="30px"><span>润曦</span> 👍（0） 💬（0）<div>当你给.box添加 will-change 后，浏览器会为这些元素创建独立的合成层。这意味着：

每个独立的合成层都是主线程计算的产物，主线程负责布局和样式计算。但通过创建独立层，这些层的渲染（transform、opacity 等变化）可以由合成器线程在不触发主线程布局的情况下完成。

合成层不在独立的线程上运行，但可以由不同的线程并行处理。例如，主线程处理布局和样式，而合成器线程处理图层的合成和硬件加速操作。</div>2024-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-12</li><br/><li><img src="" width="30px"><span>Geek_8d67bb</span> 👍（0） 💬（0）<div>“因为从层树开始，后续每个阶段都会多一个层结构，这些都需要额外的内存，所以你需要恰当地使用 will-change”这里应该说的是 隐式合成 的概念；</div>2023-10-19</li><br/><li><img src="" width="30px"><span>Geek_c84b62</span> 👍（0） 💬（0）<div>为什么没有设置will-change属性，在layers中看到也分层了</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/2c/e1/74c5e110.jpg" width="30px"><span>lzh</span> 👍（0） 💬（0）<div>你好请问文中这句话里的一帧是指一层吗：“这段代码就是提前告诉渲染引擎 box 元素将要做几何变换和透明度变换操作，这时候渲染引擎会将该元素单独实现一帧”</div>2022-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f2/30/5b677e8d.jpg" width="30px"><span>Yvan</span> 👍（0） 💬（0）<div>两个问题，评论区都已经提到了
1.帧改为层
2.will-change 是配合css使用还是配合js使用
另外，app夜间模式影响查看html代码
</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/81/bff52f91.jpg" width="30px"><span>1830</span> 👍（0） 💬（0）<div>老师。我有一些疑问希望老师可以解答：
        1. canvas动画和svg动画和传统css动画，js动画在执行性能上有何提升
        2. transform的动画是否都是基于合成执行的
        3. 普通图层的修改是不是会造成整个网页的重排重绘</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（0） 💬（0）<div> 补充一点：使用 will-change 会为每个 .box 生成一个图层。</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（0） 💬（0）<div>关于课后题，就我观察到的现象描述(Mac air 2019)：
1. 使用 will-change，帧率维持在 60FPS 之上，很稳定；GPU 很多空闲时间，压力小；内存占用3.6MB。
2. 不使用 will-change，帧率波动特别大，范围从 60FPS之上 ～ 30&#47;40FPS 之间，说明生成图片时很耗时；GPU 利用率很高，压力大；内存占用3.7MB。
PS：即使使用 will-change，帧率维持在 60FPS 之上，但是对于我的设备屏幕刷新率来说还是出现掉帧的情况；主线程一直都运行良好，未被阻塞。</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（0） 💬（0）<div>关于课后题，就我所观察到的现象描述：
1. 使用 will-change 属性时：帧率稳定在60FPS之上，很稳定；GPU存在很多空闲时间，说明压力小；</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/87/2c0c1c93.jpg" width="30px"><span>飞天</span> 👍（0） 💬（0）<div>老师，c ss媒体取消阻止，来优化性能怎么理解？举个例子？</div>2021-04-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLRPuYmxCsTaEroajHBWnBALgPW1PFYXviarfeCpvIGap5xZ3uo6XOyW6QA4ibvuyX0w3YsW0aYRf8w/132" width="30px"><span>Geek_2753cc</span> 👍（0） 💬（1）<div>请问老师：多个图层合成为一个图层是合成线程处理的，还是浏览器进程处理的呢？看前面的文章意思是浏览器处理的，合成线程是将多个图块合成为一个图层</div>2021-03-06</li><br/>
</ul>