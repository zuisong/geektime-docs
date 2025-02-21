从今天开始，我们开始进入全新的“安全篇”，聊聊与安全相关的HTTPS、SSL、TLS。

在[第14讲](https://time.geekbang.org/column/article/103746)中，我曾经谈到过HTTP的一些缺点，其中的“无状态”在加入Cookie后得到了解决，而另两个缺点——“明文”和“不安全”仅凭HTTP自身是无力解决的，需要引入新的HTTPS协议。

## 为什么要有HTTPS？

简单的回答是“**因为HTTP不安全**”。

由于HTTP天生“明文”的特点，整个传输过程完全透明，任何人都能够在链路中截获、修改或者伪造请求/响应报文，数据不具有可信性。

比如，前几讲中说过的“代理服务”。它作为HTTP通信的中间人，在数据上下行的时候可以添加或删除部分头字段，也可以使用黑白名单过滤body里的关键字，甚至直接发送虚假的请求、响应，而浏览器和源服务器都没有办法判断报文的真伪。

这对于网络购物、网上银行、证券交易等需要高度信任的应用场景来说是非常致命的。如果没有基本的安全保护，使用互联网进行各种电子商务、电子政务就根本无从谈起。

对于安全性要求不那么高的新闻、视频、搜索等网站来说，由于互联网上的恶意用户、恶意代理越来越多，也很容易遭到“流量劫持”的攻击，在页面里强行嵌入广告，或者分流用户，导致各种利益损失。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（124） 💬（4）<div>机密性由对称加密AES保证，完整性由SHA384摘要算法保证，身份认证和不可否认由RSA非对称加密保证</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（34） 💬（1）<div>老师好!有个问题，之前调用第三方的支付走https协议都需要本地配置一个证书。为啥最近有个项目也是用的https协议(url里会放token)。直接和http一样调用就好了，不需要本地配置证书了呢？</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/70/8159901c.jpg" width="30px"><span>David Mao</span> 👍（26） 💬（3）<div>老师，请教一下，我们现在正在申请SSL证书，SSL证书有专门的机构颁发，文中老师提到HTTPS能够鉴别危险网站，防止黑客篡改，这些具体是怎么做到的呢？由专门机构颁发的原因是什么？谢谢老师。</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/54/b2/5ea0b709.jpg" width="30px"><span>Danpier</span> 👍（11） 💬（1）<div>有个疑问，维基百科 OSI 模型图表把 SSL\TLS 归到第6层（表示层），文中说 SSL 属于第5层（会话层），这里是不是写错了？ 附：
https:&#47;&#47;en.wikipedia.org&#47;wiki&#47;OSI_model#Layer_6:_Presentation_Layer</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/08/17/e63e50f3.jpg" width="30px"><span>彩色的沙漠</span> 👍（11） 💬（1）<div>1、HTTPS相对于HTTP具有机密性，完整性，身份认证和不可否认的特性,HTTPS是HTTP over SSL&#47;TLS,HTTP&gt; HTTP over TCP&#47;IP
2、实现机密性可以采用加密手段，接口签名实现完整性，数字签名用于身份认证</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/71/0b949a4c.jpg" width="30px"><span>何用</span> 👍（7） 💬（1）<div>P-256 是 NIST（美国国家标准技术研究所）和 NSA（美国国家安全局）推荐使用的曲线。而密码学界不信任这两个机构，所以 P-256 是有可能被秘密破解但出于政治考虑而未公开？</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（6） 💬（1）<div>老师您好
一直以来不太明白openssl的各版本，我看官网上还有2.0和3.0的，还有后面还有t、h、j字母跟在后面，这些大概有什么区别，正常使用不知道选择什么版本好，老师有什么建议么
感谢老师回复</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（6） 💬（2）<div>1、https与http协议相比，最重要的是增加安全性，这种安全性的实现主要是依赖于两个协议底层依赖的协议是不同的，https在传输的应用层与传输层协议之间增加了ssl&#47;tls,这就使得http在固有协议之上增加一层专用用于处理数据安全的工具。

2、机密性：数据使用非对称加密传输
完整性：数据用公钥加密，私钥解密，数据生成摘要算法，同步传输</div>2019-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（5） 💬（1）<div>老师好，我想问下，在HTTPS协议上传输的报文，是怎么被缓存的，因为传输的内容应该都是加密的，那么如何做到If-Match或者If-Modified-Since判断的呢？CDN可以解析加密过后的内容吗？</div>2021-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/ac/cec17283.jpg" width="30px"><span>zhangdroid</span> 👍（5） 💬（1）<div>HTTPS：即HTTP over SSL&#47;TLS，用来解决HTTP明文传输导致的不安全问题。流程大致为：
使用对称加密算法加解密报文，保证机密性；使用摘要算法保证数据完整性；使用证书CA来进行身份认证;而不可否认则由非对称加密算法来实现。由于非对称加密算法耗时比对称加密算法长，所以用非对称加密算法来加解密给报文加密的对称算法的秘钥：即使用公钥对对称加密算法秘钥进行加密，私钥用来相应地解密。</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（5） 💬（1）<div>老师，以下问题，麻烦解答：
1. 这就是 HTTPS 与 HTTP 最大的区别，它能够鉴别危险的网站?这个仅仅从浏览器弹出不安全的提示来说的嘛？或者说怎么个鉴别法？
2. 网站是否真实也无法验证。加了https的网站也有可能是钓鱼网站吧？也没法验证啊？</div>2019-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/a7/2c979c01.jpg" width="30px"><span>蒋润</span> 👍（5） 💬（2）<div>老师你好  https能有效防止抓包然后篡改报文数据,防止xxs攻击吗</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/0e/5f0bb588.jpg" width="30px"><span>懒人一枚</span> 👍（4） 💬（1）<div>觉得大佬还可以再深入一些，比如浏览器是如何验证证书的，证书对浏览器对作用是什么，这个证书和我们平时接口调用使用的证书有什么区别呢，为什么有的网站有证书，浏览器却不认</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/e3/0ec0b681.jpg" width="30px"><span>mini💝</span> 👍（4） 💬（2）<div>请问老师 端口的作用是什么呢？为什么http和https的默认端口是不一样的</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（4） 💬（1）<div>1：你能说出 HTTPS 与 HTTP 有哪些区别吗？
       正如文中所言HTTPS比HTTP多了一个S，这个S代表安全，是基于SSL&#47;TSL实现的，SSL&#47;TSL是专门用于安全传输的，具体咋实现的比较复杂还没弄明白，主要就是各种加密算法的应用，后面继续看。

2：你知道有哪些方法能够实现机密性、完整性等安全特性呢？
这个问题不知如何回答，不会，看答案如下。
机密性由对称加密AES保证
安全性由SHA384摘要算法保证
身份认证由RSA非对称加密算法保证
不可否认由RSA非对称加密算法保证
符合以上四点的才算是安全的通信方式，实现安全性看样子很不容易啊！
这些加密算法，他的发明者是否比较容易破解呢？还是说加密之后即使是发明者也无能为力，那如果解密的东西丢啦咋弄？</div>2020-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（4） 💬（7）<div>老师，我的个人网站：https:&#47;&#47;www.xttblog.com  在mac上的谷歌浏览器最新版中控制台总是会报一个错误，而我已经是https了，这个问题，空扰了我很久</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（3） 💬（1）<div>“明文”和“不安全”仅凭 HTTP 自身是无力解决的，需要引入新的 HTTPS 协议  老师，请问下明文和不安全不是同一个东西么？为什么要分开说呢</div>2022-02-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4faqHgQSawd4VzAtSv0IWDddm9NucYWibRpxejWPH5RUO310qv8pAFmc0rh0Qu6QiahlTutGZpia8VaqP2w6icybiag/132" width="30px"><span>爱编程的运维</span> 👍（3） 💬（1）<div>像一般的web网站存储用户的密码，密码存在数据库表中都是加密后的，这个加密跟https中的加密有啥区别？</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/ca/02b0e397.jpg" width="30px"><span>fomy</span> 👍（3） 💬（2）<div>如果每个人都可以生成一个证书，钓鱼网站也可以申请呀，不就没有什么安全性可言了吗？</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（3） 💬（1）<div>请问一下老师我这边用WireShark抓包，发现两个TLS请求和响应之间和两个HTTP请求和响应之间有很多个TCP的包，请问一下这些TCP的包是一个HTTP的响应没有发完后续一致在通过TCP包发HTTP响应的responseBody吗？ </div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b9/b9/9e4d7aa4.jpg" width="30px"><span>乘风破浪</span> 👍（2） 💬（2）<div>机密性虽然可以让数据成为“秘密”，但不能防止黑客对数据的修改，黑客可以替换数据，调整数据的顺序，或者增加、删除部分数据，破坏通信过程。
一个疑问，黑客如果不知道加密的秘钥，他截获了数据，怎么篡改数据，又如何加密？接受者又如何解密？接受者还用原来的秘钥解不了。如果黑客能获得秘钥，他就可以随便改，完整性也就没法保证了。
感觉数据完整性变成了鸡生蛋，蛋生鸡的问题。</div>2021-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/96/e3/dd40ec58.jpg" width="30px"><span>火车日记</span> 👍（2） 💬（1）<div>1 明文、不安全vs四个特性，端口80vs端口443，无加密解密流畅性vs一定的性能消耗 
2 对称加密算法保证机密性，散列值算法保证完成性和安全性</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>秘密就在于 HTTPS 名字里的“S”，它把 HTTP 下层的传输协议由 TCP&#47;IP 换成了 SSL&#47;TLS。--记下来</div>2023-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/3b/fd/2e2feec3.jpg" width="30px"><span>💍</span> 👍（1） 💬（1）<div>1.   http：不安全，明文传输，容易被劫持和篡改，协议名为http，端口号默认：80
     https：相对很安全，加密传输，相对http新增了SSL&#47;TLS层，通过一系列的密钥交换算法，加密算法， 签名算法，摘要算法实现了传输的机密性 完整性 身份认证 和 不可否认这几个安全特性，协议名为https，端口号默认为 443

2 . 机密性由对称加密AES保证，完整性由SHA384摘要算法保证，身份认证和不可否认由RSA非对称加密保证（这个是借鉴其他同学的，我觉得我还得学习下后面的课才能充分的理解）
</div>2023-01-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ojfRyNRvy1x3Mia0nssz6CNPHrHXwPPmibvds1URgoHQuKXrGiaxrEbsT6sAvuK4N4AOicySh8S9iaWcOLjteOl6Kgg/132" width="30px"><span>泥鳅儿</span> 👍（1） 💬（1）<div>您好，老师，我用openssl 生成了一个自定义证书，用https访问网站提示是不安全的，我点击继续前往，传输的数据会加密吗，这种加密安全吗，容易被破解吗</div>2022-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（1） 💬（1）<div>老师好，有几个问题请教下：“收发报文不再使用 Socket API，而是调用专门的安全接口。”这个安全接口是什么呢？另外SSL&#47;TLS运行在第五层，通讯不走下层TCP&#47;IP的话，怎么把消息发到交换机呢？</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3c/4d/3dec4bfe.jpg" width="30px"><span>蔡晓慧</span> 👍（0） 💬（2）<div>老师，我想问下SSL网关是否会限制自签名的证书，因为最近公司遇到了这样的问题。</div>2023-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/2b/14/2fa758b9.jpg" width="30px"><span>栗子叶</span> 👍（0） 💬（1）<div>老师还能回复吗？ HTTPS是不是还没有实现 “不可否认”的特性啊？</div>2023-03-07</li><br/><li><img src="" width="30px"><span>Geek_11246e</span> 👍（0） 💬（2）<div>其实没太明白您说的http代理的对报文的修改；改为https的时候，端对端还是可以解密的；除非是透明代理之类；不然还是可以改https</div>2023-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM74658w9PQeTM4TcM14BzfpJnVLrsciaS26ibRwRbCE09ydI6UlZhFrJh7iaVLp2xxhBppVDKLyRRg9Q/132" width="30px"><span>Geek_21a73c</span> 👍（0） 💬（1）<div>www.chrono.com 拒绝了我们的连接请求。这个问题怎么解决呢

C:\Windows\System32\drivers\etc\hosts写入了127.0.0.1 activate.navicat.com
127.0.0.1 www.chrono.com
127.0.0.1 www.metroid.net
127.0.0.1 origin.io

打开了nginx.exe
</div>2022-06-09</li><br/>
</ul>