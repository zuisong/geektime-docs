你好，我是徐昊。今天我们来聊聊如何将模型映射为RESTful API。

通过前面九节课的学习，你应该已经学会了如何通过几种设计模式避免架构约束对模型的影响（第4-6节），也学会了几种不同的建模方法以构造业务模型（第7-9节）。然而我们之前讲的内容，主要的着眼点在于如何获得模型，以及如何组织代码。接下来，就是通过模型获得API，从而将模型作为业务能力，暴露给其他消费者调用。

在前面的课程中，我们一直都在强调领域驱动设计受到行业热捧的一个原因：**寻找到一个在软件系统生命周期内稳固的不变点，由它构成架构、协同与交流的基础，帮助我们更好地应对软件中的不确定性**。

API作为对外暴露的接口，也是需要保持高稳定性的组件。我们希望API最好能像领域模型一样稳定。于是**通过领域模型驱动获得API的设计**（Domain Model Driven API Design），就成了一种非常自然的选择。

那么今天我们就来讲一讲怎样构建领域驱动的API设计，以及为何我们会选用RESTful API。

## 什么风格的API适合作为模型API？

想要实现领域模型驱动API并不困难，但是我们需要选择恰当的API风格：**要从数据角度，而不要从行为角度去构建API**，以保证构建的API能够和领域模型结合得更加紧密。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/c5/2c/184978c8.jpg" width="30px"><span>爱睡觉</span> 👍（4） 💬（1）<div>URI是不是太长的问题，让我想起了代码层面违反迪米特法则的情况。它们的共同点是暴露了一个层级结构。
如果说因为URI体现的是稳定的业务模型，所以暴露层级是合理的，那么是不是在代码层面，如果对象层级符合模型，也不需要在意迪米特法则呢？</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/93/32/e11fcd33.jpg" width="30px"><span>Oops!</span> 👍（3） 💬（5）<div>HTTP常用的方法就get put post delete patch, 实际业务中对一个资源对象的操作可能超过5种，api的body的报文结构如何设计，才能避免api退化成混合了rpc风格的api呢？如修改文章内容，可能修改文章的body，也可能是修改文章标题,都用put, 请求的body怎么设计更符合面向对象的范式呢？</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/71/04d35c67.jpg" width="30px"><span>何炜龙</span> 👍（2） 💬（1）<div>订阅专栏跟送朋友专栏这两个API，HTTP 方法和 URI是一样的，无法区分，一般来说，当前用户的身份都会通过HTTP cookie进行鉴权，所以建议订阅专栏的URI直接简化为&#47;subscriptions，送朋友专栏的URI为&#47;users&#47;{friend_id}&#47;subscriptions，这两个API都由User-Subscriptions聚合来实现</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/76/abb7bfe3.jpg" width="30px"><span>大海浮萍</span> 👍（2） 💬（7）<div>读者Oops的问题，我在下一节中还是没有找到答案，这也是我一直没有在项目中使用restful api的原因，对一个聚合的下某个实体的操作（系统用例：修改、发布、撤回、审批、拒绝、同意..）大多数情况下会超过get put post delete put这五种，尤其是在复杂的业务系统中。看遍全网所有讲restful api的文章，均没有讲到这点，不知道是因为他们的业务简单，还是他们根本就没有在真实的业务系统中实践过。还请作者能再详细的分析一下这个问题，或者给出一个解法</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/86/ae/163ec4e5.jpg" width="30px"><span>码农戏码</span> 👍（1） 💬（1）<div>哇，原来restful api与rpc有这样的区别，与rpc相比还真没看出restful的好，在公司内部也有大量的讨论，主要restful api以资源为重点，不能出现动词，而HTTP中的几个动词不足以覆盖业务行为需求

现在看主要是对rest背后的原理没有明白，比如哪个主哪个次，像&#47;schools&#47;students,还是&#47;students&#47;schools,总是分不清，常常争吵，以文中所讲用领域模型来理解，并着重在聚合关系上，那就清晰得多，与角色目标实体建模法相得益彰

但对于to b项目系统筛选器的筛选项达到百个，各种组合，搜索api使用http get以过滤器的方式增加参数，就会超出http限制，不得不使用post，理解为创建了一个搜索任务，但总感觉别扭</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（1） 💬（1）<div>本章
REST 希望开发者面向资源编程，网络交互设计的重心放在抽象交互需要用到哪些资源上，而不是抽象系统该有哪些行为（服务）上。所以要求采用统一接口，从约束开发者的行为来逼迫开发则尝试提炼资源模型的思考。（与要求领域服务要加动词异曲同工）

课后题：
实现倒是不难，但我觉得不该这么做。
实现：
提供大而全的数据结构，客户端与服务交互时上次客户端的类型，服务端通过识别类型提供对应客户端需要的数据内容，并将这些内容填充在大而全的数据结构上。做到多端多面，每种端都只需要关心这个大而全的数据结构中自己关心的部分。（因为数据结构上不关心的部分不会有数据填充，所以也没有冗余数据带来的性能下降）
不应该这么做：
1.RESTful 架构风格的核心是开放性和扩展性。我认为开发性的重心是放在产品侧的，讲究的是我抽象一个功能，可以给任何具象的端或则行业来用，我不感知你们的差异，也就是我只满足共性部分。所以不该去做量身定做的事。量身定做的事由各端各行业自行扩展。
2.旁外化：开放性的对立面，比如说智慧供应链。我认为智慧供应链的智慧是站在需求端的，以满足所有类型的供应链需求，做到千链千面。
</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/04/41/082e2706.jpg" width="30px"><span>keep_curiosity</span> 👍（1） 💬（3）<div>如果出现跨多个聚合的行为URI该如何设计呢？</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（0） 💬（2）<div>重读疑惑：

先说结论： 仅看极客2c的App，聚合应该是Column，而不是Author。
论据：
1.用户查看资源的核心目标是 Column。
2.用户付费购买的核心单元是 Column。
3.用户没有购买 Author的诉求，仅是通过 Author 查看其下的 Column。

类比:
Column就像电商网站的商品， 计算机基础&#47;后端&#47;前端&#47;产品 这些就像是类目, 而Author就像是品牌。有些场景我需要查看某品牌下的商品，有些场景我需要查看商品是属于哪个品牌的，但我不会购买品牌， 品牌只是商品关于信誉这个维度的补充信息。作者之于专栏也是如此。

旁外话:
仅看看极客2b的App，以Author为聚合就没毛病。再次类比电商，Column依旧是商品，但Author这时候就是具体的供应商。我只会和供应商谈合作，签合同，做结算，而不是商品。</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/76/abb7bfe3.jpg" width="30px"><span>大海浮萍</span> 👍（0） 💬（1）<div>没搞明白角色在api中的作用，就比如那个admin_id，在api中如何体现</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c2/79/ff406f99.jpg" width="30px"><span>石华杰</span> 👍（0） 💬（1）<div>内容理解：
1、从行为角度设计的 API，是 RPC 风格的 API，这种 RPC 风格API的方法名不是来自于领域对象，入参和出参与领域模型无光，因此它不是领域模型驱动的API设计。不过目前大部分用的是这种风格的 API ，见名知意更容易理解，比如用户注册，用register而不是POST &#47;users。
2、RESTful API 是作为实现领域驱动 API 设计的最佳选择，它易于被其他系统整合，没有什么其它数据风格 API 可选。
3、将模型映射为 RESTful API，a.通过 URI 表示领域模型；b.根据 URI 设计 API。只有前面的领域模型没有问题，这一步很简单。
思考题：
使用GraphQL？</div>2021-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/81/1680ec3f.jpg" width="30px"><span>冯</span> 👍（0） 💬（3）<div>我有个疑问，像GET &#47;users&#47;{user_id}&#47;subscriptions，这个api只要我知道user id,是不是就可以看任意的用户的订阅了？安全性怎么保证呢</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/ba/b1d50b75.jpg" width="30px"><span>张建飞</span> 👍（1） 💬（0）<div>关于HTTP常用的方法就get put post delete patch，无法表达业务动作语义的问题。可以参考Google的自定义方法做法：https:&#47;&#47;cloud.google.com&#47;apis&#47;design&#47;custom_methods 。《程序员的底层思维》</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/7d/1454db9c.jpg" width="30px"><span>KeepGoing</span> 👍（1） 💬（0）<div>有一种CASE是如果服务内部的多种资源是有关联关系的，比如其中一种资源的状态改变，业务上也要求其它关联资源跟着变，或者还有对多种资源统一管理操作的需要，比如有一个对多种资源统一管理状态的开关等类似这样的场景。请问这种情况下该怎么单纯从资源的角度进行API设计？</div>2022-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/81/1680ec3f.jpg" width="30px"><span>冯</span> 👍（1） 💬（0）<div>不同的格式是什么意思？json or xml？如果指的是这个的话，可以通过Content-Type协商</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>2024年01月16日08:28:18
完犊子了，我们团队所有请求都是用 post，因为为了避免用其他请求方式带来的隐患，那这样的确有点实现不了领域驱动 API 了，
比如创建客户，restful 就是 post &#47;customer，我们post &#47;createCustomer 
查询客户信息 restful get &#47;customer&#47;{customerId}，我们 post &#47;getCustomerInfo</div>2024-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/58/f2c6d65b.jpg" width="30px"><span>王棕生</span> 👍（0） 💬（0）<div>徐老师，还有一个问题想请教：

查询某个用户订阅的所有专栏信息，应该用下面的哪一个URI表达呢？

（1）GET   &#47;users&#47;{user_id}&#47;Subscriptions&#47;Columns
（2）GET   &#47;users&#47;{user_id}&#47;Columns

或者有更合适的表示？</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6a/58/f2c6d65b.jpg" width="30px"><span>王棕生</span> 👍（0） 💬（0）<div>徐老师，您好！ 
首先感谢您通俗易懂和独到的见解分析，有一个问题想请教一下：
如果想获取某位作者其所有专栏的所有内容，应该用下面哪一个来表示呢？
（1）GET   &#47;authors&#47;{author_id}&#47;columns&#47;contents
（2）GET   &#47;authors&#47;{author_id}&#47;contents

或者有其他方式的 URI 能更好的表示出其领域模型？

期望得到您的反馈！感谢徐老师！</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/37/913de94f.jpg" width="30px"><span>keys头</span> 👍（0） 💬（2）<div>“用户登陆”应该用什么Uri 比较好？</div>2022-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>好神奇</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a0/9e/abb87028.jpg" width="30px"><span>(╯°□°）╯︵ ┻━┻..囧RZ=3=3</span> 👍（0） 💬（0）<div>关于思考题，我可能会选择在领域模型暴露的完整数据接口之上再引入一层 BFF 来解决不同客户端的不同数据格式需要</div>2022-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/78/b4/b4958648.jpg" width="30px"><span>少年游</span> 👍（0） 💬（2）<div>刚从第二节回来，心中有个小问题，当前端查询条件多变时该如何设计api</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/f8/d378c121.jpg" width="30px"><span>无争就是yk</span> 👍（0） 💬（1）<div>标准的http方法是http 本身定义的，本意并不是解决业务表达的问题。在实际使用过程中，这样硬扭感觉有点奇怪。其实这里又面临之前讨论的问题，类似查询类的是否走这套领域模型。还是说这套模型只解决模型的创建和修改。</div>2021-11-26</li><br/>
</ul>