你好，我是唐聪。

今天我将通过在Kubernetes集群中创建一个Pod的案例，为你分析etcd在其中发挥的作用，带你深入了解Kubernetes是如何使用etcd的。

希望通过本节课，帮助你从etcd的角度更深入理解Kubernetes，让你知道在Kubernetes集群中每一步操作的背后，etcd会发生什么。更进一步，当你在Kubernetes集群中遇到etcd相关错误的时候，能从etcd角度理解错误含义，高效进行故障诊断。

## Kubernetes基础架构

在带你详细了解etcd在Kubernetes里的应用之前，我先和你简单介绍下Kubernetes集群的整体架构，帮你搞清楚etcd在Kubernetes集群中扮演的角色与作用。

下图是Kubernetes集群的架构图（[引用自Kubernetes官方文档](https://kubernetes.io/docs/concepts/overview/components/)），从图中你可以看到，它由Master节点和Node节点组成。

![](https://static001.geekbang.org/resource/image/b1/c0/b13d665a0e5be852c050d09c8602e4c0.png?wh=1920%2A831)

控制面Master节点主要包含以下组件：

- kube-apiserver，负责对外提供集群各类资源的增删改查及Watch接口，它是Kubernetes集群中各组件数据交互和通信的枢纽。kube-apiserver在设计上可水平扩展，高可用Kubernetes集群中一般多副本部署。当收到一个创建Pod写请求时，它的基本流程是对请求进行认证、限速、授权、准入机制等检查后，写入到etcd即可。
- kube-scheduler是调度器组件，负责集群Pod的调度。基本原理是通过监听kube-apiserver获取待调度的Pod，然后基于一系列筛选和评优算法，为Pod分配最佳的Node节点。
- kube-controller-manager包含一系列的控制器组件，比如Deployment、StatefulSet等控制器。控制器的核心思想是监听、比较资源实际状态与期望状态是否一致，若不一致则进行协调工作使其最终一致。
- etcd组件，Kubernetes的元数据存储。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（5） 💬（1）<div>感觉这篇在讲述的创建pod的过程中，少了一些中间环节，比如介绍list-watch机制和Informer模块</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/00/bfc101ee.jpg" width="30px"><span>Tendrun</span> 👍（0） 💬（1）<div>是不是kube-apiserver 的Cache中缓存了全量的etcd key-value数据，还是说不是全量，只是一部分。如果是一部分那这部分缓存的维护更新机制是怎样的呢</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/ae/37b492db.jpg" width="30px"><span>唐聪</span> 👍（24） 💬（1）<div>kubernetes中创建一个pod工作流程，resource version含义与etcd，通过label&#47;fieldSelecotor查询性能，是比较常见的面试题。</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/61/e6/fedd20dc.jpg" width="30px"><span>mmm</span> 👍（10） 💬（0）<div>informer watch请求的resource version比kube-apiserver缓存中保存的最小resource version还小，kube-apiserver就会返回“too old Resource Version”，然后触发informer进行list全量数据，导致expensive request</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/2b/94b5b872.jpg" width="30px"><span>ly</span> 👍（1） 💬（0）<div>too old Resource Version

在更新资源的过程中，这个资源已经被其他进程更新的时候</div>2021-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（1） 💬（1）<div>有哪些原因可能会导致 kube-apiserver 报“too old Resource Version”错误呢： 有bug的时候</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/83/7788fc66.jpg" width="30px"><span>Simon</span> 👍（1） 💬（0）<div>思考题:

请求的版本在etcd已经回收了是不是就报&quot;too old Resource Version&quot;?</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/db/17/aee5d35a.jpg" width="30px"><span>远天</span> 👍（0） 💬（0）<div>唐老师，你好，prefix默认是&#47;registry，如果想自定义的话，要怎么设置呢？</div>2023-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/46/0f/f6cfc659.jpg" width="30px"><span>mckee</span> 👍（0） 💬（0）<div>导致 kube-apiserver 报“too old Resource Version”错误：
revision太小，数据可能被压缩，会触发relist；
watch cache size太小；</div>2022-05-23</li><br/>
</ul>