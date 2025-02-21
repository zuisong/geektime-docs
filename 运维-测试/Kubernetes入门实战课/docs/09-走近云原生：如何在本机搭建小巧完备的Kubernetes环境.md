你好，我是Chrono。

在前面的“入门篇”里，我们学习了以Docker为代表的容器技术，做好了充分的准备，那么今天我们就来看看什么是容器编排、什么是Kubernetes，还有应该怎么在自己的电脑上搭建出一个小巧完善的Kubernetes环境，一起走近云原生。

## 什么是容器编排

容器技术的核心概念是容器、镜像、仓库，使用这三大基本要素我们就可以轻松地完成应用的打包、分发工作，实现“一次开发，到处运行”的梦想。

不过，当我们熟练地掌握了容器技术，信心满满地要在服务器集群里大规模实施的时候，却会发现容器技术的创新只是解决了运维部署工作中一个很小的问题。现实生产环境的复杂程度实在是太高了，除了最基本的安装，还会有各式各样的需求，比如服务发现、负载均衡、状态监控、健康检查、扩容缩容、应用迁移、高可用等等。

![图片](https://static001.geekbang.org/resource/image/47/da/4790335b7fdd6a29d2cdda3yy3e337da.png?wh=900x551 "图片来自网络")

虽然容器技术开启了云原生时代，但它也只走出了一小步，再继续前进就无能为力了，因为这已经不再是隔离一两个进程的普通问题，而是要隔离数不清的进程，还有它们之间互相通信、互相协作的超级问题，困难程度可以说是指数级别的上升。

这些容器之上的管理、调度工作，就是这些年最流行的词汇：“**容器编排**”（Container Orchestration）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/23/bb/74/edc07099.jpg" width="30px"><span>柳成荫</span> 👍（69） 💬（2）<div>镜像拉取成功，遇到了几个坑
1. docker版本过低，docker升级到20.10.1以上
2. 不能用root账号，加上--force
3. 镜像拉取不下来，切换到国内镜像，先执行 minikube delete
再执行 minikube start --image-mirror-country=&#39;cn&#39;</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（56） 💬（4）<div>1.1、如何理解容器编排？
先拆成两个部分，什么是容器？什么是编排？以前，程序运行在物理机或虚拟机中。容器，是现代程序的运行方式。编排就是部署、管理应用程序的系统，能动态地响应变化，例如以下部分功能。
 - 回滚
 - 滚动升级
 - 故障自愈
 - 自动扩缩容
自动完成以上所有任务。需要人工最初进行一些配置，就可以一劳永逸。回顾一下，什么是容器编排，运行容器形式的应用程序，这些应用程序的构建方式，使它们能够实现回滚、滚动升级、故障自愈、自动扩缩容等。

1.2、如何理解 Kubernetes？
举一个例子，寄、收快递的过程。发件人将货物按照快递公司的标准打包，提供基本信息（收货地址等），然后交给快递小哥。其他事情，无需发件人操心了，例如快递用什么交通工具运输、司机走哪条高速等等。快递公司同时提供物流查询、截断快递等服务。重点在于，快递公司仅需要发件人提供基本信息。Kubernetes 也是类似的，将应用程序打包成容器，声明运行方式，交给 Kubernetes 即可，同时它提供了丰富的工具和 API 来控制、观测运行在平台之上的应用程序。

1.3 容器编排应该能够解决什么问题？
屏蔽底层的复杂性。

2、Kubernetes 和 Docker 之间有什么区别？
Docker 应用打包、测试、交付。Kubernetes 基于 Docker 的产物，进行编排、运行。例如现在有 1 个集群，3 个节点。这些节点，都以 Docker 作为容器运行时，Docker 是更偏向底层的技术。Kubernetes 更偏向上层的技术 ，它实现了对容器运行时的抽象，抽象的目的是兼容底层容器运行时（容器进行时技术不仅有 Docker，还有 containerd、kata 等，无论哪种容器运行时，Kubernetes 层面的操作都是一样的）以及解耦，同时还提供了一套容器运行时的标准。抽象的产物是容器运行时接口 CRI。

说的不对的地方请斧正 : - )
</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（18） 💬（4）<div>记录一下我遇到的坑，和评论里面解决方案:
1. 不能用root账号，使用普通用户加上--force
2. 镜像拉取不下来，切换到国内镜像，先执行 minikube delete
再执行 minikube start --image-mirror-country=&#39;cn&#39;  --kubernetes-version=v1.23.3
3.  安装一直停留在这里    
  - Booting up control plane ...| 调整虚拟机配置，调到4c8g。
4. 我自己之前的一个配置错误，将minikube 生成的kubectl 加入到了path中。</div>2022-07-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIERY97h7dmXbtur6rhZWA9Jb3TtSsJh7icDdFjdLmruTXC22qibOVTmW2a04TxMhxqtNJibYL1iaU7yQ/132" width="30px"><span>Geek_8ac303</span> 👍（16） 💬（1）<div>1、运行容器：kubectl run ngx --image=nginx:alpine
2、查看pod：kubectl get pods -o wide
NAME   READY   STATUS  
ngx    0&#47;1     ContainerCreating
3、结果：拉取镜像拉不下来，一直卡在那，但是用docker pull 单独拉去镜像是没问题的，鼓捣了两三个小时，后来发现了一个参数可以解决这个问题，--registry-mirror=https:&#47;&#47;twm4fpgj.mirror.aliyuncs.com 这部分是指定docker的镜像加速地址（我是用的阿里的地址，每个人的应该是不一样的），原来通过kubectl调用的docker的配置并不是&#47;etc&#47;docker&#47;daemon.json 里面的配置
4、重新安装：
minikube stop
minikube delete --all
minikube start --kubernetes-version=v1.23.9 --image-mirror-country=&#39;cn&#39; --registry-mirror=https:&#47;&#47;twm4fpgj.mirror.aliyuncs.com</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/92/4b/1262f052.jpg" width="30px"><span>许飞</span> 👍（15） 💬（2）<div>minikube start --kubernetes-version=v1.23.3 --image-mirror-country=&#39;cn&#39; --force
</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3a/ae/13976fd2.jpg" width="30px"><span>孙中伟</span> 👍（14） 💬（3）<div>minikube start  --image-mirror-country=&#39;cn&#39; --image-repository=&#39;registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#39; --base-image=&#39;registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#47;kicbase:v0.0.28&#39; --kubernetes-version=v1.23.3

使用上述命令，终于start成功</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（13） 💬（1）<div>尝试回答一下这两个问题：docker和k8s之间的区别，一个是容器技术，一个是容器编排技术，两者思考的维度是不一样的，就容器而言，容器解决的问题是隔离，是一次打包到处运行的问题，最大的价值就在于镜像的迁移。编排技术则是关注的是整个系统的问题，如果你只关注一个服务，迁移一个服务，那docker就够，但要迁移整个系统以及运维，那就需要编排，包括网络关系，负载均衡，回滚，监控，扩缩容问题则需要容器编排技术。
</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（11） 💬（3）<div>碰到一坑 minikube start 无法启动 群友建议minikube delete --all --purge 解决</div>2022-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/1f/90/bf183d37.jpg" width="30px"><span>DmonJ</span> 👍（10） 💬（1）<div>当前最新的minikube是1.26.1, 文章中的是1.25.2, 可以使用指定下载版本的方式确保安装的版本与文章中的一致:
`
curl -LO https:&#47;&#47;github.com&#47;kubernetes&#47;minikube&#47;releases&#47;download&#47;v1.25.2&#47;minikube-linux-amd64
sudo install minikube-linux-amd64 &#47;usr&#47;local&#47;bin&#47;minikube
`
全部版本链接:`https:&#47;&#47;github.com&#47;kubernetes&#47;minikube&#47;releases`</div>2022-08-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（7） 💬（1）<div>kubeadmin和minikube有什么区别，用哪个如何选择</div>2022-07-11</li><br/><li><img src="" width="30px"><span>Geek_b4e756</span> 👍（6） 💬（2）<div>把前人踩过的坑重新踩了一遍，加深各参数的印象，
docker version :24.0.5
minikube v1.31.0
root 用户终启动成功的最终指令是：
minikube start  --image-mirror-country=&#39;cn&#39; --image-repository=&#39;registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#39; --base-image=&#39;registry.cn-hangzhou.aliyuncs.com&#47;google_containers&#47;kicbase:v0.0.28&#39; --kubernetes-version=v1.23.3 --force</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（5） 💬（2）<div>老师，我说出本课比较影响体验的一个地方吧：

现在大家安装的minikube的版本都是：v1.26.0。（这个版本是6月22号发布的）大家七月份学习这个课程的话。

Release Notes 是这样说的：

Note: Using a minikube cluster created before 1.26.0, using the docker container-runtime (default), and plan to upgrade the Kubernetes version to v1.24+? After upgrading, you may need to delete &amp; recreate it. none driver users, cri-docker is now required to be installed, install instructions. See issue #14410 for more info.

Kubernetes version to v1.24+ 以上的版本是一个分水岭，老师应该讲v1.24+ 的版本会比较好一些吧？

不然按照课程中的方式，大家都只能安装v1.23.3，不知道怎么解决高版本Kubernetes的问题。</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/c4/2b/b3f917ec.jpg" width="30px"><span>一颗红心</span> 👍（5） 💬（1）<div>直接使用官方的最新版，总是失败。
指定版本后可以正常启动😅</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（5） 💬（4）<div>`Google 又联合 Linux 基金会成了 CNCF`，应该修改为`Google 又联合 Linux 基金会成立了 CNCF`</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（5） 💬（1）<div>按照老师的教程，集群成功拉起。
就是拉取镜像时要耐心一点
</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（4） 💬（2）<div>docker：23.0.1
minikube：1.29.0
kubectl：1.26.1

使用最新版k8s需要执行如下命令：
minikube start --driver=docker --container-runtime=containerd</div>2023-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（4） 💬（2）<div>老师你好，有几个小问题：
1. Hadoop是借鉴那几篇论文的内容吗？然后迅速占领了市场。
2. 文章中的“kubelet”服务是做什么的呀？
3. “minikube，运行镜像也不过 1GB”。 这里的运行镜像是什么？ 是我们之前学习的 image文件吗？
4. source &lt;(kubectl completion bash)  没看懂这个命令后面的部分，能大致说一下么？
5. 浏览器输入gcr.io 会跳转到 https:&#47;&#47;cloud.google.com&#47;container-registry&#47; 这个网站，是正确的吗？
6. minikube ssh   前面的“minikube”是 节点的名称，对吧？
</div>2022-07-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/P5EIPG3R01kEcsSSm0UZlyysg3qak8qWQXlwKKIoCkdxKtyorxD6h4S7bVvNNBM9icynCGvZO0bA5jGNgy3oBiag/132" width="30px"><span>Geek_7e25fd</span> 👍（4） 💬（2）<div>老师，如何解决镜像拉取的过程当中，速度过慢或者无法下载的问题呢？能加餐镜像加速的知识？</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/45/27/4fbf8f6a.jpg" width="30px"><span>luke Y</span> 👍（3） 💬（1）<div>哈哈哈 wsl2(Ubuntu-20.04) 按照老师教的安装成功，不想虚拟机的可以试试😂  不过不管虚拟机还是别的方式别忘了备份</div>2022-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（3） 💬（1）<div>思考题：

1. 容器编排的目的是使容器的管理更加的工程化，解决一些因为容器规模上升所带来的潜在问题，比如容器间通信，容器的负载均衡，等等。Kubernetes 就是让容器编排的最佳实践得以落地的一个有力工具

2. docker 技术目的是提供创建容器以及容器镜像方法，聚焦的点是容器技术本身。而 K8S 技术目的是解决由于容器规模增大而带来的各种工程化问题，它以容器技术为基础，但是聚焦的点不再是容器技术了，而是上层的系统架构等问题

老师，source &lt; (kubectl completion bash) 这条命令貌似在 bash 中有语法错误，好像是 &lt; 后面多了个空格，应该是 source &lt;(kubectl completion bash) ？

另外，minikube 默认是从 gcr.io 抓取镜像，如果 gcr.io 无法访问的话就换成 DockerHub 吗？</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/52/40/db9b0eb2.jpg" width="30px"><span>自由</span> 👍（3） 💬（1）<div>执行 minikube start --kubernetes-version=v1.23.3 至少需要虚拟机分配了 2 个 cpu。关闭虚拟机，然后在 virtualBox 中选中当前虚拟机，右键，进入设置，单击系统，单击处理器，调整处理器数量。</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（3） 💬（1）<div>更新的够早的</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/f8/bc5faaec.jpg" width="30px"><span>Panda</span> 👍（2） 💬（1）<div>1. 容器编排是一种自动化管理容器化应用程序的方法， 在容器编排中， 多个容器被组织和协调以形成一个应用程序的整体。 它涉及到容器的创建、部署、连接、配置、伸缩和管理等方面的任务。 主要是目的是为了简化容器化应用程序的部署和管理过程， 提高应用程序的可靠性、可扩展性和弹性。 它可以自动化处理复杂的任务， 如容器的调度、负载均衡、服务发现、故障恢复等， 以确保应用程序始终处于所需的状态。 

2.  kubernetes  是容器编排的工具， kubernetes 是政府，docker就是人民。 政府治理人民。 kubernetes 治理docker 。 负责集群（可以运行容器的集群） 管理， 自动化部署、资源调度和负载均衡， 服务发现和连接， 伸缩和弹性、故障恢复和自愈性。 
</div>2023-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6e/8c/af652cee.jpg" width="30px"><span>tiger</span> 👍（2） 💬（1）<div>一个小问题，老师提到的补全代码命令：source &lt; (kubectl completion bash)，重定向符&lt;后面要去除空格，否则会语法报错。</div>2022-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（1） 💬（1）<div>是否可以理解为 , 将docker 应用, 从操作系统上, 迁移到kubernetes上, 由其统一管理,和维护?</div>2023-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/0c/370626c4.jpg" width="30px"><span>IT_matters</span> 👍（1） 💬（1）<div>建议大家和作者保持minikube版本一致，最新版本下载不到对应的kicbase镜像，会有点麻烦，指定安装版本用这个
curl -Lo minikube https:&#47;&#47;storage.googleapis.com&#47;minikube&#47;releases&#47;v1.25.2&#47;minikube-linux-amd64</div>2023-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/56/8d1444d5.jpg" width="30px"><span>W33D</span> 👍（1） 💬（1）<div>创建 Kubernetes 实验环境(非root用户，否则使用--force)：
sudo minikube start --driver=none --kubernetes-version=v1.23.9 --image-mirror-country=&#39;cn&#39; --registry-mirror=https:&#47;&#47;XXXXX.mirror.aliyuncs.com
minikube安装集群时，提示：If you are running minikube within a VM, consider using --driver=none:这个提示意味着你正在运行Minikube的虚拟机中，建议使用&quot;none&quot;驱动程序来避免在虚拟机中再次运行虚拟化。
</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（1） 💬（1）<div>问题2: 你认为 Kubernetes 和 Docker 之间有什么区别？
答: Docker作为一个容器实现方案, 解决的是应用的打包和分发, 进程的隔离等问题; kubernetes解决的是容器的编排.
前者面向容器化的应用解决问题;后者面向容器的管理解决问题.</div>2023-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（1） 💬（1）<div>回答问题1: 你是怎么理解容器编排和 Kubernetes 的？它们应该能够解决什么问题？
答: 容器编排解决的是多个容器应用之间的协同问题, 例子如入门篇中WordPress应用需要三个容器协同工作; kubernetes是容器编排的一个实现工具, 另外还解决了除此之外的自动化缩容扩容, 服务发现, 负载均衡, 实现了自动部署、扩展和管理容器化应用程序.</div>2023-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/33/acacb6ac.jpg" width="30px"><span>砖用冰西瓜</span> 👍（1） 💬（1）<div>请问跟 K8S 一块发的那篇论文是“Borg, Omega, and Kubernetes”这篇吗？</div>2023-03-28</li><br/>
</ul>