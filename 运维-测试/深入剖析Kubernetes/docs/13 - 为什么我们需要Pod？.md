你好，我是张磊。今天我和你分享的主题是：为什么我们需要Pod。

在前面的文章中，我详细介绍了在Kubernetes里部署一个应用的过程。在这些讲解中，我提到了这样一个知识点：Pod，是Kubernetes项目中最小的API对象。如果换一个更专业的说法，我们可以这样描述：Pod，是Kubernetes项目的原子调度单位。

不过，我相信你在学习和使用Kubernetes项目的过程中，已经不止一次地想要问这样一个问题：为什么我们会需要Pod？

是啊，我们在前面已经花了很多精力去解读Linux容器的原理、分析了Docker容器的本质，终于，“Namespace做隔离，Cgroups做限制，rootfs做文件系统”这样的“三句箴言”可以朗朗上口了，**为什么Kubernetes项目又突然搞出一个Pod来呢？**

要回答这个问题，我们还是要一起回忆一下我曾经反复强调的一个问题：容器的本质到底是什么？

你现在应该可以不假思索地回答出来：容器的本质是进程。

没错。容器，就是未来云计算系统中的进程；容器镜像就是这个系统里的“.exe”安装包。那么Kubernetes呢？

你应该也能立刻回答上来：Kubernetes就是操作系统！
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/c9/abb7bfe3.jpg" width="30px"><span>段帅民</span> 👍（421） 💬（14）<div>这文章读起来像吃脆苹果，爽，这是我订阅专栏中写的最好的，没有之一</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（60） 💬（13）<div>看得太爽了。请教一个问题：
war和tamcat这种情况。
如果把war独立出来做一个镜像的话，应该用什么做基础镜像呢？
我现在做镜像的时候通常都是用debian做基础镜像，但如果只是为了复制这个.war包的话，用debian感觉蛮浪费的。应该怎样做到最小呢，而且要支持cp命令。</div>2018-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/61/985f3eb7.jpg" width="30px"><span>songyy</span> 👍（43） 💬（3）<div>为什么说“Docker in Docker”这种方式在生产环境后患无穷呀？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/77/30e059c8.jpg" width="30px"><span>kindnull</span> 👍（32） 💬（7）<div>从事Linux运维工作多年，有一点一直有点不明白，这里到底谁挂载到谁上面：
volumeMounts：
      -mountpath: &#47;app
        name: app-volume

文中有有这句话说&quot;而后这个 &#47;app 目录，就挂载了一个名叫 app-volume的Volume&quot;
这里是说将app-volume挂载到&#47;app上，但是app是个目录，那我想问的是app-volume是个目录还是设备？
同样下面：
volumeMounts:
    -mountpath:&#47;root&#47;apache-tomcat-7.0.42-v2&#47;webapps
       name:app-volume
---Tomecat容器同样声明了挂载app-volume到自己的webapps目录下

这里又说把app-volume挂载到webapps下，webapps明显是个目录，那app-volume是个目录吗？

但是我清楚记得在Linux下。如果要挂载一个分区设备到一个目录或者一个目录到另外一个主机目录下应该是：
mount  -t xxfs  src_dir   dest_dir
比如： mount  -t xfs &#47;dev&#47;sda   &#47;opt&#47;app
           mount -t nfs &#47;share&#47;data  192.168.0.100:&#47;data
上面的挂载的app-volume到底是设备还是文件，或者是去的一个别名？</div>2018-09-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PUiby8MibibKcMd88OtDq1c0myEILZjap46fyiaOlML0UlNWzj9NTIEXOhXCCR1tcUibG0I6UoGp59Zj8H5EYwzkY9g/132" width="30px"><span>fldhmily63319</span> 👍（18） 💬（2）<div>重问： 关于升级war和tomcat那块，也是先修改yml？然后kubenertes执行升级命令，pod会重新启动，生产也是按照这种方式吗？

所以这种情况下面，如果只是升级个war包，或者加一个新的war包，tomcat也要重新启动？这就不是完全松耦合了？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（16） 💬（2）<div>张老师，我们公司一直有一个问题： 我们用docker 管理测试环境，对于springboot 项目，一向是java -jar xx.jar 的方式启动，但因为是测试环境，经常代码本身有问题导致java（也就是容器主进程）启动不起来，进而触发健康检查重新调度该服务，然后开发总是抱怨看不到事故现场。我打算自己实现一个程序（我们称为nile），容器启动时先启动nile确保容器可以启动起来，再由nile启动java进程。这时还可以让nile 读取用户配置 自定义设置jvm 参数、nile向zk汇报一些应用情况等。这个做法呢，nile可以算是java 的sidecar，按您文章的说法，nile和java 是拓扑关系而不是对等关系，这个时候我一个pod里分别是nile和java容器是否可能呢？</div>2018-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/2e/01b2839e.jpg" width="30px"><span>巩夫建</span> 👍（15） 💬（8）<div>非常棒，释义了pod的理念。有个小问题，像我之前一个docker中跑tomcat和nginx两个进程，共用同一个文件，如果拆成三部分，第一init container 文件镜像，第二 tomcat镜像，第三 nginx镜像，如何保证init container 启动后启动tomcat，最后启动nginx，还有这种优点有什么?目前只想到镜像高复用，谢谢作者。</div>2018-09-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rUPjvMdUGic56wNdVm0be85REaB7nLwyEC7HiamhmeWsQichtADA3IsFubIqOXMjlsEtmicdpDRC2YhNWVrpPKj1lw/132" width="30px"><span>姜子牙</span> 👍（14） 💬（1）<div>容器的“单进程模型”，并不是指容器里只能运行“...
这一段里说容器的单进程模型。我在跑一个web后端服务，springboot实现。 entrypoint 是java -jar xxxx.jar  .这条命令产生的进程就是PID=1的吗？ 容器只能管理PID=1的。我理解的就是这个进程执行不成功，容器户退出。但是如果我的springboot程序有问题，没跑成功，容器依然跑着呢，为啥?</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（11） 💬（4）<div>war包的例子并没有解决频发打包的问题吧? wa包变动后, geektime&#47;sample:v2包仍然需要重新打吧. 这和东西一股脑装在tomcat中后, 重新打tomcat 并没有差太多吧?</div>2018-10-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GDYkD2X7pXSKUSaUFC8u3TBPaakaibnOBV2NYDc2TNfb8Su9icFMwSod6iaQX5iaGU2gT6xkPuhXeWvY8KaVEZAYzg/132" width="30px"><span>extraterrestrial！！</span> 👍（10） 💬（2）<div>容器不能管理多进程那块，能不能每个容器都默认搬一套系统的init过去，而不要让普通应用进程做进程1，这样是不是就可以支持容器里面管理多进程了？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/14/c4/e354d8ba.jpg" width="30px"><span>魏颖琪</span> 👍（9） 💬（1）<div>写得很清晰，但是rsyslogd例子有问题。在ptree中rsyslogd给出的in:imklog，in:imuxsock，rs:main Q:Reg是线程不是进程。在ps -ef中是看不到的，但是在ps -efL中可以看到（When used with -L, the NLWP (number of threads) and LWP (thread ID) columns will be added. -- man ps)。而ptree的-P除了显示进程号，也会显示线程号（Child threads of a process are found under the parent process and are shown with the process name in curly braces.  -- man pstree)）。如果出书的话，建议老师选择另外的例子。</div>2019-01-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLIjtoBftwZxfXcxsTZUFGkd7SnnKJCazmBbwFEVPmHbWsWRwC7SHCGUNibCIvpddqct1Ybezmz6w/132" width="30px"><span>Eddie LAU</span> 👍（8） 💬（1）<div>此专栏追到现在，老师用通俗的语言阐述了k8s的原理的同时也极力推崇k8s。我在学习使用的过程中也确实体会到了其各种优势。但是反过来想，老师是否可以简单举两个例子说下k8s目前为止依然存在的一些缺陷和不足呢？方便我们在应用过程中加以注意。</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/19/a15d060d.jpg" width="30px"><span>silverhawk</span> 👍（8） 💬（1）<div>非常好，请教一个问题，你之前说比如PHP和MySQL最好分在不同的pod，很可能就是不同的node上了，那么对于latency非常敏感的比如cache，像redis和一个web server是不是做成不同的container部署在一个pod里面合适呢？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/f3/01bf3b3e.jpg" width="30px"><span>王亚南</span> 👍（5） 💬（1）<div>不得不说，真是良心之作。</div>2018-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/b3/244b5192.jpg" width="30px"><span>lggl</span> 👍（5） 💬（1）<div>关于升级war和tomcat那块，也是先修改yml？然后kubenertes执行升级命令，pod会重新启动，生产也是按照这种方式吗？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b6/97/93e82345.jpg" width="30px"><span>陆培尔</span> 👍（4） 💬（2）<div>张老师的课获益匪浅，我们现在在做spring boot项目的容器化，现在是把整个jar包连同环境打成镜像，现在是否可以分解为一个jar包和一个java基础环境镜像？</div>2018-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/dd/6a1ba128.jpg" width="30px"><span>star</span> 👍（4） 💬（1）<div>对于war包这个例子还有点不明白，war包这个 &#47;app 目录，就挂载了一个名叫 app-volume...那么这个app-volume是对应宿主机？还是infra容器？

难道可以创建一个没有任何对应的volume么？

</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/08/c43f85d9.jpg" width="30px"><span>IOVE.-Minn</span> 👍（3） 💬（1）<div>老师，咨询个事情。现在在中国哪些地方能考CKA呢？ 费用是多少呢？ 有年限限制的么？</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a6/23/91e74c43.jpg" width="30px"><span>leo</span> 👍（3） 💬（1）<div>不好意思，还是我，您的回复我没看懂。我的问题有两个
1.产生日志的容器是否属于应用容器？
2.一个Pod里是否可以只有init container，没有用户容器？
烦请解答一下，感谢！</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（3） 💬（1）<div>在 Pod 中，所有 Init Container 定义的容器，都会比 spec.containers 定义的用户容器先启动。并且，Init Container 容器会按顺序逐一启动，而直到它们都启动并且退出了，用户容器才会启动。
这里的init Container 容器是在启用完后，【会被自动删除】，接下来才启动用户窗口吗？</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a0/30/5a7247eb.jpg" width="30px"><span>eden</span> 👍（2） 💬（1）<div>老师，我有个疑问。按我之前对docker的理解docker容器也可以启动多个进程，一个docker容器不一定就是一个进程，比如docker容器的启动程序可以是个脚本，通过脚本可以启动多个进程，只要只有一个进程运行在前台即可。</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b2/47/11321969.jpg" width="30px"><span>烽火戏诸侯</span> 👍（2） 💬（1）<div>张老师 请教个问题哈，关于initcontainer这块，可不可以理解pod里面的container 有着服务依赖的关系，那以此类推，statefulset 可以理解是这个逻辑层次更高的概念吗？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/32/fab70236.jpg" width="30px"><span>择动</span> 👍（2） 💬（1）<div>偶像，那pod有和虚拟机在类比时又有什么不同呢，还是没什么不同？</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/4a/b722cbbc.jpg" width="30px"><span>Xiao淩求个好运气</span> 👍（1） 💬（1）<div>就这一篇文章，配得上我为整个专栏付费，真是醍醐灌顶</div>2020-03-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/mrJwOdcr1xslW2eZFc1nogbRNc8rPRExOaQsgFXFicKF0H7TOtII1n1haaJd7t55ZWeUz1FPGZian5ejcvuJibQQg/132" width="30px"><span>九月の秋雨</span> 👍（1） 💬（1）<div>老师你好,我对tomcat和war包的打包方式有点疑问.
docker镜像设计之初就是为了&quot;一次打包,到处运行&quot;,镜像内应该包含能够运行应用的完整的环境.但是将war包和tomcat拆开打包的反正不就违反了这一原则吗?而且应用的运行方式和底层的基础设施绑定了,如果我的开发人员在本地运行的是docker而不是k8s的话他就无法通过这种pod的方式来运行他的应用.</div>2018-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCEsLNSXFBaTZeHxGENXHibdsycvOpQFKKNIxxKhD4xApwgZhfQoZC77WXtvNLv8lY3oLJUwV6MpQ/132" width="30px"><span>weiwunb</span> 👍（1） 💬（3）<div>老师 关于init container第二个日志例子 比较费解: 因为init container启动完成退出之后 应用容器才会启动，那收集日志的工作放在init container 怎么还源源不断把日志发到es呢？??</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/64/54458855.jpg" width="30px"><span>Caesar</span> 👍（1） 💬（1）<div>centos7+kubernetes+cri-containerd+kata-runtime，经过实践，在一个pod中有两个业务容器，两个业务容器会共享 Pause 容器除了Pid Namespace外所有的命名空间</div>2018-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bc/08/c43f85d9.jpg" width="30px"><span>IOVE.-Minn</span> 👍（1） 💬（1）<div>请问，sidecar这种用initcontainer的方式和后面讲到的statefulset的改变拓扑状态，有什么区别么？ </div>2018-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cf/f1/bf63fef6.jpg" width="30px"><span>洛子墟</span> 👍（1） 💬（1）<div>完美解决war和tomcat做一起，完成镜像的频繁打包问题！而且占据空间太大! 666</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（1） 💬（1）<div>&quot;Pod 的生命周期只跟 Infra 容器一致，而与容器 A 和 B 无关&quot;，那么当Pod中用户的容器A或者B崩溃了，k8s怎么收到failure message并且重新去部署Pod呢</div>2018-09-23</li><br/>
</ul>