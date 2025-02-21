你好，我是七牛云许式伟。

前面几讲我们聊到桌面软件开发，是从原生应用（Native App）角度来讲的，我们的讨论范围还只是单机软件，没有涉及网络相关的部分。

虽然介绍 Model 层的时候，我拿基于数据库实现 Model 层来谈常见的两个误区，但这只是因为这种问题经常能够见到，比较典型。实际纯单机软件很少会基于数据库来做，通常是自己设计的内存中的数据结构。

## 浏览器

今天开始我们聊聊浏览器。从商业价值看，浏览器带来的最为重大的进步是如下这三点。

**其一，软件服务化。**当产品交付从单机软件转向云服务后，社会分工就发生了巨大变化。

互联网让 “24 小时不间断服务”成为可能。任何一个环节的力量都得到百倍乃至千倍的放大，都有可能成长出一个超级节点，进而吞噬上下游，让服务链条更短。

**其二，随时发布。**这极大改进了软件迭代的效率。人们快速试验自己的想法，不必过度因为顾虑软件质量召回而束手束脚。

**其三，跨平台。**浏览器消除了不同操作系统平台的差异性，让一份代码到处运行成为可能。

不过我们今天把重心放到界面开发这个视角。**从作为界面开发框架的角度看，浏览器带来的最重大变化又是哪些？**

![](https://static001.geekbang.org/resource/image/b8/c5/b8063e7ac32e854676b640c86d4628c5.png?wh=1841%2A1172)

**其一，操作系统的窗口系统被颠覆。**一个网页只是一个窗口，不再有父子窗口。所有网页中的界面元素，都是一个虚拟视图（Virtual View），无论是大家耳熟能详的通用控件（比如 input，image，div 等等），还是自绘窗口（canvas）都一样。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/d3/b2/5da80ecc.jpg" width="30px"><span>热海</span> 👍（8） 💬（2）<div>许老师, 我在前面11.多任务:进程,线程与协程 中, 对&quot;从操作系统内核的主线程来说，内核是独立进程，但是从系统调用的角度来说,操作系统内核更像是一个多线程的程序,每个系统调用是来自某个线程的函数调用.&quot; 这个说法不是太理解?
1. 从操作系统内核的主线程来说,内核是独立进程.  这个说法, 就是说操作系统内核就是一个多线程的进程,这些线程没有用户态的地址空间; 内核的各个线程共享3G~4G的地址空间, 共用一份内存地址映射表;这样理解对吗?
2.从系统调用的角度来说, 操作系统内核更像是一个多线程的程序,每个系统调用是来自某个线程的函数调用.  这里我有些困惑. 比如, 应用程序A, 运行起来是一个进程A, 其中通过系统调用进行操作系统内核执行代码时, 这时使用的是谁的堆栈?是进程A的堆栈, 还是操作系统进程的堆栈? 我的理解进程A应该有用户态堆栈, 但是有没有内核态堆栈?这个内核态堆栈是属于进程A还是操作系统进程的堆栈?这个地方没有理解?请帮忙解惑.</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b9/8d/00bded19.jpg" width="30px"><span>不温暖啊不纯良</span> 👍（4） 💬（1）<div>看了老师这篇文章之后，我突然有个启发，人在沉浸于自己的小宇宙造火箭的时候，也不要忽略外界的发展，更需要关注自己的同行，和在未来有可能跟自己所造的火箭产生竞争关系的行业。</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6f/f9/77c7cca7.jpg" width="30px"><span>Null</span> 👍（3） 💬（1）<div>现在搜facebook libra, 好像是已经宣告失败了。</div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/32/36c16c89.jpg" width="30px"><span>Geek_osqiyw</span> 👍（47） 💬（3）<div>做到CEO的技术大牛，认知高度和广度，看问题的视角，确实让人耳目一新。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/c2/e9fa4cf6.jpg" width="30px"><span>Charles</span> 👍（24） 💬（1）<div>Google在某些方面像是“烂好人”，相信技术改变世界，造福人类。
腾讯微信就自私商业化一些，哪怕有研究院，核心技术永远也只是服务自己的公司，相信有用户世界就是我的。
</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/97/6c1e90f1.jpg" width="30px"><span>Eason</span> 👍（8） 💬（0）<div>由命令行，到GDI，到浏览器，到小程序。由浏览器到小程序这一步，技术上我们最能适应，因为整个UI开发的基础框架技术没有很大变化，但是背后的理念感觉却发生了很大变化。许老师文章我都看好几遍，感觉里面有些不少东西值得我学习思考，看一次是get 不到的。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/71/ed/45ab9f03.jpg" width="30px"><span>八哥</span> 👍（4） 💬（0）<div>Facebook本身账户体系有了，现在推出Libra，有了支付体系。之前Facebook已经有开放平台，（App Store），加上PWA。国外可能走了国内不相同的路线。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/d3/c273ee50.jpg" width="30px"><span>程序员Artist</span> 👍（2） 💬（0）<div>自始至终的不看好小程序，尤其是中国产小程序。各大商业公司是放心把命交给操作系统还是一个商业公司的APP呢？中国一堆小程序平台协议也不可能统一。从商业和技术角度都不可能成功。最多就是一个极小的场景补充。</div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/cd/2c513481.jpg" width="30px"><span>瀚海星尘</span> 👍（2） 💬（1）<div>小程序技术本质还是web，不同的是微信对它的管理模式相当创新，一种很有创意的组织模式。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/e1/b7be5560.jpg" width="30px"><span>sam</span> 👍（2） 💬（0）<div>看到了一场新的战争，PWA+Libra，最终赢家Facebook。

对于应用开发商也是多了一个安全保障，不必押注微信小程序一家。无论如何，平台之争都是激烈的。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/4b/6f/50be543b.jpg" width="30px"><span>景南鑫 Rock.J</span> 👍（1） 💬（0）<div>纬度太高，这讲不适合初级架构听，涉及的技术太少。高阶视角，。
</div>2021-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/b6/fcf322a7.jpg" width="30px"><span>antipas</span> 👍（1） 💬（0）<div>想起了凯文凯利的”失控“理论，世界会越来越 多中心化且具有分布式智能，创新来自于被创造者，造物主和被创造者共享控制权同呼吸共命运</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/81/2127e215.jpg" width="30px"><span>梦醒十分</span> 👍（1） 💬（0）<div>许老师的文章质量高呀！</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>刀刃，永远是两面的。
--记下来</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（0） 💬（0）<div>许老师，我想了解下，浏览器作为操作系统做了哪些事情，为应用开发提供了哪些能力？微信作为toC平台，它提供的小程序接口，和浏览器做的事情有什么本质差别？</div>2023-03-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRXEzxNmtrLYrwP3miawZdzYDiczib2GPsSKk5pbjFEIk1PmMiaWHviaqk7YvQbraA4s6BbibLeWTpOvbA/132" width="30px"><span>fjf--</span> 👍（0） 💬（0）<div>虽然好多还是一知半解，但是开阔了眼界</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/4a/a145c675.jpg" width="30px"><span>张浩_house</span> 👍（0） 💬（0）<div>大佬看问题就是深入～</div>2020-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（0） 💬（0）<div>许老师对go语言的预测就很精准，期待对PWA的预测结果！</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/77/3a8fb89f.jpg" width="30px"><span>活水</span> 👍（0） 💬（0）<div>学习下libra和pwa,听过名字，现在看了意识到原来是要这么做的原因，嗯，保持好奇心。</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a4/58/8d2ba4b2.jpg" width="30px"><span>dxdingdu</span> 👍（0） 💬（0）<div>许总的视野真是高!</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/8f/ad6039b6.jpg" width="30px"><span>沫沫（美丽人生）</span> 👍（0） 💬（0）<div>从应用分发的角度，我们放弃了PWA而转向了微信小程序。小程序有对存储空间的严格限制，无法在本地缓存数据，会很消耗用户的流量，不知道许老师在这方面有没有好点建议。谢谢！</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f1/12/7dac30d6.jpg" width="30px"><span>你为啥那么牛</span> 👍（0） 💬（0）<div>我觉得还是PWA更有远见，国内太浮躁，小程序最终还是依靠浏览器，浏览器依赖OS。就像webos一样，腾讯多么想收购的那个手机操作系统</div>2019-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/25/75be8cdf.jpg" width="30px"><span>Halohoop</span> 👍（0） 💬（0）<div>卧槽～这文章看得我又都快s了～</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/20/b7/bdb3bcf0.jpg" width="30px"><span>Eternal</span> 👍（0） 💬（0）<div>最后老师的预言听得新潮澎湃，期待大佬的厮杀，这样小菜才有机会</div>2019-07-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqsQxqMHibXJMAFpXibKuoIPicm9SVMPaSfmPzBXpdGicS4s7nY7CEfeKs40vNh4g9Ic2t7Lcz1iasSic8Q/132" width="30px"><span>Geek_a06b28</span> 👍（0） 💬（0）<div>许老师，在设计生产交易系统架构和数据分析系统架构（含大数据平台），有以下问题咨询您:
1、2种系统在总体、应用、数据、技术架构等纬度在设计的时候需要注意哪些关键的点？
2、两者之间如何实现有效且良好的衔？
3、如果使用数据服务平台是需要2个还是1个即可呢？
期待您的回复。</div>2019-07-13</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>感觉小程序类似云上的SaaS服务</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/af/c9/d9c72c60.jpg" width="30px"><span>MindController</span> 👍（0） 💬（0）<div>长见识了，激动人心</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/08/4d3e47dd.jpg" width="30px"><span>Aaron Cheung</span> 👍（0） 💬（0）<div>起床打卡23</div>2019-07-09</li><br/>
</ul>