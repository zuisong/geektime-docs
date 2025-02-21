你好，我是秦晓辉。

前面几讲我们介绍了 MySQL、Redis、Kafka、Elasticsearch 这些常见组件的监控方法，相信你对各类中间件的典型监控逻辑已经有了一定的认识。接下来我要介绍的是云原生时代的扛把子 Kubernetes 的监控，云原生这个词就是随着 Kubernetes 火起来的。Kubernetes 架构比较复杂，我会用两讲的时间来分享。

虽然网上可以找到基于 Prometheus 做的 Operator，一键监控 Kubernetes，但是很多人仍然不知其所以然，这两讲我会按照组件粒度掰开来讲，争取让你理解其中的原理，至于后面你用什么工具来落地，那都是技术的层面了，好办。

要监控 Kubernetes，我们得先弄明白 Kubernetes 有哪些模块要监控，所以我们先来看一下 Kubernetes 的架构。

## Kubernetes 架构

下面是 Kubernetes 的架构图，用户交互部分是 UI 和 CLI，这两个不需要监控，关键是**Control plane（控制面）和 Worker node（工作负载节点）**。控制面的组件提供了管理和调度能力，如果控制面组件出了问题，我们就没法给 Kubernetes 下发指令了。工作负载节点运行了容器，以及管理这些容器的运行时引擎（图上的 Docker）、管理 Pod 的 Kubelet，以及转发规则的 Kube-Proxy。工作负载节点如果出问题，可能会直接影响业务流量，所以对这类节点的监控就显得更为重要了。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_1a3949</span> 👍（3） 💬（1）<div>尝试回答一下课后题：

使用group_left，为container_*添加kube_pod_labels标签
container_fs_writes_bytes_total * on(namespace, pod) group_left(label_region, label_dept) kube_pod_labels</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（0） 💬（1）<div>老师请教一下，我如何监控所有的pod，只要pod异常我就报警呢？</div>2023-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5d/52/21275675.jpg" width="30px"><span>隆哥</span> 👍（0） 💬（1）<div>老师请教一下，ServiceAccount在k8s高版本我是1.26.0版本，无法自动创建secret，如果是自己手动创建secret的话，是帐号密码形式的嘛，如果自己创建secret</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（0） 💬（1）<div>公司准备搭建自己的运维监控系统 怎么把老师讲的这些结合起来？老师介绍了监控数据采集 存储 但是运维系统搭建 原型上 我感觉有点懵逼</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：Go程序指标只对Go程序有效吗？
Kube-proxy的Go程序指标，是针对Go应用吗？如果不是Go应用呢？比如Java应用就不会有这个指标吧。
Q2：[1m]是什么意思？
多个指标后面有”[1m]”，比如：irate(container_network_transmit_bytes_total[1m])，是表示1分钟吗？
Q3：监控大盘的配置是categraf内置的吗？
文中提到“Categraf 内置了 Kube-Proxy 的监控大盘；
Categraf 内置了 Kubelet 的监控大盘；Categraf 也提供了容器的监控大盘。”点开链接后，是一个json格式的配置文件。请问：这些配置文件是categraf本身就有的吗？
Q4：配置文件所在的github链接是专栏的吗？
问题三中提到的几个监控大盘，都对应一个github链接，https:&#47;&#47;github.com&#47;flashcatcloud这个链接是本专栏自己的吗？还是一个开源项目？</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/25/19cbcd56.jpg" width="30px"><span>StackOverflow</span> 👍（1） 💬（1）<div>在 k8s 1.24之后的版本，创建的 serviceaccount 没有自动生成 secret，需要手动创建一个</div>2023-03-01</li><br/>
</ul>