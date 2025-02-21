你好，我是雪飞。

用了这么久的命令行，是不是很喜欢 kubectl 这个集群管理工具，我个人也是更喜欢使用命令行来管理集群。不过，这节课我给你介绍两款 K8s 集群的可视化管理工具：Dashboard 和 Kuboard，通过可视化管理工具可以更加直观地查看集群状态以及管理资源对象。

## Dashboard

K8s Dashboard 是一个官方支持的开源 Web 界面工具，它极大地简化了 K8s 集群的管理和监控。通过浏览器访问一个直观的用户界面，你可以执行资源的部署、更新、删除和查看操作，同时监控集群状态和资源对象的使用情况。Dashboard 支持故障排查工具，如日志查看和事件监控，以及与 K8s RBAC 的集成，提供了细粒度的访问控制。此外，它还允许用户设置资源配额和限制，帮助优化资源使用和成本控制。

总体而言，Dashboard 是一个功能全面的可视化工具，为 Kubernetes 集群管理者提供了一种直观、高效、安全的方式来管理和监控集群资源，无需复杂的命令行操作。下面我们就先来部署一下 Dashboard。

### 部署 Dashboard

Dashboard 需要部署到 K8s 集群中，使用 YAML 文件部署。

1. 下载 Dashboard 的 YAML 部署文件。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/5d/13/cb8e35cb.jpg" width="30px"><span>阿宣</span> 👍（0） 💬（0）<div>Dashboard部署成功以后页面访问不了</div>2025-01-09</li><br/>
</ul>