你好，我是徐文浩。

上节课里，我们看到了随着时代的变迁，人们已经不满足于通过MapReduce这样批处理的方式进行数据分析了。于是，Yahoo推出了S4，不过S4并没有在历史舞台上站稳脚跟。在S4的论文发表的同一年，我们今天的主角，也就是Storm走上了历史舞台。在接下来的几年里，Storm一度成为业界进行实时数据处理的标准解决方案。

令人惊叹的是，Storm并不是来自哪一个业界的大公司。而是来自一个只有3个人的创业公司BackType，它的主要作者南森·马茨（Nathan Marz）那个时候也才仅仅21岁。而没过多久之后，BackType就被当时如日中天的Twitter收购了。可以说，Storm证明了即使是到了今天，天才工程师仍然能够凭借一己之力，对整个行业产生重要的影响。

不过，作为一个开源项目，Storm一开始并没有以论文的形式发表。直到2014年，Twitter才发表了《Storm @Twitter》这样一篇更加偏重于Storm如何在Twitter内部使用的论文。而且，这篇论文中的作者中，也没有Storm最初的作者南森·马茨。虽然论文里没有南森的名字，但是Storm最大的功劳也仍然来自于他这个最初的作者。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（8） 💬（2）<div>徐老师好，我认为可以通过修改Topology来提高Bolt的并行度，新流入的数据根据新版的Topology分发数据。Bolt节点分成两种，一种是无状态的，一种是有状态的。比如ParseTweetBolt是无状态的，很容易扩展，WordCountBolt是有状态的，需要把状态迁移到新节点上，可以采用一致性hash扩容、翻倍扩容等方式，减少需要迁移的数据。</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（2） 💬（0）<div>这样看来,了解storm了，那么flink也必须要看看</div>2022-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ed/9f/497fbe0f.jpg" width="30px"><span>Defu Li</span> 👍（1） 💬（1）<div>老师，位运算这里应该是有问题的，如果第三步发送出去的是三个tuple，且这三个tuple异或完正好是0（01 xor 10  xor 11 = 00），那么AckerBolt最后结果也会是0了</div>2022-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/04/30/7f2cb8e3.jpg" width="30px"><span>CRT</span> 👍（1） 💬（0）<div>流量徒增的情况下，通过hash算法将多出来的数据均匀分布到新的计算节点就好了。</div>2022-01-05</li><br/>
</ul>