你好，我是于航。今天我来和你聊一聊 Wasm 模块的基本组成结构与字节码分析。

在之前的课程中，我们介绍了 Wasm 其实是一种基于“堆栈机模型” 设计的 V-ISA 指令集。在这节课中，我们将深入 Wasm 模块的字节码结构，探究它在二进制层面的基本布局，以及内部各个结构之间的协作方式。

那为什么要探究 Wasm 在二进制层面的基本布局呢？因为在日常的开发实践中，我们通常只是作为应用者，直接将编译好的 Wasm 二进制模块文件，放到工程中使用就完事了，却很少会去关注 Wasm 在二进制层面的具体组成结构。

但其实只有在真正了解 Wasm 模块的二进制组成结构之后，你才能够知道浏览器引擎在处理和使用一个 Wasm 模块时究竟发生了什么。所以今天我们就将深入到这一部分内容中，透过现象看本质，为你揭开 Wasm 模块内部组成的真实面目 —— Section。相信通过这一讲，你能够从另一个角度看到 Wasm 的不同面貌。

## Section 概览

从整体上来看，同 ELF 二进制文件类似，Wasm 模块的二进制数据也是以 Section 的形式被安排和存放的。Section 翻译成中文是“段”，但为了保证讲解的严谨性，以及你在理解上的准确性，后文我会直接使用它的英文名词 Section。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（4） 💬（1）<div>能不能结合 wasm 的可识别文本 来讲解各个  section ？ 这个干讲不是特别形象。

比如 使用  assemblyscript 编译后生成的 wat 文件</div>2020-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/15/886f5c66.jpg" width="30px"><span>Twittytop</span> 👍（2） 💬（1）<div>我有一个疑问，如果一个整数经过编码之后还变大了，那为什么还要编码？为啥不用它原来的大小存储</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（1） 💬（1）<div>对于文中 c++ 编译成 wasm二进制文件，我的疑问在于每个 Section 具体内容的所占字节如何确定呢？我在官网上也没有找到相应的知识。作者能辛苦解答下吗？或者评论区的大佬指导下？</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a9/84/c87b51ce.jpg" width="30px"><span>xiaobang</span> 👍（1） 💬（1）<div>table section 中如果存放的不是anyfunc，调用call indirect 会失败的吧</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/44/00/1676ac9a.jpg" width="30px"><span>忒亚</span> 👍（0） 💬（1）<div>这章好抽象</div>2022-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/60/6f/1a03b508.jpg" width="30px"><span>哄哄</span> 👍（0） 💬（1）<div>据我所知varint32编码的很小的整数仅占用一个字节。1和7编码后不应该是6个字节。</div>2021-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/69/27/b6358f79.jpg" width="30px"><span>champ</span> 👍（0） 💬（3）<div>最后那个例子里面的，payload_len为什么是由5个16进制表示？
我的理解是varuint32，不是应该有32bit，也就是4个16进制数字表示吗？

还有最后的紫色方块由6个16进制数字表示一个函数签名也不太明白</div>2021-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（14） 💬（0）<div>ELF是和特定平台相关的二进制格式。WASM是一个通用的字节码格式，和平台无关，由浏览器的解释器执行</div>2020-09-11</li><br/><li><img src="" width="30px"><span>阿吉学习wasm</span> 👍（3） 💬（0）<div>ELF Section 和 Wasm Section 相同：都采用了线性结构，都有“魔数”和版本号等等。
不同点：ELF是有段和节的划分，多个节构成段。而WASM直接是段。</div>2020-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/33/de01b796.jpg" width="30px"><span>胖狐狸</span> 👍（0） 💬（0）<div>除了其中名为 “Custom Secton”-&gt;除了其中名为 “Custom Section”
发现一个typo</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>还是看得稀里糊涂，对wasm没有理解，但感觉很吸引人。截止到现在有一些疑问：
1. 为啥要把type section和function section这两个分开，按一般的思路会觉得是在一起的，像个头文件。
2. 导入的memory，能被其他wasm模块使用？直接操作其他模块的内存么？应该不可能吧。或者是结合function section，从内存中获取一个函数的返回值？
3. 既然很多语言都支持这套VM，那对于像golang这种有比较重的运行时的语言，运行时部分的功能是如何定义的？是每个golang生成的wasm模块都带一套运行时？还是共享？</div>2023-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/a3/52702576.jpg" width="30px"><span>becky</span> 👍（0） 💬（0）<div>大概看了一下wiki，ELF包含两种视图：program header显示运行时使用的segments，Section header列出section的集合；关于section的信息有code、data和section name，section包含用于链接和重定位的重要数据。
两种section相同处是都有header描述section的信息，以及具体的数据。不同处是elf中用于描述section的header在elf的section header table中，而wasm的header是在section内部；并且elf中的section不用按顺序排列。
对elf不太了解，不知道理解的对不对。</div>2023-08-10</li><br/>
</ul>