你好，我是袁武林。

前面的大部分课程，我基本都是围绕“如何开发和设计一个IM系统”的技术点，来进行分析和讲解的，但在实际项目的工程落地实践中，IM系统的监控和保障也是极其重要的一环。

只有通过对消息收发链路的监控，我们才能够实时地了解到链路是否可用，后端服务是否足够健康；如果监控体系不够完善，我们的业务即使上线了，也是处于“蒙眼狂奔”的状态。所以，我们要在工程上线时有一个**“服务上线，监控先行”**的意识和原则。

今天，我们就一起来聊一聊，消息收发链路中监控体系搭建的问题。

在IM场景中，常见的监控模式大概可以分为两种：一种是基于数据收集的被动监控，一种是基于真实探测的主动监控。下面我们来分别看一下这两种监控模式的实现细节和区别。

## 基于数据收集的被动监控

“基于数据收集的被动监控”，应该是我们日常开发保障中，最常见的服务和系统监控方式了。

一般来说，被动监控可以粗略地分成几个子类型：系统层监控、应用层监控及全链路Trace监控。

### 系统层监控

系统层监控是整个监控体系中最基础的监控方式，一般来说，它主要监控的是操作系统维度的一些核心性能指标。

举个例子：我们要对上线的业务进行监控，可以通过Nagios、Zabbix等类似的系统监控工具，来实时收集机器相关的性能数据，如CPU、内存、IO、负载、带宽、PPS、Swap等数据信息。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/6c/0c2a26c7.jpg" width="30px"><span>clip</span> 👍（5） 💬（1）<div>思考题：
感觉整体可以正常运转，但是会丢失一些细节。
如果被调用服务只是 server 侧没接 trace 那会丢失 server 侧及这个服务内部的其他调用的 trace。
如果被调用服务的 client 也没接 trace 那这次调用会被当做调用它的服务的内部的一个逻辑，但不影响整个链路里其他部分的监控。</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/6c/0c2a26c7.jpg" width="30px"><span>clip</span> 👍（3） 💬（1）<div>“对单机的应用状态分别进行监控”是指怎样的监控呢？
是类似监控应用层整体情况那样但改成单机器监控，还是做每台机器的系统层监控呢？
感觉系统层监控的话好像还是不太容易和应用层整体的报错对应起来。</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（3） 💬（1）<div>个人觉得不可用，调用环节已经断层</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/98/5591d99d.jpg" width="30px"><span>唯我天棋</span> 👍（1） 💬（1）<div>如果不是rpc模式的，长连接模式的，消息异步发送，怎么进行全链路监控呀？</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（4） 💬（0）<div>     自己其实在工作中越来越觉得监控的重要：知道问题才能解决问题；监控的方案其实同样是在完善中的个人觉得不同系统关注的监控应当不一样，需要对现有的监控系统做二次开发-制定出适合自己系统的监控系统才是合适的系统。这个就像MQ虽然有许多，可是不同场景适用的不同，如何写出合适自己系统的监控才是关键。</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/16/4d1e5cc1.jpg" width="30px"><span>mgxian</span> 👍（2） 💬（0）<div>trace会中断 无法查看整个链路的情况 主要是因为 traceid 和 parent span id 无法正常传递</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>traceid之前的系统实践过，现在没搞懂spanid的生成并保障在traceid下唯一，特别是对于并发请求多个服务的时候</div>2020-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/15/070d83ae.jpg" width="30px"><span>Z邦</span> 👍（0） 💬（0）<div>老师能否开一篇详解应用层监控需要监控的指标、获取方法，异常幅度等细节？</div>2019-10-12</li><br/>
</ul>