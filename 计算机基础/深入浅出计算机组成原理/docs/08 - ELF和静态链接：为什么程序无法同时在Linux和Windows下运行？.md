过去的三节，你和我一起通过一些简单的代码，看到了我们写的程序，是怎么变成一条条计算机指令的；if…else这样的条件跳转是怎么样执行的；for/while这样的循环是怎么执行的；函数间的相互调用是怎么发生的。

我记得以前，我自己在了解完这些知识之后，产生了一个非常大的疑问。那就是，既然我们的程序最终都被变成了一条条机器码去执行，那为什么同一个程序，在同一台计算机上，在Linux下可以运行，而在Windows下却不行呢？反过来，Windows上的程序在Linux上也是一样不能执行的。可是我们的CPU并没有换掉，它应该可以识别同样的指令呀？

如果你和我有同样的疑问，那这一节，我们就一起来解开。

## 编译、链接和装载：拆解程序执行

[第5节](https://time.geekbang.org/column/article/93359)我们说过，写好的C语言代码，可以通过编译器编译成汇编代码，然后汇编代码再通过汇编器变成CPU可以理解的机器码，于是CPU就可以执行这些机器码了。你现在对这个过程应该不陌生了，但是这个描述把过程大大简化了。下面，我们一起具体来看，C语言程序是如何变成一个可执行程序的。

不知道你注意到没有，过去几节，我们通过gcc生成的文件和objdump获取到的汇编指令都有些小小的问题。我们先把前面的add函数示例，拆分成两个文件add\_lib.c和link\_example.c。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（68） 💬（2）<div>老师，我曾经在linux上使用过wine，有好多window软件不能很好兼容的运行，这是为什么呢？是不是除了执行文件格式之外，还有其他的因素影响软件的运行呢？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（58） 💬（1）<div>Java的跨平台运行是如何做到的呢？跟本节内容有关系吗？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/00/2a248fd8.jpg" width="30px"><span>二星球</span> 👍（31） 💬（4）<div>老师好，就是没有操作系统，直接在硬件上运行的可执行程序，其格式应该不是pe或elf，应该是纯的机器指令吧，pe或elf格式的可执行程序是跟操作系统绑定的，经过翻译后成为纯机器指令，才能被执行，不知道这样理解对不。</div>2019-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/00/2a248fd8.jpg" width="30px"><span>二星球</span> 👍（28） 💬（2）<div>老师好，我有个问题，就是我可以用编程语言写一个不依赖操作系统的可执行程序，这个可执行程序不是pe格式，也不是elf的，那为什能执行呢，是不是因为这个可执行程序全是纯的cpu指令，没有其他要解析的东西？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a4/9c/b32ed9e9.jpg" width="30px"><span>陆离</span> 👍（24） 💬（1）<div>高级语言都是先编译成汇编语言，再汇编成机器码执行的吗？</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（22） 💬（1）<div>补充一下:
ELF其实是一种文件格式的标准，ELF文件有三类:可重定向文件、可执行文件、共享目标文件。代码经过预处理、编译、汇编后形成可重定向文件，可重定向文件经过链接后生成可执行文件。
另外我想请教一下，机器码是在哪一步形成的？</div>2019-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（17） 💬（1）<div>所以理论上，只要不涉及到windows和linux的系统api调用，理论上只要搞定了可执行文件格式这个问题，那么C程序就是二进制可移植的？</div>2019-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Cib5umA0W17N9pichI08pnrXAExdbyh7AVzH4nEhD6KN3FXuELk4LJJuqUPPD7xmIy9nq5Hjbgnzic7sVZG5BKiaUQ/132" width="30px"><span>被过去推开</span> 👍（15） 💬（2）<div>Java的类加载是由jvm完成，大致过程为装载-链接-初始化-运行，所以是jvm帮我们屏蔽了操作系统之间的差异。为了加快程序启动速度，一些类会延迟加载，所以jvm中有很多动态链接。</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/4a/04fef27f.jpg" width="30px"><span>kdb_reboot</span> 👍（9） 💬（1）<div>这里(gcc -g -c add_lib.c link_example.c)需要extern int addd(int a, int b);</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/70/6e/27f43b70.jpg" width="30px"><span>疯狂土豆</span> 👍（8） 💬（2）<div>老师，我非科班出身，现在正在看汇编，像上面的汇编片段，我知道汇编指令，但是汇编指令之前的是什么东西，6b1:   48 89 e5                mov    rbp,中的6b1:   48 89 e5大概是干什么用的，汇编刚刚开始学，像JVM等编译的字节码都有这些东西。只希望可以看懂这些是干什么用的。谢谢老师</div>2019-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ec/2a/b11d5ad8.jpg" width="30px"><span>曾经瘦过</span> 👍（7） 💬（3）<div>mark   后面去读一读 程序员的自我修养</div>2019-05-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqyicZYyW7ahaXgXUD8ZAS8x0t8jx5rYLhwbUCJiawRepKIZfsLdkxdQ9XQMo99c1UDibmNVfFnAqwPg/132" width="30px"><span>程序水果宝</span> 👍（5） 💬（1）<div>为啥通过 gcc 的 -o 参数生成对应的可执行文件后，再执行objdump命令查看到的地址不是从0开始而是从6b0开始</div>2020-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（5） 💬（1）<div>mark 
本章内容确实在链接装载与库里有更详尽的说明。</div>2019-05-13</li><br/><li><img src="" width="30px"><span>lzhao</span> 👍（5） 💬（1）<div>上周五还在思考这个问题？这答案说来就来，及时雨宋江</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/00/9b49f42b.jpg" width="30px"><span>skye</span> 👍（4） 💬（1）<div>老师，嵌入式开发都需要交叉编译，这个是因为CPU的指令集差异，现在什么方法屏蔽这个差异，实现不交叉编译也能实现程序在嵌入式设备上的运行吗？</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/03/11/f58c6278.jpg" width="30px"><span>你好呀</span> 👍（3） 💬（1）<div>整个elf文件都加载到内存吗，还是只加载一部分？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/45/126cd913.jpg" width="30px"><span>袭</span> 👍（2） 💬（1）<div>老师请问下，为什么visua studio里面除了静态库以外还有动态库，以及需要指定额外依赖等？</div>2019-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（1） 💬（1）<div>不是很懂objdump 执行了一下-help命令
objdump -help

  -lazy-bind               - Display mach-o lazy binding info
  -s                       - Display the content of each section
  -section-headers         - Display summaries of the headers for each section.
  -source                  - Display source inlined with disassembly. Implies disassemble object
  -t                       - Display the symbol table
  -weak-bind               - Display mach-o weak binding info


-t 就是符号表吧？
-s 就是每个section的内容
-lazy-bind 就是只有在运行的时候才会链接绑定的吗？
-weak-bind 弱绑定 (emmm 想起了java里面的弱引用， 这个是弱绑定，不敢瞎说)

objdump -source link-example 

link-example:   file format Mach-O 64-bit x86-64

Disassembly of section __TEXT,__text:
__text:
省略 地址 指令 数据

_add:
省略 地址 指令 数据

_main:
省略 地址 指令 数据

Disassembly of section __TEXT,__stubs:
__stubs:
省略 地址 指令 数据

__stub_helper:
省略 地址 指令 数据

-------------------
objdump -s link-example 

link-example:   file format Mach-O 64-bit x86-64

Contents of section __text:

...

Contents of section __stubs:
...

Contents of section __stub_helper:
...

Contents of section __cstring:
...

Contents of section __nl_symbol_ptr:
...

Contents of section __la_symbol_ptr:
...
Contents of section __unwind_info:
...


------

按老师说的，是有这些东西应该。但是具体看不太懂。

嗯 -o是目标文件 不是可执行文件
gcc -o link-example add.o main.o
将目标文件链接之后 才能生成可执行文件
可执行文件里面不仅仅有指令和代码，还有符号表和重定位表。 进一步学习需要看老师推荐的书。</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/27/f2/50ba2f35.jpg" width="30px"><span>憨豆桑</span> 👍（0） 💬（1）<div>大佬你这讲得是静态链接方式吧？动态链接过程又是咋样的，能不能给我补补课？</div>2023-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/fa/2bdf8cc6.jpg" width="30px"><span>指北君</span> 👍（0） 💬（1）<div>老师好，我理解程序要跨平台的痛点是两个操作系统下可执行文件的格式不一样，但是可执行文件都是由高级语言-》汇编-》机器码，然后通过链接生成的，理论上：
1.所有语言都是要生成机器码
2.保证Linux 有兼容 PE 格式的装载器，Windows 有兼容 WSL的装载器
但是现在这两点都是能够保证的，那为啥还有不是跨平台的语言？而且还有什么像Java不依赖操作系统，要自己搞一套JVM来支持跨平台？</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（99） 💬（0）<div>readelf -s link_example.o &#47;&#47;查看符号表
objdump -r link_example.o &#47;&#47;查看重定位表</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（10） 💬（0）<div>茶艺师学编程

关键词

编译 complie
汇编 assemble
链接 link
装载 load
装载器 loader
链接器 linker
目标代码 object program
可执行文件 executable flie

可执行可链接文件 ELF executable and linkable file format
符号表 symbols table 
file header 
.text section 代码段 （code section ）
.data section 数据段
.rel text section 重定位 （relocation  table）
.symbols section 符号表

PE protable executable format</div>2020-11-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXNhbTULKiakib8lYXrvGF2zPwfedooBzC2EtSv1nt1MwV1KUvTkcJrvCBFvcdwJicnr3OEXnk9GUCg/132" width="30px"><span>WENMURAN</span> 👍（7） 💬（1）<div>ELF和静态链接
   在“C语言代码-汇编代码-机器码”的过程中，计算机执行时由两部分组成：一：编译、汇编、链接。二：通过装载器把可执行文件装载到内存中。
   C语言代码&gt;编译器&gt;汇编代码&gt;汇编器&gt;目标文件+静态程序库&gt;链接器&gt;可执行文件&gt;加载器&lt;内存中的过程和数据&lt; CPU
从目标代码到可执行文件的过程中，经过了一道叫ELF的手续，它有个符号表，把之前的函数名变量名等到都保存起来，并且和地址关联起来，ELF文件格式把之前的各种信息分成一个一个section保存起来，包括跳转信息。然后CPU这边的加载器只要根据ELF的格式识别一下就可以直接执行了。
Section还有这些东西：代码段（保存指令），数据段（保存初始化数据信息），重定位表（跳转地址），符号表。
感觉ELF就像再加一层的编译</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（1）<div>老师问一下Mac系统的可执行文件格式是什么，也是ELF吗？还是mac自己有自己一套？</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e1/7a/b206cded.jpg" width="30px"><span>人在江湖龙在江湖</span> 👍（3） 💬（0）<div>这一节可执行文件最好用gdb一步一步调试，最好看看每一步汇编，详细的看看内部一些细节才好。推荐陈皓10年前写的“用GDB调试程序”系列：https:&#47;&#47;blog.csdn.net&#47;haoel&#47;article&#47;details&#47;2879</div>2020-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f0/36/020428c7.jpg" width="30px"><span>Dana</span> 👍（2） 💬（0）<div>Linux 系统 最后可执行为的文件为 ELF</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/21/c5/024e1ef1.jpg" width="30px"><span>X</span> 👍（1） 💬（0）<div>可执行文件通过装载器，将各个指令装载到内存中，cpu通过读取内存中的指令并执行，将执行结果往输出设备输出。</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/21/c5/024e1ef1.jpg" width="30px"><span>X</span> 👍（1） 💬（0）<div>符号表、重定位表。
重定位表里面存放的是一些当前文件找不到的东西。
符号表是当前文件的一些映射信息。
然后通过链接，先将每个文件的符号表链接在一起组成一个更大的符号表（全的）。
这个时候重定位表的数据都可以从这个大而全的符号表里找到对应的了。</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/93/9d/299e4d20.jpg" width="30px"><span>自强不息</span> 👍（1） 💬（0）<div>objdump -r link_example.o &#47;&#47;查看重定位表。为什么必须要重定位？在硬件上留个偏移地址接口，在多放个加法器，不可以吗？重定位应该算改代码吧，代码稳定点不好吗？</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/e1/7a/b206cded.jpg" width="30px"><span>人在江湖龙在江湖</span> 👍（1） 💬（0）<div>通过一个小例子，一步步分析汇编语句，这种讲解静态链接原理，感觉很好</div>2020-11-12</li><br/>
</ul>