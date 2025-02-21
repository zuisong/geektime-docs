你好，我是韩健。

很多同学可能都有这样的感觉，每次要开发分布式系统的时候，就会遇到一个非常棘手的问题，那就是如何根据业务特点，为系统设计合适的分区容错一致性模型，以实现集群能力。这个问题棘手在当发生分区错误时，应该如何保障系统稳定运行，不影响业务。

这和我之前经历的一件事比较像，当时，我负责自研InfluxDB系统的项目，接手这个项目后，**我遇到的第一个问题就是，如何为单机开源版的InfluxDB设计分区容错一致性模型。**因为InfluxDB有META和DATA两个节点，它们的功能和数据特点不同，所以我还需要考虑这两个逻辑单元的特点，然后分别设计分区容错一致性模型。

那个时候，我想到了CAP理论，并且在CAP理论的帮助下，成功地解决了问题。讲到这儿，你可能会问了：为什么CAP理论可以解决这个问题呢？

因为在我看来，CAP理论是一个很好的思考框架，它对分布式系统的特性做了高度抽象，比如抽象成了一致性、可用性和分区容错性，并对特性间的冲突（也就是CAP不可能三角）做了总结。一旦掌握它，你就像拥有了引路人，自然而然就能根据业务场景的特点进行权衡，设计出适合的分区容错一致性模型。

那么问题来了：我说的一致性、可用性和分区容错性是什么呢？它们之间有什么关系？你又该如何使用CAP理论来思考和设计分区容错一致性模型呢？这些问题就是我们本节课所要讲的重点了。我建议你集中注意力，认真学习内容，并学以致用，把CAP理论应用到日常工作中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/ed/ea2cbf3a.jpg" width="30px"><span>Sinclairs</span> 👍（64） 💬（3）<div>CP模型的KV存储，适合用于提供基础服务，保存少量数据，作用类似zookeeper。
AP模型的KV存储，适合查询量大的场景，不要求数据的强一致性，目前广泛应用于分布式缓存系统。
一点思考，不知道对不对？</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/69/c02eac91.jpg" width="30px"><span>大漠胡萝卜</span> 👍（37） 💬（2）<div>网络分区，怎么理解？</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/70/6411282d.jpg" width="30px"><span>陈</span> 👍（29） 💬（1）<div>cp模型适合要求acid场景，比如银行转账。ap模型适合只要求base的场景，比如网页cdn场景，不知道理解得对不对。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（22） 💬（28）<div>还是不太明白分区容错性P和可用性A的区别，不都是随时可以提供服务吗？</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（20） 💬（4）<div>知乎上看到的，与各位分享

一个分布式系统里面，节点组成的网络本来应该是连通的。然而可能因为一些故障，使得有些节点之间不连通了，整个网络就分成了几块区域。数据就散布在了这些不连通的区域中。这就叫分区。当你一个数据项只在一个节点中保存，那么分区出现后，和这个节点不连通的部分就访问不到这个数据了。这时分区就是无法容忍的。提高分区容忍性的办法就是一个数据项复制到多个节点上，那么出现分区之后，这一数据项就可能分布到各个区里。容忍性就提高了。然而，要把数据复制到多个节点，就会带来一致性的问题，就是多个节点上面的数据可能是不一致的。要保证一致，每次写操作就都要等待全部节点写成功，而这等待又会带来可用性的问题。总的来说就是，数据存在的节点越多，分区容忍性越高，但要复制更新的数据就越多，一致性就越难保证。为了保证一致性，更新所有节点数据所需要的时间就越长，可用性就会降低。

作者：邬江
链接：https:&#47;&#47;www.zhihu.com&#47;question&#47;54105974&#47;answer&#47;139037688
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/6d/b623562a.jpg" width="30px"><span>霹雳大仙pp</span> 👍（19） 💬（1）<div>以阿里nacos来说，配置中心是cp，保证各节点配置强一致；注册中心是ap，保证了可用性，牺牲了强一致性。
</div>2020-03-09</li><br/><li><img src="" width="30px"><span>zjm_tmac</span> 👍（19） 💬（2）<div>这里的节点1同步给节点2指的是日志复制还是等待节点2的事务提交完成？
如果是日志复制的话，会不会两边提交事务的时间不一致，造成读取不一致。
如果是等待事务提交的话，是不是变成了完全阻塞的，性能很低还有各种各样问题。</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/eb/3165ae4c.jpg" width="30px"><span>NICK</span> 👍（11） 💬（1）<div>可不可以理解成在分布式场景下:
1.  如果业务需要强一致性，则只能牺牲可用性而选择CP模型。
2. 如果业务需要最终一致性即可，则优先满足可用性，选择AP模型？</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1c/e1/c99d1473.jpg" width="30px"><span>longyi</span> 👍（8） 💬（2）<div>受限于 Raft 的强领导者模型。所有请求都在领导者节点上处理，整个集群的性能等于单机性能。这样会造成集群接入性能低下，无法支撑海量或大数据量的时序数据。
&#47;&#47;老师，这里应该是所有的写请求都在领导者节点上处理吧？
&#47;&#47;另外，如果采用multi-raft，每个raft分片都有自己的leader，这样请求将不限于节点，而是在分片的leader上，这样性能也没那么差，老师觉得呢？</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/62/6f/7f8a3bdb.jpg" width="30px"><span>小跑</span> 👍（7） 💬（1）<div>怎么觉得etcd-raft不是严格意义上的一致性，是线性的，只要满足大多数的情况下，哪怕个别节点挂掉，也能对外提供读写服务，所以从这个角度看，它其实一种ap模型吧。</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（7） 💬（10）<div>有个问题想不通，求助一下》
在如何使用CAP理论一节，但就文中定义来说: 选择C时拒绝的是&quot;写入&quot;。选择A时，讨论的是&quot;返回&quot;相对新的信息。
请问，根据这样的定义，某些基于raft的系统中(比如consul)，在分区后，在少数分区一方的拒绝写入，就满足了C，而任何一个节点都支持读取陈旧的数据，又满足了A。CAP齐全，这不是矛盾了么？
我查阅了些资料包括维基百科，对C和A的定义也都如此。
我发现&lt;&lt;designing data-intensive applications&gt;&gt;这本书里有简单的用写入或读取这样的字样，而是一直用&quot;线性一致性&quot;（p336）。

CP的KV存储一般都被借助用于提供给次级应用做严格的一致性的保障。
AP的KV存储一般都被用于海量数据高并发需求下的数据操作，或者是多可用区高延迟的场景下的最终一致性保障。
</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/4b/c385f755.jpg" width="30px"><span>向前走</span> 👍（6） 💬（2）<div>可用性和分区容错性理解上感觉有点类似，都是保证能提供服务，这两个主要的区别是什么呢，老师</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/f0/06ecce19.jpg" width="30px"><span>Skysper</span> 👍（5） 💬（3）<div>文中说节点1和节点2通信异常的时候，仍然能够提供服务，是满足分区容错性的，那么这个仍然能够提供服务怎么理解？是不是同时体现了可用性（一个分区容错性体现了两个特性）？可用性与分区容错性是不是存在一定的边界？同样如果是满足CP的情况下，是不能写入，还可以读吗？或者都不可以，如果都不可以，是不是又不满足P了呢？</div>2020-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/tjhOILHBAmlx6YiaTZJzqzxn1uyB6XpdvGDIZhBn127TYEcoLLzxRiaKvtVd3HllQqPx7cqf2YmibyBUgGGGJPDkw/132" width="30px"><span>zmysang</span> 👍（5） 💬（1）<div>如果meta节点采用ap架构，在网络分隔的情况下，分隔的节点之间独立，各自接收到请求后自行处理，不会进行数据同步，导致不同meta节点上的元数据信息不一致。那么在数据请求的过程，可能会出现对不同节点发送请求有的可以成功有的不能成功的情况，这其实也会造成一种不可用的情况。
针对CP 模型的 KV 存储和 AP 模型的 KV 存储，分别适合怎样的业务场景呢？
针对cp模型的kv存储，适用于对数据的一致性以及可靠性要求比较高的情况；
针对ap模型的kv存储，适用于对延迟要求比较高，对数据一致性要求没有那么高的情况。</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/03/5b/3cdbc9fa.jpg" width="30px"><span>宁悦</span> 👍（4） 💬（1）<div>12306抢票的时候的余票查询是一个AP模型，不管在哪里都能查询到票数，但是票数不一定和实际票数相匹配。
购买车票的时候就是一个CP模型，不管从哪里访问，能不能买到票都是一致的。
就导致明明查询余票的时候有票，但是真正买的时候没票的情况。</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（3） 💬（1）<div>看完老师的例子感觉对cap又有新的认识和理解</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（3） 💬（3）<div>分区容错性和可用性。有点分不清，我感觉说的是一回事啊！都是对外提供可用的服务。</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/3d/54bbc1df.jpg" width="30px"><span>Jaime</span> 👍（2） 💬（1）<div>假设meta节点选择了ap，有一种情况当data节点扩容的时候，因为要做机器间的数据平衡和迁移，那么元数据信息就会发生改变，如果meta节点是ap的时候，客户端读取数据就可能拿到不是最新的元信息，就会发生往data节点写入失败或者查找失败的问题，不知道我说的这种情况对不对? </div>2020-08-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/c38aFXkgKzcaEnz56Zyib5yE88NvzKrnYpJFTe9aodn0cXR2CwA1vs1sP7luwFHeSXuoJlreBtkq3YAFPlmibdibw/132" width="30px"><span>Geek_9ad555</span> 👍（1） 💬（1）<div>打卡总结下：
1.要想分布式系统稳定运行，首先必须保证内部问题得到解决，不能出现多个山头，也就是分区容忍性。
2. 一致性 分为强一致性，弱一致性，和最终一致性。
       a. 强一致性 对错误零容忍，一点儿错就导致全部不可用
       b.弱一致性允许数据不准确 
       c.最终一致性允许在运行过程中不一致，但是最终必须一致
3. 可用性 
   </div>2020-07-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoZqcVJzUjfu5noOW6OPAh6ibrBicibLmicibnVyVLHdf7GwAzf2th5s1oQ9pUbLpmq2mlVBauUZn8QUnw/132" width="30px"><span>funnyx</span> 👍（1） 💬（2）<div>老师您好，如果在保证分区容错的前提下，两个节点数据同步不及时，会产生数据不一致问题，那这种应该如何处理？是从客户端角度考虑还是从服务端架构重新考虑？</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/ea/ad78ac44.jpg" width="30px"><span>vv</span> 👍（1） 💬（2）<div>kafka的isr是ca模型吧</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/00/3afbab43.jpg" width="30px"><span>88591</span> 👍（1） 💬（1）<div>CP 模型的 KV 存储：对业务数据比较敏感，不允许出错。服务慢一点没关系，但是不能出错。比如金融业务
AP 模型的 KV 存储 :业务的可用性优先，可以允许数据有延迟。比如 ：日志数据</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/49/99ca2069.jpg" width="30px"><span>哼歌儿李</span> 👍（1） 💬（1）<div>CAP 理论是一个很好的思考框架，它对分布式系统的特性做了高度抽象，比如抽象成了一致性、可用性和分区容错性，并对特性间的冲突做了总结</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（1）<div>先回答老师问题CP的KV存储肯定是无法容忍不一致的关键数据比如受理订单数据，宁愿出错暴露出来，不能不一致，不然处理错误的情况更麻烦，还有涉及到钱的转账等业务的。AP的KV可以用作不重要的系统比如日志查询系统或者不重要功能，比如查库存，只要真正购买的时候再做检验就行了.如果一旦分区就不可用体验很差</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/fd/ec24cba7.jpg" width="30px"><span>fcb的鱼</span> 👍（1） 💬（1）<div>您好，请教个问题。假设有这么种情况，当前单节点的mysql数据库有某张表因为写入量极大而导致写入延迟很高(暂时先忽略读的量)，现在想将其扩充为集群部署。但是扩充为集群后，这个写入要怎么做，因为只是单张表的写入量大，也没法拆分表，想问下业内现在对这种场景分布式下怎么进行数据写入的。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（1） 💬（1）<div>CP要求强一致性场景，如各种金融银行等交易系统。分布式事务性比较强。
AP要求不断提供服务可用，现在感觉最贴切的就是12306购票了，在最后存储端才做一致性检验，还没抢到票。整体购票只要求最终一致性吧。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/80/741d9e98.jpg" width="30px"><span>Geek_bc461b</span> 👍（1） 💬（1）<div>如果META节点采用AP的策略，假如出现网络通信故障导致多个META节点之间的元数据不一致的，这种情况下，如果外部系统访问这个集群，每次集群返回的结果可能都不一样。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/7e/e6/8e9a4387.jpg" width="30px"><span>如果一切重来</span> 👍（0） 💬（1）<div>大佬你好，读横向扩展是在牺牲一致性的情况下实现的吧。因为目前来说，大部分节点确保写入成功，则系统就认为写入成功。</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/2f/4f89f22a.jpg" width="30px"><span>李鑫磊</span> 👍（0） 💬（1）<div>文章最后说的延迟指的是什么？相应客户端的延迟？还是数据在副本之间复制的延迟？</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>两者的偏向在上面的CAP三角中说明的很清晰了,就是在CP更加偏向于对于一致性的保证,而AP偏向于对可用性的保证,就好比淘宝发布一个商品,在这个商品发布过程中,我们肯定要保证用户能获取到商铺中的其他商品,保证可用性,但是再下单购买的时候,库存是否充足,就是要保证一致性,避免超卖问题</div>2020-08-11</li><br/>
</ul>