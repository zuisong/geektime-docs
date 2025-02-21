你好，我是秦晓辉。

上一节我们对比了 Zabbix 和 Prometheus 的设计理念，在数据采集方面 Prometheus 依靠了庞大的社区力量缔造了 Exporter 生态。这节课我们就围绕 Exporter 来聊一聊，看看 Exporter 是因何崛起，有什么问题，以及如何解决。

## Exporter 因何崛起

纵观国际可观测性头部厂商，比如 Datadog、Dynatrace、NewRelic，他们都有自己的 all-in-one 的 agent，可见大家普遍认为这是一个最佳实践。开源社区也有类似的项目，就是 Telegraf、Categraf。但是企业要真正落地的时候，很多公司还是在使用各种零散的 Exporter。原因何在？我感觉主要是因为如下几点。

- Exporter 的生态更好，包括各类文档、博客、分享，以及 Exporter 对应的 Grafana Dashboard；
- Prometheus 主推的就是 Exporter，用户接触这个生态肯定是从 Prometheus 官网文档开始，被引导去使用 Exporter 也是理所当然。而一旦用起来了，再换就有迁移成本了；
- Exporter 是开源集市的玩法，普通技术人员很容易做一个 Exporter，既满足自己的需求也建立了个人品牌。同时又因为是自己的需求驱动，Exporter 的研发人员对相关数据如何采集、哪些数据更为关键，相对更熟悉，做出来的 Exporter 也就更实用。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/5d/6cf4d143.jpg" width="30px"><span>小青</span> 👍（0） 💬（0）<div>Cprobe 和 categraf 什么区别呢？</div>2025-02-18</li><br/>
</ul>