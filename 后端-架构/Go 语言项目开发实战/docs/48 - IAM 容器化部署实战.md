你好，我是孔令飞。

在 [45讲](https://time.geekbang.org/column/article/415606)中，我介绍了一种基于Kubernetes的云原生架构设计方案。在云原生架构中，我们是通过Docker + Kubernetes来部署云原生应用的。那么这一讲，我就手把手教你如何在Kubernetes集群中部署好IAM应用。因为步骤比较多，所以希望你能跟着我完成每一个操作步骤。相信在实操的过程中，你也会学到更多的知识。

## 准备工作

在部署IAM应用之前，我们需要做以下准备工作：

1. 开通腾讯云容器服务镜像仓库。
2. 安装并配置Docker。
3. 准备一个Kubernetes集群。

### 开通腾讯云容器服务镜像仓库

在Kubernetes集群中部署IAM应用，需要从镜像仓库下载指定的IAM镜像，所以首先需要有一个镜像仓库来托管IAM的镜像。我们可以选择将IAM镜像托管到[DockerHub](https://hub.docker.com/)上，这也是docker运行时默认获取镜像的地址。

但因为DockerHub服务部署在国外，国内访问速度很慢。所以，我建议将IAM镜像托管在国内的镜像仓库中。这里我们可以选择腾讯云提供的镜像仓库服务，访问地址为[容器镜像服务个人版](https://console.cloud.tencent.com/tke2/registry)。

如果你已经有腾讯云的镜像仓库，可以忽略腾讯云镜像仓库开通步骤。

在开通腾讯云镜像仓库之前，你需要[注册腾讯云账号](https://cloud.tencent.com/document/product/378/17985)，并完成[实名认证](https://cloud.tencent.com/document/product/378/3629)。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（1）<div>总结：
1. 开通容器服务镜像仓库，自己搭建的话可以使用 harbor
2. 安装并配置Docker，配置主要包括，docker 通过非 root 用户使用；配置 docker 开启启动；
3. 准备一个 Kubernetes 集群。可以参见 follow-me-install-kubernetes-cluster 教程</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/05/11/06ae74fa.jpg" width="30px"><span>Mr.凉</span> 👍（0） 💬（1）<div>老师您好，这块有点没懂，为什么执行make push 就会生成下面四个镜像？

$ make push REGISTRY_PREFIX=ccr.ccs.tencentyun.com&#47;marmotedu VERSION=v1.1.0

上述命令，会构建 iam-apiserver-amd64、iam-authz-server-amd64、iam-pump-amd64、iamctl-amd64 四个镜像


</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（0） 💬（1）<div>老师好！iam-apiserver使用到MySQL和cache，在k8s集群中部署以上4个应用，iam-apiserver的Pod连不上MySQL，应用拉不起来。</div>2021-09-26</li><br/>
</ul>