你好，我是LMOS。

前面的课程里，我们学习了IO Cache、IO调度和IO管理的相关知识，但怎样度量和检测一个应用使用IO的情况呢？我们今天就来聊聊这个问题。

这节课我想带你认识两大监控IO操作的神器——iostat与iotop，让你掌握安装、使用它们的方法以及它们的工作原理。在Linux系统上，iostat和iotop这两个IO数据工具非常常用。它们都是性能分析领域中不可缺少的工具性软件，也经常被Linux网络服务器运维人员，用于分析某些服务器的IO类性能与故障。

### 安装iostat与iotop

在带你安装这两个工具之前，我先简单介绍下这两个工具的功能。iostat可以用来分析Linux系统整体IO的使用情况；而iotop作为iostat增强版和功能升级版，可以分析Linux系统每一个进程使用IO的情况。

在我们日常使用的Linux发行版中，是不包含iostat与iotop两个IO工具软件包的，需要我们自行安装它们才可以使用。

各大Linux发行版软件包管理方法并不统一，导致安装应用软件的方式不尽相同。考虑到Ubuntu、Deepin都是基于Debain开发的，所以我们这里**以Debain系的Linux发行版为例**进行操作。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题：
Q1：iostat显示的“4 CPU”是4个物理CPU还是四个核？
文中的例子，在老师的电脑上，用iostat显示的是“4 CPU”，这应该是一个CPU的四个核吧。
Q2：“合并”的读&#47;写请求是什么意思？ 
Q3：sda和sdb是两个硬盘吗？ 还是一个硬盘的两个不同分区？
文中例子中，老师电脑上显示了sda和sdb，它们是两个硬盘吗？ 还是一个硬盘的两个不同分区？（一般认为电脑只会有一个硬盘，我猜想老师的电脑也是一个硬盘）
Q4：iostat是统计多长时间内的数值？
既然是统计，需要有一个时间段的概念。Iostat不带任何选项时，统计时长是多少？</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（2） 💬（1）<div>iotop需要启动su，会显示root下的详单，更详细的啊
但缺点也明显，启动完需要关闭terminal然后再重启才行！</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/c3/2c53acd7.jpg" width="30px"><span>雄鹰</span> 👍（0） 💬（0）<div>请教一个iostat统计时，列数的排列顺序会变化，有什么参数可以固定列数的显示排列顺序吗？</div>2023-04-24</li><br/>
</ul>