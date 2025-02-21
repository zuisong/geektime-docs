你好，我是winter。今天我们来讲讲浏览器API。

浏览器的API数目繁多，我们在之前的课程中，已经一起学习了其中几个比较有体系的部分：比如之前讲到过的DOM和CSSOM等等。但是，如果你留意过，会发现我们讲到的API仍然是标准中非常小的一部分。

这里，我们不可能把课程变成一本厚厚的API参考手册，所以这一节课，我设计了一个实验，我们一起来给API分分类。

我们按照每个API所在的标准来分类。所以，我们用代码来反射浏览器环境中全局对象的属性，然后我们用JavaScript的filter方法来逐步过滤掉已知的属性。

接下来，我们整理API的方法如下：

- 从Window的属性中，找到API名称；
- 查阅MDN或者Google，找到API所在的标准；
- 阅读标准，手工或者用代码整理出标准中包含的API；
- 用代码在Window的属性中过滤掉标准中涉及的API。

重复这个过程，我们可以找到所有的API对应的标准。首先我们先把前面已经讲过的API过滤掉。

##JavaScript中规定的API

大部分的API属于Window对象（或者说全局对象），我们可以用反射来看一看现行浏览器中已经实现的API，我这里使用Mac下的Chrome 72.0.3626.121版本。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/56/4b8395f6.jpg" width="30px"><span>CC</span> 👍（128） 💬（0）<div>经过几天的整理，终于穷尽了 Chrome 下的 API。记得之前看别人文章中介绍的各种 API 一头雾水，现在回头看，多了不少熟悉感，而且每个 API 都能落在知识树的一个节点上。

分享整理所得：

W3C 标准下的 API：
* Web Audio API
* Web Cryptography API
* Media Source Extensions
* The Screen Orientation API
* Network Information API
* Web MIDI (Musical Instrument Digital Interface ) API 
* IndexedDB API
* Gamepad API
* DeviceOrientation Event
* Web App Manifest
* WebVTT: The Web Video Text Tracks Format
* Touch Events
* Scalable Vector Graphics (SVG)
* Resize Observer API
* Intersection Observer
* Mutation Observer
* Cooperative Scheduling of Background Tasks
* Service Worker API
* Payment Request API
* Presentation API
* Web Authentication API

WICG 标准下的 API：
* Input Device Capabilitie
* Web Bluetooth API
* WebUSB API

ECMA 标准下的 API：
* JavaScript 全局变量
* ECMAScript 2018 Internationalization API

WHATWG 标准下的 API：
* Streams
* Encoding
* URL

Khronos 标准下的 API：
* WebGL

未标准化的 API：
* Web Background Synchronization
* WebRTC API
* Document Object Model XPath
* Visual Viewport API
* Performance Timeline API
</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（26） 💬（0）<div>整理的过程中，我发现我对翻阅标准的恐惧心降低了... 而且大概了解了一下这些spec都在干些啥(虽然也有很多并不知道他们是在干啥)...

就是花的时间有点长... 都整理完太累了... 有些词实在是检索不到spec，只能在一些犄角旮旯的地方甚至源码里看到引用...

过程中，甚至提升了搜索引擎的使用技巧：
关键词 site:域名
&quot;关键词&quot;

结果如下（肯定有不准确的地方... 仅供参考）：
https:&#47;&#47;gist.github.com&#47;aimergenge&#47;c0fb01dbdbf3aa1c2b31e3f2ae779274

tc39,w3c,whatwg 基本就这几个组织在推动web发展....
另外还有个khronos管openGL、webGL等图形标准的...</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f7/56/b82eeac7.jpg" width="30px"><span>champ可口可乐了</span> 👍（14） 💬（0）<div>其实，MDN上已经整理好了
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;API</div>2020-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（6） 💬（0）<div>1. 通过老师的课，感觉慢慢会去翻标准了，之前学习没有见过的API，只是到MDN为止。
2. 浏览器器中大多数的对象都原型继承自Object，是否可以根据原型继承关系 将window上面的api绘制成一颗树？有了这些继承关系 是否更容易理清这些全局属性呢。
</div>2019-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/29/59663398.jpg" width="30px"><span>🐳李小博🐳</span> 👍（4） 💬（1）<div>有一个疑惑是，大小写的两个属性有什么区别
Screen，screen
Event，event</div>2019-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/1f/f95bd8c9.jpg" width="30px"><span>余文郁</span> 👍（2） 💬（0）<div>winter老师，问个关于DOM获取的问题，通过querySelectorAll获取的是静态集合，但通过getElementByClassName获取的是动态集合，会随着DOM结构的变化而变化，想这些获取的HTMLCollection和NodeList如何判断是不是动态的呢，以及他们底层的原理是怎么样的呢，为什么会有动态静态之分</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/12/13/e103a6e3.jpg" width="30px"><span>扩散性百万咸面包</span> 👍（1） 💬（0）<div>说实话，老师这个整理API的学习方法挺好，加深对API的整体理解，对技术也有了更全面的认知。（还可以归个类，大致分分组）以后我学其他技术的时候也用这个办法，快速上手。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1a/5d/3c8004c6.jpg" width="30px"><span>*</span> 👍（0） 💬（0）<div>WHATWG、W3C这两个组织有什么区别啊</div>2022-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（0） 💬（1）<div>我过滤到其他API之前还剩下523个，大家呢？</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5e/e3/da3167ff.jpg" width="30px"><span>李岩</span> 👍（0） 💬（0）<div>醍醐灌顶
</div>2020-06-16</li><br/>
</ul>