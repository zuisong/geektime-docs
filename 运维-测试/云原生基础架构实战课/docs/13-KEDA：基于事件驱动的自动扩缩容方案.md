你好，我是潘野。

上一讲里，我们掌握了如何使用Kubernetes HPA这个工具，它配合Prometheus-Adapter即可实现应用的水平扩展能力。

不过，其中我们也发现了Prometheus-Adapter的一些局限性，例如依赖Prometheus，大部分情况下不能做到开箱即用，需要应用开发自定义Prometheus metrics，才能配合HPA使用。

那么有没有开箱即用型的工具，也能够配合HPA实现水平扩展呢？这就是我们今天要学习的KEDA。

## KEDA的由来

在Kubernetes诞生的时候，第一个专门为 Kubernetes 设计的监控工具，叫Heapster。Heapster能够收集Node节点上的cAdvisor数据，获取pod的CPU、内存、网络和磁盘的指标，它与 Horizontal Pod Autoscaler (HPA) 等工具结合使用，即可实现自动扩缩容。

但是2016年Prometheus从CNCF毕业之后，社区转向支持Prometheus，停止了对Heapster的维护。直到2018年的10月，Prometheus-Adapter才首次发布，直到2019年4月，Prometheus-Adapter才支持了Kubernetes HPA，所以在那段时期，Kubernetes社区还没有非常成熟的自动扩缩容方案。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（2） 💬（0）<div>keda 用是可以用 但要看你集群规模 和应用的架构，我觉得kubernetrs应用基本都是这样，只有规模足够大使用效果更好，你说你就5个页面几个后端，上集群可能就大材小用了</div>2024-04-22</li><br/>
</ul>