你好，我是海丰。

马上就要到新年了，我在这里先给你拜个早年，**祝你牛年顺风顺水，随心随意** ！

到今天为止，我们基本上已经把 AI 产品经理的三大能力学完了，我非常开心看到很多同学一直坚持学习到现在，并且还一直和我互动，比如“悠悠”“AsyDong”“Yesss!”等等，希望你们能和我在新的一年里继续走完这趟 AI 学习之旅。

春节期间在陪伴家人之余，也希望你不要停下学习的脚步。这里，我特意为你准备了两篇轻松的加餐。今天，我们先来聊聊很多同学都比较关注的用户增长模型，说说拉新模型怎么构建，以及模型效果怎么评估。

## 关于用户增长理论

首先，我们来说说什么是用户增长理论。关于用户增长有一个著名的模型——AARRR，它是Acquisition、Activation、Retention、Revenue、Refer这5个单词的缩写，对应着用户生命周期中的5个重要环节，如下图所示。

![](https://static001.geekbang.org/resource/image/44/0e/445e00a9f4c3bfc0960c83d6e3bf3f0e.jpeg?wh=1920%2A307)

如果从拉新角度出发，要想实现一个完美的模型，有一个重要的前提就是需要不断地烧钱获客。但从如今市场上的流量分布来看，新用户的增长一定会越来越缓慢，野蛮式的扩张已经成了过去式，资本的进入也愈来愈趋于理性，所以，从这套模型出发，从获客到激活再到留存的这条路径困难重重。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/de/89/8d20e0bd.jpg" width="30px"><span>阿白</span> 👍（10） 💬（0）<div>没看明白这节，模型是输入用户特征，预测是否是留存用户。如何据此来判断不同渠道的优劣呢？根据统计出来的留存率不就能直接判断了吗？</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c1/32/e9319b83.jpg" width="30px"><span>李迎 | Lena</span> 👍（5） 💬（1）<div>主渠道和新渠道的优劣怎么能通过模型指标，比如KS和AUC来比较呢？渠道本身的优劣应该看的是ROI，KS和AUC看的是模型的好坏。</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（1） 💬（0）<div>模型 Y 标签 啥意思？</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/33/5d8a5a90.jpg" width="30px"><span>文杰</span> 👍（1） 💬（1）<div>老师，怎么判断问题是分类问题还是回归问题？然后针对每种问题如何选择模型？一直很困惑，希望老师指导</div>2021-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ba/0e/dc3422fb.jpg" width="30px"><span>Doria</span> 👍（0） 💬（0）<div>老师 7%和9%的比率也是约定俗成的吗 为什么要这样划分呢</div>2023-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/19/2f33b810.jpg" width="30px"><span>加菲猫</span> 👍（0） 💬（0）<div>有个疑问，从结果上新老渠道相差不大，但老渠道结果值都比新渠道高点，以为这种出报告结论时是倾向说新渠道没有特别的优势，结果为什么提示新渠道活跃度高呢？</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/6b/54/ee2b0cb7.jpg" width="30px"><span>想做产品的一帆</span> 👍（0） 💬（0）<div>请问老师，对于  “新渠道”可能引入的用户群体活跃，并且数据表现比较好，因此效果并不比“主渠道”差太多 -这个结论，“用户群体活跃&quot;-&gt;使得模型分类预测效果好  这个逻辑我不太能明白，活跃就意味着新渠道的特征对预测值的贡献大吗？活跃指的是什么呢？</div>2021-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（0） 💬（0）<div>Ai融合能力值+1</div>2021-02-10</li><br/>
</ul>