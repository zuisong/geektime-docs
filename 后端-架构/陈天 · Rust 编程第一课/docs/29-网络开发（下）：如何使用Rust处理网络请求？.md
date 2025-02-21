你好，我是陈天。

上一讲介绍了如何用Rust做基于 TCP 的网络开发，通过 TcpListener 监听，使用 TcpStream 连接。在 \*nix 操作系统层面，一个 TcpStream 背后就是一个文件描述符。值得注意的是，当我们在处理网络应用的时候，有些问题一定要正视：

- 网络是不可靠的
- 网络的延迟可能会非常大
- 带宽是有限的
- 网络是非常不安全的

我们可以使用 TCP 以及构建在 TCP 之上的协议应对网络的不可靠；使用队列和超时来应对网络的延时；使用精简的二进制结构、压缩算法以及某些技巧（比如 HTTP 的 304）来减少带宽的使用，以及不必要的网络传输；最后，需要使用 TLS 或者 noise protocol 这样的安全协议来保护传输中的数据。

好今天我们接着看在网络开发中，主要会涉及的网络通讯模型。

### 双向通讯

上一讲 TCP 服务器的例子里，所做的都是双向通讯。这是最典型的一种通讯方式：  
![](https://static001.geekbang.org/resource/image/fb/c0/fbe99846847d7d495685eb7bd62889c0.jpg?wh=2463x1007)

一旦连接建立，服务器和客户端都可以根据需要主动向对方发起传输。整个网络运行在全双工模式下（full duplex）。我们熟悉的 TCP / WebSocket 就运行在这种模型下。

双向通讯这种方式的好处是，数据的流向是没有限制的，一端不必等待另一端才能发送数据，网络可以进行比较实时地处理。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（9） 💬（2）<div>虽然一直做的后端，控制平台&#47;平台数据分离 我都没了解过，P2P 也只是知道个概念而已。</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/4c/2f/af2c8d1b.jpg" width="30px"><span>杨学者</span> 👍（0） 💬（0）<div>在 *nix 操作系统层面

怎么回事，敏感字被和谐了？还是说linux&#47;unix？</div>2023-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6b/04/cea8eb77.jpg" width="30px"><span>RG</span> 👍（0） 💬（0）<div>文章里面提到一个stun，有一个栈是webrtc，是一系列的技术的集合，包括网络、多媒体之类的很多东西，用来点对点的做多媒体传输。同样的也可以用来做文件传输，比如说snapdrop。webrtc的好处在于浏览器可用，可以非常方便的构建基于web的p2p应用</div>2023-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/fb/f7/88ab6f83.jpg" width="30px"><span>进击的Lancelot</span> 👍（0） 💬（0）<div>思考题：将 floodsub 替换成 gossipsub 的实现：
https:&#47;&#47;gist.github.com&#47;rust-play&#47;abc70764587405a8a0fa5be30c46886c</div>2022-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/32/3d/e41711c0.jpg" width="30px"><span>Lucifer</span> 👍（0） 💬（0）<div>不错，谢谢</div>2022-03-28</li><br/>
</ul>