你好，我是韩健。

谈起比特币，你应该再熟悉不过了，比特币是基于区块链实现的，而区块链运行在因特网上，这就存在有人试图作恶的情况。学完[01讲](https://time.geekbang.org/column/article/195662)和[13讲](https://time.geekbang.org/column/article/209450)之后，有些同学可能已经发现了，口信消息型拜占庭问题之解、PBFT算法虽然能防止坏人作恶，但只能防止少数的坏人作恶，也就是(n - 1) / 3个坏人 (其中n为节点数)。可如果区块链也只能防止一定比例的坏人作恶，那就麻烦了，因为坏人可以不断增加节点数，轻松突破(n - 1) / 3的限制。

那区块链是如何改进这个问题的呢？答案就是PoW算法。

在我看来，区块链通过工作量证明（Proof of Work）增加了坏人作恶的成本，以此防止坏人作恶。比如，如果坏人要发起51%攻击，需要控制现网51%的算力，成本是非常高昂的。为啥呢？因为根据Cryptoslate 估算，对比特币进行 51% 算力攻击需要上百亿人民币！

那么为了帮你更好地理解和掌握PoW算法，我会详细讲解它的原理和51%攻击的本质。希望让你在理解PoW算法的同时，也了解PoW算法的局限。

首先我来说说PoW的原理，换句话说，就是PoW是如何运行的。

## 如何理解工作量证明？

什么是工作量证明(Proof Of Work，简称PoW)呢？你可以这么理解：就是一份证明，用来确认你做过一定量的工作。比如，你的大学毕业证书就是一份工作量证明，证明你通过4年的努力完成了相关课程的学习。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（10） 💬（2）<div>课后思考：应该是工作量增加了，根据概率来算，前4位是0的概率是（1&#47;10）^4，更多的零就意味着1&#47;10的指数更大，那么能获取到这个数的概率就越小，这样工作量也就越大。</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（6） 💬（1）<div>约定更多的 0，从概率上讲应难度增加了吧，因为所有 5 个 0 的哈希肯定也都满足 4 个 0</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（3） 💬（1）<div>理论上selfish mining只需25%算力就能发起攻击，尽管一开始算力不占多数，但可以吸引其他节点一起加入，最终超过50%</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（3） 💬（1）<div>工作量增加，通过哈希算法计算出连续8个零的概率低，需要做的工作量自然就高</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（1）<div>理论上是增加了,因为000000包含了0000,所以理应更加难以计算</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/39/f9623363.jpg" width="30px"><span>竹马彦四郎的好朋友影法師</span> 👍（0） 💬（1）<div>pow算法中能确实证明工作量是该算法的根本，所以如果NP=P的话，区块链就亡了</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（0） 💬（1）<div>是矿工挖到了之后进行工作量的哈希计算，满足条件再向区块链广播吗？</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（0） 💬（1）<div>现实中有哪些基于签名的消息型解决算法？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（0） 💬（1）<div>工作量 算力</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/20/08/bc06bc69.jpg" width="30px"><span>Dovelol</span> 👍（0） 💬（2）<div>老师好，想问下，假如pow算法中链的目前节点是5个，我要计算出一个新节点，要求是“计算出的哈希值，小于目标值”，这个计算出的哈希值要小于哪个目标值呢？是所有5个节点还是某个节点？</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（0） 💬（1）<div>应该是增加了工作量吧</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/ea/ce9854a5.jpg" width="30px"><span>坤</span> 👍（0） 💬（1）<div>全网难度是动态调整的，落到工作量上从概率上讲是增加了。</div>2020-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（2） 💬（0）<div>这里有两个疑惑.
1.什么是目标值？这里似乎没有前文，理解不了。
2. 工作量计算这里，例如前n个零，数学上能保证哈希之后，一定可以得到吗？如果有可能无法哈系得到呢？是否会出现这样的情况。
多谢了</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/df/6e6a4c6b.jpg" width="30px"><span>kevin</span> 👍（0） 💬（0）<div>通过对区块头执行 SHA256 哈希运算，得到小于目标值的哈希值，来证明自己的工作量的
— 为什么是经过两轮hash就会算出小于目标值</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/03/5b/3cdbc9fa.jpg" width="30px"><span>宁悦</span> 👍（0） 💬（0）<div>增加了工作量，5个零的情况是包含4个零的情况的。通过估计全世界大约有多少台计算机，这个数目的倒数就决定了前面有多少个零，计算机越多，要求前面的零就越多。</div>2020-05-23</li><br/>
</ul>