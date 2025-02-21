你好，我是Mike，今天我们继续学习trait相关知识。

回顾一下我们上一节课中类型参数出现的地方。

- 用 trait 对 Ｔ 作类型空间的约束，比如`T: TraitA`。
- blanket implementation 时的 T，比如 `impl<T: TraitB> TraitA for T {}`。
- 函数里的 T 参数，比如 `fn doit<T>(a: T) {}`。

你要注意区分不同位置的 T。它的基础意义都是类型参数，但是放在不同的位置其侧重的意义有所不同。

- `T: TraitA` 里的T表示类型参数，强调“参数”，使用TraitA来削减它的类型空间。
- `impl<T: TraitB> TraitA for T {}` 末尾的T更强调类型参数的“类型”部分，为某些类型实现 TraitA。
- `doit<T>(a: T) {}` 中第二个T表示某种类型，更强调类型参数的“类型”部分。

这节课我们要讲的是另外一个东西，它里面也带T参数。我们一起来看一下，它与之前这几种形式有什么不同。

## trait上带类型参数

trait上也是可以带类型参数的，形式像下面这样：

```plain
trait TraitA<T> {}
```

表示这个trait里面的函数或方法，可能会用到这个类型参数。在定义trait的时候，还没确定这个类型参数的具体类型。要等到impl甚至使用类型方法的时候，才会具体化这个T的具体类型。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（18） 💬（2）<div>rust生命周期的独特设计，导致了该语言需要设计一些处理方式应对特殊情况，比如生命周期的标注（主要是给编译器进行代码处理时的提示）。事实上，我们在日常开发中应该避免一些陷入复杂情况的方式：比如，传入参数都用引用（borrow），传出结果都应该是owner。rust也为我们提供了处理各种情况的工具。所以，一般来说，我们应该在传入参数的时候用&amp;dyn T，传出结果用Box&lt;dyn T&gt;。</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（6） 💬（1）<div>&amp;dyn TraitA没有所有权，而Box&lt;dyn TraitA&gt;有所有权。</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（6） 💬（2）<div>关联类型之所以要单独设计，因为编译器可以通过输入判断具体类型，而无法推断出输出类型，所以，输出的类型需要明确指定</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（4） 💬（1）<div>这篇文章真不错，值得反复看。慢就是快，学习不能浮躁，妄想速成，一知半解反而给后边的学习造成很多障碍。</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（2） 💬（4）<div>最后安全的trait object听的似懂非懂，为什么是安全的，为什么是不安全的？希望具体讲下原因</div>2023-11-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（1） 💬（1）<div>笔记：



trait 可以带泛型 generics

trait 关联类型 associated type 跟泛型类似， 但必须在 impl 的时候就具化

泛型就随便啥时候具化都行了





`fn doit(i: u32) -&gt; impl TraitA` =&gt; 某一种实现了 TraitA 的类型

`fn doit(i: u32) -&gt; Box&lt;dyn TraitA&gt;` =&gt; 多种实现了 TraitA 的类型



前两次刷 rbe 和 rustbook 的时候都没反应过来为啥叫 trait object, 看这课终于明白了， 原来 trait obejct 指的是 typeOuter 的 OuterSizedObj, 然后这个 OuterSizedObj 里面可以包裹各种实现了 traitA 的 type 对应 obj

还是得多刷点儿资料， 多看对于同一概念的不同表达， 明白的快



</div>2023-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（1） 💬（1）<div>思考题： &amp;dyn traitA 和 Box&lt;dyn traitA&gt; 严格来说都是指向 actual object 的指针， 只不过 `&amp;` 叫做引用， `Box` 叫做智能指针, 这俩都是固定大小的， 所以都能用在 trait object

区别：
&amp;dyn traitA 是一个不拿所有权的指针 =&gt; 所以经常用在参数里
Box&lt;dyn traitA&gt; 是拥有内部数据所有权的指针 =&gt; 所以经常用在返回值里， 参数里应该也能用


</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/36/f6/7945e06f.jpg" width="30px"><span>李诗涛</span> 👍（0） 💬（1）<div>老师老师，我有一个问题。就是您说impl trait目前有两个使用的地方，分别是函数入参和返回。但给出的例子里，在入参使用impl trait时编译器会自动展开。但在出返回值使用impl trait时，若是返回了不同的类型却会报错。这是怎么理解？</div>2024-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（0） 💬（1）<div>基础部分非常详细，建议老师可以深入讲一下trait object的内存相关知识，以及trait object会丢失本身类型信息这些注意点。</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（1）<div>思考题：&amp;dyn TraitA 是借用，Box&lt;dyn TraitA&gt; 会转移所有权。

通过下面的程序可以测试出来：

fn doit3(t1: &amp;dyn TraitA, t2: Box&lt;dyn TraitA&gt;) {
    println!(&quot;{:?}&quot;, t1);
    println!(&quot;{:?}&quot;, t2)
}

fn main() {
    let a = AType;
    let b = BType;
    doit3(&amp;a, Box::new(b));
    println!(&quot;{:?}&quot;, a);
    println!(&quot;{:?}&quot;, b);
}

输出：

error[E0382]: borrow of moved value: `b`
  --&gt; examples&#47;trait_object.rs:29:22
   |
26 |     let b = BType;
   |         - move occurs because `b` has type `BType`, which does not implement the `Copy` trait
27 |     doit3(&amp;a, Box::new(b));
   |                        - value moved here
28 |     println!(&quot;{:?}&quot;, a);
29 |     println!(&quot;{:?}&quot;, b);
   |                      ^ value borrowed here after move
</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/85/c0cf6544.jpg" width="30px"><span>老大</span> 👍（0） 💬（1）<div>不要在 trait 里面定义构造函数，比如 new 这种返回 Self 的关联函数。你可以发现，确实在整个 Rust 生态中都没有将构造函数定义在 trait 中的习惯。
这句话，在上面的例子中 确实有在trait中定义了new函数返回self的。怎么就感觉有冲突呢？</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/f1/bd61dbb1.jpg" width="30px"><span>Ransang</span> 👍（0） 💬（1）<div>struct Atype;
struct Btype;
struct Ctype;

trait TraitA {}

impl TraitA for Atype {}
impl TraitA for Btype {}
impl TraitA for Ctype {}

fn doit(i: u32) -&gt; &amp;&#39;static dyn TraitA { &#47;&#47; 注意这里的返回类型换成了 dyn TraitA
  if i == 0 {
    return &amp;Atype
  } else if i == 1 {
    return &amp;Btype
  } else {
    return &amp;Ctype
  }
}
老师 我这种也能通过编译 ，我一开始尝试用&amp;dyn TraitA没通过编译，小助手报错error[E0106]: missing lifetime specifier并提示我用&amp;&#39;static dyn TraitA，在字符串那节您提过 &#39;static 表示这个引用可以贯穿整个程序的生命周期，想问下您这段代码为什么加了&#39;static就可以通过编译，以及这个生命周期的概念又是怎么回事，谢谢了</div>2023-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/7c/f8f38ad0.jpg" width="30px"><span>可爱的小奶狗</span> 👍（0） 💬（2）<div>老师，actix-web-4.4.0 的router.rs中的to方法： pub fn to&lt;F, Args&gt;(mut self, handler: F) -&gt; Self ，这个handler为什么可以接收一个async函数作为参数(async函数并未实现F trait的方法)呢？实在想不明白。</div>2023-11-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（0） 💬（1）<div>&amp;dyn TraitA 是实现了TraitA的类型的对象的引用，Box&lt;dyn Trait&gt;则是获取了该对象的所有权。</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ff/d8/d48d6088.jpg" width="30px"><span>一个人旅行</span> 👍（0） 💬（1）<div>1. &amp;dyn TraitA 是一个引用，引用指向实现了TraitA特征的具体类型，没有这个具体类型的所有权，相当于借用。
2. Box&lt;dyn TraitA&gt; 是一个智能指针，将实现了TraitA特征的具体类型保存在堆上，并且拥有这个具体类型的所有权。</div>2023-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/8d/13/943a4759.jpg" width="30px"><span>:-O</span> 👍（0） 💬（0）<div>很棒的文章，我看懂trait了</div>2024-12-10</li><br/>
</ul>