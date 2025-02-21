你好，我是孔令飞。

上一讲，我介绍了IAM部署用到的两个核心组件，Nginx和Keepalived。那么这一讲，我们就来看下，如何使用Nginx和Keepalived来部署一个高可用的IAM应用。下一讲，我再介绍下IAM应用安全和弹性伸缩能力的构建方式。

这一讲，我们会通过下面四个步骤来部署IAM应用：

1. 在服务器上部署IAM应用中的服务。
2. 配置Nginx，实现反向代理功能。通过反向代理，我们可以通过Nginx来访问部署在内网的IAM服务。
3. 配置Nginx，实现负载均衡功能。通过负载均衡，我们可以实现服务的水平扩缩容，使IAM应用具备高可用能力。
4. 配置Keepalived，实现Nginx的高可用。通过Nginx + Keepalived的组合，可以实现整个应用架构的高可用。

## 部署IAM应用

部署一个高可用的IAM应用，需要至少两个节点。所以，我们按照先后顺序，分别在`10.0.4.20`和`10.0.4.21`服务器上部署IAM应用。

### 在`10.0.4.20`服务器上部署IAM应用

首先，我来介绍下如何在`10.0.4.20`服务器上部署IAM应用。

我们要在这个服务器上部署如下组件：

- iam-apiserver
- iam-authz-server
- iam-pump
- MariaDB
- Redis
- MongoDB
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（8） 💬（3）<div>iamctl 好用的不行，已经沉淀为了自己的 pctl 了，这不是抄袭，这是模仿～</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/99/8c0d8f66.jpg" width="30px"><span>㊣Coldstar</span> 👍（0） 💬（1）<div>阿里云有免费的内网负载均衡可以使用 腾讯云 没看到可以创建 内网专用的负载均衡，这样的话，利用云基础设施可以简化部署</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（0）<div>总结：
1. 在服务器上部署 IAM应用中的服务。20 机器上还会部署 Mysql, Redis, MongoDB
2. 配置 Nginx。主要是添加两个 server，在 http{} 中添加 upstream。
4. 配置 Keepalived</div>2021-12-04</li><br/>
</ul>