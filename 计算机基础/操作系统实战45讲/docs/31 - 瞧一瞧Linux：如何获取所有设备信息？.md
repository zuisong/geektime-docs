你好，我是LMOS。

前面我们已经完成了Cosmos的驱动设备的建立，还写好了一个真实的设备驱动。

今天，我们就来看看Linux是如何管理设备的。我们将从Linux如何组织设备开始，然后研究设备驱动相关的数据结构，最后我们还是要一起写一个Linux设备驱动实例，这样才能真正理解它。

## 感受一下Linux下的设备信息

Linux的设计哲学就是一切皆文件，各种设备在Linux系统下自然也是一个个文件。不过这个文件并不对应磁盘上的数据文件，而是对应着存在内存当中的设备文件。实际上，我们对设备文件进行操作，就等同于操作具体的设备。

既然我们了解万事万物，都是从最直观的感受开始的，想要理解Linux对设备的管理，自然也是同样的道理。那么Linux设备文件在哪个目录下呢？其实现在我们在/sys/bus目录下，就可以查看所有的设备了。

Linux用BUS（总线）组织设备和驱动，我们在/sys/bus目录下输入tree命令，就可以看到所有总线下的所有设备了，如下图所示。

![](https://static001.geekbang.org/resource/image/56/28/567588d1ca461ed56c4cd3447d9dff28.jpg?wh=990x1047 "Linux设备文件")

上图中，显示了部分Linux设备文件，有些设备文件是链接到其它目录下文件，这不是重点，重点是你要在心中有这个目录层次结构，即**总线目录下有设备目录，设备目录下是设备文件**。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（1） 💬（1）<div>以前作为使用者去写驱动，现在以提供者的角度去分析驱动，又来到了熟悉的file_operations结构了，写过简单的内核2.6 和 3.4版本的驱动，每个版本都稍有区别，盲猜这个是5版本的，毕竟有些陌生的函数，刚才看到了一个评论驱动是如何操作硬件的，来个最简单的按键驱动就知道了，这还没谈谈设备树，设备树也应该谈谈，到底是哪个大聪明想到的设备树</div>2022-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（10） 💬（1）<div>
关于驱动程序Demo
一、miscdrv是一个内核模块
1、四个操作函数，封装在file_operations结构中，包括：
misc_open在打开设备文件时执行
misc_release在关闭设备文件时执行
misc_read在读取设备时执行
misc_write在写入设备时执行
file_operations又被封装在miscdevice中，在注册设备时传入

2、devicesinfo_bus_match函数用于总线设备的过滤，被封装在bus_type结构中
bus_type描述了总线结构，在总线注册时传入

3、module_init和module_exit声明入口和出口函数：
miscdrv_init注册设备和总线，在安装内核模块时执行
miscdrv_exit反注册设备和总线，在卸载内核模块时执行

4、只有misc_read比较复杂：
A、通过注册时的devicesinfo_bus获取kset，枚举kset中的每一个kobj
B、对于每个kobj，通过container_of转换为subsys_private
C、对于每个subsys_private，枚举其bus中每个设备，并通过misc_find_match函数进行处理
D、misc_find_match会在kmsg中输出设备名称

二、app.c
就是打开设备，写一下，读一下，关闭设备，主要是触发设备输出

三、执行顺序，需要两个Terminal，T1和T2
1、T1：make
2、T1：sudo insmod miscdrv.ko
3、T2：sudo cat &#47;proc&#47;kmsg
4、T1：sudo .&#47;app
5、T2：ctrl+c
6、T1：sudo rmmod miscdrv.ko</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（10） 💬（1）<div>关于数据结构
一、目录组织相关结构
kobject结构表示sysfs一个目录或者文件节点，同时提供了引用计数或生命周期管理相关功能；
kset结构，可以看作一类特殊的kobject，可以作为kobject的集合；同时承担了发送用户消息的功能；

Linux通过kobject和 kset来组织sysfs下的目录结构。但两者之间关系，却并非简单的文件和目录的关系。每个kobject的父节点，需要通过parent和kset两个属性来决定：
A、无parent、无kset，则将在sysfs的根目录（即&#47;sys&#47;）下创建目录；
B、无parent、有kset，则将在kset下创建目录；并将kobj加入kset.list；
C、有parent、无kset，则将在parent下创建目录；
D、有parent、有kset，则将在parent下创建目录，并将kobj加入kset.list；

kobject和kset并不会单独被使用，而是嵌入到其他结构中发挥作用。

二、总线与设备结构
bus_type结构，表示一个总线，其中 subsys_private中包括了kset；
device结构，表示一个设备，包括驱动指针、总线指针和kobject；
device_driver结构，表示一个驱动，其中 driver_private包括了kobject；
上面说的kset和kobject的目录组织关系，起始就是存在于这些数据结构中的；
通过kset和kobject就可以实现总线查找、设备查找等功能；

三、初始化
全局kset指针devices_kset管理所有设备
全局kset指针bus_kset管理所有总线

初始化调用链路：
kernel_init-&gt;kernel_init_freeable-&gt;do_basic_setup-&gt;driver_init
-&gt;devices_init设备初始化
-&gt;buses_init总线初始化

四、设备功能函数调用
miscdevice结构，表示一个杂项设备；
其中 file_operations包含了全部功能函数指针；

以打开一个设备文件为例，其调用链路为：
filp_open-&gt;file_open_name-&gt;do_filp_open-&gt;path_openat-&gt;do_o_path-&gt;vfs_open-&gt;do_dentry_open
通过file_operations获取了open函数指针，并进行了调用</div>2021-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（6） 💬（2）<div>在Linux系统中，sudo可以获取超级用户的权利，它之后的命令可以在内核态下进行工作。
而加载miscdrv.ko模块和app测试都需要在内核态下进行。</div>2021-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（1）<div>加载内核模块，使用内核驱动，得 sudo 权限</div>2021-07-19</li><br/><li><img src="" width="30px"><span>Geek_Lawrence</span> 👍（1） 💬（1）<div>驱动程序仍然是“软件”部分，“软件”如何驱动“硬件”，这部分能否更细致点，想了解下驱动程序是如何连接硬件并且驱动硬件工作的，其更加底层的工作原理是什么呢？</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/18/93/a1bbda42.jpg" width="30px"><span>Zhang</span> 👍（0） 💬（1）<div>终于看到这了，看到曙光了感觉，打个卡，感觉今天课后作业简单了</div>2022-06-25</li><br/><li><img src="" width="30px"><span>Mingjie</span> 👍（0） 💬（2）<div>老师，HDMI驱动是属于哪类驱动设备？我觉得是块类型设备，不是有显存这个说法嘛，我想的对吗</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ef/fa/5e9f3dc9.jpg" width="30px"><span>驰往</span> 👍（0） 💬（1）<div>既陌生又熟悉的代码。曾几何时，大学的时候就是从platform device入手，深入学习驱动设备模型，然而由于工作环境，越工作越上层，最终没有踏入内核这片圣地。如今再学操作系统，希望能够借此机会，了却当年的初心😄。</div>2021-08-31</li><br/>
</ul>