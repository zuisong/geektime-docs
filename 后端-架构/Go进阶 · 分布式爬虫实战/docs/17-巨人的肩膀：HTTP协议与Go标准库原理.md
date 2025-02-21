你好，我是郑建勋。

在正式开始这节课之前，我想给你分享一段话。

> 学校教给我们很多寻找答案的方法。在我所研究的每一个有趣的问题中，挑战都是寻找正确的问题。当Mike Karels和我开始研究TCP拥堵时，我们花了几个月的时间盯着协议和数据包的痕迹，问 ：“为什么会失败？”。

> 有一天，在迈克的办公室里，我们中的一个人说：“我之所以搞不清楚它为什么会失败，是因为我不明白它一开始是怎么工作的。”这被证明是一个正确的问题，它迫使我们弄清楚使TCP工作的 “ack clocking”。在那之后，剩下的事情就很容易了。

这段话摘自《Computer Networking A Top-Down Approach 6th》这本书，它启发我们，解决网络方面的问题，核心就是要搞懂它的工作原理。

在上节课，我介绍了一个最简单的HTTP请求，了解了一个网络数据包是如何跨过千山万水到达对端的服务器的。不过就像前面引文说的那样，这是不够的。所以这节课，让我们更近一步，来看看当数据包到达对端服务器之后，操作系统和硬件会如何处理数据包，同时我将介绍HTTP协议，带你理清Go HTTP标准库高效处理网络数据包的底层设计原理。

## 操作系统处理数据包流程

当数据包到达目的地设备后，数据包需要经过复杂的逻辑处理最终到达应用程序。数据包的处理过程大致可以分为7步，我们可以根据下面这张流程图一层一层来理解。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/35/77/95e95b32.jpg" width="30px"><span>木杉</span> 👍（18） 💬（0）<div>贴那么多书单  还不如多粘贴一些代码  可以学习呢  </div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（13） 💬（1）<div>这一讲的内容应该出现在真正需要使用到该讲的知识的时候，而不是现在就把理论一股脑抛出来。个人觉得，没有实战结合的理论，就是凭空增加认知负荷</div>2022-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/fc/0e887697.jpg" width="30px"><span>kkgo</span> 👍（11） 💬（0）<div>到现在还没有进入爬虫的设计，太多基础了</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/21/8c13a2b4.jpg" width="30px"><span>周龙亭</span> 👍（3） 💬（0）<div>浅尝辄止的铺垫太多了，还不如几句话带过</div>2023-01-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIqvYMQ1yscgB6xS4nDkoOuP6KiaCiaichQA1OiaQ9rFmNtT9icgrZxeH1WRn5HfiaibDguj8e0lBpo65ricA/132" width="30px"><span>Geek_crazydaddy</span> 👍（3） 💬（0）<div>1.没想到啥不妥的地方，连接池的连接数量？比如大量并行请求可能会有建立大量连接？
2.保留的连接数量以及连接何时释放</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（1） 💬（0）<div>确实都是这些理论,没必要讲操作系统 网络原理这些知识,本来这门课的定位就是实战课,大家也都是想跟着练手一个项目,真去学这些基础理论知识,肯定深入学习一点,这样花这么多篇幅介绍,实在没有必要</div>2024-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/d6/76fe5259.jpg" width="30px"><span>Dream.</span> 👍（0） 💬（0）<div>这一讲学的真难啊。时隔这么长时间回来重新学习，这次跟着老师的思路一点点深入扒拉了net&#47;http的GET请求背后的源码。找transport就找了半天，才发现是在send调用的入参里传进去使用的，在里面实现了多路复用。但是到最后还是没看到协程是在什么时候启动，整个GET的请求链路，我看下来还是属于同步I&#47;O处理，没理解文中多次提到的异步I&#47;O到底是什么。</div>2024-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（0） 💬（0）<div>在设计自己的爬虫框架的时候，为了解耦将所有网络请求都封装到了自己的 spiderClient 中，管理爬虫对 http 的请求。
spiderClient 组合了标准库的 http.Client，此时需要注意在并发情况下 spiderClient 是否会出现性能问题，其中感觉最关键的就是需要知晓 http.Client 是否管理了连接池，如果没有，那需要自己实现这部分。
文章说 http.Client 管理了连接池，这个问题也有久了答案。

第二个问题：Go 标准库使用了连接池，你觉得实现一个连接池应该考虑哪些因素？
连接的创建：什么时候需要创建新的连接，什么时候倾向等待其他链接的释放，是否要预创建连接
连接的销毁：什么时候自动销毁，当连接池占用的资源过多的时候是否主动释放，如果主动释放，淘汰策略是怎样的
对每个链接的控制：连接是否健康
连接池的控制：连接总数是否要限制，连接如何回收</div>2024-01-25</li><br/>
</ul>