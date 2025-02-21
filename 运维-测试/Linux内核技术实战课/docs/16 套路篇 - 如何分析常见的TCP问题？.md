你好，我是邵亚方。

对互联网服务而言， 网络问题是非常多的，而且很多问题的外在表现都是网络问题，这就需要我们从网络入手，分析清楚根本原因是什么。而要分析各种各样的网络问题，你必须掌握一些分析手段，这样在出现问题的时候，你就可以高效地找到原因。这节课我就带你来了解下TCP的常见问题，以及对应的分析套路。

## 在Linux上检查网络的常用工具

当服务器产生问题，而我们又不清楚问题和什么有关时，就需要运行一些工具来检查系统的整体状况。其中，dstat是我们常用的一种检查工具：

```
$ dstat
--total-cpu-usage-- -dsk/total- -net/total- ---paging-- ---system--
usr sys idl wai stl| read  writ| recv  send|  in   out | int   csw 
  8   1  91   0   0|   0  4096B|7492B 7757B|   0     0 |4029  7399 
  8   1  91   0   0|   0     0 |7245B 7276B|   0     0 |4049  6967 
  8   1  91   0   0|   0   144k|7148B 7386B|   0     0 |3896  6971 
  9   2  89   0   0|   0     0 |7397B 7285B|   0     0 |4611  7426 
  8   1  91   0   0|   0     0 |7294B 7258B|   0     0 |3976  7062
```

如上所示，dstat会显示四类系统资源的整体使用情况和两个关键的系统指标。这四类系统资源分别是：CPU、磁盘I/O、 网络和内存。两个关键的系统指标是中断次数（int）和上下文切换次数（csw）。而每个系统资源又会输出它的一些关键指标，这里你需要注意以下几点：

![](https://static001.geekbang.org/resource/image/14/68/145508f238e794df5fbf84f200c7ce68.jpg?wh=3732%2A1895)

如果你发现某一类系统资源对应的指标比较高，你就需要进一步针对该系统资源做更深入的分析。假设你发现网络吞吐比较高，那就继续观察网络的相关指标，你可以用dstat -h来查看，比如针对TCP，就可以使用dstat -tcp：

```
$ dstat --tcp
------tcp-sockets-------
lis  act  syn  tim  clo 
  27   38    0    0    0
  27   38    0    0    0
```

它会统计并显示系统中所有的TCP连接状态，这些指标的含义如下：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/3b/d7/9d942870.jpg" width="30px"><span>邵亚方</span> 👍（11） 💬（0）<div>课后作业答案：
- 请问 tcpdump 在解析内核缓冲区里的数据时，为什么使用 PACKET_MMAP 这种方式？你了解这种方式吗？这样做的好处是什么？
评论区有同学已经回答的很好了，
“PACKET_MMAP减少了系统调用，不用recvmsg就可以读取到捕获的报文，相比原始套接字+recvfrom的方式，减少了一次拷贝和一次系统调用。”</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（5） 💬（1）<div>请问老师Wireshark和tcpdump在实现原理上，是否也是监控网卡以内的行为？</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（3） 💬（2）<div>1.感谢作者的总结，请教下ss命令或者读proc文件会进行加锁吗？如果会是否影响性能。proc下的meminfo会
2.bpf的性能好和tcpdump的性能差，如何理解。是否
3.后续会出实际的tracepoint或者stap之类的实际案件排查吗？</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/15/106eaaa8.jpg" width="30px"><span>stackWarn</span> 👍（9） 💬（1）<div>PACKET_MMAP减少了系统调用，不用recvmsg就可以读取到捕获的报文，相比原始套接字+recvfrom的方式，减少了一次拷贝和一次系统调用。</div>2020-09-24</li><br/>
</ul>