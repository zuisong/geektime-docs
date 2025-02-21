你好，我是陈天。

上堂课我们用最原始的方式构建了一个 RawBuilder 派生宏，本质就是从 TokenStream 中抽取需要的数据，然后生成包含目标代码的字符串，最后再把字符串转换成 TokenStream。

说到解析 TokenStream 是个苦力活，那么必然会有人做更好的工具。 [syn](https://github.com/dtolnay/syn)/[quote](https://github.com/dtolnay/quote) 这两个库就是Rust宏生态下处理 TokenStream 的解析以及代码生成很好用的库。

今天我们就尝试用这个 syn / quote工具，来构建一个同样的 Builder 派生宏，你可以对比一下两次的具体的实现，感受 syn / quote 构建过程宏的方便之处。

## syn crate 简介

先看syn。**syn 是一个对 TokenStream 解析的库，它提供了丰富的数据结构，对语法树中遇到的各种 Rust 语法都有支持**。

比如一个 Struct 结构，在 TokenStream 中，看到的就是一系列 TokenTree，而通过 syn 解析后，struct 的各种属性以及它的各个字段，都有明确的类型。这样，我们可以很方便地通过模式匹配来选择合适的类型进行对应的处理。

**syn 还提供了对 derive macro 的特殊支持**——[DeriveInput](https://docs.rs/syn/latest/syn/struct.DeriveInput.html) 类型：

```rust
pub struct DeriveInput {
    pub attrs: Vec<Attribute>,
    pub vis: Visibility,
    pub ident: Ident,
    pub generics: Generics,
    pub data: Data,
}
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/3a/e06f8367.jpg" width="30px"><span>HiNeNi</span> 👍（1） 💬（0）<div>感谢老师加餐！顶顶顶！</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/b0/f9ad2d76.jpg" width="30px"><span>Abc简简简简</span> 👍（0） 💬（0）<div>宏好难🤯  现在看宏只能借助ide的提示来看</div>2024-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>厉害啊</div>2024-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c6/0b/eb3589f1.jpg" width="30px"><span>🐳大海全是水</span> 👍（0） 💬（0）<div>可以把宏生成的代码写到代码文件里吗？如果每次都是编译生成，看不见摸不着不好调试，每次生成也比较耗时。</div>2023-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（0） 💬（0）<div>宏用起来还是挺方便的，就是写起来有点复杂。</div>2023-01-29</li><br/>
</ul>