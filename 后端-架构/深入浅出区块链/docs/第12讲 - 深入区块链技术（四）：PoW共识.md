上一篇文章中，我们谈到了区块链其实就是一种分布式系统，它在技术上并没有跳出分布式系统的理论框架，只是给出了一种不同于计算科学领域的解决方案。今天，我们就来重点聊聊区块链的这种解决方案： PoW 共识机制。

## PoW工作量证明

因为比特币采用了PoW共识机制，所以这个概念才得以被广泛传播。PoW全称Proof of Work，中文名是工作量证明，PoW共识机制其实是一种设计思路，而不是一种具体的实现。

PoW机制其实早在1997年就被提出了，它早期多被应用在抵抗滥用软件服务的场景中，例如抵抗垃圾邮件（所以PoW在邮件服务系统会有所涉及）。

我们借用维基百科的一张图来解释一下PoW机制是如何用在这个场景中的。

为了防止垃圾消息泛滥，接收者并不直接接受来自任意发送者的消息，所以在一次有效的会话中，发送者需要计算一个按照规则约定难题的答案，发送给接受者的同时，需要附带验证这个答案，如果这个答案被验证有效，那么接受者才会接受这个消息。

![](https://static001.geekbang.org/resource/image/c5/82/c5ddd1f74c990471750a8db6ad177182.png?wh=960%2A268)

可以看出PoW的核心设计思路是提出一个计算难题，但是这个难题答案的验证过程是非常容易的，这种特性我们称之为计算不对称特性，我们在“浅谈区块链共识机制”中举的24点游戏的例子就具备了计算不对称特性。

## 如何理解区块链PoW

上面介绍了一般的PoW是什么，那么区块链上的PoW又是如何设计的呢，我们还是以比特币为例子来讲一讲，这个部分会有代码演示，如果你在收听音频，可以点击文稿查看。

在分析拜占庭将军问题的时候可以看出，如果所有节点在同一时刻发起提案，那么这个系统的记账过程将会非常的复杂混乱，为了降低具有提案权的节点数量，采用工作量证明不失为一个好办法。

所以我们需要构造一个计算不对称的难题，这个难题在比特币中被选定为以SHA256算法计算一个目标哈希，使得这个哈希值符合前N位全是0。

举个例子，假设我们给定一个字符串“geekbang”，我们提出的难题是，计算一个数字，与给定的字符串连接起来，使这个字符串的SHA256计算结果的前4位是0，这个数字我们称作nonce，比如字符串"geekbang1234"，nonce就是1234，我们要找到符合条件的nonce。

我们以Python代码作为示例。

```

#!/usr/bin/env python
import hashlib

def main():
    base_string = "geekbang"
    nonce = 10000
    count = 0
    while True:
        target_string = base_string + str(nonce)
        pow_hash = hashlib.sha256(target_string).hexdigest()
        count = count + 1
        if pow_hash.startswith("0000"):
            print pow_hash
            print "nonce: %s  scan times: %s" % (nonce, count)
            break
        nonce = nonce + 1

if __name__ == '__main__':
    main()
```

代码中，我规定了基础字符串是"geekbang"，nonce从10000开始自增往上搜索，直到找到符合条件的nonce值。

我们计算的结果放在图中，你可以点击查看。

```
# 前4位是0
0000250248f805c558bc28864a6bb6bf0c244d836a6b1a0c5078987aa219a404
nonce: 68828  scan times: 58829
# 前5位是0
0000067fc247325064f685c32f8a079584b19106c5228b533f10c775638d454c
nonce: 1241205  scan times: 1231206
# 前7位是0
00000003f41b126ec689b1a2da9e7d46d13d0fd1bece47983d53c5d32eb4ac90
nonce: 165744821  scan times: 165734822
```

可以看出，每次要求哈希结果的前N位多一个0，计算次数就多了很多倍，当要求前7位都是0时，计算次数达到了1.6亿次。这里我同时截图了操作系统当时CPU的负载，可以看到单核CPU负载长时间达到100%。

![](https://static001.geekbang.org/resource/image/6c/b5/6c4b21deef14e84091e477ac1ff6b3b5.png?wh=1462%2A444)

通过上述程序，希望你对区块链PoW机制有个直观的了解。由于结果只能暴力搜索，而且搜索空间非常巨大，作弊几乎不可能，另外符合条件的nonce值也是均匀分布在整个空间中的，所以哈希是一个非常公平且粗暴的算法。

以上代码的基本逻辑就是PoW挖矿过程，搜索到一个目标值就会获得记账权，距离上一次打包到现在未确认的交易，矿工就可以一次性将未确认的交易打包并广播了，并从Coinbase获得奖励。

实际挖矿的基本步骤如下。

1. 生成Coinbase交易，并与其他所有准备打包进区块的交易组成交易列表，并生成默克尔哈希；
2. 把默克尔哈希及其他相关字段组装成区块头，将区块头（Block Header）作为工作量证明的输入，区块头中包含了前一区块的哈希，区块头一共80字节数据；
3. 不停地变更区块头中的随机数即nonce的数值，也就是暴力搜索，并对每次变更后的的区块头做双重SHA256运算，即SHA256(SHA256(Block\_Header))），将结果值与当前网络的目标值做对比，如果小于目标值，则解题成功，工作量证明完成。

如果更深程度去理解的话，PoW机制是将现实世界的物理资源转化成区块链上虚拟资源的过程，这种转化为区块链提供了可信的前提。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/66/68/812ffbac.jpg" width="30px"><span>熊猫</span> 👍（26） 💬（1）<div>自私挖，全节点，双花攻击和重放攻击能分别讲解是什么意思吗？</div>2018-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/3a/23453336.jpg" width="30px"><span>八神</span> 👍（3） 💬（1）<div>交易是用收款方的公钥加密的，除了收款方可以查看，别人无法看，校验这笔交易的人该如何校验呢？必须是收款方才能校验吗？</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1f/14/2c0a2cc7.jpg" width="30px"><span>sunshuai</span> 👍（3） 💬（1）<div>老师   现在是不是出了一个ant e3型号的asic矿机是针对ethash的</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/c3/deae021f.jpg" width="30px"><span>沃野阡陌</span> 👍（3） 💬（1）<div>什麽是coinbase奖励？</div>2018-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b4/3a/02ea71fa.jpg" width="30px"><span>sunny</span> 👍（1） 💬（1）<div>矿池进行计算挖矿，那最终的账簿记账就是由矿池这个中心节点记账，那么矿池内的矿工还会进行记账吗，矿工还会有自己的账簿吗</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（1） 💬（1）<div>「ETHASH 是 Dagger-Hashimoto 的修改版本，它是典型的内存困难型挖矿算法。」请问以太坊的挖矿，矿机是占用大量内存还是占用大量cpu？

我其实是想问，一台主机上能不能部多个挖矿机，比如，门罗和ETH，我以为一个是消耗cpu，一个是消耗内存。</div>2018-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/76/6f10ba8e.jpg" width="30px"><span>skevy</span> 👍（0） 💬（1）<div>举个例子，假设我们给定一个字符串“geekbang”，我们提出的难题是，计算一个数字，与给定的字符串连接起来，使这个字符串的 SHA256 计算结果的前 4 位是 0，这个数字我们称作 nonce，比如字符串 &quot;geekbang1234&quot;，nonce 就是 1234，我们要找到符合条件的 nonce。

老师请问下上边这一段中，给定的字符串geekbang，会随时变化吗？还是固定的
</div>2018-04-28</li><br/><li><img src="" width="30px"><span>塞翁</span> 👍（0） 💬（2）<div>生成 Coinbase 交易，并与其他所有准备打包进区块的交易组成交易列表，并生成默克尔哈希；

这段中，怎么保证收到的交易列表的完整性，如果漏收交易，所有运算都白费了？或者说，这个交易列表完整性是怎么判断的？纯粹按照时间？</div>2018-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/39/c0c41d51.jpg" width="30px"><span>ylshuibugou</span> 👍（0） 💬（1）<div>为什么矿池的特殊在于它可以产生新的区块</div>2018-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/30/ce2cc535.jpg" width="30px"><span>小5</span> 👍（0） 💬（1）<div>看了下精通比特币电子书，这些基本的概念里面都有讲，什么时候能上一些网上搜不到的东西</div>2018-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/73/fd1e37a2.jpg" width="30px"><span>良辰美景</span> 👍（0） 💬（1）<div>我最近听得到吴军老师说比特币交易成本极高。去中心化带来了大量资源的浪费。如果有好的解决办法是个暴富的机会哦</div>2018-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/2b/df3983e2.jpg" width="30px"><span>朱显杰</span> 👍（4） 💬（0）<div>PoS和DPoS就是对pow不环保的改进，不过也带来了新的问题，所以不可能三角还是有一定道理的</div>2018-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e4/c7/7f8be879.jpg" width="30px"><span>山哥</span> 👍（2） 💬（0）<div>老师的表达能力还要在简洁下。


举个例子，假设我们给定一个字符串“geekbang”，我们提出的难题是，计算一个数字，与给定的字符串连接起来，使这个字符串的 SHA256 计算结果的前 4 位是 0，这个数字我们称作 nonce，比如字符串 &quot;geekbang1234&quot;，nonce 就是 1234，我们要找到符合条件的 nonce。


这段文字写的很拗口。。。py代码简单明了。</div>2021-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/g1icQRbcv1QvJ5U8Cqk0ZqMH5PcMTXcZ8TpS5utE4SUzHcnJA3FYGelHykpzTfDh55ehE8JO9Zg9VGSJW7Wxibxw/132" width="30px"><span>杨家荣</span> 👍（1） 💬（0）<div>极客时间第二期
21天打卡行动 9&#47;21
&lt;&lt;深入浅出区块链11&gt;&gt;共识算法与分布式一致性算法
回答老师问题
PoW 工作量证明的挖矿过程是否可以替换成有意义的算法呢，历史上是否有过类似创新?
我想到的是POS权益证明机制;
POS是否会取代POW，好的算法机制需要时间和市场的验证，没有哪个机制会一直适用于社会发展，一定时期内可能会存在一个当时最好的算法机制。
当随着时间的推移社会的进步技术的成熟，必定会有一个更好的算法机制出现，这是事物发展的必然过程。就像电力的早期发明者没有尝试发明太阳能技术或地热能源。但随着时间的发展，事情总会发展到这个阶段。
[来源:https:&#47;&#47;baijiahao.baidu.com&#47;s?id=1631392991136867009&amp;wfr=spider&amp;for=pc]
今日所学:
1,因为比特币采用了 PoW 共识机制，所以这个概念才得以被广泛传播。PoW 全称 Proof of Work，中文名是工作量证明，PoW 共识机制其实是一种设计思路，而不是一种具体的实现。
2,挖矿的基本步骤:
生成 Coinbase 交易，并与其他所有准备打包进区块的交易组成交易列表，并生成默克尔哈希；
把默克尔哈希及其他相关字段组装成区块头，将区块头（Block Header）作为工作量证明的输入，区块头中包含了前一区块的哈希，区块头一共 80 字节数据；
不停地变更区块头中的随机数即 nonce 的数值，也就是暴力搜索，并对每次变更后的的区块头做双重 SHA256 运算，即 SHA256(SHA256(Block_Header))），将结果值与当前网络的目标值做对比，如果小于目标值，则解题成功，工作量证明完成;
3,PoW 挖矿算法大致分为两个大类，第一类叫做计算困难，第二类叫内存困难。
4,PoW 的优势和劣势:
PoW 共识的内在优势在于可以稳定币价，因为在 PoW 币种下，矿工的纯收益来自 Coinbase 奖励减去设备和运营成本，成本会驱使矿工至少将币价维持在一个稳定水平，所以攻击者很难在短时间内获得大量算力来攻击主链。
PoW 共识的外在优势是目前它看起来依然是工业成熟度最高的区块共识算法，所以在用户信任度上、矿工基础上都有很好的受众。
PoW 共识最大的缺点是非常消耗计算资源，耗电耗能源，这一点也一直为人们所诟病。因为每次产生新的区块都会让相当一部分工作量证明白白浪费了，也就是将计算资源浪费了
5,PoW 共识机制是一种简单粗暴的共识算法，它不要求高质量的 P2P 网络资源，它可以为公链提供稳定有效的记账者筛选机制。同时它也面临了挖矿中心化严重的问题，这也促使人们研究出了新的共识机制，</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（0）<div>51%是如何算出来的，比特币出现分支的概率有多大？</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>pow，通过遍历区块头中nonce，直到找到对区块头双重sha后得到比目标值还小的哈希值，即认为解题成功，具有记账权。pow是计算型问题，提高算力就能提高记账概率，要达到控制记账权的目的，需要拥有超过全网51%的算力，这个算力成本极大，但在现在算力集中化的环境下，如果多个矿池联合起来是可以超过这个门槛的，这怎么破？</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/84/78/c246f6d5.jpg" width="30px"><span>Jeff</span> 👍（0） 💬（0）<div>这一节单独剖析PoW还是不错的。这个过程需要多理解，我也在反复看，希望老师有一套Java的demo供参考。</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/d6/124e2e93.jpg" width="30px"><span>Calios</span> 👍（0） 💬（0）<div>python代码示例在iPhone上看不到，有其他同学有这个问题么？</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/83/e2612d81.jpg" width="30px"><span>锐</span> 👍（0） 💬（0）<div>自私挖矿是个什么概念？老师解释一下呢</div>2018-06-20</li><br/>
</ul>