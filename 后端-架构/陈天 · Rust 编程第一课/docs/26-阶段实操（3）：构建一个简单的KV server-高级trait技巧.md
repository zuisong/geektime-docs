你好，我是陈天。

到现在，泛型的基础知识、具体如何使用以及设计理念，我们已经学得差不多了，也和函数作了类比帮助你理解，泛型就是数据结构的函数。

如果你觉得泛型难学，是因为它的抽象层级比较高，需要足够多的代码阅读和撰写的历练。所以，通过学习，现阶段你能够看懂包含泛型的代码就够了，至于使用，只能靠你自己在后续练习中不断体会总结。如果实在觉得不好懂，**某种程度上说，你缺乏的不是泛型的能力，而是设计和架构的能力**。

今天我们就用之前1.0版简易的 KV store 来历练一把，看看怎么把之前学到的知识融入代码中。

在 [21 讲](https://time.geekbang.org/column/article/425001)、[22讲](https://time.geekbang.org/column/article/425005)中，我们已经完成了 KV store 的基本功能，但留了两个小尾巴：

1. Storage trait 的 get\_iter() 方法没有实现；
2. Service 的 execute() 方法里面还有一些 TODO，需要处理事件的通知。

我们一个个来解决。先看 get\_iter() 方法。

## 处理 Iterator

在开始撰写代码之前，先把之前在 src/storage/mod.rs 里注掉的测试，加回来：

```rust
#[test]
fn memtable_iter_should_work() {
    let store = MemTable::new();
    test_get_iter(store);
}
```
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/98/6a/3ddeca6e.jpg" width="30px"><span>losuika</span> 👍（4） 💬（3）<div>rocksdb 的实现 https:&#47;&#47;play.rust-lang.org&#47;?version=stable&amp;mode=debug&amp;edition=2021&amp;gist=1f4b28ff3fcbdb421a0743d47c7b75c3，rocksdb 需要开启 feature multi-threaded-cf ，然后感觉 trait 约束是不是也要改下？需要带上生命周期，rocksdb 库似乎没有办法拿到所有权的迭代器</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/6a/3ddeca6e.jpg" width="30px"><span>losuika</span> 👍（2） 💬（1）<div>Option 有个 transpose ，可以直接 Option&lt;Result&gt; 到 Result&lt;Option&gt;</div>2021-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（1） 💬（1）<div>哈 昨天终于完成 21，22，今天继续</div>2021-10-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIVblkHYeYrgys7iaARHkicbYCZoibE1tJO0C6NEgw1f13RDgVABBgXDSFBzabLIUPNEPdxib1Ep5aYZg/132" width="30px"><span>Geek_e2201d</span> 👍（0） 💬（2）<div>陈老师，我尝试把MemTable与SledDb整合到一个Server中，通过config参数来动态选择MemTable还是SledDb。尝试了很久都失败了，编译器提示错误为:
50 | let resp = service_cloned.execute(msg);
 |    ^^^^^^^ method cannot be called on `Service&lt;Box&lt;dyn Storage&gt;&gt;` due to unsatisfied trait bounds
...
 = note: the following trait bounds were not satisfied:
     `Box&lt;dyn Storage&gt;: Storage`

我的疑问是Box&lt;dyn Storage&gt;为什么不满足Storage呢？

server.rs代码如下: 
use anyhow::Result;
use async_prost::AsyncProstStream;
use futures::prelude::*;
use kv::{CommandRequest, CommandResponse, MemTable, SledDb, Service, Storage};
use tokio::net::TcpListener;
use kv::service::ServiceInner;
use tracing::info;
use clap::{Parser, ArgEnum};

#[derive(Parser)]
#[clap(name = &quot;kv server&quot;)]
struct Cli {
​#[clap(arg_enum, long, short, default_value=&quot;memory&quot;)]
​storage: StorageType,

​#[clap(long, short=&#39;d&#39;, default_value=&quot;.&#47;sled&quot;)]
​sled_dir: String,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ArgEnum)]
enum StorageType {
​Memory,
​Sled,
}

#[tokio::main]
async fn main() -&gt; Result&lt;()&gt; {
​tracing_subscriber::fmt::init();
​let args: Cli = Cli::parse();

​let addr = &quot;127.0.0.1:9527&quot;;
​let listener = TcpListener::bind(addr).await?;
​info!(&quot;Start listening on {}&quot;, addr);

​let db : Box&lt;dyn Storage&gt; = match args.storage {
  ​StorageType::Memory =&gt; Box::new(MemTable::default()),
  ​StorageType::Sled =&gt; Box::new(SledDb::new(args.sled_dir)),
​};

​let service: Service&lt;Box&lt;dyn Storage&gt;&gt; = ServiceInner::new(db).into();
​loop {
 ​let (stream, addr) = listener.accept().await?;
 ​info!(&quot;Client {:?} connected&quot;, addr);
 ​let service_cloned = service.clone();
 ​tokio::spawn(async move {
  ​let mut stream =
   ​AsyncProstStream::&lt;_, CommandRequest, CommandResponse, _&gt;::from(stream).for_async();
  ​while let Some(Ok(msg)) = stream.next().await {
   ​info!(&quot;Got a new command: {:?}&quot;, msg);
   ​let resp = service_cloned.execute(msg);
   ​info!(&quot;Response: {:?}&quot;, resp);
   ​stream.send(resp).await.unwrap();
  ​}
  ​info!(&quot;Client {:?} disconnected&quot;, addr);
 ​});
​}</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/79/ff/1dc5e2f3.jpg" width="30px"><span>无常</span> 👍（0） 💬（1）<div>请问老师，设计和架构应该如何学习，有什么推荐的资料吗？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/12/e4/57ade29a.jpg" width="30px"><span>dva</span> 👍（0） 💬（2）<div>第二题我想到的是，不过这样要改注册函数，看起来怪怪的，不知道老师的方法是什么
pub trait Notify1&lt;Arg,E&gt;{
    fn notify(&amp;self,arg:&amp;Arg)-&gt;Option&lt;E&gt;;
}

impl &lt;Arg,E&gt;Notify1&lt;Arg,E&gt;for Vec&lt;fn(&amp;Arg)-&gt;Option&lt;E&gt;&gt; {
    fn notify(&amp;self, arg: &amp;Arg) -&gt; Option&lt;E&gt; {
        for f in self{
            match f(arg){
                Some(e)=&gt; return Some(e),
                _=&gt;{},
            }
        }
        None
    }
}

第三题和老师写的sleddb差不多，直接加了一些TryFrom，中间遇到没有装llvm clang的错误 “error: failed to run custom build command for `librocksdb-sys ...” 还有起名字 rocksdb和包名冲突。写这个扩展有个非常深的体会就是，编译器提示真好。</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/fb/7fe6df5b.jpg" width="30px"><span>陈卧虫</span> 👍（0） 💬（0）<div>还有人和我一样在学么</div>2025-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/68/45/ddf89612.jpg" width="30px"><span>bestgopher</span> 👍（0） 💬（0）<div>我们服务是异步的，但是sled读取文件没看到异步操作，这样是否有问题呢？</div>2022-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/2a/96b38944.jpg" width="30px"><span>Alvin</span> 👍（0） 💬（5）<div>老师 跟着课程的代码实现过程发现最后持久化存储这边会报个错
 the trait `From&lt;&amp;[u8]&gt;` is not implemented for `abi::Value`</div>2022-04-16</li><br/>
</ul>