在前面几节课中，我们学习了面向对象的一些理论知识，比如，面向对象四大特性、接口和抽象类、面向对象和面向过程编程风格、基于接口而非实现编程和多用组合少用继承设计思想等等。接下来，我们再用四节课的时间，通过两个更加贴近实战的项目来进一步学习，如何将这些理论应用到实际的软件开发中。

据我了解，大部分工程师都是做业务开发的，所以，今天我们讲的这个实战项目也是一个典型的业务系统开发案例。我们都知道，很多业务系统都是基于MVC三层架构来开发的。实际上，更确切点讲，这是一种基于贫血模型的MVC三层架构开发模式。

虽然这种开发模式已经成为标准的Web项目的开发模式，但它却违反了面向对象编程风格，是一种彻彻底底的面向过程的编程风格，因此而被有些人称为[反模式（anti-pattern）](https://zh.wikipedia.org/wiki/%E5%8F%8D%E9%9D%A2%E6%A8%A1%E5%BC%8F)。特别是**领域驱动设计**（Domain Driven Design，简称DDD）盛行之后，这种基于贫血模型的传统的开发模式就更加被人诟病。而基于充血模型的DDD开发模式越来越被人提倡。所以，我打算用两节课的时间，结合一个虚拟钱包系统的开发案例，带你彻底弄清楚这两种开发模式。

考虑到你有可能不太了解我刚刚提到的这几个概念，所以，在正式进入实战项目的讲解之前，我先带你搞清楚下面几个问题：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/37/56/f57c24f1.jpg" width="30px"><span>倡印</span> 👍（76） 💬（3）<div>小时候妈妈说我贫血 ，长大了才知道我真的贫血</div>2020-07-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjRETqRjvLESLDZkNTjIiaSibtNYBaS1o8WMUicOFn3ycF3Mgh6LRJibqSBjVBjiaO2ibW0gHkafATb21A/132" width="30px"><span>lmdcx</span> 👍（51） 💬（9）<div>看到「领域驱动设计有点儿类似敏捷开发、SOA、PAAS 等概念，听起来很高大上，但实际上只值“五分钱”。」时，不知道引起了多少人的共鸣，O(∩_∩)O~。  做技术的本身就经常会遇到沟通问题，一些人还总喜欢“造概念”，唯恐别人听懂了，争哥这句话无疑说中了我们的心坎儿。  
当然我这里也不是说 DDD 不好（看后面的争哥也没这个意思），但是每个理论都有自己的局限性和适用性，看很多文章在讲一些理论时，总是恨不得把自己的理论（其实也算不得自己的）吹成银弹，态度上就让人很难接受。  
我还是喜欢争哥的风格，逻辑很清晰，也很严谨，很务实。  

关于老师的问题。  
说句实话，我们就没有写过充血模型的代码。  
我们会把 UserEntity、UserBo 混着用， UserBo 和 UserVo 之间转换时有时还会用 BeanUtils 之类的工具 copy 。  
对于复杂的逻辑，我们就用复杂 SQL 或者 Service 中的代码解决。  

不过我在翻一些框架时，比如 Java 的并发包时不可避免的需要梳理 Lock、Condition、Synchronizer 之间的关系。比如看 Spring IOC 时，也会需要梳理围绕着 Context 、 Factory 展开的很多类之间的关系。  
就好像你要“混某个圈子”时，就不可避免的“拜码头”，认识一堆“七大姑八大姨”，然后你才能理解整个“圈子”里的关系和运转逻辑。  
我也经常会有疑问， DDD 和面向对象究竟是什么关系，也会猜想：是不是面向对象主要关注“圈子”内的问题，而 DDD 主要关注“圈子”之间的问题？有没有高手可以回答一下。  
（其实我最近一直都想订隔壁DDD的课，但是考虑到精力的问题，以及担心学不会，主要不是争哥讲O(∩_∩)O~，所以没下手）</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/5e/a897cb0d.jpg" width="30px"><span>grey927</span> 👍（11） 💬（1）<div>能否用代码表达一下充血模型，其实还是不太理解</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（10） 💬（1）<div>1.目前基本都在接触贫血开发模型，充血的可能局部模块设计的时候，会把数据和方法组织到一个类里面去。但是DB的操作完全隔离。
这里有一个问题:充血模型的话，OOP的想法，应该是每个人(假设人是类，具体的人就是人这个类的实例化)管理自己的属性，比如我的主管。
这个时候有一个需求。批量修改人员的主管。那么充血模型是要遍历委托给每个具体的人自己去修改呢？还是提供一个service，直接批量操作DB。
2. entity,bo,vo我的做法是不合并，但是真的有贯穿三层的模型。那么就直接用一个。但是要单独分包。并且组内规范好这个包里面的东西都是有修改风险的。我个人倾向用麻烦换容错。毕竟软件的变化性比较大</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/27/827015c0.jpg" width="30px"><span>追风少年</span> 👍（9） 💬（3）<div>1. 以前做的项目都是基于贫血模型的，这次的话涉及风控业务，也是基于贫血模型，但是各种问题不断，正在考虑优化，这里刚好看到老师的文章，希望能有所借鉴。
2. Entity是ORM中数据库映射的实体类，BO是业务操作相关实体类，VO是视图层对应实体类。在简单情况下，这三个类可能是一样的，比方说你填写一个登陆注册的表单，此时前端传给后端接口的数据，一般就是VO，而通过业务层Service操作，加入创建时间，IP地址等，就转换成了BO，最后对应到数据层就转换为了Entity，也许一次注册可能需要写多个库，就会生成多个Entity。
有些复杂业务，还有DO,DTO，PO之类的概念，但是个人感觉很模糊，也不是很了解。这里希望老师能指点一下。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e1/75/bbdf9052.jpg" width="30px"><span>饭太司替可</span> 👍（8） 💬（1）<div>项目中用到了google的ProtocolBuffer，根据数据结构体生成的类模型只能包含数据，不能包含方法。这种情况也是贫血模型吧。</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/56/311be282.jpg" width="30px"><span>安静</span> 👍（6） 💬（1）<div>要是有代码例子就好了。实操性会强很多。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（3） 💬（2）<div>最近在看消息队列的专栏，里面有提到Pulsar这个产品采用了存储与计算分离的设计。本质上和文中提到的数据与操作分离应该是一个意思吧？难道也是一种面向过程的设计</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c4/9d/7c4dbcd9.jpg" width="30px"><span>迁橘</span> 👍（3） 💬（1）<div>看完了, 感觉热血沸腾, 特别期待下一节课.
课堂讨论:
1, 自己所参与做的项目中都是典型的基于贫血模型开发模式.
2, 我是基本都用一个类的, 因为所做的系统业务想比较简单, 也就没必要, 还有些共用的属性字段会拿出来,用继承的方式. 基本项目都是这么过来的. 也没遇到啥问题, (大家勿笑哈)

从第一节课听到现在, 受益匪浅, 每节课都会听个3-5遍. 到现在, 基本能意识到自己在工作种存在的一些问题,以及需要提升进步的地方, 期待后面的课程....</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/3c/a01a60f3.jpg" width="30px"><span>十二差一点</span> 👍（3） 💬（3）<div>MVC是面向过程编程，是因为它违反了封装的特性，数据和逻辑操作分离开了，在controller进行相关数据逻辑操作，而model仅仅只是个数据层，没有任何操作。而MVVM是面向对象编程，因为它把数据和其相关逻辑操作封装在了viewModel，只暴露给外部相关方法，controller想要获取数据直接通过这些方法就行了，不用像MVC在controller层进行一堆逻辑操作，同时减轻了controller的代码，在viewModel也方便维护数据逻辑操作。不知道这样的理解对不对？</div>2019-11-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJjiaBHJyfAKK02CCcibkqI0jpaHJEcyrTRI4xbrqHCWiaia88WQs4r8zJVmHfibqricUYeUT2ezAZAC7wQ/132" width="30px"><span>爱喝酸奶的程序员</span> 👍（2） 💬（1）<div>一直贫血……我们的代码一直都是一点点修改就写SQL,但是感觉只是提了充血模式的长处……没有一个例子有点空洞</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ca/cbce6e94.jpg" width="30px"><span>梦想的优惠券</span> 👍（2） 💬（1）<div>是否可以采用组合的方式，来减少重复字段？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/59/ffa298a2.jpg" width="30px"><span>成葛格</span> 👍（2） 💬（1）<div>这么说来我所有的项目都是基于贫血模式的；现实的开发中就是把三个VO都合成一个的。不知道会有什么问题？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/90/ec/ede93589.jpg" width="30px"><span>拂尘</span> 👍（2） 💬（3）<div>老师，我还是学生，然后学的web架构里面我只知道实体类，那个vo，bo，和entity为什么需要定义三个啊，不是用一个实体类就可以了嘛？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（2） 💬（2）<div>1. 针对第一个问题，我就和楼上的很多同学一样，是一直在贫血的世界里不亦乐乎，丝毫没有体会过充血的愉快感。但是，现在自己有一个小打小闹的项目开启，虽然已经做了点，但是现在开始修正还来得及，准备尝试下用充血的模型，跟上老师的实战节奏。
2. 针对第二个问题，我还是倾向于不合并。虽然目前看来大部分字段是差不多的，但是万一后面内容扩展了，功能扩展了，有特殊处理相关的呢？

设计模式的课程真的是值得品味好几次，每次学习的时候，生怕上次的内容没有仔细看完，而跟不上当节课的内容，有点忐忑。老师的内容循序渐进，对于我这个职场比菜鸟稍微好点的鸟来说，都是一句句精辟的话语，打开了我很多平时看到的心结，也指出了我平时开发中的很多不足，原来我一直在落后的时代写代码。

所以，如何摆脱我的上古时代的开发模式，就是紧跟着老师的步伐走。虽然一开始说8个月的时间，但我觉得，8个月一晃就过去了，保持这个节奏，很赞。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/d9/2105007a.jpg" width="30px"><span>Geek_1r26uy</span> 👍（1） 💬（1）<div>我们项目像是充血和贫血的结合体。涉及不是很烦复杂的业务基本上Repository这一层只跟单表操作。也就是只针对一张表的CRUD，业务逻辑在service这一层。这样也可以实现代码的重用。但是entity，domain实体大多时候只是做一个数据的传递功能。老师这种算充血模式的DDD吗？</div>2019-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/0f/67a7142a.jpg" width="30px"><span>carol</span> 👍（1） 💬（1）<div>问个小白问题。请问下，什么是业务？怎么来评判业务复杂不复杂呢？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/00/7daa7403.jpg" width="30px"><span>Eden Ma</span> 👍（1） 💬（2）<div>移动端的MVVM和MVP算是充血吗？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fb/6c/12fdc372.jpg" width="30px"><span>被水淹没</span> 👍（1） 💬（1）<div>我觉得，简单的贫血模型可以不区分BOVO，直接把DO直接set到ResultData然后就丢给前端，区分各个pojo
如果分领域的话，区分各类pojo是有必要的
老师您觉得呢</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/5b/fd0b96cb.jpg" width="30px"><span>清风自来</span> 👍（1） 💬（1）<div>老师，我有个问题，一直在疑问中，重domain轻service，那哪些业务应该写在service哪些应该写在domain呢？如果是有两个服务，一个订单服务，一个商品服务。我订单服务中需要商品信息支撑。调用商品服务的这个过程应该在domain还是在Service。如果在Service层，我是不是可以这样理解Service层应该处理的业务。1.构建domain(包括调用服务获取构建信息)。2.调用domain.do()，做业务处理。3. BO转化DO。4.调用Repository存DO？</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/47/ded5da90.jpg" width="30px"><span>御风</span> 👍（0） 💬（1）<div>现在的项目分为controller、facade、service、dao四层，facade和service两层的具体分工是什么？需要共用BO还是有各自的BO？</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/49/bd914b5f.jpg" width="30px"><span>公号-彤哥读源码</span> 👍（0） 💬（1）<div>有个疑问，之前老师说的购物车那个例子，items不暴露get方法，怎么转成VO返回前端？</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8d/cd/b6bdc1b2.jpg" width="30px"><span>Jessica</span> 👍（0） 💬（1）<div>老师，按照我们之前的项目解决方案里，我们是采用了DDD分层架构，但是没有使用充血模型，依然使用了贫血模型，通篇没看到老师提基于贫血模型的DDD架构，我在想是没有这种用法吗？</div>2019-12-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BIRpwViaN51yynIeFonD7QRlwDCVtKibrG956NTxzEqibOZZVjhMMgibOPmd3VicfYxpknZsic1oJq8KicZvXkmmiajuQg/132" width="30px"><span>tuyu</span> 👍（0） 💬（1）<div>老师, 我觉得设计数据库结构我也会犯一些问题, 但自己可能不知, 能否花一个时间讲讲数据库设计的坑</div>2019-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/e8/4c943503.jpg" width="30px"><span>乐</span> 👍（551） 💬（51）<div>## 为什么贫血模型盛行

下面几项自己都中过招（环境问题和个人问题）：

### 环境问题 ##

* 近朱者赤，近墨者黑
    * 大多数人都是模仿别人的代码，而别人的代码基本上都是 demo，没有复杂的业务逻辑，基本是贫血模型
    * 找不到好的指导与学习对象
* 接触不到复杂业务项目
    * 做 web 项目的，很大一部分就是简单的 CURD，贫血模型就能解决
* 公司以任务数来衡量个人价值

### 个人问题 ###

* 不考虑项目质量属性
    * 只关心当前业务，没有意识去思考后期该如何维护和响应业务变更
* 求快不求质
    * 个人以任务数来自我满足
    * 没有 60 分和 100 分的概念
    * 需求分析、设计、编码合为一体

## 如何理解充血模型

先推荐一本书：整洁架构设计

先说一下充血模型中各组件的角色：

* controller 主要服务于非业务功能，比如说数据验证
* service 服务于 use case，负责的是业务流程与对应规则
* Domain 服务于核心业务逻辑和核心业务数据
* rep 用于与外部交互数据

----

额外说一点，业务开发个人倾向于六边形架构，而非传统的三层架构。六边形架构更能体现当下 web 应用的场景

六边形项目结构（根据实际情况自行组织与定义）：

* InboundHandler 代替 controller
    * *WebController：处理 web 接口
    * *WeChatController：处理微信公众号接口
    * *AppController：处理 app 接口
    * *MqListener：处理 消息
    * *RpcController：处理子系统间的调用
* service 服务于 use case，负责的是业务流程与对应规则
    * CQPS + SRP：读写分离和单一原则将 use case 分散到不同的 service 中，避免一个巨大的 service 类（碰到过 8000 行的 service）
* Domain 服务于核心业务逻辑和核心业务数据
    * 最高层组件，不会依赖底层组件
    * 易测试
* outBoundhandle 代替 rep
    * MqProducer：发布消息
    * Cache：从缓存获取数据
    * sql：从数据库获取数据
    * Rpc：从子系统获取数据

----

各层之间的数据模型不要共用，主要是因为稳定性不同，各层数据模型的变更原因和变更速率是不同的，离 IO 设备越近的的稳定性越差，比如说 controller 层的 VO，rep 层的 entity。Domain 层是核心业务逻辑和核心业务数据，稳定性是最高的

----

几个不太容易理解的点（我刚开始碰到的时候很费解）：

* use case 和 核心业务逻辑该如何定义与区分
    * 哪些该放到 service 里面，哪些该放到 Domain 中
* rep 是依赖于 service 的，而不是 service 依赖 rep 层
    * 业务逻辑是最高层组件（最稳定的），rep 层是底层组件
* 接口能反转依赖关系

----

一剂良药：所有的中间层都是为了解耦</div>2019-11-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（284） 💬（17）<div>我个人认为，充血模型在web开发领域不流行的一个根本原因，在于互联网兴起后各种层出不穷的需求变动，以及短命的项目生存周期，充血模型应对复杂业务确实很有优势，但是这是建立在复杂业务本身其实相对稳定上，比如银行的业务，虽然复杂，但是其实很稳定。但是要是换在互联网，今天改需求明天改需求，甚至很多时候根本就是推倒了重来的需求，充血模型面对这种状态，根本是力不从心的</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（179） 💬（16）<div>一直贫血而不自知</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（86） 💬（0）<div>设计模式_10
# 问题: 
- 1. 做的Android项目更多，Android开发也是经历了MVC==&gt;MVP(依然是一种MVC架构)==&gt;MVVM的模式演进。类MVC模式比较多，在UI相关的开发中，只用过贫血模式(之前也尝试过使用充血模式，但考虑到不一致带来的成本就放弃了)；在UI无关的复杂服务类开发中，也用过充血模型(虽然我不知道它叫充血模型)。我认为贫血模型的优点是更容易看懂，充血模型的优点是更能应对复杂业务。
- 2. 我认为还是不要放在同一个类中，原因是：成本大于收益。成本：一个复杂的类，在被不同的模块调用时充当着不同的角色，甚至，不同的模块调用不同的字段，需要大篇幅的文档来描述这些差异。稍有修改，复杂度的增加非线性。优点：代码重用。

# 感想:
软件开发处理的是工程学问题，解决方案依赖场景，一个新技术的火爆一定是解决了当前主流场景的痛点问题，随着规模和复杂度的变化，场景也随之变化；争论贫血模式更好还是充血模式更好，争论哪个开发语言更好，这样的问题都是伪命题，我们更应该投入精力的是为当前场景选择最合适的解决方案。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/5d/735fdc76.jpg" width="30px"><span>╭(╯ε╰)╮</span> 👍（36） 💬（5）<div>个人感觉业务被贫血模型绑架的另一个原因是以前缓存nosql这些技术不不成熟 刚毕业那会哪有什么redis，机器的内存也不多。都是公司堆在角落的旧机器。一些业务如果在domain里实现可能会hold住数据库中的大部分数据。所以业务上都需要翻译成sql的where和join来减少网络和内存的开销。功能都被sql抢了去，想充血也充不起来。现在随便开个项目不带个redis老板都会质疑一下。mysql的访问也都是能少就少，不行再多加几台云服务器。老板也显得更有面儿。</div>2019-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（27） 💬（1）<div>基本上经历过的web项目都是基于贫血模型开发模式的，entity，bo，vo不能放在一个类里，每个对象的应用场景不同，entity是映射数据库字段的，bo，vo适合业务和展示相关的，而且entity相对来讲变化不多，bo，vo可能会频繁变化，所以不适合放在同一个类里</div>2019-11-27</li><br/>
</ul>