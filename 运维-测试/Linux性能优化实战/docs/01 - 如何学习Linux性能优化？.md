你好，我是倪朋飞。

你是否也曾跟我一样，看了很多书、学了很多Linux性能工具，但在面对Linux性能问题时，还是束手无策？实际上，性能分析和优化始终是大多数软件工程师的一个痛点。但是，面对难题，我们真的就无解了吗？

固然，性能问题的复杂性增加了学习难度，但这并不能成为我们进阶路上的“拦路虎”。在我看来，大多数人对性能问题“投降”，原因可能只有两个。

一个是你没找到有效的方法学原理，一听到“系统”、“底层”这些词就发怵，觉得东西太难，自己一定学不会，自然也就无法深入学下去，从而不能建立起性能的全局观。

再一个就是，你看到性能问题的根源太复杂，既不懂怎么去分析，也不能抽丝剥茧找到瓶颈。

你可能会想，反正程序出了问题，上网查就是了，用别人的方法，囫囵吞枣地多试几次，有可能就解决了。于是，你懒得深究这些方法为啥有效，更不知道为什么，很多方法在别人的环境有效，到你这儿就不行了。

所以，相同的错误重复在犯，相同的状况也是重复出现。

其实，性能问题并没有你想像得那么难，**只要你理解了应用程序和系统的少数几个基本原理，再进行大量的实战练习，建立起整体性能的全局观**，大多数性能问题的优化就会水到渠成。

我见过很多工程师，在分析应用程序所使用的第三方组件的性能时，并不熟悉这些组件所用的编程语言，却依然可以分析出线上问题的根源，并能通过一些方法进行优化，比如修改应用程序对它们的调用逻辑，或者调整组件的配置选项等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/60/05/3797d774.jpg" width="30px"><span>forever</span> 👍（365） 💬（12）<div>我遇到性能瓶颈的排查思路

有监控的情况下，首先去看看监控大盘，看看有没有异常报警，如果初期还没有监控的情况我会按照下面步骤去看看系统层面有没有异常
1、我首先会去看看系统的平均负载，使用top或者htop命令查看,平均负载体现的是系统的一个整体情况，他应该是cpu、内存、磁盘性能的一个综合，一般是平均负载的值大于机器cpu的核数，这时候说明机器资源已经紧张了
2、平均负载高了以后，接下来就要看看具体是什么资源导致，我首先会在top中看cpu每个核的使用情况，如果占比很高，那瓶颈应该是cpu,接下来就要看看是什么进程导致的
3、如果cpu没有问题，那接下来我会去看内存，首先是用free去查看内存的是用情况，但不直接看他剩余了多少，还要结合看看cache和buffer，然后再看看具体是什么进程占用了过高的内存，我也是是用top去排序
4、内存没有问题的话就要去看磁盘了，磁盘我用iostat去查看，我遇到的磁盘问题比较少
5、还有就是带宽问题，一般会用iftop去查看流量情况，看看流量是否超过的机器给定的带宽
6、涉及到具体应用的话，就要根据具体应用的设定参数来查看，比如连接数是否查过设定值等
7、如果系统层各个指标查下来都没有发现异常，那么就要考虑外部系统了，比如数据库、缓存、存储等

基本上就上面这些步骤，有些不完整，希望跟着老师学习一些更系统的排查思路！</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/42/f7/06cd1560.jpg" width="30px"><span>X</span> 👍（63） 💬（2）<div>D2打卡

1. 笔记
技巧一：虽然系统的原理很重要，但在刚开始一定不要试图抓住所有的实现细节。”

深陷到系统实现的内部，可能会让你丢掉学习的重点，而且繁杂的实现逻辑，很可能会打退你学习的积极性。所以，我个人观点是一定要适度。

2. 心得
作为一个完美主义者，一学起原理类的东西，真的不要太容易跑偏😂经常是看着某个重要原理，就想着找找看相关内容，然后就各种跳转搜索，以前最开始学数据结构的定义，都能跑到编译原理上，最后开始计算二进制了。

有时候大半天了，一个原理都没看完，就各种死抠和联想。这么做确实印象深刻，但是真的很低效，心累。

老师这里说的适度，真的很重要，而且这个度，确实应该是过来人才知道啊。

我一向喜欢系统化的学习，能有个“升级简化版”的系统知识图谱，不要太开心。可惜不能上传图片，不然可以把每次标记和补充也都打个卡了。

开始学了，加油！冲着我的四个月后涨工资的目标去了！</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/d2/c7357723.jpg" width="30px"><span>发条橙子 。</span> 👍（26） 💬（1）<div>以前看服务器的资源使用只会简单的使用 top命令 看cpu使用的百分比。，但是却不清楚到底多高才算高危 ，面对持续增长我该怎么预防或处理 ， load指标具体的含义 和 cpu有什么关联 ..这些都没有一个整体的概念 </div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/1f/6bc10297.jpg" width="30px"><span>Allen</span> 👍（21） 💬（1）<div>『day1』
这周工作中遇到了一个紧急的问题（用的是arm系列的单板），单板的空间几乎快满了。 使用了top和free命令查看，单板内存的使用情况，仅仅凭借这两个命令，是不可能分析出来原因的。

查看&#47;proc&#47;&lt;pid&gt;&#47;下的的meminfo、status等文件可以具体才看到虚拟内存和实际物理内存的使用情况。  之前根本不了解&#47;proc&#47;&lt;pid&gt;里面的文件都是干嘛的。

希望跟着老师的专栏，可以了解下linux系统的基本知识，以后遇到相关问题时，可以有一些思路。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/0c/32ec9763.jpg" width="30px"><span>Luna</span> 👍（14） 💬（1）<div>性能指标概念：高并发 =&gt; 吞吐   响应快 =&gt; 延时
该概念是从应用负载的角度出发：Application ▹Libraries▹System Call▹Linux Kernel ▹Drive

 与之对应的是系统资源视角出发 ：Drive▹Linux Kernel ▹System Call ▹Libraries ▹Application 

性能指标的评判有以上二种常用的角度

接着六步

1.选择性能指标评估应用和系统的性能

2.为应用和系统设定性能目标

3.进行性能基准测试

4.性能分析定位瓶颈

5.优化系统和应用程序

6.性能监控和告警

六步总结，从正确的角度出发，设定目标（性能优化不是漫无目的的），基准测试（了解现有系统应用的运行时情况），根据情况分析瓶颈，优化它，设置监控和告警（其实可以再扩展比如达到一定的负载，采取降级等操作）</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（13） 💬（1）<div>“你可以先学会我给你讲的这些系统工作原理，但不要去深究 Linux 内核是如何做到的，而是要把你的重点放到如何观察和运用这些原理上”
--------------------------
感觉说的很对，前几天订阅了刘超老师的《趣谈LinuxOS》，这个专栏罗列了不少Linux内核的代码片段，可以说是基本都看不懂，作为一名7年java尴尬的一批，主要就是总是陷入到Linux内核的代码中，导致一篇专栏反复看了两遍也没懂得更多，所以果断阶段性放弃了，所以聚焦比较重要，我也是拿这个作为自己的座右铭了，希望可以把这个专栏坚持下去！加油！💪！☆！</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/ed/d50de13c.jpg" width="30px"><span>mj4ever</span> 👍（8） 💬（2）<div>之所以选择学习这个专栏，就是希望能解决实际工作中的一些技术问题，当公司研发的产品在现场运行，出现性能问题的时，不会束手无策，毫无思路，误打误撞的去解决问题。
因此，希望通过3个月的学习，自己可以掌握以下几个方面：
1、建立整体性能的全局观
2、理解最基本的几个系统知识原理
3、掌握Linux 性能工具图谱的熟练应用
感谢大家，也感谢能不断坚持的自己。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/f4/773e7e4b.jpg" width="30px"><span>java小白</span> 👍（4） 💬（1）<div>D2打卡，做了一段时间的性能优化工作，发现自己工作中只是重复的进行压测，压接口压场景，遇到的最大问题是CPU高，基本就是通过线程栈去分析那些线程有问题然后抛给开发去看代码是不是有问题，一个个的去解决，最后成功降低CPU的也不多，堆栈、磁盘I&#47;O、网络这些基本都没怎么重点用到。现在总结下自己面对的问题：①性能分析没有一个整体的分析思路，在遇到各种各样的问题的时候应该用什么样的方法去分析；②自己没有编程开发的经验，代码方面一直是自己的薄弱环节，也在逐渐学习加强。想问下作者，代码开发基础在性能优化工作中到底能占多少比重有多重要？</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c5/1231d633.jpg" width="30px"><span>梁中华</span> 👍（4） 💬（1）<div>打卡，希望作者必要的时候能结合虚拟机和docker来讲下，在这两种环境下的性能问题分析有什么要注意的，毕竟现在的应用不是运行在虚拟机就是运行在容器中</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/e5/791d0f5e.jpg" width="30px"><span>白下</span> 👍（3） 💬（1）<div>Linux的性能调优问题往往是涉及很多其他服务性能调优问题。
运维经常接触的：
nginx&#47;haproxy性能调优
数据库oracle mysql的性能调优
kafka队列的性能调优
redis&#47;memcache缓存的性能调优

然后就是具体应用层面的
java JVM服务性能调优
python 服务性能调优

希望讲师可以围绕实际的这些案例去展开。
在我工作中所遇到的 其实就是服务在linux上面跑出现了“性能瓶颈”？
涉及性能的无外乎在linux的表象就是 CPU高了 内存占用高了 磁盘IO高了 网卡流量高了。

以Nginx为例每一个高并发 高吞吐量 低延迟要求的服务都需要linux配合个性化配置柏阔内核参数 基于操作系统配置调整相关服务参数 根据使用场景配置相关参数以达到——以较低的物理机资源实现较高的业务吞吐量并维持低延迟的目标

工作中一般涉及到性能优化的两个触发点：
1 性能突然恶化（CPU 内存 磁盘 网卡）排查解决问题
2 压测想提高单节点吞吐量 应对大促、成本优化、业务增长带来的对资源的需求。

</div>2018-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/54/73cc7f73.jpg" width="30px"><span>王旧业</span> 👍（2） 💬（1）<div>案例在工具的选用上，能否尽量使用操作系统自带的工具。例如，top命令等。因为在实际定位客户环境问题时，安装一些新的工具往往流程上很麻烦，并且还有一些工具是开源的，客户有时候会认为这些工具有风险</div>2019-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/e0/c85bb948.jpg" width="30px"><span>朱雯</span> 👍（2） 💬（1）<div>1:不需要了解所有组件的实现细节，只要能理解他们的基本工作方式和写作原理
2:性能指标有1:高并发和响应快，从性能优化核心指标来看对应吞吐和延时着两项，从系统资源的视角看，对应的是资源利用率和饱和度
3:性能问题的本质是：系统资源已经到达瓶颈，但是请求的处理还不够快，无法支撑起更多的请求
4:处理步骤：
            1:选择指标评估应用程序和系统的性能
            2:为应用程序和系统设置性能目标
            3:进行性能基准测试    
            4:性能分析定位瓶颈
            5:优化系统和程序
            6 :性能监控和告警
学习技巧:1:系统原理很重要，但是不要死抠细节
                2:边学边实践，不断掌握linux性能分析和优化
                3:勤于思考，多问为什么多总结</div>2018-12-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIR1mtu6aanP8OhibVFsruxI7oBtO6KTvLXDLGKELzRGHHlvBhzedfF7tiaMWSAlG4ia3OXChWLynjYQ/132" width="30px"><span>李孝东</span> 👍（2） 💬（1）<div>最近遇到一个问题，之前一直没有问题，我们公司最近gitlab服务器在push和pull的时候存在20%左右的可能连接不上，内网使用应该不存在网络问题，项目也不多一共就130多个，频度高的应该在30个以内，内部员工60人左右，最近一直出现这个状况，一开始以为压力大，仔细排查后压力也不大，8核16GB内存完全足够，内接数也就几十个，也会出现连接不上重试一下又正常了，web端都正常，开始怀疑是sshd配置，仔细排查了也没不当的地方，网上也有说是gitlab的问题，修改了参数重启似乎也没有效果，不知道原因在哪，希望老师可以指点一下方向。</div>2018-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/9b/0bc44a78.jpg" width="30px"><span>yyl</span> 👍（1） 💬（1）<div>我的困惑之一就是对性能指标认识不足，比如网络延时，我可能会觉得100ms算正常的，但是有的却觉得这不可忍受</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e5/33/ff5c52ad.jpg" width="30px"><span>不负</span> 👍（1） 💬（1）<div>linux性能优化方面比较小白，但是性能优化是个大头：像（client端）项目的性能优化等，老师你所说的基本原理应该也适应于这些？</div>2019-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epibiah7ib9ELda3J60xQ4Lw08DkoicEne8YJj0EgeT55OkKpXKdoXpduccv0Qiahu2YgvCvjKpTn9hm9A/132" width="30px"><span>jiabin</span> 👍（1） 💬（1）<div>能不能讲讲sbrk和mmap？最近有个守护进程遇到问题，就是即使周末木有作业跑，内存使用也维持在20G左右不降。后来调查发现跟malloc有关，设置了mmap的阀值和最大值之后，问题就解决了。但是我还是不很理解为何。</div>2019-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/c5/a2946220.jpg" width="30px"><span>陈启永</span> 👍（1） 💬（1）<div>我是做开发的，最近碰到了服务器 CPU 使用率和系统负载过高的问题。
问题是这样子的，我们的服务由阿里云的两台 4 核 8 G 的云服务器提供，服务器就部署了 Nginx + PHP-fpm ，MySQL 和 Redis 都是使用阿里云的服务。每当有其它渠道给导流时，服务器的 CPU 使用率基本都是满负荷运行的，系统负载更是高的可怕，最高时都超过了 250 ！！可想而知，当时的服务响应有多慢。
我观察到，当时的 TCP 连接数的三个指标分别为：ESTABLISHED 4236;NON_ESTABLISHED 7140;TCP_TOTAL 11376，这是不是说明并发已经很高了呢？
在这种情况下，应用程序（PHP）还有没有优化空间，还是只能增加服务器来分流了呢？</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1c/14/2388d9e4.jpg" width="30px"><span>Blue_Eye</span> 👍（1） 💬（1）<div>可能碰到的最大问题现在就是db load 很高，但是不知道怎么排查到底是因为什么导致他很高，用ps aux看都是db的进程，不知道有没有系统log可以把这些正在跑的进程sql 语句指令找出来，也不知道怎么修复，一头雾水</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/c8/8627f5c1.jpg" width="30px"><span>右耳朵猫咪</span> 👍（1） 💬（1）<div>用centos实操可以吗</div>2018-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/11/a6/49b74f15.jpg" width="30px"><span>大臭</span> 👍（1） 💬（1）<div>之前一直不理解，把cpu跑满了好还是不好，感觉cpu空闲很多很浪费资源，但是平时优化的时候，都是要降低cpu使用率。
而且之前遇到性能问题，总是会把cpu，内存，磁盘io，网络，gc日志全看一遍，有的时候也找不到问题所在，很浪费时间精力。
期待这次学习后可以对性能的各种指标有个系统的认知，排查问题有个明确的思路。
谢谢老师。</div>2018-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（1） 💬（1）<div>学linux性能优化，linux内核要学习的吗，如果要学习那不是也要学C语言？一般电商应用级的优化涉及linux内核优化的多吗？</div>2018-11-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIfQHOCVibxib3GfYKUZonqCibM8Weic5BIOJDGz4QjcBDUYkQPK9tThzibF0Rdd704z85zZl3fQy7H8xw/132" width="30px"><span>Karis0901</span> 👍（1） 💬（1）<div>遇到的困难和疑惑：
开发的深度学习应用程序在Linux环境下吞吐和延时表现都比较差，机器资源尤其是CPU的消耗很大，然而并不知道如何分析其中的性能问题，到底是应用程序算法、编程语言、深度学习底层库还是机器的原因？希望通过本课程能过学习在观察到表现的时候，能够应用性能工具抽丝剥茧地分析具体的性能瓶颈，好做对应的优化。
同时，同样的模型利用深度学习工具包对应的JavaAPI，在相同的机器上，性能却有所提高，但内存反而占用比较大。所以疑惑的是，python和java开发的应用程序为什么对资源的消耗是截然不同的。</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/b0/fb5bad5c.jpg" width="30px"><span>敬艺</span> 👍（1） 💬（1）<div>请讲讲如何综合CPU,内存，IO等指标的数据来判断问题所在？大概的套路是什么？现象是：机器响应慢。</div>2018-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLd4KC3FsQ8ag2P5xsyM8xeZB0GQoTsKjxogibicVcqRt25tVHLMjyDlYcz0wjIrtF4TF9JHQ41d0yA/132" width="30px"><span>Jerry</span> 👍（1） 💬（1）<div>最近遇到的问题，一台宿主机上内存吃紧，已经确认到是宿主机上的qemu-kvm进程占用了大量的内存，需要进一步细化的确认是虚机内哪些东西导致宿主机内存吃紧，或者说qemukvm这个进程的哪些东西导致内存吃紧</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d9/9c/a59f6e8b.jpg" width="30px"><span>西门吹牛不吹牛</span> 👍（1） 💬（1）<div>昨天刚好遇到一个性能问题，百思不得其解，rhel7上跑Oracle 数据库，cpu分配了8核，load avg不超过3，就看到一个Oracle进程cpu 98%，然后开发编译存储过程卡，但是其他cpu内核都是1%以下，通过进程查找Oracle id杀掉之后开发编译就好了。但是为毛其他cpu内核不用？？偏偏挤到这一个cpu核心上？？</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/ce/d53edf66.jpg" width="30px"><span>王阳</span> 👍（1） 💬（1）<div>之前做一个存储的项目，性能一度陷入瓶颈，最后分析是系统的调度太慢，然后就进入各种调参重试，虽然最终项目达标了，但是总有点感觉瞎猫碰上死耗子，希望通过这次课程，能系统的了解下性能优化的方法，努力提升自己</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/6b/0b6cd39a.jpg" width="30px"><span>朱月俊</span> 👍（1） 💬（1）<div>之前遇到过一些性能问题，比如重启数据库后，发现iowait很快飙升，然后机器关机，然后重启机器重试以上操作，iowait稳定。具体原因不能准确定位出来，只能靠猜，使用iowait还是别人提醒，不然都不知道用哪些性能指标来找问题。
通过一步一步跟着专栏老师学习远离，实战，学习老师的思路来提高性能分析和优化能力，同时在工作中不断去验证和锻炼自己这方面。</div>2018-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/aa/fa/3ad0a689.jpg" width="30px"><span>廖师虎</span> 👍（0） 💬（3）<div>文中的Linux性能优化思维导图是图片格式的，能提供思维导图原始文件吗</div>2020-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ad/ff/3ff03b0e.jpg" width="30px"><span>Paky_Dpc</span> 👍（0） 💬（1）<div>我已经购买订阅了这个课程，要怎么样才能这个课程的文稿和性能优化工具包？</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/33/8680446c.jpg" width="30px"><span>拭心</span> 👍（0） 💬（1）<div>打卡2，0720</div>2020-07-20</li><br/>
</ul>