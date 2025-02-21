你好，我是张磊。今天我和你分享的主题是：撬动离线业务之Job与CronJob。

在前面的几篇文章中，我和你详细分享了Deployment、StatefulSet，以及DaemonSet这三个编排概念。你有没有发现它们的共同之处呢？

实际上，它们主要编排的对象，都是“在线业务”，即：Long Running Task（长作业）。比如，我在前面举例时常用的Nginx、Tomcat，以及MySQL等等。这些应用一旦运行起来，除非出错或者停止，它的容器进程会一直保持在Running状态。

但是，有一类作业显然不满足这样的条件，这就是“离线业务”，或者叫作Batch Job（计算业务）。这种业务在计算完成后就直接退出了，而此时如果你依然用Deployment来管理这种业务的话，就会发现Pod会在计算结束后退出，然后被Deployment Controller不断地重启；而像“滚动更新”这样的编排功能，更无从谈起了。

所以，早在Borg项目中，Google就已经对作业进行了分类处理，提出了LRS（Long Running Service）和Batch Jobs两种作业形态，对它们进行“分别管理”和“混合调度”。

不过，在2015年Borg论文刚刚发布的时候，Kubernetes项目并不支持对Batch Job的管理。直到v1.4版本之后，社区才逐步设计出了一个用来描述离线业务的API对象，它的名字就是：Job。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/44/68/5d1fcf32.jpg" width="30px"><span>刘孟</span> 👍（118） 💬（5）<div>需要创建的 Pod 数目 = 最终需要的 Pod 数目 - 实际在 Running 状态 Pod 数目 - 已经成功退出的 Pod 数目 = 2 - 0 - 0= 2。而parallelism数量为4，2小于4，所以应该会创建2个。</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（44） 💬（5）<div>说到pod的重新启动，我想再请教一个问题：假设我把deployment的restart policy设置成always，假设某个pod中的容器运行失败，那么是重新创建了一个新的pod，还是仅仅重启了pod里的容器？pod的名称和ip地址会变化吗？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（28） 💬（5）<div>问个不相关的问题：configmap 更新，怎么做到不重启 pod 生效</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/0d/3dc5683a.jpg" width="30px"><span>柯察金</span> 👍（19） 💬（1）<div>job 执行结束，处于 completed 状态之后，还会占用系统资源吗，可以让它执行结束后自动退出吗</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（17） 💬（1）<div>请问job成功结束后一直处于completed状态吗？需要手动清吗？</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/fc/f46062b6.jpg" width="30px"><span>abc</span> 👍（16） 💬（1）<div>请问老师：miss的数目100是默认的吗？哪个参数可以修改呢</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（10） 💬（3）<div>Job的第三种方法中是不是需要有其他process最后去Kill这个Job，否则Job会在Pod退出后不断创建新的Pod？</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/e7/d58e287c.jpg" width="30px"><span>参悟</span> 👍（9） 💬（1）<div>最近实践遇到的问题，盼请赐教，多套分支的开发，测试环境，是按一套k8s集群按命名空间分区，还是按多套集群，实践方案哪种更好，有何优缺点？如果按一套多空间，会有nodeport冲突的问题，比如数据库需要暴露稳定的端口，方便运维。</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（6） 💬（1）<div>并发度为4，意味着可以同时启动不超过4个job。

completion2 - running0 - completed0 = 2

所以会启动2个job</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（4） 💬（1）<div>另外我想请教一下，CronJob是定期产生新的Job，还是定期重启同一个Job任务？</div>2018-10-12</li><br/><li><img src="" width="30px"><span>hochuenw</span> 👍（3） 💬（1）<div>老师请问kubeflow在哪一部分用到了第一种job的使用方法？他们不是自己写了tf-operator吗</div>2018-11-04</li><br/><li><img src="" width="30px"><span>Nokiak8</span> 👍（3） 💬（2）<div>老师，请教一个问题，假如Job中定义的pod运行失败，比如有异常。pod就会接着新生成，这样带来的就是会有大量的pod 产生，如何解决这种问题？</div>2018-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（3） 💬（1）<div>放miss数量达到100时，cronjob是永远不再创建新的job（相当于整个cronjob失效），亦或只是不再运行miss（错过）的那些job？</div>2018-10-12</li><br/><li><img src="" width="30px"><span>georgesuper GoodTOGreater</span> 👍（2） 💬（1）<div>是不是Spark job,hadoop job,k8s job 底层原理都相似？</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/64/54458855.jpg" width="30px"><span>Caesar</span> 👍（2） 💬（1）<div>(1) 若所有容器重启成功，pod应该是running，或者succeeded
(2) 若有容器没有成功，看具体原因,pending,failed...</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/bf/aacc0d22.jpg" width="30px"><span>acmore</span> 👍（1） 💬（1）<div>如果开启了Pod优先级和抢占调度，Job起的Pod被抢占时，可能会出现Job的succeeded 或者failed的值为1，但是我们应该期望Job的pod被抢占时不应该影响Job的状态。有什么解决办法吗？</div>2018-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/64/54458855.jpg" width="30px"><span>Caesar</span> 👍（1） 💬（3）<div>另外一个问题，如果restartpolicy=on-failure的话，只重启pod中的容器
（1）如果pod中的所有容器重启成功，pod是什么状态？
（2）pod中有容器重启不成功，pod是什么状态？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2e/72/145c10db.jpg" width="30px"><span>每日都想上班</span> 👍（0） 💬（2）<div>cronjob可以每秒执行吗</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（0） 💬（1）<div>请问这里的label必须成对出现吗？
apiVersion: batch&#47;v1
kind: Job
metadata:
  name: process-item-$ITEM
  labels:
    jobgroup: jobexample
spec:
  template:
    metadata:
      name: jobexample
      labels:
        jobgroup: jobexample</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（1）<div>如果想模仿传统调度系统，比如执行1000个Job，是不是可以为Job指定资源需求，然后把并行度和完成度都设为1000，这样k8s调度时会不会调度尽可能多的Pod，直到集群资源耗尽（但此时可能只能运行300个Pod）。然后若有Pod退出，k8s自动再补上新的Pod，直到满足完成数。不知道是不是这样？如果是就能满足一个基本调度系统的需求了。</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/64/54458855.jpg" width="30px"><span>Caesar</span> 👍（0） 💬（1）<div>还有一个问题，设置restartpolicy=on-fauilure 时，如果只重启pod中的容器并且重启成功，那么pod的状态是什么呢？</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/d9/829ac53b.jpg" width="30px"><span>fangxuan</span> 👍（10） 💬（0）<div>从公式可以看出，启动的job的最大值由completion决定</div>2018-11-23</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（6） 💬（0）<div>K8S支持编排长期运行作业和执行完即退出的作业：

（1）支持Long Running Job（长期运行的作业）： Deployment 、StatefulSet、DaemonSet

（2）这次好Batch Job（执行完即退出的作业）：Job、CronJob

CronJob与Job关系，正如同Deployment与ReplicaSet的关系一样。CronJob是一个专门用来管理Job对象的控制器。只不过，它创建和删除Job的依据，是schedule字段定义的


</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（1） 💬（0）<div>第二十二课:撬动离线业务：Job和CronJob
K8s的Task分为Long Run Task：Deployment、StatefulSet、DaemonSet和一次性执行任务Batch Job

离线任务Job的restartPolicy只允许Never或OnFailure，而在Deployment里，restartPolicy只允许被设置为Always。

 Job 对象的 spec.backoffLimit 字段表示失败后重启次数

spec.activeDeadlineSeconds 字段可以设置最长运行时间

spec.parallelism，它定义的是一个 Job 在任意时间最多可以启动多少个 Pod 同时运行

spec.completions，它定义的是 Job 至少要完成的 Pod 数目，即 Job 的最小完成数

Job Controller 控制的对象，直接就是 Pod。

CronJob和Job的关系就像Deployment和ReplicaSet的关系，CronJob是专门用来管理Job对象的控制器，它通过schedule这个字段创建和删除job。

可以通过 spec.concurrencyPolicy 字段来定义具体的处理策略。比如：
concurrencyPolicy=Allow，这也是默认情况，这意味着这些 Job 可以同时存在；
concurrencyPolicy=Forbid，这意味着不会创建新的 Pod，该创建周期被跳过；
concurrencyPolicy=Replace，这意味着新产生的 Job 会替换旧的、没有执行完的 Job。

</div>2021-10-11</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIC5FK1ibcFwyTQ5TugfhJicSsZ3x5GfibRrUNTxpb8IY88wNREl4GlbJqUUibCHAhZp9wqic2eia2Dpgsw/132" width="30px"><span>江</span> 👍（1） 💬（0）<div>请教一下，如果多个job 间存在拓扑关系，比如有顺序依赖，这个是不是得用外部工具?</div>2021-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/55/fe/ab541300.jpg" width="30px"><span>小猪</span> 👍（1） 💬（3）<div>我想把job在每一个物理机上定期执行，来删除指定目录下的日志文件，就像DaemonSet那样部署到每一个物理机。这种需求怎么使用job处理？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/56/37a4cea7.jpg" width="30px"><span>单朋荣</span> 👍（1） 💬（0）<div>大神，我一直很喜欢你的课程。现在更新的也比较多了~能不能在以后的章节里讲讲自动伸缩控制HPA、VPA、CA的知识点，谢谢了。</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/83/ae/c082bb25.jpg" width="30px"><span>大星星</span> 👍（1） 💬（0）<div>你好，磊哥，我想问下job运行后，会有字段controller-uid。这个东西和node节点有关系么，还是它只是用来标识job。job应该是调度器随便调度一个节点，执行job吧，谢谢。</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（0）<div>The Job &quot;pi&quot; is invalid: spec.completions: Invalid value: 4: field is immutable. 好像 completions 不让填写。</div>2023-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/96/11/ec3cdd5d.jpg" width="30px"><span>ipso</span> 👍（0） 💬（0）<div>v1-27版本的k8s: cronjson.yaml

apiVersion: batch&#47;v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: &quot;*&#47;1 * * * *&quot;
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - &#47;bin&#47;sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure

create失败，可以去k8s文档找找答案</div>2023-09-05</li><br/>
</ul>