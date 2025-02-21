你好，我是卢誉声。

在上一讲中，我们已经通过一些简单的编程示例，展示了C++20及其后续演进提供的位操作库的基本使用方法。

但是，简单的示例还无法体现位操作库的真正威力。所以，这一讲我会通过一个较为完整的工程代码，带你体会如何充分利用全新的位操作库，实现强大的序列化和反序列化功能以及位运算。

好，话不多说，就让我们开始吧（课程配套代码可以从[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

## 扩展数据流处理实战案例

在实际生产环境中，我们经常需要通过网络传输特定的数据，但是不同语言和不同平台的内存模型可能完全不同。这时，发送方需要将数据转换为符合特定标准的数据流，接收方将数据解析后转换为内部变量。

我们将变量转换为数据流的操作称为“序列化（Serialization）”，将数据流转换成变量的过程称为“反序列化（Deserialization）”。

![](https://static001.geekbang.org/resource/image/20/cb/20bafd91c9182fe98299a4a5300d61cb.jpg?wh=2559x695)

我们曾在[第13讲](https://time.geekbang.org/column/article/627936)——Ranges实战：数据序列函数式编程中，实现了一个获取三维模型数据并进行统计的程序。

今天，我们将继续对其进一步扩展，使用位操作库实现序列化和反序列化。

不知道你是否还记得，我在第13讲偷了一个懒，直接使用了硬编码的代码作为数据输入。我们会在这一讲改进一下，将本地的二进制文件读取到内存里，将其转换成内部变量。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（1）<div>分享一下我的思考题答案：
inline constexpr uint8_t ComputeByteOrder2() {
    constexpr int16_t num = 0x0102;
    constexpr std::bitset&lt;16&gt; bs(num);

    if constexpr(bs[7] == 0b1) {
        return 1;
    }
    else {
        return 0;
    }
}

enum class endian
{
    little,
    big,
    native = ComputeByteOrder2()
};</div>2024-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请问：C++20的位操作比以前版本的性能有多少提升？</div>2023-03-02</li><br/>
</ul>