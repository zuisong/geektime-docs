你好，我是Chrono。

距离《Kubernetes入门实战课》完结已经有一段时间了，不知道你是否还在持续地学习、实践这个云原生时代的操作系统呢？我想答案应该是肯定的吧。

这次我带来了一个关于Kubernetes的最新消息，长期以来被关注的“下一代” Ingress 对象：Gateway API，在经过了近4年的讨论、测试和验证之后，终于在2023年的11月正式发布，可以用于生产环境，也就是我们常说的GA（generally available）。

那么，什么是Gateway API呢？它与Ingress有什么样的联系和区别呢？我们应该怎样在Kubernetes里部署和使用它呢？

今天我就来深入探讨这个话题，来看看Kubernetes的最新进展。

## 什么是 Gateway API

我们在[第21讲](https://time.geekbang.org/column/article/538760)对Ingress做过详细的介绍，相信你已经对它很熟悉了，它管理集群的进出口流量，提供完善的负载均衡和反向代理功能，**是部署Kubernetes应用必不可缺的组件**。

但是，Ingress的缺点也很明显，它自身的能力较弱，只能编写有限的路由规则，不能完全满足各种实际需求，所以Ingress Controller的实现者（如NGINX Ingress Controller、Kong Ingress Controller等）不得不使用大量的annotation和CRD来定制、扩展功能。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoREZlw6JWh1OXYvcKhOToBPCSqVr33Vhc0gmW9jNT3JHtW7NtaiaiaNJicjjxyVia7Oec3Qq1bzLGreQ/132" width="30px"><span>Geek_07ead6</span> 👍（1） 💬（1）<div>老师，不是说Gateway Class、Gateway 和 HTTPRoute是代替原来的ingress、ingressclass、ingressController这三个东西的吗？为啥上面又多了kong ingress controller的部署，kong ingress controller不只是原来ingressController的一个实现吗。没看懂新的里面GateWay和kong ingress controller的关系是啥，老师能加张图说一下Gateway Class、Gateway、HTTPRoute、kong ingress controller这四者的关系吗？</div>2024-04-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erLkXxEDm9ib2rtlHbVVO4qlFBWp5AArFpPctzSE0zkiaMiaol1IHVJ35ECC2goY5ibSufFPLp6dOzNmg/132" width="30px"><span>Geek_768d90</span> 👍（1） 💬（1）<div>感谢老师的坚持与付出！我认为学习K8S本身也要遵循CI&#47;CD：不断学习新知识，集成进自己的大脑；不断地在现网中实践，提供更加优化的交付方案。
我坚信这门课在极客时间一定会是一门精品课！</div>2023-12-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erRCf8vWbWibajdSaMtCM1OzPQ6uPhblgL4zXJvKoaQYVmialqFqr0NIdD6Dlm1F5icOBxiaXvUcQs4BA/132" width="30px"><span>sgcls</span> 👍（0） 💬（1）<div>Gateway API 与 Ingress 类似的功能模块映射：
Gateway --- Ingress Controller # 流量控制器
Gateway Class --- Ingress Class # 流量控制器类别
HTTPRoute --- Ingress # 路由规则集

这里 HTTPRoute 与 Ingress 的 Yaml 不同点：
HTTPRoute 指定了 Controller（parentRefs.0.name -&gt; Gateway 对象），而
Ingress 指定的是 Controller Class （spec.ingressClassName -&gt; Ingress Class 对象）


为什么这里会不一致呢？有种割裂感。
是不是因为 Ingress Class 后面才引入的，所以在 Ingress 里明确设置 ingressClassName 指向 Ingress Class 以支持新特性呢..</div>2024-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7a/72/a86c521e.jpg" width="30px"><span>六月</span> 👍（0） 💬（1）<div>看完本章马上去试了一下😂发现我的集群是1.23.17版本的。。。</div>2024-02-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9LFicnceEOlv9eNwJqjRDHbX87iaJectWs9ibgRLs8jTsDZDsvnTzUI8J1YJ1CiaNWzXiaTnkjscz4gR0wcvw3JfasoO0rg9FliaDsK8FqTQmHyNE/132" width="30px"><span>Geek_479239</span> 👍（0） 💬（1）<div>居然读到了最新的文章，新公司在用k8s开发，正好学习实战下</div>2023-12-01</li><br/>
</ul>