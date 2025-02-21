你好，我是李兵。

在上一节我们分析了V8的运行时环境，准备好了运行时环境，V8就可以执行JavaScript代码了。在执行代码时，V8需要先将JavaScript编译成字节码，然后再解释执行字节码，或者将需要优化的字节码编译成二进制，并直接执行二进制代码。

也就是说，V8首先需要将JavaScript**编译**成字节码或者二进制代码，然后再**执行**。

在后续课程中，我们会分析V8如何解释执行字节码，以及执行编译好的二进制代码，不过在分析这些过程之前，我们需要了解最基础的知识，那就是CPU如何执行二进制代码。

因为字节码的执行模式和CPU直接执行二进制代码的模式是类似的，了解CPU执行二进制代码的过程，后续我们分析字节码的执行流程就会显得比较轻松，而且也能加深我们对计算机底层工作原理的理解。

今天我们就要来分析下二进制代码是怎么被CPU执行的，在编译流水线中的位置你可以参看下图：

![](https://static001.geekbang.org/resource/image/a2/a2/a20dec9ec8a84c8519dd1c4a18c2dda2.jpg?wh=2284%2A1285 "CPU执行二进制代码")

## 将源码编译成机器码

我们以一段C代码为例，来看一下代码被编译成二进制可执行程序之后，是如何被CPU执行的。

在这段代码中，只是做了非常简单的加法操作，将x和y两个数字相加得到z，并返回结果z。

```
int main()
{  
    int x = 1;
    int y = 2;
    int z = x + y;
    return z;
}
```

我们知道，CPU并不能直接执行这段C代码，而是需要对其进行编译，将其转换为二进制的机器码，然后CPU才能按照顺序执行编译后的机器码。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/50/656a0012.jpg" width="30px"><span>王楚然</span> 👍（41） 💬（1）<div>1. 二进制代码装载进内存，系统会将第一条指令的地址写入到 PC 寄存器中。
2. 读取指令：根据pc寄存器中地址，读取到第一条指令，并将pc寄存器中内容更新成下一条指令地址。
3. 分析指令：并识别出不同的类型的指令，以及各种获取操作数的方法。
4. 执行指令：由于cpu访问内存花费时间较长，因此cpu内部提供了通用寄存器，用来保存关键变量，临时数据等。指令包括加载指令，存储指令，更新指令，跳转指令。如果涉及加减运算，会额外让ALU进行运算。
5. 指令完成后，通过pc寄存器取出下一条指令地址，并更新pc寄存器中内容，再重复以上步骤。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/40/e6d4c1b4.jpg" width="30px"><span>ChaoZzz</span> 👍（11） 💬（7）<div>不理解为什么要 movl  $0, -4(%rbp) 把 0 写进栈帧</div>2020-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/ea/38c063d5.jpg" width="30px"><span>OnE</span> 👍（5） 💬（3）<div>“movl  $0, -4(%rbp)”这条指令并不是“在栈中把返回值默认设置为0”，一般情况下函数不是通过eax来返回值？那为什么还要多此一举呢？感觉这一条指令的存在像是编译器的默认做法，可能是出于安全考虑。</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/74/7dd9c65e.jpg" width="30px"><span>亦枫丶</span> 👍（1） 💬（1）<div>“现在 x+y 的结果保存在了 eax 中了，接下来 CPU 会将结果保存中内存中” ，老师这里的内存是不是应该是寄存器呀，还是说这个结果确实写到了内存？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/35/35/9c5eb2c2.jpg" width="30px"><span>Prof.Bramble</span> 👍（3） 💬（2）<div>老师，我想问问关于全局执行上下文，如果它是存放在堆中的，那全局变量里面的基础类型的值，也在堆中吗？还是基础类型的值依然通过某种映射保存在栈中？

我个人更希望理解成是在堆中，主要产生这个问题的原因是我好奇全局变量的声明数量是否会影响栈空间的容量，还是说栈中保存的全局执行上下文只是一个指向栈存储位置的指针？</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/26/e0bd8d24.jpg" width="30px"><span>Crystal</span> 👍（1） 💬（0）<div>关于内存寄存器推荐《汇编语言》 王爽，入门级教程，很受用</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/15/8db238ac.jpg" width="30px"><span>神仙朱</span> 👍（1） 💬（1）<div>更新地址到pc寄存器，好像是存指令开头的地址，怎么知道这条指令到哪里结束，也就是结尾地址呢</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/67/01/313652c2.jpg" width="30px"><span>馒头爱学习</span> 👍（0） 💬（0）<div>上大学的时候，觉得学习汇编没什么用处，现在终于找到用武之地了，感谢老师！</div>2022-01-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBUFdN3p3KvwsAeYltGbenNFPmIJ1tdXVGkVkkibKs1n12Brd1iae5BNXnW8HKSYX8bTtSqrpeuJUw/132" width="30px"><span>Geek_bb5943</span> 👍（0） 💬（0）<div>到这里留言的人比较少，我也来聊聊吧。代码到二进制代码，经过ast语法解析，再到字节码，在到机器码，也就是二进制代码，二进制代码会被写入内存，被写入到pc寄存器，后面通过读取寄存器里的指令并分析执行，就可以啦！不知道理解有没有错</div>2020-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/88/2e/db17801a.jpg" width="30px"><span>灰的更高</span> 👍（0） 💬（0）<div>老师，我对于指令存储的内存地址的想法，您看是否正确。因为文中指令间的内存地址以字节为单位，相差四个字节，就表示系统或汇编器为32位，32位的十六进制地址应该是8位，若以字节为单位，也就变成9位地址，是否可以这样理解？</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（0） 💬（0）<div>我记得有逻辑地址和物理地址。</div>2020-04-17</li><br/><li><img src="" width="30px"><span>Geek_177f82</span> 👍（0） 💬（0）<div>程序加载进内存后，第一条指令更新到pc寄存器。当该指令取后需要做两件事。1、更新下一条指令地址到pc寄存器；2、分析当前指令。那我的理解是，每次cpu时钟周期开始的第一个阶段（取出指令）的时候，就开始更新下一条指令的pc寄存器，那么这个时候当前指令还没执行。那么跳转指令怎么更新的呢？（我的理解是当前指令必须先执行，才会把需要跳转指令的地址更新到pc寄存器。）</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bb/61/2c2f5024.jpg" width="30px"><span>haijian.yang</span> 👍（0） 💬（0）<div>老师，在 Node.js 中，V8 是什么时候执行 JS 代码的，是在事件循环中吗？因为上一节课说到 V8 和事件循环在同一个线程中。</div>2020-04-10</li><br/>
</ul>