你好，我是韩健。

上一讲，我们了解到，PBFT可以防止备份节点作恶，因为这个算法是主节点和备份节点组成的，那你想象一下，如果主节点作恶（比如主节点接收到了客户端的请求，但就是默不作声，不执行三阶段协议），这时无论正常节点数有多少，备份节点肯定没办法达成共识，整个集群都没办法正常运行。这么大的问题，你该怎么解决呢？

答案是视图变更（View Change），也就是通过领导者选举，选举出新的主节点，并替换掉作恶的主节点。（其中的“视图”你可以理解为领导者任期的，不同的视图值对应不同的主节点。比如，视图值为1时，主节点为A；视图值为2时，主节点为B。）

对于领导者模型算法而言，不管是非拜占庭容错算法（比如Raft），还是拜占庭容错算法（比如PBFT），领导者选举都是它们实现容错能力非常重要的一环。比如，对Raft而言，领导者选举实现了领导者节点的容错能力，避免了因领导者节点故障导致整个集群不可用。而对PBFT而言，视图变更，除了能解决主节点故障导致的集群不可用之外，还能解决主节点是恶意节点的问题。

对你来说，理解视图变更，可以理解拜占庭容错算法如何处理领导者故障和作恶。这样一样，从07讲到13讲（非拜占庭容错场景到拜占庭容错场景），你就能更全面地理解领导者选举的原理，和能解决的问题了，这样当你后续熟悉其他领导者选举算法，或设计自己的领导者选举算法时，也能更加的得心应手了。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/68/93c05ab0.jpg" width="30px"><span>laugh</span> 👍（6） 💬（1）<div>PBFT 全称 Practical Byzantine-Fault-Tolerant</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（4） 💬（1）<div>不能处理客户端请求，因为此时主节点已经出问题了，无法进入预准备阶段。</div>2020-06-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（4） 💬（1）<div>专栏更新完了，老师还在给我们加餐，为老师的付出点赞！老师，六一快乐！</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ca/cbce6e94.jpg" width="30px"><span>梦想的优惠券</span> 👍（2） 💬（1）<div>当恶意节点为主节点的时候，当客户端请求的时候，主节点有有可能传递恶意信息给其他节点，然后返回给客户端吗?</div>2021-01-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELC6LzMPYfq0kyTJOcaEo2Lsic8ETuFX8MLzn320E1GxgFMRXTTFoVChicswWViclvVh8ZfU4zUoAznQ/132" width="30px"><span>Geek_c7118e</span> 👍（0） 💬（1）<div>f是怎么知道的，怎么知道叛将的数量</div>2021-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/YicovLZyvibpkfJwuAib1FEyibVDN6Oia1Wsg7jibT0uTj0UDH75KAX6vfSvstjy1IHTW7WpNbMlZZO9SnGoPj3AE2DQ/132" width="30px"><span>要努力的兵长</span> 👍（0） 💬（0）<div>13讲说，客户端未收到 f+1 个一致响应消息，认为集群发生故障  重新发起请求。
 这个地方说，  同样的情况 是怀疑 主节点叛变  然后向 所有节点发送消息 触发视图变更选举新 主节点。    老师 能详细说说 这两种区别吗？？？  还是说 是决定重新请求还是 去触发视图变更， 全看 客户端自己的意愿？</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（0） 💬（0）<div>韩老师，“给不同的预准备请求分配不同的序号“不是应该的吗？给不同的预准备请求分配相同的序号，才会导致混乱吧？</div>2020-08-16</li><br/>
</ul>