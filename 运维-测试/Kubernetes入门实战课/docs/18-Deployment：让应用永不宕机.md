你好，我是Chrono。

在上一节课里，我们使用kubeadm搭建了一个由两个节点组成的小型Kubernetes集群，比起单机的minikube，它更接近真实环境，在这里面做实验我们今后也更容易过渡到生产系统。

有了这个Kubernetes环境，接下来我们就在“初级篇”里学习的Pod知识基础上，深入研究一些由Pod衍生出来的其他API对象。

今天要看的API对象名字叫“**Deployment**”，顾名思义，它是专门用来部署应用程序的，能够让应用永不宕机，多用来发布无状态的应用，是Kubernetes里最常用也是最有用的一个对象。

## 为什么要有Deployment

在[第13讲](https://time.geekbang.org/column/article/531566)里，我们学习了API对象Job和CronJob，它们代表了生产环境中的离线业务，通过对Pod的包装，向Pod添加控制字段，实现了基于Pod运行临时任务和定时任务的功能。

那么，除了“离线业务”，另一大类业务——也就是“在线业务”，在Kubernetes里应该如何处理呢？

我们先看看用Pod是否就足够了。因为它在YAML里使用“**containers**”就可以任意编排容器，而且还有一个“**restartPolicy**”字段，默认值就是 `Always`，可以监控Pod里容器的状态，一旦发生异常，就会自动重启容器。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/f8/01e7fc0e.jpg" width="30px"><span>郑小鹿</span> 👍（38） 💬（6）<div>问题回答
1、如果把 Deployment 里的 replicas 字段设置成 0 会有什么效果？有什么意义呢？
做了下实验，效果如下：
$ kubectl get po -n nginx-deploy                   
No resources found in default namespace.
$ kubectl get deploy                  
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   0&#47;0     0            0  

意义：关闭服务的同时，又可以保留服务的配置，下次想要重新部署的时候只需要修改deployment就可以快速上线。

2、你觉得 Deployment 能够应用在哪些场景里？有没有什么缺点或者不足呢？
使用场景：用在部署无状态服务，部署升级，对服务的扩缩容；多个Deployment 可以实现金丝雀发布

不足：Deployment把所有pod都认为是一样的服务，前后没有顺序，没有依赖关系，同时认为所有部署节点也是一样的，不会做特殊处理等

疑问：Deployment变更副本数时，是先删除pod，然后再重建pod，如果服务启停时间比较长，会出现什么问题不？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/3d/b290414d.jpg" width="30px"><span>岁月长</span> 👍（37） 💬（1）<div>回答问题1:
之前在公司的时候，有时候会把服务下线，这个时候就会把 replicas 字段改为 0，观察一段时间没问题后在把配置删除，如果有报错也方便马上恢复</div>2022-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（30） 💬（1）<div>懂后恍然大悟，不懂时举步维艰，学习的快乐大抵如此</div>2022-08-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKx6EdicYYuYK745brMa9yAlkZs2YmzxRAm4BQ2kw9GbtcC8ebnQlyBfIJnGjH57ib4HVlQIpSbTrBw/132" width="30px"><span>dst</span> 👍（9） 💬（2）<div>回答一下问题2，deploy是只能用在应用是无状态的场景下，对于有状态的应用它就无能为力了，需要使用其他的api</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（8） 💬（2）<div>老师，我想线创建一个pod，然后直接使用ngx-aadep来管理老的pod，这样的方式不行吗，你课程里说，pod不属于deployment。那我就单独创建，但是显示我语法错误。

cat ngx-aadep.yaml 
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: ngx-aa
  name: ngx-aa
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ngx-aa
cat ngx-aapod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: ngx-aa
    app: ngx-aa
  name: ngx-aa
spec:
  containers:
  - image: nginx:alpine
    name: ngx-aa
</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/b4/47c548fd.jpg" width="30px"><span>一只鱼</span> 👍（7） 💬（1）<div>按照文章中的说法，一层一层嵌套：deployment 管理 pod , pod 管理 containers 

那谁来管理 deployment 呢，如果 deployment 出错了怎么办？</div>2023-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/6f/1654f4b9.jpg" width="30px"><span>nc_ops</span> 👍（6） 💬（1）<div>对这句话有个疑问，“kubectl scale 是命令式操作，扩容和缩容只是临时的措施，如果应用需要长时间保持一个确定的 Pod 数量，最好还是编辑 Deployment 的 YAML 文件”
我刚实验通过kubectl scale去扩容pod数量，然后通过kubectl delete去删除一个pod，立马又会新生成一个pod，所以通过kubectl scale也是能保持一个确定的pod数量的吧？通过yaml文件去改变副本的好处准确来说应该是让整个生产环境里只有一份配置的描述，避免当kubectl scale执行后，实际deployment规格与yaml文件里不一致，避免让运维引发混淆</div>2022-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/7e/f1efd18b.jpg" width="30px"><span>摊牌</span> 👍（6） 💬（1）<div>我有个疑惑，如果像部署redis, etcd等集群模式，比如3个pod, 对应的集群里应该会有个master，像这种有状态的服务，如果采用deployment模式部署会有影响吗，还是单独部署3个pod, 望大家指点</div>2022-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（4） 💬（1）<div>1. 设置为0，就是pod没了，deployment还有，看同学们回答是保留配置，这个不错。
2. 管理无状态服务，什么叫有状态，什么叫无状态，我不太理解。

另外，我刚刚突发奇想，deployment只留一个头加上select配置，然后里面的pod对象单独取出来，建立一个文件，pod可以建立，但是deloyment无法建立，但是提示我是语法错误，其实我不太理解。既然这两服务是独立了，我为啥不能这么做呢</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/4e/ed/a15897e3.jpg" width="30px"><span>mango</span> 👍（3） 💬（2）<div>这里开始人就少了，看来很多人倒在上一节安装那</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1b/f8/01e7fc0e.jpg" width="30px"><span>郑小鹿</span> 👍（3） 💬（3）<div>「 下属字段“matchLabels”定义了 Pod 对象应该携带的 label，它必须和“template”里 Pod 定义的“labels”完全相同 」

老师这个应该是指某个标签的内容完全一样吧。selector.matchLabels”是“template.matadata”中“labels”的子集。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3b/29/0f86235e.jpg" width="30px"><span>明月夜</span> 👍（2） 💬（1）<div>老师好，我有一些疑问：
1. 既然Deployment 只是帮助 Pod 对象能够有足够的副本数量运行，我尝试着在这个deployment之外，单独起一个pod，设置一样label，明面上pod数量增加了，不符合deployment里replicas的预期，多出来的pod应该被销毁才对，但实际并不是这样，这个独立的pod并没有影响到这个deployment，为什么？
2. 我看了service那一章，service里也是在selector字段下指明要代理的pod的标签，我也做了同样的试验，在deployment之外，单独起一个pod，设置一样的标签，service除了能代理deployment的pod外，这个独立的pod也能被代理，为什么会有这种不一致性？</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/ce/05/4c493ef9.jpg" width="30px"><span>李泽文</span> 👍（2） 💬（2）<div>老师，我还是不太理解Job和Deployment的区别，什么是在线业务，什么是离线业务？通过对Job和Deployment的对别，感觉都差不多。Job里可以通过配置实现pod的总数量，并发数量，这个跟Deployment的replicas有什么区别？在Job里我们可以配置pod运行失败的重启策略，这个跟Deployment的动态扩缩容又有什么区别？</div>2023-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（2） 💬（1）<div>deployment 提供的多实例，在对外提供服务的时候是只有一个应用，还是多个应用同时提供服务呢？ 它是支持负债均衡吗？ 如果是，那与service提供的负债均衡有什么区别？</div>2022-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（2）<div>请教老师两个问题：
Q1：有状态的应用怎么发布？
既然Deplayment是用来发布无状态的应用，那有状态的应用怎么发布？
k83不能发布有状态的应用吗？

Q2：怎么访问用Deployment创建的Nginx？
我用Deployment成功创建了两个nginx，一个IP是172.17.0.11,请问怎么访问该Nginx？（最好能给出具体的操作方法）。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（2） 💬（1）<div>第二个问题，如果是有状态应用不同Pod间互相访问，而deployment生成的pod最后带有不固定的哈希字符串，无法唯一确定某个pod，此时deploy不适用了。</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/15/c4866257.jpg" width="30px"><span>咩咩咩</span> 👍（2） 💬（1）<div>第一个问题：将replicas设置为0，对应应用的pod数量为0，应用停止服务。这样的方式保存了deployment，如果需要启动应用，将replicas设置为需要的数量即可
</div>2022-08-01</li><br/><li><img src="" width="30px"><span>Geek_e46db2</span> 👍（1） 💬（1）<div>一个node默认最多110个pod，如果机器资源有限情况下，比如创建了30个就占满了，k8s会自动限制node保证可用吗？</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b9/6f/b40d1acf.jpg" width="30px"><span>mkcaptain</span> 👍（1） 💬（2）<div>老师，问个问题
既然deployment和pod定义是松散的连接关系，也有用label指向了具体pod
那deployment的template部分能去掉么。也就是说deployment能只用label去管理已经运行的pod么？</div>2022-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/c3/775fe460.jpg" width="30px"><span>rubys_</span> 👍（1） 💬（1）<div>老师，我有一个疑问，就是能不能把 pod 理解为一个进程，如果我的应用在之前没有使用 k8s 部署的时候是启动了 100 个进程，现在换做 k8s 来部署的话，是不是要设置 replicas 为 100 才有 100 个进程来对外提供服务</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b9/4b/2376a469.jpg" width="30px"><span>DN</span> 👍（1） 💬（1）<div>想请教一下老师，在master通过 deployment部署的应用， kubectl exec -it nginx-deployment-85658cc69f-l68tx -- &#47;bin&#47;bash 报错connect: connection refused， 但其他的命令 apply describe等都正常，想问一下可能是什么原因，感谢感谢。</div>2022-08-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dotGbXAlAZg0bhCq4P96A40mdyavzR33jSqIHk8xLlic4B5PYNDIP5MEa1Fk9yxzdz9scHUM7IUNR71nVZNoV7Q/132" width="30px"><span>yhtyht308</span> 👍（1） 💬（1）<div>使用 kubectl get 命令通过参数l查找标签名，是对应pod的labels，不是name。可以通过“kubectl get pod --show-labels”来查找。
</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（0） 💬（1）<div>老师 问一下 k8s是不是不适合部署websocket之类的长链接服务 随着pod的自动销毁重建 长链接就丢失了</div>2024-03-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIoRAqV3Yic1wa2gKDq74h1SB5azIpZAOE2uY43CZevju1vd4wxibXq3Y6LJvxJ4tlsJEEmkI64ZJvw/132" width="30px"><span>余晓杰</span> 👍（0） 💬（1）<div>可以将某个节点拉出，不参与生产，然后用来定位问题吗</div>2023-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/d8/708a0932.jpg" width="30px"><span>李一</span> 👍（0） 💬（1）<div>感谢老师的精彩讲解，让k8s 知识体系，更加清晰和立体的展现出来。
回答一下老师的问题：
1. replicas 设置为0 
deployment会创建成功，带启动的POD数量和期望都是0，会保存服务配置(包括 pull 镜像、设置环境变量等等） 为后续快速上线做准备。
2. deployment的使用场景，是无状态的应用，每次deloy启动pod会在固定名称后面加入随机字符串，对于有状态的服务，需要使用k8s其他组件</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/14/b9/47377590.jpg" width="30px"><span>Jasper</span> 👍（0） 💬（3）<div>想问下，老师学习这些知识点是从哪里看的？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（0） 💬（1）<div>精彩</div>2022-08-01</li><br/><li><img src="" width="30px"><span>张仁（信息中心）</span> 👍（0） 💬（1）<div>快更快更</div>2022-08-01</li><br/>
</ul>