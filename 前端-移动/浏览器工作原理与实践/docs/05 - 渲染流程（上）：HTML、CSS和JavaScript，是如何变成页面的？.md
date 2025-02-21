在[上一篇文章](https://time.geekbang.org/column/article/117637)中我们介绍了导航相关的流程，那导航被提交后又会怎么样呢？就进入了渲染阶段。这个阶段很重要，了解其相关流程能让你“看透”页面是如何工作的，有了这些知识，你可以解决一系列相关的问题，比如能熟练使用开发者工具，因为能够理解开发者工具里面大部分项目的含义，能优化页面卡顿问题，使用JavaScript优化动画流程，通过优化样式表来防止强制同步布局，等等。

既然它的功能这么强大，那么今天，我们就来好好聊聊**渲染流程**。

通常，我们编写好HTML、CSS、JavaScript等文件，经过浏览器就会显示出漂亮的页面（如下图所示），但是你知道它们是如何转化成页面的吗？这背后的原理，估计很多人都答不上来。

![](https://static001.geekbang.org/resource/image/2b/79/2b08a85c63bee68c6fd95dabb648fd79.png?wh=1142%2A451)

渲染流程示意图

从图中可以看出，左边输入的是HTML、CSS、JavaScript数据，这些数据经过中间渲染模块的处理，最终输出为屏幕上的像素。

这中间的**渲染模块**就是我们今天要讨论的主题。为了能更好地理解下文，你可以先结合下图快速抓住HTML、CSS和JavaScript的含义：

![](https://static001.geekbang.org/resource/image/31/e6/31cd7172f743193d682d088a60cb44e6.png?wh=1142%2A704)

HTML、CSS和JavaScript关系图

从上图可以看出，**HTML的内容是由标记和文本组成**。标记也称为**标签**，每个标签都有它自己的语义，浏览器会根据标签的语义来正确展示HTML内容。比如上面的`<p>`标签是告诉浏览器在这里的内容需要创建一个新段落，中间的文本就是段落中需要显示的内容。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（292） 💬（35）<div>关于下载css文件阻塞的问题，我理解
1 不会阻塞dom树的构建，原因Html转化为dom树的过程，发现文件请求会交给网络进程去请求对应文件，渲染进程继续解析Html。
2 会阻塞页面的显示，当计算样式的时候需要等待css文件的资源进行层叠样式。资源阻塞了，会进行等待，直到网络超时，network直接报出相应错误，渲染进程继续层叠样式计算

</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（89） 💬（3）<div>这节讲的有些过于省略了，好多东西没有深入去讲。我记得是DOM树和CSSOM树并行构建合成渲染树。从这个角度来说，不会阻塞DOM树的构建，但是会阻塞页面显示，因为页面显示需要完整的渲染树去完成布局计算。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c5/5d/9e75eb36.jpg" width="30px"><span>Bean</span> 👍（21） 💬（1）<div>老师，渲染进程的工作原理您是从哪知道的，看浏览器的源码吗？ 有链接吗来一个</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（17） 💬（7）<div>请问老师，为什么没有清晰地将输入内容和输出内容区分开来不好，我们平时编码过程中，应该尽量做到将输入内容和输出内容区分开来吗？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d8/9b/f9a00567.jpg" width="30px"><span>why.</span> 👍（3） 💬（1）<div>dom 树解析在前，合成在后，既然解析阶段都阻塞了，合成那就更不用说了啊，阻塞，可以这样理解吗?</div>2019-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b4/61/1db459e5.jpg" width="30px"><span>哎姆哦剋</span> 👍（0） 💬（1）<div>答案到底是什么，老师给个标准答案啊！</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e7/20/70a95f94.jpg" width="30px"><span>潮汐</span> 👍（0） 💬（1）<div>对留言顶部第一条基本赞成。
但有个疑问：css文件的下载是在网络进程中进行，成功或失败，都是在通知准备渲染进程时已经确定了的吧，还是说渲染过程中会并行下载文件。如果是前者，应该没有阻碍的问题，最多延迟进入准备渲染阶段，也相当于阻塞了页面加载；如果是后者，猜测会阻碍布局树的生成。
提个建议：如果上一节课的问题有标准的对与错答案，下节课开头，老师能不能给一个解答或提及。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5f/02/f8a80843.jpg" width="30px"><span>XWL</span> 👍（0） 💬（1）<div>应该不会阻塞，link加载CSS样式本身是异步进行的，所以并不会影响浏览器继续解析之后的DOM的标签，最后由CSS树和DOM树合成render树，然后由render树渲染成页面，所以CSS的下载不阻塞DOM树，但阻塞着最后页面的渲染。
这是我的理解，有错误请指出。。。
另外，老师为什么不讲讲回流和重绘</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/ce/1e02a513.jpg" width="30px"><span>刘大夫</span> 👍（36） 💬（1）<div>这节讲的真好，什么 CSSOM、渲染树不是不讲，而是真的过时了，现在就是分层、光栅化和合成</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/b8/62ed38de.jpg" width="30px"><span>海骅薯条</span> 👍（35） 💬（0）<div>下载CSS文件阻塞了，原则上会阻塞页面的显示，但是浏览器可以有自己的容错机制，例如下载超时后，均采用user-agent stylesheet 默认样式进行渲染就可以啦，虽然丑点，但是内容在HTML都显示出来啦</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ad/ec/776c9f72.jpg" width="30px"><span>袋袋</span> 👍（8） 💬（5）<div>不阻塞dom合成，也不阻塞页面渲染，页面还是会生成，只不过没有样式而已，别忘了标签是有语义化的</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（6） 💬（2）<div>
DOM树的构建和样式计算都是在渲染进程的主线程上执行的，他们可以并行执行吗？如果可以的话，那他们是如何来实现并行的呢？是通过异步回调还是说用的是类似于Generator函数的协程呢？在css会阻塞dom树的构建的情况下，主线程是如何去暂停DOM树的构建，后期又是如何恢复DOM树的构建的呢？希望老师解答一下</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（6） 💬（4）<div>css继承中应该不是所有的属性都会继承吧</div>2019-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/f4/a40453e7.jpg" width="30px"><span>man-moonth</span> 👍（6） 💬（0）<div>我打开chrome面板的performance，记录了页面的加载过程。想请教一个问题。
首先确认一下几个概念：
1. recalculatestyle过程是指生成computedStyle过程吗？
2. DOMContentLoaded事件标识浏览器已经完全加载了 HTML，DOM 树已经构建完毕。
我发现在DOMContentLoaded之前，生成computedStyle和构建DOM的过程是并行的。我之前的想法是，计算DOM节点的样式（computedStyle）的前置条件是构建DOM、CSS生成StyleSheets并完成属性值标准化，这样才能保证DOM节点样式的计算有条不紊。我的问题是：浏览器是如何并行处理构建DOM、生成computedStyle的流程的？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（5） 💬（1）<div>如果下载 CSS 文件阻塞了，会阻塞 DOM 树的合成吗？会阻塞页面的显示吗？
不会阻塞DOM 树的合成，但会阻塞页面的显示。
DOM 树和CSSOM树是并行生成的，两个都完成后才进行布局树的生成，但如果期间有JS文件，那就需要等待JS文件加载并执行完成，JS也需要等待CSSOM树生成，因为JS可能操作DOM树和CSSOM树。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/6e/46a5da10.jpg" width="30px"><span>Hong</span> 👍（4） 💬（1）<div>提个建议哈，老师讲到专有名词的时候，如果能把对应的英文名标注一下就更好了，比如提到的渲染树LayoutTree，否则可能容易造成困扰；上面内容如果再能详细深入一些就更好了。

觉得前端开发如何按上面的内容来回答，面试官可能不会很满意，最后还是推荐一片经典详文
https:&#47;&#47;www.html5rocks.com&#47;zh&#47;tutorials&#47;internals&#47;howbrowserswork&#47;</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（4） 💬（0）<div>思考题。不会，CSS阻塞了，DOM树照样能正常解析和渲染。猜测浏览器机制，会优先渲染DOM到页面上。平时网络不好时遇到过。</div>2019-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoLuYlxY5PGFMQqICGqPibvIic6O0RM56GtjbFwccMyDoUQHGI4LwLhVtFazmnHqCfTP2KHUHSckiazg/132" width="30px"><span>基础平台部-学习账号</span> 👍（3） 💬（0）<div>document.styleSheets接口只会返回引入和嵌入文档的样式表吧，不会返回内联样式，mdn有说明：https:&#47;&#47;developer.mozilla.org&#47;zh-CN&#47;docs&#47;Web&#47;API&#47;Document&#47;stylesheets</div>2021-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/2b/3b/10825655.jpg" width="30px"><span>Neil</span> 👍（3） 💬（3）<div>布局树构造过程示意图误导性太强了。计算样式阶段并不会生成&quot;ComputedStyle&quot;树，而是遍历styleSheets里的规则和DOM树，计算出每个DOM节点样式，放在每个DOM节点的ComputedStyle属性里。
参考：
https:&#47;&#47;www.youtube.com&#47;watch?v=m-J-tbAlFic
https:&#47;&#47;www.youtube.com&#47;watch?v=PwYxv-43iM4&amp;list=PL9ioqAuyl6ULtk9hyUKX__VH1EBE5r4me&amp;index=1
</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/28/17/2ee45db9.jpg" width="30px"><span>abson</span> 👍（3） 💬（2）<div>老师你好，我特意试了一下在HTML文件分别写了link、style和内联样式的形式引入css代码，然后在谷歌浏览器控制台上输出styleSheets的时候发现styleSheetList数组就只有两个，分别是link和style，内联样式是没有的。您本文说styleSheet会把三种css引入方式都显示出来这里是否是有别的依据支持呢？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/cc/8b/0060a75c.jpg" width="30px"><span>tomision</span> 👍（3） 💬（3）<div>老师，有个问题：

前端优化中总是告诉我们将 &lt;script&gt; 标签放在 &lt;&#47;body&gt; 的前面，即页面的最底部；

除了放在顶部执行的时候可能获取不到想要的 dom 元素之外，放在底部其实也会阻塞 DOM 解析？

所以 DOM 解析是一点点渲染出来的还是一次性渲染出来的？如果是等待全部解析完成，再提交进入后续的流程，那其实 &lt;script&gt; 标签放在页面底部的价值呢？</div>2020-02-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDVEPYH20ibMFeHjU9WVicAW1gzia2axxibOW2ibxic333ODcTx52ia9DfcRyUcUwAAmGTXBfCriaT9ONygg/132" width="30px"><span>xinCrazy</span> 👍（2） 💬（0）<div>加点chromium源码就好了</div>2022-08-14</li><br/><li><img src="" width="30px"><span>Geek_4c5172</span> 👍（2） 💬（0）<div>Chrome 版本：Version 103.0.5034.0 (Official Build) canary (arm64)。

通过一系列的试验，得出一些规律：

1. html解析渲染顺序是，对dom树进行深度遍历，依次解析渲染；例如：html -&gt; head -&gt; link(head) -&gt; script(head) -&gt; body -&gt; ...

2. 当html渲染遇到css或js时，会阻塞html渲染；当css或js下载、解析、执行完毕之后，html将继续渲染。

3. js的下载和执行会阻塞css的解析。
</div>2022-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（2） 💬（1）<div>1，不会阻塞dom树生成，因为dom树只要把html下载下来后就可以生成了
2，会阻塞页面显示，浏览器需要等待下载样式表文件合成样式表，进行后面的样式计算。
但是实际观察chrome浏览器加载页面，即便某个样式文件因为网络错误不能下载，页面最终也会显示，是不是样式计算和后续的布局是一个反复的过程？即，先用浏览器默认样式和style标签内样式、内联样式合成并布局显示页面，等下载好外部样式表再次合成并布局。不知道这样理解对不对？另外，如果用户通过操作修改了样式，是不是合成和布局也需要重新进行？</div>2019-08-15</li><br/><li><img src="" width="30px"><span>Geek_1efec9</span> 👍（1） 💬（0）<div>老师说的问题， 我认为是没有错误的。结合渲染进程来说，其只有一个主线程。那在渲染进程开始解析HTML数据的时候，只能一行一行执行，如果遇到CSS或者JS，就会停下DOM的解析，去下载或者执行CSS或者JS，接着继续对DOM的解析，然后输出DOM。</div>2022-09-26</li><br/><li><img src="" width="30px"><span>Geek_d95d52</span> 👍（1） 💬（1）<div>domtree 的 构建  和 css rule的生成 是 串行 还是并行</div>2021-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/e2/23e44221.jpg" width="30px"><span>余熙</span> 👍（1） 💬（0）<div>请问老师的插图是用什么软件画的呢？
每张图风格都不一样，老师的插图好丰富生动，对帮助理解提升好大。</div>2020-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c0/fa/61f78abd.jpg" width="30px"><span>Geek_012295</span> 👍（1） 💬（1）<div>老师您用的是什么作图软件，可以告知一下吗？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/73/56/9cfb1e43.jpg" width="30px"><span>sheeeeep</span> 👍（1） 💬（0）<div>自己总结一下老师对课后问题的回答：JS的执行会阻塞解析DOM，执行过程中，如果读取元素了的样式，则需要先下载完成CSS，则同样会导致DOM解析的阻塞</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/27/1f/42059b0f.jpg" width="30px"><span>HXL</span> 👍（0） 💬（0）<div>首先结论是可能会影响DOM树的合成, 这取决于页面是否有script标签. 

- 前提条件
1. chrome 128 
2. 是否阻塞 DOM树的合成 只需要通过 elements 面板即可看出来.
3. 假设有如下代码

&quot;&quot;&quot;html
&lt;head&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;theme.css&quot;&gt;
&lt;&#47;head&gt;

&lt;body&gt;

    &lt;p&gt;
        this is a paragraph
    &lt;&#47;p&gt;

    &lt;script&gt;
        let e = document.getElementsByTagName(&#39;p&#39;)[0]
    &lt;&#47;script&gt;

    &lt;p&gt;
        this is another paragraph
    &lt;&#47;p&gt;
&lt;&#47;body&gt;
&quot;&quot;&quot; 
&quot;&quot;&quot;ts
app.get(&#39;&#47;theme.css&#39;, async (c) =&gt; {
  await sleep(10000)
  const indexContent = await fs.readFile(path.join(__dirname, &#39;theme.css&#39;), &#39;utf8&#39;)
  return c.text(indexContent)
})
&quot;&quot;&quot;

- 现象1
1. script 之后 DOM 需要在 10s之后才会合成.
2. FP 出现在 10s之后

- 注释掉script标签之后的现象
1. script 之后 DOM 立即合成
2. FP 出现在 10s之后</div>2024-10-11</li><br/>
</ul>