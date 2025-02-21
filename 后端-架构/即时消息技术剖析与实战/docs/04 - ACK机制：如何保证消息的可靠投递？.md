你好，我是袁武林。

在第一节的课程中，我们说到了即时消息系统中的四个重要特性，实时性、可靠性、一致性、安全性。

上一节课我们从如何保证消息实时性方面，了解了业界常用的一些方式以及背后具体的原理。那么今天我们接着来讲一讲，在即时消息的系统架构设计里，如何来保证消息的可靠投递。

首先，我们来了解一下，什么是消息的可靠投递？

站在使用者的角度来看，消息的可靠投递主要是指：消息在发送接收过程中，能够做到不丢消息、消息不重复两点。

这两个特性对于用户来讲都是非常影响体验的。我们先说一下不丢消息。

试想一下，你把辛辛苦苦攒到的零花钱打赏给了中意的“主播小姐姐”，但由于系统或者网络的问题，这条对你来说至关重要的打赏消息并没有成功投递给“主播小姐姐”，自然也就没有后续小姐姐和你一对一的互动环节了，想想是不是很悲剧？

消息重复也不用多说，谁也不愿意浪费时间在查看一遍又一遍的重复内容上。

那么在一般的IM系统的设计中，究竟是如何解决这两大难题的呢？下面我们结合一些简单的案例，来看一看“不丢消息”“消息不重复”这些能力，在技术上到底是怎么实现的。

## 消息丢失有哪几种情况？

我们以最常见的“服务端路由中转”类型的IM系统为例（非P2P），这里解释一下，所谓的“服务端路由中转”是指：一条消息从用户A发出后，需要先经过IM服务器来进行中转，然后再由IM服务器推送给用户B，这个也是目前最常见的IM系统的消息分发类型。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/58/f2c6d65b.jpg" width="30px"><span>王棕生</span> 👍（117） 💬（5）<div>有了 TCP 协议本身的 ACK 机制为什么还需要业务层的ACK 机制？
答：这个问题从操作系统(linux&#47;windows&#47;android&#47;ios)实现TCP协议的原理角度来说明更合适： 
     1  操作系统在TCP发送端创建了一个TCP发送缓冲区，在接收端创建了一个TCP接收缓冲区；
     2  在发送端应用层程序调用send()方法成功后，实际是将数据写入了TCP发送缓冲区；
     3  根据TCP协议的规定，在TCP连接良好的情况下，TCP发送缓冲区的数据是“有序的可靠的”到达TCP接收缓冲区，然后回调接收方应用层程序来通知数据到达；
     4  但是在TCP连接断开的时候，在TCP的发送缓冲区和TCP的接收缓冲区中可能还有数据，那么操作系统如何处理呢？ 
           首先，对于TCP发送缓冲区中还未发送的数据，操作系统不会通知应用层程序进行处理（试想一下：send()函数已经返回成功了，后面再告诉你失败，这样的系统如何设计？太复杂了...），通常的处理手段就是直接回收TCP发送缓存区及其socket资源；
           对于TCP接收方来说，在还未监测到TCP连接断开的时候，因为TCP接收缓冲区不再写入数据了，所以会有足够的时间进行处理，但若未来得及处理就发现了连接断开，仍然会为了及时释放资源，直接回收TCP接收缓存区和对应的socket资源。

总结一下就是： 发送方的应用层程序，调用send()方法返回成功的时候，数据实际是写入到了TCP的发送缓冲区，而非已经被接收方的应用层程序处理。怎么办呢？只能借助于应用层的ACK机制。</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/8f/551b5624.jpg" width="30px"><span>小可</span> 👍（43） 💬（1）<div>两个ack的作用不同，tcp的ack表征网络层消息是否送达；业务层ack是真正的业务消息是否送达和是否正确处理，达到不丢消息，消息不重复的目的，即我们要保证的消息可靠性</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/a9/ae10f6cd.jpg" width="30px"><span>影随</span> 👍（21） 💬（3）<div>老师您好，服务A向客户端B发送消息，第一次发送msg1，timestamp假设为 01（简写），序号为 01，这条消息因为某种原因，未存储时间戳和序号01，也未发送ack通知。A第二次发送msg2，timestamp为 02，序号为02，它做了存储，保存了最新的时间戳和序号。A第三次发送 msg3，此时B宕机了。 等B重启时，向A发送最新的时间戳和序号 02， 那么A发送大于02序号的消息，即 msg3， 那么 msg1如何保证不丢失呢？  </div>2019-09-10</li><br/><li><img src="" width="30px"><span>墙角儿的花</span> 👍（8） 💬（4）<div>1、回答老师的问题：TCP层的ACK只是TCP包分片的ACK，并不能代表整个应用层的消息得到应答。理论上操作系统的TCP栈肯定是知道整个TCP消息得到对方的ACK了，但是操作系统好像并没提供这种接口。发送成功的接口返回成功通常都表示为操作系统发送成功了，至于链路上有没有问题就不知道了。
2、向老师请教下其他问题，恳请解答。
A、如果接收方本地保存了所有曾经接收过的消息id，接收方是很方便去重，但是，如果用户clear了本地消息该怎么办，是要一直存储所有已经接收的消息id吗
B、对于防范服务器宕机的时间戳机制，其实本质是序号，但是网络传输并不能保证服务器按序号发送的消息，低序号的就一定先于高序号的被接收方接收。所以如果高序号的已经被接收方处理且应答，而某个低序号的消息还没得到接收方应答的场景，通过序号保证完整性貌似不可取。</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（7） 💬（5）<div>老师 从客户端到服务端，服务端要对客户端发送的消息去重， 用哪个字段呀。 这个字段应该是客户端发送消息由客户端产生的吧。 那如何能保证这个字段全局唯一，而不是客户端A 产生了和客户端B 同样的这个字段？ 去重的步骤是什么呢？ 是去数据库查找是否有这个字段的内容嘛？</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/34/0c2c1200.jpg" width="30px"><span>L</span> 👍（6） 💬（3）<div>老师你好，关于完整性检查我有个问题。
下次会话时用户重装了软件&#47;清空缓存&#47;甚至更换了设备导致本地没有上次会话的时间戳了，这时候岂不是无法获取丢失的那些消息？</div>2019-10-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELZPnUAiajaR5C25EDLWeJURggyiaOP5GGPe2qlwpQcm5e3ybib8OsP4tvddFDLVRSNNGL5I3SFPJHsA/132" width="30px"><span>null</span> 👍（5） 💬（1）<div>老师，您好！

文中提到：用户 A 等待 IM 服务器返回超时，用户 A 被提示发送失败。但可以通过重试等方式来弥补。

我有个疑问：客户端在超时时间内没有收到响应然后重试，但实际上，请求已经在服务端成功处理了。这时用户 A 和 IM 服务器的状态就不一致了，用户 A 看到的是发送失败，而 IM 服务器却是处理成功的。

同样的，IM 服务器在等待​ ACK 通知也存在这样的问题：IM 服务器在有限的重试次数内，一直没收到 ACK 通知，而消息却成功推送给了用户 B，IM 服务器和用户 B 的状态也不一致了。

在有限的重试次数内（线上不可能无限重试吧？），无法得到确定的返回结果，导致客户端和服务端的状态不一致，如何解决这个问题吖？
​</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（5） 💬（2）<div>您好，我在读到在消息完整性检查那里时有些疑惑，如果服务端将msg2发出之后，服务端和客户端断链，导致客户端无法接收消息，那么重新连接之后，是可以发送时间戳检测进行重传的。
但是，如果在服务端存储了发送方客户端发送的消息后，正准备将该消息推送给接收方客户端时发生宕机，那么当接收方客户端和服务端重新连接之后，服务端该如何知道自己要将之前存储的消息发送给接收方的客户端呢？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（5） 💬（1）<div>保证消息不丢失的做法：
1、发送消息阶段通过客户端的发送重试机制，和服务端的去重，保证发送时消息不丢失不重复
2、服务端推送阶段通过ACK确认机制和客户端去重保证推送时消息不丢失不重复
3、最后使用时间戳的同步机制来保证消息的完整性，这个应该要在服务端无法触发重推消息时才进行的一个操作</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/55/198c6104.jpg" width="30px"><span>小伟</span> 👍（3） 💬（1）<div>思考题：TCP和业务层做在的维度不一样，故虽然两者的ACK机制原理一样，但不能相互替代。TCP的ACK完成只能说明数据包已经正确传输完毕，但不代表数据包里的数据已经被正确处理完毕。业务层的ACK就是来保证数据包里的数据正确处理完毕的。TCP的ACK完成是业务层ACK的前提，业务层ACK完成是业务规则上的保证。</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/09/31/535d60bc.jpg" width="30px"><span>RuBy</span> 👍（3） 💬（4）<div>老师，请问消息落地的话传统的redis+mysql是否会有性能瓶颈？是否会考虑leveldb（racksdb）这种持久化kv存储呢？</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/44/d5cf762b.jpg" width="30px"><span>段先森</span> 👍（3） 💬（2）<div>想问一下老师，一般来说对于直播的业务场景，消息存储这个环节用什么MQ会比较好些</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（2） 💬（1）<div>TCP层的ACK机制只能确保传输层（或者说网络传输上）消息传递没有丢失，并不能从“业务层”角度确保消息已经完全正确投递和展示。网络包到达客户端后，可能会出现解析失败，落db失败的情况。</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/5b/d2e7c2c4.jpg" width="30px"><span>时隐时现</span> 👍（2） 💬（1）<div>消息ID要求全局唯一且时间趋势递增吗？如果是这样，像微信和QQ这样体量的系统，要构建一个多大的消息序列集群才能满足需求？另外，微信和QQ的消息序列集群是全球唯一一个，还是多个集群并行部署？如果是全球唯一1个集群，跨半球的消息发送会不会延时很大，如果是多个集群，又如何保证时间趋势递增？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/20/1e/23e6109f.jpg" width="30px"><span>小袁</span> 👍（2） 💬（1）<div>有2个问题
1 服务端发消息给客户端，没收到ack重试有最大次数吗？是像tcp那样一直重试直到收到ack吗？

如果客户端有bug导致处理消息一直失败，是否会导致服务端一直在重试，然后队列就满了。

2 收到消息后处理失败了要怎么处理，是不做等待服务端重发吗？</div>2019-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（2） 💬（1）<div>老师您好，我想问下服务端IM先后推送两条消息msg0、msg1、msg2到客户端B，如果msg0、msg2先到达，此时客户端B应该不会更新到msg2的发送时间戳吧，而是等待msg1到达。如果此时陆续msg3、msg4消息到达，msg1还没到达，客户端是否也可像tcp一样，发送3个msg0消息到服务端IM，而不需要等待超时就让IM服务端立即重发msg1，这样可以降低延时，等到msg1到达客户端B后，可以直接将时间戳更新至最新到达消息的时间戳吧，而不是msg1的时间戳，不知道的理解的对不对，老师有时间看看</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/ca/9f57577b.jpg" width="30px"><span>长江</span> 👍（2） 💬（4）<div>有了 TCP 协议本身的 ACK 机制为什么还需要业务层的 ACK 机制？
1.TCP属于传输层，而IM服务属于应用层，TCP的ACK只能保证传输层的可靠性，即A端到B端的可靠性，但是不能保证数据能够被应用层正确可靠处理，比如应用层里面的业务逻辑导致消息处理失败了，TCP层是不知道的。
2.TCP虽然是可靠性传输协议，但是如果传输过程中，假如数据报文还没被接收端接收完毕，接收端进程服务崩溃了，而用户又不再立刻启动这个应用程序，这也会导致消息丢失的吧。
所以不能只依靠TCP的ACK机制的。</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（1） 💬（1）<div>如果客户端B离线了一段时间，当重连的时候服务器端已经积累了大量B的消息，比如999+条聊天记录，那么服务器端要逐条推送并且逐一更新时间戳么？还是可以批量推送，批量推送又如何保证客户端B的时间戳是最后一条的？</div>2019-12-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJI35InfGaliaSwAmOyk0kPV6n41icaYLcqRzrAA4hpRGRyictPgmabXY3lyQBtECTpibl6cYIsUrS1KA/132" width="30px"><span>铱</span> 👍（1） 💬（1）<div>老师有个问题请教您，如果在说到服务端发送消息到客户端时为了保证消息重复发送客户端时客户端能够识别重复需要带上一个当前会话范围唯一的sid，同时为了防止服务端发送消息和客户端接收消息步调不一致需要传送一个timestamp（也可用全局顺序号代替，这样的话是否可以直接让sid为一个全局顺序号，从而替代上面所提到sid+timestamp的功能？</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（1） 💬（1）<div>tcp的ack只保证网络传输过程中的消息可靠达到。但是，在业务场景上网络传输只是其中的一个步骤，所以，不能保证。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（1） 💬（1）<div>老师 为什么服务器需要维护一个ack列表呀，它为啥不能像client发送端那样 发送之后等待回应， 如果没收到， 在重发？
或者 client发送端为啥不维护一个ack列表， 而是发送后等待回应，没回应再重发</div>2019-10-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqZjLcrj0O1D0EnDmbvROsYjic6cqiciabYMGUzYL3O90egkmgvAVT6WqBUKodCgyAy0hSuibxiaibRI2Ew/132" width="30px"><span>风尘</span> 👍（1） 💬（1）<div>用户B，只用一个时间戳的话，是否会出现这样的问题：
服务器给用户B 推送两条消息：消息1，消息2。用户B 收到了消息2，未收到消息1，然后下线了。
重新上线之后，由于记录了消息2 的时间戳，用于跟服务端比较，服务端只会推比消息2 更晚的消息。
消息1 就丢失了。</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3d/02/ecdb4e66.jpg" width="30px"><span>东东🎈</span> 👍（1） 💬（1）<div>老师，服务端消息重发，是需要单独开一个定时器是吧，多少秒一次合适呢？一次拉取多少条消息进行重发呢？谢谢</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（1） 💬（1）<div>如果客户端一直连接不上，IM服务器会怎么处理，缓存一段时间的数据?</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7e/dd/8098a7e0.jpg" width="30px"><span>阳阳</span> 👍（1） 💬（1）<div>请问一下老师：如果im服务器发给用户的第一条消息，用户b没有给业务层ack，但是im服务器紧接着又收到了第二条消息往用户b发送，此时用户b返回了正常ack。那么第一条消息在超时的时候会从队列里拿出来重传，假设用户b收到且返回ack成功，这个时候第一条消息</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/d1/f427b83e.jpg" width="30px"><span>javaworker</span> 👍（0） 💬（1）<div>老师，为什么业务端有对sequenceId的去重，IM端还要有去重呐？IM端不去重也可以吧，反正最终发到业务端有去重啊</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/dc/fc9efd01.jpg" width="30px"><span>HELSING</span> 👍（0） 💬（1）<div>ack 重传需要设置重传次数吗？比如接收端业务逻辑有异常，每次处理都抛异常，那服务端要怎么处理？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（0） 💬（1）<div>tcp保证的是网络传输，业务层保证的是消息处理阶段，这两个在不同的层级</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/7d/40/2a0ac40f.jpg" width="30px"><span>五点半先生</span> 👍（0） 💬（1）<div>单聊消息是不可以认为是一种特殊的群聊，存储方式是不是一样的</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/5b/d2e7c2c4.jpg" width="30px"><span>时隐时现</span> 👍（0） 💬（1）<div>评论里有人提到如果客户端清空所有消息，再次上线时如何进行消息完整性检查？是要把所有的历史消息都拉取一遍吗？</div>2019-09-25</li><br/>
</ul>