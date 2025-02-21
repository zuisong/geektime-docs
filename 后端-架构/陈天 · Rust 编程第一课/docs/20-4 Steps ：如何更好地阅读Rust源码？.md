你好，我是陈天。

到目前为止，Rust 的基础知识我们就学得差不多了。这倒不是说已经像用筛子一样，把基础知识仔细筛了一遍，毕竟我只能给你提供学习Rust的思路，扫清入门障碍。老话说得好，师傅领进门修行靠个人，在 Rust 世界里打怪升级，还要靠你自己去探索、去努力。

虽然不能帮你打怪，但是打怪的基本技巧可以聊一聊。所以在开始阶段实操引入大量新第三方库之前，我们非常有必要先聊一下这个很重要的技巧：**如何更好地阅读源码**。

其实会读源码是个终生受益的开发技能，却往往被忽略。在我读过的绝大多数的编程书籍里，很少有讲如何阅读代码的，就像世间的书籍千千万万，“如何阅读一本书”这样的题材却凤毛麟角。

当然，在解决“如何”之前，我们要先搞明白“为什么”。

## 为什么要阅读源码？

如果课程的每一讲你都认真看过，会发现时刻都在引用标准库的源码，让我们在阅读的时候，不光学基础知识，还能围绕它的第一手资料也就是源代码展开讨论。

如果说他人总结的知识是果实，那源代码就是结出这果实的种子。只摘果子吃，就是等他人赏饭，非常被动，也不容易分清果子的好坏；如果靠朴素的源码种子结出了自己的果实，确实前期要耐得住寂寞施肥浇水，但收割的时刻，一切尽在自己的掌控之中。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Fr0y2ad4CLZNN0iaokfdyfAGwzMdttoIVfgzjBlwaCW2YB26mZta4v6pI2DV0OibCeC1OhME7NmrZo9OoRAfIhwQ/132" width="30px"><span>Geek_1b6d74</span> 👍（17） 💬（1）<div>陈天大神太强了，学习他的课程不仅学习了一门新的语言，还弄明白了很多编程底层原理</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（6） 💬（1）<div>老师，专门开一期如何读开源项目源码吧，真的，这个比懂任何技巧都更有意义，目前也没有教这个的。</div>2021-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ca/fd/4e6dd31c.jpg" width="30px"><span>枸杞红茶</span> 👍（6） 💬（1）<div>我原本准备去超市摸鱼，陈天老师给我渔船把我扔到了大海里</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（3） 💬（1）<div>1. 我们一起大致分析了 Bytes 的 clone() 的使用的场景，你能用类似的方式研究一下 drop() 是怎么工作的么？

如果是Shared, 就像Arc那样decrease counter; 如果是KIND_VEC, with unique ownership, deallocate memory immediately.

    unsafe fn promotable_odd_drop(data: &amp;mut AtomicPtr&lt;()&gt;, ptr: *const u8, len: usize) {
        data.with_mut(|shared| {
            let shared = *shared;
            let kind = shared as usize &amp; KIND_MASK;
            if kind == KIND_ARC {
                release_shared(shared as *mut Shared);
            } else {
                debug_assert_eq!(kind, KIND_VEC);
                drop(rebuild_boxed_slice(shared as *mut u8, ptr, len));
            }
        });
    }

2. 仔细看 Buf trait 里的方法，想想为什么它为 &amp;mut T 实现了 Buf trait，但没有为 &amp;T 实现 Buf trait 呢？如果你认为你找到了答案，再想想为什么它可以为 &amp;[u8] 实现 Buf trait 呢？

因为advance method需要更改T内部状态

    fn advance(&amp;mut self, cnt: usize) {

3. 花点时间看看 BufMut trait 的文档。Vec 可以使用 BufMut 么？如果可以，试着写写代码在 Vec 上调用 BufMut 的各种接口，感受一下。

只能在`Vec&lt;u8&gt;` 上用; 跟着doc试了一下.

值得注意的是, `advance_mut`是 `unsafe`:

        #[inline]
        unsafe fn advance_mut(&amp;mut self, cnt: usize) {
            let len = self.len();
            let remaining = self.capacity() - len;
            assert!(
                cnt &lt;= remaining,
                &quot;cannot advance past `remaining_mut`: {:?} &lt;= {:?}&quot;,
                cnt,
                remaining
            );
            self.set_len(len + cnt);
        }

4. 如果有余力，可以研究一下 BytesMut。重点看一下 split_off() 方法是如何实现的。

`split_off` 也是根据kind来:

- 如果是KIND_VEC, 就变成两个Arc, 共享同一个buf pointer
- 如果是KIND_ARC, 就increase ref count, 设置不同的start, end

感觉真正困难的是 `reserve` 和 `resize`; 这两个method要求KIND_ARC; 这样, 所有outgoing的`BytesMut` 能view underlying Vec pointer change during reallocation</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f5/9d/104bb8ea.jpg" width="30px"><span>Geek2014</span> 👍（2） 💬（1）<div>而 data 这个 AtomicPtr 指针，在指向 Shared 结构时，这个结构的对齐是 2&#47;4&#47;8 字节（16&#47;32&#47;64 位 CPU 下），末尾一定不为 0：

老师，为啥对齐2&#47;4&#47;8字节，末尾一定不为0呢</div>2021-10-08</li><br/><li><img src="" width="30px"><span>Geek_b52974</span> 👍（1） 💬（1）<div>看後面的解釋還是有點懵，我試著照自己的理解說明
最後一位是用來記錄是否是 shared
但是我們會需要知道升級成 shared 前最後一位是 odd 還是 event 所以用   PROMOTABLE_ODD_VTABLE PROMOTABLE_EVENT_VTABLE 來做不同的 clone 方式

```
unsafe fn promotable_even_clone(data: &amp;AtomicPtr&lt;()&gt;, ptr: *const u8, len: usize) -&gt; Bytes {
    let shared = data.load(Ordering::Acquire);
    let kind = shared as usize &amp; KIND_MASK;

    if kind == KIND_ARC {
        shallow_clone_arc(shared as _, ptr, len)
    } else {
        debug_assert_eq!(kind, KIND_VEC);
        let buf = (shared as usize &amp; !KIND_MASK) as *mut u8;
        shallow_clone_vec(data, shared, buf, ptr, len)
    }
}
```
promotable_event_clone 相比 promotable_odd_clone 多了下面這個操作
let buf = (shared as usize &amp; !KIND_MASK) as *mut u8;

先把最後一位還原成原本的樣子，再進行 clone
不知道這樣理解對不對</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e4/a1/178387da.jpg" width="30px"><span>25ma</span> 👍（0） 💬（1）<div>值得反复深度阅读，很有收获</div>2022-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/7c/f6/028f80a8.jpg" width="30px"><span>施泰博</span> 👍（0） 💬（1）<div>看完我觉得值得，得反复看很多编了。</div>2021-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d3/ef/b3b88181.jpg" width="30px"><span>overheat</span> 👍（0） 💬（3）<div>Bytes可以支持反序吗？我想要从结尾往开头操作。。。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ab/b8/0a979678.jpg" width="30px"><span>小康</span> 👍（0） 💬（1）<div>老师，目前中国rust岗位很多都是区块链相关的技术岗位呀？？？java转Rust跨度会不会太大？？？
</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（0） 💬（1）<div>按照老师个步骤, 一步一步来, 受益匪浅!

试了试resize:

```
    use bytes::BytesMut;
    
    fn main() {
        let mut buf = BytesMut::from(&amp;b&quot;hello world&quot;[..]);
        let cap_orig = buf.capacity();
        let other = buf.split_off(5);
        assert_eq!(buf, &amp;b&quot;hello&quot;[..]);
        assert_eq!(buf.as_ptr() as usize + 5, other.as_ptr() as usize);
    
        buf.resize(cap_orig + 10, b&#39;w&#39;);
        println!(&quot;{:?}&quot;, buf);
        println!(&quot;{:?}&quot;, other);
        assert_ne!(buf.as_ptr() as usize + 5, other.as_ptr() as usize);
    }
  ```  

output

```
b&quot;hellowwwwwwwwwwwwwwww&quot;
b&quot; world&quot;
```

本以为resize了第一个buf, 会覆盖掉other的部分, 毕竟他们之前共享一个storage...

结果第一个buf新开了memory, 和other就撇清关系了...

BytesMut真的太难了...不过bytes这个crate真的很适合精读...里面有各种底层技巧…</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e3/3b/3125ed1d.jpg" width="30px"><span>目标</span> 👍（0） 💬（0）<div>我也暂停下，跟着大佬学习阅读源码。阅读完再继续学习。</div>2024-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（0） 💬（0）<div>牛逼</div>2023-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/80/18/4e23cd5e.jpg" width="30px"><span>日月星辰</span> 👍（0） 💬（1）<div>&amp;b&quot;hello world&quot;[..]  这是什么格式，懵逼了，基础太差，到处找不到解释这个的</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>针对思考题：

1.来看一段 promotable_even_drop 的代码，它会先判断保存在 data(AtomicPtr) 中的数据是否是共享的，如果是，直接调用 release_shared 进行释放(shared_drop 直接执行这一步即可)；如果不是共享数据，则先消除 data 中数据最后一位的 flag，然后调用free_boxed_slice 进行释放
unsafe fn promotable_even_drop(data: &amp;mut AtomicPtr&lt;()&gt;, ptr: *const u8, len: usize) {
    data.with_mut(|shared| {
        let shared = *shared;
        let kind = shared as usize &amp; KIND_MASK;

        if kind == KIND_ARC {
            release_shared(shared.cast());
        } else {
            debug_assert_eq!(kind, KIND_VEC);
            let buf = ptr_map(shared.cast(), |addr| addr &amp; !KIND_MASK);
            free_boxed_slice(buf, ptr, len);
        }
    });
} 
2. 因为 Buf Trait 中有 advance 这样的方法，其 reveiver type 是 &amp;mut self，如果为 T&amp; 实现了 Buf Trait，那么它无法调用 advance，会产生 immutable borrow cannot be borrowed as mutable 这样的错误。而之所以可以为 &amp;[u8] 实现 Buf Trait，是因为 advance 可以直接通过切片的方式对 *self 进行修改，即 advance(&amp;mut self, cnt) =&gt; *self= &amp;self[cnt..]
3. Vec 可以使用 BufMut，因为 Vec[u8] 实现了 BufMut Trait，文档中 BufMut 的第一个例子就是在 vec 上使用 BufMut
4. split_off 的核心在于 shallow_clone 函数，这个函数会先判断 self 的类型是否为共享，如果是，增加引用计数，如果不是，则先将其升级为共享数据，然后返回 BytesMut 对象。但这个方法本身是不安全的，需要调用者自己去保证返回的 BytesMut 和原来的 BytesMut 之间没有重叠的视图</div>2022-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>没想通为什么没为Vec&lt;u8&gt;实现Buf而只实现了BufMut</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/0b/ce/f0c520d1.jpg" width="30px"><span>鹅帮逮</span> 👍（0） 💬（0）<div>mark,阅读源码对于我还是有点难度，后面会再来复习</div>2022-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/da/b8/3f80b8a5.jpg" width="30px"><span>交流会</span> 👍（0） 💬（0）<div>老师您好,请问match的源码实现从哪里找呢,希望能提供下查找的思路就可以,doc.rs的src里只有大堆的注释和说明,却没看到源码,找了很久也没找到...</div>2022-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（0） 💬（0）<div>由于编译 proto 在 Windows 中文用户名称上出问题，我打算先阅读 prost-build 的源码</div>2021-10-19</li><br/>
</ul>