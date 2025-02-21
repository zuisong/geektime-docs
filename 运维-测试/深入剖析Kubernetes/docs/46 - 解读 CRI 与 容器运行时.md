你好，我是张磊。今天我和你分享的主题是：解读 CRI 与 容器运行时。

在上一篇文章中，我为你详细讲解了 kubelet 的工作原理和 CRI 的来龙去脉。在今天这篇文章中，我们就来进一步地、更深入地了解一下 CRI 的设计与工作原理。

首先，我们先来简要回顾一下有了 CRI 之后，Kubernetes 的架构图，如下所示。

![](https://static001.geekbang.org/resource/image/70/38/7016633777ec41da74905bfb91ae7b38.png?wh=1940%2A1183)  
在上一篇文章中我也提到了，CRI 机制能够发挥作用的核心，就在于每一种容器项目现在都可以自己实现一个 CRI shim，自行对 CRI 请求进行处理。这样，Kubernetes 就有了一个统一的容器抽象层，使得下层容器运行时可以自由地对接进入 Kubernetes 当中。

所以说，这里的 CRI shim，就是容器项目的维护者们自由发挥的“场地”了。而除了 dockershim之外，其他容器运行时的 CRI shim，都是需要额外部署在宿主机上的。

举个例子。CNCF 里的 containerd 项目，就可以提供一个典型的 CRI shim 的能力，即：将Kubernetes 发出的 CRI 请求，转换成对 containerd 的调用，然后创建出 runC 容器。而 runC项目，才是负责执行我们前面讲解过的设置容器 Namespace、Cgroups和chroot 等基础操作的组件。所以，这几层的组合关系，可以用如下所示的示意图来描述。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（20） 💬（1）<div>kubelet 可以直接对接contained ? 中间不需要额外实现cri shim ？还是containerd 中已经集成了cri shim？</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（36） 💬（1）<div>DevicePlugin中的allocate函数是是在container creating的时候被调用，从而device plugin可以执行特定的操作，比如attach设备以及驱动目录。
所以应该是使用到了：
Createcontainer()这个接口
</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（10） 💬（0）<div>containerd应该会把请求交给contained-shim，然后再调runC吧</div>2019-07-16</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（8） 💬（0）<div>调度器将Pod调度到某一个Node上后，Node上的Kubelet就需要负责将这个Pod拉起来。在Kuberentes社区中，Kubelet以及CRI相关的内容，都属于SIG-Node。

Kubelet也是通过控制循环来完成各种工作的。kubelet调用下层容器运行时通过一组叫作CRI的gRPC接口来间接执行的。通过CRI， kubelet与具体的容器运行时解耦。在目前的kubelet实现里，内置了dockershim这个CRI的实现，但这部分实现未来肯定会被kubelet移除。未来更普遍的方案是在宿主机上安装负责响应的CRI组件（CRI shim），kubelet负责调用CRI shim，CRI shim把具体的请求“翻译”成对后端容器项目的请求或者操作 。

不同的CRI shim有不同的容器实现方式，例如：创建了一个名叫foo的、包括了A、B两个容器的Pod

Docker: 创建出一个名叫foo的Infra容器来hold住整个pod，接着启动A，B两个Docker容器。所以最后，宿主机上会出现三个Docker容器组成这一个Pod

Kata container: 创建出一个轻量级的虚拟机来hold住整个pod，接着创建A、B容器对应的 Mount Namespace。所以，最后在宿主机上，只会有一个叫做foo的轻量级虚拟机在运行


</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/f6/af833125.jpg" width="30px"><span>Vinsec</span> 👍（4） 💬（0）<div>天冷适合搞学习 打卡</div>2018-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（1）<div>docker shim 是不是可以理解成remote+CRI shim的一个k8s内部集成的一种实现</div>2019-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/59/dc9bbb21.jpg" width="30px"><span>Join</span> 👍（2） 💬（0）<div>对CRI的认识更进一层了</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（2） 💬（4）<div>Containerd 中的cri-shim和用来控制runC的containerd-shim有什么区别呢？</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/5c/416bcce6.jpg" width="30px"><span>郑然</span> 👍（2） 💬（1）<div>老师请教两个问题: 
1. 为什么kubelet要给apiserver返回redirect url呢? 这样做有什么特殊考虑吗?
2. 镜像服务, 以及下载完镜像之后, 如何和createcontainer接口发生关联的, 这块的细节能讲讲吗?</div>2018-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（0）<div>第四十四课:解读CRI与容器运行时
CRI机制能够发挥作用的核心，就在于每个容器项目现在都能自己实现一个CRI shim，自行对CRI请求进行处理。

CRI可以分为两组，第一组是RuntimeService。它提供的接口主要是跟容器相关的操作，比如创建或启动容器，删除容器，和执行exec命令等。这组的设计原则是确保这个接口本身只关注容器。第二组是ImageService，它提供的接口主要是容器镜像相关的操作，比如拉取和删除镜像等。</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（0） 💬（0）<div>CreateContainer或者RunPodSandbox吧</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/eb/80f9d212.jpg" width="30px"><span>lttzzlll</span> 👍（0） 💬（5）<div>k8s中是否可以同时存在 docker, containerd, gVisor 等不同的容器？根据label分配不同的任务。</div>2021-09-13</li><br/>
</ul>