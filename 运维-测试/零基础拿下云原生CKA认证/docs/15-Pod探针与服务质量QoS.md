你好，我是雪飞。

前两节课我带你了解了集群的安全策略，K8s 通过 RBAC 权限控制有效应对了外部访问风险，并且通过网络策略控制 Pod 的出入口流量，从而应对了内部访问风险。这节课我们讨论如何保障 K8s 集群中应用的稳定性，由于应用是以 Pod 的方式部署在集群中，所以 K8s 稳定性的策略主要是针对 Pod。

我给你介绍保障 Pod 稳定性最常用的两种方式，一种是 Pod 探针，另一种是 Pod 的资源请求和限制。

## Pod 探针

你一定见过心电监测设备吧，在病人身上贴上几个电极来检查心跳情况，从而了解病人的健康状况。K8s 提供的 Pod 探针也有类似的功能，只不过它的监测对象是集群中的 Pod。Pod 探针通过定期检查 Pod 容器的存活和就绪状态，从而监测 Pod 容器的健康情况。对于不健康的 Pod 容器，可以根据策略自动重启、替换，或者移出 Service 的代理列表，确保应用的稳定性和可靠性，大大减轻了运维人员的工作量。

### 探针种类

针对 Pod 容器启动和运行过程，K8s 提供了 3 种类型的探针。

- **启动探针（Startup Probes）：**启动探针用于确定容器是否已经完全启动。在容器启动期间，启动探针进行探测，如果探测失败，K8s 会认为容器启动失败，并根据重启策略进行重启。在启动探针探测成功之前，其他类型的探针都会暂时处于禁用状态。启动探针一旦检测成功，就停止了。这主要适用于容器启动时间较长的场景。
- **就绪探针（Readiness Probes）：**就绪探针用于确定容器是否已经准备好接收访问请求。如果就绪探针探测失败，K8s 会将该容器从 Service 负载均衡的代理列表中清除。如果探测成功，Pod 会进入 READY 状态，并被加入到 Service 的 Endpoints 终端列表中。这确保了只有完全启动并准备好对外提供服务的容器才会接收请求。
- **存活探针（Liveness Probes）：**存活探针用于确定容器是否正常运行。如果存活探针探测失败，K8s 会认为容器不再健康，并根据容器的重启策略来重启它。这有助于自动恢复那些进入异常状态但未崩溃的容器。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（0） 💬（1）<div>1.设置启动探针
# my-pod-probe.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: my-pod-probe
spec:
  containers:
  - name: nginx-c-probe
    image: swr.cn-north-4.myhuaweicloud.com&#47;ddn-k8s&#47;docker.io&#47;nginx:1.26.1-alpine
    startupProbe:
      exec:
        command:
        - cat
        - &#47;root&#47;config.txt
      initialDelaySeconds: 5
      periodSeconds: 5
      successThreshold: 1
      failureThreshold: 3

2.然后再来修改 Pod，在运行容器时执行 “touch &#47;data&#47;config.txt” 命令来创建这个配置文件，再观察一下 Pod 的运行情况

这个试了半天都没成功。不知道哪里出问题了。请老师帮看一下。
# my-pod-probe.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: my-pod-probe
spec:
  containers:
  - name: nginx-c-probe
    image: swr.cn-north-4.myhuaweicloud.com&#47;ddn-k8s&#47;docker.io&#47;nginx:1.26.1-alpine
    command: [&quot;&#47;bin&#47;sh&quot;, &quot;-c&quot;]
    args: [&quot;touch &#47;root&#47;config.txt&quot;]
    startupProbe:
      exec:
        command:
        - cat
        - &#47;root&#47;config.txt
      initialDelaySeconds: 5
      periodSeconds: 5
      successThreshold: 1
      failureThreshold: 3

</div>2024-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/4b/95812b15.jpg" width="30px"><span>抱紧我的小鲤鱼</span> 👍（0） 💬（1）<div>
    readinessProbe:
      exec:
        command:
        - cat
        - &#47;data&#47;config.txt
      initialDelaySeconds: 5
      periodSeconds: 5
      successThreshold: 1
      failureThreshold: 3
</div>2024-07-27</li><br/>
</ul>