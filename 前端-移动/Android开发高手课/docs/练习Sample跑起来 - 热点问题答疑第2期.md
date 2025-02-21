你好，我是孙鹏飞。今天我们基于[专栏第5期](http://time.geekbang.org/column/article/71982)的练习Sample以及热点问题，我来给你做答疑。有关上一期答疑，你可以点击[这里](http://time.geekbang.org/column/article/73068)查看。

为了让同学们可以进行更多的实践，专栏第5期Sample采用了让你自己实现部分功能的形式，希望可以让你把专栏里讲的原理可以真正用起来。

前面几期已经有同学通过Pull request提交了练习作业，这里要给每位参与练习、提交作业的同学点个赞。

第5期的作业是根据系统源码来完成一个CPU数据的采集工具，并且在结尾我们提供了一个案例让你进行分析。我已经将例子的实现提交到了[GitHub](http://github.com/AndroidAdvanceWithGeektime/Chapter05)上，你可以参考一下。

在文中提到，“当发生ANR的时候，Android系统会打印CPU相关的信息到日志中，使用的是[ProcessCpuTracker.java](http://androidxref.com/9.0.0_r3/xref/frameworks/base/core/java/com/android/internal/os/ProcessCpuTracker.java)”。ProcessCpuTracker的实现主要依赖于Linux里的/proc伪文件系统（in-memory pseudo-file system），主要使用到了/proc/stat、/proc/loadavg、/proc/\[pid]/stat、/proc/\[pid]/task相关的文件来读取数据。在Linux中有很多程序都依赖/proc下的数据，比如top、netstat、ifconfig等，Android里常用的procrank、librank、procmem等也都以此作为数据来源。关于/proc目录的结构在Linux Man Pages里有很详细的说明，在《Linux/Unix系统编程手册》这本书里，也有相关的中文说明。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N0NACGUr8dNAbN6BdiagPHBaB0EnyDsI9zWpwJteqTY38apOEnTOA7JkBAQnzYKJBgxu3Q8YMUILwLAB6camn4w/132" width="30px"><span>Swing</span> 👍（1） 💬（2）<div>鹏飞模拟的这个例子，显示的都是minor fault，所以，而没有 major的统计，是因为文件系统的cache，还在等待批量写入磁盘吗？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/45/b2/ee0cfc12.jpg" width="30px"><span>Seven</span> 👍（1） 💬（0）<div>作业做完才发现鹏飞老师已经上传例子了。我只是参考了ProcessCpuTracker.java得到的数据是通过哪几个数据计算出来的，并没有参考上面的算法，因为开始兴高采烈的把ProcessCpuTracker.java的代码复制到项目中，项目一堆红线在我的脑门挂上了几条黑线。。。那时候就决定自己写，没想到确实可以利用ProcessCpuTracker.java里面的源码。
看到这句话“在不同的 Linux 内核中，该目录下的内容可能会有所不同”，才知道怪不得每个文档说的参数的含义不一样，原来内核不同。
想知道kernel这个数据代表什么意思，是怎么计算的</div>2018-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/48/03abbbd1.jpg" width="30px"><span>瑞</span> 👍（0） 💬（0）<div>那这种需要怎么解决呢？</div>2019-06-03</li><br/>
</ul>