你好，我是杨文坚。

之前，我们课上所有Vue.js的代码，都是在浏览器里运行的。在浏览器里，编译后的Vue.js源码是纯粹的JavaScript代码，可以直接执行，并渲染出对应的视图和交互效果。

但在JavaScript代码还没通过&lt;script&gt;标签加载出来之前，整个页面一直是“白屏”，这个状态要等待JavaScript加载完，才能渲染出页面的功能视图。就像图中这样，浏览器控制台记录的白屏过程：

![图片](https://static001.geekbang.org/resource/image/78/a3/7869521f8b5a584c0c6b1707dbe377a3.png?wh=981x716)

为什么会有这个现象呢？

其实也很简单，因为图中渲染方式是“浏览器端渲染”，先等待页面的HTTP请求响应，返回页面的HTML，此时HTML还没有视图内容，只有JavaScript和CSS这些静态资源的引用，等到这些HTML里依赖的前端资源加载完毕后，最后执行JavaScript代码渲染出HTML结果，同时，对应CSS资源才会渲染样式效果。

如果请求页面依赖的资源文件体积太大，页面渲染就需要更长的等待时间，导致“白屏”时间等待太久，用户体验就很糟糕。

那么能不能无需等待JavaScript资源加载，就先渲染页面，来尽可能缩短“白屏”时间呢？

答案是有的，就是“服务端渲染”。究竟“浏览器渲染”和“服务端渲染”有什么渲染区别，带着这个问题，我们开始今天的学习。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rUqhSN2OVg5aHw10Hxib61nGv1SXxD6zowFl27oSm9Y6g8grRpTxCxwk7qg14a1TtmpzMTM2y810MnibBhwn75Mg/132" width="30px"><span>初烬</span> 👍（1） 💬（1）<div>类似于智慧城市这种有地图和数据模型渲染的场景可以采用SSR吗？</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（1）<div>SSR感觉也不一定一定能减少白屏时间。比如，如果SSR时服务端渲染较慢，页面也同样不能快速显示出来。另外，页面渲染的性能应该主要取取决于FP、FCP。</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-09-19</li><br/>
</ul>