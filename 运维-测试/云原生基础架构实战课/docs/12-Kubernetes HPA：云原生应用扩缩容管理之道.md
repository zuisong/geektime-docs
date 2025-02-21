你好，我是潘野。

上一讲的末尾我讲了公有云上引起浪费的两个大类情况，其实云资源浪费是一个普遍存在的问题，无论是在公有云还是私有云环境中都可能发生，如何解决云资源浪费也是基础架构管理中非常重要的一个部分。

今天我们展开讲讲，哪些原因会造成云资源浪费，以及我们怎么利用好云原生技术来解决云资源的浪费问题，提升我们的资源使用率。

## 哪些情况会造成资源浪费？

云资源利用率低是指已分配的云资源没有被充分利用，导致闲置浪费。我们看看哪些情况会造成这个结果。

**首先是过度或错误配置。**在创建云实例时，为了满足峰值需求，应用维护者往往会配置过多的资源。然而，实际应用中，资源需求通常会低于峰值，导致大部分时间资源处于闲置状态。

比如我就遇到过这种情况：开发申请了十台300G内存的机器做Redis Cluster，而上线之后，发现实际使用率只有20%，这就相当于8台机器被浪费了。

错误配置的现象也很常见，配置云资源时，由于缺乏经验或相关知识，可能会出现错误配置。例如应用程序比较消耗CPU，不太消耗内存，但是却申请了一个内存很大的机器，导致资源浪费。

**然后是资源预留问题。** 为了保证资源的可用性，应用维护者会预留一定量的资源保障应用做横向或者纵向扩展。然而，预留资源往往无法完全利用，导致资源闲置浪费。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（0） 💬（2）<div>事件驱动动态扩缩容方案用knatine方案吗？</div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（1）<div>根据业务情况和历史数据 定时提前扩容。
VPA 有什么示列吗？</div>2024-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/81/53/857c999f.jpg" width="30px"><span>Starduster</span> 👍（1） 💬（0）<div>老师好，请问VPA做不到对pod资源限制的热更新吗？假设host资源足够，是不是只需要更改k8s记录的资源限制字段就行了，一定要重启pod才能生效吗？</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0f/d5/73ebd489.jpg" width="30px"><span>于加硕</span> 👍（0） 💬（0）<div>老师你好。微服务架构下，应用服务需要做容量规划么？还是统一用HPA来支撑流量变化？
</div>2024-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（0）<div>首先，VPA 不像 HPA，HPA 不会更改正在运行的 Pod，而 VPA 会更新正在运行的 Pod 资源配置，这会导致 Pod 的重建和重启。而且 Pod 有可能被调度到其他的节点上，这有可能会中断应用程序，这点可以说是 VPA 落地的最大的阻碍




这句话有毛病吧，VPA 不会中断正在运行的 pod。VPA 的策略是通过 gradual rolling updates 实现平滑地应用升级，避免影响 pod 的运行。</div>2024-09-04</li><br/>
</ul>