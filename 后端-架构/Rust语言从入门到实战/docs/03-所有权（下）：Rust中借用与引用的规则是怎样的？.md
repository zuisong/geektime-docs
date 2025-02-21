你好，我是Mike。今天我们继续探讨Rust中所有权这一关键设计。

上节课我们了解了计算机内存结构知识，理解了Rust在内存资源管理上特立独行的设计——所有权，也知道了Rust准备采用所有权来重构整个软件体系。那么这节课我们继续学习所有权的相关内容——借用与引用，学完这节课我们就会对Rust语言的所有权方案有一个相对完整的认知了。

这节课我会用一些精心设计的示例，让你体会Rust引用的独特之处。

## 借用与引用

我们来复习一下上一节课最后一个例子。我们想在函数 `foo` 执行后继续使用字符串s1，我们通过把字符串的所有权转移出来，来达到我们的目的。

```plain
fn foo(s: String) -> String {
    println!("{s}");
    s
}

fn main() {
    let s1 = String::from("I am a superman.");
    let s1 = foo(s1);
    println!("{s1}");
}
```

这样可以是可以，不过很麻烦。一是会给程序员造成一些心智负担，还得想着把值传回来再继续使用。如果代码中到处都是所有权传来传去，会让代码显得相当冗余，毕竟很多时候函数返回值是要用作其他类型的返回的。为了解决这个问题，Rust引入了借用的概念。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/29/9e/15/e499fc69.jpg" width="30px"><span>Andylinge</span> 👍（22） 💬（2）<div>1. 不可变引用的作用域跨越了所有权变量的写入过程，意味着同一个作用域同时存在可变引用和不可变引用，编译器为了防止读取错误，不能通过编译。可以把a = 20放到引用之前，即可编译通过。
2. 可变引用如果可以Copy，就违反了可变引用不能同时存在的规则，因此只能Move.
跟唐老师学习我觉得我理解能力变强了，感谢唐老师的课程，扫清了很多基础的迷雾。</div>2023-10-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqrbHib1v0wPRVHxrFK2CPQQX8Wg3rRMPiaZ5teMKu5klT48yns6yo4krZsIqHskwdEsibVvQ3QB7CUQ/132" width="30px"><span>Geek_6fjt20</span> 👍（11） 💬（3）<div>rust完全模拟了现实世界中借的概念，a有一本书，b要用的时候向a借，b不能超出a的移动范围（作用域范围），因为怕借了不还跑路了。</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/00/a4a2065f.jpg" width="30px"><span>Michael</span> 👍（8） 💬（2）<div>想请问下下面这段代码，为什么变量b之前的mut是必须的，变量c之前不需要：

fn main() {
    let mut a1 = 10u32;
    let mut b = &amp;mut a1;
    *b = 20;

    let c = &amp;mut b;
    **c = 30;          &#47;&#47; 多级解引用操作

    println!(&quot;{c}&quot;);
}</div>2023-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ff/d8/d48d6088.jpg" width="30px"><span>一个人旅行</span> 👍（5） 💬（2）<div>问题1. 所有权型变量被借用时，不能对所有权型变量进行修改。
问题2. 同一时刻，所有权型变量只能有一个可变引用或多个不可变引用。如果复制，则会有多个不可变引用，违反了借用规则。</div>2023-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/eb/cf/8fa3dd5a.jpg" width="30px"><span>RobinH</span> 👍（3） 💬（1）<div>所有权 感觉像是一种 栈范围 在控制</div>2024-01-22</li><br/><li><img src="" width="30px"><span>Geek_c01211</span> 👍（2） 💬（2）<div>感觉讲的比较细，给了很多 case 去分析，很喜欢，但是想请教一个问题，为啥可变引用和不可变引用或者多个不可变引用的作用域之间不能重叠？如果编译器不对这一块做检查，会有啥样子的问题了，基于目前的例子，好像没有办法合理的解释为什么不能重叠</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（2） 💬（1）<div>1. 不可变引用的语义更像是“借一下这个值使用一下”，如果在不可变引用作用域结束之前，对所有权变量进行写入，那么这个借的“值”，就没有意义了，因为不确定是否跟想借的时候是一致的。

2. 如文中所说，可变引用的作用域不能交叉，如果采用 copy，则两份可变引用其实是互不影响的，即可以交叉，就产生矛盾了。</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（1）<div>想问下老师，下面这段代码中，s2 和 s3 分别是什么类型的变量（所有权型还是引用型？），引用算不算上一种特殊的资源（值）？变量 s3 对 s2 拥有所谓的“所有权”吗？

let mut s1 = &quot;Hello World&quot;.to_string();
let s2 = &amp;mut s1;
let s3 = s2;
println!(&quot;{s3}&quot;)</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ac/5c/bb67abe6.jpg" width="30px"><span>林子茗</span> 👍（1） 💬（1）<div>思考题1：因为这样会导致b的结果不一致，类似于数据库的不可重复读。
2：多个引用都能修改，可能会有并发问题，所以还是数据不一致的问题。</div>2024-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（1） 💬（2）<div>一句话总结：资源在借用期间不能被修改（包括定义可变借用）</div>2023-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/65/13/8654e7c9.jpg" width="30px"><span>Citroen</span> 👍（1） 💬（1）<div>看了老师的文章体会深刻醍醐灌顶。不可变借用，从字面理解就是借出去了，你就不能变了，所以既然保证不变了，那这样的借用当然可以被借出去N次（原变量不可变是只限于在借出去的变量的有效生命周期内）。可变借用就是借出去随时有被改变的可能，在同一生命周期内借出去多次，有不确定性的被谁改变的风险，尤其多线程中，所以就只让你借出去一次，既然存在有不确定性的被修改的可能，那这个时期肯定就不会让你再有不可以变借用了（因为随时会改变了，不可变借用本身也就不成立了）。Rust这个逻辑看似很繁杂，实则逻辑环环相扣清晰很符合常规。</div>2023-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/fa/25/e40eeb9c.jpg" width="30px"><span>三过rust门而不入</span> 👍（1） 💬（1）<div>太细了，这个课程写的真的好！</div>2023-11-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ4reATXtqhQ26vWXhiaZUEF9W1E0ZEqibrxxzR7NrlGwjrCZeLvF2HnL8jFjGXaFtN1vBTSia6492g/132" width="30px"><span>javpower</span> 👍（1） 💬（1）<div>借用规则类似于读写锁，即同一时刻只能拥有一个写锁，或者多个读锁，不允许写锁和读锁同时出现。这是为了避免数据竞争，保障数据一致性。
</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/51/ea/d9a83bb3.jpg" width="30px"><span>古明地觉</span> 👍（1） 💬（1）<div>1. 如果换个例子就好解释了
fn main() {
    let mut s = &quot;hello&quot;.to_string();
    let p = &amp;s;  &#47;&#47; 不可变借用
    s.push_str(&quot; world&quot;);  &#47;&#47; 可变借用
    println!(&quot;{}&quot;, p);  &#47;&#47; 不可变借用
}
由于不可变借用和可变借用的范围出现了重叠，因此编译出错。而 a = 20 和此处类似，都是修改了实际数据。

2. 因为多个可变引用的作用范围不能存在交集，所以 Copy 的话没有意义，因此只能 Move</div>2023-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/da/d7f591a7.jpg" width="30px"><span>励研冰</span> 👍（1） 💬（1）<div>从语意上保证了安全性，不可变引用语意:从此刻开始到我的运用域结束，原始值请保持我开始的状态，不然就破坏了我的不可变引用的语;可变引用同样的道理;。类似于mysql中的可重复读事物，不过mysql的实现方式是通过mvcc ,为了提高并发度；而rust是限制修改，更像是排斥锁，不允许交叉；不过这样的话不知道后面的 无谓并发 在对同一个数据的修改上会不会有什么问题</div>2023-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/05/ca/eefef69b.jpg" width="30px"><span>刘永臣</span> 👍（1） 💬（1）<div>问题1：所有权借出时，原所有权变量不能操作；
问题2：引用的复制实际上是所有权的借出，类似于所有权转移，不是复制数据。</div>2023-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/eb/cf/8fa3dd5a.jpg" width="30px"><span>RobinH</span> 👍（0） 💬（1）<div>struct NewNode&lt;T&gt; {
    val: T,
    next: Option&lt;Box&lt;NewNode&lt;T&gt;&gt;&gt;,
}

impl&lt;T: Display&gt; NewNode&lt;T&gt; {
    fn new(val: T) -&gt; Self {
        NewNode { val, next: None }
    }

    pub fn put(&amp;mut self, val: T) {
        let mut cur = self;
        while let Some(node) = &amp;mut cur.next {  &#47;&#47; `cur.next` is borrowed here
            cur = node;
        }

        &#47;&#47; error: `cur.next` is assigned to here but it was already borrowed
        cur.next = Some(Box::new(NewNode { val, next: None }));
    }
}

while 完后，while 里的 cur.next 应该结束了，下一行的 cur.next 赋值应该不会发生可变引用问题，为什么会出现借用报错？老师有空帮指导下哈 </div>2024-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/c5/a53f8bbc.jpg" width="30px"><span>Young！</span> 👍（0） 💬（1）<div>1. 为了保证数据在内存中的一致性。如果当前时刻，可变引用可以修改原数据值，原值也可以改变自身的值，那在多线程的情况下就会发生原值不一致的问题。所以在同一时刻只有一个不管是原值也好可变引用也好，只有一个所有权才能去改变原值！
2. 我觉得还是第一个问题的结论，当前时刻如果有多个可变引用的话，你改我改，数据最后都乱了。</div>2023-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/cd/e0/7ba3c15d.jpg" width="30px"><span>Mango</span> 👍（0） 💬（1）<div>function (&amp;mut s1) 值可以修改，且后面可以继续使用（引用传递）</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（0） 💬（1）<div>有两个疑问
1. 是不是代码只要遵守了这些引用的规则，就能够解决C语言中指针使用的所有不安全的问题？
2. 没有这些规则，C语言指针能够实现的所有安全的功能，用Rust语言是否都能解决？
如果能有个C语言中指针的问题清单，使用哪些规则分别解决什么问题的对应列表，理解起来就更透彻了。
例如，越界，返回局部变量的地址，悬挂的指针等。</div>2023-12-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/jwGOeRZ97OGOFTpW8AsJJNGHhPsm8hP3RvjnKyAibDfSZSjcvoFkDzZYXQS7pyqicwUe5WC5opEDYkrTG0Yazo2A/132" width="30px"><span>Apple_9029b4</span> 👍（0） 💬（1）<div>b的作用域是3-6行，在当中发生了写入，这个是不允许的</div>2023-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（1）<div>
fn main() {
    let mut a = 10u32;
    let mut b = &amp;mut a;
    let c = &amp;mut b;
    let d = &amp;mut c;

    ****d = 30;

    println!(&quot;{d}&quot;);
}
为何上面的c可以引用b；而d却不能再引用c了</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（1）<div>println!(&quot;{a}&quot;);  &#47;&#47; 这一句移到的前面来  
|               ^^^ immutable borrow occurs here&#47;&#47; 提示说这里发生了不可变借用7 |     
println!(&quot;{b}&quot;);  
|               --- mutable borrow later used here&#47;&#47; 在这后面使用了可变借用

上面的代码中为何同样是println!语句，上面的是不可变借用而下面的却又是可变借用？</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/b7/1a18a39d.jpg" width="30px"><span>5-刘新波(Arvin)</span> 👍（0） 💬（1）<div>讲的太棒，非常清晰！</div>2023-11-12</li><br/><li><img src="" width="30px"><span>Geek_f84b05</span> 👍（0） 💬（1）<div>这段描述“我们来看剩下的一些语言细节。下面这段代码展示了 mut 修饰符，&amp;mut 和 &amp; 同时出现的情况，也就是说，可变引用和不可变引用是可以同时存在的。”与“在一个所有权型变量的可变引用与不可变引用的作用域不能交叠，也可以说不能同时存在。”相矛盾，事实上代码中的两个引用的作用域并没有重叠，也就是说可变引用和不可变引用是并没有同时存在</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（0） 💬（1）<div>    &#47;&#47; 思考题1
    &#47;&#47; 问题: 为啥在不可变引用存在的情况下, 原变量不能被修改呢?
    &#47;&#47; 我的解答: 因为如果可以修改原变量, 那么对于不可变引用来说相当于是可变了, 失去了不可变引用的意义
    &#47;&#47; let mut a: u32 = 10;
    &#47;&#47; let b = &amp;a;
    &#47;&#47; a = 20;
    &#47;&#47; println!(&quot;{}&quot;, b);

    &#47;&#47; 思考题2
    &#47;&#47; 问题: 可变引用复制的时候，为什么不允许 copy，而是 move?
    &#47;&#47; 我的解答:
    &#47;&#47;        如果是copy, 那么会发生两个可变引用同时存在的情况, 违反了可变引用的规则
}
</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（0） 💬（1）<div>多级引用那块没怎么看懂XD</div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3e/e8/3736f3cd.jpg" width="30px"><span>冷石</span> 👍（0） 💬（1）<div>赞👍</div>2023-10-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83equY82MMjfvGtzlo8fhT9fdKO5LjWoy0P8pfCmiaFJS0v8Z4ibzrmwHjib9CnmgMiaYMhPyja7qS6KqiaQ/132" width="30px"><span>Geek_004fb2</span> 👍（0） 💬（1）<div>1.明确声明的是不可变借用,拥有所有权的如果能改变值,那么对我这个不可变借用来说是不安全的
2.如果Copy的话,违背了可变引用独占的原则</div>2023-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/5d/fc/2e5e2a90.jpg" width="30px"><span>二夕</span> 👍（0） 💬（1）<div>思考题 1：第三行创建了一个不可变引用，它会借用原始变量 a 的所有权，为了避免潜在的数据竞争和不确定性，a 在借用期间不能修改；
思考题 2：Rust 借用规则中有说：一次只能由一个可变引用或多个只读引用。如果允许复制可变引用，就可能会导致多个可变引用同时存在，并同时修改同一个值，违反了 Rust 的借用规则。所以为了避免这种情况，Rust 禁止了可变引用的复制，只允许移动操作。</div>2023-10-26</li><br/>
</ul>