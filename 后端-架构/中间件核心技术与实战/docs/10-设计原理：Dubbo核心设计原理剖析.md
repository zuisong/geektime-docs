你好，我是丁威。

这节课，我们来剖析一下Dubbo中一些重要的设计理念。这些设计理念非常重要，在接下来的11和12讲Dubbo案例中也都会用到，所以希望你能跟上我的节奏，好好吸收这些知识。

微服务架构体系包含的技术要点很多，我们这节课没法覆盖Dubbo的所有设计理念，但我会带着你梳理Dubbo设计理念的整体脉络，把生产实践过程中会频繁用到的底层原理讲透，让你轻松驾驭Dubbo微服务。

我们这节课的主要内容包括服务注册与动态发现、服务调用、网络通信模型、高度灵活的扩展机制和泛化调用五个部分。

## **服务注册与动态发现**

我们首先来看一下Dubbo的服务注册与动态发现机制。

Dubbo的服务注册与发现机制如[下图](https://dubbo.apache.org/imgs/architecture.png)所示：

![图片](https://static001.geekbang.org/resource/image/a1/3b/a15364103e405767efbca0719959773b.png?wh=899x531)

Dubbo中主要包括四类角色，它们分别是注册中心（Registry）、服务调用者&amp;消费端（Consumer）、服务提供者（Provider）和监控中心（Monitor）。

在实现服务注册与发现时，有三个要点。

1. 服务提供者(Provider)在启动的时候在注册中心(Register)注册服务，注册中心(Registry)会存储服务提供者的相关信息。
2. 服务调用者(Consumer)在启动的时候向注册中心订阅指定服务，注册中心将以某种机制（推或拉）告知消费端服务提供者列表。
3. 当服务提供者数量变化（服务提供者扩容、缩容、宕机等因素）时，注册中心需要以某种方式(推或拉)告知消费端，以便消费端进行正常的负载均衡。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/86/25/25ded6c3.jpg" width="30px"><span>zhengyu.nie</span> 👍（0） 💬（0）<div>作者你好，dubbo线程池默认200个线程设置基于什么考虑？你的线程池文章推荐是20个线程</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/89/93a4019e.jpg" width="30px"><span>fantasyer</span> 👍（0） 💬（2）<div>老师好，网络通信模型这部分提到，iothreads默认为 CPU 核数再加一，如果增加iothreads的话也建议保持在“2*CPU 核数”以下，这里线程数不超过2*CPU核数原因是什么？</div>2022-07-19</li><br/>
</ul>