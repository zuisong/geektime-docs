你好，我是卢誉声。

在上一讲中，我们了解到C++模板不仅具备强大的泛化能力，自身也是一种“图灵完备”的语言，掀起了C++之父Bjarne Stroustrup自己都没料到的“模板元编程”这一子领域。

但是，使用模板做泛型编程，最大的问题就是缺少良好的接口，一旦使用过程中出现偏差，报错信息我们难以理解，甚至无从下手。更糟的是，使用模板的代码几乎无法做到程序ABI层面兼容。这些问题的根本原因是C++语言本身缺乏模板参数约束能力，因此，既能拥有良好接口、高性能表达泛化，又能融入语言本身是非常困难的。

好在C++20标准及其后续演进中，为我们带来了Concepts核心语言特性变更来解决这一难题。那么它能为我们的编程体验带来多大的革新？能解决多少模板元编程的历史遗留问题？今天我们一起探究Concepts。

课程配套代码，点击[这里](https://github.com/samblg/cpp20-plus-indepth)即可获取。

## 定义Concepts

首先我们看看Concepts是什么，它可不是横空出世的，C++20为模板参数列表添加了一个特性——约束，采用约束表达式对模板参数进行限制。约束表达式可以使用简单的编译期常量表达式，也可以使用C++20引入的requires表达式，并且支持约束的逻辑组合，这是对C++20之前enable\_if和type\_traits的进一步抽象。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（4） 💬（1）<div>请教老师两个问题：
Q1：b不是派生类，为什么不报错？
BaseClass b;    doGetValue(b);  b是BaseClass，不是BaseClass的派生类，为什么不报错？
Q2：原子约束的f1和f2为什么失败？
f1前面加的 requires (S&lt;T&gt;{})表示什么意思？为什么失败？
原子约束有关键字吗？或者说，怎么看出来一个约束是原子约束？
另外，struct S中的constexpr operator什么意思？</div>2023-01-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（1） 💬（2）<div>requiresexport template &lt;typename T1, typename  T2&gt;
    requires requires (T1 x, T2 y) { x + y; }
std::common_type&lt;T1, T2&gt; func(
    T1 arg1, T2 arg2
) {
    return arg1 + arg2;
}

没看明白requires requires (T1 x, T2 y) { x + y; }是啥意思，如果第一个requires是子句的关键字，requires (T1 x, T2 y) { x + y; }是表达式的话，那不是说这里必须是bool型的吗？x+y不一定是bool型的吧？</div>2023-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/6e/757d42a0.jpg" width="30px"><span>lmnsds</span> 👍（0） 💬（1）<div>编译器如何判断约束之间的偏序关系呢？</div>2024-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（0） 💬（1）<div>requires 后边接约束表达式，约束表达式应该怎么理解？</div>2023-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/7c/46/3809b32e.jpg" width="30px"><span>MrDuin</span> 👍（0） 💬（1）<div>C++20的新特性，对yC++语言的心里负担更大了。</div>2023-03-28</li><br/>
</ul>