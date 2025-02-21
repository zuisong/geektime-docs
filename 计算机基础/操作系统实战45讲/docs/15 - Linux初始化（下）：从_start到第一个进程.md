你好，我是LMOS。

今天我们继续来研究Linux的初始化流程，为你讲解如何解压内核，然后讲解Linux内核第一个C函数。最后，我们会用Linux的第一个用户进程的建立来收尾。

如果用你上手去玩一款新游戏做类比的话，那么上节课只是新手教程，而这节课就是更深入的实战了。后面你会看到很多熟悉的“面孔”，像是我们前面讲过的CPU工作模式、MMU页表等等基础知识，这节课都会得到运用。

## 解压后内核初始化

下面，我们先从setup.bin文件的入口\_start开始，了解启动信息结构，接着由16位main函数切换CPU到保护模式，然后跳入vmlinux.bin文件中的startup\_32函数重新加载段描述符。

如果是64位的系统，就要进入startup\_64函数，切换到CPU到长模式，最后调用extract\_kernel函数解压Linux内核，并进入内核的startup\_64函数，由此Linux内核开始运行。

### 为何要从\_start开始

通过上节课对vmlinuz文件结构的研究，我们已经搞清楚了其中的vmlinux.bin是如何产生的，它是由linux/arch/x86/boot/compressed目录下的一些目标文件，以及piggy.S包含的一个vmlinux.bin.gz的压缩文件一起生成的。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（35） 💬（3）<div>大体上整理了一下，有问题欢迎帮忙指正【上】：
Grub在&#47;boot目录下找到的linux内核，是bzImage格式
1、bzImage格式生成：
1.1、head_64.S+其他源文件-&gt;编译-&gt; vmlinux【A】
1.2、objcopy工具拷贝【 拷贝时，删除了文件中“.comment”段，符号表和重定位表】-&gt;vmlinux.bin【A】
1.3、gzib压缩-&gt;vmlinux.bin.gz
1.4、piggy打包，附加解压信息-&gt;piggy.o-&gt;其他.o文件一起链接-&gt;vmlinux【B】
1.5、objcopy工具拷贝【 拷贝时，删除了文件中“.comment”段，符号表和重定位表】-&gt;vmlinux【B】
1.6、head.S +main.c+其他-&gt;setup.bin
1.7、setup.bin+vmlinux.bin【B】-&gt;bzImage合并-&gt;bzImage

2、GRUB加载bzImage文件
2.1、会将bzImage的setup.bin加载到内存地址0x90000 处
2.2、把vmlinuz中的vmlinux.bin部分，加载到1MB 开始的内存地址

3、GRUB会继续执行setup.bin代码，入口在header.S【arch&#47;x86&#47;boot&#47;header.S】
GRUB会填充linux内核的一个setup_header结构，将内核启动需要的信息，写入到内核中对应位置，而且GRUB自身也维护了一个相似的结构。
Header.S文件中从start_of_setup开始，其实就是这个setup_header的结构。
此外， bootparam.h有这个结构的C语言定义，会从Header.S中把数据拷贝到结构体中，方便后续使用。

4、GRUB然后会跳转到 0x90200开始执行【恰好跳过了最开始512 字节的 bootsector】，正好是head.S的_start这个位置；

5、在head.S最后，调用main函数继续执行

6、main函数【 arch&#47;x86&#47;boot&#47;main.c】【16 位实模式】
6.1、拷贝header.S中setup_header结构，到boot_params【arch\x86\include\uapi\asm\bootparam.h】
6.2、调用BIOS中断，进行初始化设置，包括console、堆、CPU模式、内存、键盘、APM、显卡模式等
6.3、调用go_to_protected_mode进入保护模式

7、 go_to_protected_mode函数【 arch&#47;x86&#47;boot&#47;pm.c】
7.1、安装实模式切换钩子
7.2、启用1M以上内存
7.3、设置中断描述符表IDT
7.4、设置全局描述符表GDT
7.4、protected_mode_jump，跳转到boot_params.hdr.code32_start【保护模式下，长跳转，地址为 0x100000】 

8、恰好是vmlinux.bin在内存中的位置，通过这一跳转，正式进入vmlinux.bin

9、startup_32【 arch&#47;x86&#47;boot&#47;compressed&#47;head64.S】
全局描述符GDT
加载段描述符
设置栈
检查CPU是否支持长模式
开启PAE
建立MMU【4级，4G】
开启长模式
段描述符和startup_64地址入栈
开启分页和保护模式
弹出段描述符和startup_64地址到CS：RIP中，进入长模式

10、 startup_64【 arch&#47;x86&#47;boot&#47;compressed&#47;head64.S】
初始化寄存器
初始化栈
调准给MMU级别
压缩内核移动到Buffer最后
调用.Lrelocated

11、.Lrelocated
申请内存
被解压数据开始地址
被解压数据长度
解压数据开始地址
解压后数据长度
调用 extract_kernel解压内核

12、extract_kernel解压内核【 arch&#47;x86&#47;boot&#47;compressed&#47;misc.c】
保存boot_params
解压内核
解析ELF，处理重定向， 把 vmlinux 中的指令段、数据段、BSS 段，根据 elf 中信息和要求放入特定的内存空间
返回了解压后内核地址，保存到%rax

13、返回到.Lrelocated继续执行
跳转到%rax【解压后内核地址】，继续执行
解压后的内核文件，入口函数为【arch&#47;x86&#47;kernel&#47;head_64.S】</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（18） 💬（2）<div>大体上整理了一下，有问题欢迎帮忙指正【下】：
14、SYM_CODE_START_NOALIGN(startup_64)【arch&#47;x86&#47;kernel&#47;head_64.S】
SMP 系统加电之后，总线仲裁机制会选出多个 CPU 中的一个 CPU，称为 BSP，也叫第一个 CPU。它负责让 BSP CPU 先启动，其它 CPU 则等待 BSP CPU 的唤醒。
第一个启动的 CPU，会跳转 secondary_startup_64 函数中 1 标号处，对于其它被唤醒的 CPU 则会直接执行 secondary_startup_64 函数。

15、secondary_startup_64 函数【arch&#47;x86&#47;kernel&#47;head_64.S】
各类初始化工作，gdt、描述符等
跳转到initial_code，也就是x86_64_start_kernel

16、 x86_64_start_kernel【 arch&#47;x86&#47;kernel&#47;head64.c】
各类初始化工作，清理bss段，清理页目录，复制引导信息等
调用x86_64_start_reservations

17、x86_64_start_reservations【 arch&#47;x86&#47;kernel&#47;head64.c】
调用start_kernel();

18、start_kernel【 init&#47;main.c】
各类初始化：ARCH、日志、陷阱门、内存、调度器、工作队列、RCU锁、Trace事件、IRQ中断、定时器、软中断、ACPI、fork、缓存、安全、pagecache、信号量、cpuset、cgroup等等
调用 arch_call_rest_init，调用到rest_init

19、rest_init【 init&#47;main.c】
kernel_thread，调用_do_fork，创建了kernel_init进程，pid=1 . 是系统中所有其它用户进程的祖先
kernel_thread，调用_do_fork，创建了 kernel_thread进程，pid=2， 负责所有内核线程的调度和管理
【最后当前的进程， 会变成idle进程，pid=0】

20、kernel_init
根据内核启动参数，调用run_init_process，创建对应进程
调用try_to_run_init_process函数，尝试以 &#47;sbin&#47;init、&#47;etc&#47;init、&#47;bin&#47;init、&#47;bin&#47;sh 这些文件为可执行文件建立init进程，只要其中之一成功就可以

调用链如下：
try_to_run_init_process
run_init_process
kernel_execve
bprm_execve
exec_binprm
search_binary_handler-》依次尝试按各种可执行文件格式进行加载，而ELF的处理函数为 load_elf_binary
load_elf_binary
start_thread
start_thread_common，会将寄存器地址，设置为ELF启动地址
当从系统调用返回用户态时，init进程【1号进程】，就从ELF执行了

到此为止，系统的启动过程结束。</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（6） 💬（1）<div>_start在setup.bin的开头， x86_64_start_kernel在vmlinux.bin的开头，然后start_kernel初始化，然后rest_init初始化第一个用户进程和第一个内核进程，开始操作系统罪恶的一生。</div>2021-06-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlaNica7xRH6LlMNJtrbK0toc1od8YdqLZOD2AbnOZ2QyKC13gvrrL9cOx5dyYNcsHnJkR6K4ibxZQ/132" width="30px"><span>Geek_59a6f9</span> 👍（2） 💬（2）<div>老师，你这里说的grub是grub legacy还是grub2啊？grub2应该首先会进入保护模式，那grub2还会跳转到inux&#47;arch&#47;x86&#47;boot&#47;head.S 里的main函数 再去执行一次切换保护模式吗？这个时候应该早就是保护模式了吧</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（1） 💬（1）<div>课程已经快进入正题了，下一步就是内存了吧</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/e7/261711a5.jpg" width="30px"><span>blentle</span> 👍（1） 💬（1）<div>收获盛大，终于看到了稍微能消化的一篇了</div>2021-06-11</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（1） 💬（1）<div>这个问题是考对Linux熟悉程度了。哈</div>2021-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5f/09/2ec44412.jpg" width="30px"><span>Qfeng</span> 👍（0） 💬（1）<div>内核启动最后创建了两个进程：kernel_init和kernel_thread，前面是第一个用户进程，后续用户进程都是从它fork而来，后面是内核进程，用来管理后续内核线程调度。这两个进程令我印象深刻。
</div>2022-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/06/30/c26ea06a.jpg" width="30px"><span>艾恩凝</span> 👍（0） 💬（1）<div>这节终于结束了，计划俩月完成，感觉进度有点慢了，到现在快20天了，应该去年来参与这门课的</div>2022-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>果然厉害了</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ef/18/6a620733.jpg" width="30px"><span>kocgockohgoh王裒</span> 👍（0） 💬（1）<div>请问为什么有两个重名的startup_64啊  名字不回冲突么</div>2021-12-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cabLXAUXiavXnEckAgo971o4l1CxP4L9wOV2eUGTyKBUicTib6gJyKV9iatM4GG1scz5Ym17GOzXWQEGzhE31tXUtQ/132" width="30px"><span>日就月将</span> 👍（0） 💬（1）<div>老师，自动编译配置文件里有修改grub menuentry选项吗 要是想修改在哪里改啊</div>2021-11-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlaNica7xRH6LlMNJtrbK0toc1od8YdqLZOD2AbnOZ2QyKC13gvrrL9cOx5dyYNcsHnJkR6K4ibxZQ/132" width="30px"><span>Geek_59a6f9</span> 👍（0） 💬（2）<div>老师，对于非boot cpu的启动不是很清楚。是BSP启动以后发一个中断唤醒其他cpu，然后执行到secondary_startup_64吗？接着还是会去执行start_kernel? 可是我们主cpu已经初始化内核里内存部分了，其他cpu再去执行的话就会有问题吧？</div>2021-06-19</li><br/><li><img src="" width="30px"><span>Geek_009bb2</span> 👍（0） 💬（0）<div>&quot;通常我们不会传递参数，所以这个函数会执行到上述代码的 15 行，依次尝试以 &#47;sbin&#47;init、&#47;etc&#47;init、&#47;bin&#47;init、&#47;bin&#47;sh 这些文件为可执行文件建立进程，但是只要其中之一成功就行了&quot; 麻烦问一下这里是不是如果grub中设置了initrd 则会执行initramfs中的 init，最终由initramfs中的init通过switch root 切换到根文件系统的 init </div>2024-09-12</li><br/><li><img src="" width="30px"><span>1+1=2</span> 👍（0） 💬（0）<div>总结的很浅显，欢迎大家指导：
加电→BIOS→引导设备（硬盘&#47;U盘）的引导扇区→加载GRUB→加载vmlinuz

加电瞬间，CS=0xF000*16+IP=0xFFF0→0xFFFF0（此时BIOS正式启动）→进行设备初始化和检查（跳转到内存运行）→在内存中建立中断表和中断服务程序（从0x00000开始1kb构建中断表，在中断表位置用256kb构建BIOS数据区（0x00400~0x004FF），在0x0e05b加载8kb的中断服务程序）→启动引导设备（Linux中的MBR即第一个扇区512kb）→boot.img写入硬盘的MBR，并且记录core.img文件占用的第一个扇区的扇区号→硬盘启动diskboot.img，读取core.img其余部分到内存中→控制权交给kernel.img→具有文件识别功能，访问&#47;boot&#47;grub目录并加载相关配置文件和功能→加载Linux的vmliuz内核文件→setup.bin&#47;_start→将vmlinuz的setup.bin读到内存地址0x90000处，然后跳转到0x90200（跳过bootsector，从_start开始）→调用head.S&#47;main执行初始化，进入

保护模式（go_to_protected_mode）→跳转到boot_params.hdr.code32_start的地址（0x100000）→且vmlinux.bin在1MB中，跳转后进入到vmlinux.bin→调用startup_32函数，重新加载段描述符→（支持长模式）设置64位的全局描述符、设置MMU页表、开启分页进入长模式→跳转到startup_64函数（进入64位）→初始化长模式数据段寄存器，确定解压缩地址→拷贝压缩vmlinux.bin到该地址→跳转到decompress_kernel地址处，解压vmlinux.bin.gz→函数中调用extract_kernel()，并根据piggy.o中信息解压vmlinux.bin.gz出vmlinux（elf）→调用parse_elf解析elf格式：将vmlinux中的指令段、数据段、BSS段，根据elf信息放入指定的内存空间，返回指令段的入口地址→通过jmp *rax进入内核→调用secondary_startup_64（）→x86_ 64start_kernel()，处理页表→start_kernel(),调用内核初始化函数，具备了提供功能服务能力→建立第一个进程

</div>2024-08-06</li><br/><li><img src="" width="30px"><span>Geek_5b3649</span> 👍（0） 💬（0）<div>现在很多场景下grub.cfg使用linux而非linux16命令加载内核，linux命令使用32-bit boot protocol。这种情况下，grub2不需要加载实模式代码(setup.bin)。grub2只加载保护模式代码(vmlinux.bin)并最终把控制权交给vmlinux.bin的最开始:startup_32。</div>2024-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/2c/180075e0.jpg" width="30px"><span>小豪</span> 👍（0） 💬（0）<div>vmlinuz文件能够被grub加载，是因为它也包含了grub头信息吗</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/82/3e/1fc6e36a.jpg" width="30px"><span>zlig</span> 👍（0） 💬（0）<div>还是不理解为啥linux要把vmlinux.bin压缩这么多次。</div>2021-09-19</li><br/>
</ul>