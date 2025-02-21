你好，我是张磊。今天我和你分享的主题是：谈谈Service与Ingress。

在上一篇文章中，我为你详细讲解了将Service暴露给外界的三种方法。其中有一个叫作LoadBalancer类型的Service，它会为你在Cloud Provider（比如：Google Cloud或者OpenStack）里创建一个与该Service对应的负载均衡服务。

但是，相信你也应该能感受到，由于每个 Service 都要有一个负载均衡服务，所以这个做法实际上既浪费成本又高。作为用户，我其实更希望看到Kubernetes为我内置一个全局的负载均衡器。然后，通过我访问的URL，把请求转发给不同的后端Service。

**这种全局的、为了代理不同后端Service而设置的负载均衡服务，就是Kubernetes里的Ingress服务。**

所以，Ingress的功能其实很容易理解：**所谓Ingress，就是Service的“Service”。**

举个例子，假如我现在有这样一个站点：`https://cafe.example.com`。其中，`https://cafe.example.com/coffee`，对应的是“咖啡点餐系统”。而，`https://cafe.example.com/tea`，对应的则是“茶水点餐系统”。这两个系统，分别由名叫coffee和tea这样两个Deployment来提供服务。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/43/e2/a1ff289c.jpg" width="30px"><span>wang jl</span> 👍（19） 💬（3）<div>文章里面这个nginx ingress只是api网关啊，负载均衡体现在哪里？其实还是service做的？</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/b2/dfdcc8f3.jpg" width="30px"><span>黄巍</span> 👍（12） 💬（3）<div>「但是，相信你也应该能感受到，由于每个 Service 都要有一个负载均衡服务，所以这个做法实际上既浪费成本又高。」没错，下周的 KubeCon 我会做一个关于共享 4 层 LoadBalancer 的session :)</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/21/b0fe1bfd.jpg" width="30px"><span>Adam</span> 👍（8） 💬（1）<div>感觉再加上一层ingress，又多了一层转发，性能上会不会损失比较大。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/43/e2/a1ff289c.jpg" width="30px"><span>wang jl</span> 👍（7） 💬（1）<div>lvs-&gt;nginx-&gt;lvs-&gt;service 这操作骚得可以。
关键是lvs还是nat模式的。</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（7） 💬（2）<div>老师，为什么在创建 Ingress 所需的 SSL 证书（tls.crt）和密钥（tls.key）之后，使用curl命令还需要加上--insecure.
&quot;curl --resolve cafe.example.com:$IC_HTTPS_PORT:$IC_IP https:&#47;&#47;cafe.example.com:$IC_HTTPS_PORT&#47;tea --insecure&quot;

我的理解是：创建的SSL证书和密钥没有通过CA验证，所以要加上--secure. 对吗？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/3d/d998a34f.jpg" width="30px"><span>zylv</span> 👍（4） 💬（2）<div>ingress-controller 里面如果不配置域名，配置ip,可以吗</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3d/0e/92176eaa.jpg" width="30px"><span>左氧佛沙星人</span> 👍（2） 💬（1）<div>请问各位大神和老师
可以看到，这个 Service 的唯一工作，就是将所有携带 ingress-nginx 标签的 Pod 的 80 和 433 端口bao lu出去。
为啥需要创建一个svc呢？为啥需要bao lu80和443呢？</div>2020-03-11</li><br/><li><img src="" width="30px"><span>Holy</span> 👍（2） 💬（3）<div>K8s目前这几类负载均衡都属于服务端负载均衡，优点很明显，对客户端友好透明，无需额外的感知工作，缺点是在大流量高并发对性能有要求的场景，负载均衡器可能会变为单点瓶颈，不知道自己理解的对不对</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/30/231af749.jpg" width="30px"><span>陈小虎</span> 👍（2） 💬（1）<div>这种非系统类控制器本来就主要部署在work-node上吧：）</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（140） 💬（0）<div>思考题：
spec:
  rules:
  - host: www.mysite.com
    http:
      paths:
      - backend:
          serviceName: site-svc
          servicePort: 80
  - host: forums.mysite.com
    http:
      paths:
      - backend:
          serviceName: forums-svc
          servicePort: 80</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（58） 💬（5）<div>总结一下，从集群外访问到服务，要经过3次代理：

访问请求到达任一宿主机，会根据NodePort生成的iptables规则，跳转到nginx反向代理，
请求再按照nginx的配置跳转到后台service，nginx的配置是根据Ingress对象生成的，
后台service也是iptables规则，最后跳转到真正提供服务的POD。

另外，如果想查看nginx-ingress-controller生成的nginx配置，可以这么做：

$ kubectl get pods -n ingress-nginx 
NAME                                        READY   STATUS    RESTARTS   AGE
nginx-ingress-controller-85d94747dd-lsggm   1&#47;1     Running   0          3h45m

$ kubectl exec nginx-ingress-controller-85d94747dd-lsggm -it --namespace=&quot;ingress-nginx&quot; -- bash

$ cat &#47;etc&#47;nginx&#47;nginx.conf
...
$ exit</div>2018-11-21</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（40） 💬（0）<div>Kubernets中通过Service来实现Pod实例之间的负载均衡和固定VIP的场景。

Service的工作原理是通过kube-proxy来设置宿主机上的iptables规则来实现的。kube-proxy来观察service的创建，然后通过修改本机的iptables规则，将访问Service VIP的请求转发到真正的Pod上。

基于iptables规则的Service实现，导致当宿主机上有大量的Pod的时候，成百上千条iptables规则不断刷新占用大量的CPU资源。因此出现了一种新的模式: IPVS，通过Linux的 IPVS模块将大量iptables规则放到了内核态，降低了维护这些规则的代价（部分辅助性的规则无法放到内核态，依旧是iptable形式）。

Service的DNS记录： &lt;myservice&gt;.&lt;mynamespace&gt;.svc.cluster.local ，当访问这条记录，返回的是Service的VIP或者是所代理Pod的IP地址的集合

Pod的DNS记录： &lt;pod_hostname&gt;.&lt;subdomain&gt;.&lt;mynamespace&gt;.svc.cluster.local， 注意pod的hostname和subdomain都是在Pod里定义的。

Service的访问依赖宿主机的kube-proxy生成的iptables规则以及kube-dns生成的DNS记录。外部的宿主机没有kube-proxy和kube-dns应该如何访问对应的Service呢？有以下几种方式：

NodePort： 比如外部client访问任意一台宿主机的8080端口，就是访问Service所代理Pod的80端口。由接收外部请求的宿主机做转发。

即：client --&gt; nodeIP:nodePort --&gt; serviceVIP:port --&gt; podIp:targetPort

LoadBalance：由公有云提供kubernetes服务自带的loadbalancer做负载均衡和外部流量访问的入口

ExternalName：通过ExternalName或ExternalIp给Service挂在一个公有IP的地址或者域名，当访问这个公有IP地址时，就会转发到Service所代理的Pod服务上

Ingress是用来给不同Service做负载均衡服务的，也就是Service的Service。


</div>2020-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/93/e8bfb26e.jpg" width="30px"><span>Dem</span> 👍（33） 💬（1）<div>Nginx Ingress Controller的mandatory.yaml地址改掉了。现在的命令：
kubectl apply -f https:&#47;&#47;raw.githubusercontent.com&#47;kubernetes&#47;ingress-nginx&#47;master&#47;deploy&#47;static&#47;mandatory.yaml</div>2019-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（13） 💬（1）<div>Nginx Ingress Controller的mandatory.yaml地址改掉了。现在的命令：
kubectl apply -f https:&#47;&#47;raw.githubusercontent.com&#47;kubernetes&#47;ingress-nginx&#47;controller-v0.34.1&#47;deploy&#47;static&#47;provider&#47;baremetal&#47;deploy.yaml</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/dd/6e/f3cfebc5.jpg" width="30px"><span>峰哥</span> 👍（11） 💬（3）<div>Ingress只支持7层的话，tcp协议的service怎么处理？</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/e2/823a04b4.jpg" width="30px"><span>小小笑儿</span> 👍（11） 💬（0）<div>感觉是因为nodeport之类的没有路由功能而出现的ingress，而且ingress还是需要由loadbalance之类的暴露给集群外部访问</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/ed/e6a6e60e.jpg" width="30px"><span>busman</span> 👍（8） 💬（2）<div>老师，我目前遇到个场景，就是一个非常耗资源的服务，需要容器化，部署在k8s集群中。目前问题就是这种大资源程序怎么打包(也是直接运行在一个容器里吗？)，如何调度？是否有通用方案。
这个程序大致是一个深度学习的算法，有tensorflow很耗cpu(监控来看，直接在一个容器里运行，能到十几核)，也会加载很大的模型(内存占用6G)，就这样的场景，老师能点拨一下吗？感谢</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/fe/ab541300.jpg" width="30px"><span>小猪</span> 👍（6） 💬（4）<div>请问ingress里配置的域名访问地址，那么集群外部怎么根据域名访问到k8s的服务呢？</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（5） 💬（0）<div>“Ingress是service的service” 太精辟了！一下就理解了ingress存在的意义！</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/b9/dbf629c0.jpg" width="30px"><span>Tao</span> 👍（5） 💬（1）<div>apiVersion: extensions&#47;v1beta1
kind: Ingress
metadata:
  name: cafe-ingress
spec:
  tls:
  - hosts:
    - www.mysite.com
    - forums.mysite.com
    secretName: mysite-secret
  rules:
  - host: www.mysite.com
    http:
      paths:
      - path: &#47;mysite
        backend:
          serviceName: site-svc
          servicePort: 80
  - host: forums.mysite.com
    http:
      paths:
      - path: &#47;forums
        backend:
          serviceName: site-svc
          servicePort: 80
</div>2020-01-10</li><br/><li><img src="" width="30px"><span>学习者</span> 👍（4） 💬（0）<div>问题描述：前后端分离，但是同一域名下既有前端代码（部署在nginx中，以静态文件方式访问。），又用nginx 的proxy_pass ,根据url （location &#47;xx&#47; {}）反向代理做了后端。
方案 1：client -&gt; lb -&gt; ingress -&gt; nginx  (nginx 只部署前端，ingress 配置后端连接pod 的service，)
方案2 ： client -&gt; nginx  ( 后端采用nodeport暴露出来，采用问题描述方法部署)
请问这两种方案的可行性？或者还有什么更好的方案吗？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/26/7387fc89.jpg" width="30px"><span>王天明</span> 👍（3） 💬（0）<div>张老师，curl 那行代码，应该在“--insecureServer”中间换行了。</div>2018-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/41/37/b89f3d67.jpg" width="30px"><span>我在睡觉</span> 👍（2） 💬（1）<div>老师这节课讲的ingress是一个7层负载均衡
用ingress是否可以搭建一个4层负载均衡？</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/62/9b248708.jpg" width="30px"><span>阿硕</span> 👍（2） 💬（1）<div>一个ingress部署后，每个node上的端口都会占用，在真实环境中是不是每个node前都在外加一个lvs？</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/93/aa3cb0fc.jpg" width="30px"><span>火车飞侠</span> 👍（2） 💬（2）<div>老师，如果我后端服务是https的，ingress如何定义呢？</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（2） 💬（0）<div>学习过程中遇到一些一直想不通的问题，麻烦能怎么联系老师解答下吗？</div>2018-11-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4fZ9thib248ZkR1N3Eekeyb8N1V1Ud0uePctlI4VQUibPSmEZvgoP0VYl6IsVHJc7ZMiczQMtU76y6E6ag1zNAK4Q/132" width="30px"><span>Geek_336577</span> 👍（1） 💬（0）<div>通过NodePort暴露nginx其实是有问题的，如果该机器挂了，那就访问不了了，做不到高可用。nginx前面可以做一层keepalive+haproxy做高可用，外部就访问keepalive的vip，haproxy转发到nginx的svc就好</div>2023-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/50/59d429c9.jpg" width="30px"><span>MiracleWong</span> 👍（1） 💬（0）<div>由 @思维 给出的地址：https:&#47;&#47;raw.githubusercontent.com&#47;kubernetes&#47;ingress-nginx&#47;controller-v0.34.1&#47;deploy&#47;static&#47;provider&#47;baremetal&#47;deploy.yaml

我们可以看到使用的Helm Charts 是helm.sh&#47;chart: ingress-nginx-2.11.1
如果你是使用helm （v3 版本）管理服务的话，可以通过
helm repo add ingress-nginx https:&#47;&#47;kubernetes.github.io&#47;ingress-nginx
helm repo update
helm search repo ingress-nginx (看到现在最高版本是3.23.0)

helm install ingress-nginx ingress-nginx&#47;ingress-nginx  安装。

如果想安装  ingress-nginx-2.11.1 
可以
helm fetch ingress-nginx&#47;ingress-nginx --version 2.1.1
tar zxvf ingress-nginx-2.11.1.tgz
helm install ingress-nginx .&#47;ingress-nginx  进行安装

如果下载镜像版本过慢，可以考虑把镜像推送到私有仓库</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/41/37/b89f3d67.jpg" width="30px"><span>我在睡觉</span> 👍（1） 💬（0）<div>是否也可以用云提供的7层负载均衡器+nodeport形式实现的ingress效果。这样做效率是否会更高？</div>2021-01-20</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（1） 💬（0）<div>按照文档操作，最后的curl报了个异常

curl --resolve cafe.example.com:$IC_HTTPS_PORT:$IC_IP https:&#47;&#47;cafe.example.com:$IC_HTTPS_PORT&#47;tea --insecure
curl: (35) SSL received a record that exceeded the maximum permissible length.</div>2020-07-04</li><br/>
</ul>