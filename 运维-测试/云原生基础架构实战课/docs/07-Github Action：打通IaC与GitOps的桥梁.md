你好，我是潘野。

前面的课程里，我们学习了通过持续集成与部署的方式管理IaC代码的思路。不过知识必须学以致用，才能真正掌握。接下来的三讲内容，我们就来实操演练，学会如何使用GitOps，从而更好地管理IaC代码。

今天，我们会使用GitHub Actions这个工具来管理Terraform代码。为什么要选择GitHub Actions呢？

之前我们已经了解到，GitOps方式离不开在GitHub里管理代码。GitHub是一个广泛使用的代码托管平台，提供了许多与代码管理和协作相关的功能。而GitHub Actions是Github中自带的CI/CD工具，上手门槛较低。掌握了这个工具，能让你的管理、部署工作事半功倍。

## 基于Github Action的管理架构

在进入实操演练之前，我们需要先了解一下基于Github Action的管理架构长什么样。具体来说，就是通过Github Action来管理Terrafrom代码，并自动执行变化的代码，从而更改基础设施的架构。

![](https://static001.geekbang.org/resource/image/8c/ce/8c06230517da0ff6bfa5d7d1de1a24ce.jpg?wh=2119x1658)

对照架构图，不难看出Github Action的Terraform代码的管理主要体现在以下方面：

- 用户提交Pull Request之后，Github Action 通过OIDC的方式与AWS账户进行认证。
- 通过认证之后，Github Action执行 `terrafrom plan` 和 `terrafrom apply` 两个命令，Terrafrom会根据代码去更改基础设施配置。
- Terrafrom的状态文件会存在对象存储S3中，以便追踪Terrafrom的变化。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（0） 💬（1）<div>老师 关于AWS如何授权Github Action 我还是不太理解 上面那一步在AWS的IAM里配置Github token url的同时 是不是还需要我登入github认证？ 还是说 那个url是统一的 只要你指明github id  那只要是github这个id发来的请求都是合法的？</div>2024-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/fb/89/9bdafa93.jpg" width="30px"><span>黑石</span> 👍（0） 💬（0）<div>&quot;token.actions.githubusercontent.com:sub&quot;: &quot;repo:cloudnative-automation&#47;github-action-terrafrom:*&quot; } } } ]}

老师，这里的repo要改成自己的repo 吗</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（0） 💬（1）<div>开通EKS是不是需要额外的费用？</div>2024-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（0） 💬（0）<div>很不错，解答了我上节课后的疑问，因为我都是在本地apply所以会让手动确认，action后只要pr通过merge到main就生成，也很省事</div>2024-04-08</li><br/>
</ul>