你好，我是陶辉。

这一讲我们将以一个实战案例，基于前两讲提到的HTTP/2和ProtoBuf协议，看看gRPC如何将结构化消息编码为网络报文。

直接操作网络协议编程，容易让业务开发过程陷入复杂的网络处理细节。RPC框架以编程语言中的本地函数调用形式，向应用开发者提供网络访问能力，这既封装了消息的编解码，也通过线程模型封装了多路复用，对业务开发很友好。

其中，Google推出的gRPC是性能最好的RPC框架之一，它支持Java、JavaScript、Python、GoLang、C++、Object-C、Android、Ruby等多种编程语言，还支持安全验证等特性，得到了广泛的应用，比如微服务中的Envoy、分布式机器学习中的TensorFlow，甚至华为去年推出重构互联网的New IP技术，都使用了gRPC框架。

然而，网络上教你使用gRPC框架的教程很多，却很少去谈gRPC是如何编码消息的。这样，一旦在大型分布式系统中出现疑难杂症，需要通过网络报文去定位问题发生在哪个系统、主机、进程中时，你就会毫无头绪。即使我们掌握了HTTP/2和Protobuf协议，但若不清楚gRPC的编码规则，还是无法分析抓取到的gRPC报文。而且，gRPC支持单向、双向的流式RPC调用，编程相对复杂一些，定位流式RPC调用引发的bug时，更需要我们掌握gRPC的编码原理。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eovXluTbBvyjZQ5zY8e3AZLONj6Qx5mcF4G7ZWYVbeicDzOlakFj4dKh6jCFHfqXvrLccuiaxYicmTxg/132" width="30px"><span>远方的风</span> 👍（21） 💬（1）<div>老师的广度和深度是如何练成的呢，是看书，还是实际工作中都有涉及？一开始搞web开发的，对底层这些研究的就没这么深了</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a9/cb/a431bde5.jpg" width="30px"><span>木头发芽</span> 👍（4） 💬（1）<div>公司所有项目(小程序端除外)都选型用了gRPC,不止微服务之间还包括了移动端,web端到服务器的通信.
18年开始使用时还遇到不小的阻力,特别是客户端离开了http+json的舒适区转到gRpc+pb 要研究怎么使用.也遇到了不少坑比如:
iOS的protoc编出的代码无法建立tls连接一致卡在证书校验步骤.
grpc-web在浏览器http1.1转http2的问题.
envoy做代理和负载均衡导致大量连接处于closed状态的问题.
在走完一遍后,后面就用起来非常的爽了.

不过流的用法还没实践,通过这节课又加深了一些,找个版本使用一下流方式的接口.</div>2020-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/56/75/6bf38a1e.jpg" width="30px"><span>坤哥</span> 👍（2） 💬（1）<div>陶哥，你的技术真不简单了，买了第二门web协议讲课程，希望能跟随你的步伐成长，你比我老大更牛</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/63/5e/799cd6dc.jpg" width="30px"><span>🎧重返归途</span> 👍（1） 💬（1）<div>protobuf是属于协议还是文件格式，看到有资料说把protobuf和json和xml作比较？合适么？</div>2020-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/91/962eba1a.jpg" width="30px"><span>唐朝首都</span> 👍（1） 💬（1）<div>基本原理+工具使用，理论结合实践才能把这些协议搞清楚呀！</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（1） 💬（1）<div>“分析包体时，可以通过 Stream 中 Length-Prefixed Message 头部，确认 DATA 帧中含有多少个消息，因此可以确定这是一元模式还是流式调用”
——————————————————
老师好，Length-Prefixed Message 头部不是只有长度和是否压缩吗？怎么能确认有多少个消息的？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（1） 💬（1）<div>client流模式中是不是每一个rpc请求消息的第一个data帧中才有Length-Prefixed Message ，然后下一个data帧只有protobuf数据，直到这个rpc请求消息发完。然后同一个stream上的下一个rpc消息的第一个data帧再加入Length-Prefixed Message 。以此类推。</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/ee/46/7d65ae37.jpg" width="30px"><span>木几丶</span> 👍（0） 💬（0）<div>老师，从抓包看，grpc三次握手后升级为HTTP2协议，为什么既没有基于TCP的101状态码升级，也没有基于TLS握手升级呢？直接就开始发送MAGIC帧了</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（0）<div>老师，我又试了一下，如果消息内容比较大，压缩会缩小尺寸，如果消息内容比较小，压缩反而会增大尺寸。</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（0） 💬（0）<div>老师，这两节课受益匪浅，自己实践了一下。我的消息内容只有一个7个字节的字符串，加上序号和类型是9个字节，如果不压缩，消息体就是9个字节，如果压缩，在grpc消息中有这么一条：Message-encoded entity body (gzip): 33 bytes -&gt; 9 bytes，消息体还是一样的，这33字节是怎么来的呢？为什么9个字节的body也没有变化呢？</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（0）<div>记得以前看到说， 帧的最后4个字节就是StreamId，接收方通过StreamId从乱序的帧中识别出相同StreamId的帧序列，按照顺序组装起来就实现了虚拟的“流”。
</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f9/30/54c71bf9.jpg" width="30px"><span>不会飞的海燕</span> 👍（0） 💬（0）<div>老师有grpc方面的优化，深度定制案例 介绍吗</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（0）<div>从http1.1 升级到 http2.0 要哪些地方改造呢，就改个versionCode 吗</div>2020-06-15</li><br/>
</ul>