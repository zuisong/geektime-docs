你好，我是张磊。今天我和你分享的主题是：找到容器不容易之Service、DNS与服务发现。

在前面的文章中，我们已经多次使用到了Service这个Kubernetes里重要的服务对象。而Kubernetes之所以需要Service，一方面是因为Pod的IP不是固定的，另一方面则是因为一组Pod实例之间总会有负载均衡的需求。

一个最典型的Service定义，如下所示：

```
apiVersion: v1
kind: Service
metadata:
  name: hostnames
spec:
  selector:
    app: hostnames
  ports:
  - name: default
    protocol: TCP
    port: 80
    targetPort: 9376
```

这个Service的例子，相信你不会陌生。其中，我使用了selector字段来声明这个Service只代理携带了app=hostnames标签的Pod。并且，这个Service的80端口，代理的是Pod的9376端口。

然后，我们的应用的Deployment，如下所示：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hostnames
spec:
  selector:
    matchLabels:
      app: hostnames
  replicas: 3
  template:
    metadata:
      labels:
        app: hostnames
    spec:
      containers:
      - name: hostnames
        image: k8s.gcr.io/serve_hostname
        ports:
        - containerPort: 9376
          protocol: TCP
```

这个应用的作用，就是每次访问9376端口时，返回它自己的hostname。

而被selector选中的Pod，就称为Service的Endpoints，你可以使用kubectl get ep命令看到它们，如下所示：

```
$ kubectl get endpoints hostnames
NAME        ENDPOINTS
hostnames   10.244.0.5:9376,10.244.0.6:9376,10.244.0.7:9376
```

需要注意的是，只有处于Running状态，且readinessProbe检查通过的Pod，才会出现在Service的Endpoints列表里。并且，当某一个Pod出现问题时，Kubernetes会自动把它从Service里摘除掉。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/72/92e43306.jpg" width="30px"><span>纳爱斯</span> 👍（41） 💬（3）<div>老师，是每个 node 上都会有 iptables 的全部规则吗</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b1/da/88197585.jpg" width="30px"><span>甘陵笑笑生</span> 👍（7） 💬（2）<div>请教一下 service的VIP设置后会变吗 如果变 什么时候会变</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/c1/431039c0.jpg" width="30px"><span>AmyHuang</span> 👍（2） 💬（2）<div>老师 现在有个问题请教：service 三副本 把一个副本所在节点驱逐，pod迁移到新的节点有一段时间可以telnet podip +port，但是直接curl service +port 会有数据中断，这个可能是我们设置什么导致呢？</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/1a/eb8021c3.jpg" width="30px"><span>追寻云的痕迹</span> 👍（88） 💬（2）<div>iptables是万恶之源，在复杂系统中，网络处理越简单越好。现在k8s这套玩法，给实际工作中的运维排错带来极大的麻烦。</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/8b/bd318156.jpg" width="30px"><span>qingbo</span> 👍（37） 💬（2）<div>看到也有同学问pod DNS，希望能讲得更详细些。我查阅官方文档及自己实践后的了解是这两种pod有DNS记录：
1. statefulset的pod。有人问之前讲DNS的是在哪，就是“20 | 深入理解StatefulSet（三）：有状态应用实践”这一篇。
2. pod显式指定了hostname和subdomain，并且有个headless service的名字和subdomain一样。在“27 | 聪明的微创新：Operator工作原理解读”一篇中讲到的etcd operator就是这样让pod拥有了DNS记录。Deployment的pod template也可以指定hostname和subdomain，但是却没办法给每个pod分配不同的hostname。指定hostname和subdomain之后，hostname.subdomain.default.svc.cluster.local这样的域名确实可以解析，但是因为多个pod都是这个FQDN，所以解析出来的效果和headless service一样，多个A记录，也就失去意义了。github上有个issue想让deployment管理的pod也有独立的DNS，好像没得到支持。</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（30） 💬（1）<div>老师，..svc.cluster.local这些点前面的东西能写全吗？录音听了N次也没记下来。文字不行的话能不能弄个图片？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（29） 💬（0）<div>示例终于都可以工作了，深化理解。
一种是通过&lt;serviceName&gt;.&lt;namespace&gt;.svc.cluster.local访问。对应于clusterIP
另一种是通过&lt;podName&gt;.&lt;serviceName&gt;.&lt;namesapce&gt;.svc.cluster.local访问,对应于headless service.
&#47; # nslookup *.default.svc.cluster.local
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      *.default.svc.cluster.local
Address 1: 10.244.1.7 busybox-3.default-subdomain.default.svc.cluster.local
Address 2: 10.96.0.1 kubernetes.default.svc.cluster.local
Address 3: 10.97.103.223 hostnames.default.svc.cluster.local
</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（17） 💬（0）<div>ipvs负载均衡：round robin
    least connection
    destination hashing
    source hashing
    shortest expected delay
    never queue
    overflow-connection</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/6c/4a68a916.jpg" width="30px"><span>双叶</span> 👍（13） 💬（1）<div>不太赞同 ipvs 比 iptables 快是因为把更多的操作放到了内核里面，不管 ipvs 还是 iptables，他的所有逻辑都是在内核里面跑的，只是 iptables 需要遍历规则，而规则数量会跟随 pod 数量增长，导致时间复杂度是 O(n)，而 ipvs 是专门做负载均衡的，时间复杂度是 O(1)。

这篇文章里面有比较细致的说明：https:&#47;&#47;www.tigera.io&#47;blog&#47;comparing-kube-proxy-modes-iptables-or-ipvs&#47;
基本来说，就是 iptables 不能放太多规则</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/eb/b5bb4227.jpg" width="30px"><span>runner</span> 👍（11） 💬（2）<div>请问老师，每个节点会有全部的iptables规则么，还是只有自己所属服务的规则？
如果服务是nodePort类型，它会在所有节点上占用端口？还是容器所在的几个节点占用端口？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/35/5b/c9d7e8c0.jpg" width="30px"><span>李康</span> 👍（9） 💬（1）<div>
-A KUBE-SEP-57KPRZ3JQVENLNBR -s 10.244.3.6&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000

-A KUBE-SEP-WNBA2IHDGP2BOBGZ -s 10.244.1.7&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000

-A KUBE-SEP-X3P2623AGDH6CDF3 -s 10.244.2.3&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000

问下为啥源地址是这个啊？现在数据包源地址不应该是客户端的地址吗？</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/d1/2c6f297f.jpg" width="30px"><span>mcc</span> 👍（8） 💬（9）<div>描述一个实际使用中遇到kube-proxy的一个问题。我使用service的nodeport模式对外发布服务，前端使用openresty做代理的，upstream就配置node ip+nodeport。在使用过程中发现openresty经常不定期报104:connection reset by peer when read response head这个错误，从错误看出openstry从nodeport读取数据的时候tcp连接被重置了，使用同一openresty的后端是普通虚拟机的节点的服务却没有这个问题，问题还有个特点就是某个服务长时间没有被访问，第一次点击的时候就会出现，然后后面就好了。nodeport是被kube-proxy监听的，问题就出在openresty与kube-proxy的tcp连接上，能否帮忙分析kube-proxy为何会重置连接？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8c/0c/a36cdf51.jpg" width="30px"><span>grep</span> 👍（4） 💬（2）<div>示例里这里打出来的 endpoints ip：
kubectl get endpoints hostnames
NAME        ENDPOINTS
hostnames   10.244.0.5:9376,10.244.0.6:9376,10.244.0.7:9376

与下面的 iptables 规则里的 endpoint ip 对不上
-A KUBE-SEP-57KPRZ3JQVENLNBR -s 10.244.3.6&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000
-A KUBE-SEP-57KPRZ3JQVENLNBR -p tcp -m comment --comment &quot;default&#47;hostnames:&quot; -m tcp -j DNAT --to-destination 10.244.3.6:9376

-A KUBE-SEP-WNBA2IHDGP2BOBGZ -s 10.244.1.7&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000
-A KUBE-SEP-WNBA2IHDGP2BOBGZ -p tcp -m comment --comment &quot;default&#47;hostnames:&quot; -m tcp -j DNAT --to-destination 10.244.1.7:9376

-A KUBE-SEP-X3P2623AGDH6CDF3 -s 10.244.2.3&#47;32 -m comment --comment &quot;default&#47;hostnames:&quot; -j MARK --set-xmark 0x00004000&#47;0x00004000
-A KUBE-SEP-X3P2623AGDH6CDF3 -p tcp -m comment --comment &quot;default&#47;hostnames:&quot; -m tcp -j DNAT --to-destination 10.244.2.3:9376

是不是中间重新部署过？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/2a/2ac18fb8.jpg" width="30px"><span>艾斯Z艾穆</span> 👍（4） 💬（1）<div>您好，我使用coreDNS插件版本是1.2.6 
配置文件的内容：
Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local. in-addr.arpa ip6.arpa {
            pods insecure
            upstream
            fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        proxy . 100.64.255.100 223.5.5.5 11.125.1.12
        cache 30
        loop
        reload
        loadbalance
    }
在解析公网的域名的时候会有小概率随机出现unknown host，请问会是什么问题</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/7d/ac715471.jpg" width="30px"><span>独孤九剑</span> 👍（3） 💬（0）<div>“服务”本质是一种“反向代理”机制</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（3） 💬（0）<div>iptables的负载均衡分两种：random &#47; nth，random是随机模式，--probability p指定了概率，nth是轮巡模式，--every n和--packet p指定了每n个packet中匹配其中的第p个。</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/f2/fee557fe.jpg" width="30px"><span>Mr.Cling</span> 👍（3） 💬（3）<div>这时候，任何发往 10.102.128.4:80 的请求，就都会被 IPVS 模块转发到某一个后端 Pod 上了。

请问这里的10.102.128.4的IP是什么IP？</div>2019-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/82/164b9073.jpg" width="30px"><span>Majorin_Che</span> 👍（3） 💬（1）<div>所以这里服务发现的方式就是通过label发现pod，是这样理解吗？</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/85/99545c24.jpg" width="30px"><span>叶王</span> 👍（2） 💬（0）<div>endpoint ip 和后面 iptables ip 没有对上。</div>2022-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（1）<div>必然会存在着轮询去进行负载均衡的策略以及利用会话保持的进行保证客户端分配固定的pod Ip的模式</div>2020-09-30</li><br/><li><img src="" width="30px"><span>思维决定未来</span> 👍（2） 💬（6）<div>如果把这三条规则的 probability 字段的值都设置成1&#47;3，那么第一条规则命中几率是1&#47;3，第二条是2&#47;3 * 1&#47;3=2&#47;9，第三条是1&#47;3 * 1&#47;3 = 1&#47;9</div>2019-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（2） 💬（0）<div>&quot;我在前面的文章中还介绍过 Service 与 DNS 的关系.&quot;可以帮忙指明一下是第几章吗？找了一圈没找到。

另外：试着通过域名访问hostanmes，不行。通过ip可以。
vagrant@kubeadm1:~&#47;37ServiceDns$ curl hostnames.svc.cluster.local:80
curl: (6) Could not resolve host: hostnames.svc.cluster.local

vagrant@kubeadm1:~&#47;37ServiceDns$ curl 10.110.252.216:80
hostnames-84985c9fdd-sgwpp


</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c3/bd/03a16b21.jpg" width="30px"><span>Long Long☞</span> 👍（2） 💬（1）<div>老师 现在我遇到一个问题，同一个域名希望在不同的namespace中解析成不同的IP，要怎么实现</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/61/677e8f92.jpg" width="30px"><span>xianhai</span> 👍（2） 💬（0）<div>服务发布有问题,如何确定问题出在kubeproxy上还是overlay network上？这一块如何trouble shooting，能讲讲吗？</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（2） 💬（0）<div>sevice是由kubelet创建的吗？再有kubenates的sevice代理的却不是pod，而是apiserver的容器，那么kubenates service是什么时候由谁创建出来的？</div>2018-11-16</li><br/><li><img src="" width="30px"><span>Geek_553e7d</span> 👍（1） 💬（2）<div>kube-proxy 的負載平衡利用了NAT，不就浪費了 CNI SPEC 的直接透過 pod ip 存取 pod 不需要 NAT的美意了嗎？為什麼要這麼設計呢？感覺這兩個設計互相衝突🤔

Kubernetes imposes the following fundamental requirements on any networking 
implementation (barring any intentional network segmentation policies):

- pods on a node can communicate with all pods on all nodes without NAT
- agents on a node (e.g. system daemons, kubelet) can communicate with all pods on 
  that node. 
  Note: For those platforms that support Pods running in the host network 
  (e.g. Linux):
  - pods in the host network of a node can communicate with all pods on all nodes 
    without NAT</div>2024-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/44/b8/d5fe40fb.jpg" width="30px"><span>Vndi</span> 👍（1） 💬（0）<div>意思是原生service都只能走nat不走容器网络了？那istio service规则不写在iptables里，应该是可以用容器网络的吧</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/86/68/ecac85d4.jpg" width="30px"><span>越战越勇</span> 👍（1） 💬（2）<div>你好，请教下，service的负载均衡支持一致性hash策略吗，有个需求，如：客户端通过udp端口10010通过service访问到某个pod，但是后续客户端还会通过10010发送数据，但是要求后续发送的数据都转发到第一次的pod。  期待您的答复，谢谢</div>2021-03-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJOBwR7MCVqwZzc3keFAJT12Sic3VYWx4PrZbCGDm4kBZD3oqnR4xsibGGtGy4tFO8y05Ims27SiaavA/132" width="30px"><span>海阔天空</span> 👍（1） 💬（0）<div>对于 ClusterIP 模式的 Service 来说，它代理的 Pod 被自动分配的 A 记录的格式是：..pod.cluster.local。这条记录指向 Pod 的 IP 地址。 ==&gt; 目前版本，并没有找到对应的DNS记录呀</div>2020-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/01/a0/07ca2bd2.jpg" width="30px"><span>一路顺风</span> 👍（1） 💬（0）<div>老师，请问通过service的vip访问后端服务是如何保持tcp连接的状态的</div>2020-08-19</li><br/>
</ul>