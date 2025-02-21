你好，我是Chrono。

在[第1节课](https://time.geekbang.org/column/article/231454)的时候，我就说到过“函数式编程”，但只是简单提了提，没有展开讲。

作为现代C++里的五种基本编程范式之一，“函数式编程”的作用和地位正在不断上升，而且在其他语言里也非常流行，很有必要再深入研究一下。

掌握了函数式编程，你就又多了一件“趁手的兵器”，可以更好地运用标准库里的容器和算法，写出更灵活、紧凑、优雅的代码。

所以，今天我就和你聊聊函数式编程，看看它给C++带来了什么。

## C++函数的特殊性

说到“函数式编程”，那肯定就要先从函数（function）说起。

C++里的函数概念来源于C，是面向过程编程范式的基本部件。但严格来说，它其实应该叫“子过程”（sub-procedure）、“子例程”（sub-routine），是命令的集合、操作步骤的抽象。

函数的目的是封装执行的细节，简化程序的复杂度，但因为它有入口参数，有返回值，形式上和数学里的函数很像，所以就被称为“函数”。

在语法层面上，C/C++里的函数是比较特别的。虽然有函数类型，但不存在对应类型的变量，不能直接操作，只能用指针去间接操作（即函数指针），这让函数在类型体系里显得有点“格格不入”。

函数在用法上也有一些特殊之处。在C/C++里，所有的函数都是全局的，没有生存周期的概念（static、名字空间的作用很弱，只是简单限制了应用范围，避免名字冲突）。而且函数也都是平级的，不能在函数里再定义函数，也就是**不允许定义嵌套函数、函数套函数**。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/09/16/1161017c.jpg" width="30px"><span>罗剑锋</span> 👍（23） 💬（2）<div>我在GitHub的lambd.cpp里写了一小段代码，示范了function + lambda实现成员函数的方法，算是对课下作业2的一个参考，同学们可以看看。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/d4/77/21a75ab3.jpg" width="30px"><span>冻冻</span> 👍（66） 💬（6）<div>老师，用“map+lambda”的方式来替换难以维护的 if&#47;else&#47;switch，能举个例子吗？</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9e/89/6e9c05d6.jpg" width="30px"><span>被讨厌的勇气</span> 👍（24） 💬（2）<div>采用lambda表达式替换类的成员函数，成员变量通过 &#39;[this]&#39;可以捕获（相当于成员函数中的this参数），参数、返回值、函数体，lambda表达式都可以实现，所以理论上，是可以替换的。

试了一下，报错：在类内部无法定义auto。之前老师提到过的。</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/97/fc/0ca13c5c.jpg" width="30px"><span>xGdl</span> 👍（18） 💬（2）<div>lambda由类的operator重载而来，最大的特征是携带私货（闭包），我一般使用闭包最多的就是将任务打包Task推送线程池或下一个流程。这一过程在没有闭包之前，实现起来有些麻烦。</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/ba/01762322.jpg" width="30px"><span>海怪哥哥</span> 👍（9） 💬（1）<div>关于lambda对于外部变量的捕获。大家可以这样理解更容易，如果把lambda表达式看成一个常规的变量，那么相同作用域（比如同一个函数）内的变量跟常量对它都是可见的。</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8f/0a/22863f93.jpg" width="30px"><span>sp0917</span> 👍（7） 💬（1）<div>罗老师，
auto pfunc = &amp;my_square;    【1】
auto pfunc = my_square;       【2】
这两种表示有什么区别？
我一直认为函数名和函数指针是对等的，所以我直觉就是使用【2】，但发现这两个在使用pfunc进行操作时效果一样。</div>2020-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/a3/23540579.jpg" width="30px"><span>robonix</span> 👍（5） 💬（1）<div>老师，lambda表达式是不是没有常量引用呢？如果怕修改被捕获的变量只能用值传递，那么就有拷贝发生了？</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/a0/c94a1a64.jpg" width="30px"><span>张JL</span> 👍（5） 💬（1）<div>我常用lambda替换函数中的小段重复代码。
相同代码重复写几遍感觉很蠢，拿出来做成函数又没有必要，因为没有其他的调用需求，这时候用lambda就简洁多了</div>2020-05-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKibu8C3CeYGFicJ1kRwibvSGYjaC0R3HsAVBNDE0seEI33Lm7GZ4LibTnVHWcGiczVxfzDLLqySjjoFzQ/132" width="30px"><span>Charles</span> 👍（4） 💬（1）<div>感觉lambda和函数指针的差别好像不是太大，可能是我还没有真正理解吧，我觉得lambda的捕获功能，普通函数也可以用传引用的方式实现？然后将函数打包到别的地方，是不是也可以把普通函数的函数指针打包到别的地方？</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6d/68/e40b3300.jpg" width="30px"><span>Bluebuger</span> 👍（3） 💬（1）<div>Map + lambda是个好东西 想起了以前做 虚拟机时候指令操作码处理时候的一堆case(switch语句)</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/8b/e3b827b7.jpg" width="30px"><span>笨蛋小孩</span> 👍（3） 💬（1）<div>老师早啊!</div>2020-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（2） 💬（2）<div>普通函数所不具备的特殊本领，就是可以“捕获”外部变量，在内部的代码里直接操作.如果外部变量n定义最外层,且在普通函数前面,也是可以在函数中使用到的.此时应该和lambda没有区别了吧?</div>2021-01-05</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ywSuwVNMKNjRLPMjZmpQOQHWW2usAu8RwRIOlBHaVVU6J3xHdtibgO6FVzYkRIkV50vCr62ia4OwJp07giabiazUGA/132" width="30px"><span>ripple</span> 👍（2） 💬（2）<div>罗老师，lamda不能传到外界去么？我发现不捕获变量就可以传，捕获了就传不了，不清楚哪条语法可以解决
testB(void (*func)(std::string)) {
}

test() {
    std::string result = &quot;&quot;;
    auto func = [&amp;result] (std::string params) mutable{
        result = params;
    };

   testB(func);
}</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d6/67/5e0cac1b.jpg" width="30px"><span>Tedeer</span> 👍（2） 💬（1）<div>我看到老师文章中说到每个lambda表达式都有个全局唯一类型，只有编译器知道；lambda表达式只能通过auto声明，且auto变量必须在定义时初始化，而在类声明时，成员并未被赋值，就不知道lambda表达式类型，无法推导出具体类型，编译器会报错，所以无法使用lambda表达式作成员函数，请问老师我这样理解对吗？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（2） 💬（6）<div>个人认为lambda表达式还有个重要的用途是它可以自定义stl函数谓词规则(pred)，例如自定义排序规则，而无需使用传统的仿函数那种麻烦的方法。</div>2020-05-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BUJPBATdJ5PiaPbSPJjzfgwCvSu6QOmQSC1GY7At4spmhzO5xaxwTuVAkKrVxom0NkJclnULUqMdPlhdfpiaxEXw/132" width="30px"><span>Loca..</span> 👍（1） 💬（1）<div>有一个问题是，在：“lambda 的注意事项--2.lambda的变量”这一小节里，既然[=]是按值捕获，那么表达式里面的就是外部值的拷贝，既然是拷贝，那么就与原x独立了，但在下面的代码第三行注释里却说x只读，不允许修改，我的理解是它可以修改，但是修改的是这份拷贝，而不是上面的x.所以第三行是可以存在的，您觉得呢</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/67/057e5d93.jpg" width="30px"><span>flying</span> 👍（1） 💬（2）<div>老师你好：

如果用function包装lambda表达式，是否可以作为类的成员变量？然后再lambda表达式里面操作类的成员变量。例如

#include &lt;funcitional&gt;
typedef  std::function&lt;void(int)&gt; Handler;

class Test
{
public:
        Test(int type)
        {
		    if (1 == type)
			{
				handler = [this](int t)
			    {
			        m_int_list.push_back(t);
			    };
			}
			else
			{
			    handler = [this](int t)
			    {
			        m_int_list.push_back(t + 1);
			    };
			}
		}
        
        int insert(int t)
		{
		    handler(t);
		}
private:
    Handler handler;
	std::list&lt;int&gt; m_int_list;
};

这个例子能够运行成功，并且不会出现coredump。
但是在实际的系统中，编写了类似的代码，结果导致coredump。每当lambda表达式访问类的成员变量时，就会coredump。

老师，这是什么原因呢？

最后通过函数指针的形式解决的。</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6b/0d/74aeb985.jpg" width="30px"><span>睡着的海豚</span> 👍（0） 💬（1）<div>lambda表达式无法替换成员函数，因为lambda表达式是局部的，生命周期短，流程式控制；成员函数要求函数可以隶属于所有对象，还要求函数能在本类中调用的同时也能在外部类中被调用，面向对象式控制</div>2023-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/6c/419506e5.jpg" width="30px"><span>野焚，雪祭</span> 👍（0） 💬（1）<div>让我想起了以前经常用的js的underscore和lodash</div>2023-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/3d/f5/177a2a05.jpg" width="30px"><span>🍁枫叶</span> 👍（0） 💬（2）<div>感谢Chrono老师的对lambda表达式的讲解，因为C++这块之前我一直很难理解，也不会写，总感觉怪怪的，不像python，C#那样用着顺手。但是通过老师这节课的讲解，我发现我突然懂了，而且对其结构有了深刻的印象，复杂的不说，简单的已经会写了，看着也不那么奇怪了，有醍醐灌顶之功效。</div>2023-01-13</li><br/><li><img src="" width="30px"><span>鲁宁</span> 👍（0） 💬（1）<div>匿名使用lambda表达式是不是就是在定义的时候有直接调用呢？
</div>2022-11-29</li><br/><li><img src="" width="30px"><span>Geek5657</span> 👍（0） 💬（2）<div>lambda表达式捕获share_ptr时，   lambda表达式又被其他对象长期持有，导致share_ptr 永远无法释放怎么解决呢？
lambda 表达式内部 是知道可释放 share_ptr 的时机，但是share_ptr 本身没有  release的接口，无法释放</div>2022-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJaLyy9PnSBlWdPzUH3ic0DWdfoeUNSmew2RVoUs8N864M1Pm0U7POyVu0DT6lVJVvzL1B29oGKHlA/132" width="30px"><span>Geek_19fed9</span> 👍（0） 💬（1）<div>老师，我试了一下示例代码，我看到在DemoLambdal里定义了一个返回值auto的print函数。用c++11编译不过，用14就能编译过了，意思是14版以后就支持了类内使用auto了吗？</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/09/f2/6ed195f4.jpg" width="30px"><span>于小咸</span> 👍（0） 💬（1）<div>map+lambda 方法很不错诶，以后多实践下</div>2021-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b3/17/9f6d67dc.jpg" width="30px"><span>超越杨超越</span> 👍（0） 💬（1）<div>请问一下，lamda和c中的匿名函数相比有啥不同呢</div>2021-03-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ7mAt63VrbLZPHpeZxSc4IlBYswQSnaAB5wGePaGFDehgiaNfIxI1SJ5yIHIlmVk8hsw0RaoaSCPA/132" width="30px"><span>Stephen</span> 👍（0） 💬（2）<div>现代 C++ 里的五种基本编程范式，我只知道四种：面向过程，面向对象，泛型编程和函数式编程，请问老师，另一种是什么？</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/70/bdf11801.jpg" width="30px"><span>小政哥</span> 👍（0） 💬（2）<div>局部的变量 lambda变量捕获与文中相同
相关代码
auto f6 = []()
{
    int count = 10;
    cout &lt;&lt; &quot;f6&quot; &lt;&lt; endl;
    &#47;&#47;auto f7 = [=, &amp;count]()
    auto f7 = [=, &amp;count]()
    {
        cout &lt;&lt; &quot;f7&quot; &lt;&lt; endl;
        count += 30;
        cout &lt;&lt; count &lt;&lt; endl;
    };
    f7();
    cout &lt;&lt; count &lt;&lt; endl;
};
但是全局变量 按值和引用都可以修改</div>2020-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/70/bdf11801.jpg" width="30px"><span>小政哥</span> 👍（0） 💬（1）<div>visual studio 2019 编译
lambda变量捕获是否需要区分 捕获的是局部变量还是全局变量？
我捕获全局变量  用值捕获还是引用捕获都是可以修改的，但是不支持 auto f3 = [=, &amp;x]()       &#47;&#47; lambda表达式，用“&amp;”按引用捕获x，其他的按值捕获 这种方式 错误是：无法使用 lambda ， 捕获必须是来自封闭函数范围的变量
我捕获局部变量 用值捕获不能修改，引用捕获可以修改的，第三种方式也是支持的</div>2020-10-11</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ywSuwVNMKNjRLPMjZmpQOQHWW2usAu8RwRIOlBHaVVU6J3xHdtibgO6FVzYkRIkV50vCr62ia4OwJp07giabiazUGA/132" width="30px"><span>ripple</span> 👍（0） 💬（1）<div>最近在一个方法里要发送一条指令，去同步的从服务器获取返回结果
func test{
 std::string result = &quot;&quot;;
 define c = lamda;
 发送携带了lamda的数据结果到消息处理队列
 信号量等待
 返回result
}

lamda中捕获了result值，将lamda传给了处理消息的队列，然后网络返回后，调用了对应消息的这个lamda的函数指针，并修改result的值，但是这种写法打死编译不过，不晓得咋搞，最后还是采用的一个全局对象来存储。</div>2020-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/2c/06375913.jpg" width="30px"><span>宇天飞</span> 👍（0） 💬（1）<div>你对函数式编程有什么样的理解和认识呢？
1、函数式变量像是一个数据公式，可以不断调用
2、相对于常规的函数，函数式编程会更加灵活，像是当前上下文一部分的概念
3、多个组合容易实现

lambda 表达式的形式非常简洁，可以在很多地方代替普通函数，那它能不能代替类的成员函数呢？为什么？
1、可以
2、成员变量初始化</div>2020-09-01</li><br/>
</ul>