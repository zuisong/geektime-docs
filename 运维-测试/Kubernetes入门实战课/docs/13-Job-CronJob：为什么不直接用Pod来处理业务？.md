你好，我是Chrono。

在上次的课里我们学习了Kubernetes的核心对象Pod，用来编排一个或多个容器，让这些容器共享网络、存储等资源，总是共同调度，从而紧密协同工作。

因为Pod比容器更能够表示实际的应用，所以Kubernetes不会在容器层面来编排业务，而是把Pod作为在集群里调度运维的最小单位。

前面我们也看到了一张Kubernetes的资源对象关系图，以Pod为中心，延伸出了很多表示各种业务的其他资源对象。那么你会不会有这样的疑问：Pod的功能已经足够完善了，为什么还要定义这些额外的对象呢？为什么不直接在Pod里添加功能，来处理业务需求呢？

这个问题体现了Google对大规模计算集群管理的深度思考，今天我就说说Kubernetes基于Pod的设计理念，先从最简单的两种对象——Job和CronJob讲起。

## 为什么不直接使用Pod

现在你应该知道，Kubernetes使用的是RESTful API，把集群中的各种业务都抽象为HTTP资源对象，那么在这个层次之上，我们就可以使用面向对象的方式来考虑问题。

如果你有一些编程方面的经验，就会知道面向对象编程（OOP），它把一切都视为高内聚的对象，强调对象之间互相通信来完成任务。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（29） 💬（2）<div>回答一下今天的作业：
1. 你是怎么理解 Kubernetes 组合对象的方式的？它带来了什么好处？
Kubernetes中组合对象，类似于面向对象编程中的继承，即不破坏父对象的功能，又扩展了自己领域场景中的功能，在API层面也简单了，只需要处理自己扩展的功能即可，比在一个对象上做加法进入逻辑判断要优雅很多。

2. Job 和 CronJob 的具体应用场景有哪些？能够解决什么样的问题？
Job与CronJob分别对应一次性调用的任务与周期性定时任务；前者任务只运行一次，比如用在手工触发的场景如数据库备份、恢复与还原，数据同步，安全检查，巡检等；后者用于定时任务，非手工触发，由CronJobController每隔10s遍历需要执行的CronJob，同样也使用在如数据库备份、恢复与还原、数据同步、安全检查、定期巡检以及所有周期性的运维任务。
Job与CronJob解决了任务的管理，如执行超时、失败尝试、执行数量与并行数量、任务结果记录等等，方便对任务执行的监控与管理；另外，Pod解决了批处理任务关联打包统一调度，容器解决了任务运行时环境。</div>2022-07-20</li><br/><li><img src="" width="30px"><span>Geek_b9dad2</span> 👍（18） 💬（1）<div>课外小贴士里第4条和第6条感觉是有冲突的，这个怎么理解呢？</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（15） 💬（1）<div>不得不服这个设计，为后续扩展带来了无限的可能，而且又不影响现有的pod体系功能！原来面向对象的思想还能在YAML中这么用。</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b5/46/2ac4b984.jpg" width="30px"><span>三溪</span> 👍（7） 💬（5）<div>我想补充一下关于job配置的一个细节，大家可能复制黏贴罗老师的配置所以不会发现这个问题。
job.spec.containers.template.spec.containers.image是不能指定镜像版本号的，只能指定镜像：完整的镜像:版本号只能由pod定义，否则会从互联网拉取镜像，如果能联网当然没事，离线环境会直接报错无法拉取镜像，虽然你本地确实存在该版本的镜像且imagePullPolicy设置为Never或IfNotPresent。
比如我是离线环境，job里image配置为：- image: busybox:1.35.0，那么就会报错无法拉取镜像。</div>2022-07-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJw1XoOvKHBmyvGpxyoWibq7FYj6blWe0cUKJCqUFPHF1jmkxdBe6icTVC0nTYYPIP2ggx3UodKsLibQ/132" width="30px"><span>Geek_7ba156</span> 👍（5） 💬（1）<div>666，超爱这种讲课方式。老师你一定要多出课啊，笔芯~</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（5） 💬（2）<div>终于知道老师昵称的由来了</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（4） 💬（1）<div>原来一直奇怪为什么有那么多spec、template不停的嵌套？今天终于明白了：不同层级自己描述自己的，相互不影响，不合陌生人说话</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（4） 💬（3）<div>Command 用双引号里写命令，不能有空格。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（2） 💬（2）<div>最近在把业务服务迁移到 Kubernetes 上部署，其中就有一个定时服务，包含 30 个定时 job。我想着直接搬到 Kubernetes 的 CronJob 上来，这样开发团队就少维护一个第三方的开源框架了（用于定时任务调度）。

但我发现一个问题，导致迁移不了，就是触发频率：kubernetes cronjob 只支持到分钟，不能到秒级调度，即最高是每分钟运行一次任务；但他们的定时任务，有些是每 10 秒运行一次，15 秒一次，或 30 秒一次。

这种分钟内的调度，搞不定，感觉非常遗憾。

我在想，标准的 cron 只支持到分钟级别，那么分钟级别以内的定时调度呢？可能就是常驻进程了。</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/7e/735968e2.jpg" width="30px"><span>西门吹牛</span> 👍（2） 💬（1）<div>组合的方式能少写很多代码，Java 很多中间件都这么搞，组合优于继承，基于接口而非实现编程，自由组合</div>2022-07-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（2） 💬（4）<div>思考题：
1. 大的组件有小的组件拼接而成，这样做的其中一个好处就是低耦合，每个组件都是独立的个体，去操作一个组件时不需要理会其他组件的具体内部细节，直接拼接在一起即可。这么做也非常易于维护，比如 Job 中想要更换 Pod 也不需要更改 Job 本身的一些属性

2. Job 主要用在一些 one-off 的场景，就是需要去处理一些临时的一次性的情况，比如 service 的 setup，文件的构建等等。而 Cronjob 主要用途是去完成一些需要定期更新的任务，比如 一些 daily 的 pipeline，定时的检查，检验系统安全等等


有个问题请教老师，在 sleep-job 的那个例子中，不太理解为什么有时候在 Job 完成后，其中的一个 Pod 会被 Terminate 掉，然后最后只剩 3 个 Pod？用课程中的 YAML 文件试了几次，这种情况有时会发生有时不会，不知道是不是跟 YAML 中 Job 设置的字段有关？

:~&#47;k8s-testing$ kubectl get pod
NAME              READY   STATUS        RESTARTS   AGE
echo-job-qqq9k    0&#47;1     Completed     0          7m23s
ngx               1&#47;1     Running       0          11d
sleep-job-9ktxs   0&#47;1     Completed     0          17s
sleep-job-sndgm   0&#47;1     Completed     0          17s
sleep-job-tpbw7   1&#47;1     Terminating   0          9s
sleep-job-v8x8s   0&#47;1     Completed     0          12s</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/06/f0/be51ab1d.jpg" width="30px"><span>蓝色天空</span> 👍（1） 💬（1）<div>只启动2个job问题是超时了
修改activeDeadlineSeconds 设置即可</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/3d/b290414d.jpg" width="30px"><span>岁月长</span> 👍（1） 💬（2）<div>运行sleed-job 的时候发现无法达到预期的 4个，有时候是2，有时候是3；修改了 backoffLimit :10 之后才达到预期。
想问下老师，为什么运行会出现这种情况呢？运行也没有超过设置的超时的时间</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/55/aa/e05a5778.jpg" width="30px"><span>武安君</span> 👍（1） 💬（1）<div>层层套娃！小接口大组合，既能解耦，又能灵活组合在不破坏细粒度逻辑下实现更多的功能！</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，有几个小问题：

1. 我用的是 zsh 如果 使用 kubectl create job echo-job --image=busybox $out
   会报这个错误：error: Invalid dry-run value (client -o yaml). Must be &quot;none&quot;, &quot;server&quot;, or &quot;client&quot;. 
   必须要这样使用才行：kubectl create job echo-job --image=busybox --dry-run=client -o yaml ，这是什么原因呢？

2. 文中说：“不直接和 apiserver 打交道”。怎么听你的语音是apiversion呢？

3. 我们在job.yml文化中定义的Pod的name是echo-job，然后为什么还要加一个随机字符串呢？ 这里的名字是我们自定义的吧，和job自动管理好像关系不大吧？</div>2022-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（1） 💬（1）<div>1. 不太理解。
2. cronjob很好理解，定时任务，备份数据库，跑批啥的，就常用。job是一次性任务，一次性数据拷贝。</div>2022-07-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（1） 💬（1）<div>cronjob适合增量数据同步，job是一次性的，适合一次性启动停止的任务。
想到一个问题，cronjob里面的pod任务自己又起了定时任务，正好两个任务冲突了咋办（套娃警告）？</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/ce/2978a69a.jpg" width="30px"><span>油菜花</span> 👍（1） 💬（1）<div>老师你好，请问问一下定时任务触发完成之后会有一个status为completed状态的pod，这个不用自动删除吗？不删除会有什么影响呢？</div>2022-07-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2xoGmvlQ9qfSibVpPJyyaEriavuWzXnuECrJITmGGHnGVuTibUuBho43Uib3Y5qgORHeSTxnOOSicxs0FV3HGvTpF0A/132" width="30px"><span>psoracle</span> 👍（1） 💬（1）<div>请问下云原生生态体系中有没有关于Job与CronJob管理的项目可以推荐下，能够对任务有一个可视化的统一管理平台？</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（1） 💬（1）<div>对于cronjob有些疑惑，在实际业务中，定时任务一般按照定时规则执行相应的业务逻辑；如果把我们传统的定时任务业务服务打成镜像，然后在k8s创建一个cronjob对象，这个cronjob对象只会根据schedule定期创建容器，至于容器内部执行的定时逻辑好像和cronjob并没有直接的关系。换句话说，cronjob只能定期帮你启动服务，启动后，服务内部的事情我不管</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（3）<div>请教老师两个问题：
Q1：echo-job的YAML文件中有两个同样的name。
一个是： metadata:   name: echo-job
另外一个是：spec:&#47;template:&#47;spec:&#47;containers: name:echo-job
这两个name有关系吗？

Q2：CronJob例子，get pod为什么是3个？
文章中get pod的输出结果是3个pod，我的虚拟机中也是输出3个，
为什么是3个？cronjob.yml中的内容看不出来哪一项是和POD的数量有关</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（1）<div>1. 组合优于继承， 解耦；
2. 应用场景举例：Job -》历史全量数据导入；CronJob -》每天的增量数据导入。</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/d8/708a0932.jpg" width="30px"><span>李一</span> 👍（1） 💬（1）<div>老师您好，请教个问题，像k8s的cronJob在实际项目中，会替代一些现有项目的定时任务库吗？比如spring job或者quartz</div>2022-07-20</li><br/><li><img src="" width="30px"><span>Geek_686ca8</span> 👍（0） 💬（1）<div>一切皆对象，感觉这是kubenetes的高妙之处。</div>2024-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/12/35/4ca3cc7d.jpg" width="30px"><span>lip</span> 👍（0） 💬（1）<div>Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  52s               default-scheduler  Successfully assigned default&#47;ngx-pod to minikube
  Warning  Failed     13s               kubelet            Failed to pull image &quot;nginx:alpine&quot;: rpc error: code = Unknown desc = error pulling image configuration: Get &quot;https:&#47;&#47;production.cloudflare.docker.com&#47;registry-v2&#47;docker&#47;registry&#47;v2&#47;blobs&#47;sha256&#47;54&#47;5461b18aaccf366faf9fba071a5f1ac333cd13435366b32c5e9b8ec903fa18a1&#47;data?verify=1719390002-zHNUIUT1m7L4d7nOShcKGd3odog%3D&quot;: dial tcp 199.59.148.6:443: i&#47;o timeout
  Warning  Failed     13s               kubelet            Error: ErrImagePull
  Normal   BackOff    12s               kubelet            Back-off pulling image &quot;nginx:alpine&quot;
  Warning  Failed     12s               kubelet            Error: ImagePullBackOff
  Normal   Pulling    1s (x2 over 51s)  kubelet            Pulling image &quot;nginx:alpine&quot;

老师，执行 kubectl apply -f ngx-pod.yml 命令总显示 i&#47;o timeout ，是什么原因</div>2024-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>比如说我有个发邮件的单次任务 任务代码用job去控制调用发送，那我要怎么给对应pod中的程序发送参数呢？又怎么通过另一个pod中的程序去调用这个邮件任务的job运行呢？pod能否像函数一样被自由调用呢？</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>突发奇想  既然都是组合 那cronjob是否可以直接用pod组合而不用job 测试了一下 发现不行 报错 missing required field &quot;jobTemplate&quot; 看来各种对象组合 还是有一定规律的 不是想怎么组合就怎么组合啊</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>亲自上级试了试 cronjob创建完后用 kubectl get job还真有新的job创建 再一次证明 cronjob由job组成 job由pod做成 就是组合套路嘛</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/38/4c9cfdf4.jpg" width="30px"><span>谢小路</span> 👍（0） 💬（1）<div>朋友们，我这边没有复杂集群使用经验，就是说 job 和 cronjob 这两对象存在感是不是很低啊。业务的定时任务，不是都集成在服务里吗？也是部署成一个服务，多实例的话，用分布式锁解决多实例运行冲突的问题。</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9b/64/dadf0ca5.jpg" width="30px"><span>至尊猴</span> 👍（0） 💬（2）<div>hi Chrono 老师，
我在自己环境做sleep-job这个场景的测试时，有job不能complete，请问这种情况怎么定位分析呢？


[wangfeng@fedora kube]$ kubectl apply -f sleep-job.yml 
job.batch&#47;sleep-job created
[wangfeng@fedora kube]$ kubectl get pod -w
NAME              READY   STATUS      RESTARTS   AGE
echo-job-8vvfz    0&#47;1     Completed   0          13h
ngx               1&#47;1     Running     0          19h
sleep-job-fsnk4   0&#47;1     Completed   0          7s
sleep-job-l656p   1&#47;1     Running     0          7s
sleep-job-zfl66   1&#47;1     Running     0          4s
sleep-job-zfl66   0&#47;1     Completed   0          7s
sleep-job-hqkwk   0&#47;1     Pending     0          0s
sleep-job-hqkwk   0&#47;1     Pending     0          0s
sleep-job-zfl66   0&#47;1     Completed   0          7s
sleep-job-hqkwk   0&#47;1     ContainerCreating   0          0s
sleep-job-l656p   0&#47;1     Completed           0          11s
sleep-job-l656p   0&#47;1     Completed           0          11s
sleep-job-hqkwk   1&#47;1     Running             0          2s
sleep-job-hqkwk   1&#47;1     Terminating         0          5s
sleep-job-hqkwk   1&#47;1     Terminating         0          5s
sleep-job-hqkwk   0&#47;1     Terminating         0          11s
sleep-job-hqkwk   0&#47;1     Terminating         0          11s
sleep-job-hqkwk   0&#47;1     Terminating         0          11s

--------------
[wangfeng@fedora ~]$ kubectl get job
NAME        COMPLETIONS   DURATION   AGE
echo-job    1&#47;1           2s         13h
sleep-job   3&#47;4           6m31s      6m31s
[wangfeng@fedora ~]$ kubectl get pod
NAME              READY   STATUS      RESTARTS   AGE
echo-job-8vvfz    0&#47;1     Completed   0          13h
ngx               1&#47;1     Running     0          20h
sleep-job-fsnk4   0&#47;1     Completed   0          6m41s
sleep-job-l656p   0&#47;1     Completed   0          6m41s
sleep-job-zfl66   0&#47;1     Completed   0          6m38s
</div>2023-04-04</li><br/>
</ul>