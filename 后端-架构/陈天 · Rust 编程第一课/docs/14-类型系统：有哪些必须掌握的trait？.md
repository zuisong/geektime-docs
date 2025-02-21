你好，我是陈天。

开发软件系统时，我们弄清楚需求，要对需求进行架构上的分析和设计。在这个过程中，合理地定义和使用 trait，会让代码结构具有很好的扩展性，让系统变得非常灵活。

之前在 get hands dirty 系列中就粗略见识到了 trait 的巨大威力，使用了 From&lt;T&gt; / TryFrom&lt;T&gt; trait 进行类型间的转换（[第 5 讲](https://time.geekbang.org/column/article/413634)），还使用了 Deref trait （[第 6 讲](https://time.geekbang.org/column/article/414478)）让类型在不暴露其内部结构代码的同时，让内部结构的方法可以对外使用。

经过上两讲的学习，相信你现在对trait 的理解就深入了。在实际解决问题的过程中，**用好这些 trait，会让你的代码结构更加清晰，阅读和使用都更加符合 Rust 生态的习惯**。比如数据结构实现了 Debug trait，那么当你想打印数据结构时，就可以用 {:?} 来打印；如果你的数据结构实现了 From&lt;T&gt;，那么，可以直接使用 into() 方法做数据转换。

## trait

Rust 语言的标准库定义了大量的标准 trait，来先来数已经学过的，看看攒了哪些：

- Clone / Copy trait，约定了数据被深拷贝和浅拷贝的行为；
- Read / Write trait，约定了对 I/O 读写的行为；
- Iterator，约定了迭代器的行为；
- Debug，约定了数据如何被以 debug 的方式显示出来的行为；
- Default，约定数据类型的缺省值如何产生的行为；
- From&lt;T&gt; / TryFrom&lt;T&gt;，约定了数据间如何转换的行为。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（36） 💬（1）<div>老师，你讲得太通透，太详细了，太负责任了，全网最好的教程了</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3d/be/98bebd57.jpg" width="30px"><span>c4f</span> 👍（18） 💬（4）<div>1. 不行。因为 Vec 和 Copy 都不是用户自己 crate 中定义的，所以根据孤儿原则无法为 Vec 实现 Copy trait

2. 因为 Arc 实现了 Deref 和 DerefMut trait，解应用可以直接访问内部的 Mutex

3. 实现的时候遇到了一个问题：对于非法的 index （比如测试用例中的 128）该如何返回，没找到解决方法于是只针对 List&lt;u32&gt; 实现了 Index trait，这样在遇到非法 index 时返回 &amp;0 即可。
针对 Vec 测试了一下非法 index 的情形，发现会直接终止进程。具体代码如下

```rust
fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
    &#47;&#47; todo!();
    if let Some(idx_abs) = 
        if index &gt;= 0 {
            Some(index as usize)
        } else {
            self.len().checked_sub(index.abs() as usize)
        } {
        let mut iter = self.iter();
        for _i in 0..idx_abs {
            iter.next();
        }
        iter.next().unwrap_or(&amp;0)
    } else {
        &amp;0
    }
}
```

</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bc/2c/963688bb.jpg" width="30px"><span>noisyes</span> 👍（12） 💬（1）<div>刚才的小例子中要额外说明一下的是，如果你的代码出现 v.as_ref().clone() 这样的语句，也就是说你要对 v 进行引用转换，然后又得到了拥有所有权的值，那么你应该实现 From，然后做 v.into()。  这句话怎么理解呀</div>2021-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（5） 💬（1）<div>老师，这里有一些概念没搞清晰。
1. * 这个符号，有时表示解引用，有时表示获取变量地址的值，对吗？有点搞混场景了。
2. trait继承这里，经常看到一句话，组合优于继承，怎么理解。同时对于实现和继承来说，可能基础不扎实，一直没理解好什么时候继承什么时候实现，学java的时候，那些抽象类和接口也迷糊的很。

另外这里隐藏了很多东西，看老师代码的时候经常用unwrap，其实生产环境代码是非常危险的。例如今天写hashmap替换里面内容时，最好用containkeys判断一下，如果没有则插入一个空的，再使用get_mut和unwarp，这样就保证安全不会panic了。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（4） 💬（3）<div>第3题, 同样使用标准库的2个方法, `checked_rem_euclid`取得合理索引值, `iter().nth()`获得实际值
```rust
use std::{
    collections::LinkedList,
    ops::{Deref, DerefMut, Index},
};
struct List&lt;T&gt;(LinkedList&lt;T&gt;);

impl&lt;T&gt; Deref for List&lt;T&gt; {
    type Target = LinkedList&lt;T&gt;;

    fn deref(&amp;self) -&gt; &amp;Self::Target {
        &amp;self.0
    }
}

impl&lt;T&gt; DerefMut for List&lt;T&gt; {
    fn deref_mut(&amp;mut self) -&gt; &amp;mut Self::Target {
        &amp;mut self.0
    }
}

impl&lt;T&gt; Default for List&lt;T&gt; {
    fn default() -&gt; Self {
        Self(Default::default())
    }
}

impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let len = self.0.len();
        &#47;&#47;标准库的checked_rem_euclid方法, 如果len=0 则返回None
        &#47;&#47;这里直接把i进行unwrap, 如果链表长度不为0, 则i一定在0..len范围内, 可以放心使用, 
        &#47;&#47;如果长度为零, 意味这对一个空链表进行索引, 那么我panic应该也是合情合理的吧
        let i = (index as usize).checked_rem_euclid(len).unwrap();
        &amp;self.0.iter().nth(i).unwrap()
    }
}

#[test]
fn it_works() {
    let mut list: List&lt;u32&gt; = List::default();
    for i in 0..16 {
        list.push_back(i);
    }

    assert_eq!(list[0], 0);
    assert_eq!(list[5], 5);
    assert_eq!(list[15], 15);
    assert_eq!(list[16], 0);
    assert_eq!(list[-1], 15);
    assert_eq!(list[128], 0);
    assert_eq!(list[-128], 0);
}
```

playground 链接:  https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=73b4129f1a6608892691da92d501ba15</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/28/cc69ea4b.jpg" width="30px"><span>周烨</span> 👍（4） 💬（3）<div>1. 不能，因为不能确定T是否实现了Copy trait。
2. 因为Arc实现了Deref trait
3. ```impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let len = self.len() as isize;
        let i = if index % len &gt;= 0 {
                index % len
            } else {
                len + index % len
            } as usize;
        let it = self.iter();
        return it.skip(i).next().unwrap();
    }
}```</div>2021-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/08/e1/b4748943.jpg" width="30px"><span>夏洛克Moriaty</span> 👍（2） 💬（3）<div>let a = *list;
let b  = list.deref();

老师请问下这两种方式有什么区别，为什么a和b的类型不同？</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/50/87/a6637d48.jpg" width="30px"><span>GE</span> 👍（1） 💬（1）<div>1. 不能，但是这里和T关系无关，而是因为Vec本身已经实现了Drop trait，所以和Copy trait是冲突的
```
&#47;&#47; source code
unsafe impl&lt;#[may_dangle] T, A: Allocator&gt; Drop for Vec&lt;T, A&gt;
```

</div>2022-01-04</li><br/><li><img src="" width="30px"><span>Taozi</span> 👍（1） 💬（3）<div>第三题里面给List&lt;T&gt;实现DerefMut时，为什么不需要加type Target = LinkedList，那返回的Self::Target是什么。</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a3/87/eb923eb3.jpg" width="30px"><span>0@1</span> 👍（1） 💬（2）<div>老师，想提前问下unsafe相关的问题，这个目前比较困扰我进一步学习Rust.
比如这个 std::mem::forget(t), 看了下源码，是直接调用 ManuallyDrop::new(t), 看文档，好像这2个又不是直接等价的。forget的源码如下，多了些属性宏修饰，编译器是不是多加了处理，从而跟直接调用 ManuallyDrop::new(t)起到的效果不一样？

如果是的话，这些宏的文档在哪里可以看到，类似的这些编译器处理的宏有哪些，他们的文档在哪里，谢谢。
Note: 我学rust陆续2年了，看源码时对这些需要编译器额外处理的东西比较困惑，不知道如何去进一步的理解他们, rust中很多隐含规则貌似都有他们的影子。
#[inline]
#[rustc_const_stable(feature = &quot;const_forget&quot;, since = &quot;1.46.0&quot;)]
#[stable(feature = &quot;rust1&quot;, since = &quot;1.0.0&quot;)]
#[cfg_attr(not(test), rustc_diagnostic_item = &quot;mem_forget&quot;)]
pub const fn forget&lt;T&gt;(t: T) {
    let _ = ManuallyDrop::new(t);
}




</div>2021-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/11/677b83ba.jpg" width="30px"><span>james</span> 👍（0） 💬（1）<div>向老师请教一个问题：在如下Deref范例中，既然deref的self变量是&amp;Self类型，那self.value的类型应该就是&amp;Self.Target，但汉服返回时为何还要在self.value前加&amp;呢？

use std::ops::Deref;

struct DerefExample&lt;T&gt; {
    value: T
}
impl&lt;T&gt; Deref for DerefExample&lt;T&gt; {
    type Target = T;

    fn deref(&amp;self) -&gt; &amp;Self::Target {
        &amp;self.value
    }
}

</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/30/338409a9.jpg" width="30px"><span>作死的卡基</span> 👍（0） 💬（1）<div>想请教一下老师，比如要自己实现 Drop trait，有没有类似 Java 中子类覆写父类方法的机制，甚至覆写时还能用super.xxx()还能调用父类的被覆写方法。还是只能自己新建一个 trait？</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（0） 💬（1）<div>impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let len = self.len() as isize;
        if len == 0 {
            panic!(&quot;empty list&quot;);
        }
        let index = (index % len + len) % len;
        self.iter().nth(index as usize).unwrap()
    }
}
</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（3）<div>clone_from 这里说提高效率的，没看出来区别到底在哪里，源码里面也是直接 clone的？解释也没看懂，多谢了。</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/43/fa0a797e.jpg" width="30px"><span>三叶虫tlb</span> 👍（0） 💬（2）<div>&amp;self.0，0是指下标第一个属性的意思吗？</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（1）<div>打个卡，这一节内容有点多，断断续续多了好几遍才读完</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f8/e0/d6e3cc8f.jpg" width="30px"><span>qgaye</span> 👍（0） 💬（1）<div>请教老师，为啥 [1, 2, 3, 4] 是 impl Into&lt;Vec&lt;T&gt;&gt; 这个类型呢</div>2021-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ef/030e6d27.jpg" width="30px"><span>xl000</span> 👍（0） 💬（1）<div>```rust
impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let len = self.len() as isize;
        let mut n = if index &lt; 0 { len + index } else { index };
        if n &gt;= len || n &lt; 0 {
            n = 0;
        }
        self.iter().nth(n as usize).unwrap()
    }
}
```</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（1）<div>&quot;实际上，任何编程语言都无法保证不发生人为的内存泄漏，比如程序在运行时，开发者疏忽了，对哈希表只添加不删除，就会造成内存泄漏。但 Rust 会保证即使开发者疏忽了，也不会出现内存安全问题。&quot;，Rust 可以保证对哈希表只添加，不删除，还不会有内存泄漏吗？</div>2021-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/61/8f7fca5b.jpg" width="30px"><span>史双龙</span> 👍（0） 💬（2）<div>1.Box、Vec等好像不具备Copy属性类型。所以不行，
2.Arc 实现了 Deref 和 DerefMut trait
3.直接上第三题，用的笨方法。
impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        match (self.0.len().checked_sub(index.abs() as usize)) &gt; Some(0) {
            false =&gt; return self.0.iter().next().unwrap(),
            true =&gt; {
                let mut i = 0;
                let mut iter = self.0.iter();
                loop {
                    if i == index &amp;&amp; index &gt;= 0 {
                        return iter.next().unwrap();
                    }
                    if index &lt; 0 &amp;&amp; i == index + self.0.len() as isize {
                        return iter.next().unwrap();
                    }
                    iter.next();
                    i = i + 1;
                }
            }
        };
    }
}</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/8a/26/2e2f9cfc.jpg" width="30px"><span>Koco</span> 👍（2） 💬（0）<div>大部分教程都跟字典似的，罗列知识点，枯燥难啃。这教程讲得太好了，一边学一边忍不住赞叹。高屋建瓴，提纲挈领，深入浅出。不仅有术——结构化的知识，还有道——计算机语言的学习方法。陈老师太牛了。</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ca/68/161971d5.jpg" width="30px"><span>波罗</span> 👍（0） 💬（0）<div>在讲Copy trait和 Clone trait是有这样一句话：&quot;这样的 trait 虽然没有任何行为，但它可以用作 trait bound 来进行类型安全检查，所以我们管它叫标记 trait。&quot;，不太理解，难道Clone trait就不能用作trait bound了吗</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（0）<div>buf.sort() 这里有点不明白，在 IDE 中输入 buf，会提示有 sort 这个方法，但是我们并没有给 Buffer 添加 sort 方法啊？难道 Rust 默认为所有类型都实现了 sort 方法？</div>2024-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>老师，Copy trait是浅拷贝，按位复制栈数据，Clone  trait某些场景是深拷贝，某些场景是浅拷贝，引用计数增加而堆内存只有一份的就是浅拷贝，堆内存再复制一份形成一个新对象的就是深拷贝，这样理解对不对？</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/28/a7/1f6a6c5f.jpg" width="30px"><span>foobar</span> 👍（0） 💬（0）<div>Q1,Q2 前面的答案非常全面了。这里对 Q3 补充一种新的思路:
- 参考 Golang Zero Value 设计，增加 T:Default
- 安全性保证：虽然用到了 unsafe 代码，但是考虑到 List 的 Cell 成员，故 List:!Sync . 此处安全性得到保证

[Rust Playground](https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=74133fab4134f8102cafdcb101daa368)

```rust
use std::cell::Cell;
use std::{
    collections::LinkedList,
    ops::{Deref, DerefMut, Index},
};

&#47;&#47;&#47;! 本题需求的特殊性,访问越界位置时,要返回一个&#39;零值&#39;
struct List&lt;T&gt;(LinkedList&lt;T&gt;, Cell&lt;Option&lt;T&gt;&gt;);

impl&lt;T&gt; Deref for List&lt;T&gt; {
    type Target = LinkedList&lt;T&gt;;

    fn deref(&amp;self) -&gt; &amp;Self::Target {
        &amp;self.0
    }
}

impl&lt;T&gt; DerefMut for List&lt;T&gt; {
    fn deref_mut(&amp;mut self) -&gt; &amp;mut Self::Target {
        &amp;mut self.0
    }
}

impl&lt;T&gt; Default for List&lt;T&gt; {
    fn default() -&gt; Self {
        Self(Default::default(), Cell::new(None))
    }
}

&#47;&#47;&#47;! 为了返回&#39;零值&#39;, 这里限定了 T:Default
&#47;&#47;&#47;! &#39;零值&#39; 的概念,参考 Golang: https:&#47;&#47;go.dev&#47;tour&#47;basics&#47;12
impl&lt;T: Default&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let ls_len = self.len() as isize;
        if index &lt;= -ls_len || index &gt;= ls_len {
            let def = unsafe { &amp;mut *self.1.as_ptr() };
            if def.is_none() {
                *def = Some(Default::default());
            }
            return def.as_ref().unwrap();
        }
        let index = if index &lt; 0 { ls_len + index } else { index };
        self.iter().nth(index as usize).unwrap()
    }
}

fn main() {
    let mut list: List&lt;u32&gt; = List::default();
    for i in 0..16 {
        list.push_back(i);
    }

    assert_eq!(list[0], 0);
    assert_eq!(list[5], 5);
    assert_eq!(list[15], 15);
    assert_eq!(list[16], 0);
    assert_eq!(list[-1], 15);
    assert_eq!(list[128], 0);
    assert_eq!(list[-128], 0);
}


```</div>2023-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b8/43/015e2cc0.jpg" width="30px"><span>Silwings</span> 👍（0） 💬（0）<div>老师你好,请教一下,在arc_mutext_is_send_sync()的最终示例中,16和19行的花括号去掉就不能正常运行时为什么?</div>2023-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/5c/37/6717a50e.jpg" width="30px"><span>Dizzy</span> 👍（0） 💬（1）<div>```rust
impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        let len = self.0.len();
        let index = (len as isize + index) as usize % len;
        &amp;self.0.iter().nth(index).unwrap()
    }
}
```</div>2022-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/b1/2e96794c.jpg" width="30px"><span>flyflypeng</span> 👍（0） 💬（0）<div>老师，我按照最直接的逻辑来处理，很纠结如何才能返回一个T类型的默认值。参考老师的答案，我觉得对于输入的index值映射到0~len-1区间内，不是很符合预期的逻辑，可能对于不再区间范围内的，我们可能会返回错误，或者返回一个默认值
impl&lt;T&gt; Index&lt;isize&gt; for List&lt;T&gt; {
    type Output = T;

    fn index(&amp;self, index: isize) -&gt; &amp;Self::Output {
        if index &lt; 0 {
            &#47;&#47; 返回默认值的引用
        }

        for (i, item) in self.0.iter().enumerate() {
            if i == index as usize {
                return item;
            }
        }

        &#47;&#47;返回默认值引用
    }
}</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/b1/2e96794c.jpg" width="30px"><span>flyflypeng</span> 👍（0） 💬（0）<div>老师，我对于文中关于copy和clone的区别还不是很理解？不知道什么时候该用copy trait，什么时候用clone trait？</div>2022-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/0b/ce/f0c520d1.jpg" width="30px"><span>鹅帮逮</span> 👍（0） 💬（0）<div>所以上面的代码 Developer 类型在做参数传递时，会执行 Move 语义，而 Language 会执行 Copy 语义。
这句话怎么理解呢？为什么Language 不执行move</div>2022-04-30</li><br/>
</ul>