在上一篇文章中，我和你一起理清了我们即将构建的持续交付系统的需求，以及要具备的具体功能。那么，从这一篇文章开始，我们就要正式进入实战阶段了。我会和你详细介绍基于开源工具，从0开始搭建一套持续交付平台的详细过程，以及整合各个持续交付工具的一些技术细节。

按照我在前面分享的内容，搭建一套持续交付系统的第一步，就是搭建一套代码管理平台。这里我选择的开源工具是GitLab，它是一套高仿GitHub的开源代码共享管理平台，也是目前最好的开源解决方案之一。

接下来，我们就从使用GitLab搭建代码管理平台开始吧，一起看看搭建GitLab平台的过程中可能遇到的问题，以及如何解决这些问题。

## 利用GitLab搭建代码管理平台

GitLab早期的设计目标是，做一个私有化的类似GitHub的Git代码托管平台。

我第一次接触GitLab是2013年, 当时它的架构很简单，SSH权限控制还是通过和Gitolite交互实现的，而且也只有源码安装（标准Ruby on Rails的安装方式）的方式。

这时，GitLab给我最深的印象是迭代速度快，每个月至少会有1个独立的release版本，这个传统也一直被保留至今。但是，随着GitLab的功能越来越丰富，架构和模块越来越多，也越来越复杂。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/4d/abb7bfe3.jpg" width="30px"><span>铭熙</span> 👍（4） 💬（2）<div>GitLab的高可用，能否详细说下携程的实现？</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/24/c6b763b4.jpg" width="30px"><span>桃子-夏勇杰</span> 👍（2） 💬（1）<div>没太看明白，为什么要对gitlab做二次开发。jar的发布与gitlab有什么关系？gitlab不就是一个代码版本库工具么？</div>2019-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（2） 💬（0）<div>老师，关于Gitlab的高可用方案可否再详细科普一下呀，ssh2做代理除了代理ssh请求，可以代理http&#47;https请求吗？另外是如何根据group的名字做sharding和备用切换的呢？ 谢谢</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8d/bf/507144e8.jpg" width="30px"><span>熙</span> 👍（2） 💬（0）<div>非常赞的分享</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/6b/77bb8501.jpg" width="30px"><span>丫头</span> 👍（0） 💬（0）<div>gitlab搭建&#47;安装好后，如何通过域名让团队其他人员使用？真正的为团队协作赋能。</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/93/4f/61edeea6.jpg" width="30px"><span>Ac、</span> 👍（0） 💬（1）<div>这套方案能用在其它开发语言吗？比如：go、PHP</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/86/655307b3.jpg" width="30px"><span>江湖小虾</span> 👍（0） 💬（0）<div>谢谢，老师的分享</div>2018-09-22</li><br/>
</ul>