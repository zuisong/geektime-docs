你好，我是张磊。今天我和你分享的主题是：编写自己的存储插件之FlexVolume与CSI。

在上一篇文章中，我为你详细介绍了Kubernetes里的持久化存储体系，讲解了PV和PVC的具体实现原理，并提到了这样的设计实际上是出于对整个存储体系的可扩展性的考虑。

而在今天这篇文章中，我就和你分享一下如何借助这些机制，来开发自己的存储插件。

在Kubernetes中，存储插件的开发有两种方式：FlexVolume和CSI。

接下来，我就先为你剖析一下Flexvolume的原理和使用方法。

举个例子，现在我们要编写的是一个使用NFS实现的FlexVolume插件。

对于一个FlexVolume类型的PV来说，它的YAML文件如下所示：

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-flex-nfs
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  flexVolume:
    driver: "k8s/nfs"
    fsType: "nfs"
    options:
      server: "10.10.0.25" # 改成你自己的NFS服务器地址
      share: "export"
```

可以看到，这个PV定义的Volume类型是flexVolume。并且，我们**指定了这个Volume的driver叫作k8s/nfs**。这个名字很重要，我后面马上会为你解释它的含义。

而Volume的options字段，则是一个自定义字段。也就是说，它的类型，其实是map\[string]string。所以，你可以在这一部分自由地加上你想要定义的参数。

在我们这个例子里，options字段指定了NFS服务器的地址（server: “10.10.0.25”），以及NFS共享目录的名字（share: “export”）。当然，你这里定义的所有参数，后面都会被FlexVolume拿到。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/97/93e82345.jpg" width="30px"><span>陆培尔</span> 👍（0） 💬（1）<div>老师的课讲得太好了，什么时候开始讲容器网络方面的内容？感觉这一块一直有很多地方搞不明白，service,ingress，lb,跨节点组网等等</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（164） 💬（3）<div>思考题：

1. Register过程： csi 插件应该作为 daemonSet 部署到每个节点（node）。然后插件 container 挂载 hostpath 文件夹，把插件可执行文件放在其中，并启动rpc服务（identity, controller, node）。External component Driver Registrar 利用 kubelet plugin watcher 特性watch指定的文件夹路径来自动检测到这个存储插件。然后通过调用identity rpc服务，获得driver的信息，并完成注册。


2. Provision过程：部署External Provisioner。 Provisioner 将会 watch apiServer 中 PVC 资源的创建，并且PVC 所指定的 storageClass 的 provisioner是我们上面启动的插件。那么，External Provisioner 将会调用 插件的 controller.createVolume() 服务。其主要工作应该是通过阿里云的api 创建网络磁盘，并根据磁盘的信息创建相应的pv。

3. Attach过程：部署External Attacher。Attacher 将会监听 apiServer 中 VolumeAttachment 对象的变化。一旦出现新的VolumeAttachment，Attacher 会调用插件的 controller.ControllerPublish() 服务。其主要工作是调用阿里云的api，把相应的磁盘 attach 到声明使用此 PVC&#47;PV 的 pod 所调度到的 node 上。挂载的目录：&#47;var&#47;lib&#47;kubelet&#47;pods&#47;&lt;Pod ID&gt;&#47;volumes&#47;aliyun~netdisk&#47;&lt;name&gt;


4. Mount过程：mount 不可能在远程的container里完成，所以这个工作需要kubelet来做。kubelet 的 VolumeManagerReconciler 控制循环，检测到需要执行 Mount 操作的时候，通过调用 pkg&#47;volume&#47;csi 包，调用 CSI Node 服务，完成 volume 的 Mount 阶段。具体工作是调用 CRI 启动带有 volume 参数的container，把上阶段准备好的磁盘 mount 到 container指定的目录。</div>2018-10-31</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（19） 💬（0）<div>PVC描述的，是Pod想要使用的持久化存储的属性，比如存储的大小、读写权限等
PV描述的，则是一个具体的Volume的属性，比如Volume的类型、挂载目录、远程存储服务器地址等

有两种管理PV的方式：  人工管理（Static Provisioning），自动创建（Dynamic Provisioning）。Dynamic Provisioning机制工作的核心，就在于一个名叫StorageClass的API对象。Kubernetes能够根据用户提交的PVC，找到一个对应的StorageClass了。然后，Kuberentes就会调用该StorageClass声明的存储插件，创建出需要的PV。

需要注意的是，StorageClass并不是专门为了Dynamic Provisioning而设计的。比如，我在PV和PVC里都声明了storageClassName=manual。而我的集群里，实际上并没有一个叫manual的StorageClass对象。这完全没有问题，这个时候Kubernetes进行的是Static Provisioning，但在做绑定决策的时候，它依然会考虑PV和PVC的StorageClass定义。而这么做的好处也很明显：这个PVC和PV的绑定关系，就完全在我自己的掌握之中。

存储插件的开发方式有两种：FlexVolume和CSI 

FlexVolume： kubelet --&gt; pkg&#47;volume&#47;flexvolume.SetUpAt() --&gt; &#47;usr&#47;libexec&#47;kubernetes&#47;kubelet-plugins&#47;volume&#47;exec&#47;k8s~nfs&#47;nfs mount &lt;mount dir&gt; &lt;json param&gt;

FlexVolume的方式，需要手动先创建好PV，由FlexVolume来执行Attach和Mount操作。

相比于 FlexVolume，CSI 的设计思想是把插件的职责从“两阶段处理”，扩展成了 Provision、Attach 和 Mount 三个阶段。其中，Provision 等价于“创建磁盘”，Attach 等价于“挂载磁盘到虚拟机”，Mount 等价于“将该磁盘格式化后，挂载在 Volume 的宿主机目录上”。
</div>2020-10-29</li><br/><li><img src="" width="30px"><span>Geek_5baa01</span> 👍（12） 💬（0）<div>Provision：调用阿里云 API  Create 云盘
Attach： 调用阿里云 API 挂载云盘到 ECS 
Mount: 挂载云盘到对应的 pod volume 目录</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（10） 💬（0）<div>&#39;test 正是我们前面定义的 PV 的名字&#39;,这个是否是typo？PV的名字是pv-flex-nfs？</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/09/e1/100a0526.jpg" width="30px"><span>kakj</span> 👍（6） 💬（4）<div>java程序员从入门到放弃到再入门到再放弃中</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b4/8a/ffc23116.jpg" width="30px"><span>leo</span> 👍（2） 💬（0）<div>厉害了 新的知识！</div>2018-11-20</li><br/><li><img src="" width="30px"><span>vincent</span> 👍（1） 💬（0）<div>简单说是两阶段：
attach + mount
细了说：1、创建卷资源  2、attach节点  3、node上创建设备格式化  4、挂在设备</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（1） 💬（0）<div>问题：

1. 既然csi的PV是自己定义的类型，那么volume controller应该不会做这个红娘吧？所以问题是，他们是怎么完成绑定的？绑定后的状态会改变为 bound 吗？
2. 按照我的理解 driver 插件应该安装到每个node上，那么适合使用 daemonSet 去部署插件和 Driver Registerar sidecar。而 External Provisioner&#47;Attacher 则只需要一份部署就可以。为什么文中建议把三个 External components 都部署为sidecar？</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/01/1d/12d716c9.jpg" width="30px"><span>guolisen</span> 👍（0） 💬（0）<div>kubelet为什么会知道 对应的可执行程序叫做nfs(k8s~nfs&#47;nfs)？是在哪里告诉kubelet的？</div>2023-02-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Ezw43LrWwwqsCxuccwwQ7OibXq5sxJPOnicsPpFvBrkQQXcuhqfnxXq5ypcVY0Vg5AiaXZbh3tXmibH9icjcaFuBOsw/132" width="30px"><span>BobToGo</span> 👍（0） 💬（0）<div>🐮🍺</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/e8/98/6adce1b7.jpg" width="30px"><span>chenkai-1</span> 👍（0） 💬（0）<div>1.register(包含调用identity获取插件信息）：将插件注册到kubelet里面，将可执行文件放在插件目录下
2.External Provisioner：处理 Provision 的阶段。External Provisioner 监听APIServer 里的 PVC 对象。当一个 PVC 被创建时，调用 CSI Controller 的 CreateVolume 方法，创建PV。
3.External Attacher ：处理“Attach 阶段”。监听了 APIServer 里 VolumeAttachment 对象的变化。一旦出现了 VolumeAttachment 对象，External Attacher 就会调用 CSI Controller 服务的 ControllerPublish 方法，完成它所对应的 Volume 的 Attach 阶段。
4.mount：kubelet 的 VolumeManagerReconciler 控制循环检查到它需要执行 Mount 操作的时候，会通过 pkg&#47;volume&#47;csi 包，直接调用 CSI Node 服务完成 Volume 的“Mount 阶段”。
</div>2021-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（1）<div>脑壳疼... 没用过docker 没用过k8s,操作系统知识不扎实,导致我看到这里好累啊,还是基础差</div>2021-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3d/0e/92176eaa.jpg" width="30px"><span>左氧佛沙星人</span> 👍（0） 💬（0）<div>思考题，应该参考local path storage provisioner 或者 local volume storage provisioner，需要新增的是，讲创建好的云盘，attach到主机上，这样对吗？</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/ae/c082bb25.jpg" width="30px"><span>大星星</span> 👍（0） 💬（1）<div>有个问题，请教下，三个external组建为什么要独立出来。这个不需要吧。只要csi 三个服务起来了，自动注册插件。他们三个服务也负责watch api，每当有请求过来，provision attatch.mount动作时候分别找对应服务请求就行。不知道都一个个分出来有必要么？</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（0） 💬（1）<div>你好，自己实现的nfs flexvolume是否可以在pvc中指定呢？怎么指定呢？</div>2018-10-31</li><br/>
</ul>