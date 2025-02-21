你好，我是张磊。今天我和你分享的主题是：深入解析Pod对象之基本概念。

在上一篇文章中，我详细介绍了Pod这个Kubernetes项目中最重要的概念。而在今天这篇文章中，我会和你分享Pod对象的更多细节。

现在，你已经非常清楚：Pod，而不是容器，才是Kubernetes项目中的最小编排单位。将这个设计落实到API对象上，容器（Container）就成了Pod属性里的一个普通的字段。那么，一个很自然的问题就是：到底哪些属性属于Pod对象，而又有哪些属性属于Container呢？

要彻底理解这个问题，你就一定要牢记我在上一篇文章中提到的一个结论：Pod扮演的是传统部署环境里“虚拟机”的角色。这样的设计，是为了使用户从传统环境（虚拟机环境）向Kubernetes（容器环境）的迁移，更加平滑。

而如果你能把Pod看成传统环境里的“机器”、把容器看作是运行在这个“机器”里的“用户程序”，那么很多关于Pod对象的设计就非常容易理解了。

比如，**凡是调度、网络、存储，以及安全相关的属性，基本上是Pod 级别的。**

这些属性的共同特征是，它们描述的是“机器”这个整体，而不是里面运行的“程序”。比如，配置这个“机器”的网卡（即：Pod的网络定义），配置这个“机器”的磁盘（即：Pod的存储定义），配置这个“机器”的防火墙（即：Pod的安全定义）。更不用说，这台“机器”运行在哪个服务器之上（即：Pod的调度）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（319） 💬（2）<div>对于 Pod 状态是 Ready，实际上不能提供服务的情况能想到几个例子：
1. 程序本身有 bug，本来应该返回 200，但因为代码问题，返回的是500；
2. 程序因为内存问题，已经僵死，但进程还在，但无响应；
3. Dockerfile 写的不规范，应用程序不是主进程，那么主进程出了什么问题都无法发现；
4. 程序出现死循环。
</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/55/73/0b6351b8.jpg" width="30px"><span>细雨</span> 👍（35） 💬（2）<div>问一下老师，infra 网络的镜像为什么取名字叫 pause 呀，难道它一直处于“暂停状态”吗？</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（21） 💬（1）<div>你好，我进入shell容器，然后执行ps ax，跟例子的结果不一样。例子代码也一样，添加了shareProcessNamespace: true了，为什么不行呢，请问可能出现的原因在哪里
&#47; # ps
PID USER TIME COMMAND
1 root 0:00 sh
10 root 0:00 ps

请问怎么开启sharepid功能呢？</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/d8/abb7bfe3.jpg" width="30px"><span>两两</span> 👍（15） 💬（1）<div>pod runing好理解，但k8s怎么知道容器runing呢，通过什么标准判断？应用死循环，k8s怎么能感知？</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（14） 💬（9）<div>以前我对容器的认识还不深，竟然用tail -f Catalina.out作为前台进程，这样即使tomcat进程挂掉，容器还是正在运行。应用不可用tomcat进程还在经常会遇到，比如内存溢出，或者应用依赖的数据库等外部系统动荡导致应用不正常。怎么在应用的角度来决定容器是否应该退出？应用提供一个健康检查url，跑前台shell定期检查该url，状态不对则shell退出，从而容器退出。</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/52/a51cbdef.jpg" width="30px"><span>杨孔来</span> 👍（12） 💬（3）<div>老师，如果pod中的image更新了（比如 通过jenkins发布了新版本），我想通过重启pod,获取最新的image，有什么命令，可以优雅的重启pod，而不影响当前pod提供的业务吗</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/a6/723854ee.jpg" width="30px"><span>姜戈</span> 👍（10） 💬（2）<div>通过node selector将任务调度到了woker1   成功运行之后 再修改worker1的label,  任务会重新调度吗？</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/8f/759b7761.jpg" width="30px"><span>ethfoo</span> 👍（9） 💬（1）<div>如果pod加了健康检查，是不是就不关心应用进程是不是容器的初始化进程呢？因为应用进程挂了，虽然容器不会自动退出，但是kubelet会主动去kill掉这个容器</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ef/dd/599d77c0.jpg" width="30px"><span>hexinzhe</span> 👍（8） 💬（3）<div>比较想要知道优雅停机方面的更详细内容，比如说terminationgraceperiodseconds与prestop之间的关系，两者怎么用</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/08/2aecb51f.jpg" width="30px"><span>混沌渺无极</span> 👍（6） 💬（1）<div>各位，中秋节好。
如果entrypoint是一个一直运行的命令，那postStart会执行吗？还是启动一个协程成执行entrypoint，然后再运行一个协程执行这个postStart，所以这两个命令的执行状态是独立的，没有真正的先后关系。</div>2018-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ercmNryEicqDS73icpUu7W0BnZ7ZIia6jR7kdVMIzH0q1d7L8EKAYWeTJcribibGcHnJzpsjRFxAe26egQ/132" width="30px"><span>pytimer</span> 👍（6） 💬（2）<div>老师，问一下，我看pod.status.phase是running，但是Ready是false，如果我想判断pod状态，要怎么做</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（5） 💬（1）<div>本地测试的进入shell容器后执行ps ax，跟例子的结果不一样。没有看到nginx窗口里的nginx进程信息，为什么，我看也有人遇到这个问题.
&#47; # ps
PID USER TIME COMMAND
1 root 0:00 sh
10 root 0:00 ps</div>2018-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/7f/a2/8ccf5c85.jpg" width="30px"><span>XThundering</span> 👍（4） 💬（3）<div>文章中有处有问题：&quot;ImagePullPolicy 的值默认是 Always，即...&quot; 这部分和官方文档与实际情况不一致。
在官方文档中提到&quot;The default pull policy is IfNotPresent&quot;，我这边在使用中发现的也是这样子的~
附一下官方文档链接：https:&#47;&#47;kubernetes.io&#47;docs&#47;concepts&#47;containers&#47;images&#47;</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/97/93e82345.jpg" width="30px"><span>陆培尔</span> 👍（4） 💬（3）<div>关于pod还有一事请教，之前老师说过pod所有进出流量都会经pause这个根容器，那么是否可以这样理解，实现service mesh的最佳方式是扩展这个根容器的功能来做流量控制和路由，这比再注入一个envoy要更加底层，更加原生？</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/eb/57/3032e1a7.jpg" width="30px"><span>loda</span> 👍（3） 💬（1）<div>请教个问题，当资源不足的时候，在调用k8s扩容会出现失败，然后一直pending，表示资源不够。怎么能在请求失败前提前检测到该现象呢，避免在继续出现pending请求？

如果要每次扩容前都全量扫描一个所有pod和node，然后计算剩余资源，开销也太大了；
如果要维护一个和kube-scheduler缓存一致的资源池，会不会又出现数据不一致的问题

业界在碰到该类问题的时候，都是怎么处理的呢？</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/89/9312b3a2.jpg" width="30px"><span>Vincen</span> 👍（2） 💬（2）<div>pod对象中的有些字段不能够在deployment中使用比如文章中提到的HostAliases，我们通常使用deployment来部署pod。这种情况怎么办？</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（2） 💬（3）<div>老师，pod的&#47;etc&#47;hosts文件怎么理解？是pause 容器的文件吗？</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（2） 💬（1）<div>老师您好，您提出的思考题能以java web解释下原因吗？还没实践过，想知道答案，谢谢</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/2d/befd19a6.jpg" width="30px"><span>AFA</span> 👍（2） 💬（2）<div>您好，pod结构体的文件目录是不是要指定kuber版本号？不指定版本号是不是有可能找不到？</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bb/49/975d4569.jpg" width="30px"><span>奇奇不怪</span> 👍（0） 💬（1）<div>你好，我看了评论去的很多遇到了实验结果和文章中的不符合，我根据你的回复查看了api-service的配置，默认是有一个--feature-gates=AllAlpha=true。这个应该就是你说的1.11默认开启的参数吧，但是我还是看不到nginx的进程。这会是什么原因造成的。</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/1c/2e30eeb8.jpg" width="30px"><span>旺旺</span> 👍（0） 💬（1）<div>nginx的yaml文件，后面几行好像少了2个空格缩进，应该是下面这样的吧：
root@k8s-master:~&#47;k8s# cat nginx.yaml 
apiVersion: v1
kind: Pod
metadata:
 name: nginx
spec:
 shareProcessNamespace: true
 containers:
 - name: nginx
   image: nginx
 - name: shell
   image: busybox
   stdin: true
   tty: true
</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/63/95fadffe.jpg" width="30px"><span>刘家兴</span> 👍（0） 💬（1）<div>error: error validating &quot;liujx-nginx-pod-shareProcessNamespace.yaml&quot;: error validating data: ValidationError(Pod.spec): unknown field &quot;shareProcessNamespace&quot; in io.k8s.api.core.v1.PodSpec; if you choose to ignore these errors, turn validation off with --validate=false

老师这是咋回事儿</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（0） 💬（1）<div>k8s pod type struct 路径改了，最新的路径在： kubernetes&#47;staging&#47;src&#47;k8s.io&#47;api&#47;core&#47;v1&#47;types.go</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/2e/01b2839e.jpg" width="30px"><span>巩夫建</span> 👍（0） 💬（1）<div>中秋节快乐，感谢作者地产出。知识点很丰富，对实际工作帮助很大。有个标签的问题求解一下，如果node1打了标签ssd，其他node没有打标签，如果一个没有标记标签的pod，在资源充足的情况下会偶发部署到node1上吗？如果资源不充足，会去占用node1的资源吗？
回答作业题，java的项目经常由于oom，导致pod正常，里面的子进程被kill掉。现在是关闭oom，是否有其他更优方案?</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/86/8211935c.jpg" width="30px"><span>Vincent</span> 👍（0） 💬（1）<div>思考题是Java web项目内存溢出？</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/c4/038f9325.jpg" width="30px"><span>Jeff.W</span> 👍（199） 💬（7）<div>POD的直议是豆荚，豆荚中的一个或者多个豆属于同一个家庭，共享一个物理豆荚（可以共享调度、网络、存储，以及安全），每个豆虽然有自己的空间，但是由于之间的缝隙，可以近距离无缝沟通（Linux Namespace相关的属性）。</div>2018-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d2/2f/04882ff8.jpg" width="30px"><span>龙坤</span> 👍（40） 💬（2）<div>你好，我进入shell容器，然后执行ps ax，跟例子的结果不一样。例子代码也一样，添加了shareProcessNamespace: true了，为什么不行呢，请问可能出现的原因在哪里
&#47; # ps
PID   USER     TIME  COMMAND
    1 root      0:00 sh
   10 root      0:00 ps

</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（27） 💬（0）<div>只要容器没有down掉，pod就会处于running状态。pod只会监控到容器的状态，但不会监控容器里面程序的运行状态。如果程序处于死循环，或者其他bug状态，但并没有异常退出，此刻容器还是会处于存活状态，但实际上程序已经不能工作了。
日常使用的感受是这样的，不知道对不。</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/ae/344fbda3.jpg" width="30px"><span>追风</span> 👍（9） 💬（0）<div>作者的那句评论。先让让子弹飞一会，让我看出了作者决胜千里之外的眼界。哈哈哈</div>2019-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ea/88/914d0c1b.jpg" width="30px"><span>短笛</span> 👍（4） 💬（2）<div>Pod 的意思我理解应该是指 a small herd or school of marine animals, especially whales 而不是豆荚，为什么是鲸群呢？因为 Docker 的 Logo 啊 😂</div>2018-11-21</li><br/>
</ul>