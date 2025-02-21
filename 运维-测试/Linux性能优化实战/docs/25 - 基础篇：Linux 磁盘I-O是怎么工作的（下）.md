你好，我是倪朋飞。

上一节我们学习了 Linux 磁盘 I/O 的工作原理，并了解了由文件系统层、通用块层和设备层构成的 Linux 存储系统 I/O 栈。

其中，通用块层是 Linux 磁盘 I/O 的核心。向上，它为文件系统和应用程序，提供访问了块设备的标准接口；向下，把各种异构的磁盘设备，抽象为统一的块设备，并会对文件系统和应用程序发来的 I/O 请求，进行重新排序、请求合并等，提高了磁盘访问的效率。

掌握了磁盘 I/O 的工作原理，你估计迫不及待想知道，怎么才能衡量磁盘的 I/O 性能。

接下来，我们就来看看，磁盘的性能指标，以及观测这些指标的方法。

## 磁盘性能指标

说到磁盘性能的衡量标准，必须要提到五个常见指标，也就是我们经常用到的，使用率、饱和度、IOPS、吞吐量以及响应时间等。这五个指标，是衡量磁盘性能的基本指标。

- 使用率，是指磁盘处理I/O的时间百分比。过高的使用率（比如超过80%），通常意味着磁盘 I/O 存在性能瓶颈。
- 饱和度，是指磁盘处理 I/O 的繁忙程度。过高的饱和度，意味着磁盘存在严重的性能瓶颈。当饱和度为 100% 时，磁盘无法接受新的 I/O 请求。
- IOPS（Input/Output Per Second），是指每秒的 I/O 请求数。
- 吞吐量，是指每秒的 I/O 请求大小。
- 响应时间，是指 I/O 请求从发出到收到响应的间隔时间。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（29） 💬（4）<div>【D25打卡】
总结：
磁盘性能检测指标：
使用率：磁盘处理I&#47;O的时间百分比，使用率只考虑有没有I&#47;O，不考虑I&#47;O的大小。注意当使用率为100%时，由于可能存在并行I&#47;O，磁盘并不一定饱和，所以磁盘仍然可能接收新的I&#47;O请求
饱和度：磁盘处理I&#47;O的繁忙程度，注意当饱和度为100%时，磁盘不能接收新的I&#47;O请求
吞吐量：每秒I&#47;O请求大小
IOPS：Input&#47;Output Per Second 每秒的I&#47;O请求数
响应时间：I&#47;O请求从发出到收到响应的间隔时间

不孤立比较某项指标，结合读写比例、I&#47;O类型（随机还是连续）以及I&#47;O大小综合分析
例如：随机读写：多关注IOPS
          连续读写：多关注吞吐量

服务器选型时，对磁盘I&#47;O性能进行基础测试，使用 fio
磁盘I&#47;O观测：iostat
进程I&#47;O观测：pidstat,iotop
指导：遇到I&#47;O性能时，先通过iostat查看磁盘整体性能，然后用pidstat或iotop定位到具体的进程

疑惑：
对磁盘的使用率和饱和度还是没太理解，比如说磁盘的使用率达到100%，由于并行I&#47;O，不一定饱和了，所以还可能接收新的I&#47;O请求，还希望老师再指点下。</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/64/ad837224.jpg" width="30px"><span>Christmas</span> 👍（17） 💬（1）<div>一趟调度法，电梯调度法等调度是发生在磁盘控制器硬件上的吗？通用块层的调度是os级别的对吧？</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/ee/e3c4c9b3.jpg" width="30px"><span>Cranliu</span> 👍（8） 💬（2）<div>关于磁盘的饱和度，有没有经验值可以参考下呢？谢谢</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/65/ae/9727318e.jpg" width="30px"><span>Boy-struggle</span> 👍（7） 💬（3）<div>老师，如何根据系统调用判断IO为随机还是顺序，IO 的位置怎么体现，希望老师可以结合案例具体讲解一下，多谢！</div>2019-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/27/6679da14.jpg" width="30px"><span>程序员历小冰</span> 👍（6） 💬（2）<div>请问作者对《性能之垫-洞悉系统、企业和云计算》这本书的看法？适合作为工具书，用于查阅；还是可以进行通篇学习</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/84/d8e63885.jpg" width="30px"><span>仲鬼</span> 👍（5） 💬（3）<div>&quot;r_await+w_await ，就是响应时间&quot;
对这句表述有怀疑。
r_await、w_await分别是读、写请求的平均等待时间，二者相加什么都不是。因为a&#47;b + c&#47;d不等于(a+c)&#47;(b+d)。
</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（4） 💬（3）<div>仲鬼
2019-01-25

2
&quot;r_await+w_await ，就是响应时间&quot;
对这句表述有怀疑。
r_await、w_await分别是读、写请求的平均等待时间，二者相加什么都不是。因为a&#47;b + c&#47;d不等于(a+c)&#47;(b+d)。
展开
作者回复: 从公式上是这样，但间隔时间相同的时候呢？

man手册解释await是平均等待时间，我理解意思是toal wait time &#47; total req number，跟间隔时间无关
-----------------------------------------------
&quot;r_await、w_await分别是读、写请求的平均等待时间&quot;基于读写的平均等待时间没错，但是结果也是基于一定的时间范围内的，比如说过去1s，过去5s，显然间隔时间无论设置成多少，都是一样的.
即a&#47;t + b&#47;t = (a+b)&#47;t</div>2019-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/93/cfed7c6c.jpg" width="30px"><span>Vincent</span> 👍（2） 💬（1）<div>随机io和顺序io就跟数据结构有关系了吧？比如数组和链表。除了通过代码判断是随机io还是顺序io 系统有什么工具可以判断吗？</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/1d/12c7c021.jpg" width="30px"><span>挺直腰板</span> 👍（1） 💬（3）<div>老师，如何知道是随机IO还是顺序IO,两者性能差还是蛮大</div>2019-03-24</li><br/><li><img src="" width="30px"><span>fran712</span> 👍（1） 💬（2）<div>请问将&#47;dev&#47;sda直接挂载到某个目录和将磁盘只一个分区后，&#47;dev&#47;sda1挂载到某个目录，这两种挂载的区别是什么？</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/da/6a/91bd13de.jpg" width="30px"><span>张挺</span> 👍（0） 💬（3）<div>使用率指标不太理解，请问这个值是怎么计算出来的呢？</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（1）<div>老师在使用网络挂载的共享存储io性能差，有什么优化方式吗</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/56/115c6433.jpg" width="30px"><span>jssfy</span> 👍（0） 💬（1）<div>iotop可以看到在nfs上的流量不？</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/c1/d402bfbf.jpg" width="30px"><span>一生一世</span> 👍（0） 💬（1）<div>老师能否提供一些参数性能指标参考，有时候能看到指标却无法确定是否有问题</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/9e/3278e1d8.jpg" width="30px"><span>胡萝卜</span> 👍（0） 💬（2）<div>饱和度具体是怎么定义的呢？还是有的明白</div>2019-01-16</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（6） 💬（0）<div>day26打卡
之前都没用过fio测试磁盘实际性能，基本都是依赖磁盘型号查官网数据作为依据～
iostat和iotop倒是会经常用，之前有几列输出的内容自己理解有偏差，这下算是纠正过来了💪</div>2019-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/84/d8e63885.jpg" width="30px"><span>仲鬼</span> 👍（3） 💬（1）<div>&quot;r_await+w_await ，就是响应时间&quot;
对这句表述有怀疑。
r_await、w_await分别是读、写请求的平均等待时间，二者相加什么都不是。因为a&#47;b + c&#47;d不等于(a+c)&#47;(b+d)。
展开
作者回复: 从公式上是这样，但间隔时间相同的时候呢？

man手册解释await是平均等待时间，我理解意思是toal wait time &#47; total req number，跟间隔时间无关</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/00/3afbab43.jpg" width="30px"><span>88591</span> 👍（2） 💬（0）<div>老师 ，应用程序可以控制磁盘的顺序写吗？</div>2019-11-15</li><br/><li><img src="" width="30px"><span>Geek_e2b0f9</span> 👍（1） 💬（0）<div>怎么分析io类型 是连续还是随机</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e3/cc/0947ff0b.jpg" width="30px"><span>nestle</span> 👍（0） 💬（0）<div>请问aqu-sz指的是通用块层中的队列长度吗?</div>2022-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/01/5bc28ed8.jpg" width="30px"><span>black</span> 👍（0） 💬（2）<div>使用率，是指磁盘处理 I&#47;O 的时间百分比。过高的使用率（比如超过 80%），通常意味着磁盘 I&#47;O 存在性能瓶颈。
%util ，就是我们前面提到的磁盘 I&#47;O 使用率；
---------------------------------------
man手册对%util的解释：Percentage  of elapsed time during which I&#47;O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to 100%.
向设备发出I&#47;O请求所用的时间百分比（设备的带宽利用率）。当该值接近100%时，设备饱和。
换成公式的话，就是： 请求时间&#47;（请求时间+io处理时间）</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/50/01/5bc28ed8.jpg" width="30px"><span>black</span> 👍（0） 💬（0）<div>%util ，就是我们前面提到的磁盘 I&#47;O 使用率；
-----------------------------
man手册对%util的解释</div>2022-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VX0ib4CV0m7fwxB2xFcIJaYYWXXpfxxYbfBErqBej9395hgZszqS3dz9bThCxOuFfJ8Xibx9HbdNmZJwL5m33wIw/132" width="30px"><span>chaoxifuchen</span> 👍（0） 💬（0）<div>现在业务应用程序对数据的操作有数据库，缓存中间件，一般只有日志直接涉及io读写，对io性能比较敏感的主要有数据库，es,prometheus等应用</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/99/7a/558666a5.jpg" width="30px"><span>AceslupK</span> 👍（0） 💬（1）<div>IOPS vs 吞吐量 
每秒IO请求数，每秒IO请求大小，这该咋区分</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/17/796a3d20.jpg" width="30px"><span>言十年</span> 👍（0） 💬（0）<div>工作多年，没有关注过IO这个问题。
观测命令。到是让我觉得，可以看一个进程打日志的速率。评估下磁盘容量了。或者优化程序中没必要的日志打印。
还有看打日志多的进程。</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/aa/6f780187.jpg" width="30px"><span>言希</span> 👍（0） 💬（0）<div>老师您好，我请假一个磁盘性能问题
我在压测Kafka写性能的时候发现如下问题
物理机挂载多块HDD盘，应用程序采用 内存映射的方式来写文件
现象：当随机性越强，多块盘的utils使用率会下降的很明显，增加客户端去压也压不上去
个人感觉瓶颈出在OS将数据从PageCache刷到磁盘，导致应用程序写PageCache会阻塞
</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（0） 💬（1）<div>老师请问下：网络存储在创建目录和删除文件时比较慢，如何定位呀？</div>2020-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKVIjh4T1akib5iav5IIGjXB9x98p9Y80STRcwpMDqxfGLrMvHamxlxEqLMTpiayWFWSNpBcbGwkRjRw/132" width="30px"><span>马吉辉</span> 👍（0） 💬（2）<div>其中 iostat 工具中的指标
%util ，就是我们前面提到的磁盘 I&#47;O 使用率；
r&#47;s+ w&#47;s ，就是 IOPS；
rkB&#47;s+wkB&#47;s ，就是吞吐量；
r_await+w_await ，就是响应时间。

问题：老师这些指标，对于ssd 或者机械盘 的正常指标范围是什么？</div>2020-04-25</li><br/><li><img src="" width="30px"><span>刘友淙</span> 👍（0） 💬（0）<div>D11 打卡</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/3a/9001e627.jpg" width="30px"><span>流水</span> 👍（0） 💬（0）<div>磁盘饱和度是不是可以拿raid0来举例，raid0的磁盘阵列有多块磁盘，不同磁盘可以并行处理请求，所以util达到100%时可能还可以处理新的请求</div>2020-03-27</li><br/>
</ul>