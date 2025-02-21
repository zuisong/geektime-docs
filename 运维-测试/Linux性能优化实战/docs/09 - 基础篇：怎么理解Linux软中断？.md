你好，我是倪朋飞。

上一期，我用一个不可中断进程的案例，带你学习了iowait（也就是等待I/O的CPU使用率）升高时的分析方法。这里你要记住，进程的不可中断状态是系统的一种保护机制，可以保证硬件的交互过程不被意外打断。所以，短时间的不可中断状态是很正常的。

但是，当进程长时间都处于不可中断状态时，你就得当心了。这时，你可以使用 dstat、pidstat 等工具，确认是不是磁盘 I/O 的问题，进而排查相关的进程和磁盘设备。关于磁盘 I/O 的性能问题，你暂且不用专门去背，我会在后续的 I/O 部分详细介绍，到时候理解了也就记住了。

其实除了 iowait，软中断（softirq）CPU使用率升高也是最常见的一种性能问题。接下来的两节课，我们就来学习软中断的内容，我还会以最常见的反向代理服务器 Nginx 的案例，带你分析这种情况。

## 从“取外卖”看中断

说到中断，我在前面[关于“上下文切换”的文章](https://time.geekbang.org/column/article/69859)，简单说过中断的含义，先来回顾一下。中断是系统用来响应硬件设备请求的一种机制，它会打断进程的正常调度和执行，然后调用内核中的中断处理程序来响应设备的请求。

你可能要问了，为什么要有中断呢？我可以举个生活中的例子，让你感受一下中断的魅力。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（154） 💬（9）<div>[D9打卡]
======================================
问题:怎么理解软中断?
我的理解比较简单粗暴, 硬中断是硬件产生的,比如键盘、鼠标的输入，硬盘的写入读取、网卡有数据了；软中断是软件产生的，比如程序内的定时器、[文中提到的RCU锁]。
再加上今天的上半部下半部，更好的理解了网卡的处理实际是有硬中断和软中断的。
======================================
问题:有没有碰到过因为软中断出现的性能问题?
有，且是血淋淋的教训。
之前的c程序用到了别人写的动态库[如:lib.a]，在物理机上，进程的cpu利用率在0%；而切换到了云服务器，即使空载，单进程的cpu利用率都有30%+。
以前没经验嘛,各种自查,无结果,但是自己的进程cpu利用率又那么高,总是不安心.
后来才通过vmstat 检测到系统的软中断每秒有100W+次.
最后各自百度,找人,才发现是那个动态库在处理网络收发消息时,使用了usleep(1)来休息,每次休息1纳秒,单次中断的耗时都不止1纳秒.
--------------------------------------
如果是现在,我会如下分析:
1.检测是哪个线程占用了cpu: top -H -p XX 1 &#47; pidstat -wut -p XX 1 
2.在进程中打印各线程号. 找到是哪个线程.[ 此过程也可以省略 但可以快速定位线程]
3.第一步应该可以判断出来中断数过高. 再使用 cat &#47;proc&#47;softirqs 查看是哪种类型的中断数过高.
4.不知道perf report -g -p XX 是否可以定位到具体的系统调用函数.
5.最终还是要查看源码,定位具体的位置,并加以验证.
--------------------------------------
感觉现在随便怎么分析都可以快速定位到是动态库的锅.
想当初可是好几个月都无能为力啊, 最后还是几个人各种查,搞了一周多才定位到原因.
最后再吐槽下,没有root权限的普通账户真是不方便啊,有些工具只能安装在自己的目录下, 还有些好用的工具根本无权限运行,哎...</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（130） 💬（2）<div>经常听同事说大量的网络小包会导致性能问题，一直不太理解，从今天的课程来看，是不是大量的小网络包会导致频繁的硬中断和软中断呢？希望老师给予指点，谢谢</div>2018-12-10</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（27） 💬（1）<div>打卡，day10
用外卖的例子，延伸到网卡的例子，非常形象，👍</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（19） 💬（2）<div>【D9打卡】
主题:软中断
中断:系统用来响应硬件设备请求的一种机制，会打断进程的正常调度和执行，通过调用内核中的中断处理程序来响应设备的请求。
1.中断是一种异步的事件处理机制，能提高系统的并发处理能力
2.为了减少对正常进程运行进行影响，中断处理程序需要尽快运行。
3.中断分为上下两个部分
(1)上部分用来快速处理中断，在中断禁止模式下，主要处理跟硬件紧密相关的或时间敏感的工作
(2)下部分用来延迟处理上半部分未完成的工作，通常以内核线程的方式运行。
小结:
上半部分直接处理硬件请求，即硬中断，特点是快速执行
下部分由内核触发，即软中断，特点是延迟执行
软中断除了上面的下部分，还包括一些内核自定义的事件，如:内核调度 RCU锁 网络收发 定时等
软中断内核线程的名字:ksoftirq&#47;cpu编号
4.proc文件系统是一种内核空间和用户空间进行通信的机制，可以同时用来查看内核的数据结构又能用了动态修改内核的配置，如:
&#47;proc&#47;softirqs 提供软中断的运行情况
&#47;proc&#47;interrupts 提供硬中断的运行情况
</div>2018-12-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/2o1Izf2YyJSnnI0ErZ51pYRlnrmibqUTaia3tCU1PjMxuwyXSKOLUYiac2TQ5pd5gNGvS81fVqKWGvDsZLTM8zhWg/132" width="30px"><span>划时代</span> 👍（15） 💬（1）<div>我的心得：
中断过程的工作包括，应答并重新设置硬件，从设备拷贝数据到内存以及反向操作，处理硬件请求，并发送新的硬件请求。
中断处理流程：硬件--&gt;特殊电信号（中断）--&gt;中断处理器--&gt;IRQ线（中断号）--&gt;操作系统内核（调用中断处理程序，上半部）--&gt;ksoftirqd&#47;n（内核线程处理软中断，下半部）
因为中断打断了其他代码的执行（进程，内核本身，甚至其他中断处理程序），它们必须尽快执行完，所以内核把中断处理切分为两部分：上半部，对于时间非常敏感，硬件相关，保证不被其他中断（特别是相同中断）打断的任务，由中断处理程序处理；其他所有能够被允许稍后完成的工作推迟到下半部（任务尽可能放在下半部）。

基于Linux内核2.6，稍后执行的中断下半部使用三种方式实现：
1、软中断，可在所有处理器上同时执行，同类型也可以，仅网络和SCSI直接使用；
2、tasklet，通过软中断实现，同类型不能在处理器上同时执行，大部分下半部处理又tasklet实现；
3、工作队列，在进程上下文中执行，允许重新调度甚至睡眠，如获得大量内存、信号量、执行阻塞式I&#47;O非常有用。
ksoftirqd&#47;n，每个处理器都有一组辅助处理中断的内核线程，专为出现大量软中断处理而设计，避免跟其他重要任务抢夺资源。</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/b4/e4d13c1a.jpg" width="30px"><span>沙皮狗</span> 👍（8） 💬（1）<div>老师，有一点很疑惑。在《Linux内核设计与实现》一书中提到&quot;在2.6以后的内核中提到，目前有三种方式实现中断下半部：工作队列，tasklet和软中断，软中断机制并不完全等同于中断下半部，很多人把所有下半部当成是软中断。&quot;请问这部分怎么理解？麻烦老师解答一下</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/0f/954be2db.jpg" width="30px"><span>茴香根</span> 👍（8） 💬（3）<div>老师说软中断是在内核线程ksoftirqd&#47;cpu中运行。思考和疑问，这个内核线程为什么叫线程，不是进程吗？猜测这个线程很特殊，属于内核中的某一进程，而且这个进程还能够直接与挂接的用户空间内存进行交互。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/01/c723d180.jpg" width="30px"><span>饼子</span> 👍（8） 💬（1）<div>积累了知识，但是没有遇到优化软中断的情况，不知道在哪些情况下会考虑进去？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7c/59/26b1e65a.jpg" width="30px"><span>科学Jia</span> 👍（6） 💬（1）<div>老师老师，女童鞋举手问您，软中断既然是内核方式运行，那就没有可能是应用程序引起，那如果软中断很频繁，作为应用程序该怎么考虑解决内核的问题？很忧伤啊。</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/e6/c8f20c9e.jpg" width="30px"><span>一往而深</span> 👍（6） 💬（1）<div>我也来理解一下，先来硬的：
硬件层面，来事情了cpu就必须过来处理，网卡就能存储那么多数据，如果设计成延迟的话可能有丢数据的坑，所以必须过来把数据拿出来放在容量大的地方，然后就进入下半场，软中断，应该就没那么着急了，有时间就给它处理掉，软中断处理过程中应该也是可以再处理硬中断的。意淫一下 不知道对不对啊</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/26/d4/add17f35.jpg" width="30px"><span>聰</span> 👍（5） 💬（6）<div>明明只有两个cpu ，请问老师为何会出现多个CPU呢？百度无果
[root@master ~]# grep processor &#47;proc&#47;cpuinfo |wc -l
2
[root@master ~]# head -1 &#47;proc&#47;softirqs
                    CPU0       CPU1       CPU2       CPU3       CPU4       CPU5       CPU6       CPU7       CPU8       CPU9       CPU10      CPU11      CPU12      CPU13      CPU14      CPU15      CPU16      CPU17      CPU18      CPU19      CPU20      CPU21      CPU22      CPU23      CPU24      CPU25      CPU26      CPU27      CPU28      CPU29      CPU30      CPU31      CPU32      CPU33      CPU34      CPU35      CPU36      CPU37      CPU38      CPU39      CPU40      CPU41      CPU42      CPU43      CPU44      CPU45      CPU46      CPU47      CPU48      CPU49      CPU50      CPU51      CPU52      CPU53      CPU54      CPU55      CPU56      CPU57      CPU58      CPU59      CPU60      CPU61      CPU62      CPU63      CPU64      CPU65      CPU66      CPU67      CPU68      CPU69      CPU70      CPU71      CPU72      CPU73      CPU74      CPU75      CPU76      CPU77      CPU78      CPU79      CPU80      CPU81      CPU82      CPU83      CPU84      CPU85      CPU86      CPU87      CPU88      CPU89      CPU90      CPU91      CPU92      CPU93      CPU94      CPU95      CPU96      CPU97      CPU98      CPU99      CPU100     CPU101     CPU102     CPU103     CPU104     CPU105     CPU106     CPU107     CPU108     CPU109     CPU110     CPU111     CPU112     CPU113     CPU114     CPU115     CPU116     CPU117     CPU118     CPU119     CPU120     CPU121     CPU122     CPU123     CPU124     CPU125     CPU126     CPU127
</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（5） 💬（1）<div>问一个很low的问题，我们平常有时候会使用crtl+z ，crtl+c这种挂起或中断的命令，跟文中提到的硬中断，软中断是否有什么关联。</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/43/abb7bfe3.jpg" width="30px"><span>阿巍-豆夫</span> 👍（5） 💬（2）<div>老师，请教下，一般进程都是多线程运行的。你所说的中断是线程的级别，还是进程的级别？ 送外卖的场景没有解释到多线程的场景。 如果是多线程是不是根本不存在中断的情况？</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（1）<div>老师，我开发了一个日志搜集系统，上面需要压测，但是我不知道要测试哪些性能指标，这个应用的性能指标和优化和压测后面的课程会讲吗</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/16/38/88eb9377.jpg" width="30px"><span>周谦</span> 👍（2） 💬（2）<div>问下 D状态的进程cpu会空等这个进程吗</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/0f/c43745e7.jpg" width="30px"><span>hola</span> 👍（2） 💬（1）<div>我想问个问题，缺页中断有统计信息吗</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/93/cfed7c6c.jpg" width="30px"><span>Vincent</span> 👍（2） 💬（1）<div>最开始的中段缺点是处理中断信号时不能响应别的中断信号。所以Linux处理中断 是分了两部分去响应中断 上半部分是硬中断 响应快 下半部分是软中断内核处理响应慢 采用了异步的方式 所以 上部分将中断信号发送给内核的时候（即软中断） 必然会先存到一个数据队列中。下半部分是从队列中去取的数据。所以 在Linux发生了中断 必然是硬中断和软中断同时出现的。 不知道理解的对不对。</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/8a/ff94bd60.jpg" width="30px"><span>涛涛</span> 👍（2） 💬（1）<div>倪老师是不是总吃外卖。</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/15/5dabb390.jpg" width="30px"><span>Geek_fbe6fe</span> 👍（2） 💬（1）<div>想问下老师，现在一些的语言中实现协程是不是就是利用中断的系统命令实现的协程操作呢？</div>2018-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1e/0d/f8ad03fb.jpg" width="30px"><span>Glen</span> 👍（2） 💬（1）<div>留言里也有很多资深的同学啊</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/23/972dcd30.jpg" width="30px"><span>allan</span> 👍（2） 💬（1）<div>老师，您好，问一下 是不是上半部的硬中断和下半部的软中断 是发生在同一个 CPU 上吗？还是说 上半部 执行完，下半部可以调度到 其他 CPU 上执行接下来的？</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8b/15/5278f52a.jpg" width="30px"><span>春暖花开</span> 👍（2） 💬（2）<div>是否可以将中断处理专门属于一个核心cpu处理，通过亲和性</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（2） 💬（1）<div>软中断时间太长会不会影响性能</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/8b/2c81a375.jpg" width="30px"><span>好说</span> 👍（2） 💬（1）<div>老师，生产环境的服务器的磁盘数量一般有很多，每块盘读写都比较高，有某块盘特别高，这个时候想要获取哪个进程使得这块盘IO特别高要怎么分析呢</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/27/76489618.jpg" width="30px"><span>sunsweet</span> 👍（1） 💬（2）<div>系统调用的实现也是通过软中断，int 80指令触发，跟这里的软中断概念一样吗？</div>2019-04-07</li><br/><li><img src="" width="30px"><span>Geek_94e115</span> 👍（1） 💬（1）<div>3. 软中断分析  #https:&#47;&#47;www.cnblogs.com&#47;cherishui&#47;p&#47;4318660.html
	- softirq_vec[32]
	- open_softirq #软终端注册
	- __softirq_pending  #软终端执行位图 对应bit被设置  #通过 raise_softirq_irqoff 开启某个软终端
	- _do_softirq #遍历 sirq vec #执行对应类型的 sirq  的action 
	- 前者被调用的时机 #硬件中断处理完，返回时调用(irq_exit()) # ksoftirqd - wakeup_softirqd  #local_bh_enable bh执行前，如果不在硬中断中，就执行软中断 ，这样可以保证 hirq 和 sirq 的有序 
	</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（1） 💬（1）<div>我的环境也是ubantu,使用 cat &#47;proc&#47;softirqs查看，为什么显示了很多CPU，有128个？
root@kaipule-virtual-machine:~# cat &#47;proc&#47;softirqs 
                    CPU0       CPU1       CPU2       CPU3       CPU4       CPU5       CPU6       CPU7       CPU8       CPU9       CPU10      CPU11      CPU12      CPU13      CPU14      CPU15      CPU16      CPU17      CPU18      CPU19      CPU20      CPU21      CPU22      CPU23      CPU24      CPU25      CPU26      CPU27      CPU28      CPU29      CPU30      CPU31      CPU32      CPU33      CPU34      CPU35      CPU36      CPU37      CPU38      CPU39      CPU40      CPU41      CPU42      CPU43      CPU44      CPU45      CPU46      CPU47      CPU48      CPU49      CPU50      CPU51      CPU52      CPU53      CPU54      CPU55      CPU56      CPU57      CPU58      CPU59      CPU60      CPU61      CPU62      CPU63      CPU64      CPU65      CPU66      CPU67      CPU68      CPU69      CPU70      CPU71      CPU72      CPU73      CPU74      CPU75      CPU76      CPU77      CPU78      CPU79      CPU80      CPU81      CPU82      CPU83      CPU84      CPU85      CPU86      CPU87      CPU88      CPU89      CPU90      CPU91      CPU92      CPU93      CPU94      CPU95      CPU96      CPU97      CPU98      CPU99      CPU100     CPU101     CPU102     CPU103     CPU104     CPU105     CPU106     CPU107     CPU108     CPU109     CPU110     CPU111     CPU112     CPU113     CPU114     CPU115     CPU116     CPU117     CPU118     CPU119     CPU120     CPU121     CPU122     CPU123     CPU124     CPU125     CPU126     CPU127     </div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5e/62/a6631e94.jpg" width="30px"><span>张强</span> 👍（1） 💬（1）<div>倪老师，您好。我今天遇到个问题，服务端监听程序收到的客户端的连接状态使用netstat命令看到有几个syn_recv状态（少量），我使用telnet新的连接来测试也是这个状态。客户端的请求数量规模很小，在个位数。这种问题的解决思路是什么？很难出现，重启后好了，其他监听端口也没问题。</div>2018-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7e/2c/54d68da4.jpg" width="30px"><span>魏峰</span> 👍（1） 💬（1）<div>scp小文件很慢的的原因是网络小包的软中断？</div>2018-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/20/36/b3e2f1d5.jpg" width="30px"><span>wykkx</span> 👍（1） 💬（1）<div>老师我们线上系统最近有个问题，4核的cpu，load5和load15总是过一段时间就超过4*0.8的值,这个时候我用top看系统的情况，没有D进程，也没有一直R的进程，cpu利用率很低不到5%，cs的值也就几千，iostat查看util和iowait的值都不高，vmstat中r和b这两列基本都是0，偶尔r会有1.这台机器上就一个java进程，请教下下次复现该问题时，我该如何排查？谢谢</div>2018-12-11</li><br/>
</ul>