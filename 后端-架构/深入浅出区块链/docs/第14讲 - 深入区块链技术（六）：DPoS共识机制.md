上一篇文章里，我们讲解了PoS共识机制，这一篇我们来分享PoS的一个扩展机制，这个机制在业界也非常的流行，它叫做DPoS共识机制。DPoS全称是Delegated Proof of Stake，中文翻译过来是代理权益证明。

## 从BM开始聊起的故事

我们聊DPoS时，为什么要从BM聊起呢，

其实，这和聊比特币绕不开中本聪一样，DPoS是BM一手创造的。DPoS不是独立提出的共识算法，而是直接被BM应用到比特股项目中，在稳定运行了3年多后，又接着被BM构造成可复用的区块链工具箱：石墨烯。

虽然应用得很早，但DPoS算法直到2017年才被BM单独拎出来作了一篇“DPoS技术白皮书”，这期间伴随着比特股、Steemit、EOS三个项目的依次发布。

那么到底BM是谁，市场上对这个人的评价为什么富有争议呢？或许我们从了解BM开始，才能体会到DPoS的精髓。

我们在前面的文章中曾简单提过BM，BM的本名是Daniel Larimer，由于他的GitHub昵称是ByteMaster，所以才被称作BM。BM是比特股、Steemit、EOS项目的创始人，截止发稿时，这三个产品的市值均在区块链项目的Top33以内。

与年少成名V神的辍学经历不同，BM 2003年毕业于弗吉尼亚理工学院，获得计算机学士学位，算是正经的科班出身。

BM曾直言不讳地说到：“我的人生目标就是找到自由市场的方案来保护生命、自由和财产”。他认为要达成这个目标，就必须要从货币开始。

我们在数字货币一节提到过，无论是贵金属还是信用货币，都是历史的必然，所以在选择使用什么货币上，BM认为不一定是美元，他希望的是：构造一种自由安全的数字货币。

2009年，他怀揣梦想开始了数字货币的事业，他先发现了比特币，于是不遗余力地推广着这个项目。

然而在2010年，BM指出中本聪10分钟一次的交易确认时间太长了，这样的话，性能会是一个瓶颈，然而这样的想法却遭到了中本聪的暴击：看不懂就算了，我没时间搭理你。

于是，BM觉得比特币不是希望，便着手开发第一个项目——比特股，同时创造出DPoS，把自己的高性能共识算法想法形成了实践。

在这里，我们可以看出DPoS与其他共识机制的第一个区别，就是交易确认时间短。

2014年，当V神还在到处奔走，开始发起以太坊项目的众筹时，当很多项目还是基于比特币的微创新时，比特股就已经横空出世了。

所以比特股一跃成为了当时的明星项目，它的口号是“Beyond Bitcoin”，在这里我们可以感受到极强的攻击性和目的性，也正因为如此，日益强大的比特币社区被树在了它的对立面。

比特股一共有2个版本，比特股在1.0版本之前，某些版本甚至都没有提供向下兼容。虽然后来正式发布了1.0版本，似乎并没有改善多少。糟糕的使用体验，庞大的系统资源开销，还是让尝鲜的用户逐渐流失了。

这时候BM利用了自己手里超过1/3的记账节点，在没有达成社区共识的情况下，强行增发了比特股总量。这一招几乎就是比特股项目的灭顶之灾，社区人就此纷纷退出。

虽然社区萎靡，BM还是继续了开发工作，将比特股升级到了2.0，它的易用性和稳定性勉强可以满足正常使用。随着比特股2.0的发布，BM也同时发布了石墨烯工具箱。

尽管在技术上提供了改进，但比特股社区最终选择让BM离开比特股项目，比特股回到了另一位币圈大佬——巨蟹的手里。随后比特股的发展陷入了长期的低迷，长期在2分，最多到2角钱左右，直到去年的牛市，比特股涨到过2元人民币。

虽然最终离开了比特股，但是BM依然会参与BTS紧急Bug修复工作。与此同时，BM又开发了一款旨在颠覆传统互联网媒体行业的项目——Steemit，这也是开辟了基于区块链Token内容社区的先例。Steemit也是基于石墨烯技术的，它非常流行。

2017年，随着Steemit的成熟，BM宣布退出了Steemit，开展了下一个项目EOS。EOS的目的是要做出区块链行业的操作系统，为开发者提供底层功能，包括并行运算、数据库、账户系统等等。

EOS一经发布，就广受关注，短短五天内，EOS便筹集到了数亿美金，它的代币销售规模在目前为止是最大的。

现阶段的EOS超级节点竞选也体现出了BM强大的影响力。 EOS项目影响力也越来越大，BM因为与V神在区块链上的理念不合，也经常互怼，他们争论的重点是二人对于去中心化的前提假设不同，这也造就了两个不同的设计逻辑，所以，两人的争论过程可以说是非常地吸引眼球了。

我们从BM的个人经历、项目经验、影响力都可以看出BM是一个很懂金融的天才式程序员，同时也是一个有点刚愎自用导致与社区矛盾不断的意见领袖。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/2b/df3983e2.jpg" width="30px"><span>朱显杰</span> 👍（10） 💬（1）<div>中本聪不理BM是有原因的，DPoS已经和区块链原教旨主义去中心化背道而驰，但谁规定区块链一定是去中心化的呢？如果区块链想要有实际落地的应用场景，完全去中心化不太现实，弱中心化是大趋势。</div>2018-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（3） 💬（1）<div>数字货币的推出会对法币产生一定的冲击。如果哪天政府想操控数字货币，那么控制21个节点就可以了，很危险啊</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/fd/1e3d14ee.jpg" width="30px"><span>王宁</span> 👍（3） 💬（1）<div>区块链的分叉与合并这个在哪一节有介绍？
对这一块特别困惑:
1. 分叉中记录的交易是怎么被主链认可合并进去的呢？
2.主链合并完之后理论上会出现交易时间戳较晚的账本在时间较早的前面？这个时候对一个人交易的遍历会产生什么样的影响？
3.会不会出现账户状态不一致的情况。比如根据A链计算的结果一个用户有10个币，根据B链就是的有两个币，对于这种差额之间的交易有没有很好的办法去还原呢？

问的比较浅，诸位见笑，确实蛮纠结这个。</div>2018-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/a8/6f26f14a.jpg" width="30px"><span>unite</span> 👍（2） 💬（1）<div>我想请问老师，如果5G技术得到普及，网络带宽极大提升，是不是就能有效解决记账节点过多时TPS有限的问题？</div>2018-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/10/84a4caf6.jpg" width="30px"><span>徐威</span> 👍（2） 💬（1）<div>DPOS节点间的结盟就无法被解决啊</div>2018-04-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OwlfSZBK8I7dpGtLia70p3e4cXib5ZsbY1vIpXiaWtAowoawJQFNVibGurpKlDwIBXmqZZpHx7RtSwCEyjOepicjstA/132" width="30px"><span>ytl</span> 👍（1） 💬（1）<div>可能备选的节点恶意攻击主节点，以谋求上位。
形成21个主节点的联盟，称霸世界。
主节点集中在一个地区，有环境风险。
</div>2018-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/c8/67a885eb.jpg" width="30px"><span>张军营Jason</span> 👍（0） 💬（1）<div>21个超级节点通过什么方式判断交易有效？不太明白,还是说只有21个节点能发起交易打包</div>2018-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/10/84a4caf6.jpg" width="30px"><span>徐威</span> 👍（0） 💬（1）<div>陈老师觉得类似rsk这样的侧链发布智能合约，有哪些缺陷。相比以太坊、eos</div>2018-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/c3/deae021f.jpg" width="30px"><span>沃野阡陌</span> 👍（2） 💬（0）<div>中本聪不搭理他一定有道理。谢谢老师的讲解，D P O S共识背后有无法解决的人性困境，投票是比较脆弱的机制，所有这些都需要哲学思考。</div>2018-04-25</li><br/><li><img src="" width="30px"><span>文储-极客26</span> 👍（0） 💬（0）<div>拥有出块权的节点多久换一次呢，如果一个节点一直选举不上是不是就意味着他没有收益。</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/2a/a0154ed1.jpg" width="30px"><span>金贵华</span> 👍（0） 💬（0）<div>个人认为，现在区块链数字货币的运行，要思考如何让人的生产价值与数字货币的获取进行挂钩，而不是通过所谓算力来获取数字货币，这种情况是不合理 。</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（0） 💬（0）<div>EOS 原来是  DPoS</div>2021-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>Dpos通过投票的方式推出几个代理节点作为见证人来轮流挖矿，相比pos，它的出矿速度可以很快，根据cap理论，网络势必趋于中心化。dpos让权益最高的见证人挖矿并只使用最长链，尽可能规避了拜占庭错误（最大权益人也是最大损失人），但这些都是软件技术手段，不像pow有那么高的作弊门槛。</div>2021-02-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/g1icQRbcv1QvJ5U8Cqk0ZqMH5PcMTXcZ8TpS5utE4SUzHcnJA3FYGelHykpzTfDh55ehE8JO9Zg9VGSJW7Wxibxw/132" width="30px"><span>杨家荣</span> 👍（0） 💬（0）<div>极客时间第二期
21天打卡行动 12&#47;21
&lt;&lt;深入浅出区块链14&gt;&gt;DPoS共识机制
回答老师问题:有关 DPoS 算法，你能想到有哪些攻击方式吗?
同时展开分叉攻击;
[来源:http:&#47;&#47;www.sohu.com&#47;a&#47;295383153_618509]
今日所学:
1,BM传奇;
2,DPoS 共识算法就是将 PoS 共识算法中的记账者转换为指定节点数组成的小圈子，而不是所有人都可以参与记账,
3,只有这个圈子中的节点才能获得记账权。这将极大地提高系统的吞吐量，因为更少的节点也就意味着网络和节点的可控。
4,TPS = transactions &#47; block_timeTPS 表示区块链每秒能确认的交易数， transactions 是由区块大小 block_size 和平均每笔交易大小决定的，而区块大小受全网网络状态 network_bandwidth 限制，也是由记账节点之间物理带宽 witness_performance 决定的
5,DPoS 共识机制本身将“矿池”纳入系统内部，并把它们统称为见证节点，虽然不会出现中心化挖矿的风险，但是 DPoS 由于节点数不多，并且见证节点权力较大，可以认为 DPoS 本身就是带中心化思路的共识机制。</div>2020-01-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FheCgo4Ovibo0L1vAGgMdZkzQMm1GUMHMMqQ8aglufXaD2hW9z96DjQicAam723jOCZwXVmiaNiaaq4PLsf4COibZ5A/132" width="30px"><span>miniluo</span> 👍（0） 💬（0）<div>为什么说去中心化可以提升资产流通率？流通意味可以带来经济效益。前半句不解，期待回复，谢谢</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>POW，POS，dPOS，均在用吗？哪个用得最多？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/0c/abb7bfe3.jpg" width="30px"><span>blockchain_geek</span> 👍（0） 💬（0）<div>algorand的提出，对共识算法发展有了很大的改进，老师能对algorand谈一下吗</div>2018-06-21</li><br/>
</ul>