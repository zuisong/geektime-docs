你好，我是雪飞。

上一课我们学习了 YAML 文件的相关知识，同时动手编写了 YAML 文件，现在你就可以使用 YAML 文件来与 K8s 集群沟通，从而实现应用部署和集群管理的需求。在接下来的课程中，我将继续深入介绍 K8s 中常用的资源对象，这些资源对象提供了应用部署、参数配置、网络访问、持久化存储、安全策略等等功能，满足各种实际的应用场景。对于 K8s 资源对象的管理，我会同时使用 kubectl 命令和 YAML 文件这两种方式来加深你的理解和记忆。

今天，我给你讲一下 K8s 中最核心的资源对象——Pod，它是 K8s 管理的最小可部署资源对象。其他很多资源对象都是基于 Pod 来实现更复杂的应用部署和管理。例如，Deployment 就是通过管理多个 Pod 来实现应用的高可用性和滚动更新。接下来，让我们详细了解一下什么是 Pod。

## 认识 Pod

Pod 的中文意思为豌豆荚，因为 Pod 中包含了一个或多个容器，容器和 Pod 的关系很像豌豆和豆荚的关系，所以这就是 Pod 名称的来历。在 K8s 中，Pod 是一个逻辑概念，而容器才是运行着应用镜像的实际载体，那为啥 K8s 不直接管理容器，而是还要搞出一个 Pod 呢？

![图片](https://static001.geekbang.org/resource/image/a9/04/a9059aeyyc92yyffbc54897809a49e04.jpg?wh=300x205)

最重要的原因就是：在一些常见的应用场景下，容器并不是孤零零的存在，它可能会跟其他容器之间有着很亲密的关系，它们相互协作，一起启动，一起停止，一起提供服务，同时它们需要彼此间可以方便的通信以及访问相同的数据。所以 K8s 就在容器的基础上创建了 Pod 这个更高层级的资源对象，Pod 可以将多个容器组合到一起部署和管理，同一 Pod 中的容器可以共享网络和存储空间，这种机制保证了对容器管理的一致性和灵活性。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/28/040f6f01.jpg" width="30px"><span>Y</span> 👍（1） 💬（1）<div># three_container_pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: test
spec:
  containers:
  - image: nginx
    name: nginx
    volumeMounts:   # 容器 Nginx 挂载 Volume
    - name: data
      mountPath: &#47;data
  - image: memcached
    name: memcached
    volumeMounts:   # 容器 memcached 挂载 Volume
    - name: data
      mountPath: &#47;data
  - image: redis
    name: redis
    volumeMounts:   # 容器 redis 挂载 Volume
    - name: data
      mountPath: &#47;data
  volumes:          # 定义了一个临时 Volume
  - name: data
    emptyDir: {}</div>2024-07-17</li><br/>
</ul>