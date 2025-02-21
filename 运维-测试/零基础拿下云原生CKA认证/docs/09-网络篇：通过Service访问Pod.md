你好，我是雪飞。

前面我们学习了通过 Deployment 部署无状态应用 Pod，其中有些 Pod 中的应用是提供 Web 访问服务，所以需要通过网络访问到这些 Pod。

在部署 Pod 的时候，K8s 集群给它们分配了自己的 IP 地址，Pod 可以直接通过集群内部 IP 地址相互访问。但是我们还需要解决两个问题：

第一个是服务发现，K8s 中 Pod 的 IP 地址是动态分配的，每次 Pod 重启后都会重新分配一个内部 IP，因此无法使用固定的 IP 来访问 Pod。

第二个是负载均衡，Deployment 管理的 Pod 是多副本的，并且可以扩缩容，因此需要一个统一的访问入口将访问请求自动分配给这些 Pod 副本。为了解决这两个问题，Service 资源对象应运而生。

## 认识 Service

Service 是 K8s 中负责网络服务发现和负载均衡的资源对象，它定义了通过网络访问 Pod 的方式。当我们访问 Service 时，它自动将访问请求转发到相应的 Pod 上，然后由 Pod上的应用处理访问请求。

Service 主要处理“服务发现”和“负载均衡”这两个重要问题。服务发现是指当 Pod 发生变化时（如故障重启、扩容缩容等），Service 仍能自动找到变化后的 Pod。负载均衡是指 Service 可以代理多个 Pod 的网络访问，通过一定机制把访问 Service 的请求自动分配到这些代理的 Pod 中。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（0） 💬（1）<div>LoadBalancer 类型能不能给一个实际的例子，方便可以实操或者加深理解</div>2024-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/11/09/c2d178b7.jpg" width="30px"><span>子路无倦</span> 👍（0） 💬（0）<div>pod内可以通过svc 的cluster ip访问其他pod, 无法使用service name 访问是什么情况呢？我看coredns运行状态是正常的。</div>2024-12-31</li><br/>
</ul>