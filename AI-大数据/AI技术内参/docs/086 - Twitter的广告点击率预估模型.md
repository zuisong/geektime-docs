在上一篇文章的分享里，我们了解了LinkedIn这家公司是怎么来做最基本的广告预估的。LinkedIn的广告预估模型分为三部分，这里面的核心思想是直接对“冷启动”和“热启动”进行建模，外加和EE策略（Exploit &amp; Explore）结合在一起，从而提升了效果。

今天，我们就结合论文《Twitter时间轴上的广告点击率预估》（Click-through Prediction for Advertising in Twitter Timeline）\[1]，来看看Twitter的广告预估到底是怎么做的。

## Twitter的广告预估

我们前面提到过最基本的广告形态分类，可以分为“搜索广告”和“展示广告”。当计算广告在互联网上出现以后，这两种广告形态就迅速被很多网站和服务商所采纳。

在最近的10年里，随着社交媒体的发展，希望在社交媒体的**用户信息流**里投放广告的需求逐渐增强。我们之前谈到的Facebook的案例，其实也是往用户的信息流中插入广告。很多类似的社交媒体都争先恐后地开始进行相似的项目，这一类广告经常被称为**社交广告**。

社交广告的特点是，需要根据用户的社交圈子以及这些社交圈所产生的内容，而动态产生广告的内容。广告商和社交媒体平台都相信，不管是在投放的精准度上，还是在相关性上，社交广告都有极大的可能要强过搜索广告和展示广告。毕竟，在社交媒体上，用户有相当多的信息，例如年龄、性别，甚至在哪里工作、在哪里上学等，这些信息都有助于广告商的精准投放。而用户自己在社交媒体上追踪的各种信息，又可以让广告商清晰地知道用户的喜好。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/30/b6/fedb6472.jpg" width="30px"><span>艾熊</span> 👍（1） 💬（0）<div>我觉得也可以tune一下树模型用树模型呀，树模型也可以融合多目标也可以适用于pair对的目标呀！</div>2018-06-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI5uDOruARAmM91UYKs8yyXZpkdXkXF96AaZSib3dUNRah6SjY4eHbLJiczlrnsPXCvvax3icd8w9JJQ/132" width="30px"><span>yy</span> 👍（1） 💬（0）<div>是不是因为树模型不太适合用户id和广告id当特征，而信息流又希望把这些算成实时的，所以不太适合</div>2018-06-20</li><br/>
</ul>