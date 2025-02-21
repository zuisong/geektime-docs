缓存（Cache）是计算机领域里的一个重要概念，是优化系统性能的利器。

由于链路漫长，网络时延不可控，浏览器使用HTTP获取资源的成本较高。所以，非常有必要把“来之不易”的数据缓存起来，下次再请求的时候尽可能地复用。这样，就可以避免多次请求-应答的通信成本，节约网络带宽，也可以加快响应速度。

试想一下，如果有几十K甚至几十M的数据，不是从网络而是从本地磁盘获取，那将是多么大的一笔节省，免去多少等待的时间。

实际上，HTTP传输的每一个环节基本上都会有缓存，非常复杂。

基于“请求-应答”模式的特点，可以大致分为客户端缓存和服务器端缓存，因为服务器端缓存经常与代理服务“混搭”在一起，所以今天我先讲客户端——也就是浏览器的缓存。

## 服务器的缓存控制

为了更好地说明缓存的运行机制，下面我用“生鲜速递”作为比喻，看看缓存是如何工作的。

夏天到了，天气很热。你想吃西瓜消暑，于是打开冰箱，但很不巧，冰箱是空的。不过没事，现在物流很发达，给生鲜超市打个电话，不一会儿，就给你送来一个8斤的沙瓤大西瓜，上面还贴着标签：“保鲜期5天”。好了，你把它放进冰箱，想吃的时候随时拿出来。

在这个场景里，“生鲜超市”就是Web服务器，“你”就是浏览器，“冰箱”就是浏览器内部的缓存。整个流程翻译成HTTP就是：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（90） 💬（4）<div>Cache 和 Cookie 的相同点是：都会保存到浏览器中，并可以设置过期时间。
不同点：
1. Cookie 会随请求报文发送到服务器，而 Cache 不会，但可能会携带 if-Modified-Since（保存资源的最后修改时间）和 If-None-Match（保存资源唯一标识） 字段来验证资源是否过期。
2. Cookie 在浏览器可以通过脚本获取（如果 cookie 没有设置 HttpOnly），Cache 则无法在浏览器中获取（出于安全原因）。
3. Cookie 通过响应报文的 Set-Cookie 字段获得，Cache 则是位于 body 中。
4. 用途不同。Cookie 常用于身份识别，Cache 则是由浏览器管理，用于节省带宽和加快响应速度。
5. Cookie 的 max-age 是从浏览器拿到响应报文时开始计算的，而 Cache 的 max-age 是从响应报文的生成时间（Date 头字段）开始计算。</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/d2/d7a200d5.jpg" width="30px"><span>小鸟淫太</span> 👍（35） 💬（3）<div>1. cookie是方便进行身份识，cache是为了减少网络请求。
2. 强制刷新是因为请求头里的 If-Modified-Since 和 If-None-Match 会被清空所以会返回最新数据</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（25） 💬（3）<div>对于第二个问题：发现强制刷新后请求头中 没有了 If-None-Match ，而且 Cache-Control: no-cache

是这个原因吗？</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/04/0e/87adea1d.jpg" width="30px"><span>DENG永青</span> 👍（23） 💬（2）<div>Etag的工作原理
Etag在服务器上生成后,客户端通过If-Match或者说If-None-Match这个条件判断请求来验证资源是否修改.我们常见的是使用If-None-Match.请求一个文件的流程可能如下：
新的请求
客户端发起HTTP GET请求一个文件(css ,image,js)；服务器处理请求,返回文件内容和一堆Header(包括Etag,例如&quot;2e681a-6-5d044840&quot;),http头状态码为为200.

同一个用户第二次这个文件的请求
客户端在一次发起HTTP GET请求一个文件,注意这个时候客户端同时发送一个If-None-Match头,这个头中会包括上次这个文件的Etag(例如&quot;2e681a- 6-5d044840&quot;),这时服务器判断发送过来的Etag和自己计算出来的Etag,因此If-None-Match为False,不返回200,返 回304,客户端继续使用本地缓存；

注意.服务器又设置了Cache-Control:max-age和Expires时,会同时使用,也就是说在完全匹配If-Modified-Since和If-None-Match即检查完修改时间和Etag之后,服务器才能返回304.</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/0a/da55228e.jpg" width="30px"><span>院长。</span> 👍（20） 💬（4）<div>老师我有几个问题想问一下： 
1. F5刷新的时候，请求头加上&quot;Cache-Control: max-age=0&quot;，您文章里说，服务器用一个最新生成的报文回应浏览器，那这时候响应返回的应该是&quot;200 OK&quot;吗？为什么我在极客网页版的这个页面刷新后，有个叫&quot;106804&quot;的资源返回的是&quot;304&quot;，但是强制刷新是&quot;200 ok&quot;，产生的效果好像不同呀。这里是不是应该换一种方式说？感觉强制刷新说的有些简单了。
2. F5刷新发送的请求头是固定的吗？还是会根据浏览器不同而产生变化？
3. 200（from memory cache）和200(from disk cache)是针对内存和硬盘的，他们出现的场景分别是什么呢？
4. HTTP缓存有标准性的流程吗？比如说从我输入URL开始，到后续刷新或者强制刷新等？
5.对于&quot;must-revalidate&quot;我有疑问，本身存储机制不就是如果不过期的话可以继续使用，过期的话去请求服务器吗？那这个属性还有什么意义呢？
6. no-cache,no-store,max-age等属性可以共存吗？
问题有点多，因为网上资料质量参差不齐，解释有些也不全相同，所以在这里咨询下老师，希望老师可以解答一下，或者有推荐的讲述HTTP缓存的文章也可以，谢谢老师</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（15） 💬（1）<div>老师，nocache，每次使用前都需要去浏览器问一下有没有过期，这不也是一次请求吗？那不和没有缓存一个意思吗</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（12） 💬（2）<div>我有一个问题，就拿咱们极客时间的网页来说，会请求一个Id-00001.ts的文件，响应头中指示了cache-control: max-age= 7200， 要一个小时才过期，那么为什么每次刷新都是304, 像这种情况不应该直接200 cacahe from disk才对么？为什么明明没有过期还要去服务器协商呢？</div>2019-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/99/c4302030.jpg" width="30px"><span>Khirye</span> 👍（8） 💬（1）<div>Hi, 我对缓存控制策略这张流程图有一些疑惑，must-revalidate是指缓存过期之后，必须要向服务器验证缓存，这一步应该是在图中”缓存最多x秒“这个判断之前的吧？
因为只有缓存超过了max-age的期限，才会进入”must-revalidate的判断“这一步吧？
烦请解惑，谢谢！</div>2019-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/37/5ae95580.jpg" width="30px"><span>风宇殇</span> 👍（7） 💬（2）<div>这篇文章将缓存讲的比较容易理解。https:&#47;&#47;mp.weixin.qq.com&#47;s&#47;cUqkG3NETmJbglDXfSf0tg</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（6） 💬（1）<div>小贴士的nginx计算etag我贴下测试logngx_sprintf(etag-&gt;value.data, &quot;&quot;%xT-%xO&quot;&quot;, r-&gt;headers_out.last_modified_time,
r-&gt;headers_out.content_length_n)相信大家看到这里更清晰明了</div>2019-07-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ia4ZTN1ibN5ovBVIaRYBibvEJW4CxRQde4ribsRF83bGaLDy0tqenD1X4gEAocSiaeb6XA2dQR69Z9hAktHV0bgPOGQ/132" width="30px"><span>walle</span> 👍（4） 💬（1）<div>cache-control 中的 private 是如何识别的呢？是根据session吗还是什么方式开识别是私有缓存呢</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（4） 💬（1）<div>请问老师弱ETag是服务器更新时自己判断本次的更新有没有语义的变化，如果语义有变化就重新生成一个ETag，如果没有变化不重新生成直接使用原来的，请问是这样的流程吗？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（3） 💬（0）<div>老师，根据服务器的缓存控制那个图，如果cache-control 设置了 no-cache 或 must-revalidate 那就 必须设置 max-age喽？</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（3） 💬（1）<div>1.cache的作用为定义浏览器对静态文件如何进行缓存控制，目的是为了有效利用可复用的资源，尽可能减少客户端的请求，优化用户体验减轻服务器响应压力。常用字段值就那么一些，并有各自的含义。cookie的作用是增加了http请求的状态性，让服务器‘认识’当前访问的用户是谁，字段key,value值都可以自定义，比较灵活。
2.看了下天猫首页的css., js文件，普通的刷新（F5）操作中，不会在请求头中包含cache-control、if-none-match，if-Modified-Since,刷新会命中缓存文件，属于强缓存。强制刷新（ctrl + f5）在请求头中附加了cache-control: no-cache，为协商缓存，相当于设置max-age=0;所以此时不会使用本地缓存，当前页面所有的请求均是如此</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c5/2e/0326eefc.jpg" width="30px"><span>Larry</span> 👍（3） 💬（1）<div>如果响应报文什么字段都不设置，单纯的返回数据，是不是也不会缓存？</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/92/de629e17.jpg" width="30px"><span>游鱼</span> 👍（3） 💬（2）<div>老师，开发提测后，有时需要清缓存才是最新的，强刷都不管用，这个有解决办法吗</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/b0/c196c056.jpg" width="30px"><span>SeaYang</span> 👍（3） 💬（1）<div>观察了一些网站的资源加载情况，有一些总结，老师帮忙看看呢，辛苦了
一、打开一个网页，比如百度、慕课网之类的，并打开开发者工具，切换到network面板

1、勾选disable cache，刷新，页面及内嵌资源文件的请求头有Cache-Control: no-cache，并且不会发送If-Modified-Since、If-None-Match（响应头设置了Last-Modified、ETag等字段）等请求头，所以文档和内嵌资源文件都会返回完整最新的，这个相当于是强制刷新了吧

2、取消勾选disable cache，刷新，页面的请求头有Cache-Control: max-age=0，而内嵌资源文件的请求头不会有Cache-Control: max-age=0。至于文档和内嵌资源文件从哪里取分两种情况：

1）若第一次请求的响应头设置了Cache-Control: no-cache或must-revalidate，且设置了Last-Modified、ETag等字段，则走条件请求，可能返回200，也可能返回304，分别取最新的数据和取本地缓存；若没设置Last-Modified、ETag等字段，则取最新完整数据

2）若第一次请求的响应头没有设置Cache-Control: no-cache或must-revalidate，文档会获取最新的数据或者304走本地缓存（响应头设置了Last-Modified、ETag等字段）；而内嵌资源稍微有点奇怪，有的资源第一次刷新时返回304，后面刷新就返回200走本地缓存了，而有的资源是一直返回200走本地缓存，不知道为什么？
       举个例子，在一个新的标签页，打开开发者工具，勾选disable cache，地址栏输入：https:&#47;&#47;www.imooc.com&#47;course&#47;list，回车待页面完全load，找到图片：https:&#47;&#47;static.mukewang.com&#47;static&#47;img&#47;course&#47;course-recommend2.png，取消勾选disable cache，刷新，发现这张图片返回304，后面继续刷新就返回200取本地缓存了，而对于别的一些图片则一直返回200取的本地缓存

二、对于文档来说，响应头里面Cache-Control只设置max-age似乎没啥用，刷新的话还是取的最新数据，前进后退只走本地缓存，即使max-age过期了且指定了must-revalidate或no-cache，比如在&#47;20-1和&#47;20-2之间一直前进后退，过了30秒还是取的本地缓存。唯一不确定的是对于文档内嵌资源文件，Cache-Control只设置max-age有没有用，因为一些网站的内嵌资源文件响应头的max-age通常设置的比较大，刷新页面这些内嵌资源文件一般都走的本地缓存，就不知道max-age过期了之后再刷新页面，这些内嵌资源文件还会不会走本地缓存

三、请求头中同时有If-None-Match、If-Modified-Since、Cache-Control，对于服务器来说，If-None-Match、If-Modified-Since的优先级高，也就是即使请求头有Cache-Control: no-cache，走的也是条件请求，而不是直接返回最新完整数据</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/43/fa115929.jpg" width="30px"><span>来自地狱的勇士</span> 👍（3） 💬（1）<div>老师，既然Etag的算法比较复杂，需要占用服务器资源，那么，实际上服务器会使用Etag吗？看到有的资料说服务器很少会用到Etag，这个说法正确吗？</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2a/62/52231841.jpg" width="30px"><span>Joe</span> 👍（2） 💬（3）<div>老师你好，如果使用的是强缓存，比如Cache-Control: max-age=36000，那么在有效期内服务器上的文件发生了改变，客户端怎么才能及时获取最新的文件？更改文件指纹是可以获取最新的文件吗？如果可以这个请求流程是什么样的？</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/87/e7085d32.jpg" width="30px"><span>青莲居士</span> 👍（2） 💬（2）<div>请问下 cache-control 头字段 与 if 系列的请求头字段有依赖关系么 ？</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>不止服务器可以发“Cache-Control”头，浏览器也可以发“Cache-Control”，也就是说请求 - 应答的双方都可以用这个字段进行缓存控制，互相协商缓存的使用策略。--记下来</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/8c/80/7310baac.jpg" width="30px"><span>刘杰</span> 👍（1） 💬（1）<div>1、相同点是：Cache和Cookie都可以通过设置max-age设置过期时间，Cache的max-age代表的是从服务器创建报文开始计算的时间，而Cookie的max-age则代表客户端接收后开始计算。差异：Cache可以通过Cache-Control来设置是否需要缓存，no-store表示不缓存，no-cache表示可以缓存，但是需要验证缓存是否过期，must-revalidate，如果缓存不过期可以使用，过期了还想用就要去服务器验证。Cookie可以通过Expires和max-age来设置过期时间，max-age优先级高与Expires。Cache可以通过If-Modified-Since&#47;Last-Modified和If-None-Match&#47;ETag来判断缓存是否有变化，Etag更加精确
</div>2021-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（1） 💬（1）<div>老师，问一下 服务器返回304，这个服务器是怎么返回的呢？又没有走指定的查询数据是否改变的接口</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（1） 💬（1）<div>1、cookie主要用于保存会话状态，会作为字段发送给服务端，用于身份认证。而cache是整个资源，也就是整个报文，不作为字段，但是要使用缓存需要设置相应字段。
2、强制刷新后：Cache-Control：no-cache，且没有If-None-Match和If-Modified-Since字段，这样就不能命中缓存了，所以会返回200；而普通刷新有这些字段，Cache-Control为max-age=0，存在If-None-Match或If-Modified-Since字段，根据情况使用强缓存协商缓存。</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/b2/1f914527.jpg" width="30px"><span>海盗船长</span> 👍（1） 💬（1）<div>“所以今天我先讲客户端——也就是浏览器的缓存。服务器的缓存控制”  哈哈 </div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e7/5d/deeb2580.jpg" width="30px"><span>cc</span> 👍（1） 💬（1）<div>怎么设置强Etag呢？
在Nginx里面配置了Expires: -1为什么HTML还会有缓存</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（1）<div>老师，您这里这么说的：“no-cache：它的字面含义容易与 no-store 搞混，实际的意思并不是不允许缓存，而是可以缓存，但在使用之前必须要去服务器验证是否过期，是否有最新的版本”。
这个no-cache在这里浏览器请示服务器，如果服务器确定资源没有过期，没有新的版本，那么浏览器就是用缓存的数据了？感觉浏览器只要加上这个，就会获得最新的数据，没有走缓存吧？</div>2019-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ia4ZTN1ibN5ovBVIaRYBibvEJW4CxRQde4ribsRF83bGaLDy0tqenD1X4gEAocSiaeb6XA2dQR69Z9hAktHV0bgPOGQ/132" width="30px"><span>walle</span> 👍（1） 💬（1）<div>max-age是不是只对文件请求有效？为什么我看到的例子都是请求文件？</div>2019-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c5/5d/9e75eb36.jpg" width="30px"><span>Bean</span> 👍（1） 💬（1）<div>老师有文章说浏览器会在js和图片等文件解析执行后直接存入内存缓存中， 而css文件则会存入硬盘文件中。为什么？ 存入内存还是硬盘 是怎么触发 的</div>2019-09-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0c/f47fd608.jpg" width="30px"><span>blackjuly</span> 👍（1） 💬（1）<div>请问老师，有看到您说的一个ETag解决的问题： 一个文件在一秒内改变多次，可以用ETag来解决文件修改无法被感知到的情况；这个有场景可以举例吗？因为总感觉修改这么频繁的东西应该就不需要缓存了吧</div>2019-08-06</li><br/>
</ul>