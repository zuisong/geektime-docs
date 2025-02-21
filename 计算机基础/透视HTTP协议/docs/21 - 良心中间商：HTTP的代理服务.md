在前面讲HTTP协议的时候，我们严格遵循了HTTP的“请求-应答”模型，协议中只有两个互相通信的角色，分别是“请求方”浏览器（客户端）和“应答方”服务器。

今天，我们要在这个模型里引入一个新的角色，那就是HTTP代理。

引入HTTP代理后，原来简单的双方通信就变复杂了一些，加入了一个或者多个中间人，但整体上来看，还是一个有顺序关系的链条，而且链条里相邻的两个角色仍然是简单的一对一通信，不会出现越级的情况。

![](https://static001.geekbang.org/resource/image/28/f9/28237ef93ce0ddca076d2dc19c16fdf9.png?wh=2097%2A606)

链条的起点还是客户端（也就是浏览器），中间的角色被称为代理服务器（proxy server），链条的终点被称为源服务器（origin server），意思是数据的“源头”“起源”。

## 代理服务

“代理”这个词听起来好像很神秘，有点“高大上”的感觉。

但其实HTTP协议里对它并没有什么特别的描述，它就是在客户端和服务器原本的通信链路中插入的一个中间环节，也是一台服务器，但提供的是“代理服务”。

所谓的“代理服务”就是指服务本身不生产内容，而是处于中间位置转发上下游的请求和响应，具有双重身份：面向下游的用户时，表现为服务器，代表源服务器响应客户端的请求；而面向上游的源服务器时，又表现为客户端，代表客户端发送请求。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（58） 💬（4）<div>代理会增加链路长度，在代理上做一些复杂的处理。会很耗费性能，增加响应时间。
1.随机
2.轮询
3.一致性hash
4最近最少使用
5.链接最少</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/44/c0/cd2cd082.jpg" width="30px"><span>BoyiKia</span> 👍（26） 💬（2）<div>老师，我发现前几节课，四次挥手的时候，是客户端主动先发 Fin信号， 今天实验结果，是源服务器，先给代理服务器发的 Fin信号。老师，我有点疑惑哈。到底是谁应该先发。还是说都可以呢。</div>2020-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUdfNDQs3eLoIjfIXDm77W66udicLfqh6NA8QX4QuZNO48UlRTfDo2Fm2jGX0z3hjnbARib8wSbxcg/132" width="30px"><span>Demon</span> 👍（18） 💬（1）<div>很多场景下，使用代理的目的就是为了匿名，不让对方知道请求&#47;响应的来源在哪儿。除了在测试环境分析技术问题的场景，现实业务中有需要在报文中携带层层代理信息的应用case吗？</div>2020-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/e3/dd40ec58.jpg" width="30px"><span>火车日记</span> 👍（12） 💬（1）<div>1 补充几个，ip_hash 、最少连接数、最快连接数，根据场景应用
2 作为中转站，需要为上游和下游开启两个连接，大量并发请求，会出现性能瓶颈，应减少资源开销，加快响应速度，比如代理缓存，动静分离</div>2019-07-16</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/ZMALpD4bKCVdsx8ymCC5Oo0oxibxIFGQzT6fP2B8MEgLGLktQRX4ictobkbcNBDTQibjoQNKBmWCKomNibWqHZ5kpg/132" width="30px"><span>Long</span> 👍（9） 💬（1）<div>老师好,文中
&quot;服务器的 IP 地址应该是保密的，关系到企业的内网安全，所以一般不会让客户端知道。&quot;
是不是可以认为,域名所对应的IP地址和真实服务器的IP地址是不一样的呢?因为真实服务器的地址一般都是私网的IP地址.</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/7e/963c037c.jpg" width="30px"><span>Aaron</span> 👍（5） 💬（1）<div>『因为通过“X-Forwarded-For”操作代理信息必须要解析 HTTP 报文头，这对于代理来说成本比较高，原本只需要简单地转发消息就好，而现在却必须要费力解析数据再修改数据，会降低代理的转发性能。』
问：代理协议的 PROXY 不也是一个头吗？同样需要对 header 的操作。它的优势是不是只在于操作的内容比 &quot;X-Forwarded-For&quot; 少一点而已？

『另一个问题是“X-Forwarded-For”等头必须要修改原始报文，而有些情况下是不允许甚至不可能的（比如使用 HTTPS 通信被加密）』
问：为什么“X-Forwarded-For”等头必须要修改原始报文呢？不是很理解。烦请老师解释一下，谢谢。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/d9/4feb4006.jpg" width="30px"><span>lmingzhi</span> 👍（5） 💬（1）<div>老师，请问有什么检测http代理ip匿名性的手段？

是否只要检查请求头是否带有“X-Forwarded-For”和“X-Real-IP”及里面是否带有真实ip即可？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（4） 💬（2）<div>1.a 代理服务器与上下游的通信机制也是http协议，因此增加了传输中的数据泄漏和篡改风险，可以使用https解决。b 如果代理服务器发生故障，会影响客户端的正常访问，可以增加代理服务器的数量，并配置代理服务器负载均衡算法。c 由于多了代理服务器的请求响应过程，增加了从源客户端和源服务器之间的来回时间。
2.轮询，加权轮询，随机法，加权随机法，源地址哈希法，最小连接数法</div>2020-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（1）<div>1：你觉得代理有什么缺点？实际应用时如何避免？
代理代理就是找她人代替你去打理一些事情，让他人代办事情你必须交代好沟通好，那效率自然会低一些，另外，如果代理出问题了，那你的事自然也办不成了，所以，可能存在单点问题，不过一般还好。

2：你知道多少反向代理中使用的负载均衡算法？它们有什么优缺点？
随机——简单，是否均匀看随机情况
轮询（一般轮询、加权轮询）——相对简单，也会考虑机器资源和性能的均衡性
哈希（一般哈希、一致性哈希、带虚拟节点的一致性哈希）——相对复杂，要求越公平就会越复杂，而且适当考虑了请求
哈希槽，和redis类似

只有能使请求尽可能的高效分发就行，请教一下VPN和代理，本质是否差不多？</div>2020-03-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoSMRiaMtAcqQ6PWHrue81oR1Ujr7lX3Mz1P00aX2SBibUX51yz3zFqovTRIDiaTWNUlq4U0KV2zib2Uw/132" width="30px"><span>Geek_6ea9af</span> 👍（3） 💬（1）<div>老师，请问在配置了正向代理之后，对于真正服务端的域名解析是发生在客户端还是代理端？该代理服务器仅做请求转发。</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d3/40/0067d6db.jpg" width="30px"><span>AKA三皮</span> 👍（3） 💬（1）<div>代理是个好东西，比如各种精细化的流量控制，灰度发布，同时微服务拆分后，服务治理的相关功能也可以下沉到代理去做，比如 限流、熔断。选个高性能的网络代理是王道，比如envoy</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/b3/8fe66459.jpg" width="30px"><span>sarah</span> 👍（3） 💬（1）<div>老师，对图中wireshark的抓包有个疑问: 每一次的http报文后面会跟着一个tcp报文，这个tcp报文是怎么产生的？作用是什么？例如，第一个http报文，HTTP GET&#47;21-1 HTTP1.1后面的TCP 80–55061 </div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（3） 💬（1）<div>老师，微服务里的网关算不算一个增强版的代理服务器呢</div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/0a/da55228e.jpg" width="30px"><span>院长。</span> 👍（3） 💬（1）<div>老师后面会讲HTTP2.0吗</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（3） 💬（1）<div>代理服务器如何连接源服务器？用 http1.0 短连接的效率不太好吧？集群一般都是局域网吗？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（2） 💬（1）<div>HAProxy是不是就是MuleSoft…</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/8f/7ecd4eed.jpg" width="30px"><span>FF</span> 👍（2） 💬（1）<div>haproxy 那个代理协议那一行要客户端自己加上去的 ？如果客户端把这个加到 x-forward-for 里面，不用代理协议，那不是也可以解决代理去修改头部的问题 ？重点都是客户端先加上去这些信息 。这样看代理协议没啥优势啊，或者不是为了解决减少中间代理再去修改头的问题 ？盼复，感谢。</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f7/0a/8534d0fa.jpg" width="30px"><span>星星之火</span> 👍（2） 💬（2）<div>老师您好，请问综合考虑代理的各种情况（比如匿名代理，篡改请求头字段）之后，怎么才能保证在服务端获取客户端的真实ip呢？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>所谓的“代理服务”就是指服务本身不生产内容，而是处于中间位置转发上下游的请求和响应。--记下来</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ff/60/df2033b8.jpg" width="30px"><span>红宝书第四版88-931</span> 👍（1） 💬（1）<div>1.正向代理隐藏了客户端，源服务器不知道发请求的是谁，代表是某科学上午工具
2.反向代码隐藏了源服务端，客户端不知道请求最终会由谁来处理，代表nginx</div>2022-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（1） 💬（1）<div>对于 transfer-encoding chunked 这种请求，如果中间有代理，是代理收到所有chunk后再转发给目标服务器吗？</div>2020-10-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/QOiaNght8yAR376VdV9L6k47ugAyEk5qJAwJrsqf4rzTDoRZoLYGL0MBTvG0TngKkE8V9CibyDP8O3DQt951Hc2w/132" width="30px"><span>xuan</span> 👍（1） 💬（1）<div>问题：
1.&quot;X-Forwarded-For”头的信息刚开始是客户端给的吗？
2.X-Forwarded-For在http头里，要修改就等于变动了原始的http报文，这个时候的修改动作发生在客户端还是代理服务器？
个人认为是客户端，两个动作应该都是在客户端</div>2020-07-20</li><br/><li><img src="" width="30px"><span>Geek_f8a084</span> 👍（1） 💬（1）<div>转发是指的代理服务吗？</div>2020-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/53/05aa9573.jpg" width="30px"><span>keep it simple</span> 👍（1） 💬（1）<div>学完了这一课，收获很大！给老师点赞~
第一个问题是：数据过滤——拦截上下行的数据，任意指定策略修改请求或者响应。这个不太理解。
第二个问题：X-Real-IP的例子，如果链路中有多个代理服务器，那只有第一个代理会加上X-Real-IP，后面的代理都不会再动这个字段了吧？</div>2020-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（1） 💬（1）<div>落下了不少课，今天补上</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（1） 💬（2）<div>前面的课程都好轻松，到这里突然感觉有点小压力了，代理proxy的课程陶辉老师的课nginx有讲过，说了缓解上游和下游的网速差异等等优化，当时一脸懵逼，不知道这玩意干啥的，学到这里才真正理解到，开源的方案都是为了解决实际应用场景的问题的，结合nginx的解决方案，应该都能解答代理的缺陷问题</div>2019-07-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLw9fVyja3eQLGQenLf5EqVaxGQoibo7rq8A7IRjlXED9FhicKukcn0ibCCtiaBqpEib4ZEIWfFOkiaGMSQ/132" width="30px"><span>Geek_d4dee7</span> 👍（1） 💬（1）<div>常听说的SLB是中间的这个代理么 老师</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>还出现了两个字段：“X-Forwarded-Host”和“X-Forwarded-Proto”，它们的作用与“X-Real-IP”类似，只记录客户端的信息，分别是客户端请求的原始域名和原始协议名。
——————————
老师，对于这句话，有点疑问，X-Forwarded-Host只是真实客户端的host吗？类比X-Real-IP，真实客户端的Host不应该是X-Real-Host吗？有关Forwarded的头不应该都是代理链路所有的以逗号分开的信息吗？</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/a7/674c1864.jpg" width="30px"><span>William</span> 👍（0） 💬（1）<div>例如下图中有两个代理：proxy1 和 proxy2，客户端发送请求会经过这两个代理，依次添加就是“Via:  proxy1, proxy2”，等到服务器返回响应报文的时候就要反过来走，头字段就是“Via:  proxy2,  proxy1”。

这段话中的Via： 我看图解HTTP 这本书上都是写着“Via:  proxy2,  proxy1” 从客户端到服务端口，和服务端到客户端都是 这个顺序.  跟老师讲的有一些差异，以哪个为准？</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7e/08/a50945c3.jpg" width="30px"><span>muzigef</span> 👍（0） 💬（1）<div>请问老师代理关系是如何建立的？比如反向代理，客户端如何知道要去哪个代理拿资源</div>2023-07-30</li><br/>
</ul>