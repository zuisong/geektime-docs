你好，我是徐长龙，今天这节课我们聊聊分布式事务。

目前业界流行微服务，DDD领域驱动设计也随之流行起来。DDD是一种拆分微服务的方法，它从业务流程的视角从上往下拆分领域，通过聚合根关联多个领域，将多个流程聚合在一起，形成独立的服务。相比由数据表结构设计出的微服务，DDD这种方式更加合理，但也加大了分布式事务的实现难度。

在传统的分布式事务实现方式中，我们普遍会将一个完整的事务放在一个独立的项目中统一维护，并在一个数据库中统一处理所有的操作。这样在出现问题时，直接一起回滚，即可保证数据的互斥和统一性。

不过，**这种方式的服务复用性和隔离性较差，很多核心业务为了事务的一致性只能聚合在一起。**

为了保证一致性，事务在执行期间会互斥锁定大量的数据，导致服务整体性能存在瓶颈。**而非核心业务要想在隔离要求高的系统架构中，实现跨微服务的事务，难度更大，**因为核心业务基本不会配合非核心业务做改造，再加上核心业务经常随业务需求改动（聚合的业务过多），结果就是非核心业务没法做事务，核心业务也无法做个性化改造。

也正因为如此，多个系统要想在互动的同时保持事务一致性，是一个令人头疼的问题，业内很多非核心业务无法和核心模块一起开启事务，经常出现操作出错，需要人工补偿修复的情况。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（2）<div>请教老师几个问题：
Q1：MySQL支持XA的bug很多，那么，实际项目中不能用XA吗？
Q2：TCC既可以是XA，也可以不是XA，对吗？
Q3：seat是采用XA的吗？还是普通的事务？
Q4：中厂、大厂一般用什么来做分布式事务？
Q5：一个网站，50万用户，这种规模的网站用什么来实现分布式事务？</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/64/457325e6.jpg" width="30px"><span>Sam Fu</span> 👍（1） 💬（1）<div>老师 xa这玩意有人用吗</div>2023-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（1）<div>前提是能接受短暂的数据不一致（非强一致性），所以业务上我们一般很少会使用分布式事务来管控，而是通过补偿机制来实现业务数据的一致性，但是如果调用的链路很长的话，补偿也是一个很头疼的事情</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/18/0fdc49d7.jpg" width="30px"><span>txjlrk</span> 👍（1） 💬（1）<div>厉害，由浅入深，由理论到实践，面面俱到。
分布式事务也分为柔性和刚性两种</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（1）<div>思考题：1.利用本地消息表+mq，或者mq的事务消息实现，可以达到解耦的目的；2.利用seata类框架，对复杂场景或者长事务可以使用sega模式。</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（1）<div>有一个没用的废话就是，要尽可能减少分布式事务的发生以及，尽可能使分布式事务的力度更细。
比如现在创建订单和支付行为很多厂商似乎就是拆开的。
 
似乎基本都是：
1. 创建订单的同时扣减库存。这一部分是一个事务；
2. 用户付款，扣减用户余额，同时修改订单状态。这部分是另外的事务；

至于如何处理事务，个人都是事务补偿会好一些。因为是人工处理的，所以更加可控。现在解决分布式事务的组件，貌似没有看到哪个实现方式是特别可用的。

而且有时候不得不考虑一个问题，多个服务间很可能不是同一套协议，也不适合让人去兼容你的事务解决方案。</div>2023-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/6c/246fa0d1.jpg" width="30px"><span>Mr.差不多</span> 👍（0） 💬（1）<div>您好，老师 TCC 和二阶段是什么关系？</div>2023-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6d/ac/6128225f.jpg" width="30px"><span>jjn0703</span> 👍（0） 💬（2）<div>AT和Saga这是另外的两种模式吗？</div>2023-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（0） 💬（1）<div>TCC 协议 是2pc 吗</div>2022-11-22</li><br/>
</ul>