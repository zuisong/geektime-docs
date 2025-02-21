你好，我是张磊。今天我和你分享的主题是：Kubernetes的资源模型与资源管理。

作为一个容器集群编排与管理项目，Kubernetes为用户提供的基础设施能力，不仅包括了我在前面为你讲述的应用定义和描述的部分，还包括了对应用的资源管理和调度的处理。那么，从今天这篇文章开始，我就来为你详细讲解一下后面这部分内容。

而作为Kubernetes的资源管理与调度部分的基础，我们要从它的资源模型开始说起。

我在前面的文章中已经提到过，在Kubernetes里，Pod是最小的原子调度单位。这也就意味着，所有跟调度和资源管理相关的属性都应该是属于Pod对象的字段。而这其中最重要的部分，就是Pod的CPU和内存配置，如下所示：

```
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
  - name: wp
    image: wordpress
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

> 备注：关于哪些属性属于Pod对象，而哪些属性属于Container，你可以在回顾一下第14篇文章[《深入解析Pod对象（一）：基本概念》](https://time.geekbang.org/column/article/40366)中的相关内容。

在Kubernetes中，像CPU这样的资源被称作“可压缩资源”（compressible resources）。它的典型特点是，当可压缩资源不足时，Pod只会“饥饿”，但不会退出。

而像内存这样的资源，则被称作“不可压缩资源（incompressible resources）。当不可压缩资源不足时，Pod就会因为OOM（Out-Of-Memory）被内核杀掉。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（82） 💬（5）<div>“为什么宿主机进入 MemoryPressure 或者 Dis...“

这是因为给宿主机打了污点标记吗？</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（41） 💬（5）<div>老师您好，cpu设置limit之后，容器的cpu使用率永远不会超过这个限制对吗？而mem设置limit之后，容器mem使用率有可能超过这个限制而被kill掉，也就是说设置了cpu limit之后，容器永远不会因为cpu超过限制而被kill对吗</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/79/22e582a5.jpg" width="30px"><span>刘岚乔月</span> 👍（21） 💬（3）<div>1、3、5都在追文章，一直都有一个疑问，请作者能解惑下。
对于主java是其他语言（非运维）的同学来说，我们是否需要深入了解k8s和docker（还是停留在使用层面） 我想一直跟着学的同学大部门还是冲着能找到更好的工作去的（有情怀的同学请忽略）
目前更大公司的招聘对于要求掌握k8s和docker的基本上都是运维岗位。
并没有招聘java要求掌握k8s和docker，面试中也不曾问到。感觉很尴尬 - -！
毕竟时间成本在哪，请作者能阐述下自己的观点！
</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（11） 💬（4）<div>在namespace limitRange 里面设置了default request 和 default limit之后，创建出来的pod即使不显式指定limit和request，是不是也是guaranteed？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/fe/7558e3f2.jpg" width="30px"><span>unique</span> 👍（10） 💬（5）<div>这时候，该 Pod 就会被绑定在 2 个独占的 CPU 核上。

独占的意思就是其它pod 不能使用这两个CPU了么？</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/f4/776ad2df.jpg" width="30px"><span>beenchaos</span> 👍（4） 💬（1）<div>请问张老师，cpuset是否只适用于nginx或者redis这类单线程的应用，为这类进程单独绑定一个CPU。而针对多线程的应用程序，设置cpuset反而会限制该应用程序的并发能力？这样理解准确么？</div>2019-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（4） 💬（1）<div>老师，能不能讲一下kubernetes是如何划分和管理宿主机上的cgroups结构的？</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/ab/3ea0e5cf.jpg" width="30px"><span>汪浩</span> 👍（3） 💬（1）<div>被称作“不可压缩资源（compressible resources）

应该是 uncompressible</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（1） 💬（2）<div>如果某个Guaranted Pod 的 Mem 设定为了256，在宿主机资源不紧张但该Pod 的的 mem 使用量达到了256以后会出现什么情况？会被oom杀掉吗？</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/73/90/9118f46d.jpg" width="30px"><span>chenhz</span> 👍（43） 💬（2）<div>
Pod 是最小的原子调度单位，所有跟调度和资源管理相关的属性，都是 Pod 对象属性的字段。其中最重要的是 Pod 和 CPU 配置。其中，CPU 属于可压缩资源，内存属于不可压缩资源。当可压缩资源不足时，Pod 会饥饿；当不可压缩资源不足时，Pod 就会因为 OOM 被内核杀掉。

Pod ，即容器组，由多个容器组成，其 CPU 和内存配额在 Container 上定义，其 Container 配置的累加值即为 Pod 的配额。

## limits 和 requests

- requests：kube-scheduler 只会按照 requests 的值进行计算。
- limits：kubelet 则会按照 limits 的值来进行设置 Cgroups 限制.


## QoS 模型
- Guaranteed： 同时设置 requests 和 limits，并且 requests 和 limit 值相等。优势一是在资源不足 Eviction 发生时，最后被删除；并且删除的是 Pod 资源用量超过 limits 时才会被删除；优势二是该模型与 docker cpuset 的方式绑定 CPU 核，避免频繁的上下午文切换，性能会得到大幅提升。
- Burstable：不满足 Guaranteed 条件， 但至少有一个 Container 设置了 requests
- BestEffort：没有设置 requests 和 limits。

## Eviction 

```bash
kubelet --eviction-hard=imagefs.available&lt;10%,memory.available&lt;500Mi,nodefs.available&lt;5%,nodefs.inodesFree&lt;5% --eviction-soft=imagefs.available&lt;30%,nodefs.available&lt;10% \
--eviction-soft-grace-period=imagefs.available=2m,nodefs.available=2m \
--eviction-max-pod-grace-period=600
```

两种模式：
- soft: 如 `eviction-soft-grace-period=imagefs.available=2m`  eviction 会在阈值达到 2 分钟后才会开始
- hard：evivtion 会立即开始。

**eviction 计算原理**： 将 Cgroups （limits属性）设置的值和 cAdvisor 监控的数据相比较。


最佳实践：DaemonSet 的 Pod 都设置为 Guaranteed， 避免进入“回收-&gt;创建-&gt;回收-&gt;创建”的“死循环”。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/42/8a79c613.jpg" width="30px"><span>wilder</span> 👍（30） 💬（1）<div>极客时间里面最爱的课程，没有之一，哈哈哈哈哈哈</div>2018-11-23</li><br/><li><img src="" width="30px"><span>Flying</span> 👍（12） 💬（2）<div>请用老师，cpuset为2，这个Pod就独占两个cpu核上，假如宿主机总共只有10个cpu核，那么这台机就只能运行5个cpuset=2的Pod吗</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（8） 💬（3）<div>能否分享一下给namespace 设置quota的经验呢？

如果设置的太小，会造成资源的浪费。如果设置太大，又怕起不到限制的作用。一个namespace使用资源太多可能会影响其他namespace用户的使用。

这是否也是namespace只能做soft multi-tenant的佐证呢？Cloudfoundry应该是按照实际的usage来设置space的quota，如果有监控插件，k8s可以也按照实际的usage来设置quota吗？</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/52/6659dc1b.jpg" width="30px"><span>黑米</span> 👍（7） 💬（8）<div>如果一个java应用JAVA_OPTS配置了-Xms4g -Xmx4g，k8s这边要配置多少的limit比较合适？直接4Gi的话应用内存达到一个阈值会被重启。</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/21/b0fe1bfd.jpg" width="30px"><span>Adam</span> 👍（4） 💬（3）<div>宿主机进入了MemoryPressure后被打上污点标记，新的POD不会被调度到此节点，那假如宿主机资源恢复正常后，这个污点标记会自己消失吗？还是说需要人工介入去处理。</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/d8/f0562ede.jpg" width="30px"><span>manatee</span> 👍（3） 💬（1）<div>请问老师，当pod因为Eviction 而被删除时，如果pod是被replica set设置了副本数的，他会在其他node中在被拉起吗</div>2019-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（2） 💬（0）<div>第四十课:K8s的资源模型和资源管理
K8s的资源分为两类，一类是可压缩资源（compressible resources），比如CPU，也就是当资源不足的时候Pod不会退出。另一类资源是不可压缩资源（incompassible resources），比如内存，其典型特点是当该资源不足的时候，Pod会因为OOM（Out Of Memory）被内核杀掉。

建议半个CPU配置用cpu=500m表示，而不是cpu=0.5（一个cpu=1000m，也就是cpu=1）

1Mi=1024*1024；1M=1000*1000

request和limit区别是：在调度的时候，kube-scheduler 只会按照 requests 的值进行计算。而在真正设置 Cgroups 限制的时候，kubelet 则会按照 limits 的值来进行设置。

当宿主机资源紧张的时间kubelet就会对Pod进行Eviction（资源回收），这时候会运用到QoS划分：
第一个会删除的是BestEffort类Pod，也就是Pod 既没有设置 requests，也没有设置 limits。
接下来第二个会删除的是Burstable类Pod。这是至少有一个 Container 设置了 requests。那么这个 Pod 就会被划分到 Burstable 类别
最后一类会删除的Pod是Guaranteed，也就是设置了request和limit，或者只设置limit的Pod。

Eviction 在 Kubernetes 里分为 Soft 和 Hard 两种模式。Soft Eviction 允许你为 Eviction 过程设置一段“优雅时间”，比如文章里的例子里的 imagefs.available=2m，就意味着当 imagefs 不足的阈值达到 2 分钟之后，kubelet 才会开始 Eviction 的过程。而 Hard Eviction 模式下，Eviction 过程就会在阈值达到之后立刻开始。

Kubernetes 计算 Eviction 阈值的数据来源，主要依赖于从 Cgroups 读取到的值，以及使用 cAdvisor 监控到的数据。

当宿主机的 Eviction 阈值达到后，就会进入 MemoryPressure 或者 DiskPressure 状态，从而避免新的 Pod 被调度到这台宿主机上。它使用taint把node taint，就无法调度Pod到其node之上了。

cpuset 方式是生产环境里部署在线应用类型的 Pod 时，非常常用的一种方式。设置 cpuset 会把容器绑定到某个 CPU 的核上，而不是像 cpushare 那样共享 CPU 的计算能力，这样能大大减少CPU之间上下文切换次数，从而提高容器性能。设置cpuset的方式是，首先Pod 必须是 Guaranteed 的 QoS 类型；然后，你只需要将 Pod 的 CPU 资源的 requests 和 limits 设置为同一个相等的整数值即可。
</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/02/fa/8149913a.jpg" width="30px"><span>大工 赵洁</span> 👍（2） 💬（3）<div>首先，你的 Pod 必须是 Guaranteed 的 QoS 类型；
然后，你只需要将 Pod 的 CPU 资源的 requests 和 limits 设置为同一个相等的整数值即可。
问题：满足条件1不就是满足了条件2了吗？</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/96/1538f36c.jpg" width="30px"><span>随意门</span> 👍（2） 💬（1）<div>请问，Kubernetes有办法限制每个容器的磁盘使用量吗？假设一个容器的日志输出到容器中的一个文件中，然后日志量有很大，怎么限制才能防止它把宿主机的磁盘都占满？</div>2019-09-25</li><br/><li><img src="" width="30px"><span>Lucius</span> 👍（1） 💬（4）<div>&quot;将 DaemonSet 的 Pod 都设置为 Guarant...&quot; 不太懂, Guaranteed和重新创建有什么关系</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/6b/9c3f3abb.jpg" width="30px"><span>阿鹏</span> 👍（1） 💬（0）<div>老师，关于资源隔离我有三个问题想请教一下。
第一，正如您所说，&#47;proc是不能被隔离的，但是我们可以通过lxcfs或者高版本的jdk版本来让容器里的服务知道自己的资源限制，或者还有方式，老师有推荐的吗？
第二，我使用lxcfs隔离后，容器内&#47;proc&#47;meminfo文件确实是限制后的内存大小，但是容器内&#47;proc&#47;cpuinfo的信息跟宿主机是一样的，那么容器内的应该要怎么知道自己正确的cpu数量呢？
第三，我参考github上的lxcfs-initializer使用DaemonSet和Initialzer给容器加入lxcfs，使用annotations做关联，使用了该annotation的deployment能正常部署，没使用的报错：
Timeout: request did not complete within allowed duration
求老师指点一下</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/ee/c5/f976e596.jpg" width="30px"><span>🎏 yingying 🎏</span> 👍（0） 💬（0）<div>老师，api server如果故障了，能不能临时调整cgroup进行扩容呢？</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/63/6513b925.jpg" width="30px"><span>杜少星</span> 👍（0） 💬（0）<div>QoS类别：
Guaranteed：requsts和limits都设置
Burstable：只设置了requests
BestEffort：requsts和limits都没设置


CPU可压缩资源
MEM\DISK不可压缩资源</div>2023-10-15</li><br/><li><img src="" width="30px"><span>Geek_4df222</span> 👍（0） 💬（0）<div>关于思考题，我的答案是：从实际工作负载的角度考虑，当然不希望pod工作在memory、disk不足的节点上，这样会增加pod异常的概率。从实现的角度，k8s应该是会将node置为不可调度状态，可能是通过打污点的方法，这样pod就不会被调度到该node上。
我还有一个问题，关于container 和cpu绑定的问题，是kubelet、cgroup还是操作系统支持的？</div>2023-08-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/yib4NPWzs5g36icOuVviaUtOUAAOvJn45EKCriaQIibSyicojLuQh687ZJ5flpvOaezORia7SjUCBtrneUGJh8HmKicrEw/132" width="30px"><span>我感觉你们在背着我学kubernetes</span> 👍（0） 💬（0）<div>而对于内存来说，当你指定了 limits.memory=128Mi 之后，相当于将 Cgroups 的 memory.limit_in_bytes 设置为 128 * 1024 * 1024。而需要注意的是，在调度的时候，调度器只会使用 requests.memory=64Mi 来进行判断 请问大佬这个64Mi 怎么算出来的呢怎么理解呢</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/6c/4a68a916.jpg" width="30px"><span>双叶</span> 👍（0） 💬（0）<div>查了一下文档，必须把 CPU Manager Policy 设置成 Static 才能有设置 cpuset 的功能

https:&#47;&#47;kubernetes.io&#47;docs&#47;tasks&#47;administer-cluster&#47;cpu-management-policies&#47;</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/bf/872c2289.jpg" width="30px"><span>Geek_Fang</span> 👍（0） 💬（0）<div>limit和request设置里面如果我只设置cpu=1，不设置其他资源，是不是也是独享的</div>2021-09-23</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（0） 💬（0）<div>因为kuberentes的cpu limit是使用cpu.cfs_quota_us实现的，所以是精确控制，因此cpu不会超过limit限制的值。 那么mem的limit是如何实现的呢？ </div>2020-12-06</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（0） 💬（1）<div>在Kubernets里，Pod是最小的原子调度单位。这也意味着，所有跟调度和资源管理相关的属性都应该是属于Pod对象的字段。通过设置requests和limits来进行资源的隔离。

cpu个数，cpu物理核、cpu逻辑核、vCPU的区别：比如：2块cpu，每块 24个物理核，每块物理核超卖成2块逻辑核，总共 2*24*2 = 96核，每个核超卖100个vCPU，则vCPU = 96*100 

1MiB和MB的区别： 1Mi = 1024* 1024 bytes ； 1M=1000*1000 bytes

cpu.shares 与 cpu.cfs_period_us &#47; cpu.cfs_quota_us的区别： 
cpu.shares无法精确控制CPU，在CPU不繁忙时，任何进程都没有CPU的限制，当CPU繁忙时，A进程的CPU能使用的量为 (A的shares)&#47;(所有进程shares的和)
cpu.cfs_period_us &#47; cpu.cfs_quota_us能够精确控制CPU，无论cpu是否繁忙，A进程能使用的CPU为cfs_period的一段时间内，只能被分配到总量为cfs_quota的CPU时间

Kuberentes的QoS有三种，在宿主机的资源紧张时起作用按优先级来驱逐Pod，分别是 Guaranteed、Burstable、BestEffort。

Kuberentes中的cpuset（绑核），其实就是将Pod的 requests设置和limits设置为相同的值
</div>2020-12-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIh7iatqAeGsJuDNxsDlmCQx64ktJl7ATAkBtDO6iczIqsLFPXkF6GPGJpMBCxbl4DJ5obHwAK0bSAQ/132" width="30px"><span>朱东辉</span> 👍（0） 💬（0）<div>由于处于这种状态下的主机被标记无敌，noschedule不可调度状态</div>2020-10-26</li><br/>
</ul>