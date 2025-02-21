你好，我是郑建勋。

上节课的最后我们提到，对于大规模的线上分布式微服务项目，在实践中，我们会选择Kubernetes作为容器编排的工具，它是云原生时代容器编排领域的霸主。这节课，让我们来看看Kubernetes的基本原理。

## 什么是Kubernetes？

[Kubernetes](https://kubernetes.io/) 这个名字来自希腊语，意思是舵手。它可以自动部署、扩容和管理容器化应用程序。Kubernetes从谷歌内部对大规模容器的排版（Orchestration）中吸取经验，以谷歌内部的 Borg 和 Omega 系统为设计灵感。2014年，Kubernetes 已经被贡献给了云原生计算基金会（CNCF，Cloud Native Computing Foundation），成为了开源项目。

和操作系统抽象了单机的资源并调度了应用程序相似，Kubernetes是云原生时代的操作系统，它抽象了多台机器的资源，并完成了资源的灵活调度，这使我们能够轻松地管理大规模的集群。

**从架构上讲，Kubernetes的节点分为了两个部分：管理节点和工作节点。管理节点上运行的是控制平面组件，而工作节点上运行的是业务服务。**

![图片](https://static001.geekbang.org/resource/image/a8/fa/a8c5f3c1090fc6bd4f805273405902fa.jpg?wh=1920x1442)

管理节点上运行的控制平面组件主要包括下面这些服务。

- API Server  
  API Server是Kubernetes组件之间，以及Kubernetes与外界沟通的桥梁。外部客户端（例如kubectl）需要通过API Server暴露的 RESTful API 查询和修改集群状态，API Server 会完成认证与授权的功能。同时，API Server是唯一与 etcd 通信的组件，其他组件要通过与 API 服务器通信来监听和修改集群状态。
- etcd  
  etcd为集群中的持久存储，Kubernetes中的众多资源（Pod、ReplicationControllers、Services、Secrets ）都需要以持久的方式存储在etcd中，这样它们就可以实现故障的容错了。
- Controller Manager  
  Controller Manager 生成并管理众多的Controller。Controller的作用是监控感兴趣的资源的状态，并维持服务的状态与期望的状态相同。核心的Controller包括Deployment Controller, StatefulSet Controller 和 ReplicaSet Controller。
- Scheduler  
  Scheduler 为 Kubernetes 的调度器，它通过API Server监听资源的变化。当需要创建新的资源时，它负责将资源分配给最合适的工作节点。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/7d/cae6b979.jpg" width="30px"><span>出云</span> 👍（0） 💬（0）<div>思考题，补充一点：解耦。</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（0）<div>思考题：
1 走api，可以统一进行认证、鉴权；
2 标准化
3 我为人人，人人为我；</div>2023-02-09</li><br/>
</ul>