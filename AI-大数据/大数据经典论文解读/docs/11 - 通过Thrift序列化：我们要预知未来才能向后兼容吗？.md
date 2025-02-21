你好，我是徐文浩。

现在，我们已经解读完了GFS、MapReduce以及Bigtable这三篇论文，这三篇论文之所以被称为Google的三驾马车，一方面是因为它们发表得早，分别在2003、2004和2006年就发表了。另一方面，是这三篇论文正好覆盖了大数据的存储、大数据的批处理也就是计算，以及大数据的在线服务领域。

相信你到这里，也看到了一个反复出现的关键字，那就是“数据”。在过去的三篇论文里，我们花了很多精力去分析谷歌是如何设计了分布式的系统架构，数据在硬件层面应该怎么存储。其中的很多设计面临的主要瓶颈和挑战，就是硬盘读写和网络传输性能。比如GFS里的数据复制，需要走流水线式的传输就是为了减少网络传输的数据量；Bigtable里，我们会对一个个data block进行压缩，目的是让数据存储的空间可以小一些。

**那么，我们能不能在“数据”本身上直接做点文章呢？**答案当然是可以的，今天这节课，我们就来一起读一篇Facebook在2007年发表的[《Thrift: Scalable Cross-Language Services Implementation》](https://thrift.apache.org/static/files/thrift-20070401.pdf)技术论文，它的背后也就是这Apache Thrift这个开源项目。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/00/4e/be2b206b.jpg" width="30px"><span>吴小智</span> 👍（20） 💬（0）<div>对于思考题，能想到两个问题：1. 每次需要传输到数据多了，对于 RPC 不是长链接交互的场景，每次都需要带上 Header，就跟 HTTP 一样每次都传输了重复的数据；2. 那就是需要每次都要解析 Header ，然后在对数据进行序列化，多做了运算，Thrift 生成代码的方式，就是把解析 Header 的这个计算，直接变成代码了，直接就可以对数据进行序列化，会快一点。</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（9） 💬（0）<div>2007年发表的Thrift论文，提到自己的优点在于提供了一套语言中立的软件栈，以很低的性能代价获得了很高的开发效率和系统可靠性。核心组件包括Types、Transport、Protocol、Versioning和Processors，Types是指跨语言的类型系统，开发者不用定义任何类型的序列化代码，Transport是指开发者可以灵活定义数据的来源和目的地，可能是网络，可能是内存的片段，也可能是文件，Protocol是指数据的序列化和反序列化过程，开发者通常不用关心，如果有需要也可以定制，Versioning是指协议支持版本，使得客户端可以向前向后兼容，Processors指的是数据的处理器，具体的逻辑由开发者实现。这种灵活的软件栈的代价是，The performance tradeoff incurred by an abstracted I&#47;O layer (roughly one virtual method lookup &#47; function call per operation) was immaterial compared to the cost of actual I&#47;O operations (typically invoking system calls)，也就是没什么代价。</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（9） 💬（0）<div>徐老师好，TCompactProtocol处理Delta Encoding的方式非常巧妙，通过判断Field第一个字节的高4位是否为0，得知到底是用了一个还是多个字节存储fieldId和fieldType。
readFieldBegin()的部分源码：
```
&#47;&#47; mask off the 4 MSB of the type header. it could contain a field id delta.
short modifier = (short)((type &amp; 0xf0) &gt;&gt; 4);
if (modifier == 0) {
  &#47;&#47; not a delta. look ahead for the zigzag varint field id.
  fieldId = readI16();
} else {
  &#47;&#47; has a delta. add the delta to the last read field id.
  fieldId = (short)(lastFieldId_ + modifier);
}
```
writeFieldBeginInternal()的部分源码：
```
&#47;&#47; check if we can use delta encoding for the field id
if (field.id &gt; lastFieldId_ &amp;&amp; field.id - lastFieldId_ &lt;= 15) {
  &#47;&#47; write them together
  writeByteDirect((field.id - lastFieldId_) &lt;&lt; 4 | typeToWrite);
} else {
  &#47;&#47; write them separate
  writeByteDirect(typeToWrite);
  writeI16(field.id);
}
```


直接把IDL写入协议的Header，协议的接收者可以根据Header的信息得知如何解析协议，但是如果每次传输的数据量不大，额外传输的IDL就会成为严重的网络负担。Apache Avro很好的解决了这个问题，在Apache Avro Specification的Protocol Declaration&#47;Protocol Wire Format&#47;Schema Resolution&#47;Parsing Canonical Form for Schemas四个章节中详细地描述了整个过程。

谁负责写数据，就以谁的IDL为准。当客户端第一次发起一种请求时，会先发送一条消息（HandshakeRequest），告知服务端接下来的请求的IDL，服务端会响应消息（HandshakeResponse），告知服务端针对这个请求响应的IDL。之后再发起相同类型的请求时，只需要发送IDL的指纹，指纹对的上，接收方就使用缓存的IDL，如果对不上，接收方会要求发送方重发Handshake。哪些内容构成了一个IDL的指纹呢？并非整个文本，因为在文本中增加一个空格，调整字段的书写顺序，并不影响数据的序列化和反序列化，只有真正影响序列化和反序列化的内容，才会被当作计算指纹的一部分。</div>2021-10-13</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（4） 💬（0）<div>其实这题我们还真做过，主要的问题是thrift是需要预先编译的，但是也不是没有法子，我就提个当时解决问题的关键字，janino。</div>2021-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c6/c0/dab2830e.jpg" width="30px"><span>平然</span> 👍（3） 💬（1）<div>TCompactProtocol 中为什么还要记录field type，不是在IDL能查到么。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2d/75/e7c29de4.jpg" width="30px"><span>wkq2786130</span> 👍（2） 💬（0）<div>很棒的文章，看完以后自己也总结了一下 放在 http:&#47;&#47;weikeqin.com&#47;2022&#47;06&#47;26&#47;thrift-protocol&#47;</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4f/40/6cfa75cb.jpg" width="30px"><span>哈达syn$</span> 👍（2） 💬（0）<div>老师会讲 lsm 相关的论文吗</div>2021-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/e1/aa0af424.jpg" width="30px"><span>可加</span> 👍（1） 💬（0）<div>模块之间的正交性是怎么理解的？尽量解耦的意思吗？</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（1） 💬（0）<div>思考题:IDL 直接序列化，然后放到存储实际数据的 Header 里呢？
这样做对于动态语言是友好的，动态语言可以根据IDL来实时生成数据结构，但是对于静态语言通常情况下都是事先通过IDL来生成不同语言的数据结构，居于这个前题那大可不必把IDL都传输，只需要传输IDL的版本号即可。
上面只是从编解码的角度讨论了IDL是否需要通过Header来保存，试想如果从数据逻辑处理角度看，在事前不知道会有什么样的数据的情况下，自然这些数据也不知道怎么处理，那么把这些解出来貌似就是一种浪费。
如果只是把数据持久化后，让后续程序来处理，那么从保存不同版本IDL的角度考虑，是有必要把IDL单独持久化，只是在设计上，可以调整为用版本号来对应IDL（每个版本的IDL单独保存），而不需要在每块数据的Head上都保存一份IDL信息。</div>2021-10-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJrOl63enWXCRxN0SoucliclBme0qrRb19ATrWIOIvibKIz8UAuVgicBMibIVUznerHnjotI4dm6ibODA/132" width="30px"><span>Helios</span> 👍（0） 💬（0）<div>放在header里面对于强类型需要来说还是需要定义一套schema的，感觉没啥意义而且还要浪费解析的性能，自己包体变大。</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/22/f4/9fd6f8f0.jpg" width="30px"><span>核桃</span> 👍（0） 💬（0）<div>ZigZag编码的方式，把负数变成正数，然后乘以2。这里怎么知道开头第一位的1到底是什么作用呢？就是是读取下一个字节还是负数？</div>2021-11-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/60/be0a8805.jpg" width="30px"><span>陈迪</span> 👍（0） 💬（0）<div>思考题：avro就是这么做的？ 可以不用事先生成代码了，我觉得不适合比如微服务之间的API调用，IDL还有文档的作用。 业务代码总归是要知道数据的严格结构的，不然业务代码咋往下写呢，那么还得有个文档</div>2021-10-15</li><br/>
</ul>