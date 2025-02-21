上一节我们讲的进程间通信，其实是通过内核的数据结构完成的，主要用于在一台Linux上两个进程之间的通信。但是，一旦超出一台机器的范畴，我们就需要一种跨机器的通信机制。

一台机器将自己想要表达的内容，按照某种约定好的格式发送出去，当另外一台机器收到这些信息后，也能够按照约定好的格式解析出来，从而准确、可靠地获得发送方想要表达的内容。这种约定好的格式就是**网络协议**（Networking Protocol）。

我们将要讲的Socket通信以及相关的系统调用、内核机制，都是基于网络协议的，如果不了解网络协议的机制，解析Socket的过程中，你就会迷失方向，因此这一节，我们有必要做一个预习，先来大致讲一下网络协议的基本原理。

## 网络为什么要分层？

我们这里先构建一个相对简单的场景，之后几节内容，我们都要基于这个场景进行讲解。

我们假设这里就涉及三台机器。Linux服务器A和Linux服务器B处于不同的网段，通过中间的Linux服务器作为路由器进行转发。

![](https://static001.geekbang.org/resource/image/f6/0e/f6982eb85dc66bd04200474efb3a050e.png?wh=3650%2A2255)

说到网络协议，我们还需要简要介绍一下两种网络协议模型，一种是**OSI的标准七层模型**，一种是**业界标准的TCP/IP模型**。它们的对应关系如下图所示：

![](https://static001.geekbang.org/resource/image/92/0e/92f8e85f7b9a9f764c71081b56286e0e.png?wh=1783%2A1843)

为什么网络要分层呢？因为网络环境过于复杂，不是一个能够集中控制的体系。全球数以亿记的服务器和设备各有各的体系，但是都可以通过同一套网络协议栈通过切分成多个层次和组合，来满足不同服务器和设备的通信需求。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（9） 💬（1）<div>老师：问个问题。我们家庭办理的宽带，都是运营商在哪一层把带宽给限制的呢？</div>2019-07-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/vTku9cFYPh2T8DSImQoPRLxgSibcVgCRYqMcEYibexxLkfn9IKhUSAasZ7QoB72SDWym31niah2y00ibRWdHibibib1wQ/132" width="30px"><span>Regina</span> 👍（5） 💬（1）<div>为什么握手使用的socket与链接的socket不一样，有什么原因吗</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（2） 💬（5）<div>为什么称为协议栈呢？这和栈这种数据结构有何关系？</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（0） 💬（1）<div>”将一个网络包从一个网络转发到另一个网络的设备称为路由器“。
这里面的网络不仅包括eth0&#47;1之类的interface，也包括自定义的interface,比如docker自动生成的docker0.就算一台机器只有一个物理网卡，也能当作路由器，是吧。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b4/f6/735673f7.jpg" width="30px"><span>W.jyao</span> 👍（0） 💬（1）<div>看到留言的问题了，这不就是arp干的事</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（0） 💬（6）<div>老师我想问一下在发送数据包的时候, Linux服务A是怎么拿到linux服务器B的mac地址的, Linux服务器B的mac地址是一开始就加上去的吗?</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/62/947004d0.jpg" width="30px"><span>www</span> 👍（2） 💬（0）<div>站得高，讲得真清楚，之前一直不太理解Socket的定位</div>2022-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/42/fc/c89243d8.jpg" width="30px"><span>侯代烨</span> 👍（1） 💬（0）<div>讲的很详细，从封包到解包过程很详细</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/3a/7ef24065.jpg" width="30px"><span>严志波</span> 👍（1） 💬（4）<div>为啥要有交换机呢</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e7/de/c62cba75.jpg" width="30px"><span>无为</span> 👍（1） 💬（1）<div>ICMP协议应该是在网络层。并不是传输层</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/81/1864f266.jpg" width="30px"><span>石将从</span> 👍（1） 💬（3）<div>这个一下子二层，一下子四层的，我都不知道是指哪一层了，也不知道从上往下数，还是从下往上数，对照了半天，尴尬</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（0） 💬（0）<div>网内靠mac定位主机，往外就要靠网关的IP，同时数据包的mac也会被网关替换成网关的mac。</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/79/14/dc3e49d1.jpg" width="30px"><span>Geek_29c23f</span> 👍（0） 💬（2）<div>同一个网络中，网络号一样，主机号不一样，这样能通过ip地址找到设备了，为什么还需要mac地址去找</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/79/14/dc3e49d1.jpg" width="30px"><span>Geek_29c23f</span> 👍（0） 💬（1）<div>ARP请求只局限在相同网段的网络。那假如需要从服务器A ping包 服务器B (图1）。不需要ARP请求嘛？或者是怎么完成连接？</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/08/32/8137ce04.jpg" width="30px"><span>李很奈斯</span> 👍（0） 💬（0）<div>爱了(⑉°з°)-♡，讲的非常不错</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/cc/dfe92ee1.jpg" width="30px"><span>宋桓公</span> 👍（0） 💬（1）<div>一个数据包里是有两个mac吗，一个是网关的，一个是局域网中pc的吗？</div>2019-10-14</li><br/>
</ul>