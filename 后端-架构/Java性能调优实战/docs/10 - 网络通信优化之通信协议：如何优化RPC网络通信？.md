你好，我是刘超。今天我将带你了解下服务间的网络通信优化。

上一讲中，我提到了微服务框架，其中SpringCloud和Dubbo的使用最为广泛，行业内也一直存在着对两者的比较，很多技术人会为这两个框架哪个更好而争辩。

我记得我们部门在搭建微服务框架时，也在技术选型上纠结良久，还曾一度有过激烈的讨论。当前SpringCloud炙手可热，具备完整的微服务生态，得到了很多同事的票选，但我们最终的选择却是Dubbo，这是为什么呢？

## RPC通信是大型服务框架的核心

我们经常讨论微服务，首要应该了解的就是微服务的核心到底是什么，这样我们在做技术选型时，才能更准确地把握需求。

就我个人理解，我认为微服务的核心是远程通信和服务治理。远程通信提供了服务之间通信的桥梁，服务治理则提供了服务的后勤保障。所以，我们在做技术选型时，更多要考虑的是这两个核心的需求。

我们知道服务的拆分增加了通信的成本，特别是在一些抢购或者促销的业务场景中，如果服务之间存在方法调用，比如，抢购成功之后需要调用订单系统、支付系统、券包系统等，这种远程通信就很容易成为系统的瓶颈。所以，在满足一定的服务治理需求的前提下，对远程通信的性能需求就是技术选型的主要影响因素。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/53/ccb62ea0.jpg" width="30px"><span>夏天39度</span> 👍（29） 💬（2）<div>老师，能说一下Netty是如何实现串行无锁化完成链路操作吗，怎么做到无锁化的线程切换</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（22） 💬（1）<div>请教老师两个问题:
1. 在RMI的实现原理示意图中客户端的存根和服务端的骨架这两个概念是啥意思, 我感觉不太理解.
2. 在TCP的四次挥手中, 客户端最后的TIME_WAIT状态是不是就是CLOSE的状态, 如果不是那TIME_WAIT状态是在啥时候转换成CLOSE状态的.</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/b5/d1ec6a7d.jpg" width="30px"><span>Stalary</span> 👍（14） 💬（3）<div>老师，如果业务架构已经选择了SpringCloud，该如何优化远程调用呢，目前使用Feign，底层配置了HttpClient，发现qps一直上不去，暂时是对频繁的请求做了本地cache，但是需要订阅更新事件进行刷新</div>2019-06-11</li><br/><li><img src="" width="30px"><span>n88</span> 👍（10） 💬（2）<div>写http是短连接不太严谨</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8b/4b/15ab499a.jpg" width="30px"><span>风轻扬</span> 👍（5） 💬（2）<div>老师。我看到留言中有同学提到http和tcp的对比。http不是建立在tcp的基础上吗？http和tcp的关系应该怎么定义呢？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/8f/acd032f2.jpg" width="30px"><span>秃然的自我~</span> 👍（4） 💬（1）<div>老师好，我想问下已经在线上跑的服务，序列化方式是hessian，如果直接换成Protobuf，那么consumer会报错吗？如果报错的话，如何避免这种情况发生呢？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/b1/7b697ed4.jpg" width="30px"><span>晓晨同学</span> 👍（3） 💬（1）<div>有个问题请教一下老师
1.一直不清楚通信协议和序列化协议的区别是什么，两者都是制定报文协议然后传输，感觉序列化协议更具体到业务属性</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（3） 💬（1）<div>能不能讲一下netty的串行无锁化</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（3） 💬（1）<div>请问老师，对于大文件的传输，用哪种协议比较好</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（2） 💬（1）<div>还知道JAVA和Python系统之间互相调用的thrift</div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/8f/82/374f43a1.jpg" width="30px"><span>假装自己不胖</span> 👍（2） 💬（1）<div>对于网络编程比较迷茫，请问有没有小白一些的读物或博客推荐一下</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（2）<div>课后思考及问题
1：网上常见有关TCP和HTTP的问题，比如：
TCP连接的建立详细过程？TCP的连接断开过程？
三次握手建立连接，四次握手断开连接，感觉有些简单啦！如果面试时问到这个问题，老师建议该怎么回答？
另外，还有问一次HTTP请求经过了几次TCP连接，这个如果面试时遇到了，老师又建议该怎么好好的回答？
</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（1） 💬（1）<div>1. 老师线上有用过grpc吗，看文档说好像现在还不是特别的稳定？
2. 文中的性能测试，http是否有打开keep alive？走tcp无疑更快，我只想知道用http会慢多少，因为毕竟http更简单。有看过其他的benchmark，在打开keep alive的情况下，性能也还行，不知道老师这个测试是否打开？另外，从测试结果上看，当单次请求数据量很大的时候，http比tcp好像查不了多少是吗？
谢谢！</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/ba/412b05c1.jpg" width="30px"><span>放下</span> 👍（0） 💬（1）<div>老师你上面Feign的压测结果都是基于HTTP1.0的短链接吗？如果是HTTP1.1压测效果会不会更好一些</div>2020-05-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKibjS2ia1BldGnI6gGcy89W5y3009dMXpsibpkWMIWK9Tks1omwT1HQjibuKWibcmegrpXztvB1BbrOaA/132" width="30px"><span>greekw</span> 👍（0） 💬（1）<div>老师，能讲下netty的rector 线程模型的实例，以及串行无锁化设计的原理</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f8/3a/e0c14cb3.jpg" width="30px"><span>lizhibo</span> 👍（0） 💬（1）<div>老师 我想问的 Dubbo怎么更换成Protobuf 系列化协议？是要扩展Dubbo Serialization 接口吗？另外 Kryo 和 Protobuf 哪个性能高点啊</div>2019-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（0） 💬（1）<div>老师，您说http是短链接，http1·1的keep alive 不是长链接么。或者用http2·0也算是优化吧？</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/0a/12faa44e.jpg" width="30px"><span>晓杰</span> 👍（0） 💬（2）<div>今天面试，我说springcloud的feign是rpc框架，然后他说不是，是伪rpc框架，请问老师springcloud的feign是rpc框架吗</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（0） 💬（1）<div>老师好!文中提到了高效的 Reactor 线程模型。有适合新手的资料链接么?还有个pr啥的能一起给我个么谢谢了，文中讲的看不懂。
</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（0） 💬（1）<div>RPC要怎么学，项目中也用到了dubbo，可跟老师说的完全不一样，不是添加其他服务接口的依赖调用方法，而是发送http请求调用其他服务的接口。使我们用错了吗？
有个疑问依赖其他的服务的接口调用方法，接口都没有实现怎么调用？</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/9f/71345740.jpg" width="30px"><span>黑崽</span> 👍（0） 💬（1）<div>断开连接是四次挥手吧</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/dd/4f53f95d.jpg" width="30px"><span>进阶的码农</span> 👍（0） 💬（1）<div>我们是用spring-cloud 继承google的grpc</div>2019-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（5） 💬（1）<div>这个Dubbo阿里可以吹很多年啊</div>2019-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/77/423345ab.jpg" width="30px"><span>Sdylan</span> 👍（2） 💬（0）<div>Spring Clound 的Feigin更多是路由功能，将注解拼接成地址，Spring Cloud主要是整体完备，负载均衡、熔断啥的。</div>2019-10-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FheCgo4OvibofpdXVyWzev07tDHpqZ5CSArjLZ10kDMDwN7sUk3AHLUsuDUWk9KZEnSTWgXoLicn18UhsGgMfzrg/132" width="30px"><span>ZeWe</span> 👍（1） 💬（0）<div>RPC 远程服务调用，是一种通过网络通信调用远程服务的技术。RPC框架底层封装了网络通信，序列化等技术，提供接口包。本地调用接口可以无感透明的访问远程服务，是分布式系统的核心。
如何优化RPC框架，可从网络通信，报文序列化两方面考虑。
网络通信
1）选择合适的通信协议 TCP, UDP等
2）TCP协议下 使用长链接，减少连接资源消耗
3）高效的IO模型 如Netty NIO, 非阻塞io，Reactor线程模型，零拷贝等
4) OS层 TCP参数设置  file-max, keepalive-time等
序列化
1） 简单高效的报文设计
2) 高效序列化框架 编码解码</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>老师netty的reactor监听链接事件的主线程,可以认为是IO多路复用里的多路复用器selector吗?</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（0） 💬（0）<div>老师厉害，层层递进啊。。。虽然可能我们目前没有用到，但是却是个非常好的地图啊。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/c5/7fc124e2.jpg" width="30px"><span>Liam</span> 👍（0） 💬（0）<div>能否讲讲不同情况下，tcp各个调优参数的值应该怎么设和通常设置为多少</div>2019-06-11</li><br/>
</ul>