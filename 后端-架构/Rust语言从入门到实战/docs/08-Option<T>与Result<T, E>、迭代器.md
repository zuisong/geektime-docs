你好，我是Mike，今天我们一起来重点学习在Rust中高频使用的 `Option<T>`、`Result<T, E>`、迭代器，通过学习这些内容，我们可以继续夯实集合中所有权相关的知识点。

`Option<T>` 和 `Result<T, E>` 并不是Rust的独创设计，在Rust之前，OCaml、Haskell、Scala等已经使用它们很久了。新兴的一批语言Kotlin、Swift 等也和Rust一样引入了这两种类型。而C++17之后也引入了它们。

这其实能说明使用 `Option<T>` 和 `Result<T, E>` 逐渐成了编程语言圈子的一种新共识。而迭代器已经是目前几乎所有主流语言的标配了，所以我们也来看看Rust中的迭代器有什么独到的地方。

如果你习惯了命令式编程或OOP编程，那么这节课我们提到各种操作对你来说可能有点陌生，不过也不用担心，这节课我设计了大量示例，你可以通过熟悉这些示例代码，掌握Rust中地道的编程风格。

## `Option<T>` 与 `Result<T, E>`

`Option<T>` 与 `Result<T, E>` 在Rust代码中随处可见，但是我们到现在才开始正式介绍，就是因为它们实际是带类型参数的枚举类型。

### `Option<T>` 的定义

```plain
pub enum Option<T> {
    None,
    Some(T),
}
```
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/28/cb/53/74a6cd05.jpg" width="30px"><span>天高地迥</span> 👍（17） 💬（1）<div>Vec&lt;String&gt; []索引不能move的原因思考：
Vec实现了Index trait的index方法，该方法返回一个引用。然后使用［］语法糖的时候，编译器会自动解引用：v［0］变成*v.index(&amp;0)。其实错误的本质是borrowed value不能move out。</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/f1/bd61dbb1.jpg" width="30px"><span>Ransang</span> 👍（7） 💬（1）<div>HashMap实现了into_iter()，因此可以用for语句获取其所有权，另外我在老师发的hashmap的文档中发现HashMap的iter()和iter_mut()是分类在Implementations中，而into_iter()是在Trait Implementations中，请问这里面有什么特殊之处吗</div>2023-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（4） 💬（1）<div>老师讲的很好，多了解rust底层规则，才能写出更好的代码。</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（2） 💬（1）<div>    let arr = vec![1,3,3,4];
    let a = arr[0];
    println!(&quot;{}&quot;, a);
    println!(&quot;{:?}&quot;, arr);
对于Vec&lt;u32&gt;是可以用v[0]的，因为u32是可以Copy的</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/73/93/abb7bfe3.jpg" width="30px"><span>Marco</span> 👍（2） 💬（1）<div>老师你好。
&quot;next() 方法&quot;这一节的例子也可以改为如下结构吧
    loop {
        match an_iter.next() {
            Some(i) =&gt; println!(&quot;{i}&quot;),
            None =&gt; break,
        }
    }</div>2023-11-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（1） 💬（1）<div>for (k, v) in myhash { &#47;&#47;`myhash` moved due to this implicit call to `.into_iter()`
    &#47;&#47; todo:
    &#47;&#47; 这里会获得v的所有权，并且消耗掉myhash
}

println!(&quot;{:?}&quot;, myhash); &#47;&#47;value borrowed here after move</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（1） 💬（1）<div> 定义了类型以后，let a: Vec&lt;u32&gt; = [1, 2, 3, 4, 5];语法错误
修改为let a= [1, 2, 3, 4, 5];</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（1）<div>请教下老师，文章中“不解包的情况下如何操作？”小节部分说到 Result&lt;T, E&gt; 的常用方法 map() 时，里面示例代码的模式匹配的 Err(..) 分支是什么意思？我试了 Err(_) 也是可以执行通过的，_ 忽略元组枚举变体 Err 的负载，（和 .. 相比）它们两个有什么区别？分别什么时候使用哪个呢？</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/e8/f7/1b45fa46.jpg" width="30px"><span>wcf</span> 👍（0） 💬（2）<div>为什么会有这个差异呢？你可以从我们第 2 讲所有权相关知识中找到答案。
============
没看出来为什么?</div>2024-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3f/7d/f624fa69.jpg" width="30px"><span>当初莫相识</span> 👍（0） 💬（0）<div>C++ 现在有Option，但是没有Result，可以如何设计自行设计一个Result呢</div>2024-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b2/8c/77d4d9bf.jpg" width="30px"><span>落星野</span> 👍（0） 💬（0）<div>上面对Go语言返回值的说法有一点小问题，Go语言不限制返回值的数量与类型，最后一个返回的 err 只是一种编码习惯，一般用于返回实现了 Error 接口的实例，亦即只要实现了 error.Error() 方法的实例返回都皆可。如果用户为了简便起见，在最后返回string类型（字符串），则返回的 err 就是一个字符串。</div>2024-10-21</li><br/><li><img src="" width="30px"><span>Geek_93cb91</span> 👍（0） 💬（0）<div>买过好几本书了&#xff0c;反复入门再入门&#xff0c;感觉唐老师的内容比书全面多了&#xff0c;再入门一遍&#xff0c;最后一遍&#xff01;</div>2024-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/8c/71ed37f8.jpg" width="30px"><span>wbytts</span> 👍（0） 💬（0）<div>unwrap_or_default 的配图，Result那一列写错文字了</div>2024-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/50/10/c57c7389.jpg" width="30px"><span>Massdama</span> 👍（0） 💬（0）<div>持有使用权的数据需要所有时要考虑借 也就是引用</div>2024-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（0）<div>第三次刷基础篇，之前不知道Some(T)是什么，具体来说是不知道Some是什么类型，因为枚举内可以包含多种类型，那么Some是什么类型？看得好懵，心里慌得一批。这次搜索了一下，大多只是说Some是Option类型，只看到Rust By Example里说了一句Some(value)是元组结构体，噢， 终于没那么懵了</div>2024-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（1）<div>可以具体展开解释一下“let maybe_some_len = maybe_some_string.map(|s| s.len());” 里面的 “map(|s| s.len())” 吗？猜|s|是闭包，s是什么呢？ self ？猜s.len()是获取长度， 但|s| s.len() 合起来写就看懵了。</div>2024-04-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（0）<div>思考题： 用 entry
use std::collections::hash_map::Entry;
match some_hashmap.entry(key) {
    Entry::Occupied(value) =&gt; ...
    Entry::Vacant(vacant entry) =&gt; ...
}

具体类型应该有点对不上， 回头看看文档的</div>2023-12-14</li><br/>
</ul>