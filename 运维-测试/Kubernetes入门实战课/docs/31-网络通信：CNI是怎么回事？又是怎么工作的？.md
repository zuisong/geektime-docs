你好，我是Chrono。

到现在，我们对Kubernetes已经非常熟悉了，它是一个集群操作系统，能够管理大量计算节点和运行在里面的应用。不过，还有一个很重要的基础知识我们还没有学习，那就是“网络通信”。

早在“入门篇”的[第6讲](https://time.geekbang.org/column/article/528692)里，我们就简单介绍过Docker的网络模式，然后在“中级篇”的[第17讲](https://time.geekbang.org/column/article/534762)，我们又为Kubernetes安装了一个网络插件Flannel。这些都与网络相关，但也只是浅尝辄止，并没有太多深究。

如果你是一个喜欢刨根问底的人，会不会很好奇：Flannel到底是如何工作的呢？它为什么能够让Kubernetes集群正常通信呢？还有没有其他网络插件呢？

今天我们就来聊一下这个话题，讲讲Kubernetes的网络接口标准CNI，以及Calico、Cilium等性能更好的网络插件。

## Kubernetes的网络模型

在学习Kubernetes的网络之前，我们还是要先简单回顾一下Docker的网络知识。

你对Docker的null、host和bridge三种网络模式还有印象吗？这里我重新画了一张图，描述了Docker里最常用的bridge网络模式：

![图片](https://static001.geekbang.org/resource/image/0b/85/0b7954a362b9e04db8b588fbed5b7185.jpg?wh=1920x1148)

Docker会创建一个名字叫“docker0”的网桥，默认是私有网段“172.17.0.0/16”。每个容器都会创建一个虚拟网卡对（veth pair），两个虚拟网卡分别“插”在容器和网桥上，这样容器之间就可以互联互通了。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/65/d6/20670fd5.jpg" width="30px"><span>Obscure</span> 👍（7） 💬（3）<div>网络基础不行，这一节内容基本看不懂。。。咋整。。。</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（6） 💬（1）<div>试着思考了一下：
1，定义规范&#47;标准，也就是接口（interface），把具体实现&#47;扩展交给社区&#47;第三方，然后使用插件（addon）的方式在 Kubernets 里应用，这真是个省力的方式！不需要去关注千变万化的底层运行环境。

2，Flannel 默认是 Overlay 模式基于Linux VxLan，数据包在跨节点间传输有封包和拆包的额外步骤，同节点的 Pod 间数据传输直接通过虚拟网桥，比如 cni0；不同节点的 Pod 间的数据传输需要借助 Flannel.1 (VTEP virtual tunnel endpoint) 分发。
Calico 也有多种工作模式，默认是 IPinIP，同节点的 Pod 间直接通过虚拟网卡结合路由表传输，跨节点间的 Pod 需要IP层的封装，数据包通过IP隧道传输，如 tunl0。多节点间的路由通过BGP协议共享。

在节点上抓包观察同节点 Pod 和 跨节点 Pod 数据传输：
```bash
kubectl exec -it ngx-dep-bfbb5f64b-87sm4 -- curl 10.244.225.25
sudo tcpdump -n -s0 -i any host 10.244.225.25
kubectl exec -it ngx-dep-bfbb5f64b-87sm4 -- curl 10.244.185.207
sudo tcpdump -n -s0 -i any host 10.244.185.207
```</div>2022-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/49/2f38bb6d.jpg" width="30px"><span>Singin in the Rain</span> 👍（4） 💬（1）<div>1、Mac VirtualBox ubuntu 22.04虚拟机环境安装Calico网络插件时，也需要指定网卡。如果enp0s3为Host-Only模式的网卡，enp0s8为NAT网络模式网卡。Flannel和Calico默认使用了enp0s8，所有虚拟机节点enp0s8网卡的IP地址是一样的，会导致冲突，Calico具体表现为calico-node只能启动一个，其他的为crashloopbackoff。因此安装的时候需要指定网卡为Host-Only模式的网卡enp0s3。详见链接：https:&#47;&#47;www.cnblogs.com&#47;xiaohaoge&#47;p&#47;16953849.html
2、安装Calico或者Flannel过程中意外导致失败，需要清除一下网络插件的安装信息，重启kubelet。
rm -rf &#47;etc&#47;cni&#47;net.d&#47;*
rm -rf &#47;var&#47;lib&#47;cni&#47;calico
systemctl  restart kubelet
详见链接：https:&#47;&#47;cloud.tencent.com&#47;developer&#47;article&#47;1820462
如果还不能正常工作，需要检查一下coredns服务，然后重启dns服务：
kubectl -n kube-system rollout restart deployment coredns</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（4） 💬（1）<div>生产环境建议用哪个网络插件呢？</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/d5/a300899a.jpg" width="30px"><span>杨丁</span> 👍（4） 💬（1）<div>老师好，您画图用的啥工具啊</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（0） 💬（1）<div>老师，好像启用了calico之后，发现grafana以及Prometheus只能在pod所在的节点访问，其他节点都无法访问grafana页面以及Prometheus页面</div>2023-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QGOH86dIQBpRKRS3icrRE4JJquETmQcXPBd4VhMCbVV4iconpgUdNFbCJYu4GSOfCics0QmGkhicY3xrrkblkkic9JQ/132" width="30px"><span>糊涂小孩123</span> 👍（0） 💬（1）<div>&#47;opt&#47;cni&#47;bin里的flannel跟以ds部署的flanneld是怎么个关系呢？这块原理是如何的</div>2023-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（0） 💬（1）<div>hostNetwork是不是属于underlay？</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（0） 💬（1）<div>引用原文 ： &quot;这里我重新画了一张图，描述了 Docker 里最常用的 bridge 网络模式：&quot;
该图中的最下方的位置，ens160是表示啥？请老师帮忙解答下，谢谢</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3b/29/0f86235e.jpg" width="30px"><span>明月夜</span> 👍（0） 💬（1）<div>老师好，在节点上（在Pod外）好像也是能访问某个Pod的ip的，这种情况的IP寻址是不是也和在Pod里面的寻址一样？</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（0） 💬（1）<div>按照老师的教程，成功从flannel换成calico了</div>2022-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（0） 💬（1）<div>老师，calico的版本是v3.24.1了</div>2022-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师一个问题：
Q1：怎么修改Prometheus的镜像源格式？
第30课的问题。
我的虚拟机上：prometheus-adapter的状态是CrashLoopBackOff。
针对这个问题，老师的回答是：“exec format error”这样的感觉都是镜像的格式不对，比如amd64&#47;arm64，换个镜像试试。

我是按照老师的如下要求修改的：
image: chronolaw&#47;kube-state-metrics:v2.5.0
image: chronolaw&#47;prometheus-adapter:v0.9.1

我的电脑是win10, intel的CPU，应该是x86系列，请问应该怎么修改上面的image语句？
</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/23/3e/3fc5d62d.jpg" width="30px"><span>卩杉</span> 👍（0） 💬（0）<div>calico-kube-controllers-54756b744f-s94cq   1&#47;1     Running            0                10h    10.10.219.65     master   &lt;none&gt;           &lt;none&gt;
calico-node-6jm8l                          1&#47;1     Running            0                10h    192.168.14.142   master   &lt;none&gt;           &lt;none&gt;
calico-node-h5fln                          0&#47;1     Error              94               10h    192.168.14.143   worker   &lt;none&gt;           &lt;none&gt;

我 worker 节点上有个 calico-node-h5fln 一直 Error，我用 describe 看提示重启失败，报错信息比较少：

Events:
  Type     Reason   Age                 From     Message
  ----     ------   ----                ----     -------
  Normal   Created  27m (x92 over 10h)  kubelet  Created container calico-node
  Warning  BackOff  23m (x55 over 9h)   kubelet  Back-off restarting failed container
  Normal   Pulled   55s (x97 over 10h)  kubelet  Container image &quot;docker.io&#47;calico&#47;node:v3.23.5&quot; already present on machine</div>2023-06-28</li><br/>
</ul>