你好，我是秦粤。上节课我们只是用Docker部署了index.js，如果我们将所有拆解出来的微服务都用Docker独立部署，我们就要同时管理多个Docker容器，也就是Docker集群。如果是更复杂一些的业务，可能需要同时管理几十甚至上百个微服务，显然我们手动维护Docker集群的效率就太低了。而容器即服务CaaS，恰好也需要集群的管理工具。我们也知道FaaS的底层就是CaaS，那CaaS又是如何管理这么多函数实例的呢？怎么做才能提升效率？

我想你应该听过Kubernetes，它也叫K8s（后面统一简称K8s），用于自动部署、扩展和管理容器化应用程序的开源系统，是Docker集群的管理工具。为了解决上述问题，其实我们就可以考虑使用它。K8s的好处就在于，它具备跨环境统一部署的能力。

这节课，我们就试着在本地环境中搭建K8s来管理我们的Docker集群。但正常情况下，这个场景需要几台机器才能完成，而通过Docker，我们还是可以用一台机器就可以在本地搭建一个低配版的K8s。

下节课，我们还会在今天内容的基础上，用K8s的CaaS方式实现一套Serverless环境。通过这两节课的内容，你就可以完整地搭建出属于自己的Serverless了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（0） 💬（1）<div>请教老师一个部署的问题：与后端代码交互，前端代码在k8s体系下怎么部署才是最佳实践。

参考官网上的例子（https:&#47;&#47;kubernetes.io&#47;zh&#47;docs&#47;tasks&#47;access-application-cluster&#47;connecting-frontend-backend&#47;），我理解是将前端代码放在nginx里面，同时在nginx.conf中配置后台api的反向代理（我的理解是解决跨域问题），然后将其部署为一个pod，并暴露出该前端工程的service ip 和 nodePort。

1）如果这里不直接暴露前端服务ip和nodePort，而走ingress，是否有必要，个人觉得没必要，因为多绕了一层。
2）nginx.conf中给后台服务配置的反向代理，是配置后台应用程序对应 service 的 ingress 地址，还是直接配置后台应用程序对应 service 的内部 ip 和端口 （或直接就是 service name) 。
  2.1）如果配置的是对应 service 的 ingress 地址，那又多绕了一层。但又想到两个点，一是前端代码如果某一天单独拎出去部署，而不是在k8s中，不受影响（可能是伪需求）；二是通过nginx-ingress-controller，Prometheus可以拿到相关api调用的监控指标（请求延迟，请求量等，但也只能获得 ingress 中对应配置的 path 数据，https:&#47;&#47;github.com&#47;kubernetes&#47;ingress-nginx&#47;pull&#47;2701）。
  2.2）如果配置的是对应service 内部 ip 和端口，提高了速度，但为了获取监控指标，也要部署一套 nginx exporter。

我们的部署方案是否欠妥（前端代码这么部署是最佳实践吗？nginx 反向代理配置呢？获取服务请求相关监控指标的方式是正确的吗？）想听听老师的想法，您所在的团队是如何做的，谢谢。（如果不是好问题，还请老师见谅，我对部署这一块做的不多，不是很熟悉。)</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/15/65/37d05463.jpg" width="30px"><span>pop</span> 👍（0） 💬（2）<div>老师我在阿里云上的centos7机器上实践，很多镜像拉取不下来。例如myapp.yaml里面的registry.cn-shanghai.aliyuncs.com&#47;jike-serverless&#47;todolist:latest是找不到的；我配置了阿里云的镜像加速，但是还是会去dockerhub中去搜索镜像。请教如何正确的拉取镜像，包括下一章的istio也是同样的问题。</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/15/8db238ac.jpg" width="30px"><span>神仙朱</span> 👍（0） 💬（1）<div>文中疑问：又因为 kubectl 是通过加密通信的，所以我们可以在一台电脑上同时控制多个 K8s 集群

这两者为什么是因果关系没太懂，不是加密通信就不能控制多个集群吗，反正都是指定上下文</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/62/24/07e2507c.jpg" width="30px"><span>托尼斯威特</span> 👍（0） 💬（1）<div>docker桌面版在preference中enable Kubernetes会自动下载repos.
docker-k8s-prefetch.sh是用来提前从阿里云的repo下载这些repo,再改名到google的repo的名字. 
但是我发现, 我启动docker带的Kubernetes时, 还是会下载一套新版的repos.</div>2020-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>云厂商serverless的最小管理调度粒度是不是就等于k8s的pod？</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/2e/0326eefc.jpg" width="30px"><span>Larry</span> 👍（0） 💬（1）<div>一个函数实例对应一个CaaS，还是多个函数实例对应一个CaaS？</div>2020-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIrg3ZKwyfUSoWDdB4mdmEOCeicfWO5WJXvNwDJsy6QV18gwQ5rlUg9MmYGIjCWU6QqQIZnXXGonIw/132" width="30px"><span>miser</span> 👍（0） 💬（1）<div>好奇怪 为什么 deployment.apps&#47;myapp READY 是0&#47;1

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps&#47;load-generator   1&#47;1     1            1           12h
deployment.apps&#47;myapp            0&#47;1     1            0           2m59s</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/15/5278f52a.jpg" width="30px"><span>春暖花开</span> 👍（0） 💬（1）<div>有个问题没有明白：我们在serverless平台下写的函数是怎么被调用的，
通常java的springboot或者spingcloud应用，会以jar
的方式启动后，监听端口，http请求数据最终会发送到监听端口，
然后一些列的解析处理，通过controller层最终到我们的业务逻辑。

但是serverless是个怎么处理方式，数据是怎么就到我们的处理函数呢？
是serverless平台怎么包装这个函数？这个一直没有明白。</div>2020-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（3）<div>在 K8s 中 容器不是部署在 Node  节点上吗？ 怎么文中部署在了Master 节点了？ Master 节点也可以充当 Node节点吗？</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（6）<div>由于我有现成的k8s环境,所以就不用重新搭建,可以直接使用了.

最近两天在折腾阿里云的弹性容器实例(ECI).
想不到这东西还能使用抢占式实例（Spot）的模式,2CPU-2G的实例,不到0.05元每小时的价格.
跑一些临时的任务还是很好的.
就是这里的还不太完善,不像竞价实例那样,有具体的规格和历史的参考价格.

另外Kubernetes还可以与ECI对接,不管是阿里云的k8s集群,还是Serverless Kubernetes,还是自建的k8s集群,
都可以使用Virtual Kubelet来创建虚拟k8s工作节点,加入到k8s集群中.
虚拟节点本身不要钱,只是调度到上面的pod需要申请ECI实例,才需要按秒付费.
我只是在阿里云的k8s上尝试了一下,想折腾的小伙伴可以用它来扩展本地机器上创建的k8s集群.

相比自建的k8s工作节点,ECI实例就不太灵活.
一个ECI实例好像对应一个pod,ECI实例的最小规格是0.25CPU和512MB内存.
对小应用来说,还是蛮浪费的.
在我们的开发环境中,一个4CPU8G的工作节点,都是跑60+个pod的.

之前发现在ECI上拉镜像超级超级慢.
今天又尝试了下ECI的镜像缓存功能.
这个功能估计目前还不完善,反正我是遇到了缓存的镜像未生效的问题,已提交工单咨询了.
话说这个功能有点费钱.
1.制作镜像缓存需要用到ECI.
2.保存镜像需要用到云盘快照.
3.使用镜像还会自动创建一个云盘,额外挂载到ECI上.(与ECI同生命周期)
用的磁盘还都是较好的ESSD,还都是20GB起步,单个镜像缓存最多支持包含20个镜像.

还不如把镜像同步到阿里云的镜像仓库中,再走私网拉取镜像.

</div>2020-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/15/5278f52a.jpg" width="30px"><span>春暖花开</span> 👍（0） 💬（0）<div>我们在serverless平台下写的函数是怎么被调用的，
通常java的springboot或者spingcloud应用，会以jar
的方式启动后，监听端口，http请求数据最终会发送到监听端口，
然后一些列的解析处理，通过controller层最终到我们的业务逻辑。

但是serverless是个怎么处理方式，数据是怎么就到我们的处理函数呢？
是serverless平台怎么包装这个函数？这个一直没有明白。</div>2020-05-06</li><br/>
</ul>