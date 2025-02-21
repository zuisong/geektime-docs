这一讲是“飞翔篇”的最后一讲，而HTTP的所有知识也差不多快学完了。

前面你已经看到了新的HTTP/2和HTTP/3协议，了解了它们的特点和工作原理，如果再联系上前几天“安全篇”的HTTPS，你可能又会发出疑问：

“刚费了好大的力气升级到HTTPS，这又出了一个HTTP/2，还有再次升级的必要吗？”

与各大浏览器“强推”HTTPS的待遇不一样，HTTP/2的公布可谓是“波澜不惊”。虽然它是HTTP协议的一个重大升级，但Apple、Google等科技巨头并没有像HTTPS那样给予大量资源的支持。

直到今天，HTTP/2在互联网上还是处于“不温不火”的状态，虽然已经有了不少的网站改造升级到了HTTP/2，但普及的速度远不及HTTPS。

所以，你有这样的疑问也是很自然的，升级到HTTP/2究竟能给我们带来多少好处呢？到底“值不值”呢？

## HTTP/2的优点

前面的几讲主要关注了HTTP/2的内部实现，今天我们就来看看它有哪些优点和缺点。

首先要说的是，HTTP/2最大的一个优点是**完全保持了与HTTP/1的兼容**，在语义上没有任何变化，之前在HTTP上的所有投入都不会浪费。

因为兼容HTTP/1，所以HTTP/2也具有HTTP/1的所有优点，并且“基本”解决了HTTP/1的所有缺点，安全与性能兼顾，可以认为是“更安全的HTTP、更快的HTTPS”。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/af/e6/9c77acff.jpg" width="30px"><span>我行我素</span> 👍（58） 💬（2）<div>2.因为HTTP&#47;2中使用小颗粒化的资源，优化了缓存，而使用精灵图就相当于传输大文件，但是大文件会延迟客户端的处理执行，并且缓存失效的开销很昂贵，很少数量的数据更新就会使整个精灵图失效，需要重新下载(http1中使用精灵图是为了减少请求)；
HTTP1中使用内联资源也是为了减少请求，内联资源没有办法独立缓存，破坏了HTTP&#47;2的多路复用和优先级策略；
域名分片在HTTP1中是为了突破浏览器每个域名下同时连接数，但是这在HTTP&#47;2中使用多路复用解决了这个问题，如果使用域名分片反而会限制HTTP2的自由发挥</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（18） 💬（2）<div>课下作业的第二题的个人理解。

问： 精灵图（Spriting）、资源内联（inlining）、域名分片（Sharding）这些手段为什么会对 HTTP&#47;2 的性能优化造成反效果呢？

答：主要是缓存和请求速度的原因。使用 HTTP&#47;2 后，请求就可以做到乱序收发、多路复用。

1. 图片就算很多，在 HTTP&#47;2 也可以做到 “并发”。使用了精灵图的话，首先文件变大了，在 HTTP&#47;2 中相比分开请求要更慢，而且不利于缓存（比如修改了其中几个图片）。

2. 资源内联，是指将一个资源作为另一个资源的一部分，使二者作为一个整体的资源来请求，比如 HTML 文件里嵌入 base64 的图片，该方案是为了减少 HTTP&#47;1 下的请求数，加快网页响应时间。HTTP&#47;2 不存在网页加载变慢的情况，而且不内联的话，能更好地发挥缓存的优势（比如图片是固定的，但 HTML 是动态的）。

3. 域名分片。这个不是很懂，老师在本文也说到： “HTTP&#47;2 对一个域名只开一个连接，所以一旦这个连接出问题，那么整个网站的体验也就变差了”。这么来说，域名分片建立多个连接，貌似就可以解决这个问题？如果不考虑这个问题的话，因为多路复用的原因，就算多了一个连接，也只是变成了两个多路复用，并没有提高多少效率，倒不是很有必要，而且代码实现也会比较麻烦。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/e5/eed499a6.jpg" width="30px"><span>Geek_hfbm3l</span> 👍（10） 💬（1）<div>老师这么理解有错吗？
http1 最好把多个请求合成一个请求（比如精灵图，资源内联，域名分片等），原因是 http1 存在 http 的队头阻塞，每次发送新的请求都又需要带上没有压缩的请求头，DNS及时有缓存也需要查找，而且有时候会被清空。http2 某些情况比如精灵图，资源内联就不需要合成一个请求，因为 http2 是基于流和帧的，没有了 http1 的队头阻塞，可以并发多个请求，而且 http2 的请求头使用了 hpage 压缩算法，下一次请求时请求头的长度会非常短（比如 65 一个数字就能表示以前的一长串 UA）。而且还加入了服务器推送，服务器会预先把可能需要的资源先推送给你。如果还是使用一个请求，可能会因为只更新一点点资源而更新整个缓存（比如更新精灵图或资源内联其中的一小部分）。</div>2019-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（6） 💬（1）<div>分析一下是否应该迁移到 HTTP&#47;2，有没有难点？
从慢、贵、难三个角度来分析
速度快，免费，部署简单，具体分析过程就不写了，我觉得应该立即迁移到 HTTP&#47;2。

精灵图（Spriting）、资源内联（inlining）、域名分片（Sharding）这些手段为什么会对 HTTP&#47;2 的性能优化造成反效果呢？
精灵图、资源内联可以减少HTTP请求数但加大单个请求的大小、域名分片为了突破与同一域名最多建立6个连接的限制，HTTP&#47;2使用流并发请求响应多个资源，完全不需要此优化，相反还会多建立TCP连接浪费资源。
</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（3） 💬（1）<div>HTTP&#47;1 里实现了长连接，为啥还会对一个域名开 6~8 个连接，是不是http为了解决http自身的对头阻塞，不要让http等待完响应之后，才发出下一个请求，而打开多个连接？这些打开了的连接会得到重复利用，就是一段时间内不会关闭？这样才会比HTTP（短连接）高效？
可以解析一下内联资源，域名分片，什么意思？</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/3f/34e5c750.jpg" width="30px"><span>看，有只猪</span> 👍（2） 💬（1）<div>老师，我还有一个问题，既然通过ALPN协商了通信采用的协议，那建立好TLS连接后，后续操作直接采用HTTP2即可，为什么还需要发送Magic呢</div>2019-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>看了下tmall.com，协议写的是https</div>2023-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/62/10/c1b4770d.jpg" width="30px"><span>球魁</span> 👍（1） 💬（1）<div>老师你好，目前我们团队正在尝试升级HTTP&#47;2协议，考虑到原域名下有很多其它团队的接口服务，我们使用一个新的域名来升级HTTP&#47;2，然后把接口逐步迁移过去。最近打算迁移一个流量很大的接口大概2000qps，前期对其做了5%小流量实验，但是结果很不理想，性能并没有提升反而劣化了。跑了一下每个阶段的耗时，发现服务端耗时大概有15-20ms的下降（接口平均耗时900ms），tcp有10ms的下降，ssl也有5-10ms的下降，请问有什么好的优化升级建议嘛？</div>2022-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJayib1ZcRfOaoLsdsWZokiaO5tLAdC4uNAicQJRIVXrz9fIchib7QwXibnRrsJaoh5TUlia7faUf36g8Bw/132" width="30px"><span>明月</span> 👍（1） 💬（2）<div>精灵图、资源内联在http2效果不好 终极原因也还是http2只能建立一个连接 这样一个大文件传输会占用这唯一的连接 缓存失效后又要更新占用这个连接更新资源 我理解的对吗</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5c/3f/34e5c750.jpg" width="30px"><span>看，有只猪</span> 👍（1） 💬（1）<div>老师，请问我对服务发现的理解对吗？
针对加密版本的HTTP&#47;2，客户端需要`Client Hello`的`ALPN`中添加支持的协议，由服务器选择，服务器也通过`ALPN`告知客户端后续通信采用的协议。
非加密版本的HTTP&#47;1中，客户端建立TCP连接后，将发送Magic。服务器识别到后，后续通信采用HTTP&#47;2。</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（1） 💬（2）<div>TCP 协议存在“队头阻塞”，所以 HTTP&#47;2 在弱网或者移动网络下的性能表现会不如 HTTP&#47;1；
老师，HTTP&#47;1，HTTP&#47;2都是基于TCP协议的，在同样“队头阻塞”的情况下，为什么HTTP&#47;1的性能要优于HTTP&#47;2 ？</div>2019-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/77/b2ab5d44.jpg" width="30px"><span>👻 小二</span> 👍（1） 💬（1）<div>有一点我不明白， http2只有一条连接， 那在多线程并发时， 应该需要锁吧， 也就是同一瞬间只能一个写入，多几条连接， 不是能并发吗？
还是说网卡层同一瞬间也只能处理一个写的请求， 所以并不并发都没关系。不过在tcp层面上的队头阻塞还是有关系的吧， 多 开一个连接， 就不会都阻塞住了

如果有多个网卡呢？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/8a/bc8cb43c.jpg" width="30px"><span>路边的猪</span> 👍（0） 💬（1）<div>为什么在使用http2的时候不可以在一个网站内多开几个tcp连接，这岂不是更高效</div>2023-02-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7JkdLdZXNYZeopVSxeI8ml4MptQMCWI7oIHaJpfYuYjlV9Efic7x19lWickckLQzmTuFlgCVmVicZ9A/132" width="30px"><span>Geek_0e3b40</span> 👍（0） 💬（1）<div>老师，请教一个关于http&#47;2的问题：
如果客户端向服务端同时发起多个请求，那服务端收到请求的顺序会和客户端发起的顺序一样吗？</div>2022-12-09</li><br/><li><img src="" width="30px"><span>Geek_8476da</span> 👍（0） 💬（1）<div>学习http到最好
好的方法应该是实践！！！</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/95/640b6465.jpg" width="30px"><span>fmouse</span> 👍（0） 💬（1）<div>老师好，对于 HTTP&#47;2 的“服务发现”用 TLS 的扩展里“ALPN”。
在 《30｜时代之风（上）：HTTP&#47;2特性概览》提到“在 HTTP&#47;2 标准制定的时候（2015 年）已经发现了很多 SSL&#47;TLS 的弱点，而新的 TLS1.3 还未发布。”
TLS1.2+的时候已经支持扩展特性了是吗。</div>2022-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（0） 💬（1）<div>老师，http2 多开几个连接，岂不是很厉害吗，为啥要限制一个，之前还6-8个呢？</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>老师课外小贴士第四条connection：upgrade应该是明文的http 1携带的字段吧  升级到HTTP2之前客户端和服务器不应该是通过HTTP1通信吗</div>2021-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/22/4e/2e081d9c.jpg" width="30px"><span>hao</span> 👍（0） 💬（1）<div>精灵图（Spriting）、资源内联（inlining）、域名分片（Sharding）这些手段为什么会对HTTP&#47;2的性能优化造成反效果呢 ？


- 精灵图（Spriting）和资源内联（inlining）减少了请求数但增加了每次请求的报文大小，但  `不利于缓存`（精灵图中某个图标改动就要重新请求整个精灵图，资源内联同理）

  &gt; 资源内联：内嵌css  、js等资源


  - 对于HTTP&#47;1来说，因为它存在  `队头阻塞`  ，所以将多个小的  `资源合并`  可以有效的缓解这种情况的出现
  - 但对于HTTP&#47;2来说，它已经引入了流的概念实现了基于单个TCP连接的多路复用，也就是说解决了  `HTTP的队头阻塞`，它不需要通过资源合并来缓解

- 域名分片是指利用多个域名和同一个IP地址建立TCP连接，巧妙地避开了浏览器对并发连接数的限制


  - 对于HTTP&#47;1来说，因为它没有  `多路复用`  ，所以这样能很好的缓解因为  `丢包重发`  而导致的  `队头阻塞`  
  - 但对于HTTP&#47;2来说，多建立的TCP连接完全是浪费资源（两端的静态表和动态表，TCP连接的成本等）  </div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>迁移到HTTP&#47;2感觉成本小收益高，好像没有什么理由不迁移一下，除了弱网环境下性能差一些，是否还有什么不利影响呢？或者不想改变也是一种原因，谁知道新东西是否有什么坑呢？</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/53/05aa9573.jpg" width="30px"><span>keep it simple</span> 👍（0） 💬（1）<div>看上去迁移到HTTP&#47;2完全不需要改应用代码呀，只需要修改nginx配置就行</div>2020-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/27/f6215028.jpg" width="30px"><span>红军</span> 👍（0） 💬（1）<div>如果浏览器比较老，只支持http1，访问http2服务器可以工作吗
</div>2019-08-12</li><br/>
</ul>