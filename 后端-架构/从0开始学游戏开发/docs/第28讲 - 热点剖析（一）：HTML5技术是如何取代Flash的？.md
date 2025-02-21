本周开始，我将会在**每周六**更新一篇“热点剖析”，阐述我对2D游戏开发之外的热点，比如HTML5游戏、移动端游戏、AR和人工智能在游戏领域的应用，以及我对微信小游戏、移动游戏、独立游戏开发者的一些观点和看法。

我已经为你讲解了核心的开发知识，对于这些相对热门领域的知识，你可以根据兴趣进行选择学习。

本周及接下来两周的周六，我会依次为你介绍HTML5游戏，以及[如何选择HTML5的游戏引擎](https://time.geekbang.org/column/article/9702)，并带你编写一款H5小游戏。

从前几年开始，H5这个技术就开始蓬勃发展。不管是懂行的还是不懂行的，都开始以“H5”这个字眼来描述产品。比如老板会说“我们就做个H5的页面吧”，或者“这个游戏是H5的吗”。很多人已经把H5等价于“手机端页面”了，这样的理解显然是错误的。

那么H5究竟是什么？它的优点在哪里？为什么现在大家都在谈论H5？你真的知道H5是什么，并真的深入理解了它吗？

## Flash是什么？

首先，在说H5之前，我想先介绍一下Flash技术。

**Flash是由Adobe公司开发的一种富媒体技术，起初是一种放置在浏览器中的插件，填补了当时HTML页面平淡的空白，增强了网页交互的能力。**你可以在Flash中做出任何东西，也可以访问本地电脑中的东西。后来，Adobe公司推出了播放器，在电脑上不打开浏览器，也可以观看或者游戏Flash程序员编写出来的产品。乃至今日，依然有大量应用于Flash的富媒体应用，比如视频的播放，比如独立的小游戏，比如网页游戏，甚至桌面应用，都是使用Flash开发的。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/ce/771c25b0.jpg" width="30px"><span>壬大师</span> 👍（2） 💬（1）<div>老师，像斗地主、三国杀这种牌类手机游戏是用html5合适还是C++合适？</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/de/5c67895a.jpg" width="30px"><span>周飞</span> 👍（11） 💬（0）<div>XMLHttpRequest是原生ajax请求，不能解决跨域问题，还是得用jsonp或cors来解决。h5提供的是postmessage</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/23/3bc60cc6.jpg" width="30px"><span>董豪强</span> 👍（3） 💬（0）<div>threejs ，更底层的其实还是webgl</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/1b/9d1c6077.jpg" width="30px"><span>曹源</span> 👍（2） 💬（0）<div>WebGL？</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/7d/8cad9f55.jpg" width="30px"><span>😯</span> 👍（1） 💬（0）<div>WebGL吧，我们之前项目做过3D模型在浏览器渲染用到的就是这</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/06/7e/9609c6e9.jpg" width="30px"><span>H.Humbert</span> 👍（1） 💬（0）<div>webgl</div>2018-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/ec/337077d5.jpg" width="30px"><span>神马*涛💋</span> 👍（0） 💬（0）<div>老师，比如一个中国象棋游戏。用H5好 ，还是做成安卓app更好？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/40/70/2a598b83.jpg" width="30px"><span>王俊涛</span> 👍（0） 💬（0）<div>canvas webgl</div>2018-06-17</li><br/>
</ul>