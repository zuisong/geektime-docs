你好，我是Mike。今天我们来一起学习trait。

trait 在Rust中非常重要。如果说所有权是Rust中的九阳神功（内功护体），那么类型系统（types + trait）就是Rust中的降龙十八掌，学好了便如摧枯拉朽般解决问题。另外一方面，如果把Rust比作一个AI人的话，那么所有权相当于Rust的心脏，类型 + trait相当于这个AI人的大脑。

![图片](https://static001.geekbang.org/resource/image/c0/28/c05e31106c4f880f5ce29cdc8f1a8128.png?wh=1920x1349)

好了，我就不卖关子了。前面我们已经学习了所有权，现在我们来了解一下这个trait到底是什么。

注：所有权是这门课程的主线，会一直贯穿到最后。

## trait是什么？

trait用中文来讲就是特征，但是我倾向于不翻译。因为 trait 本身很简单，它就是一个标记（marker 或 tag）而已。比如 `trait TraitA {}` 就定义了一个trait，TraitA。

只不过这个标记被用在特定的地方，也就是类型参数的后面，用来限定（bound）这个类型参数可能的类型范围。所以trait往往是跟类型参数结合起来使用的。比如 `T: TraitA` 就是使用 TraitA 对类型参数T进行限制。

这么讲起来比较抽象，我们下面举例说明。

### trait是一种约束

我们先回忆一下[第 7 讲](https://time.geekbang.org/column/article/722240)的一个例子。

```plain
struct Point<T> {
    x: T,
    y: T,
}

fn print<T: std::fmt::Display>(p: Point<T>) {
    println!("Point {}, {}", p.x, p.y);
}

fn main() {
    let p = Point {x: 10, y: 20};
    print(p);

    let p = Point {x: 10.2, y: 20.4};
    print(p);
}
// 输出 
Point 10, 20
Point 10.2, 20.4
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/5b/4e/8e1f699e.jpg" width="30px"><span>Mike Tang</span> 👍（11） 💬（1）<div>神说，众生平等。Rust说，众trait平等。</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（30） 💬（5）<div>trait 的依赖：小明要听从数学老师，语文老师，英语老师的话。老师之间是平等关系，多个依赖平等，最小依赖选择自己喜欢滴功能。
OOP 继承：小明要听他爸，他爷爷，他曾祖父的话。继承之间存在父子关系，继承过来一堆破属性和方法，也许根本不是自己想要滴，还要负重前行。</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（7） 💬（1）<div>在语法层面实践了组合优于继承。</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（3） 💬（1）<div>看到supertrait 和 subtrait， Shape 和 Circle 的时候， 的确联想到继承了，不过作者强调平等，那就打消了这个念头</div>2024-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1d/b5/d843bef9.jpg" width="30px"><span>cluski</span> 👍（2） 💬（1）<div>个人理解，trait很像Java中的interface。Java的interface可以作为某种能力的抽象，并且在泛型的使用中，可以起到限制的作用。
Java、C++等OOP语言中的继承个人感觉更多是在强调is-a这个概念。例如，男人是一个人，鸽子是一个鸟这类。与Rust的trait更加强调的一种能力和约束。</div>2023-11-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（1） 💬（1）<div>笔记

一般我们说关联类型 &#47; associated types 的时候， 说的是 trait 底下的 type

关联类型就是跟着 trait 走的泛型

至于啥时候关联类型要具化 &#47; 单态化 &#47; 具体写明白是啥？

得在 impl trait for typeA 的时候写清楚



一般说 A 有 trait bound， 意思就是这个 A 必须实现某个 trait

我们不仅可以搞 trait bound, 有 trait bound 之后在 where clause 里还可以搞 trait type bound：

`T: trait A, T::typeB: Debug + PartialEq`



为啥调用 trait 方法还需要 use trait?

因为 rust 不会大海捞针遍历所有 trait 找方法， 你得先指定在哪儿找

</div>2023-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（1） 💬（1）<div>既然关联类型作为占位符，那为什么这样会报错呢，按我理解理占位符应该不需要事先声明
pub trait Sport {
    type SportType;

    fn play(&amp;self, st: SportType);
}

fn main() {}


error[E0412]: cannot find type `SportType` in this scope
 --&gt; src\main.rs:4:24
  |
4 |     fn play(&amp;self, st: SportType);
  |                        ^^^^^^^^^ help: you might have meant to use the associated type: `Self::SportType`
</div>2023-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d4/2e/d478a412.jpg" width="30px"><span>duwoodly</span> 👍（1） 💬（1）<div>CPP的继承，子类会继承父类的属性和方法，子类可以重写父类的方法。 继承引起的耦合性很强。 所以新产生的语言都不再支持继承，像go和rust使用组合，降低了耦合性。
Rust 的trait 是一种约束，也是一种能力，避免了继承的强耦合，又提供了灵活性。</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/92/b5/98062fbf.jpg" width="30px"><span>王晓宇</span> 👍（0） 💬（1）<div>老师，在T上使用关联类型那个示例编译不通过
trait TraitA {
  type Mytype;
}

fn doit&lt;T: TraitA&gt;(a: T::Mytype) {}  &#47;&#47; 这里在函数中使用了关联类型

struct TypeA;
impl TraitA for TypeA {
  type Mytype = String;  &#47;&#47; 具化关联类型为String
}

fn main() {
  doit::&lt;TypeA&gt;(&quot;abc&quot;.to_string());  &#47;&#47; 给Rustc小助手喂信息：T具化为TypeA
}</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（1）<div>有没有入门项目来练练手，
看完就忘了，不上手的话</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/2e/d8/7beb49a4.jpg" width="30px"><span>飞了的鸭子被煮了</span> 👍（0） 💬（1）<div>trait 不需要考虑层级关系，感觉类型的约束更加原子化了，被消费时不需要考虑那么多的耦合。</div>2024-01-22</li><br/><li><img src="" width="30px"><span>千回百转无劫山</span> 👍（0） 💬（1）<div>从python过来的，只能说打开了新世界的大门</div>2023-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>思考题（我从 python 来的， cpp 和 java 没学过）

OOP

class 里有各种方法， 搞个子类就可以对基类进行各种修改

定义个 class, class 里有各种方法（包括 static method 啥的）

大部分情况是一个树形结构



面向 trait bound 编程

trait 类似于 OOP 里搞一个标准基类， 然后来回继承， 不同点在于更灵活

或者类似于 python3 里的 mixin（这玩意我没怎么玩过， 不熟， 但看过同事写的代码）， 搞个 must implement 的 abstract method 感觉也差不多

引用来引用去， 飞来飞去~



这种思考题没啥感觉， 反正我也不会写， 随便叨叨， 等全都刷一遍之后可能会有别的感想</div>2023-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（2）<div>我记得 trait 底下定义的函数里， 有 self 参数的叫方法（method, called on instance）， 没 self 参数的才叫 关联函数（associated function, called on type)?
=================
刚才查了下， duckduckgo 搜出来的 rust associated function 跟我记得一样， 区分 method 和 associated function， 但 Rust By Practice (RBP) 和 Rust By Example (RBE) 说的不一样...

RBP
https:&#47;&#47;practice.rs&#47;method.html
=&gt; &quot;All functions defined within an impl block are called associated functions because they’re associated with the type named after the impl.&quot; 所有在 impl 底下的函数都能叫做 associated functions

RBE
https:&#47;&#47;doc.rust-lang.org&#47;rust-by-example&#47;fn&#47;methods.html
=&gt; &quot;Some functions are connected to a particular type. These come in two forms: associated functions, and methods.&quot;
</div>2023-12-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erEHTaQDkWqEYib9iabib8rACYpSFBHTPFmgicUKaib79MB6VIxNwiajHUS8kYFEKCGOjpibf0dibhIjqhfzg/132" width="30px"><span>plh</span> 👍（0） 💬（1）<div>老师你好: 原文 [因为同一个 trait 只能实现一次到某个类型上。]  这个 &quot;某个类型&quot; 怎么理解? 
比如: 标准库上有 Option 上面 就有这么3个方法: 感觉这个有点迷惑?  

impl&lt;T&gt; IntoIterator for Option&lt;T&gt;
impl&lt;&#39;a, T&gt; IntoIterator for &amp;&#39;a Option&lt;T&gt;
impl&lt;&#39;a, T&gt; IntoIterator for &amp;&#39;a mut Option&lt;T&gt;




</div>2023-11-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ4reATXtqhQ26vWXhiaZUEF9W1E0ZEqibrxxzR7NrlGwjrCZeLvF2HnL8jFjGXaFtN1vBTSia6492g/132" width="30px"><span>javpower</span> 👍（0） 💬（1）<div>trait 类似Java中的接口
范型约束类似Java中的&lt;? extends 接口&gt;</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/22/403a340a.jpg" width="30px"><span>unistart</span> 👍（0） 💬（2）<div>最后的Blanket Implementation那部分有点没看明白，有大佬能指点一下么

问题一：文稿上修改后的代码和之后解释说明貌似对不上，文稿中说`因为 u32 并没有被 TraitB 约束，所以它不满足第 4 行的 blanket implementation。因此就不算重复实现`。但是修改后的代码中是保留的impl TraitA for u32 {}而不是impl TraitB for u32 {}。

问题二：我将有问题的代码复制到rus playground中并尝试修改，发现注释掉问题代码中的impl TraitA for u32 {}或者impl TraitB for u32 {}貌似都不会报错，没明白这是什么意思。

问题三：关于impl&lt;T: TraitB&gt; TraitA for T {}这句代码的理解，是不是为T类型实现TraitA，同时对T类型做了trait约束为TraitB，之后如果T类型实现了TraitB，那么自然就有了TraitA的能力

trait TraitA {
    fn test(&amp;self) {
        println!(&quot;TraitA::test&quot;)
    }
}

trait TraitB {
    fn some(&amp;self) {
        println!(&quot;TraitB::some&quot;)
    }
}

impl&lt;T: TraitB&gt; TraitA for T {}

impl TraitB for u32 {}
&#47;&#47; impl TraitA for u32 {}

impl TraitB for f32 {}

fn main() {
    1u32.test(); &#47;&#47; 输出 TraitA::test
    1u32.some(); &#47;&#47; 输出 TraitB::some
    
    1.0f32.test(); &#47;&#47; 输出：TraitA::test
    1.0f32.some(); &#47;&#47; 输出：TraitB::some
}


</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/43/d2/71b06883.jpg" width="30px"><span>踩着太阳看日出</span> 👍（0） 💬（1）<div>trait Shape {
    fn play(&amp;self) {    &#47;&#47; 定义了play()方法
        println!(&quot;1&quot;);
    }
}
trait Circle : Shape {
    fn play(&amp;self) {    &#47;&#47; 也定义了play()方法
        println!(&quot;2&quot;);
    }
}
struct A;
impl Shape for A {}
impl Circle for A {}

impl A {
    fn play(&amp;self) {    &#47;&#47; 又直接在A上实现了play()方法
        println!(&quot;3&quot;);
    }
}

fn main() {
    let a = A;
    a.play();    &#47;&#47; 调用类型A上实现的play()方法
    &lt;A as Circle&gt;::play(&amp;a);  &#47;&#47; 调用trait Circle上定义的play()方法
    &lt;A as Shape&gt;::play(&amp;a);   &#47;&#47; 调用trait Shape上定义的play()方法

    (&amp;a as &amp;dyn Shape).play();
    Circle::play(&amp;a as &amp;dyn Circle);
    Circle::play(&amp;a);

    A::play(&amp;a);
    (&amp;a as &amp;dyn Circle).play();
}

error[E0034]: multiple applicable items in scope
  --&gt; 07_ownership&#47;src&#47;mytest.rs:32:25
   |
32 |     (&amp;a as &amp;dyn Circle).play();
   |                         ^^^^ multiple `play` found
   |
note: candidate #1 is defined in the trait `Shape`
  --&gt; 07_ownership&#47;src&#47;mytest.rs:2:5
   |
2  |     fn play(&amp;self) {    &#47;&#47; 定义了play()方法
   |     ^^^^^^^^^^^^^^
note: candidate #2 is defined in the trait `Circle`
  --&gt; 07_ownership&#47;src&#47;mytest.rs:7:5
   |
7  |     fn play(&amp;self) {    &#47;&#47; 也定义了play()方法
   |     ^^^^^^^^^^^^^^
help: disambiguate the method for candidate #1
   |
32 |     Shape::play(&amp;(&amp;a as &amp;dyn Circle));
   |     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
help: disambiguate the method for candidate #2
   |
32 |     Circle::play(&amp;(&amp;a as &amp;dyn Circle));
   |     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

提示多个方法，感觉还是有点像集成的意思，老师解释下</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（1）<div>Rust 的 trait 更注重行为的抽象和方法的契约，而不涉及数据的继承。
OOP 的继承涉及到类的层次结构，子类继承父类的属性和方法。</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/30/55488a4c.jpg" width="30px"><span>李志勇(Leo)</span> 👍（0） 💬（1）<div>很不一样的视角【对泛型类型的约束】，
一直以interface的概念的去理解，写代码的时候感觉很有压力。</div>2023-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/0a/ac/81053dda.jpg" width="30px"><span>明天</span> 👍（0） 💬（1）<div>```rust
pub fn trait_fn() {
    trait Sport {
        &#47;&#47; 实例方法
        fn play(&amp;self) {
            println!(&quot;this is a default method&quot;);
        }
        fn play_mut(&amp;mut self);
        fn play_own(self);
        &#47;&#47; 关联函数
        fn play_some() -&gt; String {
            &quot;this is a default method&quot;.to_string()
        }
    }

    struct FootBall;

    impl Sport for FootBall {
        fn play(&amp;self) {
            println!(&quot;this is a new method&quot;);
        }

        fn play_mut(&amp;mut self) {}

        fn play_own(self) {}

        fn play_some() -&gt; String {
            &quot;this is a new method&quot;.to_string()
        }
    }

    let s1 = FootBall::play_some();
    let s2 = &lt;FootBall as Sport&gt;::play_some();

    println!(&quot;s1 = {}&quot;, s1);
    println!(&quot;s2 = {}&quot;, s2);
}
```
请问老师， `let s2 = &lt;FootBall as Sport&gt;::play_some();`这里调用的是FootBall中的play_some()方法吗，我这边试了一下， 都是FootBall中的paly_some()触发的</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/99/0d72321f.jpg" width="30px"><span>A0.何文祥</span> 👍（0） 💬（1）<div> typo：Dispaly -》 Display</div>2023-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（0） 💬（2）<div>听语音初学者完全跟不上，还是得细细看过文章才行</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/81/4c/e42bc9b8.jpg" width="30px"><span>啊Ray</span> 👍（0） 💬（1）<div>感觉关联类型那里看得一头雾水的。。能不能搞几个通俗易懂的例子讲解一下？</div>2023-11-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep7w8XNyxrp9fmSds4F1CUnDqVRUSyicsf3icLOeK5S11WybjqUM86TDz0LwJibSECD6w22umsGiamWXA/132" width="30px"><span>Geek_cbeb39</span> 👍（0） 💬（1）<div>大佬这个课之后会涉及到Rust&amp;webassmbly的内容吗</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a4/ee/b960a322.jpg" width="30px"><span>mihello</span> 👍（1） 💬（1）<div>我不是初学者了，已经用Rust写过千来行的小工具。不过始终还是没有一种通透感觉，看了这一章收获良多，有点醍醐灌顶。远远超越官方教程，官方教程真的太简陋了...
其实自己写还好，最怕看开源项目源码，如果没学透真的看不懂。看了老师的教程相信会大有进步。</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/3f/7d/f624fa69.jpg" width="30px"><span>当初莫相识</span> 👍（0） 💬（1）<div>这篇知识密度太高，学不懂了，学习rust太抽象了，很难用对比和知识迁移的方法进行学习</div>2024-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/6b/6c/3e80afaf.jpg" width="30px"><span>HappyHasson</span> 👍（0） 💬（1）<div>关联常量的一节里，`println!(&quot;{:?}&quot;,::LEN); ` 

这里为什么输出 12  ？  不是把 A 转为 TraitA 了吗？在C++的对象模型里 这里应该输出 10 。 这里的底层实现是什么 </div>2024-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（0）<div>trait TraitA {}
trait TraitB {}

impl&lt;T: TraitB&gt; TraitA for T {}

impl TraitA for u32 {}

最后一句应该是 impl TraitB for u32 {} 才对吗？</div>2024-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（0）<div>trait TraitA {}
trait TraitB {}

impl&lt;T: TraitB&gt; TraitA for T {}

impl TraitA for u32 {}

没想明白为什么这里u32 {}T {}

impl TraitA for u32 {}

没想明白为什么这里u32 {} 和 T {} 联系上了</div>2024-05-01</li><br/>
</ul>