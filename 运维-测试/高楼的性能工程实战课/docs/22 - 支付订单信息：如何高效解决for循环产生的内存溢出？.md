你好，我是高楼。

今天，我们来优化支付订单接口。通过这个接口，我们来看看怎么高效解决for循环产生的内存溢出问题。

对于JVM内存溢出或泄露来说，通常性能人员都能定位到一个应用hang住了。但是，要想进一步判断出应用hang住的原因，并没有那么容易做到。因为内存大时做堆Dump比较费时，更重要的一点是，要想把堆里面的对象和栈关联起来是需要足够的经验和时间的。这也是其中的难点之一。

这节课我就带你来看看怎么解决这个难点。

不过，在此之前，我们会先处理一个熟悉的问题，就是数据库表加索引。很显然，我们在测试这个接口时又遇到它了。虽然我在[第16讲](https://time.geekbang.org/column/article/367285)中给你重点讲过这个问题，但是这一次的每秒全表扫描比之前要高得多。通过这次的讲解，我希望你能明白只要存在全表扫描，CPU消耗很快就会达到100%。同时，也希望你能借此看清楚全表扫描对CPU消耗的影响。

## 场景运行数据

首先，我们来运行一下场景：

![](https://static001.geekbang.org/resource/image/02/e1/02f5facd8d0196ae07c223b8dc1e4ae1.png?wh=1832%2A636)

这是一个典型的TPS太低、响应时间不断上升的性能瓶颈，对于这种瓶颈的分析逻辑，我在前面的课程里已经写过很多次了，相信你已经掌握。下面我们来看一下具体的问题是什么。

## 架构图

![](https://static001.geekbang.org/resource/image/72/8f/72b7b04b1e2323d4fae9fcc30cb3be8f.png?wh=979%2A286)

这个接口的链路比较简单：User - Gateway - Order - MySQL，我们大概记在脑子里就好。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/d4/de/f129dfee.jpg" width="30px"><span>WBF</span> 👍（9） 💬（1）<div>1、mysql：
    ①查看慢日志
    ②top -Hp pid 定位线程号，通过线程号定位sql
    然后查看执行计划分析是否存在全表扫描，表大小，制定优化方案
oracel：
    ②分析awr报告


2、
《1》定位堆栈
1、命令
    （1）保存堆dump文件，打开dump文件，根据16进制线程号，查找代码的行号定位堆栈：
a. jmap -histo:live 进程pid | more      &#47;  jmap -histo pid|more） 通过进程号(jps -l)看线程调用堆栈
    jmap -dump:format=b,file=文件名 进程pid；     （b二进制格式）
b. jstack   进程pid &gt;&gt;thread.dump ;          
c. jcmd 进程pid GC.heap_dump &#47;filepath.hprof（二进制格式dump）
d. ①配置java参数：（java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=&lt;file-or-dir-path&gt;）自动抓取堆dump文件：java_pid.hprof
   ②使用Jconsole工具将操作调用的serVMOption参数：HeapDumpOnOutOfMemoryError 值设置为true
    （2）不保存dump文件，定位堆栈:
a. 通过 perf record 命令录制进程一段时间，通过 perf report 分析堆栈
b. jstack 进程pid | grep 线程pid   ：top，top -Hp 进程pid，printf &quot;%x\n&quot; 线程pid，jstack 进程pid | grep 16进制线程pid

2、图形化工具：
        ①jvm右键java进程选择线程dump生成快照或打开dump文件
        ②使用IBM Thread and Monitor Dump Analyzer for Java分析dump文件
        ③jconsole
        ④使用MAT打开dump.hprof文件，查看可疑的内存消耗点的详情，查看对象以及它的依赖  dominator_tree

《2》分析源码：
        查看代码行，分析所有调用该方法的代码逻辑，分析代码对应的SQL

《3》沟通：与开发沟通，是否存在定时任务，执行定时任务的数据量大小，有无加limit，线程数</div>2021-05-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（0） 💬（1）<div>请问，容器里面如何执行mysqlreport 呢？ 生成的数据如何拿出来？谢谢老师</div>2021-10-14</li><br/>
</ul>