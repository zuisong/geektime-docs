你好，我是陈天。

通过上一讲的学习，我们对 Rust 类型系统的本质有了认识。作为对类型进行定义、检查和处理的工具，类型系统保证了某个操作处理的数据类型是我们所希望的。

在Rust强大的泛型支持下，我们可以很方便地定义、使用泛型数据结构和泛型函数，并使用它们来处理参数多态，让输入输出参数的类型更灵活，增强代码的复用性。

今天我们继续讲多态中另外两种方式：特设多态和子类型多态，看看它们能用来解决什么问题、如何实现、如何使用。

如果你不太记得这两种多态的定义，我们简单回顾一下：特设多态包括运算符重载，是指同一种行为有很多不同的实现；而把子类型当成父类型使用，比如 Cat 当成 Animal 使用，属于子类型多态。

这两种多态的实现在Rust中都和 trait 有关，所以我们得先来了解一下 trait 是什么，再看怎么用 trait 来处理这两种多态。

## 什么是 trait？

trait 是 Rust 中的接口，它**定义了类型使用这个接口的行为**。你可以类比到自己熟悉的语言中理解，trait 对于 Rust 而言，相当于 interface 之于 Java、protocol 之于 Swift、type class 之于 Haskell。

在开发复杂系统的时候，我们常常会强调接口和实现要分离。因为这是一种良好的设计习惯，它把调用者和实现者隔离开，双方只要按照接口开发，彼此就可以不受对方内部改动的影响。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（12） 💬（5）<div>1. 不可以。关联类型无法就只能impl一次了，我们需要为Complex实现多个Add&lt;Rhs&gt;。
2. 不能。返回类型中的 Self 需要是Sized，而 dyn Write 不是Sized。
3. #[derive(Debug, Copy, Clone)]
4. impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
        type Item = &amp;&#39;a str;

        fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
            match self.s.find(self.delimiter) {
                None =&gt; None,
                Some(i) =&gt; {
                    let s = &amp;self.s[..i + self.delimiter.len_utf8()];
                    *self.s = &amp;self.s[i + self.delimiter.len_utf8()..];
                    if let Some((start, _)) =
                        s.as_bytes().iter().enumerate().find(|(_, b)| **b != b&#39; &#39;)
                    {
                        Some(&amp;s[start..])
                    } else {
                        None
                    }
                }
            }
        }
    }

这个SentenceIter的功能定义不明确，分割出来的每个sentence如果都需要包括delimiter的话，那剩余部分没有delimiter的情况该返回None吗？或者返回一个不带delimiter的剩余部分？都很别扭。</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（6） 💬（1）<div>1. 不应该这么做。如果这么做的话，同一个类型对同一个 trait 只能有一个实现，
Rhs 也之能有一种可能，这样就不能既实现 String + String 又实现 String + &amp;str，没有扩展性。

2. 不能编译通过，因为 by_ref 返回值含有 Self，不能作为 trait object 的方法使用。

3. 对 Complex 实现 Copy 和 Clone

```
#[derive(Debug, Copy, Clone)]
struct Complex {
    real: f64,
    imagine: f64,
}
```

4. 

```rust
impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str;

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        self.s.find(self.delimiter).map(|index| {
            let next = &amp;self.s[..index + self.delimiter.len_utf8()];
            *self.s = &amp;self.s[index + self.delimiter.len_utf8()..];
            next.trim_start()
        })
    }
}
```

有个小小的疑问想请教下老师，在 **Trait Object 的实现机理** 这一小节开始给的配图中，
formatter 这个 trait object 的 ptr 为啥会指向参数 text 呢？不是指向 HtmlFormatter 这个实例数据吗？</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（3） 💬（3）<div>```
    &#47;&#47; 指向同一种类型的同一个 trait 的 vtable 地址相同
    &#47;&#47; 这里都是 String + Display
    assert_eq!(vtable1, vtable3);
    &#47;&#47; 这里都是 String + Debug
    assert_eq!(vtable2, vtable4);
```

我原本以为String有个method call table, Display也有一个单独的; 那么说, 我自己写了个trait给String type, 岂不是编译的时候, 我自己提供的method需要append到String之前已经有的vtable?

1. vtable和method call table有啥区别呢?

2. 那么call `fn fmt(&amp;self, f: &amp;mut Formatter&lt;&#39;_&gt;) -&gt; Result;`的时候, 编译器是知道这个call在各个不同的实现中vtable的offset? 而且, 这些offset都要一样? 因为我记得, 编译的时候, 因为类型被erase了, 只能通过addr + offset (ptr, *args) 来call metho

例如, vtable1 + offset 和 vtable3 + offset 的地址都是call table中 fmt method 对应地址?</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/6f/a0/5ae45670.jpg" width="30px"><span>QY</span> 👍（2） 💬（3）<div>请问第四题为什么要用&amp;mut &amp;s 呢？ 是性能更好吗？
感觉&amp;s使用起来自由度更高。宣言s时不需要mut s。</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/08/e1/b4748943.jpg" width="30px"><span>夏洛克Moriaty</span> 👍（2） 💬（1）<div>今天内容很多，也很细，看来需要常来温故才行</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/3f/83/fa29cc24.jpg" width="30px"><span>王鹏飞</span> 👍（1） 💬（1）<div>内容言简意赅， 只讲核心， 含金量十足； 但是需要自己补充相对基础的东西，才能理解</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（1） 💬（2）<div>老师，这里关于静态分发和动态分发，有个例子没搞懂

#[drive(Debug)]
struct Foo;

trait Bar{
    fn baz(&amp;self);
}

impl Bar for Foo{
    fn baz(&amp;self) { println!(&quot;{:?}&quot;,self)};
}

fn static_dispatch&lt;T&gt;(t: &amp;T) where T:Bar{
    t.baz();
}

&#47;&#47;为什么这里是动态分发就无法确定类型大小
&#47;&#47;这里t也是限制为&amp;Bar对象呀.
fn dynamic_dispatch(t: &amp;Bar){
  t.baz();
}

这里不能理解的是动态分发，参数t也是要求为&amp;Bar的呀，那么这里到底和静态分发的核心区分是什么？凭什么就无法确定类型大小而需要用虚表呢？这个实在不太理解，多谢了。</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（1） 💬（1）<div>&gt; C++ &#47; Java 指向 vtable 的指针，在编译时放在类结构里，

现在C++的vtable也是分开放的 (可能看编译器, clang是分开的); 

不过对 cpp, 对interface的实现大家都和original class definition放在一起. 没有试过在分开的文件中impl一个cpp的class的interface (parent inheritance). 可能也行, 但是不符合cpp的convention. 

rust相对而言, 对某个类型的impl可以到处放.

```
vtable for Foo:
        .quad   0
        .quad   typeinfo for Foo    &#47;&#47; RTTI for foo
        .quad   Foo::method1()      &#47;&#47; where vtable starts
        .quad   Bar::method2()      &#47;&#47; for method2 in vtable
        .quad   Foo::~Foo() [complete object destructor]
        .quad   Foo::~Foo() [deleting destructor]
```

https:&#47;&#47;guihao-liang.github.io&#47;2020&#47;05&#47;30&#47;what-is-vtable-in-cpp</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/a2/c30ac459.jpg" width="30px"><span>hughieyu</span> 👍（1） 💬（1）<div>1. 不可以。 Complex不能实现Add多次，只能实现对一种类型的计算。
2. 不能。 对于trait object来说， Self信息已经被擦除了。
3. #[derive(Debug, Copy, Clone)] 或者 用自定义类型包装Rc实现Add 如RcComplex(Rc&lt;Complex&gt;)
4. impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str; &#47;&#47; 想想 Item 应该是什么类型？

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
       match self.s.find(self.delimiter) {
           None =&gt; None,
           Some(idx) =&gt; {
               let slice = &amp;self.s[..idx+self.delimiter.len_utf8()];
                *self.s = &amp;self.s[idx+self.delimiter.len_utf8()..];

                match slice.as_bytes().iter().enumerate().find(|(_,b)|**b != b&#39; &#39;){
                    None =&gt; None,
                    Some((start,_)) =&gt; Some(&amp;slice[start..]),
                }
           }
       }
    }
}

问题： trait泛型和关联类型的使用场景还是有些模糊</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（1）<div>陈天老师的这部分是目前看到的最生动的教程，the book对有些内部机制bi而不谈，其他书面教程感觉我自己的语文没学好。我现在是看了第20章再回头看的，终于明白了trait object这个之前差不多直接跳过的概念。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（0） 💬（2）<div>第四题, 用标准库里的`split_at`实现一个:

```rust
struct SentenceIter&lt;&#39;a&gt; {
    s: &amp;&#39;a mut &amp;&#39;a str,
    delimiter: char,
}

impl&lt;&#39;a&gt; SentenceIter&lt;&#39;a&gt; {
    pub fn new(s: &amp;&#39;a mut &amp;&#39;a str, delimiter: char) -&gt; Self {
        Self { s, delimiter }
    }
}

impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str; 

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if self.s.is_empty() {
            return None;
        }
        match self.s.find(self.delimiter) {
            Some(count) =&gt; {
                   &#47;&#47;标准库的split_at 方法
                let (first, last) = self.s.split_at(count + self.delimiter.len_utf8());
                *self.s = last.trim();  &#47;&#47;把self.s修改为split之后的后半部分
                return Some(first.trim());  &#47;&#47;返回前半部分
            }
            None =&gt; { &#47;&#47;处理没有找到的情况
                let s = (*self.s).trim();
                *self.s = &quot;&quot;;
                if s.is_empty() { &#47;&#47;如果此时s长度为0, 则返回None, 否则将s先trim之后返回
                    return None;
                } else {
                    return Some(s);
                }
            }
        }
    }
}

```</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/22/d12f7a72.jpg" width="30px"><span>TheLudlows</span> 👍（0） 💬（3）<div>老师，为什么加了关联类型之后，需要用Sized对Self进行限定呢？</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/8c/8e3d356c.jpg" width="30px"><span>野山门</span> 👍（0） 💬（1）<div>看大家的答案后，小小的改进了一下第四题：
```
impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
  type Item = &amp;&#39;a str; &#47;&#47; 想想 Item 应该是什么类型？

  fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
    if self.s.trim().is_empty() {
      return None;
    }
    match self.s.find(self.delimiter) {
      None =&gt; {
        let s = self.s.trim();
        *self.s = &quot;&quot;;
        Some(s)
      }
      Some(i) =&gt; {
        let next_index = i + self.delimiter.len_utf8();
        let s = &amp;self.s[..next_index].trim();
        *self.s = &amp;self.s[next_index..];
        Some(s)
      }
    }
  }
}
```</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/11/323358ed.jpg" width="30px"><span>wzx</span> 👍（0） 💬（2）<div>第四题：

struct SentenceIter&lt;&#39;a&gt; {
    s: &amp;&#39;a mut &amp;&#39;a str,
    delimiter: char,
    splited: Vec&lt;&amp;&#39;a str&gt;,
    index: usize,
}

impl&lt;&#39;a&gt; SentenceIter&lt;&#39;a&gt; {
    pub fn new(s: &amp;&#39;a mut &amp;&#39;a str, delimiter: char) -&gt; Self {
        let splited: Vec&lt;&amp;&#39;a str&gt; = s.split_inclusive(delimiter).collect();
        Self {
            s,
            delimiter,
            splited,
            index: 0
        }
    }
}

impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str; &#47;&#47; 想想 Item 应该是什么类型？

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if self.index &lt; self.splited.len() {
            let r = Some(self.splited[self.index].trim());
            self.index += 1;
            return r
        }
        None
    }
}</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（0） 💬（1）<div>rust泛型真的太抽象了</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>“如果不提供泛型参数，那么加号右值和左值都要是相同的类型。”，解决了我根据前一节内容看到“impl Add&lt;&amp;str&gt; for String”的困惑，这种感觉真的舒服，你仔细琢磨的问题，不明白的，老师下节课就告诉你了。</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/3e/edb93e8c.jpg" width="30px"><span>青山</span> 👍（2） 💬（0）<div>官方文档对object safety的讨论被移除了，发现在https:&#47;&#47;doc.rust-lang.org&#47;reference&#47;items&#47;traits.html#object-safety中有进行讨论</div>2023-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/e0/3b/8ec916b2.jpg" width="30px"><span>多少</span> 👍（2） 💬（0）<div>听音频总结部分有彩蛋哈哈</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（0）<div>&quot;第二，Rust 对含有 async fn 的 trait &quot; 这部分应该更新了吧？现在rust已经支持 含有 async fn 的 trait</div>2024-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/02/11/37e1a4d8.jpg" width="30px"><span>难念的经</span> 👍（0） 💬（0）<div>```rust
use std::str::SplitInclusive;


struct SentenceIter&lt;&#39;a&gt; {
    iter:  SplitInclusive&lt;&#39;a, char&gt;,
}

impl&lt;&#39;a&gt; SentenceIter&lt;&#39;a&gt; {
    pub fn new(s: &amp;&#39;a mut &amp;&#39;a str, delimiter: char) -&gt; Self {
        Self { iter: s.split_inclusive(delimiter).into_iter() }
    }
}

impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str; &#47;&#47; 想想 Item 应该是什么类型？

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        &#47;&#47; 如何实现 next 方法让下面的测试通过？
        match self.iter.next() {
            Some(value) =&gt; Some(value.trim()),
            None =&gt; None,
        }
    }
}



#[test]
fn it_works() {
    let mut s = &quot;This is the 1st sentence. This is the 2nd sentence.&quot;;
    let mut iter = SentenceIter::new(&amp;mut s, &#39;.&#39;);
    assert_eq!(iter.next(), Some(&quot;This is the 1st sentence.&quot;));
    assert_eq!(iter.next(), Some(&quot;This is the 2nd sentence.&quot;));
    assert_eq!(iter.next(), None);
}

fn main() {
    let mut s = &quot;a。 b。 c&quot;;
    let sentences: Vec&lt;_&gt; = SentenceIter::new(&amp;mut s, &#39;。&#39;).collect::&lt;Vec&lt;&amp;str&gt;&gt;();
    println!(&quot;sentences: {:?}&quot;, sentences);
}
```</div>2024-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/08/2b/7a1fb4ff.jpg" width="30px"><span>David.Du</span> 👍（0） 💬（0）<div>这两张内容一定要多读几遍</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/7c/2e/f200062c.jpg" width="30px"><span>你看上去很好吃</span> 👍（0） 💬（0）<div>    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if self.s.is_empty() {
            return None;
        }
        if let Some(pos) = self.s.find(self.delimiter) {
            let left = &amp;self.s[..pos+self.delimiter.len_utf8()].trim();
            let right = &amp;self.s[pos+self.delimiter.len_utf8()..];
            *self.s = right;
            Some(left)
        } else {
            let result = *self.s;
            *self.s = &quot;&quot;;
            Some(result.trim())
        }
    }</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>字符串解析为数字代码，没法解析负数啊</div>2023-09-15</li><br/><li><img src="" width="30px"><span>Zoom 6</span> 👍（0） 💬（0）<div>参考其他同学的代码，学习了使用 split_at 
impl&lt;&#39;a&gt; Iterator for SentenceIter&lt;&#39;a&gt; {
    type Item = &amp;&#39;a str;

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        if let Some(index) = self.s.find(self.delimiter) {
            let (first, second) = self.s.split_at(index + self.delimiter.len_utf8());
            *self.s = second.trim();
            Some(first.trim())
        } else {
            if self.s.len() == 0 {
                None
            } else {
                let s = *self.s;
                *self.s = &quot;&quot;;
                Some(s.trim())
            }
        }
    }
}</div>2023-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/d0/efa32d10.jpg" width="30px"><span>张晶鹏</span> 👍（0） 💬（1）<div>示例里面的
impl Parse for Twhere T: FromStr + Default,

这个用法怎么理解呢，为所有满足 FromStr + Default 这个约束的类型实现了一个通用的函数？编译器会默认为把这个实现关联到子类型吗

</div>2023-04-15</li><br/><li><img src="" width="30px"><span>yxxu</span> 👍（0） 💬（0）<div>老师，为啥  &amp;&#39;a mut &amp;&#39;a str，这样标注生命周期，在创建了 SentenceIter 之后 打印 s1，会报错？
代码如下：
https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=2aa9abf3f0c2ce781d1a34d36b30bff9</div>2023-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/83/c04e6b76.jpg" width="30px"><span>Darren</span> 👍（0） 💬（1）<div>请问 陈天老师，第4题，成员类型s: &amp;&#39;a mut &amp;&#39;a str,  我看写成 s: &amp;&#39;a str也可以， 像您那么写的好处是什么呢？</div>2022-10-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/6xQSiaCXJUM56oosZbUtm7qM1M0QQd8c4Qov8BDZGGnpe6nU2v8MibP0GiaaBpibTbcXzItZrjBwibD7IadpDnlIqKA/132" width="30px"><span>Geek_e284c2</span> 👍（0） 💬（0）<div>在基本 trait 这一小节中。
    关于把 trait 当成父类，实现 trait 的类型比做子类，那么有默认实现的方法相当于子类中可以重载但不是必须重载的方法。
    在Java和C++中方法的重载是具有相同的方法名，但是形参列表不同，可以对方法进行重载，而文中对应的重载应该是对应 Java&#47;C++ 中的函数重写，即子类型可以对父类型中的方法进行覆盖重写。
    然后导致我这里的理解有问题，所以这里应该是不是写错了，还是Rust中的重载与重写和Java中的不同。</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/8a/7c1baa25.jpg" width="30px"><span>buoge</span> 👍（0） 💬（0）<div>这一章 从早上上班，看到晚上下班 lol</div>2022-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIDqHQQByGiaXcAk94MdDn3ftupZLXyR6bAKibxOzMxy5h3uBwZ7QiaCiaIfbCMK0cIQfGNax8iawoiaQAg/132" width="30px"><span>nuan</span> 👍（0） 💬（0）<div>“self 在用作方法的第一个参数时，实际上是 self: Self 的简写”，没明白 self: Self 是什么。</div>2022-03-13</li><br/>
</ul>