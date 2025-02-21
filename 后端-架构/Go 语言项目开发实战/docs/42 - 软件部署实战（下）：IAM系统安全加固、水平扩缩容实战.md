你好，我是孔令飞。

这一讲和前面两讲，都是介绍如何基于物理机/虚拟机来部署IAM的。在前面两讲，我们了解了如何部署一个高可用的 IAM 应用，今天就再来看看IAM 应用安全和弹性伸缩能力的构建方式。在这一讲中，我会带你加固IAM应用的安全性，并介绍如何具体执行扩缩容步骤。

接下来，我们先来看下如何加固IAM应用的安全性。

## IAM应用安全性加固

iam-apiserver、iam-authz-server、MariaDB、Redis和MongoDB这些服务，都提供了绑定监听网卡的功能。我们可以将这些服务绑定到内网网卡上，从而只接收来自于内网的请求，通过这种方式，可以加固我们的系统。

我们也可以通过iptables来实现类似的功能，通过将安全问题统一收敛到iptables规则，可以使我们更容易地维护安全类设置。

这门课通过iptables来加固系统，使系统变得更加安全。下面，我先来对iptables工具进行一些简单的介绍。

### iptables简介

iptables是Linux下最优秀的防火墙工具，也是Linux内核中netfilter网络子系统用户态的工具。

netfilter提供了一系列的接口，在一个到达本机的数据包，或者经本机转发的数据包流程中添加了一些可供用户操作的点，这些点被称为HOOK点。通过在HOOK点注册数据包处理函数，可以实现数据包转发、数据包过滤、地址转换等功能。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/64/53/c93b8110.jpg" width="30px"><span>daz2yy</span> 👍（14） 💬（3）<div>系统缩容的时候逆向操作应该是从修改 iptables 开始 =&gt; keepalived =&gt; Nginx =&gt; 关闭服务 =&gt; 删除节点；不然先关闭了服务，这时候 nginx 还是会把流量导过来的吧？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/46/717d5cb9.jpg" width="30px"><span>惜心（伟祺）</span> 👍（3） 💬（1）<div>这课值了 整个大工程开发的全套啊</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/26/a6ffea5b.jpg" width="30px"><span>hi,guy</span> 👍（2） 💬（3）<div>后面能不能补充下项目的可观测性章节，如此多服务怎么治理，有什么好的方法没有？</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bf/86/c0cb35f0.jpg" width="30px"><span>8.13.3.27.30</span> 👍（0） 💬（1）<div>我们的服务是部署在k8s上的，防火墙这块要在哪里做？</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（0）<div>总结：
IAM系统安全加固，Iptables 是Linux系统的防火墙，与Netfilter一起工作，对网络包进行过滤、修改、转发等操作。
详情先略过</div>2021-12-05</li><br/>
</ul>