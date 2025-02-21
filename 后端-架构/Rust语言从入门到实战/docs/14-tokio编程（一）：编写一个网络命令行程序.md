你好，我是Mike，上一节课我们了解了Rust异步编程和tokio的基础知识，今天我们就来一起用tokio做一个小应用。

## 准备阶段

我们常常需要知道远程服务器上的一些信息，这有一些现成的工具可以做到。我们来试一下如何使用tokio实现这一功能。

**目标：**编写一个获取服务器时间的命令行程序。

**任务分解：**

1. 命令行：这个工具取名为 getinfo, 参数格式是 `getinfo {ip}`，就是在 getinfo 后接IP地址，获取服务器时间。
2. tcp server：监听 8888 端口，获取从客户端来的请求，然后获取服务器本地时间，返回。
3. tcp client：连接服务端地址 `ip:port`，向服务端发送获取服务器时间指令。
4. 测试。

## 实现

下面我们开始实现。

### 创建项目

我们打开终端或者IDE中的Terminal，执行：

```plain
cargo new --bin getinfo
```

### 命令行雏形

Rust标准库中实际已经有获取命令行参数的功能，`std::env` 提供了一种获取命令行参数的方法 [std](https://doc.rust-lang.org/std/index.html)::[env](https://doc.rust-lang.org/std/env/index.html)::[args](https://doc.rust-lang.org/std/env/fn.args.html)()，可以将命令行参数转换成一个迭代器，通过 for 循环就可以遍历所有命令行参数，当然也可以使用迭代器上的 `.nth()` 直接定位到某一个参数。比如：

```plain
let addr = env::args()
    .nth(1)
    .unwrap_or_else(|| "127.0.0.1:8888".to_string());
```
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLO6XvxfFPMGcVSSX8uIZY2yib29qlyat178pU4QM3gIic5GXZ8PC0tzRiazP3FiajXbTj19SE4ZhV0gQ/132" width="30px"><span>PEtFiSh</span> 👍（6） 💬（1）<div>EOF: End of file. 在linux万物皆file的情况下connection也可以是一个file。所以，当Connection关闭的时候，就会产生EOF。
stream.read_to_end()是持续read()直到EOF，因此能够读完网络里的数据，如果使用stream.read_to_end(&amp;mut buf).await?;读取的话，会持续wait，直到连接关闭才能进行后续的操作。</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/06/f8/09ad484b.jpg" width="30px"><span>学水</span> 👍（5） 💬（3）<div>感觉这部分内容和java的netty包有点像</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c9/96/4577c1ef.jpg" width="30px"><span>沉默的话唠</span> 👍（2） 💬（1）<div>跟着一路下来，感觉讲师讲的真的不错。 不知道后面考不考虑有训练营之类的，更加全面体系的课程。</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/65/13/8654e7c9.jpg" width="30px"><span>Citroen</span> 👍（1） 💬（3）<div>这段代码
let mut framed_stream = Framed::new(stream, LengthDelimitedCodec::new())
请问一下老师，我现在需要接收client端的数据（数据是打包好的protobuf序列化后的二进制数据，
前面有四位长度表示这个序列化后的二进制数据的长度，也就是说数据格式是，头（四位 用于说明后面完整protobuf序列化后的数据长度）加内容（protobuf序列化后的二进制数据）,len(四位长度）加main(protobuf序列化后的二进制数据 每次长度不固定，但可通过前面的len可以知道），每段数据都是这样 这样的数据怎么取？</div>2023-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/39/ab/ca/32d6c05d.jpg" width="30px"><span>哄哄</span> 👍（1） 💬（1）<div>应该用什么已有的crate包，感觉也是新人的一个问题。请问上哪能快速认识常用第三方包呢？</div>2023-11-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>EOF =&gt; End Of File, 在数据流断开的时候会碰到

stream.read_to_end(buf) =&gt; 把这个 stream 里接收到的所有数据都丢到一个 buf_vec 里， 应该是一个阻塞函数吧， 只要链接不断开， 就一直等待， 单开一个进程 &#47; 线程来跑 read_to_end 然后在别的进程 &#47; 线程从 buf 里往外面读数据

不过感觉如果用 read_to_end 的话当前 stream 就没办法往里写数据了， 这咋整啊， 难道是 clone 一份 stream 然后在其他进程 &#47; 线程来写吗， 还是设计的时候就不考虑往 `用了 read_to_end 的 stream`里继续写数据了？</div>2023-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（0） 💬（1）<div>啊？ 有源码的啊， star 一下先</div>2023-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/77/2a/0cd4c373.jpg" width="30px"><span>-Hedon🍭</span> 👍（0） 💬（1）<div>思考题1：EOF

	EOF 是 &quot;End of File&quot; 的缩写，意为“文件结束”。它是一个用于表示文件或数据流末尾的控制信号或字符。当读取文件或数据流时，EOF用于指示没有更多的数据可读取。
	
	EOF 通常出现在以下几种情况：

	1. 文件读取：在读取文件内容时，到达文件末尾后，会遇到 EOF。这告诉程序没有更多的数据可读取。

	2. 标准输入：在某些编程语言或环境中，如 Unix&#47;Linux 的命令行，可以使用特定的键盘组合（如 Ctrl+D ）来生成 EOF 信号，表示标准输入结束。

	3. 数据流结束：在处理数据流（如网络传输中的数据）时，EOF 可以用来指示数据传输已经完成。


思考题2：stream.read_to_end()

	首先我觉得核心点在 “读完” 这个概念上，即意味着连接中的数据是有限的，才有读完，如果是无限的流数据，那么 stream.read_to_end() 会一直阻塞等待数据的到来。如果明确数据的有限的，那么在数据源发出 EOF 后，stream.read_to_end() 就会返回，那这个时候是可以 “读完” 的。当前，前提是你的内存得够。


(连续2周搬砖赶需求，终于能抽点时间续上 rust 的学习了 T_T)</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/99/0d72321f.jpg" width="30px"><span>A0.何文祥</span> 👍（0） 💬（1）<div>cargo new --bin getinf应为cargo new --bin getinfo</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/9e/15/e499fc69.jpg" width="30px"><span>Andylinge</span> 👍（0） 💬（2）<div>Windows 11 报如下错误，大家可以把process里面的获取时间命令自己用Rust重写一下。
```Listening on: 127.0.0.1:8880
Accepted a connection from: 127.0.0.1:9354
gettime
thread &#39;tokio-runtime-worker&#39; panicked at src&#47;server.rs:80:58:
called `Result::unwrap()` on an `Err` value: Error { kind: NotFound, message: &quot;program not found&quot; }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
error: process didn&#39;t exit successfully: `D:\00-Program\05-Rust\14-Rust_MikeTang\r14_tokio\getinfo\target\debug\server.exe` (exit code: 0xc000013a, STATUS_CONTROL_C_EXIT)
```</div>2023-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/06/f8/09ad484b.jpg" width="30px"><span>学水</span> 👍（0） 💬（1）<div>第一版server代码，没读到完整请求的话，为啥更新offset为n而不是end呢</div>2023-11-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7Q403U68Oy4lXG5sFBPVKLrfwaRzBqpBZibpEBXcPf9UOO3qrnh7RELoByTLzBZLkN9Nukfsj7DibynbZjKAKgag/132" width="30px"><span>superggn</span> 👍（2） 💬（0）<div>笔记

stream &#47; socket 这个东西， 不用关心具体定义， 只要知道拿着它可以进行读写操作就行了



server 跑起来了之后可以用 nc 命令来简单跑一下测试（不用 client.rs）， 注意 nc 发的消息自带一个 `\n`, 记得 strip_suffix 搞一下

&gt;nc 127.0.0.1 8888



ps: 前段时间撸 https:&#47;&#47;github.com&#47;jonhoo&#47;rust-tcp 快撸哭了... 看到 tokio 这么简单的代码真舒服</div>2023-12-21</li><br/>
</ul>