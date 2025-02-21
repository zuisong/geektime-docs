上一节，我们讲了IP的一些基本概念。如果需要和其他机器通讯，我们就需要一个通讯地址，我们需要给网卡配置这么一个地址。

## 如何配置IP地址？

那如何配置呢？如果有相关的知识和积累，你可以用命令行自己配置一个地址。可以使用ifconfig，也可以使用ip addr。设置好了以后，用这两个命令，将网卡up一下，就可以开始工作了。

**使用net-tools：**

```
$ sudo ifconfig eth1 10.0.0.1/24
$ sudo ifconfig eth1 up
```

**使用iproute2：**

```
$ sudo ip addr add 10.0.0.1/24 dev eth1
$ sudo ip link set up eth1
```

你可能会问了，自己配置这个自由度太大了吧，我是不是配置什么都可以？如果配置一个和谁都不搭边的地址呢？例如，旁边的机器都是192.168.1.x，我非得配置一个16.158.23.6，会出现什么现象呢？

不会出现任何现象，就是包发不出去呗。为什么发不出去呢？我来举例说明。

192.168.1.6就在你这台机器的旁边，甚至是在同一个交换机上，而你把机器的地址设为了16.158.23.6。在这台机器上，你企图去ping192.168.1.6，你觉得只要将包发出去，同一个交换机的另一台机器马上就能收到，对不对？

可是Linux系统不是这样的，它没你想的那么智能。你用肉眼看到那台机器就在旁边，它则需要根据自己的逻辑进行处理。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/53/19/965c845c.jpg" width="30px"><span>袁沛</span> 👍（344） 💬（10）<div>20年前大学宿舍里绕了好多同轴电缆的10M以太网，上BBS用IP，玩星际争霸用IPX。那时候没有DHCP，每栋楼有个哥们负责分配IP。</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/c6/4a7b2517.jpg" width="30px"><span>Will王志翔(大象)</span> 👍（139） 💬（1）<div>以问答写笔记：

1. 正确配置IP?
	
CIDR、子网掩码、广播地址和网关地址。
	
2. 在跨网段调用中，是如何获取目标IP的mac地址的？
	
从源IP网关获取所在网关mac,
然后又替换为目标IP所在网段网关的mac,
最后是目标IP的mac地址
	
3. 手动配置麻烦，怎么办？
	
DHCP！Dynamic Host Configuration Protocol！
DHCP, 让你配置IP，如同自动房产中介。
	
4. 如果新来的，房子是空的(没有操作系统)，怎么办？
	
PXE， Pre-boot Execution Environment.
&quot;装修队&quot;PXE，帮你安装操作系统。</div>2018-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/36/9e/8f031100.jpg" width="30px"><span>ERIC</span> 👍（91） 💬（14）<div>刘老师你好，文章关于DHCP可能是有两处错误。DHCP Offer 和 DHCP ACK都不是广播包，而是直接发到客户机的网卡上的。这是wiki上的链接：
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Dynamic_Host_Configuration_Protocol#DHCP_offer
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;Dynamic_Host_Configuration_Protocol#DHCP_acknowledgement

另外我自己也抓了包验证，https:&#47;&#47;baixiang.oss-cn-shenzhen.aliyuncs.com&#47;dhcp&#47;dhcp.png。</div>2019-03-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/FMwyx76xm95LgNQKtepBbNVMz011ibAjM42N2PicvqU9tib9n43AURiaq6CKCqEoGo9iahsNNsTSiaqANMmfCbK0kZhQ/132" width="30px"><span>机器人</span> 👍（51） 💬（2）<div>那么跨网段调用中，是如何获取目标IP 的mac地址的？根据讲解推理应该是从源IP网关获取所在网关
mac,然后又替换为目标IP所在网段网关的mac,最后是目标IP的mac地址，不知对否</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/39/60d6a10d.jpg" width="30px"><span>天涯囧侠</span> 👍（47） 💬（2）<div>在一个有dhcp的网络里，如果我手动配置了一个IP，dhcp Server会知道这个信息，并不再分配这个IP吗？会的话具体是怎样交互的呢？</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f8/bd/16545faf.jpg" width="30px"><span>陈浩佳</span> 👍（38） 💬（3）<div>我分享一个我最近遇到的问题:
最近我们的设备增加了dhcp自动分配地址的功能。我把几台设备连到同个路由器上，但是发现每台设备最后分配到的ip都是一样的，我登录了路由器里面查看，显示的设备列表确实是ip都是一致的，mac地址是不一致的。。。。所以就觉得有点奇怪。不过这里要说明的是，设备的mac地址是我们自己程序里面设置的，网卡不带mac地址的----最后查看代码发现，我们设备代码是先启动了dhcp客户端，后面再设置了mac地址，这里就有问题了，所以，我把它倒过来，先设置mac地址，再启动dhcp客户端，这样就解决问题了。。。由于原先启动dhcp的时候还未设置mac地址，所以默认的mac地址都是一致的，所以获取的ip都是一致的。但是，这里也说明一个问题，路由器列表上的mac地址不一定就是分配ip时的mac地址，如果分配到ip后再去修改mac地址，也是会同步到路由器上的，但是不会重新分配ip。
</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/95/dd73022c.jpg" width="30px"><span>我是曾经那个少年</span> 👍（38） 💬（1）<div>看了虽然懂了，但是对于一个做软件开发的，不知道怎么去实战！</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/f1/432e0476.jpg" width="30px"><span>X</span> 👍（36） 💬（1）<div>进入BIOS设置页面，有一项PXE Boot to LAN，若设置为Enabled则表示计算机从网络启动，从PXE服务端下载配置文件和操作系统内核进行启动；若设置为Disabled则表示从本地启动，启动动BIOS后，会去寻找启动扇区，如果没有安装操作系统，就会找不到启动扇区，这个时候就启动不起来。</div>2018-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（35） 💬（6）<div>跨网段的通信，一般都是ip包头的目标地址是最终目标地址，但2层包头的目标地址总是下一个网关的，是么？</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/fd/8022b3a2.jpg" width="30px"><span>penghuster</span> 👍（32） 💬（1）<div>请教一下，pxe客户端请求的IP，是否最终会直接用于系统</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（32） 💬（1）<div>要是以前大学老师能够讲得如此精彩，易懂，大学就不会白学了</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/97/8d7a6460.jpg" width="30px"><span>卡卡</span> 👍（25） 💬（1）<div>pxe要去tftp下载初始文件，那么pxe自己是不是也需要一个tftp客户端？</div>2018-05-25</li><br/><li><img src="" width="30px"><span>呵呵</span> 👍（20） 💬（1）<div>pxe客户端是放在哪里的？</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/94/05044c31.jpg" width="30px"><span>踢车牛</span> 👍（10） 💬（3）<div>老师，你好，上面你提到网关至少和当前一个网络的一个网卡在同一个网段内，这么说网关上可以配置多个网卡，
假如网关上有两个网卡，其中一个是192.168.1.6，另一个是
16.158.23.X,这样包可以发出去么？</div>2018-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/cd/3aff5d57.jpg" width="30px"><span>Alery</span> 👍（9） 💬（7）<div>“如果你配置了网关的话，Linux 会获取网关的 MAC 地址，然后将包发出去。对于 192.168.1.6 这台机器来讲，虽然路过它家门的这个包，目标 IP 是它，但是无奈 MAC 地址不是它的，所以它的网卡是不会把包收进去的。”

刘老师，网络包到达网关，根据第一章网关应该也是会通过ARP协议大吼一声谁的ip地址是192.168.1.6，当192.168.1.6这台主机发现在叫自己就会响应网关他的mac地址，这样不就有获得192.168.1.6主机的mac地址了吗？</div>2018-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fe/8f/466f880d.jpg" width="30px"><span>没心没肺</span> 👍（8） 💬（1）<div>当年联机打C&amp;C，眼看快要败了，偷偷拧掉终结器……嘿嘿……</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/ce/a8c8b5e8.jpg" width="30px"><span>Jason</span> 👍（7） 💬（1）<div>大道至简。牛</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（6） 💬（1）<div>想问一下老师，为什么要用tftp而不是ftp，我记得ap更新系统也是tftp</div>2018-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5b/b9/d07de7c6.jpg" width="30px"><span>FLOSS</span> 👍（6） 💬（1）<div>交换机，路由器，集线器这些东西的区别是什么？DHCP是不是只有在路由器中有？ARP协议是PC对PC的还是，PC给路由器，然后路由器再给另外一台PC，路由器有自己的MAC地址吗？</div>2018-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/af/73/946c4638.jpg" width="30px"><span>🤘🤘🤘</span> 👍（5） 💬（1）<div>Clients requesting renewal of an existing lease may communicate directly via UDP unicast, since the client already has an established IP address at that point. Additionally, there is a BROADCAST flag (1 bit in 2 byte flags field, where all other bits are reserved and so are set to 0) the client can use to indicate in which way (broadcast or unicast) it can receive the DHCPOFFER: 0x8000 for broadcast, 0x0000 for unicast.[4] Usually, the DHCPOFFER is sent through unicast. For those hosts which cannot accept unicast packets before IP addresses are configured, this flag can be used to work around this issue.  维基上说的是两种选择(广播和单播 通常为单播)</div>2019-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/35/3b8372c5.jpg" width="30px"><span>chinhu ko</span> 👍（5） 💬（1）<div>为什么我的网卡标识一个是 enp5s0f1 ,一个是 lo ,一个是 wlp4s0 ,没有你提到的 eth0 和 eth1 ？</div>2018-05-26</li><br/><li><img src="" width="30px"><span>Subhuti</span> 👍（4） 💬（1）<div>在这个广播包里面，新人大声喊：我是新来的（Boot request），我的 MAC 地址是这个，我还没有 IP，谁能给租给我个 IP 地址！
请问，目标端口67，这个是如何获得的呢？</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/0a/e564e572.jpg" width="30px"><span>N_H</span> 👍（4） 💬（1）<div>网关是硬件吗？</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/88/fe/c18a85fe.jpg" width="30px"><span>随风</span> 👍（4） 💬（1）<div>pxe在bios后面启动，那时候还没有操作系统，也就没有文件系统，那下载的文件存放在何处呢？小白求解！</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ca/61/b3f00e6f.jpg" width="30px"><span>byte</span> 👍（4） 💬（1）<div>客户端和DHCP server的识别在MAC和IP层都是广播地址，他们通过BTOOP的协议内容来识别是否为自己的应答？</div>2018-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/0f/1f229bf5.jpg" width="30px"><span>Void_seT</span> 👍（4） 💬（1）<div>我印象中10.0.0.1&#47;24是路由器地址，这是把这台机器配成路由器了么？配成10.0.0.2&#47;24也没问题吧？</div>2018-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（3） 💬（1）<div>吼是同一个网段 是arp协议在发挥作用 是在找mac地址相同的机器 是在二层设备里发生的事情</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0f/70/759b1567.jpg" width="30px"><span>张飞online</span> 👍（3） 💬（1）<div>在上面是，先判断目的地址是不是在同一网段，然后确定是否发arp广播，还是先发广播，发现没有应答，然后发网关</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/d2/71987d0b.jpg" width="30px"><span>夜禹</span> 👍（3） 💬（1）<div>老师，跨网段请求如果在外面没找到目标MAC，就不会回子网找了吗</div>2018-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/69/5f1f0d1c.jpg" width="30px"><span>支离书</span> 👍（3） 💬（1）<div>学习了，pxe客户端获取到的操作系统最后安装到硬盘上了吗？如何安装的？pxe写启动扇区吗？</div>2018-06-22</li><br/>
</ul>