你好，我是欧创新。前面我们讲了DDD的一些重要概念以及领域模型的设计理念。今天我们来聊聊“DDD分层架构”。

微服务架构模型有好多种，例如整洁架构、CQRS和六边形架构等等。每种架构模式虽然提出的时代和背景不同，但其核心理念都是为了设计出“高内聚低耦合”的架构，轻松实现架构演进。而DDD分层架构的出现，使架构边界变得越来越清晰，它在微服务架构模型中，占有非常重要的位置。

那DDD分层架构到底长什么样？DDD分层架构如何推动架构演进？我们该怎么转向DDD分层架构？这就是我们这一讲重点要解决的问题。

## 什么是DDD分层架构？

DDD的分层架构在不断发展。最早是传统的四层架构；后来四层架构有了进一步的优化，实现了各层对基础层的解耦；再后来领域层和应用层之间增加了上下文环境（Context）层，五层架构（DCI）就此形成了。

![](https://static001.geekbang.org/resource/image/d6/e1/d6abc3e4f5837cd51b689d01433cace1.jpg?wh=1300%2A636)

我们看一下上面这张图，在最早的传统四层架构中，基础层是被其它层依赖的，它位于最核心的位置，那按照分层架构的思想，它应该就是核心，但实际上领域层才是软件的核心，所以这种依赖是有问题的。后来我们采用了依赖倒置（Dependency inversion principle,DIP）的设计，优化了传统的四层架构，实现了各层对基础层的解耦。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/07/44/1df0e4cd.jpg" width="30px"><span>平平淡淡财是真</span> 👍（149） 💬（5）<div>老师你好，问一个对象命名的问题，例如：VO、DO、DTO、PO、POJO、Entity、model这些使用场景和代表的含义是什么？帖子上看的解释各不相同，很不确定。我的理解是这样的：VO=值对象、DO=PO=POJO=Entity=就是基础的实体对象，DTO=数据传输对象，model=前后端传输的数据模型。
请老师指点一下</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/b8/a3dbb4f2.jpg" width="30px"><span>Jerry.hu</span> 👍（43） 💬（7）<div>老师能否结合一个实战的小项目进行讲解和梳理、同时可以将其项目贡享在git上 让大家结合实战 感觉效果会更好</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0b/9d/a7ff709c.jpg" width="30px"><span>FlyFish</span> 👍（32） 💬（2）<div>老师好，可以具体讲讲domain层的service和application层service的区别吗，什么东西该房domian，什么该放application的service，然后application层app和aplication层的service具体又该如何界定，现在有点云里雾里，有点傻傻分不清楚</div>2019-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/34/5e5b958e.jpg" width="30px"><span>How2Go</span> 👍（20） 💬（5）<div>已经结束的课程，老师还会回复吗？
----------
老师，这一节读了几遍，还没有太理解应用服务层。根据课程所说，我的理解是应用服务层会编排领域服务的执行，组织领域服务返回的结果。 但又不是API Gateway -- API Gateway 在基础层。 那么， 这个应用服务层， 是否就是BFF？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（19） 💬（6）<div>请问，最后图中MapperXML是什么？是mybatis那种做对象和数据库字段映射的xml文件么？如果是，那其中包含了与业务逻辑无关的数据库具体实现，放在领域层是否不太合适？</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/50/a54f0907.jpg" width="30px"><span>祥敏</span> 👍（15） 💬（3）<div>您好，根据三层架构和DDD四层架构映射这张图，以SSM框架组合谈谈我的理解和问题：
1.三层架构的业务接口层、业务逻辑层、数据访问层，对应实际开发的controller、service和dao三层；
2.图中三层架构中业务逻辑层的VO对应为四层架构中用户接口层的DTO，我的理解是VO原本就在三层架构的用户接口层，在三层架构中也会用DTO竖向穿透三层简化开发。图中的DTO划分为用户接口层，实际只是VO。
3.业务逻辑层中的service拆分为四层架构中的application service和domain service两层，如果以常见的CRUD开发来讲，domain service和applicatioin service是否在简单场景中就重叠了？
4.三层开发中的仓储的依赖倒置已经实现了，mybatis层仓储接口被service层调用，mapper xml作为仓储的接口实现。如果采用DDD四层划分，mapper xml会被划分到基础层。repository aop这里的界面截指的是什么，是指ORM框架内部的bean与关系数据库实体之间的关系映射吗？
5.聚合跟关注实体的持久化：聚合根、实体采用充血模型开发，CRUD中的CUD都会在聚合根、实体中实现，domain service 实现查询功能以及调用充血模型中的CUD方法，这样理解对吗？</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（13） 💬（5）<div>请教老师：解耦各层对基础层依赖，采用依赖倒置的方式？这有点抽象，不知道是通过什么的一种方法？</div>2019-12-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dxDiajEGQoG0FRDX0CyQ43bLzO8w5tUyS3mDiaY7Q97xicLIGSmTFJZjAibYRWwvEYur9vjt9Tzic5icUETIbRGkhHGA/132" width="30px"><span>Geek_d94e60</span> 👍（12） 💬（10）<div>老师您好，请教个问题，微服务拆分后，原来参数类或公共类业务数据  ，每个微服务都会用到，目前有两种方式处理
一，单独抽取一个公共服务，其它微服务都通过接口访问公共类或参数类数据

二，每个微服务都存放该类数据，但只能通过其中一个服务来维护，其它微服务走同步的方式保证数据的一致性

您比较推荐哪种呢？或者是否有其它的思路？</div>2019-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（9） 💬（4）<div>感觉用户接口层，存在感好低。仅仅存在调用应用层。 为什么还要存在这个层级？是因为，需要限制用户接口的访问？</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（7） 💬（2）<div>领域层之间能直接通信吗？  还是说要交给应用层？</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6e/a8/ee6bc8a5.jpg" width="30px"><span>LY</span> 👍（6） 💬（3）<div>对今天的思考题不太理解，领域对象不应该是放在领悟层么，应用层只是会重建这些领域对象而已，所以应用层应该不会写领域对象的类才对。那又何来应用层有哪些对象的问题呢？</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b8/36/542c96bf.jpg" width="30px"><span>Mr.Strive.Z.H.L</span> 👍（5） 💬（2）<div>老师你好，之前提过 实体是充血的，聚合根也是实体，对外提供该聚合的方法，聚合内实体的访问都必须通过聚合根，同时一个仓储对应一个聚合。我想问的是： 一个聚合内部有多个实体，那聚合根对外暴露的接口的方法岂不是非常多？？聚合内任意实体的增删改查，都通过聚合根这个充血模型对外提供？？
感觉聚合的设计是非常有讲究的………</div>2019-11-01</li><br/><li><img src="" width="30px"><span>Geek_c1891e</span> 👍（4） 💬（1）<div>老师请教个问题:领域c需要用到领域b中访问数据库的一个方法3，但是领域b的聚合根没有对外封装暴露这个方法(可能是在领域b中在调用这个方法3之前有很多业务逻辑只适合领域b的业务)。像这种情况怎么做比较好？领域c直接倒置注入领域b访问数据库的方法3；还是让领域b封装暴露一个直接调整方法3的给领域c使用？还是有其他更好的方法？</div>2020-12-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/gmu7HicQS0bhTl4mdmF8OF6r9SGtiaBmdjV2mDPhlsfCjp3kVicucRuNnhJy3E2DTaNeHzYpVc583UibHrX3ukiaJfw/132" width="30px"><span>Geek_73f7d7</span> 👍（4） 💬（2）<div>老师你好，最近公司再做智能手环相关产品，由于手环品类多，各大厂商的协议也不能，每次都需要针对新的手环开发新的web产品，但是他们的功能都大致一样，目前是把权限管理作为边界，抽出了一个微服务，前端也用了组件化达到复用，那么针对设备管理，或者对接这块，老师有没有好的建议，期待老师回复</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ea/19/14018371.jpg" width="30px"><span>瓜瓜</span> 👍（4） 💬（3）<div>作者回复: 依赖倒置后基础层就通过仓储接口获取外部参数了，然后根据这些业务参数完成基础逻辑的实现，这个实现是在基础层。不采用依赖倒置的传统四层架构，基础层和业务逻辑实现可能会在应用层或领域层，两者逻辑混杂，不利于解耦。
老师您好
基础层通过仓储接口过去外部参数，这句话不是很懂，基础层的逻辑，哪些属于基础层逻辑呢？比如根据do的不同状态决定是否存库或者是否发送到消息总线中，是否是指这一类逻辑？还有，是不是领域层（或者是应用层）的对象do和仓储层对象po的转换发生在仓储层，还是仓储层传给基础层的实体就是do而不是po？do还po的转换应该放在哪里？
根据依赖倒置的原理，感觉基础层暴露给应用层和领域层的仓储层中的接口参数是do（领域实体），而不是po，不知道理解的对不对，望老师解答，感谢感谢感谢
还有您说的如果采用传统的四层架构，基础层以及基础层业务逻辑实现就会耦合在应用层或领域层，是不是就是上面说的根据不同的状态做不同处理的逻辑，还有没有其他常见的逻辑？感谢老师</div>2019-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKZ16iaIia0029oI1Qh5NicibpbTiaBAaCOPYXoLplKHr6uQ2rSVxPZanBvpMcL2NuhwKQYCFnaHP5tedQ/132" width="30px"><span>FIGNT</span> 👍（4） 💬（7）<div>对层级的依赖倒置不太理解。好像还有个防腐层的概念。不知道能解释下吗</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/b1/758f2fe7.jpg" width="30px"><span>香</span> 👍（3） 💬（2）<div>有这样一个问题需要请教一下老师。
在我的实际场景中有这样一个微服务，它就是用来转调各个微服务来组装数据返回给前端页面的。
如果采用DDD的设计理念，我的想法是这样：
1.首先它就是个转调的服务，没有核心逻辑业务而言，所以分层应该只有用户接口层、应用层和基础层；
2.在应用层调用其它微服务接口，完成数据的组装后交由给用户接口层；
我的问题是：
1.我的这样设计有没有问题？
2.在应用层调用其它微服务时，它需要用到一些Rest调用的组件或客户端，那么这些Rest调用的客户端是放在应用层本身还是基础层？还是？
3.看到老师回答的一些问题提到DTO到DO对象的转换的说明，但都是建立在有领域层的场景，在我的场景中，没有领域层，那么我理解就不存在所谓的DO对象，这种转换要如何处理，就是当我通过用户接口层去调用应用层的应用服务方法时，在我的应用服务里，我的方法参数该如何设计？
说实话感觉这一讲如果能结合着一个小demo，就是有一份简单的小代码架构会比较好理解的。
另外我还有一个疑问就是：
4.在每一层都需要做一个对象的转换，这样我理解是不是会产生太多的这种冗余代码了？因为我看到这一讲的时候还有大家的提问，我脑海里满是各种对象的translate。
</div>2020-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/15/0f/4e1a9d92.jpg" width="30px"><span>沈</span> 👍（3） 💬（3）<div>老师，.领域层可以依赖基础层，而基础层不能依赖领域层，那领域层的repo如何调用基础层的dao进行落库呢？</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c7/dc/1268c9f9.jpg" width="30px"><span>鲲哥</span> 👍（3） 💬（2）<div>欧老师，你好。问一个具体实现上的问题。充血模型的实体如果需要持久化，是直接调用repository还是由领域服务调用？如果直接调用，那在spring是如何实现的呢？sprign中repository一般单例bean,充血应该不是单例吧？那他是如何依赖repository的呢？</div>2019-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/51/b8/f76b15a1.jpg" width="30px"><span>sundy</span> 👍（2） 💬（1）<div>老师我想请教一下，DDD除了在微服务和中台有所应用，其他方面是否也可以应用，比如分布式，单体应用，甚至移动端的组件化，因为像我们这种小企业和初创公司，微服务很难落地，业务较为复杂时可能也就能采用传统的分布式、soa。</div>2020-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（2） 💬（3）<div>老师好，现在大多数orm框架都支持多RDBMS，只需要简单配置就能实现mysql到mssql的替换。那还需要依赖倒置吗？</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/9e/5b/8c51e671.jpg" width="30px"><span>Geek_zyq</span> 👍（1） 💬（1）<div>老师我想请问一下：上一讲说到如果要一次变更多个聚合的数据，需要使用领域事件，这一讲又说应用层负责编排协调多个聚合，这两者的功能好像重复了？我可不可以不用领域事件，就在应用层去协调多个聚合？</div>2021-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/07/44/1df0e4cd.jpg" width="30px"><span>平平淡淡财是真</span> 👍（1） 💬（2）<div>感觉依赖倒置只是一种思想，从老师上面的传统四层架构演进到依赖倒置的四层架构的图中看出，改变了两点，这里我只理解了其中的一个点，就是倒置后，接口层--&gt;应用层--&gt;领域层，只保留层级之间的依赖关系，而基础层去依赖其他的层级，但实际使用过程中，感觉依然是其他层去使用基础层，依然对基础层存在依赖。这一点不是很理解</div>2020-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIjPolxbUHLkgXFibMEuL0knexNb0ibBmiagVPnK9CiazS8NcXHBwqPIzo4cqG5iaicXibic3pHuKNWDiaYbaw/132" width="30px"><span>玛尼玛尼哄</span> 👍（1） 💬（1）<div>欧老师您好，我在理解基础概念和分层架构的时候有几个问题请教一下，希望能得到你的回复
1、分层结构中，领域层的entity应该是基础概念中的聚合，而不是一个实体（或者聚合根）是吧？我理解的聚合根也只是聚合中的一个特殊的实体。
2、在基础概念中有介绍聚合，【领域模型内的实体和值对象就好比个体，而能让实体和值对象协同工作的组织就是聚合，它用来确保这些领域对象在实现共同的业务逻辑时，能保证数据的一致性】。我原本的理解中，聚合通过组合使用内部多个实体的的业务方法，来实现垮内部多个实体的复合业务，以此来体现聚合在实体间的【协同】作用，保证数据的一致性；我的理解中聚合也可以认为是一个【大】的实体，内部用充血模型来实现夸多个内部实体的业务逻辑。但是后面又出现了领域服务，用来处理聚合内夸多个实体的复合业务问题。哪我想请问下，这个聚合对内部实体的【协同】表现在什么地方？同时聚合如何来保证数据的一致性呢？这不应该是领域服务来保证的吗？</div>2020-12-01</li><br/><li><img src="" width="30px"><span>昌南一枝花</span> 👍（1） 💬（1）<div>假如用户接口层只是需要简单的调用单个的领域服务方法，而在应用层创建一个对应的方法来透传参数调用领域服务，是不是太死板了？是不是实际开发过程中松散分层更实用？</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/92/67/a8c5cacf.jpg" width="30px"><span>李剑洪</span> 👍（1） 💬（1）<div>对于基础层公共工具包，配置等这些同样会在领域层使用到，通过依赖倒置，那这些公共工具包怎么处理？</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/f7/24df0ff9.jpg" width="30px"><span>Winon</span> 👍（1） 💬（1）<div>老师，你第二张图的聚合只包含实体和值对象，但是最后一张分层架构图的聚合又包含了领域服务，能说下为什么吗？</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/5b/6f/113e24e6.jpg" width="30px"><span>阿信</span> 👍（1） 💬（2）<div>老师，您好，请问下
DO可以采用充血模型，封装自身相关的行为。如注入Repository完成自身的持久化等。
那DO的作用域会在哪些层？ 或者说哪几层可访问DO？

我的理解：领域服务可访问DO，基础层和用户层不可访问。 
这个理解是否正确？另应用层是否可访问，我现在不太确定？会基于什么因素来考虑？</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7a/a4/79ffe77c.jpg" width="30px"><span>发飙的蜗牛</span> 👍（1） 💬（1）<div>DDD分层架构主要分为用户接口层，应用层，领域层自己基础层。用户接口层对外提供api接口，接收用户(可以是用户操作，其他微服务调用，消息监听等)指令调用，用户接口层调用应用层接口。应用层负责服务的组合和编排，体现在业务用例场景或者业务流程等，调用领域层领域服务来组装应用服务，然后暴露给接口层。领域层服务系统核心业务逻辑，包含重要的领域对象，如聚合，实体，值对象，领域服务等，实体都是充血模型，体现业务能力，领域服务跨多个实体协作完成业务功能。基础层提供基础服务，例如数据库，第三方服务，消息中间件等。依赖倒置能够使基础层跟其他层解耦，例如当需要替换数据库的时候，只需要替换实现就可以！DDD分层架构设计，严格把握处理好层级关系，设计好代码边界，有利于以后威服务架构的演进，从而响应业务变化。
老师，对于这个架构讲解，建议给一个代码例子，放个github地址更好呢！感谢，学到很多</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/90/39f9c90b.jpg" width="30px"><span>北极光</span> 👍（1） 💬（2）<div>老师，我有两个问题：
1.基础服务 如果碰到工具类，还可以勉强放里面，但是静态扩展类就不行了，因为最新框架领域才是最低层。那么这种静态扩展类怎么放好呢？或则说怎么处理？

2.领域的实体，虽然说是充血模型，但是实体里面的某个方法，很可能会细分很多业务类，甚至用到设计模式，比如用工厂。那么这些由实体的某一个方法细分开来的实现类，应该放在哪里？还是放在领域层吗？如果放在领域层，有什么好的方式区分他跟实体的区别呢？比如实体我放在entity文件夹下面，这些放在哪个文件夹下面呢？实体调用这些类，是直接new呢？还是这些类也用接口？</div>2019-12-23</li><br/>
</ul>