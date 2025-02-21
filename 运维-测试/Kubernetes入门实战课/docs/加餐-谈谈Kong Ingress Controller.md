你好，我是Chrono。

课程已经完结三个多月了，还记得结课时我说的那句话吗：“是终点，更是起点”，课程的完结绝不意味着我们终止对Kubernetes的钻研，相反，不论你我，都会在这个学习的道路上持续地走下去。

当初开课时，我计划了很多内容，不过Kubernetes的领域实在太广，加上我日常工作比较忙，时间和精力有限，所以一些原定的知识点没有来得及展现，比较可惜，我一直想找机会做个补偿。

这几天开发任务略微空闲了些，我就又回到了专栏，准备使用另一个流行的工具：Kong Ingress Controller，再来讲讲对Kubernetes集群管理非常重要的Ingress。

## 认识Kong Ingress Controller

我们先快速回顾一下Ingress的知识（[第21讲](https://time.geekbang.org/column/article/538760)）。

Ingress类似Service，基于HTTP/HTTPS协议，是七层负载均衡规则的集合，但它自身没有管理能力，必须要借助Ingress Controller才能控制Kubernetes集群的进出口流量。

所以，基于Ingress的定义，就出现了各式各样的Ingress Controller实现。

我们已经见过了Nginx官方开发的Nginx Ingress Controller，但它局限于Nginx自身的能力，Ingress、Service等对象更新时必须要修改静态的配置文件，再重启进程（reload），在变动频繁的微服务系统里就会引发一些问题。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/cb/1f/d12f34de.jpg" width="30px"><span>Sheldon</span> 👍（4） 💬（1）<div>谢谢老师的加餐，这个课程真的很超值。</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a6/d4/8d50d502.jpg" width="30px"><span>简简单单</span> 👍（4） 💬（1）<div>赞</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f2/cc/b281c2b8.jpg" width="30px"><span>寒夜客来茶当酒</span> 👍（1） 💬（1）<div>我在文中看到了
“但它局限于 Nginx 自身的能力，Ingress、Service 等对象更新时必须要修改静态的配置文件，再重启进程（reload）”
 但是我学习了上文中 nginx ingress controller 的使用，并没有提及到修改 ingress 规则后需要重启 nginx 的相关内容，拜托老师解惑</div>2024-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/6f/1654f4b9.jpg" width="30px"><span>nc_ops</span> 👍（1） 💬（1）<div>老师，进入pod时为什么会默认进入proxy这个容器？这是在yaml文件的哪个位置确定的呢？</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5f/12/791d0f5e.jpg" width="30px"><span>mono176</span> 👍（0） 💬（1）<div> Failed to pull image &quot;kong&#47;kubernetes-ingress-controller:2.7.0&quot; 镜像拉去不下来，有国内阿里云的镜像嘛</div>2024-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/c1/e6/13b98a6b.jpg" width="30px"><span>钢</span> 👍（0） 💬（1）<div>traefik也是一种ingress Controller吗？</div>2023-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（1）<div>谢谢老师，两周的高强度学习，完成了k8s的入门。
后面就要开始用k8s完成一系列云原生应用开发部署</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/25/19cbcd56.jpg" width="30px"><span>StackOverflow</span> 👍（0） 💬（1）<div>和 apisix 功能很类似</div>2023-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/65/27fabb5f.jpg" width="30px"><span>茗</span> 👍（0） 💬（1）<div>老师，我初始化集群的时候制定了service的网段，为啥创建的service的ip地址不是我指定的网段呢？</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/35/be8372be.jpg" width="30px"><span>quietwater</span> 👍（0） 💬（1）<div>老师的课程很对我的胃口，按部就班学习不会有什么障碍，必须点赞！！！APISIX也是一种Ingress，老师是否可以介绍一下。查了一些资料，感觉APISIX比Kong更强大。求解惑！！！</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/85/6f/1654f4b9.jpg" width="30px"><span>nc_ops</span> 👍（0） 💬（1）<div>除了执行curl $(minikube ip):32521 -H &#39;host: kong.test&#39; -i，如果想在网页上查看实验结果，该怎么操作呢</div>2023-02-17</li><br/>
</ul>