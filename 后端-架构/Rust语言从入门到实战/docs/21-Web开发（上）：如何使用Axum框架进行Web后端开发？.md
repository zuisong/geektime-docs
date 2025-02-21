你好，我是Mike, 今天我们来讲一讲如何用Axum框架进行Web服务器后端开发。

关于Rust是否适合做Web后端开发，很多人持怀疑态度。认为Web开发讲究的是敏捷，一种动态的、带运行时的、方便修改的语言可能更适合Web开发。

但有一些因素，其实决定了Rust非常适合Web开发。

1. 时代变化：芯片摩尔定律已失效，服务器成本逐渐占据相当大的比例，无脑堆服务器的时代已经过去。当前阶段，对于规模稍微大一些的公司来说，降本增效是一个很重要的任务。而Rust的高性能和稳定可靠的表现非常适合帮助公司节省服务器成本。
2. 随着业务的成型，一些核心业务会趋于稳定，模型和流程抽象已经基本不会有大的改动。这时，使用Rust重写或部分重写这些业务，会带来更强的性能和更可靠稳定的服务表现。
3. Rust非常适合用来做一些通用的中间件服务，目前开源社区已经出现了一些相当优秀的中间件产品。
4. Rust的表达能力其实非常强，其强大的类型系统可帮助开发者轻松地对问题进行建模。一个中等熟练的Rust开发者做原型的速度不会比Python慢多少，在复杂问题场景下，甚至更快。
5. Rust的语言层面的设计使它特别适合做重构。重构Rust工程特别快，重构完后，也不用担心出错的问题。相对于动态语言，对应的测试用例都可以少准备很多。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（3） 💬（1）<div>版本已经更新到 0.7 啦</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/19/c756aaed.jpg" width="30px"><span>鸠摩智</span> 👍（3） 💬（1）<div>windows powershell中的启动命令：$env:RUST_LOG=&quot;debug&quot; ; cargo run 。不设置级别的话，默认看不到debug级别的日志</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/57/a3daeaae.jpg" width="30px"><span>tan</span> 👍（2） 💬（1）<div>时区设置
● cargo add time --features macros
● cargo add tracing-subscriber --features time

```rust
use time::macros::{format_description, offset};
use tracing_subscriber::fmt::time::OffsetTime;

let time_fmt = format_description!(&quot;[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:3]&quot;);
let timer = OffsetTime::new(offset!(+8), time_fmt);


&#47;&#47; init 
tracing_subscriber::fmt().with_max_level(Level::TRACE).with_timer(timer).init();


&#47;&#47; use
tracing::info!(&quot;listening on {}&quot;, listener.local_addr().unwrap());
```
</div>2024-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d5/a9/2cac96a9.jpg" width="30px"><span>一只</span> 👍（2） 💬（1）<div>第一个例子 hello-world 需要使用链接中的依赖版本才能运行，应该是库的接口发生变更了。
或者使用 官方最新例子
```rust
use axum::{response::Html, routing::get, Router};

#[tokio::main]
async fn main() {
    &#47;&#47; build our application with a route
    let app = Router::new().route(&quot;&#47;&quot;, get(handler));

    &#47;&#47; run it
    let listener = tokio::net::TcpListener::bind(&quot;127.0.0.1:3000&quot;)
        .await
        .unwrap();
    println!(&quot;listening on {}&quot;, listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

async fn handler() -&gt; Html&lt;&amp;&#39;static str&gt; {
    Html(&quot;&lt;h1&gt;Hello, World!&lt;&#47;h1&gt;&quot;)
}
```</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/8a/7c1baa25.jpg" width="30px"><span>buoge</span> 👍（1） 💬（1）<div>日志部分配合这个看会更佳
使用 tracing 记录日志：https:&#47;&#47;course.rs&#47;logs&#47;tracing.html</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/ee/33ef689b.jpg" width="30px"><span>土土人</span> 👍（0） 💬（1）<div>Axum ctrl c退出为啥会报错？还有启动线程不会按核数自动分配吗？</div>2024-02-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VF71Gcf2C2bjYPFCRv0TPfwhkJmT5WhtusltuaXQM0KMDibdallNFypqWV6v2FJ4bqNwzujiaF5LEDeia7JMZTTtw/132" width="30px"><span>Geek_e72251</span> 👍（0） 💬（2）<div>tracing输出的日志时区不对，怎么设置时区啊？</div>2023-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1ooqYIZ7khDvoGHWv21vPYECXjd562DM1boWqIUxhyNUic5uyYnfglAjluMZWLZcONtTSib57EAJz4cicm4nBkpug/132" width="30px"><span>Carlsama</span> 👍（0） 💬（1）<div>内容已经调整到0.7了吗？看了评论有点不敢跟着抄写代码，等都更完再一块看</div>2023-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（0） 💬（1）<div>怎么用这个框架实现读取、导出xls或者pdf文件啊？</div>2023-12-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qUHuge7oea6mA4bUTyJ4rpTP7Havj5m2WEqKvrARDbe8HYnu52vQ8DfAWNkLEfQbic83ibDhnUZYRTwut5Dl8icDA/132" width="30px"><span>雍和</span> 👍（0） 💬（1）<div>老师，文中说的evn_logger是不是笔误了呢？实际是env_logger？</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（0） 💬（2）<div>咋没有用最新版的0.7版本啊？</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>错别字： 
carge add tracing-subscriber
</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（2）<div>老师，请问能否介绍最新版本的 axum ?</div>2023-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/05/93/3c3f2a6d.jpg" width="30px"><span>安石</span> 👍（0） 💬（0）<div>并发性能好像没有node的好。。。。</div>2024-06-26</li><br/>
</ul>