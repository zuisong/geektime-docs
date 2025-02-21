前面我们讲了两个常用文本类的RPC协议，对于陌生人之间的沟通，用NBA、CBA这样的缩略语，会使得协议约定非常不方便。

在讲CDN和DNS的时候，我们讲过接入层的设计，对于静态资源或者动态资源静态化的部分都可以做缓存。但是对于下单、支付等交易场景，还是需要调用API。

对于微服务的架构，API需要一个API网关统一的管理。API网关有多种实现方式，用Nginx或者OpenResty结合Lua脚本是常用的方式。在上一节讲过的Spring Cloud体系中，有个组件Zuul也是干这个的。

## 数据中心内部是如何相互调用的？

API网关用来管理API，但是API的实现一般在一个叫作**Controller层**的地方。这一层对外提供API。由于是让陌生人访问的，我们能看到目前业界主流的，基本都是RESTful的API，是面向大规模互联网应用的。

![](https://static001.geekbang.org/resource/image/f0/b8/f08ef51889add2c26c57c9edd3db93b8.jpg?wh=706%2A965)

在Controller之内，就是咱们互联网应用的业务逻辑实现。上节讲RESTful的时候，说过业务逻辑的实现最好是无状态的，从而可以横向扩展，但是资源的状态还需要服务端去维护。资源的状态不应该维护在业务逻辑层，而是在最底层的持久化层，一般会使用分布式数据库和ElasticSearch。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/74/c63449b1.jpg" width="30px"><span>问题究竟系边度</span> 👍（35） 💬（0）<div>dubbo 是这个rpc框架包括服务发现，服务均衡负载，接口层面监控。对于rpc中的扩展点比较多。后面会用servicemesh ,传输协议较多选择


spring cloud 是一个完整微服务框架，包括rpc框架,整体链路监控，熔断降级，网关，配置中心，安全验证。主要用http协议传输


对于跨语言的，首先要定义非编程语言相关的协议，例如http，protobuf ，然后需要每个语言需要写相关客户端，至于复杂程度，就要看服务发现，均衡负载是在客户端实现还是另外写一个代理</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/31/53b449e9.jpg" width="30px"><span>andy</span> 👍（17） 💬（2）<div>spring cloud的restful方式虽然基于json，但是服务端在发送数据之前会将DTO对象转换为JSON，客户端收到JSON之后还会转换为DTO。这时会在客户端和服务端分别创建各自的DTO对象，会出现代码的重复，如果共享jar，又出现jar管理的问题。</div>2018-08-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoRyUPicEMqGsbsMicHPuvwM8nibfgK8Yt0AibAGUmnic7rLF4zUZ4dBj4ialYz54fOD6sURKwuJIWBNjhg/132" width="30px"><span>咸鱼与果汁</span> 👍（8） 💬（2）<div>同样是基于TCP协议，为什么RPC会比HTTP快呢？</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/bf/85b957fc.jpg" width="30px"><span>咕咕咕</span> 👍（4） 💬（1）<div>还真是越到后面人越来越少 我看到现在也好多没看懂  准备先看完整体后  再回过头 仔细再看一遍</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c6/33/9ffaa2c7.jpg" width="30px"><span>怎么肥四</span> 👍（3） 💬（1）<div>书读百遍，其义自现。听不懂不要急，多看多听时间会让我们成长。</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（24） 💬（0）<div>题目1:
1.Dubbo只实现了服务治理，而Spring Cloud子项目分别覆盖了微服务架构下的众多部件。

2.Dubbo使用RPC通讯协议
Spring Cloud使用HTTP协议REST API

3.Dubbo通信性能略胜于Spring Cloud

4.Dubbo通过接口的方式相互依赖，强依赖关系，需要严格的版本控制，对程序无入侵
Spring Cloud 无接口依赖，定义好相关的json字段即可，对程序有一定入侵性


</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/65/03/973b24ec.jpg" width="30px"><span>谢晋</span> 👍（8） 💬（0）<div>Dubbo 和 SpringCloud 各有优缺点？
Dubbo只实现了服务治理，而Spring Cloud子项目分别覆盖了微服务架构下的众多部件。
Spring Cloud使用HTTP协议REST API
Dubbo使用RPC通讯协议
Dubbo通信性能略胜于Spring Cloud
Dubbo通过接口的方式相互依赖，强依赖关系，需要严格的版本控制，对程序无入侵
Spring Cloud 无接口依赖，定义好相关的json字段即可，对程序有一定入侵性
跨语言的RPC调用协议？
Thrift是Facebook提供的跨语言轻量级RPC消息和数据交换框架；
Ptotocol Buffers是Google提供的一个开源序列化框架，类似于XML、JSON这样的数据表示语言</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（7） 💬（0）<div>第二题，可以使用 thrift 和 protobuf</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cc/b3/a7d41547.jpg" width="30px"><span>及子龙</span> 👍（6） 💬（0）<div>我们用的是gRpc，对多语言支持的比较好。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（4） 💬（0）<div>跨语言调用的场景，可以使用序列化工具，比如Thrift、protobuf等序列化框架。</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（4） 💬（0）<div>题目2:
可以使用Thrift和Protocol Buffers。
Thrift是Facebook提供的跨语言轻量级RPC消息和数据交换框架；
Ptotocol Buffers是Google提供的一个开源序列化框架，类似于XML、JSON这样的数据表示语言。</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/2b/df3983e2.jpg" width="30px"><span>朱显杰</span> 👍（3） 💬（1）<div>请教下，文中说的dubbo的jar包，具体是指啥？我们公司正在用dubbo，不需要在应用离单独部署jar包啊</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（2） 💬（0）<div>2.跨语言如果使用 restful 基本可以直接用 如果用二进制rpc需要分别实现相应的客户端sdk</div>2018-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（1） 💬（1）<div>“0x92，表示有两个参数。其实这里存的应该是 2，之所以加上 0x90，就是为了防止歧义，表示这里一定是一个 int。”  
请问，是与谁发生了什么歧义呢？0x92不是与下面的参数值2（0x92）产生了歧义吗？谢谢。</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d7/b8/c42d2527.jpg" width="30px"><span>Jason Ding</span> 👍（1） 💬（0）<div>dubbo的rpc协议应该是dubbo协议，dubbo协议的序列化协议的 缺省值为hessian2，rmi协议缺省为java，http协议缺省为json</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/59/dc9bbb21.jpg" width="30px"><span>Join</span> 👍（1） 💬（0）<div>一般都gRPC，另外一个就是Thrift了</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/95/640b6465.jpg" width="30px"><span>fmouse</span> 👍（1） 💬（1）<div>Hessian2 不需要定义协议文件，不需要在客户端和服务端根据协议文件生成Stub，而是自描述的。文中后面说为了客户端和服务端序列化和反序列化，需要共享JAR。这个JAR是什么，接口定义，传递对象DTO的定义，不就是协议吗。这里没绕过来，没理解。帮忙进一步解释下，谢谢大家。</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/1e/126f58f2.jpg" width="30px"><span>乘风</span> 👍（1） 💬（0）<div>看刘老师推荐的论文都很经典，请问能再推荐一些相关的经典论文吗</div>2019-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIwMegHIHZLXIMpwlNib0XhF6G1QOPMRlzia1ZkicicxXY38RP63ia3g1fv9GZGLJoqblwlC9gDQkG3V5Q/132" width="30px"><span>Geek_a1d4e0</span> 👍（0） 💬（0）<div>多谢老师分享，普及了该领域的知识</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/f9/b2fe7b63.jpg" width="30px"><span>King-ZJ</span> 👍（0） 💬（0）<div>在微服务工作中，dubbo的等技术不断涌现，切切实实地解决实际问题。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/c3/ce3a18c6.jpg" width="30px"><span>土豆牛肉</span> 👍（0） 💬（0）<div>有了nginx，为什么还要用vanish呢</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/85/ed/905b052f.jpg" width="30px"><span>超超</span> 👍（0） 💬（0）<div>答问题一：Spring Clould与Dubbe间的对比可以看成是REST与升级版的RPC的对比。</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/ea/bdab7a0d.jpg" width="30px"><span>stany</span> 👍（0） 💬（0）<div>深入浅出，条理很清晰了。</div>2018-08-06</li><br/>
</ul>