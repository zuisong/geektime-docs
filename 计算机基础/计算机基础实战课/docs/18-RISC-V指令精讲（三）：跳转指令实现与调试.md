你好，我是LMOS。

在[第五节课](https://time.geekbang.org/column/article/546957)，我们曾经提到RV32I有两种跳转指令，即无条件跳转指令和有条件的跳转指令。

不过，前面我们只是简单了解了跳转指令长什么样，并没有深入讲解。接下来的两节课，我们就好好研究一下跳转指令的原理，挨个指令做调试。

这节课我们从源头说起，弄明白为什么需要有跳转指令存在，然后再熟悉一下无条件跳转指令。至于有条件跳转指令，我们放在下节课继续学习。这节课代码，你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson18~19)下载。

## 为什么要有跳转指令

我们不妨回忆一下：C语言中if、for、goto等流程控制语句都是如何实现的？还有C语言的函数是如何调用和返回的？

通过前面的学习，我们了解到CPU执行指令是由PC寄存器指向的。每次执行完指令，CPU的PC寄存器就会自动增加一条指令大小的数值，使之指向下一条指令，如此循环，这就导致CPU只能在PC寄存器的引导下顺序地执行指令，而C语言函数就是一条条指令组成的。显然，只靠这样的机制，C语言无法实现流程控制和函数的调用与返回。

如果现在有一种机制，它能够修改CPU里PC寄存器的值，或者根据特定的条件来修改CPU的PC寄存器的值，让PC寄存器能指向特定的内存地址，读取里面的指令并运行。这样，上述问题就会迎刃而解了。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/ae/c3/d930693b.jpg" width="30px"><span>LockedX</span> 👍（1） 💬（1）<div>jal指令只能跳转基于pc寄存器的地址，即pc+x
而jalr可以跳转到自定义寄存器的地址，更加灵活</div>2022-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（1） 💬（1）<div>jalr多了一个源寄存器，既可以与jal交换使用组成类似偏移地址加基地址进行分页跳转（模仿x86，可4kb一个分页），还有一个重要功能就是，jalr的立即数可变为jal的操作码加目标寄存器（实现jalr-jal），jal的立即数可变为jalr的操作码加目标寄存器加功能加源寄存器！
这样设计的好处方便cpu自动化，提升效率（流水线不停转，交替使用减少去内存取指令浪费的时间，方便一次性执行完一个细分项目，如线程）</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/8d/9387b732.jpg" width="30px"><span>贺宾</span> 👍（0） 💬（1）<div>为什么在我的main.c文件中能设置断点，而在jal.S 中却不能设置断点，需要在vscode中安装什么插件吗？</div>2022-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c8/c8/d23a126b.jpg" width="30px"><span>南城忆潇湘</span> 👍（0） 💬（1）<div>老师，请教下，    “我们一旦单步调试，程序代码就会跳到 jal a0，imm_l2 指令处，pc + 12 等于 0x10180，a0 等于 0x10178，”  这一句中的12是怎么计算的，跟前面说的符号扩展怎么对应的，这一点没搞明白， （ “pc = pc + 符号扩展（imm &lt;&lt; 1）”）  这里的imm是什么，左移了一位，是imm左移一位变成了12吗，我是硬看的汇编代码中间隔了3条指令要偏移12</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（0） 💬（1）<div>课后思考题：
jal的立即数只有20位，加上2字节对齐。只能寻址当前指令前后大约1MB的地址空间。
故而有jalr指令存在的必要。（不知道对不对😂）</div>2022-09-05</li><br/>
</ul>