你好，我是唐聪。

在使用etcd的过程中，你是否被日志中的"apply request took too long"和“etcdserver: request timed out"等高延时现象困扰过？它们是由什么原因导致的呢？我们应该如何来分析这些问题？

这就是我今天要和你分享的主题：etcd延时。希望通过这节课，帮助你掌握etcd延时抖动、超时背后的常见原因和分析方法，当你遇到类似问题时，能独立定位、解决。同时，帮助你在实际业务场景中，合理配置集群，遵循最佳实践，尽量减少expensive request，避免etcd请求出现超时。

## 分析思路及工具

首先，当我们面对一个高延时的请求案例后，如何梳理问题定位思路呢？

知彼知己，方能百战不殆，定位问题也是类似。首先我们得弄清楚产生问题的原理、流程，在[02](https://time.geekbang.org/column/article/335932)、[03](https://time.geekbang.org/column/article/336766)、[04](https://time.geekbang.org/column/article/337604)中我已为你介绍过读写请求的核心链路。其次是熟练掌握相关工具，借助它们，可以帮助我们快速攻破疑难杂症。

这里我们再回顾下03中介绍的，Leader收到一个写请求，将一个日志条目复制到集群多数节点并应用到存储状态机的流程（如下图所示），通过此图我们看看写流程上哪些地方可能会导致请求超时呢？

![](https://static001.geekbang.org/resource/image/df/2c/df9yy18a1e28e18295cfc15a28cd342c.png?wh=1920%2A1328)

首先是流程四，一方面，Leader需要并行将消息通过网络发送给各Follower节点，依赖网络性能。另一方面，Leader需持久化日志条目到WAL，依赖磁盘I/O顺序写入性能。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/9d/84/171b2221.jpg" width="30px"><span>jeffery</span> 👍（9） 💬（1）<div>能规避
expensive request，大包请求导致的延迟吗</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/86/39/d12aaabf.jpg" width="30px"><span>kingstone</span> 👍（2） 💬（1）<div>老师您好，请问关于etcd grafana监控，grafana.com上有没有比较好用的dashboards？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/27/5d218272.jpg" width="30px"><span>八台上</span> 👍（0） 💬（3）<div>想问一下出现这个错  etcdserver: request timed out ， 客户端进行重拾处理吗？  谢谢</div>2021-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/30/85/14c2f16c.jpg" width="30px"><span>石小</span> 👍（0） 💬（1）<div>感谢唐老师，干货，实用。老师后期会讲etcd典型的应用场景（比如服务发现）和注意事项吗？</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（3） 💬（0）<div>老师问下，为什么磁盘IO波动会引起leader切换</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/72/83/7a331b42.jpg" width="30px"><span>哈登</span> 👍（0） 💬（0）<div>请问下怎么将trace 日志打印的阈值改成 1 纳秒
</div>2024-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/4d/97/1d99a0a3.jpg" width="30px"><span>柒城</span> 👍（0） 💬（1）<div>老师你好，我在使用集群时出现一直打印etcdserver: request timed out。然后看了一个节点坏了，但是磁盘并没有坏，除了io延时套可能造成的原因还有哪些？</div>2021-06-22</li><br/>
</ul>