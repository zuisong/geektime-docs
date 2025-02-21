你好，我是程远。

从这一讲开始，我们进入到了容器网络这个模块。容器网络最明显的一个特征就是它有自己的Network Namespace了。你还记得，在我们这个课程的[第一讲](https://time.geekbang.org/column/article/308108)里，我们就提到过Network Namespace负责管理网络环境的隔离。

今天呢，我们更深入地讨论一下和Network Namespace相关的一个问题——容器中的网络参数。

和之前的思路一样，我们先来看一个问题。然后在解决问题的过程中，更深入地理解容器的网络参数配置。

## 问题再现

在容器中运行的应用程序，如果需要用到tcp/ip协议栈的话，常常需要修改一些网络参数（内核中网络协议栈的参数）。

很大一部分网络参数都在/proc文件系统下的[/proc/sys/net/](https://www.kernel.org/doc/Documentation/sysctl/net.txt)目录里。

**修改这些参数主要有两种方法：一种方法是直接到/proc文件系统下的"/proc/sys/net/"目录里对参数做修改；还有一种方法是使用[sysctl](https://man7.org/linux/man-pages/man8/sysctl.8.html)这个工具来修改。**

在启动容器之前呢，根据我们的需要我们在宿主机上已经修改过了几个参数，也就是说这些参数的值已经不是内核里原来的缺省值了.

比如我们改了下面的几个参数：

```shell
# # The default value:
# cat /proc/sys/net/ipv4/tcp_congestion_control
cubic
# cat /proc/sys/net/ipv4/tcp_keepalive_time
7200
# cat /proc/sys/net/ipv4/tcp_keepalive_intvl
75
# cat /proc/sys/net/ipv4/tcp_keepalive_probes
9
 
# # To update the value:
# echo bbr > /proc/sys/net/ipv4/tcp_congestion_control
# echo 600 > /proc/sys/net/ipv4/tcp_keepalive_time
# echo 10 > /proc/sys/net/ipv4/tcp_keepalive_intvl
# echo 6 > /proc/sys/net/ipv4/tcp_keepalive_probes
#
 
# # Double check the value after update:
# cat /proc/sys/net/ipv4/tcp_congestion_control
bbr
# cat /proc/sys/net/ipv4/tcp_keepalive_time
600
# cat /proc/sys/net/ipv4/tcp_keepalive_intvl
10
# cat /proc/sys/net/ipv4/tcp_keepalive_probes
6
```
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（15） 💬（2）<div># nsenter -t &lt;pid&gt; -n bash -c &#39;echo 600 &gt; &#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_keepalive_time&#39; （root 用户）
$ sudo nsenter -t &lt;pid&gt; -n sudo bash -c &#39;echo 600 &gt; &#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_keepalive_time&#39; （非 root 用户）

其中，&lt;pid&gt; 表示容器 init 进程在宿主机上看到的 PID。</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/60/71ed6ac7.jpg" width="30px"><span>谢哈哈</span> 👍（7） 💬（3）<div>宿主机的进入容器网络地址空间通过nsenter --target $(docker inspect -f {.State.Pid}) --net</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/62/c4/be92518b.jpg" width="30px"><span>🐭</span> 👍（4） 💬（1）<div>既然nsenter与docker exec 原理一样，为啥nsenter修改proc&#47;sys&#47;net不会报错无权限呢</div>2021-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/b0/b073fe8b.jpg" width="30px"><span>aMaMiMoU</span> 👍（4） 💬（2）<div>老师您好，有几个问题能否帮忙解答下，谢谢
1.在&#47;proc&#47;sys&#47;net 的诸多参数里，如何确认哪些是host level 哪些是容器level的呢？
2.对于host level的这些参数，在启动容器的时候通过sysctl能修改么？如果能修改，是不是相当于同时影响了同host里其他容器的运行时参数呢？</div>2020-12-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（4） 💬（1）<div>这些问题文档上都没写，还是老师功力高，场景多。
请教个问题，对于proc文件系统的其他目录容器怎么隔离的呢，比如在容器里面free命令看到的是宿主机的内存。</div>2020-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4Lprf2mIWpJOPibgibbFCicMtp5bpIibyLFOnyOhnBGbusrLZC0frG0FGWqdcdCkcKunKxqiaOHvXbCFE7zKJ8TmvIA/132" width="30px"><span>Geek_c2089d</span> 👍（3） 💬（1）<div>老师，咨询一个问题，就是我有一个容器里面有两个服务，映射出8000和9000的端口，在容器内会出现8000端口的服务访问宿主机ip：9000的端口不通，但是我service iptables stop ; seriver docker stop ;
server docker start ; 就可以访问了。一旦reboot就不行了。请问是怎么样的问题
 </div>2021-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f2/73/1c7bceae.jpg" width="30px"><span>乔纳森</span> 👍（2） 💬（1）<div>我们是在 initContainers 中 执行 如下来修改容器内的内核参数的，需要privileged: true
mount -o remount rw &#47;proc&#47;sys
          sysctl -w net.core.somaxconn=65535</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（1） 💬（1）<div>老师，为啥隔离的这些网络参数不和 &#47;sys&#47;fs&#47;cgroup&#47;net_cls,net_prio,cpu,pid 等一样，统一放在&#47;sys&#47;fs&#47;cgroup&#47;下面，而是跟宿主机共用一套 ？</div>2021-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a5/3c/7c0d2e57.jpg" width="30px"><span>程序员老王</span> 👍（1） 💬（2）<div>网卡是通过端口号来区分栈数据吧，命名空间在这里隔离是网络参数配置吗？还是网卡</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8b/65/0f1f9a10.jpg" width="30px"><span>小Y</span> 👍（0） 💬（1）<div>来到网络的章节基本不太懂，得多听几遍，多补充补充了😆</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（23） 💬（2）<div>docker exec、kubectl exec、ip netns exec、nsenter 等命令原理相同，都是基于 setns 系统调用，切换至指定的一个或多个 namespace(s)。 </div>2020-12-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqYia7VlBNus8kg5daQyb0AywUMMFWH2eUyTIDfBa3tua0Giaxtmx9icxLWyoHTHjo9bFoGOLWMYIdyA/132" width="30px"><span>麻瓜镇</span> 👍（4） 💬（1）<div>为什么有的参数是从host namespace复制，有的参数直接使用缺省值呢？为什么要这样设计？</div>2021-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/JWoFanyWDk7lWL7g8rLYI0icH1XOVoCyjR9HoMzliauxggPSWWeYVleqKwiaUnBEChfIctoFzVoBqqVT3Lot18Srg/132" width="30px"><span>Geek_fd78c0</span> 👍（1） 💬（1）<div>想问一下，容器启动时网络是桥接模式，启动以后，如何新增容器中端口到host端口的映射？</div>2022-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7b/b3/194f7f90.jpg" width="30px"><span>没伞的孩子得使劲奔跑</span> 👍（0） 💬（0）<div>Kubernetes 里的allowed-unsafe-sysctls 这个特性，需要1.21版本，老版本可以尝试在initcontainer初始化，但是需要privileged权限

Docker 的–sysctl 这个学到了.

之前我也一直理解docker 本质是一个进程，有隔离机制，也没想到net内核参数也被隔离了。</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（0）<div>不仅学习到了docker命令的--sysctl参数的用法，还了解到了其原理，真是酣畅淋漓。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d6/43/0704d7db.jpg" width="30px"><span>cc</span> 👍（0） 💬（0）<div>&quot;tcp_congestion_control 的值是 bbr，和宿主机 Network Namespace 里的值是一样的，而其他三个 tcp keepalive 相关的值，都不是宿主机 Network Namespace 里设置的值，而是原来系统里的缺省值了。&quot;
------
这里比较困惑，为什么要这样设计呢？</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ce/58/71ed845f.jpg" width="30px"><span>Dexter</span> 👍（0） 💬（1）<div>pid =  clone(new_netns, stack + STACK_SIZE, CLONE_NEWNET | SIGCHLD, NULL);  代码例子中的一段， clone系统调用中的参数，new_netns和 CLONE_NEWNET flag这两者有什么关系呢？</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/04/3f/f28d76c5.jpg" width="30px"><span>Shone</span> 👍（0） 💬（0）<div>CY老师，这里我又想起最近遇到的rp_filter 的问题，因为我们的slb用的是ipvs tunnel，需要给应用pod设置tun0设备并且绑定vip，同时还需要设置rp_filter为0或者2。这里我们遇到的问题是有时候node上的这个配置会被改成1，导致ipvs数据面不工作，解决办法是把node上这个值设为0，但是我发现这个时候pod eth0这个值是1，它对应的calico这个值也是1，所以这种情况下好像是node的rp_filter会覆盖其它的设置，对这里不是很理解了。</div>2021-01-10</li><br/>
</ul>