你好，我是邢云阳。

在前几节课中，我们围绕单 Kubernetes 集群的资源如何操控，做了详细的介绍以及代码实践。但随着企业业务的发展和对云原生技术应用的深入，越来越多的企业开始面临管理多个Kubernetes 集群的需求。这些集群可能分布在不同的云供应商、地理位置或边缘设备上，以满足不同场景下的性能、成本及合规性要求。因此，本节课我将为你介绍一款由华为开源的多集群管理软件–Karmada，并讲解如何通过动态客户端等方式通过 Karmada 来操作多集群。

首先我们先来认识一下 Karmada。

## 什么是 Karmada？

Karmada 是一个由华为开源的云原生多云容器编排平台，目标是让开发者像使用单个 Kubernetes 集群一样使用多个 Kubernetes 集群。开发者可以在多个 Kubernetes 集群和云中运行云原生应用程序，而无需更改应用程序。Karmda 的架构图如下：

![图片](https://static001.geekbang.org/resource/image/0f/80/0fa97cyyb6b61190143e38518df57b80.png?wh=1706x1127)

可以看到 Karmada 在架构上，参考了很多 Kubernetes 的设计，比如 apiserver、调度器 scheduer、controller-manager、etcd等等。因此用户可以像访问普通 Kubernetes 一样，通过命令行，Rest API（client-go）等方式来访问 karmada。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2d/e5/6b/17de4410.jpg" width="30px"><span>🤡</span> 👍（0） 💬（1）<div>这里为什么要修改chart包里的这些参数的原因可以解释一下吗</div>2025-02-02</li><br/>
</ul>