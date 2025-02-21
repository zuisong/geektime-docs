你好，我是潘野。

前面的课程里，我们学习了云原生的基本组成技术，现代化的云原生技术架构如何管理以及公有云的基本特点等内容。你可能觉得前面的知识偏理论，眼睛看会了、脑袋明白了，但是手还不会。

从这一章开始，我为你设计了一系列的实验，从易到难、循序渐进地带你实战演练，最终形成一套可以用在生产环境的基础架构自动化管理方式。除了提高实践水平，你还能加深对不可变基础设施、混合云管理等理论的理解。

这一讲我们会利用Terraform工具，在AWS中启动一个Kubernetes集群，帮你尽快熟悉现代IaC面向资源的管理方式。

## 前期准备工作

为什么我们选择公有云AWS作为课程的实践环境呢？

因为它提供了完整的IaaS API与文档，更方便我们学习实践。而且无论是哪个云厂商，提供的功能都差不多。即便你所在的团队是自建机房，多数也会采用像Openstack、VMware这样的IaaS解决方案，哪怕API或操作跟公有云略有差别，使用方法和思路也基本一致。

好，下面正式进入实战环节，我们先从配置本地环境开始。我们选用一台Ubuntu 22.04的虚拟机作为基础操作环境。

首先，我们需要安装AWS的命令行工具AWS CLI。如果你使用的是Mac OS或者Windows系统，可以参照AWS的[官方文档](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)来配置你的环境，这里我们只列出Linux环境的配置命令。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_45a572</span> 👍（2） 💬（1）<div>老师您好，有一个场景，我的vpc使用tf创建之后。创建了rds也使用了这个vpc.  因为是在eks创建的脚本中写的vpc. 我此时释放eks，那么这个vpc也被释放了这个问题应该如何处理？</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/24/52/4e1f33d0.jpg" width="30px"><span>发条橙</span> 👍（0） 💬（3）<div>$ terraform apply
╷
│ Error: error configuring Terraform AWS Provider: error validating provider credentials: error calling sts:GetCallerIdentity: operation error STS: GetCallerIdentity, https response error StatusCode: 403, RequestID: afe63bae-7f5f-45b2-a3b5-80364f4a5f34, api error InvalidClientTokenId: The security token included in the request is invalid.
│ 
│   with provider[&quot;registry.terraform.io&#47;hashicorp&#47;aws&quot;],
│   on main.tf line 11, in provider &quot;aws&quot;:
│   11: provider &quot;aws&quot; {
</div>2024-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/73/9eb7c992.jpg" width="30px"><span>Eason Lau</span> 👍（0） 💬（1）<div>老师请问你在创建过程中有在哪里指定node的数量么？
另外就是eks集群是不是得挺贵啊？自己做实验的话😭</div>2024-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/4d/1b/062941b4.jpg" width="30px"><span>🐭 🐹 🐭 🐹 🐭</span> 👍（0） 💬（1）<div>为什么现在遇到的场景基本上是一个集群呢？是因为私有云的原因吗</div>2024-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a1/bc/ef0f26fa.jpg" width="30px"><span>首富手记</span> 👍（0） 💬（0）<div>多集群管理的时候，就把每个集群的差异地方抽出来 用变量的方式来管理应该就可以了</div>2024-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/90/9c/288e4db2.jpg" width="30px"><span>良凯尔</span> 👍（0） 💬（0）<div>针对Kubernetes集群的生命周期管理，比如说部署集群、扩容节点等等操作，使用Kubernetes SIGs 的 Cluster API（基于k8s CRD的方式来管理Kubernetes集群）会更加方便，众多云厂商都提供了自己的provider，使得可以基于不同云厂商的基础设施来部署Kubernetes集群；    </div>2024-04-06</li><br/>
</ul>