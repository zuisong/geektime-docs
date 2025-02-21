你好，我是何小锋。上一讲我们学习了如何在没有接口的情况下完成RPC调用，其关键在于你要理解接口定义在RPC里面的作用。除了我们前面说的，动态代理生成的过程中需要用到接口定义，剩余的其它过程中接口的定义只是被当作元数据来使用，而动态代理在RPC中并不是一个必须的环节，所以在没有接口定义的情况下我们同样也是可以完成RPC调用的。

回顾完上一讲的重点，咱们就言归正传，切入今天的主题，一起看看如何在线上环境里兼容多种RPC协议。

看到这个问题后，可能你的第一反应就是，在真实环境中为什么会存在多个协议呢？我们说过，RPC是能够帮助我们屏蔽网络编程细节，实现调用远程方法就跟调用本地一样的体验。大白话说就是，RPC是能够帮助我们在开发过程中完成应用之间的通信，而又不需要我们关心具体通信细节的工具。

## 为什么要支持多协议？

既然应用之间的通信都是通过RPC来完成的，而能够完成RPC通信的工具有很多，比如像Web Service、Hessian、gRPC等都可以用来充当RPC使用。这些不同的RPC框架都是随着互联网技术的发展而慢慢涌现出来的，而这些RPC框架可能在不同时期会被我们引入到不同的项目中解决当时应用之间的通信问题，这样就导致我们线上的生成环境中存在各种各样的RPC框架。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/57/fb/7f6d64ba.jpg" width="30px"><span>Desmond</span> 👍（12） 💬（3）<div>在反序列化后，且调用API前加一个过滤器，识别是什么协议，老协议按老逻辑走，新协议按新协议逻辑走，多个过滤器构成一个调用链</div>2020-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f1/55/8ac4f169.jpg" width="30px"><span>陈国林</span> 👍（6） 💬（1）<div>当下云原生微服务框架 Service meth大火，通过在meth层做兼容应该可以解决多RPC协议问题</div>2020-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/ef/090e13a5.jpg" width="30px"><span>zero</span> 👍（0） 💬（1）<div>rpc的调用是微服务间直连调用，请问协议转换这层逻辑放在哪里，换了新协议是指在当前rpc框架更换协议还是直接更换了rpc框架</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/75/ff76024c.jpg" width="30px"><span>那个谁</span> 👍（0） 💬（3）<div>我想到的一种思路是，上线带监控的rpc，把未包含的协议监控起来，逐步上线支持</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（10） 💬（1）<div>
RPC架构层次：
♻️序列化框架：作用是将方法调用时传入的发送数据从对象转为二进制，序列化一般用在协议里面的payload里面（最简单就是java对象序列化为二进制流封装为消息体然后基于http传输）如jdk、msgpack、protobuf、json、hessian等，推荐首选的还是 Hessian 与 Protobuf。
♻️编解码框架：编解码是对网络传输消息进行处理，把二进制的数据(payload)进一步封装（或者拆解）为rpc的协议(消息头+消息体)。
♻️协议：包括协议头和协议体，协议的作用就是用于分割二进制数据流。每种协议约定的数据包格式是不一样的。是网络传输数据格式的约定，作用将发送的数据按照一定的规约进行序列化为二进制流，有http&#47;tcp&#47;ftp等协议，grpc就是就是基于http的协议。
     -&gt;补充：协议解析过程就是把一连串的二进制数据变成一个 RPC 内部对象，但这个对象一般是跟协议相关的，所以为了能让 RPC内部处理起来更加方便，我们一般都会把这个协议相关的对象转成一个跟协议无关的 RPC 对象。
♻️Proxy：作用是让RPC框架根据调用的服务接口提前生成动态代理实现类，实现类似本地的调用感觉。
♻️负载均衡框架：结合服务注册中心实现服务端列表的路由选择和调用，如restTemplate、ribbon、feignClient等。
♻️熔断降级框架：实现调用过程中的熔断保护和降级函数。</div>2020-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（8） 💬（0）<div>magic number和协议可以缓存到map中，或者redis中，从配置中心读取，当配置中心修改后，热更新到对应的缓存中。</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（4） 💬（0）<div>dubbo就支持多种协议</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/cb/c7541d52.jpg" width="30px"><span>cwfighter</span> 👍（2） 💬（0）<div>插件化，支持自定义协议插件即可</div>2020-09-03</li><br/><li><img src="" width="30px"><span>hillwater</span> 👍（0） 💬（0）<div>这种是单端口多协议吗？</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（0）<div>“等所有的应用都接入完新的 RPC 以后，再让所有的应用逐步接入到新的 RPC 上”
这句话没看懂逻辑</div>2022-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/cb/c7541d52.jpg" width="30px"><span>cwfighter</span> 👍（0） 💬（0）<div>还是要结合先住，如果rpc框架已经比较老旧了，还不如直接完全迁移到新的RPC框架做一次技术体系升级。我们目前就在做框架迁移，修改老的框架成本高，稳定性存疑，果断放弃，直接迁移新框架。当然，过程是很漫长的，迁移细节也很多。。</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/81/66/31c7969e.jpg" width="30px"><span>随风而逝</span> 👍（0） 💬（0）<div>课后思考，解析magicnumber拿到协议类型，如果类型遗漏或更新不及时，就需要某种机制去支持我们能动态的获取对应协议的解析规则。想到一种方案，就是增加新的协议时，可将 新的协议及对应的解析规则进行存储，比如说放在一个 “协议配置中心”， 服务方通过magicnumber进协议匹配时，去请求协议配置中心，拉去对应的解析规则，拉取后进行实例后存储在本地。</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（0）<div>如果线上协议存在很多种的话，就需要我们事先在 RPC 里面内置各种协议，但通过枚举的方式可能会遗漏，不知道针对这种问题你有什么好的办法吗？
没get到为什么会出现遗漏的现象？
如果真的会遗漏，评论中协议过滤器链的思路很好</div>2020-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/26/f54c9888.jpg" width="30px"><span>redis</span> 👍（0） 💬（0）<div>配置外部化，rpc框架一般都支持协议的扩展，可以通过加载外部配置的方式去构建应用支持的协议</div>2020-04-23</li><br/>
</ul>