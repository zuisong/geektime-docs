你好，我是月影。今天，我们来讲SVG。

SVG的全称是Scalable Vector Graphics，可缩放矢量图，它是浏览器支持的一种基于XML语法的图像格式。

对于前端工程师来说，使用SVG的门槛很低。因为描述SVG的XML语言本身和HTML非常接近，都是由标签+属性构成的，而且浏览器的CSS、JavaScript都能够正常作用于SVG元素。这让我们在操作SVG时，没什么特别大的难度。甚至，我们可以认为，**SVG就是HTML的增强版**。

对于可视化来说，SVG是非常重要的图形系统。它既可以用JavaScript操作绘制各种几何图形，还可以作为浏览器支持的一种图片格式，来 独立使用img标签加载或者通过Canvas绘制。即使我们选择使用HTML和CSS、Canvas2D或者WebGL的方式来实现可视化，但我们依然可以且很有可能会使用到SVG图像。所以，关于SVG我们得好好学。

那这一节课，我们就来聊聊SVG是怎么绘制可视化图表的，以及它的局限性是什么。希望通过今天的讲解，你能掌握SVG的基本用法和使用场景。

## 利用SVG绘制几何图形

在第1节课我们讲过，SVG属于**声明式绘图系统**，它的绘制方式和Canvas不同，它不需要用JavaScript操作绘图指令，只需要和HTML一样，声明一些标签就可以实现绘图了。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5d/9afdf648.jpg" width="30px"><span>Link</span> 👍（36） 💬（4）<div>1. 使用 CSS 设置样式的好处：可以将样式和节点解耦，有利于样式的模块化和复用，比如多种主题色，一键换色等。
2. 先用 SVG 生成层级关系图，再用 Canvas 来完成绘制，此时 SVG 将作为一张静态图片被绘制在 Canvas 中。和单独使用 Canvas 绘图相比，这种混合方式代码量更少，代码更加可读，易维护。</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3c/21/58f3740d.jpg" width="30px"><span>Geek_3469f6</span> 👍（7） 💬（4）<div>if(target.nodeName === &#39;text&#39;) target = target.parentNode;
 
请问，这句代码是不是有问题？找到文本节点的父节点，是group节点。设置了fill，有什么用处？</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/b6/51eda97d.jpg" width="30px"><span>Frojan</span> 👍（5） 💬（1）<div>canvas绘制svg，和单独用svg对比，好处是可以规避svg节点过多时的性能瓶颈，但是也失去了svg方便的可交互性。和单独用canvas对比，写法就由写一堆绘制指令变成了写声明式svg加一句绘图指令，单纯绘制性能在绘制指令多且复杂的情况貌似有比较大的提升？(这个不确定svg的解析时间是不是可以忽略) ，但是交互还得使用canvas的方式实现，如果要做动画也会变得麻烦。</div>2020-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Fnol5T7X9z9icw8yP1Zx5enHdYqbmP4EbNymaP87USujdeDp22QYMEwfYqkT7mOkXYegBZmhRx9bDbUbKGTPYlg/132" width="30px"><span>Geek_00734e</span> 👍（4） 💬（2）<div>SVG画出来的效果看着更加清晰，canvas画出来的好模糊，这是什么原因啊。尺寸都是一样的</div>2021-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/14/66/57b04294.jpg" width="30px"><span>Cailven</span> 👍（4） 💬（2）<div>关于svg，我补充一点，如今微信公众号互动图文支持使用svg制作交互和动画，但不支持js语言，因此掌握原生svg语言非常重要，并不是任何场景都可以使用js来声明和调用该系统的。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/70/02b627a6.jpg" width="30px"><span>coder</span> 👍（3） 💬（1）<div>做可视化组件，从性能的角度来讲，是SVG好一些，还是Canvas好一些？</div>2020-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKCiciak9BCOSsuydrXxSklzpzbr3nqj1E5vZCPlPPUSZs5q4R6LAgI56Ria6hdJFEAibvZEca0O5Lxdg/132" width="30px"><span>Geek_07ad60</span> 👍（3） 💬（2）<div>还是不太理解声明式和指令式，请老师再详解一下，谢谢！</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3f/5f/053bc2da.jpg" width="30px"><span>特异型大光头</span> 👍（2） 💬（2）<div>&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;

&lt;head&gt;
    &lt;meta charset=&quot;UTF-8&quot;&gt;
    &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1.0&quot;&gt;
    &lt;title&gt;Document&lt;&#47;title&gt;
&lt;&#47;head&gt;

&lt;body&gt;
    &lt;svg xmlns=&quot;http:&#47;&#47;www.w3.org&#47;2000&#47;svg&quot; version=&quot;1.1&quot;&gt;
    &lt;&#47;svg&gt;
    &lt;script&gt;
        const svgroot = document.querySelector(&#39;svg&#39;);
        const circle = document.createElementNS(&#39;http:&#47;&#47;http:&#47;&#47;www.w3.org&#47;2000&#47;svg&#39;, &#39;circle&#39;);
        circle.setAttribute(&#39;cx&#39;, 100);
        circle.setAttribute(&#39;cy&#39;, 100);
        circle.setAttribute(&#39;r&#39;, 50);
        circle.setAttribute(&#39;fill&#39;, &#39;#ff0000&#39;);
        svgroot.appendChild(circle);
    &lt;&#47;script&gt;
&lt;&#47;body&gt;

&lt;&#47;html&gt;
老师为何我创建后,控制台也生成了svg,和circle,但就是页面上显示不出来...
</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f5/c2/4e551270.jpg" width="30px"><span>姚凯伦</span> 👍（2） 💬（1）<div>最近也遇到过用svg绘制元素太多导致渲染卡顿问题，后来改用使用一条 path 绘制所有元素，但是 path 一长也同样存在渲染卡顿问题，不知道老师有没有遇到过类似的问题</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/fe/f8/9854ff33.jpg" width="30px"><span>段亚东</span> 👍（0） 💬（1）<div>这两个案例，为什么不直接用div css画呢？</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/14/86/54542ea4.jpg" width="30px"><span>颖</span> 👍（4） 💬（2）<div>老师能否多做一些svg交互的课程，不用js操作，我们有很大需求，愿意买课</div>2020-08-02</li><br/><li><img src="" width="30px"><span>胖橘猫</span> 👍（1） 💬（0）<div>只有我存在获取省市县三级json数据的问题吗？获取数据时候出现net::ERR_NAME_NOT_RESOLVED，ping 也无法ping通</div>2021-07-02</li><br/><li><img src="" width="30px"><span>Geek_12e8fd</span> 👍（0） 💬（0）<div>如果你选择先用SVG生成层级关系图，然后再用Canvas来完成绘制，与单独使用它们绘图的主要区别体现在以下几个方面：

绘图过程与交互性：
使用SVG生成层级关系图时，每个图形元素（如圆形、文本等）都是独立的DOM元素，这使得添加用户交互（如鼠标悬停高亮、点击事件等）变得非常简单直接。你可以像操作普通的HTML元素一样给SVG元素绑定事件[2]。
相比之下，Canvas绘图则更加底层，所有的图形都是通过绘图指令在画布上直接绘制的，没有独立的DOM元素与之对应。因此，实现用户交互通常需要更多的计算和逻辑判断，比如通过计算鼠标位置与图形元素的相对位置来确定交互[2]。
性能考虑：
SVG的性能主要取决于DOM操作的开销。当图形复杂或需要频繁更新时，大量的SVG节点可能会导致性能下降[2]。然而，SVG在处理少量或静态图形时通常表现良好。
Canvas则更适合处理大量或频繁更新的图形。由于它直接操作像素，不依赖于DOM树，因此在渲染大量图形或动画时通常具有更好的性能[2]。
灵活性与可维护性：
SVG是声明式的，通过定义图形元素的属性和样式来绘图，这种方式更接近于HTML和CSS的编写方式，对于前端工程师来说更加直观和易于理解[1]。此外，SVG文件可以独立于其他代码存在，方便单独编辑和测试。
Canvas是命令式的，通过JavaScript代码执行绘图指令来绘制图形。这种方式提供了更大的灵活性，可以实现更复杂的视觉效果和动画效果。但是，这也意味着Canvas绘图代码通常与业务逻辑紧密耦合，维护和修改可能更加复杂。
结合使用的优势：
将SVG和Canvas结合使用可以充分发挥两者的优势。例如，你可以使用SVG生成复杂的静态图形或需要高交互性的部分，然后将它们作为图像绘制到Canvas上，以便利用Canvas的高性能渲染能力来处理大量动态图形或动画[4]。
综上所述，选择先用SVG生成层级关系图再用Canvas绘制，还是单独使用它们绘图，取决于具体的应用场景和需求。如果图形复杂且需要高交互性，SVG可能是更好的选择；如果图形数量众多或需要高性能渲染，Canvas则更具优势。而在某些情况下，结合使用两者可以达到最佳效果。</div>2024-06-14</li><br/><li><img src="" width="30px"><span>Geek_12e8fd</span> 👍（0） 💬（0）<div>当使用SVG创建图形时，确实可以通过CSS来设置SVG元素的样式，包括circle元素的背景色和文字属性。以下是如何使用CSS来设置层级关系图中circle的背景色和文字属性的示例，以及这样做的好处：

设置样式
假设你的SVG层级关系图在HTML文档中看起来像这样：

html
&lt;svg id=&quot;hierarchy-svg&quot; ...&gt;  
  &lt;!-- SVG内容，包括circle和text元素 --&gt;  
&lt;&#47;svg&gt;
你可以通过CSS来设置样式：

css
#hierarchy-svg circle {  
  fill: #ddd; &#47;* 设置circle的背景色 *&#47;  
  stroke: #000; &#47;* 设置circle的边框颜色 *&#47;  
  stroke-width: 2px; &#47;* 设置circle的边框宽度 *&#47;  
}  
  
#hierarchy-svg circle:hover {  
  fill: #f00; &#47;* 鼠标悬停时改变circle的背景色 *&#47;  
}  
  
#hierarchy-svg text {  
  fill: #333; &#47;* 设置text的颜色 *&#47;  
  font-family: Arial, sans-serif; &#47;* 设置字体 *&#47;  
  font-size: 12px; &#47;* 设置字体大小 *&#47;  
}
这样做的好处
统一样式管理：通过将SVG样式放在CSS文件中，你可以更容易地管理和维护样式。这意味着你可以在一个地方更改所有circle或text元素的样式，而不是在每个SVG元素中单独设置。
代码复用：CSS的复用性意味着你可以为SVG元素定义通用的样式规则，并在多个SVG实例中应用这些规则。
响应式设计：使用CSS媒体查询，你可以轻松地调整SVG元素的样式以适应不同的屏幕尺寸和分辨率，实现响应式设计。
易于阅读和维护：将样式与结构分离可以使HTML和SVG代码更易于阅读和维护。CSS文件本身也更容易组织和管理。
动画和过渡效果：CSS还支持动画和过渡效果，这意味着你可以很容易地为SVG元素添加动态效果，如颜色变化、大小缩放等。
与现有工具集成：许多现有的前端工具，如预处理器（如Sass或Less）、CSS框架（如Bootstrap）和CSS-in-JS库（如styled-components或emotion），都可以与CSS一起使用来增强SVG样式的开发体验。
通过结合使用SVG和CSS，你可以创建出既功能强大又视觉吸引人的可视化图表和图形。</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2c/0d/4f270e21.jpg" width="30px"><span>南风知我意NY</span> 👍（0） 💬（0）<div>老师，获取地区数据接口报错怎么办？</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/41/6e/e04ab385.jpg" width="30px"><span>null</span> 👍（0） 💬（0）<div>作业1用 css 实现，使用了两种布局形式，优点就是布局和样式分离，可以使用 css 样式，很方便；
1: 嵌套式 https:&#47;&#47;github.com&#47;bjfecxn&#47;geek-visual-demo&#47;blob&#47;master&#47;basic&#47;city-css.html
2: 仿 svg 层级模式：https:&#47;&#47;github.com&#47;bjfecxn&#47;geek-visual-demo&#47;blob&#47;master&#47;basic&#47;city-css2.html

作业2：https:&#47;&#47;github.com&#47;bjfecxn&#47;geek-visual-demo&#47;blob&#47;master&#47;basic&#47;city-svg-canvas.html
可能是缺少实际项目经验，目前并没有感受到太多这样的好处，并且 canvas 明显模糊很多，看评论要根据 devicePixelRate 设置好 canvas；待优化～
</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e4/a0/62a8b07e.jpg" width="30px"><span>阿东</span> 👍（0） 💬（0）<div>作业
1. 优点和html内联样式分离一样，缺点是需要更多的className节点
2. svg作为一张图片，会失去它原有的层级关系，适用于把整个svg当成单独对象处理的场景</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/6e/8ca500c6.jpg" width="30px"><span>雨田²⁰¹⁸</span> 👍（0） 💬（0）<div>老师，我这边画了尺子，尺子上有旋转，缩放，关闭，切换线的ICON， 尺子我是用canvas纯moveTo lineTo画出来的，涉及到每次移动、按钮操作多需要重绘。

这种情况，用svg是否能性能更佳呢</div>2021-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL1H2TOJnNTblhmzJ2p88sTjvb86PuXP7A8HpCNKrfobuOc6Cxgy1UogZMIPTmD3VDGXZfTXIaWNw/132" width="30px"><span>Geek_cd63d9</span> 👍（0） 💬（1）<div>老师好，我实现的只显示最外层的圆，内层的dom结构有，但不显示，有时间能帮我看眼吗？https:&#47;&#47;github.com&#47;ByteJitter&#47;visualization&#47;blob&#47;master&#47;3&#47;2.html</div>2020-08-06</li><br/>
</ul>