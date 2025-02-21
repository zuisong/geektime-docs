你好，我是秦粤。上节课我向你介绍了云原生基金会CNCF的重要成员K8s，它是用于自动部署、扩展和管理容器化应用程序的开源系统。通过实践，我们在本地搭建K8s，并将“待办任务”Web服务案例部署到了本地K8s上。K8s这门技术，我推荐你一定要学习下，不管是前端还是后端，因为从目前的发展趋势来看，这门技术必定会越来越重要。

今天这节课我们就继续学习如何搭建私有的Serverless环境。具体来说，我们会在上节课部署本地K8s的基础上，搭建Serverless底座，然后继续安装组件，扩展K8s的集群能力，最终让本地K8s集群支持Serverless。

## 搭建Serverless的前提

在开始之前，我们先得清楚一个问题，之前在基础篇讲Serverless Computing，也就是FaaS的时候，也有同学提问到，“微服务、Service Mesh和Serverless到底是什么关系？”

这些概念确实很高频地出现在我们的视野，不过你不要有压力，我在学习Serverless的时候也被这些概念所困扰。我们可以先回顾下微服务，我们在用微服务做BaaS化时，相信你也发现了微服务中有很多概念和Serverless的概念很接近。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（5） 💬（1）<div>折腾了一番,在老师的帮助下终于调通了.
在此给有需要的小伙伴一个参考:

1. 需要新建一个OTS表user
   主键:id 主键类型:INTEGER
   顺带,需要插入一条记录,比如:
   主键id: 1 属性列名称: users 属性列类型:字符串 属性值: &quot;&quot;
2. 文中的&#39;然后修改项目 k8s-myapp 目录中的 YAML 文件，改成你自己仓库中的 URI。&#39;
   可能是`knative-myapp`
   代码仓库中后来重命名为了 knative-myapp

----------------------------
之前在阿里云k8s上看到了&quot;应用目录&quot;&quot;服务网格&quot;选项,后来也逐步的尝试了helm,istio.
虽然之前也看到了&quot;Knative(公测)&quot;选项,但一直未尝试.
直到看了老师这篇文章,才知道原来是做这个的.正好这次把它用起来.

话说使用了这个后,k8s的节点负载就开始报警.
原来istio&#47;knative自身就有些系统的pod需要创建,额外每个服务还会多2个sidecar.
导致以下集群中就多了很多pod.
看来老师文中提到的4CPU8G内存还是有必要的.

目前来看,感觉Knative安装还是没有istio方便.
我是跟着另外一个专栏,在集群中安装的Istio 1.5.2版本.
想着阿里云上的Knative才0.11.0版本,而官方已经到了1.14.0版本.
本打算自己按着官方文档安装一番,结果很多镜像拉取不了.最后还是放弃了.
后来在安装阿里云自带的Knative时走了些弯路,花了不少时间.
主要是卸载Knative不干净,导致重装时怎么也装不成功,需要手动删除k8s上的一些资源才行.
</div>2020-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/65/c1/afcd981b.jpg" width="30px"><span>程序员二师兄</span> 👍（4） 💬（2）<div>了解到云原生，三驾马车：K8s、Service Mesh、Serverless。还有其他的知识点：lstio、docker、Knative</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1a/94/e4499114.jpg" width="30px"><span>小黑小小黑</span> 👍（1） 💬（1）<div>阿里的函数计算是基于knative来实现的吗?</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/26/63/5d099a2d.jpg" width="30px"><span>邵萍</span> 👍（0） 💬（1）<div>kiali控制台的用户名和密码是什么？登不进去呀</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>请问下作者生产环节当中的serverless架构有哪些实践可以优化faas的这个请求联路，因为经过虚拟化、容器、overlay好多层之后网络性能有很多损耗，现在有些企业尝试cilium+istio的方式来尽量减少过多的用户与内核态切换</div>2020-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>请问下为何不用istio和k8s hpa的原生功能来做服务发现、负载均衡、版本管理等实现呢？感觉knative有些多余啊</div>2020-07-01</li><br/>
</ul>