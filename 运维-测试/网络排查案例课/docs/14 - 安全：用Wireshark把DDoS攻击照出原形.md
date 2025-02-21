你好，我是胜辉。

在过去几节课里，我们集中学习了TCP传输相关的知识，无论是[第8讲](https://time.geekbang.org/column/article/484667)的MTU、[第9讲](https://time.geekbang.org/column/article/484923)和[第10讲](https://time.geekbang.org/column/article/485689)的传输速度、[第11讲](https://time.geekbang.org/column/article/486281)的拥塞控制，还是第12和13讲的各种重传，我们可以说是把TCP传输相关的核心概念全部过了一遍。一方面学习了RFC规范和具体的Linux实现，一方面也通过案例，把这些知识灵活运用了起来。想必现在的你，再去处理TCP传输问题的时候，已经强大很多了。

不过，上面的种种，其实还是在协议规范这个大框架内的讨论和学习，默认前提就是通信两端是遵照了TCP规定而展开工作的，都可谓是谦谦君子，道德楷模。

但是，有明就有暗。不遵照TCP规范，甚至寻找漏洞、发起攻击，这种“小人”乃至“强盗”的行为，也并非少见，比如我们熟知的 **DDoS攻击**。

那么这节课，我们就不来学习怎么做君子了，当然，也不是教你做“小人”，而是我们要**了解“小人”可能有的各种伎俩，通过Wireshark把这种种攻击行为照个彻底，认个清楚**。这样，以后你如果遇到这类情况，就心里有数，也有对策了。

## NTP反射攻击案例

我在公有云做技术工作的时候，发现游戏类业务遭到DDoS的情况比较多见。有一次，一个游戏客户就发现，他们的游戏服务器无法登录，被玩家投诉，可以说是十万火急。客户的工程师做了tcpdump抓包，然后赶紧把抓包文件传给我们一起分析。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（4） 💬（3）<div>1 假如利用反射攻击，有可能攻击流量翻倍；也有可能攻击流量打出来，被运营商给干掉了一部分，结果没有100M；
2 cdn按照不同来源IP，把攻击流量稀释了，一定程度上可以缓解ddos；</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（3） 💬（2）<div>CDN通过 GSLB 将流量都分散到不同的POP节点去了。 如果堵住GSLB，应该就另说了吧</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（2） 💬（1）<div>为什么IP 协议不检查源IP 呢？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（1） 💬（1）<div>我记得 QUIC 协议的 UDP 包载荷普遍大于 512 字节</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>这次理解了为什么dns协议为啥既采用UDP，又采用TCP的原因了。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>UDP 头部其实只有 8 个字节，分别是：2 个字节的源端口号；2 个字节的目的端口号；2 个字节的报文长度；2 个字节的校验和。
TCP header ： 20字节</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（2）<div>“肉机”发出 100Mbps 的攻击流量，到达被攻击站点的时候，仍然是 100Mbps 吗？为什么呢？
答：到达被攻击点的时候；可能高于100Mbps，可能因为中间节点mtu导致的。
为什么 CDN 可以达到缓解 DDoS 的效果呢？
答：因为CDN有多个边缘节点，这些边缘节点的IP不同，ddos在这些边缘节点会被消散很多</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（0）<div>文中说，当 DNS 报文超过 512 会自动转为 TCP 报文，可是实际情况是，一般都要求 DNS 解析的 IP 不能超过 15 个 IP，以避免超过 512，这是为什么呢？</div>2023-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>三刷笔记：
# 学到的知识
主要就是学习了DDoS的原理以及相应的抓包实现。


DDoS拒绝服务攻击的种类
1、耗尽服务器资源：无法接受用户的请求，比如TCP的半连接队列满了。
2、耗尽网络带宽：用户的请求发不进来

## 直接攻击
利用TCP直接进行攻击。

如果用TCP的话，就直接攻击，而不像借助UDP的反射攻击。
比如SYN攻击、半连接攻击、全连接攻击、CC攻击。

## 耗尽网络带宽
利用UDP依靠别的服务器资源耗尽目标受害者的网络带宽。
典型的有NTP借力打力的放大攻击。

所谓借力打力，指的是「IP协议不验证源地址的特性」，可以依托别的服务器资源作为手中的武器

所谓放大指的就是请求与响应数据体的大小完全不成比例，响应数据远大于请求数据。

为什么放大攻击都是依托于UDP呢？
1、UDP报文简单
因为UDP简单，易于构造。只有8个字节，分别是2字节的源端口、目的端口、长度、校验和。

2、UDP是无状态的
不需要握手，不需要维持连接。

感觉1和2就是一体两面的。因为UDP无状态，所以协议报文不需要那么复杂，8字节就够了。</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>如果你也担心自己家的路由器也中招了的话，可以自测一下。访问https:&#47;&#47;badupnp.benjojo.co.uk&#47;这个站点，它会对你的出口 IP（家用路由器的出口 IP）进行探测，看看是否有 1900 端口可以被利用。如果没有漏洞，网页会提醒你“All good! It looks like you are not listening on UPnP on WAN”。</div>2022-03-21</li><br/>
</ul>