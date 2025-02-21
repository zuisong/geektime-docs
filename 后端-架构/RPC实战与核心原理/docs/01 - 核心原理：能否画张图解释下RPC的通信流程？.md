你好，我是何小锋。只要你做过几年开发，那我相信RPC这个词你肯定是不陌生了。写专栏之前，我还特意查了下RPC的百度指数，发现这些年RPC的搜索趋势都是稳步上升的，这也侧面说明了这项技术正在逐步渗透到我们的日常开发中。作为专栏的第一讲，我想只围绕“RPC”这个词，和你聊聊它的定义，它要解决的问题，以及工作原理。

在前些年，我面试工程师的时候，最喜欢问候选人一个问题，“你能否给我解释下RPC的通信流程”。这问题其实并不难，不过因为很多工程师平时都在用各种框架，他们可能并未停下来思考过框架的原理，所以，问完这问题，有的人就犹豫了，吱唔了半天也没说出所以然来。

紧接着，我会引导他说，“你想想，如果没有RPC框架，那你要怎么调用另外一台服务器上的接口呢”。你看，这问题可深可浅，也特别考验候选人的基本功。如果你是候选人，你会怎么回答呢？今天我就来试着回答你这个问题。

## 什么是RPC？

我知道你肯定不喜欢听概念，我也是这样，看书的时候一看到概念就直接略过。不过，到后来，我才发现，“定义”是一件多么伟大的事情。当我们能够用一句话把一个东西给定义出来的时候，侧面也说明你已经彻底理解这事了，不仅知道它要解决什么问题，还要知道它的边界。所以，你可以先停下来想想，什么是RPC。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/98/8f1aecf4.jpg" width="30px"><span>楼下小黑哥</span> 👍（103） 💬（8）<div>我们目前服务内部调用都是使用 rpc，对外接口采用 restful 接口。
采用rpc 开发最终要我觉得是设置合理超时时间以及重试次数。因为 rpc毕竟需要走网络调用，存在网络耗时。超时间太短，可能导致服务提供端实际执行成功，消费端却因为超时报错结束。这就有可能导致数据状态不一致。

另外，整个链路的超时需要合理设置，如A-》B-〉C，A的超时时间要大于B。

重试次数也需要关注，默认情况下，如 dubbo 重试次数为2，调用失败的情况下，框架会重新调用。而有些服务不能重复调用。
服务提供者应该是最熟悉自己服务的，所以服务提供者可以设置默认超时时间以及重试次数，消费者不设置，就会采用服务提供者参数设置。
😅想了下，开发过程中其实还有好多细节要注意，细节决定成败，后面章节可以再聊聊，让我们跟老师一起学习。</div>2020-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJTBnGDMyaGia98uoKVFwpVFC4CiafrWySk2DsTA3pDSrm4wEfeFSnsnWc9qzcVWnDZEsYtV1DcEkYQ/132" width="30px"><span>Geek_c8b5a1</span> 👍（61） 💬（4）<div>1、你应用中有哪些地方用到了 RPC？
在公司内部不同服务之间的调用都是走的RPC
2、你认为，RPC 使用过程中需要注意哪些问题？
1）下游服务的服务能力，避免因为你的调用把别人给调挂了，要事前协商好qps等，做好限流
2）调用服务异常时，要考虑降级、重试等措施
3）核心的服务不能强依赖非核心的服务，避免核心服务因为非核心服务异常而不可用</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（50） 💬（4）<div>1：你应用中有哪些地方用到了 RPC？
       我认为还是分开说比较好一点，侠义的RPC就是为了实现进程间方法调用像进程内方法调用一样简单。广义的RPC可以认为只要跨进程通信就是RPC，即使是在一台机器上两个进程间进行通信了，也是RPC，，不过目前来看RPC更强调侠义的含义。广义的含义和网络通信是一个意思，话说两台电脑之间想通信不靠网络靠什么呢？人肉操作嘛？
OK，RPC核心就是为了应用解藕而存在，只有系统间是进程通信必然会用到RPC。

2：你认为，RPC 使用过程中需要注意哪些问题？
第一服务注册服务发现，服务注册中心
第二服务治理，有多少服务？都是那些服务？谁调用谁？怎么下线服务？怎么修改服务分组？怎么修改服务别名？服务限流怎么控制？服务降级怎么控制？服务上下游信息？服务调用链信息？
第三服务监控，方法调用链监控？每个方法的监控，比如：TPS&#47;调用量&#47;可用率&#47;以及各种汇总聚合信息，最小&#47;最大&#47;平均&#47;各种TP分位统计，报警配置信息等等，这些东西一下就知道服务是否可用？在一个完整的调用链上那个服务比较慢？也可以统计服务的调用次数？对于分析排查问题，尤其是性能问题帮助非常大
第四日志查询平台，实时日志、现场日志、历史日志都能根据关键字界面化傻瓜式的查询出来，也能统计出日志里的报错信息关键字等。非常利于业务问题的排查，及时发现系统中的业务问题。
第五配置中心，可以调整日志级别、各种业务开关、服务分组别名信息，对于服务控制会非常灵活。
话说JD这些做的还挺不错，不过全链路跟踪系统好像做的还不太好，如果这个改造好了，那链路上那个系统慢就一目了然了，性能问题的排查会更简单方便。</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（32） 💬（9）<div>第一幅图中，编解码是一种码吗？
为什么序列化后生成编解码后还要再编码，才能放到网络上呢?
为什么不能直接一步序列化就放到网络上？</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ed/91/5dece756.jpg" width="30px"><span>陛下</span> 👍（23） 💬（3）<div>现在最严重的问题就是事物吧，分布式事物，感觉一直没有好办法解决</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/bf/ee93c4cf.jpg" width="30px"><span>雨霖铃声声慢</span> 👍（15） 💬（1）<div>1. 你应用中有哪些地方用到了 RPC？
我们的应用是微服务架构的，RPC就是连接这些微服务之间的纽带。
2. 你认为，RPC 使用过程中需要注意哪些问题？
因为RPC也是网络调用，性能方面肯定不如本地调用，所有RPC的API设计要仔细考虑，比如一次性能完成的调用就不要走多次调用。另外我认为最重要的是要有监控系统能监控所有的调用链，方便问题排查和性能调优。 </div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（14） 💬（4）<div>1、你应用中有哪些地方用到了 RPC？
答：我们目前系统进行拆分（C++开发的），也是分布式部署的，我们的RPC在系统间交互（或同步）数据时使用RPC接口进行调用。其次，我们RPC还是一个信息管家，可以通过事件进行提醒应用层主备机信息等。
2、你认为，RPC 使用过程中需要注意哪些问题？
答：这个问题让我想起了一次面试中面试官问我“你觉得一个设计RPC框架中最重要的是哪一点？”我当时首先说了RPC框架首先是通信、自定义协议（protobuf）、序列化、注册中心。我们的RPC由于C++开发的，只提供消息传输的功能，序列化和协议在应用层做的（主要是考虑不同项目的业务也有区别）。我觉得其中最重要的就是注册中心（数据中心）实现了，这个决定了RPC所能提供扩展功能。</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/55/198c6104.jpg" width="30px"><span>小伟</span> 👍（13） 💬（2）<div>我觉得广义来说，只要涉及调用的网络通信都属于RPC的范畴，包括Rest API，因为本质上都是走网络通信的非本地调用。
关于服务内部用RPC，服务外部用Rest API，主要考量的还是安全性。服务内部网络一般认为是相对安全的，因为已经有了很多手段来避免数据包外泄，故不需要强认证。而服务外部是对公网开放的，或至少部分是对公网开放的，数据在公网传输被认为是相对不安全的，所以要强认证。认证强弱的差别导致了RPC分成两派：针对服务内的高效的狭义RPC，和针对服务外的相对低效的RPC(Rest API)。
早在EJB的时代，有个叫RMI的东西，流程和RPC惊人的一致，只不过RMI还需要调用方维护大量底层细节，感觉RPC是从RMI发展来的，是好用版RMI。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4a/59/899e3b06.jpg" width="30px"><span>Leon</span> 👍（9） 💬（3）<div>老师你好，最近在从零开始手写个RPC框架，深有感触。
实现了多种序列化机制，集成了protobuff、protostuff、json和hessian等。
目前在编码服务发现，基于zk，思路是有，不是太清晰，编码总是断断续续。
希望多点实战性的指导</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/0e/c77ad9b1.jpg" width="30px"><span>eason2017</span> 👍（7） 💬（3）<div>调用过程中超时了怎么处理业务？
重试机制，降级处理。
什么场景下最适合使用 RPC？
网络安全稳定的环境。
什么时候才需要考虑开启压缩？
压缩后，数据量有明显的降低，压缩会使用CPU等资源，还是要看性价比。</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（6） 💬（6）<div>服务调用的RPC框架
RPC在使用中需要接口的版本，比如服务提供方升级了接口，比如增加字段了。请求方没有修改接口的版本。这样调用就会出问题了。这个问题的根本属于协议内容，如果设计好的协议支持兼容扩展，一般是向下兼容，就能实现低版本的调用方照样调用高版本的服务方</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/42/e5/61cfe267.jpg" width="30px"><span>Eclipse</span> 👍（5） 💬（2）<div>1 请求远程api接口，RESTful?
2 通讯的话，netty更适合做底层的事，rpc设计了部分业务治理？</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/fe/038a076e.jpg" width="30px"><span>阿卧</span> 👍（4） 💬（1）<div>1. 服务内部系统间交互时会经常用到rpc，例如创建订单的流程，订单中心调用业务系统的创单，并返回结果。
2. 要注意，rpc接口调用超时，接口访问量过高导致服务被拖垮等问题。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ed/a87bb8fa.jpg" width="30px"><span>此鱼不得水</span> 👍（2） 💬（2）<div>希望老师可以详细讲解一下服务注册和发现的流程，目前网上很多的资料对这个部分都介绍的比较马虎。</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>老师文中提到RPC主要体现再两个方面: 
屏蔽远程调用跟本地调用的区别，让我们感觉就是调用项目内的方法；
隐藏底层网络通信的复杂性，让我们更专注于业务逻辑。

这样话是不是RPC的实现和具体的传输协议没有关系，不管是TCP还是UDP哪怕是http&#47;2只要能满足上面就可以？</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/2b/4814d3db.jpg" width="30px"><span>阿土</span> 👍（2） 💬（2）<div>RPC的接口升级是一个很大而且很考验设计能力、管理能力的问题。包括且不限于接口字段添加与减少，版本升级，向下兼容，变更通知等。</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/23/76511858.jpg" width="30px"><span>洛奇</span> 👍（2） 💬（1）<div>老师，RPC和RMI  (远程方法调用) 有什么关系？</div>2020-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ca/82/85f6a1a2.jpg" width="30px"><span>番茄炒西红柿</span> 👍（1） 💬（1）<div>1.公司内的服务一般走rpc（目前用的是spring的解决方法）
2.rpc的问题：流控，错误处理，最难的问题：分布式事务处理</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/e6/50da1b2d.jpg" width="30px"><span>旭东(Frank)</span> 👍（1） 💬（1）<div>调用跨进程的服务或者跨网络的进程服务，像调用本地服务一样。

请问老师，课程中RPC 如果是调用同台上的不同应用服务是否也是按网络调用方式执行，还是有所优化呢？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（1） 💬（1）<div>1 公司项目不同服务之间的内部调用
2 数据传输量大小&#47;超时处理&#47;异常处理</div>2020-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/58/25152fa9.jpg" width="30px"><span>kevin</span> 👍（1） 💬（2）<div>1.内部服务见调用，访问缓存，ＭQ，数据库等都是通过RPC调用的；
2. 对于RPC调用要注意设置服务端超时时间和客户端超时时间，重试策略，快速失败，限流，降级，线程池等，对于多中心和机房的还要考虑具体的理由策略。</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/cd/d39e568c.jpg" width="30px"><span>felix</span> 👍（1） 💬（1）<div>建议老师，回复不要再加“您好，用户ID”了，用户ID非常干扰回复内容，谢谢。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/61/fedca2e9.jpg" width="30px"><span>(Kelen)</span> 👍（1） 💬（1）<div>老师你好，有个想法，我们在熟悉rpc过程中，我体会到，把概念最好解释清楚的方法之一是结合实际例子。就像算法学习一样，比如rpc,老师可以概念后面结合一个自己手写的简单的rpc，然后贴上各种代码。这样读者会不会更清楚，课下也可以练习</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（1） 💬（1）<div>只要存在client server通讯就需要rpc，对吗？知名rpc框架底层用的都是netty吗？</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/04/8a/942719cd.jpg" width="30px"><span>阳🌏Y(^_^)Y☀️光</span> 👍（1） 💬（1）<div>网站应用互相调用用的都是RESTful API，在学习各类分布式框架和计算引擎的时候基本随时都会看到RPC </div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d7/58/a2e8084f.jpg" width="30px"><span>crown</span> 👍（1） 💬（1）<div>工作中哪里用到了rpc？
    我是做游戏服务器开发的，有多个网关，多个业务处理服务器，玩家socket和某个确定的网关连接，网关和多个业务服务器连接。
   玩家发出请求，网关把请求转发给确定的业务服务器(也可以rpc调用)，业务服务器把处理结果返回给网关，网关再转发给客户端。
    重点是:如果网关和业务服务器rpc调用出现了超时后的处理。  希望能从本专栏学到点rpc知识应用到游戏服务器框架设计。</div>2020-02-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKUcSLVV6ia3dibe7qvTu8Vic1PVs2EibxoUdx930MC7j2Q9A6s4eibMDZlcicMFY0D0icd3RrDorMChu0zw/132" width="30px"><span>Tesla</span> 👍（1） 💬（3）<div>老师好，例如说redis的rpc调用。是指redis-cli开启的客户端，去远程调用redis-server中的方法吗？我一直以为redis-cls组件只是传命令字符串给服务端，经由服务端的唯一入口 一个解析命令的方法，再去触发相关操作。</div>2020-02-17</li><br/><li><img src="" width="30px"><span>蔡佳伟</span> 👍（0） 💬（1）<div>看完动手做一个！</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/98/5386341d.jpg" width="30px"><span>Coder</span> 👍（0） 💬（2）<div>请教一个问题，
调用方发起了一个请求K， 但是服务提供方是一个安装在分布式环境下每台主机上的一个程序。在不同的机器上安装不同的版本，比如版本1只实现了A,B请求， 版本2 实现了A,B,C请求，版本3实现了A,B,C,K请求。调用方对所有服务方机器进行调用，取得结果。那么没有实现k请求的机器，就会一直没有响应。这种问题怎么处理呢？ 是在调用方加上检查protocol版本检查，装了什么版本的机器发什么请求，还是在服务提供方那里，对不能识别的RPC请求，全部直接报错？</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f9/33/17246ab9.jpg" width="30px"><span>Goslly</span> 👍（0） 💬（1）<div>服务提供方调用方法的时候，不一定非得是反射吧？！</div>2020-05-04</li><br/>
</ul>