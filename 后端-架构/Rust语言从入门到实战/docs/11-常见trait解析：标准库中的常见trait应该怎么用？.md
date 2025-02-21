你好，我是Mike，今天我们一起来学习Rust中的常见trait。

前面两节课我们已经讲过trait在Rust中的重要性了，这节课就是trait在Rust标准库中的应用。Rust标准库中包含大量的trait定义，甚至Rust自身的某些语言特性就是在这些trait的帮助下实现的。这些trait和标准库里的各种类型一起，构成了整个Rust生态的根基，只有了解它们才算真正了解Rust。

注：这节课大量代码来自 [Tour of Rust’s Standard Library Traits](https://github.com/pretzelhammer/rust-blog/blob/master/posts/tour-of-rusts-standard-library-traits.md)，我加了必要的注解和分析。

学习完这节课的内容，你会对很多问题都豁然开朗。下面就让我们来学习标准库里一些比较常用的trait。

## 标准库中的常用trait

### Default

我们来看Default trait的定义以及对Default trait的实现和使用。

```plain
trait Default {
    fn default() -> Self;
}
```

```plain
struct Color(u8, u8, u8);
impl Default for Color {
    // 默认颜色是黑色 (0, 0, 0)
    fn default() -> Self {
        Color(0, 0, 0)
    }
}

fn main() {
    let color = Color::default();
    // 或
    let color: Color = Default::default();
}
```
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3a/2e/d8/7beb49a4.jpg" width="30px"><span>飞了的鸭子被煮了</span> 👍（4） 💬（1）<div>asref: A 到 B，
deref：B回到A</div>2024-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（3） 💬（1）<div>Deref 和 AsRef&lt;T&gt; 是 Rust 中用于类型转换的 trait。

Deref trait 允许你重载解引用操作符 *，使得一个类型可以被像指针一样解引用。这样可以方便地访问类型内部的数据。当你对一个实现了 Deref trait 的类型使用解引用操作符时，编译器会自动调用 Deref trait 中的 deref 方法来获取对应的值。

AsRef&lt;T&gt; trait 则是用于将一个类型转换为另一个类型的引用。它提供了一个 as_ref 方法，该方法返回一个指向目标类型的引用。这在需要将一个类型转换为另一个类型的引用时非常有用，例如将字符串转换为字节切片。

总结一下区别：

Deref trait 用于重载解引用操作符 *，使得一个类型可以被像指针一样解引用。
AsRef&lt;T&gt; trait 用于将一个类型转换为另一个类型的引用。
在使用上，如果你需要对一个类型进行解引用操作，你可以实现 Deref trait。如果你需要将一个类型转换为另一个类型的引用，你可以实现 AsRef&lt;T&gt; trait。</div>2023-12-22</li><br/><li><img src="" width="30px"><span>Zoom 6</span> 👍（2） 💬（1）<div>Deref 是重载了运算符，AsRef是做的类型转换</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/66/03/abb7bfe3.jpg" width="30px"><span>兰天白云</span> 👍（0） 💬（1）<div>老师，您在讲到from和into的时候，说“因为 into() 是方法，而 from() 是关联函数。”，而在trait声明里都是有返回值的呀？该怎样理解呢？</div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（0）<div>能讲一下在trait中如何使用async fn吗？我还不会使用</div>2023-12-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>as_ref 没印象了， 找gpt4看了看， 总结了下核心就这俩：

- implicit vs explicit
    - Deref trait 自动运行， `*T` 直接触发 deref()， 看起来像是隐式触发
    - AsRef trait 需要显式调用 as_ref()
- 功能不同（我看到这条的时候都愣了， 这谁不知道， 为撒还算是 key diff）
    - Deref 是解引用的
    - AsRef 是创建引用的</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>请问下面这一句，能否只写Ord和Eq？Ord是PartialOrd的超集, Eq是PartialEq的超集。 编译器应该可以判断出，已经实现了Ord和Eq，当然也肯定实现了PartialOrd和PartialEq。
#[derive(Ord, PartialOrd, PartialEq, Eq)] &#47;&#47; 注意这一句，4个都写上</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/25/2db95c79.jpg" width="30px"><span>杨赛军</span> 👍（0） 💬（1）<div>Deref 不能传递所有权变量，Asref可以传递所有权变量</div>2023-11-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（2） 💬（0）<div>笔记

1. Deref trait =&gt; 给 typeA 实现了 Deref trait 之后就可以 *typeAinstance 了

2. deref coercion =&gt; 我们要对 obj_0 做一些事情的时候， 如果发现 obj_0 不适配， 就试一下 *obj_0, 看看它的 deref 是否适配， 如果适配， 就对 deref result 搞事， 如果不适配， 就继续找 deref, 直到当前 obj 没有 deref 为止
</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/74/b6/42e74b6d.jpg" width="30px"><span>Logical_Monster</span> 👍（0） 💬（0）<div>运算符重载那里的代码应该改为，直接那样写main函数会有所有权问题：
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

&#47;&#47; 为 Point 类型实现 Add trait，这样两个Point实例就可以直接相加
impl Add for Point {
    type Output = Point;
    fn add(self, rhs: Point) -&gt; Point {
        Point {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = Point { x: 3, y: 4 };
    let p3 = p1 + p2;
    
    println!(&quot;{:?}&quot;, p3); &#47;&#47; Output: Point { x: 4, y: 6 }
    assert_eq!(p3, Point { x: 4, y: 6 });
}</div>2024-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/da/97/e421b1ae.jpg" width="30px"><span>周鹏</span> 👍（0） 💬（0）<div>struct Point {
    x: i32,
    y: i32,
}

&#47;&#47; 为 Point 类型实现 Add trait，这样两个Point实例就可以直接相加
impl Add for Point {
    type Output = Point;
    fn add(self, rhs: Point) -&gt; Point {
        Point {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = Point { x: 3, y: 4 };
    let p3 = p1 + p2; &#47;&#47; 这里直接用+号作用在两个Point实例上
&#47;&#47;这里move了
    assert_eq!(p3.x, p1.x + p2.x); &#47;&#47; ✅
&#47;&#47;这里不能再用会报错
    assert_eq!(p3.y, p1.y + p2.y); &#47;&#47; ✅
&#47;&#47;这里不能用
}</div>2024-03-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/da/97/e421b1ae.jpg" width="30px"><span>周鹏</span> 👍（0） 💬（0）<div>struct Point {
    x: i32,
    y: i32,
}

&#47;&#47; 为 Point 类型实现 Add trait，这样两个Point实例就可以直接相加
&#47;&#47; 建议加上
impl std::ops::Add for Point {
    type Output = Point;
    fn add(self, rhs: Point) -&gt; Point {
        Point {
            x: self.x + rhs.x,
            y: self.y + rhs.y,
        }
    }
}

fn main() {
    let p1 = Point { x: 1, y: 2 };
    let p2 = Point { x: 3, y: 4 };
    let p3 = p1 + p2; &#47;&#47; 这里直接用+号作用在两个Point实例上
    assert_eq!(p3.x, p1.x + p2.x); &#47;&#47; ✅
    assert_eq!(p3.y, p1.y + p2.y); &#47;&#47; ✅
}</div>2024-03-31</li><br/>
</ul>