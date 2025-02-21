> 本课程为精品小课，不标配音频

你好，我是文强。

这节课开始，我们就正式来写消息队列架构中的元数据集群部分。首先我们需要初始化一个项目，接下来我会详细讲解如何组织项目结构，以及如何编译打包 Rust 项目。

## Rust 的 bin、lib 和 mod

在初始化项目之前，我们先来学习 3 个基础概念，cargo 中的 bin、lib、mod。

在 Rust 中，项目代码是通过 bin、lib、mod 这三种形式来组织的，先介绍下它们的功能。

**1. bin**

用来存放主入口 main 函数的目录。如下所示，它是通过 cargo.toml 中的 \[\[bin]] 语法指定的。name 表示编译生成的二进制文件的名称，path 表示主入口 main 函数所在的文件。当然，你可以在 cargo 文件中指定多个 \[\[bin]] ，生成多个目标二进制文件。

```plain
[[bin]]
name = "placement-center"
path = "src/placement-center/server.rs"


[[bin]]
name = "placement-center1"
path = "src/placement-center/server1.rs"


```

**2. lib**

这是 Library 的简写，表示功能库的集合。比如我们有一批通用的功能，就可以通过 lib 来组织，封装成一个独立的 lib，给其他项目调用。在 [https://crates.io/](https://crates.io/) 上的各种基础功能库都是lib 的形式。从功能来看，Rust 中 lib 的概念相当于 Java Maven 中的 module。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/c7/8c2d0a3d.jpg" width="30px"><span>余泽锋</span> 👍（0） 💬（0）<div>老师，您好，《Good First Issue》点击进去发现是 404 not found 的错误。</div>2025-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/70/cdef7a3d.jpg" width="30px"><span>Joe Black</span> 👍（0） 💬（0）<div>针对推荐的目录结构，编译结果不是还存在工作空间下的target目录下吗？那个bin目录怎么放项目启动命令？自己拷贝进去吗？</div>2024-10-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2giaUb5iczia7HciagrnDoo4hSSZKFQT0VXKyjE9eBb2FzBGvD2qoU0icS3WYRvN15BM6iaicW9cOTmewDHrDvFPIIcLQ/132" width="30px"><span>Shopman</span> 👍（0） 💬（0）<div>windows下编译就卡住了，主要卡在了rocksdb这，是不是这个项目不支持windows</div>2024-09-27</li><br/>
</ul>