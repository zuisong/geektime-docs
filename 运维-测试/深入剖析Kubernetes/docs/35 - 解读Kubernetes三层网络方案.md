你好，我是张磊。今天我和你分享的主题是：解读Kubernetes三层网络方案。

在上一篇文章中，我以网桥类型的Flannel插件为例，为你讲解了Kubernetes里容器网络和CNI插件的主要工作原理。不过，除了这种模式之外，还有一种纯三层（Pure Layer 3）网络方案非常值得你注意。其中的典型例子，莫过于Flannel的host-gw模式和Calico项目了。

我们先来看一下Flannel的host-gw模式。

它的工作原理非常简单，我用一张图就可以和你说清楚。为了方便叙述，接下来我会称这张图为“host-gw示意图”。

![](https://static001.geekbang.org/resource/image/3d/25/3d8b08411eeb49be2658eb4352206d25.png?wh=2880%2A1528 "图1 Flannel host-gw示意图")

假设现在，Node 1上的Infra-container-1，要访问Node 2上的Infra-container-2。

当你设置Flannel使用host-gw模式之后，flanneld会在宿主机上创建这样一条规则，以Node 1为例：

```
$ ip route
...
10.244.1.0/24 via 10.168.0.3 dev eth0
```

这条路由规则的含义是：目的IP地址属于10.244.1.0/24网段的IP包，应该经过本机的eth0设备发出去（即：dev eth0）；并且，它下一跳地址（next-hop）是10.168.0.3（即：via 10.168.0.3）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/55/86/ca7c94ce.jpg" width="30px"><span>羁绊12221</span> 👍（8） 💬（1）<div>老师好，flannel UDP 隧道封装的是IP包，vxlan封装的是 二层帧，Calico IPIP模式封装的也是IP包。。感觉上使用隧道通信封装IP报文就够了吧？封装二层帧有什么考虑吗？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/6e/f3cfebc5.jpg" width="30px"><span>峰哥</span> 👍（5） 💬（1）<div>老师好，有个1.4的K8S集群，sprincloud的微服务，怎么升级到1.10，是生产环境，有什么好的办法，谢谢
</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/44/ebfe7b27.jpg" width="30px"><span>davad_dee</span> 👍（2） 💬（3）<div>图 1 Flannel host-gw 示意图  第一个路由表中第三条路由 src 192.168.0.2 是否应该是 10.168.0.2</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/f0/8b1c5ae9.jpg" width="30px"><span>.</span> 👍（2） 💬（1）<div>请问，如果是想要静态ip，是不是只能选择calico方案，flannel不行</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（2） 💬（1）<div>请问张老师，calico、flannel、Weave、romana 等网络插件，有没有比较权威的性能对比数据？和 bare metal 比起来，性能损耗差距有多大呢？网上搜了一圈，说什么的都有，是不是三层的方案大概都是 10% 左右的 overhead 的呢？</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（0） 💬（1）<div>BGP 这种，会不会导致路由表很大</div>2019-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（162） 💬（3）<div>写了两篇文档：
Docker单机网络模型动手实验 https:&#47;&#47;github.com&#47;mz1999&#47;blog&#47;blob&#47;master&#47;docs&#47;docker-network-bridge.md
Docker跨主机Overlay网络动手实验 https:&#47;&#47;github.com&#47;mz1999&#47;blog&#47;blob&#47;master&#47;docs&#47;docker-overlay-networks.md
通过动手实验加深理解容器网络。分享出来希望对小伙伴有所帮助。

看来学完了这篇，可以再写一个Docker跨主机路由方案动手实验</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（126） 💬（2）<div>三层和隧道的异同：
相同之处是都实现了跨主机容器的三层互通，而且都是通过对目的 MAC 地址的操作来实现的；不同之处是三层通过配置下一条主机的路由规则来实现互通，隧道则是通过通过在 IP 包外再封装一层 MAC 包头来实现。
三层的优点：少了封包和解包的过程，性能肯定是更高的。
三层的缺点：需要自己想办法维护路由规则。
隧道的优点：简单，原因是大部分工作都是由 Linux 内核的模块实现了，应用层面工作量较少。
隧道的缺点：主要的问题就是性能低。</div>2018-11-12</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（56） 💬（0）<div>Kubernetes通过一个叫做CNI的接口，维护了一个单独的网桥来代替docker0。这个网桥的名字就叫作：CNI网桥，它在宿主机上的设备名称默认是：cni0。

容器“跨主通信”的三种主流实现方法：UDP、host-gw、VXLAN。 之前介绍了UDP和VXLAN，它们都属于隧道模式，需要封装和解封装。接下来介绍一种纯三层网络方案，host-gw模式和Calico项目

Host-gw模式通过在宿主机上添加一个路由规则： 

    &lt;目的容器IP地址段&gt; via &lt;网关的IP地址&gt; dev eth0

IP包在封装成帧发出去的时候，会使用路由表里的“下一跳”来设置目的MAC地址。这样，它就会通过二层网络到达目的宿主机。
这个三层网络方案得以正常工作的核心，是为每个容器的IP地址，找到它所对应的，“下一跳”的网关。所以说，Flannel host-gw模式必须要求集群宿主机之间是二层连通的，如果宿主机分布在了不同的VLAN里（三层连通），由于需要经过的中间的路由器不一定有相关的路由配置（出于安全考虑，公有云环境下，宿主机之间的网关，肯定不会允许用户进行干预和设置），部分节点就无法找到容器IP的“下一条”网关了，host-gw就无法工作了。

Calico项目提供的网络解决方案，与Flannel的host-gw模式几乎一样，也会在宿主机上添加一个路由规则：

    &lt;目的容器IP地址段&gt; via &lt;网关的IP地址&gt; dev eth0

其中，网关的IP地址，正是目的容器所在宿主机的IP地址，而正如前面所述，这个三层网络方案得以正常工作的核心，是为每个容器的IP地址，找到它所对应的，“下一跳”的网关。区别是如何维护路由信息：
Host-gw :  Flannel通过Etcd和宿主机上的flanneld来维护路由信息
Calico: 通过BGP（边界网关协议）来实现路由自治，所谓BGP，就是在大规模网络中实现节点路由信息共享的一种协议。

隧道技术（需要封装包和解包，因为需要伪装成宿主机的IP包，需要三层链通）：Flannel UDP &#47; VXLAN  &#47; Calico IPIP
三层网络（不需要封包和解封包，需要二层链通）：Flannel host-gw &#47; Calico 普通模式
</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/e7/47429b6c.jpg" width="30px"><span>米开朗基杨</span> 👍（28） 💬（3）<div>写了篇关于calico开启反射路由模式的文章，希望对大家有所帮助：https:&#47;&#47;www.yangcs.net&#47;posts&#47;calico-rr&#47;</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（11） 💬（0）<div>三层网络优点： 不需要封包、拆包，传输效率会更高；可以设置复杂的网络策略。
隧道模式优点： 不需要在主机间的网关中维护容器路由信息，只需要主机有三层网络的连通性即可。</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（9） 💬（2）<div>所以三层可达，二层不可达的k8s集群不能使用Flannel host-gw模式，只能使用其他模式？</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/47/8da914be.jpg" width="30px"><span>Geek_1264yp</span> 👍（8） 💬（7）<div>老师你好，问个小白问题，怎么判断集群里的宿主机是否二层互通，或者说怎么实现二层互通？</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ef/2a/e9c5c163.jpg" width="30px"><span>小江哥哥</span> 👍（7） 💬（1）<div>对于二层联通的网络：
可以选择flannel的host-gw或者calico（非ipip模式），将宿主机当作网关，进行直接跳转，区别为calico自己封装了一个组件（BIRD）存储并维护路由关系，flannel维护并借助K8S的etcd存储路由关系。

对于多个vlan的网络：
flannel的vxlan和calico的ipip模式都可以选择，它们都通过内核模块进行了一次封包和解包过程，有内核态到用户态的切换，效率损耗较大（20%-30%）。不同点在于，calico拥有‘重型武器’BGP，可以通过它与宿主机的网关交换，共同维护路由关系，实现伪二层直连，方便自定义网络架构，定制程度比flannel高。

其他区别：
1. flannel的所有模式都使用了cni的网桥模式，不用在宿主机上维护这么多设备对的映射关系，calico则相反。
2. 所有网络IP规划分配，路由规则存储维护calico都大包大揽，通过BGP，等组件维护，flannel的路由存储和维护需要依赖K8s的etcd，且会与apiserver交互。
3. 在大规模集群中。对于路由规则的跟踪维护，calico有自己的中心化方案（Route Reflector模式），避免了路由信息指数级增长。
4. 在非二层直连网络中，calico支持通过与宿主机网关的互动（BGP协议），组成三层网络，避免了使用ipip封包解包，提高网络性能，这点上比flannel定制化程度更高。</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（7） 💬（0）<div>三层网络方案简单易懂，开销小，缺点是需要物理互联，连接节点有限；
隧道协议更通用，可以打通不同网段，但是开销大，协议复杂，难排错；</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/72/145c10db.jpg" width="30px"><span>每日都想上班</span> 👍（7） 💬（0）<div>架设k8s集群后，对操作系统及网络知识有了一个很好的复习，感谢大神</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/32/c2/ffa6c819.jpg" width="30px"><span>冰冻柠檬</span> 👍（5） 💬（0）<div>听老师的讲解真是太过瘾了！！</div>2020-07-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ZwGweFhVUTfOrrYRk6Dic1IBxFyj2ZgsI1UXQeic2B5uJFdjicsIicnKrJts9v7nGUTCQlSKNUpmvYULq5KjqWjU4g/132" width="30px"><span>freeman</span> 👍（4） 💬（0）<div>老师，能介绍一下Cilium吗</div>2018-11-13</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（3） 💬（2）<div>有个疑问，为什么叫 “三层”网络方案呢？


</div>2020-11-25</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（3） 💬（4）<div>有一个疑问 ，Calico IPIP模式下。IPIP封包前后，IP Header里面的目的IP都是“192.168.2.2”。那为什么封包前不能从Node1发送到Node2 ？</div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a3/ce/12f9d2ae.jpg" width="30px"><span>朱升平</span> 👍（3） 💬（0）<div>网络是短板，得多学习学习！</div>2018-11-12</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（2） 💬（1）<div>隧道技术（需要封装包和解包，因为需要伪装成宿主机的IP包，需要三层链通）：Flannel UDP &#47; VXLAN  &#47; Calico IPIP
三层网络（不需要封包和解封包，需要二层链通）：Flannel host-gw &#47; Calico </div>2020-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（2） 💬（2）<div>三层网络方案和“隧道模式”的异同，以及各自的优缺点：三层网络方案要求宿主机二层连通，隧道模式不要求宿主机二层连通；三层网路方案没有封包和解包，性能上比隧道模式要好。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/72/145c10db.jpg" width="30px"><span>每日都想上班</span> 👍（2） 💬（1）<div>碰到一个奇怪的问题，集群中一台master节点重启后，发现docker images 镜像都被清空了一样，然后我重新pull过来，过一会又没有了，这个是哪里问题呢？</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/ee/6bbac848.jpg" width="30px"><span>再见孙悟空</span> 👍（2） 💬（0）<div>凌晨在追，感觉像追剧！嘻嘻</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（1） 💬（0）<div>目的都是将数据包送至宿主机，不同点是隧道模式是通过将数据包封装在宿主机的udp报文内，交由对端对应的服务解封包，三层网络模式是通过配置路由的下一跳来实现，即使是通过ipip隧道也只是多封装了一层ip头，解包后也是直接进入内核网络协议栈，通过路由规则路由到目标容器。</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/70/4e7751f3.jpg" width="30px"><span>超级芒果冰</span> 👍（1） 💬（1）<div>有一个疑问，在BGP这块内容中，有一段这样的描述
“AS 1 里面的主机 10.10.0.2，要访问 AS 2 里面的主机 172.17.0.3 的话。它发出的 IP 包，就会先到达自治系统 AS 1 上的路由器 Router 1。Router 1 的路由表里，有这样一条规则，即：目的地址是 172.17.0.2 包，应该经过 Router 1 的 C 接口，发往网关 Router 2。所以 IP 包就会到达 Router 2 上，然后经过 Router 2 的路由表，从 B 接口出来到达目的主机 172.17.0.3”
描述中ip包的目的地址是172.17.0.3，而Router 1 的路由表规则是目的地址是 172.17.0.2 包，应该经过 Router 1 的 C 接口，这里该怎么理解？</div>2022-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（1） 💬（1）<div>calico：
通过veth pair路由规则，实现直接在二层网络通信；对不同子网的三层网络通信，使用ipip来再次封装一次ip包，实现外部的寻址。
flannel vxlan:
它在三层网络外层，又做了一次二层链路寻址（避免tun0的用户态到内核态的切换开销）;
mac地址是各个flannel.1的地址，flannel.1所在主机地址，都可以由flannel进程从etcd中获取到。

张老师，这两种方式性能差别在什么地方啊？谢谢！！</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/76/1f/e7cd0190.jpg" width="30px"><span>M</span> 👍（1） 💬（5）<div>二层可达和三层可达的区别是什么，不都需要ip地址和mac地址才能通信吗</div>2020-10-22</li><br/><li><img src="" width="30px"><span>0.7</span> 👍（1） 💬（2）<div>公有云的vpc算纯二层吗？可以使用host-gw吗？我试了下，没搞通。</div>2020-05-08</li><br/>
</ul>