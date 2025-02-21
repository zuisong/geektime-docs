你好，我是朱晔。今天，我要和你分享的内容是分析定位Java问题常用的一些工具。

到这里，我们的课程更新17讲了，已经更新过半了。在学习过程中，你会发现我在介绍各种坑的时候，并不是直接给出问题的结论，而是通过工具来亲眼看到问题。

为什么这么做呢？因为我始终认为，遇到问题尽量不要去猜，一定要眼见为实。只有通过日志、监控或工具真正看到问题，然后再回到代码中进行比对确认，我们才能认为是找到了根本原因。

你可能一开始会比较畏惧使用复杂的工具去排查问题，又或者是打开了工具感觉无从下手，但是随着实践越来越多，对Java程序和各种框架的运作越来越熟悉，你会发现使用这些工具越来越顺手。

其实呢，工具只是我们定位问题的手段，要用好工具主要还是得对程序本身的运作有大概的认识，这需要长期的积累。

因此，我会通过两篇加餐，和你分享4个案例，分别展示使用JDK自带的工具来排查JVM参数配置问题、使用Wireshark来分析网络问题、通过MAT来分析内存问题，以及使用Arthas来分析CPU使用高的问题。这些案例也只是冰山一角，你可以自己再通过些例子进一步学习和探索。

在今天这篇加餐中，我们就先学习下如何使用JDK自带工具、Wireshark来分析和定位Java程序的问题吧。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（24） 💬（1）<div>1、jmap -dump是会dump所有的对象，不关心是否可达；jmap -dump:live只会dump存活的对象，即可以从GcRoot可达的对象。测试是在循环中，一直创建对象，然后休眠1s，dump2次，发现创建对象的个数不同。</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（6） 💬（2）<div>老师，你让我这个Java重新整理了方向，这才是 Java 更高层次需要掌握的东西，不然平时只知道写代码，遇到问题只会重启的话，对自己能力的提升实在是太慢了。

Java 的世界，还是离不开 JVM的判断。Wireshark 原来还可以分析 MySQL 相关，以前一直觉得只能网络抓包呢，哈哈</div>2020-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/79/673f4268.jpg" width="30px"><span>小杰</span> 👍（6） 💬（1）<div>老师现在特别火的阿里定位问题的工具Arthas  是不是都是拿jvm工具实现的呢，感觉很强大</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（5） 💬（1）<div>墙裂建议收藏，总有一天用得着。</div>2020-04-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（4） 💬（2）<div>-XX:ThreadStackSize=256k 实际效果是256M
-Xss:256k 实际效果是256k
官方文档提示这两个参数效果等同，都是byte为单位
https:&#47;&#47;docs.oracle.com&#47;javase&#47;8&#47;docs&#47;technotes&#47;tools&#47;unix&#47;java.html#BABHDABI</div>2020-04-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（3） 💬（4）<div>老师，你的第一个演示我这儿直接就被杀掉了
 java -jar target&#47;java-common-mistakes-0.0.1-SNAPSHOT.jar -Xms1g -Xmx1g
 jps 正常
jinfo $pid
提示：Error attaching to process ： Can&#39;t attach symbolicator to the process
发现进程已经被kill掉</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/27/2a/a914cd3f.jpg" width="30px"><span>若镜</span> 👍（2） 💬（1）<div>作为同样的一个15years+的programmer 不得不说 老师分享的足够干货 多谢。</div>2020-10-23</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（2） 💬（1）<div>重新认识用Wireshark分析问题，谢谢老师</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e9/d8/026493cc.jpg" width="30px"><span>vivi</span> 👍（2） 💬（2）<div>jmap -dump是输出堆中所有对象  jmap -dump:live是输出堆中所有活着的对象  而且jmap -dump:live会触发gc  线上使用要注意这个</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/49/0b9ffc8e.jpg" width="30px"><span>刘大明</span> 👍（2） 💬（1）<div>这篇定位java问题的文章,真的是打开了新天地.以前重来没有关注过jvm相关的信息,这次是开了眼界.</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/0d/0e65dee6.jpg" width="30px"><span>FelixFly</span> 👍（1） 💬（1）<div>老师，咨询一下Full GC 基本 10 秒一次这个结论是怎么总结出来的？Full GC一般控制在多少秒一次比较好？</div>2020-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/72/70190bc1.jpg" width="30px"><span>子不语</span> 👍（1） 💬（2）<div>老师好，第一个例子，启动 10 个死循环的线程，每个线程分配一个 10MB 左右的字符串，然后休眠 10 秒，完整的代码能给下吗。或者能否把案例的代码都上传到github。</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e8/65/dd1c0d22.jpg" width="30px"><span>润欢➿</span> 👍（0） 💬（1）<div>老师课程真的很好，带我进入了新java领域。

感谢，每节课都有认真看。写md笔记。</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/79/01/e71510dc.jpg" width="30px"><span>hellojd</span> 👍（4） 💬（1）<div>连接mysql,可以指定固定端口？怎么设置？有啥意义？不太明白</div>2020-04-22</li><br/><li><img src="" width="30px"><span>不能忍的地精</span> 👍（3） 💬（0）<div>刚好最近在看JVM.昨天利用jvm的工具发现了生产OOM的原因,今天又补课了</div>2020-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（2） 💬（0）<div>期待下一篇加餐~</div>2020-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/e0/3db22579.jpg" width="30px"><span>技术骨干</span> 👍（2） 💬（0）<div>明天上班路上好好读</div>2020-04-22</li><br/><li><img src="" width="30px"><span>李恺</span> 👍（0） 💬（0）<div>集中回顾一遍排障工具！</div>2024-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（0） 💬（0）<div>
生产环境有一条简单的 SQL 查询(使用 mybatis 仅有 where 子句且表中数据不到两万)耗时接近 1 分钟，但在测试环境却秒出。百思不得其解。
</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/87/f5/c6d1ffed.jpg" width="30px"><span>时光之刃</span> 👍（0） 💬（0）<div>老师是一个实干家，期待有关源码分析的专栏</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/dd/19/45afa234.jpg" width="30px"><span>🐛🐛</span> 👍（0） 💬（0）<div>jinfo在jdk8下面会报错么</div>2020-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/9b/59776420.jpg" width="30px"><span>百威</span> 👍（0） 💬（0）<div>文中wireshark的mysql用不到线上服务中吧0.0</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7c/ce/376842fb.jpg" width="30px"><span>Corsica</span> 👍（0） 💬（0）<div>怎么想到用wireshark来分析Mysql问题的呢？</div>2020-06-25</li><br/>
</ul>