你好，我是海丰。

模型稳定性指的是模型性能的稳定程度，只有稳定性足够好的模型才能通过上线前的评估，而且上线后，我们也要对模型稳定性进行观测，判断模型是否需要迭代。在实际工作中，我们会用PSI来评估模型的稳定性。

这节课，我们就借助一个信用评分的产品，来详细说一说PSI是什么，它该怎么计算，以及它的评估标准。

## 案例：客群变化对模型稳定性的影响

在金融风控领域，稳定性对于风控模型来说就是压倒一切的条件。模型只有足够稳定，才能既通过上线前层层的验证和审批，又能在上线后运行足够长的时间。但在实际工作中，像客群变化这类无法避免的情况，往往会直接影响模型的稳定性。

比如说，在模型上线时候，前端流量有5000的测试用户，模型输出的分布可能是下面这样的。如果业务设置阈值为 60 分，那么，60 分以下的人我们会拒绝放款。这样一来，模型会拒绝掉大概 20%的人，这种情况对于业务来说是可以接受的。

![](https://static001.geekbang.org/resource/image/ee/10/eeeeb7ec08e77b1429a66b655765f010.jpeg?wh=1920%2A1080)

如果模型上线后，前端流量没有发生变化，还是 5000 个待测用户，但是客群发生了变化，从测试用户变成了线上的用户。这个时候，模型输出的分布就会变成下面这样。

![](https://static001.geekbang.org/resource/image/88/c5/88e92dc914694a2bf1946120b74917c5.jpeg?wh=1920%2A1080)

如果我们还是用 60 作为阈值，模型就会拒绝掉 50% 的用户。当前市场下，前端流量这么贵，如果风控拒绝了 50% 的用户申请，估计市场或者运营的同学，肯定不会放过风控部门了。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/27/19/2f33b810.jpg" width="30px"><span>加菲猫</span> 👍（8） 💬（0）<div> ( 实际占比 - 预期占比 )结果如果有正有负，SUM求和会互相抵消</div>2021-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/36/8c/97f709a4.jpg" width="30px"><span>金鱼</span> 👍（6） 💬（0）<div>在占比都比较小的情况下，采用比较后取对数，可以在消除量纲的前提下，将差别放大。作为系数乘以差值，将差异放大。</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3e/a8/0652c503.jpg" width="30px"><span>舞动的浅小白</span> 👍（5） 💬（0）<div>训练集（In the Sample，INS）、验证集（Out of Sample，OOS）、测试集（Out of Time，OOT）</div>2022-06-27</li><br/><li><img src="" width="30px"><span>Geek_5a5f1e</span> 👍（2） 💬（0）<div>老师，我们是做电商的推荐产品，用深度学习模型，也实际使用计算了IV、WOE、PSI这些指标评估特征，但对结果的置信度不是很确认。这些指标主要是在机器学习使用，是否在深度学习这里也适用呢？</div>2021-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/4e/f42d27e8.jpg" width="30px"><span>Rosa rugosa</span> 👍（1） 💬（0）<div>防止PSI出现负值</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/6b/54/ee2b0cb7.jpg" width="30px"><span>想做产品的一帆</span> 👍（1） 💬（0）<div>请问老师，若是采用等频分箱，则计算时使用每组人数所在的阈值段占总分段的百分比去计算吗？</div>2021-02-21</li><br/><li><img src="" width="30px"><span>Geek_d54869</span> 👍（0） 💬（0）<div>感觉这个PSI计算的是客群稳定性，即样本的分布差异，而不是模型的稳定性，如果客群发生变化，模型自然会受到影响，表现会差，需要重新调整。</div>2024-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ba/0e/dc3422fb.jpg" width="30px"><span>Doria</span> 👍（0） 💬（0）<div>in是取对数吗</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/33/c3/f485c1bb.jpg" width="30px"><span>EnidYin</span> 👍（0） 💬（0）<div>为了将差别放大</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/55/b6/8673d349.jpg" width="30px"><span>潘平</span> 👍（0） 💬（0）<div>老师，请教个问题。分类问题怎么计算稳定性呢？</div>2023-09-01</li><br/><li><img src="" width="30px"><span>Geek_d54869</span> 👍（0） 💬（0）<div>避免直接求和导致的正负抵消问题 另外就是可以避免由于样本集差异太大导致的问题</div>2023-06-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqygTiaQS2XznovZ4mxhAFb1CrNL9iaTXKtfOdKJfiaS9KtWfH5B1UGkiaUwsFPHYGoKH8Xwrn0kPzRLQ/132" width="30px"><span>Geek_72a416</span> 👍（0） 💬（0）<div>我怎么觉得，第一个预期分布和实际分布反了？蓝色应该是实际分布呢</div>2021-06-20</li><br/>
</ul>