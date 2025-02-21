你好，我是陈天。

通过 HTTPie 和 Thumbor 的例子，相信你对 Rust 的能力和代码风格有了比较直观的了解。之前我们说过Rust的应用范围非常广，但是这两个例子体现得还不是太明显。

有同学想看看，在实际工作中有大量生命周期标注的代码的样子；有同学对 Rust 的宏好奇；有同学对 Rust 和其它语言的互操作感兴趣；还有同学想知道 Rust 做客户端的感觉。所以，我们今天就来**用一个很硬核的例子把这些内容都涵盖进来**。

话不多说，我们直接开始。

## SQL

我们工作的时候经常会跟各种数据源打交道，数据源包括数据库、Parquet、CSV、JSON 等，而打交道的过程无非是：数据的获取（fetch）、过滤（filter）、投影（projection）和排序（sort）。

做大数据的同学可以用类似 Spark SQL 的工具来完成各种异质数据的查询，但是我们平时用 SQL 并没有这么强大。因为虽然用 SQL 对数据库做查询，任何 DBMS 都支持，如果想用 SQL 查询 CSV 或者 JSON，就需要很多额外的处理。

所以如果能有一个简单的工具，**不需要引入 Spark，就能支持对任何数据源使用 SQL 查询**，是不是很有意义？

比如，如果你的 shell 支持这样使用是不是爽爆了？![](https://static001.geekbang.org/resource/image/3e/7c/3e8e6586d8599e39a6704cf82352cd7c.jpg?wh=1920x703)  
再比如，我们的客户端会从服务器 API 获取数据的子集，如果这个子集可以在前端通过 SQL 直接做一些额外查询，那将非常灵活，并且用户可以得到即时的响应。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/c0/cb5341ec.jpg" width="30px"><span>leesper</span> 👍（33） 💬（1）<div>
陈天老师，学完了这节课程，我觉得你和陈皓老师给了我新的启发。

在陈皓老师的《左耳听风》的《编程的本质》一节，提到了这么两个公式

（1）程序=算法+数据结构
（2）算法=逻辑+控制

我从这两个公式中领悟出：“程序=逻辑抽象+数据结构+控制”。数据结构是业务逻辑的静态的描述，它用术语表示数据结构的定义，而逻辑抽象是动态的，是对业务流程的抽象。

您在课程里所说的“绝大多数处理逻辑都是把数据从一个接口转换成另一个接口。”、“好的代码，应该是每个主流程都清晰简约，代码恰到好处地出现在那里，让人不需要注释也能明白作者在写什么”

与陈皓老师的“有效地分离 Logic、Control 和 Data 是写出好程序的关键所在！”，其实表达的是同一个意思。写任何代码，设计好Logic和Data，业务流程就算完成了（功能性需求），然后在这个基础上不断地优化Control，就能提高代码性能（非功能性需求）。

以“高性能网络编程”为例，网络编程的业务逻辑是“客户机-服务器模型”：

（1）客户进程发送请求
（2）服务进程处理请求（可能会访问某些本地或远程资源）
（3）服务进程发送响应
（4）客户进程处理响应

在这个过程中所体现的就是您所说的“绝大多数处理逻辑都是把数据从一个接口转换成另一个接口”的过程：

（1）客户进程中的业务数据变成请求数据包
（2）请求数据包编码成字节流发送到网络上
（3）服务进程获得字节流把它解码成请求数据包
（4）服务进程根据请求数据包访问资源得到结果
（5）客户进程把结果数据变成响应数据包
（6）响应数据包编码成字节流发送到网络上
（7）客户进程获得字节流把它解码成响应数据包
（8）客户进程处理响应数据包

对于一个最简单的iterative echo server来说，一次服务一个客户端，字节码解码成字符串，业务逻辑就是把客户端发来的再原封不动编码成字节码发回去就可以了。

然而对于一个有着复杂业务逻辑的高性能服务器来说，要考虑的点就不一样了：
（1）要实现字节码和“自定义消息”之间的来回转换，就要自定义Codec，甚至要引入protobuffer&#47;flatbuffer，并实现消息的注册机制
（2）要一次服务多个客户端，就要引入epoll&#47;kqueue这样的IO multiplexing机制，实现单个线程监听多个socket fd，甚至one-loop-per-thread，并做好网络连接管理，关闭服务器的时候不能硬着陆，要优雅关闭：等待所有网络连接接收并处理完消息再退出
（3）要提高IO性能，就要引入nonblocking IO
（4）要避免复杂业务逻辑占用IO线程资源，就要引入工作者线程池，把服务端对消息的处理放到另一个线程中执行，并做好IO线程和工作者线程的同步
（5）如果服务端要访问远程资源，就要引入配置，在服务启动时装配好各种mysql或者redis的handle，甚至自己实现一个connector访问其他的服务

这些都是属于Control范畴要考虑的东西。Logic决定了程序复杂度的下限，Control决定了上限。把Logic和Control混在一起，往往是写出来的代码难以维护的原因。</div>2021-09-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/ajNVdqHZLLDoDeeNST87MZEdfT8n7yEWp06KsFCTs2ssFh2tbHu413nibrRObOia1Zn9pqiaHgIicVkSHRZM3LHOEA/132" width="30px"><span>葡萄</span> 👍（20） 💬（2）<div>老师的课程消除了对解决这类问题(自己实现一个解析器的扩展)的恐惧，或者说以前一直在使用高级封装的语言，对这些偏低层一点的东西总是不敢触碰，一点点分析下来，完全没有想象中的那么难。哈哈，这就是get hands dirty的精要吧。学习rust很好，听老师讲课更好，感谢老师。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（7） 💬（1）<div>In [1]:  import queryer_py

In [2]: sql = queryer_py.example_sql()

In [3]: print(queryer_py.query(sql, &#39;csv&#39;))
name,total_cases,new_cases,total_deaths,new_deaths
European Union,36489548.0,84973.0,766627.0,541.0
India,32857937.0,47092.0,439529.0,509.0
South America,36922209.0,37641.0,1131322.0,1104.0
Iran,5025233.0,33170.0,108393.0,599.0
Africa,7821187.0,30793.0,196917.0,639.0
Brazil,20804215.0,27345.0,581150.0,737.0

本周最骄傲、最爽的demo：

```shell
$ tree .

.
├── httpie
│   ├── src
│   └── target
├── queryer_all
│   ├── queryer
│   ├── queryer-py
│   └── target
├── scrape_url
│   ├── src
│   └── target
├── thumbor
│   ├── src
│   └── target
```</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/b2/9223bc53.jpg" width="30px"><span>Fenix</span> 👍（14） 💬（1）<div>太赞了，这种教学模式，处理问题的思路很有启发</div>2021-09-03</li><br/><li><img src="" width="30px"><span>Geek_01c6d8</span> 👍（9） 💬（1）<div>全网最好的rust课程，没有之一！！！</div>2021-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（6） 💬（1）<div>老师如何有效阅读docs.rs，我看你引入来的crate的文档，但是不知道如何有效学习？</div>2021-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ca/06/a110cc63.jpg" width="30px"><span>拉斯特</span> 👍（6） 💬（1）<div>通过一个实际案例展现了rust的特性，设计模式的使用，决解问题的思路和设计过程。简直不要太棒～</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/1f/e894ae27.jpg" width="30px"><span>Colt</span> 👍（5） 💬（1）<div>老师的思路非常正，这几次实践课可以看出RUST的魅力和优雅，能力有限需要多品几次</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/ad/4efd929a.jpg" width="30px"><span>老荀</span> 👍（5） 💬（1）<div>太强了！这种实战性质的教学正是大家都需要的！不是那种重复啰嗦语法细节的烂课程</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d2/5a/63af190e.jpg" width="30px"><span>玄澈</span> 👍（4） 💬（1）<div>老师你好，有观点认为用 Deref 模拟继承通常不是好的做法。例如：https:&#47;&#47;www.zhihu.com&#47;question&#47;36488041
https:&#47;&#47;rust-unofficial.github.io&#47;patterns&#47;anti_patterns&#47;deref.html
有好处也有坏处，我们该如何权衡以至于防止滥用呢。</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/1b/11/7d96bff5.jpg" width="30px"><span>yyxxccc</span> 👍（3） 💬（1）<div>陈老师再来几个白金，王者级难度的👍，这一讲看得我地铁坐过站了😂。</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（3） 💬（1）<div>Node 来了：

```js
node 
Welcome to Node.js v14.17.5.
Type &quot;.help&quot; for more information.
&gt; const rs = require(&#39;.&#39;)
undefined
&gt; rs.example_sql()
&#39;SELECT location name, total_cases, new_cases, total_deaths, new_deaths FROM https:&#47;&#47;raw.githubusercontent.com&#47;owid&#47;covid-19-data&#47;master&#47;public&#47;data&#47;latest&#47;owid-covid-latest.csv where new_deaths &gt;= 500 ORDER BY new_cases DESC LIMIT 6 OFFSET 5&#39;
```

爽～</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/3e/692a93f7.jpg" width="30px"><span>茶底</span> 👍（3） 💬（1）<div>今天这个雀食帅</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/7c/f6/028f80a8.jpg" width="30px"><span>施泰博</span> 👍（2） 💬（1）<div>reqwest 请求，broken pipe怎么破？</div>2021-11-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/b7/4097aa22.jpg" width="30px"><span>null</span> 👍（2） 💬（1）<div>理论时长：24:58，实际时常：24小时</div>2021-10-11</li><br/><li><img src="" width="30px"><span>兴小狸</span> 👍（2） 💬（1）<div>说实话，越敲越慌，我完全不知道在做啥子~</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bc/2c/963688bb.jpg" width="30px"><span>noisyes</span> 👍（2） 💬（1）<div>我只能说牛逼</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/33/d4/c37f531a.jpg" width="30px"><span>沐佑</span> 👍（1） 💬（2）<div>如果引入pyo3遇到这个问题：unresolved macro `proc_macro_call!`
请参考：https:&#47;&#47;github.com&#47;rust-analyzer&#47;rust-analyzer&#47;issues&#47;6835</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（1） 💬（3）<div>来来来，看看俺的😆:
node
https:&#47;&#47;github.com&#47;Rust-Beginner&#47;queryer&#47;blob&#47;master&#47;queryer-node&#47;README.md

老师在获取 sql 和 output 参数的时候用的都是cx.argument，但我运行的时候发现如果只传一个参数会直接报 TypeError: not enough arguments。改用 cx.argument_opt 就好了，具体参考我的代码。

另外我的输出使用 console.table 美化了一下，还处理了查询结果为空的情况。

web前端
https:&#47;&#47;github.com&#47;Rust-Beginner&#47;queryer&#47;blob&#47;master&#47;queryer-fed&#47;README.md

作为一名前端er，界面是不能马马虎虎哒，用户体验也要有一点～～
和老师的比起来，高下立判哈哈哈（对不起😂
</div>2021-10-25</li><br/><li><img src="" width="30px"><span>兴小狸</span> 👍（1） 💬（1）<div>&#47;&#47;&#47; 把 SqlParser 的 SelectItem 转换成 DataFrame 的 Expr
像这些功能，是为外部引入的结构实现某些特定的 trait 吗？这样算修改外部包的功能吗？</div>2021-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（1） 💬（1）<div>『宏编程的主要流程就是实现若干 From和 TryFrom』这里有点绕。是说实现From trait的工作可以算是一种宏编程吗？毕竟代码里只是实现了trait，没有定义宏。</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/01/b5/d53eb811.jpg" width="30px"><span>暂时用这个名字和头像</span> 👍（0） 💬（1）<div>为啥课程绝大多数代码都无法运行的？老师有跑过的吗
error[E0308]: mismatched types
   --&gt; 06_queryer&#47;queryer&#47;src&#47;lib.rs:78:59
    |
78  |         .fold(filtered, |acc, (col, desc)| acc.sort(&amp;col, desc));
    |                                                ----       ^^^^ expected struct `SortOptions`, found `bool`
    |                                                |
    |                                                arguments to this function are incorrect
    |
note: associated function defined here
   --&gt; &#47;root&#47;.cargo&#47;registry&#47;src&#47;github.com-1ecc6299db9ec823&#47;polars-lazy-0.23.2&#47;src&#47;frame&#47;mod.rs:271:12
    |
271 |     pub fn sort(self, by_column: &amp;str, options: SortOptions) -&gt; Self {
    |            ^^^^
</div>2022-08-20</li><br/><li><img src="" width="30px"><span>兴小狸</span> 👍（0） 💬（1）<div>唔~我代码抄了一半都是不懂的，我这样抄有效吗？老师。我也不理解为啥要这样写，也不知道这样实现的道理</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（1）<div>neno done
```rs
use neon::prelude::*;

fn example_sql(mut cx: FunctionContext) -&gt; JsResult&lt;JsString&gt; {
    Ok(cx.string(queryer::example_sql()))
}

fn query(mut cx: FunctionContext) -&gt; JsResult&lt;JsString&gt; {
    let sql = cx.argument::&lt;JsString&gt;(0)?;
    let output = cx.argument_opt(1);
    let rt = tokio::runtime::Runtime::new().unwrap();
    let data = rt.block_on(async { queryer::query(sql.value(&amp;mut cx)).await.unwrap() });
    if let Some(v) = output {
        let csv: Handle&lt;JsString&gt; = v.downcast(&amp;mut cx).unwrap();
        let csv = csv.value(&amp;mut cx);
        if csv.eq(&quot;csv&quot;) {
            return Ok(cx.string(data.to_csv().unwrap()));
        }
        return cx.throw_error(format!(
            &quot;Output type {} not supported&quot;,
            csv
        ));
    } else {
        return Ok(cx.string(data.to_csv().unwrap()));
    }

}

#[neon::main]
fn main(mut cx: ModuleContext) -&gt; NeonResult&lt;()&gt; {
    cx.export_function(&quot;example_sql&quot;, example_sql)?;
    cx.export_function(&quot;query&quot;, query)?;
    Ok(())
}
```</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（2）<div>pyo3这个例子，现在有点跑不动了。
ld: symbol(s) not found for architecture x86_64
          clang: error: linker command failed with exit code 1 (use -v to see invocation)
https:&#47;&#47;github.com&#47;PyO3&#47;pyo3&#47;issues&#47;1800，暂时不是很懂为什么</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/76/26f555ce.jpg" width="30px"><span>上沅同学</span> 👍（0） 💬（1）<div>讲的太棒了！就是没怎么看懂，要慢慢啃。。</div>2021-12-29</li><br/><li><img src="" width="30px"><span>Geek_9d1ee1</span> 👍（0） 💬（1）<div>回来看这个代码，发现个问题，

&#47;&#47;&#47; 把 SqlParser 的 BinaryOperator 转换成 DataFrame 的 Operator
impl TryFrom&lt;Operation&gt; for Operator {...}

这里 Operator 是个外部的(Polars 里的) Type, 为什么可以为这个实现 TryFrom</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/7d/ac/a6026f3b.jpg" width="30px"><span>Lambda</span> 👍（0） 💬（1）<div>我看不懂, 但我大受震撼</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>怎样才能使DataSet显示超过8行8列，现在超过这个数就有行或者列用省略号代替了</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c4/92/338b5609.jpg" width="30px"><span>Roy Liang</span> 👍（0） 💬（1）<div>我自己实现了JsonReader，不知道为什么不支持标准的JSON，只支持这种格式（外层没有中括号，对象之间没有逗号分隔只有换行，成员不能是嵌套的JSON）
{&quot;a&quot;:1, &quot;b&quot;:2.0, &quot;c&quot;:false, &quot;d&quot;:&quot;4&quot;}
{&quot;a&quot;:-10, &quot;b&quot;:-3.5, &quot;c&quot;:true, &quot;d&quot;:&quot;4&quot;}</div>2021-11-04</li><br/>
</ul>