你好，我是葛俊。今天，我来和你聊聊研发环境的问题，也就是如何才能让开发人员少操心环境，甚至不操心环境。从这篇文章开始，我们就一起进入工程方法模块了。

在[第5篇文章](https://time.geekbang.org/column/article/129857)关于“持续开发”的讨论中，我与你介绍了获取开发环境是开发工作的核心步骤之一，对提高研发效能来说是非常值得优化的环节。当时，我与你提到了开发环境服务系统以及沙盒环境，解决了开发环境的准备工作。

而这里的“开发环境”只是研发环境的一部分，特指开发机器环境，包括开发机器的获取、网络配置、基本工具以及代码的获取和配置。今天，我们就来看看整体的研发环境的配置问题，从全局上切实解决开发人员因为操心环境而导致的效能低下。

在此之前，你可以先回忆下是否对以下问题似曾相识呢？

- 开发人员使用的电脑配置太低，运行太慢，编译一次要10分钟；
- 测试环境不够，上线时熬夜排队等环境；
- 工具零散，不成系统，很多步骤需要手动操作，开发思路常常因为流程不连贯而被打断；
- 团队成员的环境设置参差不齐，有个别开发人员环境配置得比较好，效率比较高，但没有固化下来，其他团队成员也用不上。

这些问题，实际上都可以归结为研发环境不够高效。就像低劣的空气质量和食物质量会影响我们的身体健康一样，不理想的研发环境会严重降低研发效能。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/65/203298ce.jpg" width="30px"><span>小名叫大明</span> 👍（16） 💬（2）<div>我看到了个人认为比较重要信息: Facebook认为人力成本更高，这个意识比较重要，很多公司没这个意识，有这个意识的确是通过延长工作时长来补，加班及长期加班又降低了非工具和环境造成编码效率，恶性循环。 

慢慢理解招聘时多研发自驱，兴趣等能力的重视的原因了。哈哈</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/ab/fcf0cec4.jpg" width="30px"><span>寒光</span> 👍（6） 💬（1）<div>想问下老师，“一图胜千言”的解决方案有没有对应的开源产品呢？现实中这个问题太烦人了，好多流程管理系统对图片不友好，word文档又太麻烦，不好管理。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（1）<div>我办公用的电脑，显示器，键盘，触控板都是我自己花钱买的。
公司配的比较差。</div>2019-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/38/ba6a106f.jpg" width="30px"><span>Phoenix</span> 👍（2） 💬（1）<div>说到痛点了，换过两家公司，都是考虑低成本，仅仅勉强提供可用的电脑配置，又以网络安全为由不准员工自己带电脑，结果就是下面的开发机器卡，慢，死机，领导天天在讲敏捷开发，高效，请问这种情况老师有什么破局之道吗？</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/45/bf0ed816.jpg" width="30px"><span>大磊</span> 👍（2） 💬（1）<div>Facebook的IDE没有使用那些商业的软件吗，比如jetbrains的，免费的vscode等，我感觉这些很好用啊😂</div>2020-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（2） 💬（1）<div>关于研发环境的高效性，我目前的工作中是用资源池的方式，可以在几分钟内获取一套自定义的虚机，通过加载项目维护的Docker镜像，可以在半小时内搭建一套完整的环境。
但这种方式对于小型公司来说，有没有成本来创建和维护这样一套环境？从技术人员的角度来看，这样做很有价值，从公司长期发展的角度来说，也是有必要的。但是很多公司 不是互联网公司，它们可能是很传统的软件公司，平时没有高并发之类的需求，例如政府相关的项目，这种类型的项目，很多时候在现场开发，机器都不是自己提供的。这种情况很难保证研发环境的高效。
当然，这也许只是一个借口，用来发牢骚，我们应该抓住工作中任何机会去改善和提升。

关于思考题中的截屏，这是非常有价值的一个做法，特别有时涉及到不同组沟通讨论的时候，截图是很好的证据。我们的解决方案和你说的差不多，涉及到不同的工具，处理方式不太一样。
1. 如果工具本身支持图片存储，例如ZenHub或者JIRA，我们用工具本身来存储图片。
2. 如果工具本身不支持图片存储，我们用公司提供的网盘来存储图片，在工具中引用相关的链接。</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/ab/fcf0cec4.jpg" width="30px"><span>寒光</span> 👍（2） 💬（1）<div>截图的这个处理方法的确很赞👍</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（1） 💬（2）<div>做到研发环境的高效性，一个基本的前提就是要意识到人的价值，人比软硬件更有价值。
如果认识不到这一点，文章中说的这些内容，会很难推动。</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>其实做到这样还是需要公司自己内部有个为开发服务的运维团队的，至少要有几个岗。感觉这个在大部分中小公司不现实....</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/22/8bb1640f.jpg" width="30px"><span>oillie</span> 👍（0） 💬（1）<div>我一般都是在jira里贴图的，然后把jira链接放到commit message里</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（0） 💬（2）<div>之前想在公司应用trunk base的代码管理，发现总会跟别人的代码产生冲突，但每个人负责的模块不同，按理不应该冲突才对。学到这里恍然大悟，我们的开发环境和测试环境混合在了一起，并且代码没有及时同步！由于我们是一个机器人团队，每台机器人既是开发环境也是测试环境，大家通常会在机器人上进行开发，但机器人没办法分配给每人一台。

代码分散在了不同的测试环境中，没有及时同步到仓库，而测试环境又是大家共享，当同步代码时就不可避免地产生了冲突。
</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/cf/f2c7d021.jpg" width="30px"><span>李双</span> 👍（0） 💬（1）<div>都是基于长远考虑，学习了</div>2019-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/8d/e07c8b7c.jpg" width="30px"><span>刘晓光</span> 👍（0） 💬（1）<div>请教一个问题，开发机能够快速分配，有没有回收的策论？能给介绍一下么？</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>让开发流程顺畅，不阻塞，就等于是提高了效率，提升了研发效能，而且这种提升是每个开发者，员工能立即享受到的提升。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/8b/fdb853c4.jpg" width="30px"><span>Weining Cao</span> 👍（0） 💬（1）<div>我们现在遇到的一个问题是线上测试资源不够。因为我们发布的软件要支持mac系统，可是目前没有找到合适的提供mac虚拟机的服务商，可是买mac硬件又很贵。。。所以现在大部分mac环境提测的job都会长时间排队。。。</div>2019-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/a7/db7a7c50.jpg" width="30px"><span>送普选</span> 👍（1） 💬（0）<div>葛老师，问下测试数据环境有好的方法么？比如使用docker容器初始化MySQL实例或测试数据，测试完成后容器里的数据自动随容器销毁，不会遗留问题污染数据环境，谢谢</div>2021-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqcb9ibDU3etVicvJJSgvWyh0Bpo0j40l3FXzjJoZYla29icEjpzw3x0aBb1cpGfWibUMeg3KSQ3ELmaQ/132" width="30px"><span>Geek_ocu3ef</span> 👍（0） 💬（0）<div>我看新闻，说是facebook已经在2018年停止维护Nuclide&#47;Atom-IDE了，转投vscode了，vscode可以利用remote插件远程登录到数据中心的开发机上开发，速度很快，目前没有发现什么卡顿的情况，感觉这个玩意很好用。</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/4d/2116c1a4.jpg" width="30px"><span>Bravery168</span> 👍（0） 💬（0）<div>好的研发基础支撑工具和环境对于提高研发效率，真的是非常重要。</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ff/52/093bb1a1.jpg" width="30px"><span>小包</span> 👍（0） 💬（0）<div>第二个例子是，我为一个云产品团队提供联调环境。这个云产品结构非常复杂，有十多个服务，至少需要 3 台服务器；不但有软件，还有数据、组网等复杂的设置，部署很困难；更严重的问题是，这个环境一旦损坏就很难修复，需要从头再来，所以开发人员自己配置基本不可能，运维人员也是忙于维护，应接不暇。
----------------------------------
我们的环境及遇到的问题跟这很类似，机器池如何组建能否详细说明下，非常感兴趣
如果一套环境需要3台机器，要保持两套空闲可用的环境，那么这个机器池需要多少准备多少机器呢，具体如何操作的呢？</div>2021-04-21</li><br/>
</ul>