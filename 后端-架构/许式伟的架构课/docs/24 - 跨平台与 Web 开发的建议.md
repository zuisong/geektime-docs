你好，我是七牛云许式伟。

上一讲我们聊了浏览器，以及移动浏览器之争：小程序与 PWA。

当我们思考浏览器从技术上带来了什么的时候，我们可以把它分为两点。

- 跨平台桌面程序开发；
- Web 开发（B/S 架构的新型应用）。

今天我们分别就跨平台桌面程序和 Web 开发展开来聊一聊。

## 跨平台桌面程序开发

跨平台的桌面程序开发是一个超级难题。无数人前仆后继，各种方案层出不穷，但至今为止，仍然没有称得上真正深入人心的解决方案。

原因很简单，因为桌面程序本身的范畴在变。有两个关键的因素会导致桌面开发产生巨大的差异性。

一个因素自然是操作系统。不同的操作系统抽象的界面程序框架并不一致。这些不一致必然导致开发工作量的增加。

放弃某个操作系统，就意味着放弃某个流量入口，也就意味着放弃这些用户。所以虽然很麻烦，我们还是不得不支持着每一个主流的操作系统。

另一个因素是屏幕尺寸。就算相同的操作系统，在不同尺寸的屏幕上，交互的范式也会存在很大的差异性，这也会导致不低的跨平台工作量。

首先我们看下操作系统。

- PC 本地：Windows，macOS，Linux 等等；
- PC Web：Chrome，Safari，FireFox 等等；
- Mobile 本地：Android，iOS 等等；
- Mobile Web：小程序，PWA 等等。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（43） 💬（3）<div>因为工作的原因，莫名其妙的成为了大前端的一员，从Windows原生直绘界面到基于Qt的Web混合开发，再到Flutter移动跨平台，一路走来是越来越惊讶，前端的知识体系气泡越吹越大，突发学海无涯之感。不过我也一直在思考那么不变的东西，从框架的架构角度理解，它们其实是借鉴和传承的，因此不论是使用C++还是JS或者Dart，貌似都不再是难题了。学习架构课不一定就是奔着学完做架构师去的，也是为了更好的把自己的知识体系串通组建起来，没必要在开发语言的细节泥潭里无法自拔</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/ce/462c2309.jpg" width="30px"><span>笛神</span> 👍（21） 💬（6）<div>关于model层，一直认为使用spring框架的开发人员把service+dao用的太狭隘了，service堆满了业务处理，定义各种方法，感觉完全变回面向过程编程，丢掉了业务实体类，丢掉了数据行为封装，存在很多的耦合和重复。。一直想灌输将行为封装回业务实体里，service驱动业务实体来实现业务，而不是把所有业务逻辑在service层来实现掉。这样model层才会丰满，才是对现实世界的抽象，不知这个理解是否正确？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（19） 💬（3）<div>model和viewmodel的本质区别是什么？老师</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/8d/ab469ad5.jpg" width="30px"><span>黄强</span> 👍（15） 💬（2）<div>认真对待Model层，将其做厚，相应的前端会更薄，更能适应变化的可能，再次体现架构师对稳定点，变化点的抉择</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/97/abcd222a.jpg" width="30px"><span>杨洪林</span> 👍（8） 💬（1）<div>server 架构下的automation 具体指那些动作？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8d/65/633a7478.jpg" width="30px"><span>ANYI</span> 👍（4） 💬（2）<div>“”Model 层做厚”，老师，这个应该怎样去理解处理，很多现在项目都固化了，model就是对应了数据库表，通过service来处理业务，就是spring mvc这种分层，怎样去把这个model做厚呢？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b9/8d/00bded19.jpg" width="30px"><span>不温暖啊不纯良</span> 👍（3） 💬（2）<div>是不是mvc的设计思想，在前后端都有应用。

前端的mvmc中的model指的是将用户行为产生的数据抽象成业务数据，比如说表单的填写就是，提前给用户设计好了业务模型，然后用户将数据输入这个模型，viewModel负责窗口的渲染,presenter是负责数据的存取。

后端的mvc中的model指的是实体类，实体类是对业务的封装和模型化……只能编到这里了，

重新理解一下，原来的桌面应用开发，在以前还没有前后端分离这一说，所以mvc应该涵盖整个开发流流程……哦，我明白了，整个mvc应该是从业务架构的角度出发去理解它，那么任何应用的架构都是从业务需求开始的，有了业务需求之后，第1个产生的应该就是业务模型，也就是model层，m排第一，然后是我们必须要把业务数据和代码可视化，于是有了view 层，让用户在特定的业务框架中去交互，实行业务操作，生产业务数据，最后把用户这些数据处理和存储，也就是我们的controller 层。

原来mvc架构思想，是对需求的一种抽象的模板。

好了老师，我编完了。</div>2021-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（3） 💬（1）<div>理解起来还是有些吃力，请问能结合一下具体项目吗？最好是某个开源项目</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（2） 💬（1）<div>被MVC，MVP，MVMP绕晕了</div>2019-07-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（2） 💬（3）<div>您好，对model层的理解还是不够，我原先最早认为就是数据结构层，您说把model层做厚的含义是什么？</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/95/90/59446bd9.jpg" width="30px"><span>卢</span> 👍（1） 💬（2）<div>许老师，你好！文中把model层做厚该怎么理解？利用数据库存储过程简化代码逻辑？设计更优的数据结构？没理解做厚是啥意思</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e6/16/7c8ab10c.jpg" width="30px"><span>有只骆驼</span> 👍（1） 💬（1）<div>还是有点迷糊。

在过去的实际开发中，我们对于Model 层的讨论经常在探讨到底是贫血模型还是充血模型。从某种意义上来说，Model 除了不仅不是一层薄薄的的数据载体和简单的行为定义外，还承载着对整个业务对象描述与驱动，概括了业务核心的本身且能被任意需要的合法对象消费。

感觉自从上次GIAC大会后，大佬们都在说领域驱动设计所想表达的思想。

</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/6e/267bd6ee.jpg" width="30px"><span>1900</span> 👍（1） 💬（2）<div>为啥桌面程序员也叫大前端呢？（另外到底啥叫大前端呢？）

我的初步理解是和用户打交道的软件开发叫前端开发，我的理解对么？

最后，有“大后端”这个术语么？如果有，具体又指什么？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/25/1d3d616f.jpg" width="30px"><span>虎哥</span> 👍（1） 💬（1）<div>把多租户的 API 转译成单租户的场景。所以这一层并不需要太多的代码，甚至理论上自动实现也是有可能的。请问哪里有相关资料可以查阅这个内容</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（0） 💬（1）<div>java的MVC和前端的MVC是一回事吗</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（0） 💬（1）<div>prsenter由谁来实现？主体代码运行在哪一侧啊？</div>2023-03-29</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（1）<div>Session-based Model 和 浏览器一侧的 Model是怎么交互的，没太明白。</div>2020-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gmP4Yh00MZPwNvr4UQdLeXaX3TVyZEEp195S3vD3Sfl1xz5jBr1474Mt6w5OPr0KsrnQObfLRy5PkKNFjSBiasA/132" width="30px"><span>大头爸爸</span> 👍（0） 💬（1）<div>”但是一旦数据在 Server 端，数据可靠性的责任方就到了软件厂商这边。如果厂商不小心把数据搞丢了，
用户就会跳起来。“
请问这里的软件厂商是浏览器这边还是服务器这边?</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/a4/813c4685.jpg" width="30px"><span>小鬼</span> 👍（2） 💬（0）<div>现在再回想起来，看看许老师以前在WPS的架构设计，其实沿用了很多年，包括后来我们在移动端还有Web端重新实现一遍，包括层次划分和模型，基本还是复用PC那套。
从这个角度来看，做厚Model的价值就体现出来了，在不同平台上，Model是稳定的，可以快速展开工作，换种开发语言和平台，也只是再结合平台的特性去处理细节。</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（0）<div>老师真全能</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（1） 💬（0）<div>浏览器解决跨操作系统问题
本质上要求其它系统服务对外提供一套标准
未来云也会有一套标准，云上的中间件会基于这个标准构建</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8f/3a/b15e7392.jpg" width="30px"><span>呼啦啦~</span> 👍（0） 💬（0）<div>在B&#47;S架构下，MVMP中的P，物理是是存在B端还是C端的？以及presenter具体是什么？</div>2024-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/5a/574f5bb0.jpg" width="30px"><span>Lukia</span> 👍（0） 💬（1）<div>“在服务端，Session-based Model 和 Session-based ViewModel 并不发生直接关联，它们通过自己网络遥控浏览器这一侧的 Model 和 ViewModel，从而响应用户的交互。”关于这一点有几个问题请教老师。1. 为什么在服务端和浏览器分别都会有mode和view model层 2.如果说viewmodel是考虑到表现，对model层的转译，那么model是不是应该在服务端同时view model在浏览器端呢 3. </div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/47/a4be64d8.jpg" width="30px"><span>Liber</span> 👍（0） 💬（0）<div>Electron为什么入选进表格中？</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/08/4d3e47dd.jpg" width="30px"><span>Aaron Cheung</span> 👍（0） 💬（0）<div>迟到的打卡24</div>2019-07-15</li><br/>
</ul>