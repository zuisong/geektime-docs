你好，我是LMOS。

上节课，我们通过实现一个获取时间的系统服务，学习了Cosmos里如何建立一个系统服务接口。Cosmos为应用程序提供服务的过程大致是这样的：应用程序先设置服务参数，然后通过int指令进入内核，由Cosmos内核运行相应的服务函数，最后为应用程序提供所需服务。

不知道你是否好奇过业内成熟的Linux内核，又是怎样为应用程序提供服务的呢？

这节课我们就来看看Linux内核是如何实现这一过程的，我们首先了解一下Linux内核有多少API接口，然后了解一下Linux内核API接口的架构，最后，我们动手为Linux内核增加一个全新的API，并实现相应的功能。

下面让我们开始吧！这节课的配套代码你可以从[这里](https://gitee.com/lmos/cosmos/tree/master/lesson42)下载。

## Linux内核API接口的架构

在上节课中，我们已经熟悉了我们自己的Cosmos内核服务接口的架构，由应用程序调用库函数，再由库函数调用API入口函数，进入内核函数执行系统服务。

其实对于Linux内核也是一样，应用程序会调用库函数，在库函数中调用API入口函数，触发中断进入Linux内核执行系统调用，完成相应的功能服务。

在Linux内核之上，使用最广泛的C库是glibc，其中包括C标准库的实现，也包括所有和系统API对应的库接口函数。几乎所有C程序都要调用glibc的库函数，所以**glibc是Linux内核上C程序运行的基础。**
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（10） 💬（1）<div>三、Demo部分
1、新建一个源码编译目录
mkdir kernelbuild

2、下载源码，解压
wget https:&#47;&#47;mirrors.edge.kernel.org&#47;pub&#47;linux&#47;kernel&#47;v5.x&#47;linux-5.10.59.tar.gz   

tar -xzf linux-5.10.59.tar.gz   

cd linux-5.10.59

3、清理
make mrproper

4、修改文件
4.1、arch&#47;x86&#47;entry&#47;syscalls&#47;syscall_64.tbl
#在440后面增加一行
441  common  get_cpus    sys_get_cpus

4.2、include&#47;linux&#47;syscalls.h
#在最后一个asmlinkage增加一行
asmlinkage long sys_get_cpus(void);

4.3、kernel&#47;sys.c  
#在最后一个SYSCALL_DEFINE0后面增加下面几行
&#47;&#47;获取系统中有多少CPU
SYSCALL_DEFINE0(get_cpus)
{
    return num_present_cpus();
}

5、内核配置
make menuconfig
make oldconfig

6、修改.config，去掉一个证书
CONFIG_SYSTEM_TRUSTED_KEYS=“”

7、编译
make -j4

8、安装
sudo make modules_install
sudo make install

9、测试
#include &lt;stdio.h&gt;
#include &lt;unistd.h&gt;
#include &lt;sys&#47;syscall.h&gt;
int main(int argc, char const *argv[])
{
    &#47;&#47;syscall就是根据系统调用号调用相应的系统调用
    long cpus = syscall(441);
    printf(&quot;cpu num is:%d\n&quot;, cpus);&#47;&#47;输出结果
    return 0;
}

gcc  cpus.c -o cpus

.&#47;cpus
在没有修改的内核上返回是-1
在修改过的为num_present_cpus数量，我的虚拟机返回的是1</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（5） 💬（1）<div>二、linux内核部分【下】
2、当产生系统调用时
2.1、应用直接syscall或通过glibc产生了syscall

2.2、cpu会产生类似于中断的效果，开始到entry_SYSCALL_64执行
&#47;&#47;文件路径arch&#47;x86&#47;entry&#47;entry_64.S
SYM_CODE_START(entry_SYSCALL_64)
&#47;&#47;省略代码
call   do_syscall_64
SYM_CODE_END(entry_SYSCALL_64)

&#47;&#47;文件路径arch&#47;x86&#47;entry&#47;entry_64.S
SYM_CODE_START(entry_SYSCALL_compat)
call   do_fast_syscall_32
SYM_CODE_END(entry_SYSCALL_compat)

2.3、调用do_syscall_64
#ifdef CONFIG_X86_64
__visible noinstr void do_syscall_64(unsigned long nr, struct pt_regs *regs)
{
    nr = syscall_enter_from_user_mode(regs, nr);
    instrumentation_begin();
    if (likely(nr &lt; NR_syscalls)) {
        nr = array_index_nospec(nr, NR_syscalls);
        regs-&gt;ax = sys_call_table[nr](regs);
    }
    instrumentation_end();
    syscall_exit_to_user_mode(regs);
}
#endif

2.4、根据sys_call_table调用对应的功能函数
sys_call_table[nr](regs)
如果我们传入257，就会调用__x64_sys_openat
如果我们传入441，就会调用__x64_sys_get_cpus

2.5、但咱们实际写的函数sys_get_cpus，好像和实际调用函数__x64_sys_get_cpus，差了一个__x64，这需要一个wrapper
arch\x86\include\asm\syscall_wrapper.h
#define SYSCALL_DEFINE0(sname)                      \
    SYSCALL_METADATA(_##sname, 0);                  \
    static long __do_sys_##sname(const struct pt_regs *__unused);   \
    __X64_SYS_STUB0(sname)                      \
    __IA32_SYS_STUB0(sname)                     \
    static long __do_sys_##sname(const struct pt_regs *__unused)

#define __X64_SYS_STUB0(name)                       \
    __SYS_STUB0(x64, sys_##name)

#define __SYS_STUB0(abi, name)                      \
    long __##abi##_##name(const struct pt_regs *regs);      \
    ALLOW_ERROR_INJECTION(__##abi##_##name, ERRNO);         \
    long __##abi##_##name(const struct pt_regs *regs)       \
        __alias(__do_##name);

SYSCALL_DEFINE0(get_cpus)，会展开成为
__X64_SYS_STUB0(get_cpus) 
然后
 __SYS_STUB0(x64, sys_get_cpus)
然后
long __x64_sys_get_cpus(const struct pt_regs *regs);

这样前后就对上了，glibc和linux内核就通了。</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（4） 💬（1）<div>一、glibc部分【上】
1、应用程序调用open函数
&#47;&#47;glibc&#47;intl&#47;loadmsgcat.c
# define open(name, flags)  __open_nocancel (name, flags)

2、展开后实际上调用了
__open_nocancel(name, flags)

3、而__open_nocancel 最终调用了INLINE_SYSCALL_CALL
&#47;&#47;glibc&#47;sysdeps&#47;unix&#47;sysv&#47;linux&#47;open_nocancel.c
__open_nocancel(name, flags)
-&gt;return INLINE_SYSCALL_CALL (openat, AT_FDCWD, file, oflag, mode);

4、宏展开【理解就好，不保证顺序】
4.1、初始为
INLINE_SYSCALL_CALL (openat, AT_FDCWD, file, oflag, mode);

4.2、第1次展开INLINE_SYSCALL_CALL
#define INLINE_SYSCALL_CALL(...) \
  __INLINE_SYSCALL_DISP (__INLINE_SYSCALL, __VA_ARGS__)

展开得到：
__INLINE_SYSCALL_DISP(__INLINE_SYSCALL, __VA_ARGS__【openat, AT_FDCWD, file, oflag, mode】)

4.3、第2次展开__INLINE_SYSCALL_DISP
#define __INLINE_SYSCALL_DISP(b,...) \
  __SYSCALL_CONCAT (b,__INLINE_SYSCALL_NARGS(__VA_ARGS__))(__VA_ARGS__)

展开得到：
__SYSCALL_CONCAT(b【__INLINE_SYSCALL】,__INLINE_SYSCALL_NARGS(__VA_ARGS__【openat, AT_FDCWD, file, oflag, mode】))(__VA_ARGS__【openat, AT_FDCWD, file, oflag, mode】)

4.4、第3次展开__INLINE_SYSCALL_NARGS
__INLINE_SYSCALL_NARGS(__VA_ARGS__【openat, AT_FDCWD, file, oflag, mode】)

#define __INLINE_SYSCALL_NARGS(...) \
  __INLINE_SYSCALL_NARGS_X (__VA_ARGS__,7,6,5,4,3,2,1,0,)

展开得到：
__INLINE_SYSCALL_NARGS_X(openat, AT_FDCWD, file, oflag, mode,7,6,5,4,3,2,1,0,)

然后展开__INLINE_SYSCALL_NARGS_X
#define __INLINE_SYSCALL_NARGS_X(a,b,c,d,e,f,g,h,n,...) n

展开得到参数个数：4

从而4.4的结果为
__SYSCALL_CONCAT(__INLINE_SYSCALL,4)(__VA_ARGS__【openat, AT_FDCWD, file, oflag, mode】)

4.5、然后展开__SYSCALL_CONCAT，其实就是字符拼接
__SYSCALL_CONCAT(__INLINE_SYSCALL,4)

#define __SYSCALL_CONCAT_X(a,b)     a##b
#define __SYSCALL_CONCAT(a,b)       __SYSCALL_CONCAT_X (a, b)

展开得到：
__INLINE_SYSCALL4

从而4.5的结果为
__INLINE_SYSCALL4(openat, AT_FDCWD, file, oflag, mode)

4.6、然后展开INTERNAL_SYSCALL4
#define __INLINE_SYSCALL4(name, a1, a2, a3, a4) \
  INLINE_SYSCALL (name, 4, a1, a2, a3, a4)

展开得到：
INLINE_SYSCALL(openat, 4, AT_FDCWD, file, oflag, mode)</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（3） 💬（1）<div>二、linux内核部分【上】
1、在make时，会通过syscall_64.tbl生成syscalls_64.h，然后包含到syscall_64.c，进行调用号与函数之间的绑定。
arch&#47;x86&#47;entry&#47;syscalls&#47;syscall_64.tbl
arch&#47;x86&#47;include&#47;generated&#47;asm&#47;syscalls_64.h
arch&#47;x86&#47;entry&#47;syscall_64.c

1.1、以sys_openat为例，在syscall_64.tbl中为
257    common    openat            sys_openat
441    common    get_cpus          sys_get_cpus

1.2、make后，在生成的syscalls_64.h中为
__SYSCALL_COMMON(257, sys_openat)

1.3 在syscall_64.c中，展开__SYSCALL_COMMON
#define __SYSCALL_COMMON(nr, sym) __SYSCALL_64(nr, sym)
展开就是
__SYSCALL_64(257, sys_openat)

1.4、在syscall_64.c中，第一次展开__SYSCALL_64
#define __SYSCALL_64(nr, sym) extern long __x64_##sym(const struct pt_regs *);
#include &lt;asm&#47;syscalls_64.h&gt;
#undef __SYSCALL_64
展开就是
extern long __x64_sys_openat(const struct pt_regs *);
也就是每个__SYSCALL_64都展开成了一个外部函数

1.5、在syscall_64.c中，第二次展开__SYSCALL_64
#define __SYSCALL_64(nr, sym) [nr] = __x64_##sym,

asmlinkage const sys_call_ptr_t sys_call_table[__NR_syscall_max+1] = {
    [0 ... __NR_syscall_max] = &amp;__x64_sys_ni_syscall,
#include &lt;asm&#47;syscalls_64.h&gt;
};

展开其实就是指向了外部函数
[257]=__x64_sys_openat,

全部展开结果，都会被包含到sys_call_table中，从而完成了调用号与函数之间的绑定。</div>2021-08-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI3F4IdQuDZrhN8ThibP85eCiaSWTYpTrcC6QB9EoAkw3IIj6otMibb1CgrS1uzITAnJmGLXQ2tgIkAQ/132" width="30px"><span>cugphoenix</span> 👍（2） 💬（1）<div>看了Linux 系统调用表的生成方式，又刷新了对宏定义的认知，灵活性极强，用起来可太花哨了</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/b3/ac/2c8baa5e.jpg" width="30px"><span>Zhendicai</span> 👍（2） 💬（1）<div>int指令和syscall指令都会发生特权级切换吧，但是syscall能直接调定位到具体系统调用函数，int则需要经过中断门描述符表和分发器才行。int的步骤要多一些，那就是取指令次数要多一些？还有个问题使用int来执行系统调用是不是也会遇到中断优先级的问题？</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（2） 💬（1）<div>搬了下答案
1.syscall
syscall是x64的系统调用。其调用号通过rax进行传递。查看具体的调用号，linux环境下在unistd.h中定义。如果是64位，则可以查看&#47;usr&#47;include&#47;asm&#47;unistd_64.h，如果是32位，则查看&#47;usr&#47;include&#47;unistd_32.h。

参数传递：处于用户态时，参数传递顺序为：rdi，rsi，rdx，rcx，r8，r9，处于内核态时，参数传递顺序：rdi，rsi，rdx，r10，r8，r9（补充：这是看别人文章是这么写的，但是我在实际操作中发现，我运行用户态汇编代码，通过rcx传递参数时函数返回错误，用ida查看，发现用户态的值传递其实是：rdi，rsi，rdx，r10，r8，r9（和前面提到的内核态的一致），内核的值传递我没有进行测试，欢迎各位大佬评论区补充）

2.int 80h
int 80h 是32位x86的系统调用方式。同样通过ax传递调用号，参数传递顺序是：ebx，ecx，edx，esi，edi

*** note ***
intel体系的系统调用限制最多六个参数，没有任何一个参数是通过栈传递的。系统调用的返回结果存放在ax寄存器中，且只有整型和内存型可以传递给内核
</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f4/48/2242bed9.jpg" width="30px"><span>吴建平</span> 👍（1） 💬（1）<div>有个疑问，最后验证的应用例子，怎么链接到系统调用的呢，没看到链接过程，默认链接glibc么？</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（0） 💬（1）<div>因为这里用到的指令是最新处理器为其设计的系统调用指令 syscall。这个指令和 int 指令一样，都可以让 CPU 跳转到特定的地址上，只不过不经过中断门，系统调用返回时要用 sysexit 指令</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（0） 💬（1）<div>实验太顶了，有时间一定搞一下，今天问题属于知识盲区，贴上链接：https:&#47;&#47;blog.csdn.net&#47;sdulibh&#47;article&#47;details&#47;50890250

不学习就变废物😂</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>syscall应该是系统与应用软件的接口？类似win系统的消息模块？int是操作系统与硬件的接口？如新插入usb鼠标？</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（3） 💬（0）<div>一、glibc部分【下】
4.7、展开INLINE_SYSCALL
&#47;&#47;glibc&#47;sysdeps&#47;unix&#47;sysv&#47;linux&#47;sysdep.h
#define INLINE_SYSCALL(name, nr, args...)       \
  ({                  \
    long int sc_ret = INTERNAL_SYSCALL (name, nr, args);    \
    __glibc_unlikely (INTERNAL_SYSCALL_ERROR_P (sc_ret))    \
    ? SYSCALL_ERROR_LABEL (INTERNAL_SYSCALL_ERRNO (sc_ret))   \
    : sc_ret;               \
  })

展开得到
INTERNAL_SYSCALL (openat, 4, args【AT_FDCWD, file, oflag, mode】);  

4.8、展开INTERNAL_SYSCALL
#define INTERNAL_SYSCALL(name, nr, args...)       \
  internal_syscall##nr (SYS_ify (name), args)

展开得到
internal_syscall4(SYS_ify(openat), args【AT_FDCWD, file, oflag, mode】)

展开 SYS_ify(openat)
#define SYS_ify(syscall_name) __NR_##syscall_name
得到
__NR_openat

从而得到
internal_syscall4(__NR_openat, args【AT_FDCWD, file, oflag, mode】)

4.9、最后internal_syscall4中，汇编调用了syscall

glibc\sysdeps\unix\sysv\linux\x86_64\64\arch-syscall.h
#define __NR_openat 257

syscall时，先传入调用号257，然后是四个位真正的参数。</div>2021-08-17</li><br/>
</ul>