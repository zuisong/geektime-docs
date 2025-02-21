> 本课程为精品小课，不标配音频

你好，我是文强。

前面我们完成了项目初始化和基础模块的开发，这节课我们正式进入逻辑功能部分的开发。我们第一个要做的就是网络 Server 模块。

开发网络 Server 模块的核心是：**从业务需求视角出发，分析 Server 应该具备哪些能力，从而根据这些信息选型出技术层面网络层和应用层的协议**。

前面我们讲到，第一阶段我们会完成消息队列中的**“元数据服务”，**那么接下来我们就来看一下这个元数据存储服务的网络 Server 怎么选型。

## 网络 Server 模块选型

先来看一下元数据服务（Placement Center）的架构图。

![图片](https://static001.geekbang.org/resource/image/5c/f9/5c5dd56a4d0f8673618a46d563f82ff9.png?wh=1139x641)

在前面的定义中，我们的元数据服务有两个功能：

1. **分布式的 KV 存储能力**：需要给 Broker 集群提供分布式的 KV 存储能力，从性能来看，需要支持较高并发的读写。
2. **集群管控和调度能力**: 根据运行信息对 Broker 集群进行管控、调度，比如元数据更新、Leader 切换等等。

所以从网络模块的角度来看，就需要能支持：**较高的吞吐和并发能力**。那协议怎么选择呢？

从技术上来看，很多开源组件会选择 **TCP + 自定义协议**来完成网络 Server 的开发。我们最终选择的是**基于 gRPC 协议来实现我们的 Server**。考虑如下：
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（0）<div>我觉得这里介绍编译protobuf文件时，最好顺带的说一点build.rs的作用。这个对于其它语言转过来的开发者而言还是挺新奇的。</div>2024-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/a9/9b/b114d348.jpg" width="30px"><span>吃饱喝足开始干活</span> 👍（0） 💬（0）<div>简单例子，最易吸收❤️</div>2024-09-21</li><br/>
</ul>