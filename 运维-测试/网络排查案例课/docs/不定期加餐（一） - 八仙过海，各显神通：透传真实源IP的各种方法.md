你好，我是胜辉。这节加餐课，我们来聊聊透传真实源IP的各种方法。

在互联网世界里，真实源IP作为一个比较关键的信息，在很多场合里都会被服务端程序使用到。比如以下这几个场景：

- **安全控制**：服务端程序根据源IP进行验证，比如查看其是否在白名单中。使用IP验证，再结合TLS层面和应用层面的安全机制，就形成了连续几道安全门，可以说是越发坚固了。
- **进行日志记录**：记下这个事务是从哪个源IP发起的，方便后期的问题排查和分析，乃至进行用户行为的大数据分析。比如根据源IP所在城市的用户的消费特点，制定针对性的商业策略。
- **进行客户个性化展现**：根据源IP的地理位置的不同，展现出不同的页面。以eBay为例，如果判断到访问的源IP来自中国，那就给你展现一个海淘页面，而且还会根据中国客户的特点，贴心地给你推荐流行爆款。

虽然源IP信息有这么多用处，但是现实情况中，这个源IP信息还不是那么好拿。这个原因有很多，最主要的还是跟负载均衡（LB）的设计有关系。

一般来说，用户发起HTTP请求到网站VIP，VIP所在的LB会把请求转发给后端，一前一后分别有两个TCP连接。

- 前一个TCP连接的客户端IP是CIP，服务端IP是VIP。
- 后一个TCP连接的客户端IP是LB的SNAT IP，服务端IP是SIP。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="" width="30px"><span>woJA1wCgAASVwFBCYVuFLQY8_9xjIc3w</span> 👍（1） 💬（3）<div>toa就算服务器加载内核模块了，但后端应用也需要改造吧</div>2022-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（1） 💬（1）<div>思考题：
选中tcp option
</div>2022-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZicRP0FZ78kT68wEGeWzPnxrF4s3Ea36XdMA2pj2TAbU3eibVt7KqzS5B7LbWMhRfSc3XEUL3Hrjw/132" width="30px"><span>liubiqianmoney</span> 👍（0） 💬（1）<div>FULLNAT LVS 的VIP有IPV6和IPV4，用户通过DNS的A和AAAA获取相应的VIP，RS是Nginx，Nginx的deny指令只能拒绝IPV4用户的请求，似乎是TOA不支持？</div>2024-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>tcp option  address:
它是利用 TCP Options 的字段来承载真实源 IP 信息，这个是目前比较常见的第四层方案。不过，这并非是 TCP 标准所支持的，所以需要通信双方都进行改造。也就是：对于发送方来说，需要有能力把真实源 IP 插入到 TCP Options 里面。对于接收方来说，需要有能力把 TCP Options 里面的 IP 地址读取出来。</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>1、http headers 允许使用逗号分隔的值分开成多个。 比如 vary 等。
2、tcp应用可以直接回包给真实源。 如果负载与RS使用IPIP的话。</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/66/4835d92e.jpg" width="30px"><span>潘政宇</span> 👍（0） 💬（1）<div>Toa </div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/8b/7a/ec36ff82.jpg" width="30px"><span>原则</span> 👍（1） 💬（0）<div>IP 层的方法不太理解，为什么是通过 LB 传递了真实源 IP，后续通信却绕开了 LB 呢？这是什么架构？好像没见过。</div>2023-06-18</li><br/>
</ul>