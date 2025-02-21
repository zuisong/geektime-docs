你好，我是潘野。

前面两讲，我们分别使用了两种持续集成工具（GitHub Action和Tekton）来实现IaC的GitOps。有同学可能有疑问，自己所在公司里的线上环境不是很大，只有两三个Kubernetes集群，应用也不是很多，十几个应用而已。为这个环境单独折腾一套持续集成环境，似乎投入产出比不高。

那么有没有什么轻量级的办法，同样可以实现GitOps方式下的IaC管理配置呢？

没错，这就是今天我们要学习的，基于Kubernetes Operator模式的云资源管理方式。

## Kubernetes Operator

首先，我给不熟悉Kubernetes Operator的同学介绍下什么是Operator。

### 控制器

如果你在Kubernetes中部署过应用，应该对Deployment控制器、Statefulset控制器，还有Job控制器相对熟悉，这些都属于Kubernetes 内置控制器，用于管理 Kubernetes 集群中的各种资源。

除了这些常见的控制器，我们日常工作里，还有三种控制器用得比较多。

第一个是常用在日志收集、监控方面的DaemonSet控制器。它的作用是在集群中的每个节点运行守护进程，确保集群中每个节点上都运行一个Pod副本。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（4）<div>使用 Crossplane 管理数据库，是通过在k8s上部署Operator ，直接在 k8s 所在的云厂商之上 创建的，就是说是 通过 k8s api 来管理了云资源，是这样吗？</div>2024-04-15</li><br/>
</ul>