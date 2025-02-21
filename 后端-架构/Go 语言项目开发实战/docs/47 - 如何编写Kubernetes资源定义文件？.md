你好，我是孔令飞。

在接下来的48讲，我会介绍如何基于腾讯云EKS来部署IAM应用。EKS其实是一个标准的Kubernetes集群，在Kubernetes集群中部署应用，需要编写Kubernetes资源的YAML（Yet Another Markup Language）定义文件，例如Service、Deployment、ConfigMap、Secret、StatefulSet等。

这些YAML定义文件里面有很多配置项需要我们去配置，其中一些也比较难理解。为了你在学习下一讲时更轻松，这一讲我们先学习下如何编写Kubernetes YAML文件。

## 为什么选择YAML格式来定义Kubernetes资源？

首先解释一下，我们为什么使用YAML格式来定义Kubernetes的各类资源呢？这是因为YAML格式和其他格式（例如XML、JSON等）相比，不仅能够支持丰富的数据，而且结构清晰、层次分明、表达性极强、易于维护，非常适合拿来供开发者配置和管理Kubernetes资源。

其实Kubernetes支持YAML和JSON两种格式，JSON格式通常用来作为接口之间消息传递的数据格式，YAML格式则用于资源的配置和管理。YAML和JSON这两种格式是可以相互转换的，你可以通过在线工具[json2yaml](https://www.json2yaml.com/convert-yaml-to-json)，来自动转换YAML和JSON数据格式。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（3） 💬（2）<div>覆盖掉挂载的整个目录，使用volumeMount.subPath来声明我们只是挂载单个文件，而不是整个目录，只需要在subPath后面加上我们挂载的单个文件名即可</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（0） 💬（1）<div>总结：
YAML规范：属性和值都是大小写敏感的；使用两个空格代表一层缩进；
k8syaml: 以交互式的方式，动态生成 Deployment、DaemonSet、StatefulSet 对象；
校验 Kubernetes YAML 的工具：kubeeval 验证k8syaml文件的正确性；kubescore 验证 k8syaml 文件的安全性；如果希望自定义验证策略，可以考虑使用 copper。
kube-neat 工具 可以将 kubectl xxx -oyaml 导出来的 yaml的 status 部分和部分meta 部分过滤掉；
kubectx 和 kubens 快速切换 k8s 环境</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（0）<div>推荐的工具很实用👍</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（0）<div>json2yaml 和 yaml2json 过于常用，我是集成到vim的快捷方式中了。

老师的这个中文注释太详细了，适合新手。😄

后面这几个工具学习了。</div>2021-10-10</li><br/>
</ul>