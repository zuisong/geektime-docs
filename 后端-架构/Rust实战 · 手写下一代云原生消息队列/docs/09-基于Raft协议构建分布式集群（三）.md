> 本课程为精品小课，不标配音频

你好，我是文强。这节课我们继续完善基于 Raft 协议开发的分布式集群。我们会讲解如何开发 Raft Node 上的 Raft 状态机，并最终构建包括**发起选举**、**选举 Leader**、**心跳发送、心跳过期**等等 Raft 协议定义的核心步骤的集群。

首先我们需要再回顾一下 Raft 协议的原理，以便接下来更好地理解 Raft 状态机的构建。建议你主要回顾前面推荐的[《Raft 协议的动图原理展示》](https://thesecretlivesofdata.com/raft/)。从功能上看，Raft 算法由下面六个核心流程组成：

1. 节点发现
2. 发起选举
3. 选举 Leader
4. 心跳检测
5. 心跳超时
6. 重新发起选举

所以我们构建状态机也是围绕这六点展开的。最开始先来记住一个定义，就是：**Raft 状态机本质上是一个 Tokio 的任务（也就是 Tokio Task）**。接下来我们简单聊一下 Raft 状态机的运行原理。

## 状态机运行原理

先来看下面这张图：

![](https://static001.geekbang.org/resource/image/93/fe/930210fc45f6d88e476be0ccc05ec8fe.jpeg?wh=1920x1080)

如上图所示，Raft Node 主要由 gRPC Server、Raft 状态机、Raft Storage 三部分组成。其中最关键的是 Raft 状态机，它驱动了 Raft Node 向前运行。从启动流程的角度看，服务启动后，会先启动 gRPC Server、初始化 RawNode，然后启动 Raft 状态机。Raft 状态机本质上是一个 Loop 线程，它会不间断地运行去驱动 RawNode 向前运行。