你好，我是袁武林。

在[第1讲“架构与特性：一个完整的IM系统是怎样的？”](https://time.geekbang.org/column/article/127872)中，我有讲到即时消息系统中非常重要的几个特性：实时性、可靠性、一致性、安全性。实际上，这些特性的实现大部分依赖于通道层的稳定和高可用。

对于即时消息系统来说，消息的通道主要承载两部分流量：一部分是用户发出的消息或者触发的行为，我们称为**上行消息**；一部分是服务端主动下推的消息和信令，我们称为**下行消息**。

由此可见，消息通道如果不稳定，一来会影响用户发送消息的成功率和体验，二来也会影响消息的下推，导致用户没法实时收到消息。

那么，在面对如何保障消息通道的高可用这一问题时，业界有哪些比较常用的优化手段呢？

## 让消息通道能连得上

要保障消息通道的高可用，最基本的是要让通道能随时连得上。不过你可能会觉得，这看起来好像挺简单的，不就是申请个外网虚拟IP，把接入层服务器挂上去，然后通过域名暴露出去就行了吗？

但实际上，这个“连得上”有时真正做起来却不是那么容易的，主要原因在于用户的网络情况复杂性高。比如，有的用户走2G网络来连，有的通过HTTP代理来连，还有的会出现DNS解析服务被封的情况，诸如此类。

此外，移动运营商各种比较奇怪的限制也会导致连通性不佳的问题。因此，要想你的通道能让用户随时都连得上，还需要做一些额外的优化。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（14） 💬（1）<div>假如现在有用户A和B，以及三个接入节点S1，S2和S3，A给B发消息。A和B都查询最优接入节点，分别对应S1和S2节点。A–＞S1最优没问题，但S2–＞B一定是最优的吗？不一定，上下行通道隔离后，查询最优节点是客户端给节点发消息，代表的是该节点的上行通道是最优的，并不代表节点到客户端的下行通道是最优的。</div>2019-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（6） 💬（7）<div>老师，有3点不明白！
1:基于tcp的长链接不是全双工吗？为什么下行会影响上行呢？我的理解是，这里的影响不是通道影响，其实是服务器处理能力的影响，是这样吗？
2:HTTP Tunnel这个东西确实没用过！如果他是基于http的短链接，那它也没法实现一个完整的即时消息系统呀！比如他们拿不到服务器的推送消息！
3:在老师说的把通道和业务隔离上，我明白确实需要这样优化！有一点不明白的是，这里的通道和服务是不是可以理解为链接服务和业务逻辑服务！比如链接服务只管链接，链接服务和业务逻辑通过消息队列解耦！但是如果是这样的话，用户的链接映射维护是在链接服务中呀！不在业务层！
老师的问题，我感觉因为隔离开了，所以就不是“原子”的了，那么就可能存在能发看不到，能看到发不出去的情况</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（5） 💬（1）<div>还有个问题，为什么上行通道不直接使用长连接，而要使用长连接。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/5b/d2e7c2c4.jpg" width="30px"><span>时隐时现</span> 👍（3） 💬（1）<div>上下行通道隔离，消息发送方采用短链接，除了基于http tunnel不适合长连接的考量，还有其他因素吗？
作者提到可避免客户端维护多个长连接的开销，可是单纯的tcp连接应该不会耗费多少资源，和每次都采用短连接相比，还能接受连接不断的创建和关闭的代价。</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/15/070d83ae.jpg" width="30px"><span>Z邦</span> 👍（2） 💬（1）<div>希望老师可以出一篇监控的文章。。感谢感谢</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（2） 💬（2）<div>通道隔离的最大问题个人觉得连接断开时机问题，比如A断开，B什么时候断开，要做跟踪记录</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/b7/57f153f6.jpg" width="30px"><span>Sun Fei</span> 👍（1） 💬（1）<div>两个通道隔离之后，如果消息队列里消息比较多，会不会影响消息的实时性？</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（1） 💬（1）<div>问题1：短链接怎么idle几分钟呢？http不是无状态的吗？
问题2：如果上行通道和下行通道隔离，是不是2者对应两个不同的集群呢？</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（2）<div>既然客户端可以通过跑马竞速，选出一个最快ip链接。为什么服务器要返回一个排序IP列表？客户端还依据这个列表顺序进行判断么？</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（0） 💬（1）<div>上下行通道隔离能够隔离保护我们的消息接收和消息发送，那么通道隔离会不会带来一些负面影响呢？

1.需要维护两个连接，消耗一定客户端性能。
</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（0） 💬（1）<div>HTTP Tunnel在下行通道也会使用吗，如果存在代理的情况，下行通道发送给代理的数据如何再转发给客户端</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（2）<div>考一下讲师：知道为啥14000是安全的吗</div>2021-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/icniaGmw8xiboyC25ic8l7Vf67Czx5s3XiaezApmK13hcia9U33YibpcKHq2iaJwIIoToLwZcoKQoR5dnvTILibMs4ZZ3qQ/132" width="30px"><span>xie</span> 👍（0） 💬（0）<div>老师  可以连上的常见的端口除了你说的那几个还有吗？能否完整列一下</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/f9/5e11442f.jpg" width="30px"><span>阿怪是个笨小孩</span> 👍（0） 💬（0）<div>老师您好，关于上下行通道隔离这里我没太懂，请教一下；
在直播互动中下推消息由于扇出大，比如按照1:9999投递，那投递消息的用户A使用短连和长连有啥区别吗？最后一张图看的有点蒙</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/dd/8098a7e0.jpg" width="30px"><span>阳阳</span> 👍（0） 💬（0）<div>“我们可以通过暴露多个业界验证过比较安全的连接端口”这个比较安全是从什么方面考虑的？既然端口大家都知道这些比较安全，恶意攻击的人不是更加方便去攻击了吗？还是说安全是指这几个端口比较稳定？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/71/895ee6cf.jpg" width="30px"><span>分清云淡</span> 👍（0） 💬（0）<div>主要应该是 上行下行 也就是输入输出之间的同步问题 同时如果按照文中的设计 单个 长链接 上行 如何做到上行之间的有序 去重 重发 就会很复杂 这样 输入之间 输入输出之间 就需要考虑更多的问题</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>老师在第十课的&lt;自动智能扩缩容：直播互动场景中峰值流量的应对&gt;中提到关于上下隔离的优点&quot;能够隔离各自上行操作，避免下行推送通道产生影响，轻量、独立的长连接服务容易扩容。&quot;;坑没踩过，准备等十一长假开始自己写一个IM并在特定范围内试用-到时候就知道有哪些坑了。
      进阶篇已经用到了不少基础篇和场景篇的知识：属于一边学习一边复习过程吧；期待老师的后续分享。</div>2019-09-26</li><br/>
</ul>