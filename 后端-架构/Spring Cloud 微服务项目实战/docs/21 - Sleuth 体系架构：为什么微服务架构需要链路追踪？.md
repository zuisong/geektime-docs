你好，我是姚秋辰。

俗话说，人非圣贤孰能无过，你有过来我有过，微服务它也有过。所谓“过”，便是这线上环境所发生的Bug。

面对线上Bug怎么办？有则改之，无则加勉而已。Sentinel用自己的文治武功替我们搞定了后半句“无则加勉”。那么这前半句“有则改之”，我们该如何下手去改呢？

请你想一下，在开发小哥改正线上Bug之前，咱们是不是需要先找到Bug发生的原因呢？所以今天我们就来聊一聊“如何找Bug”这个话题，且看我是如何使用Sleuth提供的“调用链追踪”技术，按图索骥查明Bug真相的。

首先我来带你了解一下调用链追踪要解决的问题。

## 调用链追踪解决了什么问题

我们可以想象这样一个场景，你负责的是一个庞大的电商微服务架构系统，每个服务之间都有复杂的上下游调用关系，而且并发量还不小，每秒上万QPS不在话下。

在这个微服务系统中，用户通过浏览器的H5页面访问系统，这个用户请求会先抵达微服务网关组件，然后网关再把请求分发给各个微服务。所以你会发现，用户请求从发起到结束要经历很多个微服务的处理，这里面还涉及到消息组件的集成。

我画了一幅图来展示这个复杂的关系。

![图片](https://static001.geekbang.org/resource/image/c4/5c/c468311yy62e782c5f99108c3a372e5c.jpg?wh=1920x801)

现在问题来了，突然有一天，有用户上报，说他在页面端看到了一个报错，每次点击下单都会报一个500错误。如果问题被交到了你手上，你该怎么排查呢？
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（18） 💬（1）<div>我猜是加在http请求头传递下去的</div>2022-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5f/47/02fb90f0.jpg" width="30px"><span>杨极客</span> 👍（12） 💬（1）<div>既然已经有了traceid，不可以通过创建时间来区分项目顺序吗</div>2022-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（2） 💬（1）<div>如果采样率小于1，zipkin肯定会受影响，日志里面会有traceid和spanid吗？还是采样的才会有，没有采样的就不会有？</div>2022-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（1） 💬（2）<div>我想去一个问题，如果采样率不是1，那么异常发生的时候，是不是有可能不会记录链路呢？</div>2022-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/58/84/a8aac073.jpg" width="30px"><span>金尚</span> 👍（0） 💬（1）<div>老师传统单体应用可以用sleuth吗</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/58/84/a8aac073.jpg" width="30px"><span>金尚</span> 👍（0） 💬（1）<div>老师不是微服务架构可以用sleuth吗。</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/9b/68/6f1a48fe.jpg" width="30px"><span>兴趣使然</span> 👍（0） 💬（0）<div>为什么不用skywalking</div>2023-02-07</li><br/>
</ul>