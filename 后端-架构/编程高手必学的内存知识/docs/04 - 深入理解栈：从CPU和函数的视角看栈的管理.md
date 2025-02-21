你好，我是海纳。

上节课，我们讲到，栈被操作系统安排在进程的高地址处，它是向下增长的。但这只是对栈相关知识的“浅尝辄止”。那我们今天这节课，就会跟着前面的脉络，让你可以更深刻地理解栈的运行原理。

栈是每一个程序员都很熟悉的话题，但你敢说你真的完全了解它吗？我相信，你在工作中肯定遇到过栈溢出（StackOverflow）的错误，比如在写递归函数的时候，当漏掉退出条件，或者退出条件不小心写错了，就会出现栈溢出错误。我们也经常听说缓冲区溢出带来的严重的安全问题，这在日常的工作中都是要避免的。

所以，今天这节课，我们继续深入探讨一下栈这个话题，我会带你基于“符合人的直观思维”，也就是函数的层面和CPU的机器指令层面，多角度来理解栈相关的概念。这样，你以后遇到与栈相关的问题的时候，才知道如何着手进行排查。最后，我们还会通过一个缓冲区溢出攻击栈的案例，看看我们在日常工作中如何提升代码的健壮度和安全性。

## 函数与栈帧

当我们在调用一个函数的时候，CPU会在栈空间（这当然是线性空间的一部分）里开辟一小块区域，这个函数的局部变量都在这一小块区域里存活。当函数调用结束的时候，这一小块区域里的局部变量就会被回收。

这一小块区域很像一个框子，所以大家就命名它为stack frame。frame本意是框子的意思，在翻译的时候被译为帧，现在它的中文名字就是栈帧了。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/20/3b/2a/f05e546a.jpg" width="30px"><span>🐮</span> 👍（14） 💬（1）<div>老师，出堆后栈空间里的数据还是保留的啊，是不是叫栈空间扩展和收缩形象点</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cf/c6/6a2d0a5e.jpg" width="30px"><span>鵼</span> 👍（6） 💬（2）<div>老师好，栈溢出的例子，在栈桢上不是先保存基地址rbp，然后分配rsp保存参数和局部变量吗？所以在参数的栈高位应该还有rbp，然后才是rip。但是代码本地运行一下是可以的，通过objdump看，发现没有push %rbp，mov %rsp，%rbp了。这是因为gcc加了-o1的优化参数。这个是不是有点类似方法内敛呢？不加-o1,就还会先保存rbp了，在执行即使段错误。
然后，思考题答案，通过objdump看，发现参数寄存器rdi和rsi保存的不再是值了，而是通过lea把参数的栈地址传递过去了。因此修改就等于是修改了main的栈桢上的值。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2e/3e/5ae876fd.jpg" width="30px"><span>GL</span> 👍（5） 💬（2）<div>swap函数在C传入指针或C++的引用 是拿到了操作数的存放地址 所以可以改变对应的值，Java语言的入参如果基本数据类型是没法改变外部变量的值，如果是引用类型是可以改变引用对象内的属性值。</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（3） 💬（2）<div>又看了一遍老师这一课，没太看懂栈溢出攻击这一块的细节，想多请教一下：

执行test函数后，字符串数组s中从0元素到15元素在栈中存储地址是从高向低的吗？随后call copy方法后，会压栈下一条指令地址到栈上，这条指令存储地址更低。所以最后让栈溢出时多拷贝地址是把地址数值的低位放在内存地址高位、数值的高位放在内存地址低位满足小端序顺利解析到这条地址的数值。

不知道这样理解对吗，因为对老师举的这个例子比较感兴趣，所以想把细节搞清楚，如果没理解对不知道能不能辛苦老师多讲一下，感谢！</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/c9/5d03981a.jpg" width="30px"><span>thomas</span> 👍（1） 💬（1）<div>第 3 行的作用呢，是把栈向下增长 0x10，这是为了给局部变量预留空间。从这里，你可以看出来运行 fac 函数要是消耗栈空间的。
==========================&gt;
请问栈增长多少是如何预估出来的？ </div>2021-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a3/33/8680446c.jpg" width="30px"><span>拭心</span> 👍（1） 💬（2）<div>看的有点晕，尤其是各个汇编指令和他们操作的寄存器的作用，不知道您是怎么记忆这些晦涩的内容呢？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/56/3c/f9ff3ed8.jpg" width="30px"><span>杨军</span> 👍（1） 💬（1）<div>这个就是csapp 中 lab2 的内容，好亲切</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/fe/882eaf0f.jpg" width="30px"><span>威</span> 👍（1） 💬（1）<div>老师您好，缓冲区溢出的Segment Fault，是指一个栈桢里溢出，还是栈桢之间的溢出。我理解是按照文章说的保护机制，应该是溢出到了别的栈桢，才会出现Segment Fault。不知道这样的理解正不正确呢？</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（0） 💬（2）<div>老师想提个小建议，能不能把汇编代码也贴上来比较方便理解，n*(n-1)那个例子因为示例代码只有机器码，只能看着您的文字理解，我们这种刚开始入门的同学看着可能比较抽象，不过这一课又把栈更深入地理解了一遍，谢谢老师</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/eb/2e/90fea784.jpg" width="30px"><span>柒</span> 👍（0） 💬（1）<div>老师，我觉得你一下用python，一下用c语言，不太好。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2a/48/791d0f5e.jpg" width="30px"><span>Rovebiy</span> 👍（0） 💬（1）<div>老师，是不是曾经在知乎写过专栏进击的Java新人？</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（0） 💬（2）<div>思考题：反汇编结果显示传递的是地址
000000000040052d &lt;swap&gt;:
  40052d:	55                   	push   %rbp
  40052e:	48 89 e5             	mov    %rsp,%rbp
  400531:	48 89 7d e8          	mov    %rdi,-0x18(%rbp)
  400535:	48 89 75 e0          	mov    %rsi,-0x20(%rbp)
  400539:	48 8b 45 e8          	mov    -0x18(%rbp),%rax
  40053d:	8b 00                	mov    (%rax),%eax
  40053f:	89 45 fc             	mov    %eax,-0x4(%rbp)
  400542:	48 8b 45 e0          	mov    -0x20(%rbp),%rax
  400546:	8b 10                	mov    (%rax),%edx
  400548:	48 8b 45 e8          	mov    -0x18(%rbp),%rax
  40054c:	89 10                	mov    %edx,(%rax)
  40054e:	48 8b 45 e0          	mov    -0x20(%rbp),%rax
  400552:	8b 55 fc             	mov    -0x4(%rbp),%edx
  400555:	89 10                	mov    %edx,(%rax)
  400557:	5d                   	pop    %rbp
  400558:	c3                   	retq   

0000000000400559 &lt;main&gt;:
  400559:	55                   	push   %rbp
  40055a:	48 89 e5             	mov    %rsp,%rbp
  40055d:	48 83 ec 10          	sub    $0x10,%rsp
  400561:	c7 45 fc 02 00 00 00 	movl   $0x2,-0x4(%rbp)
  400568:	c7 45 f8 03 00 00 00 	movl   $0x3,-0x8(%rbp)
  40056f:	48 8d 55 f8          	lea    -0x8(%rbp),%rdx
  400573:	48 8d 45 fc          	lea    -0x4(%rbp),%rax
  400577:	48 89 d6             	mov    %rdx,%rsi
  40057a:	48 89 c7             	mov    %rax,%rdi
  40057d:	e8 ab ff ff ff       	callq  40052d &lt;swap&gt;
  400582:	8b 55 f8             	mov    -0x8(%rbp),%edx
  400585:	8b 45 fc             	mov    -0x4(%rbp),%eax
  400588:	89 c6                	mov    %eax,%esi
  40058a:	bf 30 06 40 00       	mov    $0x400630,%edi
  40058f:	b8 00 00 00 00       	mov    $0x0,%eax
</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ce/87/41c44923.jpg" width="30px"><span>会爆炸的小米Note</span> 👍（2） 💬（0）<div>由于main函数向swap函数传递的参数小于6个 只会使用用寄存器传参 不会在main函数的参数构建区存放a,b,&amp;a,&amp;b的值
main函数调用swap(a,b)时会用mov把在main函数局部变量区存放的a，b的值复制到rdi，rsi
main函数调用swap(&amp;a,&amp;b)时会用leaq把在main函数局部变量区存放的a，b的地址值复制到rdi，rsi
这样在swap的时候相当于对main函数局部变量区的a，b直接操作
leaveq相当于 mov rbp,rsp 
                   pop rbp
retq相当于    pop rip
都是AT&amp;T格式的


</div>2022-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（2） 💬（0）<div>copy 越界处理了数组，导致 copy 函数栈帧的返回地址变成了 bad 函数的地址，所以 bad 函数执行了～～</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（2） 💬（1）<div>吊打面试官的配图很清晰，点赞！</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e7/8e/318cfde0.jpg" width="30px"><span>Spoon</span> 👍（1） 💬（0）<div>可以在test前加一下这个代码
    printf(&quot;The bad  address:%p\n&quot;, &amp;bad);
    printf(&quot;The t[~] address:0x&quot;);
    for (int j = BUFFER_LEN - 1; j &gt;= BUFFER_LEN - 8; j--)
    {
        printf(&quot;%x&quot;, (t[j] &amp; 0xff));
    }
    printf(&quot;\n&quot;);
使用-O1不会有push rbp;mov rsp rbp;这样的操作
copy溢出的原理是应为eip压栈时占用8字节，copy调用完以后，现在s之上，元old eip压栈地址变为bad函数地址
</div>2022-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（1）<div>我无论在本地的mac上还是centos上(Rocky 9.2， 5.14.0)，都无法复现栈溢出的例子。
代码和gcc指令完全复制自文章中。
请问这是为什么？</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1a/3b/363561e5.jpg" width="30px"><span>gover</span> 👍（0） 💬（0）<div>lea 替代 mov</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/90/f63eb1da.jpg" width="30px"><span>程序猿</span> 👍（0） 💬（0）<div>BUFFER_LEN 不是24吗？为什么栈里面值预留了初始化的16个字节？</div>2022-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a2/55/1092ebb8.jpg" width="30px"><span>边城路远</span> 👍（0） 💬（0）<div>我用的高版本的gcc-11.3.0，没有出现栈溢出，原因是编译器自动做了处理，反汇编后test函数第一条指令是“sub    $0x18,%rsp”， 而在另外一台低版本机器上，反汇编后test函数第一条指令是“sub    $0x10,%rsp”</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/27/0b/12dee5ed.jpg" width="30px"><span>进化论</span> 👍（0） 💬（0）<div>400531: 48 83 ec 10 sub $0x10,%rsp %rsp存储的地址-16  这16单位是？ 参数n不是4字节吗为啥是16？ 还有返回地址，返回值，那这16也没想明白都包括的什么数据

400535: 89 7d fc mov %edi,-0x4(%rbp).  这里代表%rbp存储的地址减了4字节吗？</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/95/13/ea2584d3.jpg" width="30px"><span>jferic</span> 👍（0） 💬（0）<div># gcc -O1 -o fac fac.c

000000000040052d &lt;fac&gt;:
  40052d:       53                      push   %rbx
  40052e:       89 fb                   mov    %edi,%ebx
  400530:       b8 01 00 00 00          mov    $0x1,%eax
  400535:       83 ff 01                cmp    $0x1,%edi
  400538:       74 0b                   je     400545 &lt;fac+0x18&gt;
  40053a:       8d 7f ff                lea    -0x1(%rdi),%edi
  40053d:       e8 eb ff ff ff          callq  40052d &lt;fac&gt;
  400542:       0f af c3                imul   %ebx,%eax
  400545:       5b                      pop    %rbx
  400546:       c3                      retq

-O1 优化后：
使用 push %rbx 通过 %rbx 寄存器在计算 fac(n-1) 的时先把 n 在 push 到 栈 上，
接着通过 callq 算出 fac(n-1) 结果存入 %eax，
然后使用 pop %rbx 把 n 存入 %rbx 寄存器，
其后执行 imul   %ebx,%eax  计算 n * fac(n-1)</div>2022-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/95/13/ea2584d3.jpg" width="30px"><span>jferic</span> 👍（0） 💬（0）<div>文中：“第 1 行是将当前栈基址指针存到栈顶，第 2 行是把栈指针保存到栈基址寄存器，这两行的作用是把当前函数的栈帧创建在调用者的栈帧之下。保存调用者的栈基址是为了在 return 时可以恢复这个寄存器。”

请问老师，是 14 行的 leaveq 指令恢复调用者的寄存器吗？可以展开讲一下这个 leaveq 指令吗？</div>2022-02-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（0） 💬（1）<div>老师，为什么栈溢出就会崩溃呢，栈帧里面存放的都是数据，权限基本都一样的吧，应该不是出现覆盖了权限不同的数据导致崩溃吧， 还是说栈溢出了就是会崩溃，那是谁检测栈溢出的，又是怎么通知到内核，然后内核发信号让这个进程主动崩溃的</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/77/4b/ede8aa13.jpg" width="30px"><span>喵吉豆豆</span> 👍（0） 💬（1）<div>40052d:       55                      push   %rbp  
40052e:       48 89 e5                mov    %rsp,%rbp  
400531:       48 83 ec 10             sub    $0x10,%rsp

第2个例子里一开始栈为什么要扩0x10呢？只算到一个局部变量需要的0x04，还有一条imul语句，加起来也不到0x10，不知道是哪里理解的不对</div>2021-12-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/d4MHbXBwovYHW7xA18j88ibw1wS2R1JCoH5oLJIMUTdXe07dyVeTNWNzqWUKT7nPg21oClPhy1rSZPFiaibHeUFBA/132" width="30px"><span>Geek_a5edac</span> 👍（0） 💬（0）<div>看了四章，基本上没有什么理解的压力，都很快掌握老师讲的要点，主要是因为本人之前已经看了《深入理解计算机操作系统》《linux 0.11 源码》相关数据，大体上有了一个基本的认识。但还是感谢老师这么课程，我认为这么课程很好把握之前的知识点比较系统地做了梳理，并在一些细节上突出了下。</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/1d/97/9a8b2d0c.jpg" width="30px"><span>🙃</span> 👍（0） 💬（0）<div>提一个小建议：可以在每篇文章后面附上作者决定不错的文章或者paper，这样既可以在作者的专栏里对整体有一个完整的印象，也可以根据作者推荐的文章来深入理解！</div>2021-11-15</li><br/>
</ul>