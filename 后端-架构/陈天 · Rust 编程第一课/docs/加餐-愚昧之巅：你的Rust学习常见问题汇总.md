你好，我是陈天。

到目前为止，我们已经学了很多 Rust 的知识，比如基本语法、内存管理、所有权、生命周期等，也展示了三个非常有代表性的示例项目，让你了解接近真实应用环境的 Rust 代码是什么样的。

虽然学了这么多东西，你是不是还是有种“一学就会，一写就废”的感觉？别着急，饭要一口一口吃，任何新知识的学习都不是一蹴而就的，我们让子弹先飞一会。你也可以鼓励一下自己，已经完成了这么多次打卡，继续坚持。

在今天这个加餐里我们就休个小假，调整一下学习节奏，来聊一聊 Rust 开发中的常见问题，希望可以解决你的一些困惑。

## 所有权问题

**Q：**如果我想创建双向链表，该怎么处理？

Rust 标准库有 [LinkedList](https://doc.rust-lang.org/std/collections/struct.LinkedList.html)，它是一个双向链表的实现。但是当你需要使用链表的时候，可以先考虑一下，**同样的需求是否可以用列表 Vec&lt;T&gt;、循环缓冲区 VecDeque&lt;T&gt; 来实现**。因为，链表对缓存非常不友好，性能会差很多。

如果你只是好奇如何实现双向链表，那么可以用之前讲的 Rc / RefCell （[第9讲](https://time.geekbang.org/column/article/416722)）来实现。对于链表的 next 指针，你可以用 Rc；对于 prev 指针，可以用 [Weak](https://doc.rust-lang.org/std/rc/struct.Weak.html)。

Weak 相当于一个弱化版本的 Rc，不参与到引用计数的计算中，而Weak 可以 [upgrade](https://doc.rust-lang.org/std/rc/struct.Weak.html#method.upgrade) 到 Rc 来使用。如果你用过其它语言的引用计数数据结构，你应该对 Weak 不陌生，它可以帮我们打破循环引用。感兴趣的同学可以自己试着实现一下，然后对照这个[参考实现](https://gist.github.com/matey-jack/3e19b6370c6f7036a9119b79a82098ca)。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/87/cc/628b5fe3.jpg" width="30px"><span>秋声赋</span> 👍（2） 💬（1）<div>我看到用了很多的宏，这个有没有详细的说明呢？</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（49） 💬（1）<div>第一个，没有标注生命周期，但即使标注也不对，因为返回值引用了本地已经 drop 的 String，会造成悬垂指针问题；

第二个，和第一个类似，因为参数是具有所有权的 String，该 String 会在函数执行完后被 drop，返回值不能引用该 String；

第三个，因为 Chars 的完整定义是 Chars&lt;&#39;a&gt;，根据生命周期标注规则，Chars 内部的引用的生命周期和参数 name 一致，所以不会产生问题。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/ed/3dbe915b.jpg" width="30px"><span>乌龙猹</span> 👍（22） 💬（8）<div>陈老师，啥时候再出一门 Elixir 编程的第一课啊 </div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/38/c9/63ea8fe6.jpg" width="30px"><span>Arthur</span> 👍（12） 💬（1）<div>lifetime1:
name为函数内部的临时变量，类型是String，函数返回值为其引用，但引用的变量name生命周期在函数结束时，会被drop，因此此处引用失效，无值可借；

lifetime2:
name为具有所有权的参数，类型是String，在函数被调用时，所有权会move给name，在函数执行结束时，name会被drop，因此返回值的引用还是无值可借，编译器无法推导出合理的生命周期；

lifetime3:
chars()返回的iterator具有和函数参数name相同的生命周期，name本身又是一个借用，真正具有所有权的变量存活的比函数久，因此这个函数可以编译通过

参考材料：
编译器报错信息
```plain
   |
12 | fn lifetime1() -&gt; &amp;str {
   |                   ^ expected named lifetime parameter
   |
   = help: this function&#39;s return type contains a borrowed value, but there is no value for it to be borrowed from

  --&gt; src&#47;main.rs:18:31
   |
18 | fn lifetime2(name: String) -&gt; &amp;str {
   |                               ^ expected named lifetime parameter
   |
   = help: this function&#39;s return type contains a borrowed value with an elided lifetime, but the lifetime cannot be derived from the arguments

```

标准库具体实现
```rust
&#47;&#47; Returns an iterator over the chars of a string slice.
pub fn chars(&amp;self) -&gt; Chars&lt;&#39;_&gt;

&#47;&#47; Converts the given value to a String.
fn to_string(&amp;self) -&gt; String
```</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e6/58/a0f74927.jpg" width="30px"><span>gnu</span> 👍（10） 💬（1）<div>lifetime1: 
返回的引用是在 lifetime1 里被分配，lifetime1 结束后引用就被回收，所以错误。
改为转成 string 后返回。
```
fn lifetime1() -&gt; String {
    let name = &quot;Tyr&quot;.to_string();
    name[1..].to_string()
}
```


lifetime2:
函数参数是 String，编译器无法通过参数确定返回值 &amp;str 的生命周期。
修改为
```
fn lifetime2(name: &amp;String) -&gt; &amp;str {
    &amp;name[1..]
}
```

lifetime3:
返回 Chars 类型的生命周期与参数 name 关联，所以正确。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（6） 💬（2）<div>老师，关于智能指针一些问题：
数据放在堆上，返回指针给栈上的结构体
智能指针有个特点，*解耦到原型，&amp;*就是获取数据的引用，单&amp;栈上结构体的地址
*因为会解耦出原型，所以原数据是否实现copy trait，否则会move，智能指针就没有所有权了</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/02/22/19585900.jpg" width="30px"><span>彭亚伦</span> 👍（5） 💬（1）<div>关于String 和 &amp;str相关的各种问题,  我的经验, 一个核心原因是因为 String 实现了Deref&lt;Target = str&gt;,  String和&amp;str是通过这个Deref Trait建立了互换的关系; 

这样做带来了很多便利, 同时也有个side effect, 就是当参数要求是 &amp;str 时, 实参可能是&amp;str也可能是&amp;String, 而两者的生命周期明显是不一样的, 于是就产生了各种看似比较难以琢磨的问题.</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/74/d4/38d813f0.jpg" width="30px"><span>Kerry</span> 👍（3） 💬（1）<div>例子一：

1. &amp;str生命周期不明确
2. 返回了局部函数拥有所有权的引用，也是生命周期问题

可改为：

fn lifetime1() -&gt; &amp;&#39;static str { 
    let name = &quot;Tyr&quot;;
    &amp;name[1..]
}

例子二：

函数参数不是引用类型，而且String没有实现Copy Trait，传参的时候会把形参的所有权给到实参，这时候跟例子一是一样的。解决办法是把形参定义为引用类型，如&amp;str（&amp;String也不是不行）:

fn lifetime2(name: &amp;str) -&gt; &amp;str { 
    &amp;name[1..]
}

注意这里例子二不用指定返回值的生命周期，因为编译器可以从参数列表自动推断。

例子三：

Chars是字符串切片迭代器，生命周期与&amp;str是一致的，这一点可以从签名中看出：

&#47;&#47; std::str::chars
pub fn chars(&amp;self) -&gt; Chars&lt;&#39;_&gt;

&#47;&#47; std::str::Chars
pub struct Chars&lt;&#39;a&gt; {
    pub(super) iter: slice::Iter&lt;&#39;a, u8&gt;,
}</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（3） 💬（1）<div>比较简单的问题，第一个 name 在函数里面创建的 String，函数返回时就释放掉了，这是最直白的悬垂引用。第二个 name 是从调用者 move 过来的 String，进入该函数，所有权就归函数了，返回时 name 也将被释放。第三个 name 不用加生命周期标注可以正常工作，参数是引用，返回的数据与该参数的生命周期相同，没有问题，可以编译通过。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/e9/da5c0203.jpg" width="30px"><span>亚伦碎语</span> 👍（2） 💬（1）<div>对&amp;str 和 &amp;String的区别，更新一点：
String可以动态的调整内存大小。 str不能resize. 
&amp;str直接是指到了String存储的引用，&amp;String是对于String内存对象的引用。
参考：
https:&#47;&#47;users.rust-lang.org&#47;t&#47;whats-the-difference-between-string-and-str&#47;10177&#47;8</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/4a/30cf63db.jpg" width="30px"><span>丁卯</span> 👍（1） 💬（1）<div>to_owned() 什么意思？</div>2021-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（1） 💬（1）<div>老师，String，Vec算是智能指针吗？*String解除str，然后&amp;*String就是&amp;str了，Box::new()好像也可以这样用，Box::new(String::new)这样的使用，内存发生了什么变化啊</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/c3/ed5881c6.jpg" width="30px"><span>手机失联户</span> 👍（0） 💬（1）<div>老师，我看课程里没有提到rust宏相关的知识点，请问后续会讲这个吗？因为有些rust项目，比如tokio都会用到宏，导致代码不是很容易懂，老师能不能后续专门出一期讲一下。</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/19/70/7dbf25dc.jpg" width="30px"><span>mobus</span> 👍（0） 💬（1）<div>老师，有没有办法快速提取 枚举值？比如jsonrpc request ，为了匹配最终请求值，代码膨胀的太厉害了</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/25/c6/5b3ddf17.jpg" width="30px"><span>活着</span> 👍（0） 💬（1）<div>老师辛苦了，课程非常好👍</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/e9/da5c0203.jpg" width="30px"><span>亚伦碎语</span> 👍（0） 💬（1）<div>use std::str::Chars;

&#47;&#47; 错误，为什么？
&#47;&#47; name 在lifetime1 的block下就会被drop掉，所以返回&amp;str是不对
fn lifetime1() -&gt; String {
    let name = &quot;Tyr&quot;.to_string();
    name[1..].to_string()
}

&#47;&#47; 错误，为什么？
&#47;&#47; name类型变为String, ownership改变，但是返回是引用，block结束会被drop掉。可以讲入参改为引用。
fn lifetime2(name: &amp;String) -&gt; &amp;str {
    &amp;name[1..]
}

&#47;&#47; 正确，为什么？
&#47;&#47; 默认和参数一样的生命周期
fn lifetime3(name: &amp;str) -&gt; Chars {
    name.chars()
}</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>某些情景下带环的结构可以用Arena实现，比如typed_arena，用的时候不管释放，用完了一起释放。</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（0） 💬（1）<div>假如 泛型T约束需要实现AsRef trait, str 已经实现AsRef tarit,那么&amp;str符合这个泛型参数吗?</div>2021-09-19</li><br/><li><img src="" width="30px"><span>大哉乾元</span> 👍（0） 💬（1）<div>请教老师一个问题，关于文件操作的相对路径，如果是先编译再执行，rust会以可执行文件所在目录作为当前目录进行文件操作，如果直接cargo run的话则是以源文件目录作为相对目录执行，有办法统一起来么？</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/61/8f7fca5b.jpg" width="30px"><span>史双龙</span> 👍（0） 💬（2）<div>在用rust重新撸leetcode，真痛苦。</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（0） 💬（1）<div>打卡 真的是愚昧之巅了 需要重头再来了</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e4/a1/178387da.jpg" width="30px"><span>25ma</span> 👍（0） 💬（1）<div>1.返回是一个&amp;str,但是name的生命周期在函数执行结束就已经drop掉了，所以会造成悬垂指针的问题
2.同样也是犯规，一个&amp;str,不同的地方是当name这个不可变变量传递进函数lifttime2的时候已经将值move,然而这时再返回一个&amp;str,同样也会造成悬垂指针的问题</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0a/c8/dae4a360.jpg" width="30px"><span>Do</span> 👍（0） 💬（1）<div>太慢了</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/a2/c30ac459.jpg" width="30px"><span>hughieyu</span> 👍（0） 💬（1）<div>1. name drop了
2. name drop了
3. name的内存数据拷贝并转换到了一个新的拥有所有权的对象中</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/96/ea51844f.jpg" width="30px"><span>Frère Jac</span> 👍（1） 💬（0）<div>我知道 cargo build 有 --offline  选项，
也知道有 cargo fetch 预下载依赖，
问题是比如我 日常开发在 mac 上进行，
但是最终交付要在公司内网 Linux 服务器进行构件交付，不能连接外网，我该如何操作才能把需要的依赖收集好，然后 copy 至目标构件服务器进行构件呢？</div>2023-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/73/50/791d0f5e.jpg" width="30px"><span>我还是新人</span> 👍（0） 💬（0）<div>思考题
 fn lifetime1() -&gt; &amp;str  这个name 握有值的所有权， 在函数执行完后就被销毁了，返回它的引用自然没有意义。
fn lifetime2(name: String) -&gt; &amp;str 同样的道理，传进来的name也有所有权，也会在函数执行完后被销毁。
fn lifetime3(name: &amp;str) -&gt; Chars  这个函数传进的是引用，没有所有权，所以函数执行完不会销毁值。同时可以将生成&amp;str通过copy给传递出去。
不过我有个新的问题。对于那些生成fn test() -&gt; &#39;static str这样的返回static这样的函数，生命周期与进程相同，会不会导致内存泄漏呢？</div>2024-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/84/e51e1db3.jpg" width="30px"><span>木鸢</span> 👍（0） 💬（1）<div>还没看到这里就体会到陈老师说的愚昧之颠了，rust的大量简写就当是语言特色来看了，到了所有权、rc、arc、生命周期这些章节，看完理论再对照代码就蒙圈了，代码完全看不懂啊！
vec!和直接定义切片有什么区别？
String::from定义的字符串和直接双引号定义的结果是一回事吗？
生命周期标示是 &#39; 还是 &#39;a-z ，参数里面中定义，和外界传参时候定义有区别吗？
语法 spawn（|| {}）到底表示什么意思？还是说这个写法是spawn独有的呢？

肯定是我太白，太先去看看rust基础语法再来从新看，润了润了

PS：陈老师讲得非常透彻，计算机基础，rust编程思想都娓娓道来，有rust经验的同学肯定会很有共鸣，评论区的精华帖也能看到</div>2022-10-09</li><br/>
</ul>