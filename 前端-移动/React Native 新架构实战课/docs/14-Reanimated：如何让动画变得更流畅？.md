你好，我是蒋宏伟。

今天我们来聊一聊React Native中动画的原理。在开始之前，我想请你思考一下：动画的本质到底是什么？

你可能知道，与真实世界中连续运动的事物不同，我们在手机、电脑、电影院的屏幕中看到的动画，实际是由一张张快速切换图片组成的。看动画时，我们的眼睛接收到的是一张张并不连续的静态图片，但我们的大脑把这些不连续的图片“想象”成了一系列连续事件，这就是动画的基本原理。

而手机动画要想流畅，一般而言需要保证每 1 秒渲染 60 帧的速度。这里的每一帧都是一张静态图片，也就是说 1 秒钟需要渲染出 60 个静态图片。这也意味着手机处理每一帧动画的耗时，需要保证在 16.6ms（=1000/60）以内，如果处理一帧的耗时超过 16.6ms ，就会掉帧。掉帧多了，我们的大脑就会感觉到动画中的不连续性，也就是常说的卡顿。

动画对渲染性能的要求很高。理论上，你可以使用 setInterval 每 16.6ms 执行一次 setState 改变状态，渲染新的视图，来实现动画。但实际上，setState 是一种耗时比较长的更新页面的方法，特别是在复杂页面、复杂交互的情况下，setInterval + setState 的方案并不适合用来实现动画。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/ba/5c/ca8f01b4.jpg" width="30px"><span>Wcly👺</span> 👍（1） 💬（1）<div>请问现在Reanimated支持RN新架构了吗？</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/e7/646bd9f1.jpg" width="30px"><span>worm</span> 👍（1） 💬（1）<div>老师您好，Reanimated 是如何把 JS 动画代码放到 UI 主线程的 JS 虚拟机中的呢？这部分是 C++ 实现的吧？有没有这部分的讲解材料或者实现的源码位置？</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/04/97267e91.jpg" width="30px"><span>happy</span> 👍（0） 💬（1）<div>老师，问个问题。被RN的动画抓狂，想实现一个ScrollView，内部有很长的列表，然后要实现一个切换scrollView的高度的动画，内容的不会动。整体就是高度变大变小的一个动画，感觉都很难实现。。。Animated提供的貌似都是transform之类的动画，没有设置height的这种动画吗？</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e3/23/b190b05d.jpg" width="30px"><span>*****</span> 👍（0） 💬（1）<div>有人碰到过 android debug 时 demo  crash吗？</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4c/fd/2e4cd48f.jpg" width="30px"><span>见字如晤</span> 👍（0） 💬（1）<div>我记得 react-native-gesture-handler 也是使用了 UI线程，都交给 UI 线程，UI 线程会不会也“不堪重负”？</div>2022-06-08</li><br/>
</ul>