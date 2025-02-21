你好，我是Mike。今天我们一起来学习如何用Rust进行GUI开发，我们用的GUI库是Slint。

GUI开发非常有趣，它能让你看到立竿见影的效果。这是为什么很多人学习编程喜欢从GUI开发开始（Web开发也是类似的道理）。而且GUI库还能用来做点小游戏什么的，非常有趣。而这两年，Rust生态中冒出来几个非常不错的GUI库，比如Slint、egui、Makepad等，今天我们就以Slint为例来讲讲。

学完这节课的内容，你就能使用Rust动手编写GUI程序了。

## Slint简介

Slint是一个轻量级的GUI框架，使用Rust实现，提供了Rust、CPP、JavaScript接口。对，你没看错，你也可以用JavaScript来调用Slint库做GUI开发。Slint的架构简洁优美，你可以在1～2天的时间里掌握它的理念和编程方法。

Slint的两位创始人之前是QT的核心开发者，因此从Slint上可以看到非常浓厚的QT（主要是QML）风格。QT是目前IT业界最流行的品质最好的开源跨平台GUI库，可以说Slint继承了QT的最佳实践，同时又与编程语言界的最佳实践Rust结合起来，得到了一个相当优美的GUI框架。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/ec/5508ec31.jpg" width="30px"><span>尤达</span> 👍（1） 💬（2）<div>slint依赖qt吗？cargo run报错：
= note: LINK : fatal error LNK1181: 无法打开输入文件“Qt5Cored.lib”
</div>2023-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/04/6a/6aa6c0ea.jpg" width="30px"><span>beshall</span> 👍（0） 💬（1）<div>老师，问个小问题，slint我编出来的程序打开有控制台窗口，这个怎么去除？</div>2024-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（0） 💬（1）<div>老师，代码用x86_64-pc-windows-gnu编译无法在Windows上运行，用msvc可以</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（1）<div>老师，你可以以最新版1.3.2来讲吗？</div>2023-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/5f/894761f8.jpg" width="30px"><span>十八哥</span> 👍（0） 💬（1）<div>Slint好像实现多窗口还是比较麻烦啊</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>请问老是，Rust 的 GUI 框架除了 Slint，还有其它推荐吗？</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/07/93/710c7ee2.jpg" width="30px"><span>不忘初心</span> 👍（0） 💬（1）<div>商用slint需要官方授权吗? 有无法律风险?</div>2023-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epvZCxlwoJpxVgG4zCsCpsmqfqxHic82ukC3LOloI5OG7IgVEmNos7gnSYnN9LCjxRCicQxyjVhlx6w/132" width="30px"><span>tianyu0901</span> 👍（0） 💬（1）<div>想了解下Slint许可证问题，什么情况下商用要付费？谢谢老师！</div>2023-12-20</li><br/>
</ul>