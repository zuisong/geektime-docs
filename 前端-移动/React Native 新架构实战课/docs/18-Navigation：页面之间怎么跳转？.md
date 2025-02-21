你好，我是蒋宏伟。今天我要给你介绍的是导航。

导航是用来管理页面之间的链接的。你平时用的 App，比如微信、抖音、京东，都有很多个页面，这些页面之间会有跳转、返回、切换等链接操作，这些链接操作就是导航。我们开发 React Native App 也一样，需要使用导航来链接各个页面。

尽管导航是开发 React Native App 必不可少的工具之一，但 React Native 框架并未将其内置，需要开发者自己进行集成。在 2018 年之前，业内用得比较多的导航是 React Native Navigation，在 2018 年之后大家用得更多的是 React Navigation。它们的名字很相似，不过你可千万不要搞混了，**目前官方推荐的、主流的导航是 React Navigation，而不是 React Native Navigation。**

你可以看一下，[React Navigation](https://reactnavigation.org/)、[React Native Navigation](https://wix.github.io/react-native-navigation/docs/before-you-start/) 和 React Native 三个库的 npm 下载量：

![图片](https://static001.geekbang.org/resource/image/ab/71/ab4b904ec634cacd2c7ffe7341788771.png?wh=1920x764)

这张图中，蓝色线条代表的是 React Navigation，绿色线条代表的是 React Native Navigation，橙色线条代表的是 React Native。从三个库的下载量中你可以看出，目前 React Navigation 导航已经成为主流，把 React Native Navigation 导航远远地甩在了后面，并且每十次 React Native 框架的下载，有七到八次都会下载 React Navigation 导航，由此可见，React Navigation 确实是非常受欢迎的。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erje3495m1a2Go8c801c8OwtEzaHicomaEfcIal5jQSH2I1QrfSgBKoZzsGcRiaIv2Fj5ibNTCj3c0Mg/132" width="30px"><span>潇潇暮雨</span> 👍（3） 💬（1）<div>老师，可以讲一下原生页面与RN页面相互跳转吗</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/76/6f/2f9312c8.jpg" width="30px"><span>007</span> 👍（1） 💬（1）<div>老师，能讲一下Modal页面。还有自定义导航动画么？</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f3/20/d0ec3eda.jpg" width="30px"><span>维筱</span> 👍（0） 💬（1）<div>老师，求画图软件</div>2023-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/64/9e/b8892546.jpg" width="30px"><span>追风</span> 👍（0） 💬（1）<div>方便讲解一下react-native中路由鉴权的方案吗？</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3c/fa/b88b8b4e.jpg" width="30px"><span>郭浩</span> 👍（0） 💬（0）<div>如何解决两个Tab之间的滑动冲突问题？</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/fb/d7/6de93467.jpg" width="30px"><span>章鱼哥</span> 👍（0） 💬（0）<div>老师您好，我想请教一下TS项目 { navigation }和{ route }的类型该如何写？</div>2022-10-19</li><br/><li><img src="" width="30px"><span>Geek_27a13a</span> 👍（0） 💬（0）<div>老师，您好
react-native 新搭建的0.69.0项目怎么兼容  react-native-screens（3.13.1）这个问题应该怎么解决呢？</div>2022-06-26</li><br/><li><img src="" width="30px"><span>Geek_27a13a</span> 👍（0） 💬（0）<div>老师，您好
React Native 项目0.69.0版本下,安装react-native-screens（3.13.1）报错。提示react-native-screens版本不支持，这个怎么解决呢？？</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（0）<div>老师，请问如果很多页面使用 react navigation 关联起来，是否会有性能问题 ？</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（0）<div>老师的一节课，我学习花了一周💧
试着动手做了示例和作业，用 react navigation drawer 把整节示例串起来了。代码 https:&#47;&#47;bit.ly&#47;3O9xk3U

</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（0）<div>老师，关于导航前套里的这点
---
第二个问题更严重，如果想从 Home 的 Page1 页面跳转到 Message 的 Page3 下面，用户必须点开过 Message 标签页，不然就会出现报错。
---
使用 navigation.navigate(&#39;Message&#39;, {screen: &#39;Page3&#39;}); 代替 navigation.navigate(&#39;Page3&#39;); 是不会报错的。</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cc/1d/3c0272a1.jpg" width="30px"><span>abc🙂</span> 👍（0） 💬（0）<div>一直纠结tab的最佳实践路由，官方文档也不给一个建议~今天学习到了</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bb/2e/70d25615.jpg" width="30px"><span>风之化身</span> 👍（0） 💬（0）<div>感觉v6版的 react-navigation 的TS类型系统做的也很好，可以讲讲最佳实践。我们团队用的 v3 版本：1、类型系统不太满意；2、navigation.setParams 对引用类型修改会影响到上一个页面传递过来的</div>2022-05-09</li><br/>
</ul>