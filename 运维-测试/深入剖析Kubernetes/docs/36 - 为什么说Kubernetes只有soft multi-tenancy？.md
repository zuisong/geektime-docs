你好，我是张磊。今天我和你分享的主题是：为什么说Kubernetes只有soft multi-tenancy？

在前面的文章中，我为你详细讲解了Kubernetes生态里，主流容器网络方案的工作原理。

不难发现，Kubernetes的网络模型，以及前面这些网络方案的实现，都只关注容器之间网络的“连通”，却并不关心容器之间网络的“隔离”。这跟传统的IaaS层的网络方案，区别非常明显。

你肯定会问了，Kubernetes的网络方案对“隔离”到底是如何考虑的呢？难道Kubernetes就不管网络“多租户”的需求吗？

接下来，在今天这篇文章中，我就来回答你的这些问题。

在Kubernetes里，网络隔离能力的定义，是依靠一种专门的API对象来描述的，即：NetworkPolicy。

一个完整的NetworkPolicy对象的示例，如下所示：

```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

我在和你分享前面的内容时已经说过（这里你可以再回顾下第34篇文章[《](https://time.geekbang.org/column/article/67351)[Kubernetes 网络模型与 CNI 网络插件](https://time.geekbang.org/column/article/67351)[》](https://time.geekbang.org/column/article/67351)中的相关内容），**Kubernetes里的Pod默认都是“允许所有”（Accept All）的**，即：Pod可以接收来自任何发送方的请求；或者，向任何接收方发送请求。而如果你要对这个情况作出限制，就必须通过NetworkPolicy对象来指定。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/18/34/c082419c.jpg" width="30px"><span>风轨</span> 👍（128） 💬（1）<div>job，cronjob这类计算型pod不需要也不应该对外提供服务，可以拒绝所有流入流量，提高系统安全。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（13） 💬（1）<div>iptables -A FORWARD -d $podIP -m physdev --physdev-is-bridged -j KUBE-POD-SPECIFIC-FW-CHAIN

文中提到，上面这条iptables规则的作用是：“拦截”在同一个宿主机、接入同一个bridge上的容器发送过来的数据包。

iptables设置的是IP包被过滤处理的规则，而bridge是二层设备，数据包在bridge上的流动，如果受到上面规则的控制，就是说iptables还能设置二层链路的过滤规则？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9f/a1/d75219ee.jpg" width="30px"><span>po</span> 👍（4） 💬（1）<div>老师你好，我想确认下基于ovs的网络，是不是不用iptables了，使用openflow实现networkpolicy，使用vni实现多租户，谢谢。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8c/db/90b7b2a9.jpg" width="30px"><span>OldGood</span> 👍（2） 💬（1）<div>老师，什么时候讲ingress？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/3c/b5a00c1a.jpg" width="30px"><span>johnson.skiii</span> 👍（17） 💬（5）<div>张大请教一下；本来kube-proxy就会写大量的iptables规则，如果网络情况复杂，实施的networkpolicy又多的话，那么iptables会不会成为比较大的瓶颈，有什么好的解决方案吗？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（14） 💬（0）<div>文章中对iptables的讲解, 是我见过的对iptables讲解的最好的一个, 厉害</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/30/2f8b78e9.jpg" width="30px"><span>CYH</span> 👍（4） 💬（2）<div>hi，老师：请问我安照k8s官网拒绝所有进出流量，为什么该pod还是能ping通外部的ip呢？</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ca/13/0b8c7184.jpg" width="30px"><span>Jerome</span> 👍（3） 💬（2）<div>2021-11-23，第四遍学习打卡。</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（3） 💬（0）<div>2020-04-06，打卡。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/2f/71ffe33e.jpg" width="30px"><span>heartbeat</span> 👍（2） 💬（2）<div>任何 Namespace 里的、携带了 project=myproject 标签的 Pod； namespaceselector应该是选择namespace的吧，project=myproject这个标签应该是匹配namespace的而不是匹配pod的，所以上面那个解释应该是携带了project=myproject 标签的所有namespace下的所有pod 不知道这个理解是否正确</div>2019-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（2） 💬（0）<div>老师您好，请教一个问题，我在阿里云测试环境部署的高可用集群，部署的时候关闭了iptables service，后来尝试开启，但是遇到容器内无法跟kubernetes 的cluster通信的问题。我看了&#47;etc&#47;sysconfig&#47;iptables的配置，input配置的是drop，然后开放一些常用端口和所有内网ip，不知道应该如何排查了</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/65/b80035a6.jpg" width="30px"><span>ryan</span> 👍（1） 💬（0）<div>第二遍终于看懂一些了，老师太厉害了</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/7f/1c505317.jpg" width="30px"><span>killua</span> 👍（1） 💬（1）<div>iptable的规则多的话 会有性能问题吗？</div>2020-07-09</li><br/><li><img src="" width="30px"><span>0mfg</span> 👍（1） 💬（0）<div>[BGP 消息]
我是宿主机 192.168.1.2
10.233.2.0&#47;24 网段的容器都在我这里
这些容器的下一跳地址是我

和老师确认一下对应图例10.233.2.0&#47;24应该是10.233.1.0&#47;24吧</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（1） 💬（0）<div>apiVersion: extensions&#47;v1beta1
kind: NetworkPolicy
metadata:
  name: my-network-policy
  namespace: my-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress

我只能想到一种情况：随机数生成器，因为要保证产生的随机数不受任何干扰，所以可以禁掉所有内网访问，只要把产生的结果发送出去就可以。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/bf/863d440a.jpg" width="30px"><span>jaxzhai</span> 👍（1） 💬（0）<div>apiVersion: networking.k8s.io&#47;v1
kind: NetworkPolicy
metadata:
  name: deny-all-policy
  namespace: my-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress

可以做访问策略，我理解成可以是区域隔离。</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5f/f8/1d16434b.jpg" width="30px"><span>陈麒文</span> 👍（0） 💬（0）<div>科普了一下iptables，参考网址：https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;441089738</div>2022-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d6/fb/837af7bf.jpg" width="30px"><span>董永刚</span> 👍（0） 💬（1）<div>老师，“携带了 project=myproject 标签的 Namespace 里的任何 Pod；”这句话如何理解？

所有namespace里面携带了  project=myproject 标签 的pod？</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>NetworkPolicy 实际上只是宿主机上的一系列 iptables 规则。这跟传统 IaaS 里面的安全组（Security Group）其实是非常类似的。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/a6/cb7350b9.jpg" width="30px"><span>Geek_e1336f</span> 👍（0） 💬（1）<div>“第二条 FORWARD 链“拦截”的则是最普遍的情况，即：容器跨主通信。这时候，流入容器的数据包都是经过路由转发（FORWARD 检查点）来的。” ，到forward链不都经过路由判断不是本机的要转发给其它节点吗？为啥会在forward链上呢？不应该在input链做验证吗？</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（0） 💬（0）<div>第三十六课:为什么说Kubernetes只有soft multi-tenancy？
k8s里的Pod默认都是“允许所有Accept All”的访问，而一旦Pod被NetworkPolicy选中，那这个Pod就会进入“拒绝所有Deny All”，其实NetworkPolicy就是个“白名单”。

K8s网络插件对Pod进行隔离，其实是考在主机上生成NetworkPolicy对应的iptables规则来实现的。</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/1b/f5/52dada23.jpg" width="30px"><span>Fresh feel</span> 👍（0） 💬（0）<div>老师我想问一下，“所以说，Kubernetes 从底层的设计和实现上，更倾向于假设你已经有了一套完整的物理基础设施。然后，Kubernetes 负责在此基础上提供一种“弱多租户”（soft multi-tenancy）的能力。”我是不是可以理解成在IaaS云上依靠IaaS的能力本身就实现了隔离；而如果是私有化部署的话感觉使用NetworkPolicy的方式也不比IaaS的隔离直观，或者是设置几个默认的NetworkPolicy规则来对应限制IaaS中租户&#47;项目的隔离访问。还有就是在管理上是不是也不如IaaS方便，管理的疑问是不是需要都看完能获得解答。</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/7d/ac715471.jpg" width="30px"><span>独孤九剑</span> 👍（0） 💬（0）<div>还是要学好linux啊</div>2021-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Um0fKCDsGBRO1CEia0EwoIb11icf0SlFBTT63XAy1DooRZeBvavefTcSNQOSSdDthSpAgknjtfNqF4fo15wEJ7SQ/132" width="30px"><span>张裕尧</span> 👍（0） 💬（1）<div>有一个问题想请教一下，Flannel 项目为什么不添加NetworkPolicy的功能呢？Flannel应该也可以有能力在宿主机上创建iptables</div>2021-01-17</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（0） 💬（0）<div>Kubernetes里通过NetworkPolicy对象来设置Pod的网络隔离，比如允许Pod接受哪些请求(ingress)，允许Pod像哪些发出请求(egress)。

NetworkPolicy实际上只是宿主机的一系列iptables规则，它没有像传统IaaS一样提供一个二层网络的强隔离。所以说，Kubernets从底层的设计和实现上，更倾向于假设你已经有了一套完整的物理基础设施。然后Kubernets负责在此基础上提供一种“弱多租户”（soft multi-tenancy）的能力。
</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div>apiVersion: extensions&#47;v1beta1
kind: NetworkPolicy
metadata:
    name:  my-network-policy1
    namespace: myspace
spec:
    podSelector: {}
    policyTypes:
    - Ingress

像这样全封闭的Pod,适用于计算密集型的吧,一般可以使用于去进行一些自我计算,计算完成就死亡的Pod</div>2020-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/01/96/afcb6174.jpg" width="30px"><span>冬冬</span> 👍（0） 💬（0）<div>k8s使用NetworkPolicy定义pod的隔离机制，使用ingress和egress定义访问策略（限制可请求的pod及namespace、port端口），其本质上是k8s网络插件在宿主机上生成了iptables路由规则；
</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（0） 💬（0）<div>精彩，再说一次。。。</div>2020-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/88/528442b0.jpg" width="30px"><span>Dale</span> 👍（0） 💬（0）<div>纯计算类型的pod，不对外暴露任何服务，比较适合拒绝网络请求</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>k8s的网络配置的前提是：你的物理基础设施已经就绪</div>2019-11-23</li><br/>
</ul>