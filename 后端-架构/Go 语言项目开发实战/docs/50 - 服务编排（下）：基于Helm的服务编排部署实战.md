你好，我是孔令飞。

上一讲，我介绍了 Helm 的基础知识，并带着你部署了一个简单的应用。掌握Helm的基础知识之后，今天我们就来实战下，一起通过Helm部署一个IAM应用。

通过Helm部署IAM应用，首先需要制作IAM Chart包，然后通过Chart包来一键部署IAM应用。在实际开发中，我们需要将应用部署在不同的环境中，所以我也会给你演示下如何在多环境中部署IAM应用。

## 制作IAM Chart包

在部署IAM应用之前，我们首先需要制作一个IAM Chart包。

我们假设IAM项目源码根目录为`${IAM_ROOT}`，进入 `${IAM_ROOT}/deployments`目录，在该目录下创建Chart包。具体创建流程分为四个步骤，下面我来详细介绍下。

**第一步，**创建一个模板Chart。

Chart是一个组织在文件目录中的集合，目录名称就是Chart名称（没有版本信息）。你可以看看这个 [Chart 开发指南](https://helm.sh/zh/docs/topics/charts) ，它介绍了如何开发你自己的Chart。

不过，这里你也可以使用 `helm create` 命令来快速创建一个模板Chart，并基于该Chart进行修改，得到你自己的Chart。创建命令如下：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（7） 💬（1）<div>“给所有字符串类型的值加上引号。”
深有体会，很多开源的chart也可能存在这种问题。比如pvc的名称，没有用quote加引号，用户如果非得来一个全数字的pvc就悲剧了。helm会默认转换为数字类型。

我一般调试时使用helm upgrade --install —debug —dry-run。如果可以看到渲染后的yaml，调试起来还是蛮方便的。</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（1）<div>总结：
制作chart的流程：
1. 使用 helm create 命令创建一个 chart；
2. chart 的目录结构：Chart.yaml, values.yaml, templates, charts 等。
3. templates 目录中包含资源的定义文件，使用了 go template 语法，有点凌乱。
4. 建议 values.yaml 文件中个，给所有字符串类型的值加上引号；使用字符串来表示整型，通过 {{ int $values }} 方式来引用。
5. 使用 helm lint 或者 helm install --dry-run 方式，验证helm package的格式，但内容上不一定符合你预期。</div>2021-12-05</li><br/><li><img src="" width="30px"><span>GeekCoder</span> 👍（0） 💬（1）<div>一个应用有多个服务，其中一个服务改动之后，得重新打一个chart包？全部重新部署？</div>2022-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（1）<div>对于一些yaml配置，如果pro 使用，test 不需要，该如何配置呢。比如node 亲和性配置，可能线上要配，测试环境就无所谓了。</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/30/5b/82e3952c.jpg" width="30px"><span>Wongkakui</span> 👍（0） 💬（0）<div>有个疑问，一般集群内的资源都是运维管理的，但我们项目使用到的资源可以通过helm values维护在自己代码仓库，运维缺改不了，这种情况有最佳实践吗</div>2023-03-05</li><br/>
</ul>