“透视HTTP协议”这个专栏已经陪伴了你近三个月的时间，在最后的这两讲里，我将把散落在前面各个章节的零散知识点整合起来，做一个总结，和你一起聊聊HTTP的性能优化。

由于HTTPS（SSL/TLS）的优化已经在[第28讲](https://time.geekbang.org/column/article/111287)里介绍的比较详细了，所以这次就暂时略过不谈，你可以课后再找机会复习。

既然要做性能优化，那么，我们就需要知道：什么是性能？它都有哪些指标，又应该如何度量，进而采取哪些手段去优化？

“性能”其实是一个复杂的概念。不同的人、不同的应用场景都会对它有不同的定义。对于HTTP来说，它又是一个非常复杂的系统，里面有非常多的角色，所以很难用一两个简单的词就能把性能描述清楚。

还是从HTTP最基本的“请求-应答”模型来着手吧。在这个模型里有两个角色：客户端和服务器，还有中间的传输链路，考查性能就可以看这三个部分。

![unpreview](https://static001.geekbang.org/resource/image/3a/62/3a8ab1e3ace62d184adc2dc595d32f62.png?wh=1142%2A426)

## HTTP服务器

我们先来看看服务器，它一般运行在Linux操作系统上，用Apache、Nginx等Web服务器软件对外提供服务，所以，性能的含义就是它的服务能力，也就是尽可能多、尽可能快地处理用户的请求。

衡量服务器性能的主要指标有三个：**吞吐量**（requests per second）、**并发数**（concurrency）和**响应时间**（time per request）。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（24） 💬（2）<div>你有 HTTP 性能优化的经验吗？常用的有哪些方法？
本人生产环境中会用到的：tcp fast open，DNS，HTTP缓存，DNS-prefetch

你是怎么理解客户端的“延迟”的？应该怎样降低延迟？
就是客户端与服务器一次请求响应的往反时间，降低延迟的话用DNS缓存，TCP连接复用，使用CDN，应该可以降低延迟。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d2/78/1f1b45f9.jpg" width="30px"><span>Jaykey</span> 👍（9） 💬（1）<div>把课程中学习到的技术用到了生产上，给Nginx添加了缓存控制的头，保证了每一次上线之后资源能更新到用户的设备上，作为前端驱动运维的方式</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（5） 💬（1）<div>1. 你有 HTTP 性能优化的经验吗？常用的有哪些方法？
优化业务逻辑、启用缓存减少交互次数、开启压缩、按需传输(图片的裁剪)减少传输体积；
后端服务器的弹性负载，确保后端服务运行正常。
另：客户端性能过剩，把一部分服务器的计算交给客户端来完成？
2. 你是怎么理解客户端的“延迟”的？应该怎样降低延迟？
客户端与服务端的交互的环节过多、环节耗时过长就会出现延迟。
服务端使用高版本的HTTP协议，在耗时长的环节，用钱和空间换时间。</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/b5/b4/f31c09aa.jpg" width="30px"><span>Wakeup</span> 👍（4） 💬（1）<div>老师 我对比了下瀑布图 感觉http1的content download的时间比http2的要短，请问下为什么
然后在一个连接上，并发请求很多资源，服务器的资源就不会耗尽了吗？
为什么多个h2请求中间如果有h1，并发会被h1阻断</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（4） 💬（4）<div>老师，再请教一个知识，ATM,帧中继这种是属于局域网技术吗？那中间一公里用到了哪些网络技术呢？底层还是以太网这种协议吗？中间一公里是不是有特殊的协议？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（4） 💬（2）<div>光进铜退这里的铜是说的最后一公里吗？即使是铜的时代那中间一公里也是用的光纤吧？这叫主干网？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（3） 💬（1）<div>在浏览器，资源文件获取还是挺耗时间的，尽量把静态资源资源文件合并，css文件，js文件这些能合并就合并，图片能拼就拼，能用CDN，绝不用服务器。</div>2020-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（2） 💬（1）<div>程序上大图片和大视频进行质量压缩，返给接口压缩后的文件</div>2023-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（2） 💬（1）<div>目前解决的现场问题 瓶颈在数据库 还没到http传输层面 并且这个是内网服务 访问的范围在市内 这种的话还属于老师您说的三公里模型吗</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（2） 💬（3）<div>老师，为什么因为队头阻塞所以浏览器允许只能并发6个请求呢？</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a8/1e/4ec85e24.jpg" width="30px"><span>joel</span> 👍（1） 💬（2）<div>老师，请教一个关于最多6个并发连接的问题。
假如现在有10个资源，一个tcp 最多支持6个请求，那当第7个请求的时候，能不能在重新开一个tcp 链接，然后继续请求资源。还是说只能在现有的tcp 链接上等待。</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（1） 💬（1）<div>中间一公里的说法很容易引起混淆，尤其是对熟悉通信网复杂性的工程师而已更加费解。</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>业务侧角度：减少非必要接口调用、检查重复接口调用情况、修改接口数据结构，提取公共参数减少数组的重复参数、梳理优化浏览器的渲染</div>2024-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/e7/a6c603cf.jpg" width="30px"><span>GitHubGanKai</span> 👍（0） 💬（1）<div>老师，有关http性能优化这块，假设在用户在浏览器中的前端页面同时发起了6个请求，那么请求过程中，涉及到的性能相关的就比较多，比如说用户网络质量，服务器处理的性能等很多因素，那我我的疑问是：在浏览器中通过http发送请求的时候，在http或者tcp这层关系中，是否会做什么优化吗？比如网络不好的情况下，在tcp这层发送的包就比较小，网络好的时候，就发送的报文包就大一点，是否会有这样的优化？我们做前端开发的在做性能优化的时候，对于网络差的情况下，有没有什么方法能够在传输过程中控制http传输包的大小呢？，比如网络差就发送小一点的包，网络好就传输大点的包，从而根据网络好坏进行传输优化。</div>2023-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/d0/0d/752ff95f.jpg" width="30px"><span>justorez</span> 👍（0） 💬（1）<div>资源消耗瀑布图，排队时间说错了吧？Resource scheduling queueing 4.2ms 才是排队时间吧</div>2023-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（0） 💬（1）<div>感觉还有好多比如数据库的读写，线程（协程）的并发通信以及锁的粒度也可能影响速度，还有静态资源在浏览器的渲染也挺费时间的。</div>2021-10-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLFMU0wXIHE51jLWGrfEI9fpgyYcSYqJXSRicO55SXibJ9dgpudavKia0OMIjkx08M6beSYDtYQF360g/132" width="30px"><span>胡戎</span> 👍（0） 💬（1）<div>“总时间 415.04 毫秒里占了差不多 99%。”
我一直在怀疑jmeter等测试工具测试的响应时间指标是否准确，如webgis系统。
老师有没有什么方法可以准确的测出用户从请求到渲染排版结束正常显示的时间，特别是多用户。</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/6b/13/38a14e66.jpg" width="30px"><span>果汁</span> 👍（0） 💬（1）<div>老师我想问一下那个并发6个请求的问题，应该不只是6个XHR请求吧，其中也包括请求js、css文件这些请求</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（2）<div>性能优化的思路是相通的，不过具体到每一个细分的领域具体措施又是不一样的。
作为业务研发除代码层、系统设置层、软件系统架构层的性能优化，感觉其他的涉足的都比较少，感觉无能为力，比如：带宽不够、机器不好这些公司级别的人物才能推动。

水管理论，找“细管”，然后换“粗管”，如果换不了基本没辙了。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（0） 💬（1）<div>老师好，想请问对于 HTTP 的首字节优化可以从哪些地方入手呢？根据 Chrome 的分析来看，从响应开始，首字节占据了很大一部分时间。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（0） 💬（1）<div>ab测试，就是破坏rfc的标准。这个标准服务器端是没法限制的，只能靠客户端的自觉性。</div>2019-09-03</li><br/>
</ul>