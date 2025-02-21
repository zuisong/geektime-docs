你好，我是潘野。

我们在第十二讲曾经提到，动态扩缩容有两个层级，一个着眼于应用层级，通过上一讲的学习，我们掌握了如何使用Prometheus-Adapter与KEDA解决这个层级的问题。

第二个层级是Kubernetes集群本身容量的动态扩缩容，也就是根据集群的负载情况自动增加或减少节点数量，以满足应用的需求。

在这个层级的动态扩缩容中，我们可以使用 Kubernetes 官方社区支持的集群自动扩缩容工具Cluster Autoscaler，它能根据 Pod 的资源需求和节点的资源可用情况自动扩缩容集群。

除了Kubernetes社区主推的Cluster Autoscaler之外，云厂商也推出了自己的集群扩缩容工具来弥补Cluster Autoscaler中的一些不足，比如今天课程里将要重点学习的AWS Karpenter。

## Cluster Autoscaler

Kubernetes 集群伸缩一直是集群管理的重要课题之一，随着容器技术的普及和广泛应用，更需要我们找到高效伸缩集群的方式，来满足不断变化的负载需求。

Cluster Autoscaler 作为 Kubernetes 早期推出的集群伸缩工具，在简化集群管理方面发挥了重要作用。它通过监控集群资源利用率，自动增减节点以满足 Pod 需求，有效降低了运维成本并提高了资源利用率。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_45a572</span> 👍（0） 💬（1）<div>请教一个老师一个问题: aws的iam和k8s的rbac是不是有重合？ 用rbac能替代iam的权限检验吗</div>2024-04-29</li><br/>
</ul>