你好，我是欧创新。

为了更好地理解DDD的设计流程，今天我会用一个项目来带你了解DDD的战略设计和战术设计，走一遍从领域建模到微服务设计的全过程，一起掌握DDD的主要设计流程和关键点。

## 项目基本信息

项目的目标是实现在线请假和考勤管理。功能描述如下：

1. 请假人填写请假单提交审批，根据请假人身份、请假类型和请假天数进行校验，根据审批规则逐级递交上级审批，逐级核批通过则完成审批，否则审批不通过退回申请人。
2. 根据考勤规则，核销请假数据后，对考勤数据进行校验，输出考勤统计。

## 战略设计

战略设计是根据用户旅程分析，找出领域对象和聚合根，对实体和值对象进行聚类组成聚合，划分限界上下文，建立领域模型的过程。

战略设计采用的方法是事件风暴，包括：产品愿景、场景分析、领域建模和微服务拆分等几个主要过程。

战略设计阶段建议参与人员：领域专家、业务需求方、产品经理、架构师、项目经理、开发经理和测试经理。

### 1. 产品愿景

产品愿景是对产品顶层价值设计，对产品目标用户、核心价值、差异化竞争点等信息达成一致，避免产品偏离方向。

事件风暴时，所有参与者针对每一个要点，在贴纸上写出自己的意见，贴到白板上。事件风暴主持者会对每个贴纸，讨论并对发散的意见进行收敛和统一，形成下面的产品愿景图。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ce/c72d4c67.jpg" width="30px"><span>movesan</span> 👍（34） 💬（1）<div>从第一课看到这里，终于有了一些领域建模的一些理解，希望可以慢慢的打开这扇门。

战略设计阶段：
此阶段主要是依赖于事件风暴（可理解为基于事件流程的头脑风暴），来呈现出产品的发展方向以及核心流程和场景，并文档化。
1.产品要解决的问题，以及从用户角度归纳出典型业务场景，落实文档 -----&gt; 产品愿景、场景分析
2.找出上一步总结出的关键名词，作为各个场景的实体 -----&gt; 领域建模：找出领域对象
3.根据上一步总结出实体，总结出之间的关系（聚合根、值对象、普通实体），划分出聚合 -----&gt; 领域建模：定义聚合
4.以上一步归纳出的聚合为单位，根据业务场景将聚合分组，得到限界上下文（也就是所属的领域） -----&gt;领域建模：定义界限上下文
感觉在第 1 步落实文档后，后面的 2，3，4 领域建模阶段都要不断的参照第 1 步总结出的业务流程场景来进行拆解与合并；
产品愿景、场景分析 两个阶段是从宏观到微观的过程，而 领域建模阶段是从微观到宏观的过程，也就是自底向上的思想。整体就像是总分、分总的过程。

战术设计阶段：
有了战略设计阶段的结果，反而战术设计阶段相对清晰一些。
1.按照 DDD 四层模型建包
2.确定聚合中的对象关系
3.通过战略设计阶段文档中的命令、事件来编排充血模型的领域对象，构建应用服务与领域服务

以上是初识领域驱动设计自己的一些理解，感觉如果战略设计阶段清晰完整，后面的战术设计阶段（代码落实阶段）会相对更容易一些。</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ae/18/b649c2c0.jpg" width="30px"><span>盲僧</span> 👍（24） 💬（3）<div>新哥，把代码放到git上给兄弟们个地址吧</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/43/85/a529c1ff.jpg" width="30px"><span>Aries</span> 👍（16） 💬（4）<div>命令和事件那块感觉有些模糊，比如下单是命令还是事件呢？ 按照我们的系统设计，下单则是事件。</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/85/9ab352a7.jpg" width="30px"><span>iMARS</span> 👍（14） 💬（2）<div>请教老师一个问题，在上述考勤系统中，在人员实体和组织关系实体之间，如何抉择人员是聚合根，而组织关系不是？或者说判断聚合根的依据是什么？谢谢</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（8） 💬（3）<div>我觉得老师可以讲一下CQRS，毕竟微服务好多都是要查询的哈哈</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/76/06/12413a29.jpg" width="30px"><span>Alex zhang</span> 👍（6） 💬（3）<div>老师，代码有github链接吗</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/22/b8c596b6.jpg" width="30px"><span>风</span> 👍（5） 💬（1）<div>老师这篇文章对DDD的理解效果非常高，实际的案例分析过程有一种Ddd不再是飘在空中，有点落地的感觉了，谢谢老师👨‍🏫，真的很用心</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/93/1ebfb1ca.jpg" width="30px"><span>古腪</span> 👍（5） 💬（3）<div>有个场景希望老师帮分析下，一个是用户可以有多个角色，一个角色有多个用户，并且有多个权限，一个是权限可能配置多个角色，这种情况要怎么设计聚合咧？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a8/fa/e98afa52.jpg" width="30px"><span>Tan</span> 👍（3） 💬（1）<div>产品愿景可以不安上面的来吗？ 我的理解就是
1、产品是为谁服务
2、解决了什么问题
3、给产品确定名称
4、给产品定义功能
5、竞品分析
6、本产品的优势
</div>2019-12-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2viaqSM1mTMletYasDQgTUOlx0mpk5D748ERrVurTedCBzgdoHyJIKNj5icugj5TXa4L3GM72eicRNPjd5ItfHeOA/132" width="30px"><span>大飞</span> 👍（2） 💬（1）<div>新哥，问个有点奇怪的问题，在设计过程中，对于一些复杂的流程细节没考虑到位，或者忽略了某个细节流程，而导致在程序落地过程中，发现原有的建模不够严谨，对于这种场景，有什么补救措施吗，或者如何避免这一问题的发生？</div>2020-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/41/44/bc8bc7cf.jpg" width="30px"><span>小之</span> 👍（2） 💬（2）<div>老师你好，我看这边直接从限界上下文入手了，这边为什么没有聊子域划分问题呢，子域和限界上下文的区别一直是个老大难问题，一个在问题空间，一个在解决方案空间，我们日常怎么取舍呢</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ec/66/57d5a1de.jpg" width="30px"><span>JKing</span> 👍（2） 💬（1）<div>应用层我理解其实就是BFF</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（2） 💬（1）<div>推广活动为一个聚合，直播推广为一个聚合，但是这两个聚合之间又是有联系的，比如直播推广可以参与推广活动。那这样这个命令到底属于哪个聚合呢？还是说将推广活动作为一个值对象呢</div>2019-11-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epy83Wich4cvDNzsfPNe9iaiaDqE7apkM5OPL3Mj2HVicibQNteosS9uxHbQwWfBLKibibe9Aibzx41TIDqLA/132" width="30px"><span>Geek_8dfa3e</span> 👍（1） 💬（1）<div>中台和应用的边界怎么定义？应用会有实体对象吗？哪些实体对象会落中台，哪些落应用</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/56/c39046c0.jpg" width="30px"><span>Jie</span> 👍（1） 💬（1）<div>窗外37度，空调房内看得酣畅淋漓，之前的知识都串起来了！</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/63/f008057a.jpg" width="30px"><span>alex</span> 👍（1） 💬（1）<div>有没有一个基于 DDD 设计实现的实际可用的开源项目可以分享下</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/6d/b623562a.jpg" width="30px"><span>霹雳大仙pp</span> 👍（1） 💬（3）<div>审批规则值对象有查询审批规则方法？这里不是很明白。
不应该通过领域服务或者聚合根来做查询吗？这里的值对象是充血模型？
望老师回复。</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/88/a7/fb383ef7.jpg" width="30px"><span>MaLu</span> 👍（1） 💬（1）<div>这篇实例，将之前的铺垫进行的应用，很有参考与启发，我已珍藏为行动指南。</div>2019-11-25</li><br/><li><img src="" width="30px"><span>Geek_606081</span> 👍（0） 💬（1）<div>老师，场景分析内容部分，审批场景文字说明的配图是人员场景的图，是配图错了吗？感觉文字和图片不匹配呢？
</div>2020-12-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKv92yhBU4EpUIeo4UgAQvsMGnu2S1XNxq2TyVWgw8n2ByDSm7JcqiaVibOTyr9sq2awZHq1dSYb2Vg/132" width="30px"><span>archerwong</span> 👍（0） 💬（1）<div>欧老师，我想问下，在DTO想DO转换的过程中，是在领域服务外进行的，如果我的聚合内有一个聚合根，两个实体，那么这两个实体在实例化的时候，是需要先new，然后再调用实体的set方法的，那么这个算是外部绕过聚合根，直接操作了实体么</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>实体中的值对象 是否可以放到一个表中设计呢。</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/65/0e/6dee8123.jpg" width="30px"><span>errocks</span> 👍（0） 💬（2）<div>请教一下, 如果目前公司还是单体架构, 是不是没太大必要做DDD的实现, 这样还是会增加系统的复杂度, 带来的效益好像没有微服务架构高. </div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/85/9ab352a7.jpg" width="30px"><span>iMARS</span> 👍（0） 💬（1）<div>审批规则是不是应该规划成一个通用子域？请假单的提交和审批都会用到。</div>2020-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/bb/dc/9caa24dd.jpg" width="30px"><span>机器猫</span> 👍（0） 💬（1）<div>git里面我看都是领域服务直接操作的数据库，不是应该在实体中操作数据库吗？</div>2020-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/a4/32866c50.jpg" width="30px"><span>Avril</span> 👍（0） 💬（1）<div>欧老师，你好，想问下，聚合比较推荐小聚合，每个聚合一般只有两三个领域对象吧？这样，一个项目里，是不是拆分成很多的聚合，也就很多的package。</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/9c/b821c12d.jpg" width="30px"><span>明哥</span> 👍（0） 💬（1）<div>代码如果要落地的话，老师在框架这块有没有什么建议呢？例如使用Axon或者Reveno这种开源cqrs框架</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/80/e5/251d89b5.jpg" width="30px"><span>锦鲤</span> 👍（0） 💬（1）<div>新哥，案例中，第一步找出实体中出现的刷卡明细、考勤明细和考勤统计这三个分析出来的实体在场景分析里面并没有直接的关联，我的问题是：是场景分析中遗漏了，还是根据逻辑推理推导出来的？
</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/7b/39283ec4.jpg" width="30px"><span>yangjuicy</span> 👍（0） 💬（1）<div>状态为啥是值对象？没有理解</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/a6/188817b6.jpg" width="30px"><span>郭嵩阳</span> 👍（0） 💬（1）<div>老师您好，有几个问题请教您
1.事件风暴 是否在 有相关原型 进行会好一点  如果没有原型 总觉得有些空洞 即使产品提供了简单的用户旅程，您做事件风暴的前提需要产品和业务提供哪些内容在进行
2.还有就是在事件风暴建立领域模型的时候，是否需要文字去记录一些名词解释，
3.在建立领域模型的时候，比如修改用户，可能会记录用户的修改明细，这个明细模型是在领域模型时候建立还是在最终建库的时候，因为这个在用户旅程或者原型可能不会提及
4.在架构的时候，这些过程图比如事件风暴或者命令风暴是否会写在架构图上体现
4.即使在确定了命令或者事件，但是命令或者事件里的规则在什么场景下记录,比如状态修改，某种状态下不能修改记录或者其他,这些规则是否在时间风暴上体现了，是怎样体现的
5.一般您做一个大系统的时间风暴大概是多长时间,包括画图的时间
现在我这里做事件风暴觉得有迷茫，因为没有产品原型，产品只是提供了用户旅程，觉得这样做出来的事件风暴总觉得不严谨，为了事件风暴而风暴</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/a6/188817b6.jpg" width="30px"><span>郭嵩阳</span> 👍（0） 💬（1）<div>老师可不可提供一个,你写的架构文档,事件风暴这些是否也体现在最终的架构文档</div>2020-06-22</li><br/>
</ul>