在不同的行业中，以及不同公司在不同阶段，对CTO的要求是非常不一样的。同时任何一个时期，对CTO的能力要求其实都是综合的。

我所在的公司是一家创业公司，我是公司的联合创始人和CTO。我想结合我在公司不同阶段的经历，谈谈我对CTO这个岗位的认识。

## 公司初创期

大多数互联网创业公司，一开始都是从几个人开始干起，我们也不例外。这个阶段最重要的是如何快速开发，快速试错，通过试错不断验证自己的idea是否靠谱。而对于技术架构是否可扩展、研发流程是否规范、绩效考核等则不会过多考虑。

记得我们在开始第一个产品的时候，直接写JSP页面，不需要前后端分离（因为我们也没有专职的前端），数据库则用了Schema free的文档数据库MongoDB，无它，就是追求最快迭代开发速度。

这个阶段的公司，应该建立怎样的认知呢？首先是创业越早期风险越高，其次是低成本试错。那么作为CTO或者技术负责人，你的决策也需要匹配公司当前的状态。  
    
比如招人方面，从匹配性上看，如果候选人没有创业心态，过于追求安稳，就可以pass掉；从技术画像上看，一个全栈工程师会比一个技术专家更能帮助到团队。  
    
比如技术选型方面，不要犯杀鸡用牛刀的错误。尽量选择轻量级的框架，考虑最大化团队的开发效率为核心。在产品还未被被验证之前，过于超前的为大规模用户使用、超高并发和海量数据访问投入设计，很可能最终只能沦为摆设。因为产品的死亡率极高，方向也随时可能发生变化。

网上流传着腾讯的QQ服务端架构从建立初期一直沿用到现在的说法，腾讯的CTO 张志东在一次内部培训中被问及此事时，很坦诚地说，其实QQ的架构一直在不停的改造和优化，到目前为止已经做了4~5次的调整。当初创业时候的规划是：第一年同时在线人数到达1K，第二年2K，第三年4K，第四年8K，第五年就可以上万了，而实际上第五年的时候腾讯已经做到了500万的同时在线数，目前QQ支持的最大的同时在线人数已经超过上亿。张志东说，如果1998年创业初期，就让他做到支持500万的同时在线人数，可能就不敢创业了。

## 高速发展期

一旦你的产品通过了用户和市场验证，公司可能会进入了新的发展阶段，这时候你才有机会接受进一步的考验。随时用户和业务的增长，产品需求可能越来越多，公司对产品的迭代要求更高，老的技术架构已经不能适应新的业务迭代，同时管理层也越来越关注产品的稳定性对客户的影响，你的团队人员在不断的膨胀，而你还没有准备好绩效管理，也还不知道如何去淘汰不合适的员工……

开始接近自己的创业梦，发现梦想并不是想象中那么美。在公司的高速发展期，问题产生的速度远比你想象中快。这个阶段的CTO应该建立怎样的认知呢？
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/1e/db1ee238.jpg" width="30px"><span>严长友</span> 👍（33） 💬（0）<div>结合前面CTO能力模型
创业初期需要：冲锋陷阵的猛将
高速发展期需要：指挥若定的大帅
稳定发展期需要：指点江山的领袖</div>2018-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（5） 💬（0）<div>听过很多道理，却依然过不好这一生</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/9a/1c9b3fa9.jpg" width="30px"><span>Kqiu</span> 👍（1） 💬（0）<div>初创期：快速试错，验证产品假设，实现最小mvp模型。（尖兵一招鲜）
快速发展期(业务突进期)：
1. 抓大放小，分清主次
2. 追根溯源，分析问题本质
3. 充分放权（定目标，抓考核，排兵布阵），有效监督
平稳发展期：保持半饥饿状态和狼性，避免技术过度镀金和官僚滋生。选拔和培养人才，搭建组织梯队，结合团队成熟度，业务特点，竞争格局，制定作战方政。加强补位意识，制定防范和风控措施。</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a0/5d/fba8228b.jpg" width="30px"><span>飞龙在天</span> 👍（1） 💬（0）<div>发展阶段不同，面临的问题不同，就需要解决各种问题的能力。</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1b/70/547042ee.jpg" width="30px"><span>谭方敏</span> 👍（1） 💬（0）<div>借用新零售模式的人场货的特点来说，就是人场事，一堆怎么样的人（团队成员，实力情况，层次结构及体系）在某个场景（状态，阶段）中做件咋样的事情？</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/df/23/dbb2fb8e.jpg" width="30px"><span>zhengxm_16</span> 👍（1） 💬（0）<div>听过很多道理，却依然过不好这一生！太贴切了：有多少人回顾已走过的路的时候是否都会有同理心？</div>2021-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/AVqAefJCk4FP4I7CjicqrOlyS0frwDXYBHl2dymliauzlNwNg9Bx6phpYQsl6dsUN3Ug6NKNgrMzicKHN1SD3109g/132" width="30px"><span>geek_46dxh5</span> 👍（1） 💬（0）<div>在不同阶段有不同目标</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4c/00/7d1f630c.jpg" width="30px"><span>get√</span> 👍（0） 💬（0）<div>公司发展不同阶段，需要注重的事情不同。</div>2019-12-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/S8nYMkG2uByU9IpbAExZwCoj4PCJEs28ZMgHM0y8L2VicDkQzGrOVpG4Qedm9toibAGEzOLKbnibmM46zuW95Oib0w/132" width="30px"><span>爱笑笑</span> 👍（0） 💬（0）<div>成功者总有一些相似的优点</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/0b/7d36e256.jpg" width="30px"><span>厚厚</span> 👍（0） 💬（0）<div>抓大放小，识别问题</div>2018-06-08</li><br/>
</ul>