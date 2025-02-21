上一节，我们讲的UDP，基本上包括了传输层所必须的端口字段。它就像我们小时候一样简单，相信“网之初，性本善，不丢包，不乱序”。

后来呢，我们都慢慢长大，了解了社会的残酷，变得复杂而成熟，就像TCP协议一样。它之所以这么复杂，那是因为它秉承的是“性恶论”。它天然认为网络环境是恶劣的，丢包、乱序、重传，拥塞都是常有的事情，一言不合就可能送达不了，因而要从算法层面来保证可靠性。

## TCP包头格式

我们先来看TCP头的格式。从这个图上可以看出，它比UDP复杂得多。

![](https://static001.geekbang.org/resource/image/64/bf/642947c94d6682a042ad981bfba39fbf.jpg?wh=2203%2A1618)

首先，源端口号和目标端口号是不可少的，这一点和UDP是一样的。如果没有这两个端口号。数据就不知道应该发给哪个应用。

接下来是包的序号。为什么要给包编号呢？当然是为了解决乱序的问题。不编好号怎么确认哪个应该先来，哪个应该后到呢。编号是为了解决乱序问题。既然是社会老司机，做事当然要稳重，一件件来，面临再复杂的情况，也临危不乱。

还应该有的就是确认序号。发出去的包应该有确认，要不然我怎么知道对方有没有收到呢？如果没有收到就应该重新发送，直到送达。这个可以解决不丢包的问题。作为老司机，做事当然要靠谱，答应了就要做到，暂时做不到也要有个回复。

TCP是靠谱的协议，但是这不能说明它面临的网络环境好。从IP层面来讲，如果网络状况的确那么差，是没有任何可靠性保证的，而作为IP的上一层TCP也无能为力，唯一能做的就是更加努力，不断重传，通过各种算法保证。也就是说，对于TCP来讲，IP层你丢不丢包，我管不着，但是我在我的层面上，会努力保证可靠性。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/34/e1/d1f201ae.jpg" width="30px"><span>code4j</span> 👍（60） 💬（10）<div>老师您好，昨天阿里云出故障，恢复后，我们调用阿里云服务的时后出现了调用出异常  connection reset。netstat看了下这个ip发现都是timewait，链接不多，但是始终无法连接放对方的服务。按照今天的内容，难道是我的程序关闭主动关闭链接后没有发出最后的ack吗？之前都没有问题，很不解</div>2018-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/dd/4f53f95d.jpg" width="30px"><span>进阶的码农</span> 👍（23） 💬（1）<div>状态机图里的不加粗虚线看不懂什么意思 麻烦老师点拨下</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/46/dffc60d2.jpg" width="30px"><span>凛</span> 👍（134） 💬（8）<div>旧书不厌百回读，熟读深思子自知啊。

再一次认识下TCP这位老司机，这可能是我读过的最好懂的讲TCP的文章了。同时有了一个很爽的触点，我发现但凡复杂点儿的东西，状态数据都复杂很多。还有一个，也是最重要的，我从TCP中再一次认识到了一个做人的道理，像孔子说的：“不怨天，不尤人”。人与人相处，主要是“我，你，我和你的关系”这三个处理对象，“你”这个我管不了，“我”的成长亦需要时间，我想到的是“我和你的关系”，这个状态的维护，如果能“无尤”，即不抱怨。有时候自己做多点儿，更靠谱点，那人和人的这个连接不是会更靠谱么？这可能是我从TCP这儿学到的最棒的东西了。

感谢老师的讲解，让我有了新的想法和收获。</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/57/3a729755.jpg" width="30px"><span>灯盖</span> 👍（131） 💬（3）<div>流量控制是照顾通信对象
拥塞控制是照顾通信环境</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/0a/077b9922.jpg" width="30px"><span>krugle</span> 👍（118） 💬（3）<div>流量控制和拥塞控制什么区别</div>2018-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pc41FOKAiabVaaKiawibEm7zglvnsYBnYeRiaSAElf9ciczovXmXmI0hOeR6U9RULFtMoqX5kobNttvwXCLsUM9Hbcg/132" width="30px"><span>monkay</span> 👍（88） 💬（5）<div>如果是建立链接了，数据传输过程链接断了，客户端和服务器端各自会是什么状态？
或者我可以这样理解么，所谓的链接根本是不存在的，双方握手之后，数据传输还是跟udp一样，只是tcp在维护顺序、流量之类的控制</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/45/f5/b3d7febf.jpg" width="30px"><span>Adolph</span> 👍（60） 💬（6）<div>为什么要四次挥手
任何一方都可以在数据传送结束后发出连接释放的通知，待对方确认后进入半关闭状态。当另一方也没有数据再发送的时候，则发出连接释放通知，对方确认后就完全关闭了TCP连接。

举个例子：A 和 B 打电话，通话即将结束后，A 说“我没啥要说的了”，B回答“我知道了”，但是 B 可能还会有要说的话，A 不能要求 B 跟着自己的节奏结束通话，于是 B 可能又巴拉巴拉说了一通，最后 B 说“我说完了”，A 回答“知道了”，这样通话才算结束。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（46） 💬（2）<div>多谢分享，精彩。扫除了我之前很多的疑问。tcp连接的断开比建立复杂一些，本质上是因为资源的申请（初始化）本身就比资源的释放简单，以c++为例，构造函数初始化对象很简单，而析构函数则要考虑所有资源安全有序的释放，tcp断连时序中除了断开这一重要动作，另外重要的潜台词是“我要断开连接了 你感觉把收尾工作做了”</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（42） 💬（3）<div>评论区不能互评，如下两个问题是我的看法，不对请指出 多谢


我们做一个基于tcp的“物联网”应用（中国移动网络），如上面所说tcp层面已经会自动重传数据了，业务层面上还有必要再重传吗？如果是的话，业务需要多久重传一次？

--- TCP的重传是网络层面和粒度的，业务层面需要看具体业务，比如发送失败可能对端在重启，一个重启时间是1min，那就没有必要每秒都发送检测啊.

1、‘序号的起始序号随时间变化，...重复需要4个多小时’，老师这个重复时间怎么计算出来的呢？每4ms加1，如果有两个TCP链接都在这个4ms内建立，是不是就是相同的起始序列号呢。
答:序号的随时间变化，主要是为了区分同一个链接发送序号混淆的问题，两个链接的话，端口或者IP肯定都不一样了.2、报文最大生存时间（MSL）和IP协议的路由条数（TTL）什么关系呢，报文当前耗时怎么计算？TCP层有存储相应时间？
答:都和报文生存有关，前者是时间维度的概念，后者是经过路由跳数，不是时间单位.
</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（27） 💬（5）<div>网络_11
读完今天呢内容后，有一个强烈的感受：技术的细节非常生动。
之前对于TCP的感知就是简单的“三次握手”，“四次挥手”，觉得自己掌握了精髓，但随便一个问题就懵了，比如，
- 客户端什么时候建立连接？
&gt; 根据以前的认知，会以为是“三次握手”后，双方同时建立连接。很显然是做不到的，客户端不知道“应答的应答”有没有到达，以及什么时候到达。。。
- 客户端什么时候断开连接？
&gt; 不仔细思考的话，就会说“四次挥手”之后喽，但事实上，客户端发出最后的应答(第四次“挥手”)后，永远无法知道有没有到达。于是有了2MSL的等待，在不确定的网络中，把问题最大程度地解决。

TCP的状态机，以及很多的设计细节，都是为了解决不稳定的网络问题，让我们看到了在无法改变不稳定的底层网络时，人类的智慧是如果建立一个基本可靠稳定的网络的。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（24） 💬（1）<div>老师好，我看书中说是计数器每4微妙就加1的。</div>2018-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4d/62/bfbf8ee3.jpg" width="30px"><span>走过全世界。</span> 👍（20） 💬（4）<div>三次握手连接就是：
A：你瞅啥
B：瞅你咋地
A：再瞅一个试试
然后就可以开始亲密友好互动了😏</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/7d/370b0d4c.jpg" width="30px"><span>西部世界</span> 👍（19） 💬（2）<div>我也纠结了4ms加一重复一次的时间是4个多小时的问题。
具体如下:
4ms是4微秒，等于100万分之一秒，32位无符号数的最大值是max=4294967296(注意区分有符号整数最大值)
公式如下4&#47;1000000*max&#47;60&#47;60=4.772小时。</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/c5/3467cf94.jpg" width="30px"><span>正是那朵玫瑰</span> 👍（19） 💬（4）<div>老师有几个疑问：
1、当三次握手建立连接后，每次数据交互都还会ack吗？比如建立连接后，客户端发送数据包给服务器端，服务器成功收到数据包后会发送ack给客户端么？
2、如果建立连接后，客户端和服务器端没有任何数据交互，双方也不主动关闭连接，理论上这个连接会一直存在么？
3、2基础上，如果连接一直会在，双方又没有任何数据交互，若一方突然跑路了，另一方怎么知道对方已经不在了呢？在java scoket编程中，我开发客户端与服务器端代码，双方建立连接后，不发送任何数据，当我强制关闭一端时，另一端会收到一个强制关闭异常，这是如何知道对方已经强制关闭了呢？</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/a6/723854ee.jpg" width="30px"><span>姜戈</span> 👍（12） 💬（1）<div>Tcp三次握手设计被恶意利用 ，造就了ddos。</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（8） 💬（1）<div>感谢老师耐心回答，另外RFC文档上，microsecond是微秒哈，毫秒是milisecond😁</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（7） 💬（1）<div>我认为每4微妙，seq自增1这个说法不太靠谱，可能是以讹传讹，计算出来是4.7小时左右一轮回。随着网卡速率加快，我觉得这个数据会变小。可以通过wireshark抓包实验计算一下。
http:&#47;&#47;www.cnblogs.com&#47;chenboo&#47;archive&#47;2011&#47;12&#47;19&#47;2293327.html</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/15/7d47de48.jpg" width="30px"><span>咖啡猫口里的咖啡猫🐱</span> 👍（7） 💬（2）<div>老师再问个问题，TCP保证有序（后续到的包会等待之前的包），流量控制，拥塞机制，导致网络出现抖动时，延迟性就高，响应慢，，为什么要在应用层写重发机制，，毕竟TCP保证有序性，意义不大啊😄</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/37/76/6c85bc5a.jpg" width="30px"><span>水到渠成</span> 👍（6） 💬（2）<div>“……RST 是重新连接，……”“……A 就表示，我已经在这里等了这么长时间了，已经仁至义尽了，之后的我就都不认了，于是就直接发送 RST，B 就知道 A 早就跑了。”感觉这里不太理解，为什么早就跑路了却要发一个RST,那不是又要建立连接了，但是我已经不需要建立连接了呀！难道我要在连接上然后专门过去说一下再见？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/e7/043f9dda.jpg" width="30px"><span>.</span> 👍（5） 💬（1）<div>之前看过《UNIX网络编程 卷I》，看这几节简直不要太舒服，跟吃豆腐脑一样。</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/b3/798a4bb2.jpg" width="30px"><span>帽子丨影</span> 👍（5） 💬（1）<div>Java服务器，close_wait特别多，怎么定位到是那一块的代码有问题呢</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5c/cb/65b38e27.jpg" width="30px"><span>wang-possible</span> 👍（4） 💬（1）<div>老师您好，如果一个端口是如何接收多个客户端的请求</div>2019-07-24</li><br/><li><img src="" width="30px"><span>Geek_f6f02b</span> 👍（4） 💬（2）<div>因而，每个连接都要有不同的序号。这个序号的起始序号是随着时间变化的，可以看成一个 32 位的计数器，每 4ms 加一，这里有个疑问就是，这个序号只跟时间有关跟，上一个序号无关是吗，比如上一个序号是 X ,那么如果过来 8ms 再发下一个包，那么这个包的 tcp 序号就是 x+2 ,而不是 x+1 是吗？</div>2019-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（3） 💬（1）<div>老师 文中提到的icmp报文  是那台 将ttl减为0上的那台路由器上发出的吗？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/7d/791d0f5e.jpg" width="30px"><span>蚂蚁吃大象</span> 👍（3） 💬（1）<div>四次挥手为何有fin+ack？为何不只是fin？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（3） 💬（2）<div>TCP包头格式一节，图后第三段第四句话有语病，“解决不丢包问题”，应该是”解决丢包问题“。另外，关于序号的解读有误，序号并非每4ms自增1，如果是，时间4个多小时也对不上，查了《TCP&#47;IP》详解，其数字和传输的包大小以及SYN状态位有关，在 SYN flag 置 1 时，此为当前连接的初始序列号（Initial Sequence Number, ISN），数据的第一个字节序号为此 ISN + 1；在 SYN flag 置 0 时，为当前连接报文段的累计数据包字节数。
</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（2） 💬（1）<div>RST是重新连接，为什么A在2MSL后收到B的FIN包会发RST呢？难道此时的A已经变成了另一个应用？</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/af/f59b4c7c.jpg" width="30px"><span>深海极光</span> 👍（2） 💬（4）<div>老师请问一下，我们都说tcp链接是四元组，从ip协议层有5元组的说法，是加上协议类型，那是不是说明同一个端口既能接收tcp的包也能接收udp的包呢？</div>2019-03-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIHq3CYG3iaEwGv7FVYZGXaGYbGHc1VNmog1ByZNtTjYJdmdATQI64icd7P1hmS4uib2wbn1cicKYkjPw/132" width="30px"><span>Geek_h1q46c</span> 👍（2） 💬（1）<div>“The generator is bound to a (possibly fictitious) 32 bit clock whose low order bit is incremented roughly every 4 microseconds.”
上面是从RFC739 p26复制的。
4 microseconds = 4微秒 = 4μs
所以是4μs自增1</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/15/7d47de48.jpg" width="30px"><span>咖啡猫口里的咖啡猫🐱</span> 👍（2） 💬（1）<div>还是我老师，，TCP重传，底层会处理去重后传给上层？   那会不会把缓冲区撑死啊，毕竟要过滤对比去重，再传给上层。。那一个包rece缓存区生命周期是？</div>2018-06-11</li><br/>
</ul>