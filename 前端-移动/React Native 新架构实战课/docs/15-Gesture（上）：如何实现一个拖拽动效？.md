你好，我是蒋宏伟。

我刚开始做 React Native 开发的时候，曾经被手势问题困扰过好几次。

第一次，我想在 Android 上实现类似 iOS 的下拉刷新效果。你可能知道，iOS 的 ScrollView 组件是有回弹属性 [bounces](https://reactnative.cn/docs/scrollview) 的。当开启回弹效果时，ScrollView 的内容区顶到头还可以继续往下拉，但 Android 的 ScrollView 组件就没有 bounces 属性，实现不了这种带回弹的下拉刷新效果。

第二次，我是想实现类似抖音评论区的手势动效。这个手势动效在上下方向存在三个手势，分别是最外层视频区域的上下切换动画、评论框的上下拖拽动画和评论内容的上下滚动动画。这种多视图、多手势的动效，本身就非常复杂，而且当时 React Native 框架自带的手势动画模块的能力太弱，也实现不了。

第三次，我想实现类似淘宝首页的手势动效。淘宝首页头部区域是由轮播图、金刚区等组成的固定内容区域，底部区域是由多 Tab 、多长列表组成的可左右切换、可上下滚动的区域，实现难度非常高。

我提到的这三个手势动效的需求，都需要手势和动画搭配在一起才能实现。

但当初我用的是 React Native 的 0.44 版本，因为社区的Gesture 手势库 [react-native-gesture-handler](https://docs.swmansion.com/react-native-gesture-handler/) 和Reanimated 动画库 [react-native-reanimated](https://docs.swmansion.com/) 都还不太成熟，所以我选择了 React Native 框架自带的手势模块 [PanResponder](https://reactnative.cn/docs/panresponder) 和动画模块 [Animated](https://reactnative.cn/docs/animated) 进行开发。但是仅仅只是如何解决手势冲突这个问题，就把我拦住了，只能降级处理。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/83/52/e6d46fb3.jpg" width="30px"><span>Hadwz</span> 👍（0） 💬（1）<div>老师，用Gesture 手势库和 Reanimated，实现在ScrollView里上下拖拽一个元素，并在元素到达列表的顶部&#47;底部的时候，滚动ScrollView，让列表和元素同时移动，有什么实现思路吗？</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/24/bfd04641.jpg" width="30px"><span>ZouLe</span> 👍（0） 💬（1）<div>上 Reanimated v2 和 Gesture v2 就不能用原来的浏览器debug模式开发了，这个转换跨度还是蛮大的 😄</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bb/2e/70d25615.jpg" width="30px"><span>风之化身</span> 👍（3） 💬（0）<div>讲的蛮好，建议录个小视频看下最终效果会更直观点～</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e3/23/b190b05d.jpg" width="30px"><span>*****</span> 👍（0） 💬（0）<div>Gesture.Pan 手指离开屏幕后，下次在拖动就无效了</div>2024-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（0）<div>手势这三节课，学习了好几周 💦
试着做了作业一 https:&#47;&#47;bit.ly&#47;3HXMCae ，使用了 react-native-gesture-handler 的 Swipeable 组件完成的。尝试着自己用 Reanimated 写，发现对我这新手难度大了写 😂</div>2022-06-29</li><br/>
</ul>