你好，我是陈天。储备好前置知识之后，今天我们就正式开始 Rust 语言本身的学习。

学语言最好的捷径就是把自己置身于语言的环境中，而且我们程序员讲究 “get hands dirty”，直接从代码开始学能带来最直观的体验。所以从这一讲开始，你就要在电脑上设置好 Rust 环境了。

今天会讲到很多 Rust 的基础知识，我都精心构造了代码案例来帮你理解，**非常推荐你自己一行行敲入这些代码，边写边思考为什么这么写，然后在运行时体会执行和输出的过程**。如果遇到了问题，你也可以点击每个例子附带的代码链接，在 [Rust playground](https://play.rust-lang.org/) 中运行。

Rust 安装起来非常方便，你可以用 [rustup.rs](https://rustup.rs/) 中给出的方法，根据你的操作系统进行安装。比如在 UNIX 系统下，可以直接运行：

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

这会在你的系统上安装 Rust 工具链，之后，你就可以在本地用 `cargo new` 新建 Rust 项目、尝试 Rust 功能。动起手来，试试用Rust写你的第一个 [hello world 程序](https://play.rust-lang.org/?version=stable&mode=debug&edition=2018&gist=3d8814d1b868534a65ef79b3114d8cf5)吧！

```rust
fn main() {
    println!("Hello world!");
}
```

你可以使用任何编辑器来撰写 Rust 代码，我个人偏爱 VS Code，因为它免费，功能强大且速度很快。在 VS Code 下我为 Rust 安装了一些插件，下面是我的安装顺序，你可以参考：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1d/71/25/e9bad0b3.jpg" width="30px"><span>树静风止</span> 👍（8） 💬（1）<div>2022-12-28，这是一条较新的错误处理解决留言。
如果你是在windows环境下cargo run课程中的代码发现出现以下错误：
error: linking with `x86_64-w64-mingw32-gcc` failed: exit code: 1
网上解决方案是安装x86_64-pc-windows-msvc，但是你已经成功安装，却依然报错。
原因是除了安装msvc工具链以外，你还需要切换rust当前默认的工具链。
# 显示当前安装的工具链信息
rustup show
# 设置当前默认工具链
 rustup default stable-x86_64-pc-windows-msvc

这样你就可以正常编译运行了。</div>2022-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（53） 💬（6）<div>export RUSTUP_DIST_SERVER=https:&#47;&#47;mirrors.sjtug.sjtu.edu.cn&#47;rust-static
export RUSTUP_UPDATE_ROOT=https:&#47;&#47;mirrors.sjtug.sjtu.edu.cn&#47;rust-static&#47;rustup

rust国内安装必备环境配置</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/03/43/ed0dcb27.jpg" width="30px"><span>赵岩松</span> 👍（61） 💬（4）<div>
文中的&quot;Rust 没有语句（statement），只有表达式（expression）&quot;表述我认为是错误的，
我猜这里想表达的内容应该类似于《Rust程序设计语言中》的如下语句
&quot;Rust 是一门基于表达式（expression-based）的语言，这是一个需要理解的（不同于其他语言）重要区别&quot;
但是我的观点是：Rust既存在语句也存在表达式
我的依据为书中接下来的内容
&quot;语句（Statements）是执行一些操作但不返回值的指令。表达式（Expressions）计算并产生一个值&quot;
书中还附带了一个简单的例子，在这里我大体描述一下
`let y = 6;`中，6为一个表达式，它计算出的值是 6,`let y = 6;`做为一个整体是一条语句，他并不返回值，所以我们不能在Rust中这样书写`let x = (let y = 6);`
关于这个问题还有来自交流群内&quot;Tai Huei&quot;提供的截图中的文字作为依据
&quot;Statements are instructions that do something, they do not return a value. Expressions evaluate to a value, they return that value&quot;
&quot;Rust is an expression-oriented language. This means that most things are expressions, and evaluate to some kind of value. However, there are also statements. -Steve Klabnik(member if the Rust core team)&quot;</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（38） 💬（3）<div>我想很多人不会被课后问题所困扰而是被 Copy 和 Clone，初学时我也很纠结，这里贴上某位大佬的总结：

Copy 和 Clone 两者的区别和联系有：

Copy内部没有方法，Clone内部有两个方法。

Copy trait 是给编译器用的，告诉编译器这个类型默认采用 copy 语义，而不是 move 语义。Clone trait 是给程序员用的，我们必须手动调用clone方法，它才能发挥作用。

Copy trait不是你想实现就实现，它对类型是有要求的，有些类型就不可能 impl Copy。Clone trait 没有什么前提条件，任何类型都可以实现（unsized 类型除外）。

Copy trait规定了这个类型在执行变量绑定、函数参数传递、函数返回等场景下的操作方式。即这个类型在这种场景下，必然执行的是“简单内存拷贝”操作，这是由编译器保证的，程序员无法控制。Clone trait 里面的 clone 方法究竟会执行什么操作，则是取决于程序员自己写的逻辑。一般情况下，clone 方法应该执行一个“深拷贝”操作，但这不是强制的，如果你愿意，也可以在里面启动一个人工智能程序，都是有可能的。

链接：https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;21730929</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（14） 💬（2）<div>2. 一个模式匹配就行了，还做到了 panic-free：

let args = std::env::args().collect::&lt;Vec&lt;String&gt;&gt;();
if let [_path, url, output, ..] = args.as_slice() {
    println!(&quot;url: {}, output: {}&quot;, url, output);
} else {
    eprintln!(&quot;参数缺失&quot;);
}</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/74/d4/38d813f0.jpg" width="30px"><span>Kerry</span> 👍（10） 💬（3）<div>课后习题需要自己查一点接口资料，结合错误信息来逐步解决编译问题。

问题一：

重复的abc计算代码可以重构为如下函数：

```rust
fn next_fib(a: &amp;mut i32, b: &amp;mut i32) {
    let c = *a + *b;
    *a = *b;
    *b = c;
}
```

以for in循环为例，用法如下：

```rust

fn fib_for(n: u8) {
    let (mut a, mut b) = (1, 1);
    
    for _i in 2..n {
        next_fib(&amp;mut a, &amp;mut b);
        println!(&quot;next val is {}&quot;, b);
    }
}
```

问题二：

```rust
fn main() -&gt; Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt; {
    let args: Vec&lt;String&gt; = env::args().collect();
    if args.len() &lt; 3 {
        println!(&quot;Usage: url outpath&quot;);
        return Ok(())
    }

    args.iter().for_each(|arg| {
        println!(&quot;{}&quot;, arg);
    });

    let url = &amp;args[1];
    let output = &amp;args[2];

    println!(&quot;Fetching url: {}&quot;, url);
    let body = &amp;reqwest::blocking::get(url)?.text()?;

    println!(&quot;Converting html to markdown...&quot;);
    let md = html2md::parse_html(body);

    fs::write(output, md.as_bytes())?;
    println!(&quot;Converted markdown has been saved in {}.&quot;, output);

    Ok(())
}
```

好歹是跑起来了……装了智能提示真不错，有better impl的建议 :)</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/96/81c8cc33.jpg" width="30px"><span>Quincy</span> 👍（10） 💬（3）<div>use std::fs;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name=&quot;scrape_url&quot;)]
struct Opt {
    #[structopt(help=&quot;input url&quot;)]
    pub url: String,
    #[structopt(help=&quot;output file, stdout if not present&quot;)]
    pub output: Option&lt;String&gt;,
}

fn main() {
    let opt = Opt::from_args();

    let url = opt.url;
    let output = &amp;opt.output.unwrap_or(&quot;rust.md&quot;.to_string());

    println!(&quot;Fetching url: {}&quot;, url);
    let body = reqwest::blocking::get(url).unwrap().text().unwrap();

    println!(&quot;Converting html to markdown...&quot;);
    let md = html2md::parse_html(&amp;body);

    fs::write(output, md.as_bytes()).unwrap();
    println!(&quot;Converted markdown has been saved in {}.&quot;, output);
}
</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/79/803537db.jpg" width="30px"><span>慢动作</span> 👍（9） 💬（1）<div>字符串字面量为什么有into方法，这中间经历了什么过程？看文档根本不知道这个方法哪里来的，😂。还是有点操之过急，看到不明白就瞎忙活，感觉还是得循序渐进</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c9/be/1949917d.jpg" width="30px"><span>🔥神山 | 雷神山</span> 👍（8） 💬（1）<div>
2. 在 scrape_url 的例子里，我们在代码中写死了要获取的 URL 和要输出的文件名，这太不灵活了。你能改进这个代码，从命令行参数中获取用户提供的信息来绑定 URL 和文件名么？类似这样：
```rust
use std::env;
use std::error;
use std::fs;
use std::process;

const NOT_ENOUGH_ARGS_CODE: i32 = 1;
const NOT_GET_HTTP_DATA_CODE: i32 = 2;
const CAN_NOT_CONVERT_MD_CODE: i32 = 3;

#[derive(Debug)]
struct Config {
    url: String,    &#47;&#47;网址
    output: String, &#47;&#47;输出文件名
}

impl Config {
    fn new(url: String, output: String) -&gt; Config {
        Config { url, output }
    }

    fn curl_url(&amp;self) -&gt; Result&lt;String, Box&lt;dyn error::Error&gt;&gt; {
        println!(&quot;Fetching url: {}&quot;, self.url);
        let body = reqwest::blocking::get(&amp;self.url)?.text()?;
        Ok(body)
    }

    fn convert_md_file(&amp;self, body: String) -&gt; Result&lt;(), Box&lt;dyn error::Error&gt;&gt; {
        println!(&quot;Converting html to markdown...&quot;);
        let md = html2md::parse_html(&amp;body);
        fs::write(&amp;self.output, md.as_bytes())?;
        println!(&quot;Converted markdown has been saved in {}.&quot;, self.output);
        Ok(())
    }
}

fn parse_args(args: &amp;[String]) -&gt; Result&lt;Config, &amp;str&gt; {
    if args.len() &lt; 3 {
        return Err(&quot;Not enough arguments!&quot;);
    }
    let url = args[1].clone();
    let output = args[2].clone();
    Ok(Config::new(url, output))
}

fn main() {
    let args: Vec&lt;String&gt; = env::args().collect();
    match parse_args(&amp;args) {
        Err(err) =&gt; {
            println!(&quot;Error: {}&quot;, err);
            process::exit(NOT_ENOUGH_ARGS_CODE);
        }
        Ok(cfg) =&gt; match cfg.curl_url() {
            Err(err) =&gt; {
                println!(&quot;Error: {}&quot;, err.to_string());
                process::exit(NOT_GET_HTTP_DATA_CODE);
            }
            Ok(body) =&gt; {
                let result = cfg.convert_md_file(body);
                if result.is_err() {
                    println!(&quot;Error: Can NOT write data to {}&quot;, cfg.output);
                    process::exit(CAN_NOT_CONVERT_MD_CODE);
                }
            }
        },
    }
}
```</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（6） 💬（1）<div>这里有几个小疑惑.
1.首先把函数作为参数这里，例如a(1，b(2))这样的，那么和先调用b得到结果再填入a中有什么本质区别吗？我不理解的是，分开调用好像也没什么问题，有什么场景下需要函数作为参数这样调用的？
2.派生宏这里#[derive(Debug)]，这个例子中实现的是什么功能不太理解？
3.println! 这里的语法多了一个感叹号，很多语言都有println，多了这个感叹号封装多了一些什么吗？看过一些资料也不太理解
多谢了</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ee/f8/6f69be1e.jpg" width="30px"><span>Raina</span> 👍（6） 💬（1）<div>所以还是要有rust基础才行，我先去看看Rust圣经再回来&gt;_&lt;</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/44/2267a5a7.jpg" width="30px"><span>一期一会</span> 👍（4） 💬（1）<div>运行2md代码，发生openssl编译问题：
Compiling openssl-sys v0.9.66
error: failed to run custom build command for `openssl-sys v0.9.66`

折腾了大半天还是不行</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/da/a8a32113.jpg" width="30px"><span>太子长琴</span> 👍（4） 💬（1）<div>fib 这个还挺有意思的，可以把 next 单独拿出来，在内部做赋值（c = *a+*b, *a=*b, *b=c）；也可以把 a 先算出来，然后 swap ab（a = a+b, swap(a,b)）；或者使用 mut reference tuple（fib = (fib.1, fib.0+fib.1)）。

第二个在RPL中有个I&#47;O Project的例子，用了 Config，不过感觉捕捉一下 Err 就可以了：
```rust
let args: Vec&lt;String&gt; = env::args().collect();
    let (url, output) = parse_config(&amp;args);
    if let Err(e) = scrape_url::scrape(url, output) {
        println!(&quot;{}&quot;, e);
    }
```

课程真心不错~深入浅出不啰嗦~</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c9/be/1949917d.jpg" width="30px"><span>🔥神山 | 雷神山</span> 👍（4） 💬（3）<div>1. 在上面的斐波那契数列的代码中，你也许注意到计算数列中下一个数的代码在三个函数中不断重复。这不符合 DRY（Don’t Repeat Yourself）原则。你可以写一个函数把它抽取出来么？
1) 定义一个loop_calc:
```rust
fn loop_calc(mut first_num: i32, mut second_num: i32, limit: u8) {
    for _i in 2..limit {
        let sum_num = first_num + second_num;
        first_num = second_num;
        second_num = sum_num;
        println!(&quot;next val is {}&quot;, sum_num);
    }
}
```
2) 在三个函数:fib_loop, fib_while, fib_for分别调用loop_calc(a, b, n)即可
完整版本:
```rust
fn loop_calc(mut first_num: i32, mut second_num: i32, limit: u8) {
    for _i in 2..limit {
        let sum_num = first_num + second_num;
        first_num = second_num;
        second_num = sum_num;
        println!(&quot;next val is {}&quot;, sum_num);
    }
}

fn fib_loop(n: u8) {
    let a = 1;
    let b = 1;
    loop_calc(a, b, n);
}

fn fib_while(n: u8) {
    let (a, b) = (1, 1);
    loop_calc(a, b, n);
}

fn fib_for(n: u8) {
    let (a, b) = (1, 1);
    loop_calc(a, b, n);
}

fn main() {
    let n = 10;
    fib_loop(n);
    fib_while(n);
    fib_for(n);
}
```
</div>2021-08-27</li><br/><li><img src="" width="30px"><span>Geek_67a5d1</span> 👍（3） 💬（1）<div>初学者，花了一天时间才基本消化了老师讲20分钟的东西😅。简单方式做一下思考题2：

use std::fs;

fn print_usage_prompt_and_exit() {
    println!(&quot;USAGE: cargo run -- url file.md&quot;);
    std::process::exit(-1);
}

fn main() {
    let args: Vec&lt;String&gt; = std::env::args().skip(1).collect();

    if args.len() != 2 {
        print_usage_prompt_and_exit();
    }

    let (url, output) = (&amp;args[0], &amp;args[1]);

    println!(&quot;Fetching url: {}&quot;, url);
    let body = reqwest::blocking::get(url).unwrap().text().unwrap();

    println!(&quot;Converting html to markdown...&quot;);
    let md = html2md::parse_html(&amp;body);

    fs::write(output, md.as_bytes()).unwrap();
    println!(&quot;Converted markdown has been saved in {}.&quot;, output);
}
</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/98/e0/8c814c13.jpg" width="30px"><span>王硕尧</span> 👍（3） 💬（1）<div>其实 fn(i32) -&gt; i32 这个类型是一个函数指针类型：https:&#47;&#47;doc.rust-lang.org&#47;reference&#47;types&#47;function-pointer.html</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（2） 💬（1）<div>关于函数返回的 unit ，是不是可以认为是c&#47;c++的void 也就是返回一个空类型？
</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（2） 💬（3）<div>    &#47;&#47; let url = &quot;https:&#47;&#47;www.rust-lang.org&#47;&quot;;
    let args: Vec&lt;String&gt; = env::args().collect();
    let url = &amp;args[1];

不查资料真是想不到怎样正确获取命令行参数</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/47/e00e9841.jpg" width="30px"><span>manonloki</span> 👍（1） 💬（1）<div>use std::env;
use std::fs;
fn main() -&gt; Result&lt;(), Box&lt;dyn std::error::Error&gt;&gt;{
    &#47;&#47; 先判判断参数长度是否足够
    if env::args().len() &lt; 2 {
        println!(&quot;Not Enought Arguments&quot;);
    }

    &#47;&#47; 转为数组进行操作
    let args: Vec&lt;String&gt; = env::args().collect();

    &#47;&#47; 从第二个开始是参数
    let url = &amp;args[1];
    let output = &amp;args[2];

    println!(&quot;fetching url:{}&quot;, url);
    let body = reqwest::blocking::get(url)?.text()?;

    println!(&quot;Converting html to markdown...&quot;);
    let md = html2md::parse_html(&amp;body);

    fs::write(output, md.as_bytes())?;

    println!(&quot;Converted markdown has been saved in {}.&quot;, output);

    Ok(())
}
</div>2022-01-13</li><br/><li><img src="" width="30px"><span>chyuwei</span> 👍（1） 💬（1）<div>文章中设计将mod放在某个文件夹中，于当前的 The Rust Programming Language 不一样。
不过我记得老版书的方法和课程中介绍的是一致的。
现在的大概是
一个 hello.rs 与 文件夹hello
使用hello的地方可以直接申明 mod hello

</div>2022-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/3d/f40f2898.jpg" width="30px"><span>fainle</span> 👍（1） 💬（1）<div>第一个例子：执行 cargo run 后没有反应
提示  Blocking waiting for file lock on package cache</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/95/b6/9aff520e.jpg" width="30px"><span>虾</span> 👍（1） 💬（1）<div>Rust给结构体成员初始化，为什么会用类似js的冒号呢？
js用键值对风格的冒号，有情可原（虽然我也不喜欢）。毕竟js没有静态的结构体。
但Rust的结构体是静态的，并不是字典。我觉得，冒号后面应该只会跟类型，不跟值。并且把初始化列表的逗号改为分号，这样风格才更统一啊。
不知道作者大人怎么理解这个问题？这是个纯粹的风格的问题，还是有什么不得不为之的理由呢？</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/17/2d/b7614553.jpg" width="30px"><span>Bruce</span> 👍（1） 💬（1）<div>更新的有点慢😂</div>2021-08-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJGSiaRVNB3B267z9BA9HjvCZoFkMm5ficrLTjPdQAFXTmqSGAxCfjujXSS8icpUFXEFsDf4rSOYrvcA/132" width="30px"><span>Geek_7eba7c</span> 👍（1） 💬（4）<div>html2md: Error: Command failed: git --no-pager --git-dir=&quot;&#47;Users&#47;chenang&#47;.cargo&#47;registry&#47;index&#47;github.com-1ecc6299db9ec823&#47;.git&quot; show origin&#47;master:ht&#47;ml&#47;html2md
fatal: 无效的对象名 &#39;origin&#47;master&#39;。 cargo.toml 提示这个错 ，帮忙看下</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（5）<div>nightly里打开destructuring_assignment特性，就可以像python&#47;js等其他语言里那样写：

let (mut a, mut b) = (1, 1);
for _i in 2..n {
    (a, b) = (b, a + b);
}</div>2021-08-28</li><br/><li><img src="" width="30px"><span>Geek_632da1</span> 👍（1） 💬（1）<div>刚学完更新的一讲，很不错的呢！结合汉哥的《rust编程之道》来看，感觉学起来还是很nice的！加油！</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/98/e0/8c814c13.jpg" width="30px"><span>王硕尧</span> 👍（1） 💬（1）<div>Rust 既有statement又有expression，Rust的statement主要用于显式顺序表达式求值以及包含一些表达式：In contrast, statements in Rust serve mostly to contain and explicitly sequence expression evaluation.

https:&#47;&#47;doc.rust-lang.org&#47;reference&#47;statements-and-expressions.html</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/1a/5a/c3a553dd.jpg" width="30px"><span>少年 🎨</span> 👍（0） 💬（2）<div>卡在国内镜像设置这，我是不是太笨了。</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4a/f4/513d26e8.jpg" width="30px"><span>zoomdong</span> 👍（0） 💬（1）<div>第二题我是这样处理的，但是没有加上错误处理的机制，这块后续学习了再补一下:
```rs
use std::fs;
use std::env;

fn main() {

    &#47;&#47; .collect() 能创建一个包含迭代器所有值的 vector
    let args: Vec&lt;String&gt; = env::args().collect();
    &#47;&#47; 这里要取引用
    let (url, output) = (&amp;args[1], &amp;args[2]);
    println!(&quot;The all args are is {:?}&quot;, args);

    println!(&quot;Fetching url: {}&quot;, url);

    let body = reqwest::blocking::get(url).unwrap().text().unwrap();

    println!(&quot;Converting html to markdown...&quot;);
    let md = html2md::parse_html(&amp;body);
    fs::write(output, md.as_bytes()).unwrap();
    println!(&quot;Converted markdown has been saved in {}.&quot;, output);

}
```</div>2022-01-04</li><br/><li><img src="" width="30px"><span>ykang</span> 👍（0） 💬（1）<div>请问，有无共同学习的微信群或QQ群？</div>2022-01-01</li><br/>
</ul>