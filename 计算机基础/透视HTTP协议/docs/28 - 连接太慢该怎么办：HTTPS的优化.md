你可能或多或少听别人说过，“HTTPS的连接很慢”。那么“慢”的原因是什么呢？

通过前两讲的学习，你可以看到，HTTPS连接大致上可以划分为两个部分，第一个是建立连接时的**非对称加密握手**，第二个是握手后的**对称加密报文传输**。

由于目前流行的AES、ChaCha20性能都很好，还有硬件优化，报文传输的性能损耗可以说是非常地小，小到几乎可以忽略不计了。所以，通常所说的“HTTPS连接慢”指的就是刚开始建立连接的那段时间。

在TCP建连之后，正式数据传输之前，HTTPS比HTTP增加了一个TLS握手的步骤，这个步骤最长可以花费两个消息往返，也就是2-RTT。而且在握手消息的网络耗时之外，还会有其他的一些“隐形”消耗，比如：

- 产生用于密钥交换的临时公私钥对（ECDHE）；
- 验证证书时访问CA获取CRL或者OCSP；
- 非对称加密解密处理“Pre-Master”。

在最差的情况下，也就是不做任何的优化措施，HTTPS建立连接可能会比HTTP慢上几百毫秒甚至几秒，这其中既有网络耗时，也有计算耗时，就会让人产生“打开一个HTTPS网站好慢啊”的感觉。

不过刚才说的情况早就是“过去时”了，现在已经有了很多行之有效的HTTPS优化手段，运用得好可以把连接的额外耗时降低到几十毫秒甚至是“零”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（17） 💬（2）<div>Session ID:会话复用压力在服务端
Session Ticket:压力在客户端，客户端不安全所以要频繁换密钥文件
PSK:验证阶段把数据也带上，少一次请求
前两个都是缓存复用的思想，重用之前计算好的结果，达到降低CPU的目的。第三个就是少一次链接减少网络开销。
感觉都可以把开销大的东西缓存起来复用，缓存真个好东西，空间局部命中和时间局部命中定理太牛逼了。不过最关键的还是找性能瓶颈，精确定位性能瓶颈比较重要，然后针对瓶颈优化，空间换时间或者时间换空间。这个时候算法的价值就体现出来了。可惜这些我都不会╯﹏╰</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（10） 💬（1）<div>session id 把会话信息存在服务端
session ticket 把会话信息存在客户端
psk 在session ticket 的基础上，使用early data顺便再发送一下服务端的数据</div>2020-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（7） 💬（1）<div>1. 你能比较一下“Session ID”“Session Ticket”“PSK”这三种会话复用手段的异同吗？

答：
（1）Session ID 类似网站开发中用来验证用户的 cookie，服务器会保存 Session ID对应的主密钥，需要用到服务器的存储空间。
（2）Session Ticket 貌似有点类似网站开发中的 JWT（JSON Web Token），JWT的做法是服务器将必要的信息（主密钥和过期时间）加上密钥进行 HMAC 加密，然后将生成的密文和原文相连得到 JWT 字符串，交给客户端。当客户端发送 JWT 给服务端后，服务器会取出其中的原文和自己的密钥进行 HMAC 运算，如果得到的结果和 JWT 中的密文一样，就说明是服务端颁发的 JWT，服务器就会认为 JWT 存储 的主密钥和有效时间是有效的。另外，JWT 中不应该存放用户的敏感信息，明文部分任何人可见（不知道 Session Ticket 的实现是不是也是这样？）
（3）PSK 不是很懂，貌似是在 tcp 握手的时候，就直接给出了 Ticket（可是这样 Ticket 好像没有加密呢）。

总的来说，Session ID 需要服务器来存储会话；而 Session Ticket 则不需要服务器使用存储空间，但要保护好密钥。另外为了做到“前向安全”，需要经常更换密钥。PSK相比 Session Tick，直接在第一次握手时，就将 ticket 发送过去了，减少了握手次数。</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（3） 💬（1）<div>1、相同点：都是会话复用技术
区别：
Seesion ID：会话数据缓存在服务端，如果服务器客户量大，对服务器会造成很大压力
Seeion Ticket：会话数据缓存在客户端
PAK：在Seesion Ticket的基础上，应用数据和Session Ticket一起发送给服务器，省去了中间服务器与客户端的确认步骤

2、暂无</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（2） 💬（2）<div>1.抓包看了下 442 ，复用会话时 Client Hello session_ticket 确实有数据，Sessioin Id 好像也还会复用。
Transport Layer Security
    TLSv1.2 Record Layer: Handshake Protocol: Client Hello
        Content Type: Handshake (22)
        Version: TLS 1.0 (0x0301)
        Length: 512
        Handshake Protocol: Client Hello
            ...
            Random: 9474888cafdce89fd32eac247a8b464f842efbac706d8930…
            Session ID Length: 32
            Session ID: a4a0caef10dee7a6f44aa522a35f6c799101d5eced01eb32…   # Session ID
            ...
            Extension: session_ticket (len=192)     # session_ticket
                Type: session_ticket (35)
                Length: 192
                Data (192 bytes)
            ...

Transport Layer Security
    TLSv1.2 Record Layer: Handshake Protocol: Server Hello
        Content Type: Handshake (22)
        Version: TLS 1.2 (0x0303)
        Length: 100
        Handshake Protocol: Server Hello
            ...
            Random: e82519e9e8bfcbd40e1da7a202bd50ff993d5ef0cbc33378…
            Session ID Length: 32
            Session ID: a4a0caef10dee7a6f44aa522a35f6c799101d5eced01eb32…   # Session ID
            Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (0xc030)
            ...
    TLSv1.2 Record Layer: Change Cipher Spec Protocol: Change Cipher Spec
    TLSv1.2 Record Layer: Handshake Protocol: Finished   

2.有个疑问：会话复用技术，保存会话数据的一端使用对端传过来的 Sessin Id 查询到之前的 master secret，但它如何安全的把这个 master secret 传递给对端（对端应该只有 Sessin Id 吧）？

3.抓包过程用 Chrome 发请求，前三次 Client Hello, Server Hello 握手过程都因为 Alert (Level: Fatal, Description: Certificate Unknown) 失败了，第四次才成功。 而使用 FireFox 发请则不会出现。这是因为 Chrome 内置的证书更少吗？</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>老师，以下问题麻烦请回答一下：
1.客户端有时还会再去访问 CA，下载 CRL 或者 OCSP 数据，这又会产生 DNS 查询、建立连接、收发数据等一系列网络通信，增加好几个 RTT。这个CRL 或者 OCSP是对应到某个网址上面的嘛？客户端根据网址访问？

2.它可以让服务器预先访问 CA 获取 OCSP 响应，然后在握手时随着证书一起发给客户端，免去了客户端连接 CA 服务器查询的时间。这里不是客户端自己去验证的会不会有问题？服务器自己代做了。</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>good good study，day day up.</div>2023-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/6c/d4/85ef1463.jpg" width="30px"><span>路漫漫</span> 👍（1） 💬（1）<div>老师，文章里说，这后一次握手的重点是算出主密钥“Master Secret”，而主密钥每次连接都要重新计算，未免有点太浪费了。难道每次连接的主密钥是一样的？不是每次连接的ecdhe的公钥私钥都是不同的吗？怎么还可以缓存呢？</div>2021-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（1） 💬（1）<div>1：你能比较一下“Session ID”“Session Ticket”“PSK”这三种会话复用手段的异同吗？
1-1：回话复用
核心是缓存主密钥，为啥要缓存？因为计算出主密钥比较费劲，如果能重复利用，重复计算的活就免了，这是在拿空间换时间。
1-2：Session ID
可以认为是缓存主密钥的key，在客户端和服务器都有存储，通过传递这个key来获取和重用主密钥。
缺点是太费服务器的村村资源，因为每一个客户端的回话数据都需要保存，如果客户端有百万甚至千万基本，那存储空间使用的就有些多啦！
1-3：Session ticket
这个方案可以解决服务器存储空间压力山大的问题，核心是把信息放在客户端存储，当然是加密后的信息，服务器侧需要解码后再使用。
1-44：PSK
和Session ticket类似，为了效率加大了一些安全风险，ticket中带上了应用数据的信息，这样能省去服务器的确认步骤。为了加强安全性，使用上做了一些限制。
有此可见，没有完美的解决方案，具体想要什么需要自己权衡对待。想要实现多快好省，那要么是一句口号，要么必须付出其他的代价。

2：你觉得哪些优化手段是你在实际工作中能用到的？应该怎样去用？
软件优化这个估计最常用，也能用到，一些安全漏洞或性能优化常这么玩。</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/03/24a892b7.jpg" width="30px"><span>书生依旧</span> 👍（1） 💬（1）<div>PSK 在发送 Ticket 的同时会带上应用数据，免去了 1.2 里面的服务器确认步骤。
这句话有点不太理解，请问老师：
1. 看图上 pre_shared_key 是在 Hello 中发送的，Session Ticket 也是在 Hello 中发送的吗？
2. 带上应用数据是什么数据?
3. 1.2 里面的服务器验证指的是哪个步骤？</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>关于证书优化“OCSP Stapling”（OCSP 装订），有个小点，赘述一下：针对服务器返回的OCSP 响应，客户端是会进行相关验证的，大概是验证 ocsp响应数据是否被篡改、响应数据内的一些状态码等</div>2024-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/98/fab9bd2a.jpg" width="30px"><span>Mingyan</span> 👍（0） 💬（2）<div>老师请问一下，ssl connections什么条件下才会复用的？我遇到从一台机子循环发送A然后B两个请求，A和B是不同域名下的资源。第一个请求是A第二个请求是B第三个请求再发A并不会复用ssl connections而是新开。</div>2023-06-26</li><br/><li><img src="" width="30px"><span>Geek_11246e</span> 👍（0） 💬（1）<div>请问异步通信可以讲下吗</div>2023-02-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ojfRyNRvy1x3Mia0nssz6CNPHrHXwPPmibvds1URgoHQuKXrGiaxrEbsT6sAvuK4N4AOicySh8S9iaWcOLjteOl6Kgg/132" width="30px"><span>泥鳅儿</span> 👍（0） 💬（2）<div>老师，如果安装的ssl证书过期了，之后进行的http数据传输还是加密的吗</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/01/c5/b48d25da.jpg" width="30px"><span>cake</span> 👍（0） 💬（1）<div>老师请问下    非对称加密解密处理“Pre-Master” 这计划的意思就是生成 “Pre-Master” 的意思么</div>2021-11-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKiay65IMyD82E59Xnbp370ChMG3N9XQuXoKwfhZJ19zotzKMlJhwzBDxE61bp26jdkf54NY9L41yg/132" width="30px"><span>Geek_5227ac</span> 👍（0） 💬（1）<div>罗老师，本节最后提到PSK有遭重放隐患，但为什么TLS开始握手阶段的明文传输没有重放危险呢，是因为有携带应用数据才谈重放吗？另外HTTPS是先有tcp连接了再来TLS握手，那有没可能黑客通过不断地先进行TCP连接再TLS握手来很快消耗掉服务器提供正常服务的连接资源？</div>2021-03-24</li><br/><li><img src="" width="30px"><span>Geek_e4a9c5</span> 👍（0） 💬（1）<div>接之前提的问题，可是session id和session ticket不也是一段时间内固定的吗，psk只是加上了https报文信息，还是不太理解“更容易”被攻击的原因，万分感谢老师解答。</div>2020-08-26</li><br/><li><img src="" width="30px"><span>Geek_e4a9c5</span> 👍（0） 💬（1）<div>请问PSK 为什么容易受到重放攻击呢</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a5/f0/8648c464.jpg" width="30px"><span>Joker</span> 👍（0） 💬（1）<div>特来请教老师，第二个问题，有什么开源的项目里面有实现了这些吗？</div>2020-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/67/beca0050.jpg" width="30px"><span>Amberlo</span> 👍（0） 💬（1）<div>老师好，关于 证书优化，获取CRL列表的时候会不会存在中间人攻击呢</div>2020-04-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/81/51/4999f121.jpg" width="30px"><span>qzmone</span> 👍（0） 💬（1）<div>老师，https:&#47;&#47;www.chrono.com:441&#47;28-1 这个我抓包看到client和server的session-ID不一样，而且每次也都是server发了变更密码规范消息后才发加密的数据，跟您说的不一致？不知什么原因</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（0） 💬（1）<div>1、相同点：都是会话复用技术
区别：
Seesion ID：会话数据缓存在服务端，如果服务器客户量大，对服务器会造成很大压力
Seeion Ticket：会话数据缓存在客户端
PAK：在Seesion Ticket的基础上，应用数据和Session Ticket一起发送给服务器，省去了中间服务器与客户端的确认步骤

2、暂无</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/26/7e/823c083e.jpg" width="30px"><span>Wr</span> 👍（0） 💬（1）<div>1、相同点：都是会话复用技术
区别：
Seesion ID：会话数据缓存在服务端，如果服务器客户量大，对服务器会造成很大压力
Seeion Ticket：会话数据缓存在客户端
PAK：在Seesion Ticket的基础上，应用数据和Session Ticket一起发送给服务器，省去了中间服务器与客户端的确认步骤

2、暂无</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（0） 💬（2）<div>老是，如果使用服务器集群来做专门的加解密运算，建立TSL链接时，客户端将数据发送给服务器集群计算密钥，服务端又是如何安全的将密钥返回？或者是在解密报文时，又如何将解密后的报文安全返回？</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/e4/825ab8d9.jpg" width="30px"><span>刘政伟</span> 👍（0） 💬（1）<div>客户端再次访问的时候会携带session ticket，服务器解密后验证有效期，就可以恢复会话，开始加密通信；关于这句话，服务器解密后只是验证ticket的有效期吗？session ticket用于加密会话信息，如果不做其它验证，是怎么确定客户端的身份呢？</div>2019-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/77/e5/eed499a6.jpg" width="30px"><span>Geek_hfbm3l</span> 👍（0） 💬（1）<div>老师好，问下使用了 OCSP Stapling 那客户端是不是就不要去 CA 验证证书了，那会不会导致不安全呢。</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师你好，预共享密钥的0-RTT不是真的0-RTT吧。</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师你好，有什么好办法可以有效监控和调优Https连接建立的具体时间吗？</div>2019-07-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLCEsLNSXFBaUaaIsA1PDvKUXC8T3EHBYhicVlLK7SLiaVjbwDXLkH4SVvEic9iaIrGVo9aROttCbcibibQ/132" width="30px"><span>Geek_43174f</span> 👍（0） 💬（1）<div>你好，有个问题想请教一下，线上的项目，一个是生产环境，一个是测试环境，我在同一个浏览器上进行访问这两个环境，当我从测试上切换到生产上之后，生产环境需要重新进行登录，而且当我从生产上切换到测试上之后也需要进行登录，点击登录之后就报400错误，而且接口调用也改变了</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（0） 💬（1）<div>TCP fast open开启算不算优化呢</div>2019-07-31</li><br/>
</ul>