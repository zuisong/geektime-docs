你好，我是张磊。今天我和你分享的主题是：Kubernetes网络模型与CNI网络插件。

在上一篇文章中，我以Flannel项目为例，为你详细讲解了容器跨主机网络的两种实现方法：UDP和VXLAN。

不难看到，这些例子有一个共性，那就是用户的容器都连接在docker0网桥上。而网络插件则在宿主机上创建了一个特殊的设备（UDP模式创建的是TUN设备，VXLAN模式创建的则是VTEP设备），docker0与这个设备之间，通过IP转发（路由表）进行协作。

然后，网络插件真正要做的事情，则是通过某种方法，把不同宿主机上的特殊设备连通，从而达到容器跨主机通信的目的。

实际上，上面这个流程，也正是Kubernetes对容器网络的主要处理方法。只不过，Kubernetes是通过一个叫作CNI的接口，维护了一个单独的网桥来代替docker0。这个网桥的名字就叫作：CNI网桥，它在宿主机上的设备名称默认是：cni0。

以Flannel的VXLAN模式为例，在Kubernetes环境里，它的工作方式跟我们在上一篇文章中讲解的没有任何不同。只不过，docker0网桥被替换成了CNI网桥而已，如下所示：

![](https://static001.geekbang.org/resource/image/9f/8c/9f11d8716f6d895ff6d1c813d460488c.jpg?wh=1767%2A933)

在这里，Kubernetes为Flannel分配的子网范围是10.244.0.0/16。这个参数可以在部署的时候指定，比如：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（210） 💬（7）<div>思考题：为什么 Kubernetes 项目不自己实现容器网络，而是要通过 CNI 做一个如此简单的假设呢？

解答：没有亲历 Kubernetes 网络标准化的这个阶段，以下内容都是基于猜测，大家见笑了。
最开始我觉得这就是为了提供更多的便利选择，有了 CNI，那么只要符合规则，什么插件都可以用，用户的自由度更高，这是 Google 和 Kubernetes 开放性的体现。但转念一想，如果 Kubernetes 一开始就有官方的解决方案，恐怕也不会有什么不妥，感觉要理解的更深，得追溯到 Kubernetes 创建之初的外部环境和 Google 的开源策略了。Github 上最早的 Kubernetes 版本是 0.4，其中的网络部分，最开始官方的实现方式就是 GCE 执行 salt 脚本创建 bridge，其他环境的推荐的方案是 Flannel 和 OVS。
所以我猜测：
首先给 Kubernetes 发展的时间是不多的（Docker 已经大红大紫了，再不赶紧就一统天下了），给开发团队的时间只够专心实现编排这种最核心的功能，网络功能恰好盟友 CoreOS 的 Flannel 可以拿过来用，所以也可以认为 Flannel 就是最初 Kubernetes 的官方网络插件。Kubernetes 发展起来之后，Flannel 在有些情况下就不够用了，15 年左右社区里 Calico 和  Weave 冒了出来，基本解决了网络问题，Kubernetes 就更不需要自己花精力来做这件事了，所以推出了 CNI，来做网络插件的标准化。我觉得假如社区里网络一直没有好的解决方案的话，Kubernetes 肯定还是会亲自上阵的。
其次，Google 开源项目毕竟也不是做慈善，什么都做的面面俱到，那要消耗更多的成本，当然是越多的外部资源为我所用越好了。感觉推出核心功能，吸引开发者过来做贡献的搞法，也算是巨头们开源的一种套路吧。</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（7） 💬（1）<div>&quot;实际上，对于 Weave、Calico 这样的网络方案来说，它们的 DaemonSet 只需要挂载宿主机的 &#47;opt&#47;cni&#47;bin&#47;，就可以实现插件可执行文件的安装了。&quot;这个是用hostpath类型的卷实现吗？</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/5b/94bb1036.jpg" width="30px"><span>燕岭听涛</span> 👍（4） 💬（3）<div>老师，您好，咨询一个问题：flannel经常出现 no ip address available in range，出现后就只能重置节点。这个是什么原因造成的，为什么pod删除后不回收ip地址？或者还有别的解决办法吗？希望能收到您的回复。</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/8c/48a4d0a0.jpg" width="30px"><span>慕世勋</span> 👍（1） 💬（1）<div>请教下目前有相对成熟的k8s商业网络解决方案吗，用于大规模集群使用,主要避免雪崩造成大规模故障，你也知道，网络是个很敏感的课题</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（1） 💬（1）<div>上一章节不是说介绍flannel的hostgw模式吗？</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/36/6addd2b6.jpg" width="30px"><span>萧箫萧</span> 👍（0） 💬（1）<div>可以谈一下在pod内 请求一个域名的完整流程吗？ 比如说我最近遇到一个问题，reslove.conf这些文件内容都是正常的情况下，在某个image内为什么nslookup kuberenetes.default.svc.cluster.local 解析结果正常。
nslookup kubernetes.default 解析到外网。像这类问题如何从理论角度分析？</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/88/528442b0.jpg" width="30px"><span>Dale</span> 👍（0） 💬（1）<div>老师啥时候讲解一下calico，对比flannel网络优缺点哈</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（48） 💬（3）<div>其实本章难点在于实现网络方案对应的CNI插件，即配置Infra容器的网络栈，并连到网桥上。整体流程是：kubelet创建Pod-&gt;创建Infra容器-&gt;调用SetUpPod（）方法，该方法需要为CNI准备参数，然后调用CNI插件（flannel)为Infra配置网络；其中参数来源于1、dockershim设置的一组CNI环境变量；2、dockershim从CNI配置文件里（有flanneld启动后生成，类型为configmap）加载到的、默认插件的配置信息（network configuration)，这里对CNI插件的调用，实际是network configuration进行补充。参数准备好后，调用Flannel CNI-&gt;调用CNI bridge（所需参数即为上面：设置的CNI环境变量和补充的network configuation）来执行具体的操作流程。</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/d2/ebe20bb5.jpg" width="30px"><span>阿棠</span> 👍（44） 💬（11）<div>前几章都很好理解，一到网络这块，就蒙了，没耐心看下去了</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（28） 💬（0）<div>把握几个核心，然后串起来，其它需要的东西再去拿就可以了。
问题牵引：
网络方案是谁？它和“CNI标准”的关系（实现）是？kubernetes网络配置由谁来完成？（或者说我要怎么做才能实现它？？）

核心支撑点：
1、flannel网络方案本身
2、CNI插件，这里是内置的Flannel插件
3、dockershim(DRI)

两个背景知识：
1、CNI 的设计思想：Kubernetes 在启动 Infra 容器之后，就可以直接调用 CNI 网络插件，为这个 Infra 容器的 Network Namespace，配置符合预期的网络栈。
2、建立网络的“三类”基础组件&#47;可执行文件。

串线（着重描述三个核心点之间的串联关系）：
kubelet 创建 Pod -&gt;创建 Infra 容器。主要是由（CRI）**dockershim **调用 Docker API 创建并启动 Infra 容器-&gt; SetUpPod方法。方法的作用是：1.为 CNI 插件准备参数，2.然后调用 CNI 插件为 Infra 容器配置网络。
1.所需参数-&gt;实现ADD&#47;DEL方法-&gt;CNI插件（*flannel插件*)实现。：
1.1参数一：由 dockershim 设置的一组 CNI 环境变量，ADD&#47;DEL方法参数。
1.2参数二：是 dockershim 从 CNI “配置文件”里加载到的、默认插件的配置信息；由*flannel网络方案本身*安装时生成。
2.调用 CNI 插件:
引：&quot;dockershim 对 *Flannel CNI 插件*的调用，其实就是走了个过场。Flannel CNI 插件唯一需要做的，就是对 dockershim 传来的 Network Configuration (CNI配置文件）进行补充。&quot;
接下来，Flannel CNI 插件-&gt;调用 CNI bridge 插件(参数一：“CNI环境变量&#47;ADD&quot;, 参数二：”Network Confiuration&#47;Delegate&quot;)，--&gt;“代表”Flannel，将容器加入CNI网络（cni0网桥）。</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/20/10/5786e0d8.jpg" width="30px"><span>bus801</span> 👍（13） 💬（1）<div>要是再来一篇calico的就完美了</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/9d/5839e490.jpg" width="30px"><span>LÉON</span> 👍（12） 💬（2）<div>一直在苦苦自学，在容器的存储还有网络一直困扰。一直在拜读不拜听 受益匪浅 继续努力</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/88/528442b0.jpg" width="30px"><span>Dale</span> 👍（10） 💬（0）<div>我认为是在大规模的集群环境中，网络方案是最复杂的，针对不同的的环境和场景，网络需要灵活配置。k8s集群里只关心最终网络可以连通，而不需要在内部去实现各种复杂的网络模块，使用CNI可以方便灵活地自定义网络插件，网络可以独立。</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/fc/e56c9c4a.jpg" width="30px"><span>A7kou</span> 👍（4） 💬（0）<div>https:&#47;&#47;github.com&#47;y805939188&#47;k8s-cni-test
从 0 实现的简单 cni 插件，内附教学，感兴趣的同学可以瞅瞅</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/b4/7f1e7e20.jpg" width="30px"><span>毛玉明</span> 👍（4） 💬（3）<div>k8s里可以不使用cni直接使用docker0的网桥吗，看了下目前公司的集群没有找到cni0的这个设备</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/01/96/afcb6174.jpg" width="30px"><span>冬冬</span> 👍（3） 💬（0）<div>kubernetes使用cni作为pod的容器间通信的网桥（与docker0功能相同）
初始化pod网络流程：创建Infra容器 调用cni插件初始化infra容器网络（插件位置：&#47;opt&#47;cni&#47;bin&#47;flannel），开始 dockershim 设置的一组 CNI 环境变量（枚举值ADD、DELETE），用于表示将容器的VethPair插入或从cni0网桥移除。
与此同时，cni bridge插件检查cni网桥在宿主机上是否存在，若不存在则进行创建。接着，cni bridge插件在network namespace创建VethPair，将其中一端插入到宿主机的cni0网桥，另一端直接赋予容器实例eth0，cni插件把容器ip提供给dockershim 被kubelet用于添加到pod的status字段。接下来，cni bridge调用cni ipam插件 从ipam.subnet子网中给容器eth0网卡分配ip地址 同时设置default route配置，最后cni bridge插件为cni网桥设置ip地址。</div>2020-08-19</li><br/><li><img src="" width="30px"><span>vincent</span> 👍（3） 💬（1）<div>Kubernetes是否可以给Pod创建多张网卡，分配多个IP？</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/92/14/6ca50b3b.jpg" width="30px"><span>大G来了呦</span> 👍（2） 💬（0）<div>存储和网络需要好好吸收才行</div>2020-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（0）<div>精彩！老师不但教知其然，而且完全详细的讲解所以然。谢谢。学习了。</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（2） 💬（1）<div>因为现实中的容器网络太多样、太复杂，为了解耦、可扩展性，设计了CNI接口，这个接口实现了共同的功能：为infra容器的network namespace配置网络栈</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/51/82/2e4e0ad4.jpg" width="30px"><span>其玄</span> 👍（1） 💬（0）<div>插件CNI的作用：1、把容器以 Veth Pair 的方式“插”到 CNI 网桥上；2、CNI bridge 插件调用 CNI ipam 插件，从 ipam.subnet 字段规定的网段里为容器分配一个可用的 IP 地址。然后，CNI bridge 插件就会把这个 IP 地址添加在容器的 eth0 网卡上，同时为容器设置默认路由。

这样就让容器和宿主机可以互通</div>2023-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c1/4c/e72d3360.jpg" width="30px"><span>NulI</span> 👍（1） 💬（1）<div>两款比较实用的CNI插件，可以试试：
（1）轻量级kube-ipam帮你轻松实现K8S容器的IP地址永久固定不变   https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;JLEPko0dN0f7bdmCwvuljA
（2）基于Multus与Kube-ipam实现Web和数据库分层网络安全访问  https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;8x8B_qhK4Y1JlkXkYpD6ng</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>K8S 太强了  比虚拟机解决方案 先进了很多   用更少的存储 做更多的事情</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（0）<div>所有容器都可以直接使用 IP 地址与其他容器通信，而无需使用 NAT。所有宿主机都可以直接使用 IP 地址与所有容器通信，而无需使用 NAT。反之亦然。容器自己“看到”的自己的 IP 地址，和别人（宿主机或者容器）看到的地址是完全一样的。</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/8c/c86340ca.jpg" width="30px"><span>巴西</span> 👍（1） 💬（0）<div>网络篇确实难度上来了,需要多看几遍</div>2020-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/00/d3/ef5d2af0.jpg" width="30px"><span>Geek_81c7c9</span> 👍（1） 💬（0）<div>老师你好，请问在CNI方案出现之前，有其它的容器固定IP方案吗？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/1c/d7/a53dad9e.jpg" width="30px"><span>叫我天才好了</span> 👍（1） 💬（0）<div>思考题，高内聚，低耦合？
</div>2019-12-04</li><br/><li><img src="" width="30px"><span>Geek_8b926a</span> 👍（0） 💬（0）<div>在非常大的集群中，flannel和calico就显得性能不足，存在瓶颈问题。以上几章也介绍了架构都是基于flannel网桥去做的，从网络架构来看多了一层损耗。因为我司的网络插件是自研的，故学习了常见的网络插件作对比。总结如下。开源这种在小规模，网络环境简单使用较好，学习成本低。维护成本低，但是健壮性一般。 我司自研的网络插件基于二层网络实现，也是遵循的cni这种模式。其依赖于基础设施网络，因为容器网络层是“直达”的，不存在像flannel还需要中间再转发一层以及维护路由表关系。我司的容器网络直接底层打通，路由关系不需要在集群层面维护。这样优点是容器层面直接可以点对点进行访问，中间过一个容器网网关转发，性能上非常优越，但是容器网络配置不灵活，必须遵照基础网络架构（物理层面）进行容器网络配置。</div>2023-05-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/z4hFFGreQKeXzVG5eiaFuuWcMd6pibDdQwdNT5S29Eg92WjGgKBY8LRhvrGNqJwHsysWHMW4emiaEAKWKs4OoibPicQ/132" width="30px"><span>strive</span> 👍（0） 💬（0）<div>醍醐灌顶式的讲解，NB</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>老师，这段话能再解释一下吗？没有理解这里面的逻辑，既然都可以拿到而且也必须拿到，为什么还要在乎顺序呢？

“这个设计其实很容易理解。在编程时，容器的 Namespace 是可以直接通过 Namespace 文件拿到的；而 Host Namespace，则是一个隐含在上下文的参数。所以，像上面这样，先通过容器 Namespace 进入容器里面，然后再反向操作 Host Namespace，对于编程来说要更加方便。”</div>2023-01-08</li><br/>
</ul>