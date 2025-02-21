上一节我们讲了容器网络的模型，以及如何通过NAT的方式与物理网络进行互通。

每一台物理机上面安装好了Docker以后，都会默认分配一个172.17.0.0/16的网段。一台机器上新创建的第一个容器，一般都会给172.17.0.2这个地址，当然一台机器这样玩玩倒也没啥问题。但是容器里面是要部署应用的，就像上一节讲过的一样，它既然是集装箱，里面就需要装载货物。

如果这个应用是比较传统的单体应用，自己就一个进程，所有的代码逻辑都在这个进程里面，上面的模式没有任何问题，只要通过NAT就能访问进来。

但是因为无法解决快速迭代和高并发的问题，单体应用越来越跟不上时代发展的需要了。

你可以回想一下，无论是各种网络直播平台，还是共享单车，是不是都是很短时间内就要积累大量用户，否则就会错过风口。所以应用需要在很短的时间内快速迭代，不断调整，满足用户体验；还要在很短的时间内，具有支撑高并发请求的能力。

单体应用作为个人英雄主义的时代已经过去了。如果所有的代码都在一个工程里面，开发的时候必然存在大量冲突，上线的时候，需要开大会进行协调，一个月上线一次就很不错了。而且所有的流量都让一个进程扛，怎么也扛不住啊！

没办法，一个字：拆！拆开了，每个子模块独自变化，减少相互影响。拆开了，原来一个进程扛流量，现在多个进程一起扛。所以，微服务就是从个人英雄主义，变成集团军作战。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/11/e8506a04.jpg" width="30px"><span>小宇宙</span> 👍（47） 💬（5）<div>flannel的backend除了UDP和vxlan还有一种模式就是host-gw，通过主机路由的方式，将请求发送到容器外部的应用，但是有个约束就是宿主机要和其他物理机在同一个vlan或者局域网中，这种模式不需要封包和解包，因此更加高效。</div>2018-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（17） 💬（1）<div>回答自己提的udp丢包的问题，希望老师帮忙看看是否正确。
flannel实际上是将docker出来的包再加udp封装，以支持二层网络在三层网络中传输。udp确实可能丢包，丢包是发生在flannel层上，丢包后内层的docker（如果被封装的是tcp）无ack,源docker的虚拟网卡还会按tcp协议进行重发。无非是按flannel原理多来几次。</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/85/ed/905b052f.jpg" width="30px"><span>超超</span> 👍（4） 💬（1）<div>回答问题1：是不是在dockerX网卡上做NAT？</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/ae/c082bb25.jpg" width="30px"><span>大星星</span> 👍（3） 💬（1）<div>想问下老师，后一种使用VTEP，为什么flannel.id里面内部源地址配置的是flannel.id的mac地址，而不是使用第一种打开dev&#47;net&#47;tun时候源地址写的是容器A的源地址。
为什么两种情况下不一样了，谢谢</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a1/3a/9e48ce31.jpg" width="30px"><span>小宇</span> 👍（3） 💬（1）<div>老师好，我这里有一个疑问，第28讲的VXLAN，虚拟机通信时包的结构， VTEP的设备ip为什么在VXLAN头之外，我的理解VTEP设备的ip应该和flannel的VXLAN模式一样，在VXLAN头里面。
</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3a/e1/b6b311cb.jpg" width="30px"><span>╯梦深处゛</span> 👍（2） 💬（1）<div>对于 IP 冲突的问题，如果每一个物理机都是网段 172.17.0.0&#47;16，肯定会冲突啊，但是这个网段实在太大了，一台物理机上根本启动不了这么多的容器，所以能不能每台物理机在这个大网段里面，抠出一个小的网段，每个物理机网段都不同，自己看好自己的一亩三分地，谁也不和谁冲突。
-----------------------------------------------------------------------------------------------------
老师，不同节点之间不一定都是不同网段的，相反很多时候，一个K8S集群的所有节点都是在一个网段，请问在这种场景下，如果避免这种冲突的问题呢？
</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/94/d4499319.jpg" width="30px"><span>allwmh</span> 👍（1） 💬（1）<div>flannel怎么做容器的IP保持呢？</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/1a/20977779.jpg" width="30px"><span>峻铭</span> 👍（0） 💬（1）<div>如物理机A坏了，docker要迁移到C上去，物理机B内容器中的应用如何和C中的通信</div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（11） 💬（0）<div>1 快速迭代，单体应用不能满足快速迭代和高并发的要求，所以需要拆成微服务，容器作为集装箱，可以保证应用在不同的环境快速迁移，还需要一个容器的调度平台，可以将容器快速的调度到任意服务器，这个调度平台就是k8s。2 微服务之间存在服务调用的问题，就像集团军作战，需要解决各个部队位置和部队之间通讯的问题，2.1 位置问题用注册中心，但是可能会有ip端口冲突，Flannel是为了解决这种问题的技术，给每个物理机分配一小段网络段，每个物理机的容器只使用属于自己的网络段，2.2 部队之间通讯 容器网络互相访问，Flannel使用UDP实现Overlay网络，每台物理机上都跑一个flannelid进程，打开dev&#47;net&#47;tun设备的时候，就会有这个网卡，所有发到flannel.1的网络包，都会被flannelid进程截获，会讲网络包封装进udp包，发到b的flannel.1，b的flannelid收到网络包以后，解开，由flannel.1发出去，通过dock0给到容器b。通讯比较慢，Flannel使用VXLAN技术，建立一个VXLAN的VTEP，通过netlink通知内核建立一个VTEP的网卡flannel.1，A物理机上的flannel.1就是vxlan的vtep，将网络包封装，通过vxlan将包转到另一台服务器上，b的flannel.1接收到，解包，变成内部的网络包，通过物理机上的路由转发到docker0，然后转发到容器B里面，通信成功。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/5b/983408b9.jpg" width="30px"><span>悟空聊架构</span> 👍（6） 💬（0）<div>“例如物理机 A 是网段 172.17.8.0&#47;24，物理机 B 是网段 172.17.9.0&#47;24”，这里应该是指物理机A给docker分配的网段吧？老师，这个容易造成误解哦……</div>2018-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/6e/85512d27.jpg" width="30px"><span>刘工的一号马由</span> 👍（6） 💬（0）<div>1默认路由发到容器网络的网关
2underlay网络</div>2018-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/ee/f5c5e191.jpg" width="30px"><span>LYy</span> 👍（2） 💬（1）<div>Flannel原理总结:
1. 网络打平: 主机间独立虚拟网段，不使用NAT(存在IP&#47;端口冲突问题);
2. 网络互通: 通过Overlay(基于UDP or VXLAN)，配合虚拟网段、路由表实现；
3. E2E:
  a) Overlay via UDP: 
  容器A虚IP -{路由表}-&gt; 容器eth0(基于veth pair) -&gt; docker0(基于veth pair) -{路由表}-&gt; flannel.1网卡(打开&#47;dev&#47;net&#47;tun字符设备) -&gt; flanneld读取 -&gt; flanneld进行UDP封包 -&gt; Node1 eth0 -&gt; Node2 eth0 -&gt; flanneld进行UDP解包 -&gt; flannel.1网卡 -&gt; docker0 -&gt; 容器eth0 -&gt; 容器B虚IP
  b) VXLAN: 
  容器A虚IP -{路由表}-&gt; 容器eth0(基于veth pair) -&gt; docker0(基于veth pair) -{路由表}-&gt; flannel.1网卡(创建VTEP网卡) -&gt; flannel.1进行VXLAN封包 -&gt; Node1 eth0 -&gt; Node2 eth0 -&gt; flannel.1进行VXLAN解包 -&gt; flannel.1网卡 -&gt; docker0 -&gt; 容器B虚IP
4. flanneld职责:
  a) Overlay via UDP:
      - 维护Node间网络规划信息
      - 创建veth pair?(存疑)
      - 配置路由规则
      - 创建flannel.1网卡(通过打开&#47;dev&#47;net&#47;tun字符设备)
      - 读取flannel.1网络流量，进行UDP封包&#47;解包
  b) VXLAN
      - 维护Node间网络规划信息
      - 创建veth pair?(存疑)
      - 配置路由规则(应该除了网段还有各Node flannel.1的MAC信息)
      - 创建flannel.1网卡(创建VTEP网卡, 基于netlink)
5. 封包结构:
  a) UDP封包: Node eth0 MAC头|Node IP头|UDP头(flanneld port)|容器IP头|Payload
  b) VXLAN封包: Node eth0 MAC头|Node IP头|UDP头(?port)|VXLAN头|flannel.1 MAC头|容器IP头|Payload

flannel方案简析:
1) Overlay via UDP基于用户态处理网络流量，性能较差;
2) 数据面与控制面未分析, 规模增长后可能存在管理问题。</div>2023-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rurTzy9obgda82kG3FTrszfzuIRQH2Mljc36u9KZLnOcJEtjY1NqdEROjpkLZia8Lu97OKhoIIicHu4xoiclHpOAA/132" width="30px"><span>Geek_536b07</span> 👍（2） 💬（0）<div>容器网络，讲的的太模糊了，容器集群注册的一般是podip，一般都会遇到跨集群访问的问题，这才是开发人员要去解决的重点</div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（2） 💬（0）<div>#  tcpdump -i eth0 dst 192.168.1.7 -w  dst.pcap
抓了下 vxlan 类型的 flannel 容器间的包，确实是 udp 的封包，但是没有看到 vxlan 的信息，不知道这要怎么看？
Frame 3: 201 bytes on wire (1608 bits), 201 bytes captured (1608 bits)
Ethernet II, Src: fa:16:3e:08:a8:46 (fa:16:3e:08:a8:46), Dst: fa:16:3e:5a:de:91 (fa:16:3e:5a:de:91)
Internet Protocol Version 4, Src: 192.168.1.4, Dst: 192.168.1.7
User Datagram Protocol, Src Port: 54228, Dst Port: 8472
Data (159 bytes)</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/60/f21b2164.jpg" width="30px"><span>jacy</span> 👍（2） 💬（1）<div>udp丢包能接受吗</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/46/26/fa3bb8e6.jpg" width="30px"><span>⊙▽⊙</span> 👍（2） 💬（0）<div>老师我想问下，如何知道容器宿主机的地址，这样才可以在对数据包进行二次封装的时候把目的地址填写进去</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/10/78/29bd3f1e.jpg" width="30px"><span>王子瑞Aliloke有事电联</span> 👍（1） 💬（1）<div>老刘讲的太好了！！！这个专栏超值，开眼界了，而且讲的通俗易懂-虽然还有很多知识我没有懂，但开眼界了。</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>vxlan要通过组播来实现广播，k8s有完整的集群信息，flannel是不是可以不用组播也能实现arp的解析？</div>2022-08-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rurTzy9obgda82kG3FTrszfzuIRQH2Mljc36u9KZLnOcJEtjY1NqdEROjpkLZia8Lu97OKhoIIicHu4xoiclHpOAA/132" width="30px"><span>Geek_536b07</span> 👍（0） 💬（0）<div>容器网络主流应该是k8s的网络实现，涉及到namespace 如果做pod内容器网络共享，如何通过svc访问pod，sts如何固定dns，没有结合k8s单独把网络插件拎出来讲，就很懵逼</div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/23/e8/9f445339.jpg" width="30px"><span>章潘</span> 👍（0） 💬（0）<div>ip，mac，vlan，vxlan等等都可以理解为对网络数据或者资源的标记。从这个角度出发，容器中的IP或端口冲突问题，是因为在同一个域用了相同的标签。所以要解决冲突问题，方式就太多了。选择不同的网段是方式之一。</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/73/01eafd3c.jpg" width="30px"><span>singularity of space time</span> 👍（0） 💬（0）<div>老师您好
在原文的表述中“物理机 B 上的 flanneld 收到包之后，解开 UDP 的包，将里面的网络包拿出来，从物理机 B 的 flannel.1 网卡发出去”
这里写“发出去”感觉并不恰当，它应该是写入&#47;dev&#47;net&#47;tun设备，然后被flannel.1网卡接收到，再进入宿主机协议栈，然后经过路由发往docker0网卡，从docker0网卡中出去进入网关，再得到容器内部
</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/83/93d389ba.jpg" width="30px"><span>我是谁</span> 👍（0） 💬（0）<div>老师好，有个问题。
28讲的时候，vxlan报文的外层ip和外层mac地址都是vtep设备的，但是这讲提到的flannel的vxlan方案中，外层ip和外层mac地址都是宿主机的，vtep设备的mac地址反而放在里内层，这是一个问题。另一个问题是内层mac地址不应该是虚拟机的吗？</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/f9/b2fe7b63.jpg" width="30px"><span>King-ZJ</span> 👍（0） 💬（0）<div>在容器真实运用在实际环境中时，必须考虑通信的问题，运用flannel网络方案来解决问题，一个是UDP的用户态方案，一个是VXLAN内核态的方案，VXLAN方案在实际的使用中更常见。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（0） 💬（0）<div>VXLAN 模式的 VTEP 相较于 &#47;dev&#47;net&#47;tun 字符设备网卡，性能改善是在 VTEP 通信比字符设备网卡通信少了内核态用户态间的数据拷贝？</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/5a/2ed0cdec.jpg" width="30px"><span>donson</span> 👍（0） 💬（0）<div>flannel网络的地址段是10.242.0.0&#47;16，默认每个Node上的子网划分是10.242.x.0&#47;24，请问这个子网划分在哪里可以配置，比如我想划分成&#47;21</div>2018-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/ae/2b8192e8.jpg" width="30px"><span>selboo</span> 👍（0） 💬（0）<div>物理机A和物理机B是以access模式连接到交换机。此时flannel.1 在加上 VXLAN 头可以通信吗？？？求老师解答。</div>2018-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（0） 💬（0）<div>1.容器访问外面还是应该用nat
2.使用bgp协议的其他实现 calico kube-router</div>2018-07-25</li><br/>
</ul>