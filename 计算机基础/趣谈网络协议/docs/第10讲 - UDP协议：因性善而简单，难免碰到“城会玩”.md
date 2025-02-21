讲完了IP层以后，接下来我们开始讲传输层。传输层里比较重要的两个协议，一个是TCP，一个是UDP。对于不从事底层开发的人员来讲，或者对于开发应用的人来讲，最常用的就是这两个协议。由于面试的时候，这两个协议经常会被放在一起问，因而我在讲的时候，也会结合着来讲。

## TCP和UDP有哪些区别？

一般面试的时候我问这两个协议的区别，大部分人会回答，TCP是面向连接的，UDP是面向无连接的。

什么叫面向连接，什么叫无连接呢？在互通之前，面向连接的协议会先建立连接。例如，TCP会三次握手，而UDP不会。为什么要建立连接呢？你TCP三次握手，我UDP也可以发三个包玩玩，有什么区别吗？

**所谓的建立连接，是为了在客户端和服务端维护连接，而建立一定的数据结构来维护双方交互的状态，用这样的数据结构来保证所谓的面向连接的特性。**

例如，**TCP提供可靠交付**。通过TCP连接传输的数据，无差错、不丢失、不重复、并且按序到达。我们都知道IP包是没有任何可靠性保证的，一旦发出去，就像西天取经，走丢了、被妖怪吃了，都只能随它去。但是TCP号称能做到那个连接维护的程序做的事情，这个下两节我会详细描述。而**UDP继承了IP包的特性，不保证不丢失，不保证按顺序到达。**

再如，**TCP是面向字节流的**。发送的时候发的是一个流，没头没尾。IP包可不是一个流，而是一个个的IP包。之所以变成了流，这也是TCP自己的状态维护做的事情。而**UDP继承了IP的特性，基于数据报的，一个一个地发，一个一个地收。**

还有**TCP是可以有拥塞控制的**。它意识到包丢弃了或者网络的环境不好了，就会根据情况调整自己的行为，看看是不是发快了，要不要发慢点。**UDP就不会，应用让我发，我就发，管它洪水滔天。**

因而**TCP其实是一个有状态服务**，通俗地讲就是有脑子的，里面精确地记着发送了没有，接收到没有，发送到哪个了，应该接收哪个了，错一点儿都不行。而**UDP则是无状态服务**。通俗地说是没脑子的，天真无邪的，发出去就发出去了。

我们可以这样比喻，如果MAC层定义了本地局域网的传输行为，IP层定义了整个网络端到端的传输行为，这两层基本定义了这样的基因：网络传输是以包为单位的，二层叫帧，网络层叫包，传输层叫段。我们笼统地称为包。包单独传输，自行选路，在不同的设备封装解封装，不保证到达。基于这个基因，生下来的孩子UDP完全继承了这些特性，几乎没有自己的思想。

## UDP包头是什么样的？

我们来看一下UDP包头。

前面章节我已经讲过包的传输过程，这里不再赘述。当我发送的UDP包到达目标机器后，发现MAC地址匹配，于是就取下来，将剩下的包传给处理IP层的代码。把IP头取下来，发现目标IP匹配，接下来呢？这里面的数据包是给谁呢？

发送的时候，我知道我发的是一个UDP的包，收到的那台机器咋知道的呢？所以在IP头里面有个8位协议，这里会存放，数据里面到底是TCP还是UDP，当然这里是UDP。于是，如果我们知道UDP头的格式，就能从数据里面，将它解析出来。解析出来以后呢？数据给谁处理呢？

处理完传输层的事情，内核的事情基本就干完了，里面的数据应该交给应用程序自己去处理，可是一台机器上跑着这么多的应用程序，应该给谁呢？

无论应用程序写的使用TCP传数据，还是UDP传数据，都要监听一个端口。正是这个端口，用来区分应用程序，要不说端口不能冲突呢。两个应用监听一个端口，到时候包给谁呀？所以，按理说，无论是TCP还是UDP包头里面应该有端口号，根据端口号，将数据交给相应的应用程序。

![](https://static001.geekbang.org/resource/image/2c/84/2c9a109f3be308dea901004a5a3b4c84.jpg?wh=2183%2A1103)

当我们看到UDP包头的时候，发现的确有端口号，有源端口号和目标端口号。因为是两端通信嘛，这很好理解。但是你还会发现，UDP除了端口号，再没有其他的了。和下两节要讲的TCP头比起来，这个简直简单得一塌糊涂啊！

## UDP的三大特点

UDP就像小孩子一样，有以下这些特点：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（277） 💬（6）<div>网络_10
# 作业
- 连接：在自己监听的端口接收到连接的请求，然后经过“三次握手”，维护一定的数据结构和对方的信息，确认了该信息：我发的内容对方会接收，对方发的内容我也会接收，直到连接断开。
- 断开：经过“四次挥手”确保双方都知道且同意对方断开连接，然后在remove为对方维护的数据结构和信息，对方之后发送的包也不会接收，直到 再次连接。

我看到有的同学说，TCP是建立了一座桥，我认为这个比喻不恰当，TCP更好的比喻是在码头上增加了记录人员，核查人员和督导人员，至于IP层和数据链路层，它没有任何改造。
</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/c4/8d1150f3.jpg" width="30px"><span>Richie</span> 👍（172） 💬（5）<div>TCP&#47;UDP建立连接的本质就是在客户端和服务端各自维护一定的数据结构（一种状态机），来记录和维护这个“连接”的状态 。并不是真的会在这两个端之间有一条类似“网络专线”这么一个东西（在学网络协议之前脑海里是这么想象的）。

在IP层，网络情况该不稳定还是不稳定，数据传输走的是什么路径上层是控制不了的，TCP能做的只能是做更多判断，更多重试，更多拥塞控制之类的东西。
</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/0a/e564e572.jpg" width="30px"><span>N_H</span> 👍（8） 💬（1）<div>客户端和服务端建立tcp连接时，为了验证连接是否还在，客户端和服务端之间应该会不停地发送一些确认的信息，保证客户端和服务端之间的连接还在。（推测的）</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/cd/2c3808ce.jpg" width="30px"><span>Yangjing</span> 👍（5） 💬（8）<div>后面可以讲一下实际的分析不？比如用工具 wireshark 对包进行分析讲解，自己能看懂一部分简单的</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/2a/7d8b5943.jpg" width="30px"><span>LH</span> 👍（4） 💬（1）<div>前面说tcp是基于流的传输，无头无尾。后面说UDP的头和tcp不一样，我被搞晕流</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（4） 💬（2）<div>老师好，如何理解HTTP协议的多数据通道共享一个连接？</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/d8/e8eda334.jpg" width="30px"><span>Yang</span> 👍（3） 💬（1）<div>我想问一下，如果一个公司开发应用，他们可以自己选择用UDP 还是TCP吗？ </div>2019-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/87/c415e370.jpg" width="30px"><span>滢</span> 👍（3） 💬（1）<div>UDP应该也有错误检测的吧，老师是否补充下UDP检验和^_^</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f4/14/1d235e1c.jpg" width="30px"><span>A-李永军</span> 👍（3） 💬（2）<div>刘老师，udp传输怎样能避免乱序呢？</div>2018-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6e/04/94677062.jpg" width="30px"><span>嘎子</span> 👍（0） 💬（1）<div>哈哈哈！太赞啦！写的好好笑！</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/62/49/6332c99b.jpg" width="30px"><span>man1s</span> 👍（0） 💬（1）<div>为什么我感觉从上层往底层讲会好一些</div>2019-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/c8/0b88a29e.jpg" width="30px"><span>彩票365苹果版下载</span> 👍（298） 💬（4）<div>每次最后的问题，应该在第二次讲课的时候给答案说出来啊</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/88/b36caddb.jpg" width="30px"><span>仁者</span> 👍（73） 💬（0）<div>我们可以把发送端和接收端比作河流的两端，把传输的数据包比作运送的石料。TCP 是先搭桥（即建立连接）再一车一车地运（即面向数据流），确保可以顺利到达河对岸，当遇到桥上运输车辆较多时可以自行控制快慢（即拥堵控制）；UDP 则是靠手一个一个地扔（即无连接、基于数据报），不管货物能否顺利到达河对岸，也不关心扔的快慢频率。</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/bc/88a905a5.jpg" width="30px"><span>亮点</span> 👍（30） 💬（0）<div>第一个问题:TCP连接是通过三次握手建立连接，四次挥手释放连接，这里的连接是指彼此可以感知到对方的存在，计算机两端表现为socket,有对应的接受缓存和发送缓存，有相应的拥塞控制策略</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/01/22729368.jpg" width="30px"><span>Havid</span> 👍（27） 💬（0）<div>包最终都是通过链路层、物量层这样子一个一个出去的，所以连接只是一种逻辑术语，并不存在像管道那样子的东西，连接在这里相当于双方一种约定，双方按说好的规矩维护状态。</div>2018-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/ac/7f056518.jpg" width="30px"><span>Mr.Peng</span> 👍（27） 💬（1）<div>对包分析的工具及书籍分享一些！</div>2018-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/a0/26a8d76b.jpg" width="30px"><span>Chok Wah</span> 👍（20） 💬（1）<div>可以详细讲讲UDP常见小技巧，面试常问。
比如UDP发过去怎么确认收到；
基于UDP封装的协议一般会做哪些措施。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/03/4e71c307.jpg" width="30px"><span>蓝色理想</span> 👍（16） 💬（3）<div>似懂非懂，看来还是没懂╯□╰…如果有代码演示看看效果就很好了👍</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6f/a7/0bc9616f.jpg" width="30px"><span>耿老的竹林</span> 👍（15） 💬（1）<div>
UDP协议看起来简单，恰恰提供给了巨大的扩展空间。</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/bf/a9c9b1a1.jpg" width="30px"><span>Yang</span> 👍（13） 💬（0）<div>连接:3次握手之后，咱俩之间确认自己发的东西对方都能收到，然后咱俩各自维护这种状态！连接就建立了……</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/dc/87809ad2.jpg" width="30px"><span>埃罗芒阿老师</span> 👍（10） 💬（0）<div>1.两端各自记录对方的IP端口序列号连接状态等，并且维护连接状态
2.三次握手四次挥手</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（6） 💬（1）<div>以前觉得UDT应用不广，听了课之后觉得UDT的应用很多，但实际怎么查看应用用的是TCP还是UDP
呢？</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/1c/26dc1927.jpg" width="30px"><span>次郎</span> 👍（5） 💬（0）<div>能不能讲解一些打洞之类的知识？</div>2018-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/0b/13ee0753.jpg" width="30px"><span>小q</span> 👍（5） 💬（1）<div>上面说可以推荐本分接析包的书籍，是什么书呀</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/6a/3ea0c553.jpg" width="30px"><span>Eric</span> 👍（4） 💬（0）<div>深入浅出，少见的课程，很好！</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/fd/56c4fb54.jpg" width="30px"><span>Skye</span> 👍（4） 💬（1）<div>请问老师，TCP自面向字节流，和UDP的数据包具体形式是怎么样的。面向字节流之后下层还怎么封装呀</div>2018-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（4） 💬（0）<div>听一遍不够，要多听几遍</div>2018-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bd/62/283e24ab.jpg" width="30px"><span>雨后的夜</span> 👍（3） 💬（1）<div>&quot;而这个 RTMP 协议也是基于 TCP 的&quot;  -- 这里是不是搞错了，是UDP吧？</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d7/39/6698b6a9.jpg" width="30px"><span>Hector</span> 👍（3） 💬（0）<div>其实TCP来源于人类的交流，航海的双方通信交流的一个要义我们术语叫double-check.双方建立通信连接和结束会话一模一样，还对重要信息进行复述。</div>2019-05-05</li><br/><li><img src="" width="30px"><span>horsechestnut</span> 👍（3） 💬（0）<div>计算机会在内核中维护一个数据结构，以及状态机，去保证tcp是连接的</div>2018-08-07</li><br/>
</ul>