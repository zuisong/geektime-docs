你好，我是陈天。

上篇我们的KV store刚开了个头，写好了基本的接口。你是不是摩拳擦掌准备开始写具体实现的代码了？别着急，当定义好接口后，先不忙实现，在撰写更多代码前，我们可以从一个使用者的角度来体验接口如何使用、是否好用，反观设计有哪些地方有待完善。

还是按照上一讲定义接口的顺序来一个一个测试：首先我们来构建协议层。

### 实现并验证协议层

先创建一个项目：`cargo new kv --lib`。进入到项目目录，在 Cargo.toml 中添加依赖：

```rust
[package]
name = "kv"
version = "0.1.0"
edition = "2018"

[dependencies]
bytes = "1" # 高效处理网络 buffer 的库
prost = "0.8" # 处理 protobuf 的代码
tracing = "0.1" # 日志处理

[dev-dependencies]
anyhow = "1" # 错误处理
async-prost = "0.2.1" # 支持把 protobuf 封装成 TCP frame
futures = "0.3" # 提供 Stream trait
tokio = { version = "1", features = ["rt", "rt-multi-thread", "io-util", "macros", "net" ] } # 异步网络库
tracing-subscriber = "0.2" # 日志处理

[build-dependencies]
prost-build = "0.8" # 编译 protobuf
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d2/1f/2ef2514b.jpg" width="30px"><span>newzai</span> 👍（15） 💬（3）<div>dev-dependencies 与 dependencies的第三方crate是如何划分的?tokio 为啥不放到 dependencies? 放到 dependencies 与 dev-dependencies 有啥区别？某些如何决策一个 crate放到哪个 dependencies？</div>2021-10-11</li><br/><li><img src="" width="30px"><span>Geek_b52974</span> 👍（7） 💬（1）<div>为何不是这样设计

  fn set(&amp;self, table: &amp;str, key: String, value: impl Into&lt;Value&gt;) 

这样以来就可以让使用者知道他有一个新的type 需要存时应该 implement 这个 trait 也不会让使用时需要一直 写into</div>2021-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/7c/f6/028f80a8.jpg" width="30px"><span>施泰博</span> 👍（6） 💬（1）<div>用powershell的。RUST _LOG=info。改成$env:RUST_LOG=&quot;info&quot;;然后再cargo run</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（4） 💬（1）<div>老师，get_all接口为什么不好？</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/6a/3ddeca6e.jpg" width="30px"><span>losuika</span> 👍（3） 💬（1）<div>感觉 get_iter 加上生命周期的约束好一些，因为现在 GAT 还没稳定，可以这样实现下，
fn get_iter&lt;&#39;a&gt;(
    &amp;&#39;a self,
    table: &amp;str,
) -&gt; Result&lt;Box&lt;dyn Iterator&lt;Item = crate::Kvpair&gt; + &#39;a&gt;, crate::KvError&gt; {
    let table = self.get_or_create_table(table);
    let inner = Iter::new(table);
    Ok(Box::new(inner))
}

struct Iter&lt;&#39;a&gt; {
    _table: *const Ref&lt;&#39;static, String, DashMap&lt;String, Value&gt;&gt;,
    inner: dashmap::iter::Iter&lt;&#39;a, String, Value&gt;,
}

impl&lt;&#39;a&gt; Iter&lt;&#39;a&gt; {
    fn new(table: Ref&lt;&#39;a, String, DashMap&lt;String, Value&gt;&gt;) -&gt; Self {
        let t = unsafe {std::mem::transmute::&lt;Ref&lt;&#39;a, String, DashMap&lt;String, Value&gt;&gt;, Ref&lt;&#39;static, String, DashMap&lt;String, Value&gt;&gt;&gt;(table)};
        let _table = Box::leak(Box::new(t)) as *const Ref&lt;&#39;static, String, DashMap&lt;String, Value&gt;&gt;;

        let inner = unsafe {(*_table).iter()};
        Self {_table, inner}
    }
}

impl&lt;&#39;a&gt; Iterator for Iter&lt;&#39;a&gt; {
    type Item = crate::Kvpair;

    fn next(&amp;mut self) -&gt; Option&lt;Self::Item&gt; {
        let item = self.inner.next();
        item.map(|v| crate::Kvpair::new(v.key(), v.value().clone()))
    }
}

impl&lt;&#39;a&gt; Drop for Iter&lt;&#39;a&gt; {
    fn drop(&amp;mut self) {
        unsafe { drop_in_place(self._table as *mut Ref&lt;&#39;a, String, DashMap&lt;String, Value&gt;&gt;) };
    }
}</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（1）<div>必须仔细看老师的教程，不仔细就掉坑里了。说实话老师的文章讲的是真心详细，基本上把所有的坑都讲了。如果实在编译不过，去下载老师的源码，千万记得要坚持下去。</div>2021-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ef/030e6d27.jpg" width="30px"><span>xl000</span> 👍（2） 💬（1）<div>```Rust
impl Kvpair {
    &#47;&#47;&#47; 创建一个新的 kv pair
    fn new(key: impl Into&lt;String&gt;, value: impl Into&lt;Value&gt;) -&gt; Self {
        Self {
            key: key.into(),
            value: Some(value.into()),
        }
    }
}
```
老师Value类型的参数为什么不用impl Into&lt;Value&gt;来定义呢，会有什么问题吗</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（2） 💬（2）<div>得益于老师良好的抽象，我抽出了中午的时间，完成了 hdel 和 hexist 两个命令，如下：
```
running 6 tests
test service::command_service::tests::hget_with_non_exist_key_should_return_404 ... ok
test service::command_service::tests::hexist_should_work ... ok
test service::command_service::tests::hget_should_work ... ok
test service::command_service::tests::hdel_should_work ... ok
test service::command_service::tests::hset_should_work ... ok
test service::command_service::tests::hgetall_should_work ... ok
```

有时间再来慢慢补充，rust 确实是爽的不行。</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8b/66/2b55a7ac.jpg" width="30px"><span>周</span> 👍（1） 💬（3）<div>我把prost的版本改成0.9（0.8版本的可以正常运行) ，然后再测试examples的时候 client.send的时候有个报错:
the method `send` exists for struct `AsyncProstStream&lt;tokio::net::TcpStream, CommandResponse, CommandRequest, AsyncDestination&gt;`, but its trait bounds were not satisfied
the following trait bounds were not satisfied:
`AsyncProstStream&lt;tokio::net::TcpStream, CommandResponse, CommandRequest, AsyncDestination&gt;: futures::Sink&lt;_&gt;`
which is required by `AsyncProstStream&lt;tokio::net::TcpStream, CommandResponse, CommandRequest, AsyncDestination&gt;: SinkExt&lt;_&gt;`rustcE0599
stream.rs(24, 1): doesn&#39;t satisfy `_: SinkExt&lt;_&gt;`
stream.rs(24, 1): doesn&#39;t satisfy `_: futures::Sink&lt;_&gt;`.
我试着用“如何阅读源码”里边的方法，但是还是不太懂这个错误的原因。希望老师能指点下查错的方法</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（1）<div>tcp的半包粘包等，是被prost处理掉了吗？</div>2021-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（1） 💬（1）<div>文中代码有一处错误：
let cloned = service.clone();
&#47;&#47; 创建一个线程，在 table t1 中写入 k1, v1
let handle = thread::spawn(move || {
      let res = cloned.execute(CommandRequest::new_hset(&quot;t1&quot;, &quot;k1&quot;, &quot;v1&quot;.into()));
      assert_res_ok(res, &amp;[Value::default()], &amp;[]);
});

下面的 execute 应该是有 cloned 来执行的，不能由 service 执行，所有权问题。
</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/35/60/d3e723a7.jpg" width="30px"><span>Jagger</span> 👍（0） 💬（2）<div>陈老师，Value::default() 这个函数我没有找到哎？</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/fe/cc/d1923683.jpg" width="30px"><span>东子</span> 👍（0） 💬（1）<div>#[derive(Clone, Debug, Default)]
pub struct MemTable {
    tables: DashMap&lt;String, BTreeMap&lt;String, String&gt;&gt;,
}

impl MemTable {
    &#47;&#47;&#47; 创建一个缺省的 MemTable
    pub fn new() -&gt; Self {
        Self::default()
    }

    &#47;&#47;&#47; 如果名为 name 的 hash table 不存在，则创建，否则返回
    fn get_or_create_table(&amp;self, name: &amp;str) -&gt; Ref&lt;String, BTreeMap&lt;String, String&gt;&gt; {
        match self.tables.get(name) {
            Some(table) =&gt; table,
            None =&gt; {
                let entry = self.tables.entry(name.into()).or_default();
                entry.downgrade()
            }
        }
    }
    fn set(&amp;self, table: &amp;str, key: String, value: String) -&gt; Result&lt;bool&gt; {
        let mut table = self.get_or_create_table(table);
        table.insert(key, value);
        Ok(true)
    }
}

tables: DashMap&lt;String, BTreeMap&lt;String, String&gt;&gt;,我把dashmap换成 btreemap 就会报错

error[E0596]: cannot borrow data in a dereference of `dashmap::mapref::one::Ref&lt;&#39;_, String, BTreeMap&lt;String, String&gt;&gt;` as mutable
  --&gt; src&#47;map_demo.rs:71:9
   |
71 |         table.insert(key, value);
   |         ^^^^^ cannot borrow as mutable
陈老师 </div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6e/72/f8e5b97e.jpg" width="30px"><span>啦啦啦啦啦啦啦</span> 👍（0） 💬（1）<div>实现 Hmget：
 &#47;&#47;&#47; 从一个 HashTable 里获取 批量 keys 对应的 values
    fn get_values(&amp;self, table: &amp;str, keys: &amp;Vec&lt;String&gt;) -&gt; Result&lt;Vec&lt;Option&lt;Value&gt;&gt;, KvError&gt;;
&#47;&#47;&#47; 创建 HMGET 命令
    pub fn new_hmget(table: impl Into&lt;String&gt;, keys: Vec&lt;impl Into&lt;String&gt; + Copy&gt;)  -&gt; Self {

        Self {
            request_data: Some(RequestData::Hmget(Hmget {
                table: table.into(),
                keys: keys
                    .iter()
                    .map(|&amp;s| s.into())
                    .collect(),
            })),
        }
    }

impl CommandService for Hmget {
    fn execute(self, store: &amp;impl Storage) -&gt; CommandResponse {
        match store.get_values(&amp;self.table, &amp;self.keys) {
            Ok(v) =&gt; v.into(),
            Err(e) =&gt; e.into(),
        }
    }
}

fn get_values(&amp;self, table: &amp;str, keys: &amp;Vec&lt;String&gt;) -&gt; Result&lt;Vec&lt;Option&lt;Value&gt;&gt;, KvError&gt; {
    let table = self.get_or_create_table(table);
    let mut result: Vec&lt;Option&lt;Value&gt;&gt; = Vec::new();
    for key in keys.iter() {
      if let Some(val) = table.get(key).map(|v| v.value().clone()) {
        result.push(Some(val));
      }
    }
    Ok(result)
  }
#[test]
    fn hmget_should_work() {
        let store = MemTable::new();
        let cmd = CommandRequest::new_hset(&quot;score&quot;, &quot;u1&quot;, 10.into());
        dispatch(cmd, &amp;store);
        let cmd = CommandRequest::new_hset(&quot;score&quot;, &quot;12&quot;, 11.into());
        dispatch(cmd, &amp;store);
        let cmd = CommandRequest::new_hmget(&quot;score&quot;, vec![&quot;u1&quot;, &quot;12&quot;]);
        let res = dispatch(cmd, &amp;store);
        assert_res_ok(res, &amp;[10.into(), 11.into()], &amp;[]);
    }</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>hmget&#47;hmset等命令调用storage接口时，如何进行错误处理比较好？我现在是忽略错误，返回默认值，感觉不太好</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>```
impl CommandService for Hexist {
    fn execute(self, store: &amp;impl Storage) -&gt; CommandResponse {
        match store.contains(&amp;self.table, &amp;self.key) {
            Ok(v) =&gt; v.into(),
            Err(e) =&gt; e.into(),
        }
    }
}
```
这里编译报错：^^^^ the trait `From&lt;bool&gt;` is not implemented for `abi::CommandResponse`
布尔值怎样转为CommandResponse呢？
</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/f1/d2fc86bb.jpg" width="30px"><span>终生恻隐</span> 👍（0） 💬（1）<div>&#47;&#47; hmget
    &#47;&#47; 创建 HGETALL 命令
    pub fn new_hmget(table: impl Into&lt;String&gt;, keys: Vec::&lt;impl Into&lt;String&gt; + Copy&gt;) -&gt; Self {
        let mut v: Vec::&lt;::prost::alloc::string::String&gt; = Vec::new();
        for &amp;i in keys.iter() {
            v.push(i.into());
        }
        &#47;&#47; map 显示 not reference, why?
        &#47;&#47; let a:  Vec::&lt;::prost::alloc::string::String&gt; = keys.iter().map(|&amp;x| x.into()).collect();
        Self {
            request_data: Some(RequestData::Hmget(Hmget {
                table: table.into(),
                keys: v
            })),
        }
    }

impl CommandService for Hmget {
    fn execute(self, store: &amp;impl Storage) -&gt; CommandResponse {
        let mut out: Vec::&lt;Kvpair&gt; = Vec::new();
        for key in self.keys {
            match store.get(&amp;self.table, &amp;key) {
                Ok(Some(v)) =&gt; out.push(Kvpair::new(key, v)),
                _ =&gt; {}
            }
        }
        return out.into();
    }
}</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（1） 💬（0）<div>做iter的练习被生命周期折磨得快哭了。后面应该着重再讲一讲的</div>2022-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/90/88/a0ba61d5.jpg" width="30px"><span>愚乐</span> 👍（0） 💬（0）<div>源码在哪里呀？</div>2024-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/65/a7/d0788ec6.jpg" width="30px"><span>Jonny Jiang</span> 👍（0） 💬（0）<div>我看有的trait在某个练习项目里放在dependencies，在另一个练习项目里就放在dev-dependencies。比如：tokio。这个有什么讲究吗？</div>2024-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e1/eb/de152d8c.jpg" width="30px"><span>梦中的哈德森</span> 👍（0） 💬（1）<div>痛苦，一模一样的代码敲下去，编译就是不通过，各种飘红</div>2024-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6e/df/2a3a2fd0.jpg" width="30px"><span>zyg</span> 👍（0） 💬（0）<div>mod.rs 里面真的好杂 一会接口定义 一会有实现 一会有导出 一会有test 。。。。。</div>2024-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/61/c1/93031a2a.jpg" width="30px"><span>Aaaaaaaaaaayou</span> 👍（0） 💬（0）<div>老师，为啥 tracing_subscriber 不用 import 就可以直接使用了？</div>2024-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/da/f057374c.jpg" width="30px"><span>DeenJun</span> 👍（0） 💬（0）<div>Storage trait应该设计为async_trait，因为如果换成FS的实现，get set就是异步的</div>2024-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/a5/6d/ad719e86.jpg" width="30px"><span>心看世界</span> 👍（0） 💬（0）<div>老师真的写的太好了，老师是真正的 rust 布道者，我真的很佩服。
不但教会了我们怎么学习 rust，还教会了我们编程思维。
非常感谢，非常荣幸。</div>2023-03-23</li><br/><li><img src="" width="30px"><span>兴小狸</span> 👍（0） 💬（0）<div>敲完之后也还是晕晕乎乎的，主要对整体的设计没有理解透彻，对于怎样去设计一个类似的系统也是没有思路，trait 应该有哪些主要的方法，不知道该怎样去决定。当然，主要的数据结构该怎样设计，也是没有头绪。
不过也有一些小小的收获，比如，测试的代码可以有些思路，还有 From trait 的应用也有理解到一些。</div>2022-12-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/TusRVU51UggZGpicXMgH64Cb8jek0wyTOpagtUHNAj0EPbhbEv0FJpFU2K3glbtOdJXiaQ9o6QoEfv5PiaIu7rwng/132" width="30px"><span>Geek_a6c6ce</span> 👍（0） 💬（0）<div>咔哒</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（1）<div>看到ServiceInner和Service的实现代码就勾起了我一直的一个疑问
ServiceInner&lt;Store: Storage&gt; 写成这样不可以么？为什么还要在实现Service方法时才确定泛型参数，就像文中这样： impl&lt;Store: Storage&gt; Service&lt;Store&gt;
更高一级的抽象有必要么？我感觉在这个软件的可见生命周期里都不太会用有非Storage的Store吧？
但我在看rust的一些三方实现以及之前其他支持复杂泛型的语言的代码里，好像都是这种风格。
不太理解其意义。</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4d/47/e00e9841.jpg" width="30px"><span>manonloki</span> 👍（0） 💬（0）<div>这里填个坑，prost生成的代码中有两个Value 。
一个是结构体 对应的是message Value,
另一个是枚举value::Value 对应的是 message Value{ value }。
例子里用的是结构体。如果引入了枚举那个，就会报错说没有实现Default。
如果强制手工实现也会报其他错误。具体原因学识尚浅不太清楚，但是这坑给新人指出来，免得跟我一样卡了两天……</div>2022-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/be/aa622bf8.jpg" width="30px"><span>爱学习的小迪</span> 👍（0） 💬（1）<div>老师，这个 as _ 是什么意思？</div>2022-02-05</li><br/>
</ul>