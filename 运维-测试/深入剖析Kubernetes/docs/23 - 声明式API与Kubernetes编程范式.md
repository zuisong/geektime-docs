你好，我是张磊。今天我和你分享的主题是：声明式API与Kubernetes编程范式。

在前面的几篇文章中，我和你分享了很多Kubernetes的API对象。这些API对象，有的是用来描述应用，有的则是为应用提供各种各样的服务。但是，无一例外地，为了使用这些API对象提供的能力，你都需要编写一个对应的YAML文件交给Kubernetes。

这个YAML文件，正是Kubernetes声明式API所必须具备的一个要素。不过，是不是只要用YAML文件代替了命令行操作，就是声明式API了呢？

举个例子。我们知道，Docker Swarm的编排操作都是基于命令行的，比如：

```
$ docker service create --name nginx --replicas 2  nginx
$ docker service update --image nginx:1.7.9 nginx
```

像这样的两条命令，就是用Docker Swarm启动了两个Nginx容器实例。其中，第一条create命令创建了这两个容器，而第二条update命令则把它们“滚动更新”成了一个新的镜像。

对于这种使用方式，我们称为**命令式命令行操作**。

那么，像上面这样的创建和更新两个Nginx容器的操作，在Kubernetes里又该怎么做呢？

这个流程，相信你已经非常熟悉了：我们需要在本地编写一个Deployment的YAML文件：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/21/8c13a2b4.jpg" width="30px"><span>周龙亭</span> 👍（129） 💬（5）<div>是因为envoy提供了api形式的配置入口，更方便做流量治理</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（82） 💬（14）<div>老师，用声明式api的好处没有体会太深刻。
如果在dosomething中merge出新的yaml，然后用replace会有什么缺点？
好像在这篇文章中仅仅提到声明式的可以多个客户端同时写。除此之外，还有其他优点吗？
也就是说修改对象比替换对象的优势在哪？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/49/125f5adc.jpg" width="30px"><span>mazhen</span> 👍（49） 💬（3）<div>有个疑问，在envoy-initializer的“控制循环”中获取新创建的Pod，这个Pod是否已经在正常运行了？
Initializer 提交patch修改Pod对象，Kubernetes发现Pod更新，然后以“滚动升级”的方式更新运行中的Pod？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（47） 💬（2）<div>kubectl apply 是通过mvcc 实现的并发写吗？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/08/2aecb51f.jpg" width="30px"><span>混沌渺无极</span> 👍（43） 💬（2）<div>dynamic admission control有点像防火墙的DNAT，数据包即将进入路由表的瞬间被修改了目的地址，这样路由表就对数据包的修改[无感]。
patch就像多人使用git来进行文件的&quot;合并型&quot;修改。</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/24/28acca15.jpg" width="30px"><span>DJH</span> 👍（28） 💬（2）<div>请教老师，Initializer和Preset都能注入POD配置，那么这两种方法的适用场景有何不同？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（23） 💬（5）<div>又查了下envoy的设计，感觉它支持热更新和热重启，应该很适合声明式规则的开发范式，这可以看做一种优势，相比而言，nginx的reload需要把worker进程退出，比较面向命令</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/cd/56/dca89081.jpg" width="30px"><span>lucasun</span> 👍（19） 💬（3）<div>Initializer不是一直bata然后废弃了嘛，istio用的是MutatingAdmissionWebhook吧</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/5e/818a8b1b.jpg" width="30px"><span>Alex</span> 👍（19） 💬（2）<div>Initializer与新的pod 在git merge冲突了该怎么解决？</div>2018-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3e/d2/5f9d3fa7.jpg" width="30px"><span>羽翼1982</span> 👍（16） 💬（1）<div>所以这个问题的答案是什么呢？
我的理解是Envy性能更高，占用系统资源更少</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（12） 💬（1）<div>服务网格最初是由linkerd项目提出概念的，lstio是另外一个后起之秀，使大家都关注到了边车代理模式和服务治理的新方法的巨大威力。文中应该笔误写错为微服务了。

不过瑕不掩瑜，本节写的极其精彩和深入浅出。</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/be/8350f94d.jpg" width="30px"><span>gotojeff</span> 👍（8） 💬（1）<div>Hi 老师
‘’‘有个疑问： name 为envoy的configmap是在哪里定义的呢？
2018-10-16
 作者回复
文中不是贴出来了？
’‘’
configmap模板中的 metadata - name是envoy-initializer，但是在下面的container volumes中的configmap name是envoy，我的疑惑是这是2个不同的configmap吧？后者是在其他地方定义的？
</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/42/79604ce6.jpg" width="30px"><span>公众号：云原生Serverless</span> 👍（8） 💬（1）<div>磊哥竟然穿插了istio的讲解，后续有没有计划讲讲knative呢</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（7） 💬（3）<div>老师，为什么修改对象可以多个客户端同时写，而替换不行？感觉还差一层窗户纸，老师帮我捅破:)
或者有什么资料可以让我更深入理解下吗？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/b4/a6db1c1e.jpg" width="30px"><span>silver</span> 👍（6） 💬（1）<div>kubectl apply怎么做concurrency control呢？假设client A和B都有version 1的spec。然后他们在各自修改了spec之后call apply。假设client A的patch操作先成功，如果kubectl简单的与etcd里有的spec做一个diff，会不会出现一个client B把client A的更新个revert的情况？</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/18/e7/d58e287c.jpg" width="30px"><span>参悟</span> 👍（5） 💬（1）<div>我想envoy的成功，是因为它真正理解了k8s的技术精髓，并成功的应用到了当前最火的微服务领域，将微服务体系与K8S捆绑在一起，service mesh成为微服务新一代技术的代言，这无论从技术上还是战略上都赢得了google的芳心，成功也就水到渠成。</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/5b/07858c33.jpg" width="30px"><span>Pixar</span> 👍（4） 💬（3）<div>可以这样理解吗？以istio 为例，其实存储在etcd 中的 pod 对象并没有 envoy 设置，所有的envoy 设置都是对象被etcd 取出后 initiater  加上去的？  initiater 加上去以后，会用含有envoy 配置的 对象复盖掉 etcd 中没有envoy 配置的吗？</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/86/fb/4add1a52.jpg" width="30px"><span>兵戈</span> 👍（4） 💬（2）<div>针对磊哥的思考题，Envoy的官方文档有相关文章分析：https:&#47;&#47;www.envoyproxy.io&#47;docs&#47;envoy&#47;latest&#47;intro&#47;comparison
比如完备的 Http&#47;2 支持、高级负载均衡、可插入式架构、详细的统计分析等，可见Envoy这个组件比较完备且性能够好。</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（4） 💬（3）<div>老师您好，我对声明式api还是没有太理解，除了apply还有其他的命令吗？您文中提到的kubectl set image和kubectl edit也算是声明式api吗</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/3e/534db55d.jpg" width="30px"><span>huan</span> 👍（3） 💬（1）<div>之前一直用nginx和haproxy，没用过envoy。
查了下官网，看envoy的核心特性之一是“small memory footprint”，我想这个特征特别适合envoy作为sidecar的角色注入到每个pod中（类似的用汇编写的pause容器一样的底层容器）</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/50/bde525b1.jpg" width="30px"><span>北卡</span> 👍（2） 💬（1）<div>对envoy不太明白，envoy和traefik有什么类似之处吗？</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/e5/7e86498f.jpg" width="30px"><span>cqc</span> 👍（1） 💬（1）<div>除了能想到envoy作为通用的sidecar可以提供更为完善的微服务治理能力之外，在代理网络流量方面，感觉其他两个软件也能做到。求解答^.^</div>2018-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/47/08/985632a6.jpg" width="30px"><span>旭</span> 👍（1） 💬（1）<div>老师，我的Nodeport与master的ip不能访问，node的ip和nodeport是可以访问，把forward改成accept也还是不行，麻烦老师指点下，多谢了</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/80/be/8350f94d.jpg" width="30px"><span>gotojeff</span> 👍（0） 💬（1）<div>有个疑问： name 为envoy的configmap是在哪里定义的呢？
</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/60/0d5aa340.jpg" width="30px"><span>gogo</span> 👍（0） 💬（1）<div>老师您好，有个问题请教您，提交镜像的时候可以使用latest标签吗？如果image是latest的话，kubectl apply怎样强制重新拉取镜像呢？</div>2018-10-16</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（48） 💬（2）<div>通俗地说：如果要把一个东西存入冰箱。命令式API需要做的是：打开冰箱 -&gt; 放入东西 -&gt; 关掉冰箱。而声明式就是： 这个东西在冰箱里。



命令式请求与声明式请求：
（1）服务对于命令式请求，一次只能处理一个写请求，否则可能会导致冲突
（2）服务对于声明式请求，一次能处理多个请求，并且具备Merge的能力

kubectl replace命令与kubectl apply命令的本质区别在于，kubectl replace的执行过程，是使用新的YAML文件中的API对象，替换原有的API对象；而kubectl apply，则是执行了一个对原有API对象的PATCH（部分更新）操作

声明式API特点：
（1）我们只需要提交一个定义好的API对象来“声明”，我所期望的状态是什么样子
（2）声明式API允许由多个API写端，以PATCH的方式对API对象进行修改，而无需关心本地原始YAML文件的内容
（3）有了上述两个能力，Kubernetes项目才可以给予对API对象的增、删、改、查，在完全无需外界干预的情况下，完成对“实际状态”和“期望状态”的调谐（Reconcile）过程


</div>2020-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/40/ba/2c8af305.jpg" width="30px"><span>Geek_zz</span> 👍（46） 💬（0）<div>居然看一遍就记住了这节课的原理</div>2018-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/98/9e/b9069b65.jpg" width="30px"><span>Lis</span> 👍（18） 💬（0）<div>老师好，课后作业的方式非常棒，可否在下一节课的开始先总结一下课后作业呢？</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/98/02/14e24394.jpg" width="30px"><span>Zhikun Lao</span> 👍（6） 💬（1）<div>老师你好！
”如果你对这个 Demo 感兴趣，可以在这个 GitHub 链接里找到它的所有源码和文档。这个 Demo，是我 fork 自 Kelsey Hightower 的一个同名的 Demo“

我看这个initializer的plugin都已经没了，现在是不是都要写Admission hook了？ https:&#47;&#47;kubernetes.io&#47;docs&#47;reference&#47;access-authn-authz&#47;extensible-admission-controllers&#47;#

例如这个 https:&#47;&#47;github.com&#47;kubernetes&#47;kubernetes&#47;blob&#47;v1.13.0&#47;test&#47;images&#47;webhook&#47;main.go</div>2019-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9c/67/c0128e6c.jpg" width="30px"><span>Dillion</span> 👍（4） 💬（0）<div>我对声明式API的理解是：apiserver与etcd在不断维护者某个对象各个属性字段。修改对象状态的方式是修改这个对象的属性。也就是，对象的属性作为API，暴露给用户，用户通过修改对象属性，实现对对象的修改。</div>2018-10-15</li><br/>
</ul>