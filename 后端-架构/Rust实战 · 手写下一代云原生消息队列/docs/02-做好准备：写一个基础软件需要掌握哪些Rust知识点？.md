> 本课程为精品小课，不标配音频

你好，我是文强。

从这节课开始，我们正式进入实践落地阶段。为了能让你更好地理解本课程后续的内容，我会先带你了解写一个分布式基础软件所需要用到的 Rust 关键知识点。

> Tips：这节课只是起到一个“引导点明”的作用，不会详细展开讲解各个知识点。建议你先根据上节课推荐的资料把 Rust 的相关知识点都过一遍，再来看这节课的内容，会更好理解。

接下来，我整理了一个常用的 Rust 知识点集合（这个信息来源于多份学习资料，我只是做了一下总结）。你可以根据表格来看一下自己对 Rust 的掌握程度，然后查缺补漏。

![](https://static001.geekbang.org/resource/image/1y/f3/1yy72588146f7e15f1502afab537caf3.jpg?wh=1560x1502)

基于上面的表格，接下来我们重点讲一下在编码过程中最常用到且在理解上有一定挑战的几个知识点。

1. 包管理工具：Cargo
2. 生命周期和所有权
3. 泛型和Trait
4. 智能指针
5. 并发编程和Tokio
6. 测试用例

## 包管理工具：Cargo

无论是哪份学习资料，都会告诉你 Cargo 的重要性。在我看来 Cargo 是 Rust 的核心竞争力之一，是学习 Rust 必须完整掌握的知识点。想要学好 Cargo 看这份资料即可[《Cargo 使用指南》](https://course.rs/cargo/intro.html)。

在 Cargo 里面重点关注以下三个命令，掌握后基本就入门了。

![图片](https://static001.geekbang.org/resource/image/71/3c/7178116bc586b5b82374bef833cdb63c.jpeg?wh=1892x533)  
使用示例如下：

```plain
# 用 cargo build 根据 release 标准将项目打包成一个可执行的二进制文件
cargo build --release： 


# 运行名为 mqtt-broker 的这个模块里面的测试用例
cargo test --package mqtt-broker


# 执行 cmd 包中名字为 placement-center 的 bin 的 main 函数，并给这个main函数传递conf参数
cargo run --package cmd --bin placement-center -- --conf=config/placement-center.toml
```