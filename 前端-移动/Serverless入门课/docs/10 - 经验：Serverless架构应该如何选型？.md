你好，我是秦粤。通过前面的两节实践课，我们体验了在本地环境中搭建K8s，并且我们利用K8s的组件扩展能力，在本地的K8s上安装了Istio和Knative。正如我在前面课程中所说的，K8s可以让我们的集群架构，轻松迁移到其他集群上，那么今天我就带你将我们本地K8上部署的“待办任务”Web服务部署到云上的K8s集群。

实践课里还有这么个小细节，不知道你注意没，我们使用Knative时，应用和微服务部署都需要关心项目应用中的Dockerfile，而我在使用FaaS函数时，连Dockerfile都不用管了，其实这就是Serverless带来的变革之一。当然，现在有很多应用托管PaaS平台，也做了Serverless化，让我们部署一个应用时只需要关心Release分支的代码合并，例如Heroku、SAE等等。

这里我需要先解释一下，K8s集群的运维工作对于很多个人开发者来说，是有些重的。我们通常了解基本知识，用kubectl调用K8s集群就可以了。咱们课程里，我是为了让你更好理解Serverless的工作原理，所以才向你介绍Knative在K8s上的搭建和使用过程。

实际工作中K8s集群的运维，还是应该交给专业的运维人员。另外，云服务商的K8s集群，都会提供控制面板，一键安装组件。我们在使用Serverless的部署应用时，不用关心底层“被透明化”的类似Knative、Istio等等插件能力，这也是Serverless应用的价值所在，虽然它本身的底层构建在复杂且精密的各种服务上，但我们使用Serverless却极其精简。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（5） 💬（1）<div>补交一下作业.
今天通过ASK的Knative部署了老师的这套服务.
给有需要的同学一个参考:

1. 创建Serverless Kubernetes时,推荐勾选上PrivateZone.
   我未勾选该选项,导致服务内无法通过`user.default.svc.cluster.local`互相访问
   后来我是kubectl exec -it xxx -- &#47;bin&#47;bash 进了pod,修改了`&#47;etc&#47;hosts`完成的配置.
2. 需要参考文章[Knative On ASK 给您带来极致的 Serverless 体验](https:&#47;&#47;yq.aliyun.com&#47;articles&#47;759756)
   创建好集群后,在钉钉群中联系客服,帮忙开通Knative功能.
   注: 部署成功后,会多出一个SLB,也会多出`knative-serving`命名空间.
       暂时还无法通过控制台的UI查看及操作Knative,只能通过命令行操作.
3. 微调调试的部署yaml文件.
   比如添加一个注解,便于在pod上申请一个公网IP.
      k8s.aliyun.com&#47;eci-with-eip: &quot;true&quot;
   由于我的k8s机器未创建NAT网关,默认的pod是无法访问公网,拉取镜像的.
   所有需要在每个pod上都申请一个公网IP.
      目前NAT网关是12元&#47;天,而一个公网IP才0.02元&#47;小时的配置费用
4. 查看服务的域名
      kubectl get ksvc
5. 配置域名解析
   需要解析到Knative的负载均衡SLB的公网IP上
6. 验证部署效果
</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（1）<div>感觉Knative还是太新了,目前还未出1.0版本.
不过有了它,确实是可以方便的基于k8s环境,搭建属于自己的serverless平台做定制化.

今天无意中看到一个IBM的免费视频讲堂,推荐给感兴趣的小伙伴.
[Kubernetes 原生无服务器开源项目 Knative](https:&#47;&#47;developer.ibm.com&#47;cn&#47;os-academy-knative&#47;)
</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>现在云厂商都会基于kata或者rust-vmm来实现“serverless”式的容器服务，请问您怎么看？另外厂商一般使用virtual-kubelet来管理serverless容器产品，例如腾讯EKS，为什么不用原生的kubelet结合containerd来进行管理呢？</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>资源的物理机虚拟化 是什么意思的？ 是一份资源虚拟出多份资源使用吗？</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（0）<div>阿里云 客服响应速度是一大亮点 ，这点我认同。哈哈，每次有问题提工单都能快速的响应</div>2020-05-12</li><br/>
</ul>