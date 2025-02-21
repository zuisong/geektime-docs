你好，我是卢誉声。

上一讲，我们重点讨论了C++传统函数式编程的困境，介绍了Ranges的概念，了解到range可以视为对传统容器的一种泛化，都具备迭代器等接口。但与传统容器不同的是，range对象不一定直接拥有数据。

在这种情况下，range对象就是一个视图（view）。这一讲，我们来讨论一下视图，它是Ranges中提出的又一个核心概念，是Ranges真正解放函数式编程的重要驱动力（项目的完整代码，你可以[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

## 视图

视图也叫范围视图（range views），它本质是一种轻量级对象，用于间接表示一个可迭代的序列。Ranges也为视图实现了视图的迭代器，我们可以通过迭代器来访问视图。

对于传统STL中大部分可接受迭代器参数的算法函数，在C++20中都针对视图和视图迭代器提供了重载版本，**比如ranges::for\_each等函数，这些算法函数在C++20中叫做Constraint Algorithm**。

那么Ranges库提供的视图有哪些呢？

我把视图类型和举例梳理了一张表格，供你参考。

![](https://static001.geekbang.org/resource/image/ab/15/ab5c7d5043e35756c8dfe7784cafb615.jpg?wh=3500x1365)

所有的视图类型与函数，都定义在std::ranges::views命名空间中，标准库也为我们提供了std::views作为这个命名空间的一个别名，所以实际开发时我们可以直接使用std::views。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/27/27/a6/32e9479b.jpg" width="30px"><span>tang_ming_wu</span> 👍（5） 💬（1）<div>对比函数式编程实现和传统编程实现，我个人觉得函数式编程只是伪需求和一小部分人的自嗨：（1）不方便调试（2）不方便设计解耦（3）不方便维护（4）不方便阅读理解。</div>2023-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5c/c9/f1b053f2.jpg" width="30px"><span>Family mission</span> 👍（0） 💬（1）<div>views::reverse和ranges::reverse_view的使用
#include &lt;iostream&gt;
#include &lt;ranges&gt;
 
int main()
{
    namespace ranges=std::ranges;
    namespace views = std::views;
    static constexpr auto il = {3, 1, 4, 1, 5, 9};
 
    ranges::reverse_view rv{il};
    for (int i : rv)
        std::cout &lt;&lt; i &lt;&lt; &#39; &#39;;
    std::cout &lt;&lt; &#39;\n&#39;;
 
    for (int i : il | views::reverse)
        std::cout &lt;&lt; i &lt;&lt; &#39; &#39;;
    std::cout &lt;&lt; &#39;\n&#39;;
 
    &#47;&#47; operator[] is inherited from std::view_interface
    for (auto i{0U}; i != rv.size(); ++i)
        std::cout &lt;&lt; rv[i] &lt;&lt; &#39; &#39;;
    std::cout &lt;&lt; &#39;\n&#39;;
}</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5c/c9/f1b053f2.jpg" width="30px"><span>Family mission</span> 👍（0） 💬（1）<div>作者你好，感觉ranges作用以及功能性都不错，请教个问题
template &lt;class Element, size_t Size&gt;
class ArrayView : public std::ranges::view_interface&lt;ArrayView&lt;Element, Size&gt;&gt; {
中class ArrayView 继承std::ranges::view_interface&lt;ArrayView&lt;Element, Size&gt;&gt;不太理解的点是继承模板类不都是类名&lt;模板类型&gt;这种么，这个写法是两个尖括号是啥意思</div>2023-12-13</li><br/><li><img src="" width="30px"><span>常振华</span> 👍（0） 💬（1）<div>函数式编程的可读性真是差，非常差，C++发展越来越倒退了</div>2023-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/34/7f/6c99fc74.jpg" width="30px"><span>大熊猫有宝贝</span> 👍（0） 💬（1）<div>工厂和工具函数之间的关系该怎么理解呢？</div>2023-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3c/15/0c2db845.jpg" width="30px"><span>📷全程不笑🏀</span> 👍（0） 💬（1）<div>老师好，请教个问题，我的环境是ubuntu20.04， gcc版本11.1.0。
工厂小节中的示例代码编译报错了， istream_view与istream相关。
第25行的视图初始化应该为小括号吧，大括号{}我这边编译报错。另外28行的views::istream也编译报错，替换成ranges::istream_view运行正常，不知道是不是我环境的问题？</div>2023-02-10</li><br/>
</ul>