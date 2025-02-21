你好，我是陈天。今天来学集合容器。

现在我们接触到了越来越多的数据结构，我把 Rust 中主要的数据结构从原生类型、容器类型和系统相关类型几个维度整理一下，你可以数数自己掌握了哪些。  
![](https://static001.geekbang.org/resource/image/d9/4c/d9c1d7ce878b5ef17eb1c8c69e17404c.jpg?wh=2364x1718)  
可以看到，容器占据了数据结构的半壁江山。

提到容器，很可能你首先会想到的就是数组、列表这些可以遍历的容器，但其实**只要把某种特定的数据封装在某个数据结构中**，这个数据结构就是一个容器。比如 Option&lt;T&gt;，它是一个包裹了 T 存在或不存在的容器，而Cow 是一个封装了内部数据 B 或被借用或拥有所有权的容器。

对于容器的两小类，到目前为止，像 Cow 这样，为特定目的而产生的容器我们已经介绍了不少，包括 Box、Rc、Arc、RefCell、还没讲到的 Option 和 Result 等。

今天我们来详细讲讲另一类，集合容器。

## 集合容器

集合容器，顾名思义，就是把一系列拥有相同类型的数据放在一起，统一处理，比如：

- 我们熟悉的字符串 String、数组 \[T; n]、列表 Vec&lt;T&gt;和哈希表 HashMap&lt;K, V&gt;等；
- 虽然到处在使用，但还并不熟悉的切片 slice；
- 在其他语言中使用过，但在 Rust 中还没有用过的循环缓冲区 VecDeque&lt;T&gt;、双向列表 LinkedList&lt;T&gt; 等。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（24） 💬（1）<div>问老师一个工程性上的问题，也困扰了我好久，之前我在用rust开发项目的时候，数据解析性项目，会存在一个字段被多个类，或者函数使用，由于所有权的问题，导致代码中出现了大量的clone函数，后面在做性能分析的时候，发现20%的时间竟然浪费在clone上，求问老师，如何减少clone的调用次数？</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（12） 💬（4）<div>1. 不可以，但稍微改造下也是可以的

str 实现了 AsRef&lt;[u8]&gt;，AsRef&lt;OsStr&gt;，AsRef&lt;Path&gt;，AsRef&lt;str&gt;

如果 T: AsRef&lt;[U]&gt;，编译器可以推断出 str 是 AsRef&lt;[u8]&gt;，即 U 是 u8 类型

如果 T: AsRef&lt;U&gt;，编译器就懵逼了，因为它有四种选择。

问题的关键就在于编译器无法推断出 U 的类型，因此如果稍微改造下，其实还是可以通过手动标记来通过编译的：

```rust
use std::fmt;

fn main() {
    let s = String::from(&quot;hello&quot;);
    print_slice1::&lt;_, [u8]&gt;(&amp;s); &#47;&#47; [104, 101, 108, 108, 111]
    print_slice1::&lt;_, str&gt;(&amp;s);  &#47;&#47; &quot;hello&quot;
}

fn print_slice1&lt;T, U: ?Sized&gt;(s: T)
where
    T: AsRef&lt;U&gt;,
    U: fmt::Debug,
{
    println!(&quot;{:?}&quot;, s.as_ref());
}
```

2. 看了下 rxjs 的定义，第二个参数如果小于第一个参数的话，得到的结果好像没啥意义（反正我个人是没看懂），
所以只处理了第二个参数不小于第一个参数的情况。

```rust
struct WindowCountIter&lt;T: Iterator&gt; {
    iter: T,
    window_size: usize,
    start_window_every: usize,
}

impl&lt;T: Iterator&gt; Iterator for WindowCountIter&lt;T&gt; {
    type Item = Vec&lt;&lt;T as Iterator&gt;::Item&gt;;

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        let mut item = Vec::with_capacity(self.window_size);

        for _ in 0..self.window_size {
            if let Some(v) = self.iter.next() {
                item.push(v);
            }
        }

        for _ in 0..(self.start_window_every - self.window_size) {
            self.iter.next();
        }

        if item.is_empty() {
            None
        } else {
            Some(item)
        }
    }
}

trait IteratorExt: Iterator {
    fn window_count(self, window_size: usize, start_window_every: usize) -&gt; WindowCountIter&lt;Self&gt;
    where
        Self: Sized,
    {
        if start_window_every &gt; 0 &amp;&amp; start_window_every &lt; window_size {
            panic!(&quot;start_window_every 不能小于 window_size&quot;)
        }
        WindowCountIter {
            iter: self,
            window_size,
            start_window_every: if start_window_every == 0 {
                window_size
            } else {
                start_window_every
            },
        }
    }
}

impl&lt;T: Iterator&gt; IteratorExt for T {}
```</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（5） 💬（3）<div>老师问个问题，为什么rust解引用是用&amp;T 来表示，而不是用*T</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（4） 💬（1）<div>怎么留言越来越少了……
不要放弃啊，我也有被卡好几天的时候，但慢慢地就走出来了。
1. 编译器推断不出 U 的类型，因为 T 实现了多个 AsRef trait。可以使用 turbofish 手动指定 U，同时也要注意到对于 str 和 [u8] 来说，U 需要是 ?Sized。
2. 一开始我以为 WindowCount 结构体 next 方法返回的是一个新的 Iterator，这个新的 Iterator 里是 count 个 Item。后来我发现这不可能实现啊……我为什么一开始是这么想的呢，是受 slice 的 chunks 方法影响，chunks 方法这不是正好符合题目要求么，但 slice 是有长度信息的，而 Iterator 只能一直 next。后来我偷瞄了老师的实现，发现原来是想用 Vec 来承载每一组数据…… 具体实现代码就不贴了，和老师的差不多。

但我又回过头来想 rxjs 的 windowCount 好像不是这个意思，它的每一组数据还是一个流。那它怎么实现的呢？
我想这可能跟 rxjs 的设计有关，它是把数据 push 到订阅者，而 Iterator 是 pull。
rxjs 单独使用 windowCount 是这样的效果：假如数据源是点击事件，count 是 3，一开始还没点击就产生一个 Observable（我们叫它 A），然后我点击第一下，这次点击就被推送到 A 了，点击第二下，也推送到 A，点击第三下，也推送到 A，这时候 A 已经吐 3 个数据了，紧接着就会产生下一个高阶 Observable B，用来承载接下来的三次点击……
但这个 Iterator 是个同步模型，而且还没有数据总量的信息，我根本无法判断这次 next 是应该返回 None 还是 Some。

建议类似题目可以给出多一点的提示……
</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（3） 💬（3）<div>还有个问题, 为啥需要 import FromIterator 才能使用 String::from_iter呢? String不都已经impl了吗? https:&#47;&#47;doc.rust-lang.org&#47;src&#47;alloc&#47;string.rs.html#1866-1872</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（3） 💬（2）<div>1. 有歧义, U可以是str, 也可以是[u8];

2. 用vec作弊了: eagerly load window_size大小的element; 没有lazy load

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=e6759f0d43bfbbb9f9a4b4aaf4a8ed8b

没有贴tests; 在link里面有

```
struct WindowCount&lt;T&gt;
where
    T: Iterator,
{
    window_size: usize,
    start_window_every: usize,
    iter: T,
}

impl&lt;T&gt; Iterator for WindowCount&lt;T&gt;
where
    T: Iterator,
{
    type Item = &lt;Vec&lt;&lt;T as Iterator&gt;::Item&gt; as IntoIterator&gt;::IntoIter;
    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if self.window_size == 0 {
            return None;
        }

        let mut v = Vec::with_capacity(self.window_size);
        for _ in 0..self.window_size {
            if let Some(item) = self.iter.next() {
                v.push(item);
            } else {
                break;
            }
        }

        &#47;&#47; advance steps
        for _ in 0..self.start_window_every {
            if self.iter.next().is_none() {
                break;
            }
        }
        if v.is_empty() {
            None
        } else {
            Some(v.into_iter())
        }
    }
}
trait IteratorExt: Iterator {
    fn window_count(self, window_size: usize, start_window_every: usize) -&gt; WindowCount&lt;Self&gt;
    where
        Self::Item: std::fmt::Debug,
        Self: Sized,
    {
        WindowCount {
            window_size,
            start_window_every,
            iter: self,
        }
    }
}

impl&lt;T: Iterator&gt; IteratorExt for T {}
```</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/c1/7f596aba.jpg" width="30px"><span>给我点阳光就灿烂</span> 👍（1） 💬（1）<div>写了一个缓存库，想问一下老师如何优化hashmap的性能，目前为了算法上的O1，使用了box和raw指针，但是会box和rebox又让性能慢了一些。https:&#47;&#47;github.com&#47;al8n&#47;caches-rs</div>2021-09-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJlLmHNjThjiahjUNav9W5PI1IQCic5PcbM700V9YlAWDibjeeOOlAKGvAv4zU7ic0OQJZ0KKZicvbEKPw/132" width="30px"><span>朱中喜</span> 👍（0） 💬（2）<div> let b1 = v1.into_boxed_slice();
    let mut b2 = b1.clone();
    let v2 = b1.into_vec();
    println!(&quot;cap should be exactly 5: {}&quot;, v2.capacity());
    assert!(b2.deref() == v2);

b2的类型是Box([T]), 为何对b2做deref就变成Vec了？在标准库里没找到针对Box slice的Deref实现😭</div>2021-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（0） 💬（2）<div>1. 可以为同一个具体类型实现不同的AsRef Trait, 编译器无法从上下文中推断出U的具体类型，所以不能这样写。

2. 不知道实现的符不符合要求，以及有什么问题。
pub struct Window&lt;I&gt; {
    iter: I,
    count: usize,
    start: usize,
}

pub trait IteratorExt: Iterator {
    fn window_count(self, count: usize, start: usize) -&gt; Window&lt;Self&gt;
    where
        Self: Sized,
    {
        Window {
            iter: self,
            count,
            start,
        }
    }
}

impl&lt;T: Iterator&gt; IteratorExt for T {}

impl&lt;I: Iterator&gt; Iterator for Window&lt;I&gt; {
    type Item = Vec&lt;&lt;I as Iterator&gt;::Item&gt;;

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if self.count == 0 {
            return None;
        }

        for _ in 0..self.start {
            self.iter.next()?;
        }

        let mut v = Vec::with_capacity(self.count);

        for _ in 0..self.count {
            v.push(self.iter.next()?);
        }
        Some(v)
    }
}

#[test]
fn if_it_works() {
    let v1 = vec![&#39;a&#39;, &#39;b&#39;, &#39;c&#39;, &#39;d&#39;, &#39;e&#39;, &#39;f&#39;, &#39;g&#39;, &#39;h&#39;, &#39;i&#39;];

    let mut window = v1.iter().window_count(0, 0);
    assert_eq!(window.next(), None);

    let mut window = v1.into_iter().window_count(3, 0);
    assert_eq!(window.next(), Some(vec![&#39;a&#39;, &#39;b&#39;, &#39;c&#39;]));
    assert_eq!(window.next(), Some(vec![&#39;d&#39;, &#39;e&#39;, &#39;f&#39;]));
    assert_eq!(window.next(), Some(vec![&#39;g&#39;, &#39;h&#39;, &#39;i&#39;]));
    assert_eq!(window.next(), None);

    let v2 = vec![&#39;a&#39;, &#39;b&#39;, &#39;c&#39;, &#39;d&#39;, &#39;e&#39;, &#39;f&#39;, &#39;g&#39;, &#39;h&#39;];
    let mut window = v2.into_iter().window_count(3, 0);
    assert_eq!(window.next(), Some(vec![&#39;a&#39;, &#39;b&#39;, &#39;c&#39;]));
    assert_eq!(window.next(), Some(vec![&#39;d&#39;, &#39;e&#39;, &#39;f&#39;]));
    assert_eq!(window.next(), None);

    let v3 = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let mut window = v3.into_iter().window_count(3, 3);
    assert_eq!(window.next(), Some(vec![4, 5, 6]));
    assert_eq!(window.next(), None);

    let v4 = [1, 2, 3, 4, 5, 6, 7, 8];
    let mut window = v4.iter().window_count(3, 100);
    assert_eq!(window.next(), None);
}
</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（4）<div>漂亮，老师叕解答了我的好多疑惑。现在唯一有点要适应的就是函数数式编程。C++ 和 Go 写多了，一上来就是 for 循环，要适应 Rust 的想法也是个不小的挑战。</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/6b/b813362b.jpg" width="30px"><span>陈溯</span> 👍（0） 💬（0）<div>第二题。 按照陈老师的思路让gpt写了代码。基本是一样的。就是有一行微调了。

&#47;&#47; 这句很重要，它让所有实现了 Iterator 的 T 都自动实现 IteratorExt
impl&lt;T: ?Sized&gt; IteratorExt for T where T: Iterator {}

微调成：

&#47;&#47; Implement IteratorExt for all types that implement the Iterator trait
impl&lt;I: Iterator&gt; IteratorExt for I {}
</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/a3/2d/845f2428.jpg" width="30px"><span>哈哈哈哈哈哈哈</span> 👍（0） 💬（0）<div>第二题可以结合slice的chunks, 加上文中的函数式调用：
```rust
    let data = vec![1, 2, 3, 4, 5];
    let ret = data.as_slice().chunks(2).collect::&lt;Vec&lt;_&gt;&gt;();
    println!(&quot;{:?}&quot;, ret);
```
不过这种解法可能脱离这题的初衷了</div>2024-06-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/TusRVU51UggZGpicXMgH64Cb8jek0wyTOpagtUHNAj0EPbhbEv0FJpFU2K3glbtOdJXiaQ9o6QoEfv5PiaIu7rwng/132" width="30px"><span>Geek_a6c6ce</span> 👍（0） 💬（0）<div>咔哒</div>2022-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/72/c1/59509397.jpg" width="30px"><span>沈畅</span> 👍（0） 💬（1）<div>官方文档 filter里面用了两个 **
let a = [0, 1, 2];

let mut iter = a.iter().filter(|x| **x &gt; 1); &#47;&#47; need two *s!

assert_eq!(iter.next(), Some(&amp;2));
assert_eq!(iter.next(), None);

为啥 我们只用一个就行？
let v = vec![1,2,3,4];
    let ret = v.iter()
               .map(|v| v*v)
               .filter(|v| *v &lt; 16)
               .take(5)
               .collect::&lt;Vec&lt;_&gt;&gt;();</div>2022-07-25</li><br/>
</ul>