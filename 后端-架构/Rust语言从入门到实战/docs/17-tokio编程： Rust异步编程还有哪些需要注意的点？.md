你好，我是Mike。前面几节课，我们学习了Rust异步编程和tokio的基础知识，我们先来简单回顾下。

1. `async/.await` 语法
2. tokio基本概念和组件
3. 使用tokio编写一个网络并发应用
4. 使用Arc和Mutex在多个task之间共享数据
5. 在并发task之间使用Channel传递数据

通过学习这些内容，你应该已经能使用tokio开发Rust异步并发应用了。这节课，我们对Rust异步并发相关的知识点来做一点补遗。

## async其他知识点

Rust代码中的async函数，其实和Rust的普通函数是不相容的。async Rust就好像是Rust语言里的一个独立王国。

### async代码的传染性

Rust async代码具有传染性。前面我们给出了使用 `async/.await` 的两条规则。

1. async函数或block只有被 `.await` 后才被驱动。
2. `.await` 只能在async函数或block中使用。

这就导致在业务代码中（非tokio那个顶层Runtime代码），如果你需要调用一个async函数，那么你也需要让你现在这个调用者函数也是async的，你可以看我给出的这个例子。

```plain
// 我们定义foo1为一个异步函数
async fn foo1() -> u32 {
  100u32
}
// 我需要在foo2函数中调用foo1，那么这个foo2也必需要是async函数
async fn foo2() -> u32 {
  foo1().await
}
// 我需要在foo3函数中调用foo2，那么这个foo3也必需要是async函数
async fn foo3() -> u32 {
  foo2().await
}

#[tokio::main]
async main() {
  let num = foo3().await;
  println!("{}", num);
}
```
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/23/5c74e9b7.jpg" width="30px"><span>$侯</span> 👍（3） 💬（1）<div>老师，新的1.75是不是支持asnyc trait了</div>2023-12-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（1） 💬（1）<div>期待axum的实战</div>2023-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/00/a4a2065f.jpg" width="30px"><span>Michael</span> 👍（1） 💬（2）<div>等了一个周末就7分钟的课程，而且最近几节将tokio的内容相对有点不充实，既然是进阶篇，异步这一块把 Future、Executor 的实现原理带着分析下。</div>2023-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/07/93/710c7ee2.jpg" width="30px"><span>不忘初心</span> 👍（1） 💬（1）<div>每天能更新一节就好了, 隔天更新拖的时间太长了</div>2023-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（1）<div>期待老师的实战课程</div>2023-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/15/0e/a0a26779.jpg" width="30px"><span>青云</span> 👍（1） 💬（0）<div>这几个RUST专栏里面最适合入门的</div>2024-10-25</li><br/>
</ul>