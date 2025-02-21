你好，我是倪朋飞。

专栏更新至今，四大基础模块之一的CPU性能篇，我们就已经学完了。很开心过半数同学还没有掉队，仍然在学习、积极实践操作，并且热情地留下了大量的留言。

这些留言中，我非常高兴地看到，很多同学已经做到了活学活用，用学过的案例思路，分析出了线上应用的性能瓶颈，解决了实际工作中的性能问题。 还有同学能够反复推敲思考，指出文章中某些不当或不严谨的叙述，我也十分感谢你，同时很乐意和你探讨。

此外，很多留言提出的问题也很有价值，大部分我都已经在app里回复，一些手机上不方便回复的或者很有价值的典型问题，我专门摘了出来，作为今天的答疑内容，集中回复。另一方面，也是为了保证所有人都能不漏掉任何一个重点。

今天是性能优化答疑的第一期。为了便于你学习理解，它们并不是严格按照文章顺序排列的。每个问题，我都附上了留言区提问的截屏。如果你需要回顾内容原文，可以扫描每个问题右下方的二维码查看。

## 问题1：性能工具版本太低，导致指标不全

![](https://static001.geekbang.org/resource/image/19/ba/19084718d4682168fea4bb6cb27c4fba.png?wh=750%2A747)

这是使用 CentOS 的同学普遍碰到的问题。在文章中，我的 pidstat 输出里有一个 %wait 指标，代表进程等待 CPU 的时间百分比，这是 systat 11.5.5 版本才引入的新指标，旧版本没有这一项。而CentOS 软件库里的 sysstat 版本刚好比这个低，所以没有这项指标。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（44） 💬（4）<div>打卡day14
之前一直理解有误，感谢指出！
pidstat 中， %wait 表示进程等待 CPU 的时间百分比。此时进程是运行状态。
top 中 ，iowait% 则表示等待 I&#47;O 的 CPU 时间百分比。此时进程处于不可中断睡眠态。
等待 CPU 的进程已经在 CPU 的就绪队列中，处于运行状态；而等待 I&#47;O 的进程则处于不可中断状态。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/32/0b/981b4e93.jpg" width="30px"><span>念你如昔</span> 👍（18） 💬（1）<div>非常非常感谢，这钱花的值，之前没有对这些东西形成体系，老是感觉有力使不上的感觉，自从看了老师的文档，终于飘了，都想跳槽了？！。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/3d/1189e48a.jpg" width="30px"><span>微思</span> 👍（8） 💬（1）<div>老师，等待IO的不可中断进程是否一直占用CPU？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/ca/6173350b.jpg" width="30px"><span>神奇小懒懒</span> 👍（8） 💬（1）<div>课程很系统，把自己以前的知识都串起来了，后续争取每个案例自己都做一次，并且融合自己的经验改进下案例</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/12/b3/9e8f4b4f.jpg" width="30px"><span>MoFanDon</span> 👍（4） 💬（1）<div>做了几年运维一直想要掌握，却了解的很零散。这段时间的课程让我学习很多，感谢老师。</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（1）<div>[D13打卡]
多谢老师提出来, pidstat 和 top 中的 %wait 含义并不一样.
之前只知道top是io的wait, 而新接触的pidstat的倒没有细想过.
确实是应该多man一下,看下命令文档.
刚开始要把工具用起来, 之后再查看命令的详细文档.</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/46/1d/83021ef5.jpg" width="30px"><span>大哈</span> 👍（1） 💬（1）<div>老师，您好，我想知道像pidstat这样的工具是怎么获取到这些性能数据的，我自己去开发应该从那里获取呢？</div>2019-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqcQWfsAka5Y9wVIKTKuN1173m9N5MyiadEJ2mdaUv9eHreg2oOYnGKsib9xvLtQ2cdxTKicwF351eTQ/132" width="30px"><span>胡莉婷</span> 👍（1） 💬（2）<div>补充一点。我们的进程都是后台服务，机器1和机器2启动后都没有业务进来</div>2019-01-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqcQWfsAka5Y9wVIKTKuN1173m9N5MyiadEJ2mdaUv9eHreg2oOYnGKsib9xvLtQ2cdxTKicwF351eTQ/132" width="30px"><span>胡莉婷</span> 👍（1） 💬（1）<div>老师你好，我们有个问题，还请给个思路。同样的应用程序，部署在两台机器上，比如机器1和机器2.。top发现机器2上进程数据段大小是机器1上数据段的10倍大。还有一个情况是机器2的进程(有上百个)启动后，比较集中在某一个cpu上，而机器1上我们的进程分布就比较均匀。还请指点一下</div>2019-01-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEL5xnfuicbtRz4F87AAjZX6oCEjMtYiaIu4iaQichQmy0vEBA6Sumic1RDvUCeuBEqj6iatnt2kENbKYmuw/132" width="30px"><span>dexter</span> 👍（1） 💬（1）<div>[root@localhost ~]# docker run --name phpfpm -itd --network container:nginx feisky&#47;php-fpm
flag provided but not defined: --network
See &#39;docker run --help&#39;.
[root@localhost ~]# docker version
Client version: 1.7.1
Client API version: 1.19
Go version (client): go1.4.2
Git commit (client): 786b29d&#47;1.7.1
OS&#47;Arch (client): linux&#47;amd64
Server version: 1.7.1
Server API version: 1.19
Go version (server): go1.4.2
Git commit (server): 786b29d&#47;1.7.1
OS&#47;Arch (server): linux&#47;amd64
centos6.10 安装发现没有--network参数</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/04/ae/0118c132.jpg" width="30px"><span>辉晖</span> 👍（0） 💬（1）<div>我的机器出现最多的不是RES，而是Local timer interrupts</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e5/52/35bc9c07.jpg" width="30px"><span>Musisan</span> 👍（0） 💬（1）<div>Package man-pages-3.53-5.el7.noarch already installed and latest version。
No manual entry for vmstat，
老师，这是为啥，centos7，6的。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/b4/d5d9e4fb.jpg" width="30px"><span>爱学习的小学生</span> 👍（0） 💬（1）<div>打卡</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/89/71/03a99e56.jpg" width="30px"><span>、荒唐_戏_</span> 👍（0） 💬（1）<div>day2   昨晚排查一台机器load200+  8  core 觉得摸到一点思路了，但是还没查到具体问题，还要继续加油୧( ⁼̴̶̤̀ω⁼̴̶̤́ )૭</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>机械磁盘（HDD）、低端固态磁盘（SSD）与高端固态。性能差别有多大</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/54/98/52ca7053.jpg" width="30px"><span>Vicky🐣🐣🐣</span> 👍（0） 💬（1）<div>老师好细心啊！
去年毕业，运维岗一年半，还没遇到过线上这种比较复杂的案例，几乎都是top看一下，看到是研发在自己跑脚本捞数据导致的。看完老师的分享，感觉学到了很多，就是不知道真正需要用的时候，是否能想起来以及灵活应用</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（0） 💬（1）<div>写了10年的程序终于有机会系统学习linux远离和实战了。多谢老师。</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/47/75875257.jpg" width="30px"><span>虎虎❤️</span> 👍（0） 💬（1）<div>虽然不讲各个工具的各项参数，我是很赞同的。但是，像从来没有接触过性能工具的我，根本没有意识到pidstat 和 top的wait是不同的。

是不是pidstat所有输出，都是以进程时间为基础，而top中都是以cpu时间为基础呢？

希望作者多提点一下我们新手哈。</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/c4/53cdb3ec.jpg" width="30px"><span>奋斗的菜鸟</span> 👍（0） 💬（1）<div>打卡</div>2018-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erJR5Kj0Xm6LykFHLaWqHjQiaroVxgdoGI7uHEGz2D3PfibWNkBYP23QLzFmcuicgKLbqUch0ZJ2ZNOA/132" width="30px"><span>湖湘志</span> 👍（0） 💬（1）<div> D13</div>2018-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/18/edc1b373.jpg" width="30px"><span>风飘，吾独思</span> 👍（0） 💬（1）<div>打卡</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/84/70/6573ec64.jpg" width="30px"><span>0.0</span> 👍（0） 💬（1）<div>execsnoop无法安装</div>2018-12-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（0） 💬（1）<div>perf report 显示的swapper [kernel.kallsyms] 这类信息要排除吗？自己查了一下，是内核的符号，在排障的时候要忽略不看吗？</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/56/a3/649d861c.jpg" width="30px"><span>淸曉</span> 👍（0） 💬（1）<div>老师你好，最近遇到一个问题：目录下的jar包，都安装好了，怎么用命令查看用到哪些应用或软件。所有应用&#47;软件都会显示版本号，路径，配置，等，是在一个页面显示的。
只是知道进到jar包的目录下，然后执行命令，就会出现一个页面，包含用到，比如Redis，zookeeper等的路径，版本号，等一些信息。
急需老师帮忙，这命令是什么？
望老师回复，万分感谢！</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/5b/9199c264.jpg" width="30px"><span>大兵</span> 👍（0） 💬（1）<div>@walker 你的阿里云服务是否用了Nginx做了反向代理?  这是由于nginx代理使用了短链接的方式和后端交互的原因，使得nginx和后端的 ESTABLISHED变得很少而TIME_WAIT很多. 解决方案可参考 (http:&#47;&#47;www.phpfans.net&#47;article&#47;htmls&#47;201010&#47;MzEyMTU0.html) 这篇文章.
</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（0） 💬（1）<div>在实际中遇到一个问题，阿里云的服务器，访问比较少TIME_WAIT已经达到阿里云设置的上限。但是负载，内存，io都不高，ESTABLISHED也只有300。si从0.3到3，这个应该从哪些方面入手去定位根源呢</div>2018-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/99/5d603697.jpg" width="30px"><span>MJ</span> 👍（2） 💬（0）<div>虽然有很多地方不太懂（不熟Linux原理），但还是要跟下来，多过几遍。
同时，私下学Linux原理</div>2019-03-28</li><br/><li><img src="" width="30px"><span>ch_ort</span> 👍（1） 💬（2）<div>“pidstat 中， %wait 表示进程等待 CPU 的时间百分比。
 top 中 ，iowait% 则表示等待 I&#47;O 的 CPU 时间百分比。
”
问题来了，现在通过top和mpstat发现是iowati高导致的，怎么通过pidstat找到iowait高的进程呢？</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（0）<div>测试跑的Q4 还是无法模拟出 I&#47;O 性能瓶颈，依然是要加了 --device-write-iops --device-read-iops 限制后才可以。

[root@centos-7 ~]# docker run --privileged --name=app -itd feisky&#47;app:iowait &#47;app -d &#47;dev&#47;sda -s 67108864 -c 20
e7a7deddba3d2845030515fbbe25785382306d3c600c474a22de54d543a2cf53
[root@centos-7 ~]# docker logs app
Reading data from disk &#47;dev&#47;sdb with buffer size 67108864 and count 20

# 内核cpu时间sy，软中断cpu时间si升高明显
top - 00:15:15 up 12 min,  2 users,  load average: 23.50, 7.07, 2.49
Tasks: 148 total,  43 running, 104 sleeping,   1 stopped,   0 zombie
%Cpu0  : 21.1 us, 54.9 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi, 24.0 si,  0.0 st
%Cpu1  : 21.8 us, 76.8 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  1.4 si,  0.0 st
KiB Mem :  3880792 total,   737592 free,  2880084 used,   263116 buff&#47;cache
KiB Swap:        0 total,        0 free,        0 used.   764308 avail Mem 

# docker run --privileged --name=app -itd --device-write-iops &#47;dev&#47;sda:3 --device-read-iops &#47;dev&#47;sda:3 feisky&#47;app:iowait &#47;app -d &#47;dev&#47;sda -s 67108864 -c </div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（1） 💬（0）<div>mark </div>2018-12-27</li><br/>
</ul>