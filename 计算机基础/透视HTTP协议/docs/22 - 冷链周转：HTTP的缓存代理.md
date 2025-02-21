在[第20讲](https://time.geekbang.org/column/article/106804)中，我介绍了HTTP的缓存控制，[第21讲](https://time.geekbang.org/column/article/107577)我介绍了HTTP的代理服务。那么，把这两者结合起来就是这节课所要说的“**缓存代理**”，也就是支持缓存控制的代理服务。

之前谈到缓存时，主要讲了客户端（浏览器）上的缓存控制，它能够减少响应时间、节约带宽，提升客户端的用户体验。

但HTTP传输链路上，不只是客户端有缓存，服务器上的缓存也是非常有价值的，可以让请求不必走完整个后续处理流程，“就近”获得响应结果。

特别是对于那些“读多写少”的数据，例如突发热点新闻、爆款商品的详情页，一秒钟内可能有成千上万次的请求。即使仅仅缓存数秒钟，也能够把巨大的访问流量挡在外面，让RPS（request per second）降低好几个数量级，减轻应用服务器的并发压力，对性能的改善是非常显著的。

HTTP的服务器缓存功能主要由代理服务器来实现（即缓存代理），而源服务器系统内部虽然也经常有各种缓存（如Memcache、Redis、Varnish等），但与HTTP没有太多关系，所以这里暂且不说。

## 缓存代理服务

我还是沿用“生鲜速递+便利店”的比喻，看看缓存代理是怎么回事。

便利店作为超市的代理，生意非常红火，顾客和超市双方都对现状非常满意。但时间一长，超市发现还有进一步提升的空间，因为每次便利店接到顾客的请求后都要专车跑一趟超市，还是挺麻烦的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKkDB6420zwODZTJL6icKKTpyFKuVF9GRjj1V5ziaibADbrpDMmicF8Ad5fmBjycibEg3yhpwlVOLzzxRQ/132" width="30px"><span>Teresa</span> 👍（164） 💬（3）<div>针对作业一的回答：
浏览器拿到一个网址的时候，先判断是否允许缓存，允许会先查看本地缓存:1.有缓存并在缓存可用期那直接拿来用。2.缓存不存在或者不可用 那需要请求。
浏览器拿到host，判断：1.ip+port 那直接请求对应的服务器 2.域名 那开展一系列的dns递归查询：先拿dns缓存，没有缓存-&gt;本地dns服务器-&gt;根dns服务器-&gt;顶级dns服务器-&gt;权威dns服务器-&gt;GSLB，查到ip返回最优ip组实现负载均衡，浏览器随机或者轮询取一个ip开始它的http请求之旅。
浏览器判断该网页是否允许缓存，然后添加Cache-Control的各种字段no-store是否允许缓存&#47;no-cache缓存必须进行验证&#47;noly-if-cached只接受代理的缓存等,max-age最大生存时间 max-stale 短时间过期可用 min-fresh 最短有效时间等。If-Modified-Since&#47;if-None-Match&#47;Last-modified&#47;ETag等字段用于判断服务端是否有更新。然后将请求发给代理服务器。请求代理服务器，如果是第一次，要经历浏览器和代理服务器的3次tcp握手进行连接，连接成功，发送http请求。
代理服务器拿到请求，首先查看是否允许缓存，允许那就查看自己本地缓存有没有，通过查看max-age&#47;max-stale&#47;min-fresh等信息判断是否过期，没有过期直接拿来用，将数据返回给客户端。如果过期了，代理服务器将用客户端的请求，再次像真实服务器进行请求。如果也是第一次连接，需要经历代理服务器和真实服务器的3次tcp握手，连接成功，发送请求。
真实服务器收到请求之后，通过if-Modified-Since&#47;Last-Modified&#47;if-None-Match&#47;ETag等字段判断是否有更新，没有更新，直接返回304。如果有更新，则将数据打包http response 返回。返回头字段会添加Cache-Control字段，用来判断缓存的控制策略以及生存周期，no-store不允许缓存&#47;no-cache使用缓存必须先验证&#47;must-revalidate缓存不过期可用过期必须重新请求验证&#47;proxy-revalidate缓存过期只要求代理进行请求验证  private不能在代理层保存只能在客户端保存&#47;public缓存完全开放  s-maxage缓存在代理上可以缓存的时间 no-transform不允许代理对缓存做任何的改动。然后根据业务需求判断该地址是不是需要重定向，如果需要是短期的重定向还是永久的重定向，按需将状态码修改为301或者302。最后真实服务器将数据打包成http相应 回给代理服务器。
代理服务器收到真实服务器的回应数据，首先会查看Cache-Control里的字段，是否允许它进行缓存，如果是private，代理服务器不进行缓存，直接返回给客户端。public则根据s-maxage&#47;no-transform进行缓存，如果可以优化并且代理服务器需要优化，那可能会先优化数据，否则同时将数据回发给客户端。
客户端收到数据，如果是304，则直接拿缓存数据进行渲染，并修改相关缓存变量，比如时间，以及缓存使用策略。如果收到了301或者302，那么客户端会再次发起新的url请求，进行跳转到最终的页面。
最后，底层tcp 经过4次挥手，完成关闭连接。</div>2020-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（34） 💬（3）<div>首先，老师的敬业精神令人钦佩，几乎每问必答，再者，没有给人一种你怎么这么笨这么简单的问题你还问的感受，而且看到有些地方不严谨也会干净利索的说自己可能弄错了。是个经验丰富技术精干为人真诚的大哥形象，工作或生活中有这样的朋友或大哥是一件很幸运的事情。

缓存的时间策略很重要，太大太小都不好，你觉得应该如何设置呢？
我觉得需要根据具体情况来定：
如果缓存的内容不变，那可以把缓存时间设置为永久。
如果缓存的内容会变化，但周期较长，可以根据她的变化周期来设置，比如：一天或一周
如果缓存的内容变化频繁，那缓存的过期时间就需要更短了，比如：一分钟
如果缓存的内容随时变化，且没啥规律，那还是不用用了
总之是根据场景来的核心是在提速的愿望能实现的前提下，数据也是最新的，否则不如不用缓存，从另一个角度来讲不用缓存几乎是不可能的，缓存在处处使用着，因为计算机本身就在各种各样的使用着缓存。如果完全不用直接从磁盘获取数据，也可以认为是使用缓存的一种特殊情况，缓存的过期时间为零即使即过期。</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/11/f6/36bd007d.jpg" width="30px"><span>龙宝宝</span> 👍（33） 💬（3）<div>max-stale相当于延长了过期时间，min-fresh相当于缩短了过期时间，可以这样理解吗</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/0a/da55228e.jpg" width="30px"><span>院长。</span> 👍（16） 💬（2）<div>老师您好，我想请问一下，为什么有的地方说cache-control默认是private（比如cache-control的百度百科），有的地方说默认是public（比如您这篇文章），是百度百科的是错误的吗？还是根据场景不同所以默认不同吗？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（14） 💬（1）<div>老师您好，

我想问一下，现在大多数网站都开启了 HTTPS，缓存代理还有用武之地吗？我对 HTTPS 的理解是它是端到端加密。介于客户端与服务器中间的缓存服务器是没法解密，缓存数据的。</div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/9d/2bc85843.jpg" width="30px"><span>　　　　　　　鸟人</span> 👍（8） 💬（1）<div>请问时间换空间是什么呢？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/b0/83054a91.jpg" width="30px"><span>ttsunami</span> 👍（7） 💬（1）<div>代理服务器真的那么听话吗？ 源给个private，结果自己却偷偷做一些操作也可以吧？如何验证代理服务器的处理是否夹带私心呢？ 纯靠自觉吗？ 哈哈  颇有 将在外军令有所不受的味道</div>2020-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（6） 💬（1）<div>min-fresh的含义是距离过期时间必须不短于约定的时间，保证取到的是短期内不会过时的内容。

但是这里有个风险是，万一服务器端因为某些原因重新刷新了资源(服务迁移等)，那么怎么反向通知缓存服务器去清理资源呢？尤其是已经返回给客户端的之前标记为fresh的资源?</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/71/0b949a4c.jpg" width="30px"><span>何用</span> 👍（5） 💬（1）<div>老师，CDN 服务是不是就是缓存代理的一种应用？还有文中图片的 X-Accel 是什么意思呢？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（4） 💬（1）<div>“must-revalidate”是只要过期就必须回源服务器验证，而新的“proxy-revalidate”只要求代理的缓存过期后必须验证，客户端不必回源，只验证到代理这个环节就行了。

看了一下MDN关于这两个头字段的解释

must-revalidate
Indicates that once a resource becomes stale, caches must not use their stale copy without successful validation on the origin server.
proxy-revalidate
Like must-revalidate, but only for shared caches (e.g., proxies). Ignored by private caches.

感觉MDN说的proxy-revalidate的意思似乎是对于存储在代理服务器上的共享缓存的验证策略，如果过期，必须回源验真，而不是说客户端的缓存【私有缓存】失效后回源到代理服务器验证。
而这也反过来推论，must-revalidate是向上游服务器验证cache，验证不一定回源到源服务器。

---请大师指正。。</div>2021-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（4） 💬（1）<div>我还要提醒你一点，源服务器在设置完“Cache-Control”后必须要为报文加上“Last-modified”或“ETag”字段。否则，客户端和代理后面就无法使用条件请求来验证缓存是否有效，也就不会有 304 缓存重定向

老师 这句话 没理解 能再说下吗</div>2020-08-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8mFt5wSkia31qc8paRg2uPSB6AuEBDricrSxvFBuTpP3NnnflekpJ7wqvN0nRrJyu7zVbzd7Lwjxw/132" width="30px"><span>Geek_steven_wang</span> 👍（4） 💬（1）<div>如果cache-control中没有 no-store no-cache must-revalidate这时浏览器会怎么处理？

Max-stale min-fresh 那个优先级高，如果两个都有，那个生效？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（4） 💬（2）<div>我们的做法是源服务器跟代理服务器联动，源服务器有文件变化(版本发布)，触发更新代理服务器缓存。如果没有联动的机制，简单粗暴根据应用升级周期设置过期时间也可以，但这样会多做无用功。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/d4/204d0c6d.jpg" width="30px"><span>居培波</span> 👍（4） 💬（1）<div>老师能结合nginx讲下缓存及代理吗？还是后面探索篇有讲。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>HTTP 的服务器缓存功能主要由代理服务器来实现（即缓存代理），而源服务器系统内部虽然也经常有各种缓存（如 Memcache、Redis、Varnish 等），但与 HTTP 没有太多关系。--记下来</div>2023-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>1. 老师，我看那个完整的服务器端缓存控制策略图，在图上no-cache和must-revalidate两个一般只能存在一个吧？不能同时传递。
2. 还有：“比较常用的一种做法是使用自定义请求方法“PURGE””，意思是自己在代码里面写个方法处理缓存的数据，对吧？</div>2019-12-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8mFt5wSkia31qc8paRg2uPSB6AuEBDricrSxvFBuTpP3NnnflekpJ7wqvN0nRrJyu7zVbzd7Lwjxw/132" width="30px"><span>Geek_steven_wang</span> 👍（1） 💬（2）<div>1. 文中第一张图服务器缓存控制，其实是服务器根据缓存策略向response中插入各header的过程，缓存服务器，浏览器根据header处理缓存。

2. 文中客户端缓存过程中，是浏览器根据自己的缓存策略，向服务器发请求时，设置各header。但这些策略浏览器怎么知道呢？是用户通过浏览器设置界面设置吗？还是ajax请求时设置？如果不是前后端分类的应用，怎么设置这些header?

3. 既然服务器端有自己的缓存策略，那客户端请求上来时，服务器会根据客户端请求header调整策略吗？如果会，是应用服务器自己处理，还是程序员代码预先写好处理逻辑？

4. 什么情况下客户端会有only-if-cached</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>老师请教一个有关302的问题，就是再前端代码中有个post请求，去请求后端服务器，当后端服务器处理完业务逻辑后，需要重定向到另一个网站，返回的是一个302的状态码和响应头Location是另一个网站地址。这时候问题出现了，当返回到前端的时候，浏览器没有自动跳转重定向后的地址，而是当作接口去请求了需要跳转后的地址，然后就出现了跨域的问题
这个是什么原因呢？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（1） 💬（1）<div>max-stale和min-fresh还是不太明白~~</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>没懂，好像有有点懂，大概是没懂</div>2024-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/1c/d7a1439e.jpg" width="30px"><span>KaKaKa</span> 👍（0） 💬（1）<div>老师，看到评论有这样一个问题，我也好奇
【作者回复:
1.max-age不能用在请求头里，只能在响应头里指定资源的有效期。】这句我有点疑问，在第20讲里，在客户端的缓存控制里，您说了，【当你点“刷新”按钮的时候，浏览器会在请求头里加一个“Cache-Control: max-age=0”。】</div>2022-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/53/d0/cf58d13c.jpg" width="30px"><span>玉米派🌽</span> 👍（0） 💬（1）<div>老师跨域的问题有讲解吗 </div>2022-07-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eHNmzejyQW9Ag5g3EELS1d9pTgJsvxC7CxSCxIFQqeFLXUDT52HWianQWzw14kaAT4P9UhTUSNficc9W5DlWZWJQ/132" width="30px"><span>silence</span> 👍（0） 💬（1）<div>老师请问图中的小黑圆点是指的数据包吗🕴</div>2021-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（0） 💬（1）<div>当再收到相同的请求时，代理就读取缓存里的“Vary”，对比请求头里相应的“ Accept-Encoding”“User-Agent”等字段，如果和上一个请求的完全匹配，比如都是“gzip”“Chrome”，就表示版本一致，可以返回缓存的数据。

老师问下在第15讲里说vary是响应头的字段，表示服务器根据哪些字段生成的响应报文，这里为什么成了请求头的字段？</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/22/4e/2e081d9c.jpg" width="30px"><span>hao</span> 👍（0） 💬（2）<div>想问以下老师，缓存代理收到带Vary头字段的响应报文后，是根据Vary里的内容，去上一个请求报文的中提取请求头还是说在该响应报文中提取请求头，计算hash值 ？
类似这张图的Client2和Client3，不是很清楚这个流程，希望老师可以指点下。
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;HTTP&#47;Caching&#47;http_vary.png</div>2021-05-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIpF5euTNx3GOkmf515HFh1ahAzogerLfIyLia2AspTIR9fkU6icGbo2ungo23cdM5s9dUjZGMno7ZA/132" width="30px"><span>dawn</span> 👍（0） 💬（1）<div>老师，Cache-Control: public, max-age=10, s-maxage=30，10s内直接使用浏览器缓存，10到30之间使用缓存服务器，我在实验环境20s左右抓包，缓存服务器不是以条件请求的方式请求的源服务器，这样的话那缓存服务器的30s的设置感觉没用到，感觉我是哪里没理解到位，希望老师指点一下</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（0） 💬（1）<div>关于proxy-revalidate的还以，查了一下，感觉和大师说的不一样
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;HTTP&#47;Headers&#47;Cache-Control

must-revalidate
Indicates that once a resource becomes stale, caches must not use their stale copy without successful validation on the origin server.

proxy-revalidate
Like must-revalidate, but only for shared caches (e.g., proxies). Ignored by private caches.
---感觉它说的意思是proxy-revalidate 针对共享缓存回源
基本逻辑是如果资源stale了，并且是shared的，那么回源到缓存代理验证。
文章少了约束条件，共享缓存，
也符合逻辑，private的，就没在缓存代理上存，回源只能找源服务器。
我悟了。。。</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（0） 💬（1）<div>排骨上贴着标签“max-age=30, proxy-revalidate, no-transform”。因为缓存默认是 public 的，那么它在便利店和顾客的冰箱里就都可以存 30 天，过期后便利店必须去超市进新货，而且不能擅自把“大排”改成“小排”。
老师，这里的proxy-revalidate是不是没起到作用？</div>2020-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（0） 💬（1）<div>老师，请问下缓存代理中的缓存清理，是服务端还是客户端去发起请求处理？</div>2020-05-12</li><br/><li><img src="" width="30px"><span>candy</span> 👍（0） 💬（1）<div>为啥我测试不出老师&#47;22-1的那个response返回呢，我把www.chrono.com 换为我自己的域名 在&#47;etc&#47;host配置了，nginx也换了，没有返回X-Access等</div>2019-08-30</li><br/>
</ul>