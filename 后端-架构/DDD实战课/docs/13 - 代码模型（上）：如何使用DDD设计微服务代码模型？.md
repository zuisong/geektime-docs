你好，我是欧创新。

上一讲我们完成了领域模型的设计，接下来我们就要开始微服务的设计和落地了。那微服务落地时首先要确定的就是微服务的代码结构，也就是我今天要讲的微服务代码模型。

只有建立了标准的微服务代码模型和代码规范后，我们才可以将领域对象所对应的代码对象放在合适的软件包的目录结构中。标准的代码模型可以让项目团队成员更好地理解代码，根据代码规范实现团队协作；还可以让微服务各层的逻辑互不干扰、分工协作、各据其位、各司其职，避免不必要的代码混淆。另外，标准的代码模型还可以让你在微服务架构演进时，轻松完成代码重构。

那在DDD里，微服务的代码结构长什么样子呢？我们又是依据什么来建立微服务代码模型？这就是我们今天重点要解决的两个问题。

## DDD分层架构与微服务代码模型

我们参考DDD分层架构模型来设计微服务代码模型。没错！微服务代码模型就是依据DDD分层架构模型设计出来的。那为什么是DDD分层架构模型呢？

![](https://static001.geekbang.org/resource/image/a3/01/a308123994f87a5ce99adc85dd9b4d01.jpg?wh=1106%2A996)

我们先简单回顾一下 [\[第 07 讲\]](https://time.geekbang.org/column/article/156849) 介绍过的DDD分层架构模型。它包括用户接口层、应用层、领域层和基础层，分层架构各层的职责边界非常清晰，又能有条不紊地分层协作。

- 用户接口层：面向前端提供服务适配，面向资源层提供资源适配。这一层聚集了接口适配相关的功能。
- 应用层职责：实现服务组合和编排，适应业务流程快速变化的需求。这一层聚集了应用服务和事件相关的功能。
- 领域层：实现领域的核心业务逻辑。这一层聚集了领域模型的聚合、聚合根、实体、值对象、领域服务和事件等领域对象，以及它们组合所形成的业务能力。
- 基础层：贯穿所有层，为各层提供基础资源服务。这一层聚集了各种底层资源相关的服务和能力。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/73/fbff84b5.jpg" width="30px"><span>陈 争</span> 👍（94） 💬（15）<div>不知道我这样理解的对不对
比如执行一个创建用户的命令，
1.用户接口层：
  1.1)Assembler-&gt;将CustomerDTO转换为CustomerEntity
  1.2)Dto-&gt;接收请求传入的数据CustomerDTO
  1.3)Facade-&gt;调用应用层创建用户方法
2.应用层
  2.1)Event-&gt;发布用户创建事件给其它微服务
  2.2)Service:
    内部服务-&gt;创建用户
    外部服务-&gt;创建日志
3. 领域层
  3.1)Aggregate-&gt;进入用户聚合目录下(如：CustomerAggregate)
  3.2)Entity-&gt;用户聚合跟
  3.3)Event-&gt;创建用户事件
  3.4)Service-&gt;具体的创建用户逻辑，比如用户是否重复校验，分配初始密码等
  3.5)Repository-&gt;将用户信息保存到数据库</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/67/05/2e601469.jpg" width="30px"><span>HuAng</span> 👍（27） 💬（2）<div>老师，这种代码分层的优势在哪里？不知道你还看不看留言。</div>2020-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/23/73569bd7.jpg" width="30px"><span>xj_zh</span> 👍（15） 💬（9）<div>老师，求DDD的系统样例代码。</div>2019-11-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKZ16iaIia0029oI1Qh5NicibpbTiaBAaCOPYXoLplKHr6uQ2rSVxPZanBvpMcL2NuhwKQYCFnaHP5tedQ/132" width="30px"><span>FIGNT</span> 👍（13） 💬（1）<div>我们在设计领域模型时，遇到一些问题
1. 查询聚合的操作应该放在哪一层？
2. entity的实体和值对象太多需要分目录吗？
3. 针对实体的维护，需要通过聚合去维护吗？可以直接修改实体吗？
4. 一个聚合保存在一个库里，还是多个聚合都在一个库里？一个实体需要单独放一个库吗？如果一个实体被修改了。用到这个实体的聚合需要更新吗？
5. 聚合是设计成单个的还是批处理的？比如一棵树，业务上是以一片叶子为单位的，那么是以树为聚合还是以叶子为聚合？</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/ad/5020a8c5.jpg" width="30px"><span>Farewell丶</span> 👍（9） 💬（3）<div>1.应用服务只能调用领域服务和实体的方法，能调用仓储接口的方法么？
按理说应该隔离，也就是说应用服务应该调用领域服务的方法，再让领域服务调用仓储接口的方法吧？

2.实体的转换只有从用户接口层到应用服务层一次是么？也就是说，到应用服务层之后，以及之后的仓储接口都是可以直接对领域实体进行操作的？

3.参考了Spring Data Jdbc项目，里边也采用了DDD的设计思路，但是发现会需要在实体中配置一些和底层存储相关的注解，这样会不会不能把领域层可仓储实现进行隔离？如果是这样的化，那么Spring Data Jdbc是不是没有严格遵守DDD的一些设计？而且它提供的领域事件的发布机制实现，是在对应的实体中产生的，例如在某一个实体中定义产生领域事件的源头，当对应的实体保存或更新时，就会发出这样一个领域事件。按照咱们文章中讲解的事件的发布是在应用层，那么如果要这样做的话，是不是就需要在应用层重新转发领域层实体内产生的领域事件呢？
因为看到Spring Data这样比较广泛的项目实现和咱们文章的描述有一些我理解上的区别，所以比较困惑和疑问。</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/78/2a/ce302437.jpg" width="30px"><span>小明</span> 👍（7） 💬（3）<div>欧阳老师，看回复收获很多，我也想请教一个问题，比如一个查询商品详情接口，包含查询商品信息、店铺信息、促销信息，可能跨多个域，那么结合DDD分层设计，应该怎么做呢，谢谢</div>2020-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/d4/f15ab4a3.jpg" width="30px"><span>刘小龙</span> 👍（5） 💬（1）<div>Repository，放在领域层，如果一个对象出现在领域，多个领域对其进行操作，会不会太多重复的操作数据库？【将包括核心业务逻辑和仓储代码的聚合包整体迁移，轻松实现微服务架构演进】这个是为了将各个领域的代码进行隔离，进行了竖向划分，达到目标。如果系统过大，将基础层划分出来，接口层划分出来，也就横向划分，是不是也行？</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e7/a6/9a2d7708.jpg" width="30px"><span>Tony</span> 👍（4） 💬（1）<div>实体自身的业务逻辑放在实体里面，会不会让实体对象很庞大，假如实体里面的业务逻辑设计仓储层的调用会不会有点奇怪了？求解</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/d2/638ca831.jpg" width="30px"><span>z</span> 👍（4） 💬（1）<div>业务相关的校验是放到应用层还是领域层呢？放在应用层的话应用层有了业务逻辑。放在领域层，面向web的和面向微服务间的调用校验规则不同又不够灵活难以实现。</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/17/179b24f4.jpg" width="30px"><span>燕羽阳</span> 👍（4） 💬（1）<div>在《实现领域驱动设计》这本书中，Demo(https:&#47;&#47;github.com&#47;VaughnVernon&#47;IDDD_Samples)。
会倾向于：在application中调用repository, 领域实体和领域服务是不应当调用repository的，这样领域层会保持独立。在实际写代码的过程中，发现这样代码写比较麻烦。
老师能在详细对比讲讲，对repository和第三方接口依赖的情况，在哪一层处理么？</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/2f/b0b0dd74.jpg" width="30px"><span>杨杰</span> 👍（4） 💬（1）<div>关于微服务的用户接口层和应用层有点儿疑问。在整个微服务架构里面一般微服务上层还有BFF层、聚合服务层，一般BFF层或聚合服务层用来协调多个微服务或者做数据转换。那么对于某个具体的微服务是否还需要用户接口层和应用层的区分呢？如果DTO是在用户接口层，那么这些数据如何传入到应用服务层呢？</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/84/2b/ba495eea.jpg" width="30px"><span>甲小蛙</span> 👍（3） 💬（1）<div>感觉老师有点纸上谈兵的意思呢，只讲理论，连示例代码库都没有，感觉谁都可以照着书来一个这样的课程了，总是浅尝辄止，不免有点失望</div>2020-07-30</li><br/><li><img src="" width="30px"><span>开心小毛</span> 👍（3） 💬（1）<div>接口层的facade是不是用来解析REST URL的: 调用URL对应的应用层服务，并传入URL变量作为调用参数。这样理解对么？谢谢老师。</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/34/c733b116.jpg" width="30px"><span>何磊</span> 👍（3） 💬（3）<div>老师好，有两个个疑问：
1. 如果在一个聚合中，只有一个 Entity，它已经实现了所有的业务逻辑，那么是否在聚合中还需要领域服务？

如果Entity跟Service都有业务逻辑的实现，在应用层调用的时候能否直接调用Entity呢？还是说不管如何。Service都要封装一下Entity的业务逻辑，方便应用层调用？

2. 这里困扰我的第二个问题，如果我的A微服务，需要先从自己的存储中获取数据的id（比如商品id），然后调用B服务获取id具体的信息，再进行其它处理。那么我是否这个逻辑是，A服务提供了一个查询id的方法，以及获取数据后对数据处理的方法；然后再A服务的应用层先调用查询id的方法，然后调用B服务获取到数据后，再调用另外一个方法来处理吗？</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（3） 💬（2）<div>我的理解是各个不同的微服务应该是共享一套infrastructure的吧？如果是的话，代码结构是不是不应该这样？
</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/9a/51e87979.jpg" width="30px"><span>Doctor Lau</span> 👍（2） 💬（1）<div>个人理解repository的实现应该放到infra，才能起到隔离持久层的作用，但这样按目前的工程结构会出现循环依赖，除非将领域模型提出到单独工程，请问这个问题怎么考虑的？</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（2） 💬（1）<div>老师，请教一下大家，业务数据网关如果实现？一个order-service提供了一个queryOrder的接口，输入起始日期查询对应的订单列表，其有2个消费者：C端网站应用服务 和 报表应用服务 ，C端网站应用服务 只需要知道订单的基本信息如下单时间、商品名称、金额就可以了，而报表应用服务是给管理者看的，需要的订单数据很全，除了C端网站应用服务需要的之外，还需要看平台与商家的结算金额。另外看到一篇类似的微服务分层方面的文章和课程中相比多了一个网关层，http:&#47;&#47;tbwork.org&#47;2018&#47;10&#47;25&#47;layed-dev-arch&#47;#4%E9%A2%86%E5%9F%9F%E5%88%92%E5%88%86%E5%92%8C%E5%BE%AE%E6%9C%8D%E5%8A%A1%E5%8C%96 请老师看看，然后讲解下这个网关层和api gateway是一样的吗？老师有微信交流群吗？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/5f/c6d10aa8.jpg" width="30px"><span>码弓手</span> 👍（2） 💬（1）<div>文章看完，还是又一些关于调用过程的疑问，Application层使用的是Domain层中聚合的entity对象对象呢还是repository对象，repository不是更应该放在基础层吗，repository理解起来还有一些困惑，希望大佬以一个下单为例子解说一下每个层的调用链路，谢谢！</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（2） 💬（3）<div>请教一下老师：客户端开发中，存在着UI层，那UI层的代码也放在哪儿呢？</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（2） 💬（1）<div>Controller, Service, Repository。Controller相当于用户接口层里的Facade？？？由于采用了充血模型，之前三层模型中的Service的业务逻辑被封装在了domain的各个聚合下的实体之中。如果需要使用到多个实体来完成某个操作，就要使用聚合中的service.</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/20/e4f1b17c.jpg" width="30px"><span>zj</span> 👍（2） 💬（2）<div>请教一个问题，考虑这样一个场景，主播账户作为一个聚合，优惠券模块作为一个聚合。那主播选券这个命令是不是应该属于主播账户这个聚合里。然后主播账户里的优惠券是不是就是这个聚合里的值对象了</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/31/0e/cbcada9b.jpg" width="30px"><span>伊来温</span> 👍（1） 💬（1）<div>请教一下欧老师，应用层编排领域服务之后的结果可能是另外的数据模型，这个模型是DTO吗？那这个DTO应该属于用户接口层还是应用层呢？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/2f/1e193dcc.jpg" width="30px"><span>有生之年</span> 👍（1） 💬（2）<div>老师，你好. 比如一个用户下单的场景： 需要校验用户是否合法、商品是否存在并且上架、库存是否足够等等校验，我的理解是：在应用服务会有一个方法是下单方法，这个方法内会调用用户的领域服务userValidateService，商品的领域服务productValidateService等等.  如果存在有数据不合法的情况，在应用服务中抛出异常，那这样在应用服务中的判断是否合法，算不算业务逻辑？ 会不会不符合“薄”的定义？ 不知我这样理解对不对？</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/41/82306dfe.jpg" width="30px"><span>包子</span> 👍（1） 💬（3）<div>您好老师，有个疑问。

聚合如果做了数据切片，比如账户的聚合acc001和acc002的数据库做客分库分表。那么在应用层发起一个转账请求就会出现分布事务问题，这种情况怎么解决呢？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/19/14018371.jpg" width="30px"><span>瓜瓜</span> 👍（1） 💬（1）<div>Repository（仓储）：它存放所在聚合的查询或持久化领域对象的代码，通常包括仓储接口和仓储实现方法。为了方便聚合的拆分和组合，我们设定了一个原则：一个聚合对应一个仓储。特别说明：按照 DDD 分层架构，仓储实现本应该属于基础层代码，但为了在微服务架构演进时，保证代码拆分和重组的便利性，我是把聚合仓储实现的代码放到了聚合包内。这样，如果需求或者设计发生变化导致聚合需要拆分或重组时，我们就可以将包括核心业务逻辑和仓储代码的聚合包整体迁移，轻松实现微服务架构演进。

给老师点赞</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/19/14018371.jpg" width="30px"><span>瓜瓜</span> 👍（1） 💬（2）<div>还有这个依赖倒置，一开始感觉很清晰，现在感觉越看越懵，老师能给再解答下吗？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/21/66/85f247e2.jpg" width="30px"><span>谢作作的男人</span> 👍（0） 💬（1）<div>老师，关于服务之间的调用，是在application层调用其他微服务的application层的服务还是领域层服务，可以直接依赖其他服务的domain吗</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/b8/b0c7486a.jpg" width="30px"><span>bornli(李磊)</span> 👍（0） 💬（1）<div>老师，我看有的领域层拆分，聚合和领域服务分离的，一个聚合里面，有些方法不属于实体的时候，才会放到领域服务里面，也就是说上层应用层可以调实体、可以调领域服务，和老师这里说的应用层，统一调领域服务不太一样</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e2/c0/09cef977.jpg" width="30px"><span>润！</span> 👍（0） 💬（1）<div>分布式的时候，是一个微服务一个源代码？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/f0/fab69114.jpg" width="30px"><span>StopLiu</span> 👍（0） 💬（3）<div>老师，公司java开发是按照阿里的代码规范，没办法用ddd推荐的代码结构，是不是就意味着没法用ddd了？</div>2020-05-02</li><br/>
</ul>