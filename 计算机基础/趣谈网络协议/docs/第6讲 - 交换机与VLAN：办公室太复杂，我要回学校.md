上一次，我们在宿舍里组建了一个本地的局域网LAN，可以愉快地玩游戏了。这是一个非常简单的场景，因为只有一台交换机，电脑数目很少。今天，让我们切换到一个稍微复杂一点的场景，办公室。

## 拓扑结构是怎么形成的？

我们常见到的办公室大多是一排排的桌子，每个桌子都有网口，一排十几个座位就有十几个网口，一个楼层就会有几十个甚至上百个网口。如果算上所有楼层，这个场景自然比你宿舍里的复杂多了。具体哪里复杂呢？我来给你具体讲解。

首先，这个时候，一个交换机肯定不够用，需要多台交换机，交换机之间连接起来，就形成一个稍微复杂的**拓扑结构**。

我们先来看**两台交换机**的情形。两台交换机连接着三个局域网，每个局域网上都有多台机器。如果机器1只知道机器4的IP地址，当它想要访问机器4，把包发出去的时候，它必须要知道机器4的MAC地址。

![](https://static001.geekbang.org/resource/image/08/29/0867321c36cc52bd3dd4d7622583fa29.jpg?wh=2866%2A2176)

于是机器1发起广播，机器2收到这个广播，但是这不是找它的，所以没它什么事。交换机A一开始是不知道任何拓扑信息的，在它收到这个广播后，采取的策略是，除了广播包来的方向外，它还要转发给其他所有的网口。于是机器3也收到广播信息了，但是这和它也没什么关系。

当然，交换机B也是能够收到广播信息的，但是这时候它也是不知道任何拓扑信息的，因而也是进行广播的策略，将包转发到局域网三。这个时候，机器4和机器5都收到了广播信息。机器4主动响应说，这是找我的，这是我的MAC地址。于是一个ARP请求就成功完成了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（257） 💬（18）<div>第一张图中，机器三是如何同时链接两台交换机？</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/82/39491fa6.jpg" width="30px"><span>杨武刚@纷享销客</span> 👍（110） 💬（2）<div>老师的这个比喻让我这个门外汉听得很爽，化繁为简，赞一个，希望老师以后多用比喻</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/5f/c60d0ffe.jpg" width="30px"><span>硅谷居士</span> 👍（104） 💬（1）<div>1. STP 对于跨地域甚至跨国组织的网络支持，就很难做了，计算量摆着呢。

2. ping 加抓包工具，如 wireshark</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（87） 💬（17）<div>第一:怎么感觉像培训网管呢
第二:有些东西 不适合做比喻 掌门那块不是到在讲什么 太乱了</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（60） 💬（10）<div>老师你好，我跟zixuan@有着相同的疑问。

文中提到：

当机器 2 要访问机器 1 的时候，机器 2 并不知道机器 1 的 MAC 地址，所以机器 2 会发起一个 ARP 请求。这个广播消息会到达机器 1，也同时会到达交换机 A。这个时候交换机 A 已经知道机器 1 是不可能在右边的网口的，所以这个广播信息就不会广播到局域网二和局域网三。

根据前一小节的内容，我有以下理解：
1. 交换机是二层设备，不会读取 IP 层的内容。
2. 交换机会缓存 MAC 地址跟转发端口的关系。
3. ARP 协议是广播的，目的地 MAC 地址是广播地址。

如果我的理解是正确的，那机器 2 发起的 ARP 请求中，是不含机器 1 的 MAC 地址的，只有广播地址。交换机 A 中缓存的信息是没法被利用起来的。那么交换机 A 是如何知道不需要把请求转发到其它局域网的呢？

</div>2018-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/90/0c5ed3d9.jpg" width="30px"><span>颇忒妥</span> 👍（57） 💬（4）<div>图一和图二有点看不懂，图里的交换机和PC 是物理设备，这个LAN 是什么？不是应该交换机和PC 直接用一根线相连么？</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/69/df/71563d52.jpg" width="30px"><span>戴劼 DAI JIE🤪</span> 👍（50） 💬（6）<div>有一次办公室断网，排查时候发现路由器某一个部门的端口的灯在狂闪，拔掉后恢复正常。然后去那个部门排查才发现他们插错了口，形成了环路导致广播风暴。</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/a0/021aefb5.jpg" width="30px"><span>奔跑的蜗牛</span> 👍（36） 💬（2）<div>从公众号追过来的，头一次听到这么好听的STP，终于明白原理了，再看STP就不那么头大了</div>2018-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/41/80/bd6419bb.jpg" width="30px"><span>化雨</span> 👍（21） 💬（1）<div>文中的拓扑图确实令我疑惑，好在thomas已经帮我发问了哈哈。能否考虑调整下拓扑图的画法：线条真实反应各个节点(主机，交换机等)的物理连接，同一个局域网的节点用虚线框出来</div>2018-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/99/f886543d.jpg" width="30px"><span>渔夫</span> 👍（20） 💬（1）<div>所有交换机都支持STP协议吗？除了STP还有别的什么机制能防止或预防网络环路风暴？谢谢</div>2018-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/b8/740c9b30.jpg" width="30px"><span>天空白云</span> 👍（12） 💬（1）<div>第二个问题？ping ，traceroute？</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/e0/3e636955.jpg" width="30px"><span>李博越</span> 👍（9） 💬（2）<div>看文章里最后一张图，两个不同的交换机，肯定是2个不同的网段，又为何能使用同一个vlanId进行网络划分呢？一个vlanId只能绑定一个网段才对吧？甚是不解</div>2018-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/92/99530cee.jpg" width="30px"><span>灰飞灰猪不会灰飞.烟灭</span> 👍（9） 💬（4）<div>老师，那假如既要保证vlan之间通讯，又要和其它部门通讯怎么呢？通过设置trunk吗？</div>2018-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGOSxM1GIHX9Y2JIe7vGQ87rK8xpo5F03KmiaGyXeKnozZsicHeSZrbSlzUVhTOdDlXCkTrcYNIVJg/132" width="30px"><span>ferry</span> 👍（6） 💬（2）<div>老师，您前面讲到交换机上的转发表是用于找到要接受的MAC地址，避免广播的，vlan也是用于避免全部广播的，那么他们之间的区别是否在于，转发表适用于只发送信息给一个机器，而vlan适合发送信息到一部分（大于等于1个）的机器呢？</div>2019-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/6b/85e3d900.jpg" width="30px"><span>Lsoul</span> 👍（6） 💬（1）<div>请问，图一机器三如果是双网卡又是如何通信的呢</div>2018-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（5） 💬（3）<div>原来交换机是机器学习的鼻祖</div>2019-03-08</li><br/><li><img src="" width="30px"><span>Tom</span> 👍（5） 💬（1）<div>你好，环路那个图，lan1的机器1和机器2怎么同时连两个交换机的，中间是有个集线器吗？</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/4d/392f969b.jpg" width="30px"><span>蒋旺Foo</span> 👍（4） 💬（2）<div>在讲解STP工作过程的时候，交换机如果能使用字母来命名那应该会更加清晰。因为交换机之间用数字表示距离，交换机命令也用数字，难免使人混淆。谢谢老师。</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/fa/3975f8da.jpg" width="30px"><span>王先统</span> 👍（4） 💬（1）<div>无论是hub还是交换机都是为了解决局域网内部机器的互通问题，到现在为止我们还没讲到广域网的访问，是吧？</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6e/86/c682976b.jpg" width="30px"><span>zhushenghang</span> 👍（3） 💬（2）<div>图一画的不准确。后面的说法也有问题。既然机器1的广播机器4和机器3能收到，那么他们肯定是处于一个广播域内，通俗的讲就是在一个VLAN内，那么就是纯二层的东西。
根据二层转发流程：
提取数据报的源MAC地址，查询MAC转发表（也就是L2FDB），如果找到就直接发送到对应端口。
对于表中不包含的地址，通过广播发送，也就是发送到所有端口。
使用地址自动学习（根据源MAC地址学习）和老化机制（定时机制）来维护MAC转发表的信息，二层转发一般不会更改数据包内容。
在上面的过程中，交换机 A 和交换机 B 都是能够学习到这样的信息：
机器 1 是在左边这个网口的。当了解到这些拓扑信息之后，情况就好转起来。
当机器 2 要访问机器 1 的时候，机器 2 并不知道机器 1 的 MAC 地址，所以机器 2 会发起一个 ARP 请求。
这个广播消息会到达机器 1，也同时会到达交换机 A。这个时候交换机 A 已经知道机器 1 是不可能在右边的网口的，所以这个广播信息就不会广播到局域网二和局域网三。
-&gt;这个广播照样会到达局域网二和局域网三，因为处于同一个广播域，目的MAC地址是全F的。
-&gt;二层交换机不过是提取数据报的源MAC地址，记录到二层的MAC表里方便下次收到的数据报的目的MAC是这个的时候直接转发。
-&gt;二层交换机发现数据报的目的MAC是广播地址，就会在VLAN里进行广播，所有同VLAN的服务器都能收到。

当机器 3 要访问机器 1 的时候，也需要发起一个广播的 ARP 请求。这个时候交换机 A 和交换机 B 都能够收到这个广播请求。交换机 A 当然知道主机 A 是在左边这个网口的，所以会把广播消息转发到局域网一。
同时，交换机 B 收到这个广播消息之后，由于它知道机器 1 是不在右边这个网口的，所以不会将消息广播到局域网三。
-&gt;因此这个说法也有问题，如果有多台交换机A、B上行到核心且处于同一个VLAN，同时接入交换机的集群为K8S集群，
-&gt;那么如果其中有容器从A交换机漂移到了B交换机且仅MAC发生了改变IP地址不变，那即使A交换机下的容器再广播也找不到这个容器了？
-&gt;按前面的说法聪明的交换机A并不会把广播包发往交换机B。那岂不是不通了？得等交换机mac表老化了才能通了？
-&gt;很明显交换机不会这么设计，其实上面这个只要A交换机下的容器广播了那么所有处于广播域的服务器都能收到。</div>2020-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/e5/605f423f.jpg" width="30px"><span>肖一林</span> 👍（3） 💬（1）<div>要是有交换机挂了，特别是掌门挂了，这个江湖会不会大乱</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/33/f9/50b76abe.jpg" width="30px"><span>AMIR</span> 👍（2） 💬（1）<div>老师，设置了vlan ，那么程序员想和秘书交流感情的时候，结果在不同的vlan，这时候怎么处理</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/88/fe/c18a85fe.jpg" width="30px"><span>随风</span> 👍（2） 💬（1）<div>LAN1&#47;LAN2是什么东西？机器不都是直接连接交换机的吗？</div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/1c/b0c6c009.jpg" width="30px"><span>zhj</span> 👍（2） 💬（1）<div>你好 麻烦问下，知道了对方的具体mac地址后，在同一局域网内发给具体明确的mac地址时，同一lan内的其他机器也能收到该包吗，也就是除了arp寻址阶段的明确广播外，之后寻址后的真正具体mac地址通讯也是会广播给其他lan内的机器吗(只有这样好像vlan才显得有意义，不然vlan只是个例单纯的arp广播好像意义不大)，还望解答</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/3e/925aa996.jpg" width="30px"><span>HelloBug</span> 👍（2） 💬（1）<div>老师，你好~只用交换机连接起来的网络，都是在一个局域网里是吧？</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/c3/a1a0b9ff.jpg" width="30px"><span>叮咚</span> 👍（2） 💬（1）<div>既然stp能解决环路，为什么实际场景中还是有环路发生？</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/2d/05a18518.jpg" width="30px"><span>李金洋</span> 👍（2） 💬（1）<div>是说把交换机变成单向广播吗？比如ABC三台交换机，两两互联，最后通过STP，变成A广播只发给B，B广播只发给C，然后反过来c只发给B，b只发给A(不同方向)</div>2018-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/32/3ab2277e.jpg" width="30px"><span>jacky</span> 👍（2） 💬（1）<div>老师你好，拓扑结构连线中的数字代表什么，还是仅仅是作为标记</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/9d/c36b7ef7.jpg" width="30px"><span>顾骨</span> 👍（2） 💬（1）<div>为什么网页没法留言。。。
想请教一下，第一张图能详细一点吗，有点没看懂，一个交换机怎么接2个局域网呢，机器3怎么会被两个交换机接入</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/32/3f/fa4ac035.jpg" width="30px"><span>sunlight001</span> 👍（2） 💬（1）<div>有个疑问，环路问题是交换机解决的还是人工解决的，stp在比较的时候一开始都是形成两两的门派吗，他们怎么比较成为老大的这个没看明白，请老师给解释下</div>2018-05-30</li><br/>
</ul>