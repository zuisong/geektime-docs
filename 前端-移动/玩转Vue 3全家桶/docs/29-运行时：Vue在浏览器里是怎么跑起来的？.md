你好，我是大圣。

上一讲我们学习了Vue响应式的大致原理，响应式就是可以把普通的JavaScript对象包裹成响应式对象，这样，我们对对象做的修改，响应式都能够监听到，并且执行effect内部注册的函数来执行数据修改之后的效果。

那今天我就跟你聊一下Vue在浏览器里是如何运行的，照例我们还是对着Vue 3的源码来学习，不过源码复杂，为了帮助你理解主要逻辑，我会直接把源码简化再演示，当然怎么简化源码的一些小技巧也会顺便分享给你。

好了废话不多说，我们马上开始。前端框架需要处理的最核心的两个流程，就是首次渲染和数据更新后的渲染。先来看首次渲染的源码。演示代码会用Vue 3的实际代码，你也可以在 [weiyouyi](https://github.com/shengxinjing/weiyouyi/blob/main/src/runtime-core/apiCreateApp.js#L4) 项目中看到我们课程的mini版本代码。

## 首次渲染

我们知道，想要启动一个Vue项目，只需要从Vue中引入createApp，传入App组件，并且调用createApp返回的App实例的mount方法，就实现了项目的启动。这个时候Vue也完成了首次渲染，代码逻辑如下：

![](https://static001.geekbang.org/resource/image/39/7c/3974d85351462f5190363869a39b1f7c.png?wh=1622x786)

所以createApp就是项目的初始化渲染入口。

但是这段简单的代码是怎么完成初始化渲染的呢？我们可以在Vue中的runtime-dom中看到createApp的定义，你可以打开 [GitHub链接](https://github.com/vuejs/vue-next/blob/master/packages/runtime-dom/src/index.ts#L66)查看。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/f7/0b/b01f1d68.jpg" width="30px"><span>百事可乐</span> 👍（1） 💬（2）<div>萌新表示看不懂</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/d8/96/dcf52430.jpg" width="30px"><span>关关君</span> 👍（1） 💬（1）<div>hydrate函数是不实现SSR的？
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Hydration_(web_development)</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/aa/a8/6ca767ca.jpg" width="30px"><span>openbilibili</span> 👍（0） 💬（1）<div>weiyouyi运行时的代码 应该怎么样去测试呢？</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c8/09/b34b1473.jpg" width="30px"><span>鱼腩</span> 👍（23） 💬（5）<div>果然涉及源码解释的视乎视频更适合——所见即所得。
而看文档听语音，对照源码，难上加难</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/0d/cd/791d0f5e.jpg" width="30px"><span>Mr_shaojun</span> 👍（5） 💬（0）<div>自己先看一遍代码， 然后再来看课程，感觉收获非常大</div>2022-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/67/7b/c1c78245.jpg" width="30px"><span>大果子</span> 👍（3） 💬（0）<div>大佬，求画图软件？</div>2022-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/d5/b08a27ed.jpg" width="30px"><span>灵感_idea</span> 👍（1） 💬（0）<div>这个东西，感觉还是肢解着讲更合适，从简单到复杂，然后慢慢丰富起来，再用上技巧，不过这样以来，如此篇幅的一节课是不够的，哈哈。</div>2023-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/0d/21bf48eb.jpg" width="30px"><span>NULL</span> 👍（0） 💬（0）<div>hydrate: 供水的。</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/2e/6f7b0e7c.jpg" width="30px"><span>哎呦先生</span> 👍（0） 💬（0）<div>大圣老师，patch时传递了虚拟dom，虚拟dom是在哪一步解析生成的呢？虚拟dom解析的流程是什么？</div>2022-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f3/98/f80e8bc0.jpg" width="30px"><span>Hansen</span> 👍（0） 💬（0）<div>确实有点枯燥，可以跟着老师简版瞧一瞧！</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b9/ae/1962e54f.jpg" width="30px"><span>造梦者</span> 👍（0） 💬（1）<div>老师，请问可以用createApp来创建一个通知组件吗，和用h函数创建有什么区别？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/09/7f/23bb32bd.jpg" width="30px"><span>pepsi</span> 👍（0） 💬（0）<div>流程梳理的太棒了，比自己debug强很多，赞的大圣老师</div>2022-01-12</li><br/>
</ul>