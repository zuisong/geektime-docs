你好，我是张磊。今天我和你分享的主题是：深入解析声明式API之编写自定义控制器。

在上一篇文章中，我和你详细分享了Kubernetes中声明式API的实现原理，并且通过一个添加Network对象的实例，为你讲述了在Kubernetes里添加API资源的过程。

在今天的这篇文章中，我就继续和你一起完成剩下一半的工作，即：为Network这个自定义API对象编写一个自定义控制器（Custom Controller）。

正如我在上一篇文章结尾处提到的，“声明式API”并不像“命令式API”那样有着明显的执行逻辑。这就使得**基于声明式API的业务功能实现，往往需要通过控制器模式来“监视”API对象的变化（比如，创建或者删除Network），然后以此来决定实际要执行的具体工作。**

接下来，我就和你一起通过编写代码来实现这个过程。这个项目和上一篇文章里的代码是同一个项目，你可以从[这个GitHub库](https://github.com/resouer/k8s-controller-custom-resource)里找到它们。我在代码里还加上了丰富的注释，你可以随时参考。

总得来说，编写自定义控制器代码的过程包括：编写main函数、编写自定义控制器的定义，以及编写控制器里的业务逻辑三个部分。

首先，我们来编写这个自定义控制器的main函数。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（108） 💬（3）<div>Informer 和控制循环分开是为了解耦，防止控制循环执行过慢把Informer 拖死</div>2018-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（47） 💬（3）<div>看了这两天的文章，感觉k8s的机制实在是太具有普适性了，可以基于它构建各种分布式业务平台。本质上它就是一个分布式对象管理平台。</div>2018-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/88/8cbf2527.jpg" width="30px"><span>超</span> 👍（36） 💬（3）<div>如果一个master 管理的node非常多 通过ListAndWatch 会对master的性能有影响吧</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ac/c8/4b1c0d40.jpg" width="30px"><span>勤劳的小胖子-libo</span> 👍（18） 💬（1）<div>一般这种工作队列结构主要是为了匹配双方速度不一致，也为了decouple双方。比如典型生产者消费者问题</div>2018-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（12） 💬（2）<div>请问老师，如果用deployment部署一个tag是latest的镜像，怎样进行滚动更新呢？set image的话tag不变，不能出发更新呢</div>2018-10-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLtwSXKialWYQgo1OXWYIsyj4zxK8AbQb1tp6iceZ5cGPYFcoczlubd7VicJPuvWqHrFXJXtUTP4kd9A/132" width="30px"><span>Monokai</span> 👍（6） 💬（1）<div>处理完api对象的事件后就直接存储在etcd里了么？需不需要再和apiserver打交道？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（6） 💬（1）<div>请问这个控制器是跑在node节点上的？一般哪些控制器是跑在node上哪些是跑在master上呢</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（5） 💬（1）<div>我在读完后，和学习的期间，发现不仅仅CRD有Informer,workqueue构成的自定义控制器，而且client-go中也有个类似的，这两者之间有什么联系吗，还是就是一个东西</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/eb/b5bb4227.jpg" width="30px"><span>runner</span> 👍（5） 💬（1）<div>张老师，问个问题，我们公司的docker业务，容器总数上万个，部分容器依赖宿主机配置文件。现在我们想迁k8s 的话，能不改动这些容器，把他们加入pod管理起来么？如果上万容器都重新调度生成的话，这个改动太大了。</div>2018-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/41/9170f607.jpg" width="30px"><span>LinYongRui</span> 👍（4） 💬（1）<div>张老师您好，请问如果在这个框架下，有人手动删除了一个实际的neutron network，但是本地缓存和apiserver的状态是一致的，那么在period sync的时候，是不是就不会去真正检查实际状态和本地缓存的差别了呢？因为我看到eventhandler的update那边会直接return了？ 谢谢</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/fa/5714677b.jpg" width="30px"><span>sonald</span> 👍（3） 💬（1）<div>看起来自定义的控制器是独立运行的，而不能像一个API对象一样注册到master，并且部署到master上之类的？</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/66/14/060890da.jpg" width="30px"><span>寒青</span> 👍（1） 💬（1）<div>通过aggregation layer扩展k8s api 的方式会讲吗？谢谢</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/89/9312b3a2.jpg" width="30px"><span>Vincen</span> 👍（1） 💬（1）<div>按照文章中的步骤，还需要安装neutron网络吗</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（0） 💬（1）<div>张老师, 例子中关于event有一个疑问
`utilruntime.Must(networkscheme.AddToScheme(scheme.Scheme))
glog.V(4).Info(&quot;Creating event broadcaster&quot;)
eventBroadcaster := record.NewBroadcaster()
eventBroadcaster.StartLogging(glog.Infof)
eventBroadcaster.StartRecordingToSink(&amp;typedcorev1.EventSinkImpl{Interface: kubeclientset.CoreV1().Events(&quot;&quot;)})
recorder := eventBroadcaster.NewRecorder(scheme.Scheme, corev1.EventSource{Component: controllerAgentName})

这段代码的目的是什么可以详细在详细解释下吗? 从注释能看出是为了 custom controller可以正常接收event, 但其中的原因可以说下吗?</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8a/28/45cf7f34.jpg" width="30px"><span>142</span> 👍（77） 💬（10）<div>运维人员看起来越来越费力了😢</div>2018-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/c6/b7448158.jpg" width="30px"><span>Tarjintor</span> 👍（68） 💬（8）<div>不知道现在还有人看回复没，我用了不少operator，重度使用rook&#47;ceph
感觉声明式api还是有一些本质不足的地方，主要是
1.通常operator都是用来描述复杂有状态集群的，这个集群本身就已经很复杂了
2.声明式api通过diff的方式来得出集群要做怎么样的状态变迁，这个过程中，常常会有很多状况不能覆盖到，而如果使用者对此没有深刻的认识，就会越用越糊涂
大致来说，如果一个集群本身的状态有n种，那么operator理论上就要覆盖n*(n-1)种变迁的可能性，而这个体力活几乎是不可能完成的，所有很多operator经常性的不支持某些操作，而不是像使用者想象的那样，我改改yaml，apply一下就完事了
更重要的是，由于情况太多太复杂，甚至无法通过文档的方式，告诉使用者，状态1的集群，按某种方式修改了yaml之后，是不能变成使用者期待的状态2的

如果是传统的命令式方式，那么就是所有可能有的功能，都会罗列出来，可能n个状态，只有2n+3个操作是合法的，剩下都是做不到的，这样使用者固然受到了限制，但这种限制也让很多时候的操作变得更加清晰明了,而不是每次改yaml还要思考一下，这么改，operator支持吗？

当然，声明式api的好处也是明显的，如果这个diff是operator覆盖到的，那么就能极大的减轻使用者的负担，apply下就解脱了

而这个集群状态变迁的问题是本质复杂的，必然没有可以消除复杂度的解法，无非就是这个复杂度在operator的实现者那里，还是在运维者那里，在operator的实现者那里，好处就是固化的常用的变迁路径，使用起来很方便，但如果operator的开发者没有实现某个状态的变迁路径，而这个本身是可以做到的，这个时候，就比不上命令式灵活，个人感觉就是取舍了</div>2020-05-21</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（13） 💬（1）<div>Kuberentes的API对象由三部分组成，通常可以归结为： &#47;apis&#47;group&#47;version&#47;resource，例如

    apiVersion: Group&#47;Version
    kind: Resource

APIServer在接收一个请求之后，会按照 &#47;apis&#47;group&#47;version&#47;resource的路径找到对应的Resource类型定义，根据这个类型定义和用户提交的yaml里的字段创建出一个对应的Resource对象

CRD机制：
（1）声明一个CRD，让k8s能够认识和处理所有声明了API是&quot;&#47;apis&#47;group&#47;version&#47;resource&quot;的YAML文件了。包括：组（Group）、版本（Version）、资源类型（Resource）等。
（2）编写go代码，让k8s能够识别yaml对象的描述。包括：Spec、Status等
（3）使用k8s代码生成工具自动生成clientset、informer和lister
（4） 编写一个自定义控制器，来对所关心对象进行相关操作



（1）（2）步骤之后，就可以顺利通过kubectl apply xxx.yaml 来创建出对应的CRD和CR了。 但实际上，k8s的etcd中有了这样的对象，却不会进行实际的一些后续操作，因为我们还没有编写对应CRD的控制器。控制器需要：感知所关心对象过的变化，这是通过一个Informer来完成的。而Informer所需要的代码，正是上述（3）步骤生成。
</div>2020-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a2/60/f3939ab4.jpg" width="30px"><span>哈哼</span> 👍（12） 💬（7）<div>自定义的controler这么手动跑着，挂了咋办？，是不是应该准备好镜像，用Deployment跑起来？</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/21/69c181b8.jpg" width="30px"><span>Rain</span> 👍（7） 💬（2）<div>```此外，在这个过程中，每经过 resyncPeriod 指定的时间，Informer 维护的本地缓存，都会使用最近一次 LIST 返回的结果强制更新一次，从而保证缓存的有效性。在 Kubernetes 中，这个缓存强制更新的操作就叫作：resync。需要注意的是，这个定时 resync 操作，也会触发 Informer 注册的“更新”事件。```
老师，这个地方貌似说的有点问题，看代码逻辑，正常情况下，ListAndWatch只会执行一次，即先执行List把数据拉过来，然后更新一次本地缓存，后续就进入Watch阶段，通过监听事件来实时更新本地缓存，而只有在ListAndWatch过程中，因异常退出时，比如apiserver有问题，没法正常ListAndWatch时，才会周期性的尝试进行ListAndWatch，而这个周期也不是resyncPeriod来控制的，而是一个变动的backoff时间，以防止给apiserver造成压力，而真正的resync，其实说的不是周期性更新缓存，而是根据现有的缓存，周期性的触发UpdateFunc，即同步当前状态和目的状态，确保幂等性，这个周期则是由resyncPeriod控制的。所以“每经过resyncPeriod时间，强制更新缓存”，应该是没这个逻辑的吧，还请老师确认下:)

</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（6） 💬（2）<div>实际操作环境: k8s v1.22.4, go1.17.4
将原始代码clone下来后, 执行 go mod init -&gt; go mod tidy -&gt; go build -o samplecrd-controller .

运行:
.&#47;samplecrd-controller -kubeconfig=$HOME&#47;.kube&#47;config -alsologtostderr=true

crd 的yaml格式需要修改为:
apiVersion: apiextensions.k8s.io&#47;v1
kind: CustomResourceDefinition
metadata:
  name: networks.samplecrd.k8s.io
  annotations:
    &quot;api-approved.kubernetes.io&quot;: &quot;https:&#47;&#47;github.com&#47;kubernetes&#47;kubernetes&#47;pull&#47;78458&quot;
spec:
  group: samplecrd.k8s.io
  names:
    kind: Network
    plural: networks
    singular: network
    shortNames:
    - nw
  scope: Namespaced
  versions:
  - served: true
    storage: true
    name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              cidr:
                type: string
              gateway:
                type: string

之后按照文章中的操作即可</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（4） 💬（1）<div>张老师好，很感谢您的课程分享。另外，我想深入做些自定义组件的开发，您一路已经走过来了，想听下您的建议，顺便推荐书，万分感谢！</div>2019-03-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI2vn8hyjICTCletGs0omz28lhriaZKX2XX9icYzAEon2IEoRnlXqyOia2bEPP0j7T6xexTnr77JJic8w/132" width="30px"><span>Geek_c22199</span> 👍（3） 💬（0）<div>自定义？打扰打扰，等我过半个月再来</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/88/941e488a.jpg" width="30px"><span>hugeo</span> 👍（3） 💬（0）<div>厉害了，原来这才是k8s的精髓</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/27/5d218272.jpg" width="30px"><span>八台上</span> 👍（2） 💬（2）<div>想问一下 工作队列或者delta队列  会持久化吗， 不然controller异常重启的话，队列信息不是丢了吗？</div>2021-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/95/aad51e9b.jpg" width="30px"><span>waterjiao</span> 👍（2） 💬（2）<div>磊哥，如果控制器一段时间不可用，删除的事件到了，这个资源在etcd中被删掉了，控制器重启后，期望状态和实际状态对不齐了，这个时候是不是还要用缓存的数据和实际数据做对比？如果数据较多时，又该怎么办呢？</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/4b/fa64f061.jpg" width="30px"><span>xfan</span> 👍（2） 💬（0）<div>E0107 05:44:18.230692   35973 reflector.go:134] github.com&#47;resouer&#47;k8s-controller-custom-resource&#47;pkg&#47;client&#47;informers&#47;externalversions&#47;factory.go:117: Failed to list *v1.Network: networks.samplecrd.k8s.io is forbidden: User &quot;system:node:node01&quot; cannot list resource &quot;networks&quot; in API group &quot;samplecrd.k8s.io&quot; at the cluster scope
我在node1上面运行打包后的程序报这个错，使用的kubeconfig 不是 ~&#47;.kube&#47;config 而是请问&#47;etc&#47;kubernetes&#47;kubelet.conf ，因为我没有那个config文件，请问报这个错误的原因是什么呢？
</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（2） 💬（0）<div>思考题：一个FIFO可能会support多个controller，所以controller层面的业务逻辑retry不能放在FIFO而是得有独立的retry queue。同时work queue可以用来实现backoff on error等业务逻辑，而这些逻辑不适合放在FIFO中</div>2018-10-21</li><br/><li><img src="" width="30px"><span>Geek_3635b2</span> 👍（1） 💬（0）<div>学完go再来看这两篇</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/69/5a1c6620.jpg" width="30px"><span>cosz3</span> 👍（1） 💬（0）<div>有两个问题：
1. APIServer 触发 event 的时候，是怎么知道给哪个 informer 发送 event 呢？通过文章没有看出 APIServer 加载 informer，也没看出某个 informer 主动去 APIServer 上注册自己。

2. informer ListandWatch 最多可以一次性 ListAndWatch 多少个 pod 呢？ </div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7b/2b/97e4d599.jpg" width="30px"><span>Podman</span> 👍（1） 💬（0）<div>有个小白问题请教下~
所以上一篇文章代码部分最后生成的pkg&#47;client&#47;{informers, listers, clientset}客户端代码
这个“客户端”指的就是本篇的自定义controller
而且这些informers, listers, clientset代码就是用于实现informer、list&#47;watch机制等逻辑的

不知道我这样理解对么</div>2021-04-10</li><br/>
</ul>