你好，我是陈天。

终于来到了我们这个 KV server 系列的终章。其实原本 KV server 我只计划了 4 讲，但现在 8 讲似乎都还有些意犹未尽。虽然这是一个“简单”的 KV server，它没有复杂的性能优化 —— 我们只用了一句 unsafe；也没有复杂的生命周期处理 —— 只有零星 'static 标注；更没有支持集群的处理。

然而，如果你能够理解到目前为止的代码，甚至能独立写出这样的代码，那么，你已经具备足够的、能在一线大厂开发的实力了，国内我不是特别清楚，但在北美这边，保守一些地说，300k+ USD 的 package 应该可以轻松拿到。

今天我们就给KV server项目收个尾，结合之前梳理的实战中 Rust 项目应该考虑的问题，来聊聊和生产环境有关的一些处理，按开发流程，主要讲五个方面：配置、集成测试、性能测试、测量和监控、CI/CD。

## 配置

首先在 Cargo.toml 里添加 [serde](https://github.com/serde-rs/serde) 和 [toml](https://github.com/alexcrichton/toml-rs)。我们计划使用 toml 做配置文件，serde 用来处理配置的序列化和反序列化：

```rust
[dependencies]
...
serde = { version = "1", features = ["derive"] } # 序列化/反序列化
...
toml = "0.5" # toml 支持
...
```
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4c/12/f0c145d4.jpg" width="30px"><span>Rayjun</span> 👍（19） 💬（2）<div>老师的工程底子是真的厚，我感觉整个课程下来，学 rust 是其次，更重要的是学到了老师做工程的方法，太棒了</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/ed/3dbe915b.jpg" width="30px"><span>乌龙猹</span> 👍（6） 💬（1）<div>这确实是 Rust 编程的第一课   但确是每一个务实程序员的必修课  在做一项工程时，老师的思维方式拆解问题的方法都毫无保留的分享出来   值得我们反复去阅读  反复理解    等什么时候能达到融会贯通 举一反三的时候  那时候就离 300k 的 package 不远了 </div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ad/67/8563a71f.jpg" width="30px"><span>吴云阁</span> 👍（5） 💬（1）<div>这节课的内容不仅仅是rust编程，更是毫无保留的分享工程方法。老师不仅仅是一个极其优秀的工程师，也是一个极其优秀的教学者。非常值得学习。</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1b/11/7d96bff5.jpg" width="30px"><span>yyxxccc</span> 👍（4） 💬（1）<div>看到300k的pkg，又增加了持续反复啃的动力😂</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>实操项目 120 分，我要抽出连续时间好好完成这个项目，该专栏真的值得看十遍。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ef/e2/df2a1823.jpg" width="30px"><span>楠楠嘻嘻</span> 👍（0） 💬（1）<div>确实厉害！真的是rust in action！</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（1） 💬（0）<div>思考题实现：https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=d6037374ea479690681fecf425424cbb
</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/72/f8e5b97e.jpg" width="30px"><span>啦啦啦啦啦啦啦</span> 👍（1） 💬（2）<div>想问下老师在跑 性能测试在 mac下 不会抛出 `Too many open files (os error 24)` 错误吗</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/07/03/5649301e.jpg" width="30px"><span>风吟</span> 👍（0） 💬（0）<div>“在有 100 个 subscribers 的情况下，我们的 KV server 每秒钟可以处理 714k publish 请求”。陈老师，这里“714k”中的k怎么算的，不应该是每秒钟可以处理714个请求吗？</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/6d/ad719e86.jpg" width="30px"><span>心看世界</span> 👍（0） 💬（0）<div>真的，真的，真的不错，感谢老师的分享。</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c6/0b/eb3589f1.jpg" width="30px"><span>🐳大海全是水</span> 👍（0） 💬（0）<div>jaeger官网上有提供mac上的可执行程序：jaeger-all-in-one，把这个程序启动起来就可以看jaeger UI了，不需要用docker</div>2023-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2f/d8/3f9db19f.jpg" width="30px"><span>周杨</span> 👍（0） 💬（0）<div>原来这门课程的门槛那么高呀，我感觉还需要多学几遍呢</div>2022-11-25</li><br/>
</ul>