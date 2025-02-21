你好，我是陶辉。

上一讲介绍了为应用层信息安全保驾护航的TLS/SSL协议，这一讲我们来看看最常用的应用层协议HTTP/1.1该如何优化。

由于门槛低、易监控、自表达等特点，HTTP/1.1在互联网诞生之初就成为最广泛使用的应用层协议。然而它的性能却很差，最为人诟病的是HTTP头部的传输占用了大量带宽。由于HTTP头部使用ASCII编码方式，这造成它往往达到几KB，而且滥用的Cookie头部进一步增大了体积。与此同时，REST架构的无状态特性还要求每个请求都得重传HTTP头部，这就使消息的有效信息比重难以提高。

你可能听说过诸如缓存、长连接、图片拼接、资源压缩等优化HTTP协议性能的方式，这些优化方案有些从底层的传输层优化入手，有些从用户使用浏览器的体验入手，有些则从服务器资源的编码入手，五花八门，导致我们没有系统化地优化思路，往往在性能提升上难尽全功。

那么，如何全面地提升HTTP/1.1协议的性能呢？我认为在不升级协议的情况下，有3种优化思路：首先是通过缓存避免发送HTTP请求；其次，如果不得不发起请求，那么就得思考如何才能减少请求的个数；最后则是减少服务器响应的体积。

接下来，我们就沿着这3个思路看看具体的优化方法。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/63/2e/e49116d1.jpg" width="30px"><span>Geek_007</span> 👍（16） 💬（1）<div>FB也搞了一套压缩算法ZSTD，对比起来也比gzip性能强很多，不清楚这些压缩算法的原理是啥，怎么对比，希望老师之后能答疑一下。另外普通的json和pb有不同适合的压缩算法吗？怎么比较呢？</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/63/2e/e49116d1.jpg" width="30px"><span>Geek_007</span> 👍（6） 💬（1）<div>图片压缩，腾讯说他们的TPG比Webp压缩的更小呢😀，不过除了他们内部这么说，没见过第三方资料的证明</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9f/3d/b400b98e.jpg" width="30px"><span>新声带NewVoice</span> 👍（3） 💬（1）<div>尝试过http1.1 chunk子协议，可以在同一个连接上，服务端向客户端发送多次数据。</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（3） 💬（1）<div>最近正准备用gzip优化我们的一个后端服务就看到了这一讲，赶快试试Brotli算法</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（6）<div>base64编码的作用是啥呢？只是为了把不可见字符变成可见的吗？搜到的资料都讲base64的实现原理但是并没有讲base64编码的作用的，好像挺多地方用到这个编码了。</div>2020-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（3） 💬（0）<div>Accept 头部中的 q 质量因子
======
想问一下，当服务器接收到这样的请求后，是背后的应用层处理这个压缩，还是说，支持这个标准的Http服务器本身就可以“透明”的完成这个压缩工作</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（0）<div>一般来说客户端和代理服务器之间是https协议，而代理服务器和源站之间可以只使用http协议，减少https协议额外的消息交互。
另外在减少http包体方面，老师文中提到图片压缩，而对于非图片的传输，如定义的json结构，可以通过简化json里key，value的字节数来减少传输包体大小。</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>如果上述方法都采用了。那么只能提高HTTP请求的并发度了。
1、对于客户端来说，多开TCP连接的数量。
2、对于服务器来说，可以将相同域名解析到不同的IP，然后提供同样的服务。
本质上，都是为了增加TCP连接的数量。</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/37/a0/032d0828.jpg" width="30px"><span>上杉夏香</span> 👍（0） 💬（0）<div>如果上述方法都尝试过。那么只能提高http请求的并发度了。</div>2022-07-03</li><br/>
</ul>