你好，我是LMOS。

在前面的课程中，我们建好了二级引导器，启动了我们的Cosmos，并进行了我们Cosmos的Hal层初始化。

我会用两节课带你领会Linux怎样做初始化。虽然我们自己具体实现过了初始化，不过我们也不妨看看Linux的初始化流程，借鉴一下Linux开发者的玩法。

这节课，我会先为你梳理启动的整体流程，重点为你解读Linux上GRUB是怎样启动，以及内核里的“实权人物”——vmlinuz内核文件是如何产生和运转的。下节课，我们从setup.bin文件的\_start函数入手，研究Linux初始化流程。

好，接下来我们从全局流程讲起，正式进入今天的学习。

## 全局流程

x86平台的启动流程，是非常复杂的。为了帮助你理解，我们先从全局粗略地看一看整体流程，然后一步步细化。

在机器加电后，BIOS会进行自检，然后由BIOS加载引导设备中引导扇区。在安装有Linux操作系统的情况下，在引导扇区里，通常是安装的GRUB的一小段程序（安装windows的情况则不同）。最后，GRUB会加载Linux的内核映像vmlinuz，如下图所示。

![](https://static001.geekbang.org/resource/image/f3/b3/f3d8b95e8c1563466d31f385bb42aab3.jpg?wh=3543%2A2005 "x86的全局启动流程示意图")

上图中的引导设备通常是机器中的硬盘，但也可以是U盘或者光盘甚至是软盘。BIOS会自动读取保存在CMOS中的引导设备信息。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（57） 💬（7）<div>大体上整理了一下，有问题欢迎帮忙指出【上】：

操作系统的启动分为两个阶段：引导boot和启动startup，本节主要还是boot过程：
BIOS-&gt;GRUG1-&gt;GRUB1.5-&gt;GRUB2-&gt;Linux内核【环境硬盘引导、MBR分区】

1、按电源键，系统加电

2、主板通电
CPU加电时，会默认设置[CS:IP]为[0XF000:0XFFF0]，根据实模式下寻址规则，CPU指向0XFFFF0
这个地址正是BIOS启动程序位置，而BIOS访问方式与内存一致，所以CPU可以直接读取命令并执行

3、BIOS执行
3.1、BIOS首先执行POST自检，包括主板、内存、外设等，遇到问题则报警并停止引导

3.2、BIOS对设备执行简单的初始化工作

3.3、BIOS 会在内存中：
建立中断表（0x00000~0x003FF）
构建 BIOS 数据区（0x00400~0x004FF）
加载了中断服务程序（0x0e05b~0x1005A）

3.4、BIOS根据设备启动顺序，依次判断是否可以启动
比如先检查光驱能否启动
然后依次检查硬盘是否可以启动【硬盘分区的时候，设置为活动分区】

4、硬盘引导
4.1、先说下寻址方式，与扇区编号的事情
最传统的磁盘寻址方式为CHS，由三个参数决定读取哪个扇区：磁头（Heads）、柱面(Cylinder)、扇区(Sector)
磁头数【8位】，从0开始，最大255【微软DOS系统，只能用255个】，决定了读取哪个盘片的哪个面【一盘两面】
柱面数【10位】，从0开始，最大1023【决定了读取哪个磁道，磁道无论长短都会划分为相同扇区数】
扇区数【6位】，从1开始，最大数 63【CHS中扇区从1开始，而逻辑划分中扇区从0开始，经常会造成很多误解】
每个扇区为512字节

4.2、然后说下引导方式
BIOS在发现硬盘启动标志后，BIOS会引发INT 19H中断
这个操作，会将MBR【逻辑0扇区】，也就是磁盘CHS【磁头0，柱面0，扇区1】，读取到内存[0:7C00h]，然后执行其代码【GRUB1阶段】，至此BIOS把主动权交给了GRUB1阶段代码
MBR扇区为512字节，扇区最后分区表至少需要66字节【64字节DPT+2字节引导标志】，所以这段代码最多只能有446字节，grub中对应的就是引导镜像boot.img
boot.img的任务就是，定位，并通过BIOS INT13中断读取1.5阶段代码，并运行

5、Grub1.5阶段
5.1、先说一下MBR GAP
据说微软DOS系统原因，第一个分区的起始逻辑扇区是63扇区，在MBR【0扇区】和分布表之间【63扇区】，存在62个空白扇区，共 31KB。
Grub1.5阶段代码就安装在这里。

5.2、上面提到，boot.img主要功能就是找到并加载Grub1.5阶段代码，并切换执行。
Grub1.5阶段代码是core.img，其主要功能就是加载文件系统驱动，挂载文件系统， 位加载并运行GRUB2阶段代码。
core.img包括多个映像和模块：
diskboot.img【1.5阶段引导程序】，存在于MBR GAP第一个扇区；【这里是硬盘启动的情况，如果是cd启动就会是cdboot.img】
lzma_decompress.img【解压程序】
kernel.img【grub核心代码】，会【压缩存放】
biosdisk.mod【磁盘驱动】、Part_msdos.mod【MBR分区支持】、Ext2.mod【EXT文件系统】等，会【压缩存放】

其实boot.img只加载了core.img的第一个扇区【存放diskboot.img】，然后控制权就交出去了，grub阶段1代码使命结束。
diskboot.img知道后续每个文件的位置，会继续通过BIOS中断读取扇区，加载余下的部分并转交控制权，包括：
加载lzma_decompress.img，从而可以解压被压缩的模块
加载kernel.img，并转交控制权给kernel.img
kernel.img的grub_main函数会调用grub_load_modules函数加载各个mod模块
加载各个mod后，grub就支持文件系统了，访问磁盘不需要再依靠BIOS的中断以扇区为单位读取了，终于可以使用文件系统了</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（35） 💬（1）<div>大体上整理了一下，有问题欢迎帮忙指出【下】：
6、GRUB2阶段
现在grub就能访问boot&#47;grub及其子目录了
kernel.img接着调用grub_load_normal_mode加载normal模块
normal模块读取解析文件grub.cfg，查看有哪些命令，比如发现了linux、initrd这几个命令，需要linux模块
normal模块会根据command.lst，定位并加载用到的linux模块【一般在&#47;boot&#47;grub2&#47;i386-pc目录】
当然，同时需要完成初始化显示、载入字体等工作
接下来Grub就会给咱们展示启动菜单了

7、选择启动菜单
7.1、引导协议
引导程序加载内核，前提是确定好数据交换方式，叫做引导协议，内核中引导协议相关部分的代码在arch&#47;x86&#47;boot&#47;header.S中，内核会在这个文件中标明自己的对齐要求、是否可以重定位以及希望的加载地址等信息。同时也会预留空位，由引导加载程序在加载内核时填充，比如initramfs的加载位置和大小等信息。
引导加载程序和内核均为此定义了一个结构体linux_kernel_params，称为引导参数，用于参数设定。Grub会在把控制权移交给内核之前，填充好linux_kernel_params结构体。如果用户要通过grub向内核传递启动参数，即grub.cfg中linux后面的命令行参数。Grub也会把这部分信息关联到引导参数结构体中。

7.2、开始引导
Linux内核的相关文件位于&#47;boot 目录下，文件名均带有前缀 vmlinuz。
咱们选择对应的菜单后，Grub会开始执行对应命令，定位、加载、初始化内核，并移交到内核继续执行。
调用linux模块中的linux命令，加载linux内核
调用linux模块中的initrd命令，填充initramfs信息，然后Grub会把控制权移交给内核。
内核此时开始执行，同时也就可以读取linux_kernel_params结构体的数据了
boot阶段结束，开始进入startup阶段。</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/1b/7426e629.jpg" width="30px"><span>178</span> 👍（6） 💬（1）<div>vmlinuz是可引导的、压缩的内核。“vm”代表 “Virtual Memory”，linu代表“Linux”，z代表压缩。是个有故事的缩写</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（6） 💬（1）<div>请问，为什么要用 C 代码 mkpiggy 程序生成 piggy.S 文件，并包含 vmlinux.bin.gz 文件呢？

看了这下生成的这个piggy.S 文件
主要的就是这行代码
.incbin &quot;arch&#47;x86&#47;boot&#47;compressed&#47;vmlinux.bin.gz&quot;
通过C 代码的形式，可以传入不同的参数来设置不同的压缩包vmlinux.bin.xx  来生成piggy.S 。
</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/a0/0e8d56df.jpg" width="30px"><span>孤星可</span> 👍（5） 💬（1）<div>尝试实现了 lmoskrlimg 的逻辑（即 Cosmos.eki 的生成），有兴趣可以看看。

https:&#47;&#47;github.com&#47;guxingke&#47;demo&#47;blob&#47;master&#47;bytes-demo&#47;src&#47;main&#47;java&#47;com&#47;gxk&#47;demo&#47;Main.java</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5f/09/2ec44412.jpg" width="30px"><span>Qfeng</span> 👍（4） 💬（1）<div>一、简单总结：
1. CPU上电启动BIOS（ROM）
CPU硬件被设计成在加电的瞬间，强制将 CS 寄存器的值设置为 0XF000，IP 寄存器的值设置为 0XFFF0。
CS:IP 为 0XFFFF0 的这个物理地址上连接了主板上的一块小的 ROM 芯片，BIOS 程序就被固化在该 ROM 芯片里。
总结：CPU上电后硬件自动将 CS:IP 指向地址 0XFFFF0，这里存放了BIOS程序的入口地址，达到启动 BIOS 的目的。
（注：这个ROM芯片的访问机制和寻址方式和内存一样，只是它在断电时不会丢失数据，在常规下也不能往这里写入数据，它是一种只读内存。）

2. ROM BIOS
初始化CPU和内存，将自己拷贝到内存，执行环境跳转到内存（DDR）

3. DDR BIOS
1）设备初始化
2）在内存中建立中断服务程序表（0x00000~0x003FF，1KB，256个条目）, BIOS 数据区（0x00400~0x004FF）和中断服务程序（0x0E05B~1005B，8KB）
3）搜索可引导的外部存储器，并启动其中的程序。（包括：硬盘，U盘，软驱，光驱和网络设备等）
4）Linux从硬盘启动时，硬盘中名为MRB的第一个扇区包含的GRUB 启动程序（安装GRUB时自动写入）和分区表被 BIOS 装载到 0x7c00 地址开始的内存空间，
至此BIOS使命结束，控制权交给GRUB。

4. GRUB 启动
1）GRUB包含 boot.img和core.img两部分，硬盘MRB空间有限只包含boot.img，boot.img中包含core.img存放的硬盘扇区号
2）core.img 文件是由 GRUB 安装程序根据安装时环境信息，用其它 GRUB 的模块文件动态生成，主要包含diskboot.img，kernel.img和其他功能模块。
GRUB 的 core.img 文件一旦开始工作，就可以加载 Linux 系统的 vmlinuz 内核文件了。

5. Linux vmlinuz的生成
1）由Linux 编译生成的 bzImage 文件复制而来，存放在 &#47;boot 目录下
2）bzImage 由 arch&#47;x86&#47;boot&#47;Makefile 编译而来，依赖 setup.bin和vmlinux.bin两个。
3）setup.bin 由 &#47;arch&#47;x86&#47;boot&#47; 目录下的文件编译生成
4）arch&#47;x86&#47;boot&#47;compressed 目录 编译生成 vmlinux.bin过程总结：Linux 的 kbuild（内核编译）系统会递归进入到每个目录，由该目录下的 Makefile 决定要编译的文件。每个目录编译生成一个 built-in.o，所有的 built-in.o最终链接生成一个 vmlinux 文件最终压缩成 vmlinux.bin.gz，最终由mkpiggy 生成 vmlinux。

二、思考题
为什么要用 C 代码 mkpiggy 程序生成 piggy.S 文件，并包含 vmlinux.bin.gz 文件呢？
==》通过main函数传入的可变参数可以根据需要灵活扩展piggy.S的内容？</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（1）<div>工具生成方式灵活，支持多种配置，且能满足各种场景下的需求~</div>2021-06-09</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（2） 💬（4）<div>程序来生成汇编代码，这个是有多种配置让使用者根据自己的需求来生成。比如vmlinuz.bin压缩的方式的不同又或者是cpu的指令不同。  产生的汇编代码也不同。 另外Cosmos.eki的生成过程能有个说明不？ </div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（1） 💬（1）<div>不管肚子多少遍启动流程，还是记不住各种地址，除了0×7c00，哈哈</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（1）<div>又学习了一遍启动流程。😂</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（0） 💬（1）<div>请问老师，boot.img 是 512B 大小，MBR 也是 512，难道 boot.img 安装到 MBR 的时候会把 MBR 全部覆盖掉吗？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（0） 💬（2）<div>老师好，我看别的书里面将上电后先跳转到 reset vector(0xFFFFFFF0)，然后 reset vector 会跳转到 BIOS 的入口（0xFFFF0），您这里为什么没有这个恢复向量呢</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/46/6b/e766c18d.jpg" width="30px"><span>老王</span> 👍（0） 💬（1）<div>需要多分析各个脚本的功能，才能把握住脉络</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/68/83/ecd4e4d6.jpg" width="30px"><span>WGJ</span> 👍（0） 💬（1）<div>老师，这里面好像piggy.s依赖vmlinux目标，然后vmlinux 目标又依赖piggy.s，这种互相依赖是怎么解决的啊</div>2024-02-02</li><br/>
</ul>