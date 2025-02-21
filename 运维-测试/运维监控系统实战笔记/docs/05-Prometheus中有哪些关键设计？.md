你好，我是秦晓辉。

上一讲我们介绍了如何搭建 Prometheus 系统，演示了基本的使用方法，这一讲我们深入进去，梳理一下 Prometheus 的关键设计，看看这些设计是如何奠定 Prometheus 江湖地位的。

![](https://static001.geekbang.org/resource/image/c2/b2/c2c67694da6bb16fa0cf7318abd0c5b2.jpg?wh=1601x859)

## 标准先行，注重生态

Prometheus 最重要的规范就是**指标命名方式**，数据格式简单易读，在[第2讲](https://time.geekbang.org/column/article/620800)中我们已经聊过了，它用标签集来标识指标。有些监控系统会把一些特殊的字段单独提出来，最典型的就是 hostname 字段，这种做法在一些特定场景会显得更有效。但是显然，**统一的标签集表达方式是最通用、最灵活的。**

虽然标签集很灵活，但是在实际落地时，我强烈建议你在公司推行一个标签定义规范，标签Key不能随便起名，该有的标签也不能缺失。既减少了理解成本，也保证了数据的规整完备，便于后续做数据分析。比如，对于应用层面的监控，可以要求必须具备这几个信息。

- 指标名称 metric

Prometheus内置建立的规范就是叫metric（即\_\_name\_\_）。如果是Counter类型，单调递增的值，指标名称以\_total结尾。

- 服务名称 service

服务名称service要全局唯一，比如 n9e-webapi，p8s-alertmanager，一般是系统名称加上模块名称，组成最终的服务名称。如果公司比较大，就需要一个全局的服务目录做参考，否则不同的团队可能会起相同的名称，我们可以考虑使用 Git 里的 GroupName + RepoName。系统名称最好也单独做成一个标签，比如 system=n9e system=p8s。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/5e/45/50424a7a.jpg" width="30px"><span>叶夏</span> 👍（29） 💬（3）<div>可以把Prometheus的配置yaml和告警规则yaml单独放到一个代码仓库中，把这个仓库向有需要的人开放，如果他们想要添加某一个规则，就自己修改提交PR，提交PR的部署到测试环境，验证没有问题，prometheus owner 审核PR之后合并到master分支中，这个时候在自动部署到生产环境，我们是这么做的，感觉蛮好的</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（9） 💬（1）<div>Prometheus 数据的存储按冷热数据进行分离，最近的数据肯定是看的最多的，所以缓存在内存里面，为了防止宕机而导致数据丢失因而引入 wal 来做故障恢复。数据超过一定量之后会从内存里面剥离出来以 chunk 的形式存放在磁盘上这就是 head chunk。对于更早的数据会进行压缩持久化变成 block 存放到磁盘中。

对于 block 中的数据由于是不会变的，数据较为固定，所以每个 block 通过 index 来索引其中的数据，并且为了加快数据的查询引用倒排索引，便于快速定位到对应的 chunk。</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/05/73/89148275.jpg" width="30px"><span>Ishmael</span> 👍（5） 💬（1）<div>我觉得最绝的还是限制值必须为float这点，限制死了之后保证了数据的高压缩度，进一步保证了计算性能和存储空间的节省。同时wal和分级存储也很绝，kv设计的思路也很不错。tag这个设计在实际接入中帮了大忙。</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ff/ed/791d0f5e.jpg" width="30px"><span>胡飞</span> 👍（1） 💬（1）<div>在k8s模式下部署，配置采用yaml缺点就出来了，一套环境大家都有弄，改错了，甚至缩进写错了都会造成pod重启失败。后面采用servicemonitor&#47;podmonitor 感觉就好多了</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（0） 💬（1）<div>对于一些特殊场景导致的promql 0&#47;0 的情况，在老东家遇到过windows实例 cpu利用率偶尔出现0&#47;0的情况。
这种0&#47;0好像promql没有很好的处理方法（后来排查问题大概率是镜像有bug），当时是用&quot;or&quot;临时解决了问题
现在想想，采集侧是否可以加入数据预处理呢？比如说遇到极度不合理的数值给他一个默认值？希望秦老师解答 🤣🤣🤣🤣</div>2023-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（0） 💬（1）<div>在pull的时候是单线程还是多线程，这方面会出现瓶颈吗</div>2023-02-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/f2kMO4JlbHCfR4tJuibUS1iazgkiaFymkKQgEl69c36cTKXgIMAibrT1SkjTYf5oOvWxcENGFW6eU3efaSGufDLprw/132" width="30px"><span>Geek_a99361</span> 👍（0） 💬（1）<div>Prometheus使用本地存储的方式有一些局限性，远端存储有什么推荐？比如 clickhouse或者influxDB</div>2023-01-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKicaBCtrCtnyCEicU8SZJLgRa9gicmhiaWF5krYdWRHkMbALz3tQBxOOj2Eia4DoQw1Vcvib8N5Vy7jvPg/132" width="30px"><span>irving</span> 👍（0） 💬（1）<div>telegraf是拉模式吗？telegraf中的各个plugin都要配置influxdb的地址，应该是push模式吧</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/b0/ab179368.jpg" width="30px"><span>hshopeful</span> 👍（0） 💬（1）<div>基于gorilla的时序数据压缩算法很经典</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>Q1：Prometheus是用什么开发的？JAVA吗？
Q2：Prometheus代码规模有多大？百万行代码？</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（1） 💬（0）<div>推和拉，有很大区别</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/c8/5ce842f6.jpg" width="30px"><span>maybe</span> 👍（0） 💬（0）<div>还有就是失联告警问题，拉模式很容易感知到目标失联。推模式就比较复杂了，需要对数据缺失做告警，比如 Prometheus 的 absent 函数，absent 函数需要把指标的每个标签都写全，才能达到预期效果。而指标数量何止千万，几乎不可能完成。 这个不太懂</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bb/67/a798d432.jpg" width="30px"><span>Ecoder</span> 👍（0） 💬（0）<div>Prometheus的数据模型和时序库也很经典</div>2023-01-18</li><br/>
</ul>