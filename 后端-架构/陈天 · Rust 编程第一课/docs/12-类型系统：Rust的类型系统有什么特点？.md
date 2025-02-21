你好，我是陈天。今天我们就开始类型系统的学习。

如果你用 C/Golang 这样不支持泛型的静态语言，或者用 Python/Ruby/JavaScript 这样的动态语言，这个部分可能是个难点，希望你做好要转换思维的准备；如果你用 C++/Java/Swift 等支持泛型的静态语言，可以比较一下 Rust 和它们的异同。

其实在之前的课程中，我们已经写了不少 Rust 代码，使用了各种各样的数据结构，相信你对 Rust 的类型系统已经有了一个非常粗浅的印象。那类型系统到底是什么？能用来干什么？什么时候用呢？今天就来一探究竟。

作为一门语言的核心要素，类型系统很大程度上塑造了语言的用户体验以及程序的安全性。为什么这么说？因为，在机器码的世界中，没有类型而言，指令仅仅和立即数或者内存打交道，内存中存放的数据都是字节流。

所以，可以说**类型系统完全是一种工具**，编译器在编译时对数据做静态检查，或者语言在运行时对数据做动态检查的时候，来保证某个操作处理的数据是开发者期望的数据类型。

现在你是不是能理解，为什么Rust类型系统对类型问题的检查格外严格（总是报错）。

## 类型系统基本概念与分类

在具体讲 Rust 的类型系统之前，我们先来澄清一些类型系统的概念，在基本理解上达成一致。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/54/c6/c2481790.jpg" width="30px"><span>lisiur</span> 👍（90） 💬（20）<div>思考题代码报错的主要原因是，实现 new 方法时，对泛型的约束要求要满足 W: Write，而 new 的声明返回值是 Self，也就是说 self.wirter 必须是 W: Write 类型(泛型)，但实际返回值是一个确定的类型 BufWriter&lt;TcpStream&gt;，这不满足要求。

修改方法有这么几个思路

1. 修改 new 方法的返回值

```rust
impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(addr: &amp;str) -&gt; MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt; {
        let stream = TcpStream::connect(addr).unwrap();
        MyWriter {
            writer: BufWriter::new(stream),
        }
    }
}

fn main() {
    let mut writer = MyWriter::&lt;BufWriter&lt;TcpStream&gt;&gt;::new(&quot;127.0.0.1:8080&quot;);
    writer.write(&quot;hello world!&quot;);
}
```

2. 对确定的类型 MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt;实现 new 方法：

```rust
impl MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt; {
    pub fn new(addr: &amp;str) -&gt; Self {
        let stream = TcpStream::connect(addr).unwrap();
        Self {
            writer: BufWriter::new(stream),
        }
    }
}

fn main() {
    let mut writer = MyWriter::new(&quot;127.0.0.1:8080&quot;);
    writer.write(&quot;hello world!&quot;);
}
```

3. 修改 new 方法的实现，使用依赖注入

```rust
impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(writer: W) -&gt; Self {
        Self {
            writer,
        }
    }
}

fn main() {
    let stream = TcpStream::connect(&quot;127.0.0.1:8080&quot;).unwrap();
    let mut writer = MyWriter::new(BufWriter::new(stream));
    writer.write(&quot;hello world!&quot;);
}
```

PS：第2种解法还可以对不同具体类型实现多个new方法：

```rust
impl MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt; {
    pub fn new(addr: &amp;str) -&gt; Self {
        let stream = TcpStream::connect(addr).unwrap();
        Self {
            writer: BufWriter::new(stream),
        }
    }
}

impl MyWriter&lt;File&gt; {
    pub fn new(addr: &amp;str) -&gt; Self {
        let file = File::open(addr).unwrap();
        Self { writer: file }
    }
}

fn main() {
    let mut writer = MyWriter::&lt;BufWriter&lt;TcpStream&gt;&gt;::new(&quot;127.0.0.1:8080&quot;);
    writer.write(&quot;hello world!&quot;);

    let mut writer = MyWriter::&lt;File&gt;::new(&quot;&#47;etc&#47;hosts&quot;);
    writer.write(&quot;127.0.0.1 localhost&quot;);
}
```</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（22） 💬（4）<div>老师你好，这里遇到一个需求，就是想实现一个类似二维动态数组的，然后数组里面的元素是一个指针，指向另外一个随机数组，因为这里是同事强制要求的，后面调用了一个封装第三方的C库接口，因此这里我的代码实现思路如下所示:


代码:

let mut data :Vec&lt;* const u8&gt; = Vec::new();

for i in 0..5{
    let mut num: Vec&lt;u8&gt;= Vec::new();
    for i in 0..16 {
        unsafe{
            let rand_num :u8 = rand::thread_rng().gen();
            num.push(rand_num)
        }
    }
    println!(&quot;num is : {:?},num.as_ptr(): {:?}&quot;,num,num.as_ptr());
    data.push(num.as_ptr());
}

println!(&quot;data is: {:?}&quot;,data);


结果:
num is : [248, 69, 170, 238, 134, 89, 77, 32, 116, 106, 68, 213, 113, 19, 213, 231],num.as_ptr(): 0x7ff6ec000bc0
num is : [138, 101, 105, 192, 81, 32, 133, 80, 94, 6, 205, 164, 178, 95, 60, 45],num.as_ptr(): 0x7ff6ec000bc0
num is : [204, 173, 46, 246, 72, 25, 171, 186, 167, 175, 154, 4, 219, 78, 78, 227],num.as_ptr(): 0x7ff6ec000bc0
num is : [252, 123, 170, 107, 232, 186, 203, 91, 130, 11, 92, 48, 39, 36, 10, 193],num.as_ptr(): 0x7ff6ec000bc0
num is : [143, 52, 155, 135, 50, 50, 133, 105, 143, 62, 120, 125, 88, 58, 99, 19],num.as_ptr(): 0x7ff6ec000bc0
data is: [0x7ff6ec000bc0, 0x7ff6ec000bc0, 0x7ff6ec000bc0, 0x7ff6ec000bc0, 0x7ff6ec000bc0]

搞不明白的是，这里为什么new了之后，还是会导致地址不变，有没有办法强制让变量num每次new之后就是会改变的？多谢了</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/2d/a0d6a610.jpg" width="30px"><span>荒野林克</span> 👍（11） 💬（1）<div>老师，这里有一个疑惑：
```impl&lt;W: Write&gt; MyWriter&lt;W&gt;``` 
里，impl 后面以及指明约束，为什么 MyWriter 后面还要单独写一次呢？</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（3） 💬（3）<div>追老师的更新比追剧有趣多了，配合张老师的视频课，还有陈老师 B 站的 Rust 培训视频，真的很舒服。</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（2） 💬（1）<div>fn main() {
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let even_numbers = numbers
        .into_iter()
        .filter(|n| n % 2 == 0)
        .collect();
    println!(&quot;{:?}&quot;, even_numbers);
}


请教一下这段代码为什么就无法推导类型呢？对于编译器来说，应该是知道number是vec的呀。不太懂，这里可能是我对编译原理理解不够扎实。</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f7/1b/db7a0edc.jpg" width="30px"><span>Marvichov</span> 👍（2） 💬（1）<div>W会被resolve成一个实际类型, 也就是`BufferWriter::new(stream)`的类型. 而rust要求W是一个泛型. 我的下面的改动有点多...

有一点我就有点不明白了, 声明的时候都说了W: Write, 为啥impl的时候还要说一遍呢 (不说不让编译)? 

```
use std::io::{BufWriter, Write};
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W&gt;
where
    W: Write,
{
    writer: BufWriter&lt;W&gt;,
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(stream: W) -&gt; Self {
        Self {
            writer: BufWriter::new(stream),
        }
    }

    pub fn write(&amp;mut self, buf: &amp;str) -&gt; std::io::Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())
    }
}

fn main() {
    let addr = &quot;127.0.0.1:8080&quot;;
    let stream = TcpStream::connect(addr).unwrap();
    let mut writer = MyWriter::new(stream);
    writer.write(&quot;hello world!&quot;).unwrap();
}
```</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（1）<div>不确定最后的代码里为什么要用泛型，改了几个不同的版本：

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=f21447a10eac4e3b77d39aefbd93ab6b

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=2d8037d4059efe15c3d15cfa2267bb70

https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=c57f2abe9756bf021241c63e1b944af8</div>2021-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3d/be/98bebd57.jpg" width="30px"><span>c4f</span> 👍（1） 💬（1）<div>不能编译是因为第 14 行 writer 期待的值的类型也是 W，但收到的却是 BufWriter&lt;TcpStream&gt; 因此不匹配。
参考 MyReader 进行了修改，不过这种方法修改了 MyWriter 对外提供的接口（new），应该还有别的方法，不过没找出来 hh

```

use std::io::{BufWriter, Write};
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W&gt; {
    writer: W,
}

impl&lt;W&gt; MyWriter&lt;W&gt; {
    pub fn new(writer: W) -&gt; Self {
        Self {
            writer
        }
    }
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn write(&amp;mut self, buf: &amp;str) -&gt; std::io::Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())
    }
}

fn main() {
    let mut writer = MyWriter::new(
        BufWriter::new(TcpStream::connect(&quot;127.0.0.1:8080&quot;).unwrap())
    );
    writer.write(&quot;hello world!&quot;).unwrap();
}
```

另外还有一个问题想请教老师：通过在冒号后面对范型进行限制和使用 where 对范型进行限制是否是等价的。比如下面的例子

```
impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    ...
}

impl&lt;W&gt; MyWriter&lt;W&gt;
where
    W: Write
{
    ...
}
```
</div>2021-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OEZQyDeZd2oCPZiak19FKQOZI4I21WjLlwUgJzVFxyXsVKbIlpEEEYZcHbA4lYVzFbd3CtmDfZuUictW3ujvKnUQ/132" width="30px"><span>随风wli</span> 👍（0） 💬（1）<div>老师，因为单态化，代码以二进制分发会损失泛型的信息，这里以二进制分发是指库代码编译成了类似可执行文件，然后rust直接调用吗</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/e4/aa/811ff4d7.jpg" width="30px"><span>Geek_2b06a7</span> 👍（0） 💬（1）<div>文中说 Rust 是显式静态类型，支持作用域内的类型推导，而 ML 和 Haskell 是隐式类型。
这其中的差异提现在什么地方？我没有明白他们类型系统的差异。</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（0） 💬（2）<div>老师你在对“核桃”的解答中说：
“as_ptr() 拿到的是栈上的指针，你应该需要堆上指向实际内容的指针。所以应该用 Vec::into_boxed_slice(), 然后再用 Box::into_raw 拿到裸指针。”
1. 没看明白啊，as_ptr() 怎么就是栈上的指针了？看下面的代码，打印出来明明都是同一个地址啊...
https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=5b74ccf59b05b507d588e5e0297f9448
那你所说的5个地址相同的原因就不成立了，那么到底是怎么回事儿呢？

我发现在你的代码中真正起作用的是 `Box::into_raw(boxed)` 这个表达式……

2. 还有 Vec&lt;*const u8&gt; 可以理解为指向数组的首元素啊……为啥不行呢……</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bc/2c/963688bb.jpg" width="30px"><span>noisyes</span> 👍（0） 💬（2）<div>代码不以二进制分发就没问题吧</div>2021-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f3/61/8f7fca5b.jpg" width="30px"><span>史双龙</span> 👍（0） 💬（1）<div>有点要跟不上节奏了，改了半天，跟榜一大佬差不多。
use std::io::{BufWriter, Write};
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W&gt; {
    writer: W,
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(addr: &amp;str) -&gt; MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt; {
        let stream = TcpStream::connect(addr).unwrap();
        MyWriter {
            writer: BufWriter::new(stream),
        }
    }

    pub fn write(&amp;mut self, buf: &amp;str) -&gt; std::io::Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())
    }
}

fn main() {
    let mut writer = MyWriter::&lt;BufWriter&lt;TcpStream&gt;&gt;::new(&quot;127.0.0.1:8080&quot;);
    writer.write(&quot;hello world!&quot;).unwrap();
}</div>2021-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（0） 💬（3）<div>改进了看符不符合要求，记事本写的
use std::io::{BufWriter,Write};
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W:Write&gt;{
    writer:BufWriter&lt;W&gt;
}

impl &lt;W:Write&gt;  MyWriter&lt;W&gt; {
    pub fn new(stram:W) -&gt;Self {
        Self { 
            writer: BufWriter::new(stram)
        }
    }

    pub fn write(&amp;mut self,s:&amp;str) -&gt;std::io::Result&lt;()&gt; {
        self.writer.write_all(s.as_bytes())   
    }
}
fn main() {

    let addr = &quot;127.0.0.1:8001&quot;;
    let stream = TcpStream::connect(addr).unwrap();
    let mut s =  MyWriter::new(stream);
    s.write(&quot;hello world&quot;);

}
</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/b2/9223bc53.jpg" width="30px"><span>Fenix</span> 👍（0） 💬（1）<div>想问下，看到各种文章都说python是强类型的语言呀</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>为什么中间的图上写着Haskell&#47;ML不能自动推导...类型推导可是ML系语言的标配</div>2021-09-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83equY82MMjfvGtzlo8fhT9fdKO5LjWoy0P8pfCmiaFJS0v8Z4ibzrmwHjib9CnmgMiaYMhPyja7qS6KqiaQ/132" width="30px"><span>Geek_004fb2</span> 👍（1） 💬（1）<div>BufWriter的源码有 impl&lt;W: Write&gt; Write for BufWriter&lt;W&gt; ,而TcpStream源码 impl Write for TcpStream  也实现了 Write,那么 也就是说BufWriter&lt;TcpStream&gt; 也实现了Write,所以这里不太明白为什么BufWriter&lt;TcpStream&gt;不符合本例中 W: Write的限定?请老师详解一下</div>2022-11-14</li><br/><li><img src="" width="30px"><span>Geek_8397eb</span> 👍（0） 💬（0）<div>pub struct GasSceneObj
{
    m_id: PythonObjID,
    m_cfg: SceneCfg,
    m_dictFightObj: HashMap&lt;PythonObjID, GasFightObj&gt;,
    m_dictFightObjAoiProperty: HashMap&lt;PythonObjID, GasFightObjAoiPropery&gt;,
    m_nLatestUpdate: i64,
    m_aoiState: AoiAlg,
}
请教一下老师，在同一个编译环境，同一份代码，编译出来的两个动态库的这个struct内存布局是一致的么？</div>2025-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/16/08/4f7144e5.jpg" width="30px"><span>璐璐two*^_^*</span> 👍（0） 💬（0）<div>我们 没有 TS 的身影</div>2024-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/6b/b813362b.jpg" width="30px"><span>陈溯</span> 👍（0） 💬（0）<div>思考题使用dynamic object的几个可编译的版本：
# https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=278e3bb623010d6e5e1546fef5c5e0e6
# https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=c57f2abe9756bf021241c63e1b944af8
# https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=34d98af4dc703ff0f25b4490742a881f
# https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2018&amp;gist=f21447a10eac4e3b77d39aefbd93ab6b</div>2024-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/f5/a9054651.jpg" width="30px"><span>ADkun</span> 👍（0） 💬（0）<div>问题解决：
```rust
use std::io::Write;
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W: Write&gt; {
    writer: W,
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(writer: W) -&gt; Self {
        Self { writer }
    }

    pub fn write(&amp;mut self, buf: &amp;str) -&gt; std::io::Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())
    }
}

fn main() {
    let stream = TcpStream::connect(&quot;127.0.0.1:8080&quot;).unwrap();
    let mut writer = MyWriter::new(stream);
    writer.write(&quot;hello world!&quot;);
}
```</div>2024-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/3c/70d30681.jpg" width="30px"><span>EEEEEEEarly</span> 👍（0） 💬（1）<div>fn id(x: T) -&gt; T { return x;}
 泛型不是要指定类型吗，没有类型，编译器不知道类型大小，为什么这里可以编译通过呢</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ff/d8/d48d6088.jpg" width="30px"><span>一个人旅行</span> 👍（0） 💬（0）<div>查看源码，Cell和RefCell并没有实现Deref trait，那怎么被称为只能指针呢？</div>2023-08-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM6Vj0BdiciajkSaFO0liaOCOgZC80WdkR3NvDMuaPBxfC0QPj3jHticgptVeenug06NjwY9qZW7KaG4eA/132" width="30px"><span>Geek_0d9ed6</span> 👍（0） 💬（0）<div>C语言中，void *指针就是最强大的泛型（手动狗头）</div>2023-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/a8/66/1a55d1d8.jpg" width="30px"><span>MindfulCoder</span> 👍（0） 💬（0）<div>思考题：

use std::io::{BufWriter, Write};
use std::net::TcpStream;

#[derive(Debug)]
struct MyWriter&lt;W&gt; {
    writer: W,
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(writer: W) -&gt; Self {
        Self {
            writer
        }
    }

    pub fn write(&amp;mut self, buf: &amp;str) -&gt; std::io::Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())
    }
}

fn main() -&gt; std::io::Result&lt;()&gt; {
    let stream = TcpStream::connect(&quot;127.0.0.1:8080&quot;).unwrap();
    let mut writer= MyWriter::new(BufWriter::new(stream));
    writer.write(&quot;hello world!&quot;)
}</div>2023-06-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eojp8oEsjiaDGQtTOZfLDf4m2R2SeibjgMHW9UHvKj0BaCtIGlu7ubbT41Hz1hXFhyib6o25p6LCWtNw/132" width="30px"><span>Geek_4dee8e</span> 👍（0） 💬（0）<div>impl&lt;W:Write&gt; 是限定了 MyWriter.writer的类型必须是Write类型的值，而代码中writer所得到的值时BufWriter&lt;TcpStream&gt;类型的值，所以编译器会报错。</div>2023-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/M8pharAAQmYuic3ibnLWF8sl7H0jpoVJB1Rvyoib7YRGsBdFxcaOMSOrsYDA1iaaauK5CBfoF04X0xDvu7shE0GL5w/132" width="30px"><span>Geek_0aaa22</span> 👍（0） 💬（0）<div>struct MyWriter&lt;W&gt; {
    writer: W,
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn new(writer: W) -&gt; Self {
        Self { writer }
    }
}

impl MyWriter&lt;BufWriter&lt;TcpStream&gt;&gt; {
    pub fn new_from_addr(addr: &amp;str) -&gt; Self{
        let stream = TcpStream::connect(addr).unwrap();
        Self {
            writer: BufWriter::new(stream),
        }
    }
}

impl&lt;W: Write&gt; MyWriter&lt;W&gt; {
    pub fn write(&amp;mut self, buf: &amp;str) -&gt; Result&lt;()&gt; {
        self.writer.write_all(buf.as_bytes())?;
        Ok(())
    }
}</div>2022-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ea/2e/814b2d61.jpg" width="30px"><span>Freedom</span> 👍（0） 💬（0）<div>fn te&lt;T:Copy&gt;(t: T) -&gt; T {
    return 2;
}

fn main() {

    let b = te::&lt;&amp;str&gt;(&quot;hello&quot;);
}

类似于这种情况，应该还是单态化的问题</div>2022-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/a9/688b9bc6.jpg" width="30px"><span>菅田</span> 👍（0） 💬（0）<div>思考题代码报错，为什么实际返回值类型 BufferWrite&lt;TcpStream&gt; 不会被自动推导成泛型 W: Write 呢？</div>2022-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/56/19/d2c65c01.jpg" width="30px"><span>星海</span> 👍（0） 💬（0）<div>Result&lt;_,Error&gt;和Result&lt;(),Error&gt;等价吗？</div>2022-03-13</li><br/>
</ul>