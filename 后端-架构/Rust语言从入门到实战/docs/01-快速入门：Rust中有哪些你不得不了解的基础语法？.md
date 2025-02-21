你好，我是Mike。今天是我们的Rust入门与实战第一讲。

无论对人，还是对事儿，第一印象都很重要，Rust也不例外。今天我们就来看一看Rust给人的第一印象是什么吧。其实Rust宣称的安全、高性能、无畏并发这些特点，初次接触的时候都是感受不到的。第一次能直观感受到的实际是下面这些东西。

- Rust代码长什么样儿？
- Rust在编辑器里面体验如何？
- Rust工程如何创建？
- Rust程序如何编译、执行？

下面我们马上下载安装Rust，快速体验一波。

## 下载安装

要做Rust编程开发，安装Rust编译器套件是第一步。如果是在MacOS或Linux下，只需要执行：

```plain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

按提示执行操作，就安装好了，非常方便。

而如果你使用的是Windows系统，那么会有更多选择。你既可以在WSL中开发编译Rust代码，也可以在Windows原生平台上开发Rust代码。

如果你计划在WSL中开发，安装方式与上面一致。

```plain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

如果想在Windows原生平台上开发Rust代码，首先需要确定安装 [32 位的版本](https://static.rust-lang.org/rustup/dist/i686-pc-windows-msvc/rustup-init.exe)还是 [64 位的版本](https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe)。在安装过程中，它会询问你是想安装GNU工具链的版本还是MSVC工具链的版本。安装GNU工具链版本的话，不需要额外安装其他软件包。而安装MSVC工具链的话，需要先安装微软的 [Visual Studio](https://kaisery.github.io/trpl-zh-cn/ch01-01-installation.html) 依赖。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/99/13/2b325b02.jpg" width="30px"><span>学会用实力去谈条件</span> 👍（23） 💬（3）<div>推荐几个Rust的VsCode插件
Rust Syntax：语法高亮
crates：分析项目依赖
Even Better Toml：项目配置管理
Rust Test Lens：Rust快速测试</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/4d/60/1aa99bd9.jpg" width="30px"><span>warning</span> 👍（7） 💬（7）<div>看完了Rust语言圣经，再看这个还感觉有些吃力需要时不时的看看之前的笔记。课程并不适合没接触过Rust的小白，需要自己花些时间去找别的资料进行补充</div>2023-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/b1/7214b986.jpg" width="30px"><span>知夫</span> 👍（4） 💬（2）<div>可以推荐一个项目结构的最佳实践吗？ 能囊括lib，bin，示例，单元测试，性能测试等。</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/06/9811fb65.jpg" width="30px"><span>草剑</span> 👍（3） 💬（1）<div>windows 中，不想安装 visual studio，想使用 gnu 工具链：
rustup default stable-gnu
</div>2023-11-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyhbzdkFM64Npva5ZKf4IPwhy6rDAX0L77QNESbalnXhnGKibcTbwtSaNC0hO6z0icO8DYI9Nf4xwg/132" width="30px"><span>eriklee</span> 👍（3） 💬（4）<div>IDE推荐一波RustRover，jetbrains家新出的，现在免费使用阶段</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/5f/2e620b89.jpg" width="30px"><span>阿五</span> 👍（3） 💬（2）<div>
虽然 Rust 不像 JavaScript 那样具有动态的通用数字类型，但你可以通过使用 num crate 和 Rust 的强类型系统来实现类似的通用数字操作。</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/ad/cf2e924e.jpg" width="30px"><span>Levix</span> 👍（2） 💬（1）<div>https:&#47;&#47;synctoai.com&#47;rustclosures
看了老师的第一节课，然后觉得闭包有点难理解，跑去问了下 GPT 后，整理出来一篇文档，希望对大家有用。</div>2023-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/f1/bd61dbb1.jpg" width="30px"><span>Ransang</span> 👍（2） 💬（2）<div>闭包那个测试里，为什么main函数里面可以有其他函数，就是fn里面套了一个fn ，他们之间有什么关系吗</div>2023-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/52/5205764a.jpg" width="30px"><span>🤔</span> 👍（2） 💬（2）<div>关于char的unicode散列值，gpt4的说明是：
Unicode 是一种字符集（Character Set），用于对世界上大多数语言的字符进行编码。不同于 ASCII 码仅包括了基本的英文字符和控制字符，Unicode 意在包括世界上所有的字符，包括字母、符号、表情符号（emoji）等。

在 Unicode 标准中，每个字符都有一个唯一的标识符，通常称为代码点（Code Point）。这些代码点是用整数表示的，一般用十六进制的形式来展示。例如，英文字母 &quot;A&quot; 的 Unicode 代码点是 U+0041，而中文字符 &quot;中&quot; 的 Unicode 代码点是 U+4E2D。

散列值一般用于描述数据结构中用于快速查找的数值标识，但在这里（Rust 的 char 类型存的是 Unicode &quot;散列值&quot;），这种说法不太准确。实际上，Rust 的 char 类型存储的是 Unicode 代码点。

老师可以解答一下吗</div>2023-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（1） 💬（2）<div>可以说说GNU 工具链的版本 和 MSVC 工具链的版本 有什么区别吗？ 应该怎么选择呢？</div>2024-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（1） 💬（1）<div>老师好
版次是什么？
为什么要 3 年发布一次？
和版本有什么区别？</div>2023-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/10/65fe5b06.jpg" width="30px"><span>J²</span> 👍（1） 💬（1）<div>工作之余，正在艰难抽空学习rust，希望这次能坚持学完并且入门。</div>2023-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/66/42/8a645285.jpg" width="30px"><span>uyplayer</span> 👍（1） 💬（2）<div> println!(&quot;Hello World! this is first commit in Rust&quot;)</div>2023-10-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwIgbTd3oy4ESHr6bX9iblONuwgU0MWHcgxndWwNNRQGXlhicduummSiamfTcxHsicicxR4nElxzj280Q/132" width="30px"><span>Geek_5c44aa</span> 👍（0） 💬（1）<div>语音讲解是不是有问题？都在那段IDE介绍里循环播放</div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5b/69/7ace1ddb.jpg" width="30px"><span>独钓寒江</span> 👍（0） 💬（2）<div>    &#47;&#47; 强行在字符串后面加个0，与C语言的字符串一致。 
    let byte_escape = &quot;I&#39;m saying hello.\0&quot;; 
    println!(&quot;{}&quot;, byte_escape); 

以上的代码，按注释，我理解打印出来的结果是在字符串后显示一个0， 实际打印结果是“I&#39;m saying hello.”
看了一下紧接着的参考文章 -- Tokens - The Rust Reference (rust-lang.org)， \0代表Null， 那输出结果是正常的

可以多说一下“强行在字符串后面加个0”吗？</div>2024-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ac/5c/bb67abe6.jpg" width="30px"><span>林子茗</span> 👍（0） 💬（1）<div>思考题1：采用f64，所有数字类型都转成f64，问题是丢失精度，大整数精度丢失严重。
2：Python数字类型是不可变的Number对象类型，若在Rust中使用结构体来封装数字类型一样可以实现无限大小，但是性能太差、太耗内存。</div>2024-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3a/08/27/0bd80208.jpg" width="30px"><span>xhsndl</span> 👍（0） 💬（1）<div>rust问答题，
构建自定义数据类型？
构建自定义常量？</div>2024-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1b/d3/5cf53a64.jpg" width="30px"><span>脱尼</span> 👍（0） 💬（1）<div>写单元测试的时候 use crate::foo; 会报错编译不通过。请问是啥原因？vscode 中
fn foo() -&gt; i32 {
    10i32
}

#[cfg(test)]
mod tests {
    use crate::foo;

    #[test]
    fn it_works() {
        assert_eq!(foo(), 10i32);
    }
}</div>2024-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1b/d3/5cf53a64.jpg" width="30px"><span>脱尼</span> 👍（0） 💬（1）<div>请教下老师您的代码是用 copilot 辅助写的吗？ 这边发现用 vscode + copilot 输出的code prompt 几乎和您的文章一样的，太赞了！</div>2024-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6e/1b/8ea8f15c.jpg" width="30px"><span>lhy</span> 👍（0） 💬（2）<div>想问下，我现在想在windows上装rustrover，然后远程连接到linux服务器上进行编译调试开发，这种可行吗？   因为不想在本机上去整windows相关的依赖问题。</div>2024-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/4e/71/bdfb050c.jpg" width="30px"><span>月色很美</span> 👍（0） 💬（1）<div>请教下老师，模块管理建议用新的还是2015的呢</div>2023-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/42/58/2286eca6.jpg" width="30px"><span>HdUIprince</span> 👍（0） 💬（2）<div>&quot;Rust 中的字符串字面量都支持换行写，默认把换行符包含进去。&quot;，老师这句话啥意思呀？</div>2023-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6d/2a/6173d3f7.jpg" width="30px"><span>稍后重试</span> 👍（0） 💬（1）<div>cargo 命令行工具 是来Linux终端里面的工具么？</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/cd/e0/7ba3c15d.jpg" width="30px"><span>Mango</span> 👍（0） 💬（1）<div>看了国外rust与java的对比，性能吊打，我就要来学一学，看看怎么个事</div>2023-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fa/3d/89e753be.jpg" width="30px"><span>雅致</span> 👍（0） 💬（1）<div>没有看到 rest 优势的介绍，比如 性能 内存占用 高并发项目当中的实际情况，相比 Java go 的优势有哪些，同样一个服务用 go 和 rest 写资源损耗和性能是否能更优秀</div>2023-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/7c/e91866cf.jpg" width="30px"><span>aloha66</span> 👍（0） 💬（2）<div>&#47;&#47; 闭包的定义2，省略了类型标注
    let add_one_v3 = |x|             { x + 1 };
  Compiling playground v0.0.1 (&#47;playground)
error[E0282]: type annotations needed
报了这个错，现在是需要类型了？？</div>2023-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7f/24/d9fbe1e8.jpg" width="30px"><span>dj_ukyo</span> 👍（0） 💬（1）<div>&quot;强行在字符串后面加个\0，与C语言的字符串一致。&quot;
1. 我没有看到任何内容
2. 是本来就不显示吗？</div>2023-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/1f/dc/682fa185.jpg" width="30px"><span>简爱</span> 👍（0） 💬（1）<div>https:&#47;&#47;blog.csdn.net&#47;qq_42108074&#47;article&#47;details&#47;129250580，Windows 11中搭建Rust环境，使用VS Code做为编辑器</div>2023-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（1）<div>怎么将String类型的字符串分组成单个字符组成的数组，或者按指定字符如逗号，分割成数组？</div>2023-11-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLib098UOLAHuEn82MYuaGibv5hUsgy8MFzo16GG3sSeH3t8O574icAMZG77X9aDqg2nmpDy9iad9OusA/132" width="30px"><span>路</span> 👍（0） 💬（1）<div>不会任何代码，直接就买了，能学会不，需要怎么补充，或者搭配？</div>2023-11-08</li><br/>
</ul>