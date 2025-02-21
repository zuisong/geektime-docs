你好，我是Tony Bai。

在上一讲中，我们初步实现了一个基于TCP的自定义应用层协议的通信服务端。对于一个常驻内存的服务端而言，更高的性能以及更低的资源消耗，始终是后端开发人员的追求。同时，更高性能的服务程序，也意味着在处理相同数量访问请求的前提下，我们使用的机器数量更少，这可是为公司节省真金白银的有效策略。

而且，Go语言最初设计时就被定位为“系统级编程语言”，这说明高性能也一直是Go核心团队的目标之一。很多来自动态类型语言的开发者转到Go语言，几乎都有着性能方面的考量。

所以，在实战篇的最后一讲，我们就结合上一讲实现的自定义应用层协议的通信服务端，看看优化Go程序使用的常用工具与套路，给你引引路。

## Go程序优化的基本套路

Go程序的优化，也有着固定的套路可循，这里我将它整理成了这张示意图：

![](https://static001.geekbang.org/resource/image/76/ce/767f360c71dece48b9c68dc46053yyce.jpg?wh=1980x1080)

这张图也不难理解，我简单解释一下。

**首先我们要建立性能基准。**要想对程序实施优化，我们首先要有一个初始“参照物”，这样我们才能在执行优化措施后，检验优化措施是否有效，所以这是优化循环的第一步。

**第二步是性能剖析。**要想优化程序，我们首先要找到可能影响程序性能的“瓶颈点”，这一步的任务，就是通过各种工具和方法找到这些“瓶颈点”。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/46/dfe32cf4.jpg" width="30px"><span>多选参数</span> 👍（8） 💬（1）<div>原本以为最后的实战课只是写一个稍微大点的项目。结果，恰恰相反，老师使用一个极小的项目，带着走了一遍 Go 开发和调优的过程，这种方法论或者思想的传授，真的比单纯写代码可以学到更多，是在其他书籍或专栏所没有的，很喜欢这种方式！感谢老师！

简单总结下，最后实战课核心的内容：
1. Go 开发的流程结合自己的几个月的经历，总结下：（1）首先是明确问题或需求，之后根据问题或需求，提炼出需要用到的技术点，比如 socket 技术；（2）之后，去调研相关的技术或相关项目；（3）最后写设计方案；（4）根据设计方案，实现代码。（PS：这个过程可以循环迭代）
2. Go 程序优化的过程：（1）首先是明确衡量指标，比如某个函数的执行时间、程序在一定时间内可以处理的请求量、接受的数据包数量等等（并获取首次的指标情况）；（2）之后，使用 pprof 获取 CPU、内存的使用情况，并分析使用情况，得到整个程序的瓶颈所在；（3）最后，根据分析得到的结果，优化源码；（4）优化源码后，再次测试衡量指标，根据新获取的指标情况，决定是否继续分析和优化。

另外，可以继续优化点的应该就是与 Submit 使用相同的地方，比如 submitAck。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（6） 💬（2）<div>什么时候能和老师一样有如此丰富的优化经验呢，讲的非常精彩。</div>2022-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（3） 💬（1）<div>精彩的优化过程！感谢老师这个专栏，很喜欢这种讲解知识点的方式！第一遍结束，第二遍开始记笔记分析每一行代码，第三遍再过下老师的两本书，应该算是完全入门go了</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/cb/18/0139e086.jpg" width="30px"><span>骚动</span> 👍（3） 💬（2）<div>mac下的配置参考：
1. mac不能用host，需要用ports端口映射
version: &quot;3.2&quot;
services:
  prometheus:
    container_name: prometheus
    image: prom&#47;prometheus:latest
    ports:
      - &quot;9090:9090&quot;
    volumes:
      - .&#47;conf&#47;tcp-server-prometheus.yml:&#47;etc&#47;prometheus&#47;prometheus.yml
      - &#47;etc&#47;localtime:&#47;etc&#47;localtime
    restart: on-failure

  grafana:
    container_name: grafana
    image: grafana&#47;grafana:latest
    restart: on-failure
    ports:
      - &quot;3000:3000&quot;
    volumes:
      - &#47;etc&#47;localtime:&#47;etc&#47;localtime
      - .&#47;data&#47;grafana:&#47;var&#47;lib&#47;grafana

  node_exporter:
    image: quay.io&#47;prometheus&#47;node-exporter:latest
    restart: always
    container_name: node_exporter
    command:
      - &#39;--path.rootfs=&#47;host&#39;
    ports:
      - &quot;9100:9100&quot;
    volumes:
      - &#47;Users&#47;zouqiang&#47;Documents&#47;docker&#47;monitor&#47;data&#47;node_exporter

2. grafana上配置prometheus数据源时，url:  http:&#47;&#47;本机ip:端口 , 不要用http:&#47;&#47;localhost:9090这种方式，因为容器间的localhost不是同一个localhost, 用主机名直接指定即可</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/45/16c60da2.jpg" width="30px"><span>蔫巴的小白菜</span> 👍（3） 💬（1）<div>老师，有个问题，sync.pool也就是内存池那块，请求过来之后，我看到是直接放到内存池，没有置空数据，那么在内存池获取的时候，会不会出现数据错乱的问题呢？</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/4e/8798cd01.jpg" width="30px"><span>顷</span> 👍（3） 💬（2）<div>bufio.Reader.Read 方法内部，每次从 net.Conn 尝试读取其内部缓存大小的数据，而不是用户传入的希望读取的数据大小 -----------这里有个疑问，server端for 循环里不是每次都是重新读取到的conn传过来的数据吗，也就是每次client端发送过来的payload都是要有一次必要的读取，为什么会减少读取的次数呢？</div>2022-04-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5JKZO1Ziax3Ky03noshpVNyEvZw0pUwjLcHrHRo1XNPKXdmCE88homb6ltA15CdVRnjzjgGs3Ex42CaDbeYzNuQ/132" width="30px"><span>Geek_25f93f</span> 👍（2） 💬（1）<div>老师，看网上有种说法。池化这种事情，Java很早很早之前也做过 现在都不怎么提了，go的编译器太弱了？</div>2022-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/d9/75dd7cf9.jpg" width="30px"><span>Mew151</span> 👍（1） 💬（3）<div>老师，想问一下， tcp-server-demo2-with-pprof 的代码，我在我的 Mac 上分别启动 server 和 client ，过了一段时间后 server 报如下错误（打印是我加了些详细日志之后的）：

metrics server start ok(*:8889)
server start ok(on *:8888)
[2022-10-13 13:41:54.562] io.ReadFull: read tcp 127.0.0.1:8888-&gt;127.0.0.1:49689: read: operation timed out  totalLen is 28, n is 20
[2022-10-13 13:41:54.562] handleConn: frame decode error: read tcp 127.0.0.1:8888-&gt;127.0.0.1:49689: read: operation timed out
[2022-10-13 13:41:55.545] io.ReadFull: read tcp 127.0.0.1:8888-&gt;127.0.0.1:49754: read: operation timed out  totalLen is 32, n is 15
[2022-10-13 13:41:55.545] handleConn: frame decode error: read tcp 127.0.0.1:8888-&gt;127.0.0.1:49754: read: operation timed out
[2022-10-13 13:41:55.590] io.ReadFull: read tcp 127.0.0.1:8888-&gt;127.0.0.1:49729: read: operation timed out  totalLen is 31, n is 26
...

请问这是什么原因呢？我看程序里也没有设置 SetReadDeadline 的地方，为什么会报读超时呢</div>2022-10-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5JKZO1Ziax3Ky03noshpVNyEvZw0pUwjLcHrHRo1XNPKXdmCE88homb6ltA15CdVRnjzjgGs3Ex42CaDbeYzNuQ/132" width="30px"><span>Geek_25f93f</span> 👍（1） 💬（3）<div>老师，这个frame.decode解包过程为什么不会出现粘包的现象啊？按理说收到这个frame部分也可能出现半包的情况啊，为什么我不管怎么试 在服务端加sleep时间 或者 加client的发送包体长度和协程数量，也没办法进入 if n != int(totalLen-4) 这个判断分支呀</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（1） 💬（2）<div>我这里Frame的Decode函数在读totalLen的时候会有小概率读到一个错误的数值，请问有人知道这是为什么吗？</div>2022-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（1） 💬（1）<div>对于工程师来说，这种量化的能力非常重要，只有量化了数据，才能找到瓶颈，而不是通过感觉去判断，白老师能利用这些工具将量化的过程讲的这么清晰，太强了</div>2022-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（1） 💬（1）<div>老师有时间的话，还能讲讲context相关的内容吗？</div>2022-01-29</li><br/><li><img src="" width="30px"><span>Geek_0d5d37</span> 👍（0） 💬（2）<div>老师，您好。在docker-compose.yml 文件的容器都没有看到有映射宿主机的端口，为什么可以访问对应几个端口的容器了。  PORTS 都是空白的

$docker ps 
CONTAINER ID   IMAGE                                     COMMAND                  CREATED        STATUS        PORTS     NAMES
563d655cdf90   grafana&#47;grafana:latest                    &quot;&#47;run.sh&quot;                26 hours ago   Up 26 hours             grafana
65616d1b6d1a   prom&#47;prometheus:latest                    &quot;&#47;bin&#47;prometheus --c…&quot;   26 hours ago   Up 26 hours             prometheus
b29d3fef8572   quay.io&#47;prometheus&#47;node-exporter:latest   &quot;&#47;bin&#47;node_exporter …&quot;   26 hours ago   Up 26 hours             node_exporter</div>2023-05-05</li><br/><li><img src="" width="30px"><span>Geek_xbye50</span> 👍（0） 💬（1）<div>老师讲的太精彩！很喜欢老师讲课！期待后续的课程</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3e/d1/17f3160c.jpg" width="30px"><span>军</span> 👍（0） 💬（1）<div>network_mode: host在mac不生效，改了ports映射的方式

The host networking driver only works on Linux hosts, and is not supported on Docker Desktop for Mac, Docker Desktop for Windows, or Docker EE for Windows Server.</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d4/2e/d9c38892.jpg" width="30px"><span>有</span> 👍（0） 💬（1）<div>跟着老师的教程完整的测了一遍，优化的效果太明显了，非常感谢老师准备这么好的课程，跟着大佬学习</div>2022-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>老师，判断packet的是submit还是submitack的时候可不可以用反射。我感觉这个项目还有很大的空间，比如连接包的定义还有关闭包甚至重连包，甚至可以可以模拟tcp的超时重传之类的。哈哈，后面可以慢慢的做，谢谢老师</div>2022-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/da/dcf8f2b1.jpg" width="30px"><span>qiutian</span> 👍（0） 💬（1）<div>老师，我想问下怎么进的Grafana页面，我运行了起来，然后访问:3000或者其他几个端口，都访问不了？查看三个运行的容器可以看到，浏览器进不了Grafana页面</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（0） 💬（1）<div>甭管是美发届还是技术圈，托尼老师一直值得信赖</div>2022-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/56/9d/4b2a7d29.jpg" width="30px"><span>ryanxw</span> 👍（0） 💬（1）<div>需要好好向大白老师学习，🐂</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（0） 💬（1）<div>老师给出的docker-compose.yml实测在linux下是没有问题的，但是在mac下不能直接运行。用mac的同学可以试试brew install 而不是docker来解决</div>2022-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/6d/3e570bb8.jpg" width="30px"><span>一打七</span> 👍（0） 💬（1）<div>在mac上的虚拟机里安装docker，修改了docker-compose.yml 文件，启动时进行了3000、9100、9090的端口映射，然后从mac的浏览器访问虚拟机的的3000端口，进入了grafana，配置了prometheus数据源，导入了1806仪表板，但是仪表板一直没有数据，老师能知道是哪里出了问题吗？谢谢</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/d7/f9/4c08ed90.jpg" width="30px"><span>邵康</span> 👍（0） 💬（0）<div>老师太NB了，完全不想入门课</div>2022-06-03</li><br/>
</ul>