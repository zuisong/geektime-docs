你好，我是卢誉声。

今天是第一讲，我们会从C++20中的核心特性变更——Modules模块开始，了解现代C++的编程范式、编程思想及现实问题解决方法上的革新。

我们都知道，无论是编写C还是C++程序，总少不了使用include头文件机制，这是C/C++编程中组织代码的最基本方式，用法简单、直接，而且符合直觉。但很多人不知道的是，其实include头文件机制不仅有坑，在编程过程中还会出现一些难以解决的两难问题。

接下来，我们就从这个“简单”机制开始探讨代码组织方式的门道，看看里面究竟存在哪些问题，语言设计者和广大语言使用者又是如何应对的，对这些问题的思考，将串联起我们关于C++代码组织方案的所有知识点，也终将引出我们的主角——Modules（课程配套代码点击[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

首先来看看整个故事的背景，include头文件机制，它的出现是为了什么？

## 万物始于include

作为C语言的超集，C++语言从设计之初就沿袭了C语言的include头文件机制，即通过包含头文件的方式来引用其他符号，包括类型定义、接口声明这样的代码，起到分离符号定义与具体实现的作用。

早期，能放在头文件中的符号比较有限，头文件设计是足以支撑系统设计的。但是为了提高运行时性能，开发者也会考虑将实现直接放在头文件中。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/adf8X0vmoJN8EuJOpIs81VyVmib9zgxTeWheic1C3DKfFeFT0os67qbicsRFHUeMnz7nKQ25XHp2r7wlbX8KXfLDA/132" width="30px"><span>糍粑不是饭</span> 👍（7） 💬（4）<div>老师是否考虑再增加些CMake或者包管理相关的课程呢？😃</div>2023-03-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/FhibmYQUzY7ibPac8Id5PwbibqCbvj5rWibeQhEyvYguc9pvPNUciaQydicrUjJKkhhp1s2AgfP7LRTZA8zqaa82yC8g/132" width="30px"><span>tanatang</span> 👍（5） 💬（1）<div>写面向对象的C++，成员和函数都在设计在类中，禁止使用这种不属于任何类的全局函数， 全局变量。</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/86/07/aefa4e8b.jpg" width="30px"><span>wilby</span> 👍（5） 💬（2）<div>为什么namespace让符号管理变得很复杂？老师好像就给了个结论，能展开讲讲么？</div>2023-01-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8aLz0tWdsZuMiaNUAd0dicSD9M6A77seMGFdHgvsQwOzN8ztYPiaJSo53DcbjQWUQpw4pf4rI2f7vg/132" width="30px"><span>Geek_7c0961</span> 👍（2） 💬（3）<div>&quot;这也能大量减少编译单元之间的符号冲突问题，毕竟可能出现，两个编译单元定义了同名，但只想在编译单元内部使用函数的情况，我们并不想给这些函数加上冗长的前缀。那这个时候，只需要使用 static 修饰符。比如我们可以在 A 和 B 中都定义 static 函数 to_int，然后再编译链接，这样就不会出现符号冲突的问题。&quot; 这块儿能否给个具体的代码示例?</div>2023-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/f3/22481a37.jpg" width="30px"><span>小样</span> 👍（1） 💬（1）<div>太可怕了，以前没有想过这种问题。
实际用到的代码规模并不是很大，一个人就能完全掌握各个模块，也就不会有冲突。现在来看传统上符号隔离和污染问题根本就没有在设计上解决过。软件工程规模大后必然有冲突问题。</div>2023-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/27/a6/32e9479b.jpg" width="30px"><span>tang_ming_wu</span> 👍（1） 💬（1）<div>链接过程，函数地址填充，是不是都是相对地址？</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教两个问题：
Q1：第一个专栏是什么？

Q2：实现放在头文件中为什么可以提高运行性能？
文中有这样一句话“但是为了提高运行时性能，开发者也会考虑将实现直接放在头文件中。” 为什么？</div>2023-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/40/f10493ef.jpg" width="30px"><span>中山浪子</span> 👍（0） 💬（1）<div>“ b.o 中会生成一个名为 add 的符号”一般是用什么工具或者怎么查看生成的二进制中的符号？</div>2024-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/c5/f8/623a0375.jpg" width="30px"><span>不二</span> 👍（0） 💬（1）<div>历史挺好的，但是里面概念太多，解释不清楚感觉消化不了。</div>2023-01-19</li><br/>
</ul>