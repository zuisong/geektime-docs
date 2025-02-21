你好，我是吴咏炜。

本讲我们将介绍函数对象，尤其是匿名函数对象——lambda 表达式。今天的内容说难不难，但可能跟你的日常思维方式有较大的区别，建议你一定要试验一下文中的代码（使用 xeus-cling 的同学要注意：xeus-cling 似乎不太喜欢有 lambda 的代码😓；遇到有问题时，还是只能回到普通的编译执行方式了）。

## C++98 的函数对象

函数对象（function object）\[1] 自 C++98 开始就已经被标准化了。从概念上来说，函数对象是一个可以被当作函数来用的对象。它有时也会被叫做 functor，但这个术语在范畴论里有着完全不同的含义，还是不用为妙——否则玩函数式编程的人可能会朝着你大皱眉头的。

下面的代码定义了一个简单的加 *n* 的函数对象类（根据一般的惯例，我们使用了 `struct` 关键字而不是 `class` 关键字）：

```c++
struct adder {
  adder(int n) : n_(n) {}
  int operator()(int x) const
  {
    return x + n_;
  }
private:
  int n_;
};
```

它看起来相当普通，唯一有点特别的地方就是定义了一个 `operator()`，这个运算符允许我们像调用函数一样使用小括号的语法。随后，我们可以定义一个实际的函数对象，如 C++11 形式的：
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/00/2007d2f3.jpg" width="30px"><span>zhengfan</span> 👍（34） 💬（1）<div>吴老师，您好。
四刷本讲。
我对您文中的这一句介绍有点好奇，“每个 lambda 表达式都有一个全局唯一的类型”。 请问这是怎么做到的？本质上不应该是一个函数指针么？这么规定的目的是什么？</div>2020-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/c4/8679ca8a.jpg" width="30px"><span>廖熊猫</span> 👍（17） 💬（1）<div>老师新年快乐。
lambda表达式大概是生成了一个匿名的struct吧，实现了operator(), 捕获的话对应struct上的字段。</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（9） 💬（1）<div>1、感觉lambda表达式就是C++中的闭包。

2、lambda表达式可以立即进行求职，这一点和JavaScript里的立即执行函数（Imdiately Invoked Function Expression，IIFE）一样。在JavaScript里，它是用来解决作用域缺陷的。

感觉在动态语言里被用到极致的闭包等特性，因为C++的强大、完备，在C++里很普通。

lambda的定义对应一个匿名函数对象，捕获就是构造这个对象时某种方式的初始化过程，用lambda表达式隐藏了这个过程，只保留了这个意思，更直观和写意。

老师，我对协程很感兴趣，C++会有协程么？隐约感觉捕获变量这个东西是不是可以用在实现协程上？

最后，祝老师新年快乐！</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（5） 💬（2）<div>老师，回过头来看得时候，遇到了一个问题。

在用LAMBDA表达式解决多重初始化路径的问题时，说到这样还可以提高性能，因为不需要默认构造和不需要拷贝&#47;移动。可是在第10讲中讲返回值优化的时候，不是说如果返回值时有条件判断，编译器都被会难倒，从而导致NRVO失效么（函数getA_duang）？</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/96/c679bb3d.jpg" width="30px"><span>总统老唐</span> 👍（4） 💬（1）<div>2020第一课，吴老师新年好</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/67/24/32c58f77.jpg" width="30px"><span>Daniel</span> 👍（3） 💬（2）<div>class task {
public:
  task(int data) : data_(data) {}
  auto lazy_launch()
  {
    return
      [this, count = get_count()]()
      mutable {
        ostringstream oss;
        oss &lt;&lt; &quot;Done work &quot; &lt;&lt; data_
            &lt;&lt; &quot; (No. &quot; &lt;&lt; count
            &lt;&lt; &quot;) in thread &quot;
            &lt;&lt; this_thread::get_id()
            &lt;&lt; &#39;\n&#39;;
        msg_ = oss.str();
        calculate();
      };
  }
  void calculate()
  {
    this_thread::sleep_for(100ms);
    cout &lt;&lt; msg_;
  }

private:
  int data_;
  string msg_;
};

输出：
Done work 37 (No. 2) in thread 3
Done work 37 (No. 2) in thread 3

按引用捕获，应该是线程1输出之前msg_被线程2覆盖了。</div>2022-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/21/56/91669d26.jpg" width="30px"><span>ReCharge</span> 👍（2） 💬（1）<div>&amp; 加本地变量名标明对其按引用捕获（不能在默认捕获符 &amp; 后出现；因其已自动按引用捕获所有本地变量）
老师这句话有问题么？括号内外感觉描述矛盾
&amp;本地变量名：这种写法不被允许么？</div>2022-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（2） 💬（2）<div>最近项目里使用到了libgo这个C++写的协程库，示例代码中用到了好多老师今天讲的知识点：
void foo()
{
    printf(&quot;function pointer\n&quot;);
}

struct A {
    void fA() { printf(&quot;std::bind\n&quot;); }
    void fB() { printf(&quot;std::function\n&quot;); }
};
int main()
{
    go foo;

    go []{
        printf(&quot;lambda\n&quot;);
    };

    go std::bind(&amp;A::fA, A());

    std::function&lt;void()&gt; fn(std::bind(&amp;A::fB, A()));
    go fn;
}
其中跟在&quot;go&quot;后面的内容总算能理解了，但是&quot;go&quot;的实现原理还是没搞懂，不知道后面协程这块的内容会不会有讲到。
另外对老师今天讲的 ”一般而言，按值捕获是比较安全的做法。按引用捕获时则需要更小心些，必须能够确保被捕获的变量和 lambda 表达式的生命期至少一样长“ 这句话深有体会，我在项目里按值捕获指针给协程用，结果调试的时候就是各种随机的崩溃。。。</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（2） 💬（1）<div>编译器遇到lambda 表达式时，产生一个匿名的函数对象，各种捕获相当于按值或者按引用设置给匿名对象的成员字段。
不对的地方，望老师指正。
对function&lt;int(int, int)&gt;这货怎么实现的比较好奇，大多数模板参数都是类型，做的都是是类型推导，这货居然是int(int, int)</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/57/2e/ab2d041d.jpg" width="30px"><span>西雨川久</span> 👍（1） 💬（1）<div>我提一个小问题：

原文：虽然函数名字叫 accumulate——累加——但它的行为是通过第四个参数可修改的。我们把上面的加号 + 改成星号 *，上面的计算就从从 1 加到 5 变成了算 5 的阶乘了。

实际上，还需要把第三个参数改成1，否则结果是0.</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/00/2007d2f3.jpg" width="30px"><span>zhengfan</span> 👍（1） 💬（2）<div>吴老师您好，请教一下：
对于形如[]() mutable {}的lamda表达式 还能够被认为是一个constexpr吗？</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/ea/2b2adda5.jpg" width="30px"><span>EncodedStar</span> 👍（1） 💬（1）<div>函数指针和引用这个模块中
当我们拿 add_2 去调用这三个函数模板时，fn 的类型将分别被推导为 int (*)(int)、int (&amp;)(int) 和 int (*)(int)。
第一个和第三个都是 int (*)(int) 第一个是不是  int (int)</div>2020-01-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep73FalJJ7FPUJAcK2Ket1Qia1HOHhmaEcd8zdr4O6LHHk5NwzyUTnBAOzgmMtR3H0gSgYcbH6N5Vg/132" width="30px"><span>空气</span> 👍（1） 💬（1）<div>吴老师，我在工作中很经常用到function。文中讲到function对象的创建比较耗资源，能否介绍一下原因，或者可以参考哪些资料？确实要使用的话，是否有必要使用共享指针管理来减轻复制和转移消耗？
如果lambda的推导类型不是function，那是什么类型呢？和function有什么区别？</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4e/20/83151e94.jpg" width="30px"><span>viper</span> 👍（1） 💬（2）<div>老师，为什么上面会说用add_2去调用那三模版函数返回值都是2，不该是4吗？</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/38/3a/102afd91.jpg" width="30px"><span>你好梦梦</span> 👍（0） 💬（1）<div>老师，对于一个function类型，如果把他作为函数型参，是用引用好，还是直接传值好</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3f/7d/f624fa69.jpg" width="30px"><span>当初莫相识</span> 👍（0） 💬（1）<div>关于多线程那里，有个疑问。我在尝试将*this换为=，同样都是按值捕获，为什么结果却不同呢
return [=, count = get_count()]()。
我记得[]里=是按值捕获，&amp;引用捕获，是我哪里没理解对吗，还是C++标准不同所致。</div>2022-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/2d/0b/e6836053.jpg" width="30px"><span>莫言</span> 👍（0） 💬（2）<div>请问下吴老师，this按引用捕获的时候，为什么get_count返回的值也是一样的呢？虽然引用不产生拷贝，但是get_count不是实实在在的执行了两次么</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/04/41/a044b81c.jpg" width="30px"><span>薛凯文</span> 👍（0） 💬（1）<div>Hello，老师。关于lambda adder。 
auto adder = [](int n) {
  return [n](int x) {
    return x + n;
  };
};
如果里面的lambda改成引用捕获，如下所示：
auto adder = [](int n) {
  return [&amp;n](int x) {
    return x + n;
  };
};
结果就是不对的了. adder(3)(5)的结果是10(5 + 5). 请问是什么原因啊？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/66/ed/a1233b74.jpg" width="30px"><span>蔡冰成</span> 👍（0） 💬（2）<div>hi, 吴老师
    auto dbl_lambda = [](const int&amp; x) {return x * x;};
    int dbl1 = dbl_lambda(3);
关于&quot;只要能满足 constexpr 函数的条件，一个 lambda 表达式默认就是 constexpr 函数&quot;这个结论, 我用上面对代码编译之后, 计算3*3依然是运行时调用, 使用的是https:&#47;&#47;gcc.godbolt.org&#47;, 编译环境x86-64 gcc10.2
 call   401172 &lt;main::{lambda(int)#1}::operator()(int) const&gt;
 mov    DWORD PTR [rbp-0x4],eax
请问是有什么地方不正确吗? 如果使用正常对函数加constexpr声明则是编译期计算的</div>2021-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/00/2007d2f3.jpg" width="30px"><span>zhengfan</span> 👍（0） 💬（3）<div>吴老师您好。
请问利用lamda表达式来替换bind,是否要使用std::thresholders来传递参数?</div>2020-06-30</li><br/><li><img src="" width="30px"><span>晚风·和煦</span> 👍（0） 💬（1）<div>老师，一个空类，编译器没有生成默认的构造函数是吗？😂</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/5c/b5d79d20.jpg" width="30px"><span>李亮亮</span> 👍（0） 💬（6）<div>Microsoft Visual Studio Community 2019  版本 16.4.2，语言标准：C++17 例子编译不过，水平又菜，不会改。</div>2020-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8c/df/77acb793.jpg" width="30px"><span>禾桃</span> 👍（0） 💬（9）<div>&quot;请自行运行一下代码，并把 *this 改成 this，看看输出会有什么不同。&quot;

int get_count()
{
    static int count = 0;
    return ++count;
}

class task {
public:
    task(int data) : data_(data) { cout &lt;&lt; __func__ &lt;&lt; &quot;|&quot; &lt;&lt; this &lt;&lt; endl; }
    auto lazy_launch()
    {
        return
            &#47;&#47; *this 标明按值捕获外围对象
            &#47;&#47; 变量名 = 表达式 标明按值捕获表达式的结果
                [this, count = get_count()]()
                        mutable { &#47;&#47; mutable 标记使捕获的内容可更改
                    cout &lt;&lt; __func__ &lt;&lt; &quot;|&quot; &lt;&lt; this &lt;&lt; endl;
                    ostringstream oss;
                    oss &lt;&lt; &quot;Done work &quot; &lt;&lt; data_
                        &lt;&lt; &quot; (No. &quot; &lt;&lt; count
                        &lt;&lt; &quot;) in thread &quot;
                        &lt;&lt; this_thread::get_id()
                        &lt;&lt; &#39;\n&#39;;
                    msg_ = oss.str();
                    calculate();
                };
    }
    void calculate()
    {
        this_thread::sleep_for(100ms);
        cout &lt;&lt; msg_;
    }

private:
    int data_;
    string msg_;
};

int main()
{
    auto t = task{37};
    thread t1{t.lazy_launch()};
    thread t2{t.lazy_launch()};
    t1.join();
    t2.join();
}

 打印输出
task|0x7ffe6f0e7120
operator()|0x7ffe6f0e7120
operator()|0x7ffe6f0e7120
Done work 37 (No. 2) in thread 140331800897280 
Done work 37 (No. 2) in thread 140331800897280

不太明白为什么，
#1 t1, t2这两个thread有同样的thread id(140331800897280)？
#2 为什么 count在， t1, t2运行时，打印出的都是2(No. 2)？

多谢！</div>2020-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（0） 💬（1）<div>请问老师后续会讲关于类对象及虚函数表相关知识吗，这块比较薄弱</div>2020-01-01</li><br/>
</ul>