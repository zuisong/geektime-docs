你好，我是LMOS。

在上一课中，我们一起约定了主环境，安装了编译工具和依赖库，构建了交叉编译RISC-V工具链。

今天我们继续构建RISC-V版的模拟器QEMU（代码你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson12~13)下载），让它成为“定制款”，更匹配我们的学习需要。为此，我们需要设置好主环境的环境变量，安装好VSCode及其插件，这样才能实现编辑、编译、运行、调试RISC-V程序的一体化、自动化。

话不多说，我们开始吧。

## RISC-V运行平台

有了上节课成功构建好的交叉编译器，有很多同学可能按捺不住，急着想写一个简单的Hello World程序，来测试一下刚刚构建的交叉编译器。

恕我直言，这时你写出来的Hello World程序，虽然会无警告、无错误的编译成功，但是只要你一运行，铁定会出错。

这是为什么呢？因为你忘记了交叉编译器，生成的是RISC-V平台的可执行程序，这样的程序自然无法在你的宿主机x86平台上运行，它只能在RISC-V平台上运行。

摸着自己的荷包，你可能陷入了沉思：难道我还要买一台RISC-V平台的计算机？这样成本可太高了，不划算。

贫穷让人学会变通，为了节约成本，我们希望能用软件模拟RISC-V平台。嘿！这当然可以，而且前辈们，早已给我们写好了这样的软件，它就是QEMU。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/7b/ee2e9302.jpg" width="30px"><span>廖雪峰</span> 👍（10） 💬（4）<div>如果有不想编译的同学，可以按照以下步骤运行：

1. 安装Ubuntu 22.04

2. 安装编译环境：
$ sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev

3. 直接安装riscv-gcc发行包：
$ sudo apt install gcc-riscv64-linux-gnu gcc-riscv64-unknown-elf picolibc-riscv64-unknown-elf

4. 直接安装qemu发行包：
$ sudo apt install qemu-user qemu-system-misc

5. 编写hello.c
#include&lt;stdio.h&gt;
int main()
{
	printf(&quot;Hello, riscv!\n&quot;);
	return 0;
}

6. 编译：
$ riscv64-linux-gnu-gcc hello.c -o hello

7. 运行：
$ qemu-riscv64 hello
qemu-riscv64: Could not open &#39;&#47;lib&#47;ld-linux-riscv64-lp64d.so.1&#39;: No such file or directory

如果报错找不到&#47;lib&#47;ld-linux-riscv64-lp64d.so.1，是因为这个文件实际上在&#47;usr&#47;riscv64-linux-gnu&#47;lib下，加个参数运行：

$ qemu-riscv64 -L &#47;usr&#47;riscv64-linux-gnu hello
Hello, riscv!

最后，riscv64-unknown-elf-gcc编译还没搞定，正在找原因</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/1f/1af5d4ed.jpg" width="30px"><span>光华路小霸王</span> 👍（1） 💬（1）<div>使用了 VS Code 的 Remote Development 远程调试，发现 F5 debug 回找不到编译器和 qemu，shell
登录可以，一通谷歌是  .bashrc 与 .bash_profile 的问题，把环境变量加到 bash_profile 就可以了，vscode 是运行在 login shell 的，加载的是 bash_profile ，不会加载  .bashrc 
refs: https:&#47;&#47;github.com&#47;microsoft&#47;vscode-remote-release&#47;issues&#47;854
</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/03/8f/38038fb5.jpg" width="30px"><span>Liu Zheng</span> 👍（1） 💬（1）<div>纠正一下。在环境变量设置好之前，即使在`&#47;opt&#47;riscv&#47;qemu&#47;bin`目录下，也不能直接跑`
qemu-riscv32 -version &amp;&amp; qemu-riscv64 -version &amp;&amp; qemu-system-riscv32 -version &amp;&amp; qemu-system-riscv64 -version`. 而是需要`.&#47;qemu-riscv32 ...`.</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（1） 💬（1）<div>source 的主要用途是执行文件并从文件加载变量及函数到执行环境。
~&#47;.bashrc文件中的环境变量已经在用户登录shell的时候加载进执行环境了，此时编辑不会触发加载。必须使用source或者重新登录才能触发重新加载</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7d/9f/53dd1d94.jpg" width="30px"><span>筱琲</span> 👍（0） 💬（1）<div>在build 目录下执行配置命令时，遇到几个包缺失，依次安装就好：
sudo apt install libglib2.0-dev libpixman-1-dev libsdl2-dev</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（1）<div>sudo make -j8, 这里应该不用sudo。</div>2022-09-22</li><br/><li><img src="" width="30px"><span>Geek_d47998</span> 👍（0） 💬（1）<div>tasks.json和launch.json在老师给的代码，gitee仓库下有，main.c文件里还需要放Makefile后才能按F5编译</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/24/c2/791d0f5e.jpg" width="30px"><span>jeigiye</span> 👍（0） 💬（1）<div>root@zgye-ubuntu:~&#47;test# cat hello.s 
	.file	&quot;hello.c&quot;
	.option nopic
	.attribute arch, &quot;rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0&quot;
	.attribute unaligned_access, 0
	.attribute stack_align, 16
	.text
	.section	.rodata
	.align	3
.LC0:
	.string	&quot;Risc-V&quot;
	.align	3
.LC1:
	.string	&quot;Hello %s\n&quot;
	.text
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-16
	sd	ra,8(sp)
	sd	s0,0(sp)
	addi	s0,sp,16
	lui	a5,%hi(.LC0)
	addi	a1,a5,%lo(.LC0)
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	printf
	li	a5,0
	mv	a0,a5
	ld	ra,8(sp)
	ld	s0,0(sp)
	addi	sp,sp,16
	jr	ra
	.size	main, .-main
	.ident	&quot;GCC: () 12.1.0&quot;
root@zgye-ubuntu:~&#47;test# &#47;opt&#47;riscv&#47;qemu&#47;bin&#47;qemu-riscv64 hello
Hello Risc-V
root@zgye-ubuntu:~&#47;test#

ubuntu22.04上跑通。</div>2022-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/03/8f/38038fb5.jpg" width="30px"><span>Liu Zheng</span> 👍（0） 💬（3）<div>想问一下，https:&#47;&#47;gitee.com&#47;lmos&#47;Geek-time-computer-foundation&#47;blob&#47;master&#47;lesson12~13&#47;main.c#L7-8 这里面func和sumdata分别都是什么呢？没有看到哪个地方有定义这两个东西，跑make或者vscode里面按F5也是会报错。</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/1a/3c287e37.jpg" width="30px"><span>LooMou</span> 👍（0） 💬（0）<div>window 的 wsl
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.6 LTS
Release:        20.04
Codename:       focal

riscv-gnu-toolchain 我编译的是 2024.04.12-nightly，对应的 qemu 的版本是 8.2.1
wget https:&#47;&#47;download.qemu.org&#47;qemu-&lt;version&gt;.tar.xz
直接按步骤继续，编译成功，在 ~&#47;.bashrc 中加环境变量也要在 ~&#47;.profile 里加。

代码运行成功，调试控制台：
=thread-group-added,id=&quot;i1&quot;
Warning: Debuggee TargetArchitecture not detected, assuming x86_64.
=cmd-param-changed,param=&quot;pagination&quot;,value=&quot;off&quot;
0x000100c2 in _start ()

Breakpoint 1, main () at main.c:6
6	    int i = 250;

Breakpoint 2, main () at main.c:8
8	    return 0; 
终端输出：
 *  正在执行任务: make 

CC -[M] 正在构建... add.S
CC -[M] 正在构建... main.c
CC -[M] 正在构建... main.elf
 *  终端将被任务重用，按任意键关闭。 

 *  正在执行任务: echo Starting RISCV-QEMU&amp;qemu-riscv32 -g 1234 .&#47;*.elf 

Starting RISCV-QEMU
hello world i is 250 3 250!</div>2024-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c8/b0/853cbd58.jpg" width="30px"><span>Pony</span> 👍（0） 💬（0）<div>&#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;..&#47;..&#47;..&#47;..&#47;riscv64-unknown-elf&#47;bin&#47;ld: error: &#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;rv32i&#47;ilp32&#47;crtbegin.o: Mis-matched ISA version for &#39;i&#39; extension. 2.0 vs 2.1
&#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;..&#47;..&#47;..&#47;..&#47;riscv64-unknown-elf&#47;bin&#47;ld: failed to merge target specific data of file &#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;rv32i&#47;ilp32&#47;crtbegin.o
在make all的时候报这个错误是为什么</div>2024-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/8d/abcc5fce.jpg" width="30px"><span>🔥Burn</span> 👍（0） 💬（0）<div>archlinux,在编译qemu时报了编译错误,麻烦老师看看什么问题:
lssh -lstdc++ -Wl,--end-group
&#47;usr&#47;bin&#47;ld: libcommon.fa.p&#47;ebpf_ebpf_rss.c.o: in function `ebpf_rss_load&#39;:
&#47;home&#47;burn&#47;riscv-gnu-toolchain&#47;qemu-6.2.0&#47;build&#47;..&#47;ebpf&#47;ebpf_rss.c:52: undefined reference to `bpf_program__set_socket_filter&#39;
collect2: 错误：ld 返回 1
[1926&#47;2548] Compiling C object libqemu-riscv64-linux-user.fa.p&#47;target_riscv_vector_helper.c.o
[1927&#47;2548] Compiling C object libqemu-riscv64-linux-user.fa.p&#47;target_riscv_translate.c.o
[1928&#47;2548] Compiling C object libqemu-riscv32-linux-user.fa.p&#47;target_riscv_translate.c.o
ninja: build stopped: subcommand failed.
make: *** [Makefile:162：run-ninja] 错误 1

</div>2023-05-18</li><br/><li><img src="" width="30px"><span>Geek_72a577</span> 👍（0） 💬（1）<div>qemu-6.2.0.tar.xz无法下载，有gitee替代地址的吗？</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/a4/f4e7e00d.jpg" width="30px"><span>Dean🌞中偉</span> 👍（0） 💬（2）<div>gcc编译成功：
riscv64-unknown-elf-gcc -v
Using built-in specs.
COLLECT_GCC=riscv64-unknown-elf-gcc
COLLECT_LTO_WRAPPER=&#47;opt&#47;riscv&#47;gcc&#47;libexec&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;lto-wrapper
Target: riscv64-unknown-elf
Configured with: &#47;home&#47;adrain&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gcc&#47;configure --target=riscv64-unknown-elf --prefix=&#47;opt&#47;riscv&#47;gcc --disable-shared --disable-threads --disable-tls --enable-languages=c,c++ --with-system-zlib --with-newlib --with-sysroot=&#47;opt&#47;riscv&#47;gcc&#47;riscv64-unknown-elf --disable-libmudflap --disable-libssp --disable-libquadmath --disable-libgomp --disable-nls --disable-tm-clone-registry --src=&#47;home&#47;adrain&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gcc --enable-multilib --with-abi=lp64d --with-arch=rv64imafdc --with-tune=rocket --with-isa-spec=2.2 &#39;CFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39; &#39;CXXFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39;
Thread model: single
Supported LTO compression algorithms: zlib
gcc version 10.2.0 (GCC)
debug的时候：
$ make
CC -[M] 正在构建... add.S
CC -[M] 正在构建... main.c
&#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;..&#47;..&#47;..&#47;..&#47;riscv64-unknown-elf&#47;bin&#47;ld: cannot find crtbegin.o: No such file or directory
&#47;opt&#47;riscv&#47;gcc&#47;lib&#47;gcc&#47;riscv64-unknown-elf&#47;10.2.0&#47;..&#47;..&#47;..&#47;..&#47;riscv64-unknown-elf&#47;bin&#47;ld: cannot find -lgcc
collect2: error: ld returned 1 exit status
make: *** [Makefile:37: main.elf] Error 1
是为啥呢</div>2023-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/1b/2b668b12.jpg" width="30px"><span>释迦</span> 👍（0） 💬（0）<div>为什么我按f5后弹出的对画框中cpu的寄存器是x86-64的寄存器，没有显示risc-v寄存器？步骤也是按照老师文中的步骤操作的。</div>2022-12-21</li><br/>
</ul>