你好，我是Chrono。

在前面的课里我们学习了Deployment和DaemonSet这两个API对象，它们都是在线业务，只是以不同的策略部署应用，Deployment创建任意多个实例，Daemon为每个节点创建一个实例。

这两个API对象可以部署多种形式的应用，而在云原生时代，微服务无疑是应用的主流形态。为了更好地支持微服务以及服务网格这样的应用架构，Kubernetes又专门定义了一个新的对象：Service，它是集群内部的负载均衡机制，用来解决服务发现的关键问题。

今天我们就来看看什么是Service、如何使用YAML来定义Service，以及如何在Kubernetes里用好Service。

## 为什么要有Service

有了Deployment和DaemonSet，我们在集群里发布应用程序的工作轻松了很多。借助Kubernetes强大的自动化运维能力，我们可以把应用的更新上线频率由以前的月、周级别提升到天、小时级别，让服务质量更上一层楼。

不过，在应用程序快速版本迭代的同时，另一个问题也逐渐显现出来了，就是“**服务发现**”。

在Kubernetes集群里Pod的生命周期是比较“短暂”的，虽然Deployment和DaemonSet可以维持Pod总体数量的稳定，但在运行过程中，难免会有Pod销毁又重建，这就会导致Pod集合处于动态的变化之中。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（31） 💬（2）<div>Service 的 IP 是 vip，其实就是保证外部请求的ip不变，不会因为节点变动，而 ip 跟着动，和 lvs + nginx 部署高可用集群一样，主要保证高可用。方便。
负载均衡算法，Service 会用哪种呢？
轮询，加权轮询，随机，针对有状态的一致性hash，还有针对最少活跃调用数的。
最好的负载均衡是自适应负载均衡，可以动态的监控收集服务的状态，各种指标进行加权计算，从中选出个最合适的。
感觉，service 应该是自适应，都有能力自动编排了，对于一些服务状态的数据指标，收集应该问题不大
</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/a8/d5bf5445.jpg" width="30px"><span>郑海成</span> 👍（19） 💬（1）<div>Q1: svc是基于内核的netfilter技术实现的，在用户态通过iptable和ipvs应用hook链和表，所以它的IP注定是虚拟的，至于静态考虑则是为暴露的服务提供相对稳定性能的dns解析

Q2: 负载均衡技术分为DNS、四层和七层，dns也是一种简单的负载均衡只是算法很简单随机；四层负载均衡主要有nat、IP隧道等，主要是做一些IP和端口的变换，算法也不多比如rr，七层负载均衡则是基于http header来做负载算法很多，可以做一些流量控制；其次还有在客户端做负载均衡比如nacos、istio等</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（18） 💬（5）<div>前几节课多节点集群看起来一切正常，但本节的 dns 测试一直无法通过。周末搞了两天，最终发现是 virtualbox 两张网卡的坑。首先是集群节点的 kubelet 配置需要分别指定 `KUBELET_EXTRA_ARGS=&quot;--node-ip=192.168.56.x&quot;`；然后时安装 flannel 需要指定 `--iface=enp0s3`，这张网卡应该时前面的 node-ip 对应的网卡。</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（11） 💬（1）<div>各位大佬们，如果有用虚拟机的，使用挂起再恢复的，建议每次遇到问题先重启虚拟机，踩了很多次这种挂起再恢复导致的网络问题的坑了</div>2022-08-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（10） 💬（7）<div>不知道有没有同样遇到 dns 无法解析域名的同学，重启coredns试试：
kubectl -n kube-system rollout restart deployment coredns</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b2/91/714c0f07.jpg" width="30px"><span>zero</span> 👍（6） 💬（2）<div>不知道有没有同样遇到 dns 无法解析域名的同学，可能你不能访问的原因是你网络插件Flannel的问题，我自己的虚拟机双网卡，需要在kube-flannel.yml上面指定你的网卡
        args:
        - --ip-masq
        - --kube-subnet-mgr
        - --iface=enp0s3  &#47;&#47; 这里替换成自己的网卡</div>2023-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（5） 💬（2）<div>对于使用 virtualBox 搭建环境，无法使用 DNS 和 exec 进入容器内部的同学，这里有我解决问题的方法，可以尝试参考一下。
问题的原因是，virtualBox 给每个虚拟机默认一个 NAT 的网口，这个网口的 IP 是 virtualBox 自动分配的，且所有的地址都是 10.0.2.15，这个所有节点都相同的 IP 显然会对 kubernetes 造成困扰。解决问题的办法很简单，只要指定 kubelet 使用其他网口即可（网口通常使用的是 192.168 开头的你的路由器的 IP），具体方法是在 &#47;etc&#47;systemd&#47;system&#47;kubelet.service.d&#47;10-kubeadm.conf（我使用的是 ubuntu 系统，其他系统可能是其他路径）文件中添加如下代码 Environment=&quot;KUBELET_EXTRA_ARGS=--node-ip=xxx.xxx.xxx.xxx&quot; ，其中 xxx 就是你虚拟机分配的 IP 地址。修改完成后使用 sudo systemctl daemon-reload 和 sudo systemctl restart kubelet.service 重启 kubelet。然后使用 kubectl get nodes -o wide 查看节点的 IP 是否变更

通常到这里问题就可以解决了，如果你发现依然有问题（使用 kubectl get pod -n kube-system -o wide 看是否有 pod 没有 running），可能要重新安装 flannel 插件。具体情况请问 GPT。
</div>2023-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/81/3865297c.jpg" width="30px"><span>龙之大者</span> 👍（5） 💬（6）<div>进入pod后，如果curl ngx-svc出现Could not resolve hostnames报错，可以重启coredns deployment

kubectl -n kube-system rollout restart deployment coredns

https:&#47;&#47;stackoverflow.com&#47;questions&#47;45805483&#47;kubernetes-pods-cant-resolve-hostnames</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（5） 💬（1）<div>nginx负载均衡是可以设置策略的，权重之类的，svc和nodeport是怎么设置这方面的信息呢</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/87/dde718fa.jpg" width="30px"><span>alexgreenbar</span> 👍（3） 💬（5）<div>NodePort 设置后，得注意可以通过curl集群的节点来访问服务，但这里面不包括master节点</div>2022-09-26</li><br/><li><img src="" width="30px"><span>叶峥瑶</span> 👍（2） 💬（1）<div>ping不通可能是配置问题。 可以参考这篇配置成ipvs https:&#47;&#47;blog.csdn.net&#47;Urms_handsomeyu&#47;article&#47;details&#47;106294085</div>2022-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/93/3c3f2a6d.jpg" width="30px"><span>安石</span> 👍（2） 💬（1）<div>curl ngx-svc我也运行不通，直接在pod里面访问ip可以，域名就不行。
也设置了网卡之类（虚拟机）还是不行，按照k8s官方文档操作可以了
https:&#47;&#47;kubernetes.io&#47;zh-cn&#47;docs&#47;tasks&#47;administer-cluster&#47;dns-debugging-resolution&#47;</div>2022-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/f1/8b06801a.jpg" width="30px"><span>哇哈哈</span> 👍（2） 💬（1）<div>看到这里有点懵，各种 ip 地址不懂怎么来的也不懂为什么要这么搞</div>2022-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（2） 💬（4）<div>虚拟机 curl ngx-svc 产生 Could not resolve 问题解决办法：
1. kube-flannel.yml 文件中加入  --iface=enp0s3，位置如下
  containers:
  - name: kube-flannel
    image: xxx
    command:
    - &#47;opt&#47;bin&#47;flanneld
    args:
    - --ip-masq
    - --kube-subnet-mgr
    - --iface=enp0s3 # 这里新增这条
2. 修改kubelet配置
sudo mkdir &#47;etc&#47;sysconfig
sudo vim &#47;etc&#47;sysconfig&#47;kubelet
加入：
KUBELET_EXTRA_ARGS=&quot;--node-ip=192.168.56.208&quot;
保存
重启kubelet：
systemctl restart kubelet</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/e7/c534fab3.jpg" width="30px"><span>wcy</span> 👍（2） 💬（1）<div>负载均衡 算法 5种：轮询、随机、最小连接、地址hash、加权
轮询：将所有请求依次分配到每台服务器上
随机：将请求随机分配到各个服务器
最小连接：将请求分配到连接最少的服务器上
hash：将地址hash，同一来源地址的请求分配到同一服务器上
加权：在前面4种方法基础上，按权重分配请求到服务器
</div>2022-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（2） 💬（1）<div>service声明为nodePort类型时，可以指定端口吗，老师？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>Service 和 Deployment 管理的都是 pod, 各干自己的事情相互之间不影响。 

k8s 这种 对象的设计感觉非常好</div>2022-08-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEQ91aYaGSuicvGteyiboh9LibWSxAN9zml6XVGeSGmaICIgZ8lH54ngicLicJWcAU0NENibTvtgc0d3tw/132" width="30px"><span>xuing</span> 👍（2） 💬（1）<div>老师在解释“Service 与它引用的 Pod 的关系”时，将图中service的select指向了pod的label。但是其实deployment的metadata中的label也有一个app: ngx-dep。那么service究竟是select的是deployment还是对应的pod呢。似乎指向deployment也能说得通。</div>2022-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>hello, Chrono 老师，我最近又来学习你的专栏了。

我在练习 ：如何让 Service 对外暴露服务 这个模块时，使用 curl 节点地址+对外暴露的端口，发现访问不到节点内部的网络。我是在本机直接安装的 minikube，不是在虚拟机里面安装的。

查阅了minikube 的官网，是这么写的：

如果在 Darwin、Windows 或 WSL 上使用 Docker 驱动程序，网络会受到限制，并且无法直接访问节点 IP。

我没理解错的话，应该是无法通过 Mac 通过 docker 访问到 minikube 节点里面的网络的，然后 minikube 推荐 使用隧道的 方式访问，通过这个方式，我能访问到。请问老师，这里我理解的正确吗？</div>2023-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（1） 💬（1）<div>三个K8s节点（3台虚拟机），deployment配置replica是1，同时配置了NodePort；发现只有pod分布的那个宿主机（虚拟机）机器，可以通过NodePort IP进行访问，其他两个K8s节点无法响应服务；这个正常吗？我理解配置了NodePort，是不是应该所有的宿主机都可以通过NodePort进行访问呢？</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（1） 💬（1）<div>想问下老师，master 和 worker 之间通信，需要放开什么端口？

我用公司的服务器搭建了一个集群，需要手动放开端口。在用 kubectl delete pod 的时候，发现长时间没有响应。同时，执行命令 kubectl exec 也无法进入对应的 pod。但是查看状态都是 OK 的。</div>2023-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/6e/19/3dd8d528.jpg" width="30px"><span>达尔</span> 👍（1） 💬（3）<div>老师，如果是 web 应用，总要对外暴露写 port，这时候是不是一定要有一个 service 用 NodePort 方式暴露？NodePort 是固定 ip 的形式，如果容器迁移到其他结点，是否这个固定 ip 会变化</div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c8/8a/7278c5f7.jpg" width="30px"><span>波罗蜜</span> 👍（1） 💬（1）<div>deployment: 负责创建和管理pod的副本
用的是一种声明式的语言来描述应用程序的期望状态,
并确保k8s按照描述的规范来部署和运行,处理任何失败的副本,它还支持滚动更新

service: 为一组pods 提供了一个单一的入口点，Service使用标签选择器来选择与之关联的Pods，并为它们分配一个稳定的虚拟IP地址或主机名，以便其他应用程序或用户可以通过该IP地址或主机名访问这些pods。Service还可以提供负载均衡、服务发现和内部DNS解析等功能，使应用程序能够以可靠的方式相互通信。</div>2023-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/16/85f97327.jpg" width="30px"><span>Geek_qh28g6</span> 👍（1） 💬（1）<div>root@ubuntu2004-1:~&#47;kubernetes&#47;Services# kubectl get services ngx-svc -o yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io&#47;last-applied-configuration: |
      {&quot;apiVersion&quot;:&quot;v1&quot;,&quot;kind&quot;:&quot;Service&quot;,&quot;metadata&quot;:{&quot;annotations&quot;:{},&quot;name&quot;:&quot;ngx-svc&quot;,&quot;namespace&quot;:&quot;default&quot;},&quot;spec&quot;:{&quot;ports&quot;:[{&quot;port&quot;:80,&quot;protocol&quot;:&quot;TCP&quot;,&quot;targetPort&quot;:80}],&quot;selector&quot;:{&quot;app&quot;:&quot;ngx-dep&quot;}}}
  creationTimestamp: &quot;2023-05-15T03:45:46Z&quot;
  name: ngx-svc
  namespace: default
  resourceVersion: &quot;162031&quot;
  uid: 3f41212e-b9bd-4dec-90fa-740cb97bddc2
spec:
  clusterIP: 10.99.115.6
  clusterIPs:
  - 10.99.115.6
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: ngx-dep
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
root@ubuntu2004-1:~&#47;kubernetes&#47;Services# kubectl get services
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1     &lt;none&gt;        443&#47;TCP   6d14h
ngx-svc      ClusterIP   10.99.115.6   &lt;none&gt;        80&#47;TCP    50m
root@ubuntu2004-1:~&#47;kubernetes&#47;Services# curl 10.99.115.6
srv : 10.244.0.4:80
host: ngx-dep-9bf586b97-zn868
uri : GET 10.99.115.6 &#47;
date: 2023-05-15T04:36:33+00:00

不加type: NodePort，也能在宿主机访问，这是怎么回事呢？</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d3/07/5fc3c694.jpg" width="30px"><span>泰一</span> 👍（1） 💬（1）<div>老师想请教下headless service的问题：
工作中我们使用了headless service。我看很多文档资料都说 headless svc 会返回一组 pod 地址的list，然后由客户端自己选择，做负载均衡。但是请教同事，他们说访问headless svc，是dns轮询选择一个pod地址，dns做了负载均衡。

现在有点晕了，老师能给简要的说下到底 headless service是如何做负载均衡的么
</div>2023-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d3/07/5fc3c694.jpg" width="30px"><span>泰一</span> 👍（1） 💬（2）<div>你好老师，想问下在线业务和离线业务的概念，能举个例子说明么</div>2023-05-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuj7Wx21ecNlPHCfBsQIchmFxVSlPepwUiaKh0RMGgDB0aibTM50ibQN06dDmbqjuQZUIdH4qiaRJkgQ/132" width="30px"><span>Geek_adb513</span> 👍（1） 💬（1）<div>花了钱，又没跟上课程。。。现在接着看，感觉前面内容又丢了😭😭</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（1） 💬（2）<div>老师，请教两个问题 
1.Service 和 Deployment 是不是可以写在同一个yml文件里？我看有这么干的。
2.如果可以写在同一个文件里，启动命令还是kubectl apply -f *.yml吗？</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f0/e9/1ff0a3d5.jpg" width="30px"><span>...</span> 👍（1） 💬（1）<div>为什么curl svc.default的时候，老要重启dns deployment才可以。如何彻底解决好呢</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（1） 💬（3）<div>done
在实操遇到的问题：
kubectl exec -it ngx-dep-7598659bf4-f644t -- sh
error: unable to upgrade connection: pod does not exist
原因：集群搭建的时候网络配置没弄好，一直到这节需要进入容器才发现
所以在搭建集群环境的时候，启动一个pod后，最好进入pod应用验证下。

---
感觉每篇只要理解老师画的关系图，就可以说明白了。</div>2023-01-11</li><br/>
</ul>