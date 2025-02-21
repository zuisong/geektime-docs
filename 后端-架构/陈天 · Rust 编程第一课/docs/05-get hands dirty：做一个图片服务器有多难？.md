你好，我是陈天。

上一讲我们只用了百来行代码就写出了 HTTPie 这个小工具，你是不是有点意犹未尽，今天我们就来再写一个实用的小例子，看看Rust还能怎么玩。

再说明一下，代码看不太懂完全没有关系，先不要强求理解，跟着我的节奏一行行写就好，**先让自己的代码跑起来，感受 Rust 和自己常用语言的区别，看看代码风格是什么样的，就可以了**。

今天的例子是我们在工作中都会遇到的需求：构建一个 Web Server，对外提供某种服务。类似上一讲的 HTTPie ，我们继续找一个已有的开源工具用 Rust 来重写，但是今天来挑战一个稍大一点的项目：构建一个类似 [Thumbor](https://github.com/thumbor/thumbor) 的图片服务器。

## Thumbor

Thumbor 是 Python 下的一个非常著名的图片服务器，被广泛应用在各种需要动态调整图片尺寸的场合里。

它可以通过一个很简单的 HTTP 接口，实现图片的动态剪切和大小调整，另外还支持文件存储、替换处理引擎等其他辅助功能。我在之前的创业项目中还用过它，非常实用，性能也还不错。

我们看它的例子：

```bash
http://<thumbor-server>/300x200/smart/thumbor.readthedocs.io/en/latest/_images/logo-thumbor.png
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/3a/60/6ab05338.jpg" width="30px"><span>大汉十三将</span> 👍（9） 💬（2）<div>这一章学了 3 天， 终于能看懂一点了 ： 
- 1.2:  开始接触, 一脸懵逼, 所有的代码个顶个的都看不懂, 极其痛苦的 1 个半小时
- 1.3:  通过强制自己问 chatgpt: xx 这段代码是干什么用的, 强制自己去熟悉 rust 的相关 library, 终于看懂了一些文件的一部分代码 2 h
- 1.4:  基本把不会的都询问 Chatgpt 整理了一遍, 逻辑上都顺了, 剩下一些小的语法问题需要继续记笔记 1.5 h</div>2023-01-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/ajNVdqHZLLDoDeeNST87MZEdfT8n7yEWp06KsFCTs2ssFh2tbHu413nibrRObOia1Zn9pqiaHgIicVkSHRZM3LHOEA/132" width="30px"><span>葡萄</span> 👍（56） 💬（2）<div>看老师的项目，语言已经不是最重要的了。思路和组织结构真是赏心悦目。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c2/11/323358ed.jpg" width="30px"><span>wzx</span> 👍（21） 💬（1）<div>为什么在main.rs中并没有见到引入：
use tracing_subscriber;
use reqwest;
却可以直接使用？</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（21） 💬（4）<div>最让人无法接受的点：

```shell
du -h -d 1 .&#47;target
395M	.&#47;target&#47;rls
901M	.&#47;target&#47;debug
1.3G	.&#47;target
```</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9d/e8/39433235.jpg" width="30px"><span>Christian</span> 👍（19） 💬（1）<div>感概什么时候才能达到老师这样的高度？</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（15） 💬（1）<div>逻辑清晰，喜欢这种教学方式。从项目，问题入手，也不是纠结于语法细节。</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/00/a4a2065f.jpg" width="30px"><span>Michael</span> 👍（8） 💬（1）<div> Rust，相比起有运行时Go语言，运行效率不再话下。另外，作为现代系统级编程语言，在工程实践，依赖管理，相比起C、C++要好很多，但是比起Go稍微复杂一些。

语言学习难度还是挺大的，很多新概念，新名词都要理解，不过写起来还是挺爽的。用半年实践反复学习实践，希望能啃下这门语言。

希望老师从先行者的角度，对一些难点，易错点，平时不容易接触的到的地方给学生们做下讲解，看书和看网上资料千篇一律，没什么新奇的地方，大多讲的不够透。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/96/81c8cc33.jpg" width="30px"><span>Quincy</span> 👍（8） 💬（2）<div>请问老师还有什么新的图片引擎吗？可以推荐一个吗？在 github 和 crates.io 上没有找到相似的，谢谢老师</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/93/96/81c8cc33.jpg" width="30px"><span>Quincy</span> 👍（8） 💬（2）<div>添加新功能：
1. 首先添加新的 proto
```proto
message PaddingBottom {
  uint32 x = 1;
}

&#47;&#47; 一个 spec 可以包含上述的处理方式之一
message Spec {
  oneof data {
    ...
    Watermark watermark = 7; &#47;&#47; 处理水印
    PaddingBottom  paddingBottom = 8; &#47;&#47; 填充图片
  }
}
```

2. 定义新的 spec然后为 spec 实现 SpecTransform trait 和一些辅助函数


```rust
&#47;&#47; File: 在文件 `pb&#47;mod.rs` 中
&#47;&#47; 提供一些辅助函数，让创建一个 spec 的过程简单一些
impl Spec {
    ...
    pub fn new_padding_bottom(x: u32) -&gt; Self {
        Self {
            data: Some(spec::Data::PaddingBottom(PaddingBottom { x }))
        }
    }
}
```
3. 最后在 Engine 中使用 spec
```rust
impl Engine for Photon {
    fn apply(&amp;mut self, specs: &amp;[Spec]) {
        for spec in specs.iter() {
            match spec.data {
                Some(spec::Data::Crop(ref v)) =&gt; self.transform(v),
                ...
                Some(spec::Data::PaddingBottom(ref v)) =&gt; self.transform(v),
                _ =&gt; {}
...
impl SpecTransform&lt;&amp;PaddingBottom&gt; for Photon {
    fn transform(&amp;mut self, op: &amp;PaddingBottom) {
        let rgba = Rgba::new(255_u8, 255_u8, 255_u8, 255_u8);
        let img = transform::padding_bottom(&amp;mut self.0, op.x, rgba);
        self.0 = img;
    }
}
```
4. 在 main.rs 函数中使用
```rust
&#47;&#47; 调试辅助函数
fn print_test_url(url: &amp;str) {
    use std::borrow::Borrow;
    let spec1 = Spec::new_resize(500, 800, resize::SampleFilter::CatmullRow);
    let spec2 = Spec::new_watermark(20, 20);
    let spec3 = Spec::new_padding_bottom(100); &#47;&#47; new
    let spec4 = Spec::new_filter(filter::Filter::Marine);
    let image_spec = ImageSpec::new(vec![spec1, spec2, spec3, spec4]);
    let s: String = image_spec.borrow().into();
    let test_image = percent_encode(url.as_bytes(), NON_ALPHANUMERIC).to_string();
    println!(&quot;test url: http:&#47;&#47;localhost:3000&#47;image&#47;{}&#47;{}&quot;, s, test_image);
}
```</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/3e/692a93f7.jpg" width="30px"><span>茶底</span> 👍（6） 💬（1）<div>逻辑清晰，泪目了，我咋就这么菜</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/62/e0/d2ff52da.jpg" width="30px"><span>记事本</span> 👍（4） 💬（1）<div>老师，现在只能硬抄，以后会把基础知识都讲一遍的吗？</div>2021-09-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HO3KVBk8wePF8BYoTibKSlpUpBmZl6b1eZV3VftiatM1HjQuh1Fu2Q1QCZgVXQwQxiaDXK7c6dialmEm5l9UibnbicAw/132" width="30px"><span>Geek_ff1914</span> 👍（3） 💬（1）<div>总有一天，我也会像你一样强！</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（2） 💬（1）<div>用opencv-rust实现了fliph，挺艰辛的
https:&#47;&#47;github.com&#47;honwhy&#47;first_rs&#47;tree&#47;opencv&#47;thumbor</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（2） 💬（1）<div>增加了一个油画效果
message Oil {
    int32 radius = 1;
    double intensity = 2;
}
message Spec {
    oneof data {
        Resize resize = 1;
        Crop crop = 2;
        Flipv flipv = 3;
        Fliph fliph = 4;
        Contrast contrast = 5;
        Filter filter = 6;
        Watermark Watermark = 7;
        Oil oil = 8;
    }
}

impl SpecTransform&lt;&amp;Oil&gt; for Photon {
    fn transform(&amp;mut self, op: &amp;Oil) {
        effects::oil(&amp;mut self.0, op.radius, op.intensity);
    }
}

    let spec1 = Spec::new_resize(500, 800, resize::SampleFilter::CatmullRom);
    let spec2 = Spec::new_watermark(20, 20);
    let spec3 = Spec::new_filter(filter::Filter::Marine);
    let spec4 = Spec::new_oil(4, 55.0);
    let image_spec = ImageSpec::new(vec![spec1, spec2, spec3, spec4]);</div>2022-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/95/a4/86c4cb52.jpg" width="30px"><span>ㅤ</span> 👍（2） 💬（1）<div>陈老师，我想问一下  prost这个依赖的tag是有什么作用么？看了文档也不大理解。</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/95/a4/86c4cb52.jpg" width="30px"><span>ㅤ</span> 👍（2） 💬（1）<div>现在处于看得懂的阶段，自己写的话，为什么要引用，这边为什么又不要。。。 只能靠编译硬改</div>2021-09-09</li><br/><li><img src="" width="30px"><span>兴小狸</span> 👍（2） 💬（1）<div>敲了一遍，但还是懵~</div>2021-09-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKBM3Q8ibgwVibREUulIsuRymSqLWQqexMSCOx9aYngDlra5swsvc9IgUkIwibvMX0IerWSwKFcuSzuw/132" width="30px"><span>鱼龙帅</span> 👍（2） 💬（2）<div>为啥我访问的就没有那么快？每次都是要10秒左右才来，显示是有match cache,但是还是都挺久的，哪里的姿势不对</div>2021-09-02</li><br/><li><img src="" width="30px"><span>大哉乾元</span> 👍（2） 💬（3）<div>从嵌入式过来的，涉及到web相关的东西就有点抓瞎，请问下老师这方面除了http协议外一般还需要哪方面的背景知识，有推荐的资料不？</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/ad/4efd929a.jpg" width="30px"><span>老荀</span> 👍（2） 💬（2）<div>我有预感。这会是目前网上最少的Rust中文课程。期待</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/55/3b2526ce.jpg" width="30px"><span>深山何处钟</span> 👍（1） 💬（1）<div>运行cargo build就报这个错误，网上找了很久都没有解决。希望老师帮忙解决：

process didn&#39;t exit successfully: `C:\Users\XWANG270\Videos\thumbor\target\debug\build\thumbor-dd8ed449ce21f347\build-script-build` (exit code: 101)
  --- stderr
  thread &#39;main&#39; panicked at &#39;called `Result::unwrap()` on an `Err` value: Custom { kind: PermissionDenied, error: &quot;failed to invoke protoc (hint: https:&#47;&#47;docs.rs&#47;prost-build&#47;#sourcing-protoc): Access is denied. (os error 5)&quot; }&#39;, build.rs:6:10

意思是我本地没有protoc？</div>2021-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/1a/51/ac2d80fc.jpg" width="30px"><span>苏苏</span> 👍（1） 💬（3）<div> prost_build::Config::new()
failed to resolve: use of undeclared crate or module `prost_build`
not found in `prost_build`rustc</div>2021-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/65/80/52161b2f.jpg" width="30px"><span>Faith信</span> 👍（0） 💬（1）<div>还是看完《Rust权威指南》再来学</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/66/c6/d779dfb6.jpg" width="30px"><span>松松</span> 👍（0） 💬（1）<div>Rust 2018 之后好像不要求非得整个 mod.rs 了</div>2022-01-13</li><br/><li><img src="" width="30px"><span>无下限HENTAI</span> 👍（0） 💬（2）<div>老师好，我在做完`build.rs`之后`cargo build`，但并没有生成`abi.rs`，请问可能原因是什么？
我用的是win10系统，rust版本1.57
目前文件结构如下：
```
C:.
│  .gitignore
│  abi.proto
│  Cargo.lock
│  Cargo.toml
│
└─src
    │  build.rs
    │  main.rs
    │
    └─pb
```
运行cargo build之后，src&#47;pb文件夹中并未出现`abi.rs`，所有文件直接复制您的代码也不行，可能是为什么呢？</div>2022-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/b9/3db96ade.jpg" width="30px"><span>锅菌鱼</span> 👍（0） 💬（1）<div>老师，问个问题，都用http服务器了，这里是不是可以不用protobuf了，把http协议接口的定义好即可？</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/1f/2ef2514b.jpg" width="30px"><span>newzai</span> 👍（0） 💬（1）<div>protobuf 在rust重怎么操作 extensions字段。那个库支持？prost貌似不支持</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/a2/c30ac459.jpg" width="30px"><span>hughieyu</span> 👍（0） 💬（1）<div>请问老师，接口设计中什么情况下用传入`self`的方式每次情况创建一个(文中Engine trait的定义方式)， 什么情况下使用&amp;self的方式全局共享一个(如下)
```rust
pub trait Engine {
    fn handle(&amp;self, image: Vec&lt;u8&gt;, specs: &amp;[Spec]) -&gt; Result&lt;Vec&lt;u8&gt;, anyhow::Error&gt;;
}
```</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/23/15/c06a1586.jpg" width="30px"><span>HeviLUO</span> 👍（0） 💬（1）<div>老师你好，你的图画得很清晰也很好看
是用什么工具画的呢？</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ee/eb/552f5ea6.jpg" width="30px"><span>卢旺达</span> 👍（0） 💬（1）<div>老师你好，github repo 代码里build.rs里的
 let build_enabled = option_env!(&quot;BUILD_PROTO&quot;)
        .map(|v| v == &quot;1&quot;)
        .unwrap_or(false);
BUILD_PROTO怎么赋值成1啊，我试了好多方式，都没成功。</div>2021-11-15</li><br/>
</ul>