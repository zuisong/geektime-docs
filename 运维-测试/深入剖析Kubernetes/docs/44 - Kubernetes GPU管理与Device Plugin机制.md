你好，我是张磊。今天我和你分享的主题是：Kubernetes GPU管理与Device Plugin机制。

2016年，随着 AlphaGo 的走红和TensorFlow 项目的异军突起，一场名为 AI 的技术革命迅速从学术界蔓延到了工业界，所谓的 AI 元年，就此拉开帷幕。

当然，机器学习或者说人工智能，并不是什么新鲜的概念。而这次热潮的背后，云计算服务的普及与成熟，以及算力的巨大提升，其实正是将人工智能从象牙塔带到工业界的一个重要推手。

而与之相对应的，从2016年开始，Kubernetes 社区就不断收到来自不同渠道的大量诉求，希望能够在 Kubernetes 集群上运行 TensorFlow 等机器学习框架所创建的训练（Training）和服务（Serving）任务。而这些诉求中，除了前面我为你讲解过的 Job、Operator 等离线作业管理需要用到的编排概念之外，还有一个亟待实现的功能，就是对 GPU 等硬件加速设备管理的支持。

不过， 正如同 TensorFlow 之于 Google 的战略意义一样，**GPU 支持对于 Kubernetes 项目来说，其实也有着超过技术本身的考虑**。所以，尽管在硬件加速器这个领域里，Kubernetes 上游有着不少来自 NVIDIA 和 Intel 等芯片厂商的工程师，但这个特性本身，却从一开始就是以 Google Cloud 的需求为主导来推进的。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/83/39c48a58.jpg" width="30px"><span>Eric</span> 👍（38） 💬（2）<div>单块GPU资源都不能共享，还得自己fork一份device plugin维护虚拟化的GPU。 社区有时候办事真的不利索</div>2018-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oyZfdsQL71tLcX1Eiav4NOMxa2yRSQmQNFzm7SV2aicfNkXoIN80DN2Iafpnmu2WVPBdlHylOWwElrVA8A8X71qQ/132" width="30px"><span>hlzhu1983</span> 👍（6） 💬（2）<div>张老师，问一下现在k8s关于GPU资源调度粒度是否能像CPU调度粒度那么细？现在还只能按照1块GPU卡来分配GPU资源吗？</div>2018-12-03</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（13） 💬（0）<div>Kuberentes通过Extended Resource来支持自定义资源，比如GPU。为了让调度器知道这种自定义资源在各Node上的数量，需要的Node里添加自定义资源的数量。实际上，这些信息并不需要人工去维护，所有的硬件加速设备的管理都通过Device Plugin插件来支持，也包括对该硬件的Extended Resource进行汇报的逻辑。

Device Plugin 、kubelet、调度器如何协同工作：

汇报资源： Device Plugin通过gRPC与本机kubelet连接 -&gt;  Device Plugin定期向kubelet汇报设备信息，比如GPU的数量 -&gt; kubelet 向APIServer发送的心跳中，以Extended Reousrce的方式加上这些设备信息，比如GPU的数量 

调度： Pod申明需要一个GPU -&gt; 调度器找到GPU数量满足条件的node -&gt; Pod绑定到对应的Node上 -&gt; kubelet发现需要拉起一个Pod，且该Pod需要GPU -&gt; kubelet向 Device Plugin 发起 Allocate()请求 -&gt; Device Plugin根据kubelet传递过来的需求，找到这些设备对应的设备路径和驱动目录，并返回给kubelet -&gt; kubelet将这些信息追加在创建Pod所对应的CRI请求中 -&gt; 容器创建完成之后，就会出现这个GPU设备（设备路径+驱动目录）-&gt; 调度完成
</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/94/ae0a60d8.jpg" width="30px"><span>江山未</span> 👍（8） 💬（0）<div>GPU共享及虚拟化，可以搜索一下Orion VGPU</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/88/a0/562c2626.jpg" width="30px"><span>小河</span> 👍（7） 💬（2）<div>hi，张老师，我现在将gpu的服务迁移到kubernetes上，对外提供的是gRRC接口，我使用了ingres-nginx对gRPC进行负载均衡，但是发现支持并不好，又想使用Istio以sidecar模式代理gPRC，但是又觉得太重，请问目前有什么较好的方案在kuberntes支持对gRPC的负载均衡么😀</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/0b/81ae214b.jpg" width="30px"><span>凌</span> 👍（7） 💬（1）<div>https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;NU8Cj6DL8wEKFzVYhuyzbQ</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4a/2f/42aa48d7.jpg" width="30px"><span>勇敢的心</span> 👍（4） 💬（0）<div>所以目前是无法实现多用户同时共享单块GPU咯？有没有可以实现这一功能的Magic？还有，目前可能实现GPU或者CPU数量的动态改变吗，在不重建pod的情况下？期待老师的解答</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/72/145c10db.jpg" width="30px"><span>每日都想上班</span> 👍（4） 💬（0）<div>今天爆出kubenetes安全漏洞需要升级，请问要如何升级
</div>2018-12-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/S8nYMkG2uByU9IpbAExZwLAa1no0RgKeeqjfBns0fVuBGU3GlVwia5BKujIX4648h9N2OMsyVVCLbKibje06HicvQ/132" width="30px"><span>乱愣黎</span> 👍（3） 💬（0）<div>1、device plugin只能通过patch操作来实现device信息的添加吗？能否在节点添加的时候自动添加
2、在第1点的情况下，在服务器持续集成的情况下，新旧设备device信息肯定是会不一致的，如何解决device plugin机制无法区分设备属性的情况？
    以本篇文章的内容来看，可以这么设置
    批次A使用nvidia.com&#47;GP100=4，批次B使用amd.com&#47;VEGA64=4
    这样编写资源需求和新旧设备交替都需要人为指定，这样对于运维来说很难受啊
3、是否能把GPU抽象成类似于CPU的时间片，将整个GPU计算能力池化，然后根据pod.spec.containers.resources里面的require和limits字段来分配GPU计算资源</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/c3/e545ba80.jpg" width="30px"><span>张振宇</span> 👍（1） 💬（0）<div>老师，我们的2个pod经常出现共用一张gpu卡的情况，导致性能互相影响，求解救。</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/49/e2a18264.jpg" width="30px"><span>PatHoo</span> 👍（1） 💬（0）<div>请问现在K8S支持按硬件拓扑结构调度了吗? </div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/f3/4e8fecaa.jpg" width="30px"><span>普罗@庞铮</span> 👍（1） 💬（0）<div>社区就是江湖，开源不是免费。
差异性如何体现，lol</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/00/24/6ff7cb37.jpg" width="30px"><span>硕</span> 👍（1） 💬（0）<div>刚公司需要 使用nvdia-docker 管理 gpu 用于部署ai 图像 这就来了</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/13/38fea3b3.jpg" width="30px"><span>陸思21-15-9</span> 👍（0） 💬（0）<div>看了有些cuda劫持方案，通过cuda memory computing device interface allocate </div>2024-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/47/e0/1ff26e99.jpg" width="30px"><span>gecko</span> 👍（0） 💬（0）<div>请教老师 当前是2024年 有啥比较推荐的方案吗</div>2024-11-02</li><br/><li><img src="" width="30px"><span>Geek_d573b0</span> 👍（0） 💬（0）<div>chatgpt：从您提供的博客内容和最新的Kubernetes官方文档来看，官方文档中确实有一些更新和改进，部分解决了博客中提到的Device Plugin存在的问题。以下是一些具体的分析：

1. 调度器的局限性
博客中提到的问题：

调度器只能基于“设备个数”来调度，不能处理异构设备的复杂需求。
无法在调度阶段就考虑设备的全局分布。
官方文档中的改进：

GetPreferredAllocation API：官方文档介绍了GetPreferredAllocation接口，该接口允许设备插件为设备分配提供首选集合。这虽然不完全解决调度器本身的局限性，但给设备管理器提供了更多的信息，帮助其做出更好的分配决定。
Topology Manager：文档中提到的拓扑管理器（Topology Manager）可以协调资源的拓扑对齐方式，设备插件可以返回拓扑信息（TopologyInfo），这在一定程度上解决了复杂硬件属性无法被调度器考虑的问题。
2. 缺乏设备描述的API对象
博客中提到的问题：

Kubernetes缺乏一种能够对设备进行描述的API对象，无法支持复杂的硬件属性。
官方文档中的改进：

GetAllocatableResources API：官方文档介绍了GetAllocatableResources接口，可以提供节点上所有可分配资源的信息。这包括设备的拓扑信息，NUMA节点等，增强了对设备的描述能力。
PodResourcesLister API：文档中介绍了PodResourcesLister服务，提供了关于节点上运行中的Pod和容器所消耗资源的详细信息。这可以帮助外部监控系统更好地理解和管理设备资源。
3. API 的可扩展性问题
博客中提到的问题：

Google的工程师不愿意为Allocate和ListAndWatch API添加可扩展性的参数，导致无法处理复杂的硬件设备需求。
官方文档中的改进：

DevicePluginOptions：文档中提到设备插件可以通过GetDevicePluginOptions接口返回可用的选项，这为设备插件提供了一定的扩展性。
容器运行时配置：在AllocateResponse中，设备插件可以定义容器运行时配置的修改，包括注解、设备节点、环境变量、挂载点等，这为设备插件在分配设备时提供了更多的灵活性。
4. 设备健康状态管理
博客中提到的问题：

设备故障时，无法在Pod状态中反映设备的健康状况。
官方文档中的改进：

ResourceHealthStatus：文档中提到了ResourceHealthStatus特性门控，允许在Pod的容器状态中报告分配设备的健康信息。这使得用户可以更好地理解Pod行为与设备故障之间的关联。</div>2024-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/24/3d/0682fdb9.jpg" width="30px"><span>宁建峰</span> 👍（0） 💬（0）<div>老师，有没有办法在一个pod中调度两个节点的GPU?比如说，我有两台3090*2的GPU节点，我，想创建一个pod，申请4个GPU资源，有没有办法可以实现呢？</div>2023-10-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uUwMSbicsSdrzWpnCBJKMgOpA6MzgztaqNr4w9kiciaH7wFlcsjd97cYhduMXyYicdV9r0vTTmqPReTYr6ia2S15meA/132" width="30px"><span>Geek_4acba3</span> 👍（0） 💬（0）<div>请教一下，如果根据GPU显存资源来调度有什么好办法吗？</div>2022-06-19</li><br/><li><img src="" width="30px"><span>行道者</span> 👍（0） 💬（1）<div>老师，请问如何管理多个不同k8s集群的GPU资源，业界有这样的方案吗？谢谢</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>现在的资源必然不够用,因为只能按照整数类型的分配,导致很多时候,不能共享资源
无法做到按需修改api</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>按需增加api, google把这一块完全开放出来，应该是唯一的道路</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/c6/b7448158.jpg" width="30px"><span>Tarjintor</span> 👍（0） 💬（0）<div>那么，理论上，可以做到对一个进程组的gpu使用百分比做限制吗？
之前对docker做介绍的时候，说过可以限制一个cpu所能使用的百分比</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/48/7b/bc7fcac2.jpg" width="30px"><span>Hank</span> 👍（0） 💬（1）<div>kubeflow 能否解决此事呢？    粗颗粒 转换成细粒度</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/6e/f08676bf.jpg" width="30px"><span>🔜</span> 👍（0） 💬（0）<div>[root@bigdata-k8s-master-1 ~]# curl --header &quot;Content-Type: application&#47;json-patch+json&quot; \
&gt; --request PATCH \
&gt; --data &#39;[{&quot;op&quot;: &quot;add&quot;, &quot;path&quot;: &quot;&#47;status&#47;capacity&#47;nvidia.com&#47;gpu&quot;, &quot;value&quot;: &quot;1&quot;}]&#39; \
&gt; http:&#47;&#47;localhost:8001&#47;api&#47;v1&#47;nodes&#47;k8s-master-01&#47;status
{
  &quot;kind&quot;: &quot;Status&quot;,
  &quot;apiVersion&quot;: &quot;v1&quot;,
  &quot;metadata&quot;: {

  },
  &quot;status&quot;: &quot;Failure&quot;,
  &quot;message&quot;: &quot;jsonpatch add operation does not apply: doc is missing path: &#47;status&#47;capacity&#47;nvidia.com&#47;gpu&quot;,
  &quot;code&quot;: 500

什么原因</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/84/c1/dfcad82a.jpg" width="30px"><span>Acter</span> 👍（0） 💬（0）<div>Redhat的提议或类似层面的解决方案，后面还有可能支持吗？</div>2018-12-03</li><br/>
</ul>