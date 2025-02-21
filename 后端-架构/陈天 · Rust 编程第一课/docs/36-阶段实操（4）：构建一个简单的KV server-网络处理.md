你好，我是陈天。

经历了基础篇和进阶篇中两讲的构建和优化，到现在，我们的KV server 核心功能已经比较完善了。不知道你有没有注意，之前一直在使用一个神秘的 [async-prost](https://github.com/tyrchen/async-prost) 库，我们神奇地完成了TCP frame 的封包和解包。是怎么完成的呢？

async-prost 是我仿照 Jonhoo 的 [async-bincode](https://github.com/jonhoo/async-bincode) 做的一个处理 protobuf frame 的库，它可以和各种网络协议适配，包括 TCP / WebSocket / HTTP2 等。由于考虑通用性，它的抽象级别比较高，用了大量的泛型参数，主流程如下图所示：  
![](https://static001.geekbang.org/resource/image/5a/4f/5afafe8646ee8b05b69a463ab5f5554f.png?wh=1428x895)

主要的思路就是在序列化数据的时候，添加一个头部来提供 frame 的长度，反序列化的时候，先读出头部，获得长度，再读取相应的数据。感兴趣的同学可以去看代码，这里就不展开了。

今天我们的挑战就是，在上一次完成的 KV server 的基础上，来试着不依赖 async-prost，自己处理封包和解包的逻辑。如果你掌握了这个能力，配合 protobuf，就可以设计出任何可以承载实际业务的协议了。

## 如何定义协议的 Frame？

protobuf 帮我们解决了协议消息如何定义的问题，然而一个消息和另一个消息之间如何区分，是个伤脑筋的事情。我们需要定义合适的分隔符。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（2） 💬（1）<div>越来越接近实际工作了，老师特别用心，目前没找到网络这块讲解这么详细的内容了。</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4c/2d/a0d6a610.jpg" width="30px"><span>荒野林克</span> 👍（1） 💬（1）<div>老师，代码里当 frame 刚好是 2G 时，按理说应该已经越界了吧？</div>2021-12-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BtgsMc6CpC0O1djDcNicib2eTDliaLicZjibH4dDVKZPuF9gaIG3VGEanFNnx8wqt3iaPwKD8uZcNNaOlicT2PwuToVxQ/132" width="30px"><span>Rex Wang</span> 👍（4） 💬（0）<div>GitHub代码里36_kv&#47;src&#47;error.rs中，KvError去掉了PartialEq属性宏，这是因为std::io::Error不支持binary操作符。

为了保证之前的test依然有效，可以自己定义一个IoError替换原文中KvError中的std::io::Error，手动实现impl From&lt;std::io::Error&gt; for KvError。</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（3） 💬（0）<div>思考题 1: 如果要压缩方式需要同时支持 gzip、lz4、zstd 这三种，则需要 2bit 的标记位，00 表示不压缩、01 表示 gzip、10 表示 lz4、11 表示 zstd，同样也是提取出一个 compressor 的 trait 并针对不同的压缩算法实现相应的 compress 和 decompress 方法，具体可以参考我的代码仓库：https:&#47;&#47;github.com&#47;Phoenix500526&#47;simple_kv&#47;blob&#47;main&#47;src&#47;network&#47;compress 下的文件

思考题 2: 我采用了 shellfish 实现了 simple-kv-cli，代码可以参考：https:&#47;&#47;github.com&#47;Phoenix500526&#47;simple_kv&#47;blob&#47;main&#47;src&#47;kvc-cli.rs</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ce/ed/3dbe915b.jpg" width="30px"><span>乌龙猹</span> 👍（3） 💬（0）<div>内容夯实 思路清晰  结构完整  循序渐进 每周都期待着老师更新课程内容 </div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a3/04/4e38eb46.jpg" width="30px"><span>L-Castle</span> 👍（0） 💬（0）<div>要如何实现TCP的长连接和心跳检测？而不用每次都客户端发起连接请求</div>2024-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/fa/5714677b.jpg" width="30px"><span>sonald</span> 👍（0） 💬（0）<div>```
&#47;&#47;&#47; 从 stream 中读取一个完整的 frame
pub async fn read_frame&lt;S&gt;(stream: &amp;mut S, buf: &amp;mut BytesMut) -&gt; Result&lt;(), KvError&gt;
where
    S: AsyncRead + Unpin + Send,
{
    let header = stream.read_u32().await? as usize;
    let (len, _compressed) = decode_header(header);
    &#47;&#47; 如果没有这么大的内存，就分配至少一个 frame 的内存，保证它可用
    buf.reserve(LEN_LEN + len);
    buf.put_u32(header as _);
    &#47;&#47; advance_mut 是 unsafe 的原因是，从当前位置 pos 到 pos + len，
    &#47;&#47; 这段内存目前没有初始化。我们就是为了 reserve 这段内存，然后从 stream
    &#47;&#47; 里读取，读取完，它就是初始化的。所以，我们这么用是安全的
    unsafe { buf.advance_mut(len) };
    stream.read_exact(&amp;mut buf[LEN_LEN..]).await?;
    Ok(())
}
```
这里最后面的read_exact参数是有问题的吧，假设连续两次调用read_frame而没有消费buf的话，应该改成下面这样？
```
  let start = len - size;
  stream.read_exact(&amp;mut buf[start..]).await?;
```</div>2023-01-17</li><br/>
</ul>