你好，我是秦晓辉。上一讲我们聊到了Prometheus的存储问题，并提出了3种增强方案，这一讲我们继续关注Prometheus的另一个问题——告警管理。

Prometheus的告警规则、记录规则都是采用配置文件的方式管理的，非常适合奉行Infrastructure as Code的公司或团队内部使用。但如果要把监控能力开放给全公司，就需要有较好的支持协同操作的 UI，让各个团队互不干扰的同时共享一些通用的成果。

解决这个需求的开源产品，有两款备选，一个是Grafana，另一个是夜莺（Nightingale）。Grafana擅长可视化，是监控绘图领域事实上的标准，而夜莺的侧重点是告警管理，所以这一讲我们重点来介绍一下夜莺，**我们可以通过夜莺搭建公司级的监控系统，把监控告警能力赋予公司所有的团队。**

## 夜莺简介

夜莺最初是滴滴开源的，之后捐赠给了中国计算机学会开源发展委员会（CCF ODC），目标是整合云原生开源生态的众多能力，为用户提供开箱即用、一体化全方位的云原生监控解决方案。

注：点击查看[夜莺的GitHub地址](https://github.com/ccfos/nightingale)和[文档地址](https://n9e.github.io/)

我们先来看一下夜莺的架构，对夜莺的工作模式有个基本的认识。

![图片](https://static001.geekbang.org/resource/image/41/f9/41a846502810df2e0dyyac2a4yy978f9.png?wh=1920x1287 "夜莺的单机部署架构（图片源自Nightingale官网）")

左下角 Agents 表示监控数据采集器，夜莺可以对接多种 Agent，比如 Categraf、Telegraf、Grafana-Agent、Datadog-Agent。这些 Agent 都是 PUSH 模型，周期性采集监控数据，然后推给 Server 的 HTTP 接口。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_1a3949</span> 👍（3） 💬（3）<div>尝试回答下课后问题：

告警表达式是带判断的PromQL，查询到值表示触发了阈值，查询不到表示未触发；
而告警恢复的时候，PromQL表达式返回空值，故没有$value。</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/29/95/13893803.jpg" width="30px"><span>骁毅</span> 👍（2） 💬（2）<div>“因为 Prometheus 的 Yaml 文件管理方式不太方便做公司级协同管理。Grafana 和夜莺都可以解决这个问题，”  grafana可以对prometheus的yaml进行管理么？</div>2023-02-19</li><br/><li><img src="" width="30px"><span>KEIO</span> 👍（2） 💬（3）<div>老师 请教一下 可以对比一下Grafana和Altermanager的告警管理能力吗？</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（1） 💬（1）<div>快猫的采集器我觉得很好，基本覆盖了常用服务的数据采集，只需要修改配置一下就可以了。但是我有一个疑惑，比如我监控几百台服务器，每台服务器有可能有不同的服务需要被采集，如果这样子的话，快猫服务采集的那些配置文件如何管理呢？用表格来做扁平化管理嘛。</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e9/26/472e16e4.jpg" width="30px"><span>Amosヾ</span> 👍（1） 💬（1）<div>原生k8s支持告警自愈吗？webhook的方式</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：server与Redis之间的心跳有什么作用？
Q2：webapi没有界面吗？
“Webapi 模块提供 HTTP 接口，与前端 JavaScript 交互”，从这句话看，好像webapi没有界面。
“浏览器访问 nwebapi 提供的 18000 端口就能看到登录页面”，从这句话看，好像webapi有界面。
Q3：架构图中，agents和exporter都采集数据，有什么区别？
Q4：Prometheus和Nightingale都可以处理告警，采用Nightingale后，就禁掉Prometheus自身的告警功能，是这样吗？</div>2023-01-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRVT3U6UOpRAoOOYMm0flMeX4P1VJpSnZBlaBvdW4KhWKr0BunLFlCxibdHc9s6VArA124FpwzRiaw/132" width="30px"><span>guoqp</span> 👍（0） 💬（2）<div>老师，夜莺的告警聚合怎么做</div>2024-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ab/86/6484136d.jpg" width="30px"><span>stray</span> 👍（0） 💬（1）<div>现在使用的是peometheus的采集器，想改成categraf，如何能实现平滑变更，变更完后监控图表等都不变，减少对客户的影响。</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/25/bc/910b4e25.jpg" width="30px"><span>机智的路易</span> 👍（0） 💬（1）<div>老师你好，我们公司最近在调研夜莺，请问边缘侧server端拉prometheus，如果server挂了怎么办，server需要保证高可用吗？</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/a4/ce/1e19f399.jpg" width="30px"><span>祥贵</span> 👍（0） 💬（1）<div>夜莺分为开源版和企业版，开源版能解决这些问题？</div>2023-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/56/abb7bfe3.jpg" width="30px"><span>云韵</span> 👍（0） 💬（2）<div>docker 部署的方式不支持Mac的arm64架构吗</div>2023-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/cd/4f/7d4d6fe4.jpg" width="30px"><span>GentleQ</span> 👍（0） 💬（3）<div>老师，请问告警检测是在Agent推指标到Server时做的，还是Server定期从Prometheus里拉指标进行检测的呢</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/75/2b599841.jpg" width="30px"><span>SICUN</span> 👍（0） 💬（2）<div>老师能不能谈一下边沿触发告警和周期触发告警的适用场景？</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（0） 💬（1）<div>请教一下老是，夜莺左侧的监控对象，我添加了快猫的采集，集群名称为啥都是Default，如何修改呢？</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/4e/88/791d0f5e.jpg" width="30px"><span>lei</span> 👍（0） 💬（1）<div>请教老师，我司也在打算研发一个成熟的监控平台。然而像关联分析，您在前面提过的：在虚机管理控制台可以查到宿主，宿主旁边加个看图的按钮，点击可以看宿主的监控数据，通过宿主还能看到虚机的列表，每个虚机旁边也有看图的按钮。
我能想到的就是基于api纯二次开发，可是想想工作量确实有些大。那基于夜莺或者Grafana，类似这样的功能，有什么好的建议吗？谢谢！</div>2023-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ab/86/6484136d.jpg" width="30px"><span>stray</span> 👍（0） 💬（0）<div>请问原来使用的prometheus的exporter，现在想改成categraf采集器，如何能实现平滑的进行迁移？比如一个按钮，点击后就实现了采集器的替换，监控图表和告警都保持不变？减少用户的影响。</div>2024-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（0） 💬（0）<div>是保存回复值么</div>2023-01-25</li><br/>
</ul>