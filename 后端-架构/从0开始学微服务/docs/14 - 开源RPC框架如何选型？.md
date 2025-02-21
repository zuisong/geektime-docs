[专栏第6期](http://time.geekbang.org/column/article/15092)我给你讲解了RPC远程调用的原理，简单回顾一下一个完整的RPC框架主要有三部分组成：通信框架、通信协议、序列化和反序列化格式。根据我的经验，想要开发一个完整的RPC框架，并且应用到线上生产环境，至少需要投入三个人力半年以上的时间。这对于大部分中小团队来说，人力成本和时间成本都是不可接受的，所以我建议还是选择开源的RPC框架比较合适。

那么业界应用比较广泛的开源RPC框架有哪些呢？

简单划分的话，主要分为两类：一类是跟某种特定语言平台绑定的，另一类是与语言无关即跨语言平台的。

跟语言平台绑定的开源RPC框架主要有下面几种。

- Dubbo：国内最早开源的RPC框架，由阿里巴巴公司开发并于2011年末对外开源，仅支持Java语言。
- Motan：微博内部使用的RPC框架，于2016年对外开源，仅支持Java语言。
- Tars：腾讯内部使用的RPC框架，于2017年对外开源，仅支持C++语言。
- Spring Cloud：国外Pivotal公司2014年对外开源的RPC框架，仅支持Java语言，最近几年生态发展得比较好，是比较火的RPC框架。

而跨语言平台的开源RPC框架主要有以下几种。

- gRPC：Google于2015年对外开源的跨语言RPC框架，支持常用的C++、Java、Python、Go、Ruby、PHP、Android Java、Objective-C等多种语言。
- Thrift：最初是由Facebook开发的内部系统跨语言的RPC框架，2007年贡献给了Apache基金，成为Apache开源项目之一，支持常用的C++、Java、PHP、Python、Ruby、Erlang等多种语言。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/a9/dfea2c50.jpg" width="30px"><span>张龙大骗子</span> 👍（7） 💬（2）<div>tars不是介绍说支持C++、Java、PHP、NodeJS ，最近还发布了Go语言版本的</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/57/ee02ef41.jpg" width="30px"><span>大龄小学生</span> 👍（6） 💬（1）<div>老师，rpc和mq的优势是什么？感觉rpc能做的mq都能做。</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5a/a8/f25ec64c.jpg" width="30px"><span>long.mr</span> 👍（4） 💬（2）<div>胡老师，c++的，是不是也可以考虑下baidu rpc呢,性能在rpc里还是很强的哈~，对比的时候可以考虑下呀😄</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/84/b1/72e7744e.jpg" width="30px"><span>王晓军</span> 👍（2） 💬（1）<div>老师，为什么K8s和service fabric不在你的介绍范围，他们不是微服务框架吗？</div>2018-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a6/38/55483b8c.jpg" width="30px"><span>。</span> 👍（2） 💬（1）<div>老师你好，请问RPC接口和http接口咋区分？spring cloud的调用方式算rpc接口还是http接口？</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/45/6b/7912cba5.jpg" width="30px"><span>everpan</span> 👍（2） 💬（1）<div>tars支撑java php 最近还支持go了</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/1b/6685fb62.jpg" width="30px"><span>扬扬</span> 👍（0） 💬（1）<div>本人经常使用vs2010开发，但是grpc在开发平台的支持限制性太大了，如何破呢？</div>2018-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/e1/c9aacb37.jpg" width="30px"><span>段启超</span> 👍（0） 💬（1）<div>胡老师，“相比 Dubbo 和 Motan 所采用的私有协议来说，在高并发的通信场景下，性能相对要差一些
，所以对性能有苛刻要求的情况下，可以考虑 Dubbo 和 Motan”这里，应该是性能相对要好一些吧。</div>2018-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/62/954065d4.jpg" width="30px"><span>步＊亮</span> 👍（0） 💬（1）<div>老师你好，我想请教个问题。如果我们平台采用java语言开发，从而选择了springcloud框架。当有一个原有由c++实现的服务要作为服务提供者注册进来，可以实现么？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/90/54/21795a71.jpg" width="30px"><span>gggwvg</span> 👍（15） 💬（2）<div>Tars有完整的服务治理生态，支持多语言。</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（9） 💬（0）<div>感谢开源
感谢GITHUB
感谢这个时代</div>2019-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/0d/1fd1e17a.jpg" width="30px"><span>上官</span> 👍（6） 💬（3）<div>你好，请问常用的分布式事务解决方案有哪些</div>2018-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/76/26f555ce.jpg" width="30px"><span>上沅同学</span> 👍（5） 💬（0）<div>Tars目前已经支持多语言了，联系老师修改一下文章，不然容易误导读者，而且也有失偏颇</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/51/29/24739c58.jpg" width="30px"><span>凉人。</span> 👍（2） 💬（0）<div>微信这边用Hikit框架，支持proto。 支持C++和go</div>2020-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/ea/7ae90090.jpg" width="30px"><span>明天你好</span> 👍（1） 💬（0）<div>老师好，Grpc 字段值为0或者null时，字段不展示，有什么好的解决方案呢？
func TransProtoToJson (pb proto.Message) string{
	var pbMarshaler jsonpb.Marshaler
	pbMarshaler = jsonpb.Marshaler{
		EmitDefaults: true,
		OrigName:     true,
		EnumsAsInts:  true,
	}
	_buffer := new(bytes.Buffer)
	_ = pbMarshaler.Marshal(_buffer, pb)
	return string(_buffer.Bytes())
}
用这种方案，虽然显示字段，但是数字也转成了字符串</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/2c/22b7868c.jpg" width="30px"><span>GO_DIE</span> 👍（1） 💬（2）<div>老师，前端理论上也是可以直接rpc请求获取数据的，那为啥不用rpc替代传统的http接口请求方式呢？</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（1） 💬（0）<div>brpc更好</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/1b/6685fb62.jpg" width="30px"><span>扬扬</span> 👍（1） 💬（0）<div>本人经常使用vs2010开发，但是grpc在开发平台的支持限制性太大了，如何破呢？
开发语言使用的是C++，python</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/d4/b7719327.jpg" width="30px"><span>波波安</span> 👍（1） 💬（0）<div>gRPC的多语言支持，能够基于多种语言自动生成对应语言的客户端和服务端的代码。都是使用的pb对象做序列化和反序列化，没有额外的代理，性能应该会更好一点。
sidecar可以看作是一个代理，屏蔽了服务的底层实现，将服务发现，服务治理等功能抽象出来，做统一实现。但由于多了一层代理，性能应该会受到一些影响。
请老师指正。</div>2018-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/2c/b45cc122.jpg" width="30px"><span>极客达人</span> 👍（1） 💬（1）<div>为什么要用rpc框架？</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/c6/bebcbcf0.jpg" width="30px"><span>俯瞰风景.</span> 👍（0） 💬（0）<div>微服务框架选型要根据实际业务场景，一方面是代码的可维护性，一方面是性能。
选择好框架后，就要根据实际需求选择合适的开源组件进行搭配。
对于小团队来说，直接SpringCloud。</div>2021-10-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>为什么http协议要比dubbo协议慢啊,http2不是已经做了各种优化了吗?长连接,io多路复用,压缩header等手段</div>2021-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/d5/56b3a879.jpg" width="30px"><span>poettian</span> 👍（0） 💬（0）<div>老师，最近在看rpc，有个疑问：客户端需要实现连接池吗？我看大部分rpc框架都没有提供连接池的功能，是为什么呢？</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（0）<div>Tars支持N种语言</div>2019-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（0）<div>通信协议理论上不能算框架的一部分。</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5d/73/742097e2.jpg" width="30px"><span>joseph.herder💭.</span> 👍（0） 💬（0）<div>阿忠伯，对于已经拥有一个单体PHP应用，要做PHP微服务服务端，有哪些开源的方案，例如motan等已经足够成熟可以直接用起来？</div>2019-03-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erTVmW4sciaXvr1vxntvJKLcuNibB7mZLKicM8IV5nVULWtCAArMsMbclqQKR6fHFSID37PwBdkz1Cibw/132" width="30px"><span>木匠</span> 👍（0） 💬（0）<div>dubbo要做网关层，有没有好的实现方案，或开源框架</div>2018-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b7/c2/196932c7.jpg" width="30px"><span>南琛一梦</span> 👍（0） 💬（1）<div>老师，zuul这种适合用于对外公共API服务的网关吗？如果适合，token认证这块一般如何处理啊</div>2018-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/39/76/b14221a5.jpg" width="30px"><span>随风</span> 👍（0） 💬（0）<div>服务访问如果是基于rmi，但微服务基础框架还想基于springcloud，该怎么做呢？请指教！</div>2018-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/00/27/88d2f57b.jpg" width="30px"><span>zl</span> 👍（0） 💬（1）<div>老师画的图中顺序怎么都是反的，而不是从上层到底层，还有Motan介绍模块那也是 😂</div>2018-09-29</li><br/>
</ul>