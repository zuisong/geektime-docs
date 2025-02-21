你好，我是于航。

看到这里的你，应该已经完成了本课程前两个模块的学习。随着课程的不断推进，我陆续收到了很多反馈。很高兴看到你在评论区积极留言，和大家一起讨论思考题。并且，还有很多同学提出了一些非常有意义的问题。那么，在继续学习后面更深入的内容之前，让我们先暂缓脚步，从问题出发，进行一次整体性的回顾。

在这一讲中，我会以加餐的形式，为你剖析一些值得讨论的思考题，以及你们提出的有代表性的问题。

**问题一：**在 [01 讲](https://time.geekbang.org/column/article/464550) 的最后，我留给你的问题是：在这一讲第一部分的 C 代码实例中，我们为何要给函数 findAddr 添加 `static` 关键字？不添加这个关键字的话，程序是否可以编译运行？

这里，我将那段代码简化了一下，只提取出与问题相关的部分，放到了下面。因此，问题也变成了：对于下面这段代码来说，将函数 foo 定义中使用的 `static` 关键字去掉，是否会影响程序的正常编译和运行呢？

```c++
#include <stdio.h>
inline static int foo(void) { 
  return 0;
}
int main(void) {
  printf("%d", foo());
  return 0; 
}
```

实际上，如果你能够在 [godbolt](https://godbolt.org) 上快速实践一下，就会发现：在默认情况下（没有使用任何优化参数），编译器会报出类似 “error: ld returned 1 exit status” 的链接器错误；而在使用 “-O1” 及以上优化参数的情况下，编译器则可以正常编译。那么，为什么会这样呢？
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/ce/c6/958212b5.jpg" width="30px"><span>sugar</span> 👍（3） 💬（3）<div>请教于航老师一个问题，我的日常开发程序语言主要是JavaScript和C&#47;C++，这个技术栈与老师应该比较类似。在js中，我们在运行时console.log可以打出任何一个代码中可见的变量的具体值，无论它是一个number、string这样的简单类型，还是各种类嵌套定义出的超级复杂的数据结构，这个能力在阅读其他人写的代码时很有帮助：我不确定一段程序中的某个符号代表的对象究竟是什么结构的时候，我可以直接去运行时把它log出来，尤其是项目代码量庞大的时候这能省去大量人肉读代码的时间；但是在c&#47;c++当中，据我目前所知似乎只能cout 或者 printf出一个基本类型，比如int double char等，不能像js那样轻松的console.log出任何type的变量完整结构。请问于航老师在面对这种情况时是怎么处理？是否只能人肉一个一个class definition去翻代码？c的一些三方库只能翻到.h文件，翻不到具体实现.c或者.cpp文件。</div>2022-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/97/23446114.jpg" width="30px"><span>火云邪神霸绝天下</span> 👍（1） 💬（1）<div>#include &lt;stdio.h&gt;
void foo(void) {
  int x;
  printf(&quot;%d\n&quot;, x);
  x = 10;
}
int main(void) {
  foo();
  foo();
  return 0;
}

这个代码两次输出都是0。不太明白它说清楚了什么。
本来不就该是  0   吗？

函数执行一次就栈内空间回收了吧。下次执行下次说。</div>2022-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8b/06/fb3be14a.jpg" width="30px"><span>TableBear</span> 👍（0） 💬（1）<div>专属的微信群是哪个？还能进去吗</div>2022-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（1）<div>我觉得老师可以请大佬来讲讲c语言在redis应用哈哈，有了nginx，怎么能少了redis</div>2022-01-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKwGurTWOiaZ2O2oCdxK9kbF4PcwGg0ALqsWhNq87hWvwPy8ZU9cxRzmcGOgdIeJkTOoKfbxgEKqrg/132" width="30px"><span>ZR2021</span> 👍（1） 💬（0）<div>老师强大！！！</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（1） 💬（0）<div>Good </div>2021-12-31</li><br/>
</ul>