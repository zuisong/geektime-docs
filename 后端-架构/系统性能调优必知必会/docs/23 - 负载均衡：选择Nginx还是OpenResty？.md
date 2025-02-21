你好，我是陶辉。

在[\[第21讲\]](https://time.geekbang.org/column/article/252741) 介绍AKF立方体时，我们讲过只有在下游添加负载均衡后，才能沿着X、Y、Z三个轴提升性能。这一讲，我们将介绍最流行的负载均衡Nginx、OpenResty，看看它们是如何支持AKF扩展体系的。

负载均衡通过将流量分发给新增的服务器，提升了系统的性能。因此，我们对负载均衡最基本的要求，就是它的吞吐量要远大于上游的应用服务器，否则扩展能力会极为有限。因此，目前性能最好的Nginx，以及在Nginx之上构建的OpenResty，通常是第一选择。

系统接入层的负载均衡，常通过Waf防火墙承担着网络安全职责，系统内部的负载均衡则通过权限、流量控制等功能承担着API网关的职责，CDN等边缘节点上的负载均衡还会承担边缘计算的任务。如果负载均衡不具备高度开放的设计，或者推出时间短、社区不活跃，**我们就无法像搭积木一样，从整个生态中低成本地构建出符合需求的负载均衡。**

很幸运的是，Nginx完全符合上述要求，它性能一流而且非常稳定。从2004年诞生之初，Nginx的模块化设计就未改变过，这样16年来累积下的各种Nginx模块都可以复用。它的[2-clause BSD-like license](https://opensource.org/licenses/BSD-2-Clause) 源码许可协议极其开放，即使修改源码后仍然可作商业用途，因此Nginx之上延伸出了TEngine、OpenResty、Kong等生态，这大大扩展了Nginx的能力边界。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/97/69/80945634.jpg" width="30px"><span>罐头瓶子</span> 👍（8） 💬（1）<div>我的建议直接用OR即可。nginx 配置文件与lua的编程表达能力还是有挺大差距的！rewrite access 等阶段做URL跳转 还是lua比较好用。另外我认为nginx基本不具备自己生成业务响应的能力(能自己写nginxC模块的另算），而OR则可以完全胜任这个工作。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/30/85/14c2f16c.jpg" width="30px"><span>石小</span> 👍（6） 💬（1）<div>使用nginx 作为grpc的负载均衡，采用http2的方式总是60s就自动和上游服务器断开连接，grpc_socket_keepalive、grpc_connect_timeout、grpc_read_timeout、grpc_send_timeout参数都设置过了，这种情况正常吗？采用stream的方式不会出现断开的情况</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（1） 💬（2）<div>老师推荐APISIX新一代网关吗？</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（1） 💬（1）<div>nginx的配置文件中为什么可以配置两个并列的http块儿呢，好像还不报错。</div>2020-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（0） 💬（2）<div>能落地都好</div>2020-07-30</li><br/>
</ul>