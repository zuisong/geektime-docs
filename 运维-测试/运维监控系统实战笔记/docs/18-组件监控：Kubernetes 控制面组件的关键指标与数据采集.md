你好，我是秦晓辉。

上一讲我们介绍了 Kubernetes **工作负载节点**的监控，了解了 Kube-Proxy、Kubelet、容器负载监控的方法。这一讲我们介绍**控制面组件**的监控，包括 APIServer、Controller-manager（简称CM）、Scheduler、etcd 四个组件，我会讲解这几个组件监控数据的采集方法和关键指标，并给出监控大盘。此外，我们还会学习如何使用 kube-state-metrics（简称KSM）来监控Kubernetes 的各类对象。

## 数据采集

自行搭建 Kubernetes 控制面的朋友，大都是选择 Kubeadm 这样的工具，Kubeadm 会把控制面的组件以静态容器的方式放到容器里运行，之后我会重点给你演示在这种部署方式下如何采集监控数据。

不过很多大一些的互联网公司会选择直接使用二进制的方式来部署，因为二进制的方式对于监控数据采集来说其实更简单，直接在采集器里配置要抓取的这几个组件的目标地址就可以了。

如果想要调用 Kubernetes 服务端 APIServer、Controller-manager、Scheduler 这三个组件的 `/metrics` 接口，需要有 Token 做鉴权，我们还是通过创建 ServiceAccount 的方式拿到 Token，后面也会把采集器直接部署到 Kubernetes 容器里，这样 Token 信息就可以自动 mount 到容器里，比较方便。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_1a3949</span> 👍（4） 💬（1）<div>尝试回答一下课后题：

可以为prometheus增加global.external_labels配置，增加cluster的标识以区分不同的集群：
global:
  external_labels:
    cluster:  prod-bigdata-sh
    ....

另外，请教老师一个问题，ksm的分片，官网上有statefulset、daemonset的分片方式，它们各自的适用场景是什么，在生产环境下，更推荐哪种方式？

</div>2023-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/ff/ed/791d0f5e.jpg" width="30px"><span>胡飞</span> 👍（1） 💬（1）<div>你好老师，promtheus 如果开启了remote write后，存储会用两份吗？prom本地一份数据，第三方一份数据？</div>2023-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：KSM是k8s自身的组件吗？还是一个第三方的软件？
Q2：一般性的问题，公司的实际运营中，日志数据一般保存多长时间？指标数据一般保存多长时间？（到期后是直接删除数据吧）</div>2023-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9f/b7/8b1c1b3b.jpg" width="30px"><span>姜兵</span> 👍（0） 💬（1）<div>老师您好，想问一下，生产上的各类指标开启秒级采集的话，一般最小设置为多少秒可以确保采集性能和告警的及时性？</div>2023-07-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJiaxxRyl13SvqsqWuhtJHWMVRMeIo7byfJ0AaicwcRvibcfw0DSrGHFVz7dhwicBJNsFSFRk4kuia28jQ/132" width="30px"><span>k8s卡拉米</span> 👍（0） 💬（1）<div>老师您好，采集work组件是后，您这篇文章中使用的是把prometheus当做agent，部署的这个采集的prometheus 是仅仅做采集使用吗？，我在其他机器上已经部署了prometheus用户和n9e和这个采集的prometheus 没关系是吗？</div>2023-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（0） 💬（1）<div>自己做监控系统 但是用了公有云产品 比如华为云的k8s 请问怎么监控哈 公司都是用公有云saas 自己公司卖paas产品</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/06/ff/e4828765.jpg" width="30px"><span>LiLian</span> 👍（0） 💬（1）<div>请问老师：&quot;prometheus agent mode，支持 Kubernetes 服务发现&quot;  本质上还是通过list &amp; watch 监听来自api server的信息吗？ </div>2023-02-24</li><br/><li><img src="" width="30px"><span>Geek_7656a8</span> 👍（0） 💬（0）<div>老师好； 采集到集群调度信息，但是 scheduler (0 &#47; 8767 active targets)；这是什么情况？ 数据没有推到远端的prometheus</div>2023-06-21</li><br/>
</ul>