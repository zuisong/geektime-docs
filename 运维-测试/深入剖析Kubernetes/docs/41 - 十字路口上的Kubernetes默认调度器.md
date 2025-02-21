你好，我是张磊。今天我和你分享的主题是：十字路口上的Kubernetes默认调度器。

在上一篇文章中，我主要为你介绍了Kubernetes里关于资源模型和资源管理的设计方法。而在今天这篇文章中，我就来为你介绍一下Kubernetes的默认调度器（default scheduler）。

**在Kubernetes项目中，默认调度器的主要职责，就是为一个新创建出来的Pod，寻找一个最合适的节点（Node）。**

而这里“最合适”的含义，包括两层：

1. 从集群所有的节点中，根据调度算法挑选出所有可以运行该Pod的节点；
2. 从第一步的结果中，再根据调度算法挑选一个最符合条件的节点作为最终结果。

所以在具体的调度流程中，默认调度器会首先调用一组叫作Predicate的调度算法，来检查每个Node。然后，再调用一组叫作Priority的调度算法，来给上一步得到的结果里的每个Node打分。最终的调度结果，就是得分最高的那个Node。

而我在前面的文章中曾经介绍过，调度器对一个Pod调度成功，实际上就是将它的spec.nodeName字段填上调度结果的节点名字。

> 备注：这里你可以再回顾下第14篇文章[《深入解析Pod对象（一）：基本概念》](https://time.geekbang.org/column/article/40366)中的相关内容。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/30/2f8b78e9.jpg" width="30px"><span>CYH</span> 👍（86） 💬（3）<div>问题回答：messos二级调度是资源调度和业务调度分开；优点：插件化调度框架（用户可以自定义自己调度器然后注册到messos资源调度框架即可），灵活可扩展性高.缺点：资源和业务调度分开无法获取资源使用情况，进而无法做更细粒度的调度.k8s调度是统一调度也就是业务和资源调度进行统一调度，可以进行更细粒度的调度；缺点其调度器扩展性差。以上是本人拙见，请老师指正。</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/f1/48f16eaa.jpg" width="30px"><span>Vip He</span> 👍（26） 💬（3）<div>老师您好，这个pod调度过程是并行的吗还是一个一个pod调度？</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/fe/beab006d.jpg" width="30px"><span>Jasper</span> 👍（14） 💬（7）<div>2021年了，来还18年没读完的债。在老孟的指导下学习，再回首张磊老师的文章，感慨万千</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/1d/0995be72.jpg" width="30px"><span>dgonly</span> 👍（9） 💬（2）<div>调度器对APIServer的更新失败，Bind过程失败，老师说等schedule cache同步后就恢复正常，这个怎么理解？
我理解是informer path继续watch，发现pod没有被bind到node就继续执行一遍调度流程吗？如果某种原因更新APIServer一直失败，会不会就一直执行重新调度的操作，有没有一种类似重试超过一定比如就丢弃的机制。谢谢！</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（4） 💬（0）<div>第四十一课:十字路口上的Kubernetes默认调度器
K8s项目中默认调度器的主要职责是就是为了新创建出来的Pod寻找一个最合适的Node。

调度器首先会调用一组叫Predicate的调度算法，来检每一个Node。然后再调用一组叫作Priority的调度算法来给上一步得到的结果里的每一个Node打分。最终的调度结果就是得分最高的那个Node。

Kubernetes 的调度器的核心，实际上就是两个相互独立的控制循环。第一个是Informer Path，主要是启动一系列Informer用来监听(Watch)Etcd中的Pod,Node, Service等与调度相关的API对象的变化。此外，Kubernetes 的默认调度器还要负责对调度器缓存（即：scheduler cache）进行更新。事实上，Kubernetes 调度部分进行性能优化的一个最根本原则，就是尽最大可能将集群信息 Cache 化，以便从根本上提高 Predicate 和 Priority 调度算法的执行效率。第二个控制循环是Scheduling Path，主要逻辑是不断从调度队列里调出Pod，然后用Predicates算法进行过滤，得到一组可以运行这个Pod的宿主机列表，然后再用Priority打分，得分高的称为Pod结果。
</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/57/3032e1a7.jpg" width="30px"><span>loda</span> 👍（4） 💬（5）<div>想请教个问题，kubernetes如何保证用户能提前知道这次调度能否成功？
场景：很多公司都希望提前就发现资源池余量是否充足，从而决定是要加机器还是可以继续扩容
拙见：
1.scheduler的缓存其实是一个非常重要的数据，可以提供当前时刻调度能否成功的视图，但是直接暴露出来不太符合kubernetes以apiserver为依据的原则
2.提供余量检查接口，实时查询apiserver中所有pod和node，根据扩容参数算出剩余资源量。不过规模大后，对集群压力太大
3.定时采集上述指标，缺点是实时性太差
4.监听pod crud，自己独立维护一个和scheduler一样的缓存或持久话数据，每次基于这个数据判断剩余量。缺点是维护成本较高，容易出现数据不一致

想问下，有没有更合适的方式？
</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/0b/81ae214b.jpg" width="30px"><span>凌</span> 👍（3） 💬（1）<div>如果能结合源码将解决就更好了，不知道相关代码在哪啊</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/8b/3cc461b3.jpg" width="30px"><span>宋晓明</span> 👍（3） 💬（0）<div>老师 刚才遇到一个问题 我初始化的时候 分配的ip范围是10.64.200.0&#47;22 然后两个master 3个node  kubernetes自己分配master分别是200.0&#47;24 201.0&#47;24  然后其他两个node是202.0&#47;24 203.0&#47;24 其实这些范围已经用满了 在加第三个node 在master看也成功了 但创建多个pod的时候 第三个node上的pod是失败的,后来发现第三个node上kube-bridge网桥上没有IP地址，需求是：因为master上不会有自己创建的pod的，所以master上地址段有点浪费，我如何把master上空闲的地址段用到新增node上，还是不用管，还是怎么样？</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8f/e6/932e8a90.jpg" width="30px"><span>Jake</span> 👍（1） 💬（0）<div>2023年了，来还18年没读完的债。在老孟的指导下学习，再回首张磊老师的文章，感慨万千
</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/11/831cec7d.jpg" width="30px"><span>小寞子。(≥3≤)</span> 👍（1） 💬（0）<div>2021年，找到代码了 https:&#47;&#47;github.com&#47;kubernetes-sigs&#47;scheduler-plugins&#47;blob&#47;master&#47;pkg&#47;trimaran&#47;handler.go 不知道这是不是正确的地方。</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/aa/f53a6800.jpg" width="30px"><span>Dong</span> 👍（1） 💬（0）<div>嘿嘿</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/63/6513b925.jpg" width="30px"><span>杜少星</span> 👍（0） 💬（0）<div>2023.10.15再次路过..</div>2023-10-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/uQoCBsia00Dr1g05SCZ69esjDwJWP4QGbckxNZAO44xg4Hu2YjDROoITtvcLr23ae9SrE5tVR95U8ricVMicdnUIw/132" width="30px"><span>Geek_439a6d</span> 👍（0） 💬（1）<div>请教下，为什么 kubernetes调度器 进行性能优化的最根本原则，是将集群信息 Cache 化？是因为如果不将集群信息 Cache 化，调度器性能瓶颈在从 APIServer 拉取调度过程中需要的各种信息吗？</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/3f/59/3b9da34b.jpg" width="30px"><span>初心?固执?</span> 👍（0） 💬（0）<div>可以请教个问题吗？
我不太想动数据库一级，只对其它的应用使用k8s集群部署，
然后我想k8s的节点和这些数据库节点共存(有些数据库服务器只占用了很少一部分资源)，

请问这种情况下资源调度器是怎么知道这个节点上剩余可用的cpu和内存的? </div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/76/0f/c7c8021d.jpg" width="30px"><span>豆豆</span> 👍（0） 💬（2）<div>关于默认调度器在scheduling path阶段无锁化描述，难道在predicate阶段，从queue中取pod时，不需要加锁吗？</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（0） 💬（0）<div>Scheduler是多实例的，可调度是串行的，是通过加锁吗？</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（0） 💬（1）<div>记录下，调度的过程 两个独立的循环，一个是通过informer缓存pod node信息，一个是 给需要的pod过滤符合条件的节点，然后计算得分排序。</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/89/b7fae170.jpg" width="30px"><span>那迦树</span> 👍（0） 💬（1）<div>不知道k8s的调度器是否可以自定义，我们项目的需求在目前已有的调度器还不能完全满足</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/19/18/33b7e63b.jpg" width="30px"><span>wypsmall</span> 👍（0） 💬（1）<div>请教一个问题，调度策略中有没有对网络io限制呢？也就是说不希望高网络io的pod被调度到同一个宿主机。</div>2019-02-13</li><br/>
</ul>