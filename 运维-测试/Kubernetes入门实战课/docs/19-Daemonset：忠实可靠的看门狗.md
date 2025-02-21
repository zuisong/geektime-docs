你好，我是Chrono。

上一次课里我们学习了Kubernetes里的一个新API对象Deployment，它代表了在线业务，能够管理多个Pod副本，让应用永远在线，还能够任意扩容缩容。

虽然Deployment非常有用，但是，它并没有完全解决运维部署应用程序的所有难题。因为和简单的离线业务比起来，在线业务的应用场景太多太复杂，Deployment的功能特性只覆盖了其中的一部分，无法满足其他场景的需求。

今天我们就来看看另一类代表在线业务API对象：**DaemonSet**，它会在Kubernetes集群的每个节点上都运行一个Pod，就好像是Linux系统里的“守护进程”（Daemon）。

## 为什么要有DaemonSet

想知道为什么Kubernetes会引入DaemonSet对象，那就得知道Deployment有哪些不足。

我们先简单复习一下Deployment，它能够创建任意多个的Pod实例，并且维护这些Pod的正常运行，保证应用始终处于可用状态。

但是，Deployment并不关心这些Pod会在集群的哪些节点上运行，**在它看来，Pod的运行环境与功能是无关的，只要Pod的数量足够，应用程序应该会正常工作**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/95/4e/1112248a.jpg" width="30px"><span>鱼</span> 👍（21） 💬（4）<div>老师，我想问问如果给一个node加上污点，那么在上面运行的不能容忍该污点的pod会自动跑到其他node上吗。</div>2022-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/92/4b/1262f052.jpg" width="30px"><span>许飞</span> 👍（14） 💬（1）<div>测试结论：当master节点去除污点时，pod会调度到master；master节点增加污点时，pod不会离开，手动删除后不会再增加</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（8） 💬（1）<div>Q1：1.原理上ds直接own所选择的pod，deploy则是own创建的rs，rs own pod；2.功能上deploy支持在线业务部署功能更多，比如滚动更新和回滚，快速扩缩副本，ds则副本数基本固定；3.使用上ds多用在提供平台侧的能力，deploy则多用在提供业务侧能力，当然平台侧也用得很多

Q2: taint和tolerence是和调度相关的概念，调度器调度pod是会考虑</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（5） 💬（1）<div>老师，kubectl get ds -n kube-system 找不到 Flannel ds ，查看了 kube-flannel.yml ，发现名空间已经改到 kube-flannel 。所以要使用 kubectl get ds -n kube-flannel 查看网络插件 Flannel 。</div>2022-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（4） 💬（3）<div>controller-plane是不是为了向openshift看齐</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（3） 💬（1）<div>已实操
1.重新添加master污点信息后，master节点上的pod应用不会自动删除；
2.污点容忍配置路径位置：kubectl explain ds.spec.template.spec.tolerations</div>2023-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/09/d0/8609bddc.jpg" width="30px"><span>戒贪嗔痴</span> 👍（3） 💬（2）<div>老师，是这样的，由于本人使用的k8s版本是v1.24.0，使用kubectl describe node master得到的结果是
Taints:             node-role.kubernetes.io&#47;control-plane:NoSchedule
                    node-role.kubernetes.io&#47;master:NoSchedule
因为刚开始不知道你最后那张图里说的新版本已经改为control-plane的这种写法了，导致按照教程操作下来2种方法都不能实现把pod调度到master上运行，所以请教下老师是不是taint和toleration都要改为control-plane的写法？</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（2） 💬（1）<div>如果未被忽略的污点中存在至少一个 effect 值为 NoExecute 的污点， 则 Kubernetes 不会将 Pod 调度到该节点（如果 Pod 还未在节点上运行）， 或者将 Pod 从该节点驱逐（如果 Pod 已经在节点上运行）。</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（2） 💬（4）<div>请问老师，调度是在什么时候发生的呢，我想到一个问题，一个pod的node加上污点，正常运转的情况你在回答里说，不会跑到其他机器上，那假如pod死亡，会重新根据污点情况进行调度吗，还是按照原先的策略进行调度呢</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/cd/2c3808ce.jpg" width="30px"><span>Yangjing</span> 👍（2） 💬（1）<div>类似 Mysql 的适合部署到“静态 Pod”上吗？ </div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9c/31/e4677275.jpg" width="30px"><span>潜光隐耀</span> 👍（2） 💬（1）<div>请问下，DaemonSet的Pod如果被删除，是否能被自动重建，保持高可用呢？</div>2022-08-03</li><br/><li><img src="" width="30px"><span>InfoQ_15df24517cff</span> 👍（1） 💬（2）<div>minikube创建的集群有两个节点，一个master、一个worker。但部署DaemonSet的时候，确实两个node都部署了pod，但发现一个问题，就是pod的ip都一样，这是为什么</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/f7/d8/dc437147.jpg" width="30px"><span>So what?</span> 👍（1） 💬（1）<div>因为 Deployment 所管理的 Pod 数量是固定的，而且可能会在集群里“漂移”，但，实际的需求却是要在集群里的每个节点上都运行 Pod，也就是说 Pod 的数量与节点数量保持同步。

老师，这里的“漂移”是什么意思呢，不是很明白</div>2023-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/f7/d8/dc437147.jpg" width="30px"><span>So what?</span> 👍（1） 💬（2）<div>老师，下面这个写在哪个文件里？

tolerations:
- key: node-role.kubernetes.io&#47;master
  effect: NoSchedule
  operator: Exists</div>2023-05-17</li><br/><li><img src="" width="30px"><span>Geek_02ce66</span> 👍（1） 💬（2）<div>老师请教一下使用DaemonSet启动的应用如何关闭呢</div>2023-02-27</li><br/><li><img src="" width="30px"><span>jntv</span> 👍（1） 💬（1）<div>1.重新添加master污点信息后，master节点上的pod应用不会自动删除；
2.污点容忍配置路径位置：kubectl explain ds.spec.template.spec.tolerations</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8c/bf/182ee8e6.jpg" width="30px"><span>周Sir</span> 👍（1） 💬（1）<div>Daemonset固定使用redis镜像吗</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/93/3c3f2a6d.jpg" width="30px"><span>安石</span> 👍（1） 💬（1）<div>容忍度为什么是在pod的字段而不是ds上的</div>2022-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（1） 💬（1）<div>记录一个问题:
master节点的ds报如下错:
ailed to create pod sandbox: rpc error: code = Unknown desc = failed to set up sandbox container &quot;85f6cc55c5bf809f10a6af0b888944031a14c159b9fc98b297f19874c22c5646&quot; network for pod &quot;redis-ds-2zhk6&quot;: networkPlugin cni failed to set up pod &quot;redis-ds-2zhk6_default&quot; network: open &#47;run&#47;flannel&#47;subnet.env: no such file or directory

只需将worker节点的 &#47;run&#47;flannel&#47;subnet.env 拷贝到 master 节点上的 &#47;run&#47;flannel&#47;subnet.env 再删除当前pod即可。</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f0/25/d3da7ca9.jpg" width="30px"><span>wuyang</span> 👍（1） 💬（1）<div>删除节点taint时，老是报错，有没有大神看下什么问题
wuyang@master-1:~$ kubectl describe node master | grep -i Taints
Taints:             node-role.kubernetes.io&#47;master:NoSchedule
wuyang@master-1:~$ kubectl taint node master node-role.kubernetes.io&#47;master:NoSchedule-node&#47;master untainted
error: all resources must be specified before taint changes: untainted

</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9a/e1/7df2ad19.jpg" width="30px"><span>fd</span> 👍（1） 💬（4）<div>所以，Kubernetes 就定义了新的 API 对象 DaemonSet，它在形式上和 Deployment 类似，都是管理控制 Pod，但管理调度策略却不同。DaemonSet 的目标是在集群的每个节点上运行且仅运行一个 Pod，就好像是为节点配上一只“看门狗”，忠实地“守护”着节点，这就是 DaemonSet 名字的由来。

===============
运行且仅运行一个 Pod，那我的业务Pod 就不能运行在这个节点上了么？还是 意思是 DaemonSet 其实是保证每一个节点都会有这个基础的Pod，比如日志收集，监控这类的POD，每一类的基础Pod 由 DaemonSet 保证有而且有一个？
</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（1） 💬（2）<div>记录一个问题，发现新建的pod的处于pending状态，通过kubectl describe pod发现有warning：`default-scheduler  0&#47;2 nodes are available: 1 node(s) had taint {node-role.kubernetes.io&#47;master: }, that the pod didn&#39;t tolerate, 1 node(s) had taint {node.kubernetes.io&#47;memory-pressure: }, that the pod didn&#39;t tolerate.`，发现由于主从节点各自的容忍度导致pod无法被调度，但从节点的`node.kubernetes.io&#47;memory-pressure:NoSchedule`污点一直无法去掉，只好在从节点清理了一些停止的docker容器后，发现pod被调度到了从节点，但没过多久pod的状态有变成了Evicted状态，提示The node had condition: [MemoryPressure]，然后扩容了下从节点的内存，问题终于解决。但想请教下老师，为什么从节点会被自动添加上`node.kubernetes.io&#47;memory-pressure:NoSchedule`的taint以及内存不足时无法去掉这个污点？为了扩容从节点的内存，我将从节点重启了下，然后再describe从节点，发现这个污点又消失了，这是为什么呢</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（1） 💬（1）<div>请教下老实，是不是也可以自定义开发一些其他依赖pod的API资源？</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（1） 💬（1）<div>k8s为啥没有通过参数区分deployment跟daemonset，直接封装成两种资源了？</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（1） 💬（1）<div>通俗易懂，学到了！</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：DaemonSet在每个节点都创建吗？是否可以限定节点？
文中的例子是说“而是要在每个节点上只创建出一个 Pod 实例”。但是，如果集群有100个节点，只是十个节点需要有DaemonSet，怎么处理？

Q2：去掉污点后pod还在运行
去掉污点后，kubectl get ds，发现数量从2变成1,。但是，kubectl get pod，还是有两个pod，处于运行状态。Master上的pod不会自动消失吗？ （需要用命令删除master上的pod吗）

Q3：修改ds.yml后，再次创建前需要删除原来的ds对象吗？
修改ds.yml，增加容忍度内容。再次执行“kubectl apply –f ds.yml”之前，已经存在ds对象和pod对象。再次创建ds之前，需要删掉原来的ds对象和pod对象吗？</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（1） 💬（1）<div>标签匹配 vs 污点容忍度匹配：
标签匹配的作用是实现 Pod 和 容器的匹配，进而实现对容器的编排
污点容忍度的匹配实现的是 Pod 和节点的匹配，进而对 Pod 进行编排
可以这样理解不？
</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/bf/47/c7e1633a.jpg" width="30px"><span>阿威</span> 👍（1） 💬（1）<div>使用第一种方法出现如下报错：
[root@master yaml]# kubectl taint node master node-role.kubernetes.io&#47;master:NoSchedule-node&#47;master untainted
error: all resources must be specified before taint changes: untainted</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（1） 💬（1）<div>昨天晚上搭建环境就碰见了第5点</div>2022-08-03</li><br/><li><img src="" width="30px"><span>jntv</span> 👍（0） 💬（1）<div>网络插件flannel是daemonset，位于名字空间kube-flannel内，可以用kubectl get ds -n kube-flannel查看。</div>2024-08-20</li><br/>
</ul>