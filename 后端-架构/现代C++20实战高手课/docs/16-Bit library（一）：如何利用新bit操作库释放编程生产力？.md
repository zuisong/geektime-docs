你好，我是卢誉声。

我们都知道，C++继承了C语言所有的底层操作能力，其中最重要的两个特性就是指针和位操作。对于指针，现代C++标准已经通过智能指针提出了较好的解决方案。

但是在C++20之前，C++的位操作支持还是很“基础”的。它缺乏安全性，而且不够灵活。因此，我们就围绕C++20对位操作能力的扩展这个话题，讨论一下全新的Bit library。

好，话不多说，就让我们从基本的C++位操作开始讲起（课程配套代码可以从[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

## C++位操作技术与不足

C++提供的基础位操作技术与C语言一脉相承，主要通过位操作符对整数进行位操作。我对这些基本操作做了一个总结，你可以参考后面的表格回顾一下。

![](https://static001.geekbang.org/resource/image/c9/50/c9d77bda455c87a90ce43e14e77af950.jpg?wh=2543x1437)

相比C语言，C++一直为C的底层能力提供一些高层次的安全化包装，比如为了解决裸指针的各种安全缺陷，提出了各类智能指针。

基于这种思路，C++也通过标准库提供了bitset，对二进制位串进行包装，可以在整数和bitset以及其字符串表示之间进行转换，并支持表格中的几个基础的位操作符。  
但在C++20之前，C++的位操作支持还是很“基础”的，我们重点讨论几个比较明显的问题。

**首先，没有提供字节序的检测和转换能力**。基于位进行二进制数据解析的时候，最大的问题就是不同CPU的大小端设计（比如 x86 体系结构是小端字节序，arm 支持采用大小端字节序任选其一）。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>分享一下我的思考题答案：
constexpr size_t MyBitWidth(uint64_t value){
    auto valueCeil = std::bit_ceil(value);
    size_t i = 0;
    for (; valueCeil &gt;&gt; i; ++i);

    return i - 1;
}

constexpr auto MyBitFloor(uint64_t value) {
    return std::bit_ceil(value) &gt;&gt; 1;
}</div>2024-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：浮点数位操作的转换是隐式转换吗？
C++20之前的浮点数位操作，需要先转换为整数，这个转换是隐式转换吗？还是需要写代码实现？（好久不用C++，有点忘记了）
Q2：移位怎么区分算术移位和逻辑移位？
文中提到，C++20之前的移位操作，移位的具体含义交给了具体实现。那么，具体怎么区分是算术移位还是逻辑移位？
Q3：C++20支持序列化和反序列化吗？
文中提到“这些新工具为我们实现位操作提供了更加完备的支持。同时，也为实现序列化和反序列化提供了标准化支持”，那么，C++20已经支持序列化和反序列化了吗？ （C++20之前的版本支持吗？）</div>2023-02-28</li><br/>
</ul>