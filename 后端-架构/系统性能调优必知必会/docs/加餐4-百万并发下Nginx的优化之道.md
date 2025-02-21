你好，我是专栏编辑冬青。今天的课程有点特别，作为一期加餐，我为你带来了陶辉老师在GOPS 2018 · 上海站的分享，以文字讲解+ PPT的形式向你呈现。今天的内容主要集中在Nginx的性能方面，希望能给你带来一些系统化的思考，帮助你更有效地去做Nginx。

## 优化方法论

今天的分享重点会看这样两个问题：

- 第一，如何有效使用每个连接分配的内存，以此实现高并发。
- 第二，在高并发的同时，怎样提高QPS。

当然，实现这两个目标，既可以从单机中的应用、框架、内核优化入手，也可以使用类似F5这样的硬件设备，或者通过DNS等方案实现分布式集群。

![](https://static001.geekbang.org/resource/image/1a/24/1a69ba079c318c227c9ccff842714424.jpg?wh=1888%2A1082)

而Nginx最大的限制是网络，所以将网卡升级到万兆，比如10G或者40G吞吐量就会有很大提升。作为静态资源、缓存服务时，磁盘也是重点关注对象，比如固态硬盘的IOPS或者BPS，要比不超过1万转每秒的机械磁盘高出许多。

![](https://static001.geekbang.org/resource/image/4a/2c/4aecd5772e4d164dc414d1f473440f2c.jpg?wh=1874%2A1076)

这里我们重点看下CPU，如果由操作系统切换进程实现并发，代价太大，毕竟每次都有5微秒左右的切换成本。Nginx将其改到进程内部，由epoll切换ngx\_connection\_t连接的处理，成本会非常低。OpenResty切换Lua协程，也是基于同样的方式。这样，CPU的计算力会更多地用在业务处理上。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（0） 💬（1）<div>这篇文章关于tcp好多优化参数呀</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（7） 💬（2）<div>1.&quot;我们还可以将小报文合并后批量发送，通过减少 IP 与 TCP 头部的占比，提高网络效率。在 nginx.conf 文件中打开 tcp_nopush、tcp_nodelay 功能后，都可以实现这些目的      &quot;
这里开启nodelay不是关闭nagle算法，从而不合并小包吗？感觉讲的矛盾了，求老师答疑
2. 出现过一个场景，开启numa2个node  把网卡中断绑定到1个node中的所有cpu，和 网卡中断一对一绑定到2个node的全部cpu，发现后者效果不好，单核si更高了，是numa node的竞争导致的吗？生产接入层nginx是否建议开启numa，是否有生产经验分享下呢？</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/26/9ac98036.jpg" width="30px"><span>招谁惹谁</span> 👍（0） 💬（0）<div>并发总有个上限，调优也有极限，调到什么时候是合适的呢？</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（0）<div>老师的治学态度令人钦佩</div>2020-07-17</li><br/>
</ul>