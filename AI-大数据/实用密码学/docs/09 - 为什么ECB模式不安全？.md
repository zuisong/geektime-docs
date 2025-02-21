你好，我是范学雷。

上一讲，我们讨论了对称密钥分组算法的计算过程，我们找到了影响对称密钥算法安全性的五个关键因素，以及初始化向量对算法安全性的影响和选择。

不过，还有一些遗留的问题，我们没有来得及讨论，链接模式和数据补齐方案对算法安全性有什么样的影响？它们是怎么影响分组算法安全性的呢？我们又该怎么避免这些安全陷阱呢？

其实，这都是对称密钥分析的核心问题。因为，可以说，每一种链接模式、每一种数据补齐方案都有着不同的构造，当然也就对应着不同的分析办法，而且分析起来都较为复杂。

这一讲，我们先来分析链接模式对安全性的影响，同时，我们还可以借此机会研究一下ECB模式到底有什么问题。还记得吧？我们在开篇词提到过，它不是一个安全的加密模式。

在讲ECB模式之前，首先，我们先来看看链接模式是怎么一回事。

## 链接模式怎么连？

我们上一讲说过，链接模式指的是如何把上一个分组运算和下一个分组运算联系起来，使得上一个分组运算可以影响下一个运算。但是，这个联系是怎么建立起来的，上一个运算到底又是怎么影响下一个运算的，这个描述是模糊的。

![](https://static001.geekbang.org/resource/image/25/20/25b0e86ec7352c98f332f2413c6e0220.jpg?wh=2284%2A1285)

从道理上来说，上一个分组运算的所有要素，都有可能参与到下一个分组运算里；下一个分组运算的每一个要素，都有可能接收上一个运算的一个要素或者几个要素的组合。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/d8/68/89770b8b.jpg" width="30px"><span>LXX</span> 👍（1） 💬（1）<div>老师好，ECB模式下 &quot;如果我们知道数据块对应的密文，我们就可以通过寻找重复的密文，在没有密钥，也不执行解密操作的情况下，知道对应的数据块。&quot; 这，那是每个系统使用ECB的密钥都是 一样的吗？所以，才会在没有初始向量的情况，从其他系统，比如HTTP的头部数据之类的方式来找到重复密文对应的明文？谢谢老师</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/52/56/5abb4d94.jpg" width="30px"><span>不知道该叫什么</span> 👍（0） 💬（1）<div>老师，其实有点没明白，链接模式是根据上一个分组加密完成的数据与下一组加密，还是取上一组部分的数据进行加密。</div>2022-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/D62JX0VEX0yhnWxgbiaXMUnEqdsVxc8JMxUBibVicbLSZ6zia606EG0zI9oosiceHsdiavDZGUyHzcvsEExFGxwP4mDg/132" width="30px"><span>Geek_828b39</span> 👍（0） 💬（3）<div>很多应用的场景，尤其是互联网的应用场景，注入特定明文数据、获取对应密文信息的攻击也是轻而易举的事情。如果攻击者没有“0123456789012345”的密文信息，他可以构造一个这样的明文，然后让密钥持有者加密，然后他就可以获得对应的密文分组。

为什么密钥持有者会去加密攻击者构造的明文？</div>2021-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/87/4e/98173974.jpg" width="30px"><span>明</span> 👍（0） 💬（1）<div>老师 ECB模式 因为没有链接和初始化向量 是不是对于相似的明文 加密出来的密文也是相似的呢，         

还有就是 上一个分组可以将他的几个要素通过链接模式传递给下一个分组，这里几个要素指的是啥呀，不是之前说的“分组算法的五个重要组成吧（加解密函数，秘钥， iv ，链接，数据补齐）”😁😁😁😁😁😁</div>2020-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（2）<div>问题2：分组重放攻击的最小单位就是一个组吗？可不可能把某个组内内容修改了？或者再添加一个组，让原本的明文变长？</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（0） 💬（1）<div>小白打卡中...
问题1：王二于二零二零年八月二十二日向李四借款人民币三十亿四千五百万六千圆整，立此为证。 这里有五行，为啥是四个分组？这里的四组是举例还是固定只能四组？</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（0） 💬（1）<div>好处：来自于ECB模式本身的好处，无初始化IV和串行计算，性能会提升。
风险消减点:
没有链接，那么就不会被实施&quot;分组重放”攻击，即攻击者无法通过篡改信息影响系统可用性。 

引入的风险点:
随着数据变短，使用注入攻击匹配明文和密文的难度进一步降低，信息泄露风险提高。</div>2020-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/d8/68/89770b8b.jpg" width="30px"><span>LXX</span> 👍（3） 💬（0）<div>如果数据比较小，不需要链接，那么可能就不会存在分组攻击，效率会提高， 但同样可能会存在初始向量缺失带来的问题，而且或许是否有可能经过计算机大量运算逆推出明文</div>2021-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cb/6f/b6693f43.jpg" width="30px"><span>Litt1eQ</span> 👍（1） 💬（1）<div>个人看法，对于比较小的数据分组如果说每次传递的数据都不重复的话 可以使用ECB模式 好处是不需要使用iv数据长度比较短 风险就是 如果两次传递相同的内容 最终的加密结果也是相同的</div>2020-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ac/5c/bb67abe6.jpg" width="30px"><span>林子茗</span> 👍（0） 💬（0）<div>思考题：
使用ECB的好处：不需要管理初始化向量，以及在加密和解密端同步初始化向量。
使用ECP的坏处：相同的明文总是加密成相同的密文；因为只有一个数据分组，并行运算、独立性等优势无法发挥。所以我认为不仅没有优势，反而劣势更大了。</div>2023-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>我们不应该在一般的应用程序使用 ECB 模式。--记下来</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2022-11-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIstR9CfEytdeJyicODHOe6cYGt4icg8cNVam9mE0s7picUsInZvwvia1hEtKsyHETfic0jrAddjt0wXdA/132" width="30px"><span>Geek_d68bf9</span> 👍（0） 💬（0）<div>感觉没看懂啊</div>2022-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a7/b2/274a4192.jpg" width="30px"><span>漂泊的小飘</span> 👍（0） 💬（0）<div>没有重复可能性的数据可以用ecb</div>2021-09-30</li><br/>
</ul>