你好，我是Chrono。

在上一次课里，我们看到容器技术只实现了应用的打包分发，到运维真正落地实施的时候仍然会遇到很多困难，所以就需要用容器编排技术来解决这些问题，而Kubernetes是这个领域的唯一霸主，已经成为了“事实标准”。

那么，Kubernetes凭什么能担当这样的领军重任呢？难道仅仅因为它是由Google主导开发的吗？

今天我就带你一起来看看Kubernetes的内部架构和工作机制，了解它能够傲视群雄的秘密所在。

## 云计算时代的操作系统

前面我曾经说过，Kubernetes是**一个生产级别的容器编排平台和集群管理系统**，能够创建、调度容器，监控、管理服务器。

容器是什么？容器是软件，是应用，是进程。服务器是什么？服务器是硬件，是CPU、内存、硬盘、网卡。那么，既可以管理软件，也可以管理硬件，这样的东西应该是什么？

你也许会脱口而出：这就是一个操作系统（Operating System）！

没错，从某种角度来看，Kubernetes可以说是一个集群级别的操作系统，主要功能就是资源管理和作业调度。但Kubernetes不是运行在单机上管理单台计算资源和进程，而是运行在多台服务器上管理几百几千台的计算资源，以及在这些资源上运行的上万上百万的进程，规模要大得多。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（62） 💬（6）<div>1. Kubernetes 算得上是一种操作系统吗？
算。什么是 OS，例如在物理服务器上，它用于对物理服务器硬件资源的抽象，并对进程进行调度等等。那么 Kubernetes 就是对云上资源的抽象，并对云原生微服务应用进行调度。Kubernetes 可以对公有云、私有云进行统一抽象，并实现对负载的无缝迁移和均衡，不会永远被绑定在某一个特定的云上。
OS，能屏蔽底层的复杂性，例如 Linux ，我们不用关心程序运行在哪个 CPU 核心上，OS 已经搞定了。Kubernetes 对云和应用程序进行了类似的管理，无须明确对应用程序在哪个节点或存储卷上进行硬编程。

2.我理解的 Kubernetes 组件的作用
2.1 主节点上的组件
2.1.1 API Server
负责集群中所有组件通信。访问它必须经过授权于认证。

2.1.2 集群存储
在控制平面中，只有集群存储是有状态的（会持久化的意思），存储集群的配置与状态。Kubernetes 底层用 etcd。etcd 认为一致性比可用性更加重要。对于所有分布式数据库，写操作性的一致性至关重要。etcd 使用 Raft 一致性算法解决这个问题。

2.1.3 Controller 管理器
Controller 管理器实现了控制循环，完成集群监控与事件响应。它负责创建 controller。一般控制循环包括：工作节点 controller、终端 controller 以及副本 controller。集群监控目的是保证集群当前状态与期望状态相匹配。集群监控基础逻辑大致如下：
* 获取期望状态。
* 观察当前状态。
* 判断差异。
* 变更消除差异点。

2.1.4 调度器
调度器职责是监听 API Server 来启动工作任务，并分配合适的节点。它的核心是排序系统，该系统有评分机制，将工作分配到分数最高的节点来运行任务。调度器确定可以执行任务的节点后，还会再进行前置校验，例如该节点是否仍然存在、分配的任务需要的端口当前选择的工作节点是否可以访问等，如果无法通过，该节点会被直接忽略，如果调度器最后无法找到合适的工作节点，则当前任务无法被调度，并被标记为暂停状态。 需要特别注意，调度器不负责运行任务，只为任务负责分配合适的工作节点。

2.2 工作节点上的组件

2.2.1 Kubelet
工作节点的核心部分。新工作节点加入节点后，Kubelet 会被部署到新节点，然后 Kubelet 将当前节点注册到集群中。它还有一个职责，监听 API Server 分配的任务，监听到就执行该任务，并维护一个与控制平面的通信频道。

2.2.2 容器运行时
工作节点需要通过它来获取、启动、停止执行任务依赖的容器，它负责容器管理与运行逻辑。</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（12） 💬（1）<div>老师，有几个小问题：

1. etcd能取代redis的大部分功能吗？

2.  在 Kubernetes 里则只有一类人：DevOps。是不是意味着以后对开发或者运维人员都有更大的挑战，毕竟Kubernetes的也很很庞杂的知识要去学习。

3. 状态信息中的“AGE”代表启动时长吗？

4. DNS插件在执行命令：minikube addons list 输出的列表中没看到。是不是说这个插件已经集成到k8s中了，不需要单独安装。</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（9） 💬（6）<div>执行minikube dashboard无法在本机自动用浏览器打开dashboard页面，网上搜到的解决办法：执行
kubectl proxy --port=8888 --address=&#39;虚拟机ip&#39; --accept-hosts=&#39;^.*&#39; &amp;
然后在本机打开http:&#47;&#47;虚拟机ip:8888&#47;api&#47;v1&#47;namespaces&#47;kubernetes-dashboard&#47;services&#47;http:kubernetes-dashboard:&#47;proxy&#47;#&#47;workloads?namespace=default</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（9） 💬（3）<div>请教老师几个问题：
Q1：Mater的四个组件运行在一台主机上吗？
一个mater包括四个组件，这四个组件是运行在同一台主机上吗？即“一个Mater对应一个主机”。或者是另外一种理解：mater是个逻辑概念，可以对应一台主机，也可以对应多台主机，比如两个组件运行在一台主机，另外两个组件运行在另外一台主机，两台主机合起来才是mater。哪一种理解对？
Q2：Pod与docker容器是什么关系？
一个pod就对应一个docker容器吗？ 比如创建一个nginx容器，那么此容器就对应一个pod。
Q3：Pod是集中存储在master上，由master分发到各个node运行吗？
Q4：启动k8s后台管理系统后，”node list”查询出的IP是固定的吗？
09课文章中，用“minikube node list”查询出来的结果中，IP是“192.168.49.2”。在我的笔记本上，查出来的也是“192.168.49.2”。 请问，这个IP是固定的吗？
Q5：09课中，启动nginx后怎么验证启动成功？
09课的最后，用“kubectl run ngx --image=nginx:alpine”这个命令启动了nginx，此命令中没有指定端口映射。 请问，怎么验证启动成功？  Localhost:80 吗？</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（8） 💬（2）<div>课后思考：
1. kubernetes 算得上是一种操作系统，正如它定位的就是 cloud native 一样。它与传统意义上的操作系统不同的是管理、调度的都是虚拟化&#47;池化的资源，与硬件之间隔了一层宿主操作系统（传统 OS）。
2. 哈哈，我觉得这里面的组件没有一个是多余的——都重要。没有 etcd 就没有持久化信息&#47;配置；没有 apiserver 整个集群就失联、失控；没有 kubelet 该节点就失联了；没有节点里的 container runtime 就没有 Pod，也就是没有任何应用服务；没有 kube-proxy，节点的服务就是孤岛；没有 controller manager 就无法管理节点及 Pod ，也就无法对外提供应用服务；没有 scheduler 集群就处于失衡状态。这里 apiserver 、 kubelet 、 kube-proxy 充当不同的桥接作用。</div>2022-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/d8/708a0932.jpg" width="30px"><span>李一</span> 👍（6） 💬（2）<div>问一个小白问题，看架构图 ETCD是在Master节点上的，由于ETCD记录了节点信息、ConfigMap、Secret数据，如果Master 节点宕机或数据损坏，K8S 如何保证数据完整性？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b5/46/2ac4b984.jpg" width="30px"><span>三溪</span> 👍（5） 💬（1）<div>罗老师画思维导图是真的强</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（5） 💬（2）<div>2.2.3 Kube-proxy
负责本地集群网络，保障 Pod 间的网络路由与负载均衡</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/8b/e3b827b7.jpg" width="30px"><span>笨蛋小孩</span> 👍（5） 💬（1）<div>老师，是不是minikube的作用就是提供了以上的基础组件？</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（3） 💬（1）<div>1. 什么是操作系统？根据我所学到知识，操作系统是帮助人管理硬件的，具体来说就是管理内存，cpu，硬盘这些内容。文件是硬盘的抽象，内存是内存条的抽象，进程是运行程序的抽象。总的来说，操作系统就是硬件再软件层面如何被抽象和管理的工具。从这个角度来看，k8s不算操作系统，因为k8s并不直接控制硬件，而是控制更高级别的抽象软件。但从结果上来看，k8s可以管理，并且主要是为这个产生的，所以又算是操作系统。与传统的操作系统区别在于，传统操作系统管理可以更多是单机管理，无法跨机器跨集群管理，但k8s可以，因为k8s天然在云上。
2. 对于一个操作系统来说，管理的重点在于，网络，计算和存储，网络方面会使用到kube-proxy和apiserver，计算方面有contonller-manager，scheduler，apiserver和kubelet，存储方面主要是etcd，我觉得都挺重要，缺少一环都无法成就操作系统的管理了，但硬要说最重要，可能还是etcd，毕竟其他的一关机就没了，但存储还在。</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（3） 💬（3）<div>一直没有清楚  module 和addon 区别，今天总于明白了😂</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/4e/ed/a15897e3.jpg" width="30px"><span>mango</span> 👍（2） 💬（1）<div>安装minikub碰到的问题，minikub start的时候，一直下载不了gcr.io&#47;k8s-minikube&#47;kicbase 。
我的解决方法：下载其他代替镜像（anjone&#47;kicbase）
docker pull anjone&#47;kicbase
minikube start --vm-driver=docker --base-image=&quot;anjone&#47;kicbase&quot; --kubernetes-version=&#39;v1.22.0&#39; 

</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/55/51/c7bffc64.jpg" width="30px"><span>Andrew</span> 👍（2） 💬（1）<div>老师，在真实环境中需要登录到master node才能对集群进行操作吗？
一般都会有一个kubeconfig文件，里面记录了server, user等信息，是通过本机直接和master node的api server进行交互吗？</div>2022-07-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（2） 💬（1）<div>回答下思考题：
1. 你觉得 Kubernetes 算得上是一种操作系统吗？
都说Kubernetes是云原生时代的操作系统，研究不深，说下自己的感受。
Kubernetes的核心是容器编排，围绕着调度，发明了Pod，再通过声明式api、控制器这些概念将Pod高效地调度与运行起来。所以说它管理软件（容器，如业务容器，本质是Node OS上的一个进程），确实是的，它控制了Pod的启停、副本等；但说它管理硬件，倒没看出来，像CPU、内存、存储也只参与了调度算法而已。

2. 和真正的操作系统相比有什么差异？说说你理解的 Kubernetes 组件的作用，你觉得哪几个最重要？
a. kube-apiserver，是k8s系统入口，类似于操作系统上的系统调用
b. kube-scheduler，调度器，容器编排最主要的组件，负责Pod调度，类似于操作系统上的控制器
c. kube-manage-controller，控制器，负责管理k8s中资源对象
d. kubelet，Pod生命周期管理，负责Pod运行环境创建，包括各种CRI、CNI等各种manager的管理
当然，etcd存储k8s所有对象配置，提供查询与订阅功能，并且性能优秀也是很重要的。</div>2022-07-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（2） 💬（2）<div>1.k8s感觉上更像是一个介于操作系统和应用之间的服务，相比传统的操作系统，它提供了更强大的资源抽象功能。
2.scheduler和kubelet比较重要。前者提供了pod调度功能，没有它服务就无法部署运行；kubelet是更基础的组件，没有它容器都无法运行，也无法上报节点状态。</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（1） 💬（1）<div>服务器是Ubuntu 22.04.2 LTS Server版本 最小化安装，没有Desktop 无法打开浏览器 故需要开启外部其他机器访问。
kubectl proxy --port=8001 --address=&#39;172.17.40.174&#39; --accept-hosts=&#39;^.*&#39; &amp;

--port 是指虚拟机端口
--address 是指虚拟机IP
http:&#47;&#47;172.17.40.174:8001&#47;api&#47;v1&#47;namespaces&#47;kubernetes-dashboard&#47;services&#47;http:kubernetes-dashboard:&#47;proxy&#47;</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（1） 💬（1）<div>请教下，容器被 scheduler 调度，但是实际对容器下发操作命令的是 kubelet，二者的通讯却是通过 apiserver 间接进行的，所以 apiserver 与 kubelet 之间是使用类似于 websocket 的流式通讯协议来通讯的吗？</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f0/e9/1ff0a3d5.jpg" width="30px"><span>...</span> 👍（1） 💬（1）<div>master节点需要安装kubectl插件吗</div>2022-10-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（1） 💬（2）<div>有几个问题想请教老师：

1. Pod 和 Node 的关系是什么？可以理解为 Pod 在 Node 上运行和挂载吗？

2. 当集群中有多个 Master 存在时，Master 和 Worker 是如何进行交流的？如果一个 Worker 可以和多个 Master 进行通信，那么 Master 之间是如何保证数据一致性的？如果 Worker 只能和某一个对应的 master 进行通信，那么 K8S 是如何处理单点故障的？

3. kube-proxy 的作用和服务对象是谁？是同一个 node 上不同的 pod 吗？我在想 container-runtime 已经包含了对外的网络模块，这里的 kube-proxy 的作用对象应该是局限于集群内部？</div>2022-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（3）<div>mac 上执行 kubectl get node, 为什么没有显示 master 节点的？
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   2d    v1.24.1</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（1） 💬（2）<div>这个结构，会不会产生信息欺骗？
apiserver负责太多内容，会不会满负荷，监控面板从etcd读数据，
如果kubelet如果一直上报错误的信息，是不是会产生监听错误的情况？</div>2022-07-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（1） 💬（2）<div>看图kubelet连接的是apiserver，可怎么又说kubelet也直接访问etcd呢？不是说apiserver是k8s集群中唯一访问etcd的组件吗？</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/27/791d0f5e.jpg" width="30px"><span>小林子</span> 👍（1） 💬（1）<div>我觉得 etcd 比较重要，它挂了，整个集群就躺了</div>2022-07-13</li><br/><li><img src="" width="30px"><span>隶</span> 👍（0） 💬（1）<div>minikube ssh登入节点, 除了master节点外, 其他的woker 节点有许多个, 这里不需要指定节点吗?</div>2024-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/cc/a0/bd31d495.jpg" width="30px"><span>陆美芳</span> 👍（0） 💬（1）<div>很不错的课程，最近刚好接触腾讯TKE，马上上来学，学完就可以用</div>2024-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6a/6f/348b4bec.jpg" width="30px"><span>下一个我</span> 👍（0） 💬（1）<div>执行minikube dashboard --port=8001时，8001也做了映射的（kubectl proxy --port=8001 --address=&#39;0.0.0.0&#39; --accept-hosts=&#39;^.*&#39; &amp;）报错如下：
🚀  正在启动代理...
19:37:28.124784   28288 binary.go:76] Not caching binary, using https:&#47;&#47;dl.k8s.io&#47;release&#47;v1.23.3&#47;bin&#47;linux&#47;amd64&#47;kubectl?checksum=file:https:&#47;&#47;dl.k8s.io&#47;release&#47;v1.23.3&#47;bin&#47;linux&#47;amd64&#47;kubectl.sha256
19:37:28.124830   28288 dashboard.go:152] Executing: &#47;home&#47;xxx&#47;.minikube&#47;cache&#47;linux&#47;amd64&#47;v1.23.3&#47;kubectl [&#47;home&#47;xxx&#47;.minikube&#47;cache&#47;linux&#47;amd64&#47;v1.23.3&#47;kubectl --context minikube proxy --port 8001]
19:37:28.147686   28288 dashboard.go:157] Waiting for kubectl to output host:port ...
19:37:28.318185   28288 out.go:239] ❌  因 HOST_KUBECTL_PROXY 错误而退出：kubectl proxy: readByteWithTimeout: EOF
老师帮看看什么问题了，谢谢！</div>2024-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/11/c8/9c92c1ac.jpg" width="30px"><span>LHANGRONG</span> 👍（0） 💬（1）<div>minikube dashboard failed to load module”canberra-gtk-module“这是什么问题呢</div>2024-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/55/61b3e9e3.jpg" width="30px"><span>承君此诺</span> 👍（0） 💬（1）<div>按评论里，通过kubectl proxy配置代理方式，没成功。我换了种方法，使用访问端配置ssh端口转发。
ssh -L 8001:127.0.0.1:42445 jxy@192.168.3.41 -N
jxy@192.168.3.41是虚拟机用户@ip；42445是dashboard port。
本机（访问端）通过http:&#47;&#47;127.0.0.1:8001&#47;api&#47;v1&#47;namespaces&#47;kubernetes-dashboard&#47;services&#47;http:kubernetes-dashboard:&#47;proxy&#47;#&#47;service?namespace=default，访问成功。</div>2024-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/52/56dbb738.jpg" width="30px"><span>牙小木</span> 👍（0） 💬（1）<div>dashboard 默认不会安装，需要执行
kubectl apply -f https:&#47;&#47;raw.githubusercontent.com&#47;kubernetes&#47;dashboard&#47;v2.7.0&#47;aio&#47;deploy&#47;recommended.yaml
...
...
The ClusterRoleBinding &quot;kubernetes-dashboard&quot; is invalid: roleRef: Invalid value: rbac.RoleRef{APIGroup:&quot;rbac.authorization.k8s.io&quot;, Kind:&quot;ClusterRole&quot;, Name:&quot;kubernetes-dashboard&quot;}: cannot change roleRef
需要 创建示例用户，参考 https:&#47;&#47;github.com&#47;kubernetes&#47;dashboard&#47;blob&#47;master&#47;docs&#47;user&#47;access-control&#47;creating-sample-user.md</div>2023-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（0） 💬（1）<div>老师，产线的机器都是基于命令行的，如何在生产环境打开dashboard呢</div>2023-07-17</li><br/>
</ul>