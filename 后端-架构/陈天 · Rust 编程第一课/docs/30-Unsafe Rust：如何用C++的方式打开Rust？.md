你好，我是陈天。

到目前为止，我们撰写的代码都在 Rust 精心构造的内存安全的国度里做一个守法好公民。通过遵循所有权、借用检查、生命周期等规则，我们自己的代码一旦编译通过，就相当于信心满满地向全世界宣布：这个代码是安全的！

然而，安全的 Rust 并不能适应所有的使用场景。

首先，**为了内存安全，Rust 所做的这些规则往往是普适性的**，编译器会把一切可疑的行为都严格地制止掉。可是，这种一丝不苟的铁面无情往往会过于严苛，导致错杀。

就好比“屋子的主人只会使用钥匙开门，如果一个人尝试着撬门，那一定是坏人”，正常情况下，这个逻辑是成立的，所有尝试撬门的小偷，都会被抓获（编译错误）；然而，有时候主人丢了钥匙，不得不请开锁匠开门（unsafe code），此时，是正常的诉求，是可以网开一面的。

其次，无论 Rust 将其内部的世界构建得多么纯粹和完美，它总归是**要跟不纯粹也不完美的外界打交道，无论是硬件还是软件**。

计算机硬件本身是 unsafe 的，比如操作 IO 访问外设，或者使用汇编指令进行特殊操作（操作 GPU或者使用 SSE 指令集）。这样的操作，编译器是无法保证内存安全的，所以我们需要 unsafe 来告诉编译器要法外开恩。

同样的，当 Rust 要访问其它语言比如 C/C++ 的库，因为它们并不满足 Rust 的安全性要求，这种跨语言的 FFI（Foreign Function Interface），也是 unsafe 的。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/51/22/d12f7a72.jpg" width="30px"><span>TheLudlows</span> 👍（1） 💬（1）<div>    pub fn as_mut_ptr(&amp;mut self) -&gt; *mut u8 {
        self as *mut str as *mut u8
    }
请问老师这个转换为什么要多一层 *mut str ，as *mut str 和 as *mut u8的区别是什么，还有说这个as 转换的过程做了什么</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>先把safe rust 弄清楚，再考虑 unsafe 的事</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（0） 💬（1）<div>不能直接使用 get_unchecked_mut() 去实现，因为即使在 unsafe 代码里面也不能对一个变量同时进行多个可变借用，需要先转换成裸指针。

不知道这样实现可以吗？
fn split_mut(s: &amp;mut str, sep: char) -&gt; Option&lt;(&amp;mut str, &amp;mut str)&gt; {
    let pos = s.find(sep);

    pos.map(|pos| {
        let len = s.len();
        let sep_len = sep.len_utf8();
        
        let ptr1: *mut u8 = s.as_mut_ptr();
        let ptr2: *mut u8 = s[(pos + sep_len)..].as_mut_ptr();
        
        unsafe {
            let s1 = std::slice::from_raw_parts_mut(ptr1, pos);
            let s2 = std::slice::from_raw_parts_mut(ptr2, len - (pos + sep_len));
            (std::str::from_utf8_unchecked_mut(s1), std::str::from_utf8_unchecked_mut(s2))
        }
    })
}

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=98493d711d7a002c318aace31ecb2af0</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/f1/d2fc86bb.jpg" width="30px"><span>终生恻隐</span> 👍（0） 💬（1）<div>fn split_mut(s: &amp;mut str, sep: char) -&gt; Option&lt;(&amp;mut str, &amp;mut str)&gt; {
    let pos = s.find(sep);

    pos.map(|pos| unsafe {
        let len = s.len();
        let sep_len = sep.len_utf8();

        let ss = s.as_mut_ptr();
        let mut scl = &amp;mut *(slice_from_raw_parts_mut(ss, pos));
        let mut scr = &amp;mut *(
            slice_from_raw_parts_mut(
                ss.offset((pos + sep_len) as isize), len-(pos + sep_len)
            )
        );

        &#47;&#47; println!(&quot;left {}&quot;, from_utf8_unchecked_mut(scl));
        &#47;&#47; println!(&quot;left {}&quot;, from_utf8_unchecked_mut(scr));

        (from_utf8_unchecked_mut(scl), from_utf8_unchecked_mut(scr))

    })
}</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（0） 💬（5）<div>因为 Send &#47; Sync 是 auto trait，所以大部分情况下，你自己的数据结构不需要实现 Send &#47; Sync，然而，当你在数据结构里使用裸指针时，因为裸指针是没有实现 Send&#47;Sync 的，连带着你的数据结构也就没有实现 Send&#47;Sync。但很可能你的结构是线程安全的，你也需要它线程安全。

但很可能你的结构是线程安全的，你也需要它线程安全？

这句话我咋理解不了啊，是线程安全的，咋还需要它线程安全？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div> let arr: [usize; 6] = unsafe { std::mem::transmute(map) };
 新版的rust1.72stable报错了，因为hashmap的源码更新了</div>2023-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>fn split_mut(s: &amp;mut str, sep: char) -&gt; Option&lt;(&amp;mut str, &amp;mut str)&gt; {
    let pos = s.find(sep);

    pos.map(|pos| {
        let len = s.len();
        let sep_len = sep.len_utf8();
        let p = s.as_mut_ptr();

        unsafe {
            let s1 = from_raw_parts_mut(p, pos);
            let s2 = from_raw_parts_mut(p.add(pos + sep_len), len - pos - sep_len);

            (from_utf8_unchecked_mut(s1), from_utf8_unchecked_mut(s2))
        }
    })
}</div>2022-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>关于思考题，我的实现：
```rust
fn split_mut(s: &amp;mut str, sep: char) -&gt; Option&lt;(&amp;mut str, &amp;mut str)&gt; {
    let pos = s.find(sep);
    pos.map(|pos| {
      let len = s.len();
      let sep_len = sep.len_utf8();
      let s1 = s.get_mut(0..pos).unwrap().as_mut_ptr();
      let s2 = s.get_mut(pos + sep_len..len).unwrap().as_mut_ptr();
      unsafe {
        let s1 = from_raw_parts_mut(s1, pos);
        let s2 = from_raw_parts_mut(s2, len - pos - sep_len);
        (from_utf8_unchecked_mut(s1), from_utf8_unchecked_mut(s2))
      }
    })
}
```
playground 连接： https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=7be8e52e1278665816a03eb30fbfaf60</div>2022-09-17</li><br/>
</ul>