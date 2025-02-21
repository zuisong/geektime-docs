你好，我是Chrono。

上次课里我们学习了Service对象，它是Kubernetes内置的负载均衡机制，使用静态IP地址代理动态变化的Pod，支持域名访问和服务发现，是微服务架构必需的基础设施。

Service很有用，但也只能说是“基础设施”，它对网络流量的管理方案还是太简单，离复杂的现代应用架构需求还有很大的差距，所以Kubernetes就在Service之上又提出了一个新的概念：Ingress。

比起Service，Ingress更接近实际业务，对它的开发、应用和讨论也是社区里最火爆的，今天我们就来看看Ingress，还有与它关联的Ingress Controller、Ingress Class等对象。

## 为什么要有Ingress

通过上次课程的讲解，我们知道了Service的功能和运行机制，它本质上就是一个由kube-proxy控制的四层负载均衡，在TCP/IP协议栈上转发流量（[Service工作原理示意图](https://kubernetes.io/zh/docs/concepts/services-networking/service/)）：

![图片](https://static001.geekbang.org/resource/image/03/74/0347a0b3bae55fb9ef6c07469e964b74.png?wh=1622x1214)

但在四层上的负载均衡功能还是太有限了，只能够依据IP地址和端口号做一些简单的判断和组合，而我们现在的绝大多数应用都是跑在七层的HTTP/HTTPS协议上的，有更多的高级路由条件，比如主机名、URI、请求头、证书等等，而这些在TCP/IP网络栈里是根本看不见的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/14/b9/47377590.jpg" width="30px"><span>Jasper</span> 👍（29） 💬（1）<div>四层架构简单，无需解析消息内容，在网络吞吐量及处理性能上高于七层。
而七层负载优势在于功能多，控制灵活强大。</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bb/69/a8bb7a4a.jpg" width="30px"><span>Xu.</span> 👍（17） 💬（3）<div>老师，我在安装文档里找到了大多数同学遇到的问题的解决方法：
https:&#47;&#47;docs.nginx.com&#47;nginx-ingress-controller&#47;installation&#47;installation-with-manifests&#47;
Create Custom Resources 这一节

注意：默认情况下，需要为 VirtualServer, VirtualServerRoute, TransportServer and Policy 创建自定义资源的定义。否则，Ingress Controller Pod 将不会变为 Ready 状态。如果要禁用该要求，请将 -enable-custom-resources 命令行参数配置为 Readyfalse 并跳过此部分。

也就是说可以 kubectl apply -f 下面几个文件：

$ kubectl apply -f common&#47;crds&#47;k8s.nginx.org_virtualservers.yaml
$ kubectl apply -f common&#47;crds&#47;k8s.nginx.org_virtualserverroutes.yaml
$ kubectl apply -f common&#47;crds&#47;k8s.nginx.org_transportservers.yaml
$ kubectl apply -f common&#47;crds&#47;k8s.nginx.org_policies.yaml

然后就启动成功了。

也可以将 -enable-custom-resources 命令行参数配置为 Readyfalse </div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/d9/cf061262.jpg" width="30px"><span>新时代农民工</span> 👍（12） 💬（1）<div>文末的kic.yml是来自 https:&#47;&#47;github.com&#47;nginxinc&#47;kubernetes-ingress&#47;blob&#47;main&#47;deployments&#47;deployment&#47;nginx-ingress.yaml</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（9） 💬（3）<div>一个小问题老师，service基于四层转发，会暴露ip。基于这些缺点我们引入了ingress，基于七层网络协议转发，但是为了外部服务访问，需要在ingress前再暴露一个nodeport类型的service，那我们这么做的意义在哪里捏，最外层的入口处不还是service吗。</div>2022-10-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oib0a89lqtOhJL1UvfUp4uTsRLrDbhoGk9jLiciazxMu0COibJsFCZDypK1ZFcHEJc9d9qgbjvgR41ImL6FNPoVlWA/132" width="30px"><span>stefen</span> 👍（7） 💬（1）<div>最后ingress-controller运行起来的pod 可以看作是一个pod的nginx反向代理的VIP， 由于pod网络隔离的原因，需要还套娃一个service, 对外提供统一的管理入口，是否可以换种思路， 在启动这种ingress-controller运行起来的pod的，设置pod的网络为host，就是公用宿主机网卡，这样就不用套娃service了.</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/63/9a/6872c932.jpg" width="30px"><span>Grey</span> 👍（7） 💬（2）<div>Nginx Ingress Controller 只用那4个不行，看了23节，跟着老师用bash脚本全部弄进去了才把kic起了起来</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/d8/708a0932.jpg" width="30px"><span>李一</span> 👍（5） 💬（1）<div>老师，请问 Ingress 工作在7层协议中，指针对http(s)应用层协议进行控制，那如果 我的应用是需要长链接的 不如IM通讯相关，那是不是Ingress就无法满足了，只能通过service 定义吗？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（4） 💬（1）<div>说一下我的感受，按照最新的理论来看，调用链路顺序是  ingress-control. ---&gt; ingress-class --&gt; ingress。

但实际上配置的时候，可以看到 ingress-control 配置了 ingress-class的引用，但ingress-class里却没有配置ingress，反而是ingress反向引用了ingress-class，即为  ingress-control. ---&gt; ingress-class &lt;--- ingress。

这种情况确实是反直觉的，我分析可能是  ingress-class 是后来提出的概念，为了兼容以前的  ingress-control --&gt; ingress 模型，才搞了ingress-class 这个缝合怪。</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（4） 💬（2）<div>为ingres-controller设置Service:
➜  ingress kubectl expose deploy nginx-kic-dep -n nginx-ingress --port=80 --target-port=80 $=out&gt;ingress-svc.yml

➜  ingress cat ingress-svc.yml     

apiVersion: v1
kind: Service
metadata:
  name: nginx-kic-svc
  namespace: nginx-ingress
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx-kic-dep
  type: NodePort

➜  ingress kubectl get svc -n nginx-ingress
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
nginx-kic-svc   NodePort   10.105.174.176   &lt;none&gt;        80:32519&#47;TCP   3m41s

➜  ingress kubectl get node -o wide        
NAME     STATUS   ROLES                  AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE           KERNEL-VERSION      CONTAINER-RUNTIME
ubuntu   Ready    control-plane,master   4d    v1.23.3   10.211.55.5   &lt;none&gt;        Ubuntu 22.04 LTS   5.15.0-58-generic   docker:&#47;&#47;20.10.12
worker   Ready    &lt;none&gt;                 4d    v1.23.3   10.211.55.6   &lt;none&gt;        Ubuntu 22.04 LTS   5.15.0-58-generic   docker:&#47;&#47;20.10.12

➜  ingress curl --resolve ngx.test:32519:10.211.55.5 http:&#47;&#47;ngx.test:32519
srv : 10.10.1.10:80
host: ngx-dep-6796688696-867dm
uri : GET ngx.test &#47;
date: 2023-02-09T15:10:48+00:00

➜  ingress curl --resolve ngx.test:32519:10.211.55.5 http:&#47;&#47;ngx.test:32519
srv : 10.10.1.11:80
host: ngx-dep-6796688696-psp5v
uri : GET ngx.test &#47;
date: 2023-02-09T15:10:50+00:00</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（4） 💬（3）<div>service方式如下：

apiVersion: v1
kind: Service
metadata:
  name: ingress-svc
  namespace: nginx-ingress
spec:
  selector:
    app: ngx-kic-dep
  ports:
  - port: 80
    targetPort: 80
  type: NodePort


请求 后面的端口要根据kubectl get svc -n nginx-ingress 查看

curl --resolve ngx.test:31967:127.0.0.1 http:&#47;&#47;ngx.test:31967</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/30/83badcc2.jpg" width="30px"><span>Albert</span> 👍（2） 💬（2）<div>service文件
apiVersion: v1
kind: Service
metadata:
  name: ngx-kic-svc
  namespace: nginx-ingress

spec:
  selector:
    app: ngx-kic-dep
  type: NodePort
  ports:
  - port: 8082
    targetPort: 80
    protocol: TCP
~                   

查看svc的ip后访问：
curl -H &quot;Host: ngx.test&quot; &quot;http:&#47;&#47;10.103.79.195:8082&quot;
</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（2） 💬（1）<div>我发现了一个问题，我是用了最新版的yml，从github拉的，没有直接用老师的，但是kic.yml文件就是使用老师贴出来的，然后运行起来，pod一直都是未READY和AVAILABLE，查看日志logs，报错：
Failed to watch *v1.Endpoints: failed to list *v1.Endpoints: endpoints is forbidden: User &quot;system:serviceaccount:nginx-ingress:nginx-ingress&quot; cannot list resource &quot;endpoints&quot; in API group &quot;&quot; at the cluster scope

我排查了很久，最后发现rabc文件规则异同，导致版本不兼容，不知道我猜测的对不对？
把老师的镜像文件 nginx&#47;nginx-ingress:2.2-alpine更换为nginx&#47;nginx-ingress:3.0.2
再次apply后，就一切正常OK了，没问题了。
总结：因没有拉老师提供的yml清单生成对应的对象，而是自己去github拉最新版本的yml生成对象，而镜像文件使用了老师提供，导致pod起不来。目测是版本对rabc规则的不兼容导致，不知道老师可以解答下吗？</div>2023-03-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（4）<div>老师，setup Ingress Controller 那里有个问题不知道如何解决，看到评论区里也有很多同学有一样的问题

$ kubectl logs ngx-kic-dep-75f4f5c7c-v9lt8 -n nginx-ingress
I0907 22:10:01.222921       1 main.go:213] Starting NGINX Ingress Controller Version=2.2.2 GitCommit=a88b7fe6dbde5df79593ac161749afc1e9a009c6 Date=2022-05-24T00:33:34Z Arch=linux&#47;arm64 PlusFlag=false
I0907 22:10:01.233010       1 main.go:344] Kubernetes version: 1.23.3
F0907 22:10:01.233818       1 main.go:357] Error when getting IngressClass ngx-ink: ingressclasses.networking.k8s.io &quot;ngx-ink&quot; is forbidden: User &quot;system:serviceaccount:nginx-ingress:default&quot; cannot get resource &quot;ingressclasses&quot; in API group &quot;networking.k8s.io&quot; at the cluster scope

pod 的状态是 CrashLoopBackOff

我是直接执行你 GitHub 上面的 setup.sh 脚本的，然后再执行 kic.yaml 的，所以 rbac.yaml 也是执行了的。或者说 rbac.yaml 文件中的参数需要更改？</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/92/4b/1262f052.jpg" width="30px"><span>许飞</span> 👍（2） 💬（2）<div>F0818 12:36:23.718350       1 main.go:357] Error when getting IngressClass ngx-ink: ingressclasses.networking.k8s.io &quot;ngx-ink&quot; is forbidden: User &quot;system:serviceaccount:nginx-ingress:default&quot; cannot get resource &quot;ingressclasses&quot; in API group &quot;networking.k8s.io&quot; at the cluster scope
老师这报错是为啥</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/30/5b/4f4b0a40.jpg" width="30px"><span>悟远</span> 👍（2） 💬（2）<div>老师，请问Ingress可以针对http2.0进行控制吗？如gRPC，我试验gPRC时通过kubectl port-forward映射到本地，再加hosts，访问gRPC时失败了</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：taint是在daemonset部分讲的，节点的taint会影响pod是否会部署到节点上。
但是，对于deployment，taint会影响吗？

Q2：第21讲最后一部分是搭建ingress controller。 这部分提到了五个yml文件。 是先执行前面四个，然后再执行最后一个来创建ingress controller吗？ 还是只执行“kubectl apply -f kic.yml”？ （如果先执行前面四个文件，这四个文件有顺序吗？）

Q3：github上的四个文件，看不到下载按钮。是因为没有登录吗？ 如果不是因为登录，是否能提供下载按钮？（现在的方法是拷贝文件内容，比较麻烦）

Q4：运行controller后，查看deploy和POD的状态都不正常。
先执行github上的四个文件，顺序是文中列出的顺序，创建都成功了。然后启动controller。
查看结果如下：
kubectl get pod -n nginx-ingress，状态是：CrashLoopBackOff
kubectl get deploy -n nginx-ingress： Ready是 0&#47;1
可能是什么原因？ （这个问题有点笼统，不太具体，老师给出一点建议即可。）</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9c/31/e4677275.jpg" width="30px"><span>潜光隐耀</span> 👍（2） 💬（4）<div>请问下，会不会介绍下gateway api？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>Chrono 老师，有两个小问题：

1.  ic 的缩写好理解，kic 这个缩写该怎么理解呢？

2. kubectl port-forward -n nginx-ingress ngx-kic-dep-8859b7b86-cplgp 8080:80 &amp; 。这个命令的 -n  nginx-ingress 代表的是哪个服务呢？ngx-kic-dep-8859b7b86-cplgp 是 ingress- controller 代表的容易名称。</div>2023-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/86/d689f77e.jpg" width="30px"><span>Hank_Yan</span> 👍（1） 💬（1）<div>如果参考了官网的步骤: https:&#47;&#47;docs.nginx.com&#47;nginx-ingress-controller&#47;installation&#47;installation-with-manifests&#47;   没有使用老师的 setup 脚本，那么步骤要严格按照官网来。 

包括 nginx&#47;nginx-ingress 版本。  用老师的 nginx&#47;nginx-ingress:2.2-alpine  。遇到503 错误，readinessProbe  地址 &#47;nginx-ready 无法访问到。 

最后全部按照官网操作，版本用 nginx&#47;nginx-ingress:3.2.0，问题解决了。</div>2023-08-10</li><br/><li><img src="" width="30px"><span>InfoQ_15df24517cff</span> 👍（1） 💬（1）<div>ingress和ingressclass不需要指定namespace吗</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/4d/7ba09ff0.jpg" width="30px"><span>郑童文</span> 👍（1） 💬（1）<div>请问老师， 既然已经在ingress class 里面指定了 controller, 为什么在controller里面还要指定ingress class呢？</div>2023-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/61/c3/791d0f5e.jpg" width="30px"><span>Arrow</span> 👍（1） 💬（2）<div>请问老师，我ingress 的规则似乎总是不生效，访问svc之后都是返回404，进controller的pod查看也只有个默认的配置，没有我ingress定义的规则，请问这个怎么排查解决</div>2023-06-17</li><br/><li><img src="" width="30px"><span>Geek_c16d38</span> 👍（1） 💬（2）<div>為什麼有點跳來跳去看不太懂 ？？？

是要從github下載 文件還是？？

因為本來就不好理解了 
又跳來跳去 不是很懂。。。？？
</div>2023-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep075ibtmxMf3eOYlBJ96CE9TEelLUwePaLqp8M75gWHEcM3za0voylA0oe9y3NiaboPB891rypRt7w/132" width="30px"><span>shuff1e</span> 👍（1） 💬（1）<div>比如，如果我要用 Nginx 开发的 Ingress Controller，那么就要用名字“nginx.org&#47;ingress-controller”，这里的nginx.org&#47;ingress-controller是怎么确定的？</div>2023-06-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Gtf3tMDmYRoCL9Eico52ciatacq4PUHfQ8icQIYKV6KLDAJyTa8ZnLXMKf05pEice5RnEagocFobca5zv8jwyPhNKA/132" width="30px"><span>Geek_9d43c0</span> 👍（1） 💬（1）<div>老师 我的node1节点的ip是10.0.4.14 因为我是公网部署的所以这个ip做了转发 转发到了我的node1的公网ip 我看我所有的pod只要部署在node1上的 kubectl get pod -o wide 都是 10.0.4.14 只有ingress的pod ip 如下
 nginx-ingress      ngx-kic-dep-5455fd7846-spglq              0&#47;1     CrashLoopBackOff   5 (71s ago)   7m14s   10.244.36.118    k8s-node1   
 describe pod之后看到的是   Warning  Unhealthy  2m27s (x22 over 2m47s)  kubelet            Readiness probe failed: Get &quot;http:&#47;&#47;10.244.36.118:8081&#47;nginx-ready&quot;: dial tcp 10.244.36.118:8081: connect: connection refused
 我理解是访问失败了 我开了node1的腾讯云的防火墙8081 但是还是失败  查了一下路由表发现master的路由表没有10.244.36.118 这个路由 想问一下我这种情况老师有什么解决经验吗 ip不是node的ip是因为ingress本身的特性导致的吗</div>2023-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/f7/d8/dc437147.jpg" width="30px"><span>So what?</span> 👍（1） 💬（3）<div>因为 Ingress Class 很小，所以我把它与 Ingress 合成了一个 YAML 文件

老师，这个意思是说把两个文件复制到一个文件里就可以了嘛</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（1） 💬（2）<div>老师，这节的ingress我反复学习，但一些概念还是比较模糊，麻烦指点一下：
1、【Nginx Ingress Controller】的安装和 【Ingress Controller】的部署是一回事吗？
2、是否 【Nginx Ingress Controller】 全局只用安装一次，【Ingress Controller】可以根据不同的服务部署多份？
3、是否 https:&#47;&#47;github.com&#47;chronolaw&#47;k8s_study&#47;blob&#47;master&#47;ingress&#47;setup.sh 命令只是安装 【Nginx Ingress Controller】？
4、是否【kind: Deployment】的ingress yaml文件可以部署不同服务的 ingress-control？但它们都指向setup.sh里配置的【Nginx Ingress Controller】？

5、是不是只部署 【kind: Deployment】的ingress yaml （配置的namespace自定义）就可以了，而无需安装 【Nginx Ingress Controller】？

有点绕哈，但【Nginx Ingress Controller】、【Ingress Controller】 这两个概念我感觉是不一致的。</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fd/30/83badcc2.jpg" width="30px"><span>Albert</span> 👍（1） 💬（1）<div>可能版本更新，建议按照官方教程来：https:&#47;&#47;docs.nginx.com&#47;nginx-ingress-controller&#47;installation&#47;installation-with-manifests&#47;

需要8个文件

kubectl apply -f common&#47;ns-and-sa.yaml
kubectl apply -f rbac&#47;rbac.yaml
kubectl apply -f common&#47;nginx-config.yaml
kubectl apply -f common&#47;default-server-secret.yaml

kubectl apply -f common&#47;crds&#47;k8s.nginx.org_virtualservers.yaml
kubectl apply -f common&#47;crds&#47;k8s.nginx.org_virtualserverroutes.yaml
kubectl apply -f common&#47;crds&#47;k8s.nginx.org_transportservers.yaml
kubectl apply -f common&#47;crds&#47;k8s.nginx.org_policies.yaml

其中rbac&#47;rbac.yaml建议使用最新版https:&#47;&#47;github.com&#47;nginxinc&#47;kubernetes-ingress&#47;blob&#47;main&#47;deployments&#47;rbac&#47;rbac.yaml，否则pod无法启动，报错：endpointslices.discovery.k8s.io is forbidden
</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（1） 💬（1）<div>罗老师，我现在遇到一个问题，使用 kubectl get pod 是可以看到pod的, 假设该pod的名称是poda, 使用 kubectl describe pod poda 也是可以看到正常信息的，使用docker exec -ti &lt;container-id&gt; sh 是可以进入该容器的， 但是使用 kubectl exec poda -- sh 提示 error: unable to upgrade connection: pod does not exist

我的环境是: Virtualbox 运行的两台 ubuntu 22.04, 使用的是 kubeadm, k8s=v1.23.3；
希望老师能给个思路，如何解决呢？</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/29/8b471f9d.jpg" width="30px"><span>半缘君</span> 👍（1） 💬（1）<div>每次都是在ignressController这里卡住，老师能详细讲一下吗，关于部署以及如何自己实现一个简单的ingressController。</div>2023-03-13</li><br/>
</ul>