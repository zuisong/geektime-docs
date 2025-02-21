你好，我是张磊。今天我和你分享的主题是：PV、PVC体系是不是多此一举？从本地持久化卷谈起。

在上一篇文章中，我为你详细讲解了PV、PVC持久化存储体系在Kubernetes项目中的设计和实现原理。而在文章最后的思考题中，我为你留下了这样一个讨论话题：像PV、PVC这样的用法，是不是有“过度设计”的嫌疑？

比如，我们公司的运维人员可以像往常一样维护一套NFS或者Ceph服务器，根本不必学习Kubernetes。而开发人员，则完全可以靠“复制粘贴”的方式，在Pod的YAML文件里填上Volumes字段，而不需要去使用PV和PVC。

实际上，如果只是为了职责划分，PV、PVC体系确实不见得比直接在Pod里声明Volumes字段有什么优势。

不过，你有没有想过这样一个问题，如果[Kubernetes内置的20种持久化数据卷实现](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#types-of-persistent-volumes)，都没办法满足你的容器存储需求时，该怎么办？

这个情况乍一听起来有点不可思议。但实际上，凡是鼓捣过开源项目的读者应该都有所体会，“不能用”“不好用”“需要定制开发”，这才是落地开源基础设施项目的三大常态。

而在持久化存储领域，用户呼声最高的定制化需求，莫过于支持“本地”持久化存储了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/99/bb/90d97247.jpg" width="30px"><span>shaobo</span> 👍（1） 💬（3）<div>k8S部署kfk，es可以用local persistent  volume吗</div>2018-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（0） 💬（1）<div>如果是容器化的kubelet要如何解决本地PV的问题，因为发现kubelet写的数据，都写在了容器里了，而没有在宿主机上。</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/dd/3b594e8d.jpg" width="30px"><span>realc</span> 👍（75） 💬（0）<div>知其然，知其所以然。很多教程教材，就跟上学时学校直接灌给我们一样，要让我们去硬啃。不如老师这课程，一个知识点，一个功能的来龙去脉、前世今生都给讲的清清楚楚的。</div>2018-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（68） 💬（4）<div>思考题，我的理解：
因为当一个pvc创建之后，kubernetes因为dynamic provisioning机制会调用pvc指定的storageclass里的provisioner自动使用local disk的信息去创建pv。而且pv一旦创建，nodeaffinity参数就指定了固定的node。而此时，provisioner并没有pod调度的相关信息。
延迟绑定发生的时机是pod已经进入调度器。此时对应的pv已经创建，绑定了node。并可能与pod的调度信息发生冲突。
如果dynamic provisioning机制能够推迟到pod 调度的阶段，同时考虑pod调度条件和node硬件信息，这样才能实现dynamic provisioning。实现上可以参考延迟绑定，来一个延迟 provision。另外实现一个controller在pod调度阶段创建pv。

</div>2018-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（18） 💬（0）<div>思考题：
因为dynamic provision机制不知道pod需要在哪个node下运行，而提前就创建好了，，</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（7） 💬（0）<div>Dynamic Provisioning 提供的是自动创建PV的机制，会根据PVC来创建PV并绑定，而我们的延迟绑定是需要在调度的时候综合考虑所有的调度条件来进行PVC和PV的绑定并调度Pod到PV所在的节点，二者有冲突</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（7） 💬（0）<div>Dynamic Provisioning 是通过pvc 创建指定规格的pv, 而Local Persistent Volume 是先创建pv, 在创建pvc, 然后在pod创建的时候绑定pv和pvc；从语义上讲，Dynamic Provisioning 就不太可能支持延迟这种效果</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（5） 💬（0）<div>因为Dynamic Provisioning会自动创建PV，也就是说，在PVC创建后就根据StorageClass去自动创建PV并绑定了，而“延迟绑定”发生在调度Pod时，此时PVC已经创建了。因此二者是矛盾的~~</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/ae/c082bb25.jpg" width="30px"><span>大星星</span> 👍（3） 💬（1）<div>手动删除pv的步骤中，1234步骤，为什么不是1342呢</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/45/fc03d0cf.jpg" width="30px"><span>海。</span> 👍（2） 💬（3）<div>如果不是Local Persistent Volume， 而使用云块存储 aws ebs ， “延迟绑定”和 Dynamic Provisioning 可以不冲突吧？ 我看https:&#47;&#47;github.com&#47;kubernetes-sigs&#47;aws-ebs-csi-driver&#47;blob&#47;master&#47;examples&#47;kubernetes&#47;dynamic-provisioning&#47;specs&#47;storageclass.yaml 的volumeBindingMode也是 WaitForFirstConsumer</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/be/18/ecac08dc.jpg" width="30px"><span>阿伦</span> 👍（0） 💬（0）<div>有一点疑惑，重启的pod，是如何保证自己一定启动在之前关联的PV机器上的，上面的例子说pod只能运行在2节点上，那如果没有这个限制，被部署在了1机器上，然后写了数据之后，pod重启，运行到2机器上了，那1机器上的PV有数据持久化又有什么意义呢？</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/a5/abb7bfe3.jpg" width="30px"><span>要没时间了</span> 👍（0） 💬（0）<div>Dynamic Provisioning 这个机制，关键是在于，如果它最终的结果是仅有一个合法的PV以及底层的持久化目录， 这就反向影响了Pod Schduling的决定，相当于可被调度的候选节点只有一个了。

要不然，就在多个，甚至集群全部节点都创建好相应的local PV。这样可以一定程度，或者彻底消除调度失败的可能。

否则，就只能在volume创建的时候想办法，在scheduler里面实现相应的通过调用CSI 的API创建volume的逻辑。

后者所谓的“动态创建”的方式，虽然可能，但是是不适合放在 scheduler里面的。scheduler按照责任划分来说，不应该再对资源进行修改了，以为她本身就是一个根据现有资源情况做调度决定的组件。

通过上面的考虑，如果资源充足，那就在集群出划分出一个专门可以使用local volume的节点池，在上面每一个节点都创建相应的PV。否则，感觉是没办法解决这个冲突的</div>2022-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/T7sFX0O4Tdwic8RUolZVe4hNPDiaiaxsfGD4qCBsmac8Iqcibe23Y3jEOQyTic7hsYn46ETeC56jhJ4nFOdOsEZxchw/132" width="30px"><span>loser</span> 👍（0） 💬（0）<div>只有几个G那种怎么挂载一个单盘呢？</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2f/03/0be37ebd.jpg" width="30px"><span>Lccc</span> 👍（0） 💬（1）<div>如果PVC支持扩展nodeAffinity字段, 是不是就可以解决延迟绑定了, StorageClass在读取到新增PVC后, 直接创建指定node的PV并进行Bound</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6b/e2/f02e45df.jpg" width="30px"><span>恰同学少年。</span> 👍（0） 💬（0）<div>&quot;需要注意的是，我们上面手动创建 PV 的方式，即 Static 的 PV 管理方式，在删除 PV 时需要按如下流程执行操作：删除使用这个 PV 的 Pod；从宿主机移除本地磁盘（比如，umount 它）；删除 PVC；删除 PV。&quot;


请问这里为什么不按这个顺序就会失败？我在k8s环境实践了以下两种方式也可以删除成功。
方案一：只不过这里可能的问题是在删除pv pvc的窗口期pod读写会有异常？
- 删除PV
- 删除PVC
- 删除Pod

方案二：
- 删除PVC
- 删除Pod
- 删除PV</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/6b/9ee9f422.jpg" width="30px"><span>wx</span> 👍（0） 💬（0）<div>思考题: 
1. Static Provisioning 的pv 是提前创建好的，调度器在调度pod时，一方面可以考虑nodeAffinity等调度需求，另一方面也能通过已有pv信息知道 pv的空间够不够。所以pv绑定pvc 可以放在Pod调度后进行。
2. Dynamic Provisioning，最大的问题: 无法提前知道节点 空间够不够。
情况一: 如果让Pod先调度到节点上之后，再通过 storageClass 创建pv绑定pvc，很有可能 节点本地磁盘空间 都不够了。
情况二: 如果先让 storageClass 创建pv绑定pvc，再调度Pod，pvc所在的节点信息 和 Pod 需要的节点信息 产生冲突。

求老师给 正确解答</div>2021-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/20/ca/2b0f69bc.jpg" width="30px"><span>SmartsYoung</span> 👍（0） 💬（1）<div>请问这个错误是什么原因呢？
Warning  FailedScheduling  62s (x2 over 64s)  default-scheduler  0&#47;1 nodes are available: 1 node(s) didn&#39;t match Pod&#39;s node affinity&#47;selector.
</div>2021-07-11</li><br/><li><img src="" width="30px"><span>Geek_5baa01</span> 👍（0） 💬（0）<div>目前的的控制器已经支持自动扫描目录创建 PV，延迟绑定还是一样，这是pod 调度规则限制，在使用 statefulset 时 k8s 会根据你使用的 stroage class 去找的已经具备 local pv 的node运行，那么其实也有一些dynamic 的特性了</div>2021-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJtl3p4gcguAZy580SyoQAic79Z7QAvTcibnicV9K8x2Yzbxa8BlknwhquzTPPklaWPDDbrECQG3uurg/132" width="30px"><span>lumence</span> 👍（0） 💬（0）<div># 有人说，文章中的例子跑不起来，可能是因为在主节点上创建了，本地卷的原因。
# 一下示例 亲测有效

apiVersion: v1
# PV 类型
kind: PersistentVolume
metadata:
  # PV 的名字
  name: example-pv
spec:
  capacity:
    # 分配 1G 空间
    storage: 1Gi
  # 允许直接挂载到容器的某个目录下
  volumeMode: Filesystem
  # 读写模式 = 只能被单个节点以读写的方式映射
  accessModes:
  - ReadWriteOnce
  # 磁盘空间回收策略 = 删除 PV 时删除里面的数据
  persistentVolumeReclaimPolicy: Delete
  # 指定存储类名字
  storageClassName: local-storage
  # 指定卷路径，就是宿主机上要被挂载的目录
  local:
    path: &#47;mnt&#47;disks&#47;vol1
  # 因为上面读写模式设置成只能一个节点访问
  # 所以这里要选择，哪个节点可以访问
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io&#47;hostname
          operator: In
          # 主机名，这里选择了master节点，所以创建 Pod 需要设置容忍度
          values:
            - kubernetes-master

---

kind: StorageClass
apiVersion: storage.k8s.io&#47;v1
metadata:
  name: local-storage
# no-provisioner 表示，必须手动创建 PV 实例，K8s 不支持自动创建
provisioner: kubernetes.io&#47;no-provisioner
# 延迟绑定。延迟到调度 Pod 的时候再决定 PV 和 PVC的 绑定关系
volumeBindingMode: WaitForFirstConsumer

---

kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: example-local-claim
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: local-storage

---

kind: Pod
apiVersion: v1
metadata:
  name: example-pv-pod

spec:
  # 使用 nodeSelector 选择主节点
  nodeSelector:
    &quot;kubernetes.io&#47;hostname&quot;: kubernetes-master
  volumes:
    - name: example-pv-storage
      persistentVolumeClaim:
       claimName: example-local-claim
  containers:
    - name: example-pv-container
      image: busybox
      command: [&quot;sh&quot;, &quot;-c&quot;]
      args:
      # 每隔 500 秒追加一行内容到 &#47;data&#47;log&#47;x.log
      - while true; do
          echo &quot;x&quot; &gt;&gt; &#47;data&#47;log&#47;x.log;
          sleep 500;
        done;
      # 将 PV 挂载到当前容器的 &#47;data&#47;log 目录
      volumeMounts:
        - mountPath: &quot;&#47;data&#47;log&quot;
          name: example-pv-storage
  # 容忍在主节点上运行此 Pod
  tolerations:
        - key: node-role.kubernetes.io&#47;master
          effect: NoSchedule
</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/01/5aaaf5b6.jpg" width="30px"><span>Ben</span> 👍（0） 💬（0）<div>思考题
Dynamic Provisioning不会考虑pv所在node, 而Local Persistent Volume跟node绑定在一起</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>我总觉得PV才像是PVC的父类,给PVC提供了一些通用的&quot;属性&quot;去继承使用.一个PV下继承了好多个PVC共享&quot;父类&quot;的&quot;属性&quot;.且各自不同的&quot;实现&quot;-&gt;申请空间的大小等.</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/92/14/6ca50b3b.jpg" width="30px"><span>大G来了呦</span> 👍（0） 💬（1）<div>发现一个问题：在pvc设置requests的大小为 1Gi，不过在使用的时候发现容量依然是整个pv的大小，请问这个原因又是什么呢，是否和accessModes模式有关呢？
[root@node1 pv]# kubectl get pv
NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                         STORAGECLASS    REASON   AGE
example-pv   6Gi        RWO            Delete           Bound    default&#47;example-local-claim   local-storage            31m
[root@node1 pv]# kubectl get pvc
NAME                  STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS    AGE
example-local-claim   Bound    example-pv   6Gi        RWO            local-storage   31m</div>2020-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9d/ee/2d02a9c0.jpg" width="30px"><span>水哥</span> 👍（0） 💬（1）<div>这个local volume使用广泛，目前公司使用的k8s集群，底层分布式存储的设计，就使用了此功能</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/e8/12cb8e99.jpg" width="30px"><span>小松松</span> 👍（0） 💬（0）<div>我有一个问题想了解一下  pod使用pv后不断地向里面写数据  如果超出pv的容量该怎么办呢？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/fe/ab541300.jpg" width="30px"><span>小猪</span> 👍（0） 💬（1）<div>pod挂载ceph rbd的存储pvc，当pod所在节点主机出故障宕机后，pod被自动调度到其他节点，但是原pod处于terminated状态，无法彻底删除，导致pvc没释放，新的pod无法使用这个pvc，进而新pod不能启动！这种情况如何解决？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/46/7f9af8de.jpg" width="30px"><span>寻</span> 👍（0） 💬（0）<div>请教一下，动态创建的存储卷如何扩容？</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bc/2a/00a3d488.jpg" width="30px"><span>Guol</span> 👍（0） 💬（0）<div>听你的课就跟听王立群讲史记一样。逻辑性强，每次听懂一点就感觉很爽。</div>2019-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（0） 💬（0）<div>张老师可以的，思考题的答案就在本章的“第二个男难点在于：”里面，不用自己总结，差点想破脑袋~</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（0） 💬（0）<div>延迟绑定之所以会和Dynamic Provisioning冲突？顾名思义，是因为后者不存在延迟的情况，即在PV、PVC匹配后，查看状态STATUS字段不是Pending（等待调度后在绑定的状态），而直接处于Bound状态。由于local Persistent Volume调度延迟的机制，所以两者有冲突。若理解有偏差，请张老师批评指正。</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/65/3b4a2930.jpg" width="30px"><span>lpf32</span> 👍（0） 💬（0）<div>动态模式下，pvc请求才会创建pv，从直觉上两者应该是绑定关系。但是local需要延迟绑定，会产生冲突。可以把pv的实际产生也推迟到调度阶段。</div>2018-12-28</li><br/>
</ul>