你好，我是卢誉声。

C++20为我们带来了重要的文本格式化标准库支持。通过Formatting库和formatter类型，我们可以实现高度灵活的文本格式化方案。那么，**我们该如何在实际工程项目中使用它呢？**

日志输出在实际工程项目中是一个常见需求，无论是运行过程记录，还是错误记录与异常跟踪，都需要用到日志。

在这一讲中，我们会基于新标准实现一个日志库。你可以重点关注特化formatter类型的方法，实现高度灵活的标准化定制。

好，话不多说，我们就从架构设计开始，一步步实现这个日志库（课程配套代码可以从[这里](https://github.com/samblg/cpp20-plus-indepth)获取）。

## 日志库架构设计

事实上，实现一个足够灵活的日志库并不容易。在实际工程项目中，日志输出不仅需要支持自定义日志的输出格式，还需要支持不同的输出目标。比如，输出到控制台、文件，甚至是网络流或者数据库等。

Python和Java这类现代语言都有成熟的日志库与标准接口。C++ Formatting的正式提出，让我们能使用简洁的方式实现日志库。

同时，Python的logging模块设计比较优雅。因此，我们参照它的架构，设计了基于C++20的日志架构。

![](https://static001.geekbang.org/resource/image/ec/0c/ec3a90b1d84e98d8b5a50ca5e752370c.jpg?wh=2698x749)

项目的模块图是后面这样。

![](https://static001.geekbang.org/resource/image/03/2d/03d1f3c199a25521cfd8258dd62e7c2d.jpg?wh=1637x1334)  
对照图片可以看到，logging模块是工程的核心，包含核心框架、handlers和formatters三个子模块。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/30/db/86/51ec4c41.jpg" width="30px"><span>李云龙</span> 👍（1） 💬（3）<div>不仅学到了format，还在老师的项目代码中学到了不同风格的时间处理</div>2024-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/be/e8/878aa74f.jpg" width="30px"><span>三笑三引伏兵</span> 👍（0） 💬（2）<div>我想问下为什么BaseHandler不声明一个emit的纯虚函数呢 因为开销吗</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>StreamHandler的“流”是否包含File？甚至包含标准输出流？
我目前的理解是：标准输出流就是控制台；“流”一般包括文件输出流、网络输出流，好像没有别的了。</div>2023-02-25</li><br/>
</ul>