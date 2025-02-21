在小区里面，是不是经常有住户不自觉就霸占公共通道，如果你找他理论，他的话就像一个相声《楼道曲》说的一样：“公用公用，你用我用，大家都用，我为什么不能用？”。

除此之外，你租房子的时候，有没有碰到这样的情况：本来合租共享WiFi，一个人狂下小电影，从而你网都上不去，是不是很懊恼？

在云平台上，也有这种现象，好在有一种流量控制的技术，可以实现**QoS**（Quality of Service），从而保障大多数用户的服务质量。

对于控制一台机器的网络的QoS，分两个方向，一个是入方向，一个是出方向。

![](https://static001.geekbang.org/resource/image/74/11/747b0d537fd1705171ffcca3faf96211.jpg?wh=1539%2A646)

其实我们能控制的只有出方向，通过Shaping，将出的流量控制成自己想要的模样。而进入的方向是无法控制的，只能通过Policy将包丢弃。

## 控制网络的QoS有哪些方式？

在Linux下，可以通过TC控制网络的QoS，主要就是通过队列的方式。

### 无类别排队规则

第一大类称为**无类别排队规则**（Classless Queuing Disciplines）。还记得我们讲[ip addr](https://time.geekbang.org/column/article/7772)的时候讲过的**pfifo\_fast**，这是一种不把网络包分类的技术。

![](https://static001.geekbang.org/resource/image/e3/6c/e391b4b79580a7d66afe4307ff3f6f6c.jpg?wh=2037%2A1175)

pfifo\_fast分为三个先入先出的队列，称为三个Band。根据网络包里面TOS，看这个包到底应该进入哪个队列。TOS总共四位，每一位表示的意思不同，总共十六种类型。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/52/e0/ef42c4ce.jpg" width="30px"><span>晓.光</span> 👍（18） 💬（1）<div>越来越发现云中的网络控制跟本地原理一致~</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/85/ed/905b052f.jpg" width="30px"><span>超超</span> 👍（10） 💬（1）<div>答问题1：是否可以在虚拟机的前一级控制出口流量？前一级的出口流量得到控制，那么虚拟机的入口流量也就得到了控制。</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（7） 💬（1）<div>超哥，有个问题想问下：你平时代码写的多吗？</div>2018-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/48/c7aad9d6.jpg" width="30px"><span>HIK</span> 👍（3） 💬（3）<div>请问如何实现疯狂发包？</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/4b/4cbd001e.jpg" width="30px"><span>佳俊</span> 👍（0） 💬（1）<div>
ovs-ofctl add-flow br0 &quot;in_port=6 nw_src=192.168.100.100 actions=enqueue:5:0&quot;
ovs-ofctl add-flow br0 &quot;in_port=7 nw_src=192.168.100.101 actions=enqueue:5:1&quot;
ovs-ofctl add-flow br0 &quot;in_port=8 nw_src=192.168.100.102 actions=enqueue:5:2&quot;

1. 这几个命令里面的in_port=6,7,8怎么和上面的queue对应起来的？
</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（37） 💬（8）<div>云里雾里 不是科班 感觉要补的东西太多了</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/c5/aaacb98f.jpg" width="30px"><span>yungoo</span> 👍（22） 💬（1）<div>通过ingress qdisc策略将入口流量重定向到虚拟网卡ifb，然后对ifb的egress进行出口限速，从而变通实现入口流控。</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/be/494010aa.jpg" width="30px"><span>zcpromising</span> 👍（13） 💬（0）<div>前面15讲以前的内容，在学校是可以接触到的，后面每讲的内容，在学校是体会不到的，每天听老师您的课程，感觉就像发现了新大陆一样，惊喜万分。要是学校老师能够按照您这样的方式讲，那该多好。</div>2018-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（6） 💬（0）<div>虚拟机的流量都通过openv switch控制，机器数量多了，openvswitch会不会成为一个瓶颈</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/c7/a147b71b.jpg" width="30px"><span>Fisher</span> 👍（6） 💬（0）<div>这篇文章控制的出口流量是控制网卡层面的，那么像标题里面的，如果是在局域网中别人疯狂下载，这种控制网速的是在哪个层面控制的，路由器本身控制速度的原理又是什么呢，只是控制转发速度吗</div>2018-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/ae/855b7e6e.jpg" width="30px"><span>Gabriel</span> 👍（3） 💬（1）<div>嗯 什么就硬着头皮也要看 我现在就是</div>2021-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/12/0e6620cd.jpg" width="30px"><span>三景页</span> 👍（1） 💬（2）<div>从刘超老师的 刘超的通俗云计算博客 追到极客时间来了</div>2021-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/39/f9/b2fe7b63.jpg" width="30px"><span>King-ZJ</span> 👍（1） 💬（0）<div>QOS服务质量在业务运行中做一个按需的配置，更好调节网络的运行流畅度，带给客户更好的体验。</div>2020-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Cib5umA0W17N9pichI08pnrXAExdbyh7AVzH4nEhD6KN3FXuELk4LJJuqUPPD7xmIy9nq5Hjbgnzic7sVZG5BKiaUQ/132" width="30px"><span>被过去推开</span> 👍（1） 💬（0）<div>很多网关都提供了基于令牌桶模式的限流，比如spring cloud gateway</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/8b/8a0a6c86.jpg" width="30px"><span>haha</span> 👍（1） 💬（0）<div>几种队列的控制策略，放到哪合适的场景适用，借鉴与启发，原理都是如此。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2025-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9a/09/af250bf8.jpg" width="30px"><span>熊@熊</span> 👍（0） 💬（0）<div>HTB的子队列会打满么？如果满了，新流量是丢弃么？还是会调整窗口？</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/92/36/6f4d8528.jpg" width="30px"><span>夜⊙▽⊙</span> 👍（0） 💬（0）<div>老师，文中提到的类别该如何理解划分？</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/da/b3/35859560.jpg" width="30px"><span>Ciao🌚</span> 👍（0） 💬（0）<div>老师，看网上有的资料说，实际上实现Qos都使用了IP头部TOS field的6个bit的DSCP的概念，而不是那4个bit，因为application都不支持。是这样吗？</div>2021-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/48/33/4663928e.jpg" width="30px"><span>W҈T҈H҈</span> 👍（0） 💬（0）<div>Qos流量判断可以做网络黑洞吗？来抵御流量攻击？</div>2020-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e4/a1/178387da.jpg" width="30px"><span>25ma</span> 👍（0） 💬（0）<div>感觉非科班需要花更多时间来消化这些知识，喜欢超哥的课程</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c8/6b/0f3876ef.jpg" width="30px"><span>iron_man</span> 👍（0） 💬（0）<div>所有的流量都通过openv</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/6f/6051e0f1.jpg" width="30px"><span>Summer___J</span> 👍（0） 💬（0）<div>3:1:6的例子、假如一开始是2个节点疯狂发包占满带宽，假如是第一个和第二个一开始在发，带宽利用占比是3:1。一段时间后，第三个节点再开始疯狂发包。这种情况，当第三个上来以后，这三个节点在带宽占用上会动态地回到3:1:6吗？</div>2018-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/82/4b56fa5f.jpg" width="30px"><span>rtoday</span> 👍（0） 💬（0）<div>ovs-vsctl set port first_br qos=@newqos 
-- --id=@newqos create qos type=linux-htb other-config:max-rate=10,000,000 queues=0=@q0,1=@q1,2=@q2
-- --id=@q0 create queue other-config:min-rate=3,000,000 other-config:max-rate=10,000,000 
-- --id=@q1 create queue other-config:min-rate=1,000,000 other-config:max-rate=10,000,000 
-- --id=@q2 create queue other-config:min-rate=6,000,000 other-config:max-rate=10,000,000

这是倒数第二个指令
我刻意排版一下，并且把数字使用三位一个撇节

1. 语法问题
为何写成
-- --id=@newqos
我可以只写下面这样吗
--id=@newqos
双横线然后后面不加上option，请问有什么特殊用意吗？

2.语意问题
是否是我吹毛求疵了
好象每个数字都少一个0
还是我的认知有误呢</div>2018-07-19</li><br/><li><img src="" width="30px"><span>网络已断开</span> 👍（0） 💬（0）<div>看完似懂非懂，心里痒痒的</div>2018-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/eb/82/4b56fa5f.jpg" width="30px"><span>rtoday</span> 👍（0） 💬（0）<div>第一题
这篇讲的是Client如何控制出口流量
那Client的入口流量
也按照一样的原理，只是由Server端，或是数据中心端的人，来控制他们的出口流量即可。这应该是有没有权限的问题。

第二题，应该是下期的主题，等下期出刊后，再来回顾本题，可能体会的比较完整。</div>2018-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/b5/dd0353f4.jpg" width="30px"><span>三水</span> 👍（0） 💬（0）<div>问题2: 可以使用Linux Network Namespace进行隔离，cgroup 就进行资源调配和统计，云计算多租户资源使用，如基于docker的云计算服务</div>2018-07-18</li><br/>
</ul>