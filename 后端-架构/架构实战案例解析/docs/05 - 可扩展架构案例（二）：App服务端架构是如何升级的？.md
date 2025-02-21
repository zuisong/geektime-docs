你好，我是王庆友。

上一讲，我与你介绍了电商平台从单体架构到微服务架构的演变过程。那么今天，我会通过一个**1号店App服务端架构改造**的例子，来具体说明架构的演变过程，让你能更深入地理解架构演变背后的原因。

好，先让时间拨回到2012年，当时随着智能设备的普及和移动互联网的发展，移动端逐渐成为用户的新入口，各个电商平台都开始聚焦移动端App。这个时候，1号店也开始试水移动端购物，从那时起，1号店App的服务端架构一共经历了三个版本的变化。

接下来，我就为你具体介绍App服务端架构变化的过程以及原因。

## V1.0架构

我先说说最开始的1.0版本。当时的情况是，App前端的iOS和Android开发团队是外包出去的，而App的服务端是由1号店内部一个小型的移动团队负责的，这个团队主要负责提供App前端需要的各个接口，接口使用的通信协议是HTTP+JSON。

具体的架构如下图所示：

![](https://static001.geekbang.org/resource/image/1c/45/1c2cc4298788d157851d08b5a49e9b45.jpg?wh=1142%2A825)

这个架构比较简单，App的服务端整体上就一个应用，由移动团队来维护所有对外接口，服务端内部有很多Jar包，比如商品搜索、商品详情、购物车等等，这些Jar包包含了各个业务线的业务逻辑及数据库访问，它们由各个业务线的开发者负责提供。

你可以看到，这个1.0版本的服务端，实际上就是一个单体应用，只是对外的接口和内部Jar包分别由不同的团队来提供，这个架构的优点和缺点同样都非常明显。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/79/673f4268.jpg" width="30px"><span>小杰</span> 👍（4） 💬（1）<div>老师，能对网关那块做详细讲解么，我是后端业务开发，提供dubbo接口给api网关层。从代码级别我知道controller在api那面实现，其余的理解很少了，希望老师从整体点播下</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/e6/11f21cb4.jpg" width="30px"><span>川杰</span> 👍（0） 💬（1）<div>老师，问个小问题：为什么您在画图的时候，要把 无线接口 和 WEB 分开，他们在细节上有什么区别吗？我理解都是一个webApi啊？</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/1c/e709be94.jpg" width="30px"><span>Din</span> 👍（3） 💬（1）<div>老师好！
1. 在3.0架构中，网关中的适配层是不是和BFF层职责一样？
2. 适配器是 Jar 包的形式，由各个业务线研发团队提供。会不会存在一个聚合服务不能落在某一个业务应用服务中，最终还是需要多一层聚合服务？
3. 为什么PC端没有网关层呢？</div>2020-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJIocn8OMjfSGqyeSJEV3ID2rquLR0S6xo0ibdNYQgzicib6L6VlqWjhgxOqD2iaicX1KhbWXWCsmBTskA/132" width="30px"><span>虚竹</span> 👍（2） 💬（3）<div>老师好，今天的课程讲的非常好，帮我理清了脉络，感谢，我是一名一线的业务开发人员，目前我们这边类似老师讲的V3.0架构，请教下，
1.如果进一步发展，web端使用前后端分离了，跟APP端一样http+json，那对于各业务线来说，是又从3个服务变成1个服务了吗？（当然1个业务服务内部可能是有很多业务侧微服务组成的）
2.业务线提供的api，除了给网关使用（外），还有供其他业务线调用的（内），以及前后端分离后自己的前端APi（自己），每部分会有各自的适配逻辑，但也都共享底层业务逻辑，在实际架构中，这部分不同的api
是放在同一个服务中通过包或类区分还是拆分为几个服务更合适？
3.进一步的发展应该就是微服务，中台了，老师还会继续实际演化的实例的吧？非常期待~</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/d2/7024431c.jpg" width="30px"><span>探索无止境</span> 👍（10） 💬（1）<div>老师您好，在V3.0架构中，通用层里面的协议适配，安全，日志，监控这几块具体做什么，怎么落地，能否提供一个推荐的方案？</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/de/eb/d98f2614.jpg" width="30px"><span>Cheney</span> 👍（2） 💬（1）<div>App 前端会通过移动网关来访问服务端接口。这里的网关主要就是负责处理通用的系统级功能，包括通信协议适配、安全、监控、日志等等；网关处理完之后，会通过接口路由模块，转发请求到内部的各个业务服务，比如搜索服务、详情页服务、购物车服务等等。对于 PC 端浏览器来说，它直接访问对应的 Web 应用，如搜索应用、详情页应用等，然后这些应用也是访问同样的内部服务。

请教老师，无线网关为什么只能针对APP，不能把WEB应用也管理起来，难道WEB应用就不需要包括通信协议适配、安全、监控、日志等等功能么。</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0a/d8/9e464759.jpg" width="30px"><span>Geek_a04165</span> 👍（1） 💬（1）<div>“服务适配层
最后是服务适配层。我们知道，外部接口的请求格式，往往和内部服务接口的格式是不一样的。具体到 1 号店当时的情况，外部接口是 HTTP+JSON 格式，内部服务是 Hessian+ 二进制格式。”

服务适配器是单独部署的一个服务吗，由业务团队还是移动端团队开发？app端的个性化需求在也是在adapter开发吗，我对adapter的职责有些困惑🤓
在我理解应该将app端的业务层和网关层独立开来；app业务层可以对多个服务聚合，可以提供个性化需求，由业务团队负责；网关层的职责就是打造通用非功能性需求；不知道是否正确，请老师指导一二🤓</div>2022-07-24</li><br/><li><img src="" width="30px"><span>Geek_35c0ff</span> 👍（1） 💬（1）<div>请问网关是无状态的，这里的状态是什么含义呢？可否举一个现实的例子说明一下，谢谢老师</div>2020-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/4e/4636a81d.jpg" width="30px"><span>jian</span> 👍（1） 💬（1）<div>老师，请问为什么外部接口的请求格式，往往和内部服务接口的格式是不一样的？如果一样都是二进制格式，效率都高，而且不用适配。</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/06/ea49b29d.jpg" width="30px"><span>小洛</span> 👍（1） 💬（1）<div>请教下老师网关数据缓存的设计以及如何保证一致性</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（1）<div>老师，假如网关中需要处理这样一个逻辑，即后端有三个远程模块A,B,C，优先级分别是A大于B大于C.即如果A模块有结果就返回A的结果给调用者，否则返回B的结果，如果A,B都无结果才返回C的结果。做法①:如果每次都进行三次请求，根据优先级进行筛选。做法②:先请求A,根据结果判断是否要再请求B,类似，根据B结果判断是否需要再请求C.
这两种做法，一个是并行，一个是串行。但是都有可能存在延时的风险，请问老师怎么做可以提高这个逻辑的处理性能？</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d8/e570daf4.jpg" width="30px"><span>陌生流云</span> 👍（0） 💬（1）<div>老师您好，请问下，所有的服务相当于都会走网关，虽然网关也是分布式部署的，但是会形成瓶颈。
我们之前就是用的Spring Cloud Gateway作为网关服务，但是网关服务被打挂了，网关内部队列阻塞，导致之前的请求全在等待超时。
这种情况怎么解决呢？</div>2022-08-25</li><br/><li><img src="" width="30px"><span>Mongo</span> 👍（0） 💬（1）<div>对V3.0的架构有点不太理解的就是，从无线网关到内部服务是SOA，请问底层是有任务编排还是？</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/62/25b29ebc.jpg" width="30px"><span>winterxxx</span> 👍（0） 💬（1）<div>弱弱问一下，架构图用的什么工具</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/43/bc/59d0720b.jpg" width="30px"><span>gaga</span> 👍（0） 💬（1）<div>老师，如果管理系统也使用这些内部服务合理吗</div>2020-10-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJyLCPnVq4gKMN5jPcd9wVVEXtZMibCNAkLrJf4uZKdV40Nelb3uPtCETfuw5hbbC693sUHQpRUMiaA/132" width="30px"><span>Robin康F</span> 👍（0） 💬（1）<div>spring cloud有一套网关组件gateway，这种框架可以直接拿来用，是不是可以不用自己实现网关呢？空网关也是性能非常好的网关</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/e1/36676a49.jpg" width="30px"><span>13W3H</span> 👍（0） 💬（1）<div>老师您好，在讲解中讲到有些通用服务（协议适配，安全，日志，监控）可以放在无线网关中。那如果在内部服务中，还有其他可以抽取的公共服务，但又不能放到无线网关中时，这时是不是在内部服务中还需要抽取一个“公共服务”？或者还有什么其他处理方法呢？</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/5e/4827557b.jpg" width="30px"><span>睡不着的史先生</span> 👍（0） 💬（1）<div>老师，前后端分离以后，没有了UI的这些后端就不叫应用了吗？那UI算什么?</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/0a/875d892d.jpg" width="30px"><span>阿男</span> 👍（0） 💬（1）<div>老师您好，关于通用网关部分承担太多的功能职责，会不会在高并发情况下存在性能瓶颈？会不会考虑对网关做集群和负载处理？</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（0） 💬（1）<div>无线接口是啥意思</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/7c/a8a37ddb.jpg" width="30px"><span>Frank</span> 👍（0） 💬（1）<div>PC端不需要通用，路由，适配层吗？</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（1） 💬（1）<div>adapter层再往后发展应该是组合服务吧？下面的业务领域层不可能把所有的功能都包含进去</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（0） 💬（0）<div>手头的项目:
1.app和pc统一都走了网关，网关负责了通用能力，日志，安全，监控。不包含业务处理的功能。
2.服务应用，只有一个，基本上但是单一支持，或者支持pc或者app不会同时支持，一般是满足app为主,有些不重要的嵌入一个h5. 
3. 由应用内部分model，一个是基础能力层(抽象上的能力),一个是业务功能的应用层聚合，
涉及其他域的数据通过rpc框架去调用，在应用层聚合</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（0） 💬（0）<div>APP服务端架构的升级过程其实就是一个应用业务的发展过程（说明公司的业务发展越来越好），软件架构也是根据当时的业务需求进行设计，过度和设计不足同样有问题（不过我私下认为如果他能过度设计说明考虑问题比较全，对架构的扩展性理解比较到位，所以比设计不足要好一点）
从单体应用到SOA再到分布式应用，都为了满足日益增长的业务需求，所以当我们遇到一个旧系统，并进行重构改造时，先看看当时最需要解决的问题是什么，然后再设计合适的架构方案</div>2020-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7y20jxxAnsdGLuUDjicibsgaMGO0PQg7WNTrNCzqmibtrsibpjJJHs6LK0FTWKs8icJickMJPkM7Tia2UA/132" width="30px"><span>旺财勇士</span> 👍（0） 💬（0）<div>这个课程不错。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b4/00/661fb98d.jpg" width="30px"><span>追忆似水年华</span> 👍（0） 💬（0）<div>“过度设计和设计不足，同样都是有害的”，感触最深的是这句话，一切都要从实际出发，结合项目实际需求，为其搭配相适应的解决方案，简单来说，就是“平衡、取舍”。</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3e/ed/e154de2e.jpg" width="30px"><span>250ZH</span> 👍（0） 💬（2）<div>V3.0架构中，APP和PC使用的所有接口都是不同的吗？</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/1a/30201f1a.jpg" width="30px"><span>Geek_kevin</span> 👍（0） 💬（0）<div>我们现在app的架构遇到了一个问题，整个公司有多个分公司，共享一个app,当我们给其中一个分公司开发一个子模块的时候，app会重新打包上线，然后其他分公司的用户就会有投诉，投诉说app有更新，但是更新之后，没有发现系统有任何变化(其实更新是针对另外一个分公司的)，还有一个问题就是各个分公司子模块越来越多，app的安装包越来越大， 考虑拆分多个app,但是公司管理层只希望整个集团只有一个app.</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/e3/7e07ae99.jpg" width="30px"><span>doannado</span> 👍（0） 💬（0）<div>20200307 单体 soa 服务化 平台化</div>2020-03-07</li><br/>
</ul>