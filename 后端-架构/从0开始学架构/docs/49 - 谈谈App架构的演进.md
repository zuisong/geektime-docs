专栏截止到上一期，架构设计相关的理念、技术、实践已经基本讲完，相信你一路学习过来会有一种感觉，这些内容主要都是讲后端系统的架构设计，例如存储高可用、微服务、异地多活等，都是后端系统才会涉及。事实上确实也是如此，通常情况下我们讲架构设计，主要聚焦在后端系统，但这并不意味着App、前端就没有架构设计了，专栏所讲述的整套架构设计理念，虽然是来源于我的后端设计经验，但一旦形成完善的技术理论后，同样适应于App和前端。

首先，先来复习一下我的专栏所讲述的架构设计理念，可以提炼为下面几个关键点：

- **架构是系统的顶层结构。**
- **架构设计的主要目的是为了解决软件系统复杂度带来的问题。**
- **架构设计需要遵循三个主要原则：合适原则、简单原则、演化原则。**
- **架构设计首先要掌握业界已经成熟的各种架构模式，然后再进行优化、调整、创新。**

复习完我们就可以进入今天的正题，我来谈谈App架构的演进，以及上面这些架构设计关键点是如何体现的。

## Web App

最早的App有很多采用这种架构，大多数尝试性的业务，一开始也是这样的架构。Web App架构又叫包壳架构，简单来说就是在Web的业务上包装一个App的壳，业务逻辑完全还是Web实现，App壳完成安装的功能，让用户看起来像是在使用App，实际上和用浏览器访问PC网站没有太大差别。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/dd/912b52ed.jpg" width="30px"><span>李奋斗</span> 👍（83） 💬（6）<div>端上的技术，山上的天儿，都变得太快。端上的架构怎么演进？我觉得要把答案交给想象力，把时间尺度拉大看，想象力才是端上复杂度的主要来源，交互革命和场景升级是端技术栈发展的重要推动力。鼠标的发明，颠覆了命令行的交互思维，iphone的问世，分分钟让习惯了上屏下键的人们大开眼界，手机和网络的突进，解锁了一堆令人兴奋的场景。VR，混合现实，AI，5G等技术都可能极大推进端技术的变革，未来端架构怎么演进？不清楚，但有一点是清晰的，一大波复杂度，就在路上。</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/e2/3de4371d.jpg" width="30px"><span>江龙</span> 👍（69） 💬（2）<div>有个api的设计原则问题最近困扰好久，请教下，就是图中的首页其实有多个资源聚合，那是应该app端去请求多个资源服务，然后聚合出来展示；还是有个后台服务去聚合后端的各个基础服务，然后只提供一个接口给app访问？这其中的粒度如何把握？</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/e1/a05a9e22.jpg" width="30px"><span>kyll</span> 👍（18） 💬（3）<div>其实，对于现在很多业务应用强制将用户绑到移动端很是反感。举个例子，第一次用丰巢寄件，竟然花了半小时，注册很麻烦。有些餐厅强制手机点餐，在pc端登录强制扫二维码，也很无语。多设备多渠道本质应该是为了方便快捷，随时随地享用服务。任何设备都有局限性，做好自己的本职即可。</div>2018-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/de/17/75e2b624.jpg" width="30px"><span>feifei</span> 👍（16） 💬（3）<div>我认为这个演讲也是朝着 all in one，即平台统一化，在app与原生接口间会出现统一化一个技术，类似java与jvm
原因：
1，原生开发成本高，每个平台都需要专门的开发人员
2，手机性能的提高，能够为平台统一化提供条件
3，用户体验，苹果的生态封闭，体验相对较好，但安卓平台很多公司都封装一套 导致体验差异很大

</div>2018-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqUFIOBnowQQbDZSr7ZcPrbnN6vmD3T0UZ4YrYmgljwlx5OTfqh9BibEqSvba0cuMzicjkkaHadeysQ/132" width="30px"><span>borefo</span> 👍（14） 💬（1）<div>一个系统架构设计出来后，如何预估这个系统能够支撑多大的请求量呢？</div>2018-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK0uyg1IicbEhLwsgM2A2ROoyVdWdmUqZfQfs6G67w9m3hdRNBMOQJatQoACj3qNGgj2KVIgricaYiaQ/132" width="30px"><span>木得感情的编码机器</span> 👍（9） 💬（1）<div>曾经做过一个移动端社交项目，开始就是用react native 开发的，但是工程里还是用了些原生的库和代码，而且是IM和拍照美化这两个核心功能。所以开发时既要边学边写原生代码，还要写RN，而且一旦RN在真机上报错，debug就是一头包。项目内测时就发现了RN光启动什么也不干就用掉了100多M内存，而且拍照美化是原生加RN，性能非常差。
内测之后就抛弃了RN，两个程序员很快就把安卓和苹果两个原生版本做出来了，因为很多原生代码可以复用，而且原生也有很好的开发框架和模式，调试非常方便和清晰。
我总结一下，是否用跨平台的方案取决于业务。如果做资讯类，信息聚合类，电商类对性能不苛求的项目，用RN这类东西完全可以。如果是游戏类，协同工具类，拍照视频类这些对性能有极高要求的，还是得用原生去开发，必要时也可以配合H5混合实现活动、任务、促销等业务。
未来前端的发展肯定是越来越复杂的，但要出现真正大一统跨平台开发框架还是需要很长一段时间，但是我这个东西一定是出至谷歌或苹果，而不会是FB或者其他大厂。现在有flutter ，但是说不准哪天swift 也能写安卓。</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/ec/804c3900.jpg" width="30px"><span>Niuniu</span> 👍（7） 💬（1）<div>我的观点可能有点相反，但凡有人上来要做native app的时候，我一般都劝退不劝进。先仔细想想你需要的那些功能WebApp能不能实现，用户体验有没有差很多，没有的话，没必要做native app。能上webapp，先上webapp，人手不够时间紧，可以考虑hybrid，实在是非native app不可，才考虑写native的。</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（5） 💬（1）<div>分久必合，安卓和IOS终将大一统为跨平台 App</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/03/9ea1ce01.jpg" width="30px"><span>大鹏</span> 👍（4） 💬（1）<div>架构设计首先要掌握业界已经成熟的各种架构模式，然后再进行优化、调整、创新。——这句话点拨了我，我自己在工作当中，往往忽略了这一点。事实大家都知道，但架构的原则会避免我们钻牛角尖</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5f/aa/63e641c1.jpg" width="30px"><span>H</span> 👍（4） 💬（1）<div>有一个疑问，虽然在这节中提问不太合适哈哈哈。
疑问：如果一次mysql查询中，涉及到7-8个表的联合查询。就是join查询。除了暴力查询方法外，有没有其他办法？比如合表，把多个字段数据合在一起，放在一个表中。这样子可以吗？如果不对，望作者指正</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/5c/3f164f66.jpg" width="30px"><span>亚林</span> 👍（4） 💬（3）<div>前端技术茫茫多，所以我转后端了</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/b9/1b63042a.jpg" width="30px"><span>天外来客</span> 👍（3） 💬（2）<div>未来app必然朝着更好的用户体验，更快的开发速度方向发展，考虑到Android和iOS都是基于Linux底层，可能会出现一个平台层隔离两者的差异，提供统一的移动端系统API供开发者使用，希望这一天早点到来</div>2018-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/3a/b0454322.jpg" width="30px"><span>Eric</span> 👍（2） 💬（1）<div>老师，我想问下 分布式 这种架构也算是面向服务做切分的一种架构模式嘛？我个人理解 分布式服务 有按功能分割的 ，也有按任务计算资源分割的，还是说 分布式 本身是一种扩展方案？我概念上有点乱，不知道老师怎么定义 分布式 这个概念，谢谢</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/20/176d0a3f.jpg" width="30px"><span>陶邦仁</span> 👍（2） 💬（2）<div>未来提供平台化，屏蔽底层原生，正如pc端cs到bs的演进</div>2018-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e1/db/c78ba338.jpg" width="30px"><span>Kliyes</span> 👍（1） 💬（3）<div>微信小程序一统江湖！</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/74/3f/5c9fd08f.jpg" width="30px"><span>李晨</span> 👍（0） 💬（1）<div>个人猜测，会不会类似微软搞的云游戏的方式，计算、交互等动作全都交给后端，然后前端只负责渲染。不过好像这种方式之前就已经存在了</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（1）<div>个人认为，浏览器会统一江湖～</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/60/b7/4a665c73.jpg" width="30px"><span>小鬼爱风雪</span> 👍（0） 💬（1）<div>恰好从最开始的原生，到h5再到ST的混合开发框架，最后经历rn都参与过，现在感觉weex被明确放弃了，flutter 和rn成了主流，小程序的更高层面的抽象出现，仿佛又回到了大前端的概念，感觉移动端演进会继续向着大统一的趋势进行，后面swift 语法的变化和新鸿蒙出现都会让开发者更简单趋势进行。</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/41/f6153c7a.jpg" width="30px"><span>Dwyane</span> 👍（0） 💬（1）<div>又回来看👀</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1b/70/547042ee.jpg" width="30px"><span>谭方敏</span> 👍（0） 💬（1）<div>架构是系统的顶层结构
架构设计的主要目的是为了解决软件系统复杂度带来的问题。
架构设计需要遵循三个主要原则：合适原则，简单原则，演化原则。
架构设计首先要掌握业界已经成熟的架构模式，然后再进行优化，调整，创新。
web app
最早的app有很多采用这种架构，就是在web的业务上包装一个APP的壳，业务逻辑完全还是web实现，APP壳完成安装的功能，让用户看起来使用APP，实际上和用浏览器访问pc网站没有太大差别。

在当时PC互联网还是主流，移动互联网还是新鲜事物，当时的业务中心还在PC互联网上，移动互联网上大都是尝试为主，为了快速和低成本，就有web app这种架构，虽然Android和iOS都已经有开发APP的功能，但原生成本太高。

原生APP
虽然web app 解决了快速开发和低成本，随着业务发展，web app 的劣势比较明显：
1）web app体验比原生app体验差距越来越明显。
2）APP业务逻辑越来越复杂，加剧了Web app体验问题。
3）移动设备在用户体验上有很多优化和改善，web app用不上这些技术技术优势，只有原来APP才行。

Hybrid APP
多平台（Android，iOS，Windows）原生开发不兼容，同样功能在不同平台需要开发一遍，为了解决这个问题，提出了体验要求高的业务采用原生APP实现，对体验要求不高的可以采用web APP方式实现。


跨平台APP
facebook react native ，
阿里 weex
Google的flutter。

APP架构演化方向很难统一，每个厂家都需求不一样，大体来说，需要在体验和减少重复减少上面做平衡取舍，分久必合，合久必分，差不多就是这样的态势。

</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（0） 💬（1）<div>App最后还得是原生，开发多次就只能加人加钱，不然你不开发多次，同类型App发狠开发多次，竞争力就没有了，不过好的是，印度，澳洲，中国都可以接各种App的外包，作为甲方用心做好交互设计比什么都重要</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/99/56f148bc.jpg" width="30px"><span>varotene</span> 👍（0） 💬（1）<div>没太理解前端组件化，容器化，能不能给点课外阅读或者再讲讲</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（0） 💬（1）<div>后面的趋势还是使用统一的架构，一次开发多个平台都能使用，在这个前提下不断优化体验。</div>2018-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d5/3f/80bf4841.jpg" width="30px"><span>文竹</span> 👍（0） 💬（1）<div>跨平台App仍是主要发展方向，此外一些跨平台的App快速设计产品也是主流（比如用Js编写，工具自动转换成原生APP）</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/4c/c5a8b831.jpg" width="30px"><span>商伯阳</span> 👍（0） 💬（1）<div>在app整体做统一，未来一两年内还是比较困难吧感觉，我们目前就是遵守iOS和Android的规则。

就像浏览器厂商对接EcmaScript规范一样，前端开发接入要跟手机厂商，软件版本走，就导致了要打很多垫片补丁才保证了app view层的适配统一。
</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/74/c63449b1.jpg" width="30px"><span>问题究竟系边度</span> 👍（0） 💬（1）<div>我觉得会，定义一个前端展示的实现接口标准，然后不同平台去实现内部展示逻辑。业务逻辑根据接口进行展示调用。 
组件间能够进行部分升级而非整个app升级



我是做后端的，纯属瞎想。。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/ec/abb7bfe3.jpg" width="30px"><span>kevenxi</span> 👍（0） 💬（1）<div>很有收获，是不具体分析几个APP的架构?</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/6b/0b6cd39a.jpg" width="30px"><span>朱月俊</span> 👍（0） 💬（1）<div>后面是否可以结合一个实际开源的项目，再结合前面各种方法论，好好解剖一个流行的分布式开源库? 至少你讲的东西，一般人做起来因为各种原因都不一定做的下去。</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a0/5f/cf72d453.jpg" width="30px"><span>小豹哥</span> 👍（2） 💬（0）<div>2016年刚毕业哪会，好多培训机构都力推安卓和IOS的课程，原来在2013年就是大势所趋了，一个技术的火爆程度有滞后效应，对技术要有前瞻性，还要有快速学习的能力来享受先发红利。</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/6b/f61d7466.jpg" width="30px"><span>prader26</span> 👍（1） 💬（0）<div>架构设计需要遵循三个主要原则：合适原则、简单原则、演化原则。
架构设计首先要掌握业界已经成熟的各种架构模式，然后再进行优化、调整、创新。

app 的演进：
Web App
原生 App
Hybrid App
组件化 &amp; 容器化
跨平台 App</div>2021-04-19</li><br/>
</ul>