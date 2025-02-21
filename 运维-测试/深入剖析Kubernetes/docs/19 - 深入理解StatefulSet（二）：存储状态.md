你好，我是张磊。今天我和你分享的主题是：深入理解StatefulSet之存储状态。

在上一篇文章中，我和你分享了StatefulSet如何保证应用实例的拓扑状态，在Pod删除和再创建的过程中保持稳定。

而在今天这篇文章中，我将继续为你解读StatefulSet对存储状态的管理机制。这个机制，主要使用的是一个叫作Persistent Volume Claim的功能。

在前面介绍Pod的时候，我曾提到过，要在一个Pod里声明Volume，只要在Pod里加上spec.volumes字段即可。然后，你就可以在这个字段里定义一个具体类型的Volume了，比如：hostPath。

可是，你有没有想过这样一个场景：**如果你并不知道有哪些Volume类型可以用，要怎么办呢**？

更具体地说，作为一个应用开发者，我可能对持久化存储项目（比如Ceph、GlusterFS等）一窍不通，也不知道公司的Kubernetes集群里到底是怎么搭建出来的，我也自然不会编写它们对应的Volume定义文件。

所谓“术业有专攻”，这些关于Volume的管理和远程持久化存储的知识，不仅超越了开发者的知识储备，还会有暴露公司基础设施秘密的风险。

比如，下面这个例子，就是一个声明了Ceph RBD类型Volume的Pod：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（80） 💬（6）<div>老师，由于无法追问，恳请能够回复详细一些。提前谢过了。
pvc的使用方式当中，对于由运维人员去创建pv，我始终有些疑问。
首先，一个pv对应一个pvc。如果实际绑定的pvc小于pv声明的存储大小，会造成存储的浪费吗？
其次，运维人员事先要创建多少个，以及多大容量的pv呢？因为并不清楚开发人员将来可能用多少1g的,10g的或者100g的pvc。创建的数量或大小不合适，会导致pv不够用。开发还是会来找运维的。
最后，如果回收方式是retain，那么pvc删除后，原来的pv并不会删除，如果开发人员想重新使用同一块存储，需要重建pv。这带来了很多运维工作。
所以，手动创建pv的最佳实践是怎样的呢？当然，如果用storage class去动态创建pv可以解决这件事，但是有时我们希望针对namespace创建属于自己的pv来限制存储的使用quota，而不得不用手动创建pv的模式。
</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/53/d4/d5596933.jpg" width="30px"><span>不知所措</span> 👍（26） 💬（3）<div>老师你好，statefulset 如果 不同的pod ，需要不同的配置，
比如说 zk集群，每个集群的myid 都是不同的，比如mysql集群每个主机的serverid 也是不同的，这种的怎么处理呢？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（18） 💬（4）<div>所以大体是Pod与PVC绑定，PVC与PV绑定，所以完成了Pod与PV的绑定?</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/ec/5da5c049.jpg" width="30px"><span>Terry Hu</span> 👍（15） 💬（5）<div>由于没有ceph server ，pv用hostPath方式，在master上创建了index.html，pv pvc都创建好了，bound上了，登陆容器后在&#47;usr&#47;share&#47;nginx&#47;html目录下死活找不到index.html，搞了一个小时。突然猛醒原来hostPath指的是worker节点的path......哎，蠢啊</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（15） 💬（1）<div>前辈，我有个疑问，我通过deployment创建一个pods，在podTemplate中我声明volume使用persistentVolumeClaim并指定我事先创建pvc name， 这个时候我删除pod， 同样当pod删除的时候并不影响我事先创建的这个pvc，我是不是可以认为deployment这种资源也是能保存存储状态的呢？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（14） 💬（1）<div>对于有些应用，比如关系数据库，它保存数据文件的位置必须严格符合POSIX接口，远程文件系统例如NFS对于类似锁定这样的操作支持的不好，即使是sqlite官方文档也不推荐用NFS。这种情况下，数据库应用好像只能用本地硬盘或者iSCSI的存储盘，这不就等同必须把重启的StatefulSet的Pod每次调度到同一个机器上才行吗？因为那个机器硬盘上的文件不会自动传输到其它机器上。是不是可以这么理解？</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/f3/fc992148.jpg" width="30px"><span>kitsdk</span> 👍（12） 💬（3）<div>pv对象不会绑定namespace吗？
命令 kubectl -n myns  delete pv --all --include-uninitialized 
执行完了，所有的pv也进入删除状态，当然因为有其他的pv绑定，没有立即删除。</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（12） 💬（1）<div>asdf100的问题应该是：一个集群中可能有很多个pv, pvc是如何找到他对应的pv的?

试着回答一下：
1、 指定了storageClassName的pv, 只有指定了同样storageClassName的pvc才能绑定到它上面。
2、对于没有指定storageClassName的pv,默认classname为&quot;&quot;, 同样只有没有指定classname的pvc才能绑定到它上面。
3、pvc可以用matchLabels和matchExpressions来指定标签完成更详细的匹配需求。
4、匹配成功应该还需要一些基本的存储条件吧，比如pvc申请的存储空间肯定不能大于指定的pv.

关于第四点没有验证过，用aws的efs可以动态扩展空间的，好像没有这些限制。请张老师详细解答一下。</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/43/15be800e.jpg" width="30px"><span>LQ</span> 👍（7） 💬（3）<div>在一个 Pod 里面有两个容器， 容器 a 里自己实现一个 fuse filesystem，将远程的文件（比如 hdfs 上的数据）mount 到该容器里，另外一个容器 b 通过什么方式能读取到容器 a 里 mount 的数据呢，通过 PV 吗？有啥解决方案没？</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（5） 💬（1）<div>如果一个stateful set的pod挂了，PV所在的机子被分配给了其他pod。那当stateful pod重新schedule的时候会不会出现PV所在机器资源不足导致无法schedule的情况？k8s是否针对这种问题有优化?</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/75/c812597b.jpg" width="30px"><span>yuliz</span> 👍（4） 💬（1）<div>storage: 1Gi，表示我想要的 Volume 大小至少是 1 GB；这里是笔误么？1Gi不等于1GB,如果这里是1G应该更符合语景</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（3） 💬（2）<div>老师您好，请问下只用Statefulset情况下，能做到指定编号的副本创建pvc，其他副本不创建pvc吗？还是说由Statefulset管理的副本必须有pvc呢？</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（3） 💬（3）<div>表示 nginx:1.9.1 里并没有 curl 命令.
通过 for i in 0 1; do kubectl exec -it web-$i -- curl localhost; done 无法获取到期待的结果.
通过
不知道其他小伙伴尝试过没有.
当然最终通过其他方式 比如之前的:
kubectl run -i --tty --image busybox:1.28.4 dns-test --restart=Never --rm &#47;bin&#47;sh
使用 wget 也是可以验证.
</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（2） 💬（1）<div>请问pvc声明的存储容量是多个pod副本share还是每一个独立的存储容量？</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/8b/3cc461b3.jpg" width="30px"><span>宋晓明</span> 👍（1） 💬（1）<div>我怎么感觉PV与PVC的关系就像LVM(逻辑卷管理)中的PV和VG的关系如出一辙呢？  也就是说PVC是在PV那么大的地盘里划出一小部分(PVC)供用户读写的，不知道理解的对不对？</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（0） 💬（1）<div>https:&#47;&#47;kubernetes.io&#47;blog&#47;2018&#47;04&#47;13&#47;local-persistent-volumes-beta&#47;
现在也开始支持本地pv了。看起来是用preempt缓解了一部分问题，但一些场景应该还会有问题</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/88/941e488a.jpg" width="30px"><span>hugeo</span> 👍（0） 💬（1）<div>最近两篇文章是都是看了两遍才明白，书读百遍其义自现，看来以后的文章估计要读更多遍了(^･ｪ･^)</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b9/99/ef60d90f.jpg" width="30px"><span>秋风扫落叶</span> 👍（59） 💬（3）<div>老师这个里面创建pv需要有ceph存储支持，大家做实验可以搞一个rook-ceph，两步创建一个ceph集群，很好用，官网： https:&#47;&#47;rook.io&#47;。</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/92/14/6ca50b3b.jpg" width="30px"><span>大G来了呦</span> 👍（30） 💬（5）<div>不使用ceph的话，可以按照hostPath来进行实验：
cat pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-test
  labels:
    name: pv-test
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  hostPath:
    path: &#47;test-volume
################
 cat sts.yaml
apiVersion: apps&#47;v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: &quot;nginx&quot;
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.9.1
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: &#47;usr&#47;share&#47;nginx&#47;html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes:
      - ReadWriteOnce
      storageClassName: manual
      resources:
        requests:
          storage: 1Gi
注意要在woker节点创建本地目录 &#47;test-volume
还有实验结果如下：
 kubectl get pv
NAME      CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
pv-test   1Gi        RWO            Recycle          Bound    default&#47;www-web-0   manual                  34m
[root@node1 pv]# kubectl get pvc
NAME        STATUS    VOLUME    CAPACITY   ACCESS MODES   STORAGECLASS   AGE
www-web-0   Bound     pv-test   1Gi        RWO            manual         5m31s
www-web-1   Pending                                       manual         5m28s
[root@node1 pv]# kubectl get po
NAME    READY   STATUS    RESTARTS   AGE
web-0   1&#47;1     Running   0          5m35s
web-1   0&#47;1     Pending   0          5m32s
# pending是由于 ReadWritOnce 只能让一个pod去挂载使用，而不是一个节点的多个pod挂载使用
</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/ea/10661bdc.jpg" width="30px"><span>kevinsu</span> 👍（18） 💬（4）<div>rook-ceph-mon的IP地址正确获取方式来自查阅rook官方文档，kubectl -n rook-ceph get service，非常重要！！！</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/71/81/4e47560f.jpg" width="30px"><span>pepezzzz</span> 👍（18） 💬（7）<div>原文中的PV创建不成功。
 spec.accessModes: Required value
 unknown field &quot;imagefeatures&quot; in io.k8s.api.core.v1.RBDPersistentVolumeSource
 unknown field &quot;imageformat&quot; in io.k8s.api.core.v1.RBDPersistentVolumeSource
修改后如下：
kind: PersistentVolume
apiVersion: v1
metadata:
  name: pv-volume
  labels:
    type: local
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce 
  rbd:
    monitors:
    - &#39;10.40.0.21:6789&#39; --修改为 kubectl get pods -n rook-ceph 查看 rook-ceph-mon- 开头的POD IP
    - &#39;10.32.0.10:6789&#39;
    - &#39;10.40.0.23:6789&#39;
    pool: kube
    image: foo
    fsType: ext4
    readOnly: false
    user: admin
    keyring: &#47;etc&#47;ceph&#47;keyring
</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/98/a29a006e.jpg" width="30px"><span>Devil May Cry.Samsara</span> 👍（16） 💬（0）<div>老师，文章有提到，即使pod删除，pvc和pc依然保留下来，这个地方是不是应该注明一下，应该是要受这个pv申明的回收策略影响的？因为之前踩过次坑，pod删除，把分配给mysql的pv里的数据也删除了。。。所以很在意这个</div>2018-12-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqZIqY4cs6YKI5w8pJmCge3G4YUV4hNW018A63iauwtLHgxnC9Mh4AZPI0QkYuq1dKVFDsw5BMRh4w/132" width="30px"><span>程序修行</span> 👍（16） 💬（1）<div>老师能每次给出本次讲解全套的实现命令吗？貌似每次复现都会花很多时间，还不知道为什么。这次就是不知道pv该怎么创建，为什么总是创建失败。</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/74/ea/10661bdc.jpg" width="30px"><span>kevinsu</span> 👍（12） 💬（7）<div>我用ubuntu完全去按照之前的安装方法搞的环境，但是到持久化存储这块老是会有这个错：Warning  FailedMount             15s (x8 over 79s)   kubelet, izj6cbsxfhzowfxz65471sz  MountVolume.WaitForAttach failed for volume &quot;pv-volume&quot; : fail to check rbd image status with: (executable file not found in $PATH), rbd output: ()
超级郁闷</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a2/60/f3939ab4.jpg" width="30px"><span>哈哼</span> 👍（6） 💬（0）<div>rolling uodate 咋搞？</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/1c/730af0ad.jpg" width="30px"><span>佳期如梦</span> 👍（6） 💬（2）<div>有个疑问，之前Deployment是通过ReplicaSet，实现所谓的版本控制（回滚，蓝绿发布之类的）。那么StatefulSet之类部署的应用该怎么实现这些功能？</div>2019-01-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/YD1RqdHwfuNHSot5OcjlNhWiatJLmlhF47sUiczmzo0znLYvOpssdsqdlGKjUenXJzTG4eBR0bIJkJeUTibQ04Yqw/132" width="30px"><span>jking</span> 👍（3） 💬（1）<div>这里的Pv与pvc是怎么绑定的啊，看了模版，感觉没什么关联关系啊</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/f2/fee557fe.jpg" width="30px"><span>Mr.Cling</span> 👍（3） 💬（0）<div>如果创建了两个存储类型和存储空间都一样的PV， pvc是怎么决定绑定哪一个pv呢？ 随机选择一个吗？ 可不可能通过类似label的筛选？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/72/535199ed.jpg" width="30px"><span>xieshiyi</span> 👍（2） 💬（0）<div>为什么有状态应用不驱逐？有反例吗？感觉驱逐也没问题。求解答</div>2018-11-24</li><br/><li><img src="" width="30px"><span>Geek_674dce</span> 👍（1） 💬（1）<div>Rook-ceph 最近集群有所更新，按照老师yaml文件创建的pod会出现无法挂载的情况，搭建rook-ceph集群步骤可以参考github上的快速启动指南访问或者查看官方文件rook.io，切记搭建集群需要为每个台机器添加硬盘加载rbd模块，具体使用步骤可以参看deploy&#47;examples&#47;csi&#47;storageclass.yaml 和 example下的mysql.yaml文件
</div>2022-04-18</li><br/>
</ul>