你好，我是雪飞。

上一讲我介绍了 K8s 中的核心资源对象——Pod，它是 K8s 中的最小部署单元，Pod 中包含了一个或者多个容器，这些容器中运行着满足各种业务需求的应用镜像。我们可以使用 kubectl 命令和 YAML 文件来部署 Pod，当 K8s 接到一个 Pod 资源对象的部署任务，它的 Scheduler 组件就会根据调度策略来决定这个 Pod 应该运行在哪些节点上，然后这些节点上的 kubelet 组件就会和容器运行时组件协同工作，将 Pod 中的容器运行在节点上。这节课我们就来深入了解一下 K8s 的节点管理和调度策略。

## 管理节点

节点是加入到 K8s 集群中的物理机、虚拟主机或者云服务器，它们组成了 K8s 集群的硬件基础设施，它也是 Pod 中容器运行的载体。节点分为管理节点和工作节点，分别运行着不同的 K8s 组件。通常 K8s 集群至少由两台以上的节点组成，这样才是真正意义上的集群，从而实现业务应用的高可用。

K8s 把节点也作为一种资源对象，从而纳入到 Controller Manager 组件的管理中。下面我们就来讲讲节点在 K8s 中的相关操作。

### 加入新节点

如果我们要新增加一个节点，需要先保证这个节点和现有 K8s 集群的节点在同一内网环境，能够相互访问。然后配置好新节点的系统环境，安装容器相关软件，安装 kubeadm 和 kubelet 组件，最后在新节点上执行 “kubeadm join” 命令来加入集群。具体过程可以参考集群搭建里介绍的步骤。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/4b/95812b15.jpg" width="30px"><span>抱紧我的小鲤鱼</span> 👍（5） 💬（1）<div>三种方法，对应本文的三个方法
1. 移除节点上的污点，
   kubectl taint nodes master-node node-role.kubernetes.io&#47;master-
2. 添加容忍
spec:
     tolerations:
     - key: &quot;node-role.kubernetes.io&#47;master&quot;
       operator: &quot;Equal&quot;
       value: &quot;&quot;
       effect: &quot;NoSchedule&quot;
3. 直接指定节点名称
 spec:
     nodeName: master-node
   </div>2024-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/93/c9302518.jpg" width="30px"><span>高志强</span> 👍（0） 💬（0）<div>奇怪了，我部署设置了容忍度的pod，并没有跑到节点1上，节点1我加了污点和效果类型都按老师步骤来的</div>2025-02-14</li><br/>
</ul>