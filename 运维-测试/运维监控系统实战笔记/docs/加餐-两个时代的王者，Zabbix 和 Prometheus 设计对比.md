你好，我是秦晓辉。

社区经常有小伙伴来询问 Zabbix 和 Prometheus 的选型问题，这节课我来介绍一下两个系统的设计理念，搞懂了它们的设计理念和折中思考，选型的烦恼自然迎刃而解。

> 注意，这里所谓的 Prometheus 不止是 Prometheus 软件本身，而是整个 Prometheus 生态，比如绘图工具 Grafana、分布式时序库 VictoriaMetrics、各类 Exporter，都可以看做是广义 Prometheus 生态的一部分。

我会从两个项目的时代背景开始聊起，进而深入到数据采集、存储、可视化、告警、事件分发等多个方面的对比，希望对你有所帮助。

## Zabbix 的时代背景

Zabbix 项目于 2001 年启动，至今已经二十多年了，Zabbix 的发展历程在其[官网](https://www.zabbix.com/cn/about)可查。

![](https://static001.geekbang.org/resource/image/8a/d0/8a913cde8bbd4fd568983d3a4945a2d0.png?wh=1920x428 "图片来自Zabbix 官网")

Zabbix 的很多设计逻辑是由其所在时代决定的，那么，那是一个怎样的时代呢？

1998 年左右，国内的四大门户网站刚刚成立，那是一个只要会写 HTML 就能挣大钱的时代。微服务？那都是 2005 年之后的事情了。监控的核心诉求就是监控服务器、各类网络设备，至于服务器上运行的各类单体应用，远没有现在的关注度高。Zabbix 的创始人 Alexei Vladishev，曾是银行的 SA，他显然是把玩过各类设备和品牌型号的，因为即便是传统企业使用的 AIX 小机，Zabbix 也是支持的。