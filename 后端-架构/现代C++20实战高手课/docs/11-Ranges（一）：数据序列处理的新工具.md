你好，我是卢誉声。

第一章，我们详细了解了C++20支持的三大核心语言特性变更——Modules、Concepts和Coroutines。但是通常意义上所讲的C++，其实是由核心语言特性和标准库（C++ Standard Library）共同构成的。

对标准库来说，标准模板库STL（Standard Template Library）作为标准库的子集，是标准库的重要组成部分，是C++中存储数据、访问数据和执行计算的重要基础设施。我们可以通过它简化代码编写，避免重新造轮子。

不过标准模板库不是完美的，它也在不断演进。原本的标准模板库，并没有给大规模、复杂数据的处理方面提供很好的支持。这是因为，C++在语言和库的设计上，让C++函数式编程变得复杂且冗长。为了解决这个问题，从C++20开始支持了Ranges——这是C++支持函数式编程的一个巨大飞跃。

特别是C++在运行时性能方面的绝对优势，Ranges让C++逐渐成为了处理大规模复杂数据的新贵。所以，我们更有必要掌握它，我相信在学完Ranges后，你会爱上这种便利的数据处理方式！

好了，话不多说，就让我们从C++函数式编程开始今天的学习吧（项目的完整代码，你可以[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>工作中防止越界访问一般是在访问前进行if条件判断，如果没有越界才会进行访问操作。而且在代码中也会增加捕获越界访问异常的代码。
下面是我根据老师的提示写的一个Range概念：template &lt;typename T&gt;
concept Range = requires(T container){
    {std::ranges::begin(container)};
    {std::ranges::end(container)};
};
</div>2024-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：“假设 f(x,g) 的定义为 g(x)”，这句话表面上理解是：g(x)=f(x,g)。但好像说不通啊。f(x,g)的参数g的定义为g(x)，是不是这样啊。
Q2：auto是由编译器来自动判断类型吗？（类似于弱类型语言了）
Q3：迭代器与只读迭代器有什么区别？难道迭代器除了“读”还可以“写”吗？ 另外，逆向迭代器，比如begin，正常是从第一个向后面遍历，那“逆向”难道会向前遍历？（已经是第一个，不可能向前遍历啊）
Q3：代码的运行环境是什么样的？
对于实例代码，想运行一下看看，IDE是什么啊，包括设置编译器版本为c++20等。
Q4：“start = std::find(getArray().begin(), getArray().end(), 1);”调用后为什么会变成悬空指针？能否再详细说明一下？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5c/c9/f1b053f2.jpg" width="30px"><span>Family mission</span> 👍（0） 💬（1）<div>#include &lt;vector&gt;
#include &lt;algorithm&gt;
#include &lt;ranges&gt;
#include &lt;iostream&gt;
 
int main() {
    namespace ranges = std::ranges;
 
    auto getArray = [] { return std::vector{ 0, 1, 0, 1 }; };
 
    &#47;&#47; 编译成功
    auto start = std::find(getArray().begin(), getArray().end(), 1);
    std::cout &lt;&lt; *start &lt;&lt; std::endl;
 
    &#47;&#47; 编译失败
    auto rangeStart = ranges::find(getArray(), 1);
    std::cout &lt;&lt; *rangeStart &lt;&lt; std::endl;
 
    return 0;
}
这个代码块中auto getArray = [] { return std::vector{ 0, 1, 0, 1 }; };编译器会报错，需要改成 auto getArray = [] { 
        
        return std::vector&lt;int&gt;{ 0, 1, 0, 1 };
        
    };才可以</div>2023-12-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJo05FofKFWYN3joX4OyCfVrU2kK7xvKdZ4Ho7bof893fE0jXk1OcB5sKLk4C1SviaNlibAiaCtp8aww/132" width="30px"><span>努力学习不准懈怠</span> 👍（0） 💬（1）<div>
#include &lt;vector&gt;
#include &lt;algorithm&gt;
#include &lt;ranges&gt;
#include &lt;iostream&gt;
 
int main() {
    namespace ranges = std::ranges;
 
    &#47;&#47; 首先，调用ranges::begin和ranges::end函数获取容器的迭代器
    &#47;&#47; 接着，通过迭代器访问数据中的元素
    std::vector&lt;int&gt; v = { 3, 1, 4, 1, 5, 9, 2, 6 };
    auto start = ranges::begin(v);
    std::cout &lt;&lt; &quot;[0]: &quot; &lt;&lt; *start &lt;&lt; std::endl;
 
    auto curr = start;
    curr++;
    std::cout &lt;&lt; &quot;[1]: &quot; &lt;&lt; *curr &lt;&lt; std::endl;
 
    std::cout &lt;&lt; &quot;[5]: &quot; &lt;&lt; *(curr + 3) &lt;&lt; std::endl;
 
    auto stop = ranges::end(v);
    std::sort(start, stop);
 
    &#47;&#47; 最后，调用ranges::cbegin和ranges::cend循环输出排序后的数据
    for (auto it = ranges::cbegin(v);
        it != ranges::cend(v);
        ++it
    ) {
        std::cout &lt;&lt; *it &lt;&lt; &quot; &quot;;
    }
    std::cout &lt;&lt; std::endl;
 
    return 0;
}
这段代码第19行应该是std::cout &lt;&lt; &quot;[4]: &quot; &lt;&lt; *(curr + 3) &lt;&lt; std::endl;</div>2023-02-22</li><br/>
</ul>