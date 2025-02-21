你好，我是蒋宏伟。

前一节课，我们讲解了手势进阶的一些内容，也分析了如何解决单视图多手势冲突的问题，但这个 Demo 其实挺基础的。今天我们要再深入一点，看一个稍微复杂点的案例，就是 Android 的回弹下拉刷新。

在Gesture的第一篇中我提到过，实现 Android 回弹下拉刷新的难点在于Android 的 ScrollView 组件就没有滚动回弹属性 bounces。而 iOS 的 ScrollView 组件是有滚动回弹属性 bounces 的，而且是默认开启的。

在 Android 回弹下拉刷新案例中，会用到 Gesture 上中下三篇中的所有知识点，包括如何将手势库 Gesture 和动画库 Reanimated 搭配一起使用，如何解决单视图多手势的冲突问题，如何解决多视图多手势的冲突问题。

今天这一讲，一方面我会重点和你介绍如何解决多视图多手势的冲突问题，另一方面我会把 Gesture 上中下三篇的内容给你串起来，帮你实现 Android 回弹下拉刷新的效果。

## Android 回弹下拉刷新

在真实的业务开发中，实现双端下拉刷新的正确逻辑是：**iOS 基于 bounces 实现，Android 基于手势实现**。不过，为了方便，我在写 Demo 的时候，直接把 iOS 的 bounces 效果关了，双端统一使用手势实现，省去了 if else 的代码，这样你看代码会容易一些。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/cc/1d/3c0272a1.jpg" width="30px"><span>abc🙂</span> 👍（2） 💬（1）<div>有没有可能跟RecyclerListView组件结合起来，实现andaroid高性能的长列表弹性滚动</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/1c/db1d53e2.jpg" width="30px"><span>风星舞</span> 👍（0） 💬（1）<div>请问GitHub仓库中运行android时的这个 yarn install-android-hermes 命令是什么作用？</div>2022-05-07</li><br/><li><img src="" width="30px"><span>Geek_84d08b</span> 👍（0） 💬（0）<div>请问：tapGesture onTouchesMove 中 refreshY.value 获取到的值一直是 -200，这个是什么原因呢？</div>2024-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e3/23/b190b05d.jpg" width="30px"><span>*****</span> 👍（0） 💬（0）<div>现在国内的大厂有使用这手势和动画库吗</div>2024-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/b5/777ba52b.jpg" width="30px"><span>侯同学</span> 👍（0） 💬（0）<div>蒋老师好

处理单视图多手势冲突的 Race Exclusive Simultaneous 与处理多视图多手势的 simultaneousWithExternalGesture requireExternalGestureToFail 有什么关系、区别 ？
只是处理单视图多手势冲突的 API 是在组件的角度，处理多视图多手势冲突的 API 是在手势的角度吗 ？
特别是 Simultaneous 与 simultaneousWithExternalGesture 感觉很像

另外上面代码中的 panGesture 调用 simultaneousWithExternalGesture 时为什么还要传入 scrollGesture tapGesture 
外部组件为什么还要响应这两个事件，虽然我测试不传确实不行</div>2023-09-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLib4GiaK4KB3UvnnzIkMAD4QzKBAkOzdntPwsb8RX1xjHYgr2w0GLWhmoPdwy3iby3zOHbeTBR2DgRQ/132" width="30px"><span>songyq</span> 👍（0） 💬（0）<div>Gesture 手势库解决手势冲突的方案 确定不是抄的apple的手势代理么？</div>2022-08-17</li><br/>
</ul>