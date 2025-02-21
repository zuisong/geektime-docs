你好，我是宫文学。

在上一节课里，我们已经实现了一个简单的虚拟机。不过，这个虚拟机也太简单了，实在是不够实用啊。

那么，今天这节课，我们就来增强一下当前的虚拟机，让它的特性更丰富一些，也为我们后续的工作做好铺垫，比如用C语言实现一个更强的虚拟机。

我们在这一节课有两项任务要完成：

首先，要支持if语句和for循环语句。这样，我们就能熟悉与程序分支有关的指令，并且还能让虚拟机支持复杂一点的程序，比如我们之前写过的生成斐波那契数列的程序。

第二，做一下性能比拼。既然我们已经完成了字节码虚拟机的开发，那就跟AST解释器做一些性能测试，看看性能到底差多少。

话不多说，开干！首先，我们来实现一下if语句和for循环语句。而实现这两个语句的核心，就是要支持跳转指令。

## 了解跳转指令

if语句和for循环语句，有一个特点，就是让程序根据一定的条件执行不同的代码。这样一个语法，比较适合我们人类阅读，但是对于机器执行并不方便。机器执行的代码，都是一条条指令排成的直线型的代码，但是可以根据需要跳转到不同的指令去执行。

针对这样的差异，编译器就需要把if和for这样结构化编程的代码，转变成通过跳转指令跳转的代码，其中的关键是**计算出正确的跳转地址**。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/4b/46/717d5cb9.jpg" width="30px"><span>惜心（伟祺）</span> 👍（0） 💬（0）<div>从计算机执行的指令来看语言设计</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>满意，学习打卡</div>2022-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdzXiawss5gGiax48CJGAJpha4pJksPia7J7HsiatYwjBA9w1bkrDicXfQz1SthaG3w1KJ2ibOxpia5wfbQ/132" width="30px"><span>chris</span> 👍（0） 💬（1）<div>文中关于分支和跳转指令的麻烦, 其实都是源于跳转目标是一个绝对地址, 如果设计成一个相对偏移的话, 其实就不存在了. 并且java字节码ifxxx和goto后面跟的也都是相对偏移. 这里不知道老师为什么要设计成绝对地址, 出于什么考虑?</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/69/ee5a40f9.jpg" width="30px"><span>闫志刚</span> 👍（0） 💬（0）<div>念念不忘，必有回响</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（0） 💬（0）<div>虚拟机的本质就是：在软件层面上再造物理机。

Java 字节码可以看作是对汇编的一种模仿、简化和实现。</div>2021-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIicr82CnrdEjibibAvyeKRQHszSzIAqoCWxN0kqC442XcjEae6S9j6NDtKLpg4Da4CUQQeUFUicWqiaDw/132" width="30px"><span>有学识的兔子</span> 👍（0） 💬（0）<div>是不是和老师提示的那样，使用C&#47;C++来编写虚拟机,以获得转译和运行字节码上性能的提升。</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（0）<div>因为最终是编译成js运行的，可以用node —prof看下有没有明显的性能瓶颈</div>2021-08-28</li><br/>
</ul>