你好，我是孔令飞。

前面两讲，我们一起看了云技术的演进之路。软件架构已经进入了云原生时代，云原生架构是当下最流行的软件部署架构。那么这一讲，我就和你聊聊什么是云原生，以及如何设计一种基于Kubernetes的云原生部署架构。

## 云原生简介

云原生包含的概念很多，对于一个应用开发者来说，主要关注点是如何开发应用，以及如何部署应用。所以，这里我在介绍云原生架构的时候，会主要介绍应用层的云原生架构设计和系统资源层的云原生架构设计。

在设计云原生架构时，应用生命周期管理层的云原生技术，我们主要侧重在使用层面，所以这里我就不详细介绍应用生命周期管理层的云原生架构了。后面的云原生架构鸟瞰图中会提到它，你可以看看。

另外，在介绍云原生时，也总是绕不开云原生计算基金会。接下来，我们就先来简单了解下CNCF基金会。

### CNCF（云原生计算基金会）简介

[CNCF](https://www.cncf.io/)（Cloud Native Computing Foundation，云原生计算基金会），2015年由谷歌牵头成立，目前已有一百多个企业与机构作为成员，包括亚马逊、微软、思科、红帽等巨头。CNCF致力于培育和维护一个厂商中立的开源社区生态，用以推广云原生技术。

CNCF目前托管了非常多的开源项目，其中有很多我们耳熟能详的项目，例如 Kubernetes、Prometheus、Envoy、Istio、etcd等。更多的项目，你可以参考CNCF公布的[Cloud Native Landscape](https://landscape.cncf.io/images/landscape.png)，它给出了云原生生态的参考体系，如下图所示：
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（2） 💬（1）<div>我觉得公用云版的云原生架构设计图还是按照传统的IAAS，PAAS，SAAS分层比较清晰。CAAS（Container As A Service）到底在哪个位置是一个问题。</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/54/7b/780c04ff.jpg" width="30px"><span>史努比</span> 👍（1） 💬（1）<div>&quot;当 Pod 健康检查失败时，Deployment&#47;StatefulSet 的控制器（ReplicaSet）会自动销毁故障 Pod&quot;这里感觉有点问题。Deployment没有问题，Statefulset理解应该是直接管理Pod的，没有借助Replicaset。</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4e/bf/0f0754aa.jpg" width="30px"><span>lianyz</span> 👍（1） 💬（2）<div>老师，服务网格一定要依赖k8s吗？</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/e4/81ee2d8f.jpg" width="30px"><span>Wisdom</span> 👍（0） 💬（1）<div>老师，基于k8s+istio，还需要另外的服务中心？感觉不需要了，本身已经具备了服务发现能力了</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（1） 💬（0）<div>我认为这篇是个运维都该看看</div>2023-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/88/454e401c.jpg" width="30px"><span>销毁first</span> 👍（0） 💬（0）<div>完整的云原生技术栈介绍，赞</div>2021-11-05</li><br/>
</ul>