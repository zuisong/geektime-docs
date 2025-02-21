你好，我是程远。今天我要和你聊一聊容器中如何使用perf。

[上一讲](https://time.geekbang.org/column/article/338413)中，我们分析了一个生产环境里的一个真实例子，由于节点中的大量的IPVS规则导致了容器在往外发送网络包的时候，时不时会有很高的延时。在调试分析这个网络延时问题的过程中，我们会使用多种Linux内核的调试工具，利用这些工具，我们就能很清晰地找到这个问题的根本原因。

在后面的课程里，我们会挨个来讲解这些工具，其中perf工具的使用相对来说要简单些，所以这一讲我们先来看perf这个工具。

## 问题回顾

在具体介绍perf之前，我们先来回顾一下，上一讲中，我们是在什么情况下开始使用perf工具的，使用了perf工具之后给我们带来了哪些信息。

在调试网路延时的时候，我们使用了ebpf的工具之后，发现了节点上一个CPU，也就是CPU32的Softirq CPU Usage（在运行top时，%Cpu那行中的si数值就是Softirq CPU Usage）时不时地会增高一下。

在发现CPU Usage异常增高的时候，我们肯定想知道是什么程序引起了CPU Usage的异常增高，这时候我们就可以用到perf了。

具体怎么操作呢？我们可以通过**抓取数据、数据读取和异常聚焦**三个步骤来实现。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/c8/cae61286.jpg" width="30px"><span>chong chong</span> 👍（6） 💬（1）<div>老师好，如果容器使用cpu share，在容器内perf看到的是宿主机信息，异常有可能是业务之间干扰导致。所以，最好是在宿主机上使用perf，我的理解对不？</div>2021-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7c/bb/635a2710.jpg" width="30px"><span>徐少文</span> 👍（5） 💬（1）<div>老师好，如果想在主机上做容器内进程的监控，直接在host上利用perf工具去获取容器的系统调用序列，这样的方法是可行的吗？</div>2021-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/70/4e7751f3.jpg" width="30px"><span>超级芒果冰</span> 👍（1） 💬（1）<div>perf 的常规步骤中，out.sv 是什么文件，需要用什么软件打开</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/30/d4737cd5.jpg" width="30px"><span>lyonger</span> 👍（1） 💬（1）<div>在容器中使用的话，限制有点多。线上业务直接perf，对线上可能会有影响？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/0a/6c74e932.jpg" width="30px"><span>光</span> 👍（1） 💬（1）<div>请教下k8s里面上下文切换和中断比较严重导致负载高。这如何处理啊</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/55/ac/53bbeeee.jpg" width="30px"><span>李雪</span> 👍（0） 💬（1）<div>Dear teacher, can I use the following command to monitor each container&#39;s events&quot;perf stat -a -e cpu-clock,context-switches,cpu-migrations,page-faults,cycles,instructions,branches,branch-misses -G kubepods.slice&#47;kubepods-burstable.slice&#47;kubepods-burstable-pod${podID}.slice&#47;docker-${dockerID}.scope -o perf_containers.csv --append -I 30000 sleep 30s&quot; or use &quot;perf stats --pid ${docker_pid}&quot; is better? Thanks.</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/9e/b26da70d.jpg" width="30px"><span>closer</span> 👍（2） 💬（0）<div>这几章都比较底层，作为运维人员，需要前置学习那些知识点，很多知识点都是盲点</div>2021-02-01</li><br/>
</ul>