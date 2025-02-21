你好，我是潘野。

上一讲，我们学习了如何使用GitHub Action来管理Terraform代码，并且也实现了GitOps的整个过程。

虽然这种方式比较容易上手，但是GitHub Action存在一定的局限性。比如有些公司并没有选择GitHub作为代码管理平台，而是选择Gitlab作为公司的代码管理平台。或者是有些公司购买的是Github Enterprise版本，这时候有一些GitHub上的第三方插件就无法在内网环境里使用。针对这些场景，我们就需要找到一个适用度更好的CI/CD工具。

在持续集成领域，有很多持续集成、持续部署的工具，除了前一讲使用的Github Action，还有大名鼎鼎的Jenkins，来自Kubernetes社区的Prow等等，而今天我们将会选择使用Tekton来作为我们CI/CD的工具链。

## 为什么选择使用 Tekton？

和其他的CI/CD工具相比，Tekton有三个优势。

第一，Tekton的设计考虑到了多种使用场景，定制程度高且相对容易上手，能够适应各种复杂的需求。例如，它用Task这个资源来描述每个步骤细节，用Pipeline这个资源将各个步骤串联在一起。因此，相比Jenkins Pipeline中将步骤与流水线混合编写，Tekton配置代码的可读性和可维护性会更好。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/b5/e9/f1aa07d6.jpg" width="30px"><span>alex run</span> 👍（0） 💬（1）<div>解决tf init加载问题，是不是可以用pvc缓存起来</div>2024-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/21/0bac2254.jpg" width="30px"><span>橙汁</span> 👍（0） 💬（1）<div>tekton有点之前用jenkins那味了，又是插件又是定义变量 最后总结的相当可以，之前看了kubernetes的gitops形式 其实gitops并不局限 iac 自动化 集群等任何方面都能用gitops方式</div>2024-04-10</li><br/><li><img src="" width="30px"><span>Geek_45a572</span> 👍（0） 💬（0）<div>可以使用cache.将provider缓存起来</div>2024-04-10</li><br/>
</ul>