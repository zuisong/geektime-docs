你好，我是小李同学，坐标深圳，是一名嵌入式开发工程师，已经工作 4 年了，目前主要从事维护系统稳定性的相关工作。今天我主要想跟你分享下我学习 eBPF 的“心路历程”，以及在这门课中的一些收获。

## 多次试图“入门”，始终不得其法

我最早接触到 eBPF 是在一篇公众号文章上，上面介绍说它是内核调试的一把利器。当时我就想了：这不是跟我平时的工作联系很密切吗？在调试死机、分析代码路径的时候应该都能用到！eBPF 的强大功能让我很激动，当时就想上手试试，看看能不能把这门技术用起来。

想象很美好，但是真正开始学习的时候却发现有些棘手。我先是找了一堆资料。关于eBPF 的资料网上倒是有很多，但是不够系统，很多资料讲解也不够细致深入，总觉着看起来不太明白。特别是有一些文章，上来直接把整个 ebpf 的原理图一贴，然后就直接懵了。

我当时想，既然看原理看不懂，那就先跑起来看看吧！我尝试了下大家说的一些适合入门的 eBPF 工具集，结果发现它们都是基于服务器使用的。而我的工作环境基本都是嵌入式平台，像 BCC 这样的工具集没法直接使用。自己折腾了下，环境没有搭建起来，第一次的尝试“入门”就这么宣告失败了。

再次看到 eBPF，是见有人推荐《BPF 之巅》和《Linux 内核观测技术 BPF》这两本书。推荐的同学说自己收获很大，我就第一时间下单了，希望能从书中找到进入 eBPF 世界的法门。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/3b/2a/f05e546a.jpg" width="30px"><span>🐮</span> 👍（1） 💬（1）<div>倪老师，我也遇到小李同学一样的问题，我也是搞嵌入式设备的，想看看能否在嵌入式设备中把ebpf用起来， 怎么可以联系到他啊，相互交流交流；</div>2022-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e6/ee/8fdbd5db.jpg" width="30px"><span>Damoncui</span> 👍（2） 💬（0）<div>更新啦更新啦~ 沙发是我的~</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/11/5e/ba72c3af.jpg" width="30px"><span>乖，摸摸头</span> 👍（0） 💬（0）<div>我也是做嵌入式的，正好能用上，感谢分享</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/07/8d/3e76560f.jpg" width="30px"><span>王建峰</span> 👍（0） 💬（0）<div>GOOD！！</div>2022-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/b0/14fec62f.jpg" width="30px"><span>不了峰</span> 👍（0） 💬（1）<div>老师，想请问一个网络问题
两台 Linux主机 （做 Oracle RAC 集群）  REHT 7.5版本。每主机两网卡绑定，方式是:roundrobin 。连同一个交换机。

遇到的问题是
从A机 ping B 机 ： 不规则的掉包。 ping -s 1500 全掉。
从B机 ping A 机 ： 结果同样是： 不规则的掉包。 ping -s 1500 全掉。

从业务网络ping A 正常， ping B机， 结果同上。 怀疑是B机的问题。

B机现在这个 网卡没有什么流量（因为业务访问流量都转到A机去了）。

想问：有没有什么方法  排查 B机，或是这个方面的问题？
主机负载空， teamdctl team0 stat ,ethtools -S 网卡 ｜grep error  也都没有错。。</div>2022-06-09</li><br/>
</ul>