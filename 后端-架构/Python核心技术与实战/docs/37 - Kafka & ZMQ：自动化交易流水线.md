你好，我是景霄。

在进行这节课的学习前，我们先来回顾一下，前面三节课，我们学了些什么。

第 34 讲，我们介绍了如何通过 RESTful API 在交易所下单；第 35 讲，我们讲解了如何通过 Websocket ，来获取交易所的 orderbook 数据；第 36 讲，我们介绍了如何实现一个策略，以及如何对策略进行历史回测。

事实上，到这里，一个简单的、可以运作的量化交易系统已经成型了。你可以对策略进行反复修改，期待能得到不错的 PnL。但是，对于一个完善的量化交易系统来说，只有基本骨架还是不够的。

在大型量化交易公司，系统一般是分布式运行的，各个模块独立在不同的机器上，然后互相连接来实现。即使是个人的交易系统，在进行诸如高频套利等算法时，也需要将执行层布置在靠近交易所的机器节点上。

所以，从今天这节课开始，我们继续回到 Python 的技术栈，从量化交易系统这个角度切入，为你讲解如何实现分布式系统之间的复杂协作。

## 中间件

我们先来介绍一下中间件这个概念。中间件，是将技术底层工具和应用层进行连接的组件。它要实现的效果则是，让我们这些需要利用服务的工程师，不必去关心底层的具体实现。我们只需要拿着中间件的接口来用就好了。

这个概念听起来并不难理解，我们再举个例子让你彻底明白。比如拿数据库来说，底层数据库有很多很多种，从关系型数据库 MySQL 到非关系型数据库 NoSQL，从分布式数据库 Spanner 到内存数据库 Redis，不同的数据库有不同的使用场景，也有着不同的优缺点，更有着不同的调用方式。那么中间件起什么作用呢？
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（23） 💬（3）<div>第一个问题，大家的回复很正确，time.sleep(1) 后置，则第一条消息会丢失，因为建立连接需要时间，建立成功之前的所有消息都会丢失。
第二个问题，在 linux socket 中, 一个连接就是一个 socket , 但在 ZMQ 中, 一个 socket 上可以承载多个数据连接. 这里 socket 和connection不再是同个层次上的等价词汇, 要把socket理解为程序员访问数据连接的一个入口。因此，我们在绑定一个 socket 之后，可以让多个发布者连接到这里即可，和多个订阅者的使用是同样的方式。</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/a5/6cc9f728.jpg" width="30px"><span>秋天的透明雨🌧️</span> 👍（3） 💬（1）<div>本机环境python 3.7.6， 需要把context = zmq.Context() 改成 context = zmq.Context.instance()</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/a8/0ce75c8c.jpg" width="30px"><span>Skrpy</span> 👍（34） 💬（4）<div>我以为实战篇会有量化交易平台的实现的…可是老师只讲了一些 Kafka 的概念，39讲的 Django 也只是官方文档的例子…老师有没有更好的实战教程？</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（9） 💬（0）<div>思考题
1.如果把time.sleep(1)放在while 循环的最后，订阅者会接收不到发布者发布的第一个消息‘server cnt 1’，因为订阅者和发布者建立连接需要时间，连接好后已经是在第一个消息发布之后了，自然订阅者会手不到第一个消息的。
2.多个发布者的话，不同的发布者使用不同的端口，而后订阅者根据匹配的端口读取消息。</div>2019-08-02</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（7） 💬（1）<div>思考题
1.如果把time.sleep(1)放在while循环最后，订阅者接收不到发布者的第一条消息，因为，发布者和订阅者建立连接需要时间，在我的电脑中，建立连接的时间不低于0.5秒，并且通过程序运行表明，只在发布者while循环中第一次执行sleep(1)，以后每次循环不执行sleep(1),接收者也能正常接收到发布者信息，
至于具体原因，需要老师讲解一下。
2.如果有多个发布者，每个发布者应该绑定一个socket
              例如，发布者1，socket.bind(&#39;tcp:&#47;&#47;*:6666&#39;)
                        发布者2，socket.bind(&#39;tcp:&#47;&#47;*:6667&#39;)
   对于接收者来讲，可以接收一个或多个发布者的消息，
              接收发布者1消息，socket.connect(&#39;tcp:&#47;&#47;127.0.0.1:6666&#39;)
              接收发布者2消息，socket.connect(&#39;tcp:&#47;&#47;127.0.0.1:6667&#39;)</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（6） 💬（0）<div>把发布者的time.sleep(1)放到循环语句后面，会导致第一条消息(server cnt 1)丢失。原因是此时发布者应该还没有和zmq完全建立通讯通道，导致消息丢失</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/59/d2/c309928f.jpg" width="30px"><span>教授</span> 👍（2） 💬（0）<div>老师，我用pyzmq，发布者&#47;订阅者模式，发现有一个订阅者突然接收不到信息了，之前能接收，请老师指点一下</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（2） 💬（0）<div>把time.sleep(1)放到while后面，消费者第一个数据包(server cnt 1)收不到</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ae/89/81404170.jpg" width="30px"><span>Carl</span> 👍（1） 💬（0）<div>我理解新增一个发布者2，将bind方法改为connect，但是测试发现并不能够接收到发布者2发布的信息</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（1） 💬（0）<div>思考题：
（1）time.sleep(1)放到循环最后，发布者第一次发送的消息，没有被订阅者接受到。
由于对zmq知之甚少，个人肤浅理解：可能是zmq的发布者在绑定端口时，中间件可能会做一系列的检测，如检测网络，检查端口的可用性等等，会有一定的延迟，因此需要在端口绑定后延迟一秒。

（2）对于有多个发布者，zmq要求不同的发布者绑定到不同的端口，多个发布者还是可以正常发送信息，而对于订阅者，需要绑定对应的发布者端口才能接受到发布者发送的信息。

以上见解，有错误之处请老师指正。</div>2020-03-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKxqOFPRvW2d6WEC705zuSSvxBOBxibBib4XQxBGAGPOx2bRGqhsSeQkUNa0Z11OJoKbuGsNaMR4GNg/132" width="30px"><span>hel793</span> 👍（1） 💬（0）<div>需安装 pyzmq</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（1） 💬（0）<div>socket.bind(&#39;tcp:&#47;&#47;*:6666&#39;)这句话里域名写成*是不是指任意域名？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第37讲打卡~</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/89/23/e71f180b.jpg" width="30px"><span>Geek_fc975d</span> 👍（0） 💬（0）<div>老师，使用pip install zmq的安装方式安装后，发现很多函数不能用，请教这是怎么回事？</div>2022-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/43/d5/358b4426.jpg" width="30px"><span>06</span> 👍（0） 💬（0）<div>文章提到中低频策略可以使用消息队列提高稳定性，那么高频策略有没有类似的实现？</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/27/85/ddeeaf30.jpg" width="30px"><span>dived</span> 👍（0） 💬（0）<div>不知道我得实现是一个和老师说得意思不
c.py
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind(&#39;tcp:&#47;&#47;127.0.0.1:6666&#39;)
s1.py&#47; s2.py
    print(&#39;send1&#39;) &#47; print(&#39;send2&#39;
    socket = context.socket(zmq.PUSH)
    socket.connect(&#39;tcp:&#47;&#47;127.0.0.1:6666&#39;)
</div>2021-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/3d/35d6670d.jpg" width="30px"><span>Claywoow</span> 👍（0） 💬（2）<div>老师，celery这个消息队列和您讲述的这两种有什么区别嘛？生产环境大多哪种消息队列比较实用和高效</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>今天谈到了数据结构，我想请教一下老师，数据结构如果是基于链表的，在其它语言中会大量使用指针和引用，但是基于python语言变量含义的特殊性及参数传递的特性，在实现链表结构的时候有没有比较明确的指导呢？

感觉9咱们专栏有很多点都和数据结构的实现有关，但是比较分散。</div>2019-08-02</li><br/>
</ul>