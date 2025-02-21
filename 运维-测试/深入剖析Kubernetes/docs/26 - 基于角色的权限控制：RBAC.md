你好，我是张磊。今天我和你分享的主题是：基于角色的权限控制之RBAC。

在前面的文章中，我已经为你讲解了很多种Kubernetes内置的编排对象，以及对应的控制器模式的实现原理。此外，我还剖析了自定义API资源类型和控制器的编写方式。

这时候，你可能已经冒出了这样一个想法：控制器模式看起来好像也不难嘛，我能不能自己写一个编排对象呢？

答案当然是可以的。而且，这才是Kubernetes项目最具吸引力的地方。

毕竟，在互联网级别的大规模集群里，Kubernetes内置的编排对象，很难做到完全满足所有需求。所以，很多实际的容器化工作，都会要求你设计一个自己的编排对象，实现自己的控制器模式。

而在Kubernetes项目里，我们可以基于插件机制来完成这些工作，而完全不需要修改任何一行代码。

不过，你要通过一个外部插件，在Kubernetes里新增和操作API对象，那么就必须先了解一个非常重要的知识：RBAC。

我们知道，Kubernetes中所有的API对象，都保存在Etcd里。可是，对这些API对象的操作，却一定都是通过访问kube-apiserver实现的。其中一个非常重要的原因，就是你需要APIServer来帮助你做授权工作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>无痕飞客</span> 👍（39） 💬（4）<div>老师，怎么优雅的卸载掉kubernetes呢？</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（29） 💬（1）<div>为什么要生命这类service account，不能直接使用role进行权限分配吗？这个中间代理的好处是啥呢？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/eb/b5bb4227.jpg" width="30px"><span>runner</span> 👍（13） 💬（1）<div>老师还是之前的问题，现在机器上有一个手动起的容器（比如是老的业务容器），想把他加到pod里管理起来，比如pod生成的时候发现已经有这个容器了，就关联这个容器，不再创建了。有办法实现么？</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（8） 💬（5）<div>但在这种情况下，这个默认 ServiceAccount 并没有关联任何 Role。也就是说，此时它有访问 APIServer 的绝大多数权限。
为什么没有关联role，就会有绝大多数权限呢？有一个默认的role么，都有什么权限呢？

另外，建议在所有的namespace给default serviceaccount绑定view，是出于安全的考虑是么？</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（4） 💬（6）<div>Prior to Kubernetes 1.6, many deployments used very permissive ABAC policies, including granting full API access to all service accounts.

Default RBAC policies grant scoped permissions to control-plane components, nodes, and controllers, but grant no permissions to service accounts outside the kube-system namespace (beyond discovery permissions given to all authenticated users).

Quoting from https:&#47;&#47;kubernetes.io&#47;docs&#47;reference&#47;access-authn-authz&#47;rbac&#47;#service-account-permissions

按我对官方文档的理解，RBAC策略下 default service account 是不是并没有任何权限，ABAC才会grant full access？

如果给所有namespace的default service account都赋予view 权限。会不会出现如下风险？
Warning: This allows any user with read access to secrets or the ability to create a pod to access super-user credentials.
</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（2） 💬（2）<div>role roleBanding serviceAccount 都是 namespaced , 那跨namespace 操作会怎么样？</div>2018-10-26</li><br/><li><img src="" width="30px"><span>无痕飞客</span> 👍（1） 💬（1）<div>老师，我kubernetes安装好了，怎么停止启动的kube进程并且卸载掉kubernetes呢？</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（66） 💬（12）<div>kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: readonly-all-default
subjects:
- kind: User
  name: system.serviceaccount.default
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/f9/4412b473.jpg" width="30px"><span>喜剧。</span> 👍（40） 💬（3）<div>kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
name: readonly-all-default
subjects:
- kind: ServiceAccount
name: system.serviceaccount.default
roleRef:
kind: ClusterRole
name: view
apiGroup: rbac.authorization.k8s.io

前面的朋友写的问题在于，default应该是serciveacount</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5d/c8/7ece6f4b.jpg" width="30px"><span>蹦蹦</span> 👍（14） 💬（4）<div>kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: readonly-all-default
subjects:
- kind: ServiceAccount
  name: default
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io

kind是ServiceAccount，不是Group。name直接写default，不指定namespace
</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（9） 💬（4）<div>老师，我查阅了相关资料。觉得思考题中的场景（为【所有namespace】下的【default service account】添加只读权限）无法实现。ClusterRoleBinding的subjects字段最多能允许我们给【default namespace】下的【所有service account】或者所有namespace下的所有 service account添加只读权限。不知道老师是否有其他方式实现？恳请回答，感谢。

思考题请问:
如何为所有 Namespace 下的默认 ServiceAccount（default ServiceAccount），绑定一个只读权限的 Role 呢？请你提供 ClusterRoleBinding（或者 RoleBinding）的 YAML 文件。</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/c3/e545ba80.jpg" width="30px"><span>张振宇</span> 👍（9） 💬（0）<div>老师rbac怎么结合企业自己的ldap用户数据进行外部登录自研的web平台</div>2019-02-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/nhLS152kEs5J65bBpM2fzMn4agfoow8xibFzNSDcmo9Oiby2lNB4hWRcetRWFyY2y05IJu8GbkZer9BUiahtadU0w/132" width="30px"><span>yuanlinios</span> 👍（7） 💬（4）<div>虽然 clusterrole&#47;clusterrolebinding 不受 namespace 限制, 但是 serviceaccount 总是存在于 namespace 下. 为一个 namespace 下的 default sa 做只读限制很容易. 那么怎么为&quot;所有&quot; (包括现有的和未来的) 的 namespace 下的 default sa 做只读的限制? 希望给点提示

</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/c4/4ee2968a.jpg" width="30px"><span>艾利特-G</span> 👍（6） 💬（3）<div>关于课后思考，我看了官方文档的这个例子。
&gt; https:&#47;&#47;kubernetes.io&#47;docs&#47;reference&#47;access-authn-authz&#47;rbac&#47;#rolebinding-and-clusterrolebinding
暂时得出的结论是通过ClusterRoleBinding做不到让每个NameSpace下的&quot;default&quot; ServiceAccount拥有namespaced resources的只读权限。
这里面描述了如何在ClusterRolebinding中将ClusterRole与&quot;manager&quot;这个group绑定。但是这个&quot;manager&quot; group，是一个user的group，不是ServiceAccount的group。
我想，将ClusterRolebinding其中的subjects[0].kind属性指定为ServiceAccount，name指定为system:serviceaccount:*:default，应该是无效的吧。
如果这样不行的话，那就只有subjects[0].kind属性指定为group，然后name指定为system:serviceaccounts，这将会对所有ServiceAccount绑定&quot;view&quot;这个ClusterRole，包括&quot;default&quot;之外的ServiceAccount。这样会对所有ServiceAccount授权集群级别的只读权限，也就是不能限制在该ServiceAccount所在的Namespace下。
如果在每个Namespace下创建RoleBinding，subjects[0].kind属性指定为ServiceAccount，name指定为default，namespace指定为该namespace，则可以使每个NameSpace下的&quot;default&quot; ServiceAccount拥有该Namespace的只读权限。</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（4） 💬（2）<div>kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: readonly-all-default
subjects:
- kind: ServiceAccount
  name: default
  namespace: system:systemaccounts
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io

老师，请问这样写对吗？</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/ac/bb/db0f9d8c.jpg" width="30px"><span>tale</span> 👍（3） 💬（1）<div>思考题正解在此：

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: readonly-all-default
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io

关于subjects中kind的解释：

1、kind为ServiceAccount的话，官方文档明确说了必须指定namespace的，所以排除这种方式。
2、kind为User时，name中一定会带有&lt;namespace&gt;信息，与题目要求“所有namespace”不符，所以也排除。
3、kind为Group时，name中填system:serviceaccounts即可。很多人担心这个Group过大，可能不止包含了所有default“用户”。但经我查明，这个Group只有Get权限，所以符合View规则，即使包含了其他“用户”也无妨。</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（3） 💬（0）<div>老师，我就想问一下，namespace 下的 default sa 没有关联任何 role，它到底有哪些权限呢？</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/b9/f2481c2c.jpg" width="30px"><span>诗泽</span> 👍（2） 💬（0）<div>“实际上，一个 ServiceAccount，在 Kubernetes 里对应的“用户”的名字是：”
ServiceAccount 有namespace 但是用户没有，那serviceaccount 与用户的映射关系是怎样的呢，所有namespace 的default ServiceAccount 对应同一个user 吗？即system.serviceaccount.default ？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/67/c0128e6c.jpg" width="30px"><span>Dillion</span> 👍（2） 💬（0）<div>system:serviceaccount:&lt;ServiceAccount 名字 &gt;
老师，这个ServiceAccount名字前面，是不是应该还有namespace</div>2018-10-22</li><br/><li><img src="" width="30px"><span>孙俊伟</span> 👍（1） 💬（0）<div>我测试情况是，默认default namespace的default sa账号连只读权限都没有。加了view 后可以只读list get。另外即使加了cluster-admin，依旧无法修改集群服务yaml。。。求解？能否突破该限制？</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c3/94/e89ebc50.jpg" width="30px"><span>神毓逍遥</span> 👍（1） 💬（0）<div>课代表来了，最近使用部署的 AWS 上的项目，由于config 中是 aws 特质的 CLI 命令，需要重新生成一个账号与去哪先，我自己使用的 LEN 工具，图形化界面操作，非常好用；另外这张内容蛮重要的，结合自己的经验主要在，1. 学会如何创建 账号、角色、绑定，方便授权权限，2则理解 
system:serviceaccount:&lt;Namespace名字&gt;:&lt;ServiceAccount名字&gt; 这个结构的含义，一定要注意，因为操作中报错，极大的概率会遇到这个问题，理解概念方便排查</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（0）<div>第二十六课:基于角色权限的控制：RBAC
K8s负责完成授权工作的机制就是RBAC。其中有三个基本概念：Role（定义了一组对K8s API对象的操作权限的规则），Subject（被规则作用的用户，可以是人user，也可以是机器servicaccount）和RoleBinding（将Role和Subject绑定起来）。以上概念是针对namespace的API对象，比如Pod等，对于没有namespace概念的,比如Node，PV，用的是ClusterRole和ClusterRoleBinding</div>2021-10-15</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（1） 💬（2）<div>实测通过，所有默认default serviceaccount有了list pod的权限

#cat example-clusterrolebinding.yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: example-clusterrolebinding
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: example-clusterrole
  apiGroup: rbac.authorization.k8s.io</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/04/5837b21c.jpg" width="30px"><span>Brown羊羊</span> 👍（1） 💬（2）<div>kind: RoleBinding
apiVersion: rbac.authorization.k8s.io&#47;v1
metadata:
  name: example-rolebinding
subjects:
- kind: Group
  name: system:serviceaccounts
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/f9/f5d0dbc8.jpg" width="30px"><span>吕凯 🌴</span> 👍（1） 💬（0）<div>我是使用的二进制方式部署，ClusterRole为system:kube-scheduler绑定到system:kube-scheduler用户，跟kube-system namespace无关</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/f9/2b4755b5.jpg" width="30px"><span>看不穿</span> 👍（1） 💬（2）<div>老师，问个网络问题，如果集群外部想访问集群里面的pod服务，可以用ingress或者NodePort实现；那请问pod想访问集群外部的服务应该怎么办？</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/ba/2c8af305.jpg" width="30px"><span>Geek_zz</span> 👍（1） 💬（0）<div>rbac 和token是怎么联系的呢</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/d9/bf/897f4f93.jpg" width="30px"><span>打小就会敲代码</span> 👍（0） 💬（1）<div>apiVersion: rbac.authorization.k8s.io&#47;v1
kind: RoleBinding
metadata:
  name: readonly-all-serviceaccount
subjects:
  - kind: Group
    name: system:serviceaccounts
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  apiGroup: rbac.authorization.k8s.io
  name: view
</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（0） 💬（0）<div>思考题就没人想过修改default secrets吗🤔</div>2023-03-07</li><br/><li><img src="" width="30px"><span>click</span> 👍（0） 💬（0）<div>https:&#47;&#47;stackoverflow.com&#47;questions&#47;52995962&#47;kubernetes-namespace-default-service-account
&gt; By default, the default service account in a namespace has no permissions other than those of an unauthenticated user. </div>2023-02-07</li><br/>
</ul>