你好，我是Mike。今天我们一起来学习Rust中类型相关的知识。

这块儿知识在其他大部分语言入门材料中讲得不多，但是对于Rust而言，却是非常重要而有趣的。我们都知道，计算机硬件执行的代码其实是二进制序列。而**对一个二进制值来说，正是类型赋予了它意义**。

比如 01100001 这个二进制数字，同样的内存表示，如果是整数，就表示97。如果是字符，就表示 `'a'` 这个 char。如果没有类型去赋予它额外的信息，当你看到这串二进制编码时，是不知道它代表什么的。

## 类型

《Programming.with.Types》2019 这本书里对类型做了一个定义，翻译出来是这样的：类型是对数据的分类，这个分类定义了这些数据的意义、被允许的值的集合，还有能在这些数据上执行哪些操作。编译器或运行时会检查类型化过程，以确保数据的完整性，对数据施加访问限制，以及把数据按程序员的意图进行解释。

有些情况下，我们会简化讨论，把操作部分忽略掉，所以我们可以简单地**把类型看作集合，这个集合表达了这个类型的实例能取到的所有可能的值**。

### 类型系统

这本书里还定义了类型系统的概念。

书里是这样说的：类型系统是一套规则集——把类型赋予和施加到编程语言的元素上。这些元素可以是变量、函数和其他高阶结构。类型系统通过你在代码中提供的标注来给元素赋予类型，或者根据它的上下文隐式地推导某个元素的类型。类型系统允许在类型间做各种转换，同时禁止其他的一些转换。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/51/ea/d9a83bb3.jpg" width="30px"><span>古明地觉</span> 👍（9） 💬（2）<div>思考题：&quot;为泛型实现了一个方法，能否再为具化类型实现一个同名方法&quot;，取决于这个泛型能否表示相应的具化类型。比如为泛型 T 和 String 实现了相同的方法，由于 T 没有施加任何约束，它可以代表 String。那么当调用方法时，对于具化类型 String 来说，要调用哪一个呢？因此会出现歧义，编译器会报错：方法被重复定义了。

但如果给泛型 T 施加了一个 Copy 约束，要求 T 必须实现了 Copy trait，那么就不会报错了，因为此时 T 代表不了 String，所以调用方法不会出现歧义。但如果再为 i32 实现一个同名方法就会报错了，因为 i32 实现了 Copy，它可以被 T 表示。

PS：老师我在 06 讲提了一个问题，之前在学 Rust 的时候就一直困扰着我，还麻烦老师解答一下。</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ff/d8/d48d6088.jpg" width="30px"><span>一个人旅行</span> 👍（5） 💬（1）<div>不能，编译器会提示duplicate definitions for XXXXX。
如果想为具化类型再实现同样的方法，则可以定义一个trait，用具化类型实现这个trait，来达到&quot;为具化类型再实现同样的方法“的目的。</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（3） 💬（1）<div>思考题：核心点就在于不能为同一个类型实现 2 个相同函数签名的方法，因为这会引起方法冲突。

编译报错如下：

error[E0592]: duplicate definitions with name `print`
  --&gt; examples&#47;generic.rs:7:5
   |
7  |     fn print(&amp;self) {
   |     ^^^^^^^^^^^^^^^ duplicate definitions for `print`
...
13 |     fn print(&amp;self) {
   |     --------------- other definition for `print`


所以一般情况下，如果 impl&lt;T&gt; 后面的 T 没有任何的约束，那么就表示为所有类型的 T 都实现了方法，比如说 print()，这个时候是不能为具化类型再次实现 print() 的，因为这个时候就产生了方法冲突。

但是，如果 impl&lt;T: std::fmt:Display&gt; 后面的 T 是有约束的，那么其实只为符合这个约束的类型实现了 print()，其余类型是没有实现的，所以是可以为其余具化类型实现相同的方法的。

如：

```rust
struct Point&lt;T&gt; {
    x: T,
    y: T,
}

struct NotDisplay {
    a: u32,
}

impl&lt;T: std::fmt::Display&gt; Point&lt;T&gt; {
    fn print(&amp;self) {
        println!(&quot;Point: {}, {}&quot;, self.x, self.y);
    }
}

impl Point&lt;NotDisplay&gt; {
    fn print(&amp;self) {
        println!(&quot;not display&quot;);
    }
}
```</div>2023-11-08</li><br/><li><img src="" width="30px"><span>Geek_de05b4</span> 👍（2） 💬（1）<div>impl&lt;T: std::ops::Add&lt;Output = T&gt;&gt; Bar&lt;T&gt; {
    fn plus(self, other: Bar&lt;T&gt;) -&gt; T {
        self.value + other.value
    }
}

impl Bar&lt;u32&gt; {
    fn plus(&amp;self, other: &amp;Bar&lt;u32&gt;) -&gt; u32 {
        self.value + other.value
    }
}

&#47;&#47;Output:
error[E0592]: duplicate definitions with name `plus`
  --&gt; src&#47;main.rs:64:5
   |
64 |     fn plus(self, other: Bar&lt;T&gt;) -&gt; T {
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ duplicate definitions for `plus`
...
70 |     fn plus(&amp;self, other: &amp;Bar&lt;u32&gt;) -&gt; u32 {
   |     --------------------------------------- other definition for `plus`

不能</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（0） 💬（1）<div>思考题：通常是不能， 但是可以通过 trait 进行特化</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（1） 💬（0）<div>和Java的范型类似</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/31/a2/16c3318d.jpg" width="30px"><span>坤</span> 👍（0） 💬（0）<div>let a = 9 + &#39;1&#39; as u8;
结果是 58,让我困惑了:9+1 结果明明是10,这怎么就58了.
然后就想:为什么是58而不是其他的值,特征是这个数字小于100,
那么&#39;1&#39; 就是 58-9=49,有了一个猜想&#39;1&#39; as u8 是指ascii码的1,转之后是49, 
然后就去验证,查看ascii,果然&#39;1&#39;是49.
</div>2024-11-22</li><br/>
</ul>