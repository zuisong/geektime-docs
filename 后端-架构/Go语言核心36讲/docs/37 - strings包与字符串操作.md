在上一篇文章中，我介绍了Go语言与Unicode编码规范、UTF-8编码格式的渊源及运用。

Go语言不但拥有可以独立代表Unicode字符的类型`rune`，而且还有可以对字符串值进行Unicode字符拆分的`for`语句。

除此之外，标准库中的`unicode`包及其子包还提供了很多的函数和数据类型，可以帮助我们解析各种内容中的Unicode字符。

这些程序实体都很好用，也都很简单明了，而且有效地隐藏了Unicode编码规范中的一些复杂的细节。我就不在这里对它们进行专门的讲解了。

我们今天主要来说一说标准库中的`strings`代码包。这个代码包也用到了不少`unicode`包和`unicode/utf8`包中的程序实体。

- 比如，`strings.Builder`类型的`WriteRune`方法。
- 又比如，`strings.Reader`类型的`ReadRune`方法，等等。

下面这个问题就是针对`strings.Builder`类型的。**我们今天的问题是：与`string`值相比，`strings.Builder`类型的值有哪些优势？**

这里的**典型回答**是这样的。

`strings.Builder`类型的值（以下简称`Builder`值）的优势有下面的三种：

- 已存在的内容不可变，但可以拼接更多的内容；
- 减少了内存分配和内容拷贝的次数；
- 可将内容重置，可重用值。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（38） 💬（1）<div>1 string拼接的结果是生成新的string，需要把原字符串拷贝到新的string中；Builder底层有个[]byte,按需扩容，不必每次拼接都需要拷贝；

2 Reader的优势是维护一个已读计数器，知道下一次读的位置，读得更快.</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/f3/8b9df836.jpg" width="30px"><span>jimmy</span> 👍（15） 💬（1）<div>strings.Builder里边的String方法是
&#47;&#47; String returns the accumulated string.
func (b *Builder) String() string {
	return *(*string)(unsafe.Pointer(&amp;b.buf))
}
这样实现的， 请问老师为什么不是
&#47;&#47; String returns the accumulated string.
func (b *Builder) String() string {
	return string(b.buf)
}
有什么特殊的点吗？ 谢谢</div>2019-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/b8/77/0e1f2b4b.jpg" width="30px"><span>Garry</span> 👍（6） 💬（2）<div>老师，我在看strings 源码的时候发现了
func noescape(p unsafe.Pointer) unsafe.Pointer {
	x := uintptr(p)
	return unsafe.Pointer(x ^ 0)
}
这个函数 最后用了个x ^ 0,但是这么操作的最后结果不还是x么，为何还要这样操作呢</div>2019-04-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（5） 💬（1）<div>看到源码有处不理解如下：
func noescape(p unsafe.Pointer) unsafe.Pointer {
x := uintptr(p)
return unsafe.Pointer(x ^ 0)
}
这个方法的意思避免逃逸分析，不太理解请指教？
第一：为什么经过这么转换会避免逃逸？
第二：避免逃逸有什么好处，既然会逃逸肯定会到heap上，如果避免逃逸那这个变量怎么使用呢，或者说是这样再stack上又分配了一个新的变量么？</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（4） 💬（2）<div>strings.Reader这里我一直有个疑问， 它读写  很对地方都是
if r.i &gt;= int64(len(r.s)) {
		return 0, nil
}
为什么在  strings.NewReader 的时候 不直接求出 len(r.s)的长度，而是每次去算长度，这样不会有性能浪费吗？</div>2020-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GBU53SA3W8GNRAwZIicc3gTEc0nSvfPJw7iboAMicjicmP6egDcibib28DkUfTYOjMd31DIznmofdRZrpIXvmXvjV1PQ/132" width="30px"><span>博博</span> 👍（2） 💬（2）<div>Builder类型中的addr *Builder 字段的意义是什么呢？</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/77/22843055.jpg" width="30px"><span>kingkang</span> 👍（2） 💬（1）<div>请问byte数组转string出现乱码怎么处理？</div>2019-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>郝林老师，麻烦看看以下问题：

1. &quot;不过，由于string值的不可变，其中的指针值也为内存空间的节省做出了贡献&quot;。 这句话该怎么理解呢？

2. 文中的这段代码：

f2 := func(bp *strings.Builder) { 

(*bp).Grow(1)  &#47;&#47; 这里虽然不会引发panic，但不是并发安全的。 
builder4 := *bp
 &#47;&#47;builder4.Grow(1) &#47;&#47; 这里会引发panic。
 _ = builder4
 
}

f2(&amp;builder1)

不是说：“虽然已使用的Builder值不能再被复制，但是它的指针值却可以。”

那这段代码：builder4.Grow(1) 。 为何还会引发panic呢？ </div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>郝林老师，能分析以下这段代码的执行步骤吗？没怎么看懂：

*(*string)(unsafe.Pointer(&amp;b.buf))  </div>2021-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（20） 💬（0）<div>二刷了一遍，又看了一遍源码；我觉得对于Builder和Reader理解应该注意：
1，结构：
    1.1 Builder结构体内部内容容器是一个切片buf还有一个addr（复制检测用的指针）
    1.2 Reader结构体内部内容容器是一个string的s和一个内部计数器i
2. Builder
    2.1 想法方法内部先调用copyCheck方法进行值复制的检测（即老师说的使用后在复制引发panic就是这个方法）
    2.2 内容容器是切片，相关拼接方法内部应用的是append函数，这些方法使用时间可以结合slice和append的原理
    2.3 公开方法Grow进行是否扩容判断逻辑，然后调用内部方法grow执行切片扩容，扩容策略：原内容容器切片容量 * 2 + Grow参数n；用这个容量make申请新的内存空间，然后copy原内容容器切片底层数组值

3. Reader
   3.1 读取方法底层是对内容容器s字符串的切片操作，这里要注意在多字节字符读取时，字符串的切片操作可能会导致拿到的字符串有乱码的风险，
   3.2 对于Read、ReadAt这些将字符串读取到传入的切片参数时，底层应用的是copy函数，so最终读出的字符串字节切片长度是copy函数两个参数中较小的一个参数的长度。同时Read、ReadAt这些方法的off参数不恰当时，会因为多字节字符串切片导致两头可能出现乱码</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/72/f1/24bc01e3.jpg" width="30px"><span>南方有嘉木</span> 👍（7） 💬（0）<div>请问容量增加n个字节，为什么是原来的2倍再加上n呢</div>2018-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/b5/f59d92f1.jpg" width="30px"><span>Cloud</span> 👍（2） 💬（0）<div>很实用！</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/df/6261264f.jpg" width="30px"><span>微微一怒很倾城</span> 👍（0） 💬（0）<div>对于builder的主要性能优势，我的理解是原始的string拼接，因为每次都要生成新的string，所以每次都要重新分配内存和拷贝，但是builder就不需要，只需要第一次分配，然后后面就不停地拼接和拷贝</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/94/abb7bfe3.jpg" width="30px"><span>Ke</span> 👍（0） 💬（0）<div>strings.Builder使用之后，可以从strings.Builder复制出来新变量，但是这个变量无法在使用WriteString或者Grow之类的操作，只能读取，并且就算原始的strings.Builder变量做了reset，这个新变量的读取也不受影响</div>2020-07-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erNhKGpqicibpQO3tYvl9vwiatvBzn27ut9y5lZ8hPgofPCFC24HX3ko7LW5mNWJficgJncBCGKpGL2jw/132" width="30px"><span>Geek_1ed70f</span> 👍（0） 💬（0）<div>读源代码讲得好深....</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-04</li><br/>
</ul>