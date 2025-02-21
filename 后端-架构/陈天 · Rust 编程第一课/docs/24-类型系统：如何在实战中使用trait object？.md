你好，我是陈天。

今天我们来看看 trait object 是如何在实战中使用的。

照例先来回顾一下 trait object。当我们在运行时想让某个具体类型，只表现出某个 trait 的行为，可以通过将其赋值给一个 dyn T，无论是 &amp;dyn T，还是 Box&lt;dyn T&gt;，还是 Arc&lt;dyn T&gt;，都可以，这里，T 是当前数据类型实现的某个 trait。此时，原有的类型被抹去，Rust 会创建一个 trait object，并为其分配满足该 trait 的 vtable。

你可以再阅读一下[第 13 讲](https://time.geekbang.org/column/article/420028)的这个图，来回顾 trait object 是怎么回事：  
![](https://static001.geekbang.org/resource/image/49/1d/4900097edab0yye11233e14ef857be1d.jpg?wh=2248x1370)

在编译 dyn T 时，Rust 会为使用了 trait object 类型的 trait 实现，生成相应的 vtable，放在可执行文件中（一般在 TEXT 或 RODATA 段）：  
![](https://static001.geekbang.org/resource/image/9d/5e/9ddeafee9740e891f6bf9c1584e6905e.jpg?wh=2389x1738)

这样，当 trait object 调用 trait 的方法时，它会先从 vptr 中找到对应的 vtable，进而找到对应的方法来执行。

使用 trait object 的好处是，**当在某个上下文中需要满足某个 trait 的类型，且这样的类型可能有很多，当前上下文无法确定会得到哪一个类型时，我们可以用 trait object 来统一处理行为**。和泛型参数一样，trait object 也是一种延迟绑定，它让决策可以延迟到运行时，从而得到最大的灵活性。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（5） 💬（1）<div>我自己的机器, 用一个unit type来排除struct initialization带来的cost:

```
struct Dummy();

impl Executor for Dummy {
    fn run(&amp;self) -&gt; Result&lt;Option&lt;i32&gt;, BoxedError&gt; {
        Ok(Some(0))
    }
}
```

generics: 243.34 ps
trait object: 2.38 ns
boxed object: 3.67ns

trait object调用时间是generics的9.78倍...居然差这么多!!

不知道为啥box还是比trait object慢; 按理说, unit type是ZST, 没有大小, 应该不涉及heap memory allocation的...速度应该和trait object一样...但实际测出来还是挺大差距的...

</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/3a/60/6ab05338.jpg" width="30px"><span>大汉十三将</span> 👍（2） 💬（1）<div>唉[苦涩] 看不懂了</div>2023-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>最近在优化 Go 写的即时对战服务，的确堆内存的分配是消耗性能的一大杀手，泛型的消耗相比堆内存的消耗，应该是可以忽略的。但在高频次的调用上，如果可以优化掉不使用泛型，代码理解与维护上没有问题，也还是尽可能避免使用泛型吧。</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/17/2d/b7614553.jpg" width="30px"><span>Bruce</span> 👍（0） 💬（1）<div>有见到trait中，除了关联类型type，还有用const定义的占位符，可以讲讲具体的吗</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（0） 💬（1）<div>实现部分需要修改的并不多，把StrategyFn的泛型参数去掉，把reader声明为可变，并在调用函数时传入BufReader的可变引用即可。
我个人觉得修改之后没有带来什么好处，之前的泛型参数并不复杂，而且反而觉得实现时的 Read Write trait bounds让代码读起来很清晰 😂</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（1） 💬（0）<div>思考题：实现上修改的地方并不多，只需修改 StrategyFn、match_with 和 default_strategy 的函数签名，将其中的泛型参数去除，然后在调用的地方传入相关的引用即可。比较上，rgrep 的泛型参数还是比较简单直观的，代码也并不会很臃肿，这里用 dynamic trait object 来替换没什么必要。


在泛型参数的版本中，传递进来的 BufReader&lt;R&gt; 不需要是可变的，而改用 trait object 就需要使用 &amp;mut dyn BufRead 而不能是 &amp;dyn BufRead？ 我尝试将 mut 关键字去掉，在调用 lines 方法时，产生了 “the `lines` method cannot be invoked on a trait object, this has a `Sized` requirement”。我查阅了 rust 文档，BufRead 中 lines 函数的实现为  


fn lines(self) -&gt; Lines&lt;Self&gt; where Self: Sized, { Lines { buf: self } }


因此，这里想向老师请教两个问题：

1. 为什么 &amp;mut dyn BufRead 对象能够调用 lines 方法，而 &amp;dyn BufRead 则不行？
2. 根据第十三讲中所说，只有满足对象安全的前提下才能调用 trait object 的方法，而满足对象安全的情况之一，是不允许携带泛型参数，因为 Rust 里带泛型的类型在编译时会做单态化，而 trait object 是运行时的产物，两者不能兼容。那这里的 lines 方法返回值为 Line&lt;Self&gt;，其中 &lt;Self&gt; 应该算是泛型参数吧，那为什么还能调用呢？
</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f8/15/2724d7ec.jpg" width="30px"><span>A.Y.</span> 👍（1） 💬（0）<div>老师好，我这边想咨询一个问题：如果使用trait object将一个闭包放入了map中，然后需要在其他的线程中取出这个闭包执行，该怎么做呢？最近测试了一下，发现编译器提示错误，好像闭包的 trait object并没有实现Sync</div>2022-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/fe/2f5d1bb7.jpg" width="30px"><span>jimmy</span> 👍（0） 💬（0）<div>We’ve mentioned that, in Rust, we refrain from calling structs and enums “objects” to distinguish them from other languages’ objects. In a struct or enum, the data in the struct fields and the behavior in impl blocks are separated, whereas in other languages, the data and behavior combined into one concept is often labeled an object. However, trait objects are more like objects in other languages in the sense that they combine data and behavior. But trait objects differ from traditional objects in that we can’t add data to a trait object. Trait objects aren’t as generally useful as objects in other languages: their specific purpose is to allow abstraction across common behavior.
  --from《The Rust Programming Language》：5. Using Trait Objects That Allow for Values of Different Types</div>2024-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（0） 💬（0）<div>二刷课程了，朋友们，有没有Rust岗位推荐呢</div>2023-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（0）<div>重新读trait object</div>2022-04-09</li><br/>
</ul>