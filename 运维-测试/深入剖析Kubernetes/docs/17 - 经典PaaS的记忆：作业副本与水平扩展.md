你好，我是张磊。今天我和你分享的主题是：经典PaaS的记忆之作业副本与水平扩展。

在上一篇文章中，我为你详细介绍了Kubernetes项目中第一个重要的设计思想：控制器模式。

而在今天这篇文章中，我就来为你详细讲解一下，Kubernetes里第一个控制器模式的完整实现：Deployment。

Deployment看似简单，但实际上，它实现了Kubernetes项目中一个非常重要的功能：Pod的“水平扩展/收缩”（horizontal scaling out/in）。这个功能，是从PaaS时代开始，一个平台级项目就必须具备的编排能力。

举个例子，如果你更新了Deployment的Pod模板（比如，修改了容器的镜像），那么Deployment就需要遵循一种叫作“滚动更新”（rolling update）的方式，来升级现有的容器。

而这个能力的实现，依赖的是Kubernetes项目中的一个非常重要的概念（API对象）：ReplicaSet。

ReplicaSet的结构非常简单，我们可以通过这个YAML文件查看一下：

```
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-set
  labels:
    app: nginx
spec:
  replicas: 3
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
        image: nginx:1.7.9
```

从这个YAML文件中，我们可以看到，**一个ReplicaSet对象，其实就是由副本数目的定义和一个Pod模板组成的**。不难发现，它的定义其实是Deployment的一个子集。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/90/aa/83c31ba3.jpg" width="30px"><span>小龙</span> 👍（163） 💬（24）<div>老师真的是厉害，我在极客时间买了17门课了，这个是含金量最高的一门</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/37/791d0f5e.jpg" width="30px"><span>胖宝王</span> 👍（123） 💬（5）<div>金丝雀部署：优先发布一台或少量机器升级，等验证无误后再更新其他机器。优点是用户影响范围小，不足之处是要额外控制如何做自动更新。
蓝绿部署：2组机器，蓝代表当前的V1版本，绿代表已经升级完成的V2版本。通过LB将流量全部导入V2完成升级部署。优点是切换快速，缺点是影响全部用户。
本文学习的滚动更新，我觉得就是一个自动化更新的金丝雀发布。</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/52/6659dc1b.jpg" width="30px"><span>黑米</span> 👍（45） 💬（36）<div>老师真的是厉害，我在极客时间买了24门课了，这个是含金量第二高的一门</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（31） 💬（1）<div>关于Pod的状态一直有一些疑问, 学完这节课就更混了, 囧.   还望老师能解答下.

`kubectl get deployments` 得到的 available 字段表示的是处于Running状态且健康检查通过的Pod, 这里有一个疑问: 健康检查不是针对Pod里面的Container吗? 如果某一个Pod里面包含多个Container, 但是这些Container健康检查有些并没有通过, 那么此时该Pod会出现在 available里面吗? 

Pod通过健康检查是指里面所有的Container都通过吗?</div>2018-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/20/10/5786e0d8.jpg" width="30px"><span>bus801</span> 👍（25） 💬（3）<div>如果我直接edit rs，将image修改成新的版本，是不是也能实现pod中容器镜像的更新？我试了一下，什么反应也没有。既然rs控制pod，为什么这样改不能生效呢？还请指教一下</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/21/5f0bf9a0.jpg" width="30px"><span>阿文</span> 👍（23） 💬（1）<div>注意，在这里，我额外加了一个–record 参数。它的作用，...

这个应该要解释下--record 是只记录当前命令，老师，你下面的命令没有加。history 里面只看到
   kubectl create --filename=nginx-deployment.yaml --record=true</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/69/21b4b5cb.jpg" width="30px"><span>王由华</span> 👍（22） 💬（6）<div>有个问题，scale down时，k8s是对pod里的容器发送kill 信号吗？所以应用需要处理好这个信号？</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/eb/112e7d16.jpg" width="30px"><span>我是一根葱</span> 👍（20） 💬（4）<div>请教个问题，如果水平收缩的过程中，某个pod中的容器有正在运行的业务，而业务如果中断的话可能会导致数据库数据出错，该怎么办？如何保证把pod的业务执行完再收缩？</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/4b/170654bb.jpg" width="30px"><span>千寻</span> 👍（15） 💬（1）<div>在滚动更新的过程中，Service的流量转发会有怎样的变化呢？</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/95/474d5eaf.jpg" width="30px"><span>Tigerfive</span> 👍（10） 💬（1）<div>半夜从火车上醒来，就来看看有没有更新，果然没有让我失望！</div>2018-10-01</li><br/><li><img src="" width="30px"><span>Nokiak8</span> 👍（8） 💬（1）<div>Cronjob 类型也有spec.revisionHistoryLimit么？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/e2/823a04b4.jpg" width="30px"><span>小小笑儿</span> 👍（8） 💬（2）<div>有几个问题想请问一下:
1是在 deployment rollout undo 的时候，是也会创建一个新的rs对象吗？如果是的话那么这个rs的template hash不就重复了？如果不是得话又是如何处理的呢？
2是deployment 关注的应该是自身的api对象和rs的api对象，但是我看deployment controller 的源码中也关注了pod的变更，这是为了处理哪种情况？</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/6b/9c3f3abb.jpg" width="30px"><span>阿鹏</span> 👍（3） 💬（2）<div>老师，我们公司准备试水k8s，我看网上很多文章都在说跨主机容器间通信的解决方案，如果我们的服务分批容器化，需要解决宿主机网络和容器网络的互通，我用flannel或者calico目前都只能做到宿主机能访问容器网络或者容器能访问宿主机网络，不能做到双向通讯，老师能指点一下吗？</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/36/abe6d066.jpg" width="30px"><span>付盼星</span> 👍（1） 💬（1）<div>老师好，如果不修改镜像名称和tag，如何做到强制拉取镜像，触发更新？</div>2018-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（1） 💬（1）<div>滚动升级指定比例的pod处于离线或新建，这个desired 值25%怎么算的呢？分子和分母各是什么？
国庆有时间充电，多来点内容呀！加油！</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/5c/69ca7575.jpg" width="30px"><span>Tylar</span> 👍（0） 💬（2）<div>老师您好，我想问一下运行一段时间以后，在容器中无法通过其他容器的pod名解析出对应的容器ip是什么情况呢</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/08/2aecb51f.jpg" width="30px"><span>混沌渺无极</span> 👍（0） 💬（1）<div>国庆第一天 看到干货！
玩k8s多久后 可以尝试看源码呢？源码入门，大佬会出文章吗？</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/37/791d0f5e.jpg" width="30px"><span>胖宝王</span> 👍（15） 💬（0）<div>金丝雀发布：先发布一台机器或少量机器，做流量验证。如果新版没问题在把剩余机器全部更新。优点是影响范围小，不足的是要自己想办法如何控制自动更新。
蓝绿部署：事先准备好一组机器(绿组)全部更新，然后调整LB将流量全部引到绿组。优点是切换快捷回滚方便。不足的是有问题则影响全部用户。
对于本文学习的 rolling update，我理解的像是自动化更新的金丝雀发布。</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/52/6659dc1b.jpg" width="30px"><span>黑米</span> 👍（12） 💬（0）<div>不用不高兴，你第二没人敢认第一👍</div>2018-12-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM49ONuR097wB6LqR8nn5kWiaQiaPic1y8UznibDOScQergTj5qeL6zQ4bIicYEkqlMiash3CUCAYmSt9tQA/132" width="30px"><span>哈希碰撞</span> 👍（9） 💬（3）<div>一个 ReplicaSet 对象,不难发现是 Deployment 的一个子集？
请问怎么不难发现？ 我觉得很难发现。。。从示例的YAML文件内容上看，看不出任何关连。</div>2019-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/48/b7054856.jpg" width="30px"><span>原来只是梦</span> 👍（9） 💬（4）<div>老师你好！之前有同学提到这个rollout像自动化的金丝雀发布，对于这一点我不太理解。发布的时候会是一个轮换的过程，也就是说用不了多少时间，就会都运行在新的rs，或者都回滚到老的rs(出错)。我的理解要金丝雀的话，需要保持同时存在两个rs一定时间，以确保新版本没问题。那么这个在k8s里是怎么实现呢？</div>2018-12-16</li><br/><li><img src="" width="30px"><span>思维决定未来</span> 👍（7） 💬（5）<div>金丝雀和蓝绿发布实际是在流量入口(Ingress)来控制的，并不是通过其他Controller来控制Deployment，在更新时，直接部署一个新的Deployment，然后通过调整流量比例到不同的Deployment从而实现对应更新，而蓝绿和金丝雀的区别就是新版本的Deployment是否一次性将副本数开到跟原Deployment一样多。</div>2019-09-04</li><br/><li><img src="" width="30px"><span>与君共勉</span> 👍（6） 💬（0）<div>我看完了“kubenetes权威指南”这本书，感觉这本书很像是使用指导，深度不够，还是张老师的课程有些深度。“kubenetes权威指南”是这样讲Deployment和ReplicateSet的区别的：Deployment继承了ReplicateSet的所有功能，让我以为他们是继承关系，认为Deployment是增强版的ReplicateSet。看了老师的文章才知道，Deployment控制的是ReplicateSet，ReplicateSet控制的是pods数量，Deployment是通过ReplicateSet间接控制了pod的数目。</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（4） 💬（0）<div>更正一个错误 revision读音    [英] [rɪˈvɪʒ(ə)n]，修订的意思。读reversion 误认为是re-版本的意思</div>2020-07-17</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（3） 💬（0）<div>控制器模式： 获取对象的期望状态和当前状态，对比这两个状态，如果不一致就做相应的动作来让当前状态和期望状态一致。

Deployment通过控制器模式控制ReplicaSet来实现“水平扩展&#47;收缩”、“滚动更新”，“版本控制”。ReplicaSet通过控制器模式来维持Pod的副本数量。

滚动更新： 你的游戏角色装备了一套一级铭文，现在有一套二级铭文可以替换。一个个替换，一次替换一个铭文，这就是滚动更新。
</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ec/3d/7efdb149.jpg" width="30px"><span>Geek_hfne2s</span> 👍（2） 💬（1）<div>一个 ReplicaSet 对象，其实就是由副本数目的定义和一个 Pod 模板组成的。不难发现，它的定义其实是 Deployment 的一个子集。
怎么看出是一个Deployment的子集？求解释</div>2020-05-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqzHZmo8b9Z9Xb62ib14ejOfTGaFhMxOyXhnxVSdnP84Q4ibnOThMNBk0Xat1adgaZX7gArjPL9Ggicw/132" width="30px"><span>七七要上天</span> 👍（1） 💬（0）<div>deployment和replicatedSet，回滚以及平滑升级。</div>2023-05-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oltLEqTrmHm2aJP99BK6tHu5h7hp4aj08wR5Wt6H31iadFduDAVvjYKmhQ2nvGbLV3lkVdiat2GRasgWXoJeTibUg/132" width="30px"><span>杨</span> 👍（1） 💬（0）<div>金丝雀发布：将一部分机器更新为新版本  然后通过日志等监控手段来查看运行状态，如果正常将剩下的机器更新为新版本，不正常回退。优点影响小，缺点发布麻烦
蓝绿发布：发布两套环境，一套蓝组(老的版本)、一套绿组(新的版本) 发布时将蓝组切换为绿组,有问题立即回退蓝组。优点：发布迅速回退迅速 缺点：需要两套设备
滚动更新发布:类似k8s也是现在最主流的发布方式，先移除一个老版本，然后新增一个新版本，循环更新，将所有的旧版本变为新版本。当然如果新版本有问题，就可以进行回滚，回滚过程和发布过程一样，只是一个逆向过程</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/2f/01b32495.jpg" width="30px"><span>小孩</span> 👍（1） 💬（1）<div>滚动更新会不会存在新旧版本服务返回不一致情况</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e5/d0/c93e55aa.jpg" width="30px"><span>ben</span> 👍（1） 💬（3）<div>问大家个问题哈，假如在做升级的时候，有个pod正在跑一个长的事务，如果这个时候升级把这个pod给杀了，那么这个事务也就断了，有没有什么方法可以控制等pod里面的程序跑完了在滚动更新呢？或者说k8s是怎么处理这种情况呢？谢谢！</div>2020-05-20</li><br/>
</ul>