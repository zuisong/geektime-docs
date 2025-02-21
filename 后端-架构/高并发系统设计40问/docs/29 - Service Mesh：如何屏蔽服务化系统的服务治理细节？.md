你好，我是唐扬。

在分布式服务篇的前几节课程中，我带你了解了在微服务化过程中，要使用哪些中间件解决服务之间通信和服务治理的问题，其中就包括：

- 用RPC框架解决服务通信的问题；
- 用注册中心解决服务注册和发现的问题；
- 使用分布式Trace中间件，排查跨服务调用慢请求；
- 使用负载均衡服务器，解决服务扩展性的问题；
- 在API网关中植入服务熔断、降级和流控等服务治理的策略。

经历了这几环之后，你的垂直电商系统基本上已经完成了微服务化拆分的改造。不过目前来看，你的系统使用的语言还是以Java为主，之前提到的服务治理的策略，和服务之间通信协议也是使用Java语言来实现的。

**那么这会存在一个问题：**一旦你的团队中，有若干个小团队开始尝试使用Go或者PHP来开发新的微服务，那么在微服务化过程中，一定会受到挑战。

## 跨语言体系带来的挑战

其实，一个公司的不同团队，使用不同的开发语言是比较常见的。比如，微博的主要开发语言是Java和PHP，近几年也有一些使用Go开发的系统。而使用不同的语言开发出来的微服务，**在相互调用时会存在两方面的挑战：**

一方面，服务之间的通信协议上，要对多语言友好，要想实现跨语言调用，关键点是选择合适的序列化方式。**我给你举一个例子。**
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/35/79/21647da2.jpg" width="30px"><span>Keith</span> 👍（14） 💬（9）<div>API网关和Service Mesh有什么区别与联系呢? (它们都可以植入了服务治理策略)</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/ac/9cc5e692.jpg" width="30px"><span>Corner</span> 👍（12） 💬（3）<div>老师，您好。请问您在文中说的&quot;轻量级客户端&quot;目前有哪些开源的SeverMesh框架有实现呢？</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（9） 💬（1）<div>老师，请问一下：
1. 如果全栈都是java，那么service mesh就不是那么重要，是吗？
2. 文中看到iptable的性能会比rpc框架的性能要查，我以为iptable是走第三层或者第四层协议，而且只是转发，性能会很高，而rpc框架走第四层协议，而且需要解析协议内容，性能会更差一些。不知道老师能否讲解一下我理解的错误
谢谢了</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（7） 💬（2）<div>本质上感觉是又多了一层中间层，这个中间层来处理服务调用相关的事情，进一步的将业务逻辑和服务处理逻辑耦合的更松散一些，多加一层距离更远了一些，所以，性能上也会损耗更多一些。
目前还未接触实际方案，理解上大概这样。</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（6） 💬（1）<div>istio 中需要使用Kubernetes 这个，必须这样？</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/9c/5b06d143.jpg" width="30px"><span>芳菲菲兮满堂</span> 👍（4） 💬（1）<div>涨姿势 envoy lisio之前都还是懵懵的</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/35/79/21647da2.jpg" width="30px"><span>Keith</span> 👍（3） 💬（1）<div>关于服务治理策略, &quot;负载均衡、熔断降级、流量控制、打印分布式追踪日志等等，这些服务治理的策略都需要重新实现&quot;:
1. 熔断降级、流量控制这些不是在API网关中实现吗? 这些需要每个RPC客户端单独实现?
2. 服务治理策略是应用于外部客户端对系统的访问, 还是也包括内部RPC客户端之间的相互访问? </div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/71/a3/b881f08c.jpg" width="30px"><span>L响</span> 👍（1） 💬（1）<div>老师，Sidecar收到iptables转发的消息后，是否还要理解rpc协议呢？如果理解，那么Sidecar能够处理不同rpc协议吗？如果不理解，是否我们在rpc客户端和服务端要使用Sidecar的协议？</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/2b/4814d3db.jpg" width="30px"><span>阿土</span> 👍（1） 💬（1）<div>轻量级客户端一般怎么实现？有现成例子可参考么？另外，少量改造是改造些什么地方呢？</div>2019-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（1） 💬（1）<div>istio 和spring boot有联系和区别吗</div>2019-11-29</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkwbyTYtSCx6Qc7cQPnnRWv38Jybh3etziaPmuP8gHcgS6FMxcdftrKgWiamH6fc2iciaicDKDVEwcEibQ/132" width="30px"><span>sami</span> 👍（0） 💬（2）<div>感觉service mesh的服务治理是个大麻烦</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（7） 💬（1）<div>嘿嘿，补课补到最新更新了。
1.k8s都没用明白，更别说服务网格了。
2.服务网格出现时k8s的容器编排已经出现，istio的实现也依托于k8s基础平台。所以这是不好分割的东西。Sidecar是容器编排里面一种&quot;组合&quot;发布服务的模式，实现了多个容器（进程）对外作为一个容器的发布方式。这是落地服务网格这种数据传输与业务解耦的第一个条件。接下来基于容器的overlay网络也降低了多一层多一条的开销，亦是利于服务网格落地的。

3.服务网格的相关技术，还可以看看微博的WeiboMesh 。毕竟极客有微课讲述，相对好理解。</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/35/28/c729d3ae.jpg" width="30px"><span>@Dimples</span> 👍（2） 💬（1）<div>service mesh会淘汰springcloud吗</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（1） 💬（3）<div>SOFAMesh，github上说，这个项目已经补弃用了！改用了为istio贡献的方式了进行开发了。</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/6e/eb079ed7.jpg" width="30px"><span>永健_何</span> 👍（1） 💬（1）<div>老师，service mesh这个概念好新颖，是不是就是一个微服务的概念啊，没接触过，挺难理解的</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（1） 💬（0）<div>AWS最近推出了AWS app mesh服务，用来对抗Google云上的Istio，要启用app mesh需要把系统部署在EKS，不过过程还是比较傻瓜式的</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/34/fb871b2c.jpg" width="30px"><span>海罗沃德</span> 👍（1） 💬（0）<div>关于多语言的服务序列化，正好在李玥老师的课里听到了</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/51/e94e0e58.jpg" width="30px"><span>lllunaticer</span> 👍（0） 💬（0）<div>iptables 的效率比&#39;轻量级客户端&#39;要低这点没有很明确的说服力</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（0） 💬（0）<div>打卡，这一块没用到。
思维导图笔记：https:&#47;&#47;www.processon.com&#47;view&#47;link&#47;60df13201e085359888f06fe</div>2021-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/92/7e2cae07.jpg" width="30px"><span>地主家也没有余粮啊</span> 👍（0） 💬（0）<div>自从进了分布式的课程，每一课都是知识扫盲篇</div>2020-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/82/438c8534.jpg" width="30px"><span>longslee</span> 👍（0） 💬（0）<div>打卡。完全还没有涉及，哈哈。</div>2019-12-07</li><br/>
</ul>