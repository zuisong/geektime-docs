你好，我是孔令飞。

我们将应用部署在Kubernetes时，可能需要创建多个服务。我就见过一个包含了40多个微服务的超大型应用，每个服务又包含了多个Kubernetes资源，比如 Service、Deployment、StatefulSet、ConfigMap等。相同的应用又要部署在不同的环境中，例如测试环境、预发环境、现网环境等，也就是说应用的配置也不同。

对于一个大型的应用，如果基于YAML文件一个一个地部署Kubernetes资源，是非常繁琐、低效的，而且这些YAML文件维护起来极其复杂，还容易出错。那么，有没有一种更加高效的方式？比如，像Docker镜像一样，将应用需要的Kubernetes资源文件全部打包在一起，通过这个包来整体部署和管理应用，从而降低应用部署和维护的复杂度。

答案是有。我们可以通过Helm Chart包来管理这些Kubernetes文件，并通过`helm`命令，基于Chart包来创建和管理应用。

接下来，我就来介绍下Helm的基础知识，并给你演示下如何基于Helm部署IAM应用。

## Helm基础知识介绍

Helm目前是Kubernetes服务编排事实上的标准。Helm提供了多种功能来支持Kubernetes的服务编排，例如 `helm` 命令行工具、Chart包、Chart仓库等。下面，我就来详细介绍下。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/59/b7/9db9c657.jpg" width="30px"><span>渊จุ๊บ</span> 👍（4） 💬（2）<div>思考题1，跟helm没太大关系，helm是帮助我们生成k8s的声明对象描述文件，服务启动安排在服务配置创建后，是属于k8s对象编排上，调整服务启动策略即可，比如dm对象的pod模板加init-container检查服务配置对象可读取后再开始后续container的启动，或者还可以使用动态准入webhook来控制服务对象的启动等，方法很多</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/f3/ed/46299341.jpg" width="30px"><span>打工人yyds</span> 👍（0） 💬（1）<div>根据helm get 所述，其作用应该是获取release的额外信息，但是在您最后的命令列表中写的是&quot;下载一个Release&quot;，是我理解错误还是手误？
```
$ helm get -h

This command consists of multiple subcommands which can be used to
get extended information about the release, including:

- The values used to generate the release
- The generated manifest file
- The notes provided by the chart of the release
- The hooks associated with the release

Usage:
  helm get [command]
# ... and many more
```</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>总结：
helm 作为Kubernetes的包管理工具，有三个概念：Chart、Repository、Release。
Chart：是一个 helm package，它是一个模板，包含了应用所需要的各种资源的定义。
Repository：存放 helm chart 的地方
Release: 每个 Chart 可以被部署多次，每次部署会创建一个对应的release。
Helm 关键的命令：helm repo list&#47;add, helm search, helm Install, helm upgrade 等</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/a6/e355f5cb.jpg" width="30px"><span>Wayne</span> 👍（0） 💬（0）<div>老师好，请问文章部署图中描述的【服务1】【服务2】指的是k8s资源这些吗（Deployment、Pod、Service）？</div>2023-07-15</li><br/>
</ul>