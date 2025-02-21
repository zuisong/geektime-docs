你好，我是胜辉。

在上节课里，我们对TLS的整体的知识体系做了总览性的介绍，然后回顾了两个实际的案例，从中领略了TLS握手的奥妙。我们也知道了，TLS握手的信息量还是很大的，稍有差池就可能引发问题。我们只有对这些知识有深刻的理解，才能更准确地展开排查。

不过，也正因为这种种严苛的条件，TLS才足够安全，因为满足了这些前提条件后，真正的数据传送就令人十分放心了。除非你能调动超级计算机或者拥有三体人的智慧，要不然一个TLS连接里面的加密数据，你是真的没有办法破解的。

可话说回来，**如果排查工作确实需要我们解开密文，查看应用层信息，那我们又该如何做到呢？**

所以在这节课里，我会带你学习TLS解密的技术要点，以及背后的技术原理，最后进行实战演练，让加密不再神秘。好了，让我们开始吧。

## TLS加密原理

在上节课里我们已经了解到，TLS是结合了对称加密和非对称加密这两大类算法的优点，而密码套件是四种主要加密算法的组合。那么这些概念，跟我们的日常工作又有着什么样的交集呢？

### 解读TLS证书

下面这个证书，是我在访问站点[https://sharkfesteurope.wireshark.org](https://sharkfesteurope.wireshark.org)的时候获取到的，我们来仔细读一下这里面的内容，看看哪些是跟我们学过的TLS知识相关的。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（5） 💬（3）<div>问题一：
1 DH算法是为了解决密钥协商的算法,Bob和Alice分别用对方的公钥和自己的私钥，一通骚操作后，得到相同的会话密钥k,这就解决了密钥不直接传输而通过协商出来；
2 DH有static DH和DHE两种实现，static的方式，私钥是不变的，有被破解的可能性，进而搞出来DHE,每次双方的私钥都变化，安全性提高了不少；
3 DHE算法性能不行，然后出现基于椭圆曲线的ECDHE;
参考:https:&#47;&#47;www.likecs.com&#47;default&#47;index&#47;show?id=124371

问题二：
经过测试curl也会读取SSLKEYLOGFILE，并把随机数和secret写入到这个文件中
SSLKEYLOGFILE=&#47;my&#47;path&#47;to&#47;file.log curl https:&#47;&#47;example.com
参考:https:&#47;&#47;davidhamann.de&#47;2019&#47;08&#47;06&#47;sniffing-ssl-traffic-with-curl-wireshark&#47;</div>2022-03-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（3） 💬（1）<div>Secret：这就是 Master secret，也就是通过它可以生成对称密钥。----------&gt;老师，这个应该是premaster吧，fun(client 随机数+server 随机数+premaster） 才算出master 吧</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bf/35/0e3a92a7.jpg" width="30px"><span>晴天了</span> 👍（2） 💬（1）<div>对如何在linux抓取https明文包有点困惑 老师有什么工具推荐吗</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/61/ec61dff3.jpg" width="30px"><span>小禾先生</span> 👍（1） 💬（1）<div>老师您好，在 linux 服务端抓包，如何通过私钥 key 文件与 wireshark 解密呢？</div>2024-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（1） 💬（2）<div>我在抓极客的页面是发现了protocol类型多了一个HTTP&#47;JSON,为什么协议会有 http&#47;json 类型的</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e4/3b/f1b9d6bf.jpg" width="30px"><span>蔡俊贤</span> 👍（0） 💬（1）<div>老师您好，想问一下如果是用postman这类工具请求，有没有办法像浏览器那样解密呢？</div>2024-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（2）<div>大佬请教一个网络方面的问题：用charles抓app包，抓不到正常的https包，但是app一直加载数据，感觉是请求服务端api接口了，为啥charles抓不到，charles抓其他app正常！通过charles界面观察到的情况是，没法发送任何http请求，但是往下拉一直在加载数据，有遇到么</div>2024-12-11</li><br/><li><img src="" width="30px"><span>ray</span> 👍（0） 💬（1）<div>老师您好，
验证server这环节有点不明白。请老师看看我的思考脉络是否正确。
client拿到server回传的证书后，会验证证书是否有CA的签名，验证通过后即确认server的身份是合法的。
问题是，CA签发给server的证书所有人都拿的到，这表示所有人都可以伪装成server。

请问验证server这个环节，client是不是还会用server的公钥加密一个字串给server用私钥解密，以确认server的真实身份（因为私钥在不外泄的状况下只有server才有）？

感谢老师的解答^^
</div>2023-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/52/5c/d4a9accb.jpg" width="30px"><span>仄言</span> 👍（0） 💬（1）<div>linux  客户端 使用tcpdump  怎么抓取https 解密?</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（2）<div>Just TrustMe 解决 ssl pin 的方法， 老师可以也一块介绍吗？</div>2022-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（1）<div>为什么curl的时候，有的可以解析，有的不可以，比如https:&#47;&#47;www.baidu.com可以解密出https，但是curl  https:&#47;&#47;openapi-fxg.jinritemai.com 就解密不出来？</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（1）<div>如果是命令行curl请求，不是通过浏览器访问，是否能解密呢？</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/f4/d5/1c9c59b4.jpg" width="30px"><span>青梅煮酒</span> 👍（0） 💬（1）<div>请问Windows上配置了SSLKEYLOGFILE环境变量后，重启浏览器抓包，文件里面sslkey.log不会写入东西，老师有遇到吗</div>2022-05-26</li><br/><li><img src="" width="30px"><span>woJA1wCgAASVwFBCYVuFLQY8_9xjIc3w</span> 👍（0） 💬（1）<div>可以看下这https:&#47;&#47;github.com&#47;ehids&#47;ecapture ，不需要CA证书，即可捕获HTTPS&#47;TLS通信数据的明文</div>2022-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>只要 不乱抓信任其他不明来源的 证书，就没有人可以破解加密的信息。 聊天记录什么的都拿不到</div>2022-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/ca/3ac60658.jpg" width="30px"><span>orange</span> 👍（0） 💬（1）<div>通过 fiddler抓https的包，在fiddler控制台看到的是明文，是fiddler做了实时解密？</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/ca/3ac60658.jpg" width="30px"><span>orange</span> 👍（0） 💬（3）<div>老师我们的公众号进入直接变成了 第三方的充值页面，  这个https可以搞定么？</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/c7/a65f5080.jpg" width="30px"><span>Lucky  Guy</span> 👍（0） 💬（2）<div>老师最近刚好遇到一个和TLS相关的问题.问题如下
浏览器----https---&gt; nginx(四层正向代理,开启了TLS SNI ) ----https---&gt;源站
nginx使用https正向代理网站的时候,个别网站刚开始是可以正常访问的,如果一直执行页面操作(如:点击页面连接,刷新页面)是没问题的,但是只要浏览器闲置一段时间(3分钟左右)后,再次刷新页面就会出现500报错. 目前感觉导致问题的原因是nginx代理到源站这段有设备校验了SNI导致的. 但是抓包也没有找到证据,请问这种情况改如何分析.. </div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/58/c7/a65f5080.jpg" width="30px"><span>Lucky  Guy</span> 👍（0） 💬（1）<div>老师你好,最近刚好遇到了一个和证书相关的问题
用户(浏览器)--https--&gt; nginx(四层正向代理代理N多个域名) --https--&gt; 源站(G网站) , 用户刚开始访问G网站的时候是可以正常访问的,如果一直频繁打开子页面也是没问题的.只要页面打开后空闲2-3分钟左右(没有数据交互)再次刷新当前页面就会出现500错误,在浏览器后台清理所有sockets后即可恢复正常. 目前只发现正向代理的G网站有这个问题,其他网站都正常. 当前怀疑是G网站校验了SNI.   目前我了解到的是 只有在tls握手的时候回会</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/f5/e3f5bd8d.jpg" width="30px"><span>宝仔</span> 👍（0） 💬（3）<div>老师你好，服务端用的是nginx，可以做TLS解密码？我指在服务端</div>2022-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/eb/09/ba5f0135.jpg" width="30px"><span>Chao</span> 👍（0） 💬（1）<div>DH 不具备前向安全性， 升级成DHE（E代表临时的），又由于DHE的性能不好。 然后再DHE上增加了ECC（椭圆曲线特性）升级为ECDHE</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>DH 算法是非对称加密算法， 因此它可以用于密钥交换，该算法的核心数学思想是离散对数。

根据私钥生成的方式，DH 算法分为两种实现：
1. static DH 算法，这个是已经被废弃了， static DH 算法不具备前向安全性。
2. DHE 算法，现在常用的；让双方的私钥在每次密钥交换通信时，都是随机生成的、临时的，这个方式也就是 DHE 算法

DHE 算法由于计算性能不佳，因为需要做大量的乘法，为了提升 DHE 算法的性能，所以就出现了现在广泛用于密钥交换算法 — ECDHE 算法是在 DHE 算法的基础上利用了 ECC 椭圆曲线特性，可以用更少的计算量计算出公钥，以及最终的会话密钥。</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（3）<div>实际测试了下，curl也会使用 SSLKEYLOGFILE 这个环境变量，并导出key信息</div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/bb/0b971fca.jpg" width="30px"><span>walker</span> 👍（0） 💬（0）<div>另外，在抓取凤凰资讯的时候，发现返回两条
第一条： 5850	138.461067	140.143.221.194	192.168.2.104	HTTP2	2838		HEADERS[27]: 200 OK, DATA[27] [TCP segment of a reassembled PDU]
第二条：5851	138.461067	140.143.221.194	192.168.2.104	HTTP2	124		DATA[27]
第二条中data数据并没有解密，这是怎么回事</div>2022-08-26</li><br/>
</ul>