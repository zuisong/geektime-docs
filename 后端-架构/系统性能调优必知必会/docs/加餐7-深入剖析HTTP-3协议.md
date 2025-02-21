你好，我是陶辉，又见面了。结课并不意味着结束，有好的内容我依然会分享给你。今天这节加餐，整理自今年8月3号我在[Nginx中文社区](https://www.nginx-cn.net/explore)与QCon共同组织的[QCon公开课](https://www.infoq.cn/video/VPK3Zu0xrv6U8727ZSXB?utm_source=in_album&utm_medium=video)中分享的部分内容，主要介绍HTTP/3协议规范、应用场景及实现原理。欢迎一起交流探讨！

自2017年起，HTTP/3协议已发布了29个Draft，推出在即，Chrome、Nginx等软件都在跟进实现最新的草案。那它带来了哪些变革呢？我们结合HTTP/2协议看一下。

2015年，HTTP/2协议正式推出后，已经有接近一半的互联网站点在使用它：

[![](https://static001.geekbang.org/resource/image/0c/01/0c0277835b0yy731b11d68d44de00601.jpg?wh=1188%2A796 "图片来自：https://w3techs.com/technologies/details/ce-http2")](https://w3techs.com/technologies/details/ce-http2)

HTTP/2协议虽然大幅提升了HTTP/1.1的性能，然而，基于TCP实现的HTTP/2遗留下3个问题：

- 有序字节流引出的**队头阻塞（**[**Head-of-line blocking**](https://en.wikipedia.org/wiki/Head-of-line_blocking)**）**，使得HTTP/2的多路复用能力大打折扣；
- **TCP与TLS叠加了握手时延**，建链时长还有1倍的下降空间；
- 基于TCP四元组确定一个连接，这种诞生于有线网络的设计，并不适合移动状态下的无线网络，这意味着**IP地址的频繁变动会导致TCP连接、TLS会话反复握手**，成本高昂。

而HTTP/3协议恰恰是解决了这些问题：

- HTTP/3基于UDP协议重新定义了连接，在QUIC层实现了无序、并发字节流的传输，解决了队头阻塞问题（包括基于QPACK解决了动态表的队头阻塞）；
- HTTP/3重新定义了TLS协议加密QUIC头部的方式，既提高了网络攻击成本，又降低了建立连接的速度（仅需1个RTT就可以同时完成建链与密钥协商）；
- HTTP/3 将Packet、QUIC Frame、HTTP/3 Frame分离，实现了连接迁移功能，降低了5G环境下高速移动设备的连接维护成本。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（6） 💬（1）<div>基于udp协议而不是tcp的五元组，我在mosh上是尝到了甜头的。
mosh好像之前也是谷歌的人搞的，可惜现在好像没继续维护了。

以前的ssh在网络出现中断后，就需要重连。
而mosh中只要服务器和客户端没重启，就可以一直连。即使电脑休眠了都没关系。
这样，只要电脑能一个月不重启，那么一个月内都不要用重新连接服务器了。

如果再配合终端复用利器（比如tmux）和vim，简直不能再完美了。
下班时合上电脑，工作时打开电脑，之前的工作环境都还在，vim还保持着之前的打开状态。

话说这个终端复用利器还是跟着老师的nginx专栏学到的。老师当时好像用的是screen。</div>2020-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5d/b5/803c9e7a.jpg" width="30px"><span>梦想歌</span> 👍（3） 💬（1）<div>干货！正好看了wireshark视频课的 http 协议，老师后面还会有其他课程吗？</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>安全的基础是网络，哪怕系统监控做到极限。最近开始重修之前报的老师的课，老师对于Nginx和Http协议的理解很透彻彻底，虽然之前的学习大多没有修完，不过都是带着问题去学习，收益还是不错的，而且定期重温总有不一样的收获。
老师若有公众号之类的可以放出，让大家可以和老师学习交流，或者看看后面哪次GOPS老师会去，去和老师学习交流。</div>2021-09-03</li><br/><li><img src="" width="30px"><span>Geek_1386e9</span> 👍（0） 💬（0）<div>感谢老师加餐分享，收益良多</div>2020-08-29</li><br/>
</ul>