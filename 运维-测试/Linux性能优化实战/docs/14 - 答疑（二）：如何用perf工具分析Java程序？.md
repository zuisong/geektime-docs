你好，我是倪朋飞。

今天是我们第二期答疑，这期答疑的主题是我们多次用到的perf工具，内容主要包括前面案例中， perf 使用方法的各种疑问。

perf 在性能分析中非常有效，是我们每个人都需要掌握的核心工具。perf 的使用方法也很丰富，不过不用担心，目前你只要会用 perf record 和 perf report 就够了。而对于 perf 显示的调用栈中的某些内核符号，如果你不理解也没有关系，可以暂时跳过，并不影响我们的分析。

同样的，为了便于你学习理解，它们并不是严格按照文章顺序排列的，如果你需要回顾内容原文，可以扫描每个问题右下方的二维码查看。

## 问题 1： 使用 perf 工具时，看到的是16进制地址而不是函数名

![](https://static001.geekbang.org/resource/image/94/69/94f67501d5be157a25a26d852b8c2869.png?wh=750%2A1782)

这也是留言比较多的一个问题，在 CentOS 系统中，使用 perf 工具看不到函数名，只能看到一些16进制格式的函数地址。

其实，只要你观察一下perf界面最下面的那一行，就会发现一个警告信息：

```
Failed to open /opt/bitnami/php/lib/php/extensions/opcache.so, continuing without symbols
```

这说明，perf 找不到待分析进程依赖的库。当然，实际上这个案例中有很多依赖库都找不到，只不过，perf工具本身只在最后一行显示警告信息，所以你只能看到这一条警告。

这个问题，其实也是在分析Docker容器应用时，我们经常碰到的一个问题，因为容器应用依赖的库都在镜像里面。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（19） 💬（1）<div>[D14打卡]
很赞同老师的观点:
&quot;任何东西的第一遍学习有不懂的地方很正常，忍住恐惧别放弃，继续往后走，前面很多问题可能会一并解决掉 ，再看第二遍、第三遍就更轻松了。&quot;
我好像很早就这样实践了: 第一遍不管看不看得懂,先尽量细看. 再特意过一段时间回头重新学一遍,除了能掌握更多的东西,还能体会到&quot;温故而知新&quot;的感觉.
----------------------------
现在就是&quot;师傅领进门,修行看个人.&quot;
&quot;先从最基本的原理开始，掌握性能分析的思路，然后再逐步深入，探究细节&quot;
----------------------------
自从学了专栏,越来越觉得自己的&lt;英语&gt;该好好补补了,深感能力不足啊.
那么多好的资源,一手资料几乎都是英文的,看不懂真是可惜了!</div>2018-12-21</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（13） 💬（2）<div>打卡day15
perf report中关于swapper的内容，后面我也去查了，才发现是自己理解有误，感谢老师指出，这里的swapper不是内存概念的swap，而是cpu空闲时执行的一个默认调用
要啃啃《性能之巅：洞悉系统、企业与云计算》了，作者博客http:&#47;&#47;www.brendangregg.com&#47;
请教老师，理解内核这块，有合适的书推荐么？我查了下，看了下目录，感觉《Linux内核设计与实现》可能比较适合，其他的如《Linux内核情景分析》，《深入理解Linux内核》怎么样？</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/04/ae/0118c132.jpg" width="30px"><span>辉晖</span> 👍（2） 💬（1）<div>对于问题1，使用方法4还是看不到函数名，只能看到一些 16 进制格式的函数地址

在载入perf.data过程不断出现提示：Failed to open ***, continuing without symbols
载入完成后，perf 界面最下面的那一行警告信息是：Cannot load tips.txt file, please install perf!</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/b8/43a4c2c0.jpg" width="30px"><span>子轩Zixuan</span> 👍（2） 💬（1）<div>趁周末跟上了老师的脚步，老师讲解的很好，感谢！另外我注意到老师在专栏里的实例都是现场调试，但是我遇到过实际情况需要尽快恢复服务，先把代码还原重新发布保证服务可用，只留下一台保留问题现场的机器，但是已经不接受请求了，像这种情况除了事先监控以外，还有别的方案能定位问题吗？</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/61/34a0da09.jpg" width="30px"><span>Griffin</span> 👍（2） 💬（1）<div>终于赶上了，倪老师能不能讲讲网络问题应该怎么排查呀，最近老是被docker，docker swarm的container寻址困扰。</div>2018-12-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO7rmfnq3iaicssF1Vl2lJicYl4C1Lb5q5vIJQwXQ2mbiaPpceeRibwoMAcDcLm5zFk1ZryicyRCVpNibfg/132" width="30px"><span>郡主秋</span> 👍（1） 💬（2）<div>老师，我的在centos7上用perf分析宿主机上的应用也是显示16进制地址，没有函数名 ，这种怎么处理呢
</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/c8/bed1e08a.jpg" width="30px"><span>辣椒</span> 👍（1） 💬（1）<div>老师，我把perf.data拷贝进容器，然后在容器中按照提示安装了perf, 再执行perf_4.9 report时报以下信息：
Kernel address maps (&#47;proc&#47;{kallsyms,modules}) were restricted.   
Check &#47;proc&#47;sys&#47;kernel&#47;kptr_restrict before running &#39;perf record&#39;
As no suitable kallsyms nor vmlinux was found, kernel samples     
can&#39;t be resolved.                                             
Samples in kernel modules can&#39;t be resolved as well.              
  xPress any key...  

我本身的机器是centos7.2. 请老师提示一下解决的思路，谢谢！

                                                </div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f4/b8/43a4c2c0.jpg" width="30px"><span>子轩Zixuan</span> 👍（1） 💬（1）<div>感谢老师耐心回复，接着线上定位问题想问下，如果要事先做好监控系统，一般需要做到什么程度？目前只有阿里云的监控感觉不够用</div>2018-12-25</li><br/><li><img src="" width="30px"><span>无名老卒</span> 👍（1） 💬（1）<div>全部刷完了，把各个CPU容易出现问题的情况基本上都写清楚了，而且都有详细的测试用例，除了软中断那个需要SYN攻击之外，其他的测试用例都一五一十的都做过了，受益良多。我有以下疑问，希望老师可以解答下：
1、软中断老师是用SYN攻击的方式来讲解这部分的实例的，那还有没有其他典型的软中断的案例呢？
2、硬中断的实例老师没有讲，可以补一篇吗？
3、老师所讲的实例，都是单一模式的，在实际的生产环境下，情况要复杂很多，老师能再讲一下印象最深刻的实际情况吗？

另外，我有一个小建议，老师的案例都是用docker来搭建环境的，在一个用例要多次下载不同的image，但其实这些image只是里面的测试用例变了，所以可以先下载file文件，使用docker -v挂载的方式进行测试。这样可以大大减少下载镜像的时间。如下，就是使用docker run -v &#47;usr&#47;local&#47;src&#47;app-fix2:&#47;app --privileged --name app-fix -d feisky&#47;app:iowait 来运行的镜像。
```
[root@linjx src]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                        PORTS               NAMES
0ecb229f87e4        feisky&#47;app:iowait   &quot;&#47;app&quot;              3 minutes ago       Up 3 minutes                                      app-fix
a251996e0d60        feisky&#47;app:iowait   &quot;&#47;app&quot;              5 hours ago         Exited (137) 20 minutes ago                       app
```</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（1） 💬（1）<div>老师，有个问题，如果iowait过高，导致系统卡死，ssh几乎操作不动，怎么快速找出进程杀掉，iotop敲了20分钟没响应</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c4/fd/2549489e.jpg" width="30px"><span>叶先生</span> 👍（0） 💬（1）<div>老师你好：
我在学习使用perf 分析打包docker 下的.net core应用时，有个问题困扰了很久 在采用你的第四条建议 外面使用 perf record 记录然后进入容器分析，一直看不到.net core 函数名 网上找了一些资料比如在dock镜像打包的时候 export COMPlus_PerfMapEnabled=1，还是无法看到，不知道哪里出了问题 </div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/10/8ef02bff.jpg" width="30px"><span>一木成舟🌊</span> 👍（0） 💬（1）<div>我是在一台机器上，report record和perf reprot的，report函数名是16进制的，看各位同学的留言是在centos下才会出现。
但是我是Ubuntu 14.04.2 LTS。也是出现这种问题了。按照老师上面的步骤，
$ apt-get install -y linux-tools-common linux-tools-generic linux-tools-$(uname -r)）
安装后，还是不行，实在让人费解。</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/54/34273afa.jpg" width="30px"><span>韦伯</span> 👍（0） 💬（1）<div>老师，我用的是ubuntu16.04，内核版本4.4.0.117，安装perf时提示需要安装linux-4.4.0.117-generic，但是安装上述包时又找不到。需要升级内核版本解决吗？有没有其他方式可以解决呢</div>2019-03-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJLm7IbU8V19ENfAnAaeibr4X5zQDw2yI8pHy1xtRgVC7S0YjdqI6jKlcQ0ueicuCaIkebSTNelRibsA/132" width="30px"><span>全大神啊</span> 👍（0） 💬（2）<div>花了两天时间看完了CPU部分，收获良多，以前不怎么用的命令，看了老师的文章了解知道了工具的作用，以及原理，大爱~接下来内存部分-.-。</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/d8/6feb6935.jpg" width="30px"><span>刘飞</span> 👍（0） 💬（1）<div>给大家分享下mac 跑docker时如果安装perf工具：
首先启动容器时，要增加启动参数--privileged，否则后续操作提示没权限
安装工具：apt-get install linux-source
可以在&#47;usr&#47;src下找到压缩宝，解压，进入tools&#47;perf，然后make&amp;&amp;make install进行编译
把编译生成的perf拷贝到&#47;usr&#47;bin下
注意：如果使用的时候不显示调用函数名，需要回到编译脚本那一步，仔细看报警信息缺哪些依赖的包，都下载下来重新编译。</div>2019-01-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（0） 💬（1）<div>docker符号找不到的问题，文章里已经给了几个方法，我想问的是，是不是可以直接把docker的符号下载下来？从宿主直接看函数调用栈？ docker不会像java一样，在java代码层面后，从系统层面(c语言层面)很难查问题？</div>2018-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bd/b5/5bcefe24.jpg" width="30px"><span>苹果彩票官网</span> 👍（0） 💬（1）<div>请教个问题，我们线上有台机器a上部署了一个java应用，通过java来调用外网的一个http服务，但是速度特别慢，但是在机器上通过curl访问就特别快，我们怀疑是在sockey层面可能存在什么问题，请问如何排查呢？</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（0） 💬（1）<div>我的centos7 安装的yum安装的perf 3.10的也是只有地址，看不到函数名。</div>2018-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（1）<div>英文是硬伤</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8c/49/791d0f5e.jpg" width="30px"><span>clivexiang</span> 👍（0） 💬（1）<div>flag</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/92/01/c723d180.jpg" width="30px"><span>饼子</span> 👍（0） 💬（1）<div>打卡学习</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/ee/e3c4c9b3.jpg" width="30px"><span>Cranliu</span> 👍（0） 💬（1）<div>近期准备把常用的工具man一把，养成习惯。</div>2018-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/74/ad/771d2646.jpg" width="30px"><span>赵奇彬</span> 👍（3） 💬（1）<div>perf生成的数据可以用火焰图显示更加直观</div>2020-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（2） 💬（0）<div>任何东西的第一遍学习有不懂的地方很正常，忍住恐惧别放弃，继续往后走，前面很多问题可能会一并解决掉，再看第二遍、第三遍就更轻松了。
------------------------------
深感共鸣，以前学习总是贪大求全，总以为一遍能看懂的决不花两遍，后来发现真实能理解起码需要2遍以上，看来基本上大多数人都是这个样子。</div>2020-07-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK0K9AM6xxDzVV6pF66jyus5NuuxZzT9icad8AQDMKibwUOy3UnoZIZdyKIKd9sA06rgFnIWwiakSeOQ/132" width="30px"><span>斑马Z</span> 👍（2） 💬（0）<div>关于本章中遇到的工具在centos系统下的安装。
yum install sysstat pstree psmisc
以及hping3的安装参考
https:&#47;&#47;www.cnblogs.com&#47;shuter&#47;p&#47;11430876.html
如果yum的数据db损坏，可能需要clean 和 makecache一下再进行
docker镜像中 apt-get update &amp;&amp; apt-get install -y linux-perf linux-tools procps

</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（2） 💬（2）<div>准备把专栏做成思维导图，方面查看。</div>2020-03-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI6uq4ea3WJciatibTOIQ0icOrjA2qpCCicT3Vgqf1FxSK8zfcmbA3TCfoiayZP4xrkDr0zoGIdEbpVjlQ/132" width="30px"><span>Geek_809e89</span> 👍（1） 💬（0）<div>使用第三种方法还是有16进制内容输入  并且只看到了add_function函数没有看到sqrt函数      至于第四种方法安装perf失败了。。。apt-get install -y linux-perf  报错Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package linux-perf   尝试了好多方法都没有成功</div>2024-10-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLHS9BjwOgkqV1NSmNRFxUC6KU0DibS75f00GhMWx4s5OYLryibaNDoJ1tZAFRaHJ7jSZXA4pNumraQ/132" width="30px"><span>Lake</span> 👍（1） 💬（1）<div>第二遍了，把第一遍看没做的实验跟着做，顺便开始整理笔记了</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/b7/f053eda7.jpg" width="30px"><span>康熙</span> 👍（1） 💬（0）<div>《Systems Performance: Enterprise and the Cloud》这本书刚出了第二版，新鲜出炉的：http:&#47;&#47;www.brendangregg.com&#47;systems-performance-2nd-edition-book.html</div>2020-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/36/e2/d235c81c.jpg" width="30px"><span>kino</span> 👍（0） 💬（0）<div>专栏买晚了，不知道老师还会不会回, 这段java代码，用 perf 只能分析到 run 方法占用cpu多吗，还能分析到run方法里面嘛, 这个结果似乎和 jstack 生成的都一样

public class CpuIntensiveTask {
  public static void main(String[] args) {
    int numThreads = 4;
    for (int i = 0; i &lt; numThreads; i++) {
      new Thread(new CpuTask()).start();
    }
  }
  static class CpuTask implements Runnable {
    @Override
    public void run() {
       while (true) {
          long sum = 0;
          for (long i = 0; i &lt; Long.MAX_VALUE; i++) {
             sum += i;
             if (i % 10000000 == 0) { 
                break;
             }
        }
     }
   }
}

生成火焰图也只到了 run 方法
perf record -F 99 -a -g -p 14869 -- sleep 10; .&#47;jmaps
perf script | FlameGraph&#47;stackcollapse-perf.pl --pid | FlameGraph&#47;flamegraph.pl --color=java --hash &gt; flamegraph.svg

perf report -i &#47;tmp&#47;perf-14869.data 的部分内容:
25.63%     0.00%  Thread-1  libjvm.so          [.] JavaCalls::call_helper(JavaValue*, methodHandle*, JavaCallArguments*, Thread*)
25.63%    25.45%  Thread-1  [JIT] tid 14869    [.] LCpuIntensiveTask$CpuTask;::run
  25.45% 0x789518929c3c
    0x78951889ca94
    java_start(Thread*)
    JavaThread::thread_main_inner()
    thread_entry(JavaThread*, Thread*)
    JavaCalls::call_virtual(JavaValue*, Handle, KlassHandle, Symbol*, Symbol*, Thread*)
    JavaCalls::call_virtual(JavaValue*, KlassHandle, Symbol*, Symbol*, JavaCallArguments*, Thread*)
    JavaCalls::call_helper(JavaValue*, methodHandle*, JavaCallArguments*, Thread*)
    call_stub
    LCpuIntensiveTask$CpuTask;::run

jstask 部分内容
&quot;Thread-1&quot; #9 prio=5 os_prio=0 tid=0x00007895100ee800 nid=0x3a22 runnable [0x00007894fb9fd000]
  java.lang.Thread.State: RUNNABLE
     at CpuIntensiveTask$CpuTask.run(CpuIntensiveTask.java:17)
     at java.lang.Thread.run(Thread.java:750)
</div>2024-11-14</li><br/>
</ul>