你好，我是Mike，今天我们来了解一下Rust中的生命周期到底是什么。

你可能在互联网上的各种资料里早就见到过这个概念了，生命周期可以说是Rust语言里最难理解的概念之一，也是导致几乎所有人都觉得Rust很难，甚至很丑的原因。其实对于初学者来说，至少在开始的时候，它并不是必须掌握的，网上大量的资料并没有指明这一点，更加没有考虑到的是应该如何让初学者更加无痛地接受生命周期这个概念，而这也是我们这门课程尝试解决的问题。

下面让我们从一个示例说起，看看为什么生命周期的概念在Rust中是必要的。

## 从URL解析说起

URL协议类似下面这个样子，可以粗略地将一个URL分割成5部分，分别是 protocol、host、path、query、fragment。

![](https://static001.geekbang.org/resource/image/af/yy/af56c3bbec82d825d566c43af83048yy.jpg?wh=1755x436)

现在我们拿到一个URL字符串，比如就是图片里的这个。

```plain
let s = "https://rustcc.cn/article?id=019f9937#title".to_string();
```

现在要把它解析成Rust的结构体类型，按照我们已掌握的知识，先定义URL结构体模型，定义如下：

```plain
struct Url {
    protocol: String,
    host: String,
    path: String,
    query: String,
    fragment: String,
}
```
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/8a/7c1baa25.jpg" width="30px"><span>buoge</span> 👍（5） 💬（1）<div>下周可以实战了，好开心😁</div>2023-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/36/33/3411df0d.jpg" width="30px"><span>seven9t</span> 👍（3） 💬（1）<div>&quot;但对计算机来讲，每一条指令的执行，是要花相对确定的时间长度的，所以就在要执行的 CPU 指令条数和执行时间段上产生了正比映射关系。这就让我们在代码的编译期间去分析运行期间变量的生存时间区间变成可能。这就是 Rust 能够做生命周期分析的原因。&quot;  静态分析和指令执行时间应该没关系，建议调整</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（3） 💬（1）<div>Rust 牵涉面过于广泛，学习语言不是为了炫技，应该以实用为主，学以致用，边学边用。Rust 没有天花板，感觉学无止境，学习任何一项知识都是学以致用</div>2023-12-04</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyhbzdkFM64Npva5ZKf4IPwhy6rDAX0L77QNESbalnXhnGKibcTbwtSaNC0hO6z0icO8DYI9Nf4xwg/132" width="30px"><span>eriklee</span> 👍（2） 💬（1）<div>rust编译器也在不断进化，实际上2021版就比2018版少了很多需要生命周期标注的场景，我相信随着rust编译器的进化，以后可能只有1%的场景需要用到生命周期标注</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/1a/269eb3d6.jpg" width="30px"><span>cfanbo</span> 👍（1） 💬（1）<div>在 “函数返回值中的引用” 这个示例中，是不是可以理解为 返回的值是s1, 但它的生命周期却是s2的生命周期，因此导致最后打印语句执行前, 由于 s2 生命周期原因被drop，而导致编译出错？</div>2023-12-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（1） 💬（1）<div>对于编译器来说，看到&lt;&gt;就是要干活的。&lt;&#39;a&gt;可以理解为一种特殊的类型参数，编译器看到&lt;&gt;里的&#39;a并不会对类型做展开，而是去检查并计算引用的生命周期。</div>2023-12-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（1） 💬（1）<div>还没到实战就已经63%的进度了😭实战内容不会很少吧。希望能够有怎么debug的教学。</div>2023-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（0） 💬（1）<div>struct A {
    foo: String,
}

impl A {
    fn play&lt;&#39;a&gt;(&amp;&#39;a self, a: &amp;&#39;a str, b: &amp;str) -&gt; &amp;str {
        a
    }
}
返回a的时候只需要标注a参数，而返回b的时候只需要标准b参数，这里进一步说明了类型标注只关注传入传出</div>2023-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>【函数返回值中的引用】一个函数中返回一个类型的引用的第一种可能的情况（返回对外部全局变量的引用）示例的 foo() 函数的返回值类型应该也需要一个生命周期参数标注：
static ASTRING: &amp;&#39;static str = &quot;abc&quot;;
fn foo() -&gt; &amp;&#39;static str {    &#47;&#47; 默认的全局 &#39;static
    ASTRING
}
或：
static ASTRING: &amp;&#39;static str = &quot;abc&quot;;
fn foo&lt;&#39;a&gt;() -&gt; &amp;&#39;a str {    &#47;&#47; 自定义的 &#39;a
    ASTRING
}</div>2024-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（0）<div>Rust 牵涉面过于广泛，学习语言不是为了炫技，应该以实用为主，学以致用，边学边用。Rust 没有天花板</div>2023-12-04</li><br/>
</ul>