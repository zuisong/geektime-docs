你好，我是Chrono。

上节课我讲了自动类型推导，提到auto推导出的类型可以附加const、volatile修饰（通常合称为“cv修饰符”）。别看就这么两个关键字，里面的“门道”其实挺多的，用好了可以让你的代码更安全、运行得更快。今天我就来说说它们俩，以及比较少见的另一个关键字mutable。

## const与volatile

先来看**const**吧，你一定对它很熟悉了。正如它的字面含义，表示“常量”。最简单的用法就是，**定义程序用到的数字、字符串常量，代替宏定义**。

```
const int MAX_LEN       = 1024;
const std::string NAME  = "metroid";
```

但如果我们从C++程序的生命周期角度来看的话，就会发现，它和宏定义还是有本质区别的：**const定义的常量在预处理阶段并不存在，而是直到运行阶段才会出现**。

所以，准确地说，它实际上是运行时的“变量”，只不过不允许修改，是“只读”的（read only），叫“只读变量”更合适。

既然它是“变量”，那么，使用指针获取地址，再“强制”写入也是可以的。但这种做法破坏了“常量性”，绝对不提倡。这里，我只是给你做一个示范性质的实验，还要用到另外一个关键字volatile。

```
// 需要加上volatile修饰，运行时才能看到效果
const volatile int MAX_LEN  = 1024;

auto ptr = (int*)(&MAX_LEN);
*ptr = 2048;
cout << MAX_LEN << endl;      // 输出2048
```

可以看到，这段代码最开始定义的常数是1024，但是输出的却是2048。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/86/1e/a222129c.jpg" width="30px"><span>无止境</span> 👍（40） 💬（9）<div>c++的指针和引用有啥区别老师？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6d/68/e40b3300.jpg" width="30px"><span>Bluebuger</span> 👍（16） 💬（2）<div>volatile 在底层用的多，驱动、裸机开发这类。由于外部硬件设备，有部分处理器设计时候直接映射的内存地址，所以除了软件可以修改，硬件可能修改，所以需要让编译器不去优化这样的变量，必须从源头重新取值。</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3d/a0/acf6b165.jpg" width="30px"><span>奋斗</span> 👍（13） 💬（1）<div>《1》volitate： cpu每次读取数据的时候，如果寄存器或者三级缓存中有该值，则直接使用，所以此时如果内存中的值被改变，值不会改变。如果加上volitate每次绕过寄存器和缓存直接从内存读取，此时内存中的值已经改变了。
《2》mutable： 1、在lambal表达式中，如果捕获按值捕获，但是在函数体中想要修改，可以使用mutable
2、多线程环境下如果某个成员函数，比如int get_count() const { }，返回类中某个成员数量，势必会进行加锁保护变量达到线程安全，此时声明mutex必须是mutable的。
int get_count() const {
    std::lock_guard&lt;std::mutex&gt; lock(m)
    return count;
}
在声明mutable  std::mutex m; 需要加 mutable</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（12） 💬（1）<div>用好const 记住文章中的“ “const &amp;”可以引用任何类型，是函数入口参数的最佳类型” 是重点</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/13/f0/ce1a26be.jpg" width="30px"><span>罗杰</span> 👍（7） 💬（2）<div>C++ 中volatile 关键字, 我感觉最关键的是要知道, 他根本不构成 同步语义, 多线程编程中要杜绝使用. 
记得之前看过一个资料, volatile 从C++ 标准中出现的原因是 为了解决 &quot;硬件映射到内存上...&quot; 的问题, 也就是说 一般的开发者, 根本不会涉及到这一块. 

java 中 volatile 和 C++ 中的 volatile 还不一样, java 中的volatile 是构成 happen-before的, 是可以使用在多线程编程当中的</div>2020-08-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（7） 💬（2）<div>&quot;const 定义的常量在预处理阶段并不存在，而是直到运行阶段才会出现。&quot;,老师,那编译阶段它也没有出现吗?</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/4b/e0/0fa53fed.jpg" width="30px"><span>木须柄</span> 👍（3） 💬（1）<div>万能引用 (universal reference) 一般是指在函数模板时传入的 &quot;T&amp;&amp;&quot; 这种形参形式，主要作用是用来同时匹配左值和右值实参的传入，这里我觉得罗老师更多是借用了这个概念，主旨是为了说明 &quot;const &amp;&quot; 使用的广泛性</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/ce/0b/b1e244e6.jpg" width="30px"><span>IMBFD</span> 👍（3） 💬（1）<div>前辈在const函数那里为什么不说明其实是const修饰了this呢？这样就很好解释了</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/2c/06375913.jpg" width="30px"><span>宇天飞</span> 👍（3） 💬（1）<div>学完了这节课，你觉得今后应该怎么用 const 呢？
1、修饰常量、成员变量、成员函数
2、修饰类的时候注意const成员以及可变成员

给函数的返回值加上 const，也就是说返回一个常量对象，有什么好处？
使用更方便，防止意外修改</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/e5/54325854.jpg" width="30px"><span>范闲</span> 👍（3） 💬（1）<div>1. effecttive里主要的用处就是const替换define，const成员函数，const &amp;入参
2.返回常量对象就是实际上保持了内部状态的不可变。不受外部影响，实际上也是不希望外部改变对象</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/3c/f6e7ebf1.jpg" width="30px"><span>陈英桂</span> 👍（2） 💬（1）<div>1、函数的入参，返回值还有变量的定义根据实际的情况，使用const来保证变量值只可以读，不可以修改。STL的迭代器也有const和非const，使用迭代器如果没有修改操作，尽量使用const版本的迭代器。
2、函数的返回值总const，表示返回值只可以读</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/b8/22516d1a.jpg" width="30px"><span>韩泽文</span> 👍（2） 💬（1）<div>我之前的理解好像与这个有偏差：
const变量在未被优化时是分配到内存中，该内存页表标记为只读，不可写。 程序执行过程中尝试修改该内存就会页出错。
同样的，const在编译阶段能够起到 安全作用，凡是同一个编译单元(同一个cc文件尝试修改它就会报错)
上面提到的编译错误其实可以躲避编译器检查的，一般的定义时标注为const，另一cc文件引用时没有const，并且有修改操作，编译不报错的！
以上是c语言的理解，不知道有没有问题，
Cpp会对const变量符号修饰吗？</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/85/191eea69.jpg" width="30px"><span>搬铁少年ai</span> 👍（1） 💬（2）<div>函数返回值如果是return by value 就没必要加const了，除非返回的是一个引用。那可不可以不返回引用就直接返回一个值呢？可能具体情况还要具体看。多数情况应该没必要</div>2022-06-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/5xUYMKU9E8unPbOo5b1RibQYDnQ4eezrTC7icibYWY0KnjSrordvdcNEwacXZb8NQlVElp2DbHs45wZxynbMQiaZkQ/132" width="30px"><span>Geek_552f7a</span> 👍（0） 💬（1）<div>请问课外贴士第4点如何理解啊？无法声明 const this 是指什么，如果可以声明，函数应该写成什么样子呢？</div>2024-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/b3/7b/95adaf84.jpg" width="30px"><span>学习者</span> 👍（0） 💬（1）<div>打卡</div>2023-05-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BUJPBATdJ5PiaPbSPJjzfgwCvSu6QOmQSC1GY7At4spmhzO5xaxwTuVAkKrVxom0NkJclnULUqMdPlhdfpiaxEXw/132" width="30px"><span>Loca..</span> 👍（0） 💬（1）<div>我有一个问题，1.既然const在运行阶段才出现，那么文章后面所说的，对没有用volatile的const常量即使指针修改了值，他还是没用，因为在编译阶段被优化了，一个运行阶段才出现的值，怎么会在编译阶段被优化。所以我的问题是，const是不是在编译阶段就已经出现了呢</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/52/28/58d7fe3d.jpg" width="30px"><span>Kermit</span> 👍（0） 💬（1）<div>（我对 const 在“*”后面的用法“深恶痛绝”，每次看到这种形式，脑子里都会“绕一下”，实在是太难理解了，似乎感觉到了代码作者“深深的恶意”）
这句话我遇到一些case，比如 Object* const obj_; 后续一个方法会对Object 对象的属性进行update，这里是不是 使用* const 会更好点，因为毕竟还是要对obj进行数据update。</div>2022-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b5/1f/2b2dfb2e.jpg" width="30px"><span>王兵</span> 👍（0） 💬（1）<div>公司里的c++代码的类成员函数有很多都是const int之类的基础类型函数返回值，一直不理解为啥要加const。个人理解没有任何意义。之前一直做c开发，对c++不太了解，望老师解惑。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/6d/85723167.jpg" width="30px"><span>张飞Dear</span> 👍（0） 💬（1）<div>1，
（1）定义函数入口参数，尽量多的用const， 对于一些输入参数 可以直接使用const &amp; 万能引用来做入口。 
（2）在类中定义一些const 函数，让编译器更好的优化。
（3）多用const 来定义一些常量，少用 #define 来定义常量，让代码更安全。
2，返回常量对象，只读状态，不让外界进行操作。</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/33/e7/145be2f9.jpg" width="30px"><span>怪兽</span> 👍（0） 💬（2）<div>1. 常量的名称都是大写，但前面加k前缀表。这是什么风格？为什么是k？
2. constexpr关键字是表示编译阶段的常量，而const表示运行时期的常量，只不过被编译器优化了，是这样理解吗？const和constexpr还有什么区别吗？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/14/ca4a1ae9.jpg" width="30px"><span>itsiam</span> 👍（0） 💬（1）<div>给函数返回值加const， 返回常量对象，可以保证改实例的成员变量不被修改。</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f6/e3/e4bcd69e.jpg" width="30px"><span>沉淀的梦想</span> 👍（0） 💬（4）<div>不太理解老师所说的 `const &amp;`  万能引用，写了个 demo 发现编译不不过啊：

```
int test(const int&amp; any) {

}

int main() {
    int a = 2;
    &#47;&#47; error: invalid conversion from ‘int*’ to ‘int’
    test(&amp;a);
}
```

因为本人工作中写的语言不是 c++，出于兴趣来学习的，问题可能有点小白，老师见谅。</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/45/d1621188.jpg" width="30px"><span>学渣汪在央企打怪升级</span> 👍（0） 💬（1）<div>突然发现是学长啊。
感觉C++ Primer挺好的，如果看得过程中留意变量定义，会归纳出const的用法的，其实照着书上的例子好好的理解为什么用const，什么时候用，也就懂了。当然老师你归纳得也非常好。</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/97/fc/0ca13c5c.jpg" width="30px"><span>xGdl</span> 👍（0） 💬（2）<div>对于const，存在常量折叠，老师所说的readonly非常到位，但对于const前后的*，只需要掌握类型的读取规则其实也就很简单《c++语法详解》，左结合优先即可。

volatile修饰，阻止编译器优化，听说在msvc具有原子保证，而gcc不保证。</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8b/19/a15d060d.jpg" width="30px"><span>silverhawk</span> 👍（0） 💬（1）<div> const 那个左右是遗传自C的那个左右法则，写代码时候也深恶痛绝，尤其是几层嵌套的const，最好加个括号一目了然。另外volatile也是经常需要跟硬件打交道的地方比较多，比如某个寄存器的值，可能程序不会修改但是被硬件中段信号修改，不过这些现在C++用不太到 了</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（2）<div>&quot;它可以修饰引用和指针，“const &amp;”可以引用任何类型，是函数入口参数的最佳类型&quot;

不太理解这个，能麻烦举个例子吗？

谢谢！</div>2020-05-22</li><br/><li><img src="" width="30px"><span>java2c++</span> 👍（0） 💬（1）<div>1.成员变量采用const代替宏定义define，功效有点类似于Java的final关键字，目的只是为了编译环节进行替换</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（0） 💬（2）<div>拿什么练手呢...工作中读C++较多， 写的少。</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b4/63/59bb487d.jpg" width="30px"><span>eletarior</span> 👍（0） 💬（1）<div>在所有能使用const的地方使用const，增强代码的健壮性，使用多了，你未必看到它的好，但是它确实在那里发挥着作用，这样的回答有点人云亦云了。
返回一个常量对象，最直接的作用是保证在函数返回时无法直接修改这个对象，比如 funcret()++ ，这种代码会在编译器失败，可以起到保护对象的作用。其他的好处需要老师指点下了
</div>2020-05-21</li><br/>
</ul>