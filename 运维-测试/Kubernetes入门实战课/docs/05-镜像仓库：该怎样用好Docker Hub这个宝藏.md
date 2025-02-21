你好，我是Chrono。

上一次课里我们学习了“Dockerfile”和“docker build”的用法，知道了如何创建自己的镜像。那么镜像文件应该如何管理呢，具体来说，应该如何存储、检索、分发、共享镜像呢？不解决这些问题，我们的容器化应用还是无法顺利地实施。

今天，我就来谈一下这个话题，聊聊什么是镜像仓库，还有该怎么用好镜像仓库。

## 什么是镜像仓库（Registry）

之前我们已经用过 `docker pull` 命令拉取镜像，也说过有一个“镜像仓库”（Registry）的概念，那到底什么是镜像仓库呢？

还是来看Docker的官方架构图（它真的非常重要）：

![图片](https://static001.geekbang.org/resource/image/c8/fe/c8116066bdbf295a7c9fc25b87755dfe.jpg?wh=1920x1048)

图里右边的区域就是镜像仓库，术语叫Registry，直译就是“注册中心”，意思是所有镜像的Repository都在这里登记保管，就像是一个巨大的档案馆。

然后我们再来看左边的“docker pull”，虚线显示了它的工作流程，先到“Docker daemon”，再到Registry，只有当Registry里存有镜像才能真正把它下载到本地。

当然了，拉取镜像只是镜像仓库最基本的一个功能，它还会提供更多的功能，比如上传、查询、删除等等，是一个全面的镜像管理服务站点。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（13） 💬（5）<div>老师您好，在文中提到的arm架构和x86架构支持，请问一下，能否使用dockerfile创建同时支持两种服务的镜像呢。</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/e1/f663213e.jpg" width="30px"><span>拾掇拾掇</span> 👍（9） 💬（1）<div>1.我猜是把自己的工具打包进去或者官方镜像满足不了他们自己的需求
2.github 和docker hub都是仓库，不过一个是代码仓库，一个是容器仓库，面向的都是程序员或者是计算机爱好者，都提供了存储和分发功能</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（8） 💬（1）<div>请问老师：

docker官网的内容我感觉很多，如何找到重点快速学习呢？</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（5） 💬（3）<div>老师，很期待后面的自建镜像仓库啊 </div>2022-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（4） 💬（1）<div>思考题：
1. 感觉还是为了方便用户，就拿 ubuntu 举例，官方的基本上就是一个空操作系统，而商业公司就会在其中配置一些环境或安装一些跟公司相关的应用，用户 pull 下来直接使用即可无需从头配置

2. 一个主要是为了管理代码，一个主要为了管理容器。代码仓库主要是面向开发人员，让开发人员能够更好更方便地提出问题、审查代码、流程版本控制等等。而容器仓库主要是面向运维人员，这里面相比代码仓库少了很多的环节，毕竟面对的是一个直接 pull 下来就可以使用的应用，不需要过多的审核和提示等等。个人感觉还是 GitHub 的影响范围更大吧，毕竟所有的应用归根结底都是程序，而并不是所有的程序都需要打包成镜像

最后想请教老师，能否指定镜像仓库而不是从默认的 dockerHub 上面抓取镜像？是使用 `docker pull --platform` 指令吗？有名的镜像仓库有哪些？</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（4）<div>老师的专栏很不错，不过看到的比较晚。知道以后就抓紧赶，终于同步了。
前面几篇的学习中，积累了如下几个问题：
Q1：04篇中，如果run命令有多行，即包含多个“\”以及多个“&amp;&amp;”，那么，最后是生成一个layer还是多个layer？（文中有一句“每个指令都会生成一个 Layer”）。
Q2：04篇的问题：基于某个系统创建的镜像，可以运行在其他系统上吗？比如，基于ubuntu18创建的镜像，可以运行在centos等系统上吗？
Q3：05篇的问题：除了docker Hub以及国外的其他几个仓库外，国内有docker仓库吗？
Q4：“课前准备”篇中，提到了VMWare Fusion。 我用的虚拟机是VMWare workstation16，这个可以吗？</div>2022-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/07/7804f4cc.jpg" width="30px"><span>逗逼师父</span> 👍（3） 💬（2）<div>1. 其他公司有自己的环境配置需求，还可以顺便刷存在感。
2. Github是代码托管，侧重服务软件的开发阶段，范围主要是使用开源软件的开发者；DockerHub是托管镜像，侧重服务软件的部署，使用阶段，范围主要是运维工作者。</div>2022-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（2） 💬（1）<div>国内Docker镜像仓库一般都是配置阿里云的吧，老师应该提一下，否则拉取镜像太慢了。</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/ba/3a348f2d.jpg" width="30px"><span>YueShi</span> 👍（1） 💬（2）<div>Docker继承git和github的好多优秀的概念，pull&#47;push&#47;commit&#47;tag&#47;。。。。

想问一下老师，在编程中经常会有一些循环依赖的问题，想请问一下，会不会Dockerfile中也有，例如 A from B， B from C， C from A，这种问题存在吗？

假想一下，alpine的镜像被投毒了，是不是整个docker image镜像世界崩塌了一半？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/1e/4a93ebb5.jpg" width="30px"><span>Aaron Liu</span> 👍（0） 💬（1）<div>自己搭建一个私有的Registry，一般用docker registry还是harbor？目的是简单易用易维护，公司内部有jfrog artifactory，但申请流程&#47;权限都比较复杂，只是项目组维护自己用到的镜像，自己搭建一个比较自由</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（2）<div>https:&#47;&#47;hub.docker.com&#47; 这个地址国内访问不了啊</div>2024-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>
如何上传镜像到hub仓库? 

1、在 docker hub 上注册用户 
2、在本机使用 docker login 命令登陆
	
	docker login -u username

	会提示输入密码: 直接输入密码, 

3、适用docker tag 命令, 对本地构建出来的镜像要命名 
	
	命名规则: 用户名&#47;镜像名称:版本号

		如: username&#47;docker-build-demo:v1.0

	&#47;&#47;[...]内的可选-默认latest
    docker tag docker-build-demo username&#47;docker-build-demo[:v1.0] 

4、使用docker push 命令发布镜像道hub仓库
	
	docker push username&#47;docker-build-demo:v1.0</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/96/bb9f9848.jpg" width="30px"><span>王中阳</span> 👍（0） 💬（1）<div>2. 你能否对比一下 GitHub 和 Docker Hub，说说它们两个在功能、服务对象、影响范围等方面的异同点呢？
回答：GitHub和Docker Hub是两个不同的平台，它们在功能、服务对象、影响范围等方面存在一些异同点。
功能
GitHub是一个面向开发者的代码托管平台，提供了代码托管、版本控制、协作开发、问题跟踪、代码审查等一系列功能。而Docker Hub则是一个面向容器的镜像仓库，提供了Docker镜像的存储、分享、构建、管理等一系列功能。
服务对象
GitHub的服务对象主要是开发者和开源社区，提供了一个开放的平台，让开发者可以共享代码、协作开发、提高代码质量和效率。而Docker Hub的服务对象主要是容器开发者和运维人员，提供了一个方便的平台，让用户可以轻松地构建、存储、分享和管理Docker镜像。
影响范围
GitHub的影响范围较广，涉及到各个领域的开发者和开源社区，是一个全球性的平台。而Docker Hub的影响范围相对较窄，主要涉及到容器开发者和运维人员，是一个相对专业化的平台。
异同点
GitHub和Docker Hub在一些方面存在一些异同点。例如，GitHub和Docker Hub都提供了一些基本的免费服务，但是在一些高级功能和服务上，需要付费才能使用。此外，GitHub和Docker Hub都提供了一些API和插件，可以方便地与其他工具和平台进行集成和扩展。
总的来说，GitHub和Docker Hub是两个不同的平台，它们在功能、服务对象、影响范围等方面存在一些异同点。GitHub主要面向开发者和开源社区，提供了代码托管、版本控制、协作开发等一系列功能；而Docker Hub主要面向容器开发者和运维人员，提供了Docker镜像的存储、分享、构建、管理等一系列功能。虽然两个平台的服务对象和功能不同，但是它们都是开放的平台，可以方便地与其他工具和平台进行集成和扩展，为开发者和运维人员提供更加便捷和高效的服务。
此外，GitHub和Docker Hub在一些方面也存在一些相似之处。例如，它们都是基于云计算的平台，可以方便地进行远程协作和管理；它们都提供了一些基本的免费服务，但是在一些高级功能和服务上，需要付费才能使用；它们都提供了一些API和插件，可以方便地与其他工具和平台进行集成和扩展。
综上所述，GitHub和Docker Hub是两个不同的平台，它们在功能、服务对象、影响范围等方面存在一些异同点，但是它们都是开放的平台，可以为开发者和运维人员提供更加便捷和高效的服务。</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ce/96/bb9f9848.jpg" width="30px"><span>王中阳</span> 👍（0） 💬（1）<div>1. 很多应用（如 Nginx、Redis、Go）都已经有了 Docker 官方镜像，为什么其他公司（Bitnami、Rancher）还要重复劳动，发布自己打包的镜像呢？
回答：其他公司发布自己打包的镜像，一方面是为了满足不同用户的需求，另一方面是为了提供更加专业化和定制化的服务。
首先，Docker 官方镜像虽然提供了很多常用的应用镜像，但是并不能满足所有用户的需求。例如，一些用户可能需要特定版本的应用或者需要特定的配置和插件，这些需求可能无法通过官方镜像来满足。此时，其他公司发布自己打包的镜像，可以提供更加定制化的服务，满足用户的个性化需求。
其次，其他公司发布自己打包的镜像，也可以提供更加专业化的服务。这些公司可能有更加深入的了解和研究，可以提供更加优化和高效的镜像，从而提高用户的使用体验和效率。此外，这些公司还可以提供更加全面的支持和服务，包括安全性、可靠性、性能优化等方面的支持，从而帮助用户更好地使用和管理镜像。
综上所述，其他公司发布自己打包的镜像，可以提供更加定制化和专业化的服务，满足用户的个性化需求，提高用户的使用体验和效率，同时也可以提供更加全面的支持和服务。</div>2023-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/92/9f/d5255fe8.jpg" width="30px"><span>snake</span> 👍（0） 💬（1）<div>1. 加点私活或者官方镜像某些功能不满足特定的需求
2. GitHub可以上传自己或者公司的开源代码，Docker Hub只是docker的镜像管理，功能比GitHub少</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（2）<div>请教下老师，是不是可以这么理解：Registry 是镜像仓库的标准化定义，而 Docker Hub 是 Registry 的一种实现，其它容器厂商也可以实现自己的 Registry？</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（0） 💬（1）<div>docker官方镜像也有用户名，library, 一般省略！</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（1）<div>打卡</div>2022-07-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqw0R25Bt0iahFhEHfnxmzr9iaZf0eLsDQtFUJzgGkYwHTqicU9TydMngrJ4yL7D50awD2VibHBAdqplQ/132" width="30px"><span>Geek_18dfaf</span> 👍（0） 💬（2）<div>老师，请问下，如果我要选redis不同版本对应的镜像，该怎么查找？</div>2022-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（0） 💬（1）<div>上传镜像，是不是相当于git，会把我的各种服务，还有参数配置都上传上去？
那是不是可以直接当git用了？</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/1c/9dd631fd.jpg" width="30px"><span>小宇哥_程振宇</span> 👍（0） 💬（1）<div>老师您好，前面的内容已经读完了，希望快快更新呦，有点迫不及待了呢~</div>2022-07-03</li><br/>
</ul>