你好，我是姚秋辰。

在前面的课程中，我们借助Nacos的服务发现能力，使用WebClient实现了服务间调用。从功能层面上来讲，我们已经完美地实现了微服务架构下的远程服务调用，但是从易用性的角度来看，这种实现方式似乎对开发人员并不怎么友好。

我们来回顾一下，在前面的实战项目中，我是怎样使用WebClient发起远程调用的。

```
webClientBuilder.build()
    // 声明这是一个POST方法
    .post()
    // 声明服务名称和访问路径
    .uri("http://coupon-calculation-serv/calculator/simulate")
    // 传递请求参数的封装
    .bodyValue(order)
    .retrieve()
    // 声明请求返回值的封装类型
    .bodyToMono(SimulationResponse.class)
    // 使用阻塞模式来获取结果
    .block()
```

从上面的代码我们可以看出，为了发起一个服务请求，我把整个服务调用的所有信息都写在了代码中，从请求类型、请求路径、再到封装的参数和返回类型。编程体验相当麻烦不说，更关键的是这些代码没有很好地践行职责隔离的原则。

在业务层中我们应该关注**具体的业务实现**，而WebClient的远程调用引入了很多与业务无关的概念，比如请求地址、请求类型等等。从职责分离的角度来说，**我们应该尽量把这些业务无关的逻辑**，**从业务代码中剥离出去**。

那么，Spring Cloud中有没有一个组件，在实现远程服务调用的同时，既能满足简单易用的接入要求，又能很好地将业务无关的代码与业务代码隔离开呢？

这个可以有，今天我就来带你了解Spring Cloud中的一个叫做OpenFeign的组件，看看它是如何简化远程服务调用的，除此之外，我还会为你详细讲解这背后的底层原理。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/14/85/73e55be5.jpg" width="30px"><span>~</span> 👍（31） 💬（1）<div>这节课好早就学完了，但是后面的思考题一直没有时间搞清楚，今天闲下来后 debug 一遍后，大概明白具体流程了。
我觉得 OpenFeign 的远程调用分为两步
1. 首先是生成动态代理类，然后将代理类作为 bean 注入到 Spring 容器中
2. 然后是在调用过程中，代理类通过进行网络请求，向调用方做请求。

动态代理的原理其实 duckduckgo 一下就能找到无数篇文章，就不多说了，这里 OpenFeign 其实底层调用的是 Feign 的方法，生成了代理类，使用的是 JDK 的动态代理，然后 bean 注入。
调用过程，就是代理类作为客户端向被调用方发送请求，接收相应的过程。其中，feign 自行封装了 JDK java.net 相关的网络请求方法，可以重点关注一下 Client 类。我之前没有了解过，以为是直接用的 netty 或者其他的网络中间件；请求过程中还有 Loadbalancer 进行负载均衡；收到响应后，还需要对响应类进行解析，才能真正取出正确的响应信息。

最后：这些天还在忙其他东西，尽管老师更一篇看一篇，但是有些还要深入了解的，就要等到把所有文章的思考题摸清楚后再一步步填坑了。比如 OpenFeign 用的自行封装的 jdk 网络组件，是否可以使用其他中间件（例如 netty）实现呢？在请求过程中实现的负载均衡 loadbalancer 是怎么工作的？
以及我在 debug 过程中发现的问题：一旦发起调用时间过长，就会报错 「stream is closed」，io 没学好的我这方面之后也得稍微努力一下；在使用 debug 启动过程中，就出现过对 feign 的动态代理类调用 hashcode 代理方法的情况，应该是 spring 某个组件调用的（我在是数据库相关），但具体是谁我也不清楚。

以上就是大体的总结和我自己记录的问题，希望以后有时间把挖的坑慢慢填上，如果有什么问题或者不对的地方，欢迎大家批评指出~</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/8b/32a8c5a0.jpg" width="30px"><span>卡特</span> 👍（8） 💬（1）<div>金丝雀发布在微服务之间的通过openfeign流量转发规则咋定义和实现?</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/dd/00/4a7b9a9f.jpg" width="30px"><span>Nico</span> 👍（4） 💬（1）<div>老师，OpenFeign是自动集成了Loadbalancer了吗？以前OpenFeign是集成的ribbon，为啥现在又改为Loadbalancer？这个是出于什么考虑</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（1）<div>老师您好，我有4个问题，请指教：Q1：“构造请求路径、降级方法”，这句话中的“降级”是不是笔误？ Q2：openfeign是否可以认为是webclient的一个升级版本？  Q3：netflix体系中，feign是对ribbon的封装，feign的底层用的是ribbon，那么，openfeign的底层也是用webclient吗？ Q4： webclient只是webflux的一个很小的部分，而且不是webflux的主要功能，对吗？  </div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1e/cf/97cd8be1.jpg" width="30px"><span>so long</span> 👍（2） 💬（2）<div>这个是不是和mybatis创建数据访问接口的代理类的过程差不多</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/85/f72f1d94.jpg" width="30px"><span>与路同飞</span> 👍（1） 💬（1）<div>如果公司用的是api网关去代理请求的。是不是就没有必要用openFeign了。没有服务名并且path也不一样</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（0） 💬（1）<div>老师，关于 OpenFeign 这样基于 HTTP 的远程调用，和 dubbo 这样基于 TCP 的远程调用，使用时候有什么选型建议吗？感觉 dubbo 的性能要好很多</div>2022-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/29/cc30bd9d.jpg" width="30px"><span>逝影落枫</span> 👍（1） 💬（0）<div>类似的还有retrofit 和forest吧</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f8/0685f395.jpg" width="30px"><span>Java</span> 👍（0） 💬（0）<div>老师，openfegin被远程服务鉴权拦截了该怎么办</div>2024-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/f2/453d5f88.jpg" width="30px"><span>seker</span> 👍（0） 💬（0）<div>OpenFeign的动态代理流程图中，LocalService是指代前文的HelloWorldService吗？还是说LocalService是OpenFeign源码中真实存在的一个interface？</div>2023-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>源码之下，了无秘密㊙️</div>2022-01-07</li><br/>
</ul>