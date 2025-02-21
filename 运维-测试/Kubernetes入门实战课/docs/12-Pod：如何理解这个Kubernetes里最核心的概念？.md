你好，我是Chrono。

前两天我们学习了Kubernetes世界里的工作语言YAML，还编写了一个简短的YAML文件，描述了一个API对象：Pod，它在spec字段里包含了容器的定义。

那么为什么Kubernetes不直接使用已经非常成熟稳定的容器？为什么要再单独抽象出一个Pod对象？为什么几乎所有人都说Pod是Kubernetes里最核心最基本的概念呢？

今天我就来逐一解答这些问题，希望你学完今天的这次课，心里面能够有明确的答案。

## 为什么要有Pod

Pod这个词原意是“豌豆荚”，后来又延伸出“舱室”“太空舱”等含义，你可以看一下这张图片，形象地来说Pod就是包含了很多组件、成员的一种结构。

![图片](https://static001.geekbang.org/resource/image/06/ba/0608d5d450c503c4102af27518d15bba.png?wh=800x533 "图片来自网络")

容器技术我想你现在已经比较熟悉了，它让进程在一个“沙盒”环境里运行，具有良好的隔离性，对应用是一个非常好的封装。

不过，当容器技术进入到现实的生产环境中时，这种隔离性就带来了一些麻烦。因为很少有应用是完全独立运行的，经常需要几个进程互相协作才能完成任务，比如在“入门篇”里我们搭建WordPress网站的时候，就需要Nginx、WordPress、MariaDB三个容器一起工作。

WordPress例子里的这三个应用之间的关系还是比较松散的，它们可以分别调度，运行在不同的机器上也能够以IP地址通信。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（77） 💬（1）<div>思考题

1. 可以把 Pod 看作是介于容器之上的一层抽象，之所以需要这一层抽象是因为容器与容器之间有着不确定的关系，有的容器需要与彼此隔离，而有的容器却需要彼此交互。当容器规模增大，容器之间的作用关系就会变得极其复杂，难于管理。Pod 的出现就是为了解决容器管理的问题，让大规模应用下的容器编排变得更加清晰有序，易于维护

2. 不管是容器还是 Pod，都是虚拟概念。把普通进程或应用加上权限限制就成了容器，再把容器加上权限限制就成了 Pod。说白了，就是不断地抽象封装，这也是软件中解决复杂问题的唯一手段。容器之于Pod，就好比 线程之于进程、函数之于类、文件之于文件夹等等</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b5/46/2ac4b984.jpg" width="30px"><span>三溪</span> 👍（36） 💬（3）<div>我这里补充下个人遇到的坑，希望对大家有所帮助！
当你使用kubectl apply -f指定YAML文件来创建pod时，只要你spec.containers.image里面的tag是latest，那么无论你的imagePullpolicy策略是什么，无论本地是否已存在该镜像文件，一定会先联网查询镜像信息，如果此时正好是私网无法连接互联网时，那么pod就会直接创建失败，你使用describe查询时报错也是无法拉取镜像。
只要tag不是latest，比如stable或者1.23什么的具体版本，本地已存在对应镜像文件，这时设置为IfNotPresent和Never才会生效，就可以在私网环境下愉快地离线创建pod。</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/dc/badd82d7.jpg" width="30px"><span>江湖十年</span> 👍（15） 💬（2）<div>imagePullPolicy 默认值并非 IfNotPresent，而是 Always：

➜ kubectl explain pod.spec.containers.imagePullPolicy
KIND:     Pod
VERSION:  v1

FIELD:    imagePullPolicy &lt;string&gt;

DESCRIPTION:
     Image pull policy. One of Always, Never, IfNotPresent. Defaults to Always
     if :latest tag is specified, or IfNotPresent otherwise. Cannot be updated.
     More info:
     https:&#47;&#47;kubernetes.io&#47;docs&#47;concepts&#47;containers&#47;images#updating-images</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（13） 💬（1）<div>container 对象. env：定义 Pod 的环境变量
-------------
这里 不应该是 container 的环境变量吗？</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（11） 💬（5）<div>老师 ，一般情况下，pod里只定义一个容器吗？  还是可以定义多个容器。  它们之间没有什么区别吗？</div>2022-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mvvjzu4D1gJl8c9lnMMTatOou2EUsWCe4XiclyUOwk2rUawwqd6KKV8z9bSRMnD3ibQPUCIZUQOAkKAaKX0Ncaibw/132" width="30px"><span>Apple_d39574</span> 👍（7） 💬（1）<div>您好，想问一下，为什么要定义容器启动时要执行的命令？不设置会怎么样？</div>2022-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/7a/a9/279c0c39.jpg" width="30px"><span>Guder</span> 👍（6） 💬（1）<div>感觉pod有点像是docker-compose</div>2022-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/15/c4866257.jpg" width="30px"><span>咩咩咩</span> 👍（6） 💬（1）<div>1.若直接使用容器来管理应用，只能一个个容器去调度。应用之间一般都有进程和进程组的关系，而容器又只是单进程模型，无法管理多个进程
2.Pod是一组共享了某些资源的容器，只是一个逻辑概念</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（5） 💬（1）<div>个人观点，不知道对不对，我觉得pod就应该叫做k8s自己的容器，如果没有pod, k8s直接调度容器对象，比如docker, 那它就永远要依赖docker; 如果k8s不对容器包装一下，没有类似pod这种粒度的话，k8s就必须选择一种现有容器技术，限制了其现在和未来的灵活性。所以，于公于私，构建pod这个基本调度单元是非常明智的选择，将来如果有新的容器技术代替了docker，但是k8s的基本单元永远是pod</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/e7/0d/98e828c2.jpg" width="30px"><span>bjdz</span> 👍（3） 💬（1）<div>向老师请教一个问题，被折磨坏了，
docker images 显示本地是有 busybox:stable-glibc 这个版本的，yaml文件中的 imagePullPolicy: IfNotPresent，image: busybox:stable-glibc，
根据这个yaml文件创建pod，显示 pod&#47;busybox created，但是 kubectl logs busybox，就显示镜像拉取失败
Error from server (BadRequest): container &quot;busybox&quot; in pod &quot;busybox&quot; is waiting to start: trying and failing to pull image
不明白为什么本地已经有镜像了，且不是最新的tag，为什么还要去拉取镜像？

get pod报错：busybox   0&#47;1     CrashLoopBackOff   7 (4m47s ago)   22m

Events:
  Normal   Scheduled  28m                   default-scheduler  Successfully assigned default&#47;busybox to minikube
  Warning  Failed     24m                   kubelet            Failed to pull image &quot;busybox:stable-glibc&quot;: rpc error: code = Unknown desc = context canceled
  Warning  Failed     24m (x2 over 24m)     kubelet            Error: ErrImagePull
  Warning  Failed     24m                   kubelet            Failed to pull image &quot;busybox:stable-glibc&quot;: rpc error: code = Unknown desc = error pulling image configuration: Get &quot;xxx&quot;: net&#47;http: TLS handshake timeout
  Normal   BackOff    24m (x2 over 24m)     kubelet            Back-off pulling image &quot;busybox:stable-glibc&quot;
  Warning  Failed     24m (x2 over 24m)     kubelet            Error: ImagePullBackOff
  Normal   Pulling    24m (x3 over 28m)     kubelet            Pulling image &quot;busybox:stable-glibc&quot;
  Normal   Pulled     21m                   kubelet            Successfully pulled image &quot;busybox:stable-glibc&quot; in 2m20.001262902s
  Normal   Created    20m (x4 over 21m)     kubelet            Created container busybox
  Normal   Started    20m (x4 over 21m)     kubelet            Started container busybox
  Normal   Pulled     20m (x3 over 21m)     kubelet            Container image &quot;busybox:stable-glibc&quot; already present on machine
  Warning  BackOff    2m55s (x86 over 21m)  kubelet            Back-off restarting failed container</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/71/48/44df7f4e.jpg" width="30px"><span>凯</span> 👍（3） 💬（4）<div>想请教一下老师，除了您讲解的内容。我更想知道您学习k8s的路线，您是怎么做到到精通的。我也自己学习，可是学习的都是一下粗略的内容。您是精读k8s的文档么，参加k8s的开源项目贡献代码么？</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（1）<div>请教老师两个问题：
Q1:：YAML中可以定义多个POD吗？
Q2：k8s集群启动命令每次开机后都要执行吗？
       minikube start --kubernetes-version=v1.23.3，这个命令是启动k8s集群，
       现在好像每次重启虚拟机后都要执行该命令，必须执行吗？</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9c/31/e4677275.jpg" width="30px"><span>潜光隐耀</span> 👍（2） 💬（2）<div>请教下，kubectl exec -it podname -- sh报错，提示：

error: Internal error occurred: error executing command in container: failed to exec in container: failed to start exec &quot;xxx&quot;: OCI runtime exec failed: exec failed: unable to start container process: exec: &quot;sh&quot;: executable file not found in $PATH: unknown

这个错误该如何解决呢？</div>2022-08-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（2） 💬（1）<div>来回答下作业：
1. 如果没有 Pod，直接使用容器来管理应用会有什么样的麻烦？
Pod是一个或多个容器的集合，首先，如果Pod中运行的是单容器，则使用Pod包一层的好处是可以管理其中容器的状态如暂停、重启等（因Pod短暂的生命周期，不清楚这么做有什么好处，debug？），比如可以替换容器镜像；其次，如果Pod中运行的是多容器，则这些容器之间共享网络与存储，可以高效的分享资源与本地化服务调用，在调度方面，如果关联容器不使用Pod包一层则会增加调试的复杂度，影响性能，有了Pod则可以统一调度方便管理。

2. 你觉得 Pod 和容器之间有什么区别和联系？
Pod是一个或多个关联容器的组合，它是一逻辑概念，它要解决的是在资源隔离的容器之上，如何实现关联容器之间高效的共享网络与存储。
实现层面首先启动infra容器pause用来创建并保持网络空间，与Pod保持一致的生命周期，再启动业务容器加入到此NET空间，在docker运行时中同一Pod中的容器共享ipc&#47;net&#47;user&#47;uts等命名空间。
Pod与容器之间的关系类似于Linux进程组与进程的关系。</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（2） 💬（1）<div>🤣原来是网线，没有插好。不说了。接受惩罚去。找了半天。</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/52/56dbb738.jpg" width="30px"><span>牙小木</span> 👍（1） 💬（1）<div>pod是个中间层，因为container千差万别，所以没有什么不是通过加一个中间件不能解决的。如果是，那就再加一层中间层。</div>2023-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（1） 💬（1）<div>我遇到了拉取镜像失败的问题，原因是 docker 仓库限频
Error from server (BadRequest): container &quot;busy&quot; in pod &quot;busy-pod&quot; is waiting to start: trying and failing to pull image
解决办法是，通过 minikube ssh 登录到节点上面去，使用 docker login 登录自己的账户。免费账户 6 小时 200 次，足够用了。</div>2023-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/97/a9/e3b097f1.jpg" width="30px"><span>蜘蛛侠</span> 👍（1） 💬（1）<div>可以这样理解嘛，Pod是不是就是把docker-compose 创建的多个容器放在了一个“房间”</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>思考题:
----------

1、容器用来隔离，Pod（容器组）用来协作。

2、容器的最佳实践是：内部只有一个进程。如果有多个，其中某个进程挂了，外界也没法知道哪出了问题。

一般来说，我们平常开发的应用服务，都是通过非亲密的方式来完成交互的，即跨节点的网络通信，这种情况下使用容器或 pod 来实现差异不大。

3、但总有一些场景，我们需要让两个服务来协同完成一些事情，比如应用服务产生的日志，需要另一个服务收集上来，然后 push 到日志中心。
云原生时代以前，它们就在同一台机器上，具备天生的亲密性，此时将它们绑起来就是最优解。因为使用相同的网络空间、存储空间、主机及域名空间、IPC 空间等，是进程间协作效率最高的方式。

如果此时依然通过容器来管理，kubernetes 根据各个节点资源情况，将它们分配到不同节点的概率会非常高，这无疑是不可取的。</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，有几个小问题。

1. 用标签 env=dev&#47;test&#47;prod，使用标签 region: north&#47;south，tier=front&#47;middle&#47;back，这里的等于号和冒号有什么区别吗？

2. kubectl delete -f busy-pod.yaml，这里的“yaml” 是不是应该写成 “yml”。</div>2022-07-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（1） 💬（1）<div>1.直接用容器管理会让我们管理容器变得很复杂，每一个容器的配置我们都要用一长串配置信息对容器进行管理和配置，而且容器间的通信貌似也是一个大问题？
2.pod就像收纳箱，里面装了不同类型的物品（容器，当我需要的时候直接找到对应的箱子打开就好。</div>2022-07-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（1） 💬（1）<div>pod.spec.containers中的command与arg分别对应Dockerfile中的ENTRYPOINT与CMD，查资源对比其不同之处有：
1. 可用形式不同，前者只有array的形式，类似于exec form，后者还有shell form，即在command中如果需要使用到shell需要显式指定如&#47;bin&#47;sh。
2. 环境变量引用方式不同，前者可以通过&#39;$(env_varname)&#39;的方式引用pod.spec.conainers.env中给定的变量，但后者需要在exec form中显式指定shell，并使用&#39;${env_varname}&#39;来引用ENV中设定的环境变量，注意两者引用的形式不同，后者是标准的shell变量引用写法，前者不是。</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（1） 💬（1）<div>提示我， image  can&#39;t  be  pulled怎么解决呀？</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/dc/d0c58ce5.jpg" width="30px"><span>闲渔一下</span> 👍（1） 💬（1）<div>1.通常应用之间存在超亲密关系，如果只按容器去管理，就把它们割裂开来了，调度的时候只能按一个个容器去调度，而有了pod，可以按照一组容器这样去调度
2.pod是一个逻辑概念，由容器组成</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/4d/f2/768daf2d.jpg" width="30px"><span>syc的猫</span> 👍（0） 💬（1）<div>思考题1：如老师所说，但还有一些特殊情况，多个应用结合得非常紧密以至于无法把它们拆开。比如，有的应用运行前需要其他应用帮它初始化一些配置，还有就是日志代理，它必须读取另一个应用存储在本地磁盘的文件再转发出去。这些应用如果被强制分离成两个容器，切断联系，就无法正常工作了。直接用容器管理应用会导致 当应用所需的服务增多时，容器规模增大，容器之间的作用关系就会变得十分复杂，难以管理。pod的存在就是为了在虚拟机和容器之间找到一个合适的粒度来管理容器，易于维护。
问题2：不管是容器还是 Pod，都是虚拟概念。把普通进程或应用加上权限限制就成了容器，再把容器加上权限限制就成了 Pod。说白了，就是不断地抽象封装，这也是软件中解决复杂问题的唯一手段。容器之于Pod，就好比 线程之于进程、函数之于类、文件之于文件夹等等。</div>2024-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/20/116db076.jpg" width="30px"><span>MrZhaoCn</span> 👍（0） 💬（1）<div>老师您好，我这边在我的mac 机器上使用minikube 搭建的环境，然后我这边遇到的问题是我本机的工作目录无法挂载到Pod里面，可以确定的是我本机的目录存在，使用kubuctl apply部署pod ，pod得镜像能正常访问，请问知道什么原因吗？
下面是pod得配置
apiVersion: v1
kind: Pod
metadata:
  name: code-server-pod
spec:
  containers:
  - name: code-server-apph5pay
    image: codercom&#47;code-server:4.20.0
    command: [&quot;code-server&quot;, &quot;--auth&quot;, &quot;none&quot;, &quot;--bind-addr&quot;, &quot;0.0.0.0:8080&quot;, &quot;&#47;home&#47;coder&#47;project&quot;]
    ports:
    - containerPort: 8080
    volumeMounts:
    - mountPath: &#47;home&#47;coder&#47;project
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      path: &#47;Users&#47;xxx&#47;home&#47;workspace&#47;ide&#47;projects&#47;AppH5Pay
      type: DirectoryOrCreate</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/d3/7e/38f506dd.jpg" width="30px"><span>Delight</span> 👍（0） 💬（1）<div>pod是一个api对象，pod是豌豆荚，主要为解决启动多个容器，以应对多应用的场景；在YAML文件中的spec.containers可以定义多个容器实例，然后apply。执行kubectl get pod 可以看到启动的容器有REDAY字段有多个。
执行kubectl cp命令时，可以将文件拷贝到pod中，但是如果pod里面有多个容器，要怎么指定拷贝到其中的一个容器呢？
百度资料如下：
kubectl cp命令将文件拷贝到Pod中指定容器的文件系统中，默认情况下会选择Pod中的第一个容器作为目标。您可以使用-c或--container选项来指定要拷贝文件的目标容器。例如，使用以下命令将文件拷贝到名为container-a的容器中：

kubectl cp &#47;local&#47;file&#47;path pod-name:&#47;container-a&#47;file&#47;path -c container-a</div>2023-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（0） 💬（1）<div>关于pod内多container共享netns, uts namespace, storage, 应该还有IPC namespace把</div>2023-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（0） 💬（1）<div>请问下老师 metadata里的labels字段有什么用？</div>2023-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/LL8H5v0z7nNwasWIw47JKiagC1JFtu6XgN4ZkBtkRD81mQVD74OSicGWg6AjCYia81RMjCDBVqqN1hd6gNXybPxpA/132" width="30px"><span>Mintisama</span> 👍（0） 💬（1）<div>求教
在执行kubectl describe pod ngx的时候，拉取镜像报错

 Failed to pull image &quot;nginx:alpine&quot;: rpc error: code = Unknown desc = Error response from daemon: Get &quot;https:&#47;&#47;registry-1.docker.io&#47;v2&#47;library&#47;nginx&#47;manifests&#47;sha256:2452715dd322b3273419652b7721b64aa60305f606ef7a674ae28b6f12d155a3&quot;: net&#47;http: TLS handshake timeout</div>2022-11-05</li><br/>
</ul>