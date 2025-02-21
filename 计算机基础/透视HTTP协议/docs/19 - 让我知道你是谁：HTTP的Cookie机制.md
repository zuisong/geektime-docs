在之前的[第13讲](https://time.geekbang.org/column/article/103270)、[第14讲](https://time.geekbang.org/column/article/103746)中，我曾经说过，HTTP是“无状态”的，这既是优点也是缺点。优点是服务器没有状态差异，可以很容易地组成集群，而缺点就是无法支持需要记录状态的事务操作。

好在HTTP协议是可扩展的，后来发明的Cookie技术，给HTTP增加了“记忆能力”。

## 什么是Cookie？

不知道你有没有看过克里斯托弗·诺兰导演的一部经典电影《记忆碎片》（Memento），里面的主角患有短期失忆症，记不住最近发生的事情。

比如，电影里有个场景，某人刚跟主角说完话，大闹了一通，过了几分钟再回来，主角却是一脸茫然，完全不记得这个人是谁，刚才又做了什么，只能任人摆布。

这种情况就很像HTTP里“无状态”的Web服务器，只不过服务器的“失忆症”比他还要严重，连一分钟的记忆也保存不了，请求处理完立刻就忘得一干二净。即使这个请求会让服务器发生500的严重错误，下次来也会依旧“热情招待”。

如果Web服务器只是用来管理静态文件还好说，对方是谁并不重要，把文件从磁盘读出来发走就可以了。但随着HTTP应用领域的不断扩大，对“记忆能力”的需求也越来越强烈。比如网上论坛、电商购物，都需要“看客下菜”，只有记住用户的身份才能执行发帖子、下订单等一系列会话事务。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（48） 💬（4）<div>1. 如果 Cookie 的 Max-Age 属性设置为 0，会有什么效果呢？
设置为0，服务器0秒就让Cookie失效，即立即失效，服务器不存Cookie。
2. Cookie 的好处已经很清楚了，你觉得它有什么缺点呢？
好处：方便了市民
缺点：方便了黑客:)</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/2a/f7e19dcc.jpg" width="30px"><span>放开那个猴子</span> 👍（37） 💬（15）<div>广告追踪没看明白呀，能否详细讲讲</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b6/17/76f29bfb.jpg" width="30px"><span>Geek_66666</span> 👍（28） 💬（2）<div>既然max-age=0会立即失效，那不就等于无记忆了？那干嘛还用cookie？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（25） 💬（1）<div>1. （我修改 Lua 文件测试了一下）如果 Max-Age 设置为0，浏览器中该 Cookie 失效，即便这个 Cookie 已存在于浏览器中，且尚未过期。另外 Web 应用开发中，可以通过这种方式消除掉用户的登陆状态，此外记得在服务器的 session 中移除该 cookie 和其对应的用户信息。
2. Cookie 的缺点：
（1） 不安全。如果被中间人获取到 Cookie，完全将它作为用户凭证冒充用户。解决方案是使用 https 进行加密。
（2）有数量和大小限制。另外 Cookie 太大也不好，传输的数据会变大。
（3）客户端可能不会保存 Cookie。比如用 telnet 收发数据，用户禁用浏览器 Cookie 保存功能的情况。</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/ee/257a22fb.jpg" width="30px"><span>饭饭</span> 👍（18） 💬（1）<div>Max-age：-1 的时候会永久有效吧 ？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（16） 💬（3）<div>对于XSS和XSRF一直不是很理解希望老师帮忙解答一下：
1. XSS攻击是指第三方的JS代码读取到浏览器A网站的Cookie然后冒充我去访问A网站吗？
2.XSRF是指浏览器从A网站跳转到B网站是会带上A网站的Cookie吗？这个不是由Domain和Path已经限定了吗？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/e6/3a/382cf024.jpg" width="30px"><span>rongyefeng</span> 👍（13） 💬（1）<div>还有一个属性叫“Secure”，表示这个 Cookie 仅能用 HTTPS 协议加密传输，明文的 HTTP 协议会禁止发送。
但 Cookie 本身不是加密的，浏览器里还是以明文的形式存在。
这里的“ Cookie 本身”怎么理解？</div>2020-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（11） 💬（2）<div>属性“HttpOnly”、“Secure”、“SameSite”很少见，老师可以给几个配套例子，后面答疑篇，可以来个攻防实战！</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/3f/830d74f4.jpg" width="30px"><span>cp3yqng</span> 👍（6） 💬（1）<div>域名+路径的方式存储cookie，感觉像只有一台业务服务器，那后台如何过分布式系统呢，用户中心是一个系统，核心业务是其他的系统，这里cookie肯定要共享，应该有一级域名和二级域名等等的概念吧，麻烦老师在解释解释。我本人是做移动端开发的，都是自己把token写在网络底层的请求头中，其实核心思想是一样的，但是缺点就是所有的域名里面都带token，这样也不好，好像还有优化的空间。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/76/1d/b4262bdc.jpg" width="30px"><span>大小兵</span> 👍（6） 💬（2）<div>要是能把session和token也说一下就好了</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（5） 💬（1）<div>1.Max-Age: 是永久有效的意思。 
2.cookie在浏览器端禁用，还有就是安全性，因为在本地是明文存储的</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/e4/4f/df6d810d.jpg" width="30px"><span>Maske</span> 👍（4） 💬（1）<div>samesite的加入是为了在一定程度上防范CSRF，比如a.com页面中有个恶意表单，提交url为b.com的域名为开头且为银行转账接口地址，且为post请求，用户误操作后会将本地cookie（domain为b.com）发送，导致账户损失，设置samesite为Lax后可避免该cookie的发送，防止该情况出现。</div>2020-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b3/c7/57e789fe.jpg" width="30px"><span>quaeast</span> 👍（4） 💬（2）<div>老师您好，我一只搞不懂cookie和session的区别</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/99/8e760987.jpg" width="30px"><span>許敲敲</span> 👍（4） 💬（1）<div>还有个名词，session 这个适合cookie放在一起的，这个老师能简单解释下嘛？</div>2019-12-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（4） 💬（1）<div>哈哈，就是九品芝麻官里的半个烧饼：你后人凭这个来找我</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/11/26838646.jpg" width="30px"><span>彧豪</span> 👍（4） 💬（6）<div>话说现在还有用cookie的吗？感觉似乎不是太安全吧，毕竟各种明文传输，我司是这么做的：浏览器登录成功, 服务端会设置一个密文的cookie, 然后浏览器再用带着这个cookie值的请求头字段去请求用户信息的接口来获取用户信息, 当然了还有其他的头字段，然后登陆之类的接口中的相应头也看不到set-cookie字段，但是浏览器的cookie中却能被设置上一个cookie键值对，以及是密文的</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/f6/ed66d1c1.jpg" width="30px"><span>chengzise</span> 👍（4） 💬（1）<div>老师好，我理解的广告跟踪那个原理是：用户访问A网站，A会给用户设置cookies（T），用户再次访问网站B时，浏览器会带上cookies（T），B网站就能够识别到被A标记的用户。这里A给用户设置的cookies里面是不是把domain设置为B网站？不然凭什么访问B网站的时候，浏览器会带上A设置的cookies。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8a/e7/a6c603cf.jpg" width="30px"><span>GitHubGanKai</span> 👍（3） 💬（2）<div>老师，有几个问题我不是很明白1⃣️：如果用户没有登录，浏览器向服务器发送请求的时候，是否还会产生cookie呢？如果会产生，那么用来干嘛呢？2⃣️：有关session，他是保存在服务器上的，如果用户没有登录，服务器是否还会产生session吗？我的理解是：应该不会产生吧！毕竟服务器保存session需要额外的空间！而且用户又没有登录，保存它做什么呢🤔？3⃣️：假设现在有三个浏览器，一个在深圳，一个在北京，一个在上海，它们都是没有登录的，同时访问同一台服务器，假设没有session的存在，会出现服务器返回数据的时候，出现无法一一对应的情况吗？就是，本来这个响应是返回给深圳那个浏览器的，结果错乱的发送给北京的那台浏览器去了！</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/0a/da55228e.jpg" width="30px"><span>院长。</span> 👍（3） 💬（1）<div>老师我是那个回复URI会跳转的那个，其他的测试案例也都会跳转。
您说的实验环境openresty需要我配置什么嘛？我应该是顺着看您的文章的，您专栏里哪一章有介绍我漏看的吗？
如果是我漏看的麻烦老师说下在哪一节，谢谢老师啦。</div>2019-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ee/d4/204d0c6d.jpg" width="30px"><span>居培波</span> 👍（3） 💬（1）<div>正常需要服务器输出cookie值value时会加密，这样稍安全点。</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f2/30/76cbc52f.jpg" width="30px"><span>威~~微冷。。。</span> 👍（3） 💬（2）<div>收获不少。老师说的这些多是建立在浏览器也就是B&#47;S模式下，浏览器帮忙解析并本地存储，在发起请求的时候请求头还自动加上cookie。那要是C&#47;S模式下，脱离了浏览器，比如说安卓客户端，这时候要达到类似cookie这样的效果，是不是需要安卓开发人员自己解析响应，然后再存储，最后再组装请求体像后台服务器发请求吗？？？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f2/f5/b82f410d.jpg" width="30px"><span>Unknown element</span> 👍（2） 💬（2）<div>老师cookie应该不止浏览器需要存储吧 服务器是不是也得存储 否则它怎么知道这个cookie是它生成的呢</div>2021-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>1：如果 Cookie 的 Max-Age 属性设置为 0，会有什么效果呢？
有效期为0秒，那就是服务器委托给浏览器暂存的信息，在浏览器一关闭时就失效。
如果想设置Cookie永不过期，怎么搞设置一个超大过期时间嘛？特殊值-1行不行？

2：Cookie 的好处已经很清楚了，你觉得它有什么缺点呢？
Cookie好处是能够保持状态信息，同样这个特点也是坏处尤其是被不怀好意的人获取之后。除此之外多传信息总会占用更多的带宽，降低传输效率，不过想传多一点也不行她的大小也是有限制的。所以，出现了别的存储技术来解决这个问题。
</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ff/a4/55520286.jpg" width="30px"><span>answer宫</span> 👍（2） 💬（2）<div>老师,有个疑问,应该是单个cookie大小不能超过4k吧,而不是总共大小不超过4k吧,我看了很多资料,怎么说的都有</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（2）<div>1.0应该是表示永久有效，不过期
2.缺点是明文，可以直接在浏览器里编辑和拷贝，容易造成泄露和伪造</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/91/09/6f0b987a.jpg" width="30px"><span>陈坚泓</span> 👍（1） 💬（1）<div>罗老师好 
看到您回答广告追踪的问题说
网站的页面里会嵌入很多广告代码

这个嵌入广告代码是指网站引入广告方的js代码嘛</div>2021-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/a4/ca/be57f01d.jpg" width="30px"><span>齐齐</span> 👍（1） 💬（1）<div>httponly感觉只是个君子协议？我理解的是，如果我自己写个浏览器，或者简单的破解了其他浏览器（Firefox之类都开源吧，把实现的关于httponly安全方面的取消掉），这样也就能js读取了吧。包括跨域名什么的</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/fc/5627215c.jpg" width="30px"><span>小何</span> 👍（1） 💬（3）<div>老师好，我想问一下细节问题，Cookie中Domain可以设置为另外一个一级域名吗，比如当前请求是A.com，Domain可以设置为B.com，这样发送请求给B.com，也会带上这个cookie？</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（1） 💬（1）<div>1. 那这个cookie就是无效的吧（如果同时存在Expires和Max-Age，Max-Age为0，也是优先Max-Age吗？）
2. cookie优化了客户端与服务器的连接过程，如果cookie泄露，这个过程不仅仅是面对用户，也是面对黑客的</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7b/f0/ccc11dec.jpg" width="30px"><span>Cris</span> 👍（1） 💬（1）<div>老师我可不可以这样理解：
1、cookie是存储在浏览器里的，不安全，为了解决安全性问题就出现了session(存储在服务器上)；
2、cookie有数量和大小的限制，于是就有了localstorage 和sessionstorage;</div>2019-08-20</li><br/>
</ul>