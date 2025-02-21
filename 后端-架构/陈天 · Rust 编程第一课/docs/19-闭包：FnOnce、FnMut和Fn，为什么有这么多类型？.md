你好，我是陈天。

在现代编程语言中，闭包是一个很重要的工具，可以让我们很方便地以函数式编程的方式来撰写代码。因为闭包可以作为参数传递给函数，可以作为返回值被函数返回，也可以为它实现某个 trait，使其能表现出其他行为，而不仅仅是作为函数被调用。

这些都是怎么做到的？这就和 Rust 里闭包的本质有关了，我们今天就来学习基础篇的最后一个知识点：闭包。

### 闭包的定义

之前介绍了闭包的基本概念和一个非常简单的例子：

> 闭包是将函数，或者说代码和其环境一起存储的一种数据结构。闭包引用的上下文中的自由变量，会被捕获到闭包的结构中，成为闭包类型的一部分（[第二讲](https://time.geekbang.org/column/article/410038)）。

闭包会根据内部的使用情况，捕获环境中的自由变量。在 Rust 里，闭包可以用 `|args| {code}` 来表述，图中闭包 c 捕获了上下文中的 a 和 b，并通过引用来使用这两个自由变量：  
![](https://static001.geekbang.org/resource/image/60/93/6060b99f222ef6e435c9fe7c83f46593.jpg?wh=2935x1544)

除了用引用来捕获自由变量之外，还有另外一个方法使用 move 关键字 `move |args| {code}` 。

之前的课程中，多次见到了创建新线程的 thread::spawn，它的参数就是一个闭包：

```rust
pub fn spawn<F, T>(f: F) -> JoinHandle<T> 
where
    F: FnOnce() -> T,
    F: Send + 'static,
    T: Send + 'static,
```
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/f0/62d8cf9e.jpg" width="30px"><span>D. D</span> 👍（31） 💬（2）<div>1. 相当于：
struct Closure&lt;&#39;a, &#39;b: &#39;a&gt; {
    data: (i32, i32, i32, i32),
    v: &amp;&#39;a [&amp;&#39;b str],
    name: String,
}

它的长度等于 4*4(4个i32) + 2*8(ptr, len) + 3*8(ptr, len, cap) = 56字节。
代码的最后不能访问name了，因为已经使用了move关键字将name的所有权移至闭包c中了。

2. 从定义可以看出，调用FnOnce的call_once方法会取得闭包的所有权。因此对于闭包c和c1来说，即使在声明时不使用mut关键字，也可以在其call_once方法中使用所捕获的变量的可变借用。

3.
impl&lt;F&gt; Executor for F
where
    F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;,
{
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
        self(cmd)
    }
}</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（5） 💬（1）<div>Rust 闭包，看这一篇真的就够了</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/22/d12f7a72.jpg" width="30px"><span>TheLudlows</span> 👍（2） 💬（1）<div>思路清晰，深入浅出，佩服陈天老师👍</div>2021-11-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIzVGyhMctYa2jumzLicZVLia0UCTqrWfiaY8pY4c3AbGH2tH5TxONcbicoXGdE3ia43TpXxbZWPZoS6Jg/132" width="30px"><span>lambda</span> 👍（2） 💬（3）<div>关于第三题有个问题，如果我把
impl&lt;F&gt; Executor for F
where
    F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;
写成：
impl Executor for fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; 

会报错：
the trait `Executor` is not implemented for
应该是没对闭包实现Executor这个trait

那我的那个声明是给哪个谁实现了Executor这个trait了呢？</div>2021-10-23</li><br/><li><img src="" width="30px"><span>linuxfish</span> 👍（1） 💬（4）<div>“然而，一旦它被当做 FnOnce 调用，自己会被转移到 call_once 函数的作用域中，之后就无法再次调用了”

老师，实际调试了一下你的代码，发现只要在`call_once`中传入闭包的引用，后续是可以继续使用闭包的，具体请看：

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=27cd35717d166f01a4045846721cf989</div>2021-10-07</li><br/><li><img src="" width="30px"><span>Geek_b52974</span> 👍（0） 💬（1）<div>1. 56
2. 傳入 FnOnce 的時候是執行 fn call_once(self, args: Args) -&gt; Self::Output; 是傳入 self, 而非 &amp;mut self 所以不需要 mut 關鍵字
3. 
impl&lt;F&gt; Executor for F where 
    F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;,
{
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
        self(cmd)
    }
}
</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（0） 💬（1）<div>两点思考, 请老师指正

1. std::function可能类似于dyn Fn()之类的trait object...可能会涉及到额外的vtable (http:&#47;&#47;www.elbeno.com&#47;blog&#47;?p=1068 提到的optimization也可能优化掉vtable);

不过重点是rust的trait object可以被lifetime 限制. 而cpp不行, 所以std::function需要在heap上得到一个pointer做type erasure

2. 例子中&amp;main的size是0...从Cpp过来的人表示很奇怪...查了一下:

main不是function pointer; 而是和closure有点相似的function item的instance (类似于一个zero sized struct, 不过包含了function name, args, lifetimes)

```
    &#47;&#47; found `fn() {main}` -&gt; closure has unique id, so does main
    &#47;&#47; it also has a struct for it
    &#47;&#47; https:&#47;&#47;github.com&#47;rust-lang&#47;rust&#47;issues&#47;62440
    &#47;&#47; size_of_val(main),
    size_of_val(&amp;main),
```

https:&#47;&#47;github.com&#47;rust-lang&#47;rust&#47;issues&#47;62440

&gt; This is the compiler&#39;s way of representing the unique zero sized type that corresponds to the function.
&gt; 
&gt; This is akin to how closures also create a unique type (but in that case, the size may be &gt;= 0 depending on the captured environment).

function item需要被显式coerce到function pointer (https:&#47;&#47;doc.rust-lang.org&#47;nightly&#47;reference&#47;types&#47;function-item.html)
</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/e9/da5c0203.jpg" width="30px"><span>亚伦碎语</span> 👍（0） 💬（1）<div>
pub trait Executor {
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;;
}

struct BashExecutor {
    env: String,
}

impl&lt;F&gt; Executor for F
where
    F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;,
{
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
        self(cmd)
    }
}

impl Executor for BashExecutor {
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
        Ok(format!(
            &quot;fake bash execute: env: {}, cmd: {}&quot;,
            self.env, cmd
        ))
    }
}

&#47;&#47; 看看我给的 tonic 的例子，想想怎么实现让 27 行可以正常执行

fn main() {
    let env = &quot;PATH=&#47;usr&#47;bin&quot;.to_string();

    let cmd = &quot;cat &#47;etc&#47;passwd&quot;;
    let r1 = execute(cmd, BashExecutor { env: env.clone() });
    println!(&quot;{:?}&quot;, r1);

    let r2 = execute(cmd, |cmd: &amp;str| {
        Ok(format!(&quot;fake fish execute: env: {}, cmd: {}&quot;, env, cmd))
    });
    println!(&quot;{:?}&quot;, r2);
}

fn execute(cmd: &amp;str, exec: impl Executor) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
    exec.execute(cmd)
}</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（0） 💬（2）<div>1、不能访问，name变量的所有权已经被移动闭包里面去了，move强制导致的
3、pub trait Executor{
    fn execute(&amp;self,cmd:&amp;str) -&gt;Result&lt;String,&amp;&#39;static str&gt;;
}

struct BashExecutor{
    env:String
}

impl Executor for BashExecutor{
    fn execute(&amp;self, cmd:&amp;str) -&gt;Result&lt;String,&amp;&#39;static str&gt; {
       Ok(format!(
            &quot;fake bash execute:env:{},cmd :{}&quot;,self.env,cmd
       )) 
    }
}

impl &lt;F&gt; Executor for F 
where F:Fn(&amp;str) -&gt;Result&lt;String,&amp;&#39;static str&gt;
{

    fn execute(&amp;self, cmd:&amp;str) -&gt;Result&lt;String,&amp;&#39;static str&gt; {
        self(cmd)
    }
    
}


fn execute(cmd:&amp;str,exec:impl Executor) -&gt; Result&lt;String,&amp;&#39;static str&gt;{
    exec.execute(cmd)
}

pub fn test(){
    let env = &quot;PATH=&#47;usr&#47;bin&quot;.to_string();

    let cmd = &quot;cat &#47;etc&#47;passwd&quot;;

    let r1 = execute(cmd, BashExecutor{env:env.clone()});
    println!(&quot;{:?}&quot;,r1);


    let r2 = execute(cmd, |cmd :&amp;str|{
        Ok(format!(&quot;fake fish execute: env: {}, cmd: {}&quot;, env, cmd))
    });
    println!(&quot;{:?}&quot;,r2);

}
</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/d3/17/22c36063.jpg" width="30px"><span>f</span> 👍（21） 💬（2）<div>发现了老师文中的一个错误结论。当闭包不使用move时，是推断着判断如何去捕获变量的，先尝试不可变引用，然后尝试可变引用，最后尝试Move&#47;Copy，一旦尝试成功，将不再尝试。当使用move时，是强制Move&#47;Copy，而不是一步一步地去推断尝试。

在the rust reference: https:&#47;&#47;doc.rust-lang.org&#47;reference&#47;expressions&#47;closure-expr.html里有说明：
```
Without the move keyword, the closure expression infers how it captures each variable from its environment, preferring to capture by shared reference, effectively borrowing all outer variables mentioned inside the closure&#39;s body. If needed the compiler will infer that instead mutable references should be taken, or that the values should be moved or copied (depending on their type) from the environment. A closure can be forced to capture its environment by copying or moving values by prefixing it with the move keyword. This is often used to ensure that the closure&#39;s lifetime is &#39;static.
```
代码验证：
```rust
fn main() {
    let mut name = String::from(&quot;hello&quot;);

    &#47;&#47; 1.不可变引用，&amp;name被存储在闭包c1里
    let c1 = || &amp;name;
    &#47;&#47; 可使用所有者变量name，且可多次调用闭包
    println!(&quot;{}, {:?}, {:?}&quot;, name, c1(), c1());

    &#47;&#47; 2.可变引用，&amp;mut name被存储在闭包c2里，调用c2的时候要修改这个字段，
    &#47;&#47; 因此c2也要设置为mut c2
    let mut c2 = || {
        name.push_str(&quot; world &quot;);
    };
    &#47;&#47; 可多次调用c2闭包
    &#47;&#47; 但不能调用c2之前再使用name或引用name，因为&amp;mut name已经存入c2里了
    &#47;&#47; println!(&quot;{}&quot;, name);  &#47;&#47; 取消注释将报错
    &#47;&#47; println!(&quot;{}&quot;, &amp;name); &#47;&#47; 取消注释将报错
    c2();
    c2();

    &#47;&#47; 3.Move&#47;Copy，将name移入到闭包c3中
    let c3 = || {
        let x = name;
        &#47;&#47; let y = name;  &#47;&#47; 取消注释见报错，use of moved value
    };
    &#47;&#47; println!(&quot;{}&quot;, name);  &#47;&#47;取消注释将报错
}
```

</div>2021-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/b1/2e96794c.jpg" width="30px"><span>flyflypeng</span> 👍（6） 💬（2）<div>有个疑问，闭包中捕获的上下文变量是被存储在栈中，那么闭包中的代码块编译后是存放在哪里？通过什么方式指向这块代码区域呢？</div>2022-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c6/0b/eb3589f1.jpg" width="30px"><span>🐳大海全是水</span> 👍（2） 💬（1）<div>这么看来Rust的闭包变量捕获不如c++的灵活，c++的lambda是可以对单个变量进行by-value或者是by-ref方式或者move捕获的，rust 闭包里写了move就全部转走了。如果我某个变量需要move，但是其他变量需要by-ref捕获，怎么实现？</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（0） 💬（0）<div>再讲FnMut或Fn被当做FnOnce调用一次后就不能调用的时候，“
&#47;&#47; 然而一旦它被当成 FnOnce 被调用，就无法被再次调用    
println!(&quot;result: {:?}&quot;, call_once(&quot;hi&quot;.into(), c));
”有问题吧？
这里不能再被调用不是因为当做FnOnce被调用，而是因为name变量移动所有权到闭包里，执行一次后，name就销毁了，取消move关键字，就可以多次调用</div>2023-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/3c/70d30681.jpg" width="30px"><span>EEEEEEEarly</span> 👍（0） 💬（0）<div>&quot;看图中 gdb 的输出，闭包是存储在栈上&quot; 这个是怎么看出来存储在栈上的？</div>2023-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/83/02/fec7a0e1.jpg" width="30px"><span>zzLion</span> 👍（0） 💬（0）<div>为什么fn定义的函数，在 call_once 之后不move呢，还是以通过call_once调用</div>2023-04-02</li><br/><li><img src="" width="30px"><span>CyNevis</span> 👍（0） 💬（0）<div>&#47;&#47; 为Fn实现Executor trait
    impl &lt;F&gt; Executor for F
    where
        F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;
    {
        fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
            self(cmd)
        }
    }</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ce/e8/8b3126d0.jpg" width="30px"><span>小扔子</span> 👍（0） 💬（0）<div>老师，感觉rust闭包与C#的委托，lambda表达式异曲同工呢</div>2022-04-13</li><br/><li><img src="" width="30px"><span>sea</span> 👍（0） 💬（0）<div>impl&lt;F&gt; Executor for F
where
    F: Fn(&amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt;
{
    fn execute(&amp;self, cmd: &amp;str) -&gt; Result&lt;String, &amp;&#39;static str&gt; {
        self(cmd)
    }
}</div>2022-03-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTL9hlAIKQ1sGDu16oWLOHyCSicr18XibygQSMLMjuDvKk73deDlH9aMphFsj41WYJh121aniaqBLiaMNg/132" width="30px"><span>腾达</span> 👍（0） 💬（1）<div>`move |y| x * y` 这里能不能再多解释一下？ 我一开始没有 加 Copy 约束 和 move 出现编译错误，一步步把这2个加上，看每一步的编译错误，最后一点不是特别明白，Copy加上了，为什么还要加 move？ 不加 move，编译器报：the parameter type `T` may not live long enough，help: consider adding an explicit lifetime bound `T: &#39;static`...</div>2022-01-26</li><br/>
</ul>