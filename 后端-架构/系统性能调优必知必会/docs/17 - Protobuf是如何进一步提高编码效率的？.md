你好，我是陶辉。

上一讲介绍的HTTP/2协议在编码上拥有非常高的空间利用率，这一讲我们看看，相比其中的HPACK编码技术，Protobuf又是通过哪些新招式进一步提升编码效率的。

Google在2008年推出的Protobuf，是一个针对具体编程语言的编解码工具。它面向Windows、Linux等多种平台，也支持Java、Python、Golang、C++、Javascript等多种面向对象编程语言。使用Protobuf编码消息速度很快，消耗的CPU计算力也不多，而且编码后的字符流体积远远小于JSON等格式，能够大量节约昂贵的带宽，因此gRPC也把Protobuf作为底层的编解码协议。

然而，很多同学并不清楚Protobuf到底是怎样做到这一点的。这样，当你希望通过更换通讯协议这个高成本手段，提升整个分布式系统的性能时，面对可供选择的众多通讯协议，仅凭第三方的性能测试报告，你仍将难以作出抉择。

而且，面对分布式系统中的疑难杂症，往往需要通过分析抓取到的网络报文，确定到底是哪个组件出现了问题。可是由于Protobuf编码太过紧凑，即使对照着Proto消息格式文件，在不清楚编码逻辑时，你也很难解析出消息内容。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/19/f9/62ae32d7.jpg" width="30px"><span>Ken</span> 👍（40） 💬（2）<div>gRPC基于Http2可以复用http2带来的新特性，比如双向流，单连接多路复用，头部压缩（hpack）。protobuf解决的是body的序列化空间效率，hpack解决的是header的空间效率，两者不冲突。</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（9） 💬（3）<div>wireshark支持protobuf协议插件：https:&#47;&#47;code.google.com&#47;archive&#47;p&#47;protobuf-wireshark&#47;downloads</div>2020-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（9） 💬（1）<div>protobuf需要通信双方提前约定好proto文件，这是一个限制，限制了它的使用场景。而http2没有这个要求，是一种更通用的设计，只要符合规范，就可以通信。</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/11/78/4f0cd172.jpg" width="30px"><span>妥协</span> 👍（4） 💬（1）<div>protobuf是按照字段名，字段类型和字段值编码。如果传输的是表格数据，就是第一行是多个字段，后面的多行都是字段值，这种情况下，字段名和字段类型只在第一行时传输，后面的多行字段值记录就不用传输了，这种效率是不是更高些?我们公司的自定义协议应该就是这种</div>2020-06-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erbY9UsqHZhhVoI69yXNibBBg0TRdUVsKLMg2UZ1R3NJxXdMicqceI5yhdKZ5Ad6CJYO0XpFHlJzIYQ/132" width="30px"><span>饭团</span> 👍（3） 💬（1）<div>老师，请问红色和蓝色位为保留位，请问蓝色是出于什么目的？</div>2020-06-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rRCSdTPyqWcW6U8DO9xL55ictNPlbQ38VAcaBNgibqaAhcH7mn1W9ddxIJLlMiaA5sngBicMX02w2HP5pAWpBAJsag/132" width="30px"><span>butterfly</span> 👍（1） 💬（1）<div>一直有个疑问:
服务器端和客户端的两端都定义了.proto文件, 两端应该都是可以知道某个字段名字和值类型的。
如果只传输 字段的 顺序 和 值(字段名字和类型都不传输)，数据传到对端的时候， 再解码出来. 为什么不能这样做呢？</div>2021-03-22</li><br/><li><img src="" width="30px"><span>Geek_78d3bb</span> 👍（1） 💬（1）<div>json简化了xml，protobuffer又优化了json 的key部分，双方都在proto中定义了key，所以只传序号查proto就知道是什么key了</div>2020-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1d/cb/791d0f5e.jpg" width="30px"><span>寻己</span> 👍（0） 💬（2）<div>听懂了60，70％吧，谢谢</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（5） 💬（0）<div>参考这里https:&#47;&#47;developers.google.com&#47;protocol-buffers&#47;docs&#47;reference&#47;arenas，学习了下protobuf对于arenas的介绍。

arena相当于内存池的概念，预先分配一块大内存，当protobuf操作消息对象需要分配内存的时候，去arenas来取，使用完之后放回到arena里。

这种做法的优势在于，1，加速内存分配和释放。2，有效利用cache line。 3，减少CPU时间</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（5） 💬（0）<div>protobuf对body进行压缩，http2对header进行压缩。
http2还可以使用stream方式传输，这些都是protobuf没有的。</div>2020-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/ef/9c/275dfed4.jpg" width="30px"><span>诸葛子房</span> 👍（0） 💬（0）<div>protobuf怎么使用缓存的</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/ee/6e7c2264.jpg" width="30px"><span>Only now</span> 👍（0） 💬（0）<div>proto和h2不是一个层级上的技术。h2工作在更底层。 grgp2 可以利用h2实现灵活的双工请求，一定程度上增加交互效率。proto主要用来编码消息体，降低body体积。
</div>2020-11-20</li><br/>
</ul>