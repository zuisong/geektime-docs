你好，我是Mike，今天我们继续讲如何使用Axum开发Web后端。学完这节课的内容后，你应该能使用Axum独立开发一个简单的Web后端应用了。

第21讲，我们已经讲到了第4步，处理Get query请求，拿到query中的参数。下面我们讲如何处理Post请求并拿到参数。

这节课的代码适用于 Axum v0.7 版本。

## 基本步骤

### 第五步：解析 Post 请求参数

当我们想向服务端提交一些数据的时候，一般使用HTTP POST方法。Post的数据会放在HTTP的body中，在HTML页面上，通常会使用表单form收集数据。

和前面的Query差不多，Axum给我们提供了Form解包器，可以方便地取得form表单数据。你可以参考下面的示例。

```plain
#[derive(Deserialize, Debug)]
struct Input {
    name: String,
    email: String,
}

async fn accept_form(Form(input): Form<Input>) -> Html<&'static str> {
    tracing::debug!("form params {:?}", input);

    Html("<h3>Form posted</h3>")
}
```
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/63/57/b8eef585.jpg" width="30px"><span>小虎子11🐯</span> 👍（2） 💬（0）<div>因为刚刚更新了版本，文字内容有调整，所以需要一些时间处理音频，所以今天的音频中午发布哦</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/8a/94/cbbf8b4d.jpg" width="30px"><span>天穹智能</span> 👍（2） 💬（2）<div>老师，请教一下axum开发web的包结构命名组织规范有没有相对比较正式点的，最近公司在用axum开发一个项目，一直在构思模块和包的结构组织。</div>2023-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（2） 💬（1）<div>怎么实现生成pdf文件，生成xls文档导入导出？生成word导出？</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/09/29c46a7b.jpg" width="30px"><span>-</span> 👍（2） 💬（2）<div>我发现一个问题，就是同样的State,handler中我放第一个参数没问题，我放到Json参数后报错，希望老师协助分析下</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f2/c2/939bec1c.jpg" width="30px"><span>meteor</span> 👍（0） 💬（1）<div>请问下，rust有什么好用的表格组件吗，可以编译成wasm的。我们的网页需要一个高性能表格，想用rust开发，然后编译为wasm。目前看了egui,请问还有其他好用的库吗</div>2024-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（1）<div>思考题：声明式参数，我个人觉得有一点“强类型”的味道，这要求把参数是什么明确表示出来，即利于代码的可读性，也有助于类型检查。

另外，想问一下老师，示例代码中数据库连接池通过 State 的方式来传递，这种方式跟声明全局变量相比有什么优劣呢？以及，如果我有多个对象需要共享，那怎么做呢？</div>2024-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/07/93/710c7ee2.jpg" width="30px"><span>不忘初心</span> 👍（0） 💬（1）<div>bb8 有mysql的crate吗? crates.io上没有找到哦</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（1）<div>本文是用了 ORM 吗？

因为我们由于使用 ORM 这种东西，因此纯靠手动拼 sql 字符串</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5c/d7/3b92bb0d.jpg" width="30px"><span>伯阳</span> 👍（0） 💬（1）<div>确实挺方便，天生支持MySQL么</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7b/94/8f68c15b.jpg" width="30px"><span>山茶花</span> 👍（0） 💬（0）<div>bb8好像没有mysql驱动，r2d2的mysql驱动不太会用，网上找了个sqlx来用

db初始化:
```
use sqlx::{MySql, Pool};
use sqlx::mysql::MySqlPoolOptions;

let url = &quot;mysql:&#47;&#47;username:password@127.0.0.1:3306&#47;test&quot;;
let pool = MySqlPoolOptions::new().connect(&amp;url).await.unwrap();
```

用法:
```
async fn todo_list(pagination: Option&lt;Query&lt;Pagination&gt;&gt;,
                   State(pool): State&lt;ConnectionPool&gt;,
) -&gt; Result&lt;Json&lt;Vec&lt;Todo&gt;&gt;, (StatusCode, String)&gt; {
    let Query(patination) = pagination.unwrap_or_default();
    let offset = patination.offset.unwrap_or(0);
    let limit = patination.limit.unwrap_or(100);

    let mut conn = pool.acquire().await.map_err(internal_error)?;
    let todos = sqlx::query_as::&lt;_, Todo&gt;(&quot;select id, description, completed from todo limit ?, ?&quot;)
        .bind(&amp;offset)
        .bind(&amp;limit)
        .fetch_all(&amp;mut conn)
        .await
        .map_err(internal_error)?;
    
    Ok(Json(todos))
}
```</div>2024-06-01</li><br/>
</ul>