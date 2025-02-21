你好，我是欧创新。好久不见，今天我带着你期待的案例来了。

还记得我们在 [\[第 18 讲\]](https://time.geekbang.org/column/article/169881) 中用事件风暴完成的“在线请假考勤”项目的领域建模和微服务设计吗？今天我们就在这个项目的基础上看看，用DDD方法设计和开发出来的微服务代码到底是什么样的？点击 [Github](https://github.com/ouchuangxin/leave-sample) 获取完整代码，接下来的内容是我对代码的一个详解，期待能帮助你更好地实践我们这个专栏所学到的知识。

## 项目回顾

“在线请假考勤”项目中，请假的核心业务流程是：请假人填写请假单提交审批；根据请假人身份、请假类型和请假天数进行校验并确定审批规则；根据审批规则确定审批人，逐级提交上级审批，逐级核批通过则完成审批，否则审批不通过则退回申请人。

在 [\[第 18 讲\]](https://time.geekbang.org/column/article/169881) 的微服务设计中，我们已经拆分出了两个微服务：请假和考勤微服务。今天我们就围绕“请假微服务”来进行代码详解。微服务采用的开发语言和数据库分别是：Java、Spring boot 和 PostgreSQL。

## 请假微服务采用的DDD设计思想

请假微服务中用到了很多的DDD设计思想和方法，主要包括以下几个：

![](https://static001.geekbang.org/resource/image/5f/92/5f22ed9bb3d5b6c63f21583469399892.jpg?wh=3175%2A1729)

## 聚合中的对象

请假微服务包含请假（leave）、人员（person）和审批规则（rule）三个聚合。leave聚合完成请假申请和审核核心逻辑；person聚合管理人员信息和上下级关系；rule是一个单实体聚合，提供请假审批规则查询。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/b0/ee/7409a0d3.jpg" width="30px"><span>冬青</span> 👍（28） 💬（1）<div>偶是编辑，这篇加餐比较长～作者会抽周末的时间把音频讲解为大家补上。感谢等待！</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/1c/e709be94.jpg" width="30px"><span>Din</span> 👍（18） 💬（7）<div>老师，您好！请教一个关于repository使用的问题

在DDD的原则里，repository操作的都是聚合根，repository的作用就是把内存中的聚合根持久化，或者把持久化的数据还原为内存中的聚合根。repository中一般也只有getById，save,remove几个方法。

例如取消订单的场景，我其实只需要更新order的状态等少数几个字段，但是如果调用repository的save方法，就会把订单其他字段以及订单明细数据都更新一次，这样就会造成性能影响，以及数据冲突的问题。

针对这个问题，我想到两种解决方案：
1. 在repository增加只更新部分字段的方法，例如只更新订单状态和取消时间 saveOrderCancelInfo（），但这样会对repository有一定的污染，并且感觉saveOrderCancelInfo掺杂了业务逻辑
2. 在repository的save方法中，通过技术手段，找出聚合根对象被修改的数据，然后只对这些数据字段做更改。

老师，您有什么建议呢？</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/2f/b0b0dd74.jpg" width="30px"><span>杨杰</span> 👍（12） 💬（1）<div>欧老师，有个关于充血模型的问题跟您探讨一下。
我研究DDD也有一段时间了，在某几个项目里面也推动团队采用DDD的设计思想，实体采用了充血模型（entity和po分开），在项目真正运行的过程中发现了几个问题：
1、由于我们的项目规模比较大，数据结构比较复杂，变动也比较频繁。每次有数据结构调整的时候改动的工作量比较大，导致团队成员比较抵触。
2、实体是充血模型的话，可以看成实体本身是有状态的。但是在一些逻辑比较复杂的场景下感觉操作起来会有点儿复杂。
最终实际的结果就是，整个团队这个充血模型用的有点儿不伦不类了。我的想法是这样的：按照DDD的设计思想，我个人觉得关键点是领域的边界，至于要不要用充血模型感觉不是那么重要（尤其是在团队整体的思想和能力达不到这么高的要求下），不知道您在实际的工作中是怎么平衡这个的。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/c9/505bfb99.jpg" width="30px"><span>CN....</span> 👍（7） 💬（3）<div>老师好，浏览代码有两点疑惑
1，我们通常会认为加了事务注解就尽量避免除数据库外的其他调用，但是代码中在领域服务中的方法中发送mq，而且是在有事务注解的方法中，这里是基于什么考虑
2，消费mq的逻辑应该属于那一层
谢谢</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ae/18/b649c2c0.jpg" width="30px"><span>盲僧</span> 👍（6） 💬（1）<div>太棒了，这个案例太精彩</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/6e/46/a612177a.jpg" width="30px"><span>Jupiter</span> 👍（5） 💬（1）<div>受益匪浅啊，感谢欧老师的课，理论和实践并存，而且值得多刷几遍去深刻理解DDD的思想。我现在的项目中能感觉有一点DDD的影子，但是我打算在我Master的作业上用一下DDD去构建一个推荐系统应用，可能会因为用DDD而用DDD，但是因为是课程设计，所以想多实践一下。有一个小问题是关于DDD里面的对象的，在前面的课程中，您提到有VO, 我现在在开发的时候 前端传给后端的对象 我使用DTO, 但是后端返回给前端的对象，我直接VO，没有中间DTO转化成VO的操作，请问这样也是可以的吧？谢谢老师。期待老师还有新的专栏分享。</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/8a/ff94bd60.jpg" width="30px"><span>涛涛</span> 👍（5） 💬（2）<div>老师您好，有两个疑问？
1.applicationService,domianService并没有实现接口，是故意这样设计的吗？
2.订单父单和子单设计成一个聚合好，还是2个聚合好？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/75/68487e89.jpg" width="30px"><span>川川</span> 👍（4） 💬（1）<div>老师你好 我看你在文章有个疑惑的点，我看你在文章里面提到“应避免不同聚合的实体对象，在不同聚合的领域服务中引用，这是因为一旦聚合拆分和重组，这些跨聚合的对象将会失效” 但是我看Approver实体的fromPerson方法就是用person聚合的尸体作为参数传递，这个是不是有违背原则呢。 </div>2020-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLOcteX7Gjxf2EK7lwjIToKYFu9LMC1ibY2XPK5022k03BHooFo8oHrIkAB68Q0O7enqjhO1FmVlbw/132" width="30px"><span>Geek_778d19</span> 👍（4） 💬（1）<div>聚合根与领域服务在职责上有些重叠了，在实现的时候如何选择？</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/9f/ee68858c.jpg" width="30px"><span>阿玛铭</span> 👍（4） 💬（1）<div>欧老师的回马枪猝不及防</div>2020-01-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/CccT5NgKlZRlTL8f4BsIDqfJ8tRkHPyaR3SXnfgU7acxo2OO7vGzNWjfQBuFnbPPzVYH8Lh49f1jyicuuRSndcA/132" width="30px"><span>Md3zed</span> 👍（3） 💬（2）<div>这样搞的太复杂了，感觉就是把简单的事情复杂化了。
DDD核心就是那几个概念的理解，微服务不一定要DDD才行，DDD只是帮助我们做领域划分，避免业务的变化导致服务的不稳定；DDD是想解决ORM的CRUD的问题，避免干尸式的“贫血”模型，它本质是一种面向对象分析和设计方法，它把业务模型转换为对象模型，通过业务模型绑定系统模型来控制业务变化带来的复杂度从而保持系统的稳定性、可扩展性、可维护性。而示例代码在这方面感觉完全为分层而分层，为DDD而DDD，可维护性，可理解性都比较差。</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/30/f1/62f0388c.jpg" width="30px"><span>波锅</span> 👍（3） 💬（1）<div>怎么跟前面写的不一样，实体不应该是充血模型么？在实体中完成存储操作。还有事件不应该在应用层么？</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/94/e83d3e91.jpg" width="30px"><span>史月Shi Yue</span> 👍（3） 💬（1）<div>老师，LeaveApplicationService在依赖LeaveDomainService的时候，依赖的应该是接口吧，看代码里注入的是类，这样就不是面向接口编程了啊</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/71/ac/c87546f5.jpg" width="30px"><span>成章</span> 👍（3） 💬（1）<div>老师你好，我有一点不懂，我看仓储的代码在domain文件里，按之前依赖倒置后的结构，是不是应该放在infer文件里才对。
我之前就有个疑问，按照依赖倒置原则来做，确实可以把仓储接口放领域，然后依赖接口使得基础设施反过来依赖领域。但是很多基础设施的东西是没有接口，或者接口不在领域层，怎么实现依赖倒置呢。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/f9/12591c6f.jpg" width="30px"><span>睡吧，娃</span> 👍（2） 💬（3）<div>老师好，我有几个问题麻烦帮忙解答一下
1、实体里实现具体业务，假如需要数据持久化或从基础层获取数据，我是否可以在实体里面调用仓储。或者说这类情况写到领域服务里面去减轻实体或者聚合根的业务的负担。
2、假如获取商品列表领域服务 从仓储会获取po的集合列表， 是否需要将集合里每个po转换成聚合跟对应的Do，然后DO的集合再转换成DTO 如果是的话，这样子会造成一定的开销，但是如果不这样 分层就会被破坏
谢谢</div>2020-07-09</li><br/><li><img src="" width="30px"><span>moming</span> 👍（2） 💬（2）<div>充血模型，是不是在实体里做数据的持久化。比如Leave导入了leaveRepositoryInterface，是不是为了持久数据？</div>2020-07-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoxUFAanq6rz2MqHXtn7vAvyIe0ljoqCtX3gnqZujLk7x90llHedHqCpHCnbYJeZmPX06Y6OFlibpQ/132" width="30px"><span>王佳山</span> 👍（2） 💬（4）<div>老师！有两个问题，哈哈
1 ddd一般应用在复杂业务中，但是复杂业务也会有管理页面，类似这样的需要还能用ddd吗，如果不用，是不是就只共用dao那一层，还是共用仓储层？
2 在 dto，do，po转换的时候遇到需要查询数据库的时候怎么办，要引用仓储层吗，感觉不好。还是尽量放在领域层解决？</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/37/455d6a8d.jpg" width="30px"><span>Geek_821c96</span> 👍（2） 💬（1）<div>老师您好，我最近看了您的课程收益良多，您的每一讲我都看完了。看完之后了我也有一些疑惑，希望能得到您的指点：1.我看到仅仓储层出现了接口定义，在其它层是不是最好不要使用接口定义了？
2.战术上感觉跟之前的事务基本的架构分层模式的区别主要是：最外层分包结构叫法不太一样但跟之前的controller,service,dao没有太大区别、实体类中多了一些业务逻辑方法、多了事件处理；
3.感觉DDD最主要还是对边界的严格控制上，具体怎么分包并无太大区别。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/38/c1/7a947bcc.jpg" width="30px"><span>乌龟</span> 👍（1） 💬（1）<div>老师，有个问题请教下，比如图书馆管理系统，有图书域（Book）、用户域（User）和图书证域（LibraryCard），借书这个动作是放在哪里合适呢，因为借书 这三个域都有用到，
1.读取用户，判断状态
2.从用户中获取图书证，判断是否超过可借书本上限
3.更新书本的借阅者

请老师帮忙指教，谢谢</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/50/c23cf47d.jpg" width="30px"><span>李</span> 👍（1） 💬（1）<div>老师，如果只有一个聚合，应用层还有意义吗？</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/15/0f/4e1a9d92.jpg" width="30px"><span>沈</span> 👍（1） 💬（2）<div>老师，您好，我们按照DDD模式，实际使用中，是将一个微服务模块拆分为四个字module，这是仓储放在基础层，这就遇到基础层不能依赖领域层的问题了，理论上mybatis-plus的mapper接口不能引入领域的domain，这个时候改如何去解决呢？谢谢解答</div>2020-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epuvKVmiaiaYDRFVRX3rGwSS4T1jibEKibqZYQjxob03ibdmguKzRsftAssCTDVWrdXL7ojNagaIdjIvzA/132" width="30px"><span>Reason</span> 👍（1） 💬（2）<div>repository返回和接受的对象用domain obj是不是要比用po更好一些？</div>2020-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8d/07/e7346b20.jpg" width="30px"><span>Geek_tony</span> 👍（1） 💬（1）<div>老师你好，目前我主要接手一个单体系统向微服务改造。该系统是银行现金管理系统，用c语言实现的，我想应用ddd思想指导，但目前遇到的瓶颈问题如下：
1.开发语言的转换，改造后的系统是java语言，那我需要熟悉原系统的c语言实现吗？还是直接从0到1搭建，和领域专家（项目经理）战略建模，划分子领域限界上下文，领域模型等等。
2.由于该系统之前的设计已经根据功能模块划分成了账户管理，信息服务，流动性管理，收付款管理等模块，相对来说职责分工明确，模块内高内聚，模块间低耦合。那我是不是可以认为这些模块分别对应一个微服务，只需要在每个模块内提取实体，值对象，聚合就可以了？
3.对于这种单体向微服务改造的系统，用传统的瀑布模型生命周期管理可以吗，需要注意什么</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/ac/e84e3864.jpg" width="30px"><span>hzeu</span> 👍（1） 💬（1）<div>老师 您好 我在查询这块有个疑问：比如分页查询这种逻辑适合在领域模型里设计吗？还是考虑使用CQRS来做？</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（1） 💬（1）<div>老师，前端有可能只展示部分数据，更新的时候也只更新部分数据；这时候dto转bo可能会将某些属性变为空值而违反bo的业务逻辑；这种情况是前后端一开始就约定好；还是在domainservice中接受前端dto,service中先加载完整的聚合，再调用更新方法？</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（1） 💬（1）<div>老师，有疑问的地方还是在领域事件这块儿；微服务内部各聚合之间使用eventbus没问题；如果不仅仅通知微服务内部的其它聚合，还要跨微服务通知)，这种情形是否就统一发布到消息代理上(rabbitmq等)更合适；即使内部的聚合也不用eventbus。</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（1） 💬（2）<div>老师每个评论都回答了，真的太用心了。另外结合我最近学习的设计思想及设计模式来问一个问题：DDD实体不应该暴露不该set get方法，但是为了从PO转换DO方便，不得不这样处理？
   最近学习到了建造者模式，通过Builder的方式来将PO的属性转换为DO，这样DO就不用暴露不必要的set get方法，但是操作起来，面对复杂嵌套的DO对象，多少还是很麻烦。
 
想听听老师的建议</div>2020-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/orTaVwTib3ribOibhLGJDAUiaMeH3UYFF9yDysdaTXdMIxrtWacibjsIAhOovIqmz1fEBMCiaWWZzS4aB4XXqUmL1VYw/132" width="30px"><span>李金尧</span> 👍（1） 💬（1）<div>认真拜读了一遍，感觉受益良多，感谢老师的分享
</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/c8/e5/c0e8c78d.jpg" width="30px"><span>克制的民工</span> 👍（1） 💬（1）<div>这一讲精彩！要好好消化一下。
再请教一个问题：前后端如果采用restful接口，请问restful api和facade 接口是什么关系？在facade 接口的基础上再封装restful api吗？在DDM分层架构中，restful api属于那一层呢。谢谢</div>2020-03-06</li><br/><li><img src="" width="30px"><span>沉迷学习Zzz</span> 👍（1） 💬（1）<div>老师，我看了下你的示例，不是说领域层和持久化数据库之间加了一个仓储层吗，为什么仓储的实现还是放在领域层呢，不应该放在基础设施层吗</div>2020-03-06</li><br/>
</ul>