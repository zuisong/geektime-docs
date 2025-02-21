你好，我是Chrono。

在前面这么多节的课程中，我们都是在研究如何使用各种API对象来管理、操作Pod，而对Pod本身的关注却不是太多。

作为Kubernetes里的核心概念和原子调度单位，Pod的主要职责是管理容器，以逻辑主机、容器集合、进程组的形式来代表应用，它的重要性是不言而喻的。

那么今天我们回过头来，在之前那些上层API对象的基础上，一起来看看在Kubernetes里配置Pod的两种方法：资源配额Resources、检查探针Probe，它们能够给Pod添加各种运行保障，让应用运行得更健康。

## 容器资源配额

早在[第2讲](https://time.geekbang.org/column/article/528640)的时候我们就说过，创建容器有三大隔离技术：namespace、cgroup、chroot。其中的namespace实现了独立的进程空间，chroot实现了独立的文件系统，但唯独没有看到cgroup的具体应用。

cgroup的作用是管控CPU、内存，保证容器不会无节制地占用基础资源，进而影响到系统里的其他应用。

不过，容器总是要使用CPU和内存的，该怎么处理好需求与限制这两者之间的关系呢？

Kubernetes的做法与我们在[第24讲](https://time.geekbang.org/column/article/542376)里提到的PersistentVolumeClaim用法有些类似，就是容器需要先提出一个“书面申请”，Kubernetes再依据这个“申请”决定资源是否分配和如何分配。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（27） 💬（1）<div>思考题：
1. 
Liveness 和 Readiness 都是循环探测，Liveness 探测失败会重启，而 Readiness 探测失败不会重启，可以从 Pod 状态 看出重启次数。
两者都可以单独使用，这时差异不大。
如果同时使用两者，Liveness 主要是确认应用运行着或者说活着，而 Readiness 是确认应用提供着服务或者说服务就绪着（可以接收流量）。

2. 
Shell 是从容器内部探测，TCP Socket 和 HTTP GET 都是在容器外部探测。 TCP Socket 基于端口的探测，端口打开即成功；HTTP GET 更丰富些，可以是端口 + 路径。
</div>2022-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/d9/cf061262.jpg" width="30px"><span>新时代农民工</span> 👍（25） 💬（1）<div>老师请问，Startup、Liveness、Readiness三种探针是按顺序执行还是并行呢？</div>2022-08-26</li><br/><li><img src="" width="30px"><span>邵涵</span> 👍（9） 💬（1）<div>如老师原文所示，在startupProbe或livenessProbe探测失败之后，pod的status初始都是running。不过，在容器重启几次之后，pod的status会变为CrashLoopBackOff

如果startupProbe和livenessProbe探测成功，readinessProbe探测失败，pod的ready一直是0&#47;1，status一直是running，当然，也不会重启
NAME            READY   STATUS    RESTARTS   AGE
ngx-pod-probe   0&#47;1     Running   0          27m</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/e1/f663213e.jpg" width="30px"><span>拾掇拾掇</span> 👍（6） 💬（2）<div>Shell：不用知道端口；TCP Socket、HTTP GET这2个都得知道端口，用的时候还得显示调用端口吧</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（4） 💬（1）<div>思考题
1.  liveness 和 readiness 探针分别代表程序正常运行和可以提供服务。要探索两者的区别就要看应用在这两种状态下的差异，即在程序运行和提供服务之间，差了些什么。程序正常运行，可能代表代码没有 bug，没有硬性的致命的问题，但是要让它达到可以提供服务的程度，还需要一些条件，比如：启动时可能需要缓存预热，这个阶段可能就是 liveness 成功但 readiness 失败。可能 pod 的负载过大，需要进行降级，这就需要将 readness 从成功改成失败。
所以可能两种探针失败也有不同的含义：liveness 失败代表应用运行出现比较致命问题，需要重启来续命。readiness 失败代表程序不太健康，这种不健康是可以恢复的。
2. 三种探测方式应用的使用情境不同吧，shell 是在操作系统层面上的探测，毕竟跑起来的业务代码不方便（可能也不应该？）关心 OS。TCP Socket 关心的是网络，关心的是不同进程间的基础通信？http Get 是在应用层面上的探测，感觉它应该和业务的关联比较紧密。

忽然感觉 kubernetes 真厉害，三种探针和三种探测方式，基本上可以检测出各个层面的问题。</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（3） 💬（2）<div>Liveness指的是进程是否存在，Readiness则是指是否能够正常提供服务，所以可以使用tcp&#39;协议检测Liveness，进程存在端口即存在，使用http检测服务，只有服务启动了参能够相应请求。

Shell是系统内进程级别交互，所以只能够本地访问，Tcp可以跨机器访问，但是访问的级别比较低，不能够获得顶层数据，Http是协议层数据，可以拿到应用层的服务信息，但是关注顶层信息，底层故障，顶层无法提供有价值信息了</div>2023-02-03</li><br/><li><img src="" width="30px"><span>Geek_2ce074</span> 👍（3） 💬（1）<div>老师 tcpSocket探测是由谁发起的</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（3） 💬（1）<div>&quot;postStart&quot;&#39;&quot;preStop&quot;感觉可以做CICD，或者各种webhock钩子，或者简单的通知</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：第27讲中，创建4个nginx实例，没有端口冲突问题吗？
四个nginx实例，两个在master，两个在worker。同一台机器上有两个pod，而pod的定义是一样的，即端口相同，那么，不存在端口冲突问题吗？

Q2：第27讲中，创建四个nginx实例后，不能访问nginx的欢迎页。
service也创建了。 用虚拟机上浏览器来访问127.0.0.1，失败，
执行“kubectl port-forward svc&#47;ngx-svc 8080:80 &amp;”以后，
浏览器上访问127.0.0.1:8080，报错：
E0826 14:32:28.734987   42769 portforward.go:391] error copying from local connection to remote stream: read tcp4 127.0.0.1:8080-&gt;127.0.0.1:59752: read: connection reset by peer

Q3：nginx的配置文件中，竖线是什么意思？
data: default.conf: |， 这里的竖线是什么意思？ 

Q4：操作系统能够看到的CPU，是指逻辑核吗？还是时间片？</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>Startup，启动探针，用来检查应用是否已经启动成功，适合那些有大量初始化工作要做，启动很慢的应用。Liveness，存活探针，用来检查应用是否正常运行，是否存在死锁、死循环。
Readiness，就绪探针，用来检查应用是否可以接收流量，是否能够对外提供服务。
--- 
startupProbe        探测失败-会重启:  
	状态: ContainerCreating -&gt; 
			Running状态--&gt; CrashLoopBackOff状态(重启过程中看到有在2个状态横跳, ContainerCreating不确定没看到)
	NAME                       READY   STATUS             RESTARTS      AGE
	ngx-pod-probe              0&#47;1     Running   		  1 (10s ago)   104s
	ngx-pod-probe              0&#47;1     CrashLoopBackOff   5 (10s ago)   104s

livenessProbe探测失败-会重启: 
	那么会持续默认5次重启(我试的默认是重启5次:RESTARTS=5), 这个过程中pod的状态会是变化Running , 重启次数完毕仍然未成功,那么状态会变成CrashLoopBackOff
	状态:  ContainerCreating -&gt; Running --&gt; CrashLoopBackOff
	READY:   1&#47;1 -&gt; 0&#47;1
	NAME                       READY   STATUS    RESTARTS     AGE
	ngx-pod-probe              1&#47;1     Running   2 (5s ago)   65s
	ngx-pod-probe              0&#47;1     CrashLoopBackOff   5 (8s ago)   3m48s

readinessProbe 探测失败 也会重启: 
	状态: Running --&gt; CrashLoopBackOff 
	READY:   0&#47;1

	NAME                       READY   STATUS              RESTARTS   AGE
	ngx-pod-probe              0&#47;1     ContainerCreating   0          2s
	ngx-pod-probe              0&#47;1     Running   1 (4s ago)   10s
	ngx-pod-probe              0&#47;1     CrashLoopBackOff   2 (6s ago)   20s
	ngx-pod-probe              0&#47;1     Running   3 (19s ago)   33s
	ngx-pod-probe              0&#47;1     CrashLoopBackOff   5 (38s ago)   2m12s</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/76/3db69173.jpg" width="30px"><span>onepieceJT2018</span> 👍（0） 💬（1）<div>探针失败了有什么发 alert 的集成方案吗 webhook 到 slack 微信 钉钉 之类</div>2023-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/5a/45a56b3a.jpg" width="30px"><span>WenjieXu</span> 👍（0） 💬（1）<div>老师，如果一个pod需要加入到service中，是否意味着必须要配置readinessProbe？还是默认不配置的话，k8s会认为是up的，放到对应service的ep对象里？</div>2023-04-22</li><br/><li><img src="" width="30px"><span>Geek_60e02d</span> 👍（0） 💬（2）<div>请教下Pod启动后，什么时候会加入service的负载均衡列表？是startup probe成功后吗？然后readyness probe失败后，会从service中移除，那么，是不是说，startup probe成功到readyness失败期间，流量会进入这个没有ready的Pod呢</div>2023-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZicRP0FZ78kT68wEGeWzPnxrF4s3Ea36XdMA2pj2TAbU3eibVt7KqzS5B7LbWMhRfSc3XEUL3Hrjw/132" width="30px"><span>liubiqianmoney</span> 👍（0） 💬（1）<div>Cgroup除了限制CPU和内存资源外，可以限制磁盘IOPS吗？</div>2022-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（1）<div>终于有人把三种probe给讲清楚了，很赞</div>2022-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（0） 💬（1）<div>老师，有一个疑问，这些探针请求是由k8s发起的，是不是都是在容器外部对容器进行访问的呢，还是说实际上是由容器内自己负责对自己进行健康检查。
，</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（1）<div>老师好，我这个yml文件使用探针，直接给我显示&#47;var&#47;run&#47;nginx.pid timeout，但是实际上又是running状态，所以不太理解，请教一下老师是什么情况
apiVersion: apps&#47;v1
kind: Deployment
metadata:
  name: nginx-deployment
  annotations:
    kubernetes.io&#47;change-cause: update to v18 ngx=latest
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2
  minReadySeconds: 15
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-config
          mountPath: &#47;etc&#47;nginx&#47;conf.d
        resources:
          requests:
            cpu: 1m
            memory: 100Mi
          limits:
            cpu: 1m
            memory: 200Mi
        startupProbe:
          periodSeconds: 1
          exec:
            command: [&quot;cat&quot;, &quot;&#47;var&#47;run&#47;nginx.pid&quot;]

        livenessProbe:
          periodSeconds: 10
          tcpSocket:
            port: 80

        readinessProbe:
          periodSeconds: 5
          httpGet:
            path: &#47;ready
            port: 80
      volumes:
      - name: nginx-config
        configMap:
          name: ngx-conf </div>2022-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ec/f6/f615ed26.jpg" width="30px"><span>一路小跑</span> 👍（0） 💬（1）<div>请教老师2个问题啊：
1.如果还想追加几个自定义的健康检查的类型，应该从哪个方面入手好呢?
2. 另外，针对健康检查失败的处理预案，可以自定义么，需要学习哪个API对象？（比如用go做一些定制）</div>2022-09-25</li><br/>
</ul>