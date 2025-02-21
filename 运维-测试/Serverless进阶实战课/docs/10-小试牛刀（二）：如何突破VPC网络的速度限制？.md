你好，我是静远。

在[冷启动](https://time.geekbang.org/column/article/563691)这节课里，我跟你聊到了影响函数第一次执行速度的因素有很多，其中一个关键因素就是：VPC网络的建联时间。

我们知道，VPC是云厂商提供给用户的一个安全隔离的网络环境，用户可以在VPC空间中部署自己的服务，如Redis、数据库、MQ等。而我们的函数通常是创建在函数专属的VPC中的。一个生产级别的函数服务应用，少不了需要和其他的资源和中间件打交道。那么，跨VPC之间的通信效率就显得尤为重要了。

今天这节课，我就针对VPC之间的通信效率，通过案例实操的方式，为你剖析函数在跨VPC上的技术要点。

希望通过这节课，能够让你得到一些在Serverless的实战和后续优化工作的启发，能举一反三地找到更多优化方法，进一步突破函数访问速度的上限。

## 跨VPC问题的演进

针对云上网络连接的方式，相信你已经了解到不少，如专线（高速通道）、VPN网关、对等连接等方式。这些方式，有的用来解决IDC和VPC的连接，有的用来解决VPC与VPC之间的互通。

这其中，对等连接的确可以解决函数跨VPC的问题，但我们试想一下，如果每个用户都通过这种方式来解决这种问题，那么平台每次都需要搭建两端的连接，并且还可能会遇到IP网段冲突的问题。这样的做法显然不具备普适性，成本也过高。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/6b/e2/e2c7f18b.jpg" width="30px"><span>Geek_4dmcwo</span> 👍（1） 💬（3）<div>func bcc和proxy bcc本来就是通的，为啥要加一层隧道呢，直接把proxy bcc做网关，不就直接可以访问user bcc了吗</div>2022-09-28</li><br/><li><img src="" width="30px"><span>Wang Yifei</span> 👍（0） 💬（1）<div>“此时 func bcc1 访问 user bcc 172.16.101.4 仍然访问不通，在 proxy bcc 侧监听 eth1 流量可以发现，eth1 发往用户 VPC 的包的源 IP 仍是 func1 bcc gre0 设备的 IP 10.0.0.3”

这里有个问题，proxy bbc的gre0设备是不是会把gre封装的包头去掉后，继续根据payload进行路由转发？ 如果是这样的话，payload的源IP为什么还是10.0.0.3，而不是192.168.80.8呢？
</div>2023-04-04</li><br/><li><img src="" width="30px"><span>Wang Yifei</span> 👍（0） 💬（1）<div>没有找到Kubernetes中相关CM的配置
但我理解，是否也可以这样实现：在func bcc1中添加一条iptables规则，把发送给172.16.101.0&#47;24流量的Source IP修改为10.0.0.3。</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>网卡会提前在用户 VPC 所在的子网 Subnet 中创建，但租户的权限属于函数计算 VPC
==========
这个是怎么实现的？</div>2022-09-20</li><br/>
</ul>