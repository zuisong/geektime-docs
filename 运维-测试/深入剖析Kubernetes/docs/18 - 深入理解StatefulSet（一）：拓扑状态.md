你好，我是张磊。今天我和你分享的主题是：深入理解StatefulSet之拓扑状态。

在上一篇文章中，我在结尾处讨论到了Deployment实际上并不足以覆盖所有的应用编排问题。

造成这个问题的根本原因，在于Deployment对应用做了一个简单化假设。

它认为，一个应用的所有Pod，是完全一样的。所以，它们互相之间没有顺序，也无所谓运行在哪台宿主机上。需要的时候，Deployment就可以通过Pod模板创建新的Pod；不需要的时候，Deployment就可以“杀掉”任意一个Pod。

但是，在实际的场景中，并不是所有的应用都可以满足这样的要求。

尤其是分布式应用，它的多个实例之间，往往有依赖关系，比如：主从关系、主备关系。

还有就是数据存储类应用，它的多个实例，往往都会在本地磁盘上保存一份数据。而这些实例一旦被杀掉，即便重建出来，实例与数据之间的对应关系也已经丢失，从而导致应用失败。

所以，这种实例之间有不对等关系，以及实例对外部数据有依赖关系的应用，就被称为“有状态应用”（Stateful Application）。

容器技术诞生后，大家很快发现，它用来封装“无状态应用”（Stateless Application），尤其是Web服务，非常好用。但是，一旦你想要用容器运行“有状态应用”，其困难程度就会直线上升。而且，这个问题解决起来，单纯依靠容器技术本身已经无能为力，这也就导致了很长一段时间内，“有状态应用”几乎成了容器技术圈子的“忌讳”，大家一听到这个词，就纷纷摇头。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（109） 💬（5）<div>今天按文章中的内容来, 确实也遇到了nslookup 反馈失败的状况.
** server can&#39;t find web-0.nginx: NXDOMAIN
*** Can&#39;t find web-0.nginx: No answer
但是直接ping  web-0.nginx 是可以获取真实ip地址的.
确实是如楼下的同学所说, 需要用 busybox:1.28.4 的镜像. 这个是最新版busybox的问题.
kubectl run -i --tty --image busybox:1.28.4 dns-test --restart=Never --rm &#47;bin&#47;sh
这样就可获得期待的结果了.
我也是google到了 https:&#47;&#47;github.com&#47;kubernetes&#47;kubernetes&#47;issues&#47;66924 才知道的.
再看楼下的评论,才发现有其他同学也遇到了,且在几天前已经给出了解决方案. 👍
新技术确实变化太快了,作者在写文章时用的没问题,也许隔一天因为某个默认镜像修改了,就会出现新的状况.</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ec/3d/7efdb149.jpg" width="30px"><span>Geek_hfne2s</span> 👍（64） 💬（7）<div>创建statefulset必须要先创建一个headless的service?分两步操作？</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/67/c0128e6c.jpg" width="30px"><span>Dillion</span> 👍（49） 💬（5）<div>在上面的例子中，web-0、web-1启动后，此时如果web-0挂了，那在创建web-0的过程中，web-1也会被重新创建一次么？？？也就是如果一个StatefulSet中只有某个Pod挂了，在重启它的时候，如何确保文中说的Pod启动顺序呢？？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/4b/170654bb.jpg" width="30px"><span>千寻</span> 👍（35） 💬（2）<div>说dns访问不到那个童鞋，不要用latest标签的busybox，用busybox:1.28.4这个tag的就可以了，我也是这样。</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/2e/01b2839e.jpg" width="30px"><span>巩夫建</span> 👍（31） 💬（9）<div>Headless Service中不通过vip，外部访问的时候，是轮询还是随机还是热备的方式访问到web-0和web-1，dns解析好像没有轮询随机概念吧。</div>2018-10-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PUiby8MibibKcMd88OtDq1c0myEILZjap46fyiaOlML0UlNWzj9NTIEXOhXCCR1tcUibG0I6UoGp59Zj8H5EYwzkY9g/132" width="30px"><span>fldhmily63319</span> 👍（26） 💬（5）<div>我也想问， &quot;Normal Service&quot;和&quot;Headless Service“的应用场景是什么？

根据文章所说的，”Headless Service不需要分配一个 VIP，而是可以直接以 DNS 记录的方式解析出被代理 Pod 的 IP 地址“，同时由于其编号的严格规定，会按照编号顺序完成创建工作。

这样是不是说，如果在部署StatefulSet的时候，大部分是推荐使用&quot;Headless Service&quot; ，而不是&quot;Normal Service”呢？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（15） 💬（1）<div>通过这种方法，Kubernetes 就成功地将 Pod 的拓扑状态（比如：哪个节点先启动，哪个节点后启动），按照 Pod 的“名字 + 编号”的方式固定了下来。
如上所述，
1. 是否可以这样理解：sts在这里只是保留了“名字 + 编号”这种网络身份，而不同网络身份对应的pod其实本质上是一样的，都是同一个模板replicate出来的？
2. 这里sts的主要意义是什么呢：仅仅是保证不同网络身份的启动顺序？</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/c7/1640226d.jpg" width="30px"><span>刘欣洲</span> 👍（15） 💬（3）<div>访问不到啊
&#47; # nslookup web-0.nginx
Server:		10.96.0.10
Address:	10.96.0.10:53

** server can&#39;t find web-0.nginx: NXDOMAIN

*** Can&#39;t find web-0.nginx: No answer

是不是需要DNS插件啊， 该如何启动呢？</div>2018-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/c3/8e1a8dbf.jpg" width="30px"><span>Plantegg</span> 👍（11） 💬（1）<div>首先busybox镜像的&#47;bin&#47; 下几百个可执行命令的md5签名都是一样的。不能按照正常的ping、nslookup逻辑来理解了。 也就是md5sum &#47;bin&#47;ping 和 md5sum &#47;bin&#47;nslookup 签名一样，我猜测这个可执行命令都是空架子，会被拦截下来。
另外就是1.28.4和1.29.3（latest) 的 nslookup 签名也不一样了</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/08/c43f85d9.jpg" width="30px"><span>IOVE.-Minn</span> 👍（8） 💬（2）<div>请教张大佬，当我跑jenkins in k8s的时候是用的statefulset部署的jenkins的master，我关联的service但是却不是无头服务啊，  spec.ports 是用的nodeport  也没有用clusterIP：none这样。但是整个服务也是正常的。这不是和你讲的statefulset必须是关联headless service违背了么？</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（8） 💬（3）<div>既然默认有安装dns 为啥还要开启dns插件呢</div>2018-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（7） 💬（1）<div>service里的dns信息是存在etcd里的嘛？有些应用的pod的域名是自己定义的。而不是k8s创建出来的带有local的域名。我可以更改service里的dns信息嘛？</div>2018-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（7） 💬（1）<div>您好。滚动升级的时候，如果新的web-0和老的web-2同时ready，但新老版本不兼容怎么办？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/09/da/2fbd0760.jpg" width="30px"><span>兽医</span> 👍（6） 💬（1）<div>请问当需要对StatefulSet进行缩容后，再扩容到原有规模。在涉及变动的Pod中，状态也会被保持吗？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/f5/ffc2bb23.jpg" width="30px"><span>Rodinian</span> 👍（5） 💬（1）<div>一直很好奇，normal service和headless service都可以指定DNS name。那两者的区别是什么？</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/0b/81ae214b.jpg" width="30px"><span>凌</span> 👍（5） 💬（3）<div>我们的服务都是通过固定ip+tcp的方式访问的，如果按照kubernetes的理念应该每次先用服务命取得一次ip在建连访问？</div>2019-01-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIacvl2hoQU10YHABicE8cTu2IKiagWw9wXPiaRcvJfF1tL2ticJVzHGqd7LmTaDuIScvPDhhMOucjUtg/132" width="30px"><span>zoroyouxi</span> 👍（4） 💬（1）<div>实践中有一点疑问，既然sts是pod的实际所有者并不经过rs，那为什么sts声明下的pod的restartpolicy也只能设置成always呢?希望张老师解答谢谢</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（4） 💬（1）<div>service没有VIP作为头。这个头到底怎么理解呢？还是不太懂什么是头。</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/ff/6b0260e1.jpg" width="30px"><span>徐骋</span> 👍（3） 💬（1）<div>既然Headless service没有VIP，是不是说只能在Kubernetes内部访问通过service name它？</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（3） 💬（2）<div>张老师, 还是有个疑问 &quot;statefulset中的pod template都是一样的，那比如说对于主从结构，应用如何知道自己是主还是从呢？而且一旦从挂掉了，为了保证启动顺序，主也要重启？&quot;  这个问题您的回答是 主也要重启. 有一个疑问, 为什么主也要重启, 主是好的呀 RUNNING &amp;&amp; Ready, 这个时候满足了从的启动条件, 从直接启动不就好了吗? 为什么主也要跟着启动一次?</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/37/7f575aec.jpg" width="30px"><span>vx:jiancheng_goon</span> 👍（3） 💬（1）<div>每次pod被重新创建后，都能够保证原来的网络标示，那有什么办法，能够固定ip呢？</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（3） 💬（1）<div>statefulset通过dns访问pod 是否必须要启动dns插件？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（2） 💬（1）<div>有两点不太明白的，请教一下。
“任何pod的变化都会触发一次statefulset的滚动更新。”
这句话怎么理解呢？实际使用上，比如我用statefulset创建了一个3个pod的etcd集群，我删掉etcd-1,etcd-1会马上重新启动，但etcd-0和etcd-2并不会被删掉重建啊。

headless server是不是只适合于这种用来做集群节点的发现使用，不适合像service那样用来开放服务访问？
用nslookup来查看headless server, nslookup etcd, 会返回3个对应pod的ip地址， 但直接去ping etcd的话，每次都会返回同一个pod的ip地址，其他两个地址永远不会被ping到。
那我建立集群的时候，去发现节点的ip时，是不是就不能直接简单配置为etcd了呢，而要配置etcd-0.etcd, etcd-1.etcd这样每个都去配置呢？

</div>2018-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/08/c43f85d9.jpg" width="30px"><span>IOVE.-Minn</span> 👍（1） 💬（1）<div>请问，“有状态的是pv，不是副本控制器，statefulset不用pv创建的pod是无状态”这句话是对的么？  是不是其实statefulset是无状态的，其实是给有状态的服务扩容和伸缩？ 那么initcontainer其实只是维护了有状态服务的拓扑状态？

</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（1） 💬（1）<div>关于nslookup无法解析的问题，debug了下dnspod的log。使用命令 `kubectl logs -f kube-dns-86f4d74b45-28xdg kubedns -n kube-system` 来监视dns pod的log。
当 `kubectl delete -f svc.yaml` 的时候，会有一个log出现：
`I1007 14:12:32.818523       1 dns.go:555] Could not find endpoints for service &quot;nginx&quot; in namespace &quot;default&quot;. DNS records will be created once endpoints show up.`
期待这个问题会随着k8s的学习深入得到解决。
</div>2018-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（1） 💬（1）<div>同楼上的问题，我这里是按照kubeadm安装的（kube-system中也添加了weave-net），但是nslookup也是报错，不知道为什么。

不过我在dsn-test的pod中运行 `ping web-1.nginx` 或者 `ping web-1.nginx.default.svc.cluster.local` 都是可以找得到对应的ip的。</div>2018-10-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GDYkD2X7pXSKUSaUFC8u3TBPaakaibnOBV2NYDc2TNfb8Su9icFMwSod6iaQX5iaGU2gT6xkPuhXeWvY8KaVEZAYzg/132" width="30px"><span>extraterrestrial！！</span> 👍（1） 💬（1）<div>有同样的问题，statefulset的template配置没有指定主从的选项，要怎么配置主从？ 比如配一个redis的主从？</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/e2/823a04b4.jpg" width="30px"><span>小小笑儿</span> 👍（1） 💬（1）<div>statefulset中的pod template都是一样的，那比如说对于主从结构，应用如何知道自己是主还是从呢？而且一旦从挂掉了，为了保证启动顺序，主也要重启？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（1） 💬（1）<div>那么两种service模式应用场景通常有哪些？</div>2018-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（0） 💬（2）<div>这个好像很难用在真实场景，我想让pod以指定的顺序启动怎么办，这个好像也是每个pod的状态相同，只是在启动后被statefulset规定的拓扑，然后按照拓扑来运作，很迷惑</div>2018-12-25</li><br/>
</ul>