你好，我是Mike。

恭喜你学完前两章的内容了，基础篇和进阶篇一共有20讲，每一讲的内容都很重要，算是你入门Rust的重要基础，所以一定要多读几遍，争取学透。为了让你学思结合，我们在每节课的最后设计了对应的思考题，这节课我们就来处理这些问题。

我也看到很多同学在课程的后面回答了这些问题，此外还有一些其他的问题，提得也很精彩，所以我挑出一并放在这里，希望能为你解惑，对你有所启发，话不多说，我们马上开始吧！

做完思考题再来看答案会更有收获。

## **基础篇**

### [01｜快速入门：Rust 中有哪些你不得不了解的基础语法？](https://time.geekbang.org/column/article/718865?utm_campaign=geektime_search&utm_content=geektime_search&utm_medium=geektime_search&utm_source=geektime_search&utm_term=geektime_search)

#### 思考题

- Rust 中能否实现类似 JS 中的 number 这种通用的数字类型呢？
- Rust 中能否实现 Python 中那种无限大小的数字类型呢？

#### 答案

在 Rust 中，有多种数字类型，包括有符号和无符号整数、浮点数、复数等。和 JS 中的 number 类型相似，Rust 中的数字类型也支持基本的数学运算，例如加减乘除和取模等。不过，和 JS 的 number 不同，Rust 的数字类型都具有固定的位数，这意味着不同的数字类型有不同的取值范围。

此外，Rust 中的数值类型需要在编译时就确定它们的类型和大小，这些类型可以通过使用 Rust 内置的类型注解，或是灵活的小数点和后缀表示法来声明。而 crates.io 上有 num crate 可以用来表示通用的数字类型，具体是通过trait机制来实现的。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/39/07/93/710c7ee2.jpg" width="30px"><span>不忘初心</span> 👍（2） 💬（1）<div>可以给 i8 类型做 impl 吗？基本数据类型无法实现 impl. 
准确点说, 应该是自身crate之外的都无法直接impl, 但可以impl trait</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a3/dc/9df4f5a0.jpg" width="30px"><span>thanks</span> 👍（1） 💬（1）<div>03｜所有权（下）：Rust 中借用与引用的规则是怎样的？
第一个问题，从现象看是 rust 的规则不允许这么写，但是不允许这么写的原因是为啥</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（1） 💬（1）<div>多刷两遍，期待老师的实战课程，能讲讲tikio么，老师</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/14/83867b58.jpg" width="30px"><span>Distance</span> 👍（0） 💬（2）<div>啊这 按照大纲今天不应该是 axum 嘛，我还以为这周 axum 能更完😂</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3d/4c/90/00336164.jpg" width="30px"><span>知足</span> 👍（0） 💬（0）<div>impl&lt;T: Display + Copy&gt; Point&lt;T&gt; {
    fn print(&amp;self) {
        println!(&quot;x&quot;);
    }
}

impl Point&lt;String&gt; {
    fn print(&amp;self) {
        println!(&quot;NotDisplay: x: {}, y: {}&quot;, self.x, self.y);
    }
}

这样还是不行：
error[E0592]: duplicate definitions with name `print`
  --&gt; src&#47;main.rs:13:5
   |
13 |     fn print(&amp;self) {
   |     ^^^^^^^^^^^^^^^ duplicate definitions for `print`
...
19 |     fn print(&amp;self) {
   |     --------------- other definition for `print`
   |
   = note: upstream crates may add a new impl of trait `std::marker::Copy` for type `std::string::String` in future versions</div>2024-11-01</li><br/>
</ul>