在[上一篇文章](https://time.geekbang.org/column/article/140140)中我们详细介绍了DOM的生成过程，并结合具体例子分析了JavaScript是如何阻塞DOM生成的。那本文我们就继续深入聊聊渲染流水线中的CSS。因为CSS是页面中非常重要的资源，它决定了页面最终显示出来的效果，并影响着用户对整个网站的第一体验。所以，搞清楚浏览器中的CSS是怎么工作的很有必要，只有理解了CSS是如何工作的，你才能更加深刻地理解如何去优化页面。

本文我们先站在渲染流水线的视角来介绍CSS是如何工作的，然后通过CSS的工作流程来分析性能瓶颈，最后再来讨论如何减少首次加载时的白屏时间。

## 渲染流水线视角下的CSS

我们先结合下面代码来看看最简单的渲染流程：

```
//theme.css
div{ 
    color : coral;
    background-color:black
}
```

```
<html>
<head>
    <link href="theme.css" rel="stylesheet">
</head>
<body>
    <div>geekbang com</div>
</body>
</html>
```

这两段代码分别由CSS文件和HTML文件构成，我们来分析下打开这段HTML文件时的渲染流水线，你可以先参考下面这张渲染流水线示意图：

![](https://static001.geekbang.org/resource/image/70/18/70a7ea0212ff35fc2be79f1d574ed518.png?wh=1142%2A469)

含有CSS的页面渲染流水线

下面我们结合上图来分析这个页面文件的渲染流水线。

首先是发起主页面的请求，这个发起请求方可能是渲染进程，也有可能是浏览器进程，发起的请求被送到网络进程中去执行。网络进程接收到返回的HTML数据之后，将其发送给渲染进程，渲染进程会解析HTML数据并构建DOM。这里你需要特别注意下，请求HTML数据和构建DOM中间有一段空闲时间，这个空闲时间有可能成为页面渲染的瓶颈。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/81/d3/f0a88806.jpg" width="30px"><span>🍐 🍾 🔆</span> 👍（16） 💬（18）<div>老师我想问下 如果script放在&lt;&#47;body&gt; 还有优化的意义么  这样就不会阻塞渲染了么 </div>2019-12-03</li><br/><li><img src="" width="30px"><span>vianem</span> 👍（0） 💬（9）<div>老师求解答：


&lt;html&gt;
&lt;head&gt;
    &lt;link href=&quot;theme.css&quot; rel=&quot;stylesheet&quot;&gt;
&lt;&#47;head&gt;
&lt;body&gt;
    &lt;div&gt;geekbang com&lt;&#47;div&gt;
    &lt;script&gt;
        while (1) {}
    &lt;&#47;script&gt;
    &lt;div&gt;geekbang com&lt;&#47;div&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;
按照文章中所说，dom解析应该一直被while循环阻塞，更生成不了布局树和绘制位图。但是我们还是能看到页面能显示出script标签前的内容呀。</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（148） 💬（24）<div>第1条：下载JavaScript文件并执行同步代码，会阻塞页面渲染
第2条：defer异步下载JavaScript文件，会在HTML解析完成之后执行，不会阻塞页面渲染
第3条：sync异步下载JavaScript文件，下载完成之后会立即执行，有可能会阻塞页面渲染
第4条：下载CSS文件，可能阻塞页面渲染
第5条：media属性用于区分设备，screen表示用于有屏幕的设备，无法用于打印机、3D眼镜、盲文阅读机等，在题设手机条件下，会加载，与第4条一致，可能阻塞页面渲染
第6条：print用于打印预览模式或打印页面，这里不会加载，不会阻塞页面渲染
第7条：orientation:landscape表示横屏，与题设条件一致，会加载，与第4条一致，可能阻塞页面渲染
第8天：orientation:portrait表示竖屏，这里不会加载，不会阻塞页面渲染

会阻塞页面的有1、3、4、5、7。我这里的问题在于是否加载CSS文件和JavaScript文件时，CSS文件一定会阻塞JavaScript代码的执行，还是说在JavaScript脚本需要使用到CSSOM能力的时候才会有这个前置依赖。</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yicibWmBIDaSpBYI5wCBDQcYu6mxjvz3XZzBibxSNXFfqCS6OJOjvy2Nc2lyDicZfmneW9ZY4KbicA1sNgLktVSicgkw/132" width="30px"><span>老余</span> 👍（23） 💬（1）<div>script异步的属性是async，不是sync</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/b0/c196c056.jpg" width="30px"><span>SeaYang</span> 👍（17） 💬（3）<div>老师，浏览器是不是有一个尽量快速渲染页面的机制呢？比如说，有时候打开一个网页很慢，后面慢慢地显示了样式错乱的页面，这明显是css没有加载构建完成，但是还是看到有页面出来了，只是样式有点乱。老师，能解释一下浏览器在这个过程中的一些优化措施吗？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/76/02/ce50af35.jpg" width="30px"><span>梦见君笑</span> 👍（16） 💬（0）<div>DOMContentLoaded: 当页面的内容解析完成后，则触发该事件 
   •JS 会阻塞DOM的解析和渲染，所以DOMContentLoaded会在JS执行后触发
   • 因为CSS会阻塞JS执行
       • 如果JS在CSS之前或只有CSS资源，则DOMContentLoaded事件不必等CSS加载完毕
       • 如果页面同时存在JS和CSS且CSS在JS之前，那DOMContentLoaded事件需等待CSS加载完毕后触发

onLoad: 等待页面的所有资源都加载完成才会触发，这些资源包括css、js、图片视频等</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/3a/2f/70c1007f.jpg" width="30px"><span>梦星魂</span> 👍（8） 💬（2）<div>老师好，经过我实践后的得知，chrome遇到外部脚本就会渲染标签之前的dom,  这应该是chrome的优化处理，但如果是内联脚本，则会阻塞全部dom的渲染</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/91/88/85e0e2a3.jpg" width="30px"><span>雨晴</span> 👍（5） 💬（5）<div>我觉得有两个问题不是很明确
1.网速很慢的时候，会出现无样式的DOM，此时的css文件没有下载解析完成，但文章中说，DOM 构建结束之后、css 文件还未下载完成的这段时间内，渲染流水线无事可做，因为下一步是合成布局树，而合成布局树需要 CSSOM 和 DOM，所以这里需要等待 CSS 加载结束并解析成 CSSOM。布局树没有生成的情况下，怎么布局？怎么渲染呢？无样式dom怎么出现的呢？
2.为什么要把JS放在&#47;body前，反正都是一样阻塞</div>2021-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f6/7d/29432580.jpg" width="30px"><span>诤</span> 👍（5） 💬（9）<div>网络进程不是按流式把数据给渲染进程，同时渲染进程用HTML parser构造DOM的么，似乎不存在预解释的机会阿</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/88/73/592c8ddd.jpg" width="30px"><span>HB</span> 👍（5） 💬（1）<div>有个疑问，DOM tree 和 render tree  构建是同时进行的还是DOM tree和 cssom都构建完成后才构建render tree呢？看how browser works  有些没看清楚</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c3/b9/c177ce04.jpg" width="30px"><span>弓</span> 👍（4） 💬（2）<div>如果没有js，解析到link 有 css这个标签的时候，css不管下没下载好，是否都会阻塞html的解析
</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/23/bd/b150086a.jpg" width="30px"><span>在路上_W</span> 👍（2） 💬（0）<div>Hardboiled Web Design这本书中讲，这个方法初看起来似乎在区分不同媒体查询的时候非常有效，但是当心，浏览器会下载每一个外联的样式表，无论这些样式在当前设备中
是否有效，这将会大大降低网站或者APP 的性能。
李老师文章说是特定场景下会才会加载，这个只是会都下载，但有些不符合条件的文件不会被解析吗？</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/7b/bd2d9d0c.jpg" width="30px"><span>(ಡωಡ)hahaha</span> 👍（2） 💬（3）<div>老师，请问一下，你在说  这个问题（渲染引擎还需要将这些内容转换为 CSSOM，因为 JavaScript 有修改 CSSOM 的能力，所以在执行 JavaScript 之前，还需要依赖 CSSOM。也就是说 CSS 在部分情况下也会阻塞 DOM 的生成）css也会阻塞dom生成，是因为js阻塞了dom, 而 JavaScript 执行之前，还需要依赖 CSSOM，是怎么判断js依赖 cssom,是 执行js  发现 需要cssom,渲染引擎 停止执行js,开始去解析css吗</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/16/b525a71d.jpg" width="30px"><span>zgy</span> 👍（1） 💬（0）<div>这个的页面的 async 写错了，在文章中“JavaScript 标记上 sync 或者 defer”</div>2023-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（1） 💬（0）<div>
1:&lt;script src=&quot;foo.js&quot; type=&quot;text&#47;javascript&quot;&gt;&lt;&#47;script&gt; &#47;&#47; 会，因为加载了js文件
2:&lt;script defer src=&quot;foo.js&quot; type=&quot;text&#47;javascript&quot;&gt;&lt;&#47;script&gt; &#47;&#47; 不会，因为是在DOM解析完成后， DOMContentLoaded 之前执行
3:&lt;script sync src=&quot;foo.js&quot; type=&quot;text&#47;javascript&quot;&gt;&lt;&#47;script&gt; &#47;&#47; 会，因为加载后立即执行
4:&lt;link rel=&quot;stylesheet&quot; type=&quot;text&#47;css&quot; href=&quot;foo.css&quot; &#47;&gt; &#47;&#47; 会，因为需要生成CSSOM
5:&lt;link rel=&quot;stylesheet&quot; type=&quot;text&#47;css&quot; href=&quot;foo.css&quot; media=&quot;screen&quot;&#47;&gt; &#47;&#47; 会，因为针对屏幕
6:&lt;link rel=&quot;stylesheet&quot; type=&quot;text&#47;css&quot; href=&quot;foo.css&quot; media=&quot;print&quot; &#47;&gt; &#47;&#47; 不会，因为在打印机才生效
7:&lt;link rel=&quot;stylesheet&quot; type=&quot;text&#47;css&quot; href=&quot;foo.css&quot; media=&quot;orientation:landscape&quot; &#47;&gt; &#47;&#47; 会，因为横屏
8:&lt;link rel=&quot;stylesheet&quot; type=&quot;text&#47;css&quot; href=&quot;foo.css&quot; media=&quot;orientation:portrait&quot; &#47;&gt; &#47;&#47; 不会，因为竖屏</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1c/02/7d613e6c.jpg" width="30px"><span>哦啦啦</span> 👍（1） 💬（1）<div>【复制好基本的布局树结构之后，渲染引擎会为对应的 DOM 元素选择对应的样式信息，这个过程就是样式计算。】
老师，这里的描述跟前面渲染流程的章节有矛盾啊，样式计算不是在布局树构建之前就做好的吗？</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/02/1c/fa6f649e.jpg" width="30px"><span>星星Leo</span> 👍（1） 💬（0）<div>所以要把js放在下面。
因为遇到js 如果是引入的话 就要等下载 而js又要等css的下载 也就是取其大者 不是引入也要等css下载 
css放在哪里应该无所谓 老师说过会提前下载</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/10/30/c07d419c.jpg" width="30px"><span>卡尔</span> 👍（1） 💬（0）<div>老师，css文件会不会阻塞页面渲染是需要通过js内容判断的吗？如果js里未引用css文件的话，是不是css文件就不会阻塞渲染呢？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/35/dc/e1d53df0.jpg" width="30px"><span>fantecy</span> 👍（0） 💬（0）<div>新版的Edge浏览器上，js和css执行是不会阻塞dom的渲染的，浏览器会把已经解析到的dom先渲染出来，然后再去执行js脚本。</div>2023-03-02</li><br/><li><img src="" width="30px"><span>Geek_3370e7</span> 👍（0） 💬（0）<div>有个问题，如果css的下载放在js的后方或者DOM里内联，那DOM解析暂停在js处的时候，只会把之前的cssom处理完吗。因为还没解析到后方css的tag，还是说这时候js会延后执行</div>2023-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e4/af/f8cf4bc2.jpg" width="30px"><span>Light 胖虎</span> 👍（0） 💬（0）<div>有一个问题，把这种外部引用全部放到html文件的最后是不是就可以解决这个问题呢
</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/10/79/390568f3.jpg" width="30px"><span>kkkkkkkk</span> 👍（0） 💬（0）<div>页面渲染需要DOM树（来自于HTML dom和JS影响） &amp; CSS树（CSS文件和JS影响）。
在解析HTML的过程中会构建DOM，同时也会请求JS和CSS文件
构建顺序：
- 从上到下
- 遇到JS和CSS文件就请求

阻塞优先级：CSS构建  &gt; JS解析 &gt; DOM构建</div>2022-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/80/ae/2c863d55.jpg" width="30px"><span>潘小安</span> 👍（0） 💬（0）<div>”对于大的 CSS 文件，可以通过媒体查询属性，将其拆分为多个不同用途的 CSS 文件，这样只有在特定的场景下才会加载特定的 CSS 文件。“
请问老师，页面需要媒体查询的时候需要从后端请求 css，这个时候会不会有页面卡顿</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e3/0f/0657ebc0.jpg" width="30px"><span>Echo</span> 👍（0） 💬（0）<div>css是下载下来之后就开始解析成cssom树了吗，还是要等待一个时机再对css进行解析</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/36/abb7bfe3.jpg" width="30px"><span>Hhpon</span> 👍（0） 💬（0）<div>老师，您好，请问解析白屏之后的首次渲染是什么？会显示出页面内容吗？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/47/abb7bfe3.jpg" width="30px"><span>LS</span> 👍（0） 💬（2）<div>这里有点问题，预解析会提前下载，其实也相当于异步了，而defer，async也是异步下载。那么用了defer，async理论上应该没啥区别？defer会在最后执行，不加defer就在中间执行，这时间(dom解析+执行js+继续dom解析， dom解析+继续dom解析+执行js)加起来时间不也是一样的么。async可能在dom解析完执行，好像也差不多没啥差别。</div>2021-09-29</li><br/><li><img src="" width="30px"><span>Geek_7be3ab</span> 👍（0） 💬（0）<div>老师，请问微信订阅号内的文章打开首屏渲染优化也是这些吗？有什么其他方式吗？</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f8/81/bff52f91.jpg" width="30px"><span>1830</span> 👍（0） 💬（0）<div>老师，这几节课介绍了渲染是依赖布局树的，布局树依赖dom树和cssom。我有个问题是布局树是必须所有的dom解析完成和cssom创建完成后再开始的嘛，还是一边解析创建，一边渲染绘制</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d5/dc/94057bab.jpg" width="30px"><span>Jinx</span> 👍（0） 💬（0）<div>请问老师，在两个非白色背景色的页面直接跳转，浏览器是不是把这里的解析白屏有优化？ 如果不是的话，那页面跳转时白屏终会一闪而过，但是在chrome里我看到这个现象（黑页面直接到黑页面）。 但是如果在iframe里进行页面跳转，就会出现 （黑-&gt; 白 -&gt; 黑）的状况。。 </div>2021-06-17</li><br/>
</ul>