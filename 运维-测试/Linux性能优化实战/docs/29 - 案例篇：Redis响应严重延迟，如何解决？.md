你好，我是倪朋飞。

上一节，我们一起分析了一个基于 MySQL 的商品搜索案例，先来回顾一下。

在访问商品搜索接口时，我们发现接口的响应特别慢。通过对系统 CPU、内存和磁盘 I/O 等资源使用情况的分析，我们发现这时出现了磁盘的 I/O 瓶颈，并且正是案例应用导致的。

接着，我们借助 pidstat，发现罪魁祸首是 mysqld 进程。我们又通过 strace、lsof，找出了 mysqld 正在读的文件。根据文件的名字和路径，我们找出了 mysqld 正在操作的数据库和数据表。综合这些信息，我们猜测这是一个没利用索引导致的慢查询问题。

为了验证猜测，我们到 MySQL 命令行终端，使用数据库分析工具发现，案例应用访问的字段果然没有索引。既然猜测是正确的，那增加索引后，问题就自然解决了。

从这个案例你会发现，MySQL 的 MyISAM 引擎，主要依赖系统缓存加速磁盘 I/O 的访问。可如果系统中还有其他应用同时运行， MyISAM 引擎很难充分利用系统缓存。缓存可能会被其他应用程序占用，甚至被清理掉。

所以，一般我并不建议，把应用程序的性能优化完全建立在系统缓存上。最好能在应用程序的内部分配内存，构建完全自主控制的缓存；或者使用第三方的缓存应用，比如 Memcached、Redis 等。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/16/af/bada0f59.jpg" width="30px"><span>李博</span> 👍（56） 💬（5）<div>老师，有个问题咨询下，为什么top显示 iowait比较高，但是使用iostat却发现io的使用率并不高那？</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/b4/6892eabe.jpg" width="30px"><span>Geek_33409b</span> 👍（29） 💬（5）<div>打卡day30 
IO性能问题首先可以通过top 查看机器的整体负载情况，一般会出现CPU 的iowait 较高的现象
然后使用 pidstat -d 1 找到读写磁盘较高的进程
然后通过 strace -f -TT 进行跟踪，查看系统读写调用的频率和时间
通过lsof 找到 strace 中的文件描述符对应的文件 opensnoop可以找到对应的问题位置
推测 对应的问题，mysql 案例中的大量读，可能是因为没有建立索引导致的全表查询，从而形成了慢查询的现象。redis 中则是因为 备份文件设置的不合理导致的每次查询都会写磁盘。当然不同的问题还需要结合对应的情况进行分析
</div>2019-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/bc/6ccac4bb.jpg" width="30px"><span>武文文武</span> 👍（13） 💬（3）<div>老师您好，一直在听您的视频，发现您用了很多的小工具来检查系统性能指标，而我们公司使用nmon工具，就能一次性将几乎所有常用的指标全部获取到了，而且还能拿到历史数据，请问我们用nmon是否就能在大部分情况下取到了您说的top pidstat等工具呢，如果不可以那您能说说原因吗？非常感谢</div>2019-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/33/30fb3ac3.jpg" width="30px"><span>____的我</span> 👍（12） 💬（2）<div>前段时间刚找到一个由于内存数据被交换到swap文件中导致内存数据遍历效率变低的问题 问题定位过程是使用pidstat命令发现进程cpu使用率变低 mpstat命令观察到系统iowait升高 由此怀疑跟io有什么关系 perf命令观察发现内存数据遍历过程中swap相关调用时间占比有点异常 然后使用pidstat命令+r参数 也观察到进程在那段时间主缺页中断升高 由此确定问题

老师的课程非常有用 多多向您学习 希望老师能多分享一些定位网络延迟问题的方法 不仅仅局限在ping探测</div>2019-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/c5/aaacb98f.jpg" width="30px"><span>yungoo</span> 👍（11） 💬（1）<div>nsenter报了loadlocale.c assertion设置

export LC_ALL=C

即可</div>2019-03-17</li><br/><li><img src="" width="30px"><span>从远方过来</span> 👍（7） 💬（1）<div>老师，你这几篇文章大量使用了strace，它的负载不是很高么？在生产上可以使用么？</div>2020-07-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/j0gBKF8EKfQ4TjoSTeRPoWia56RMCevYDauMGS9iaw4TnpC0dp2Viaict75T8TebKzAcUruWiazkyiaCQPqKZxar2M6Q/132" width="30px"><span>利俊杰</span> 👍（5） 💬（1）<div>nsenter --target $PID -- lsof -i
执行失败，提示：loadlocale.c:130: _nl_intern_locale_data: Assertion `cnt &lt; (sizeof (_nl_value_type_LC_COLLATE) &#47; sizeof (_nl_value_type_LC_COLLATE[0]))&#39; failed
可以参考下https:&#47;&#47;stackoverflow.com&#47;questions&#47;37121895&#47;yocto-build-loadlocale-c-130
配置
LANG=&#47;usr&#47;lib&#47;locale&#47;en_US
</div>2019-01-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJKkThulMFj6MNsgk6Tps4Ll1pzrricPDqAyuFkmFYMDcPgUbGuUnMYACIICRTRPWLPtib2z6V6XdBg/132" width="30px"><span>开始懂了</span> 👍（3） 💬（1）<div> curl http:&#47;&#47;10.39.25.7:10000&#47;init&#47;get_cache
&lt;!DOCTYPE HTML PUBLIC &quot;-&#47;&#47;W3C&#47;&#47;DTD HTML 3.2 Final&#47;&#47;EN&quot;&gt;
&lt;title&gt;500 Internal Server Error&lt;&#47;title&gt;
&lt;h1&gt;Internal Server Error&lt;&#47;h1&gt;
&lt;p&gt;The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.&lt;&#47;p&gt;</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（2） 💬（1）<div>git clone https:&#47;&#47;github.com&#47;feiskyer&#47;linux-perf-examples&#47;tree&#47;master&#47;redis-slow
Initialized empty Git repository in &#47;root&#47;redis-slow&#47;.git&#47;
error: The requested URL returned error: 403 Forbidden while accessing https:&#47;&#47;github.com&#47;feiskyer&#47;linux-perf-examples&#47;tree&#47;master&#47;redis-slow&#47;info&#47;refs

代码怎么克隆不下来</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9c/47/50cf2cab.jpg" width="30px"><span>Chn.K</span> 👍（1） 💬（2）<div>请教个问题：我用iotop观测IO使用情况，发现某进程的DISK READ 和DISK WRITE都是0，但是IO已经到99.99%了，通过top&#47;iostat对cpu&#47;磁盘的使用情况进行观测，均未发现什么异常，这个是什么原因呢？
Total DISK READ :      18.14 M&#47;s | Total DISK WRITE :      31.59 M&#47;s
Actual DISK READ:      18.02 M&#47;s | Actual DISK WRITE:      15.60 M&#47;s
  PID  PRIO  USER     DISK READ  DISK WRITE  SWAPIN      IO    COMMAND
  148 be&#47;4 root        0.00 B&#47;s    0.00 B&#47;s  0.00 % 99.99 % [ksoftirqd&#47;17]
23655 be&#47;4 root        0.00 B&#47;s  988.19 K&#47;s  0.00 %  0.00 % .&#47;xxxx ..&#47;etc&#47;base.conf
17535 be&#47;4 root       18.14 M&#47;s   30.63 M&#47;s  0.00 %  0.00 % xxxx
</div>2019-02-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/xzHDjCSFicNY3MUMECtNz6sM8yDJhBoyGk5IRoOtUat6ZIkGzxjqEqwqKYWMD3GjehScKvMjicGOGDog5FF18oyg/132" width="30px"><span>李逍遥</span> 👍（1） 💬（1）<div>Device:         rrqm&#47;s   wrqm&#47;s     r&#47;s     w&#47;s    rkB&#47;s    wkB&#47;s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
vda               0.00   392.00    0.00 1103.00     0.00  5984.00    10.85     1.00    0.58    0.00    0.58   0.91 100.00
我这边 %util到了100%，说明磁盘有瓶颈了吗？（请求参数一致）
</div>2019-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（1）<div>[D29打卡]
感觉每次分析的套路都差不多.
1.用top查看指标,发现 [系统] 有i&#47;o瓶颈 或者 cpu瓶颈.
2.使用iostat辅助看下磁盘i&#47;o读写速度和大小等指标.
3.用pidstat判断是哪个 [进程] 导致的. 既可以看进程各线程的cpu中断数,也可以看磁盘io数.
4.用strace追踪进程及各线程的 [系统调用].(以前经常到这里就知道了是操作的什么文件)
5.继续用lsof查看该进程打开的 [文件] .linux下一切皆文件,则可以查看的东西就很多很多了.连进程保持的socket等信息也一目了然.
6.本例因为用到了容器,所以用到了nsenter进入容器的网络命名空间,查看对应的socket信息.
7.根据第4.5步获取的信息,找源码或看系统配置.确定问题,做出调整.然后收工.</div>2019-01-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJCscgdVibmoPyRLRaicvk6rjTJxePZ6VFHvGjUQvtfhCS6kO4OZ1AVibbhNGKlWZmpEFf2yA6ptsqHw/132" width="30px"><span>夹心面包</span> 👍（0） 💬（1）<div>想请问下老师,通过top观察下的iowait到达百分之多少才算磁盘瓶颈,有没有业界的统一标准,磁盘的util值肯定是100%,还是得考虑IOPS,只通过iowait判断行不行</div>2019-01-25</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（63） 💬（0）<div>打卡day30
io问题一般都是先top发展iowait比较高，然后iostat看是哪个进程比较高，然后再通过strace，lsof找出进程在读写的具体文件，然后对应的分析</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/64/ad837224.jpg" width="30px"><span>Christmas</span> 👍（18） 💬（0）<div>进程iowait高，磁盘iowait不高，说明是单个进程使用了一些blocking的磁盘打开方式，比如每次都fsync</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（0）<div>分析规律就是：
* 根据top发现cpu0的iowait偏高
* iostat -d -x 1观察系统磁盘IO情况有无异常
* pidstat -d 1观察进程的IO其概况
* 用 strace+lsof 组合：strace -f -T -tt -p pid  和  lsof -p pid观察系统调用情况定位磁盘IO发生的现场</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/d7/0b/e92b2c13.jpg" width="30px"><span>trprebel</span> 👍（2） 💬（1）<div>老师，过了这么长时间来提问不知道您是否还能看到，这个案例的问题我在学习过程中觉得分析过程有些蹊跷，当系统出现异常时
1、我们使用top命令发现cpu有一个核使用率非常高，然后有84.7%是iowait，这是我们得到的第一个线索
2、然后使用iostat，pidstat，lsof等工具查看，这些工具查看完，如您所说，只能说明有io操作，并不能说明是有io瓶颈，并且这些指标也没有跟第一个线索关联起来，或者相互佐证
3、最后我们通过猜测读请求里面不应该有大量写操作来确定写操作的异常，虽然说定位并解决了问题，但感觉解决方案与问题和线索并没有直接关系，实际生产环境中不可能只有读操作，也有不会有“读操作里面不应该有大量写操作”的推断，那如果生产环境中我们应该如何分析呢
感觉是不是应该继续从这两个方向继续分析
1、问题：RT时间过长，进程&#47;线程在干什么，导致一直无法响应
2、线索：是哪个进程&#47;线程导致iowait如此高，以及这个进程&#47;线程在做什么
最后才定位到redis的aof操作</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e6/ee/e3c4c9b3.jpg" width="30px"><span>Cranliu</span> 👍（2） 💬（0）<div>top、iostat、pidstat、strace，以及对应用程序的了解，MySQL、Redis本质上也是一款应用程序。</div>2019-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dc/22/bb8e93b4.jpg" width="30px"><span>晴天雨伞</span> 👍（1） 💬（0）<div>nsenter这个命令太棒了。</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/24/547439f1.jpg" width="30px"><span>ghostwritten</span> 👍（1） 💬（0）<div>top-------&gt;iowait
iostat -d -x 1-----&gt;w
pidstat  -d 1
strace -f -t -TT &lt;pid&gt;
lsof -p &lt;pid&gt;
nsenter --target $PID --net -- lsof -i
config set appendfsync everysec
python: 
redis_client.sadd(type_name, key[5:])   把 Redis 当成临时空间，用来存储查询过程中找到的数</div>2021-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bc/2c/963688bb.jpg" width="30px"><span>noisyes</span> 👍（1） 💬（1）<div>为什么磁盘性能没有达到性能瓶颈，接口返回得这么慢呢</div>2021-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a3/f5/458d277b.jpg" width="30px"><span>伟啊伟</span> 👍（1） 💬（1）<div>有个问题，生产环境中往往不可能只有一类操作。像文中发展cpu io都没问题的时候，如果不是提前知道应用应该只有读操作（生产不可能），如何能快速定位到可疑点呢？</div>2020-10-26</li><br/><li><img src="" width="30px"><span>Geek_b3b8da</span> 👍（0） 💬（0）<div>我发现除了排查网络，排查cpu、内存、io、套路就是打开top，然后去看哪些指标，然后通过排除法慢慢缩小范围定位到对应的进程，首先使用pstree看看那个程序的pid是父进程还是子进程，然后通过strace -T -f -tt -e trace=all -p 1779 -o error.txt 万能命令 查看进程的详细问题，如果显示失败，那么就是排查是不是短时进程，如果不是那么用perf来查看最后还是优化代码去</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/46/28/14ef7207.jpg" width="30px"><span>maple-0406</span> 👍（0） 💬（0）<div>1.寻找可疑点，需要使用类似TOP的命令，寻找相对可疑点。以io问题为例，通常表现为iowait高，cpu使用率正常，内存相对比较富裕。
2.确定可疑点后，使用iostat 查看哪个进程使用较高，但是iostat可能无法全部看完整（例如线程读写直接销毁）
3.接下来使用strace （注意使用-f参数，同时展示线程读写情况），lsof  查到具体读写的文件。
如需要进一步查看细节，opensnoop （open系统调用）nsenter（容器网络ns）</div>2022-07-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK009KMmXKFVSEdjicpDD4ick3NZpM3JdIUibWGB03lG6yicibad0tGmQD7E3DpZ0sVRenxWNfd7iaPdp7g/132" width="30px"><span>小小菜鸟</span> 👍（0） 💬（0）<div>整体思路
两种：1、从现象看本质：
先整体看系统资源使用，初步确定问题；
再次进一步，确定进程；
再确定线程或是函数，找出问题；
2、从本质推出现象，这一般通过有经验的代码走读或是评审，顺推；
我的理解不一定准确，只是个人意见。</div>2021-08-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK0K9AM6xxDzVV6pF66jyus5NuuxZzT9icad8AQDMKibwUOy3UnoZIZdyKIKd9sA06rgFnIWwiakSeOQ/132" width="30px"><span>斑马Z</span> 👍（0） 💬（2）<div>笔记含命令，字数太多，发不上来了，有一定疑问请老师答疑。
我的redis-server进程号23497
lsof -p 23497  之后有大量的
lsof: no pwd entry for UID 100
但是我的~ # cat &#47;etc&#47;passwd|grep 100
games:x:12:100:games:&#47;usr&#47;games:&#47;sbin&#47;nologin
存在uid为100的用户，我之后又 lsof -u games  ,这里有报错lsof: no pwd entry for UID  1337，这个uid为1337的我确实没有。
说的有点绕，总之请问老师报错lsof: no pwd entry for UID *** 为什么会出现？</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/4b/97926cba.jpg" width="30px"><span>Luciano李鑫</span> 👍（0） 💬（0）<div>可是我觉的一个基于redis请求200毫秒也慢了点</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/b5/663cde8b.jpg" width="30px"><span>cornor</span> 👍（0） 💬（0）<div>感谢 学到了一套查询问题的方式</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（0） 💬（0）<div>非常好的案例，还顺复习了 redis 知识。我的环境把初始缓存数据加到 10000 后，iowait 也不是很高...</div>2019-09-07</li><br/><li><img src="" width="30px"><span>如果</span> 👍（0） 💬（0）<div>DAY29，打卡</div>2019-03-14</li><br/>
</ul>