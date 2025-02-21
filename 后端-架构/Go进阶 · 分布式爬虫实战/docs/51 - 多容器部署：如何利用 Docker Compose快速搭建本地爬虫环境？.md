你好，我是郑建勋。

这节课，我们一起来学习如何使用 Docker Compose 来部署多个容器。

## 什么是 Docker Compose？

那什么是 Docker Compose 呢？

一句话解释，Docker Compose 一般用于开发环境，负责部署和管理多个容器。

现代的应用程序通常由众多微服务组成，就拿我们的爬虫服务来说，它包含了Master、Worker、etcd、MySQL，未来还可能包含前端服务、日志采集服务、鉴权服务等等。部署和管理许多像这样的微服务可能很困难，而 Docker Compose 就可以解决这一问题。

Docker Compose 并不是简单地将多个容器脚本和 Docker 命令排列在一起，它会让你在单个声明式配置文件（例如 docker-compose.yaml）中描述整个应用程序，并使用简单的命令进行部署。部署应用程序之后，你可以用一组简单的命令来管理应用程序的整个生命周期。

Docker Compose的前身是 Fig。Fig 由 Orchard 公司创建，它是管理多容器的最佳方式。Fig是一个位于 Docker 之上的 Python 工具，它可以让你在单个 YAML 文件中定义整个容器服务。然后，使用 fig 命令行工具就可以部署和管理应用程序的生命周期。Fig 通过读取 YAML 文件和 Docker API 来部署和管理应用程序。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（3） 💬（0）<div>思考题：
docker-compose down时，会自动删除原有容器以及虚拟网。但是其中定义的volumes会保留。

如果要down的同时清理干净，就直接加参数--volumes.

这样做是为了保护用户数据，下次启动容器可以直接用.</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a5/85/b1d9df7d.jpg" width="30px"><span>青鹿</span> 👍（0） 💬（0）<div>https:&#47;&#47;goproxy.cn不生效，可在Dockerfile里添加RUN go env -w GOPROXY=https:&#47;&#47;goproxy.cn这一行，做尝试</div>2023-10-10</li><br/>
</ul>