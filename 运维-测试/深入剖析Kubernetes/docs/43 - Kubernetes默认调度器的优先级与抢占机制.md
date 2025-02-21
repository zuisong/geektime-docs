你好，我是张磊。今天我和你分享的主题是：Kubernetes默认调度器的优先级与抢占机制。

在上一篇文章中，我为你详细讲解了 Kubernetes 默认调度器的主要调度算法的工作原理。在本篇文章中，我再来为你讲解一下 Kubernetes 调度器里的另一个重要机制，即：优先级（Priority ）和抢占（Preemption）机制。

首先需要明确的是，优先级和抢占机制，解决的是 Pod 调度失败时该怎么办的问题。

正常情况下，当一个 Pod 调度失败后，它就会被暂时“搁置”起来，直到 Pod 被更新，或者集群状态发生变化，调度器才会对这个 Pod进行重新调度。

但在有时候，我们希望的是这样一个场景。当一个高优先级的 Pod 调度失败后，该 Pod 并不会被“搁置”，而是会“挤走”某个 Node 上的一些低优先级的 Pod 。这样就可以保证这个高优先级 Pod 的调度成功。这个特性，其实也是一直以来就存在于 Borg 以及 Mesos 等项目里的一个基本功能。

而在 Kubernetes 里，优先级和抢占机制是在1.10版本后才逐步可用的。要使用这个机制，你首先需要在 Kubernetes 里提交一个 PriorityClass 的定义，如下所示：

```
apiVersion: scheduling.k8s.io/v1beta1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for high priority service pods only."
```
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8c/b2/dfdcc8f3.jpg" width="30px"><span>黄巍</span> 👍（24） 💬（4）<div>「调度器会开启一个 Goroutine，异步地删除牺牲者。」这里应该是同步的 :)</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（7） 💬（1）<div>不太理解service与pod scheduling 流程有什么直接关系？</div>2018-12-02</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（96） 💬（3）<div> 调度器的作用就是为Pod寻找一个合适的Node。

调度过程：待调度Pod被提交到apiServer -&gt; 更新到etcd -&gt; 调度器Watch etcd感知到有需要调度的pod（Informer） -&gt; 取出待调度Pod的信息 -&gt;Predicates： 挑选出可以运行该Pod的所有Node  -&gt;  Priority：给所有Node打分 -&gt; 将Pod绑定到得分最高的Node上 -&gt; 将Pod信息更新回Etcd -&gt; node的kubelet感知到etcd中有自己node需要拉起的pod -&gt; 取出该Pod信息，做基本的二次检测（端口，资源等） -&gt; 在node 上拉起该pod 。

Predicates阶段会有很多过滤规则：比如volume相关，node相关，pod相关
Priorities阶段会为Node打分，Pod调度到得分最高的Node上，打分规则比如： 空余资源、实际物理剩余、镜像大小、Pod亲和性等

Kuberentes中可以为Pod设置优先级，高优先级的Pod可以： 1、在调度队列中先出队进行调度 2、调度失败时，触发抢占，调度器为其抢占低优先级Pod的资源。

Kuberentes默认调度器有两个调度队列：
activeQ：凡事在该队列里的Pod，都是下一个调度周期需要调度的
unschedulableQ:  存放调度失败的Pod，当里面的Pod更新后就会重新回到activeQ，进行“重新调度”

默认调度器的抢占过程： 确定要发生抢占 -&gt; 调度器将所有节点信息复制一份，开始模拟抢占 -&gt;  检查副本里的每一个节点，然后从该节点上逐个删除低优先级Pod，直到满足抢占者能运行 -&gt; 找到一个能运行抢占者Pod的node -&gt; 记录下这个Node名字和被删除Pod的列表 -&gt; 模拟抢占结束 -&gt; 开始真正抢占 -&gt; 删除被抢占者的Pod，将抢占者调度到Node上 
</div>2020-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/7a/55618020.jpg" width="30px"><span>马若飞</span> 👍（71） 💬（0）<div>粥变多了，所有的僧可以重新排队领取了</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（13） 💬（1）<div>因为第一种情况下集群资源发生了变化，原先无法调度的pod可能有了可调度的节点或资源，不再需要通过抢占来实现。

第二种情况是放pod调度成功后，跟这个pod有亲和性和反亲和性规则的pod需要重新过滤一次可用节点。</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（9） 💬（0）<div>Question 1:
Add&#47;update new node&#47;pv&#47;pvc&#47;service will cause the change to predicates, which may make pending pods schedulable.

Question 2:
when a bound pod is added, creation of this pod may make pending pods with matching affinity terms schedulable.

when a bound pod is updated, change of labels may make pending pods with matching affinity terms schedulable.

when a bound pod is deleted, MatchInterPodAffinity need to be reconsidered for this node, as well as all nodes in its same failure domain.</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（7） 💬（7）<div>为什么在为某一对 Pod 和 Node 执行 Predicates 算法的时候，如果待检查的 Node 是一个即将被抢占的节点，调度器就会对这个 Node ，将同样的 Predicates 算法运行两遍？

感觉执行第一遍就可以了啊，难道执行第一遍成功了，在执行第二遍的时候还可能会失败吗？感觉第一遍条件比第二遍苛刻啊，如果第一遍 ok 第二遍也会通过的</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（6） 💬（2）<div>你好，我看了scheduler 代码，若抢占成功应该是更新  status.nominatedNodeName 不是 spec.nominatedNodeName 字段</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/a5/abb7bfe3.jpg" width="30px"><span>要没时间了</span> 👍（3） 💬（0）<div>对于抢占调度，更多的是处理“使用了PriorityClass”且“需求资源不足”的Pod的调度失败case。在确定候选的nominatedNode的过程中，一个很重要的步骤就是模拟删除所有低优先级的pod，看剩余的资源是否符合高优先级Pod的需求。

回忆下上一章提到的调度算法也能够清楚，除了资源不足的原因之外，其他调度失败的原因很难通过抢占来进行恢复。</div>2020-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/69/88/528442b0.jpg" width="30px"><span>Dale</span> 👍（3） 💬（0）<div>1、集群有更新，需要将失败的pod重新调度，放到ActiveQ中可以重新触发调度策略
2、在predicate阶段，会对pod的node selector进行判断，寻找合适的node节点，需要通过将pod放到ActiveQ中重新触发predicate调度策略</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（2） 💬（0）<div>增加调度效率吧，新增加资源的时候，一定有机会加速调度pod; 而一旦某个pod调度程度，马上检验和其相关的pod是否可调度</div>2019-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b4/23/0e296758.jpg" width="30px"><span>姜尧</span> 👍（1） 💬（0）<div>pod驱逐是不是也用到了好多这节讲的api？？？</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/11/831cec7d.jpg" width="30px"><span>小寞子。(≥3≤)</span> 👍（1） 💬（0）<div>没有看代码 但是感觉kubernetes 在schedule方面还是有很多可以优化的空间吧 这些predicate 算法， 如果有几万个pod, 几千个node情况下 还能被几个master node 上面的scheduler 运行么？ cache同步都是个头疼吧。</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/aa/9a/92d2df36.jpg" width="30px"><span>tianfeiyu</span> 👍（1） 💬（0）<div>想问一下，没有开启优先级的 pod 没有 status.NominatedNodeName 字段，抢占过程这些 pod 也会被抢占吗？
</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/e2/823a04b4.jpg" width="30px"><span>小小笑儿</span> 👍（1） 💬（0）<div>第一个问题:添加更新node,pv可能让pod变成可调度的状态，就不用走抢占的流程了，service的不太明白。
第二个问题:对anti的同上</div>2018-11-30</li><br/><li><img src="" width="30px"><span>Geek_4df222</span> 👍（0） 💬（0）<div>这些操作之后，原先不能调度的pod的 Predicates 策略可能可以满足了，此时重新调度，Pod 可以被成功调度。</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/77/05/49ea32f0.jpg" width="30px"><span>Unplug</span> 👍（0） 💬（0）<div>typo: “把所调度失败的 Pod 从 unscheduelableQ 移动到 activeQ 里面。请问这是为什么” 中的 unscheduelableQ 拼错了。应该是 unschedulableQ。</div>2023-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/3a/bc801fb2.jpg" width="30px"><span>mqray</span> 👍（0） 💬（0）<div>为了确保所有的Pod都能够及时地被调度到可用的节点上，从而保证集群的高可用性和稳定性。如果不执行这个操作，那么一些本来可以被调度的Pod可能会一直处于未调度状态，从而导致应用程序无法正常运行。</div>2023-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/70/4e7751f3.jpg" width="30px"><span>超级芒果冰</span> 👍（0） 💬（0）<div>“当然，这也就意味着，我们在这一步只需要考虑那些优先级等于或者大于待调度 Pod 的抢占者。毕竟对于其他较低优先级 Pod 来说，待调度 Pod 总是可以通过抢占运行在待考察 Node 上。”
老师这段话不理解，感觉这段话和它上面的描述联系不起来？</div>2022-07-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrqLEic7DVicYY1s9ldH0vGBialDoplVGpicZUJ0Fdaklw27Frv8Ac67eicb5LibhL74SUxAzlick2nfltA/132" width="30px"><span>jiangb</span> 👍（0） 💬（0）<div>就是操作系统啊</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（0） 💬（0）<div>“第一遍， 调度器会假设上述“潜在的抢占者”已经运行在这个节点上，然后执行 Predicates 算法；
第二遍， 调度器会正常执行 Predicates 算法，即：不考虑任何“潜在的抢占者”。”

对这一段的机制，我觉得如果第一遍能执行通过，第二遍不就是必定会执行通过吗？为啥还要多此一举执行第二遍呢？有没有人和我有同样的疑惑？</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/89/34f2cbcc.jpg" width="30px"><span>杨宇</span> 👍（0） 💬（0）<div>“当一个 unschedulableQ 里的 Pod 被更新之后，调度器会自动把这个 Pod 移动到 activeQ 里”——这个移动，是从activeQ的队尾入队吗？还是可能会插入到前面？毕竟入队后还得等待前面的都出队才轮到自己。</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8f/63/a01a90ae.jpg" width="30px"><span>文军</span> 👍（0） 💬（0）<div>如果之前集群内的pod都没有设置优先级，现在有个新的pod设置了优先级却调度失败了，会发生什么，抢占策略还会被执行嘛，没设置过优先级的pod有默认优先级嘛</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/c9/c3eae895.jpg" width="30px"><span>JOKERBAI</span> 👍（0） 💬（0）<div>第一个问题：添加或者更新Node，整个集群的信息就可能发生变化，可能存在满足unscheduledQ中的Pod调度，所以要让它们试一下，不然永远就在黑屋子了。

第二个问题：Pod更新，其对应的affnity都可能更新，所以要重新调度一次</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b5/84/657d96df.jpg" width="30px"><span>zmoon</span> 👍（0） 💬（0）<div>被抢占的直接删除了么</div>2018-12-06</li><br/>
</ul>