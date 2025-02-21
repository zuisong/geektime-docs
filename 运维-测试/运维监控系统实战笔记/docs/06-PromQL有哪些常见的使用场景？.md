你好，我是秦晓辉。

上一讲我们介绍了 Prometheus 中的一些关键设计，比如注重标准和生态、监控目标动态发现机制、PromQL等，其中 PromQL 是 Prometheus 的查询语言，使用起来非常灵活方便，但很多人不知道如何更好地利用它，发挥不出它的优势。所以这一讲我们就来梳理一下PromQL的典型应用场景。

PromQL主要用于时序数据的查询和二次计算场景。我们先来回顾一下时序数据，在脑子里建立起时序数据的具象视图。

## 时序数据

我们可以把时序数据理解成一个以时间为轴的矩阵，你可以看一下我给出的例子，例子中有三个时间序列，在时间轴上分别对应不同的值。

```yaml
^
│     . . . . . . . . . .   node_load1{host="host01",zone="bj"}
│     . . . . . . . . . .   node_load1{host="host02",zone="sh"}
│     . . . . . . . . . .   node_load1{host="host11",zone="sh"}
v
<------- 时间 ---------->
```

每一个点称为一个样本（sample），样本由三部分组成。

- 指标（metric）：metric name和描述当前样本特征的labelsets。
- 时间戳（timestamp）：一个精确到毫秒的时间戳。
- 值（value）：表示该时间样本的值。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（1）<div>请问：注册用户100万的网站，适合用Prometheus吗？</div>2023-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（2） 💬（2）<div>关于标签问题，之前写代码踩过很多坑，一查promql一大堆 T.T
后来自己总结的就是所有很难发生变化的数据写标签，但是别什么乱七八糟的都加进去，只写和业务有关的；变化频繁的值写到measurement。
</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（2） 💬（1）<div>absent(node_load1{instance=~&quot;.*&quot;})
absent_over_time(node_load1{job=&quot;node-exporter&quot;}[5m])

传递给absent的任意一个时间序列有值，那么整体 absent() 就是为空；
至于答案，还没有想到好的解决方案
</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/58/84/a8aac073.jpg" width="30px"><span>金尚</span> 👍（1） 💬（1）<div>老师我一次性想查询多个指标怎么做。例如：服务器的带宽，上下行速率，丢包数等。</div>2023-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（1） 💬（1）<div>思考题：通过参考了下absent文档，我的答案如下，烦请老师指正

如果我想对 100 台机器的 node_load1 做数据缺失告警，应该如何配置？
count(node_load1 offset 1h) by (instance) unless count(node_load1} ) by (instance)

absent不适合这个场景，因为absent表示指标的有无（存在与否）。
</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（1） 💬（1）<div>大年初一来过，祝大家新年快乐！</div>2023-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/b0/ab179368.jpg" width="30px"><span>hshopeful</span> 👍（1） 💬（1）<div>另外由思考题想到一个场景：在 prometheus 体系下怎么做监控和配置告警来监控服务器挂掉的场景，希望老师能提供几种思路并说说每种思路的优缺点</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/b0/ab179368.jpg" width="30px"><span>hshopeful</span> 👍（1） 💬（1）<div>思考题中：在没有其他 label 的情况下，直接在 prometheus 里面查询 absent(node_load1{})，得到的是 empty query result。在外面在封一层 absent 函数 absent(absent(node_load1{}))，可以得到指标 {} 的值为 0，这种场景下面，即使在告警中配置 {} 值 为 0 的告警真的触发了，也不确定到底是哪个指标无数据触发的，所以感觉这个需求使用 absent 并不合适；那么我认为适合使用 absent 的场景是指标拥有的 labelsets 集合能够代表指标的时候。不知道说的对不对，麻烦老师指正下，谢谢！</div>2023-01-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkGGBK46EQppJydxheC43vBzLqC0t0bpn08cNWW6XsLoRZsLvsR0zBgXAYcAcWDZyicHXOy4ffHsw/132" width="30px"><span>Geek_51809f</span> 👍（0） 💬（1）<div>老师你好， 文中提到 irate 是拿时间范围内的最后两个值来做计算，这个怎么理解的？方便举例说明一下吗</div>2023-03-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkGGBK46EQppJydxheC43vBzLqC0t0bpn08cNWW6XsLoRZsLvsR0zBgXAYcAcWDZyicHXOy4ffHsw/132" width="30px"><span>Geek_51809f</span> 👍（0） 💬（1）<div>老师你好！问一下 rate 是计算的每秒变化率？ 还是每秒变化数量？
举例 ：sum(rate(http_server_requests_seconds_count{application=&quot;$application&quot;, instance=&quot;$instance&quot;}[1m]))
这个是表示 每秒http请求增长数量？还是每秒http请求增长率？</div>2023-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/d1/bdf895bf.jpg" width="30px"><span>penng</span> 👍（0） 💬（1）<div>PromQL查询能够限制时间戳吗？比如我有些指标是1个月前的，在查询时会把他查出来，我现在不想查询它。结果为空就好</div>2023-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/72/b4/7420b047.jpg" width="30px"><span>hello</span> 👍（0） 💬（2）<div>老师您好，我们的业务指标用的prometheus + grafana，是这样的我们每天都有一个活跃uv统计，使用 counter 类型记入prometheus指标，我一直在寻找怎么看过去一周每天的uv总数，如果我使用1d的位移，grafana默认取每天8点的 value，而我想取的是每天最后一刻的值，直到我看到您这篇文章 我改成了 max_over_time(total_uv[1d]) ,  但是又引入了一个新的问题，每个横坐标日期展示的是前一天的指标值，不知道我是否有描述清楚，您是否有遇到这样的问题，有没有解决方案？ 总结一下，就是每天一个counter，取每天末最大的counter 绘图</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>思考题：如果我想对 100 台机器的 node_load1 做数据缺失告警，应该如何配置。

count(
  group(
    last_over_time(node_label1[10m])
  ) by (instance)
) &lt; 100

对于node label最近10分钟的数据按照 instance进行 group计数，如果数量小于 100，则报警。当然这个10分钟可以按需调节。</div>2023-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCrJQ4AZe8VrDkR6IO03V4Tda9WexVT4zZiahBjLSYOnZb1Y49JvD2f70uQwYSMibUMQvib9NmGxEiag/132" width="30px"><span>Dowen Liu</span> 👍（4） 💬（0）<div>能不能提供下 prometheus 的 tsdb snapshot 啊。可以本地导入做下实验，有问题也可以以统一的数据基础反馈提问。</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（1） 💬（0）<div>可不可以讲下prometheus 如何做动态扩展，保证高可用？如果需要数据可迁移，是不是就要搭建两个实例，然后这两个实例需要互通吗？谢谢</div>2023-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/21/b0fe1bfd.jpg" width="30px"><span>Adam</span> 👍（0） 💬（0）<div>absent(node_load1{instance=~&quot;.+&quot;})，是不是可以用predict_linear来预测,如果某个指标在预测的未来值中没有更新,可能意味着数据缺失。</div>2024-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（0） 💬（0）<div>关于increase rate这几个用到extrapolatedRate的函数 希望老师有空分析一下 看源码一直看的不是很懂</div>2023-03-05</li><br/>
</ul>