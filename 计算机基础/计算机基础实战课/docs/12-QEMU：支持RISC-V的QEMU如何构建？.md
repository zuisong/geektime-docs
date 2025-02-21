你好，我是LMOS。

工欲善其事，必先利其器。作为开发者，学习过程中我们尤其要重视动手实践，不断巩固和验证自己学到的知识点。而动手实践的前提，就是要建立一个开发环境，这个环境具体包括编译环境、执行环境，以及各种常用的工具软件。

我会用两节课带你动手搭好环境，今天这节课咱们先热个身，搞清楚什么是主环境，还有怎么基于它生成交叉编译工具。

代码你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson12~13)下载。

## 主环境

主环境，有时也叫作HOST环境，也就是我们使用的计算机环境，即使用什么样的操作系统、什么架构的计算机作为开发环境。

比方说我们经常用PC机作为开发机使用，它实际就是一个基于x86架构（或其他架构）的硬件平台，再加上Windows或者Linux等操作系统共同组成的开发环境。

普通用户的电脑上经常安装的操作系统是Windows，因为界面友好方便、操作简单且娱乐影音、游戏办公等应用软件也是不胜枚举。

Windows对普通用户来说的确非常友好。但是作为软件开发者，对于志存高远、想要精研技术的我们而言，更喜欢用的是Linux系统。

它虽然没有漂亮的GUI，却暴露了更多的计算机底层接口，也生产了更多的开发工具和各种各样的工具软件。比如大名鼎鼎的编译器GCC、声名远扬的编辑器EMACS、VIM，还有自动化的脚本工具shell、make等。这些工具对开发者非常友好，配合使用可以让我们的工作事半功倍，后面你会逐渐体会到这点。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1c/f7/36/ccf3b5d1.jpg" width="30px"><span>Vic</span> 👍（5） 💬（3）<div>host使用的是Ubuntu 20.04 Desktop, 在Windows 11的笔记本, 用Virtualbox 6.1 搭建的虚机 (cpu 2 cores, 40GB 存储，4GB内存) ，按照老师的教程，以下是我的实验笔记： 
1. 在我的环境就只有一个libpython-dev 报错，因为有提示换成libpython2-dev，不碍事，而且不同的os，不同的版本，可能不会有这个问题，可以先用老师的命令。
sudo apt-get install git autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf patchutils bc libexpat-dev libglib2.0-dev ninja-build zlib1g-dev pkg-config libboost-all-dev libtool libssl-dev libpixman-1-dev libpython2-dev virtualenv libmount-dev libsdl2-dev
2. mkdir RISCV_TOOLS; cd RISCV_TOOLS
3.
git clone https:&#47;&#47;gitee.com&#47;mirrors&#47;riscv-gnu-toolchain
cd riscv-gnu-toolchain
4.
mkdir build 
cd build
..&#47;configure --prefix=&#47;opt&#47;riscv&#47;gcc --enable-multilib --target=riscv64-multlib-elf
5. 因为我的host环境是建在2cpu core的虚机上
sudo make -j 2 
6. 大约3个多小时，终于完成了。
7. cd &#47;opt&#47;riscv&#47;gcc&#47;bin
.&#47;riscv64-unknown-elf-gcc -v
8. 结果输出：
Using built-in specs.
COLLECT_GCC=.&#47;riscv64-unknown-elf-gcc
COLLECT_LTO_WRAPPER=&#47;opt&#47;riscv&#47;gcc&#47;libexec&#47;gcc&#47;riscv64-unknown-elf&#47;12.1.0&#47;lto-wrapper
Target: riscv64-unknown-elf
Configured with: &#47;home&#47;vic&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gcc&#47;configure --target=riscv64-unknown-elf --prefix=&#47;opt&#47;riscv&#47;gcc --disable-shared --disable-threads --enable-languages=c,c++ --with-pkgversion= --with-system-zlib --enable-tls --with-newlib --with-sysroot=&#47;opt&#47;riscv&#47;gcc&#47;riscv64-unknown-elf --with-native-system-header-dir=&#47;include --disable-libmudflap --disable-libssp --disable-libquadmath --disable-libgomp --disable-nls --disable-tm-clone-registry --src=&#47;home&#47;vic&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;gcc --enable-multilib --with-abi=lp64d --with-arch=rv64imafdc --with-tune=rocket --with-isa-spec=2.2 &#39;CFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39; &#39;CXXFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39;
Thread model: single
Supported LTO compression algorithms: zlib
gcc version 12.1.0 () 
9. 收工。
</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/26/1f/1af5d4ed.jpg" width="30px"><span>光华路小霸王</span> 👍（5） 💬（3）<div>编译中会卡在 
Cloning into &#39;&#47;home&#47;qing&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;gcc&#39;...
还是会去下载仓库，应该是我们下载的文件夹名称不是默认的，查看 README.md 文件，在最后说明了如何指定子模块的路径，在配置环节添加配置之后，戴尔笔记本双核  i5-4200U CPU @ 1.60GHz 编译，编译完成四十多分钟，系统使用  Debian 4.19.181-1 

..&#47;configure --prefix=&#47;opt&#47;riscv&#47;gcc \
--enable-multilib \
--target=riscv64-multlib-elf \
--with-gcc-src=&#47;home&#47;name&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gcc \
--with-binutils-src=&#47;home&#47;name&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-binutils \
--with-newlib-src=&#47;home&#47;name&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-newlib \
--with-glibc-src=&#47;home&#47;name&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-glibc \
--with-gdb-src=&#47;home&#47;name&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gdb
</div>2022-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/7d/9f/53dd1d94.jpg" width="30px"><span>筱琲</span> 👍（1） 💬（2）<div>用虚拟机的需要注意下，CPU核数，内存，磁盘，都要尽可能大一些，我设置的是4核&#47;8G&#47;100G，这样才能一路通关。不然要么卡死要么到最后提示空间不足，你连系统都启动不了。</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/8f/abb7bfe3.jpg" width="30px"><span>bubble</span> 👍（1） 💬（2）<div>mkdir -p stamps&#47; &amp;&amp; touch stamps&#47;build-gdb-newlib 卡住一直不动了。
 riscv-gnu-toolchain git:(master) ✗ ps -aux | grep make
root      580153  0.1  0.0  19764  4876 pts&#47;1    S+   15:36   0:00 sudo make -j8
root      580156  0.0  0.0  19764   748 pts&#47;2    Ss   15:36   0:00 sudo make -j8
root      580157  0.0  0.0  11792  2356 pts&#47;2    S+   15:36   0:00 make -j8
paralle+  621310  0.0  0.0  12120  1844 pts&#47;3    S+   15:38   0:00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox make</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/8b/cd/942512cf.jpg" width="30px"><span>吴卫</span> 👍（0） 💬（1）<div>你好，请问你当时使用的riscv-gnu-toolchain是什么版本的？我刚订了你的课程，由于riscv-gnu-toolchain版本更新，所以按照当前的课程指导装不起来。
</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2f/1d/7793e233.jpg" width="30px"><span>gzh4869</span> 👍（0） 💬（1）<div>直接sudo apt install gcc-riscv64-unknown-elf 是不是也行</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/cd/e2/791d0f5e.jpg" width="30px"><span>Geekysl17</span> 👍（0） 💬（1）<div>请问我在ubuntu20上运行sudo make -j8后为什么出现下面的问题啊，怎么解决呢？
Submodule &#39;gcc&#39; (https:&#47;&#47;gcc.gnu.org&#47;git&#47;gcc.git) registered for path &#39;gcc&#39;
Submodule &#39;binutils&#39; (https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git) registered for path &#39;binutils&#39;
Cloning into &#39;&#47;home&#47;ysl&#47;code&#47;OS&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;gcc&#39;...
Submodule &#39;newlib&#39; (https:&#47;&#47;sourceware.org&#47;git&#47;newlib-cygwin.git) registered for path &#39;newlib&#39;
Cloning into &#39;&#47;home&#47;ysl&#47;code&#47;OS&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;binutils&#39;...
Cloning into &#39;&#47;home&#47;ysl&#47;code&#47;OS&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;newlib&#39;...
Submodule &#39;gdb&#39; (https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git) registered for path &#39;gdb&#39;
Cloning into &#39;&#47;home&#47;ysl&#47;code&#47;OS&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;gdb&#39;...
fatal: unable to access &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#47;&#39;: gnutls_handshake() failed: Error in the pull function.
fatal: clone of &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#39; into submodule path &#39;&#47;home&#47;ysl&#47;code&#47;OS&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;binutils&#39; failed
Failed to clone &#39;binutils&#39;. Retry scheduled
</div>2022-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/3c/b4/ca6a958b.jpg" width="30px"><span>miraclezhb</span> 👍（0） 💬（1）<div>&#47;home&#47;miraclezhb&#47;projects&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;riscv-gdb&#47;gdb&#47;ada-exp.y: In function ‘int ada_parse(parser_state*)’:
&#47;home&#47;miraclezhb&#47;projects&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;riscv-gdb&#47;gdb&#47;ada-exp.y:736:15: error: ‘yyin’ was not declared in this scope; did you mean ‘yyrline’?
  736 |   lexer_init (yyin);  &#47;* (Re-)initialize lexer.  *&#47;
      |               ^~~~
      |               yyrline
&#47;home&#47;miraclezhb&#47;projects&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;riscv-gdb&#47;gdb&#47;ada-exp.y:736:3: error: ‘lexer_init’ was not declared in this scope; did you mean ‘pex_init’?
  736 |   lexer_init (yyin);  &#47;* (Re-)initialize lexer.  *&#47;
      |   ^~~~~~~~~~
      |   pex_init

老师我在编译时一直报这个错误，这个该怎么处理啊？</div>2022-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/8f/abb7bfe3.jpg" width="30px"><span>bubble</span> 👍（0） 💬（3）<div>老师我在M1的环境下用虚拟机折腾，一直编译不过去，我可以用其他环境吗？比如直接在M1的环境下学习</div>2022-09-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7mF1Zdh16zKFDsIjV6movCe1vArG6icbr9Bd537NDg7dA6y24LhdC3ypvzqJBW18oGcDeC2yTwDsw/132" width="30px"><span>肖水平</span> 👍（0） 💬（3）<div>sean@sean-VirtualBox:&#47;opt&#47;riscv&#47;gcc&#47;bin$ .&#47;riscv64-minicpu-elf-gcc -v
Using built-in specs.
COLLECT_GCC=.&#47;riscv64-minicpu-elf-gcc
COLLECT_LTO_WRAPPER=&#47;opt&#47;riscv&#47;gcc&#47;libexec&#47;gcc&#47;riscv64-minicpu-elf&#47;10.2.0&#47;lto-wrapper
Target: riscv64-minicpu-elf
Configured with: &#47;home&#47;sean&#47;risc-v&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gcc&#47;configure --target=riscv64-minicpu-elf --prefix=&#47;opt&#47;riscv&#47;gcc --disable-shared --disable-threads --enable-languages=c,c++ --with-pkgversion=gca312387ab1 --with-system-zlib --enable-tls --with-newlib --with-sysroot=&#47;opt&#47;riscv&#47;gcc&#47;riscv64-minicpu-elf --with-native-system-header-dir=&#47;include --disable-libmudflap --disable-libssp --disable-libquadmath --disable-libgomp --disable-nls --disable-tm-clone-registry --src=&#47;home&#47;sean&#47;risc-v&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;riscv-gcc --enable-multilib --with-abi=lp64d --with-arch=rv64imafdc --with-tune=rocket --with-isa-spec=2.2 &#39;CFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39; &#39;CXXFLAGS_FOR_TARGET=-Os   -mcmodel=medlow&#39;
Thread model: single
Supported LTO compression algorithms: zlib
gcc version 10.2.0 (gca312387ab1) 
</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/2c/b27eefc5.jpg" width="30px"><span>Abcd</span> 👍（0） 💬（1）<div>以前玩ARM的时候我记得有crosstool_ng?</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/8f/abb7bfe3.jpg" width="30px"><span>bubble</span> 👍（0） 💬（1）<div>开始构建工作环境了呗</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e1/1a/3c287e37.jpg" width="30px"><span>LooMou</span> 👍（0） 💬（0）<div>window的wsl
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.6 LTS
Release:        20.04
Codename:       focal

我直接 clone github，也可以用 gitee
git clone https:&#47;&#47;github.com&#47;riscv&#47;riscv-gnu-toolchain 
我切换到了 2024.04.12-nightly
git checkout f133b29
不用 clone 其他仓库了，直接按步骤继续，编译成功</div>2024-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0c/46/898e0a18.jpg" width="30px"><span>Hideinsecret</span> 👍（0） 💬（0）<div>riscv-binutils-2.35 启动提示链接失败，升级至2.38重新编译后解决问题</div>2023-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/e9/64/4c721f25.jpg" width="30px"><span>。。。</span> 👍（0） 💬（0）<div>make[2]: Leaving directory &#39;&#47;home&#47;len&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;build-gdb-newlib&#39;
make[1]: *** [Makefile:1000: all] Error 2
make[1]: Leaving directory &#39;&#47;home&#47;len&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;build-gdb-newlib&#39;
make: *** [Makefile:549: stamps&#47;build-gdb-newlib] Error 2
请问老师这是为什么呢</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2f/1d/7793e233.jpg" width="30px"><span>gzh4869</span> 👍（0） 💬（0）<div>我在执行sudo make -j8命令的时候出现这个错误是为啥啊，有大佬能解答下不
make: *** No rule to make target &#39;&#47;root&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;gcc&#39;, needed by &#39;stamps&#47;build-gcc-newlib-stage2&#39;.  Stop.
</div>2023-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/93/72/5e297fdb.jpg" width="30px"><span>l6v3～風</span> 👍（0） 💬（1）<div>编译工具链出现以下错误如何解决：
fatal: unable to access &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#47;&#39;: server certificate verification failed. CAfile: &#47;etc&#47;ssl&#47;certs&#47;ca-certificates.crt CRLfile: none
fatal: 无法克隆 &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#39; 到子模组路径 &#39;binutils&#39;
Makefile:282: recipe for target &#39;&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;binutils&#47;.git&#39; failed
make: *** [&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;binutils&#47;.git] Error 128
make: *** 正在等待未完成的任务....
fatal: unable to access &#39;https:&#47;&#47;sourceware.org&#47;git&#47;newlib-cygwin.git&#47;&#39;: server certificate verification failed. CAfile: &#47;etc&#47;ssl&#47;certs&#47;ca-certificates.crt CRLfile: none
fatal: 无法克隆 &#39;https:&#47;&#47;sourceware.org&#47;git&#47;newlib-cygwin.git&#39; 到子模组路径 &#39;newlib&#39;
Makefile:282: recipe for target &#39;&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;newlib&#47;.git&#39; failed
make: *** [&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;newlib&#47;.git] Error 128
fatal: unable to access &#39;https:&#47;&#47;gcc.gnu.org&#47;git&#47;gcc.git&#47;&#39;: server certificate verification failed. CAfile: &#47;etc&#47;ssl&#47;certs&#47;ca-certificates.crt CRLfile: none
fatal: 无法克隆 &#39;https:&#47;&#47;gcc.gnu.org&#47;git&#47;gcc.git&#39; 到子模组路径 &#39;gcc&#39;
Makefile:282: recipe for target &#39;&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gcc&#47;.git&#39; failed
make: *** [&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gcc&#47;.git] Error 128
fatal: unable to access &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#47;&#39;: server certificate verification failed. CAfile: &#47;etc&#47;ssl&#47;certs&#47;ca-certificates.crt CRLfile: none
fatal: 无法克隆 &#39;https:&#47;&#47;sourceware.org&#47;git&#47;binutils-gdb.git&#39; 到子模组路径 &#39;gdb&#39;
Makefile:282: recipe for target &#39;&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gdb&#47;.git&#39; failed
make: *** [&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gdb&#47;.git] Error 128
</div>2022-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/93/72/5e297fdb.jpg" width="30px"><span>l6v3～風</span> 👍（0） 💬（2）<div>第四步编译工具链sudo make -j8显示make: *** No rule to make target &#39;&#47;home&#47;patrick&#47;RISCV_TOOLS&#47;riscv-gnu-toolchain&#47;build&#47;..&#47;gcc&#39;, needed by &#39;stamps&#47;build-gcc-newlib-stage2&#39;</div>2022-12-29</li><br/>
</ul>