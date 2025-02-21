你好，我是何为舟。

在前面两节课中，我们讲了防火墙和WAF的工作模式，以及它们是如何作为内外网的隔离设备，在网络边界进行安全防护的。

但是，无论是防火墙还是WAF，都无法达到100%的防护效果。黑客总是能有很多其他的办法，来隐藏自己或者直接绕过这些保护机制。因此，我们仍然需要对内网中的行为进行检测，及时发现已经入侵到内网中的黑客。这就需要用到IDS（Intrusion Detection System，入侵检测系统）了。

那么，IDS的工作模式有哪些呢？它能够实现哪些功能呢？今天，我们就一起来学习，如何通过IDS进行安全防护。

## 什么是IDS？

IDS的最终目的是检测黑客的攻击行为。那我们应该在哪里进行检测呢？首先是在网络流量中：黑客在控制了一台服务器之后，需要进行权限提升，而权限提升需要黑客在内网中挖掘各个服务器存在的漏洞。因此，黑客会发起很多探测和攻击的网络请求。其次就是在服务器系统中，黑客也可以利用服务器系统或应用本身的漏洞进行权限提升，同时，黑客也会尝试在系统中留下后门，这些行为都是通过系统操作来完成的。

因此，根据检测内容的不同，IDS可以分成两种类型：NIDS（Network Intrusion Detection System，网络入侵检测系统）和HIDS（Host-based Intrusion Detection System，基于主机型入侵检测系统）。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/74/63/ea5ca6ea.jpg" width="30px"><span>拂晓</span> 👍（3） 💬（1）<div>老师，在攻击的视角，如果识别蜜罐？</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（3） 💬（1）<div>IDS、IPS 和蜜罐可以防DDoS吗？</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（1） 💬（1）<div>基于网络的IDS和基于主机的IDS，前者通用性更好，蜜罐讲的很不错，有没有开源的实现</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（7） 💬（0）<div>今天这章内容个人觉得才提到了一些KeyPoint：算是一些真正的技巧性的东西。网络攻击确实现在越来越普遍，单一工具的局限性越来越典型-就如之前曾在课程中提过“安全架构”。
个人觉得工具之间可以合理组合使用：只不过合理性我们需要结合真实生产环境去探索最合适自己企业的安全架构策略以及各工具之间的使用场景与比例；什么样阶段我们需要去使用。如同老师之前课程有提出代码混淆：这个可能就看Coding所在的页面以及对业务的影响。
安全没有绝对只有相对，如同我自己所做的数据系统性能优化和架构设计一样；如何在什么阶段用什么样的策略，后期可能的扩展策略是什么这其实和我们对工具是否使用以及使用比例有密切关系。
谢谢老师的精彩分享：可以站在更高的层次去理解和设计这块的安全问题。谢谢</div>2020-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/d3/bcb7a3fd.jpg" width="30px"><span>半兽人</span> 👍（4） 💬（0）<div>以前也听过安全厂家来推销产品时说的各种术语，但今天才是比较系统的理解了如“蜜罐”等有趣的内容</div>2020-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJcZh2daicchEoY9s2AEzgTcXrz12SUsZPAE5aO0IGGib3pLD862LZpjmFpt8MGEq6a3HmyLqrWvBSw/132" width="30px"><span>冯时</span> 👍（2） 💬（0）<div>防火墙、WAF、IDS、IPS 和蜜罐都是网络安全防御的重要组成部分，它们可以通过不同的协作方式来提供更全面和高效的安全保障。

一种常见的协作方式是防火墙与 IDS&#47;IPS 的协作。防火墙通常是网络安全的第一道防线，它可以检查流量，并根据特定的规则阻止有害流量进入网络。但是，防火墙并不能检测到所有的攻击，因此，IDS&#47;IPS 被用来增强防御能力。IDS&#47;IPS 可以分析网络流量，以及系统日志和其他信息，识别出恶意活动并生成警报。当 IDS&#47;IPS 探测到有害流量时，可以使用防火墙来阻止流量进一步渗透到网络中，从而保护网络的安全。

另一种协作方式是 WAF 与 IDS&#47;IPS 的协作。WAF 是一种基于 Web 应用程序的防护系统，它可以阻止针对 Web 应用程序的攻击，如 SQL 注入、跨站点脚本等。IDS&#47;IPS 可以检测到网络上的任何恶意活动，包括针对 Web 应用程序的攻击，但是它们无法提供像 WAF 那样的深度保护。因此，WAF 和 IDS&#47;IPS 可以协同工作，以提供更全面的保护。

蜜罐是一种特殊的安全工具，它模拟了一个虚拟的攻击目标，以吸引攻击者进行攻击，并捕获攻击者的行为数据。蜜罐不直接用于保护网络，而是用于分析攻击者的行为和技术，以便更好地理解他们的攻击方式并提高网络安全。因此，蜜罐可以与 IDS&#47;IPS 协同工作，以提高 IDS&#47;IPS 的检测精度和响应能力，并为网络安全提供更深入的分析和了解。

总之，防火墙、WAF、IDS&#47;IPS 和蜜罐可以通过不同的协作方式来提高网络安全，防范和阻止针对网络和应用程序的攻击，并收集攻击者的行为数据，以便更好地理解和应对安全威胁。</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/d7/f835081c.jpg" width="30px"><span>bin的技术小屋</span> 👍（1） 💬（0）<div>今天这章内容讲的太精彩了，感觉像是在看孙子兵法似的，读起来非常过瘾，哈哈</div>2020-02-26</li><br/><li><img src="" width="30px"><span>轩呀</span> 👍（0） 💬（0）<div>网络上有的文档好像还不是很全面，就比如：suricata都不知道怎么重启
老师，有一个问题是这样的：在suricata输出的eve.json中，应该怎么过滤掉flow流呀？
（logstash下尝试着新增了一个.conf文件，不知道怎么接收另一个文件夹中的json文件了都）</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（0）<div>学习到一些概念，要是能深入讲一些案例就更好了</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>第一次听说蜜罐 觉得挺高级的</div>2020-03-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJfTnE46bP9zFU0MJicYZmKYTPhm97YjgSEmNVKr3ic1BY3CL8ibPUFCBVTqyoHQPpBcbe9GRKEN1CyA/132" width="30px"><span>逗逼章鱼</span> 👍（0） 💬（0）<div>一直有听说蜜罐，今天终于有实感了知道具体怎么回事了。</div>2020-03-10</li><br/>
</ul>