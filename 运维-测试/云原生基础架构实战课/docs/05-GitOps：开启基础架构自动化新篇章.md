你好，我是潘野。

前面几讲，我们一起探索了IaC的发展脉络、相关工具的原理分析以及多云异构的管理方式。

不知道你是否发现一个问题？这些内容基本都是从单一维度来审视基础架构自动化，而真正维护基础设施自动化的时候，我们还会面临其他的问题，例如持续集成与自动化部署、版本控制，文档与团队协作规范等等。

而今天我们要学习的GitOps模式，就可以把这些零散的点合理组织起来，帮我们真正落地实现基础架构自动化。

## 持续集成和持续部署

我们依然从一个小场景出发。

Tom和Jerry是公司平台组的工程师。有一天Tom接到一个需求，需要在AWS中部署一套业务环境。但是，当Tom快要完成时，被抽调去支援其他紧急项目，于是Jerry接手了Tom的工作。

Jerry拿着Tom用邮件发过来的Terraform代码，继续完成部署环境的任务。不过，在运行terraform apply时他发现，Tom提供的代码可能并不是最新的，因为代码中缺少一些配置，实际状态和他代码中的描述不一致。

此时Jerry犯愁了，贸然执行可能会导致整个环境损坏。所以，Jerry只能先手动更改线上环境配置，以免影响业务上线进度，等Tom从其他项目回来之后再将问题反馈给他。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_45a572</span> 👍（2） 💬（1）<div>潘帅哥 能分享一些terraform和gitops的最佳实践吗？变更ec2实例规格有点太简单啦。例如使用tf创建eks时vpc安全组 子网 add-on  混部 …  这种生产可用的实战</div>2024-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（0） 💬（1）<div>这里的集群升级与k8s官网文档介绍的升级当时有哪些区别？文章里说升级是通过新建一个节点加入集群，在把老节点从集群移除，这原来节点上面的pod不是有重见了吗？这是服务可用性又如何保证？</div>2024-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（1） 💬（2）<div>基础设施全走gitops 还有个问题要解决，就是terraform的状态信息存储，肯定是要远程 走ci做terraform plan检测好理解，合并到主分支再次触发cicd 执行terraform apply时候会涉及到更新git仓库文件，我现在是在本地apply完直接推到git算是拿git当远程存储，不知道这部分我理解的对不对，反正terraform可以拿s3啥的当存储</div>2024-04-03</li><br/>
</ul>