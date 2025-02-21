你好，我是Chrono。

在中级篇里，我们学习了Deployment和DaemonSet两种API对象，它们是在Kubernetes集群里部署应用的重要工具，不过它们也有一个缺点，只能管理“无状态应用”（Stateless Application），不能管理“有状态应用”（Stateful Application）。

“有状态应用”的处理比较复杂，要考虑的事情很多，但是这些问题我们其实可以通过组合之前学过的Deployment、Service、PersistentVolume等对象来解决。

今天我们就来研究一下什么是“有状态应用”，然后看看Kubernetes为什么会设计一个新对象——StatefulSet来专门管理“有状态应用”。

## 什么是有状态的应用

我们先从PersistentVolume谈起，它为Kubernetes带来了持久化存储的功能，能够让应用把数据存放在本地或者远程的磁盘上。

那么你有没有想过，持久化存储，对应用来说，究竟意味着什么呢？

有了持久化存储，应用就可以把一些运行时的关键数据落盘，相当于有了一份“保险”，如果Pod发生意外崩溃，也只不过像是按下了暂停键，等重启后挂载Volume，再加载原数据就能够满血复活，恢复之前的“状态”继续运行。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（10） 💬（2）<div>Pod负责服务，Job负责调度，
Daemon&#47;Deployment负责无状态部署，StatefulSet负责状态部署，
Service负责四层访问（负载均衡、IP分配、域名访问），Ingress负责应用层（7层）访问（路由规则），
PVC&#47;PV负责可靠性存储。

K8s提供的解决方案基本就是代表了微服务部署的最佳实践了。</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（10） 💬（1）<div>好奇redis的主从，哨兵，cluster都是怎么在sts上实现的，打算抽个时间深入的学习一下。

btw，越学习越能理解到 老师讲的“云原生”的概念了</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（7） 💬（3）<div>老师，既然statefulSet对象管理的pod可以直接通过域名指定来访问，那可不可以 不给statefulSet对象创建service</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（5） 💬（1）<div>我感觉 statefulset 起到的作用相比于普通的 systemd 差不多，特别是对于数据库这种真正有状态的服务而言，实例运行的节点通常是固定的，因为对硬件的要求要比普通的节点高很多，且在生产环境不可能用任何基于网络的文件系统来存储数据库文件。由于节点固定，所以 ip 也就固定，没必要非用域名来访问，而且现在有些服务本来也实现了服务发现，客户端连接集群的任意实例都可以获取完整集群节点的 ip 就可以直连，改用域名反而不太直接，statefulset 也不能让主从配置或是sharding配置变得更方便。</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（5） 💬（1）<div>有了 StatefulSet 提供的固定名字和启动顺序，应用还需要怎么做才能实现主从等依赖关系呢？

答：我理解是采用StatefulSet对象管理多个（2n+1）有状态pod的情形下，应该在有状态应用中基于pod的固定名字进行实例通信交互，比如redis集群中节点之间通过Gossip协议进行广播自身的状态信息，从而完成实例之间依赖关系，保证集群的可用性</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（3） 💬（1）<div>老师 能讲解一下什么是operator吗？</div>2022-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（3） 💬（1）<div>作业：
1. 这个应该具体应用具体设置吧。比如 Redis ，需要给 主、从 实例加载不同的 conf 。以我目前的 kube 知识我不知道如何给不同的副本使用不同的配置文件。我只能使用临时命令实现主从 kubectl exec -it redis-pv-sts-1 -- redis-cli replicaof redis-pv-sts-0.redis-svc 6379 。
2. 若不使用“volumeClaimTemplates”内嵌定义 PVC，那么可能的后果就是，多个副本挂载同一个网络存储设备，这可能会导致数据丢失。</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/9e/e5/9e732ec1.jpg" width="30px"><span>泽</span> 👍（2） 💬（4）<div>老师 求您个事 ，讲讲helm吧，迫切想学</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/c3/775fe460.jpg" width="30px"><span>rubys_</span> 👍（2） 💬（1）<div>在我的虚拟机上 ping redis-sts-1.redis-svc 失败，一种解决方案是，kubectl get pod -o wide -n kube-system 找到 coredns 的 pod，然后删除那两个 pod，比如 kubectl delete pod coredns-65c54cc984-qlkt9 -n kube-system。等待 k8s 重新创建 coredns 的 pod 就可以 ping 了</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/da/29fe3dde.jpg" width="30px"><span>小宝</span> 👍（2） 💬（1）<div>“访问 StatefulSet 应该使用每个 Pod 的单独域名，形式是“Pod 名. 服务名”，不应该使用 Service 的负载均衡功能。”
请教老师，通常会在StatefulSet上创建一个Headless Service吧，作为pod的负载均衡。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/2e/df74d56a.jpg" width="30px"><span>起司猫</span> 👍（0） 💬（1）<div>说说自己的总结和理解（都 2024 了，还有人在学这个课程吗哈哈哈）：
1. StatefulSet 是被设计来用于管理有状态的应用的，而有状态的应用需要处理“启动顺序”、“依赖关系”、“网络标识”三个问题。
2. StatefulSet 通过 把 pod 的名称、pod 所在的主机名、 pod 域名进行了有规律的命名，通过 “[sts名]-[顺序号]”的方式对上述几个名称进行命名，使得用户能够通过 名称 和 顺序号 确认副本的身份和进行特定的处理。
3. StatefulSet 的场景下，不能通过 service 的域名去访问 pod，因为在有状态的一组应用中，访问的顺序、访问哪一个应用，应该是跟具体业务场景相关的，service 并不能帮你去做选择。
4. StatefulSet 的 pod 不需要分配 clusterIP，正如第 3 点中说的，用户要根据自己的业务场景去判断要访问哪个pod副本， 而 IP 不具备身份特征，并且原来 service 那样给 pod 分配 [对象名&#47;IP-local] 这种域名，同样不具备身份特征。这时候 headless-service 必须重新给 pod 分配具有身份特征的域名。</div>2024-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erRCf8vWbWibajdSaMtCM1OzPQ6uPhblgL4zXJvKoaQYVmialqFqr0NIdD6Dlm1F5icOBxiaXvUcQs4BA/132" width="30px"><span>sgcls</span> 👍（0） 💬（1）<div>1.容器启动脚本对环境变量（如 hostname）的不同取值，设定不同的启动参数，如 if hostname=redis-sts-0 时，添加 --master
2.使用独立定义的 PVC(kind: PersistentVolumeClaim)，生成的 pvc 名称就不是固定的了，Pod 重建后使用的 pvc 可能不是之前的 pvc，就出现了状态不一致（PV）</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/54/73cc7f73.jpg" width="30px"><span>王旧业</span> 👍（0） 💬（1）<div>有时候很难理解， 怎么这些API对象针对是否能够通过kubectl create创建yaml样本方面没有拉齐，做到一致多好哈</div>2024-07-27</li><br/><li><img src="" width="30px"><span>ray</span> 👍（0） 💬（1）<div>老师您好，
请问老师会建议把rdbms, redis, queue这类需要维护状态的服务放入k8s一起管理吗？
这类服务通常都需要放在特定规格的机器上，不像一般的pod比较能随意游移到不同节点。
虽说k8s可以匹配stateful set到特定节点，但我们仍需考虑cluster、备援、故障恢复等情境，加入这些考量后，就不太清楚是否该将上述服务放入k8s。
再麻烦老师解答～

谢谢老师＾＾</div>2023-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d3/07/5fc3c694.jpg" width="30px"><span>泰一</span> 👍（0） 💬（1）<div>老师，deployment 的 pod 没有稳定的域名，是不是就不能用用 headless svc了？（但是我看我们服务deployment也使用了 headles svc）</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d3/07/5fc3c694.jpg" width="30px"><span>泰一</span> 👍（0） 💬（1）<div>老师，想问下
是不是访问 headless svc，负载均衡到某个pod是通过k8s 的coreDNS 完成
而访问普通clusterIP 的svc，负载均衡是通过kube-proxy完成</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d3/07/5fc3c694.jpg" width="30px"><span>泰一</span> 👍（0） 💬（1）<div>“Service 原本的目的是负载均衡，应该由它在 Pod 前面来转发流量，但是对 StatefulSet 来说，这项功能反而是不必要的，因为 Pod 已经有了稳定的域名，外界访问服务就不应该再通过 Service 这一层了。所以，从安全和节约系统资源的角度考虑，我们可以在 Service 里添加一个字段 clusterIP: None ，告诉 Kubernetes 不必再为这个对象分配 IP 地址。”


老师，我想问下，如果应用A 通过  headless-service 访问应用B，不通过 service这一层做负载均衡了，那么应用 A 是怎么定位应用B的某个Pod的，这个过程能讲下么？

然后，我看k8s的文档，说访问headless服务，会返回一组pod地址列表，客户端自己做负载均衡了。
但是我们实际的服务，访问headless，直接就转发到某个pod了，和文档说的不一样，很迷惑。</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/29/895dbe3f.jpg" width="30px"><span>Leon</span> 👍（0） 💬（1）<div>老师，我发现StatefulSet里面的volumeClaimTemplates配置的PVC在用于多个POD时，容器中挂载的NFS文件系统是分别两个不同的pvc，这样两个redis中的数据还是分别隔离的，这样是正常的吗</div>2023-04-05</li><br/><li><img src="" width="30px"><span>庄颖</span> 👍（0） 💬（2）<div>老师，请问下文章最后的pvc挂载，直接使用deployment添加pvc挂载，删除对应的pod，或者删除deployment重建，只要对应的pvc名称不变，数据也不会变化啊。
这是不是意味着deployment和statefulset在使用pvc持久化数据时，是没什么去别的？</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/28/ca/47333d8b.jpg" width="30px"><span>lpqoang</span> 👍（0） 💬（1）<div>经过测试创建svc时候有个小坑，service的name必须和sts的serviceName一致，不然域名解析不到</div>2023-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（1）<div>将svc转换为headless service时，修改redis-svc.yml，添加clusterIP: None后，
执行kubectl apply -f redis-svc.yml更新svc时会报spec.clusterIPs[0]: Invalid value，
需要先将svc删除后重新apply才行，直接更新不起来。
</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b9/6f/b40d1acf.jpg" width="30px"><span>mkcaptain</span> 👍（0） 💬（1）<div>老师，有个疑问，今天讲解的中，如果固定域名绑定了pod，那结尾数字1的那个有什么作用呢？感觉一直都只会用0结尾的那个？</div>2022-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/30/5b/4f4b0a40.jpg" width="30px"><span>悟远</span> 👍（0） 💬（1）<div>老师好，我有个需求，想部署分布式爬虫环境，有什么方案可以让集群中所有副本同时启动执行任务吗？</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（1）<div>问题1： 想办法给这两个配置上配置文件，但感觉比较麻烦。 问题2： 不知道，我看答案说的是可能会多个挂载一个nfs，但如果是statefulset里面设置就不会发生这样的事情吗？

下面是一些总结和思考：
1. 有状态的状态，指的是启动顺序，机器标识和网络标识，网络标识是通过svc实现的。通过sts和svc的绑定，可以让pod拥有自己的域名，可以被直接访问到。
2. 有状态的状态对比起无状态服务，本质上来说，就是有更多的确定性，当一个deployment启动的时候，pod名称很多时候是随机的，但sts设置好以后，名称是固定的，hostname也是固定的，网络域名也是固定的，这些状态被固定住。
3. 有一个问题是，在docker-compose中，其实着一些东西也是固定的，无状态的设计是新加的，而有状态的服务是后面来的，依赖关系也在docker-compose中设计好，那么问题来了，为什么会有无状态服务，为什么不把所有服务都设计为有状态服务，我想的是不管有没有必要，都规范不就好了。</div>2022-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/23/81/3865297c.jpg" width="30px"><span>龙之大者</span> 👍（0） 💬（2）<div>执行了redis-pv-sts.yml，生产pvc一直是pending，然后报错如下

persistentvolume-controller  waiting for a volume to be created, either by external provisioner &quot;k8s-sigs.io&#47;nfs-subdir-external-provisioner&quot; or manually created by system administrator</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：怎么查询一个POD是通过什么创建的？
用“delete -f . ”来删除，发现只有最近的通过YAML创建的被删除，比如今天上午通过YAML创建了两个POD，用“delete -f . ”只删除了刚创建的这个sts，但以前通过deploy YAML创建的POD无法删除。为了删除其它POD,需要知道这个POD是通过什么创建的，请问：用哪个命令可以查看一个POD是通过什么创建的？
Q2：应用怎么控制启动顺序？
执行“kubectl apply -f redis-sts.yml”以后，两个POD被K8S启动了，已经启动了，应用还能控制启动顺序吗？
Q3：什么命令可以列出所有创建的对象？
目的是想查看以前创建的对象，各种类型的对象。是否有一个命令可以列出所有创建过得对象？
Q4：怎么判断console上安装的NFS server是否在运行，或者说怎么判断其状态？ Nfs version吗？同样，在client上，开机后怎么判断nfs client状态？（也许开机后自动运行？）</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/44/8df79d3c.jpg" width="30px"><span>事已至此开始撤退</span> 👍（0） 💬（4）<div>实践看这个，底层原理看张坤</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5e/1c/6b4e6aa5.jpg" width="30px"><span>K_Library争四狂魔</span> 👍（0） 💬（2）<div>老师您好。我理解的话WordPress实际上也是有状态的服务，它需要安装插件之后产生.php文件存放在PV里面。如果同一个WordPress实例两个节点，其中一个节点安装了WP插件，另一个节点也要同时变化（装上插件），这样的控制太复杂，所以我觉得WordPress是不适合用Service来启动多个实例的。
我觉得应该把WordPress应该跟背后的MySQL定义为同一组StatefulSet，一旦一个节点挂了，另一个节点可以读取MySQL和WordPress的文件启动之后恢复之前的状态。
您觉得有没有更好的WordPress部署方式？谢谢。</div>2022-08-22</li><br/>
</ul>