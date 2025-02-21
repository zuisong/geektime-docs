你好，我是秦晓辉。

上一讲我们在Google四个黄金指标方法论的指导下，梳理了最常用的关系型数据库——MySQL的关键指标和采集方法。这一讲我们来继续学习最常用的NoSQL数据库——Redis的关键指标，掌握相关原理和采集方法。

Redis也是一个对外服务，所以Google的四个黄金指标同样适用于Redis，与上一讲一样，我们还是从延迟、流量、错误、饱和度这些方面，来分析Redis的关键指标。

## 延迟

在软件工程架构中，之所以选择Redis作为技术堆栈的一员，大概率是想要得到更快的响应速度和更高的吞吐量，所以延迟数据对使用Redis的应用程序至关重要。通常我们会通过下面这两种方式来监控延迟。

1. 客户端应用程序埋点。比如某个Java或Go的程序在调用Redis的时候，计算一下各个命令花费了多久，然后把耗时数据推给监控系统即可。这种方式好处是非常灵活，想要按照什么维度统计就按照什么维度统计，缺点自然是代码侵入性，和客户端埋点监控MySQL的原理是一样的。
2. 使用 redis-cli 的 `--latency` 命令，这个原理比较简单，就是客户端连上 redis-server，然后不断发送 ping 命令，统计耗时。我在远端机器对某个 redis-server 做探测，你可以看一下探测的结果。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/8hAib3LaXCPfDTTw0Vibj8ajLm79ZaFGiaFic7dJHZlypFuMft1Q1UukA2vklSUAg7OBCK1Xo2TDxYibLyMj5LMdgEQ/132" width="30px"><span>y</span> 👍（0） 💬（1）<div>redis默认连接数是1w吧？</div>2023-10-22</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoUnB8oxzr2YIXrvqxpOfKEiaZ60BCwzXHlFe6gxZmBzXUdL9Yk3Yp9s11bGcK9KIKtOdZBDibQ3GAQ/132" width="30px"><span>恰同学少年</span> 👍（0） 💬（1）<div>请教下如果Redis是sentinel集群，是否支持获取集群的信息？当master切换了能否感知到，应该怎么配置</div>2023-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>老师在回复云上API监控里写：“周期性自动生成categraf的配置文件”，这是什么意思呢？</div>2023-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/72/b4/7420b047.jpg" width="30px"><span>hello</span> 👍（0） 💬（1）<div>noeviction 老师这个默认的策略是怎么淘汰的呢</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（0） 💬（1）<div>老师请教一个问题，比如我监控了十台服务器主机，我现在报警规则是内存使用率超过80%触发报警，那么我是在报警规则里面配置十条这样子的规则还是只需要配置一条，如果我只配置一条如何配置呢？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/5d/edfa625d.jpg" width="30px"><span>Mori</span> 👍（0） 💬（1）<div>感觉中间件监控方法差不多类似，比如针对云上REDIS，那么通过自己部署categraf采集还是对接云监控指标好一点呢，如果实例数量比较多，其实也能也需要管理多个categraf采集，维护稍微麻烦点
</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师两个问题：
Q1：categraf是部署在Redis所在的机器上吗？
Q2：最后的图中，”Max Memory Limit”是0，是表示满意限制吗？</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（0） 💬（2）<div>老师，请教你一个问题，就是我夜莺配置了告警规则，但是勾选企业微信和填写回调地址企业微信的webhook，为什么企业微信无法收到报警信息，历史告警里面有记录呢，webhook地址我可以确认是没错的，是我哪里配置不对嘛。</div>2023-02-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaxxRyl13SvqsqWuhtJHWMVRMeIo7byfJ0AaicwcRvibcfw0DSrGHFVz7dhwicBJNsFSFRk4kuia28jQ/132" width="30px"><span>k8s卡拉米</span> 👍（1） 💬（0）<div>老师，您好，我看redis仪表盘中没有关于redis 的状态的图表，需要向监控redis 主从状态，或者redis cluster的状态怎么做呢</div>2023-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6b/20/004af747.jpg" width="30px"><span>志强</span> 👍（0） 💬（0）<div>老师 为什么不用redis-tool</div>2023-02-18</li><br/>
</ul>