你好，我是张磊。今天我和你分享的主题是：从外界连通Service与Service调试“三板斧”。

在上一篇文章中，我为你介绍了Service机制的工作原理。通过这些讲解，你应该能够明白这样一个事实：Service的访问信息在Kubernetes集群之外，其实是无效的。

这其实也容易理解：所谓Service的访问入口，其实就是每台宿主机上由kube-proxy生成的iptables规则，以及kube-dns生成的DNS记录。而一旦离开了这个集群，这些信息对用户来说，也就自然没有作用了。

所以，在使用Kubernetes的Service时，一个必须要面对和解决的问题就是：**如何从外部（Kubernetes集群之外），访问到Kubernetes里创建的Service？**

这里最常用的一种方式就是：NodePort。我来为你举个例子。

```
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  type: NodePort
  ports:
  - nodePort: 8080
    targetPort: 80
    protocol: TCP
    name: http
  - nodePort: 443
    protocol: TCP
    name: https
  selector:
    run: my-nginx
```

在这个Service的定义里，我们声明它的类型是，type=NodePort。然后，我在ports字段里声明了Service的8080端口代理Pod的80端口，Service的443端口代理Pod的443端口。

当然，如果你不显式地声明nodePort字段，Kubernetes就会为你分配随机的可用端口来设置代理。这个端口的范围默认是30000-32767，你可以通过kube-apiserver的–service-node-port-range参数来修改它。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/26/7387fc89.jpg" width="30px"><span>王天明</span> 👍（28） 💬（6）<div>终于算是清楚了，在nodePort模式下，关于端口的有三个参数，port, nodePort, targetPort。
如果如下定义，（请张老师指出是否有理解偏差）
spec:
  type: NodePort
  ports:
    - name: http
      port: 8080
      nodePort: 30080
      targetPort: 80
      protocol: TCP

则svc信息如下，（注意下面无targetPort信息，只是ClustorPort与NodePort，注意后者为Nodeport）
ingress-nginx   ingress-nginx                 NodePort    10.105.192.34    &lt;none&gt;        8080:30080&#47;TCP,8443:30443&#47;TCP   28m

则可访问的组合为
1. clusterIP + port: 10.105.192.34:8080
2. 内网IP&#47;公网ip + nodePort: 172.31.14.16:30080。（172.31.14.16我的aws局域网ip.）

30080为nodePort也可以在iptables-save中映证。
还有，就是port参数是必要指定的，nodePort即使是显式指定，也必须是在指定范围内。

（在三板斧中也问过张老师如何使用nodePort打通外网的问题，一并谢谢了）
</div>2018-11-24</li><br/><li><img src="" width="30px"><span>Flying</span> 👍（3） 💬（2）<div>老师，你好，使用NodePort类型的Service，会创建 -A KUBE-NODEPORTS 类的 iptables规则及 SNAT规则，如果kube-proxy使用的是 ipvs模式，也同样会创建这两个规则吗</div>2019-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/26/7387fc89.jpg" width="30px"><span>王天明</span> 👍（1） 💬（3）<div>张老师，我在使用NodePort暴露外网访问一直不成功，无论是公网IP还是局域网IP但不成功，只能使用ClusterIP+NodePort访问。查看events也都正常，只几节课里使用NodePort都有类似的问题。是我理解哪里存在偏差吗？</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（107） 💬（9）<div>课后思考题:
为什么 Kubernetes 要求 externalIPs 必须是至少能够路由到一个 Kubernetes 的节点？

因为k8s只是在集群中的每个节点上创建了一个 externalIPs 与kube-ipvs0网卡的绑定关系.
若流量都无法路由到任意的一个k8s节点,那自然无法将流量转给具体的service.

--------------------------------
最近在这个externalIPs上面踩了一个坑.
在阿里云上提交了工单.第二天,应该是换了第3个售后工程师,才解决的.
给你们分享一下,哈哈!

事情是这样的:
我的k8s集群中有3个节点,假设分别是:
A: 192.168.1.1
B: 192.168.1.2
C: 192.168.1.3

症状是:
我在节点B&#47;C上,ssh 192.168.1.1, 最终都是登录到了本机,并未成功登录节点A.
但是节点A登录节点B&#47;C, 节点B和节点C互相登录都正常.
只有节点B和节点C上,登录节点A不成功.

就是因为我的某一个service服务就配置了 externalIPs, 配置的IP就是 192.168.1.1(A)
--------------------------------
那个售后工程师发现在节点B和C上有这么一条记录
$ ip addr
inet 192.168.1.1&#47;32 brd 192.168.1.1 scope global kube-ipvs0

那么在节点B和节点C上,访问192.168.1.1的流量,全都转到了kube-ipvs0.
最终这个流量都转到本机了,并未真的发送到远端真实的IP:192.168.1.1

我立马就意识到,我的service绑定了节点的IP.可能是这个导致的.
后来把externalIPs移除掉节点的IP后,该规则就不见了,节点B和节点C也可以正常访问节点A了.

--------------------------------
这个 externalIPs 其实可以填多个,且不要求本机就有对应的IP.
比如你可以填集群中根本就不存在的IP 172.17.0.1,
那么在k8s所有节点上,你都可以通过netstat -ant | grep 172.17.0.1 查看到,有监听该IP的端口.

</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（30） 💬（8）<div>对ExternalName的作用没太理解。
访问my-service.default.svc.cluster.local被替换为my.database.example.com，这和我从外部访问到 Kubernetes 里的服务有什么关系？
感觉这更像是从Kubernetes内访问外部资源的方法。</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（8） 💬（1）<div>思考题 pod的external ip 应该是通过iptables进行配置。可能是一个虚拟ip，在网络中没有对应的设备。所以，必须有路由规则支持。否则客户端可能没办法找到该ip的路径，得到目的网络不可达的回复。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/ea/ce9854a5.jpg" width="30px"><span>坤</span> 👍（5） 💬（0）<div>nodePort下必须要指定Service的port,我用的v1.14，可能检查的更严格了。</div>2019-11-06</li><br/><li><img src="" width="30px"><span>Geek_5baa01</span> 👍（4） 💬（0）<div>我一直再想 LoadBalancer 的问题，如果他是负载到 k8s node 上，那么我应该选择那些 node 做它的负载端点呢？这里被负载的 node 需要额外承担更多的网络流程，这对这些 node 带宽容量评估是个问题，另外还需要考虑 HA 问题，肯定要选择多个 node 作为负载端点，要怎么选择呢？</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（4） 💬（1）<div>在我们通过 kubeadm 部署的集群里，你应该看到 kube-proxy 输出的日志如下所示：—输出日志的命令是什么？</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（0）<div>关于源IP的问题，简易看看这篇官方文档：

文档 教程 Services 使用 Source IP
https:&#47;&#47;kubernetes.io&#47;zh&#47;docs&#47;tutorials&#47;services&#47;source-ip&#47;</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9b/2f/b7a3625e.jpg" width="30px"><span>Len</span> 👍（3） 💬（1）<div>因为 kubernetes 维护着 externalIPs IP + PORT 到具体服务的 endpoints 路由规则。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（2） 💬（0）<div>写了一个简单的nodeport,可以访问上一节的hostname deployment.
apiVersion: v1
kind: Service
metadata:
  name: hostnames
  labels:
    app: hostnames
spec:
  type: NodePort
  selector:
    app: hostnames
  ports:
  - nodePort: 30225
    port: 80
    targetPort: 9376
    protocol: TCP
    name: http


通过curl &lt;任意Node&gt;:30225可以访问。
vagrant@kubeadm1:~&#47;37ServiceDns$ curl 192.168.0.24:30225
hostnames-84985c9fdd-sgwpp

另外感觉我这边的输出关于kube-proxy:
vagrant@kubeadm1:~&#47;37ServiceDns$ kubectl logs -n kube-system kube-proxy-pscvh
W1122 10:13:18.794590       1 server_others.go:295] Flag proxy-mode=&quot;&quot; unknown, assuming iptables proxy
I1122 10:13:18.817014       1 server_others.go:148] Using iptables Proxier.
I1122 10:13:18.817394       1 server_others.go:178] Tearing down inactive rules.
E1122 10:13:18.874465       1 proxier.go:532] Error removing iptables rules in ipvs proxier: error deleting chain &quot;KUBE-MARK-MASQ&quot;: exit status 1: iptables: Too many links.
I1122 10:13:18.894045       1 server.go:447] Version: v1.12.2

后面信息都是正常的。不知道上面这些信息可以ignore吗？</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（2） 💬（1）<div>而如果你的 Service 没办法通过 ClusterIP 访问到的时候，你首先应该检查的是这个 Service 是否有 Endpoints：———请问老师service ip与cluster ip有什么区别？为什么这块不直接是service ip?</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/60/fa/9da0c30e.jpg" width="30px"><span>yuling朱</span> 👍（1） 💬（0）<div>&quot;在 NodePort 方式下，Kubernetes 会在 IP 包离开宿主机发往目的 Pod 时，对这个 IP 包做一次 SNAT 操作&quot;,有个疑问，这里表述是不是有点不准确，在ClusterIP下就不会做SNAT了吗？
只要转发到其他节点就会做SNAT。</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（0）<div>第三十八课:从外界连通你好Service与Service调试“三板斧”
Service的类型分为ClusterIP,NodePort, ExternalIP,ExternalName.

当Service没办法通过DNS访问到的时候，可以先检查Master节点的Service DNS是否可以访问到:
# 在一个Pod里执行
$ nslookup kubernetes.default

如果有问题，就去看kube-dns日志，否则，就要看Service本身定义是否有问题


如果Service没办法通过ClusterIP访问，应该先检查这个Service是否有Endpoint:
$ kubectl get endpoints hostnames

如果Endpoint正确，就要检查kube-proxy是否正确运行，如果正常，就要检查一下iptables

如果Pod没办法访问到自己，就要看看是不是kubelet 的 hairpin-mode 没有被正确设置。你只需要确保将 kubelet 的 hairpin-mode 设置为 hairpin-veth 或者 promiscuous-bridge 即可。

所谓的Service,其实就是k8s为Pod分配的、固定的、基于iptables的访问入口。
</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（1） 💬（0）<div>应该可以通过这章学的内容，访问  Dashboard 可视化插件了吧！试试</div>2020-05-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKmbibsVRmAdEqAtZL9R00FjIZuibW9fTQCXd0OCwhxsR5dfzEKJOcleIpjDqyJnpK4ArY7uGrpcgag/132" width="30px"><span>随欲而安</span> 👍（1） 💬（1）<div>对ExternalName的作用没太理解，老师能解释一下么</div>2019-06-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/0FI2bUjegtznv7XPC9DB9RJaqiaMiamWkibibPOibuUC3DCvI7XMvBANr6sDjRNbc1jwPic9pIaFxrdaib88VqUJKXSTQ/132" width="30px"><span>Chenl07</span> 👍（1） 💬（1）<div>老师，我创建一个externalip的service后，对应的service端口为30100，externalip是一个VIP，实际指向集群中某两个节点。创建后，集群中任意节点上都没有侦听这个端口(netstat grep)，那通过我的VIP，怎么能访问到30100这个端口了？</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（1） 💬（1）<div>请问一下什么应用场景下：“还有一种典型问题，就是 Pod 没办法通过 Service 访问自己？”
为什么要访问自己？</div>2018-11-22</li><br/><li><img src="" width="30px"><span>Geek_5ada4a</span> 👍（0） 💬（0）<div>“而这个机制的实现原理也非常简单：这时候，一台宿主机上的 iptables 规则，会设置为只将 IP 包转发给运行在这台宿主机(如node2)上的 Pod。所以这时候，Pod 就可以直接使用源地址将回复包发出，不需要事先进行 SNAT 了。”
这段话不太理解，即使Pod就运行在宿主机node2上，Pod ip 和宿主机node2的ip也不同吧，没有解决回消息给client时，source ip != node2 ip 的问题啊 </div>2022-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/84/ea/124f0291.jpg" width="30px"><span>国少</span> 👍（0） 💬（0）<div>有同学了解 会话保持 这部分吗？</div>2022-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（0） 💬（0）<div>如果都不能路由的kubernetes的节点的话就没什么用了，请求都无法路由进去</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/3f/59/3b9da34b.jpg" width="30px"><span>初心?固执?</span> 👍（0） 💬（0）<div>弱弱的问下，这个ExternalName是外部访问的域名吗？需要解析到其中一个node IP的这种？</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/94/e89ebc50.jpg" width="30px"><span>神毓逍遥</span> 👍（0） 💬（0）<div>这篇文档很实用，自己再部署搭建集群，需要允许 pod 被外部访问时，会用到，自己实验的平台是 AWS&#47;QINGCLOUD</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9e/24/0d6a7987.jpg" width="30px"><span>aroll</span> 👍（0） 💬（0）<div>通过Service 暴漏 Nodeport之后，外网是可以访问，为什么容器内部通过 宿主机ip+Nodeport访问不通？</div>2021-09-26</li><br/><li><img src="" width="30px"><span>Geek_5baa01</span> 👍（0） 💬（0）<div>老师我还有一个问题，我在用 aliyun LoadBalancer 时发现它其实是设置了 service nodeport ，然后创建了 SLB 指向k8s node ，并且映射了 80 到对应的 nodeport ，这种方式的网络链路更长，应该会增加网络延时，有没有更好的方式呢？</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/fe/79955244.jpg" width="30px"><span>公众号：程序员大兵</span> 👍（0） 💬（1）<div>修改了&#47;etc&#47;kubernetes&#47;manifests&#47;kube-apiserver.yaml 中 service-node-port-range 怎么才能生效呢</div>2021-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIZ2Kr6TQt91Mdr16atJvwEkyYq1YGh8qR7BPCqPlgO7ZoyM95z4uLbSkMyzcP33fyIRAcHAUdN8Q/132" width="30px"><span>极客精英</span> 👍（0） 💬（0）<div>老师，请问如果有很多微服务，需要暴露很多tcp端口，用nodeport方式暴露。但node节点非常多，考虑node本身也需要负载均衡和高可用，是不是也应该把node也挂到在均衡器下？ 外部服务通过这个负载均衡器来进入k8s集群？</div>2020-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>如果任何的Kubernetes都无法路由到,那么自然无法将流量转发给具体的Service
</div>2020-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/f2/54c30dbf.jpg" width="30px"><span>殷佳毅</span> 👍（0） 💬（0）<div>老师好，service能不能做到pod在通过svc访问时如果这个svc的后端pod有在同一个worker上时流量有限从同worker的pod走，同一个worker上没有pod时再走其他worker上的pod？</div>2020-03-31</li><br/>
</ul>