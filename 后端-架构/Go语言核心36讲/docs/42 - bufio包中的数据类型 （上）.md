今天，我们来讲另一个与I/O操作强相关的代码包`bufio`。`bufio`是“buffered I/O”的缩写。顾名思义，这个代码包中的程序实体实现的I/O操作都内置了缓冲区。

`bufio`包中的数据类型主要有：

1. `Reader`；
2. `Scanner`；
3. `Writer`和`ReadWriter`。

与`io`包中的数据类型类似，这些类型的值也都需要在初始化的时候，包装一个或多个简单I/O接口类型的值。（这里的简单I/O接口类型指的就是`io`包中的那些简单接口。）

下面，我们将通过一系列问题对`bufio.Reader`类型和`bufio.Writer`类型进行讨论（以前者为主）。**今天我的问题是：`bufio.Reader`类型值中的缓冲区起着怎样的作用？**

**这道题的典型回答是这样的。**

`bufio.Reader`类型的值（以下简称`Reader`值）内的缓冲区，其实就是一个数据存储中介，它介于底层读取器与读取方法及其调用方之间。所谓的底层读取器，就是在初始化此类值的时候传入的`io.Reader`类型的参数值。

`Reader`值的读取方法一般都会先从其所属值的缓冲区中读取数据。同时，在必要的时候，它们还会预先从底层读取器那里读出一部分数据，并暂存于缓冲区之中以备后用。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/60/47/fa06038b.jpg" width="30px"><span>人生入戏须尽欢</span> 👍（22） 💬（3）<div>bufio和bytes.buffer有什么区别吗</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b1/20/8718252f.jpg" width="30px"><span>鲲鹏飞九万里</span> 👍（1） 💬（2）<div>赫老师，您好。这段话，您写得是不是有问题，我读了好几遍也不能理解。能否详细讲解下：
“第二个事实，在压缩缓冲区之后，已写计数之后的字节只可能是已被读取过的字节，或者是已被拷贝到缓冲区头部的未读字节，又或者是代表未曾被填入数据的零值0x00。所以，后续的新字节是可以被写到这些位置上的。”</div>2023-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>郝林老师你好。

请问一下，demo84.go中：示例4和示例5中，为什么调用Peek方法最后返回的字节切片的长度都为213呀。我想的是示例5中应该返回300才对的呀。</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/4b/0ddfa9ad.jpg" width="30px"><span>小刚z</span> 👍（0） 💬（1）<div>bufio有并发都写的问题吗 看起来好像没有</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/7a/ac307bfc.jpg" width="30px"><span>到不了的塔</span> 👍（13） 💬（0）<div>bufio的应用场景应该是为了加快io速度，尤其是对比较零碎的数据（小数据）的io加速更明显。
</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/b5/f59d92f1.jpg" width="30px"><span>Cloud</span> 👍（7） 💬（1）<div>老师，什么场景适合使用bufio，能否举几个栗子呀</div>2018-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（3） 💬（0）<div>对照源码看专栏，好理解好记忆。👍</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/d2/c483b836.jpg" width="30px"><span>Wiwen</span> 👍（0） 💬（0）<div>如果Write方法发现需要写入的字节太多，同时缓冲区已空，直接写到底层写入器。
这个写入字节应该是新要写入的字节大小超过了缓存区的大小(默认值是4096)时，才直接写到底层写入器。</div>2019-02-17</li><br/>
</ul>