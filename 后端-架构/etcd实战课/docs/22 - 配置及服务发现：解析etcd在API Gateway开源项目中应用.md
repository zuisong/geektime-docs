你好，我是唐聪。

在软件开发的过程中，为了提升代码的灵活性和开发效率，我们大量使用配置去控制程序的运行行为。

从简单的数据库账号密码配置，到[confd](https://github.com/kelseyhightower/confd)支持以etcd为后端存储的本地配置及模板管理，再到[Apache APISIX](https://github.com/apache/apisix)等API Gateway项目使用etcd存储服务配置、路由信息等，最后到Kubernetes更实现了Secret和ConfigMap资源对象来解决配置管理的问题。

那么它们是如何实现实时、动态调整服务配置而不需要重启相关服务的呢？

今天我就和你聊聊etcd在配置和服务发现场景中的应用。我将以开源项目Apache APISIX为例，为你分析服务发现的原理，带你了解etcd的key-value模型，Watch机制，鉴权机制，Lease特性，事务特性在其中的应用。

希望通过这节课，让你了解etcd在配置系统和服务发现场景工作原理，帮助你选型适合业务场景的配置系统、服务发现组件。同时，在使用Apache APISIX等开源项目过程中遇到etcd相关问题时，你能独立排查、分析，并向社区提交issue和PR解决。

## 服务发现

首先和你聊聊服务发现，服务发现是指什么？为什么需要它呢?

为了搞懂这个问题，我首先和你分享下程序部署架构的演进。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（5） 💬（2）<div>老师的问题，我的个人看法是，采用etcd应该是可行的。

1.高可靠。etcd基于raft的多副本可以满足。
2.高性能。公司业务多，规模大，可以依据不同业务不同etcd的方法，分担etcd的写压力，以及数据存储量有限的问题。各自业务的etcd可以水平扩展。
3.支持多业务、多版本管理、多种发布策略。etcd可以做到多版本管理，多发布策略的话，可以级联多个etcd的方法。

另外，可能更加理想的存储架构方式是采用计算与存储分离的方法，计算部分处理读写以及扩展，存储部分处理多版本，多业务，多发布策略。</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/40/06/bb31933b.jpg" width="30px"><span>大爱无疆</span> 👍（3） 💬（1）<div>做一个etcd proxy，proxy 实现 hash，将不同的&#47;key  映射到后端不同的etcd集群上。
这样 相当于实现了 支持分片的 分布式存储。</div>2021-04-09</li><br/><li><img src="" width="30px"><span>Geek_daf51a</span> 👍（5） 💬（0）<div>思考题很棒，我认为etcd并不合适，适合使用可平行扩容的分布式数据库如tidb，运维复杂度不更低点吗，容量也更大，还能支持各种key value大小配置</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/64/cf13c011.jpg" width="30px"><span>刁寿钧</span> 👍（1） 💬（1）<div>其实还期待讨论下APISIX搭配证书使用etcd的姿势，哈哈</div>2021-03-15</li><br/><li><img src="" width="30px"><span>Geek_ed84ef</span> 👍（0） 💬（0）<div>给服务路由配Lease跟APISIX提供的健康检查插件有什么区别吗?好像都是服务异常后可自动摘除节点</div>2021-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/3b/46/3701e908.jpg" width="30px"><span>Coder</span> 👍（0） 💬（0）<div>我认为使用支持分片的nosql数据库比较合适，比如redis集群版本，一主两副本、还是很可靠得</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/3a/de/e5c30589.jpg" width="30px"><span>云原生工程师</span> 👍（0） 💬（0）<div>我认为etcd不太合适，应该使用类似阿里云drds、腾讯云tdsql这样分布式数据库，不过数据推送机制就没了，需要轮询了，但是容量不需要担心，支持多业务就表中增加一个字段或独立的表</div>2021-03-13</li><br/>
</ul>