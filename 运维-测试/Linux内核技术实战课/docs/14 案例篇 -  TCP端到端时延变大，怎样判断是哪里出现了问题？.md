你好，我是邵亚方。

如果你是一名互联网从业者，那你对下面这个场景应该不会陌生：客户端发送请求给服务端，服务端将请求处理完后，再把响应数据发送回客户端，这就是典型的C/S（Client/Server）架构。对于这种请求-响应式的服务，我们不得不面对的问题是：

- 如果客户端收到的响应时间变大了，那么这是客户端自身的问题呢，还是因为服务端处理得慢呢，又或者是因为网络有抖动呢？
- 即使我们已经明确了是服务端或者客户端的问题，那么究竟是应用程序自身引起的问题呢，还是内核导致的问题呢？
- 而且很多时候，这种问题往往是一天可能最多抖动一两次，我们很难去抓现场信息。

为了更好地处理这类折磨人的问题，我也摸索了一些手段来进行实时追踪，既不会给应用程序和系统带来明显的开销，又可以在出现这些故障时能够把信息给抓取出来，从而帮助我们快速定位出问题所在。

因此，这节课我来分享下我在这方面的一些实践，以及解决过的一些具体案例。

当然，这些实践并不仅仅适用于这种C/S架构，对于其他应用程序，特别是对延迟比较敏感的应用程序，同样具备参考意义。比如说：

- 如果我的业务运行在虚拟机里面，那怎么追踪呢？
- 如果Client和Server之间还有一个Proxy，那怎么判断是不是Proxy引起的问题呢？
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（10） 💬（0）<div>课后作业答案：
- 结合这堂课的第一张图，在这张图中，请问是否可以用 TCP 流到达 B 点的时刻（到达 Server 这台主机的时间）减去 TCP 流经过 A 点的时刻（到达 Client 这台主机的时间）来做为网络耗时？为什么？

很多同学在课后评论里都回答的很好了。比如：
“主要原因是两边的时间不统一。
有可能客户端的时间比服务端的快。
只有选取相同的时间基点，算出的差值才有意义。”


- 结合我们在“13 讲“里讲到的 RTT 这个往返时延，你还可以进一步思考：是否可以使用 RTT 来作为这次网络耗时？为什么？欢迎你在留言区与我讨论。
也不可以。
rtt时间不仅仅包含网络时间 还有内核软中断处理时间 另外还存在delayed ack，所以它不仅仅是网络传输耗时。</div>2020-10-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epUBQibdMCca340MFZOe5I1GwZ0PosPIzA0TPCNzibgH00w45Zmv4jmL0mFRHMUM9FuKiclKOCBjSmsw/132" width="30px"><span>Geek_circle</span> 👍（10） 💬（2）<div>老师好
有个现象帮忙看下如何分析定位下
centos7.2 长连接redis ，应用日志会显示无规律的出现hmget 间歇性超过200ms，最长达6s返回的情况，持续几分钟后恢复。后续要求定位，
主服务器不可中断， 不准部署抓包，安装bcc 感觉工具又可能消耗资源。排除了中间网络监控的问题 ，redis服务端也未发现超时的记录，怀疑系统层面的，是否有什么思路或者工具手段监控定位呢？</div>2020-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（6） 💬（1）<div>老师，看评论里面多次提到 delayed ack，能详细给说明下这个参数的意义吗 </div>2021-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/62/b874af21.jpg" width="30px"><span>颛顼</span> 👍（2） 💬（1）<div>这个文中几个时间点，是怎么联系起来，来验证是同一个请求的？</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（1）<div>思考题2
RTT 是否可以作为这次网络耗时？
好像不行吧。

看图好像是可以，毕竟就是tcp的一去一回。
但是这个还取决于对方返回ACK时是否及时。
有时ack是会合并的。有些内核参数好像还会延迟ack的返回时机吧。</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（1） 💬（1）<div>1.请问作者公司线上机器都装了systemtap吗？
2.这个systemtap脚本和模块以后会开源吗？</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/fb/c1334976.jpg" width="30px"><span>王崧霁</span> 👍（0） 💬（1）<div>不可以，tcp有重传</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>老师公司也在用CentOS7啊。
不知道有没有遇到过7.6版本的3.10.0.957内核bug，导致tcp的Send-Q居高不下的问题，哈哈。</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>思考题1
我觉得tcp流到B点的时间减出A点的时间做网络延迟 不合适。

主要原因是两边的时间不统一。
有可能客户端的时间比服务端的快。
只有选取相同的时间基点，算出的差值才有意义。

另外，因为TCP流会有很多Segment，可能一次请求就包含多个Segment，取哪一个或平均值，都不好实现。
而取同一个节点的时间，可以取最后一个发出去的报文和第一个发出去的报文来计算真实的时间。
毕竟数据只接收了一半，也是无法开始执行逻辑的。</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（0） 💬（1）<div>rtt统计的是tcp协议栈发出到收到的时间，包括客户端自身协议栈到发出网卡，网络传输，对方网卡接收并发到服务端协议栈，再经过返回流程到客户端协议栈的时间，rtt延时不能具体区分是哪个部分的问题。</div>2020-09-19</li><br/><li><img src="" width="30px"><span>Geek_6909db</span> 👍（2） 💬（0）<div>l老师在思考一个问题，
1.整个链路的超时时间如何设置合理性，如何做实验，比如一个请求，到nginx 服务器 TCP超时时间，nginx超时时间，到Tomcat服务器TCP超时时间，Tomcat超时时间，到DB，redis,mq超时时间，</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/fc/1e235814.jpg" width="30px"><span>耿长学</span> 👍（1） 💬（4）<div>唉，一个操作案例都没有，跟《Linux性能优化实战》几万的订阅量完全没法比，因为一个用心了，一个感觉很随意</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>老师，你好，捉个虫。「tcprstat 会记录 request 的到达时间点，以及 request 发出去的时间点，然后计算出 RT 并记录到日志中。」应该是「以及 response 发出去的时间点」吧？
</div>2023-04-03</li><br/>
</ul>