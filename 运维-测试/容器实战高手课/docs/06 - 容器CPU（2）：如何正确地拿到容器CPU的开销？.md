你好，我是程远。今天我们聊一聊，如何正确地拿到容器CPU的开销。

为啥要解决这个问题呢，还是来源于实际工作中的需要。

无论是容器的所有者还是容器平台的管理者，我们想要精准地对运行着众多容器的云平台做监控，快速排查例如应用的处理能力下降，节点负载过高等问题，就绕不开容器CPU开销。**因为CPU开销的异常，往往是程序异常最明显的一个指标。**

在一台物理机器或者虚拟机里，如果你想得到这个节点的CPU使用率，最常用的命令就是top了吧？top一下子就能看到整个节点当前的CPU使用情况。

那么在容器里，top命令也可以做到这点吗？想要知道答案，我们还是得实际动手试一试。

## 问题重现

实际上，你在使用容器的时候，如果运行top命令来查看当前容器总共使用了多少CPU，你肯定马上就会失望了。

这是因为我们在容器中运行top命令，虽然可以看到容器中每个进程的CPU使用率，但是top中"%Cpu(s)"那一行中显示的数值，并不是这个容器的CPU整体使用率，而是容器宿主机的CPU使用率。

就像下面的这个例子，我们在一个12个CPU的宿主机上，启动一个容器，然后在容器里运行top命令。

这时我们可以看到，容器里有两个进程threads-cpu，总共消耗了200%的CPU（2 CPU Usage），而"%Cpu(s)"那一行的"us cpu"是58.5%。对于12CPU的系统来说，12 * 58.5%=7.02，也就是说这里显示总共消耗了7个CPU，远远大于容器中2个CPU的消耗。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIz9dKN1C8rKQoaVtmEGdzObhlia6zAfTsPYOm4ibz39VjTbu7Aia1LyeedHR26b6nxUtcCufpichcYgw/132" width="30px"><span>上邪忘川</span> 👍（25） 💬（4）<div>随便写了一个，比较粗糙
#!&#47;bin&#47;bash
cpuinfo1=$(cat &#47;sys&#47;fs&#47;cgroup&#47;cpu,cpuacct&#47;cpuacct.stat)
utime1=$(echo $cpuinfo1|awk &#39;{print $2}&#39;)
stime1=$(echo $cpuinfo1|awk &#39;{print $4}&#39;)
sleep 1
cpuinfo2=$(cat &#47;sys&#47;fs&#47;cgroup&#47;cpu,cpuacct&#47;cpuacct.stat)
utime2=$(echo $cpuinfo2|awk &#39;{print $2}&#39;)
stime2=$(echo $cpuinfo2|awk &#39;{print $4}&#39;)
cpus=$((utime2+stime2-utime1-stime1))
echo &quot;${cpus}%&quot;
</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（21） 💬（1）<div>多谢老师的分享，之前想去搞明白进程CPU时间的计算，一直没有去花时间研究，今天终于透彻地明白了。

我有个问题不太明白，想请教下，容器运行时比如docker，在做容器化的时候，有没有办法构造出一个和物理机一样的proc文件系统呢？这样的话，容器环境和虚拟机也没啥差别了，物理机上的应用也可以无障碍运行在容器环境中。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（17） 💬（1）<div>老师，ticks 1s中是100次，这个怎么查呢？</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bf/aa/32a6449c.jpg" width="30px"><span>蒋悦</span> 👍（9） 💬（1）<div>老师您好，
我有一个问题。根据我的理解，容器的cpu使用就必须要在容器内进行，从宿主机是无法计算的，是这样吗？如果是的，那么，这个监控cpu的代码就需要侵入程序代码(容器中跑的业务代码)，这会不会有些无奈啊？另外，这个侵入的代码，所在的线程如果不能被实时调度，则瞬时速度就算的不准确了吧？

望解答。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8f/5f/11ba01f2.jpg" width="30px"><span>路一直在</span> 👍（4） 💬（2）<div>老师，如果计算容器整体的cpu使用率，使用cpuacct.stat是否完整，因为cpuacct.stat中只有us和sys的ticks，其他的类似iowait、idle等的ticks不用计算吗？</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/08/0287f41f.jpg" width="30px"><span>争光 Alan</span> 👍（4） 💬（3）<div>老师，非常感谢，之前都是模糊知道大概这个意思，这次明白了

另外有个问题：
我当然做监控的时候发现docker stats 和cadvisor(或通过cgroup直接计算)通过cgroup拿到的cpu使用率，内存使用率都是不一样的，您这边知道根本的原因吗？</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/9b/08/27ac7ecd.jpg" width="30px"><span>水蒸蛋</span> 👍（3） 💬（1）<div>老师，&#47;sys&#47;fs&#47;cgroup&#47;cpu 和 cpuacc，这2个有什么区别
还有这个获取容器中是获取容器的CPU使用，宿主机是获取宿主机的CPU使用吗</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/15/4d/bbfda6b7.jpg" width="30px"><span>笃定</span> 👍（1） 💬（1）<div>老师问一下，像Prometheus或者k8s自己的metrics server获取到的pod各个资源使用率(cpu men net io)也是这样通过查看进程&#47;proc来计算得出的吗？如果是这样的话，指标数据太多，运算太大会不会也会消耗节点资源呢</div>2021-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/a9/bc/d3e25886.jpg" width="30px"><span>GCC?</span> 👍（1） 💬（2）<div>老师，在k8s集群中，使用metrics查看到整个pod的资源用量，这个粒度已经够了吧？我的理解是如果pod内不是单一容器，或者容器内有多个进程，这个时候才应该考虑进程级的cpu用量。</div>2020-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/7e/e0/ff046b55.jpg" width="30px"><span>李兵</span> 👍（0） 💬（1）<div>老师，如已经是高负载的情况下。应该会有很多正常的进程被安排在D进程中，如何区分造成高负载的D进程呢？</div>2021-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e3/9e/b26da70d.jpg" width="30px"><span>closer</span> 👍（0） 💬（1）<div>问题1）生产上面 如果把nginx放入到pod中，是不是会碰到目前为止老师说的那些所有问题 比如关闭容器sigterm主进程nginx master。所有的nginx worker都被sigkill。
问题2）然后容器里面的各个进程用的cpu总合是会被k8s metrics计算到的吧。
谢谢。期待老师百忙中回复</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/32/535e5c3c.jpg" width="30px"><span>mlbjay</span> 👍（2） 💬（0）<div>不可以用 docker stats吗？
这不是 官方推荐吗？</div>2023-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/9a/39/a762e79d.jpg" width="30px"><span>JZ</span> 👍（1） 💬（3）<div>老师，获取cpu的开销可以使用kubectl top这个工具吧，这个拿到的值和文章中公式计算的应该是一致的吧</div>2021-01-11</li><br/><li><img src="" width="30px"><span>Geek_125396</span> 👍（0） 💬（0）<div>请问老师这个cpuacct.stat 中system+user 比cpuacct.usage计算的cpu使用率大，这个是什莫原因</div>2024-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/28/b7f6f118.jpg" width="30px"><span>易</span> 👍（0） 💬（1）<div>老师你好，我这边在容器里面执行了top命令，发现和用您讲述的方法所用的脚本获得的cpu使用率相差不大，近乎相同，这是为什么呢</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b7/24/17f6c240.jpg" width="30px"><span>janey</span> 👍（0） 💬（0）<div>感觉这种计算方法不是很简便，节点上容器多的话，不好判断是哪个容器消耗CPU最多吧</div>2022-11-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq30mvo0eATZ3Yfm5POktwic3NJSRkiagtJt1vaxyvCS22PJRm8xrulXqaLJRWQWb6zNI4zL0G2QkCA/132" width="30px"><span>heyhd9475</span> 👍（0） 💬（0）<div>老师你好，我想请问以下docker stats显示的cpu%依旧是不正确的吗，如果是文中的统计方法根据我的测试是不正确的。</div>2021-10-13</li><br/>
</ul>