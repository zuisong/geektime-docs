在开发软件的过程中我们经常会遇到错误，如果你用Google搜过出错信息，那你多少应该都访问过[Stack Overflow](https://stackoverflow.com/)这个网站。作为全球最大的程序员问答网站，Stack Overflow的名字来自于一个常见的报错，就是栈溢出（stack overflow）。

今天，我们就从程序的函数调用开始，讲讲函数间的相互调用，在计算机指令层面是怎么实现的，以及什么情况下会发生栈溢出这个错误。

## 为什么我们需要程序栈？

和前面几讲一样，我们还是从一个非常简单的C程序function\_example.c看起。

```
// function_example.c
#include <stdio.h>
int static add(int a, int b)
{
    return a+b;
}


int main()
{
    int x = 5;
    int y = 10;
    int u = add(x, y);
}
```

这个程序定义了一个简单的函数add，接受两个参数a和b，返回值就是a+b。而main函数里则定义了两个变量x和y，然后通过调用这个add函数，来计算u=x+y，最后把u的数值打印出来。

```
$ gcc -g -c function_example.c
$ objdump -d -M intel -S function_example.o
```

我们把这个程序编译之后，objdump出来。我们来看一看对应的汇编代码。

```
int static add(int a, int b)
{
   0:   55                      push   rbp
   1:   48 89 e5                mov    rbp,rsp
   4:   89 7d fc                mov    DWORD PTR [rbp-0x4],edi
   7:   89 75 f8                mov    DWORD PTR [rbp-0x8],esi
    return a+b;
   a:   8b 55 fc                mov    edx,DWORD PTR [rbp-0x4]
   d:   8b 45 f8                mov    eax,DWORD PTR [rbp-0x8]
  10:   01 d0                   add    eax,edx
}
  12:   5d                      pop    rbp
  13:   c3                      ret    
0000000000000014 <main>:
int main()
{
  14:   55                      push   rbp
  15:   48 89 e5                mov    rbp,rsp
  18:   48 83 ec 10             sub    rsp,0x10
    int x = 5;
  1c:   c7 45 fc 05 00 00 00    mov    DWORD PTR [rbp-0x4],0x5
    int y = 10;
  23:   c7 45 f8 0a 00 00 00    mov    DWORD PTR [rbp-0x8],0xa
    int u = add(x, y);
  2a:   8b 55 f8                mov    edx,DWORD PTR [rbp-0x8]
  2d:   8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
  30:   89 d6                   mov    esi,edx
  32:   89 c7                   mov    edi,eax
  34:   e8 c7 ff ff ff          call   0 <add>
  39:   89 45 f4                mov    DWORD PTR [rbp-0xc],eax
  3c:   b8 00 00 00 00          mov    eax,0x0
}
  41:   c9                      leave  
  42:   c3                      ret    
```

可以看出来，在这段代码里，main函数和上一节我们讲的的程序执行区别并不大，它主要是把jump指令换成了函数调用的call指令。call指令后面跟着的，仍然是跳转后的程序地址。

这些你理解起来应该不成问题。我们下面来看一个有意思的部分。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/4a/04fef27f.jpg" width="30px"><span>kdb_reboot</span> 👍（59） 💬（8）<div>倒数第二图比较好 
补充一下寄存器说明
rbp - register base pointer (start of stack)
rsp - register stack pointer (current location in stack, growing downwards)
建议将图编号这样评论的时候也能有所指代</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/f6/ed66d1c1.jpg" width="30px"><span>chengzise</span> 👍（46） 💬（2）<div>老师这里需要补冲一下，函数调用call指令时，（PC）指令地址寄存器会自动压栈，即返回地址压栈，函数返回ret指令时会自动弹栈，即返回地址赋值给PC寄存器，把之前。图片有显示压栈，没有文字说明，其他同学可以不太理解。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（30） 💬（2）<div>现在有点模糊的是栈只是用来做函数调用，记录跳转地址的？它和寄存器的本质区别吗？这两者能给解释一下吗？谢谢！</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（20） 💬（5）<div>push rbp；
mov rbp rsp；
老师，想问这两句是如何控制函数调用的</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（17） 💬（2）<div>老师 巨大数组为什么是分配在栈空间的呢？（java里面是分配到堆上的 c预约和java不同吗）</div>2019-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/1f/6bc10297.jpg" width="30px"><span>Allen</span> 👍（17） 💬（2）<div>int main()
{
   d:   55                      push   ebp
   e:   89 e5                   mov    ebp,esp
  10:   83 ec 18                sub    esp,0x18
    int x = 5;
  13:   c7 45 f4 05 00 00 00    mov    DWORD PTR [ebp-0xc],0x5
    int y = 10;
  1a:   c7 45 f8 0a 00 00 00    mov    DWORD PTR [ebp-0x8],0xa

老师，请教下：
   sub    esp,0x18  的目的是干什么？ 0x18 是怎么计算的？
</div>2019-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/2c/83/f85ba9cd.jpg" width="30px"><span>once</span> 👍（14） 💬（4）<div>老师 call指令已经将pc寄存器里的下一个指令（add函数执行完的跳转地址）压栈了 那 add函数里面的 push rbp压的又是什么栈 还有把main函数从栈底压到栈顶这个是什么意思 没有图看了好几遍也懵懵的 help老师</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（9） 💬（1）<div>java程序应该不是那种分页的形式，在虚机起动的时候我们根据配置或者是起动参数指定需要的内存大小，应该是预先分配好一大段连续的内存供程序使用，所以在程序运行过程中如果超出啦，预分配大小的内存就会出现内存溢出的错误</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/66/3f49793e.jpg" width="30px"><span>小猪</span> 👍（9） 💬（8）<div>老师，我觉得用goto就可以实现函数调用，起先跳转到函数，运行完，在用goto跳回来就行了</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c7/96/19149e9e.jpg" width="30px"><span>Alphalin</span> 👍（7） 💬（2）<div>请问地址34后面的地址怎么直接到39了？ 35地址在哪呢</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1e/63/d5909105.jpg" width="30px"><span>小李同学</span> 👍（6） 💬（1）<div>老师，栈是按照线程进行区分的吗？那个线程都有各自对应的栈吗？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/5a/377dc4bf.jpg" width="30px"><span>大给给</span> 👍（5） 💬（1）<div>买了好多课之后感觉最值的课程，深入浅出；另外问老师个问题，inline会提升程序的性能，根本原因是直接替换不需要让栈帧入栈出栈对门？那可不可以理解为这里比较耗性能的地方是入栈出栈操作？</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/9d/d91dc762.jpg" width="30px"><span>喜欢吃鱼</span> 👍（4） 💬（1）<div>谢谢老师的回复，我忘了贴代码了，需要优化的代码如下.网上说把大的for循环写里面是为了提高CPU流水线的分支预测的准确率，但是我对这个不是很清楚。
for（i=0;i&lt;1000;i++）{
        for（j=0;j&lt;100;j++）{
                for（k=0;k&lt;10;k++）{
                       printf(“%d”,i+j+k);
                }
        }
}</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（4） 💬（1）<div>0x0000000000400508 &lt;+0&gt;:     push   %rbp
0x0000000000400509 &lt;+1&gt;:     mov    %rsp,%rbp
0x000000000040050c &lt;+4&gt;:     sub    $0x18,%rsp
0x0000000000400510 &lt;+8&gt;:     movl   $0x1,-0x4(%rbp)
0x0000000000400517 &lt;+15&gt;:    movl   $0x2,-0x8(%rbp)
0x000000000040051e &lt;+22&gt;:    mov    -0x8(%rbp),%esi
0x0000000000400521 &lt;+25&gt;:    mov    -0x4(%rbp),%eax
0x0000000000400524 &lt;+28&gt;:    movl   $0x7,(%rsp)
=&gt; 0x000000000040052b &lt;+35&gt;:    mov    $0x6,%r9d
 0x0000000000400531 &lt;+41&gt;:    mov    $0x5,%r8d
 0x0000000000400537 &lt;+47&gt;:    mov    $0x4,%ecx
 0x000000000040053c &lt;+52&gt;:    mov    $0x3,%edx
 0x0000000000400541 &lt;+57&gt;:    mov    %eax,%edi
 0x0000000000400543 &lt;+59&gt;:    callq  0x4004cd &lt;add&gt;
 0x0000000000400548 &lt;+64&gt;:    mov    %eax,-0xc(%rbp)
 0x000000000040054b &lt;+67&gt;:    mov    $0x0,%eax
 0x0000000000400550 &lt;+72&gt;:    leaveq
 0x0000000000400551 &lt;+73&gt;:    retq
(gdb) i r
rcx            0x400560 4195680
rdx            0x7fffffffe4e8   140737488348392
rbp            0x7fffffffe3f0   0x7fffffffe3f0
rsp            0x7fffffffe3d8   0x7fffffffe3d8
r12            0x4003e0 4195296
r13            0x7fffffffe4d0   140737488348368
r14            0x0      0
r15            0x0      0
rip            0x40052b 0x40052b &lt;main+35&gt;
eflags         0x216    [ PF AF IF ]
cs             0x33     51
ss             0x2b     43
ds             0x0      0
es             0x0      0
fs             0x0      0
gs             0x0      0
(gdb) x&#47;24x $rbp
0x7fffffffe3f0: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x7fffffffe3f8: 0xd5    0x03    0xa3    0xf7    0xff    0x7f    0x00    0x00
0x7fffffffe400: 0x00    0x00    0x00    0x00    0x00    0x00    0x00    0x00
(gdb) x&#47;24x ($rbp-24)
0x7fffffffe3d8: 0x07    0x00    0x00    0x00    0x00    0x00    0x00    0x00
0x7fffffffe3e0: 0xd0    0xe4    0xff    0xff    0xff    0x7f    0x00    0x00
0x7fffffffe3e8: 0x02    0x00    0x00    0x00    0x01    0x00    0x00    0x00
从gdb的结果来看，保存了局部变量 调用函数的参数，但是这里不理解的是我的main方法里面只定义了三个局部变量，为什么要分配24字节呢？ 加上传参的4字节应该16字节也够了</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/9d/d91dc762.jpg" width="30px"><span>喜欢吃鱼</span> 👍（4） 💬（1）<div>徐老师，问您一个和这节内容不是很相关的一个问题可以吗？
为什么在写多重for循环的时候，循环次数多的大循环要写里面，小循环写外面？
希望老师解答下，非常感谢！！！</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/58/79/e7bbd28e.jpg" width="30px"><span>不系之舟</span> 👍（4） 💬（1）<div>文章中的&quot;push rbp 就把之前调用函数的返回地址，压到栈顶。&quot;

感觉这句话有问题，函数的返回地址压到栈顶，应该是call指令做的。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/43/cb6ab349.jpg" width="30px"><span>Spring</span> 👍（4） 💬（1）<div>call之后，原函数的bp就会赋值为sp，因此只要把bp压栈就好了，call之后再把之前压栈的bp出栈赋值给sp就好了。
函数返回后会把返回值放到ax寄存器，如果有多个返回值的话就将返回值的内存地址放到ax中。
因此call之后恢复回原函数还要保存bp和返回值。</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/7f/473d5a77.jpg" width="30px"><span>曾轼麟</span> 👍（4） 💬（1）<div>看了前面这几篇文章，感觉专栏有点倾向操作系统原理更多一些</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/ec/f16470a0.jpg" width="30px"><span>上五楼的快活</span> 👍（3） 💬（1）<div>老师您好，刚订阅，在哪儿加学习小组</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/60/049a20e9.jpg" width="30px"><span>吴宇晨</span> 👍（3） 💬（3）<div>我记得应该还要保存调用方的栈地址，调用结束才能还原栈，csapp之前看了，但是平常接触不到这些知识，都忘的差不多了😅😅</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（3） 💬（1）<div>Push rbp, move rpb rsp,以前一直不知道这两句的含义，现在清楚了</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/57/68e414ba.jpg" width="30px"><span>@我</span> 👍（3） 💬（1）<div>还要保护现场，保护现场的变量值也是存到系统栈里面的？多线程切换的话，是不是也要存到自己线程对应的栈里面？</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/28/96/a49c7264.jpg" width="30px"><span>matter</span> 👍（3） 💬（2）<div>实际的程序栈，顶和底跟乒乓球桶是相反的这个点我读了两遍，还没有太清楚含义。是不是指的分配栈地址的时候，分配的是一定大小的内存空间，比如从1a到3f，而第一次压栈操作存储的地址是3f而不是1a，是这样吗老师</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/7b/191a2112.jpg" width="30px"><span>愤怒的虾干</span> 👍（2） 💬（1）<div>我记得在中断处理时，需要保护现场，将cs、ip寄存器压栈，保存Flags寄存器，清除中断标识，然后跳转到中断处理命令；推广开来方法调用也需要将cs、ip寄存器压栈，保存调用前Flags寄存器状态，清除Flags寄存器的标识。老师，是这样吗？</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/b7/3681866d.jpg" width="30px"><span>不再冲动的函数</span> 👍（1） 💬（1）<div>每个线程的栈帧是什么时候分配的？编译程序的时候？还有一般每个程序的栈帧大小是多少？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（1） 💬（1）<div>在程序栈里面，除了我们跳转前的指令地址外，还需要保留CPU通用寄存器的中的数据</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（1） 💬（1）<div>问一个问题，我看老师objdump -M intel 这里-M的参数 intel是根据什么规则去选的呢？ 我看过man objdump还是不知道怎么指定</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/13/9d/d91dc762.jpg" width="30px"><span>喜欢吃鱼</span> 👍（1） 💬（1）<div>老师，为什么我把add函数变为inline函数之后，objdump出来的调用add处的汇编指令还是：call   25 &lt;main+0x25&gt;
</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/41/87/46d7e1c2.jpg" width="30px"><span>Better me</span> 👍（1） 💬（1）<div>rbp、rsp是如何管理函数之间的调用的</div>2019-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/aa/abb7bfe3.jpg" width="30px"><span>免费的人</span> 👍（1） 💬（1）<div>思考题：函数返回值、返回地址、sp bp</div>2019-05-10</li><br/>
</ul>