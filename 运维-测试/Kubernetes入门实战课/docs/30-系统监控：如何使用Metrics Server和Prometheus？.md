你好，我是Chrono。

在前面的两节课里，我们学习了对Pod和对集群的一些管理方法，其中的要点就是设置资源配额，让Kubernetes用户能公平合理地利用系统资源。

虽然有了这些方法，但距离我们把Pod和集群管好用好还缺少一个很重要的方面——集群的可观测性。也就是说，我们希望给集群也安装上“检查探针”，观察到集群的资源利用率和其他指标，让集群的整体运行状况对我们“透明可见”，这样才能更准确更方便地做好集群的运维工作。

但是观测集群是不能用“探针”这种简单的方式的，所以今天我就带你一起来看看Kubernetes为集群提供的两种系统级别的监控项目：Metrics Server和Prometheus，以及基于它们的水平自动伸缩对象HorizontalPodAutoscaler。

## Metrics Server

如果你对Linux系统有所了解的话，也许知道有一个命令 `top` 能够实时显示当前系统的CPU和内存利用率，它是性能分析和调优的基本工具，非常有用。**Kubernetes也提供了类似的命令，就是 `kubectl top`，不过默认情况下这个命令不会生效，必须要安装一个插件Metrics Server才可以。**

Metrics Server是一个专门用来收集Kubernetes核心资源指标（metrics）的工具，它定时从所有节点的kubelet里采集信息，但是对集群的整体性能影响极小，每个节点只大约会占用1m的CPU和2MB的内存，所以性价比非常高。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（14） 💬（9）<div>操作中遇到的问题以及解决办法
1: metris-server如果出现执行命令 kubectl top 不生效可以加如下配置
	apiVersion: apps&#47;v1
	kind: Deployment
	metadata:
	 ...
	  
	  template:
	    ....
	    spec:
	      nodeName: k8s-master #你自己的节点名称

2: prometheus 镜像问题
   这里我偷懒，不用骑驴找驴了，直接用老师的

   这里我建议您push到docker hub (因为集群有多个节点，push到docker hub上，这样pod调度到任意一个节点都可以方便下载)

   docker pull chronolaw&#47;kube-state-metrics:v2.5.0
   docker tag chronolaw&#47;kube-state-metrics:v2.5.0 k8s.gcr.io&#47;kube-state-metrics&#47;kube-state-metrics:v2.5.0
   docker rmi chronolaw&#47;kube-state-metrics:v2.5.0
   docker push k8s.gcr.io&#47;kube-state-metrics&#47;kube-state-metrics:v2.5.0


   prometheus-adapter 老师的版本运行不起来，我在docker hub上 找了一个可以用的

   docker pull pengyc2019&#47;prometheus-adapter:v0.9.1
   docker tag pengyc2019&#47;prometheus-adapter:v0.9.1 k8s.gcr.io&#47;prometheus-adapter&#47;prometheus-adapter:v0.9.1
   docker rmi pengyc2019&#47;prometheus-adapter:v0.9.1
   docker push k8s.gcr.io&#47;prometheus-adapter&#47;prometheus-adapter:v0.9.1

然后执行：
	kubectl create -f manifests&#47;setup
	kubectl create -f manifests

 到此，运行成功
</div>2022-09-06</li><br/><li><img src="" width="30px"><span>邵涵</span> 👍（9） 💬（1）<div>在使用hpa做自动扩容&#47;缩容时，遇到了只扩容不缩容的问题，具体情况如下：
1. 按文中的步骤，使用ab加压，可以看到pod增加到了10个
[shaohan@k8s4 ~]$ kubectl get hpa ngx-hpa -w
NAME      REFERENCE                TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
ngx-hpa   Deployment&#47;ngx-hpa-dep   150%&#47;5%   2         10        2          90s
ngx-hpa   Deployment&#47;ngx-hpa-dep   129%&#47;5%   2         10        4          105s
ngx-hpa   Deployment&#47;ngx-hpa-dep   93%&#47;5%    2         10        8          2m
ngx-hpa   Deployment&#47;ngx-hpa-dep   57%&#47;5%    2         10        10         2m15s
2. 在ab停止运行之后过了几分钟，kubectl get hpa ngx-hpa -w的输出中才出现了一行新数据，如下
ngx-hpa   Deployment&#47;ngx-hpa-dep   0%&#47;5%     2         10        10         7m31s
仍然是10个pod，并没有自动缩容
3. 查看pod
[shaohan@k8s4 ~]$ kubectl get pod
NAME                           READY   STATUS    RESTARTS     AGE
ngx-hpa-dep-86f66c75f5-d82rh   0&#47;1     Pending   0            63s
ngx-hpa-dep-86f66c75f5-dtc88   0&#47;1     Pending   0            63s
（其他ngx-hpa-dep-xxx省略，因为评论字数限制……）
test                           1&#47;1     Running   1 (6s ago)   2m5s
可以看到，有两个pod是pending状态的，kubectl describe这两个pending pod中的一个，可以看到
Warning  FailedScheduling  18s (x2 over 85s)  default-scheduler  0&#47;2 nodes are available: 1 Insufficient cpu, 1 node(s) had taint {node-role.kubernetes.io&#47;master: }, that the pod didn&#39;t tolerate.
是因为worker节点资源不足，master节点没有开放给pod调度，造成扩容时有两个pod虽然创建了，但一直在等待资源而没有进入running状态
4. 手动删除了用于执行ab的apache pod，释放资源，然后立刻查看pod，就只有两个了
kubectl get hpa ngx-hpa -w的输出中也出现了一行新数据
ngx-hpa   Deployment&#47;ngx-hpa-dep   0%&#47;5%     2         10        2          7m46s
自动缩容成功执行了

所以，看起来，hpa是“严格按顺序执行的”，它按照规则设定的条件，要扩容到10个pod，在10个pod全都running之前，即使已经符合缩容的条件了，它也不执行缩容，而是要等到之前扩容的操作彻底完成，也就是10个pod全都running了，才会执行缩容</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（9） 💬（1）<div>请教老师几个问题：
Q1：Grafana 不是Prometheus的组件吧
架构图中标红色的是属于Prometheus，在UI方面，架构图中的”prometheus web ui”应该是Prometheus的组件吧。Grafana好像是一个公共组件，不是Prometheus独有的。

Q2: Prometheus部署后有四个POD的状态不是RUNNING
blackbox-exporter-746c64fd88-ts299：状态是ImagePullBackOff
prometheus-adapter-8547d6666f-6npn6：状态是CrashLoopBackOff，
错误信息：
sc = Get &quot;https:&#47;&#47;registry-1.docker.io&#47;v2&#47;jimmidyson&#47;configmap-reload&#47;manifests&#47;sha256:91467ba755a0c41199a63fe80a2c321c06edc4d3affb4f0ab6b3d20a49ed88d1&quot;: net&#47;http: TLS handshake timeout
好像和TLS有关，需要和Metrics Server一样加“kubelet-insecure-tls”吗？在哪个YAML文件中修改？

Q3：Prometheus部署的逆向操作是什么？
用这两个命令来部署：
kubectl create -f manifests&#47;setup
kubectl create -f manifests

部署后，如果想重新部署，需要清理环境，那么，怎么清理掉以前部署的东西？
和kubectl create -f manifests&#47;setup相反的操作是“kubectl delete -f manifests&#47;setup”吗？</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/9a/8ff51c91.jpg" width="30px"><span>ningfei</span> 👍（3） 💬（1）<div>prometheus-adapter里使用这个willdockerhub&#47;prometheus-adapter:v0.9.1镜像,可以启动成功</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/a6/29ac6f6a.jpg" width="30px"><span>XXG</span> 👍（2） 💬（1）<div>metrics-server-85bc76798b-hr56n           0&#47;1     ImagePullBackOff 原因：

&lt;1&gt; 注意metrics-server版本，我拉下来的yml文件版本变成了v0.6.2，所以要根据最新的components.yaml文件中的metrics-server版本对应改一下老师的脚本；
&lt;2&gt; 注意要在Worker节点执行脚本，我就在master节点上执行了好几遍。。。</div>2022-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（2） 💬（1）<div>简单的回答一下思考题，

1，会根据设置进行扩容（scale out），但是如果不满足 HPA 的指标条件，接着会立即进行缩容（scale in），下面是我的操作观察到的日志
---
Normal  SuccessfulCreate  3s    replicaset-controller  Created pod: ngx-hpa-dep-86f66c75f5-z2gjk
Normal  SuccessfulCreate  3s    replicaset-controller  Created pod: ngx-hpa-dep-86f66c75f5-p46lr
Normal  SuccessfulDelete  3s    replicaset-controller  Deleted pod: ngx-hpa-dep-86f66c75f5-z2gjk
Normal  SuccessfulDelete  3s    replicaset-controller  Deleted pod: ngx-hpa-dep-86f66c75f5-p46lr
---

2，我现有的经验很有限，主要集中在单机&#47;集群机器指标的监控，以及对于应用及产品的监控（通过监控日志实现的），同时结合一些告警系统（alert），以便快速发现故障及解决。
关注的指标有 CPU、内存、网卡、磁盘读写，应用的性能监控和错误率（可用性）监控。性能监控指标主要是响应时间（RT）、各种吞吐量（比如QPS）等。错误率指标主要是指应用错误及异常、HTTP错误响应代码等。</div>2022-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/2f/4518f8e1.jpg" width="30px"><span>放不下荣华富贵</span> 👍（2） 💬（1）<div>自动扩容的话，通常生产环境常用的指标是什么呢？

文中采用cpu占用率，比如md5sum是非常偏向于cpu运算的工作，但扩容可能并不能达到预期的效果（工作占满了一个核但是再多一个核却不能分摊这个工作）。
所以看起来系统负载而非占用率应该是更好的扩容指标，不知道我这么理解是否正确？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ba/02/78e0d4ac.jpg" width="30px"><span>运维赵宏业</span> 👍（1） 💬（1）<div>老师您好，请教下，多k8s集群的场景下，每个集群内都要部署一套kube-prometheus吗？感谢</div>2023-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（1） 💬（1）<div>老师，有没有办法能够让k8s访问宿主机网络？物理机安装prometus+grafana比较麻烦，如果能够直接通过docker&#47;k8s装好就方便很多；但是现在生产&#47;测试环境都是物理机环境，所以想要反向通过k8s的应用监控宿主机所在网络的服务。

应该怎么配置呢？</div>2023-02-05</li><br/><li><img src="" width="30px"><span>邵涵</span> 👍（1） 💬（3）<div>安装metrics server之后，kubectl top执行失败，如下
[shaohan@k8s4 ~]$ kubectl top node
Error from server (ServiceUnavailable): the server is currently unable to handle the request (get nodes.metrics.k8s.io)

执行kubectl get apiservice v1beta1.metrics.k8s.io -o yaml看到
status:
  conditions:
  - lastTransitionTime: &quot;2022-10-29T09:57:08Z&quot;
    message: &#39;failing or missing response from https:&#47;&#47;10.98.115.140:443&#47;apis&#47;metrics.k8s.io&#47;v1beta1:
      Get &quot;https:&#47;&#47;10.98.115.140:443&#47;apis&#47;metrics.k8s.io&#47;v1beta1&quot;: dial tcp 10.98.115.140:443:
      i&#47;o timeout&#39;
    reason: FailedDiscoveryCheck
    status: &quot;False&quot;
    type: Available
在components.yaml中给deployment对象添加hostNetwork: true（在spec-&gt;template-&gt;spec下）就可以解决这个问题</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（1） 💬（1）<div>分享一下我的本课实践经验。当所有部署结束后，检查发现有 Pod 无法正常运行（也就是几个 Web UI 无法正常打开的）

```bash
# 查看 Pod 状态，发现 prometheus-operator 无法正常启动
kubectl get pod -n monitoring
NAME                                  READY   STATUS    RESTARTS   AGE
blackbox-exporter-746c64fd88-wmnd5    3&#47;3     Running   0          68s
grafana-5fc7f9f55d-qqt77              1&#47;1     Running   0          68s
kube-state-metrics-6c8846558c-w66x9   3&#47;3     Running   0          67s
node-exporter-68l4p                   2&#47;2     Running   0          67s
node-exporter-vs55z                   2&#47;2     Running   0          67s
prometheus-adapter-6455646bdc-4lz5l   1&#47;1     Running   0          66s
prometheus-adapter-6455646bdc-gxbrl   1&#47;1     Running   0          66s
prometheus-operator-f59c8b954-btxtw   0&#47;2     Pending   0          66s

# 调查 Pod prometheus-operator
kubectl describe pod prometheus-operator-f59c8b954-btxtw -n monitoring
Events:
Type     Reason            Age   From               Message
----     ------            ----  ----               -------
Warning  FailedScheduling  82s   default-scheduler  0&#47;2 nodes are available: 1 Insufficient memory, 1 node(s) had taint {node-role.kubernetes.io&#47;master: }, that the pod didn&#39;t tolerate.
Warning  FailedScheduling  20s   default-scheduler  0&#47;2 nodes are available: 1 Insufficient memory, 1 node(s) had taint {node-role.kubernetes.io&#47;master: }, that the pod didn&#39;t tolerate.

# 去除 node 的污点 node-role.kubernetes.io&#47;master
kubectl taint nodes --all node-role.kubernetes.io&#47;master-
```</div>2022-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b6/88/e8deccbc.jpg" width="30px"><span>romance</span> 👍（1） 💬（8）<div>metrics-server成功部署了，kubectl get pod -n kube-system 查看正常运行了，但用kubectl top node 时显示  Error from server (ServiceUnavailable): the server is currently unable to handle the request (get nodes.metrics.k8s.io)</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d0/51/f1c9ae2d.jpg" width="30px"><span>Sports</span> 👍（1） 💬（5）<div>prometheus-adapter的pod一直是CrashLoopBackOff，日志显示exec &#47;adapter: exec format error是啥情况？grafana和Prometheus的web端倒是可以正常打开正常显示的</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/09/d0/8609bddc.jpg" width="30px"><span>戒贪嗔痴</span> 👍（1） 💬（2）<div>老师 好，我这边装了metrics- server后不知道为什么只能看到worker节点的指标，看不到master的指标，全部显示为none。网上找了好久，没找到答案，还望老师指点下。</div>2022-08-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erRCf8vWbWibajdSaMtCM1OzPQ6uPhblgL4zXJvKoaQYVmialqFqr0NIdD6Dlm1F5icOBxiaXvUcQs4BA/132" width="30px"><span>sgcls</span> 👍（0） 💬（1）<div>metrics-server 折腾了两天，终于好了，过程记录一下：

$ kubectl top node 提示出错
Error from server (ServiceUnavailable): the server is currently unable to handle the request (get nodes.metrics.k8s.io)

期间尝试：
- spec -&gt; template -&gt; spec 下添加 hostNetwork: true

错误依旧，查看 apiserver 日志：
$ kubectl logs -n kube-system kube-apiserver-master
E0902 17:28:30.885994       1 available_controller.go:524] v1beta1.metrics.k8s.io failed with: failing or missing response from https:&#47;&#47;10.101.216.86:443&#47;apis&#47;metrics.k8s.io&#47;v1beta1: Get &quot;https:&#47;&#47;10.101.216.86:443&#47;apis&#47;metrics.k8s.io&#47;v1beta1&quot;: net&#47;http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)

看了下 kubectl describe -n kube-system pod metrics-server-6dc55579bb-qv98v 发现 metrics-server 部署在 worker 节点
Node: worker&#47;192.168.10.130

看高赞评论，尝试下指定部署到 master 看能不能行，操作：
去掉 hostNetwork: true，同时 spec -&gt; template -&gt; spec 下添加 nodeName: master，这回正常显示 master 节点的用量了，但是 worker 节点所有字段都显示 &lt;Unknown&gt;

查看 metrics-server 日志
$ kubectl logs -n kube-system metrics-server-6dc55579bb-qv98v
E0903 15:50:56.622351       1 scraper.go:140] &quot;Failed to scrape node&quot; err=&quot;Get \&quot;https:&#47;&#47;192.168.10.130:10250&#47;metrics&#47;resource\&quot;: context deadline exceeded&quot; node=&quot;worker&quot;

查看了 worker 的防火墙、VPN 也都没问题，访问 worker 节点的 10250 端口(kubelet)也正常：curl -k &#39;https:&#47;&#47;192.168.10.130:10250&#47;metrics&#47;resource&#39;

没辙了，对比了下老师的 components.yaml(k8s_study&#47;metrics&#47;components.yaml)和我的，最后作了如下修改，kubectl top node 输出才终于正常..

1. spec -&gt; template -&gt; spec 下添加 hostNetwork: true
2. spec -&gt; template -&gt; spec 下添加 nodeName: master
3. containers -&gt; secure-port=10250 改为 secure-port=4443
4. containerPort: 10250 改为 secure-port=4443
5. metrics-server deployment 的镜像(image)改为 k8s.gcr.io&#47;metrics-server&#47;metrics-server:v0.6.1</div>2024-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e0/cc/a8c26fb2.jpg" width="30px"><span>okkkkk</span> 👍（0） 💬（1）<div>prometheus遇到了两个问题，整理下
1. 发现adapter运行不起来的话，如
prometheus-adapter-8547d6666f-9wj9j   0&#47;1     CrashLoopBackOff
是老师的prometheus-adapter:v0.9.1镜像有问题，我也打了一个镜像oiouou&#47;prometheus-adapter:v0.9.1，实测正常能用
2. prometheus-k8s-0 一直处于Pending状态，我这里是内存不足了，master和worker我都分配了2G内存，之后把worker升到4G，pod都正常了</div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/25/3932dafd.jpg" width="30px"><span>GeekNeo</span> 👍（0） 💬（1）<div>最新版本：
repo=registry.aliyuncs.com&#47;google_containers

name=registry.k8s.io&#47;metrics-server&#47;metrics-server:v0.6.4
src_name=metrics-server:v0.6.4

sudo docker pull $repo&#47;$src_name

sudo docker tag $repo&#47;$src_name $name
sudo docker rmi $repo&#47;$src_name</div>2023-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/70/27/4498ce51.jpg" width="30px"><span>huanrong</span> 👍（0） 💬（1）<div>当部署了 HorizontalPodAutoscaler 后，如果再执行 kubectl scale 命令手动扩容，HorizontalPodAutoscaler 会根据定义的自动伸缩策略来调整 Pod 的数量。具体而言，如果手动扩容的数量超过了 HorizontalPodAutoscaler 的上限，则 HorizontalPodAutoscaler 会将 Pod 的数量缩回上限；如果手动扩容的数量低于 HorizontalPodAutoscaler 的下限，则 HorizontalPodAutoscaler 会将 Pod 的数量扩展到下限以上。

这是因为 HorizontalPodAutoscaler 是根据 Metrics Server 提供的指标来自动伸缩 Pod 的数量的。当手动执行 kubectl scale 命令时，虽然可以直接改变 Pod 的数量，但是 HorizontalPodAutoscaler 会继续监控 Metrics Server 提供的指标，并根据自动伸缩策略对 Pod 的数量进行调整，以确保 Pod 的数量符合预定的范围。

总结起来，当部署了 HorizontalPodAutoscaler 后，建议使用 HorizontalPodAutoscaler 来自动伸缩 Pod 的数量，而不是直接使用 kubectl scale 命令进行手动扩容。这样可以确保自动伸缩策略的生效，以及避免手动扩容和自动伸缩策略之间的冲突。</div>2023-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a9/ee/2b57ba4e.jpg" width="30px"><span>Geek_0e379d</span> 👍（0） 💬（1）<div>一切部署正常，就不知道为什么浏览器打不开</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（1）<div>Kubernetes 项目运行一个名为 registry.k8s.io、由社区管理的镜像仓库来托管其容器镜像。 2023 年 4 月 3 日，旧仓库 k8s.gcr.io 将被冻结，Kubernetes 及其相关子项目的镜像将不再推送到这个旧仓库。</div>2023-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/ad/6ee2b7cb.jpg" width="30px"><span>Jacob.C</span> 👍（0） 💬（1）<div>请问装普罗米修斯之前必须装 mertrics 吗？</div>2023-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/a9/3d48d6a2.jpg" width="30px"><span>Lorry</span> 👍（0） 💬（1）<div>分享一点：拉去metric-server镜像的时候，一定要确保k8s集群所有的节点都通过docker进行拉取（执行文中提供的拉取脚本）。
我碰到的问题是只是在master拉去来的，但是任务打到work节点后，总是出现拉去失败的异常。

kubectl decribe在定位问题的时候，真香</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c4/51/5bca1604.jpg" width="30px"><span>aLong</span> 👍（0） 💬（1）<div>alertmanager-main-2,prometheus-k8s-0&amp;1, 这三个都会提示污点问题导致pending。去除掉污点会正常启动。 这是否是常规操作？</div>2023-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/9a/7b/aa937172.jpg" width="30px"><span>LiL</span> 👍（0） 💬（1）<div>按照老师的操作，正常安装promethus和grafana,但是grafana界面打不开，提示如下，还请老师解答下呢，网上搜了一圈也没发现可行的解决方案：
If you&#39;re seeing this Grafana has failed to load its application files

1. This could be caused by your reverse proxy settings.

2. If you host grafana under subpath make sure your grafana.ini root_url setting includes subpath. If not using a reverse proxy make sure to set serve_from_sub_path to true.

3. If you have a local dev build make sure you build frontend using: yarn start, yarn start:hot, or yarn build

4. Sometimes restarting grafana-server can help

5. Check if you are using a non-supported browser. For more information, refer to the list of supported browsers.</div>2022-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/fb/8a/3e8f42f1.jpg" width="30px"><span>ybc</span> 👍（0） 💬（1）<div>遇到个问题想请教下老师和同学们： 在prometheus、grafana部署成功后，我采用了ingress的方式来进行访问，但发现prometheus的web可以正常访问，但grafana的界面访问不到，查看日志，访问成功到了ingress controller的pod，但没能转发到grafana的pod，查证ingress的转发规则没问题，试着在ingress controller的pod中ping grafana节点的ip，发现ping不通，发现同一node的某些pod可以ping通，有些则不行。 不知道大家有没有知道原因或排查思路的？

贴下我的ingress规则：
  rules:
  - host: prome.test
    http:
      paths:
      - path: &#47;
        pathType: Prefix
        backend:
          service:
            name: prometheus-k8s
            port:
              number: 9090
  - host: grafana.test
    http:
      paths:
      - path: &#47;
        pathType: Prefix
        backend:
          service:
            name: grafana
            port:
              number: 3000
</div>2022-11-09</li><br/><li><img src="" width="30px"><span>邵涵</span> 👍（0） 💬（1）<div>遇到了一个grafana的问题：仪表盘，比如文中展示的“Kubernetes &#47; Compute Resources &#47; Namespace (Pods)”，页面中图形报表没有数据展示，数字部分，比如资源使用率百分比，展示的是NO DATA

这个看起来是grafana调用prometheus获取数据失败了
安装的grafana中的默认数据源中配置的prometheus url是http:&#47;&#47;prometheus-k8s.monitoring.svc:9090，service对象prometheus-k8s的域名“prometheus-k8s.monitoring.svc”此时在集群中访问失败（通过kubectl exec进入某测试用的pod去访问该域名，得到的是Could not resolve host: prometheus-k8s.monitoring.svc），此时，在default namespace下创建新的deployment+service，新的service对象的域名也是一样访问失败的
重启coredns也不起作用，是在重启了k8s集群的虚拟机几次之后，这个问题才自己好了，service的域名都可以访问了，grafana中的仪表盘页面也有数据了

另，在发生上述问题时，prometheus的alertmanager pod也是启动失败的
[shaohan@k8s4 ~]$ kubectl get pod -n monitoring
NAME                                  READY   STATUS    RESTARTS     AGE
alertmanager-main-0                   1&#47;2     Running   2 (9s ago)   3m29s
alertmanager-main-1                   1&#47;2     Running   2 (9s ago)   3m29s
alertmanager-main-2                   1&#47;2     Running   2 (9s ago)   3m29s
通过kubectl describe可以看到
  Warning  Unhealthy  4m34s (x6 over 5m24s)  kubelet            Liveness probe failed: Get &quot;http:&#47;&#47;10.10.1.12:9093&#47;-&#47;healthy&quot;: dial tcp 10.10.1.12:9093: connect: connection refused
  Warning  Unhealthy  30s (x68 over 5m27s)   kubelet            Readiness probe failed: Get &quot;http:&#47;&#47;10.10.1.12:9093&#47;-&#47;ready&quot;: dial tcp 10.10.1.12:9093: connect: connection refused
也是网络问题，当上边提到的service域名问题经过虚拟机重启解决了之后，这个alertmanager pod探针失败的问题，也同时消失了，pod成功运行</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/87/dde718fa.jpg" width="30px"><span>alexgreenbar</span> 👍（0） 💬（1）<div>kubectl create -f manifests&#47;setup

用create没有问题，但用apply会报错，之前一直用apply，这里是有什么区别吗？

**********
kubectl apply -f manifests&#47;setup
customresourcedefinition.apiextensions.k8s.io&#47;alertmanagerconfigs.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;alertmanagers.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;podmonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;probes.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;prometheusrules.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;servicemonitors.monitoring.coreos.com created
customresourcedefinition.apiextensions.k8s.io&#47;thanosrulers.monitoring.coreos.com created
namespace&#47;monitoring created
The CustomResourceDefinition &quot;prometheuses.monitoring.coreos.com&quot; is invalid: metadata.annotations: Too long: must have at most 262144 bytes
**********</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/c3/775fe460.jpg" width="30px"><span>rubys_</span> 👍（0） 💬（2）<div>老师，我执行了 
kubectl run test -it --image=httpd:alpine -- sh 之后，在里面 ping 不了 ngx-hpa-svc 是为何？在 httpd pod 里面的 ifconfig 显示 ip 是 10.10.1.6，然后 kubectl get svc 显示的 ngx-hpa-svc 的 IP 为 10.96.32.144</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（0） 💬（2）<div>kubectl get pods -n monitoring 
alertmanager-main-0                   1&#47;2     CrashLoopBackOff   9 (8s ago)   24m
alertmanager-main-1                   2&#47;2     Running            0            24m
alertmanager-main-2                   1&#47;2     CrashLoopBackOff   9 (7s ago)   24m
blackbox-exporter-746c64fd88-tlxm4    3&#47;3     Running            0            25m
grafana-5fc7f9f55d-tvmzb              1&#47;1     Running            0            24m




kubectl describe pod alertmanager-main-0 -n monitoring
 Normal   Scheduled  25m                    default-scheduler  Successfully assigned monitoring&#47;alertmanager-main-0 to worker
  Normal   Pulled     24m                    kubelet            Container image &quot;quay.io&#47;prometheus&#47;alertmanager:v0.24.0&quot; already present on machine
  Normal   Created    24m                    kubelet            Created container alertmanager
  Normal   Pulled     24m                    kubelet            Container image &quot;quay.io&#47;prometheus-operator&#47;prometheus-config-reloader:v0.57.0&quot; already present on machine
  Normal   Created    24m                    kubelet            Created container config-reloader
  Normal   Started    24m                    kubelet            Started container config-reloader
  Warning  Unhealthy  23m (x6 over 24m)      kubelet            Liveness probe failed: Get &quot;http:&#47;&#47;10.10.171.67:9093&#47;-&#47;healthy&quot;: dial tcp 10.10.171.67:9093: connect: connection refused
  Normal   Started    14m (x7 over 24m)      kubelet            Started container alertmanager
  Warning  Unhealthy  9m54s (x169 over 24m)  kubelet            Readiness probe failed: Get &quot;http:&#47;&#47;10.10.171.67:9093&#47;-&#47;ready&quot;: dial tcp 10.10.171.67:9093: connect: connection refused


根据这篇文章https:&#47;&#47;blog.csdn.net&#47;Entity_G&#47;article&#47;details&#47;117461725进行操作，结果发现两件事，第一sts无法删除，删除sts直接0&#47;3又开始启动，请问sts是还有更上一级别得服务吗，第二个就是dump执行还是无法解决问题，请问有老师知道啥情况吗，
</div>2022-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/34/b0/8d14a2a1.jpg" width="30px"><span>大布丁</span> 👍（0） 💬（3）<div>监控系统一般都是GPE三个组件一起用的</div>2022-09-02</li><br/>
</ul>