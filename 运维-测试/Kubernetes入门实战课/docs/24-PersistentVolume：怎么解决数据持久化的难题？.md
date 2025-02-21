你好，我是Chrono。

经过了“初级篇”和“中级篇”的学习，相信你对Kubernetes的认识已经比较全面了，那么在接下来的“高级篇”里，我们再进一步，探索Kubernetes更深层次的知识点和更高级的应用技巧。

今天就先从PersistentVolume讲起。

早在[第14讲](https://time.geekbang.org/column/article/533395)介绍ConfigMap/Secret的时候，我们就遇到过Kubernetes里的Volume存储卷的概念，它使用字段 `volumes` 和 `volumeMounts`，相当于是给Pod挂载了一个“虚拟盘”，把配置信息以文件的形式注入进Pod供进程使用。

不过，那个时候的Volume只能存放较少的数据，离真正的“虚拟盘”还差得很远。

今天我们就一起来了解Volume的高级用法，看看Kubernetes管理存储资源的API对象PersistentVolume、PersistentVolumeClaim、StorageClass，然后使用本地磁盘来创建实际可用的存储卷。

## 什么是PersistentVolume

在刚完成的“中级篇”实战中（[22讲](https://time.geekbang.org/column/article/539420)），我们在Kubernetes集群里搭建了WordPress网站，但其中存在一个很严重的问题：Pod没有持久化功能，导致MariaDB无法“永久”存储数据。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（27） 💬（10）<div>如果目录没有创建， pod 会一直pending中。 我在master节点创建了目录 但 pod 没起来，查了半天才想起来pod 启动在worker节点，需要在worker 节点创建目录</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/8e/8a39ee55.jpg" width="30px"><span>文古</span> 👍（13） 💬（1）<div>老师，我个人感觉比较迷茫：k8s需要学习到什么程度才能上岗？学习云原生的线路可以说一下吗？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（5） 💬（2）<div>1. 对我来说，有点奇怪，和大家的答案是不太相同的，就是创建了pv和pvc，pod挂载之后，host-10m-pv这个文件夹自动创建了。
2. 这些概念相当复杂，除了生活实例理解外，并不理解系统中有什么好处。不过我想来想去，觉得storageclass是需要的.因为pv只进行硬件或者相关服务级别的抽象，pvc则只管请求，在数量比较多的pv的场景中，很容易选择到不想要的pv，比如1m请求了100m的，造成资源浪费，所以stroageclass是有必要存在的，但可以设计为一个选择器.


说说一些测试的操作。
1. 建立了一个pv 10m,一个pvc请求，5m。顺利请求到，这是和课程中一样的。
2. 建立两个pv,10m,两个pvc请求，都是5m，各自请求到一个，1和2的操作都使用了同同样的storageClassName。
3. 建立一个pv 10m，两个pvc请求，其中一个请求不到，显示为没有资源，除非再造一个，就可以被请求到。
4. 建了pv和pvc，先删除pv，不删除pvc，pv一直会显示terming状态，但始终不会消失，删除pvc后，删除成功。
感觉对这些概念有些理解，但更多的是迷糊、
</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/2b/8c/a6c1ec31.jpg" width="30px"><span>作草分茶</span> 👍（5） 💬（3）<div>老师，怎么没有storageClass的配置呀</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（3） 💬（1）<div>列一些常用的storageClassName会更好理解：

chatGPT的回答：
以下是一些常见的 Kubernetes 存储类（StorageClass）的名称：

standard：标准存储类，用于提供基本的存储能力，适用于一般用途。
gp2：亚马逊 Web 服务（AWS）上的一种存储类型，适用于需要快速访问和较高性能的应用程序。
rbd：Ceph 存储系统的一种存储类型，用于提供分布式块存储。
glusterfs：GlusterFS 分布式文件系统的一种存储类型，用于提供高可用性和可扩展性的存储解决方案。
nfs：网络文件系统（NFS）的一种存储类型，用于提供共享文件存储。
azure-disk：Azure 上的一种存储类型，适用于需要高可用性和可扩展性的应用程序。
local-storage：本地存储的一种存储类型，用于将本地磁盘挂载到 Kubernetes Pod 中。
请注意，这些存储类型的可用性可能因为云服务提供商的不同而有所不同。此外，还可以创建自定义存储类型来满足特定的存储需求。</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（3） 💬（2）<div>老师，想请问一下文稿的图是用什么软件画的？</div>2022-08-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（3） 💬（2）<div>跑个题： 题图是有什么关联吗？</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（2） 💬（1）<div>唉，痛苦死了， 我按照本文步骤，pv、pvc、pod都成功了，但挂载的目录里 始终找不到生成的文件，不知道问题出在哪里，痛苦查了一天多时间。
我是两台ecs机器做操作，我一直是在master节点的机器上找来找去，就是找不到。
结果无意间发现，在一台work节点的机器上找到了挂载的目录。

老师，我的问题是在使用kubectl get all 查看pod时，我怎么知道 这个pod是被分配到哪台机器上呢？
如果我早点知道，就不用这么瞎折腾了，多谢。</div>2023-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/87/e1/b3edcc09.jpg" width="30px"><span>范飞扬</span> 👍（2） 💬（2）<div>“Kubernetes 里定义存储容量使用的是国际标准，我们日常习惯使用的 KB&#47;MB&#47;GB 的基数是 1024，要写成 Ki&#47;Mi&#47;Gi，一定要小心不要写错了，否则单位不一致实际容量就会对不上。”
 Ki&#47;Mi&#47;Gi什么意思？

chatGPT的回答：
Ki&#47;Mi&#47;Gi 是二进制单位前缀，用于表示存储容量。它们的含义如下：

1 KiB (kibibyte) = 2^10 bytes = 1,024 bytes
1 MiB (mebibyte) = 2^20 bytes = 1,048,576 bytes
1 GiB (gibibyte) = 2^30 bytes = 1,073,741,824 bytes

这些单位前缀在计算机领域中用于准确地表示存储容量。与之相对的是基于十进制的单位前缀，如 KB&#47;MB&#47;GB，它们使用的是 10 的幂，而不是 2 的幂。因此，1 KB 实际上是 1,000 bytes，1 MB 是 1,000,000 bytes，1 GB 是 1,000,000,000 bytes。

在 Kubernetes 中，使用 Ki&#47;Mi&#47;Gi 单位来定义存储容量可以避免使用基于十进制的单位前缀时可能引起的容量计算不准确的问题。</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（2） 💬（7）<div>为了省事，我没有在 &#47;tmp 里建立名字是 host-10m-pv 的目录，最后发现他自己创建了</div>2023-02-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKnrjcKrRp5atleQiaD4yYw1sjguFOCCwldjE4T2cicicQaT9ELfKFhmUibT0m9gUicyHIDP9ZBdBwZk5w/132" width="30px"><span>crezov</span> 👍（1） 💬（1）<div>1、HostPath 类型的 PV 要求节点上必须有相应的目录，如果这个目录不存在（比如忘记创建了）会怎么样呢？
答：具体的行为取决于在PV配置中hostPath字段的type属性：
    DirectoryOrCreate，Kubernetes将会在节点上自动创建对应的目录；
    Directory或者没有设置，那么如果目录不存在，Pod将无法成功挂载该PV，并且Pod的状态将会是ContainerCreating，直到目录被创建。
</div>2023-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（1） 💬（1）<div>版本：1.26.3
HostPath不用手动创建目录，yml定义了会自动创建目录，亲测是这样的</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/58/6f/4acc5b43.jpg" width="30px"><span>PeiXy</span> 👍（1） 💬（1）<div>老师我现在的理解是、我默认先创建好sc，然后直接提交pvc，再由pvc去申请pv…在没有适合的pv的情况下会主动去创建一个pv对吗？</div>2022-11-17</li><br/><li><img src="" width="30px"><span>邵涵</span> 👍（1） 💬（2）<div>对于作业“HostPath 类型的 PV 要求节点上必须有相应的目录，如果这个目录不存在（比如忘记创建了）会怎么样呢？”，看评论区同学测试的结果有不同
我的测试结果是这样：
1. 用kubectl delete -f清掉本节中创建的pod、pvc、pv，手动删掉之前在节点机器上手动创建的目录&#47;tmp&#47;host-10m-pv（以及里边的a.txt文件）
2. 用本节这些yaml文件，再次按顺序创建pv和pvc，都能创建成功，截止此时，在节点机器上查看，还是没有目录&#47;tmp&#47;host-10m-pv的
3. 创建pod，也是创建成功，此时，在节点机器上，就自动创建了目录&#47;tmp&#47;host-10m-pv
[abc@k8s3 ~]$ ls -ld &#47;tmp&#47;host*
drwxr-xr-x. 2 root root 6 Oct 18 18:31 &#47;tmp&#47;host-10m-pv
4. 进入pod，在存储卷挂载路径&#47;tmp下创建文件a.txt，该文件也会出现在节点机器的目录&#47;tmp&#47;host-10m-pv下</div>2022-10-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qCv5IcP1lkO2jicrTic9KicycZXZ7WylG49GZHJCibuFQfBlJMsCpVHARuaLxIB23f3enRL4ls6EOr9wxu40K0Hl8Q/132" width="30px"><span>tcyi</span> 👍（1） 💬（2）<div>为什么我执行完老师提供的host-path-pv.yml后&#47;tmp&#47;host-10m-pv&#47;这个目录自动创建了呢？</div>2022-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9e/7d/5c78b1ff.jpg" width="30px"><span>Y。</span> 👍（0） 💬（1）<div>我有个问题哈~ Hostpath 本机的PV 不应该是 每个work节点都创建了这个pv么，哪个pod 要在节点上运行挂载都能够挂 然后还有 为什么要创建这么多PV 创建一个大PV 然后每个pod 创建小的pvc 去pv里面申请资源 这会不会维护起来更简单些？</div>2024-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（2）<div>我是用的 minikube 做的实验, 然后系统是mac本机系统, 

按照文中 步骤
1、在mac电脑 &#47;tmp中创建了 host-10m-pv 文件夹,  
2、然后创建了pv、pvc、pod  进入到 pod内, 创建文件a.txt  , b.txt  

但是在mac电脑,内&#47;tmp&#47;host-10m-pv  并没有找到这2个文件. 
请问老师是 我这个环境 有问题么?  </div>2024-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（0） 💬（1）<div>我发现 worker 节点也是自己创建了目录。</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3b/29/0f86235e.jpg" width="30px"><span>明月夜</span> 👍（0） 💬（1）<div>这 3 种访问模式限制的对象是节点而不是 Pod，因为存储是系统级别的概念，不属于 Pod 里的进程  --- 这句话怎么理解，文章里对这三种访问模式的解释，就是针对pod</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>如果我删除后，磁盘容量回收是如何操作的呢？</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>Ki&#47;Mi&#47;Gi不是IEC标准吗，国际标准是kB MB GB啊 而且是以10进制计算，只不过像Windows系统的kB MB GB还是以什么1024来规定，而不是1000来定义，历史遗留问题。</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（1）<div>想复现老师的PVC 会一直处于 Pending 状态，需先kubectl delete -f host-path-pvc.yml 然后再apply
要不然会报错误only dynamically provisioned pvc can be resized and the storageclass that provisions the pvc must support resize

应该是hostpath这种的不支持动态扩容吧？</div>2023-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/dbqU4jVNf6mmicdZ18eXgHOrd0icRfsarXAV8c5ZqOHopJ4CZ8QtuXESeLL5erHEHCibwP5Udz0RicaspGb4MNSb8g/132" width="30px"><span>ecolife_zhi</span> 👍（0） 💬（1）<div>试验了一下，host path会自动创建，不需要手动在worker节点创建</div>2023-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/2f/4518f8e1.jpg" width="30px"><span>放不下荣华富贵</span> 👍（0） 💬（3）<div>我这边依然用minikube的话，a.txt并没有创建到宿主机上，find &#47;tmp 最近创建的txt文件也没有。但是delete pod再启动，a.txt依然存在</div>2022-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/da/29fe3dde.jpg" width="30px"><span>小宝</span> 👍（0） 💬（1）<div>例子中的：
spec: storageClassName: host-test
这个StorageClass哪里来的，貌似例子中没定义。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（0） 💬（1）<div>茶艺师学编程：

1.HostPath 类型的 PV 要求节点上必须有相应的目录，如果这个目录不存在（比如忘记创建了）会怎么样呢？
pv，pvc，以及要挂上pvc的pod都能正常启动。但此时pv所指的本地目录是还没创建的
只有在pod里挂pvc的目录里写了数据，pv中所指的目录才会创建，在pod中所写的数据也会在里面。

要注意的是，pv在创建之后是不可变的，换句话说就是，在apply之后，修改了这个pv.yaml，再apply，这样的操作是不让通过。需要把pv删除了，再创建（apply），改动才能成功。</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/55/9e/a64a84ac.jpg" width="30px"><span>Geek_12fef6</span> 👍（0） 💬（1）<div>Pod挂载了PVC会自动创建目录，PVC绑定PV不会创建。</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（0） 💬（1）<div>请教老师几个问题：

1、StorageClass 是我们自己定义的 host-test，这个名字叫做host-test的StorageClass不需要我们手动创建吗？如果不需要，那么它是什么样子的存在，扮演了什么角色

2、PVC 是给 Pod 使用的对象，它相当于是 Pod 的代理；是不是可以这样理解，pod只能看到pvc，也只能操作pvc。k8s把pod到pvc的操作真正的放到pv上。pv就是一个文件系统的表示形式

3、pv定义的10mi，是需要手动输入的，那么会不会存在实际的文件系统和输入的不一致的情况，这样不会产生大问题吗？例如100g的硬盘，实际可用空间为99g，但是我定义成了100g。

麻烦老师了</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：POD里面的MySQL不能存取硬盘吗？不能的话，从MySQL读数据是从哪里读的？写入MySQL的数据又写到哪里去了？
Q2：不用k8s，只用docker，用docker创建的mysql可以持久化吗？
Q3：StorageClass怎么没有创建对象？
在PV和PVC的yml文件中，只是用了一个相同的StorageClass名字，就把PV和PVC关联起来了。既然StorageClass是一个对象，不需要创建吗？</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/09/d0/8609bddc.jpg" width="30px"><span>戒贪嗔痴</span> 👍（0） 💬（1）<div>思考：
1. 我猜测应该会自动创建目录。
2. 这种抽象可能对k8s本身减少了复杂度，解耦，但对学习者来说可能理解概念有些困难，时间成本，这也是内卷的开始。</div>2022-08-17</li><br/>
</ul>