你好，我是倪朋飞。

上一节我们详细学习了 Linux 内存回收，特别是 Swap 的原理，先简单回顾一下。

在内存资源紧张时，Linux通过直接内存回收和定期扫描的方式，来释放文件页和匿名页，以便把内存分配给更需要的进程使用。

- 文件页的回收比较容易理解，直接清空缓存，或者把脏数据写回磁盘后，再释放缓存就可以了。
- 而对不常访问的匿名页，则需要通过Swap换出到磁盘中，这样在下次访问的时候，再次从磁盘换入到内存中就可以了。

开启 Swap 后，你可以设置 /proc/sys/vm/min\_free\_kbytes ，来调整系统定期回收内存的阈值，也可以设置 /proc/sys/vm/swappiness ，来调整文件页和匿名页的回收倾向。

那么，当 Swap 使用升高时，要如何定位和分析呢？下面，我们就来看一个磁盘I/O的案例，实战分析和演练。

## 案例

下面案例基于 Ubuntu 18.04，同样适用于其他的 Linux 系统。

- 机器配置：2 CPU，8GB 内存
- 你需要预先安装 sysstat 等工具，如 apt install sysstat

首先，我们打开两个终端，分别 SSH 登录到两台机器上，并安装上面提到的这些工具。

同以前的案例一样，接下来的所有命令都默认以 root 用户运行，如果你是用普通用户身份登陆系统，请运行 sudo su root 命令切换到 root 用户。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/4b/5d/48205f1d.jpg" width="30px"><span>Free_fish</span> 👍（98） 💬（7）<div>用smem --sort swap命令可以直接将进程按照swap使用量排序显示</div>2019-01-04</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（35） 💬（4）<div>答案不是上一讲有提到吗，就算设置为0，如果空闲内存+文件页 &lt; page_low，还是会发生swap，这个值是设置swap的积极程度，就算最不积极，被逼无奈还是得swap的。</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/1e/bdbe93f4.jpg" width="30px"><span>尘封</span> 👍（19） 💬（1）<div>$ swapoff -a &amp;&amp; swapon -a，线上使用这个命令释放swap有什么风险吗？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f8/4b/5ae62b10.jpg" width="30px"><span>Geek_b04b12</span> 👍（10） 💬（2）<div>对于sar以及其他的linux命令,如果出现列对的不整齐的时候,可以适当的参考文档,增加格式化输出,例如:sar的格式化输出:sudo sar -h --human  -r -S 1 5
free 可以添加 -h :free -h 
更容易让人理解</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/84/d8e63885.jpg" width="30px"><span>仲鬼</span> 👍（9） 💬（1）<div>老师好，我研究man sar后还是没理解kbcommit，这个估计值具体指什么呢？
就算单纯以不导致OOM的最小内存理解，为什么会小于kbmemused（已用物理内存）呢？我认为应该是kbcommit &gt;= kbmemused。</div>2019-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/ca/9afb89a2.jpg" width="30px"><span>Days</span> 👍（2） 💬（1）<div>老师，请问如果关闭swap分区，swapping配置是不是无效的？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bd/16/c940b1a3.jpg" width="30px"><span>幸运的人</span> 👍（0） 💬（1）<div>老师，问一个问题
现在的公有云主机或者是私有云的虚拟机，swap默认是0，这种情况下是否还会出现swap in和swap out呢？我在留言中也看到其他同学问过相似的问题，但没有看到答案，请帮忙解释一下？谢谢。
</div>2019-05-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/oCx7GX9P4w5cml1cpbFD1x21Biad3MLCTOhTPJvicRW3xp9C8xTgdiaOSdpFyvibKSfcD1LL4miaT7VtqqKms6rgujg/132" width="30px"><span>zshanjun</span> 👍（0） 💬（2）<div>大文件读取瞬间完成，没有观察到内存的变化：
root@linux-1:~&#47;go&#47;bin# dd if=&#47;dev&#47;sda1 of=&#47;dev&#47;null bs=16G count=2048
0+1 records in
0+1 records out
1048576 bytes (1.0 MB, 1.0 MiB) copied, 0.00693471 s, 151 MB&#47;s</div>2019-01-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz5feictl6uxOFeth2zrO7LPOZKk0mvzIBYD9ic5EyGB39dicBbkYsIYoqqBsibJFo0fDicxN0CUt2dAQ/132" width="30px"><span>berryfl</span> 👍（0） 💬（1）<div>&#47;proc&#47;*&#47;status会匹配到self之类的特殊目录，把匹配的部分写复杂点可以限制到仅数字，例如+([0-9])</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/13/52/db1b01fc.jpg" width="30px"><span>白华</span> 👍（0） 💬（2）<div>我写的dd参数就是大文件系统的数据，一共就20g存储的虚拟机，传的是&#47;dev&#47;root文件系统 有10g 需要写好久，实验现象和您描述的差不多，但是swap就是没变化</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/9a/4231fb93.jpg" width="30px"><span>nemo</span> 👍（0） 💬（1）<div>请问min_free_kbytes一般设置多少？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/86/9a/4231fb93.jpg" width="30px"><span>nemo</span> 👍（0） 💬（1）<div>请教下min_free_kbytes一般设置多少？</div>2019-01-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（0） 💬（1）<div>第一次启动虚拟机按照步骤操作，swpused发现高起来好多，后来几次不知道为什么swpused高不起来了，始终维持2%上下。第一次和后面几次的差异就是第一次运行后，去安装了smem，然后重启了机器几次，系统的默认参数都没改过</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/13/52/db1b01fc.jpg" width="30px"><span>白华</span> 👍（0） 💬（1）<div>在centos系统操作还是会有区别，我的swap分的2G，但是一点都没有用到，kbswpfree总是不变，即使memused达到了98%以上，就看到了kbswpfree的波动。</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（0） 💬（1）<div>centos 没有kbactive 和kbinact 活跃内部的和非活跃内存的情况</div>2019-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（0） 💬（1）<div>[D20打卡]
好像 swappiness 配置为0也会发生swap.
这篇文章中有具体的分析: http:&#47;&#47;www.yunweipai.com&#47;archives&#47;12863.html
```
如果是全局页回收，并且当前空闲内存和所有file based链表page数目的加和都小于系统的high watermark，则必须进行匿名页回收，则必然会发生swap,可以看到这里swappiness的值如何设置是完全无关的，这也解释了为什么其为0，系统也会进行swap的原因
```
由于暂时用不上swap,所以这期就没实际操作. 还有好多专栏要学习.🙈</div>2019-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ert8UYzoypaI9wMPZQV2ibThQ2zKsoge5R25qxHP10eia5pMYOV1mq6G9bft5LoygnyR6bn8RERwQDg/132" width="30px"><span>Geek_2b6807</span> 👍（36） 💬（1）<div>希望老师在用工具的时候能够使用对内核版本要求不高的，毕竟生产环境用较新内核的还是比较少</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（4） 💬（0）<div>swappiness 使用的是默认配置的 60。如果把它配置为0 还会使用 swap 吗？ 
会使用的 ，为0 是最大限度不用，不是一定不用。</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（0）<div>总结：
- 查看使用swap最多的进程
for file in &#47;proc&#47;*&#47;status ; do awk &#39;&#47;VmSwap|Name|^Pid&#47;{printf $2 &quot; &quot; $3}END{ print &quot;&quot;}&#39; $file; done | sort -k 3 -n -r | head

- 关闭swap:
swapoff -a

- 关闭swap再重新打开
swapoff -a &amp;&amp; swapon -a

-命令可以直接将进程按照swap使用量排序显示
smem --sort swap</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/99/ba/f8db012f.jpg" width="30px"><span>流转千回</span> 👍（3） 💬（0）<div>打卡，老师这么晚还在更新专栏，致敬！</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/03/eba78e43.jpg" width="30px"><span>风清扬</span> 👍（2） 💬（2）<div>为何我试用watch -d  grep -A 15 &#39;Normal&#39; &#47;proc&#47;zoneinfo之后输出全是0呀???</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（1） 💬（0）<div>老师您好！在内存资源紧张时，Linux 通过直接内存回收和定期扫描的方式，来释放文件页和匿名页，以便把内存分配给更需要的进程使用。
这个定期扫描的周期是多少？</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/41/ba59e1ee.jpg" width="30px"><span>Ethan</span> 👍（1） 💬（0）<div>遇到类似的情况.
虚拟机,CentOS 7.4,4G内存,1G SWAP大小,swappiness设置为60,执行dd,swap没有什么变化.</div>2019-09-16</li><br/><li><img src="" width="30px"><span>如果</span> 👍（1） 💬（0）<div>DAY20，打卡</div>2019-01-31</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（1） 💬（0）<div>打卡day21
按我的理解，swapness只是几率，并不意味着一定，所以还是会发生匿名页交换，只是几率小点</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/61/2b/24133710.jpg" width="30px"><span>尘</span> 👍（0） 💬（0）<div>老师您好，free 的结果中swap占用很大，但是执行for file in &#47;proc&#47;*&#47;status ; do awk &#39;&#47;VmSwap|Name|^Pid&#47;{printf $2 &quot; &quot; $3}END{ print &quot;&quot;}&#39; $file; done | sort -k 3 -n -r | head的结果中，进程占用的swqp又很小，这个是什么原因导致的呢？</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/eb/31/2768a6a1.jpg" width="30px"><span>斌子</span> 👍（0） 💬（0）<div>做试验的时候为什么我的kbbuffers并没有增长太大，反而是kbcommit增长很快
02:21:44 PM  kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
02:21:45 PM  361.6M    131.2M      3.3G     55.7%    818.2M    952.4M      0.0k
</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/94/33/4becb05a.jpg" width="30px"><span>Jason Wong</span> 👍（0） 💬（0）<div>开启 Swap 后，你可以设置 &#47;proc&#47;sys&#47;vm&#47;min_free_kbytes ，来调整系统定期回收内存的阈值，也可以设置 &#47;proc&#47;sys&#47;vm&#47;swappiness ，来调整文件页和匿名页的回收倾向。
----这2项设置只是让内存回收到swap，这样swap不是会一直变大？由谁来回收swap呢？</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/a3/97/139eb54c.jpg" width="30px"><span>Lam</span> 👍（0） 💬（1）<div>$ free -m
             total       used       free     shared    buffers     cached
Mem:         31708      31465        242      14189        178      29689
-&#47;+ buffers&#47;cache:       1597      30110
Swap:        15919        624      15295

---
请问为什么Oracle数据库服务器上内存总是被耗尽呢，且使用了少量swap，cache占大头，是Oracle为了提高读写性能而大量使用cache吗？</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/81/60/71ed6ac7.jpg" width="30px"><span>谢哈哈</span> 👍（0） 💬（0）<div>肯定会继续使用swap，swappiness只是换出anno memory与page memory的倾向，为0时，在低于high memory的水位时就开始换出page memory到swap</div>2020-12-13</li><br/>
</ul>