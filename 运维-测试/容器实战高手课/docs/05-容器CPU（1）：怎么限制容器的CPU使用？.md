你好，我是程远。从这一讲开始，我们进入容器CPU这个模块。

我在第一讲中给你讲过，容器在Linux系统中最核心的两个概念是Namespace和Cgroups。我们可以通过Cgroups技术限制资源。这个资源可以分为很多类型，比如CPU，Memory，Storage，Network等等。而计算资源是最基本的一种资源，所有的容器都需要这种资源。

那么，今天我们就先聊一聊，怎么限制容器的CPU使用？

我们拿Kubernetes平台做例子，具体来看下面这个pod/container里的spec定义，在CPU资源相关的定义中有两项内容，分别是 **Request CPU** 和 **Limit CPU**。

```
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: app
    image: images.my-company.example/app:v4
    env:
    resources:
      requests:
        memory: "64Mi"
        cpu: "1"
      limits:
        memory: "128Mi"
        cpu: "2"
…
```

很多刚刚使用Kubernetes的同学，可能一开始并不理解这两个参数有什么作用。

这里我先给你说结论，在Pod Spec里的"Request CPU"和"Limit CPU"的值，最后会通过CPU Cgroup的配置，来实现控制容器CPU资源的作用。

那接下来我会先从进程的CPU使用讲起，然后带你在CPU Cgroup子系统中建立几个控制组，用这个例子为你讲解CPU Cgroup中的三个最重要的参数"cpu.cfs\_quota\_us""cpu.cfs\_period\_us""cpu.shares"。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（15） 💬（1）<div>为什么说“云平台里呢，大部分程序都不是实时调度的进程，而是普通调度（SCHED_NORMAL）类型进程”？这块不是很明白</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（6） 💬（2）<div>老师，不太明白  “Request CPU就是无论其他容器申请多少 CPU 资源，即使运行时整个节点的 CPU 都被占满的情况下，我的这个容器还是可以保证获得需要的 CPU 数目”，这句话改怎么理解呢？当节点cpu都被占满的情况下，我的这个容器会去抢占吗？ 另外cpu.shares是个权重，如何去保证Request CPU的数量？</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/aa/6f780187.jpg" width="30px"><span>言希</span> 👍（4） 💬（1）<div>请问老师，我在环境上遇到 cpu.cfs_quota_us 取值为 -1 的，这种是不是代表的不限制CPU的使用 ？</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c2/77a413a7.jpg" width="30px"><span>Action</span> 👍（3） 💬（1）<div>老师，假如我有10个节点，每个节点的cpu核心数是40，只是调度pod，那么limit.cpu 可以设置为400吧？</div>2020-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c5/a7/cc8764d1.jpg" width="30px"><span>Geek_cd6rkj</span> 👍（3） 💬（1）<div>老师，您好，如果一个容器里面有多个进程，这个限制是针对所有进程，还是只是pid是1的进程？</div>2020-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/15/51187703.jpg" width="30px"><span>兜兜</span> 👍（3） 💬（1）<div>请问下关于wa和hi&#47;si的问题：
1. 例子中，wa是等待磁盘IO的状态，那等待网络IO时，是不是wa呢？
2. 例子中，hi&#47;si是收到网卡中断，那收到磁盘中断时，是不是也是hi&#47;si？</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/33/110437cc.jpg" width="30px"><span>不二</span> 👍（1） 💬（1）<div>请问老师，cpu.rt_runtime_us一般是不是用不上，Linux系统中哪些程序会被配置为实时调度程序呢？如果没有实时调度程序这个参数也就没有了存在的必要吧</div>2021-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/c6/28dfdbc9.jpg" width="30px"><span>*</span> 👍（0） 💬（2）<div>老师， threads-cpu这个脚本能提供吗</div>2022-02-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLvkQrAkQv9ibJ4XarXAkia2SLvavwxWYZH1GnrcibSY0AtBDeBVxh2Cw51WlyCwwr7icOCyPsj5u0pdg/132" width="30px"><span>Geek_ce0af4</span> 👍（0） 💬（1）<div>评论区太精彩</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b0/2f/e2096905.jpg" width="30px"><span>马成</span> 👍（0） 💬（2）<div>软中断我理解就是内部中断，系统调用是其中的一种。那么sy内核时间指的是系统调用时间么？si软中断时间包含系统调用时间么？我被搞糊涂了……</div>2021-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（0） 💬（2）<div>老师，我有个困惑，在read的时候，当进程在wa状态，是不是占用着CPU？</div>2021-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/bd/ee/89f20aaa.jpg" width="30px"><span>强子</span> 👍（0） 💬（1）<div>老师 关于request cpu还是不太理解 request是必须满足的 但是通过cpu.share无法保证 那k8s是如何保证的？是scheduler在调度的时候自己计算的吗 包括允许超售的情况，能否解释一下 感谢🙏</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/08/0287f41f.jpg" width="30px"><span>争光 Alan</span> 👍（0） 💬（1）<div>好，下面我们再来运行第二个例子来理解 cpu.shares。我们先把第一个例子里的程序启动，同时按前面的内容，一步步设置好 group3 里 cpu.cfs_quota_us 和 cpu.shares。

是不是写错了，
第一个例子的程序停止？</div>2020-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/1e/9e69527e.jpg" width="30px"><span>max</span> 👍（0） 💬（1）<div>老师，容器中的应用如何获取有效网卡</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（0） 💬（4）<div>有一点不理解，想请教下老师：
而&quot;Request CPU&quot;就是无论其他容器申请多少 CPU 资源，即使运行时整个节点的 CPU 都被占满的情况下，我的这个容器还是可以保证获得需要的 CPU 数目，


假设系统只有2个group并列，group1和group2，系统总共2CPU
group1 ：request 2 cpu，limit 3 cpu
group2 ：request 2 cpu，limit 3 cpu

由于申请总量大于总量，那么按照K8S的调度原则，是没法启动全部容器的。上面的假设情况，按道理是不存在的，对吧。</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/96/a03175bc.jpg" width="30px"><span>莫名</span> 👍（39） 💬（2）<div>CPU 使用率分解图画的挺有创意👍</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/be/546665e3.jpg" width="30px"><span>心随缘</span> 👍（7） 💬（0）<div>老师的时间轴讲解TOP非常棒！CPU 使用分解的很到位~赞!</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/60/71ed6ac7.jpg" width="30px"><span>谢哈哈</span> 👍（5） 💬（0）<div>group1:group2是1比1，由于group1 limit是3.5，那group1分到的只能是两个核，剩余的2个核给group3和group4，group4:group3是3比1，那么得出group4与group3各分配的核就是1.5核与0.5核</div>2020-11-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIz9dKN1C8rKQoaVtmEGdzObhlia6zAfTsPYOm4ibz39VjTbu7Aia1LyeedHR26b6nxUtcCufpichcYgw/132" width="30px"><span>上邪忘川</span> 👍（3） 💬（2）<div>分别为2,1.5,0.5
group1和group2分配的cpu配额已经超过4个总cpu，那么就会按照cpu.shares的比例去分配cpu。其中，group1:group2=1:1，group3:group4=1:3，group2=group3+group4，得出group1:group3:group4=4:1:3</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（2） 💬（0）<div>尝试胡乱分析下：
group1 的shares为1024，quota 3.5，尝试使用4，
group2的shares默认为1024，quota设置为-1，不受限制，也即是，如果CPU上只有group2的话，那么group2可以使用完所有的CPU（实际上根据group3和group4，group2最多也就能用到1.5+3.5 core）

故而，group1和group2各分配到2

把group2分到的2CPU，看作总量，再次分析group3和group4
group3和group3尝试使用的总量超过2，所以按照shares比例分配，group3使用1&#47;(1+3) * 2 = 0.5，group4使用3&#47;(1+3) * 2 = 1.5</div>2020-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/6d/8c0a487b.jpg" width="30px"><span>册书一幕</span> 👍（1） 💬（0）<div>request只有满的时候才有用，是否意味着CPU不满的时候，request可以任意定义，容器都能使用到超出request定义的部分</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b2/91/714c0f07.jpg" width="30px"><span>zero</span> 👍（1） 💬（0）<div>这节真心不错</div>2021-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icV5dx2hqJOiaQ2S8Lh1z448lQjTZllkd6wWib21rTKq5uicIcDTr5LIYsauFEudnFWefI2xGnvXrcLNfaFrKYMuew/132" width="30px"><span>缝合怪天下无敌</span> 👍（1） 💬（1）<div>老师，这边想请教一个问题，两个容器a,b进程分别设置了cpuset以及cpu.share，其中两个进程绑定了相同的16核，a设置较大的cpu.share值而b设置较小的cpu.share值，比例为4比1，同时将这两个进程压测到80%左右的cpu使用率，发现他俩各占用了8核左右的cpu就好像cpu.share值没有生效，可以请教一下老师可能是什么原因造成cpu.share没有生效</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/21/34c72e67.jpg" width="30px"><span>cyz</span> 👍（1） 💬（0）<div>评论解答依然精彩</div>2021-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/16/02/d362f668.jpg" width="30px"><span>Giant</span> 👍（0） 💬（0）<div>非常棒！认真的看了一遍，更清楚k8s 中容器的资源限制原理了。</div>2024-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/8d/c6/9afdffaa.jpg" width="30px"><span>Andylin</span> 👍（0） 💬（0）<div>在group4：中 echo 3072 &gt; &#47;sys&#47;fs&#47;cgroup&#47;cpu&#47;group2&#47;group3&#47;cpu.shares   应该调整为echo 3072 &gt; &#47;sys&#47;fs&#47;cgroup&#47;cpu&#47;group2&#47;group4&#47;cpu.shares 才是对的</div>2023-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/d5/e5/101e13b5.jpg" width="30px"><span>HF</span> 👍（0） 💬（0）<div>echo 3072 &gt; &#47;sys&#47;fs&#47;cgroup&#47;cpu&#47;group2&#47;group3&#47;cpu.shares # shares 比例 group4: group3 = 3:1 这个地方是否有误</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/54/7b/780c04ff.jpg" width="30px"><span>史努比</span> 👍（0） 💬（0）<div>我尝试回答一下。不对之处，感谢指正：

1.当执行完create_groups.sh后，创建出了四个CPU控制组，分别是group1、group2、group3和group4，其中group3和group4属于group2层级下；

2.执行完update_group1.sh后，group1控制组设置的CPU限制是3.5核(cpu.cfs_quota_us为350000)，且节点无其他控制器组进程运行，group1控制组的进程最多能够使用到CPU配额上限，即3.5个CPU；

3.执行完update_group4.sh后，两个控制组的进程将占满节点CPU，此时节点cpu资源会被group1下和group4下的进程完全瓜分。由于group1和group4两个控制组的cpu.shares分别是1024和3072，也就是1:3，所以两个控制组下的进程能够分得的CPU资源是1核和3核；

4.最后是update_group3.sh，三个控制组(group1、group4、group3)的进程占满节点CPU，这里前后两个阶段各控制组下进程的cpu分配无变化：首先是刚开始为group3设置cpu.cfs_quota_us为-1(不限制cpu上限)，且未设置cpu.shares（默认就是1024）。此时group1、group4和group3控制组下的进程最多能够使用节点cpu资源比例由各自cpu.shares在总的cpu.shares值的比例决定，因此分别是1:3:1，最后分别能使用0.8、2.4和0.8个CPU；而后将group3的cpu.cfs_quota_us设置为150000，cpu.shares为1024。由于节点cpu占满，各控制值的cpu.shares比例未发生改变，且group3的cpu限制是大于0.8个cpu（1.5个cpu），因此group1、group4和group3控制组下进程仍然是分得0.8、2.4和0.8个CPU。</div>2022-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/6d/8c0a487b.jpg" width="30px"><span>册书一幕</span> 👍（0） 💬（1）<div>这一节有些没法理解：request是share控制的，limit是quota和period比率来控制。哪request是不是得要CPU满的时候才能生效，保证容器CPU始终占用shares比率的量。那这个limit存在的必要性是什么？可以理解成控制容器不能占用完cpu所有时间片和period周期内可用的时间片长度吗？    CPU的控制似乎跟内存有着很大区别</div>2022-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/45/c6/28dfdbc9.jpg" width="30px"><span>*</span> 👍（0） 💬（0）<div>老师，cgroup挂载掉了可以重新挂载吗</div>2022-03-25</li><br/>
</ul>