你好，我是于航，目前在 PayPal 做软件研发与技术管理工作。

也许一些同学对我比较熟悉，我之前曾在极客时间开设过一门《WebAssembly 入门课》，并且还是多个 WebAssembly、C++ 相关每日一课视频的作者。而今天，我又设计了一门新课，想要带你从不同的视角来学习 “C” 这门语言。

我相信来学习这门课的大部分同学，都或多或少接触过一些 C 语言的基础知识。但是，我认为掌握 C 语言的基本语法并不困难，更重要的是能够灵活、高效地使用这门语言，并**通过观察语言背后机器的执行细节，来深入了解关于编译优化、程序执行，以及计算机体系结构等其他相互关联的知识**。

作为 WebAssembly 技术的研究者和使用者，C 语言是我在工作中使用最多的语言之一。由于C 语言语法简单、抽象层次较低，我能够通过它在进行原型验证时精确地控制程序的运行状态。另一方面，在接触操作系统、Unix 系统编程、语言运行时，以及系统库等相关内容时，我更深切地感受到了解 C 语言对于深入理解这些内容的重要性。

因此，这门课将不会介绍 C 语言的语法细节，而是结合 C 核心语法、汇编代码，以及计算机体系结构等相关知识，来**讲述 C 语言、应用程序和操作系统三者之间的协作关系。**
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/8a/af/ea72650f.jpg" width="30px"><span>EC-hero</span> 👍（23） 💬（1）<div>老师，“如下图所示，这里，左右两个窗口中相同背景颜色的代码行，表示了 C 代码与其对应的汇编代码。可以看到，左侧 C 代码中第三行变量 x 的值被存放到了 ebx 寄存器中”     是用什么软件看的？</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d6/43/0704d7db.jpg" width="30px"><span>cc</span> 👍（13） 💬（4）<div>想了解一些关于 「C 语言为什么设计成现在这样」的内容。

之前学过 Java 和 Go，自己看了一段时间的 C 语言，比如对 C 语言的函数声明就觉得很难读，后来看了一些资料，只要掌握“声明的语法和使用的语法类似”这一点，就比较容易看懂函数声明了。

最近还在继续学 C 语言，遇到的一个困惑就是，为什么 C 语言需要有头文件，而其他接触到的语言都没有这个概念
</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8e/10/10092bb1.jpg" width="30px"><span>Luke</span> 👍（10） 💬（1）<div>好早以前搞的os实验，看到那段at&amp;t 汇编好亲切。
老师的代码等价于：

dst =src；
dst = dst + 1；

结果打印出来就是2

%1表示第二个参数，$1是立即数1。
rbp是栈的基指针，rsp是栈顶指针。
但愿没记错，哈哈。</div>2021-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/10/65fe5b06.jpg" width="30px"><span>J²</span> 👍（10） 💬（1）<div>感觉C不太容易学好</div>2021-12-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK9Yvy5STDw874VEEuPehIcONR9kEq7knIicUNuINU0ovf2ViabhFqiabZiaoXC5FqL89YDCxp3tBnFzA/132" width="30px"><span>Geek_5b2ab1</span> 👍（6） 💬（1）<div>老师你好，请问由c生成的汇编代码是平台无关的吗？之前学过arm汇编，对于arm汇编，有专门的pdf文件，讲解每条指令的作用。我看c生成的汇编代码好像不是arm汇编。
那由c生成的汇编代码是基于什么指令集的呢，有没有什么文档可以查看每条指令的介绍？</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/42/df/a034455d.jpg" width="30px"><span>罗耀龙@坐忘</span> 👍（5） 💬（1）<div>茶艺师学编程

来极客时间学的第一门语言就是C。

现在出了这门课，闭着眼睛就冲进来了。</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/8c/373d4027.jpg" width="30px"><span>龍蝦</span> 👍（4） 💬（1）<div>老师，关于最近 Linux 5.18 将升级到 C11 的消息，能否详细解释下呢？
这个升级，具体要如何实施呢？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/89/34f2cbcc.jpg" width="30px"><span>杨宇</span> 👍（3） 💬（1）<div>看到C89、C11这种命名，想起了千年虫。到了2089年，会怎样？</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/48/a3/92027340.jpg" width="30px"><span>Alan_Hwang</span> 👍（3） 💬（1）<div>于老师，散发着艺术的气息。我选C，和大家一起学C</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/31/c1ce2abc.jpg" width="30px"><span>糊糊</span> 👍（3） 💬（1）<div>这次一定坚持下去，学懂</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/3f/92/f4a1c192.jpg" width="30px"><span>GO</span> 👍（2） 💬（1）<div>老师，我想问问，因为要对C语言的本质进行相应的分析，所以汇编语言也会相应的了解，那么这门课程讲的汇编语言会涉及到哪种程度呢？
因为我虽然是计算机专业，但是学校不开汇编这门课程了，请老师解答，谢谢！</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/e9/c5/496bdd2a.jpg" width="30px"><span>再不睡觉就秃了</span> 👍（2） 💬（1）<div>冲</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/f7/7a/73e705a2.jpg" width="30px"><span>代码界的小白</span> 👍（1） 💬（1）<div>小白要开始学习C语言了</div>2022-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ed/44/4399a41a.jpg" width="30px"><span>墨</span> 👍（1） 💬（1）<div>汇编所做的事情:
1.dst = src
2.dst = src + 1
所以输出 dst 为 2</div>2021-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（1） 💬（3）<div>```c

#include &lt;stdio.h&gt;
int main(void) {
  int src = 1;
  int dst;
  asm (&quot;mov %1, %0\n\t&quot;
       &quot;add $1, %0&quot;
       : &quot;=r&quot; (dst)
       : &quot;r&quot; (src));
  printf(&quot;%d\n&quot;, dst);
}
```
上述代码，执行结果是2</div>2021-12-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoib6BjEV4KPEaIdlLEfoVFRCxCSlL2XaIVDiaakvjhWEibibym323ZeHXAY46JMO3nSHmjiaWtAY47eww/132" width="30px"><span>dobby</span> 👍（0） 💬（1）<div>老师请问C语言入门。基础知识有什么资料推荐的呢？</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/53/ade0afb0.jpg" width="30px"><span>ub8</span> 👍（0） 💬（1）<div>头像很像王菲</div>2022-04-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLBFkSq1oiaEMRjtyyv4ZpCI0OuaSsqs04ODm0OkZF6QhsAh3SvqhxibS2n7PLAVZE3QRSn5Hic0DyXg/132" width="30px"><span>ddh</span> 👍（0） 💬（1）<div>冲~~~</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/03/eba78e43.jpg" width="30px"><span>风清扬</span> 👍（0） 💬（2）<div>#include &lt;stdio.h&gt;

int main()
{
    register int x = 1;
    int y = 2;
}  
上面的代码在https:&#47;&#47;godbolt.org&#47;中生成的汇编为什么是这样的？和文章中的不一样
main:
        push    rbp
        mov     rbp, rsp
        mov     DWORD PTR [rbp-4], 2
        mov     eax, 0
        pop     rbp
        ret</div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/32/27/25501d3e.jpg" width="30px"><span>沉默王二</span> 👍（21） 💬（5）<div>好了，我来学习C语言了，永远滴神</div>2021-12-06</li><br/><li><img src="" width="30px"><span>Y</span> 👍（7） 💬（0）<div>使用C语言很多年， 一直向深入理解C和编译和运行底层原理，这个课程早上点就更好了</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/84/4a/50940078.jpg" width="30px"><span>卢承灏</span> 👍（7） 💬（0）<div>我正是因为学了go，所以我想学好C</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/a1/efcf7306.jpg" width="30px"><span>森林</span> 👍（3） 💬（0）<div>对于我们而言，C是基本功。</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/2c/b5/10141329.jpg" width="30px"><span>杰良</span> 👍（2） 💬（1）<div>深入系统与芯片的精确控制能力，从而获得高效的运行性能。简洁的语法设计，也实现了精确控制的同时拥有高层次抽血的能力。</div>2021-12-14</li><br/><li><img src="" width="30px"><span>Geek_b80486</span> 👍（1） 💬（0）<div>个人拙见，之前一直在学习arm汇编，对asm()那段代码始终理解不了，原来linux&#47;unix下内联汇编为AT&amp;T格式，%0为dst，1%为src，mov 1% 0%是将将1%的内容赋给0%，即dst = src，在此处纠结了许久，查阅资料才搞清楚，后面的代码就容易理解了。</div>2022-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/a7/ef93de5c.jpg" width="30px"><span>西北望</span> 👍（1） 💬（0）<div>报名啦</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/af/29/6cbdf6e0.jpg" width="30px"><span>欧阳</span> 👍（1） 💬（0）<div>来学习了</div>2021-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/3f/a8/cdbab84b.jpg" width="30px"><span>🇨 🇦 🇳 🇾 🇴 🇳</span> 👍（0） 💬（0）<div>两年前买的课程还没看过，现在开始学了</div>2023-04-20</li><br/>
</ul>