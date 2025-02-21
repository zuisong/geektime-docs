你好，我是倪朋飞。

上一节我讲了 CPU 使用率是什么，并通过一个案例教你使用 top、vmstat、pidstat 等工具，排查高 CPU 使用率的进程，然后再使用 perf top 工具，定位应用内部函数的问题。不过就有人留言了，说似乎感觉高 CPU 使用率的问题，还是挺容易排查的。

那是不是所有 CPU 使用率高的问题，都可以这么分析呢？我想，你的答案应该是否定的。

回顾前面的内容，我们知道，系统的 CPU 使用率，不仅包括进程用户态和内核态的运行，还包括中断处理、等待 I/O 以及内核线程等。所以，**当你发现系统的 CPU 使用率很高的时候，不一定能找到相对应的高 CPU 使用率的进程**。

今天，我就用一个 Nginx + PHP 的 Web 服务的案例，带你来分析这种情况。

## 案例分析

### 你的准备

今天依旧探究系统CPU使用率高的情况，所以这次实验的准备工作，与上节课的准备工作基本相同，差别在于案例所用的 Docker 镜像不同。

本次案例还是基于 Ubuntu 18.04，同样适用于其他的 Linux 系统。我使用的案例环境如下所示：

- 机器配置：2 CPU，8GB 内存
- 预先安装 docker、sysstat、perf、ab 等工具，如 apt install [docker.io](http://docker.io) sysstat linux-tools-common apache2-utils
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/39/6a5cd1d8.jpg" width="30px"><span>sotey</span> 👍（174） 💬（3）<div>对老师膜拜！今天一早生产tomcat夯住了，16颗cpu全部98%以上，使用老师的方法加上java的工具成功定位到了问题线程和问题函数。</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/35/25/bab760a1.jpg" width="30px"><span>好好学习</span> 👍（78） 💬（1）<div>perf record -ag -- sleep 2;perf report
一部到位</div>2018-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/39/ddcf26ac.jpg" width="30px"><span>bruceding</span> 👍（43） 💬（2）<div>http:&#47;&#47;blog.bruceding.com&#47;420.html  这个是之前的优化经历，通过 perf + 火焰图，定位热点代码，结合业务和网络分析，最终确定问题原因</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f9/3c/f75ab868.jpg" width="30px"><span>风</span> 👍（18） 💬（8）<div>老师好，我在实验的过程中，在最后使用 perf record -ag 的时候，发现记录下来的值，其中 stress 并不是消耗 CPU 最猛的进程，而是swapper，不知道什么原因？碰到这种情况时，该如何继续排查下去？以下是我的 perf report
Samples: 223K of event &#39;cpu-clock&#39;, Event count (approx.): 55956000000
  Children      Self  Command          Shared Object            Symbol
+   11.54%     0.00%  swapper          [kernel.kallsyms]        [k] cpu_startup_entry
+   11.42%     0.00%  swapper          [kernel.kallsyms]        [k] default_idle_call
+   11.42%     0.00%  swapper          [kernel.kallsyms]        [k] arch_cpu_idle
+   11.42%     0.00%  swapper          [kernel.kallsyms]        [k] default_idle
+   11.05%    11.05%  swapper          [kernel.kallsyms]        [k] native_safe_halt
+    8.69%     0.00%  swapper          [kernel.kallsyms]        [k] start_secondary
+    4.36%     4.36%  stress           libc-2.24.so             [.] 0x0000000000036387
+    3.44%     0.00%  php-fpm          libc-2.24.so             [.] 0xffff808406d432e1
+    3.44%     0.00%  php-fpm          [unknown]                [k] 0x6cb6258d4c544155
+    3.43%     3.43%  stress           stress                   [.] 0x0000000000002eff
+    3.20%     0.00%  stress           [kernel.kallsyms]        [k] page_fault
+    3.20%     0.00%  stress           [kernel.kallsyms]        [k] do_page_fault
+    3.15%     0.76%  stress           [kernel.kallsyms]        [k] __do_page_fault</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/39/ddcf26ac.jpg" width="30px"><span>bruceding</span> 👍（8） 💬（1）<div>对于内核函数的调试，4.0 的内核可以使用 eBPF 工具，2.6 或者 4.0 以下的工具，使用 systemtap。perf 是基于采样的原理。本文的例子 execsnoop 可以替换成 https:&#47;&#47;sourceware.org&#47;systemtap&#47;SystemTap_Beginners_Guide&#47;threadtimessect.html。systemtap 中文资料比较少，本人也翻译了相关文档，参考：http:&#47;&#47;systemtap.bruceding.com&#47;。</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/7c/b76ad65d.jpg" width="30px"><span>每一段路都是一种领悟</span> 👍（6） 💬（2）<div>今天一个程序负载飙到140，最高点240，我们的服务器没有挂掉，真的是牛逼，另外使用这几天的方法，基本确认了程序的问题，质问开发后，他不好意思的告诉我，io高是因为自己程序偷了懒，好在这次找到证据了，作为以后的分析案例</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（6） 💬（1）<div>实际生产环境中的进程更多，stress藏在ps中根本不容易发现，pstree的结果也非常大。老师有空讲讲如何找到这些异常进程的方法和灵感。</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（5） 💬（3）<div>execsnoop这个工具在centos里找不到，有类似的代替品吗</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/38/4c962666.jpg" width="30px"><span>小贝_No_7</span> 👍（4） 💬（1）<div>最后的perf -g有疑问。这里并没有展示出明显的stress占比较高的情况。相反是swapper较多, stress的占比其实在10%一下。请问这个怎么解释? 我看到底下也有其他朋友有类似的疑问但是没得到很好的解析。谢谢啦。  </div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（3） 💬（1）<div>execsnoop
这个工具没找到</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/77/22843055.jpg" width="30px"><span>kingkang</span> 👍（2） 💬（3）<div>倪老师你好，我自己用go写了一套微服务框架（基本网络架构是 一台http server+一台grpc server +三台mongodb 副本集群）；如果grpc server不调用mongodb 查询的话，qps能稳定在36000左右，而且压测的时候，grpc server 的cpu使用率大概在60%左右，平均负载最高不会超过2.5（服务器都是四核8G的 ）。如果一旦调用了mongodb查询的话，cpu使用率基本都能达到95%，平均负载最高能到4.6，而qps也下降到了6k左右。两种情况的内存差别并不大，系统内存一直维持在800M上下。我用老师教的方法，mongol db  find方法cpu占用过高。这个方法并没办法做到进一步优化，请问老师我这个框架cpu使用率过高的情况是不是就没办法进一步优化了？另外就是，如果我在加一台grpc server,也就是http server 调用两个grpc server  对系统qps 增加并不大，这是为什么我一直想不明白？</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/57/3c/081b89ec.jpg" width="30px"><span>rm -rf 😊ི</span> 👍（2） 💬（1）<div>想请教一下老师，running进程突然变多，突然变少的，是什么情况，主要是短时进程的问题吗？</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2a/6d/0e436c1c.jpg" width="30px"><span>梦回汉唐</span> 👍（2） 💬（1）<div>查看瞬时进程，还可以用这个方法：

watch -n 1 -d &quot;ps -A -ostat,pid,ppid,cmd | grep -i &#39;^r&#39; | grep -v ps&quot;

下面是输出：

Every 1.0s: ps -A -ostat,pid,ppid,cmd | grep -i &#39;^r&#39; | grep -v ps       Wed Mar 20 02:39:50 2019

R+   13308 13307 &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1
R+   13313 13312 &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1
R+   13314 13311 &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1
R+   13319 13317 &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1
R+   13320 13318 &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1</div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b7/e0/5fdb9fc2.jpg" width="30px"><span>刘韦菠</span> 👍（2） 💬（1）<div>我的perf record 里面 random 函数调用占比不是最高的, 最高的是一个叫做hoghdd 的函数, 这个函数里面包含了一些内存段错误和换页的函数. 这个是为什么呢? 
我的机器是mac, 然后这个批次的mac ssd 性能有问题, 官方曾经给我发过返厂维修的通知邮件, 但是因为是公司的电脑, 所以我并没有弄去维修. hog hdd 是不是 占用hdd硬盘的意思呢?

-   57.30%     0.03%  stress           stress                    [.] main                                                                                                                                  ▒
   - main                                                                                                                                                                                                  ▒
      + 21.77% hoghdd                                                                                                                                                                                      ▒
      + 16.12% random_r                                                                                                                                                                                    ▒
      + 12.09% random                                                                                                                                                                                      ▒</div>2019-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/98/b519a361.jpg" width="30px"><span>Wind～</span> 👍（2） 💬（1）<div>之前给老师留言的问题已经自己搞定了，在后续的实验中我发现我的实验有些不太一样，还是希望老师看到后可以再指点一二，老师的ps和pidstat都没有输出，而我的则是有输出，但是分析的结果导向是一致的——线索都指向了stress

----通过pidstat
[wind@aaa ~]$ pidstat -p 39945
Linux 3.10.0-862.el7.x86_64 (aaa)     2019年01月14日     _x86_64_    (1 CPU)

06时31分09秒   UID       PID    %usr %system  %guest    %CPU   CPU  Command
06时31分09秒     1     89962    0.00    0.00    0.00    0.00     0  php-fpm
[wind@aaa ~]$ 

----通过ps aux
[wind@aaa ~]$ ps aux | grep 39945
bin       39945  1.3  0.7 336684  7688 pts&#47;2    S+   06:36   0:01 php-fpm: pool www
wind      54077  0.0  0.0 112704   664 pts&#47;3    R+   06:38   0:00 grep --color=auto 39945
[wind@aaa ~]$ 

----再通过ps -efl
[wind@aaa ~]$ ps -lef | grep 121267
0 S bin       58233 121267  0  80   0 -  1070 do_wai 07:00 pts&#47;2    00:00:00 sh -c &#47;usr&#47;local&#47;bin&#47;stress -t 1 -d 1 2&gt;&amp;1
0 S wind      58250  42935  0  80   0 - 28180 pipe_w 07:00 pts&#47;3    00:00:00 grep --color=auto 121267
5 S bin      121267  75443  1  80   0 - 84171 pipe_w 06:52 pts&#47;2    00:00:06 php-fpm: pool www

----但是我的实验中有些不同的地方是，php-fpm的京城并不会发生改变但是基本上都处于S状态很少会有R状态出现，但是如果出现R状态的话，那么在过0.5秒后，就必然会出现一个Z进程
----并且在后续的perf report 中占比最高的也没有random函数
-   66.20%     0.00%  stress           stress                          [.] 0x000000000000168d                                       ▒
   - 0x168d                                                                                                                         ▒
      - 5.49% 0x2f25                                                                                                                ▒
         - 3.75% 0xffffffffba116768                                                                                                 ▒
            - 3.74% 0xffffffffba11a925                                                                                              ▒
               - 2.94% 0xffffffffba11a597</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（2） 💬（1）<div>每天都在进步  看来得好好熟悉docker了  打卡打卡</div>2018-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（1）<div>这种实操案例真是太赞了。</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/22/b9eb397f.jpg" width="30px"><span>孙志博</span> 👍（1） 💬（1）<div>确实遇到了第1种情况的问题，使用了此解决方案，点赞</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/78/be/7bf3f1b0.jpg" width="30px"><span>Silver bullet</span> 👍（1） 💬（1）<div>老是您好 看了6篇文章学了不少工具  也跟着里面的案例联系了  但是有些不常用的工具容易忘  比如vmstat 前天学的 今天就忘了  有没有什么办法记住所学过的工具呢？</div>2019-04-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLDC4cj2XKjHPNdOiaZR6oxeO36umdW8cnuW0YfyKCfpia883ib4RheBicuL2TPhMY14HQ7e7Dl4Zvhd8w/132" width="30px"><span>Geek_32a1cf</span> 👍（1） 💬（1）<div>老师，有个疑问，咱们讨论的都是有问题导致了cpu使用率较高的情况，那怎么判断是程序本身调用就需要大量的耗费cpu（例如程序纯计算）还是说程序有问题才导致了cpu的升高呢</div>2019-03-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/S2RCl03ejxSqsShDO7uExD8AREBK5O4xroRXQMjBzFRtbEvcaGNKgIPlZJNBBa1C9QSXrhGFWtttukIAvrdoBQ/132" width="30px"><span>Geek_fce8cb</span> 👍（1） 💬（1）<div>老师，没太明白 这个分析app目录下调用了stress是啥意思，这不是用的ab命令测试的吗，怎么又扯上stress去了</div>2019-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/4e/2acbc3a8.jpg" width="30px"><span>vvsuperman</span> 👍（1） 💬（2）<div>登陆到docker环境中top看到的都是整个主机的信息，而不是docker自身的进程的信息，查看不到呀</div>2019-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c2/1f/343f2dec.jpg" width="30px"><span>9527</span> 👍（1） 💬（1）<div>如果是短时间内有大量进程在不断重启，每秒的fork调用应该很多，如果能监控到一段内都调用了哪些系统函数，同样的问题应该也能先出来吧，有这样的查看一段时间内系统函数调用情况的工具吗？</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/36/abe6d066.jpg" width="30px"><span>付盼星</span> 👍（1） 💬（1）<div>老师好，之前就遇到过一次短进程的问题导致cpu使用率过高，因为我们发布应用用的是容器，把重启策略设置为always，结果容器启动时候调用java -jar 启动应用，因为配置原因，无法启动，然后它就不停启动，现象是cpu使用率过高，好在用top能发现，毕竟进程一直在。不过还有个场景就比较难搞了，系统被入侵，不停启动进程消耗资源，你杀掉之后，它又启动新的进程，pid也不同，这种情况，有处理办法么？</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b1/4d/10c75b34.jpg" width="30px"><span>Johnson</span> 👍（1） 💬（1）<div>曾经碰到CPU利用率很高，也知道是nginx造成的，整个团队都在优化，效果不理想啊</div>2018-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e9/b2/6a9203b5.jpg" width="30px"><span>小苏</span> 👍（0） 💬（1）<div>老师我写了一个测试程序java的 (cpu密集型): 命令:top -g -p 27476
    while (true) {
         Math.pow(RandomUtils.nextInt(100), RandomUtils.nextInt(100));
     }
cpu升上来了但是并没有明确的显示是由于计算次方也就是pow方法造成的
接下来我改如何用 perf  定位
+   67.60%     0.00%  perf-27476.map      [.] 0x00007f8de749930c                                                                                                                                           ▒
-   67.27%     0.90%  libjvm.so           [.] JVM_GetStackTraceElement                                                                                                                                     ▒
   - 11.07% JVM_GetStackTraceElement                                                                                                                                                                       ▒
      - 15.16% java_lang_Throwable::get_stack_trace_element                                                                                                                                                ▒
         - 23.20% java_lang_StackTraceElement::create                                                                                                                                                      ▒
            - 14.01% StringTable::intern                                                                                                                                                                   ▒
               + 9.21% StringTable::intern                                                                                                                                                                 ▒
                 3.22% UTF8::convert_to_unicode                                                                                                                                                            ▒
                 3.01% UTF8::unicode_length</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ec/8f/8299495a.jpg" width="30px"><span>少盐</span> 👍（0） 💬（1）<div>docker build -t feisky&#47;nginx:cpu -f Dockerfile.nginx .
Sending build context to Docker daemon  32.26kB
Step 1&#47;4 : FROM nginx
Get https:&#47;&#47;registry-1.docker.io&#47;v2&#47;: net&#47;http: TLS handshake timeout
Makefile:8: recipe for target &#39;build&#39; failed
make: *** [build] Error 1
为什么输入make build 出现这个错误</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/b7/d7377f0c.jpg" width="30px"><span>Vincent</span> 👍（0） 💬（1）<div>使用top时，如何只展示R状态的进程，或者按照状态排序也可以~</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/1e/bdc4f811.jpg" width="30px"><span>强友谅</span> 👍（0） 💬（1）<div>在做相关的实验，由于环境中存在代理。
1.make build报错无法拉取镜像Get https:&#47;&#47;registry-1.docker.io&#47;v2&#47;: dial tcp: lookup registry-1.docker.io on 127.0.0.53:53: read udp 127.0.0.1:40789-&gt;127.0.0.53:53: i&#47;o timeout
2.在vim &#47;lib&#47;systemd&#47;system&#47;docker.service中添加仍报该错误。
3.&#47;etc&#47;profile中通过export http_proxy=http:&#47;&#47;172.16.10.12:808
export https_proxy=http:&#47;&#47;172.16.10.12:808配置代理 ，wget www.baidu.com验证可通

4.一直纠结在我这种网络情况下如何欢畅的拖取镜像，官方文档也参照设置过，daocloud加速器也有尝试。
问题：请问现在的问题是docker仓库的问题，还是网络配置仍有问题？期望大牛的回答^_^
</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3f/5e/2fa1377d.jpg" width="30px"><span>Ignacio</span> 👍（0） 💬（1）<div>[root@rhel7 ~]# docker logs 6117d3a95fda
[15-Mar-2019 12:33:07] ERROR: failed to create new listening socket: socket(): Address family not supported by protocol (97)
[15-Mar-2019 12:33:07] ERROR: FPM initialization failed
镜像都可以拉下来，nginx可以启动，php-fpm起不来。。</div>2019-03-15</li><br/>
</ul>