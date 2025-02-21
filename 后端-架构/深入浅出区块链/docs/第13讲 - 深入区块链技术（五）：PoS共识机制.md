上一篇我们讲到了PoW共识机制，这一篇我们就来分享另外一种共识机制，PoS共识机制。

PoS全称是Proof of Stake，中文翻译为权益证明。这一篇我们会将PoS与PoW对比讲解，帮助你加深理解。

## PoS的由来

PoS最早出现在点点币的创始人Sunny King的白皮书中，它的目的就是为了解决使用PoW挖矿出现大量资源浪费的问题。PoS共识机制一经提出就引起了广泛关注，Sunny King 也基于PoW的基础框架实现了第一代PoS区块链：点点币。

PoW的具体实现有很多版本，但它们大多只是在挖矿算法上有所改进，主体逻辑并没有发生质的变化。PoS包含了多个变种实现，每个变种往往会涉及区块链代币经济模型的改动，可以说是牵一发而动全身。

这些实现有点点币、黑币、未来币、瑞迪币，它们都推动了PoS机制的发展，PoS研究前沿还有以太坊的 Casper ，以及 Cardano 的Ouroboros。

那到底是什么样的机制导致PoS具有这样的特性呢？让我们来看一看。

## 什么是PoS？

在讲PoS之前，我先来讲一个叫做币龄的概念，币龄这个概念其实很好理解，它的英文是 CoinAge，字面意思就是币数量乘以天数。

比如你有100个币，在某个地址上9天没有动，那么产生的币龄就是900，如果你把这个地址上这100币转移到任意地址，包括你自己的地址，那么900个币龄就在转移过程中被花费了，你的币数量虽然还是100个，但是币龄变更为0。币龄在数据链上就可以取到，任何人都可以验证。

我们回过头来看看PoS究竟是什么，区块链共识机制的第一步就是随机筛选一个记账者，PoW是通过计算能力来获得记账权，计算能力越强，获得记账权的概率越大。

PoS则将此处的计算能力更换为财产证明，就是节点所拥有的币龄越多，获得的记账的概率就越大。这有点像公司的股权结构，股权占比大的合伙人话语权越重。

以上算是简述了PoS的概念，实际上，PoS的发展经历了三个版本，第一个版本是以点点币为代表的PoS1.0版本，这个版本中使用的是币龄；第二个版本的代表是黑币（blackcoin），对应使用的是币数量，相当于是财产证明，后面黑币又升级到PoS3.0，这个版本又回到了币龄。

PoW早在比特币出现之前就已经应用了，而PoS是才是真正意义上为了区块链而创造出来的概念。

## PoS的实现原理

好了，现在我们开始讲解PoS的具体实现原理吧。这一部分公式较多，如果你在收听音频，可以点击文稿查看。

通过上一篇我们知道PoW挖矿的基本逻辑和步骤，我们先寻求一个nonce小于目标值，这一步用公式可表示为：

**Hash (block\_header) &lt; Target**

从公式中我们可以看到，PoW下所有矿工的目标值是一样的，只要计算结果哈希小于目标值即可，简化来看就是前导0的个数。

而在PoS系统中，这个公式变更为：

**Hash (block\_header) &lt; Target * CoinAge**

我们可以看出多引入了一个变量叫做CoinAge，也就是币龄，这里就有意思了。

这个变量为会造成每个矿工看到的目标值不一样，如果你的币龄越大，也就意味着你的获得答案越容易。这里的Target与PoW一致，与全网难度成反比，用来控制出块速度的。

例如当前全网的目标是4369，A矿工的输入的币龄是15，那么A矿工的目标值为65535，换算成十六进制就是0xFFFF，完整的哈希长度假设是8个字节，也就是0x0000FFFF。

而B矿工比较有钱，他输入的币龄是240，那么B矿工的目标值就是0x000FFFFF。你如果仔细观察肯定会发现，相比A矿工的目标值，B直接少了一个零。即如下：

- A 矿工 Hash( block\_header ) &lt; 0x0000FFFF
- B 矿工 Hash( block\_header ) &lt; 0x000FFFFF

所以B矿工获得记账权的概率肯定要比A高。

具体代码分析这里就不讲解了，这里需要币龄作为输入，如果我们写示例代码也只是一个简单的参数，PoS需要放到区块链的语境中才能运作。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/62/0a/26d00cb9.jpg" width="30px"><span>花子翁</span> 👍（4） 💬（2）<div>随着 ERC20 类型的标准合约代币的出现，这个问题被解决了，不再需要第一阶段改成 PoW，也可以将代币分散出去。  求解</div>2018-05-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUOdXYUhEIv5Ky7It6crJcUvxv7eGARYfoRbwicxyriaA2d8RgAXJT2DAM5OnEc60uibwEvF9OGoJng/132" width="30px"><span>陈浚琦</span> 👍（1） 💬（1）<div>验证节点和账号是如何绑定的？如何将奖励给到节点账户？

您的回复：coinbase交易，由矿工自己填的。

老师，您好，有项目参考，或者资料吗？
我现在使用Tendermint+Ethermint，发现节点和账户是没有绑定的，所以区块奖励它给到了一个
0x0000000000000000000000000000000000000000，也就是没有实现节点奖励，按照您的解释应该是它安装后会生成一个coinbase账户，所有的节点奖励会给到这个账户。</div>2018-04-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUOdXYUhEIv5Ky7It6crJcUvxv7eGARYfoRbwicxyriaA2d8RgAXJT2DAM5OnEc60uibwEvF9OGoJng/132" width="30px"><span>陈浚琦</span> 👍（1） 💬（1）<div>验证节点和账号是如何绑定的？如何将奖励给到节点账户？</div>2018-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/2f/59f8d577.jpg" width="30px"><span>小书童</span> 👍（1） 💬（1）<div>&quot;比如在 PoS 系统上挖矿几乎没有成本&quot;，这个不太理解。因为币龄的存在，在pos上挖矿，不同的矿工难度不一样，但还是要耗电费的呀。</div>2018-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/e5/87400c85.jpg" width="30px"><span>duer</span> 👍（1） 💬（1）<div>听完这两期节目，我最大的感受是，区块链技术对技术和算法的选型和使用l不仅仅是技术决策，更多的是商业逻辑和经济学原理，这在产品设计和技术管理的启发非常大，谢谢老师</div>2018-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/a8/6f26f14a.jpg" width="30px"><span>unite</span> 👍（1） 💬（1）<div>讲的非常好，感谢老师！</div>2018-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/1e/5f095c66.jpg" width="30px"><span>恒念</span> 👍（0） 💬（1）<div>感觉有点问题应该是pos在区块链出现前就有，而pow的应用在区块链出现后吧</div>2018-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/2b/df3983e2.jpg" width="30px"><span>朱显杰</span> 👍（0） 💬（1）<div>对于文中提到的PoS节点离线问题的解决办法，如果把节点在线时长作为币龄，是不是可以解决这个问题呢？</div>2018-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/b8/82acc94d.jpg" width="30px"><span>teletime</span> 👍（0） 💬（2）<div>使用币数量有，无成本利益问题，使用币龄有没有呢？如果有，为什么不直接使用币数量，至少币数量方法，可以解决文中提到的二、三、四。如果没有，为什么币龄方式没有，它有什么内在的成本，拥有它一段时间需要什么成本？</div>2018-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/0a/26d00cb9.jpg" width="30px"><span>花子翁</span> 👍（7） 💬（0）<div>离线怎么挖矿，将实时交易放入区块和广播区块给其他节点离线怎么能操作？？？</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（1） 💬（0）<div>Pos，权益证明，这里权益可以是币数、币龄等，高权益的节点获取记账权的概率就高，这可以解决pow算力浪费问题以及一定程度解决记账权被控制后的作弊问题，但由此带来的问题更严重。由于挖矿难度降低，挖矿所需的算力成本大减，旷工对分叉的容忍性高，币价不稳定。记账权与币龄挂钩，虽然币龄会随时间衰减，但节点也可以利用囤积币龄发动攻击，相比pow，它是用软件协议的手段来替代硬件手段，相比pow存在转漏洞的风险。</div>2021-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJF8g6VG6Eb775PbjibPwt8S8nt7ILKXibwlhGb9xkhSAcPuZWoct0D1ecicqsCJsEtzGCU8elI9eZyQ/132" width="30px"><span>Yue Wang</span> 👍（0） 💬（0）<div>如果我的币数量小于1呢，那是不是挖矿的难度反而在原来target基础上变大了？</div>2022-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/x307v1K8rWicianp7Nr7I3JKlEbp2ePV1wHlicxSPkF9m2ztttwBUjibJ2btmdH2dveej2gD2KOZsqDJvR1dia2sD8g/132" width="30px"><span>Geek_9e71fc</span> 👍（0） 💬（0）<div>分叉怎么理解啊</div>2022-04-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL7KRGHBE62Nw0tBYkBXyDib0VHZsEE6LVmXDAsDvVj37D9Ny9Dd9l2bs6LPVIAvpC8s4F5SIUCibibg/132" width="30px"><span>田永鹏</span> 👍（0） 💬（0）<div>派币用的就是pos 挖矿机制吧</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（0） 💬（0）<div>EOS 用的 POS</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5d/d4/e5ea1c25.jpg" width="30px"><span>sun留白</span> 👍（0） 💬（0）<div>请问老师离线挖矿，为何在pos币龄机制下是灾难？</div>2020-02-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/g1icQRbcv1QvJ5U8Cqk0ZqMH5PcMTXcZ8TpS5utE4SUzHcnJA3FYGelHykpzTfDh55ehE8JO9Zg9VGSJW7Wxibxw/132" width="30px"><span>杨家荣</span> 👍（0） 💬（0）<div>哪些区块链项目使用了 PoS 共识机制呢?
点点币（PPCoin）和质数币（PrimeCoin）,恒星币，狗狗币
[来源:https:&#47;&#47;www.cnblogs.com&#47;coco1s&#47;p&#47;8513376.html,
https:&#47;&#47;blog.csdn.net&#47;weixin_44172023&#47;article&#47;details&#47;90598951]
今日所学:
1,币龄的概念，币龄这个概念其实很好理解，它的英文是 CoinAge，字面意思就是币数量乘以天数。
2,PoS 的实现原理:Hash (block_header) &lt; Target
3,Hash (block_header) &lt; Target * CoinAge我们可以看出多引入了一个变量叫做 CoinAge，也就是币龄，
4,PoS 似乎完美地解决了 PoW 挖矿资源浪费的问题，甚至还顺带解决了 51% 攻击的问题，这里可以顺便讲一下 51% 攻击是什么，它是指 PoW 矿工如果积累了超过 51% 的算力，则可以一定程度篡改账本。
5,早期 PoS 币种基本都采用了分阶段挖矿，有的叫混合挖矿，其实，我并不同意混合挖矿这个说法，混合就意味着同时。很多币种其实是分了阶段的，即第一阶段是 PoW 挖矿，到第二阶段才是 PoS 挖矿;
6,PoW 系统中,，因为任何的分叉都会造成挖矿成本直接变成负收益，所以这会抵抗分叉的产生，矿工倾向于跟随“最长”的链;
7,由于以太坊部分采用了 PoS 共识，它的名字叫做 Casper，它必须解决上述无成本利益问题攻击。所以 Casper 协议要求PoS 矿工需通过抵押保证金的方法对共识结果进行下注，具体实践结果我们还需要拭目以待。
</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（0）<div>我认为是不是可以枪毙POS？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（0） 💬（2）<div>”PoS 的区块链系统无需外部物理输入“---这一句话没有看懂，PoS仅仅是把难度降低了，为什么没有外部物理输入呢</div>2019-12-03</li><br/><li><img src="" width="30px"><span>Geek_8285e5</span> 👍（0） 💬（0）<div>技术有时候都是分分合合，没有孤立的集中式和分布式。区块链去中心化，但是矿池其实就是中心化管理。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/d4/e21edf06.jpg" width="30px"><span>hanfeng</span> 👍（0） 💬（0）<div>方便到什么程度呢，每个诚实矿工在产生孤块的时候都可以继续挖下去，反正也没什么成本，反正分叉链和主链都可以同时挖，也就是任何持币较少的用户都可以尝试分叉，并且把分叉链广播出去。
 请问，在pos下，持币（s）少的人更有作恶动机，但其在分叉下，1.要分散算力，2.因为持币少而导致计算难度高，这样不就更加没有机会挖到矿了吗？
问题可能略幼稚，提前感谢解疑</div>2018-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/0d/acbf35a1.jpg" width="30px"><span>栐哥</span> 👍（0） 💬（0）<div>blk,
rdd
dcr是pow+pos</div>2018-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/78/20df8694.jpg" width="30px"><span>四正</span> 👍（0） 💬（0）<div>深入浅出！</div>2018-04-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OwlfSZBK8I7dpGtLia70p3e4cXib5ZsbY1vIpXiaWtAowoawJQFNVibGurpKlDwIBXmqZZpHx7RtSwCEyjOepicjstA/132" width="30px"><span>ytl</span> 👍（0） 💬（0）<div>以太坊用pos</div>2018-04-23</li><br/>
</ul>