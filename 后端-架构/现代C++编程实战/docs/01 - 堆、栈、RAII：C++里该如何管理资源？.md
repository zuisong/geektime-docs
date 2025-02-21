你好，我是吴咏炜。

今天我们就正式开启了C++的学习之旅，作为第一讲，我想先带你把地基打牢。我们来学习一下内存管理的基本概念，大致的学习路径是：先讲堆和栈，然后讨论 C++ 的特色功能 RAII。掌握这些概念，是能够熟练运用 C++ 的基础。

## 基本概念

**堆**，英文是 heap，在内存管理的语境下，指的是动态分配内存的区域。这个堆跟数据结构里的堆不是一回事。这里的内存，被分配之后需要手工释放，否则，就会造成内存泄漏。

C++ 标准里一个相关概念是自由存储区，英文是 free store，特指使用 `new` 和 `delete` 来分配和释放内存的区域。一般而言，这是堆的一个子集：

- `new` 和 `delete` 操作的区域是 free store
- `malloc` 和 `free` 操作的区域是 heap

但 `new` 和 `delete` 通常底层使用 `malloc` 和 `free` 来实现，所以 free store 也是 heap。鉴于对其区分的实际意义并不大，在本专栏里，除非另有特殊说明，我会只使用堆这一术语。

**栈**，英文是 stack，在内存管理的语境下，指的是函数调用过程中产生的本地变量和调用数据的区域。这个栈和数据结构里的栈高度相似，都满足“后进先出”（last-in-first-out 或 LIFO）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/e0/0a/bf7ece06.jpg" width="30px"><span>bo</span> 👍（52） 💬（8）<div>老师您好！工程的时候，具体怎么考虑在栈上分配还是在堆上分配，更合理些？</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（46） 💬（4）<div>说实话，这个专栏对于我这个经常使用C++来做项目的人来讲，我认为不适合初学者，上车需要有过C++开发经验的。一般的小伙伴可能会有压力哒，但是如果想学，克服心里畏惧，从这个专栏出发可以迅速的深入。很好的专栏。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/46/1a9229b3.jpg" width="30px"><span>NEVER SETTLE</span> 👍（33） 💬（3）<div>学习笔记：

1、概念
堆（heap）：在内存管理中，指的是动态分配内存的区域。当被分配之后需要手工释放，否则，就会造成内存泄漏。
C++ 标准里一个相关概念是自由存储区（free store），特指使用 new 和 delete 来分配和释放内存的区域。
这是堆的一个子集：new 和 delete 操作的区域是 free store，而 malloc 和 free 操作的区域是 heap 。
但 new 和 delete 通常底层使用 malloc 和 free 来实现，所以 free store 也是 heap。

栈（stack）：在内存管理中，指的是函数调用过程中产生的本地变量和调用数据的区域。

RAII（Resource Acquisition Is Initialization）：C++ 所特有的资源管理方式。
RAII 依托栈和析构函数，来对所有的资源——包括堆内存在内——进行管理。
对 RAII 的使用，使得 C++ 不需要垃圾收集方法，也能有效地对内存进行管理。

2、堆
C++程序需要牵涉到两个的内存管理器的操作：

1). 让内存管理器分配一个某个大小的内存块
分配内存要考虑程序当前已经有多少未分配的内存。
内存不足时要从操作系统申请新的内存。
内存充足时，要从可用的内存里取出一块合适大小的内存，并将其标记为已用，然后将其返回给要求内存的代码。

2). 让内存管理器释放一个之前分配的内存块
释放内存不只是简单地把内存标记为未使用。
对于连续未使用的内存块，通常内存管理器需要将其合并成一块，以便可以满足后续的较大内存分配要求。
目前的编程模式都要求申请的内存块是连续的。

从堆上申请的内存需要手工释放，但在此过程中，内存可能有碎片化的情况。
一般情况下不需要开发人员介入。因为内存分配和释放的管理，是内存管理器的任务。
开发人员只需要正确地使用 new 和 delete，即每个 new 出来的对象都应该用 delete 来释放。

3、栈
大部分计算机体系架构中，栈的增长方向是低地址，因而上方意味着低地址。
任何一个函数，根据架构的约定，只能使用进入函数时栈指针向上部分的栈空间。
当函数调用另外一个函数时，会把参数也压入栈里，然后把下一行汇编指令的地址压入栈，并跳转到新的函数。
新的函数进入后，首先做一些必须的保存工作，然后会调整栈指针，分配出本地变量所需的空间，随后执行函数中的代码。
在执行完毕之后，根据调用者压入栈的地址，返回到调用者未执行的代码中继续执行。

本地变量所需的内存就在栈上，跟函数执行所需的其他数据在一起。
当函数执行完成之后，这些内存也就自然而然释放掉了。
栈上的内存分配，是移动一下栈指针。
栈上的内存释放，是函数执行结束时移动一下栈指针。
由于后进先出的执行过程，不可能出现内存碎片。

每个函数占用的栈空间有个特定的术语，叫做栈帧（stack frame）。
GCC 和 Clang 的命令行参数中提到 frame 的，如 -fomit-frame-pointer，一般就是指栈帧。

如果本地变量是简单类型，C++ 里称之为 POD 类型（Plain Old Data）。
对于有构造和析构函数的非 POD 类型，栈上的内存分配也同样有效。
只不过 C++ 编译器会在生成代码的合适位置，插入对构造和析构函数的调用。
编译器会自动调用析构函数，包括在函数执行发生异常的情况。
在发生异常时对析构函数的调用，还有一个专门的术语，叫栈展开（stack unwinding）。

在 C++ 里，所有的变量缺省都是值语义。
引用一个堆上的对象需要使用 * 和 &amp; 。
对于像智能指针这样的类型，使用 ptr-&gt;call() 和 ptr.get()，语法上都是对的，并且 -&gt; 和 . 有着不同的语法作用。
这种值语义和引用语义的区别，是 C++ 的特点，也是它的复杂性的一个来源。
</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d9/b8/2d8900d5.jpg" width="30px"><span>史鹏飞</span> 👍（30） 💬（8）<div>老师在shape_wrapper类下边的foo函数调用完后，会把shape析构掉，但如何析构circle呢？</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/4a/0f56e0ad.jpg" width="30px"><span>LiKui</span> 👍（22） 💬（2）<div>内存泄漏的原因之二：
1. 异常或分支导致delete未得到执行
2.分配和释放不在一个函数里导致的遗漏delete</div>2019-12-19</li><br/><li><img src="" width="30px"><span>Geek_3f3bcb</span> 👍（22） 💬（1）<div>看的有点爽</div>2019-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ed/1c662e93.jpg" width="30px"><span>莫珣</span> 👍（17） 💬（2）<div>C++对象在销毁的时候会自动调用析构函数，所谓RAII机制其实就是在对象构造的时候初始化它所需要的资源，在析构的时候自动释放它持有的资源。</div>2020-04-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ncicjtgbOgxk2V3VWYJQAia7oCycVFr5Zncudb5EYWhQsMte0asAauBDh6ELrJbTwrSnboBpESBibslrcNc5icrAkw/132" width="30px"><span>super-ck</span> 👍（17） 💬（1）<div>您好，有一点不是很清楚，在n为42时为何不是构造函数-throw-析构函数这个顺序，根据上下文，为42时，按一般逻辑应该进判断执行才对</div>2020-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（15） 💬（8）<div>话说一般delete.后需要把这个变量置成nullptr吗，我有时候这样写，不知道有没有必要</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/4e/347c3e8f.jpg" width="30px"><span>楚小奕</span> 👍（13） 💬（1）<div>这个专栏配合 《modern effect c++》效果很好</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/10/e8/172b5915.jpg" width="30px"><span>张珂</span> 👍（10） 💬（2）<div>老师您好，我说一下我对内存切片那里的理解，不知道对不对：
返回的是个基类指针shape*，但其实指向的是个继承类circle对象。那么在用户程序里，就算用户记得delete这个指针shape*，也会造成circle部分永久残留在内存，从而造成内存泄漏，我理解的对吗？</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7d/a1/46c5293c.jpg" width="30px"><span>yuchen</span> 👍（7） 💬（3）<div>怕评论中您看不到，在此再问一下，麻烦您啦～
上个问题回顾：
对于图2d有疑惑，希望该图绘制中可以标明main函数占用的栈空间范围及其对应的栈帧，同理，对bar和foo也一样。如果将图2d从下到上每行编号为0，1，2，...，7，那么main、bar和foo对应的栈空间占用、栈帧分别是那几行呢？
您的回答：嗯，问得有道理。我的颜色选取不够好，回头改一下。按一般的栈帧定义，只有 0 属于 main，1–4 属于 bar。5 以上属于 foo。

首先，非常感谢您的回复～

然而，看到有人这样问您：“参数42”和“a=43”分别是函数调用的参数和函数局部变量，应该属于同一个栈帧，为什么这里不同？
您的回答是：同样，实际实现通常就是这个样子的。参数属于调用者而非被调用者，一般也是由调用者来释放——至少一般 x86 的实现是这个样子。

那么和您这里回答我的就不一致的呢。您这里回答我1-4属于bar，因此，那个人问的问题（“参数42”和“a=43”应该属于同一个栈帧）这句就是对的。另外您说“参数属于调用者而非被调用者”，这里1-4既然属于bar了，那么参数42不就属于了被调用者bar了吗？我理解的是main是调用者，main调用了bar，则bar是被调用者。</div>2019-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/01/38/5daf2cfb.jpg" width="30px"><span>吴军旗^_^</span> 👍（7） 💬（4）<div>老师可推荐一下教程吗？ 从php转过来的，感觉有点难。</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e3/cd/82829bf9.jpg" width="30px"><span>Gerry</span> 👍（6） 💬（5）<div>栈通常说是向下增长，从高地址到低地址。文中表述是向上增长感觉欠妥。</div>2019-11-27</li><br/><li><img src="" width="30px"><span>陈嘉伟</span> 👍（5） 💬（4）<div>请教一个问题，既然delete空指针是合法的，那多次delete同一个指针为什么会报错呢？</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/98/51/27c46724.jpg" width="30px"><span>xm2018</span> 👍（5） 💬（1）<div>关于演示栈展开的那段程序，如果main函数里面不try catch的话，第二个foo(42) obj的析构函数不会被调用，程序非法退出。这种情况算不算泄漏?</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/be/39cc22f5.jpg" width="30px"><span>petit_kayak</span> 👍（4） 💬（1）<div>感觉，RAII的本质就是用栈上的变量封装堆里的内存，借助栈空间的安全，来实现堆空间的安全。</div>2023-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/1a/65/bcf45f14.jpg" width="30px"><span>Home</span> 👍（4） 💬（1）<div>老师好，关于值语义和引用语义可以分别举几个例子么？</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6e/83/f429164e.jpg" width="30px"><span>Interesting</span> 👍（4） 💬（1）<div>C++是只有使用new关键字出来的对象才分配到堆上吗？
Obj obj();
Obj obj* = new Obj();
只有后者是在堆上吗？ 堆栈的却别就是 栈的销毁是随着局部变量失效和函数调用完自动销毁  而 堆是需要申请和手动销毁吗？
抱歉从别的语言转过来的可能表述不是很准确 </div>2020-04-28</li><br/><li><img src="" width="30px"><span>宋强</span> 👍（3） 💬（1）<div>请问老师，局部变量的作用域是{}界定的吗？比如我想使用std::lock_guard对函数体内部分的程序块加锁，是这样吗？
func A() {
  {
  std::lock_guard
  ...
  }
...
}</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/54/73cc7f73.jpg" width="30px"><span>王旧业</span> 👍（3） 💬（1）<div>“常见情况之一是，在工厂方法或其他面向对象编程的情况下，返回值类型是基类”
这句话的意思应该是：“返回值类型是基类指针”吧</div>2020-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/06/8d/704e2596.jpg" width="30px"><span>Anita</span> 👍（3） 💬（1）<div>在 C++ 里，所有的变量缺省都是值语义——如果不使用 * 和 &amp; 的话，变量不会像 Java 或 Python 一样引用一个堆上的对象。对于像智能指针这样的类型，你写 ptr-&gt;call() 和 ptr.get()，语法上都是对的，并且 -&gt; 和 . 有着不同的语法作用。而在大部分其他语言里，访问成员只用 .，但在作用上实际等价于 C++ 的 -&gt;。这种值语义和引用语义的区别，是 C++ 的特点，也是它的复杂性的一个来源。要用好 C++，就需要理解它的值语义的特点。

这段有些不理解，老师能再解释一下吗？谢谢</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（3） 💬（2）<div>老师反复提到，没有学过、用过c++的人不适合学；我的观点稍微有点不同：计算机基础知识扎实，熟悉Java和c，这门课还是蛮适合的。

计算机基础知识深厚，深入理解堆和栈的区别，知道什么时候用堆内存，什么时候用栈内存，那么，剩下的就是语法了。 </div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/df/0e/4e2b06d5.jpg" width="30px"><span>流浪在寂寞古城</span> 👍（3） 💬（1）<div>作为一个用c++做过一些项目，但是没有深入学习过c++的我（看到java很亲切呀，哈哈），感觉有些压力，RAII里面的这个语法就没怎么接触过。不过我会坚持看完，认真理解。勉励自己吧。这算一个flag了吧，所有小伙伴一起加油，跟大佬学习。</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/31/7b/5914f8eb.jpg" width="30px"><span>小骆驼🐪</span> 👍（2） 💬（1）<div>今天面试被问到，变量存储在哪些区域，以及c++内存区域。我回答内存区域有text,bss,data,堆，栈(这好像是c的划分)🤦</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/7f/b7/68977ad8.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>想问一下static_cast这一类的类型转换到底有什么好处呢？平时开发的时候并不太习惯用这种方式，感觉直接指针强转就可以，两者没什么实质的区别，反正能就是能，不能就是不能，static_cast只是好看一些，如果出问题的话让你死的体面点。</div>2021-06-30</li><br/><li><img src="" width="30px"><span>Geek_af30d1</span> 👍（2） 💬（1）<div>所谓值语义是一个对象被系统标准的复制方式复制后，与被复制的对象之间毫无关系，可以彼此独立改变互不影响

指针语义，引用语义：通常是指一个对象被系统标准的复制方式复制后，与被复制的对象之间依然共享底层资源，对任何一个的改变都将改变另一个
老师， 这样解释对吗？</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/99/d1/88127ae2.jpg" width="30px"><span>怎么追摩羯座</span> 👍（2） 💬（1）<div>RALL可以理解为是析构函数吗</div>2020-12-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pCVwNYT22UX6XAXJ5XLmbSHRmuPIncaJkS7S6kUKe0C8qWURib8zOhHTPwR36FeZZ4BcnKuDia4nrekqDnAkxdJQ/132" width="30px"><span>luke</span> 👍（2） 💬（2）<div>RAII这种写法如何减少同步段的操作？例如在一个函数里，我只希望lock变量赋值这个语句，而不是整段。</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（2） 💬（1）<div>老师讲的真棒，评论区的讨论也非常的有价值，让我对编程语言有了更加透彻的理解呢。 这篇已经读了5遍了，果然需要写过一段时间的代码才能读懂呢。</div>2020-03-26</li><br/>
</ul>