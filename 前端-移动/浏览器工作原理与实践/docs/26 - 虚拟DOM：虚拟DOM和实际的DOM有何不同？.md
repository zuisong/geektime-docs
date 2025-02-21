虚拟DOM是最近非常火的技术，两大著名前端框架React和Vue都使用了虚拟DOM，所以我觉得非常有必要结合浏览器的工作机制对虚拟DOM进行一次分析。当然了，React和Vue框架本身所蕴含的知识点非常多，而且也不是我们专栏的重点，所以在这里我们还是把重心聚焦在虚拟DOM上。

在本文我们会先聊聊DOM的一些缺陷，然后在此基础上介绍虚拟DOM是如何解决这些缺陷的，最后再站在双缓存和MVC的视角来聊聊虚拟DOM。理解了这些会让你对目前的前端框架有一个更加底层的认识，这也有助于你更好地理解这些前端框架。

## DOM的缺陷

通过前面一系列文章的学习，你对DOM的生成过程应该已经有了比较深刻的理解，并且也知道了通过JavaScript操纵DOM是会影响到整个渲染流水线的。另外，DOM还提供了一组JavaScript接口用来遍历或者修改节点，这套接口包含了getElementById、removeChild、appendChild等方法。

比如，我们可以调用`document.body.appendChild(node)`往body节点上添加一个元素，调用该API之后会引发一系列的连锁反应。首先渲染引擎会将node节点添加到body节点之上，然后触发样式计算、布局、绘制、栅格化、合成等任务，我们把这一过程称为**重排**。除了重排之外，还有可能引起**重绘**或者**合成**操作，形象地理解就是“**牵一发而动全身**”。另外，对于DOM的不当操作还有可能引发**强制同步布局**和**布局抖动**的问题，这些操作都会大大降低渲染效率。因此，对于DOM的操作我们时刻都需要非常小心谨慎。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（37） 💬（6）<div>虚拟DOM的出现根本意义上不是为了解决 js 频繁操作DOM而引起的性能问题，因为如果通过 js 来操作DOM，那么无论用什么方式，多少动作都需要执行，虚拟DOM并没有减少操作。虚拟DOM的意义在于改变了开发模式，之前是需要手动管理DOM，数据和DOM操作糅合在一起，开发效率低下；之后是使用框架&#47;库自动管理DOM，数据驱动DOM的更新，只需要关注数据的变化即可。但是这会遇到一个问题，就是当数据改变时，框架需要更新全部的DOM吗？显然这是不可接受的，js 操作DOM的代价很高，所以当数据变化时并不直接对DOM进行更新，而是先对应在虚拟DOM上，通过与之前的虚拟DOM进行比较，确定需要更新的变动，然后在对应在真实的DOM上。</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（31） 💬（13）<div>1. 频繁更新dom引起的性能问题
2. 将真实DOM和js操作解耦，减少js操作dom复杂性。
老师答疑的时候可以介绍下react的fiber吗？感觉李老师的文章通俗易懂，很受益（网上文章分析参差不齐的）
今日总结：
为什么会出现虚拟DOM？javascript直接操作DOM可能会引起重排 重绘等操作（强制同步布局和布局抖动）引起性能问题。这是需要一个中间层来优化dom的操作（批量更新dom，优化更新dom细节），虚拟DOM就呼之欲出了。之后从双缓存和MVC模型的角度来解析了虚拟DOM。
</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/33/f9/50b76abe.jpg" width="30px"><span>AMIR</span> 👍（15） 💬（17）<div>老师，我用js文件里面操作dom原生操作，不也是这个js文件执行完，也就是所有的dom原生操作都做完，才统一渲染页面么？我觉得虚拟dom只是对比innerHtml更有优势，并且屏蔽了原生的操作，可以使更多人来使用数据驱动视图，而不必要去操作麻烦的原生操作，就从效率来说，虚拟dom肯定比原生的差啊，虚拟dom对比完了，不还是得调用原生的操作么？他至少比原生多了diff算法的时间，麻烦老师解答下，提了挺多问题了，老师有空看一下</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ec/68/06d59613.jpg" width="30px"><span>柒月</span> 👍（10） 💬（5）<div>主要还是解决频繁操作DOM引起页面响应慢的问题。
虚拟DOM就是一个JS对象，通过diff算法比较新老DOM树的差别，来达到最小化局部更新的目的。
其本质不过是用JS的运算性能的消耗来换取操作DOM的性能消耗。</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/2e/332fee49.jpg" width="30px"><span>刘弥</span> 👍（8） 💬（1）<div>说虚拟 DOM 解决的问题，那一定应该是和 DOM 存在什么问题来进行比较吧？

DOM 存在的问题：

- 对 DOM 进行操作时往往会引起重排、重绘
- 编写不当的代码操作 DOM 还会引起强制布局和布局抖动
- 复杂的页面往往会频繁的操作 DOM

虚拟 DOM 对此的优势：

虚拟 DOM 最终当然也会产生重排、重绘等操作，但是由于虚拟 DOM 对 真实 DOM 的预解析和变化搜集的双缓存机制，使得操作 DOM 的频率会明显的降低。
操作 DOM 的频率降低同样会使得强制同步布局和布局抖动得到一定的优化。

这个是我对于虚拟 DOM 的优势的理解，如果有什么不对的，还望指正。
</div>2020-02-13</li><br/><li><img src="" width="30px"><span>😎</span> 👍（6） 💬（0）<div>似乎大家都没有提到一点，虚拟dom可以实现跨端，如React Native
</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/44/26ac883e.jpg" width="30px"><span>桃翁</span> 👍（6） 💬（7）<div>老师，为什么 React 的 Fiber 不用 async&#47;await 来实现呢？</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/22/d6/9378f4d5.jpg" width="30px"><span>隔夜果酱</span> 👍（5） 💬（1）<div>李老师后面会考虑React源码类的专栏么?
网上的视频和文章很多都流于表面,或者生搬硬套的进行解释,看的让人头大.
如果李老师有精力和兴趣的话,希望可以开专栏为我们指点迷津呀.</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（4） 💬（1）<div>老师，文中的虚拟Dom收集到足够的变化是什么意思？会不会导致页面的响应变慢？</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（3） 💬（0）<div>读完文章之后，感觉虚拟DOM技术和DOM碎片（createDocumentFragment）很像，都是提供缓存的策略。</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/97/919f5e6b.jpg" width="30px"><span>Geek_gaoqin</span> 👍（3） 💬（0）<div>老师你的课程太好了，再开个课程讲react angular等框架的知识点吧，以及结合这个浏览器原理再讲讲框架原理和源码分析吧</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/a0/c97ce2fe.jpg" width="30px"><span>coco</span> 👍（2） 💬（0）<div>希望李老师开设vue专栏，很喜欢李老师的专栏，买了不少的，还是最喜欢您的专栏，通俗易懂</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/39/08/09055b47.jpg" width="30px"><span>淡</span> 👍（2） 💬（7）<div>老师，你好。我有两个小疑问：
1.就是说到新算法的时候，使用协程说让出主线程。前面课程里说道线程同一时刻只能有一个协程能执行，这里说的协程如果还属于主线程的话，我理解的依然会卡主线程，如果不属于相当于新开线程来执行diff算法。请问我是不是哪里理解错了？
2.就是分析React更新dom，第一步说监听DOM的变化，后面又说React变化的虚拟DOM同步更新到实际DOM，触发DOM的更新。我理解第一步应该是监听虚拟DOM变更函数调用，但是这样由于示例图又不一样了，如果是实际DOM的变化都已经变化了就没后面什么事了吧？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（2） 💬（0）<div>基于 React 和 Redux 构建 MVC 模型的配图中，控制器是不是不能直接改变视图？因为 redux 模型是单向数据流吧</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/b6/76/3d68a0ae.jpg" width="30px"><span>skyline</span> 👍（1） 💬（0）<div>文中&quot;在虚拟 DOM 收集到足够的改变时，再把这些变化一次性应用到真实的 DOM 上。&quot;这句话我不赞同，虚拟DOM最中也是将对比出不的不同点一次一次调用原生API更新DOM，并不能实现“一次性”应用到真实DOM

虚拟DOM从来不是为了解决性能问题，而是现代框架为实现mvvm，解放开发人员生产力做的一种折中的方案。

个人观点</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/99/95/1e332315.jpg" width="30px"><span>Geek_2014ce</span> 👍（1） 💬（0）<div>不太赞同老师说的 “频繁更新DOM引起的性能问题”
- 根据前面的微任务章节可知，就算是频繁操作DOM，真正的进行页面的更新也是在微任务里面一次更新的，并不会频繁触发渲染流水线。(除非调用强制布局相关的接口)。
- 我也自己写DEMO去测了，for循环里面向一个父元素不断添加子节点。查看performance会发现只有脚本完全执行完了触发了一次渲染流水线。
不知道我理解是否有问题，希望老师能给予解答。(&gt;_&lt;)
</div>2021-04-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yyibGRYCArsUNBfCAEAibua09Yb9D5AdO8TkCmXymhAepibqmlz0hzg06ggBLxyvXicnjqFVGr7zYF0rQoZ0aXCBAg/132" width="30px"><span>james</span> 👍（1） 💬（0）<div>由于真实的DOM结构是非常庞大且复杂的，因此可以采用js对象来描述真实的DOM结构，这就是虚拟DOM，并且当数据更新后，需要更新视图，根据新的数据生成一个新的虚拟DOM，然后基于新的虚拟DOM，跟旧的虚拟DOM进行比较，找出更新的部分，改造旧的虚拟DOM，再讲虚拟DOM转化成真实DOM，再一次性插入到视图节点中。这样子通过避免重复操作DOM元素，牺牲js的运算消耗，但是在如今高CPU的计算机处理性能下，这点消耗可以忽略，从而提高视图渲染的性能</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（1） 💬（3）<div>频繁DOM操作是非常消耗浏览器性能的，虚拟DOM核心还是将批量DOM操作后的变化一次性更新到浏览器。</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/fa/720f57fa.jpg" width="30px"><span>zer0fire</span> 👍（0） 💬（0）<div>新浪没看出什么问题，不过打开极客时间这个页面发现一个 1.1MB 的 chunk.js</div>2024-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/8f/1c/e2a5c91e.jpg" width="30px"><span>卷不动了</span> 👍（0） 💬（0）<div>我理解只要不在页面上插入删除节点或者对dom元素的几何信息进行改变就不会触发重排重绘，就算我使用虚拟dom我在虚拟dom中增加节点依然会触发重排才对,而且我如果在页面上只想改变dom元素中某个文字，我直接操作dom明显来的更快,使用虚拟dom反而要去经过对比计算,效率明显不如前者,虚拟dom主要是提高开发效率的同时提供过得去的性能,在最初,改变dom中的内容需要手动获取dom对元素更改,使用虚拟dom只需要关心数据变化,这样使得开发效率有所提升,并且虚拟dom还可以应用在移动端,如果追求性能虚拟dom应该不是最优选择</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3d/4d/dc2da0a2.jpg" width="30px"><span>乐意</span> 👍（0） 💬（0）<div>在vue中使用document.getElementbyId获得的是虚拟dom还是真实dom呢</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/9a/46/7eb8fea9.jpg" width="30px"><span>ronny</span> 👍（0） 💬（0）<div>老师有兴趣讲讲angular源码吗</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/81/bff52f91.jpg" width="30px"><span>1830</span> 👍（0） 💬（0）<div>MVVM的虚拟dom解决的问题不在于性能，综合而言它也不一定有渲染的性能优势。之所以用最重要的是工作的效率，代码的简洁性易维护，这点我请教过大厂很多大佬，其实结合老师前面说的渲染流程也能想到</div>2021-06-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er04ibpNSFnyiaPrWjPU96q7AZzgAU1Jc1MVwVvfTrqRaR2AWYJ6Z2KXohT8fS5dKSAqa31SNmicJ1mg/132" width="30px"><span>General</span> 👍（0） 💬（1）<div>React +Redux 的数据流向是单向的，最后一张图有点迷惑，action&#47;reducer 到 view 那个箭头是不画反了？</div>2021-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/47/395438c4.jpg" width="30px"><span>das parfum</span> 👍（0） 💬（0）<div>取法乎上</div>2021-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/c0/20b4a205.jpg" width="30px"><span>啊哈哈</span> 👍（0） 💬（0）<div>1. 复杂项目（页面）下，通过虚拟DOM的生成、比对，再批量更新，比频繁操作真实DOM性能消耗更小。当然，虚拟DOM的生成比对都是占内存的，但是相比频发更新，不停的占用主线程，阻塞视图渲染，时间要快，这里实际上是用空间换取时间。
2. 虚拟DOM可以实现跨平台。</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f8/8a/f7e7fd54.jpg" width="30px"><span>君自兰芳</span> 👍（0） 💬（1）<div>“在虚拟 DOM 收集到足够的改变时，再把这些变化一次性应用到真实的 DOM 上”

有个疑问，这里的“足够的改变”，具体是足够到什么程度？按时间来算？还是按照累积的量来算？</div>2020-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pR5LYM0SnUWZialA11lAlcnHH9XUH04cqZ6AibDu2xVJic80o2oJG2jIHPiaiakOqkw4jP5Bo0IAYnLMYHyicztLfnlA/132" width="30px"><span>Geek_3b5e3c</span> 👍（0） 💬（0）<div>MVC 那张图是不是有点出入，View 和 Model也可以通信的吧，如果不能通信的话不就是MVP架构了？</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>请教老师：新数据发生时，新的虚拟dom树是整个复制旧的dom树？还是只复制修改了的dom树？</div>2020-06-26</li><br/>
</ul>