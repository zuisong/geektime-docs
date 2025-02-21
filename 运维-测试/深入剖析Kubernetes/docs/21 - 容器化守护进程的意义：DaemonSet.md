你好，我是张磊。今天我和你分享的主题是：容器化守护进程的意义之DaemonSet。

在上一篇文章中，我和你详细分享了使用StatefulSet编排“有状态应用”的过程。从中不难看出，StatefulSet其实就是对现有典型运维业务的容器化抽象。也就是说，你一定有方法在不使用Kubernetes、甚至不使用容器的情况下，自己DIY一个类似的方案出来。但是，一旦涉及到升级、版本管理等更工程化的能力，Kubernetes的好处，才会更加凸现。

比如，如何对StatefulSet进行“滚动更新”（rolling update）？

很简单。你只要修改StatefulSet的Pod模板，就会自动触发“滚动更新”:

```
$ kubectl patch statefulset mysql --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"mysql:5.7.23"}]'
statefulset.apps/mysql patched
```

在这里，我使用了kubectl patch命令。它的意思是，以“补丁”的方式（JSON格式的）修改一个API对象的指定字段，也就是我在后面指定的“spec/template/spec/containers/0/image”。

这样，StatefulSet Controller就会按照与Pod编号相反的顺序，从最后一个Pod开始，逐一更新这个StatefulSet管理的每个Pod。而如果更新发生了错误，这次“滚动更新”就会停止。此外，StatefulSet的“滚动更新”还允许我们进行更精细的控制，比如金丝雀发布（Canary Deploy）或者灰度发布，**这意味着应用的多个实例中被指定的一部分不会被更新到最新的版本。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（75） 💬（2）<div>思考题，

我觉得应该是效率的问题。

查了一下v1.11 的 release notes。scheduler关于affinity谓词的性能大大提高了。

查阅了Ds用默认调度器代替controller的设计文档
之前的做法是：
controller判断调度谓词，符合的话直接在controller中直接设置spec.hostName去调度。
目前的做法是：
controller不再判断调度条件，给每个pode设置NodeAffinity。控制器根据NodeAffinity去检查每个node上是否启动了相应的Pod。并且可以利用调度优先级去优先调度关键的ds pods。</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（40） 💬（1）<div>我跟上面的朋友有同样的疑问，关于Partition更新的。

我设置了Partition，用部分pod来做灰度发布，然后发现没问题，我要全部更新，就只需要去掉Partition字段吗？
然后我下一次更新的时候，就要再先加上Partition，然后再更新。全部更新时再去掉。

我看了老师的回复，表达的是这个意思吗？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/af/6dbbb482.jpg" width="30px"><span>紫夜</span> 👍（33） 💬（4）<div>张老师，DaemonSet的滚动更新，是先delete旧的pod，再启动新的pod，还是和Deployment一样，先创建新的pod，再删除旧的pod?</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（24） 💬（1）<div>张老师，请教几个基础问题：
1. 在上一讲中，有一点我还是没想通，为何MySQL的数据复制操作必须要用sidecar容器来处理，而不用Mysql主容器来一并解决，你当时提到说是因为容器是单进程模型。如果取消sidecar容器，把数据复制操作和启动MySQL服务这两个操作一并写到MySQL主容器的sh -c命令中，这样算不算一个进程呢？

2. StatefulSet的容器启动有先后顺序，那么当序号较小的容器由于某种原因需要重启时，会不会先把序号较大的容器KILL掉，再按照它们本来的顺序重新启动一次？

3. 在这一讲中，你提到了滚动升级时StatefulSet控制新旧副本数的spec.updateStrategy.rollingUpdate.Partition字段。假设我现在已经用这个功能已经完成了灰度发布，需要把所有POD都更新到最新版本，那么是不是Edit或者Patch这个StatefulSet，把spec.updateStrategy.rollingUpdate.Partition字段修改成总的POD数即可？

4. 在这一讲中提到ControllerRevision这个API对象，K8S会对StatefulSet或DaemonSet的每一次滚动升级都会产生一个新的ControllerRevision对象，还是每个StatefulSet或DaemonSet对象只会有一个关联的ControllerRevision对象，不同的revision记录到同一个ControllerRevision对象中？

5. Deployment里可以控制保留历史ReplicaSet的数量，那么ControllerRevision这个API对象能不能做到保留指定数量的版本记录？

问题比较多，谢谢！</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/f3/871e4a54.jpg" width="30px"><span>Kanner</span> 👍（23） 💬（3）<div>那为什么Deployment不用ControllerRevison管理版本呢</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（13） 💬（1）<div>一直不理解notation和label的区别，他们的设计思想是什么呢？加污点是前者还是后者？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/8b/3cc461b3.jpg" width="30px"><span>宋晓明</span> 👍（10） 💬（4）<div>老师：有没有公司这样用k8s的：apiserver管理很多pod 每个pod的ip地址全部暴露出来 nginx的upstream配置全是pod的ip地址，访问流程也就是client—&gt;nginx—&gt;pod:port  还有一个程序会监控pod地址变化，一旦变化，自动更新nginx配置。这是新公司使用k8s的流程，感觉好多k8s特性都没用到，比如service，ingress等 大材小用了。。。</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（9） 💬（2）<div>Stateful set 管理的replica 不是通过RS实现的么？</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/5a/2ed0cdec.jpg" width="30px"><span>donson</span> 👍（7） 💬（1）<div>“需要注意的是，在 Kubernetes v1.11 之前，由于调度器尚不完善，DaemonSet 是由 DaemonSet Controller 自行调度的，即它会直接设置 Pod 的 spec.nodename 字段，这样就可以跳过调度器了。”，后来随着调度器的完善，调度器就把DaemonSet的调度逻辑收回，由调度器统一调度。划清边界，领域内聚</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（6） 💬（1）<div>还是没有明白damonset的实现与&quot;污点&quot;的关系，理论上为了实现每个node上有且只有pod, daemonset controller 和nodeaffinity就可以了，为啥需要&quot;污点&quot;机制？</div>2018-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（4） 💬（1）<div>sts 在update的过程中如果失败，并且没有办法restore，比如pulling image fail。这种情况应该怎么恢复？

我尝试再patch一个正确的image 路径，但是没有反应。 然后我delete掉了出错的pod。正常的做法应该是什么？roll out 到上一个&#47;下一个正确版本？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b9/c8/be96e383.jpg" width="30px"><span>放开那坨便便</span> 👍（4） 💬（1）<div>“这样，mysql 这个 StatefulSet 就会严格按照 Pod 的序号，逐一更新 MySQL 容器的镜像。而如果更新有错误，它会自动回滚到原先的版本。”

我测试的时候没有自动回滚，请问自动回滚是如何实现的？需要修改什么配置么？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/fc/f46062b6.jpg" width="30px"><span>abc</span> 👍（0） 💬（1）<div>老师，咨询个问题：既然DaemonSet也是可以定义selector的，那是不是可以理解为可以人为干预DaemonSet Pod调度到指定的节点上去？</div>2018-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIbKCwLRY5icgW3WtLn0JD7EDksicGFqLAsXTm89SjNhR0KIt3N5iaQEmeic4Ld50Yxsceicia5kBODibZPA/132" width="30px"><span>starnop</span> 👍（0） 💬（1）<div>磊哥，请教一个问题， 使用kubeadm 部署kubernetes ，宿主机ip使用dhcp方式，无法固定，在重启后ip改变，这个问题目前看到的一种解法是修改配置文件，重新生成证书等操作，每次开机做这个操作有些繁琐，不知有没有什么别的解法？</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/9d/0ff43179.jpg" width="30px"><span>Andy</span> 👍（15） 💬（1）<div>k8s.gcr.io&#47;fluentd-elasticsearch镜像下不到，百度搜到有人用 mirrorgooglecontainers&#47;前头的镜像替代“科学上网”，
于是访问 https:&#47;&#47;hub.docker.com&#47;r&#47;镜像名&#47;tags 来查看替代镜像的所有版本。

https:&#47;&#47;hub.docker.com&#47;r&#47;mirrorgooglecontainers&#47;fluentd-elasticsearch&#47;tags

找到了以下两个版本来做实验。
mirrorgooglecontainers&#47;fluentd-elasticsearch:v2.0.0

mirrorgooglecontainers&#47;fluentd-elasticsearch:v2.4.0</div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/91/d4/f530914a.jpg" width="30px"><span>陈水金</span> 👍（5） 💬（1）<div>老师您好，有两个问题请教您:1.既然有ControllerVersion这样通用的版本管理对象，为什么Deployment还需要通过ReplicaSet来进行版本控制呢？2.Deployment的ownerReference又是谁呢？期待老师的解惑</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（4） 💬（0）<div>第二十一课:容器化守护进程的意义:DaemonSet
DaemonSet的主要作用是让你在Kubernete集群里，运行有且只有一个DaemonSet Pod，并且会随着新的Node添加或老的Node删除而添加&#47;删除Node上的Pod。它的应用场景有网络插件、存储插件和监控以及日志收集。它很多时候比Kubernetes集群出现的时机都要早。

这种添加删除的过程是，首先从Etcd里获取所有的Node列表，然后遍历所有的Node，看看它是否有运行着带有某种label的Pod。如果没有，就创建一个；如果多了就删除多余的。在创建的时候，通过nodeSelector或者nodeAffiinity字段，还有tolerations字段来和需要运行的Node进行一对一绑定。其中tolerations字段使得DaemonSet能够比其他控制器更早出现在Kubernetes集群启动时候。对了，这个也顺带解决了我一个疑惑，就是我现在K8s环境里的Grafana为啥没有监控到master服务器，因为少了以下这个字段

tolerations:
- key: node-role.kubernetes.io&#47;master
  effect: NoSchedule

K8s中还有一个专门的API用于版本控制，它是ControllerRevision，它在自己的Data字段里保存了对应版本DaemonSet的API对象，还有在Annotation里保存了kubectl的命令</div>2021-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ac/fd/f70a6e3e.jpg" width="30px"><span>大上海</span> 👍（3） 💬（0）<div>GFW问题拉不下来，可以自己先拉下来，再创建

docker pull mirrorgooglecontainers&#47;fluentd-elasticsearch:v2.4.0

docker tag docker.io&#47;mirrorgooglecontainers&#47;fluentd-elasticsearch:v2.4.0 k8s.gcr.io&#47;fluentd-elasticsearch:v2.4.0</div>2021-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/61/b9/dbf629c0.jpg" width="30px"><span>Tao</span> 👍（3） 💬（2）<div>DaemonSet如何保证每个node上只运行一个pod。
	我理解Nodeaffinity保证了daemonSet指定运行在哪些node上，Toleration保证了指定的Node上都可以运行pod；
	但是没有看到那个地方限制了DaemonSet保证在node上只允许一个pod。</div>2019-11-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QKbgfE8mY91fjkLuyDKHUGlpfxKyhiaib5v3ic3YT6qrLibFWxoiaKCxzLeuJROiaWquCb0cNI0lCjiaDY92hSAKHsHUg/132" width="30px"><span>罗罗</span> 👍（1） 💬（0）<div>在这里，你应该注意到 nodeAffinity 的定义，可以支持更加丰富的语法，比如 operator: In（即：部分匹配；如果你定义 operator: Equal，就是完全匹配）  </div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/3f/7825378a.jpg" width="30px"><span>无名氏</span> 👍（1） 💬（1）<div>假设有这么一种场景，业务Pod需要在每个Node上有且只有1个，在灰度升级时，按10%，30%，50%，100%批量升级，后续某个版本再次升级时，这种升级策略可能会变更，比如10%，70%，100%，请问怎么处理，谢谢。</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（1） 💬（0）<div>DJH 问的问题很好，有时候我也有过这样的疑问，稍纵即逝，没有记录下来。我试着回答一下。

1. 如果在一个容器里，命令总有先后顺序。那么你load数据的sql在server启动前如何执行。
2. 应该不会kill吧，不知道有没有参数控制。这样是不是要有一个downtime去做升级？因为可能出现版本不一致中间状态
3 应该把partation参数去掉吧，否则以后增加节点会不会出现意想不到的问题？
4应该是一个版本一个对象，每个版本对象版本号不一样
5 不了解，但是设计应该是一致的。可能有</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d1/49/791d0f5e.jpg" width="30px"><span>aake</span> 👍（0） 💬（0）<div>一个 ReplicaSet 就是应用的一个版本。所以 Deployment 不需要 ControllerRevison ？</div>2024-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（0）<div>集团军群</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/70/4e7751f3.jpg" width="30px"><span>超级芒果冰</span> 👍（0） 💬（0）<div>老师，“这个 Pod，将来只允许运行在“metadata.name”是“node-geektime”的节点上”  这是原文。想问下，怎么给给点的metadata.name属性标记上node-geektime，什么时候可以标记？</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/07/7406fe30.jpg" width="30px"><span>nullptr</span> 👍（0） 💬（0）<div>老师，agent可以搞成DaemonSet，那怎么保证他比应用pod先启动呢？</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/08/52954cd7.jpg" width="30px"><span>丁乐洪</span> 👍（0） 💬（1）<div>有没有playground？</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/fb/837af7bf.jpg" width="30px"><span>董永刚</span> 👍（0） 💬（1）<div>为什么看的时候很明白，但是实际操作的时候就各种问题，桑心</div>2021-02-23</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（0） 💬（0）<div>replicaset是不是也用controllerversion来管理版本的呢？ </div>2020-09-14</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（0） 💬（0）<div>DaemonSet在每个Node上启一个Pod实例，随着Node的增删来起停对应的Pod。

Deployment、StatefuleSet、DaemonSet三者的对比：

  类别  	Deployment	StatefulSet       	DaemonSet         
  数量  	Replicas  	Replicas          	Node数量            
  版本  	Replicates	ControllerVevision	ControllerVevision

在 Kubernetes 项目里，ControllerRevision 是一个通用的版本管理对象。这样，Kubernetes 项目就巧妙地避免了每种控制器都要维护一套冗余的代码和逻辑的问题。
</div>2020-09-14</li><br/>
</ul>