你好，我是陈天。今天我们学习如何使用 Rust 做网络开发。

在互联网时代，谈到网络开发，我们想到的首先是 Web 开发以及涉及的部分 HTTP 协议和 WebSocket 协议。

之所以说部分，是因为很多协议考虑到的部分，比如更新时的[并发控制](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match)，大多数 Web 开发者并不知道。当谈论到 [gRPC](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md) 时，很多人就会认为这是比较神秘的“底层”协议了，其实只不过是 HTTP/2 下的一种对二进制消息格式的封装。

所以对于网络开发，这个非常宏大的议题，我们当然是不可能、也没有必要覆盖全部内容的，今天我们会先简单聊聊网络开发的大全景图，然后重点学习如何使用Rust标准库以及生态系统中的库来做网络处理，包括网络连接、网络数据处理的一些方法，最后也会介绍几种典型的网络通讯模型的使用。

但即使这样，内容也比较多，我们会分成上下两讲来学习。如果你之前只关注 Web 开发，文中很多内容读起来可能会有点吃力，建议先去弥补相关的知识和概念，再学习会比较容易理解。

好，我们先来简单回顾一下 ISO/OSI 七层模型以及对应的协议，物理层主要跟 [PHY 芯片](https://en.wikipedia.org/wiki/Physical_layer)有关，就不多提了：  
![](https://static001.geekbang.org/resource/image/90/ef/909ec0f611352fyy5b99f27bb2f557ef.jpg?wh=2315x1468)

七层模型中，链路层和网络层一般构建在操作系统之中，我们并不需要直接触及，而表现层和应用层关系紧密，所以在实现过程中，**大部分应用程序只关心网络层、传输层和应用层**。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（6） 💬（1）<div>Protobuf 和二进制数据解析都是我一直在寻找的，非常赞</div>2021-11-01</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（3） 💬（2）<div>请教要实现socks5的服务程序，您建议用什么库？为什么推荐这个？</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/12/e4/57ade29a.jpg" width="30px"><span>dva</span> 👍（1） 💬（1）<div>试着做一下思考题

use anyhow::Result;
use async_prost::AsyncProstStream;
use futures::prelude::*;
use kv1::{CommandRequest, CommandResponse, Service, ServiceInner, SledDb};
use tokio::net::TcpListener;
use tracing::info;
use bytes::Bytes;
use futures::{SinkExt, StreamExt};
use tokio_util::codec::{Framed, LengthDelimitedCodec};
use prost::Message;


#[tokio::main]
async fn main() -&gt; Result&lt;()&gt; {
    tracing_subscriber::fmt::init();
    let service: Service&lt;SledDb&gt; = ServiceInner::new(SledDb::new(&quot;&#47;tmp&#47;kvserver&quot;))
        .fn_before_send(|res| match res.message.as_ref() {
            &quot;&quot; =&gt; res.message = &quot;altered. Original message is empty.&quot;.into(),
            s =&gt; res.message = format!(&quot;altered: {}&quot;, s),
        })
        .into();
    let addr = &quot;127.0.0.1:9527&quot;;
    let listener = TcpListener::bind(addr).await?;
    loop {
        let (stream, addr) = listener.accept().await?;
        println!(&quot;accepted: {:?}&quot;, addr);
        &#47;&#47; LengthDelimitedCodec 默认 4 字节长度
        let mut stream = Framed::new(stream, LengthDelimitedCodec::new());
        let svc = service.clone();

        tokio::spawn(async move {
            &#47;&#47; 接收到的消息会只包含消息主体（不包含长度）
            while let Some(Ok(data)) = stream.next().await {
                let cmd = CommandRequest::decode(data).unwrap();
                info!(&quot;req: {:?} &quot;, cmd);

                let res = svc.execute(cmd);
                info!(&quot;res: {:?} &quot;, res);
                stream.send(Bytes::from(res.encode_to_vec())).await.unwrap();
            }
        });
    }
}
</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（3） 💬（0）<div>思考题可以参考 dva 同学的实现，我这里也提供一个关于 client 的修改:

```rust
use anyhow::Result;
use bytes::Bytes;
use futures::prelude::*;
use kv::CommandRequest;
use prost::Message;
use tokio::net::TcpStream;
use tokio_util::codec::{Framed, LengthDelimitedCodec};
use tracing::info;

#[tokio::main]
async fn main() -&gt; Result&lt;()&gt; {
    tracing_subscriber::fmt().init();
    let addr = &quot;127.0.0.1:9527&quot;;
    let stream = TcpStream::connect(addr).await?;
    let mut client = Framed::new(stream, LengthDelimitedCodec::new());

    let cmd = CommandRequest::new_hset(&quot;table1&quot;, &quot;hello&quot;, &quot;world&quot;.into());
    client.send(Bytes::from(cmd.encode_to_vec())).await?;
    if let Some(Ok(data)) = client.next().await {
        info!(&quot;Got response: {:?}&quot;, data);
    }
    Ok(())
}
```</div>2022-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/68/a6/2f3037e5.jpg" width="30px"><span>贱猴🐔哥的室友</span> 👍（0） 💬（0）<div>之前以为protobuf必须和grpc等一起用比较好，发现自定义的格式其实跟 TLV（Type-Length-Value）是一样的原理，而且更简单，这种方式应该比较好</div>2022-10-10</li><br/>
</ul>