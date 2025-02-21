前面我们讲到了数据中心，里面很复杂，但是有的公司有多个数据中心，需要将多个数据中心连接起来，或者需要办公室和数据中心连接起来。这该怎么办呢？

- 第一种方式是走公网，但是公网太不安全，你的隐私可能会被别人偷窥。
- 第二种方式是租用专线的方式把它们连起来，这是土豪的做法，需要花很多钱。
- 第三种方式是用VPN来连接，这种方法比较折中，安全又不贵。

![](https://static001.geekbang.org/resource/image/9f/68/9f797934cb5cf40543b716d97e214868.jpg?wh=707%2A500)

**VPN**，全名**Virtual Private Network**，**虚拟专用网**，就是利用开放的公众网络，建立专用数据传输通道，将远程的分支机构、移动办公人员等连接起来。

## VPN是如何工作的？

VPN通过隧道技术在公众网络上仿真一条点到点的专线，是通过利用一种协议来传输另外一种协议的技术，这里面涉及三种协议：**乘客协议**、**隧道协议**和**承载协议**。

我们以IPsec协议为例来说明。

![](https://static001.geekbang.org/resource/image/52/7f/52c72a2a29c6b8526a243125e101f77f.jpeg?wh=1498%2A413)

你知道如何通过自驾进行海南游吗？这其中，你的车怎么通过琼州海峡呢？这里用到轮渡，其实这就用到**隧道协议**。

在广州这边开车是有“协议”的，例如靠右行驶、红灯停、绿灯行，这个就相当于“被封装”的**乘客协议**。当然在海南那面，开车也是同样的协议。这就相当于需要连接在一起的一个公司的两个分部。

但是在海上坐船航行，也有它的协议，例如要看灯塔、要按航道航行等。这就是外层的**承载协议**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/61/c3/5f1ec5e5.jpg" width="30px"><span>徐晨</span> 👍（249） 💬（9）<div>@Fisher 
我可以举个例子，比如说我们先约定一种颜色比如黄色（p, q 大质数），这时候我把黄色涂上红色（我的随机数 a）生成新的橙色，你把黄色涂上蓝色（你的随机数 b）生成新的绿色。这时候我们交换橙色和绿色，然后我再在绿色上加上红色生成棕色，同样你拿到橙色后加上蓝色也生成棕色。这就是最终的密钥了。如果有人在中间窃取的话，他只能拿到橙色和绿色，是拿不到最终的密钥棕色的。</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/c7/a147b71b.jpg" width="30px"><span>Fisher</span> 👍（11） 💬（3）<div>花了两个小时做了笔记，除了最后的 MPLS VPN前面的基本都理解了

有一个问题，在 DH 算法生成对称密钥 K 的时候，需要交换公开质数 pq 然后生成公钥 AB，交换 AB 生成密钥 K

这个交换过程虽然没有直接交换密钥，但是如果我是个中间人，拿到了所有的材料，我也是可以生成同样的密钥的吧？那这样怎么保证安全性？还是说我理解的不对，这个过程没法出现中间人？希望老师能够解答一下

做的笔记：https:&#47;&#47;mubu.com&#47;doc&#47;1cZYndRrAg</div>2018-07-07</li><br/><li><img src="" width="30px"><span>起风了001</span> 👍（9） 💬（4）<div>我有一个问题, 就是私钥交换协议这么厉害,为什么不在HTTPS协议上也加入这个呢? 这样就不需要证书了呀?</div>2019-05-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6a8fRQFxX5VXOpRKyYibsemKwDMexMxkzZOBquPo6T4HOcYicBiaTcqibDoTIhZSjVjF3nKXTEGDYOGPt2xqqwiawjg/132" width="30px"><span>咩咩咩</span> 👍（3） 💬（1）<div>想弱弱问一下:文中VPN和平时说的挂个VPN翻墙是两个不同的概念吗</div>2019-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eov38ZkwCyNoBdr5drgX0cp2eOGCv7ibkhUIqCvcnFk8FyUIS6K4gHXIXh0fu7TB67jaictdDlic4OwQ/132" width="30px"><span>珠闪闪</span> 👍（3） 💬（1）<div>看的有些懵。意图是来了解一下VPN如何连接丝网和公网连接的技术，老师直接讲到报文层次，没有太多的介绍网络如何打通进行业务传输。同求老师如何这么深刻理解这些网络技术的，感叹跟老师的差距真实望尘莫及~</div>2019-04-28</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIa4aLtpt1wiagBzKGKicQX3KyaulgVzmIdaSj38yYWXPBpK5gjw7Gp4EicTzq34R6raTh1ftAXBHqNA/132" width="30px"><span>大旗</span> 👍（2） 💬（1）<div>SDW 和MPLS的区别在哪里呢？</div>2019-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（2） 💬（1）<div>IPSec在隧道模式下，新IP地址的如何加上去的呢？</div>2019-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/2a/446d7a1f.jpg" width="30px"><span>Ruter</span> 👍（1） 💬（1）<div>老师讲的专业啊，感觉越来越难了，但是也得说这课买的太直了。</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>跟不上了，多看几遍  需要老师的知识图谱</div>2019-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/fc/5d901185.jpg" width="30px"><span>vic</span> 👍（1） 💬（2）<div>既然有对称密钥M为何还要生成对称密钥K来做加密传输？</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（1） 💬（1）<div>IP转发是查路由表，标签转发是查标签表，为什么说标签转发就比路由表快呢？  
还有我一直不明白的是当访问一个网址的时候，一般给的都是公有地址。何时我们才能获得要访问的是私有地址呢</div>2018-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/bc/88a905a5.jpg" width="30px"><span>亮点</span> 👍（1） 💬（1）<div>刘老师您好，我有两个疑问。1、讲解HTTPS章节的时候介绍过对称密钥的生成方法，和本节的生成方法不同，就是说对称密钥有多种生成方法吗？为什么不采用一样的呢？2、本节的对称密钥K和M，文中介绍防止被破解，会定期更新M，哪如何防止K被破解呢？</div>2018-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（0） 💬（1）<div>P（Provider）：这里特指运营商网络中除 PE 之外的其他运营商网络设备

这句话怎么理解为：P就是公网外除PE的其他路由设备，即包括相同运营商，也包括其他运营商。
但是下文又理解为是同一个运营商的网络设备，求解释一下~</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/d4/755f058b.jpg" width="30px"><span>bboot9001</span> 👍（0） 💬（1）<div>你好老师 能解释一下 vpn客户端依赖的虚拟网卡的作用吗？</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/bc/88a905a5.jpg" width="30px"><span>亮点</span> 👍（83） 💬（2）<div>近期两节内容跳跃好厉害，跟不上了😁 </div>2018-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/41/e3ece193.jpg" width="30px"><span>lovelife</span> 👍（49） 💬（0）<div>公有云和私有云之间打通主要通过两种方式，一种是专线，这个需要跟运营商购买，而且需要花时间搭建。一种是VPN, VPN包括今天说的IPSec VPN和MPLS VPN。这个还需要在公有云厂商那边购买VPN网关，将其和私有云的网关联通</div>2018-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/52/034eb0f1.jpg" width="30px"><span>Liutsing</span> 👍（11） 💬（2）<div>能讲讲VPN跟ngrok内网穿透的区别么？</div>2018-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/e5/6899701e.jpg" width="30px"><span>favorlm</span> 👍（6） 💬（0）<div>1通过路由端口映射，或者vpn
2.移动端上网需要gprs协议层</div>2018-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/29/2a/9079f152.jpg" width="30px"><span>谢真</span> 👍（5） 💬（0）<div>这篇文章讲的太好了，信息量很大，非常解惑，以前只知道概念，不知道有什么用，现在知道协议的由来了</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/4f/e0b71e72.jpg" width="30px"><span>我是谁</span> 👍（5） 💬（0）<div>感觉越来越难了，没办法多看几遍吧</div>2018-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/b1/982ea185.jpg" width="30px"><span>美妙的代码</span> 👍（5） 💬（0）<div>老师，独家网络协议图，大家都需要啊。 公有云与私有云 还是用 Mpls 。</div>2018-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/97/8e14e7d0.jpg" width="30px"><span>楚人</span> 👍（4） 💬（0）<div>老师能简单介绍一下专线吗？专线架设等</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/37/3f/a9127a73.jpg" width="30px"><span>KK</span> 👍（3） 💬（0）<div>就是一个VPN，居然有这么复杂的交互在里面。真的涨姿势啦。</div>2020-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（3） 💬（0）<div>请问老师打标签的方式为什么比查路由快?打标签每跳路由器还得写数据包，查路由表查找到之后转发出去就行了。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ae/e0/3e636955.jpg" width="30px"><span>李博越</span> 👍（3） 💬（0）<div>最近用minikube本地搭建个环境玩玩，发现了很多镜像pull超时的问题，我把本地iterm设置了socks5代理以后，手工pull镜像还是失败：
➜  ~ minikube ssh -- docker pull k8s.gcr.io&#47;pause-amd64:3.1
Error response from daemon: Get https:&#47;&#47;k8s.gcr.io&#47;v2&#47;: net&#47;http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
尝试curl看看代理是否成功：
➜  ~ curl -ik &quot;https:&#47;&#47;k8s.gcr.io&#47;v2&#47;&quot;
HTTP&#47;1.1 200 Connection established
尝试ping，却ping不通k8s.gcr.io域名
➜  ~ ping k8s.gcr.io
PING googlecode.l.googleusercontent.com (64.233.189.82): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2

查了下socks5应该是属于会话层的，而icmp是三层协议，因此ping没有走代理所以翻不了墙，然后curl走应用层因此被代理了所以返回200，但是为啥执行minikube ssh -- docker pull k8s.gcr.io&#47;pause-amd64:3.1拉不下来镜像呢？</div>2018-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/61/44/66cd6f3f.jpg" width="30px"><span>A7</span> 👍（3） 💬（0）<div>终于开始上难度了</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5c/02/e7af1750.jpg" width="30px"><span>teddytyy</span> 👍（2） 💬（2）<div>既然密钥传输是可行的，那https为啥不直接用对称加密？</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（1） 💬（0）<div>逐渐看不懂系例+1</div>2022-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKTAKspiaW6t3IWicYjIfyRskFYibBauMW79vhXWI6CNj0L7jmQs1X9wZg8pricNQWNHXGFzw2ibQkAKtA/132" width="30px"><span>Geek_2446b7</span> 👍（1） 💬（0）<div>最开始几章看到有人留言说老师用的比喻太多了，导致阅读体验下降，当时的也有同感。然而从这一章上难度（或者说这部分知识比较陌生）开始发现比喻确实挺有用的，而之前只是因为当时那部分知识可能自己相对熟悉一些。</div>2022-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/83/93d389ba.jpg" width="30px"><span>我是谁</span> 👍（1） 💬（1）<div>有个问题哈

已知p、q和 算法q^a mod p（q^b mod p）不就可以反推a和b了吗？</div>2021-03-15</li><br/>
</ul>