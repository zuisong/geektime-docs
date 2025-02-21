今天这篇文章，已经是实践案例系列的最后一篇了。在[《快速构建持续交付系统（二）：GitLab 解决配置管理问题》](https://time.geekbang.org/column/article/40169)和[《快速构建持续交付系统（三）：Jenkins 解决集成打包问题》](https://time.geekbang.org/column/article/40412)这两篇文章中，我们已经分别基于GitLab搭建了代码管理平台、基于Jenkins搭建了集成与编译系统，并解决了这两个平台之间的联动、配合问题，从而满足了在代码平台 push 代码时，驱动集成编译系统工作的需求。

算下来，我们已经通过前面这两篇文章，跑完了整个持续交付体系三分之二的路程，剩下的就是解决如何利用开源工具搭建发布平台完成代码发布，跑完持续交付最后一公里的问题了。

## 利用Ansible完成部署

Ansible 是一个自动化运维管理工具，支持Linux/Windows跨平台的配置管理，任务分发等操作，可以帮我们大大减少在变更环境时所花费的时间。

与其他三大主流的配置管理工具Chef、Puppet、Salt相比，Ansible最大的特点在于“agentless”，即无需在目标机器装安装agent进程，即可通过SSH或者PowerShell对一个环境中的集群进行中心化的管理。

所以，这个“agentless”特性，可以大大减少我们配置管理平台的学习成本，尤其适合于第一次尝试使用此类配置管理工具。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/4d/abb7bfe3.jpg" width="30px"><span>铭熙</span> 👍（4） 💬（1）<div>如果jenkins有多个slave，每个slave节点都要装ansible吧？这些slave节点上的ssh key怎么保持一致性呢？</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/fc/0e887697.jpg" width="30px"><span>kkgo</span> 👍（5） 💬（3）<div>ansible tower收费的吧</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/d4/a944bf4d.jpg" width="30px"><span>天煜</span> 👍（3） 💬（0）<div>怎么快速的在大规模集群中发布大的代码包？例如，5000台机器，发布1G的代码包。</div>2019-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/c8/50af4a53.jpg" width="30px"><span>黄云龙</span> 👍（2） 💬（1）<div>ansible 与 Docker 有什么区别</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/14/99/5b1ed92b.jpg" width="30px"><span>戴斌</span> 👍（0） 💬（0）<div>我们也是用Ansible发布的</div>2020-03-25</li><br/>
</ul>