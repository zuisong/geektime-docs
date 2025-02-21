你好，我是张磊。今天我和你分享的主题是：Prometheus、Metrics Server与Kubernetes监控体系。

通过前面的文章，我已经和你分享过了Kubernetes 的核心架构，编排概念，以及具体的设计与实现。接下来，我会用3篇文章，为你介绍 Kubernetes 监控相关的一些核心技术。

首先需要明确指出的是，Kubernetes 项目的监控体系曾经非常繁杂，在社区中也有很多方案。但这套体系发展到今天，已经完全演变成了以Prometheus 项目为核心的一套统一的方案。

在这里，可能有一些同学对 Prometheus 项目还太不熟悉。所以，我先来简单为你介绍一下这个项目。

实际上，Prometheus 项目是当年 CNCF 基金会起家时的“第二把交椅”。而这个项目发展到今天，已经全面接管了 Kubernetes 项目的整套监控体系。

比较有意思的是，Prometheus项目与 Kubernetes 项目一样，也来自于 Google 的 Borg 体系，它的原型系统，叫作BorgMon，是一个几乎与 Borg 同时诞生的内部监控系统。而 Prometheus 项目的发起原因也跟 Kubernetes 很类似，都是希望通过对用户更友好的方式，将 Google 内部系统的设计理念，传递给用户和开发者。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/84/c1/dfcad82a.jpg" width="30px"><span>Acter</span> 👍（25） 💬（1）<div>1.老师能讲下prometheus的部署方式吗？比如helm部署，operator部署，过程中具体发生了什么？
2.能否解析下prometheus server配置文件中，jobs的写法，alert rule的写法？还有alertmanager的配置。感谢</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/67/df/8b85d0d9.jpg" width="30px"><span>--</span> 👍（5） 💬（1）<div>核心监控数据是Prometheus通过Metric Server拉取的还是直接从kubelet拉取？</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/cd/c723f8f4.jpg" width="30px"><span>leisland</span> 👍（1） 💬（1）<div>老师您好，我想请教你一个k8s问题。我们使用liveness probe探针检查容器健康状态，这个探针执行的是容器里一个脚本。当容器内存和CPU过载时这个脚本会一直执行卡死然后超时。现在看k8s好像不认为执行超时是失败，在不停的去执行脚本。从而检查不到容器异常了，容器一直不重拉起。我们设置失败上限是3次，应该没起作用。请问有没有办法可以解决呢？业界都是怎么使用探针的呢？</div>2020-03-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eo6TmyGF3wMIRLx3lPWOlBWusQCxyianFvZvWeW6hYCABLqEow3p7tGc6XgnqUPVvf6Cbj2KUYQIiag/132" width="30px"><span>孙健波</span> 👍（59） 💬（4）<div>Pull和Push两种模式的区别非常有意思，Prometheus非常大胆的采用了pull的模式，但是仔细思考后就会觉得非常适合监控的场景。

Pull模式的特点
1. 被监控方提供一个server，并负责维护
2. 监控方控制采集频率

第一点其实对用户来说要求过高了，但是好处很多，比如pull 不到数据本身就说明了节点存在故障；又比如监控指标自然而言由用户自己维护，使得标准化很简单。
第二点其实更为重要，那就是监控系统对metric采集的统一和稳定有了可靠的保证，对于数据量大的情况下很重要。


缺点也很明显，用户不知道你什么时候来pull一下，数据维护多久更新也不好控制，容易造成一些信息的丢失和不准确。

当把这些优缺点权衡过后就会发现，纯监控的场景确实是适合pull的
</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ab/c9/b1b48878.jpg" width="30px"><span>Goswing</span> 👍（15） 💬（0）<div>Push模式的优点是在正常情况下数据的延迟可以做到更低，也就是能更快的获取metrics并发现问题，而pull模式一般不会设定很短的轮询时间，所以延迟更高一些。

Push模式的缺点我能想到以下几个: 
1 增加了服务的实现复杂度(比如推送错误处理等); 
2 不利于平行扩展; 
3 不支持自定义metrics采集策略，比如高峰期减少采集频率。</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（13） 💬（0）<div>pull是拉动作，监听者主动调用被监听者的接口
push是推动作，被监听者主动上报，监听者被动采集
拉动作有助于监听者自己控制频率和采样量，缺点是需要掌握所有被监听者的地址和端口，也就是要有注册中心；
推动作有利于被监听者自己控制上报数量和频率，但有可能对监听者构成额外的压力，同时有信息丢失的风险</div>2019-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/4e/83d6ddce.jpg" width="30px"><span>CalvinXiao</span> 👍（9） 💬（0）<div>push 方式针对没有 http 接口应用，例如 worker，可以设定每 5 秒上报处理了多少个 job，平均每个 job 耗时多少，有多少个错误等数据，需要配合 push gateway 使用。

当然，也可以自己写一个 exporter 通过查询日志来得到这些数据，然后用 pull 方式来获取。push 方式可以联想到 APM。</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9f/fc/0232f005.jpg" width="30px"><span>我要收购腾讯</span> 👍（6） 💬（0）<div>prometheus 的pull模式搭配自己的kubernetes SD, 加上prometheus-operator的service monitor的抽象，可以很大程度的简化配置的复杂程度</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/f9/bfb54326.jpg" width="30px"><span>狮锅艺</span> 👍（5） 💬（0）<div>文中缺少的链接：https:&#47;&#47;github.com&#47;kubernetes&#47;kubernetes&#47;blob&#47;master&#47;cluster&#47;kube-up.sh</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/37/3b/495e2ce6.jpg" width="30px"><span>陈斯佳</span> 👍（4） 💬（0）<div>第四十六课:Prometheus、Metrics

Prometheus 项目工作的核心，是使用 Pull （抓取）的方式去搜集被监控对象的 Metrics 数据（监控指标数据），然后，再把这些数据保存在一个 TSDB （时间序列数据库，比如 OpenTSDB、InfluxDB 等）当中，以便后续可以按照时间进行检索。

Metrics数据来源种类有:
第一种是宿主机的监控数据。最主要是借助Node Exporter，以DaemonSet的方式运行在宿主机上，收集包括节点负载（Load）,CPU,内存，磁盘以及网络这些常规信息。
第二种是来自于K8s的API Server,kubelet等组建的&#47;metrics API 。除了常规的 CPU、内存的信息外，这部分信息还主要包括了各个组件的核心监控指标。比如，对于 API Server 来说，它就会在 &#47;metrics API 里，暴露出各个 Controller 的工作队列（Work Queue）的长度、请求的 QPS 和延迟数据等等。这些信息，是检查 Kubernetes 本身工作情况的主要依据。
第三种 Metrics，是 Kubernetes 相关的监控数据。这部分数据，一般叫作 Kubernetes 核心监控数据（core metrics）。这其中包括了 Pod、Node、容器、Service 等主要 Kubernetes 核心概念的 Metrics。其中，容器相关的 Metrics 主要来自于 kubelet 内置的 cAdvisor 服务。在 kubelet 启动后，cAdvisor 服务也随之启动，而它能够提供的信息，可以细化到每一个容器的 CPU 、文件系统、内存、网络等资源的使用情况。

Metrics Server 在 Kubernetes 社区的定位，其实是用来取代 Heapster 这个项目的。有了 Metrics Server 之后，用户就可以通过标准的 Kubernetes API 来访问到这些监控数据了。Metrics Server 并不是 kube-apiserver 的一部分，而是通过 Aggregator 这种插件机制，在独立部署的情况下同 kube-apiserver 一起统一对外服务的。kube-aggregator 其实就是一个根据 URL 选择具体的 API 后端的代理服务器。

USE 原则指的是，按照如下三个维度来规划资源监控指标：
1. 利用率（Utilization），资源被有效利用起来提供服务的平均时间占比；
2. 饱和度（Saturation），资源拥挤的程度，比如工作队列的长度；
3. 错误率（Errors），错误的数量。

RED 原则指的是，按照如下三个维度来规划服务监控指标：
1. 每秒请求数量（Rate）；
2. 每秒错误数量（Errors）；
3. 服务响应时间（Duration）。

USE 原则主要关注的是“资源”，比如节点和容器的资源使用情况，而 RED 原则主要关注的是“服务”，比如 kube-apiserver 或者某个应用的工作情况。这两种指标，在我今天为你讲解的 Kubernetes + Prometheus 组成的监控体系中，都是可以完全覆盖到的。</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/41/37/b89f3d67.jpg" width="30px"><span>我在睡觉</span> 👍（3） 💬（1）<div>我认为拉取的最大好处是解耦，metric server对外提供标准接口，第三方实现自己的监控逻辑。还有部署的时候更方便，如果使用push的方式，那么部署一个监控组件之后需要用某种方式配置metric server，让他知道一个监控服务的存在以便通知上报数据，这样对于监控数据描述的配置文件都要配置到metric server（metric server也需要实现逻辑来处理这些配置），这显然增加了使用的复杂度，也不不够灵活。</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/79/2fde8492.jpg" width="30px"><span>李伟达</span> 👍（3） 💬（1）<div>有一个问题，就是metric server是怎么注册给metrics.k8s.io&#47;v1beta1这个api的，或者说当client访问metrics.k8s.io&#47;v1beta1这个api时，aggregator如何知道转发给哪个后端？</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/32/af5db71f.jpg" width="30px"><span>kindule</span> 👍（3） 💬（1）<div>你好，为什么node_exporter要单独分为一类而不是算作core metrics</div>2019-03-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLyfjHfjulibFGPTewSZZHm2M8yfI7BZmO9vLUFoagveCw3DWYDss7y1CecKia7lT5yb9KoAmsya2zg/132" width="30px"><span>Goteswille</span> 👍（2） 💬（0）<div>坚持、打卡</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/b2/89aae33a.jpg" width="30px"><span>志远</span> 👍（1） 💬（0）<div>pull模式由prometheus中心化管理数据收集，方便管理和后续维护，但是prometheus server的压力较大；
push模式由pushgateway接受target推送上来的数据，prometheus server的压力较小，但是每个target均需要配置推送pushgateway的配置，如果target数量较多，后续的配置管理将比较麻烦；</div>2024-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（1） 💬（0）<div>老师好，请问在拉模式下，prometheus是如何「发现」采集点的呢？谢谢</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/a2/6ea5bb9e.jpg" width="30px"><span>LEON</span> 👍（1） 💬（0）<div>老师我一直对Prometheus和SNMP server有什么区别搞不明白。这俩是一个东西吗？他们有什么具体的区别？是不是可以理解为SNMP server是Prometheus的一个子集？</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5c/65/27fabb5f.jpg" width="30px"><span>茗</span> 👍（0） 💬（0）<div>有没有大佬解释下，我运行时用的docker，k8s版本1.26。3,然后grafana里Compute Resource相关的数据面板都是nodata</div>2024-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/4e/82e9657c.jpg" width="30px"><span>jeff</span> 👍（0） 💬（0）<div>太草草了事了</div>2023-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（1）<div>Prometheus的时序数据存储依赖于第三方TSDB吗？目前这块没有像关系型数据库MySQL这样的王者啊。OpenTSDB性能非常一般，运维也比较复杂，InfluxDB社区版本只有单机版本。</div>2022-01-26</li><br/><li><img src="" width="30px"><span>Geek_089889</span> 👍（0） 💬（0）<div>Metric和链路trace 使用什么方案关联起来？为后续功能做分析支撑，</div>2021-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/6d/9e/6a82a5ea.jpg" width="30px"><span>good boby</span> 👍（0） 💬（0）<div>damonset对象可以方便提供prometheus的各个节点监控</div>2021-05-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/RxZc4ZGUwpUp5grZqJEtjgWXTgMicjmQsQByACCAmuUibJ6NZsI90IYiaOwEejy3TiaxEb2BbByve1dicNnGRgicFtFw/132" width="30px"><span>Geek_6a11b8</span> 👍（0） 💬（0）<div>想问一下怎么向controller manager的metrics接口添加metric，使调用接口后，可以返回自定义metric</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（0） 💬（0）<div> 我更加倾向于使用Push的模式,因为使用Pull的话,可能会导致频率时间短的情况下,对Server的造成巨大的压力</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/c2/41fa26df.jpg" width="30px"><span>楊威</span> 👍（0） 💬（1）<div>请教一个问题,查看apiversion里面有autoscaling&#47;v2beta2，但是通过yaml文件创建hpa之后自动就变成了autoscaling&#47;v1，这是为何？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/62/72296b09.jpg" width="30px"><span>小雨</span> 👍（0） 💬（0）<div>做超时异常退出</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8c/49/791d0f5e.jpg" width="30px"><span>clivexiang</span> 👍（0） 💬（0）<div>pull push 作用都是在收集被监控对象的数据
 
pull 拉取被监控对象的数据 
        收集 想要的数据 监控汇总 服务器实时的运行状况
到被监控的对象多 ，需要的服务器的资源大 如cpu,内存
push  主动推送数据，如服务器异常， 或主动收集想要的数据 
方便在定制消息的推送
      异常错误，可以及时上报</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b9/f5/ffc2bb23.jpg" width="30px"><span>Rodinian</span> 👍（0） 💬（0）<div>按照课里的方式，基于kubeadm部署了k8s集群，但是metrics server总是没办法正常工作。unable to fetch node metrics for node &quot;node-hostname&quot;: no metrics known for node   直接在宿主机去ping都是能ping通的</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/ea/0d7b8cdc.jpg" width="30px"><span>Vincent</span> 👍（0） 💬（0）<div>kube-up.sh 脚本的链接没设置好</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e9/91/4219d305.jpg" width="30px"><span>初学者</span> 👍（0） 💬（0）<div>老师，prometheus server pull 的core metrics信息是从metric server拿到，还是从kubelet的接口拿？还有metric server 中存储历史监控数据吗？</div>2018-12-21</li><br/>
</ul>