你好，我是何辉。

任何一门学科都有它基本的知识结构，而Dubbo作为一款优秀的微服务框架，自然也有着其领域的基础知识。所谓万丈高楼平地起，想把Dubbo用得游刃有余，对基础知识的深刻理解就尤为重要了。

举一个最基础的问题：Dubbo的总体架构是什么样？一定有初学者或者面试官问过你吧，但常年忙着写业务代码逻辑，对于这样的提问，想必你是既熟悉又陌生，有种欲言又止的感觉，心里清楚却又无法一气呵成地向他人讲清楚。

没关系，今天，我们就一起来回顾Dubbo的基础知识体系，温故知新，之后我们碰到的一些异常或者问题时，就能快速定位问题归属于Dubbo的哪个角色，找准方向力求解决。

## 总体架构

我们知道，Dubbo的主要节点角色有五个：

- Container：服务运行容器，为服务的稳定运行提供运行环境。
- Provider：提供方，暴露接口提供服务。
- Consumer：消费方，调用已暴露的接口。
- Registry：注册中心，管理注册的服务与接口。
- Monitor：监控中心，统计服务调用次数和调用时间。

我们画一张Dubbo的总体架构示意图，你可以清楚地看到每个角色大致的交互方式：

![图片](https://static001.geekbang.org/resource/image/3c/80/3ce4ae4685e533094598a4608aa6dd80.jpg?wh=1920x1136)

对于一个Dubbo项目来说，我们首先会从提供方进行工程创建（第 ① 步），并启动工程（第 ② 步）来进行服务注册（第 ③ 步），接着会进行消费方的工程创建（第 ④ 步）并启动订阅服务（第 ⑤ 步）来发起调用（第 ⑥ 步），到这里，消费方就能顺利调用提供方了。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7b/ae/66ae403d.jpg" width="30px"><span>熊猫</span> 👍（6） 💬（6）<div>老师，你好，dubbo有没有这样的功能，一个接口多种实现，根据参数(标识渠道不同)来区分最终路由到哪个实现？再或者有没有在客户端可以知道有哪几种实现？</div>2022-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL2N4mhzsvvUG8Wew1uvTHs531fsW5LfgWkv4782VtwRuMf0qicRPxWtKgIzxyFSNVKJ09FN5vcVjg/132" width="30px"><span>Geek_895efd</span> 👍（4） 💬（2）<div>老师，关于注册中心部分，确实有很多选择，相对于zookeeper等，用阿里自家孵化出的nacos来做注册中心是不是更好</div>2022-12-23</li><br/><li><img src="" width="30px"><span>Geek_327f7f</span> 👍（1） 💬（1）<div>老师，我觉得您这里的dubbo架构图跟dubbo官网的出入挺大的，感觉您这个架构图应该是在dubbo框架下的微服务架构而不是dubbo的架构图，不知道我的理解是否正确。而且provider和consumer都是需要一个container提供dubbo的运行环境的吧，我看您的架构图中只有provider有container而consumer并没有。</div>2023-05-21</li><br/><li><img src="" width="30px"><span>Geek_244b79</span> 👍（1） 💬（3）<div>老师，您好，看完课程有两个疑问，1.监控中心是存在于哪里 2.注册中心的消息推送是主动推送的吗？希望老师看到可以帮忙解答，谢谢！</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/9c/030e80d3.jpg" width="30px"><span>java小霸王</span> 👍（1） 💬（1）<div>异常信息可以看出
1 超时机制是通过completeFutrue
2 failover策略</div>2022-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/80/f8f91bae.jpg" width="30px"><span>null</span> 👍（1） 💬（1）<div>老师，注册中心使用zookeeper和etcd哪个好？</div>2022-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fe/83/df562574.jpg" width="30px"><span>慎独明强</span> 👍（1） 💬（1）<div>补充一点：负载均衡策略，源码里面还有ShorestResponseLoadBalance
异常信息获取: 1) 重试次数为3，取的默认值 正常调用+重试2次  
2） providers [192.168.100.183:28040] (1&#47;1)  providers列表为1，第一次调用就失败了
3）集群容错策略为failOver故障转移
4）超时时间为1000ms
5）调用DemoFacade的sayHello方法超时
</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/72/28d07654.jpg" width="30px"><span>simuso</span> 👍（0） 💬（1）<div>为什么本地的zk连接没问题，如何连接其他服务器的zk就不行呢</div>2023-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/24/ff/c93a66ab.jpg" width="30px"><span>天天学习</span> 👍（0） 💬（1）<div>老师，dubbo.application.service-discovery.migration在yml文件配置的时候为什么没有提示选项呢，也点不进这个配置，我用的dubbo是3.1.8版本的</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fb/c3/5ec01038.jpg" width="30px"><span>Geek_forMySelf</span> 👍（0） 💬（1）<div>发生了TimeoutException应该需要provider方实现接口的幂等吧</div>2023-03-22</li><br/><li><img src="" width="30px"><span>Geek_698227</span> 👍（0） 💬（1）<div>请问有triple的内容吗</div>2023-03-10</li><br/><li><img src="" width="30px"><span>杨老师</span> 👍（0） 💬（1）<div>Dubbo 3.x 推崇的一个应用级注册新特性，主要是为了将来能支持十万甚至百万的集群实例地址发现，并且可以与不同的微服务体系实现地址发现互联互通。

这段话该怎么理解呢？

</div>2023-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/agpX9PDdhZsps8iaMREEgpiafV0Z0KpvT4JWcghibMz0z8ct7secPeEEsClc6t1ycHdRJOWbBETUcNp1Xa6h9urEg/132" width="30px"><span>Geek_221364</span> 👍（0） 💬（1）<div>
chatGPT告诉我的，不知道是否正确
dubbo.registry.register 和 dubbo.application.register 是 Dubbo 配置中的两个参数，它们分别用于控制服务提供者在注册中心上的注册行为和服务提供者在启动时将自己的地址信息注册到注册中心上的方式。

dubbo.registry.register 参数用于控制服务提供者在注册中心上的注册行为。它的取值可以是 interface、instance 或 all，分别表示只注册服务接口、只注册服务实例或同时注册服务接口和服务实例。使用这个参数可以控制服务提供者在注册中心上的注册行为，让服务提供者只注册必要的接口或实例，避免不必要的服务暴露。

dubbo.application.register 参数用于控制服务提供者在启动时将自己的地址信息注册到注册中心上的方式。它的取值可以是 provider 或 manual，分别表示服务提供者在启动时自动将自己的地址信息注册到注册中心上或需要手动将自己的地址信息注册到注册中心上。使用这个参数可以让服务提供者更灵活地控制自己在注册中心上的注册行为，避免一些不必要的服务注册，比如在测试环境中为了避免服务提供者过多的注册到注册中心上，可以设置 manual，然后手动将需要测试的服务提供者注册到注册中心上，这样可以控制测试服务提供者的数量。</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4e/78/ee4e12cc.jpg" width="30px"><span>Lum</span> 👍（0） 💬（1）<div>先远程调用超时了，然后又启用了failover策略，结果注册中心就一个节点就报错了</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（1）<div>请问下老师 ，代码中的 Facade 可以理解为一些公用的接口和实体类声明吗？</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a9/92/d9ab26d2.jpg" width="30px"><span>小明～</span> 👍（0） 💬（2）<div>老师，您好。最近有一个关于dubbo 需求是这样的: 平常在开发的时候，同一个服务，我本机的电脑，部署在开发环境服务器上的服务，同事电脑上启动的服务都有，经常出现调试的时候路由到了同事电脑上或者服务器的服务，我有个想法是按照优先级来调用：本机 优先于 服务器 优先于 同事电脑，如果想实现这个需求，我要准备哪一块的知识呢？学完本课程能解决这个问题吗？</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（0） 💬（1）<div>老师您好，一直有一个关于dubbo的疑问，就是如果provider和consumer分别设置了超时时间，那么实际上以谁为准？</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/aa/178a6797.jpg" width="30px"><span>阿昕</span> 👍（0） 💬（1）<div>  1.调用信息，生产者、消费者的地址，重试次数，超时时间；
  2.dubbo的信息，版本号、协议、端口号，调用的接口；
  3.异常信息，具体的异常、出现异常的代码行；</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/45/416fe519.jpg" width="30px"><span>Cha</span> 👍（0） 💬（1）<div>dubbo rpc应该是不依赖tomcat或者jetty容器</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（0） 💬（1）<div>老师，文中的代码有源码吗</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（0） 💬（1）<div>sayHello 调用超时  dubbo 重试3次  并给出超时时间和具体的调用信息 是么</div>2022-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/80/93/dde3d5f0.jpg" width="30px"><span>熊悟空的凶</span> 👍（0） 💬（1）<div>老师，您好  演示项目代码git地址能方便贴下不</div>2022-12-20</li><br/>
</ul>