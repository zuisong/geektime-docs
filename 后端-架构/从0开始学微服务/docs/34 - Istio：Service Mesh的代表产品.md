专栏上一期我们聊了Service Mesh，并以Linkerd为例介绍了Service Mesh的架构。随着技术发展，现在来看Linkerd可以说是第一代Service Mesh产品，到了今天当我们再谈到Service Mesh时，往往第一个想到的是[Istio](https://istio.io/)。为什么我认为Istio可以称得上是Service Mesh的代表产品呢？在我看来主要有以下几个原因：

- 相比Linkerd，Istio引入了Control Plane的理念，通过Control Plane能带来强大的服务治理能力，可以称得上是Linkerd的进化，算是第二代的Service Mesh产品。
- Istio默认的SideCar采用了[Envoy](https://www.envoyproxy.io/)，它是用C++语言实现的，在性能和资源消耗上要比采用Scala语言实现的Linkerd小，这一点对于延迟敏感型和资源敏感型的服务来说，尤其重要。
- 有Google和IBM的背书，尤其是在微服务容器化的大趋势下，云原生应用越来越受欢迎，而Google开源的Kubernetes可以说已经成为云原生应用默认采用的容器平台，基于此Google可以将Kubernetes与Istio很自然的整合，打造成云原生应用默认的服务治理方案。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（27） 💬（1）<div>日志使用批量加队列加异步处理</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/fa/e2990931.jpg" width="30px"><span>文敦复</span> 👍（3） 💬（1）<div>批量+异步！</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/34/c082419c.jpg" width="30px"><span>风轨</span> 👍（3） 💬（1）<div>日志不是业务关键数据，丢一部分也问题不大，异步处理能减少正常业务时间等待。</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（1） 💬（1）<div>可以配置日志上传的百分比，减少上传的数量</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/15/d5/6d66288b.jpg" width="30px"><span>极极</span> 👍（3） 💬（0）<div>老师，我有几个关于长连的疑问 ，希望您能解答，谢谢！

1. 上边提到 “理论上每一次的服务调用 Proxy 都需要调用 Mixer&quot; ，但是对于长连，或者 grpc 的长连来说，也需要每次都调用mixer吗？

2. 长连的负载策略如何实现？istio 是不是做了其他优化或兼容？

3. 还有长连的可靠性如何确保？发版时 pod 更换如何确保新旧长连接的交替？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/76/256bbd43.jpg" width="30px"><span>松花皮蛋me</span> 👍（2） 💬（0）<div>异步上传日记，不需要ack</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f4/d0/ecafbabd.jpg" width="30px"><span>锋尘</span> 👍（1） 💬（0）<div>Kafka 顺序写硬盘据说效率堪比内存，未验证过！</div>2019-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（0）<div>如果对日志收集的实时性要求不高，可以尝试用异步的方式来解决。</div>2019-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（0） 💬（0）<div>异步处理</div>2018-12-29</li><br/>
</ul>