你好，我是Chrono。

前两节课里我们学习了Kubernetes里的三种API对象：Pod、Job和CronJob，虽然还没有讲到更高级的其他对象，但使用它们也可以在集群里编排运行一些实际的业务了。

不过想让业务更顺利地运行，有一个问题不容忽视，那就是应用的配置管理。

配置文件，你应该有所了解吧，通常来说应用程序都会有一个，它把运行时需要的一些参数从代码中分离出来，让我们在实际运行的时候能更方便地调整优化，比如说Nginx有nginx.conf、Redis有redis.conf、MySQL有my.cnf等等。

我们在“入门篇”里学习容器技术的时候讲过，可以选择两种管理配置文件的方式。第一种是编写Dockerfile，用 `COPY` 指令把配置文件打包到镜像里；第二种是在运行时使用 `docker cp` 或者 `docker run -v`，把本机的文件拷贝进容器。

但这两种方式都存在缺陷。第一种方法相当于是在镜像里固定了配置文件，不好修改，不灵活，第二种方法则显得有点“笨拙”，不适合在集群中自动化运维管理。

对于这个问题Kubernetes有它自己的解决方案，你也应该能够猜得到，当然还是使用YAML语言来定义API对象，再组合起来实现动态配置。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/dc/badd82d7.jpg" width="30px"><span>江湖十年</span> 👍（55） 💬（2）<div>ConfigMap 和 Secret 对存储数据的大小是有限制的，限制为 1MiB，官方文档：https:&#47;&#47;kubernetes.io&#47;zh-cn&#47;docs&#47;concepts&#47;configuration&#47;configmap&#47;#motivation</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/ed/3a/ab8faba0.jpg" width="30px"><span>陶乐思</span> 👍（29） 💬（3）<div>用env和volume两种方式创建的pod都尝试了，修改了ConfigMap&#47;Secret 的 YAML后 kubectl apply，Pod里的value并不会改变。
所以这两种方式在创建pod的时候，其实都是一次性拷贝，POD controller manager只会管理POD这个层级，并不会发现POD之下层级发生的变化。</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（23） 💬（2）<div>1. configmap 和secret相同点有很多，其中一点就是键值对数据存储。不同点就是一个加密，一个不加密，但是secret只支持base64加密吗，可以支持其他格式加密吗？如果都是base64加密，存在破解的可能性吗。是否不安全，如果不是可以选择不同的加密方式，会不会安全点。
2. 我看大家的答案是pod并不会修改里面的值，可我测试的结果是env-pod确实不会修改值，实际上应该是大家说的一次性拷贝，但另外一个vol-pod我测试的结果是，会改变值啊，难道我测试的方式有什么问题吗?</div>2022-07-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/WrANpwBMr6DsGAE207QVs0YgfthMXy3MuEKJxR8icYibpGDCI1YX4DcpDq1EsTvlP8ffK1ibJDvmkX9LUU4yE8X0w/132" width="30px"><span>星垂平野阔</span> 👍（9） 💬（2）<div>把configmap挂进了pod里面，然后重新deploy了下configmap，发现pod里面的变量还是原来的，没有同步更新。
个人猜测应该是挂载的同时已经把configmap的内容引入pod内部，除非pod重启，不然不会随着它更新。</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/b9/47377590.jpg" width="30px"><span>Jasper</span> 👍（6） 💬（1）<div>迫不及待的看完，期待下一节</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/89/ba/009ee13c.jpg" width="30px"><span>霍霍</span> 👍（4） 💬（1）<div>相见恨晚，老师带着，感觉k8s的概念学起来轻松愉快</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（4） 💬（1）<div>实测：修改了 ConfigMap&#47;Secret 的 YAML，然后使用 kubectl apply后，通过env环境变量的方式加载的配置不会更新，通过mount文件方式加载的配置会在延时约20s后更新配置。</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（4） 💬（1）<div>老师，有几个小问题：

1. 像配置这块儿，有多少个不同类型的配置，就需要定义多少个不同的Volume进行挂载吗？例如ConfigMap 和 Secret 这里挂载了两个Volume。

2. vol-pod   0&#47;1     CrashLoopBackOf   当pod变成这个状态的时候，只能删除了再重新创建吗？ 使用命令 ：kubectl delete -f vol-pod.yml。

3. 课外小贴士的最后一条，没太明白，老师能再说说看吗？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/f8/01e7fc0e.jpg" width="30px"><span>郑小鹿</span> 👍（4） 💬（3）<div>课后问题回答：
1、说一说你对 ConfigMap 和 Secret 这两个对象的理解，它们有什么异同点？
相同点：
都可以用来把配置数据和服务程序分离
都是一种用于存储的API对象
都以键值对k-v的方式存储数据
都可以作为数据卷挂载在其他API对象上使用
都不适合存储大数据，每个 ConfigMap &#47;Secret 最多支持存储1MB的数据，毕竟对内存有消耗


不同点：
ConfigMap一般存储非机密信息
Secret用于存储机密信息，默认是Base64编码方式对value字符进行处理。
Secret保存在etcd中内容是未经过加密的，对于Secret资源的权限要做好控制，可以通过RBAC规则来限制或者是使用其他加密方式


2、如果我们修改了 ConfigMap&#47;Secret 的 YAML，然后使用 kubectl apply 命令更新对象，那么 Pod 里关联的信息是否会同步更新呢？你可以自己验证看看。
如果 ConfigMap 是作为环境变量方式使用的，那数据不会被自动更新。 想要更新这些数据需要重新启动 Pod。
</div>2022-07-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（4） 💬（2）<div>想请教老师几个问题：

1、`echo -n &quot;123456&quot; | base64` 加 -n 仅仅是为了去掉换行符吗，`&quot;123456&quot;` 中并没有换行符，为什么加 -n 与不加 -n 的结果有区别？

2、构建 Pod 的时候，Secret 中的变量会被自动解码，K8S 是如何知道该用何种方式进行解码？需要通过 Secret 对象中的参数进行指定吗？</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（3） 💬（1）<div>yaml文件还真不好写，我对着课文写minikube运行不了，用老师的一下就过了</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c4/51/5bca1604.jpg" width="30px"><span>aLong</span> 👍（2） 💬（1）<div>1. ConfigMap与Secret很类似，两人使用方式上基本相同。主要不同凸显在数据的编码方式，Secret是base64，ConfigMap是明文。 
2. 当Secret更新后，通过Volume形式ConfigMap、Secret是会更新的，与其相反就是ENV形式。 ENV形式使用方面比Volume显得方便，无需读取文件。</div>2023-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（2） 💬（1）<div>尝试修改pod里面的配置，显示为只读，不能和docker一样，直接修改，不然可以测试以下，容器里面修改，会不会改变外面的数据，理论上来说可以修改的话，应该外面的也会被修改，但k8s修改一个值，必须是要通过api-server来修改，所以如果直接修改就会很奇怪，这也应该是为啥这个内容禁止我修改的原因吧。</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（2） 💬（1）<div>思考1:
configMap和secret都可以用阿里管理配置信息，都支持env和volume两种形式在pod中使用。不过configMap使用明文保存配置信息，secret采用加密方式保存；
思考2:
我的验证结果跟前面几位同学有点不一样，使用env的方式，修改ConfigMap和Secret的YAML然后kubectl apply后pod中关联的信息确实不会同步更新；但如果使用volume的话，这些关联信息是会更新的，只是更新的不及时，猜测后台有一个定时任务负责处理。</div>2022-07-26</li><br/><li><img src="" width="30px"><span>Geek_44c03e</span> 👍（1） 💬（1）<div>有个疑问。用cm管理配置文件内容在容器里变成了kv而不是像docker run -v同步文件。这样软件使用上会有问题吧？可以用nginx.conf举例</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（1） 💬（1）<div>请教老师一个问题：使用kubectl apply 命令更新对象，证明pod中的关联信息不会同步更新。那有没有机制能够在更新对象之后 同步更新pod中的关联信息的？类似以配置中心的推送一样的，不需要重启pod。</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（1） 💬（2）<div>vol-env的逻辑应该是和docker -v挂载是一样的，docker -v是宿主机一样的，两者改变是同步的。</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/82/ec/99b480e8.jpg" width="30px"><span>hiDaLao</span> 👍（1） 💬（1）<div>另外我发现使用kubectl describe pod时，所有的pod都挂载了一个类型为Projected的kube-api-access-xxx的特殊volume，请问下老师这个volume时用来做授权的吗？</div>2022-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/ac/10d68f01.jpg" width="30px"><span>江同学</span> 👍（1） 💬（1）<div>如果我们修改了 ConfigMap&#47;Secret 的 YAML，然后使用 kubectl apply 命令更新对象，那么 Pod 里关联的信息不会同步更新，需要把使用到的pod删除，重新使用apply命令更新对象才会更新到更改的信息</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：“kube-root-ca.crt”是什么configMap对象
按照文中的第一个对象创建例子，创建了一个info对象，用kubectl get cm查看，
除了info对象以外，还有一个对象kube-root-ca.crt，这是谁创建的？

Q2：k8s默认使用Base64进行加密，文中用的linux工具，也是Base64，
不都是一样吗？

Q3：etcd是k8s默认就启动的吗？我启动k8s时，用命令“minikube start --kubernetes-version=v1.23.3”，
并没有显式启动etcd。</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（1） 💬（1）<div>Linux中环境变量🈶️限制，不能食用“-”</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a3/4d/59390ba9.jpg" width="30px"><span>排骨</span> 👍（0） 💬（1）<div>启动pod之后一直报错提示
Error from server (BadRequest): container &quot;busy-pod&quot; in pod &quot;env-pod&quot; is waiting to start: CreateContainerConfigError
使用kubectl logs env-pod也是这个日志，要使用kubectl describe pod env-pod查看，发现是我的环境变量key写错了</div>2024-07-08</li><br/><li><img src="" width="30px"><span>努力的蜡笔小新</span> 👍（0） 💬（1）<div>我来说下最近学习的心得，有些东西能理解，有些我还消化不了，有的更是文章没提到的问题，但我很庆幸的是，我从一个小白，不懂容器，不懂k8s的人来说，我学习了后，我能看懂ymal的大概意思是做什么的和意图，但我也安慰自己，不可能两天时间就能消化掉人家十几年的心血，要放平心态去学习，不懂的重复多看几遍，不断的寻找文档加深理解，我相信总有一天我能在生产中应用上所学的知识</div>2024-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>ConfigMap和Secret类型的pod是否都是在其他pod对象启动前启动 k8s管理的素有对象 是不是都有个启动顺序问题啊 顺寻这个事 后边会讲么</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>kubectl create secret generic user --from-literal=name=root $out 这串命令有点困惑 其他的都是 create + 对象 + 自定义名字 这个为啥多个generic 这个是干什么用的 我发现去了会报错，除了这个secret对象多个generic其他对象是否也会又类似特殊处理情况，我改如何掌握其他对象</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/de/7e/549a899d.jpg" width="30px"><span>李童心小组</span> 👍（0） 💬（1）<div>vol-pod 会更新，但感觉不是实时的，要等一段时间，是这样的吗？</div>2023-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/3f/84/47f7b661.jpg" width="30px"><span>你好极客时间</span> 👍（0） 💬（1）<div>老师好，我这里访问报错502，这应该是wordpress的问题么？

[root@localhost ~]# curl http:&#47;&#47;127.0.0.1
&lt;html&gt;
&lt;head&gt;&lt;title&gt;502 Bad Gateway&lt;&#47;title&gt;&lt;&#47;head&gt;
&lt;body&gt;
&lt;center&gt;&lt;h1&gt;502 Bad Gateway&lt;&#47;h1&gt;&lt;&#47;center&gt;
&lt;hr&gt;&lt;center&gt;nginx&#47;1.23.2&lt;&#47;center&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;
[root@localhost ~]#
</div>2022-12-07</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（1）<div>老师，这个环境变量我在当前终端设置了，但kubectl create cm info $out 这个命令执行时，仍然报错，提示：error:Invalid dry-run value (client - o yaml).Must be &quot;none&quot;, &quot;server&quot;, or &quot;cllient&quot;, 是哪里没设置对？</div>2022-11-07</li><br/><li><img src="" width="30px"><span>edward</span> 👍（0） 💬（1）<div>export out=&quot;--dry-run=client -o yaml&quot;</div>2022-11-07</li><br/><li><img src="" width="30px"><span>Geek_cb910c</span> 👍（0） 💬（1）<div>Downward API，希望也能提一下这个。这个在实际业务中，用来获取POD信息，也算是业务中常用的配置信息</div>2022-10-24</li><br/>
</ul>