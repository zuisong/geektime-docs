你好，我是Chrono。

我们的“中级篇”到今天马上就要结束了，感谢你这段时间坚持不懈的学习。

作为“中级篇”的收尾课程，我照例还是会对前面学过的内容做一个全面的回顾和总结，把知识点都串联起来，加深你对它们的印象。

下面我先梳理一下“中级篇”里讲过的Kubernetes知识要点，然后是实战演示，搭建WordPress网站。当然这次比前两次又有进步，不用Docker，也不用裸Pod，而是用我们新学习的Deployment、Service、Ingress等对象。

## Kubernetes技术要点回顾

Kubernetes是云原生时代的操作系统，它能够管理大量节点构成的集群，让计算资源“池化”，从而能够自动地调度运维各种形式的应用。

搭建多节点的Kubernetes集群是一件颇具挑战性的工作，好在社区里及时出现了kubeadm这样的工具，可以“一键操作”，使用 `kubeadm init`、`kubeadm join` 等命令从无到有地搭建出生产级别的集群（[17讲](https://time.geekbang.org/column/article/534762)）。

kubeadm使用容器技术封装了Kubernetes组件，所以只要节点上安装了容器运行时（Docker、containerd等），它就可以自动从网上拉取镜像，然后以容器的方式运行组件，非常简单方便。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（8） 💬（1）<div>使用http:&#47;&#47;wp.test&#47;访问,需要在host改wp-kic-dep部署的那个节点的ip才可以</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（7） 💬（2）<div>以下是我在进行操作时遇到的坑，给大家填一下：
1. 在运行 nginx controller 的时候，pod 的状态一直不是 running，查看日志最后显示的是 bind() to 0.0.0.0:80 failed (13: Permission denied)。经过查资料发现，这是因为在运行 pod 的时候会桥接宿主机的 80 端口，而 80 端口是受保护的。解决办法是在 securityContext 中添加 allowPrivilegeEscalation: true，即可以进行特权升级。（https:&#47;&#47;github.com&#47;nginxinc&#47;kubernetes-ingress&#47;issues&#47;3932）
2. 不管你用什么设备访问 wp.test，请关掉科学上网软件，否则可能 502</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（7） 💬（3）<div>因为前面几节都是按照文稿来演练，坑都踩完了，本节很轻松完成。
作业：
1. 直接可以由 deployment 改编一下：修改 Kind，移除 replicas ； 根据需要添加 tolerations 设置。
2. 为 Ingress Controller 创建 Service 对象，用YAML样板来实现吧
```bash
kubectl expose deploy wp-kic-dep --port=80,443 --type=NodePort --name=wp-kic-svc -n nginx-ingress $out
```
大概的 YAML 
```yaml
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30080
  - name: https
    port: 443
    protocol: TCP
    targetPort: 443
    nodePort: 30443
```
记得移除 ingress controller deployment 里的 `hostNetwork: true`。
现在就可以愉快地访问 https:&#47;&#47;wp.test:30443&#47; 。
</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（5） 💬（2）<div>关于hostNetwork方式，分享一点，就是hostNetwork这种形式虽然可以让外界访问到，但是你一定要让外界机器通过域名，这里是“wp.test”能够路由到这台机器，当然这个很简单，只要在&#47;etc&#47;hosts里面添加一条记录就可以，但是wp.test要映射到哪一台机器？开始我在这个地方卡了好久，以为配置的是master机器，但是其实不是，应该是ingress controller的pod部署的那台机器，通过命令（kubectl get pod -n nginx-ingress -o wide）可以查看到pod是部署的机器，然后决定映射的ip；

这一点文章中有提到，但是容易忽略。</div>2023-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（4） 💬（1）<div>改成DaemonSet只需要把kind的Deployment变成DeamonSet、把replicas注释掉就可以</div>2022-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（2）<div>老师，22讲最后一步，就是创建nginx controller失败，POD状态是“CrashLoopBackOff”。用logs命令查看，错误信息是：
Error when getting IngressClass wp-ink: ingressclasses.networking.k8s.io &quot;wp-ink&quot; is forbidden: User &quot;system:serviceaccount:nginx-ingress:nginx-ingress&quot; cannot get resource &quot;ingressclasses&quot; in API group &quot;networking.k8s.io&quot; at the cluster scope

不知道是什么意思？不知道怎么修改？ （能看懂英文，但不知道说的是什么） （注：kic文件是拷贝老师的，https:&#47;&#47;github.com&#47;chronolaw&#47;k8s_study&#47;blob&#47;master&#47;ch3&#47;wp-kic.yml   完全拷贝，成功创建）</div>2022-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d2/00/9a247b1e.jpg" width="30px"><span>jason</span> 👍（3） 💬（2）<div>老师，wp.test这个域名需要指定ingress controller那个pod所在的节点ip，而ingress controller是通过deployment来管理的，pod重建时可能会被部署到别的节点，这样不是又要改host配置了吗？想问一下生产环境是怎样解决这个问题的。</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a0/ab/5f43eee8.jpg" width="30px"><span>笨晓孩</span> 👍（3） 💬（1）<div>老师，我部署完wp-svc之后，通过nodeIP:30088的方式没办法访问Wordpress页面，采用的是nodeport的方式</div>2022-10-27</li><br/><li><img src="" width="30px"><span>Geek_2ce074</span> 👍（3） 💬（1）<div>老师你好，Ingress Controller 对象，在哪个 Nginx 项目的示例 YAML 里有呀，根本找不到呀</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/88/e8deccbc.jpg" width="30px"><span>romance</span> 👍（3） 💬（6）<div>老师，数据库配置没问题，svc也正常，但访问网站时提示 Error establishing a database connection，不知道什么原因</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/9f/d2/b6d8df48.jpg" width="30px"><span>菲茨杰拉德</span> 👍（2） 💬（2）<div>配置hosts后，解析出来的还是ingress的ip，在七层负载不还是相当于用的ip来访问的吗？这个解析过程不是k8s做的吧。
我原来理解的是七层负载走http，通过域名来访问。输入域名后，k8s解析然后找到四层的ip和端口然后请求。</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>如果你使用的是 minikube 来搭建本节的实验环境，可以参考这里来在macOS本地通过域名访问服务：https:&#47;&#47;github.com&#47;kubernetes&#47;minikube&#47;pull&#47;12089</div>2023-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/9a/561e9d74.jpg" width="30px"><span>chengyi</span> 👍（1） 💬（1）<div>不过 Ingress Controller 本身也是一个 Pod，想要把服务暴露到集群外部还是要依靠 Service。Service 支持 NodePort、LoadBalancer 等方式，但 NodePort 的端口范围有限，LoadBalancer 又依赖于云服务厂商，都不是很灵活。
折中的办法是用少量 NodePort 暴露 Ingress Controller，用 Ingress 路由到内部服务，外部再用反向代理或者 LoadBalancer 把流量引进来。
请问这两段话的区别是什么，不太理解。</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（1） 💬（5）<div>我加上ingress controller后启动，报了这个错，能帮看下是什么原因么：
NGINX Ingress Controller Version=3.1.0 Commit=057c6d7e4f2361f5d2ddd897e9995bcb48ed7e32 Date=2023-03-27T10:15:43Z DirtyState=false Arch=linux&#47;amd64 Go=go1.20.2
I0404 10:41:32.746481       1 flags.go:294] Starting with flags: [&quot;-nginx-configmaps=nginx-ingress&#47;nginx-config&quot; &quot;-ingress-class=wp-ink&quot;]
I0404 10:41:32.761875       1 main.go:234] Kubernetes version: 1.23.3
I0404 10:41:32.771440       1 main.go:380] Using nginx version: nginx&#47;1.23.3
E0404 10:41:32.773053       1 main.go:753] Error getting pod: pods &quot;wp-kic-dep-7d46fd4f8d-mnxpk&quot; is forbidden: User &quot;system:serviceaccount:nginx-ingress:nginx-ingress&quot; cannot get resource &quot;pods&quot; in API group &quot;&quot; in the namespace &quot;nginx-ingress&quot;
2023&#47;04&#47;04 10:41:32 [emerg] 12#12: bind() to 0.0.0.0:80 failed (13: Permission denied)</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/07/22dd76bf.jpg" width="30px"><span>kobe</span> 👍（1） 💬（2）<div>我这个ingress controller启动后没成功，一直在不断的创建pod，如下：
wp-kic-dep-545dffd6d7-2n9cq    0&#47;1     SysctlForbidden   0          48s
wp-kic-dep-545dffd6d7-2zkh2    0&#47;1     SysctlForbidden   0          65s
wp-kic-dep-545dffd6d7-4f42q    0&#47;1     SysctlForbidden   0          20s
wp-kic-dep-545dffd6d7-4vxlw    0&#47;1     SysctlForbidden   0          53s
wp-kic-dep-545dffd6d7-6vshx    0&#47;1     SysctlForbidden   0          8s
wp-kic-dep-545dffd6d7-6zgx7    0&#47;1     SysctlForbidden   0          60s
wp-kic-dep-545dffd6d7-85mjh    0&#47;1     SysctlForbidden   0          46s
wp-kic-dep-545dffd6d7-88jcn    0&#47;1     SysctlForbidden   0          55s
wp-kic-dep-545dffd6d7-8mfjp    0&#47;1     SysctlForbidden   0          35s
wp-kic-dep-545dffd6d7-8z5ps    0&#47;1     SysctlForbidden   0          72s
wp-kic-dep-545dffd6d7-9bzgp    0&#47;1     SysctlForbidden   0          41s
wp-kic-dep-545dffd6d7-9v86q    0&#47;1     SysctlForbidden   0          15s
wp-kic-dep-545dffd6d7-c42rl    0&#47;1     SysctlForbidden   0          38s
wp-kic-dep-545dffd6d7-c8zx8    0&#47;1     SysctlForbidden   0          57s
wp-kic-dep-545dffd6d7-ccjfm    0&#47;1     SysctlForbidden   0          7s
wp-kic-dep-545dffd6d7-chwt9    0&#47;1     SysctlForbidden   0          16s
wp-kic-dep-545dffd6d7-crf4s    0&#47;1     SysctlForbidden   0          17s
wp-kic-dep-545dffd6d7-cx8bx    0&#47;1     SysctlForbidden   0          20s
wp-kic-dep-545dffd6d7-dc7w2    0&#47;1     SysctlForbidden   0          11s
wp-kic-dep-545dffd6d7-dzvvx    0&#47;1     SysctlForbidden   0          73s
wp-kic-dep-545dffd6d7-f72lj    0&#47;1     SysctlForbidden   0          66s
wp-kic-dep-545dffd6d7-gjdkz    0&#47;1     SysctlForbidden   0          27s</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（1） 💬（1）<div>apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  name: wp-kic-svc
  namespace: nginx-ingress
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30089
  selector:
    app: wp-kic-dep
  type: NodePort
status:
  loadBalancer: {}

老师，这是我写的Ingress Controller 的 Service 对象，之前用http:&#47;&#47;wp.test:30089 访问 
提示
该网页无法正常运作
wp.test 目前无法处理此请求。
HTTP ERROR 502

是因为我电脑开了vpn代理，然后关了就可以访问了，这个大家看看和我是否有同样的问题。</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（1） 💬（4）<div>apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  name: wp-kic-svc
  namespace: nginx-ingress
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30089
  selector:
    app: wp-kic-dep
  type: NodePort
status:
  loadBalancer: {}

老师，这是我写的Ingress Controller 的 Service 对象，用http:&#47;&#47;wp.test:30089 访问 提示拒绝连接   有什么排查思路吗？ hostNetwork: true 在wp-kic.yml我也注掉了。</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/9f/d2/b6d8df48.jpg" width="30px"><span>菲茨杰拉德</span> 👍（1） 💬（2）<div>kubeadm部署master和worker。跟实战演练中部署应用有啥区别。看命令行，老师是在minikube上演练这节课的吧</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/9f/d2/b6d8df48.jpg" width="30px"><span>菲茨杰拉德</span> 👍（1） 💬（2）<div>之前是搭建了k8s的master 和 worker。现在部署应用，在之前的虚拟机上建?那k8s怎么管理这些应用</div>2022-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/68/c299bc71.jpg" width="30px"><span>天敌</span> 👍（1） 💬（2）<div>老师，pod 启动启动不了，删除删除不了， describe 之后有如下报错：
failed to &quot;KillPodSandbox&quot; for &quot;f295ef40-d765-420b-b004-25d1b613ed3c&quot; with KillPodSandboxError: &quot;rpc error: code = DeadlineExceeded desc = context deadline exceeded
我该如何操作？</div>2022-10-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dotGbXAlAZg0bhCq4P96A40mdyavzR33jSqIHk8xLlic4B5PYNDIP5MEa1Fk9yxzdz9scHUM7IUNR71nVZNoV7Q/132" width="30px"><span>yhtyht308</span> 👍（1） 💬（3）<div>我的Ingress Controller正常运行了，不过打开网页出错: 404 Not Found 下面一行显示nginx&#47;1.21.6。问题可能出在哪？</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ed/3a/ab8faba0.jpg" width="30px"><span>陶乐思</span> 👍（1） 💬（5）<div>部署完wordpress设置后遇到问题：
http:&#47;&#47;192.168.1.29:30088&#47;
无法访问此网站192.168.1.29 拒绝了我们的连接请求。

192.168.1.29是Putty ssh到vm的ip地址，请问这个地址不对吗？应该用其他地址？</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/2e/df74d56a.jpg" width="30px"><span>起司猫</span> 👍（0） 💬（1）<div>碰到了一个问题：访问网站时提示 Error establishing a database connection。然后我把我已经创建的pod 都手动用 ‘kubectl delete pod’删除，重新生成了 pod 以后，数据库连接就正常了。然后才想起来，我在第一次kubectl apply -f wp-dep.yml 的时候，确实在 wp-cm 里面配错了密码，后面修改过来重新 kubectl apply 了，但是因为用的不是 volume挂载的，所以已生成的 pod 里面的PASSPORT 并不会动态更新。</div>2024-08-27</li><br/><li><img src="" width="30px"><span>Geek3524</span> 👍（0） 💬（1）<div>Hi 老师，

我可以在浏览器上通过worker node的地址访问到wp，但是master node的ip不行，这是正常的吗？</div>2024-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>测试了一下 pod用  hostNetwork: true可以跟节点宿主机绑定 但是这是随机行为 不知道跟哪个节点绑定</div>2024-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fb/f2/fe7f7add.jpg" width="30px"><span>你真是个爱xio习的好孩子呀👳</span> 👍（0） 💬（1）<div>Error from server (NotFound): error when creating &quot;wp-kic.yaml&quot;: namespaces &quot;nginx-ingress&quot; not found， 不知道为什么</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/fb/f2/fe7f7add.jpg" width="30px"><span>你真是个爱xio习的好孩子呀👳</span> 👍（0） 💬（1）<div>老师你好，我在配置ingress 和ingress-controller的时候，并没有created service&#47;wp-kic-svc 这个pod，导致后面的工作没办法进行</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/9a/561e9d74.jpg" width="30px"><span>chengyi</span> 👍（0） 💬（1）<div>我用safari浏览器无法访问，换成chrome就可以了，这似乎也是一个坑</div>2023-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8c/bf/182ee8e6.jpg" width="30px"><span>周Sir</span> 👍（0） 💬（1）<div>最新的nginx-ingress的 default-server-secret跑到哪里去了</div>2023-06-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/tjZDHOybO07lltibjmDiaQKdpE1C3ul9c9wmUWwnVohS5fSEOPcfK2d9ZvKEHu6ibMLXYNUSrA23w08Ty5MFYMfzA/132" width="30px"><span>Geek_ec6229</span> 👍（0） 💬（1）<div>访问：https:&#47;&#47;wp.test&#47;wp-admin&#47;install.php 页面显示：
Unable to connect

An error occurred during a connection to wp.test.

    The site could be temporarily unavailable or too busy. Try again in a few moments.
    If you are unable to load any pages, check your computer’s network connection.
    If your computer or network is protected by a firewall or proxy, make sure that Firefox is permitted to access the web.

查看ingress controller pod 日志显示：
27.0.0.1 - - [26&#47;Apr&#47;2023:14:28:32 +0000] &quot;GET &#47; HTTP&#47;1.1&quot; 302 0 &quot;-&quot; &quot;curl&#47;7.81.0&quot; &quot;-&quot;
127.0.0.1 - - [26&#47;Apr&#47;2023:14:29:21 +0000] &quot;GET &#47; HTTP&#47;1.1&quot; 302 0 &quot;-&quot; &quot;Mozilla&#47;5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko&#47;20100101 Firefox&#47;112.0&quot; &quot;-&quot;
求求帮忙看下什么问题
</div>2023-04-26</li><br/>
</ul>