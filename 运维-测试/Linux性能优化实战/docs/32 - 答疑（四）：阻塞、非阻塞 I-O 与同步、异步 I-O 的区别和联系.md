你好，我是倪朋飞。

专栏更新至今，四大基础模块的第三个模块——文件系统和磁盘 I/O 篇，我们就已经学完了。很开心你还没有掉队，仍然在积极学习思考和实践操作，并且热情地留言与讨论。

今天是性能优化的第四期。照例，我从 I/O 模块的留言中摘出了一些典型问题，作为今天的答疑内容，集中回复。同样的，为了便于你学习理解，它们并不是严格按照文章顺序排列的。

每个问题，我都附上了留言区提问的截屏。如果你需要回顾内容原文，可以扫描每个问题右下方的二维码查看。

## 问题1：阻塞、非阻塞 I/O 与同步、异步 I/O 的区别和联系

![](https://static001.geekbang.org/resource/image/1c/b0/1c3237118d1c55792ac0d9cc23f14bb0.png?wh=600%2A700)

在[文件系统的工作原理](https://time.geekbang.org/column/article/76876)篇中，我曾经介绍了阻塞、非阻塞 I/O 以及同步、异步 I/O 的含义，这里我们再简单回顾一下。

首先我们来看阻塞和非阻塞 I/O。根据应用程序是否阻塞自身运行，可以把 I/O 分为阻塞 I/O 和非阻塞 I/O。

- 所谓阻塞I/O，是指应用程序在执行I/O操作后，如果没有获得响应，就会阻塞当前线程，不能执行其他任务。
- 所谓非阻塞I/O，是指应用程序在执行I/O操作后，不会阻塞当前的线程，可以继续执行其他的任务。

再来看同步 I/O 和异步 I/O。根据 I/O 响应的通知方式的不同，可以把文件 I/O 分为同步 I/O 和异步 I/O。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/e7/2a/ccac99dd.jpg" width="30px"><span>eagle</span> 👍（21） 💬（4）<div>我根据我们自己实际应用中遇到的情况，试着回复一下两个问题：
安小依 的问题，df -h 显示占用100%，而关闭应用程序后，再次df -h是85%，这一般是因为该应用程序还有指向已删除文件的文件指针没有关闭，典型的比如日志文件，虽然在操作系统中用rm命令删除了，在相应的目录中已经没有该文件了，但如果应用中还有对应的文件指针没有关闭，则实际硬盘空间还不会释放，而应用程序被关闭时，实际空间才会释放。问题中更像是有些apk文件或处理后文件的文件指针没有释放。这种情况也可以通过 lsof | grep deleted 来找到这些文件。
lvy的out of memory的问题，可以先用free或top看一下可用内存是否确实没有了，如果确实是没有内存了，那再去研究内存的问题；还有一种常见情况，内存是充足的，文件描述符的个数或进程数达到上限了，那就得调整 ulimit，可以通过 ulimit -a (注意要用php的用户）来查看，关注open files和max user processes，这两个默认很小，1k和4k，建议调整到加两个0.</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/43/0e84492d.jpg" width="30px"><span>Maxwell</span> 👍（8） 💬（1）<div>Windows和linux有很大区别吧？如果想深入了解windows，有什么可以推荐的书吗？</div>2019-03-14</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（8） 💬（2）<div>打卡day33
感恩作者带来的分享，提前祝新年快乐！</div>2019-02-01</li><br/><li><img src="" width="30px"><span>Ivy</span> 👍（7） 💬（1）<div>老师您好，我最近在生产环境遇到一个问题，centos7频繁报错tcp out of memory ，访问页面时css文件响应头200，但是响应正文为空，我猜测就是因为tcp问题，有时候又能正常返回，每次重启php fpm就能解决问题，cat &#47;proc&#47;net&#47;sockstat 的时候tcp 行mem值在fpm重启前后差距很大，同时tw状态的连接也很多，alloc也很大，我该怎么去找原因？能看到每个tw状态的连接占用多少tcp 内存吗？或者怎么查询php fpm为何没有释放tcp内存？</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/88/c8b4ad9c.jpg" width="30px"><span>没有昵称</span> 👍（3） 💬（3）<div>我觉得同步异步io的提问者并不是想要理解字面意思，而是想要了解内部的工作模式，之前看过一篇文章讲解的比较好，把io分成了几个阶段，不同类型的io每个阶段都干了什么，回头再找下</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/72/3fe64bc5.jpg" width="30px"><span>LA</span> 👍（2） 💬（1）<div>老师，看了您的文章，有个问题一直在困扰这我。文章所说进程不可中断状态有可能是因为等待io响应，那这里的等待io响应包括等待从套接字读取数据么？如果是包括的话对于阻塞io来讲岂不是只要有阻塞进程就一直处在不可中断状态，从而无法被kill信号杀掉？</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/23/972dcd30.jpg" width="30px"><span>allan</span> 👍（2） 💬（1）<div>原文：DataService 停止后，bi iowait 都降到0，说明此时的所有数据都已经在系统的缓存中了。

这里所有数据指的是 数据库文件 中的数据 是吗？不包括索引。</div>2019-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/e0/7188aa0a.jpg" width="30px"><span>blackpiglet</span> 👍（2） 💬（1）<div>老师，在工作中遇到了 Ubuntu 16.04 系统死机的问题，和性能优化并不直接相关，不过还是想问一下遇到这种问题该如何分析。我能想到的步骤是：
1. 看 &#47;var&#47;crash 下是否有 kernel panic 的记录；
2. 看 &#47;var&#47;log&#47;syslog 下是否有应用程序异常记录；
3. 看服务器上主要的应用程序日志，是否有异常；
4. 查看是否有 coredump 文件；
5. 查看 IPMI 日志，是否有硬件异常。

有的时候这一趟下来，还是没有什么收获，请问老师有没有其他需要注意的？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（2） 💬（1）<div>老师，读文件系统的内容不会引起buffer升高吧，读块设备会引起，我做了文章的实验发现
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 1620788      0 431512    0    0   348    70  415  585  2  4 94  0  0
 0  0      0 1618488      0 431948    0    0   480     0 1605 2056  1  4 96  0  0
 0  0      0 1619524      0 431788    0    0    16     0 1157 1674  1  2 97  0  0
 2  0      0 1499696      0 548464    0    0 116905   281 5084 7062  3 14 82  1  0
 2  0      0 1495664      0 552444    0    0  4964   125 2996 4413  2  6 92  0  0
 2  0      0 1329960      0 646564    0    0 34028     0 8495 10589 21 24 53  1  0
 2  0      0 1152440      0 769524    0    0 142805   206 13584 16541 19 32 48  1  0
 3  0      0 1112028      0 783200    0    0 44753    86 14794 20490 19 23 57  0  0
 0  0      0 1050900      0 809624    0    0 36540     0 8927 13517  5 20 75  0  0
 0  0      0 1050892      0 809636    0    0     0     0 1277 1879  1  2 97  0  0
 0  0      0 1050632      0 809644    0    0     0     0 1344 1953  1  2 97  0  0
buffer并没有升高</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/5c/d4e19eb6.jpg" width="30px"><span>安小依</span> 👍（1） 💬（2）<div>老师，今天遇见了一个问题: 系统使用 df -h 显示磁盘占用100%了，而且应用程序(这是一个不停下载 apk 文件、解压缩并分析 apk文件的应用程序)在命令行也提示磁盘空间不足了。但是，关闭应用程序后，再次 df-h 统计，却发现这次磁盘占用是 85%，释放了 15%大约150G 的空间…能大概推测出来为什么关闭应用后，磁盘空间突然多了的原因吗？</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/83/9329a697.jpg" width="30px"><span>马殿军</span> 👍（1） 💬（1）<div>老师好，请教：目录项缓存在cache中，索引节点缓存在buffer中，这是对的吗？

还是二者都在buffer中？</div>2019-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（1） 💬（1）<div>老师，我们的测试环境机器我从几个指标看只有系统盘每秒写的数据量比测试环境多，为什么比测试环境卡很多，进程也只是测试环境一倍而已，使用vmstat pidstat,top,发现只有线上机器进程数多一倍，io写入量是测试机器10倍，测试配置4核16G，线上32核，256G，磁盘随机读写都是79MB&#47;s左右
测试17时50分54秒     0         1      3.85     16.61      4.86  systemd
线上05:50:51 PM     0         1    151.52   1922.47    210.85  systemd
top
top - 17:57:54 up 24 days,  6:32,  3 users,  load average: 2.06, 2.07, 2.41
Tasks: 974 total,   2 running, 970 sleeping,   0 stopped,   2 zombie
%Cpu(s):  2.2 us,  4.1 sy,  0.1 ni, 65.6 id, 27.7 wa,  0.0 hi,  0.0 si,  0.3 st
KiB Mem : 16249556 total,  2730324 free,  8055928 used,  5463304 buff&#47;cache
KiB Swap:        0 total,        0 free,        0 used.  7338032 avail Mem
线上 top - 17:58:03 up 73 days,  8:41,  2 users,  load average: 4.84, 3.40, 2.94
Tasks: 2651 total,   1 running, 2650 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.4 us,  0.5 sy,  0.0 ni, 92.9 id,  5.1 wa,  0.0 hi,  0.1 si,  0.0 st
KiB Mem : 26385616+total, 88973160 free, 23977900 used, 15090508+buff&#47;cache
KiB Swap:        0 total,        0 free,        0 used. 23713659+avail Mem
难道IO就是线上机器卡的原因
</div>2019-02-01</li><br/><li><img src="" width="30px"><span>陈帅</span> 👍（0） 💬（1）<div>关于，阻塞、非阻塞 I&#47;O 与同步、异步 I&#47;O ，这个问题回答。我确认下，是不是其实是一个东西，只不过划分的角度不同罢了。是这个意思吗？</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>[D32打卡]
时间过得真快，转眼专栏的五大模块已经学完了三个。😄</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/4d/bbfda6b7.jpg" width="30px"><span>笃定</span> 👍（1） 💬（0）<div>老师，有一个疑问，如果我的应用程序使用的是异步非阻塞IO调用方式，那么我发起IO请求获取大量的数据，因为是异步非阻塞的；可以不马上得到数据而继续执行其他任务，这样的话，是不是我这个系统上就不会出现CPUIOWAIT升高的情况呢（系统上就只跑这一个程序的情况下）</div>2021-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/41/59/78042964.jpg" width="30px"><span>Cryhard</span> 👍（1） 💬（0）<div>复习一下，仍然会有新的收获！谢谢！</div>2020-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/cb/791d0f5e.jpg" width="30px"><span>寻己</span> 👍（1） 💬（2）<div>《UNIX网络编程》提到的5种IO模型中，除了异步IO模型没有阻塞操作外，其他四种IO模型（阻塞IO、非阻塞IO、IO多路复用、信号驱动IO）都有阻塞操作。是不是可以这么理解:
同步IO一定有阻塞可能有非阻塞，
异步IO一定是非阻塞；
有阻塞一定是同步IO，
有非阻塞可能是同步IO或异步IO
求大佬解答问题</div>2019-04-03</li><br/><li><img src="" width="30px"><span>Geek_77df57</span> 👍（0） 💬（0）<div>同步异步，阻塞非阻塞是不是可以这样理解：
当调用者（即应用程序）是阻塞时，此时执行者（即系统）是同步执行。
当调用者（即应用程序）是非阻塞时，此时执行者（即系统）是异步执行。</div>2023-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/d4/1e0bb504.jpg" width="30px"><span>Peter</span> 👍（0） 💬（0）<div>阻塞、非阻塞 I&#47;O 以及同步、异步 I&#47;O的区别和 同步、异步、阻塞、非阻塞之间区别是不是同一个概念的？ 我之前看过还有同步阻塞、同步非阻塞、异步阻塞、异步非阻塞等</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/8f/51f044dc.jpg" width="30px"><span>谛听</span> 👍（0） 💬（0）<div>有个疑问，rust 或者 node.js 或者 python 中的 async&#47;await 是同步的还是异步的，是阻塞的还是非阻塞的？有 async 关键字，应该是异步的，可是会等待 await 返回结果后才会继续执行，又觉得是同步的。因为会等待 await 返回结果后才往下走，应该是阻塞的，但实际上其它的 future 也在执行，又不是阻塞的，有点混乱，希望能解答一下</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/e0/d856f5a4.jpg" width="30px"><span>余松</span> 👍（0） 💬（0）<div>- 阻塞&#47;非阻塞：针对的是数据未就绪操作是否能够立即返回的划分。非阻塞调用后立马返回，随后通过轮询或者事件得知数据是否就绪
- 同步&#47;异步：针对的数据就绪后的获取&#47;写入操作过程是否立刻返回的划分。同步操作有用户线程同步完成，异步操作（比如read）由于用户线程需要立刻返回，数据拷贝的操作由内核完成。</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ersRGspOZwfckQcnzQxOzUYdw36wufiaQIic4hfmPrN5arOTuPF7aTz0leNSibs8C3nc3aDuh8CcMtOw/132" width="30px"><span>curry30</span> 👍（0） 💬（1）<div>老师你好，文中说的“Buffer 的增长是因为，构建目录项缓存所需的元数据（比如文件名称、索引节点等），需要从文件系统中读取”，这里“文件系统中读取”描述有点疑惑，文件系统中读取的话，增长的cache，磁盘中读取的话才是增长Buffer吧，不是很能理解。</div>2021-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3d/a0/acf6b165.jpg" width="30px"><span>奋斗</span> 👍（0） 💬（0）<div>我觉得同步io和异步io最大区别是:同步io需要用户线程去内核主动读取数据，异步io是内核已经将数据返回给用户，用户直接使用即可</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/8e/eecebc1a.jpg" width="30px"><span>Geek_9a0180</span> 👍（0） 💬（0）<div>老师您好，不是很懂文中说的“Buffer 的增长是因为，构建目录项缓存所需的元数据（比如文件名称、索引节点等），需要从文件系统中读取”，是元数据都存在Buffer中吗？望解答</div>2021-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>老师你好，将数据从内核空间复制到用户空间这个过程中，如果这个过程中应用程序被阻塞就叫同步IO，否则就叫异步IO。这种说法对吗？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/96/82/8ac1e909.jpg" width="30px"><span>Jarvis</span> 👍（0） 💬（1）<div>他如果都从调用者的角度来看，阻塞和同步其实没什么区别？都是在得到响应之前没法做其他事？</div>2019-07-29</li><br/><li><img src="" width="30px"><span>如果</span> 👍（0） 💬（0）<div>DAY32，打卡</div>2019-03-20</li><br/>
</ul>