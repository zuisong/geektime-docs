你好，我是张磊。今天我和你分享的主题是：PV、PVC、StorageClass，这些到底在说啥？

在前面的文章中，我重点为你分析了Kubernetes的各种编排能力。

在这些讲解中，你应该已经发现，容器化一个应用比较麻烦的地方，莫过于对其“状态”的管理。而最常见的“状态”，又莫过于存储状态了。

所以，从今天这篇文章开始，我会**通过4篇文章为你剖析Kubernetes项目处理容器持久化存储的核心原理**，从而帮助你更好地理解和使用这部分内容。

首先，我们来回忆一下我在第19篇文章[《深入理解StatefulSet（二）：存储状态》](https://time.geekbang.org/column/article/41154)中，和你分享StatefulSet如何管理存储状态的时候，介绍过的Persistent Volume（PV）和Persistent Volume Claim（PVC）这套持久化存储体系。

其中，**PV描述的，是持久化存储数据卷**。这个API对象主要定义的是一个持久化存储在宿主机上的目录，比如一个NFS的挂载目录。

通常情况下，PV对象是由运维人员事先创建在Kubernetes集群里待用的。比如，运维人员可以定义这样一个NFS类型的PV，如下所示：

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: 10.244.1.4
    path: "/"
```

而**PVC描述的，则是Pod所希望使用的持久化存储的属性**。比如，Volume存储的大小、可读写权限等等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（358） 💬（17）<div>容器持久化存储涉及的概念比较多，试着总结一下整体流程。

用户提交请求创建pod，Kubernetes发现这个pod声明使用了PVC，那就靠PersistentVolumeController帮它找一个PV配对。

没有现成的PV，就去找对应的StorageClass，帮它新创建一个PV，然后和PVC完成绑定。

新创建的PV，还只是一个API 对象，需要经过“两阶段处理”变成宿主机上的“持久化 Volume”才真正有用：
第一阶段由运行在master上的AttachDetachController负责，为这个PV完成 Attach 操作，为宿主机挂载远程磁盘；
第二阶段是运行在每个节点上kubelet组件的内部，把第一步attach的远程磁盘 mount 到宿主机目录。这个控制循环叫VolumeManagerReconciler，运行在独立的Goroutine，不会阻塞kubelet主循环。

完成这两步，PV对应的“持久化 Volume”就准备好了，POD可以正常启动，将“持久化 Volume”挂载在容器内指定的路径。</div>2018-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLbswPFgMWmE28MQvjBHpAKg2Ny426dqRCgzp0ibyh0rr3nySEF621bWicySpAjATVEVyoibqloPqeLw/132" width="30px"><span>Geek_e2f5e1</span> 👍（40） 💬（1）<div>老师，如果我原先存储上就有数据需要挂载进去，那格式化操作岂不是不能满足我的需求？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（33） 💬（1）<div>张老师，问一个比较空泛的问题。您之前是做paas平台的，今后的pass平台的发展方向是什么呢？当前做paas平台，最大的阻碍是什么？最大的价值又是什么呢？</div>2018-10-27</li><br/><li><img src="" width="30px"><span>tuxknight</span> 👍（22） 💬（1）<div>在公有云上使用 PV&#47;PVC 有个很重要的限制：块存储设备必须和实例在同一个可用区。在 Pod 没被创建的时候是不确定会被调度到哪个可用区，从而无法动态的创建出PV。这种问题要怎么处理？</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/84/c1/dfcad82a.jpg" width="30px"><span>Acter</span> 👍（17） 💬（3）<div>“所谓将一个 PV 与 PVC 进行“绑定”，其实就是将这个 PV 对象的名字，填在了 PVC 对象的 spec.volumeName 字段上。” 
请问老师为什么在pvc的yaml文件中看不到这个字段呢？</div>2018-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/ea/ce9854a5.jpg" width="30px"><span>坤</span> 👍（10） 💬（1）<div>如果采用ceph  rbd StorageClass，Pod所在的node宕机后，在调度到另外一台Node上，这个过程中，k8s是会新node上重新创建PV吗？</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b4/0c/93fd5c51.jpg" width="30px"><span>jkmzg</span> 👍（7） 💬（1）<div>请问下从同一个pod spec 创建出来的不同pod中，pvc相同，会不会冲突？k8s的机制是什么呢？</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/75/c812597b.jpg" width="30px"><span>yuliz</span> 👍（7） 💬（3）<div>你好，我想请教下实际中的疑问点，如果我使用NFS作为共享存储，两个集群中的PV绑定NFS的同一目录，且这两个PV被pvc绑定，最终pod绑定pvc,当第二个pod绑定时会格式化nfs的目录，导致之前的pod数据丢失么？两个集群的pv能共用一个nfs目录和同一rbd么？</div>2018-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（6） 💬（1）<div>请问
1. 同一集群的多个pod可否同时挂载同一个pv的同一个subpath
2. 如果pv写满了如何扩容</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/a5/f8210f04.jpg" width="30px"><span>夕月</span> 👍（6） 💬（1）<div>所谓将一个 PV 与 PVC 进行“绑定”，其实就是将这个PV 对象的名字，填在了 PVC 对象的 spec.volumeName 字段上，这个好像在yaml文件里没有提现啊，只有storageClassName是一样的</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/08/c43f85d9.jpg" width="30px"><span>IOVE.-Minn</span> 👍（5） 💬（1）<div>请问，现在的NFS也是有storageclass也是可以动态配置pv的啊，但是在官方，体现的是没有的啊？这个是第三方开发的么？provisioner: fuseim.pri&#47;ifs</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（2） 💬（3）<div>文中提到attach 阶段是将远程盘挂载到宿主机上，这个操作不是应该在node 上做更合适吗？为啥会放在AD controller 中？</div>2018-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/b1/5aab73b3.jpg" width="30px"><span>阿川</span> 👍（2） 💬（1）<div>老师有一个问题需要请教，1、比如创建一个nfs的pv，但是nfs服务器不存在，此时pv也能创建成功。2、创建pvc也能跟pv关联。3、在真实创建pod使用该pvc会报错。这种情况有什么办法避免吗，比如在创建pv时就发现后端存储不存在</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/63/0112cc96.jpg" width="30px"><span>hhhhhh</span> 👍（2） 💬（1）<div>老师好，如果第二阶段肯定会格式化，那之前存储在volume中的数据不就丢失了？ </div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/61/00083e41.jpg" width="30px"><span>小白</span> 👍（1） 💬（1）<div>老师，scheduler里的volumezonechecker规则谷歌不到，可以贴个学习地址吗</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（1） 💬（1）<div>文章中为GCE 块存储 准备持久化目录第二阶段的挂载命令是不是应该用mount。创建目录不是之前kubelet已经做过了？</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>老师，现在这个方式其实要求Pod的存储信息在创建前就确定了，1.12的k8s说是支持挂载信息在宿主机和Pod，甚至Pod间互相感知，这个特性可信赖吗？</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f0/9e/cf6570f7.jpg" width="30px"><span>耀</span> 👍（21） 💬（0）<div>没有过度设计，如果没有PVC，那么用户声明就会有涉及到具体的存储类型；存储类型一旦变化了所有的微服务都要跟着变化，所以PVC和PV要分离。如果没有storageclass,那么PVC和PV的绑定就需要完全有人工去指定，这将会成为整个集群最重复而低效的事情之一，所以这种设计是刚好的设计。</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/66/e283b8b2.jpg" width="30px"><span>GR</span> 👍（8） 💬（6）<div>一个pv可以对应几个pvc，一对一吗？
可以创建一个大的pv然后每个应用有自己的pvc，存储路径通过subpath来区分，是否可行呢？</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/eb/77/ffd16123.jpg" width="30px"><span>重洋</span> 👍（4） 💬（0）<div>持久化存储的控制器 Volume Controller，kube-controller-manager 的一部分，运行在 master节点。其中包括控制循环 PersistentVolumeController、AttachDetachController。

PV、PVC匹配控制器 PersistentVolumeController ：执行控制循环，为每一个 PVC 遍历挑选可用的的 PV 进行绑定。
绑定：将 PV 对象的名字，填在 PVC 对象的 spec.volumeName 字段上。
匹配条件：
1.spec字段符合要求。
2.storageClassName一致。

Volume 类型是远程存储时：
一、远程存储挂载至宿主机(PV的准备流程)，分为两阶段：
第一阶段（Attach）（挂载磁盘）：AttachDetachController 不断地检查每一个 Pod 对应的 PV 和这个 Pod 所在宿主机之间挂载情况。从而决定，是否需要对这个 PV 进行 Attach（或者 Dettach）操作，为虚拟机挂载远程磁盘。Kubernetes 提供的可用参数是 nodeName，即宿主机的名字。
第二阶段（Mount）（mount至宿主机）：VolumeManagerReconciler，执行mount操作（必须发生再Pod宿主机上，所以是 kubelet 组件的一部分），将磁盘设备格式化并挂载到 Volume 宿主机目录。Kubernetes 提供的可用参数是 dir，即 Volume 的宿主机目录。
$ mount -t nfs &lt;NFS服务器地址&gt;:&#47; &#47;var&#47;lib&#47;kubelet&#47;pods&#47;&lt;Pod的ID&gt;&#47;volumes&#47;kubernetes.io~&lt;Volume类型&gt;&#47;&lt;Volume名字&gt; 

二、Pod 与持久化Volume宿主机目录挂载：
kubelet 为 Volume 创建的默认宿主机目录：&#47;var&#47;lib&#47;kubelet&#47;pods&#47;&lt;Pod的ID&gt;&#47;volumes&#47;kubernetes.io~&lt;Volume类型&gt;&#47;&lt;Volume名字&gt;
kubelet 把 Volume 目录通过 CRI 里的 Mounts 参数，传递给 Docker，为 Pod 里的容器挂载这个“持久化”的 Volume 。
$ docker run -v &#47;var&#47;lib&#47;kubelet&#47;pods&#47;&lt;Pod的ID&gt;&#47;volumes&#47;kubernetes.io~&lt;Volume类型&gt;&#47;&lt;Volume名字&gt;:&#47;&lt;容器内的目标目录&gt; 我的镜像 ...


Static Provisioning：手动创建 PV 与 PVC，StorageClassName 仅作为匹配字段。
Dynamic Provisioning：通过 StorageClass 自动创建 PV、自动绑定 PV 与 PVC。
StorageClass 定义插件、PV 属性，k8s根据 PVC 寻找 StorageClass，StorageClass 创建 PV。
PVC——StorageClass——PV。


Local Persistent Volume：Volume直接使用本地磁盘。
优点：本地磁盘读写性能更好。
缺点：宕机数据丢失，需要恢复机制与定期备份。

先准备好本地磁盘，然后延迟绑定。
延迟绑定：StorageClass volumeBindingMode: WaitForFirstConsumer，将 PV、PVC 的绑定推迟到 Pod 调度的时候，从而保证绑定结果不会影响 Pod 的正常调度。
1.PersistentVolumeController 遍历发现通过 StorageClass 关联的可以与 PVC 绑定的 PV；
2.第一个声明使用该 PVC 的 Pod 出现在调度器之后，调度器综合考虑这个 PVC 跟哪个 PV 绑定。
</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/ff/6201122c.jpg" width="30px"><span>Geek_89bbab</span> 👍（4） 💬（6）<div> kubectl describe persistentvolumeclaim&#47;claim1
Name:          claim1
Namespace:     default
StorageClass:  block-service
Status:        Pending
Volume:        
Labels:        &lt;none&gt;
Annotations:   .......
Events:
  Type     Reason              Age                 From                                                                                         Message
  ----     ------              ----                ----                                                                                         -------
  Warning  ProvisioningFailed  10m (x13 over 23m)  ceph.rook.io&#47;block rook-ceph-operator-5bfbf654db-ncgdf 97142e78-de86-11e8-a7d1-e6678be2ea25  Failed to provision volume with StorageClass &quot;block-service&quot;: Failed to create rook block image replicapool&#47;pvc-5b68d13b-e501-11e8-8b01-00163e0cf240: failed to create image pvc-5b68d13b-e501-11e8-8b01-00163e0cf240 in pool replicapool of size 2147483648: Failed to complete &#39;&#39;: exit status 2. rbd: error opening pool &#39;replicapool&#39;: (2) No such file or directory
. output:
  Normal  Provisioning          5m (x15 over 23m)   ceph.rook.io&#47;block rook-ceph-operator-5bfbf654db-ncgdf 97142e78-de86-11e8-a7d1-e6678be2ea25  External provisioner is provisioning volume for claim &quot;default&#47;claim1&quot;
  Normal  ExternalProvisioning  2m (x331 over 23m)  persistentvolume-controller                                                                  waiting for a volume to be created, either by external provisioner &quot;ceph.rook.io&#47;block&quot; or manually created by system administrator

老师，这个是什么原因导致的？ 没有这个文件或者目录?</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（4） 💬（1）<div>老师的问题的思考，90%都是动态申请存储的，所以我觉得pv和pvc都去掉，只有storage class和必要的参数（空间大小和读写属性 ）放在pod中即可</div>2018-10-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM6GcSnUMzR0H9haiaAxssjibGLQMLAsPKonh50g9W2Iz38LcZNGH39HPaANLtovXTp1YvsINIZoH6F0iaSGuxJMXZS/132" width="30px"><span>Geek_10d981</span> 👍（2） 💬（0）<div>其实老师最后的提问仅仅是让大家深入思考的，没有固定的解答。我尝试理解：这种分层的概念其实在高端存储用的很多，比如IBM的SVC,HDS的LUSE，EMC的TIRE，很多存储厂家的THIN PROVISION都是分层的概念，中端的NETAPP也是类似的技术（NETAPP横着切 一刀，竖着再切一刀，IBM DS7000，,8000系列也是这样，HP 3PAR也是彻底分层），当然，分层的时候要考虑SAN的结构和MULTIPATH。分层的好处很多，不仅仅只是解耦，也是对磁盘的利用率，动态调节，性能诊断更灵活。还有，HDS,EMC等厂家可以详细的性能诊断，因为高端存储都有自己的高速缓存（32G-128G，还有CROSS BAR技术），很多存储的高级功能必须是要分层才能实现的。</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/ec/5c53f9e5.jpg" width="30px"><span>小熹</span> 👍（2） 💬（0）<div>用CSI标准实现第三方存储，把存储卷的管理全部托付给第三方，就不用自己纠结pv pvc的概念了</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/ff/6201122c.jpg" width="30px"><span>Geek_89bbab</span> 👍（2） 💬（0）<div>有人执行pvc有遇到这样的错误吗？
Failed to provision volume with StorageClass &quot;rook-ceph-block&quot;: Failed to create rook block image replicapool&#47;pvc-0574eb19-e58c-11e8-8b01-00163e0cf240: failed to create image pvc-0574eb19-e58c-11e8-8b01-00163e0cf240 in pool replicapool of size 2147483648: Failed to complete &#39;&#39;: exit status 2. rbd: error opening pool &#39;replicapool&#39;: (2) No such file or directory
</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（2） 💬（0）<div>@GR 是一一对应的关系，可以创建一个大的pvc共用，用子目录区别开。前提是在一个namespace下。
也可以开发插件，支持动态创建pv</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3a/b0/a4e4c5d1.jpg" width="30px"><span>然谛</span> 👍（1） 💬（0）<div>如何理解读写模式ReadWriteMany,ReadWriteOnce,ReadOnlyMany，这块有点混乱，涉及的场景有哪些</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/05/19c5c255.jpg" width="30px"><span>微末凡尘</span> 👍（1） 💬（0）<div>pvc是接口，不负责具体的实现
pv是具体的实现，存储分为很多种，nfs，cefh等等
storageClass负责自动化创建pv</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/93/e8bfb26e.jpg" width="30px"><span>Dem</span> 👍（1） 💬（0）<div>直接使用范例中的web-frontend的yaml进行kubectl apply -f的时候会遇到报错：
```
error: error when retrieving current configuration of:
Resource: &quot;&#47;v1, Resource=pods&quot;, GroupVersionKind: &quot;&#47;v1, Kind=Pod&quot;
Name: &quot;&quot;, Namespace: &quot;default&quot;
Object: &amp;{map[&quot;apiVersion&quot;:&quot;v1&quot; &quot;kind&quot;:&quot;Pod&quot; &quot;metadata&quot;:map[&quot;annotations&quot;:map[&quot;kubectl.kubernetes.io&#47;last-applied-configuration&quot;:&quot;&quot;] &quot;labels&quot;:map[&quot;role&quot;:&quot;web-frontend&quot;] &quot;namespace&quot;:&quot;default&quot;] &quot;spec&quot;:map[&quot;containers&quot;:[map[&quot;image&quot;:&quot;nginx&quot; &quot;name&quot;:&quot;web&quot; &quot;ports&quot;:[map[&quot;containerPort&quot;:&#39;P&#39; &quot;name&quot;:&quot;web&quot;]] &quot;volumeMounts&quot;:[map[&quot;mountPath&quot;:&quot;&#47;usr&#47;share&#47;nginx&#47;html&quot; &quot;name&quot;:&quot;nfs&quot;]]]] &quot;volumes&quot;:[map[&quot;name&quot;:&quot;nfs&quot; &quot;persistentVolumeClaim&quot;:map[&quot;claimName&quot;:&quot;nfs&quot;]]]]]}
from server for: &quot;test-pod-pvc.yaml&quot;: resource name may not be empty
```
需要给metadata加一个name，例如：
```

apiVersion: v1
kind: Pod
metadata:
  labels:
    role: web-frontend
  name: web-frontend
```
不知道是不是kubernetes版本的差异。</div>2019-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/96/a6/32a286e0.jpg" width="30px"><span>大雄</span> 👍（0） 💬（0）<div>我通过cephamd部署的ceph集群，k8s版本是1.27，ceph是12.2.7 ，ceph-csi是3.11,通过storageclass自动创建pv，nginx-pod和pvc一直处于pending。。ceph集群是正常，存储pool也存在。试过手动pv正常。看了好几天完全没思路。
 kubectl get pod nginx-pod
NAME        READY   STATUS    RESTARTS   AGE
nginx-pod   0&#47;1     Pending   0          22m
[root@k8s-205 new]# kubectl get pvc
NAME        STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
nginx-pvc   Pending                                      ceph-rbd       3d2h
[root@k8s-205 new]# kubectl get storageclass
NAME       PROVISIONER    RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
ceph-rbd   ceph.com&#47;rbd   Delete          Immediate           false                  23m

ceph -s
  cluster:
    id:     ecdb563e-e05e-11ee-b9a4-525400e890d6
    health: HEALTH_OK
 
  services:
    mon: 3 daemons, quorum ceph-01,ceph-02,ceph-03 (age 38h)
    mgr: ceph-03.snrxzu(active, since 6d), standbys: ceph-02.tvgjga, ceph-01.hbmhpm
    osd: 3 osds: 3 up (since 6d), 3 in (since 5w)
    rgw: 3 daemons active (3 hosts, 1 zones)
 
  data:
    pools:   6 pools, 137 pgs
    objects: 243 objects, 1.3 MiB
    usage:   1.4 GiB used, 299 GiB &#47; 300 GiB avail
    pgs:     137 active+clean
 
</div>2024-04-22</li><br/>
</ul>