你好，我是陈天。

在上一讲里，我们已经接触了 Rust 的基本语法。你是不是已经按捺不住自己的洪荒之力，想马上用 Rust 写点什么练练手，但是又发现自己好像有点“拔剑四顾心茫然”呢？

那这周我们就来玩个新花样，**做一周“learning by example”的挑战**，来尝试用 Rust 写三个非常有实际价值的小应用，感受下 Rust 的魅力在哪里，解决真实问题的能力到底如何。

你是不是有点担心，我才刚学了最基本语法，还啥都不知道呢，这就能开始写小应用了？那我碰到不理解的知识怎么办？

不要担心，因为你肯定会碰到不太懂的语法，但是，**先不要强求自己理解，当成文言文抄写就可以了**，哪怕这会不明白，只要你跟着课程节奏，通过撰写、编译和运行，你也能直观感受到 Rust 的魅力，就像小时候背唐诗一样。

好，我们开始今天的挑战。

## HTTPie

为了覆盖绝大多数同学的需求，这次挑选的例子是工作中普遍会遇到的：写一个 CLI 工具，辅助我们处理各种任务。

我们就以实现 [HTTPie](https://httpie.io/) 为例，看看用 Rust 怎么做 CLI。HTTPie 是用 Python 开发的，一个类似 cURL 但对用户更加友善的命令行工具，它可以帮助我们更好地诊断 HTTP 服务。

下图是用 HTTPie 发送了一个 post 请求的界面，你可以看到，相比 cURL，它在可用性上做了很多工作，包括对不同信息的语法高亮显示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/de/43/b4f908af.jpg" width="30px"><span>胖胖的奥利奥</span> 👍（9） 💬（2）<div>2023年 1 月 28 日可運行代碼：

extern crate clap;
use anyhow::{anyhow, Ok, Result};
use clap::Parser;
use reqwest::Url;
use std::str::FromStr;

&#47;&#47; 定义 HTTPie 的 CLI 主入口，包含多个命令
&#47;&#47; 下面 &#47;&#47;&#47; 的注释是文档， clap 会将其当成是 CLI 的帮助

&#47;&#47;&#47; A naive httpie implementation wite Rust, can you imagine how easy it is?
#[derive(Parser, Debug)]
struct Opts {
    #[clap(subcommand)]
    subcmd: SubCommand,
}

&#47;&#47;&#47; 子命令分别对应不同的 HTTP 方法，暂时只支持 GET &#47; POST 方法
#[derive(Parser, Debug)]
enum SubCommand {
    Get(Get),
    Post(Post),
}

#[derive(Parser, Debug)]
struct Get {
    #[arg(value_parser=parse_url)]
    url: String,
}

#[derive(Parser, Debug)]
struct Post {
    #[arg(value_parser=parse_url)]
    url: String,
    #[arg(value_parser=parse_kv_pair)]
    body: Vec&lt;KvPair&gt;,
}

#[derive(Debug, Clone, PartialEq)]
struct KvPair {
    k: String,
    v: String,
}

impl FromStr for KvPair {
    type Err = anyhow::Error;

    fn from_str(s: &amp;str) -&gt; Result&lt;Self, Self::Err&gt; {
        &#47;&#47; 使用 = 进行 split，这会得到一个迭代器
        let mut split = s.split(&#39;=&#39;);
        let err = || anyhow!(format!(&quot;Failed to parse {}&quot;, s));
        Ok(Self {
            &#47;&#47; 从迭代器中取第一个结果作为 key，迭代器返回 Some(T)&#47;None
            &#47;&#47; 我们将其转换成 Ok(T)&#47;Err(E)，然后用 ? 处理错误
            k: (split.next().ok_or_else(err)?).to_string(),
            &#47;&#47; 从迭代器中取第二个结果作为 value
            v: (split.next().ok_or_else(err)?).to_string(),
        })
    }
}

fn parse_kv_pair(s: &amp;str) -&gt; Result&lt;KvPair&gt; {
    s.parse()
}

fn parse_url(s: &amp;str) -&gt; Result&lt;String&gt; {
    &#47;&#47; check url
    let _url: Url = s.parse()?;

    Ok(s.into())
}

fn main() {
    let opts = Opts::parse();

    println!(&quot;{:?}&quot;, opts);
}
</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/80/52161b2f.jpg" width="30px"><span>Faith信</span> 👍（2） 💬（1）<div>rustc 1.58.1 
不能编译的参考老师github代码依赖修改</div>2022-07-20</li><br/><li><img src="" width="30px"><span>linuxfish</span> 👍（5） 💬（3）<div>遇到一个问题，提醒下刚开始学的同学：

老师使用了 clap 包的 Pre-releases 版本，Pre-releases 版本并不保证 API 的稳定。

cargo 在安装依赖的时候会自动使用【最新】的 Pre-releases 版本（尽管你在 Cargo.toml 中指定了一个老版本）

当前 clap 包的最新版本是 v3.0.0-beta.5，若按照课程（get hands dirty：来写个实用的CLI小工具）里步骤操作，会编译不过。 不过老师在 Github 上的代码已经更新成依赖 v3.0.0-beta.5，可以照着那个写。

当然，还是建议把课程里的代码也更新下，或者用红字提示下【代码已过期，请参考 Github 上的最新代码】，不然新手会比较懵逼

参考：https:&#47;&#47;doc.rust-lang.org&#47;cargo&#47;reference&#47;resolver.html#pre-releases</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/96/81c8cc33.jpg" width="30px"><span>Quincy</span> 👍（16） 💬（1）<div>&#47;&#47;&#47; 打印服务器返回的 HTTP body
fn print_body(m: Option&lt;Mime&gt;, body: &amp;String) {
    match m {
        &#47;&#47; 对于 &quot;application&#47;json&quot; 我们 pretty print
        Some(v) if v == mime::APPLICATION_JSON =&gt; {
            &#47;&#47; println!(&quot;{}&quot;, jsonxf::pretty_print(body).unwrap().cyan())
            print_syntect(body);
        }
        &#47;&#47; 其他 mime type，我们就直接输出
        _ =&gt; println!(&quot;{}&quot;, body),
    }
}

fn print_syntect(s: &amp;str) {
    &#47;&#47; Load these once at the start of your program
    let ps = SyntaxSet::load_defaults_newlines();
    let ts = ThemeSet::load_defaults();
    let syntax = ps.find_syntax_by_extension(&quot;json&quot;).unwrap();
    let mut h = HighlightLines::new(syntax, &amp;ts.themes[&quot;base16-ocean.dark&quot;]);
    for line in LinesWithEndings::from(s) {
        let ranges: Vec&lt;(Style, &amp;str)&gt; = h.highlight(line, &amp;ps);
        let escaped = as_24_bit_terminal_escaped(&amp;ranges[..], true);
        println!(&quot;{}&quot;, escaped);
    }
}</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/76/0564a5ee.jpg" width="30px"><span>王槐铤</span> 👍（9） 💬（2）<div>环境 
cargo --version
cargo 1.52.0 (69767412a 2021-04-21)

rustc --version
rustc 1.52.1 (9bc8c42bb 2021-05-09)

编译程序代码 clap 库部分报

8 | #![doc = include_str!(&quot;..&#47;README.md&quot;)]
  |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

把 Cargo.toml 里 clap 依赖 
clap = &quot;=3.0.0-beta.4&quot;
改为 
clap = &quot;=3.0.0-beta.2&quot; 
clap_derive = &quot;=3.0.0-beta.2&quot;
即可通过 

具体原因 详见 https:&#47;&#47;github.com&#47;dfinity&#47;agent-rs&#47;pull&#47;260</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/4f/e74f870c.jpg" width="30px"><span>Tyr</span> 👍（21） 💬（10）<div>这堂课的源代码可以在这里找到：https:&#47;&#47;github.com&#47;tyrchen&#47;geektime-rust&#47;tree&#47;master&#47;04_httpie</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（54） 💬（3）<div>习惯了 npm install 的可以试试 cargo-edit:

$ cargo install cargo-edit
$ cargo add anyhow colored jsonxf mime
$ cargo add clap --allow-prerelease
$ cargo add reqwest --features json
$ cargo add tokio --features full</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/38/c9/63ea8fe6.jpg" width="30px"><span>Arthur</span> 👍（14） 💬（1）<div>对Rust里的derive, impl, trait等概念，和Java&#47;C++中面向对象编程概念里的封装、继承、方法等概念，有怎样的类比和不同，一直模糊不清，希望老师后面能讲到</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（12） 💬（2）<div>查了下colorize trait的doc (https:&#47;&#47;docs.rs&#47;colored&#47;2.0.0&#47;colored&#47;trait.Colorize.html), 没看到这个trait impl for String啊, 为啥可以call blue on String type呢?
```
format!(&quot;{:?} {}&quot;, resp.version(), resp.status()).blue();
```
老师知道这里面发生了什么转换么?</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（12） 💬（1）<div>疑问：查了下reqwest似乎是依赖tokio运行时的，是否意味着用了reqwest就必须用tokio而不能用其他的运行时比如async-std？</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d1/18/2221fb85.jpg" width="30px"><span>逸风</span> 👍（12） 💬（1）<div>喜欢这样的教学方式！</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/74/d4/38d813f0.jpg" width="30px"><span>Kerry</span> 👍（9） 💬（3）<div>简洁的背后意味着大量的抽象。

而初学者见到这么简洁的代码，会迷惑：”我复制了啥，怎么这么短就跑出这么多功能来？？？“

假以时日，就不禁感叹Rust语言表达力的强大。</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/5e/ccab5336.jpg" width="30px"><span>gzgywh</span> 👍（7） 💬（1）<div>Rust里面的宏感觉跟Python里面的装饰器作用差不多嘛？</div>2021-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/5e/0f/1a204ef7.jpg" width="30px"><span>CR</span> 👍（7） 💬（1）<div>很想知道老师的画图工具都有哪些🤔</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c4/45/88287ede.jpg" width="30px"><span>chinandy</span> 👍（6） 💬（1）<div>大家参考老师写的代码的时候，如果是网页不能正常的美化显示，有可能是网页是UTF8的原因，print_body函数match分支加一个TEXT_HTML_UTF_8判断，        Some(v) if v == mime::TEXT_HTML_UTF_8 || v == mime::TEXT_HTML =&gt; print_syntect(body, &quot;html&quot;),即可。
</div>2021-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/b7/b20ab184.jpg" width="30px"><span>麋鹿在泛舟</span> 👍（6） 💬（1）<div>通过这节课介绍初识rust，对比c++感觉有如下区别:
1. 看起来rust程序编译依赖网络，会编实时编译依赖的库，相应的引入三方包非常方便； 而不像c++要到三方库的网页上去找编译和引用的方式，要适配到自己的平台上。
2. 通过rust、宏和trait等机制把非核心的诸如校验等逻辑隔离在各自的函数中, 大幅度降低了耦合。

所以理论上rust可以写出更加简洁的代码吗？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（6） 💬（1）<div>另外一种运行工程的命令是，cargo run -- post httpbin.org&#47;post a=1 b=2
-- 就相当于 target&#47;debug&#47;httpie</div>2021-09-05</li><br/><li><img src="" width="30px"><span>Geek_2924d7</span> 👍（5） 💬（2）<div>```toml
clap = { version = &quot;3.0.7&quot;, features = [&quot;derive&quot;] } # 修改成这样
```
use clap::{Parser, Subcommand};

#[derive(Debug, Parser)]
#[clap(version = &quot;1.0&quot;, author = &quot;Tyr Chen &quot;)]
&#47;&#47; #[clap(setting( AppSettings::ColoredHelp))]
struct Opts {
    #[clap(subcommand)]
    subcmd: Subcmd,
}

#[derive(Subcommand, Debug)]
enum Subcmd {
    Get(Get),
    Post(Post),
}

#[derive(Parser, Debug)]
struct Get {
    url: String,
}

#[derive(Parser, Debug)]
struct Post {
    url: String,
    body: Vec&lt;String&gt;,
}
fn main() {
    let opts: Opts = Opts::parse();
    println!(&quot;{:?}&quot;, opts);
}
```rust

```</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/11/18/c6b3965c.jpg" width="30px"><span>tider</span> 👍（4） 💬（4）<div>rust 1.56 按教程的代码编译不通过

将Cargo.toml改了下就可以了

[package]
name = &quot;httpie&quot;
version = &quot;0.1.0&quot;
edition = &quot;2021&quot;

# See more keys and their definitions at https:&#47;&#47;doc.rust-lang.org&#47;cargo&#47;reference&#47;manifest.html

[dependencies]
anyhow = &quot;1&quot; # 错误处理
clap = &quot;=3.0.0-beta.4&quot; #命令行解释
clap_derive = &quot;=3.0.0-beta.4&quot;
colored = &quot;2&quot; # 命令终端多彩显示
jsonxf = &quot;1.1&quot; # JSON pretty print 格式化
mime = &quot;0.3&quot; # 处理 mime 类型
reqwest = { verson = &quot;0.11&quot;, features = [&quot;json&quot;]} # HTTP 客户端
tokio = { version = &quot;1&quot;, features = [&quot;full&quot;]} # 异步处理库</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0f/53/92a50f01.jpg" width="30px"><span>徐洲更</span> 👍（4） 💬（2）<div>这节课使用了clap进行命令行解析，我在看clap 的GitHub文档的时候，发现这种derive macros的参数写法应该是3.0.0版本后引进的，相关资料只看到一个exmaple。想知道老师是如何指导clap那么多用法的呢？</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/2b/03/55a85ec1.jpg" width="30px"><span>上弦の月</span> 👍（3） 💬（2）<div>2021年12月10日

rustc --version
rustc 1.56.0 (09c42c458 2021-10-18)

cargo --version
cargo 1.56.0 (4ed5d137b 2021-10-04)

note: `Parser` is imported here, but it is only a trait, without a derive macro

使用了老师 GitHub 上面的最新代码还是报以下错误的同学，直接吧 Cargo.toml 中的 clap，加上 features = [ &quot;derive&quot; ]，来激活其派生宏能力：

clap = { version = &quot;3.0.0-beta.5&quot;, features = [&quot;derive&quot;]} # 命令行解析
</div>2021-12-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/tNAmMmIN8MMCd1Leto5gtH2XhIzVRgAeqe6RJOsibEZtPpQH81MBvxu6xY5pL2fgkqNzgerQwYrmO9U3UYU2Tmw/132" width="30px"><span>Zilr</span> 👍（3） 💬（1）<div>陈老师， 为啥我用win10 powershell 和 cmd 运行的话， 都是乱码？</div>2021-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（3） 💬（3）<div>fn print_body(m: Option&lt;Mime&gt;, body: &amp;String) {
    match m {
        Some(v) if v.to_string().contains(&quot;application&#47;json&quot;) =&gt; {
            println!(&quot;{}&quot;, jsonxf::pretty_print(body).unwrap().cyan())
        }
        _ =&gt; println!(&quot;{}&quot;, body),
    }
}
优化了一下程序。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（3）<div>四个点：
1. rust 要使用 nightly 版；
2. Url 解析，不能有&lt;&gt;，应该是：parse_url(&quot;http:&#47;&#47;abc.xyz&quot;)；
3. print 或者 println 输出换行时，应该是 \n 而不是 \\n；
4. syntect 对于 json 支持是很方便的，参考：https:&#47;&#47;github.com&#47;trishume&#47;syntect&#47;blob&#47;master&#47;examples&#47;syncat.rs。

</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8e/31/28972804.jpg" width="30px"><span>阿海</span> 👍（3） 💬（1）<div>这一期小程序挺好的。上上周刚看完rust官网上的非官方文档，基本能看懂代码，但是要自己写出来就难了。期待下一期</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5d/8c/767f9aa8.jpg" width="30px"><span>任伟</span> 👍（2） 💬（1）<div>评论和正文精彩程度不相上下！</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/af/8b03ce2c.jpg" width="30px"><span>GengTeng</span> 👍（2） 💬（2）<div>结构体里的url直接用url库里的Url类型就行了，用String还得自己检查一遍。</div>2021-09-03</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（2） 💬（2）<div>能否支持HTTPS，rust有什么加解密的库？</div>2021-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/c6/d8/672f1838.jpg" width="30px"><span>王彦霖</span> 👍（1） 💬（4）<div>Result&lt;String&gt;，这种写法编译器不会出错吗</div>2021-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZCkGPSOcvucpfLqRP3aqp3qRpwJKyzjNms4jMwibIkxpjiaszqiazSItCeo3IxqQSFvMDh66XaJ2zw/132" width="30px"><span>JoeyLi666</span> 👍（1） 💬（3）<div>就觉得这个rust真的不稳定，作者的代码没几个月就不能直接运行了，做教学的，不应该拿稳定的代码做讲解吗？</div>2021-12-16</li><br/>
</ul>