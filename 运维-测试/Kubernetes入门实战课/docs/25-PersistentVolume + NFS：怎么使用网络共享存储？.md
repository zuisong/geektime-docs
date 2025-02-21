你好，我是Chrono。

在上节课里我们看到了Kubernetes里的持久化存储对象PersistentVolume、PersistentVolumeClaim、StorageClass，把它们联合起来就可以为Pod挂载一块“虚拟盘”，让Pod在其中任意读写数据。

不过当时我们使用的是HostPath，存储卷只能在本机使用，而Kubernetes里的Pod经常会在集群里“漂移”，所以这种方式不是特别实用。

要想让存储卷真正能被Pod任意挂载，我们需要变更存储的方式，不能限定在本地磁盘，而是要改成**网络存储**，这样Pod无论在哪里运行，只要知道IP地址或者域名，就可以通过网络通信访问存储设备。

网络存储是一个非常热门的应用领域，有很多知名的产品，比如AWS、Azure、Ceph，Kubernetes还专门定义了CSI（Container Storage Interface）规范，不过这些存储类型的安装、使用都比较复杂，在我们的实验环境里部署难度比较高。

所以今天的这次课里，我选择了相对来说比较简单的NFS系统（Network File System），以它为例讲解如何在Kubernetes里使用网络存储，以及静态存储卷和动态存储卷的概念。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（29） 💬（2）<div>思考题：
1: 首先，静态存储卷PV这个动作是要由运维手动处理的，如果是处在大规模集群的成千上万个PVC的场景下，这个工作量是难以想象的；
   再者，业务的迭代变更是动态的，这也就意味着随时会有新的PVC被创建，或者就的PVC被删除，这也就要求运维每碰到PVC的变更，就要跟着去手动维护一个新的
   PV。来满足业务的新需求，这个情况如果解决不了，我相信运维这个职业马上就会消失。
   最后，动态存储卷的好处还在于分层和解耦，对于简单的localPath或者NFS这种存储卷或许相对来说还比较简单一些，但是像类似于远程存储磁盘这种就相对来说比较
   复杂了，动态存储可以让我们只关注于需求点，至于怎么把这些东西创建出来，就交由各个类型的provisioner去处理就行了。
   
  缺点：缺点的话就是在于资源的管控方面，比如原本我可能只需要2Gi的空间，但是业务人员对容量把握不够申请了10Gi，就会有8Gi空间的浪费。
2:StorageClass 作用是帮助指定特定类型的provisioner，这决定了你要使用的具体某种类型的存储插件；另外它还限定了PV和PVC的绑定关系，只有从属于同一StorageClass的PV和PVC才能做绑定动作，比如指定GlusterFS类型的PVC对象不能绑定到另外一个PVC定义的NFS类型的StorageClass 模版创建出的Volume的PV对象上面去。</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/d9/cf061262.jpg" width="30px"><span>新时代农民工</span> 👍（10） 💬（2）<div>不妨试一试docker版的nfs-server，简单又方便 https:&#47;&#47;hub.docker.com&#47;r&#47;fuzzle&#47;docker-nfs-server</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fc/4f/0a452c94.jpg" width="30px"><span>大毛</span> 👍（9） 💬（1）<div>用面向对象的思想来理解 kubernetes 在存储上的设计：
SC 是类，PV 是实例，PVC 是创建实例的代码，provisioner 是工厂。
有一种豁然开朗的感觉</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（8） 💬（1）<div>老师，不知道这么理解对不对，因为存储它涉及到了对物理机文件系统绑定的操作，因此K8S做了一系列抽象。PV在这个抽象里，其实就指代了主机文件系统的路径，当然至于再往实现层面走，是网络文件系统还是主机文件系统，这就全由PV的绑定类型决定。而往抽象层走，作为K8S的核心系统，K8S想尽可能屏蔽掉底层，也就是主机文件系统的概念，所以它抽象了StorageClass，用来统一指代&#47;管理PV。至此，K8S持久化存储就可以分两个部分，第一部分是由 主机文件系统+PV+StorageClass组成的，用来将抽象对象绑定到真实文件系统的生产者部分；第二部分就是 Volume+PVC+StorageClass，完全被抽象为K8S核心业务的消费者部分，而StorageClass，可以看作是两部分连接的桥梁。</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（6） 💬（5）<div>云服务器环境搭建：主要在nfs权限那边比较麻烦

-- 服务端
1: 查看是否安装了必要的软件
	$ dpkg -l | grep rpcbind
	...

	$ sudo apt -y install rpcbind
	$ sudo apt -y install nfs-kernel-server
	$ sudo apt -y install nfs-common
2.修改 &#47;etc&#47;services 追加

	# Local services
	mountd 4011&#47;udp
	mountd 4011&#47;tcp

	内容，固定mountd 的端口号



	打开端口号访问限制：
	 TCP: 2049、111、4011
	 UDP: 111、4046、4011


3. 创建目录 追加配置（和文档中的一样）
  $ mkdir -p &#47;tmp&#47;nfs

  &#47;etc&#47;exports 内容增加以下内容（我的云服务器外网ip是175.179网段，这里要根据自身的情况修改）：
    &#47;tmp&#47;nfs 175.178.0.0&#47;16(rw,sync,no_subtree_check,no_root_squash,insecure)


   $ sudo exportfs -v
   $ sudo exportfs -v

4.开启服务

	$ sudo systemctl start  nfs-server
	$ sudo systemctl enable nfs-server
	$ sudo systemctl status nfs-server

	$ sudo systemctl start  rpcbind
	$ sudo systemctl enable rpcbind
	$ sudo systemctl status rpcbind


-- 客户端
1.安装客户端软件

   $ sudo apt -y install nfs-common
   $ sudo apt -y install rpcbind

   其它步骤和老师基本一样

</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/48/c7fb8067.jpg" width="30px"><span>zzz</span> 👍（4） 💬（2）<div>nfs provisoner 在生产建议使用HELM包方式进行，而且已经在生产实践过，
nfs-subdir-external-provisioner
优势2个：
1. 无需复杂的配置
2. 可支持离线下载，方便传输到生产环境。
自己可以玩可以采用教程的方法，了解一下RBAC的流程
</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/da/29fe3dde.jpg" width="30px"><span>小宝</span> 👍（3） 💬（1）<div>思考题:
1. 动态存储卷PV需要手动运维，而且受限于分配的大小问题，如果分配的PV都比较小，需求又比较大，极易造成PV使用不当，造成浪费。反之，动态存储则按需分配。权利的无限放大也会带来问题，就是预先申请与实际使用之间的矛盾，动态申请大了，也是一种浪费。
2. StorageClass应证了“所有问题都可以通过增加一层来解决”。作用是解决了特定底层存储与K8S上资源的解耦问题，通过SC统一接口，具体厂商负责具体的存储实现。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（2） 💬（2）<div>看了这节课和上节课，终于把storageclass的使用方式搞清楚了，如果都是静态存储和使用，那么只需要在pv和pvc中加上这个name这个属性就可以，并不需要storageClass这个对象，而关键是，这个东西是可以引用provisioner的，让这个和deployment挂钩，其实iwo有一个问题啊，为啥不讲provisioner单独设置为一个对象，而是使用deployment进行部署呢，又是设置环境变量，又是配置参数，另外rabc到底是干嘛的，我真不理解。</div>2022-09-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OwolYO3ppfrxTcX81cswxC70LwthXDDbGbmswSe1xSl2ibxibLLy0Ka0KkZakE2uWYNHUzw2SrUSrbibntN93uS5w/132" width="30px"><span>Geek_5d4e3e</span> 👍（1） 💬（1）<div>老师这个文章里存在错误，这个yaml文件并不能将回收策略更改为retain
apiVersion: storage.k8s.io&#47;v1
kind: StorageClass
metadata:
  name: nfs-client-retained

provisioner: k8s-sigs.io&#47;nfs-subdir-external-provisioner
parameters:
  onDelete: &quot;retain&quot;

正确的yaml文件内容如下：
apiVersion: storage.k8s.io&#47;v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: k8s-sigs.io&#47;nfs-subdir-external-provisioner # or choose another name, must match deployment&#39;s env PROVISIONER_NAME&#39;
reclaimPolicy: Retain
</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/94/fe/5fbf1bdc.jpg" width="30px"><span>Layne</span> 👍（1） 💬（2）<div>已实操
遇到的问题：
搭建nfs的时候，目录挂载成功，但是创建文件，没有同步到服务端
原因：
在挂载的时候，客户端目录和服务端共享目录一样导致的，挂载目录和共享目录不能根目录相同
修改前：
sudo mount -t nfs 192.168.56.103:&#47;home&#47;layne&#47;data&#47;nfs &#47;home&#47;layne&#47;data&#47;nfs
修改后：
sudo mount -t nfs 192.168.56.103:&#47;home&#47;layne&#47;data&#47;nfs &#47;data&#47;nfs</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/f1/8b06801a.jpg" width="30px"><span>哇哈哈</span> 👍（1） 💬（1）<div>有个问题没有想明白，provisioner如何知道系统的存储容量呢？如果我 pvc 一个 100G 空间，但是 nfs 只有不到 100G 空间的时候，provisioner怎么处理这种场景呢？</div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/5a/3b01789e.jpg" width="30px"><span>Quintos</span> 👍（1） 💬（1）<div>由于用的是azure国际版的aks服务，无法直接搭建nfsserver。老师能否提供基于azure的nfs sample</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（1） 💬（1）<div>这个link是官方的吗？https:&#47;&#47;github.com&#47;kubernetes-sigs&#47;nfs-subdir-external-provisioner</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bf/52/59304c42.jpg" width="30px"><span>默默且听风</span> 👍（0） 💬（1）<div>老师，请教个问题。我使用helm安装MongoDB、Redis等集群并使用nfs的时候经常会报错
 Failed to create pod sandbox: rpc error: code = Unknown desc = failed to get sandbox image &quot;k8s.gcr.io&#47;pause:3.8&quot;: failed to pull image &quot;k8s.gcr.io&#47;pause:3.8&quot;: failed to pull and unpack image &quot;k8s.gcr.io&#47;pause:3.8&quot;: failed to resolve reference &quot;k8s.gcr.io&#47;pause:3.8&quot;: failed to do request: Head &quot;https:&#47;&#47;k8s.gcr.io&#47;v2&#47;pause&#47;manifests&#47;3.8&quot;: dial tcp 108.177.97.82:443: i&#47;o timeout 
每次手动执行
#!&#47;bin&#47;bash

# Pull the desired image using crictl
crictl pull registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#47;pause:3.8

# Tag the pulled image using ctr
ctr -n k8s.io i tag registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#47;pause:3.8 k8s.gcr.io&#47;pause:3.8

echo &quot;Image pull and tag complete&quot;
之后这个错误就又不在了。这个需要怎么设置一下吗？还是我的集群有问题。已经被折磨好几天了，百度不出来才来问的</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/6c/ad/0a694b50.jpg" width="30px"><span>Greenery</span> 👍（0） 💬（1）<div>就算是动态方式，这个storageClass也是会默认生成的对吗，我发现我的pvc中配置的storageClass是nfs-client，但是我只手动配置了文中的nfs-client-retain，也成功运行了。
是不是实际上nfs-client-retain没有起作用，实际生效的sc是默认自动生成的nfs-client？</div>2023-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9b/64/dadf0ca5.jpg" width="30px"><span>至尊猴</span> 👍（0） 💬（1）<div>找到pvc不能调整大小的答案了：nfs provision 不能有空间限制，并且也不能resize
------
The provisioned storage limit is not enforced. The application can expand to use all the available storage regardless of the provisioned size.
Storage resize&#47;expansion operations are not presently supported in any form. You will end up in an error state: Ignoring the PVC: didn&#39;t find a plugin capable of expanding the volume; waiting for an external controller to process this PVC.

</div>2023-04-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/g4os8I4iaB6jn06PsvyqI1BooV5XbOC0vI3niaJ4I3SlAhkbBKG2eewlPHHJ4ROcDia18bbPFSZPDXXmgHXtrBlLg/132" width="30px"><span>Geek_f2f06e</span> 👍（0） 💬（1）<div>&#47;tmp&#47;nfs 192.168.10.0&#47;24(rw,sync,no_subtree_check,no_root_squash,insecure)

执行这句话的时候报了这个错误：
bash: syntax error near unexpected token `(&#39;

加了转译符之后报了这个错误：
bash: &#47;tmp&#47;nfs: Is a directory

这个应该怎么解决啊
</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3b/29/0f86235e.jpg" width="30px"><span>明月夜</span> 👍（0） 💬（1）<div>nfs-static-pvc的例子，不需要创建nfs的storageclass吗，直接在pvc里指定storageClassName：nfs 就可以？</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>yaml方式，安装github操作，做了下修改：在本地创建个目录，如nfs，放入自定义的yaml。
---
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nfs-provisioner

---
# patch_nfs_details.yaml
apiVersion: apps&#47;v1
kind: Deployment
metadata:
  labels:
    app: nfs-client-provisioner
  name: nfs-client-provisioner
spec:
  template:
    spec:
      containers:
        - name: nfs-client-provisioner
          image: chronolaw&#47;nfs-subdir-external-provisioner:v4.0.2
          env:
            - name: NFS_SERVER
              value: 172.17.40.171
            - name: NFS_PATH
              value: &#47;tmp&#47;nfs
      volumes:
        - name: nfs-client-root
          nfs:
            server: 172.17.40.171
            path: &#47;tmp&#47;nfs

---
# kustomization.yaml
namespace: nfs-provisioner
bases:
  - github.com&#47;kubernetes-sigs&#47;nfs-subdir-external-provisioner&#47;&#47;deploy
resources:
  - namespace.yaml
patchesStrategicMerge:
  - patch_nfs_details.yaml

在nfs目录下执行：
kubectl apply -k .
很简单的完成了，前提是网络可以稍微拿到GitHub的yaml部署文件</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>spec.nfs路径 不需要提前创建好，kubectl get pv也是可用状态，但是在创建pod状态时，pod状态一直在ContainerCreating的状态，kubectl describe pod nfs-static-pod查看问题，发现还是挂载的问题，挂载找不到目录1g-pv，报错如下：
Output: mount.nfs: mounting 172.17.40.171:&#47;tmp&#47;nfs&#47;1g-pv failed, reason given by server: No such file or directory
故删除kubectl delete -f nfs-static-pod.yml，在NFS服务器&#47;tmp&#47;nfs&#47;目录下创建目录1g-pv，重新创建容器kubectl apply -f nfs-static-pod.yml，pod创建启动正常。

但是在1.26.3中，前文我测试hostPath没问题哦，不需要提前创建目录，NFS的就需要。</div>2023-03-28</li><br/><li><img src="" width="30px"><span>Geek_0e30b3</span> 👍（0） 💬（2）<div>老师有一个问题就是 ， 假设我的NFS capacity 是10G， 那么我动态创建PV的时候 ， PVC 申请容量大于10 G， 这个会检测到 超过了NFS server 的限制吗？ 不然没有限制， 我可以创建很多PV 即使我的NFS server容量很小</div>2023-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（2）<div>nfs.path:&#47;opt&#47;nfs&#47;1g-pv目录我没有手动创建，Pod挂载的时候会提示Output: mount.nfs: mounting 192.168.72.5:&#47;opt&#47;nfs&#47;1g-pv failed, reason given by server: No such file or directory

但是HostPath挂载我自测是会自动创建的。</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/73/52/8a4cf5e9.jpg" width="30px"><span>骷髅骨头</span> 👍（0） 💬（1）<div>pv和pvc的storageClassName都是nfs-client,  而storageClass的name是nfs-client-retain, 是笔误还是？</div>2023-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（1）<div>spec.nfs里的路径如果不存在，PV 没有处于“pending”状态，但是在创建pod时会起不来，报错：reason given by server: No such file or directory，还是提前创建目录保险</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f3/37/30a09a4a.jpg" width="30px"><span>路先生</span> 👍（0） 💬（1）<div>罗老师请教下，在class-retained.yaml里面定义
parameters:
  onDelete: &quot;retain&quot;
但是执行kubectl get sc -n kube-system
RECLAIMPOLICY列显示是Delete，
执行kubectl get pv -n devops
RECLAIM POLICY列显示也是Delete，
这是正常的吗？</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/9f/d2/b6d8df48.jpg" width="30px"><span>菲茨杰拉德</span> 👍（0） 💬（1）<div>
&#47;tmp&#47;nfs 192.168.10.0&#47;24(rw,sync,no_subtree_check,no_root_squash,insecure)
这个ip 是按照nfs的节点的ip?</div>2022-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（1）<div>为什么要在 node 上手动挂载 nfs volume，然后还要在 kubernetes 上声明这个路径是 nfs 的？既然都已经挂载了，kubernetes 直接使用这个路径不就行了嘛？另外为什么 kubernetes 不能自行挂载 nfs volume 呢？要求用户必须在所有 node 上全都挂载好 nfs 不是很麻烦吗？</div>2022-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/c3/775fe460.jpg" width="30px"><span>rubys_</span> 👍（0） 💬（1）<div>chronolaw&#47;nfs-subdir-external-provisioner:v4.0.2 在我的虚拟机拉取也失败，换一台机来拉取，然后使用  docker save 保存到文件，将这个导出的镜像文件放到虚拟机里面 docker load 导入，解决虚拟机拉取镜像失败的问题</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ad/e9/778ddf53.jpg" width="30px"><span>mamafeng</span> 👍（0） 💬（3）<div>请问大佬，我使用的是云服务Centos7, 三台机器开启了内网互联，并且关闭了防火墙，而且也可以ping通，但是在clinet 使用命令 showmount -e ‘服务器的ip地址’, 却一直卡着什么反应没有


但是我在client的服务器上使用命令：sudo mount -t nfs 10.0.4.10:&#47;tmp&#47;nfs &#47;tmp&#47;data

然后使用 df -h , 发现有一条成功的挂载记录
Filesystem          Size  Used Avail Use% Mounted on
10.0.4.10:&#47;tmp&#47;nfs   59G  5.9G   51G  11% &#47;tmp&#47;data

这个时候在客户端使用命令：showmount -e 10.0.4.10 还是连接不上，一直卡着不动，
我在客户端和服务器相应的挂载目录创建文件，发现也没有共享</div>2022-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（1）<div>作业：
动态存储卷相比静态存储卷有什么好处？有没有缺点？
个人觉得动态卷的灵活性高，运维定义好相应的存储 StorageClass ，开发可以忽视不同的存储细节，只定义相应的 PVC 申请和使用存储。个人觉得它的缺点也是因为它的灵活性，也可能导致管理松散。

StorageClass 在动态存储卷的分配过程中起到了什么作用？
关联各种类型存储卷的定制化的 Provisioner。解藕了使用和各类存储的实现细节。
</div>2022-09-16</li><br/>
</ul>