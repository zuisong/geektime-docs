你好，我是月影。

今天，我们来聊一个相对轻松的话题，它不会有太多的代码，也不会有什么必须要掌握的理论知识。不过这个话题对你理解可视化，了解渲染引擎也是有帮助的。因为我今天要聊的话题是SpriteJS，这个我亲自设计和实现的图形渲染引擎的版本迭代和演进。

SpriteJS是从2017年下半年开始设计的，到今天已经快三年了，它的大版本也从1.0升级到了3.0。那么它为什么会被设计出来？它有什么特点？1.0、2.0、3.0版本之间有什么区别，未来会不会有4.0甚至5.0？别着急，听我一一道来。

## SpriteJS v1.x （2017年~2018年）

我们把时间调回到2017年下半年，当时我还在360奇舞团。奇舞团是360技术中台的前端团队，主要负责Web开发，包括PC端和移动端的产品的前端开发，比较少涉及可视化的内容。不过，虽然团队以支持传统Web开发为主，但是也支持过一部分可视化项目，比如一些toB系统的后台图表展现。那个时候，我们团队正要开始尝试探索可视化的方向。

如果你读过专栏的预习篇，你应该知道，要实现可视化图表，我们用图表库或者数据驱动框架都能够实现，前者使用起来简单，而后者更加灵活。当时，奇舞团的小伙伴更多是使用数据驱动框架[D3.js](https://d3js.org/)来实现可视化图表的。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/85/f5/1d2ca277.jpg" width="30px"><span>点滴</span> 👍（3） 💬（1）<div>使用 JavaScript Core 和 JS Bindings技术，除了跨平台，脱离浏览器，在其他方面有什么提升？目前很多跨平台的框架到后期都会面临性能与native开发性能差距。这块如何考量</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/b9/f88c01ca.jpg" width="30px"><span>赤道</span> 👍（2） 💬（1）<div>与threejs对比一下，4.0与之优劣势？</div>2021-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/82/e8/3c0c767a.jpg" width="30px"><span>LJT</span> 👍（0） 💬（0）<div>这个4版本不就是flutter么？</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/d7/a31f6526.jpg" width="30px"><span>ryannz</span> 👍（0） 💬（0）<div>另外能讲讲GPGPu就更好了</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/d7/a31f6526.jpg" width="30px"><span>ryannz</span> 👍（0） 💬（0）<div>v4的代码在有放出来嘛？很感兴趣。要从native做起，兼容web感觉也挺难的。
- native用c++实现？还是rust？？
- skia的wasm体积问题怎么解决？
- 文字和布局放弃掉挺可惜的，如果做成插件挺好的
- 文字和布局其实在native都有现成的解决方案可以借用，但是不一定能迁移到web
- native对体积倒是不太敏感
- 怎么看webgpu呢？
- skia的性能对可视化足够了吗
</div>2022-02-17</li><br/><li><img src="" width="30px"><span>蓝海</span> 👍（0） 💬（0）<div>想做智慧城市，3D楼群和城市设备的相关展示。目前正在做技术选型，请问使用SpriteJS是否试用。有没有相关推荐，谢谢！</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/01/313652c2.jpg" width="30px"><span>馒头爱学习</span> 👍（0） 💬（0）<div>聆听牛人的思路，非常受用！</div>2021-04-16</li><br/>
</ul>