想象一下，全球数十亿人突然失去了与亲朋好友的即时联系，企业沟通中断，社交媒体一片寂静。这不是科幻电影的情节，而是2021年10月4日，Facebook及其旗下服务真实经历的一幕。

你好，我是白园。今天，我们将深入探讨这场技术界的“大地震”，它不仅让Facebook市值瞬间蒸发百亿美元，更引发了全球范围内的数字恐慌，而这一切都源于一条错误的指令。

也是从这节课开始我们进入变更部分，从基础设施、基础平台到数据和配置变更，我们将通过三个案例，剖析背后的教训，学习如何在数字世界中航行，避免触礁。这节课我们就通过Facebook的这个故障案例来学习一下基础设施的故障：网络和DNS。

![图片](https://static001.geekbang.org/resource/image/b5/48/b5e5f74298edf45d97378e476a1f1848.png?wh=1932x1108)

## 案例回顾

2021年10月4日北京时间23:39，Facebook服务全面中断，此次服务中断持续了约7个小时，是近年来罕见的长时间宕机事件。不仅Facebook本身，它旗下所有相关应用和服务全面崩溃，包括但不限于Instagram、WhatsApp、Messenger等主要社交平台，以及虚拟现实平台Oculus、部分企业服务、内部工作系统。Facebook的股价在当天下跌近5%，创下了全年最大的单日跌幅，市值瞬间蒸发百亿美元。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/23/442f149d.jpg" width="30px"><span>xd</span> 👍（0） 💬（1）<div>节点不多的话，dns 写入 hosts，，</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/69/d2/8a53f0a3.jpg" width="30px"><span>E</span> 👍（0） 💬（2）<div>dns服务撤销bgp路由？</div>2024-08-08</li><br/>
</ul>