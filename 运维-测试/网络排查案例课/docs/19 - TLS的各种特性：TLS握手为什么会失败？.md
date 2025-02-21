你好，我是胜辉。

在前面三节课里，我带你排查了HTTP协议相关的问题。不知你有没有注意到，这三个案例里的HTTP都没有做加密，这就使得我们的排查工作省去了不少的麻烦，在抓包文件里直接就可以看清楚应用层的信息了。但在现实场景下，越来越多的站点已经做了HTTPS加密，所以像前面的三讲那样，在Wireshark里直接看到应用层信息的情况，已经越来越少了。

根据w3techs.com的[调查数据](https://w3techs.com/technologies/details/ce-httpsdefault)，目前Internet上78%以上的站点，都默认使用了HTTPS。显而易见，要对Internet上的问题做应用层方面的分析，TLS是一道绕不开的坎。

那你可能会问了：“我主要处理内网的问题，应该不用关心太多HTTPS的事了吧？”

这句话也许目前还勉强算对，但是随着各大企业不断推进零信任（[Zero Trust](https://en.wikipedia.org/wiki/Zero_trust_security_model)）安全策略，越来越多的内网流量也终将运行在HTTPS上，内网和公网将没有区别。

所以说，掌握HTTPS/TLS的相关知识和排查技巧，对于我们开展网络排查来说，是一项必备的技能了。

那么接下来的两节课，我们会集中到HTTPS/TLS这个主题上，来全面学习一下它的工作原理、常见问题和排查思路。这样以后面临HTTPS/TLS的问题时，你就可以运用这两讲里学到的知识和方法，展开排查工作了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/e0/ca/adfaa551.jpg" width="30px"><span>孙新</span> 👍（3） 💬（2）<div>如果有扩展的兴趣，荐书:
《图解密码技术》
《深入浅出HTTPS从原理到实战》
图解密码技术是当年做银行项目买的，银行对密码这块用的比较多，还有专门的加密机用来硬加密硬解密。密码技术可以从老师最后总结这块扩展开来，讲的很系统，也很形象，和当年《图解TCP&#47;IP》也是同期买的。这本书看完了以后密码相关的原理理解和使用应该没什么问题。市面上专门深入讲解HTTPS的书不多，可以参照这本，详细可以去豆瓣了解一下。</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（3） 💬（2）<div>问题1 ：
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Change cipher spec (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
其中OUT代表发包，IN代表收包

问题二：
不会，无“根”之木，是不行的。
</div>2022-03-04</li><br/><li><img src="" width="30px"><span>Geek6561</span> 👍（2） 💬（3）<div>问题1比较肤浅的理解：TLS应该是4次握手（client hello， serverHello、cert share，finish），TLS RSA 和TLS1.2 的ECDHE都是这种，如果是TLS 1.3的 Diffie-Hellman，4次还是5次不太确定了。TLS太复杂了，这一块的东西，老师有分享的打算吗？

问题1：如果客户端没有这个根证书，是不会信任服务端返回的证书链的。因为PKI的基础就是权威CA的合法性。

另外，老师，前面curl的返回中：common name: server (does not match &#39;api.server.777.abcd.io&#39;)，这个有影响吗？

</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>信任根证书 -&gt; 信任中间证书 -&gt; 信任叶子证书

curl -vk https:&#47;&#47;站点名

openssl s_client -tlsextdebug -showcerts -connect 站点名:443 
老师TLS case讲的很清楚 

</div>2022-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/e4/79/0f0114ba.jpg" width="30px"><span>taochao_zs</span> 👍（1） 💬（1）<div>1 TLS是四次握手，前面2次是hello握手，后面2次是交换密钥握手
2 会信任，只要中间证书是根证书签发出来的，可以验证证书的关系链是否一致（证书包含相同密钥和签名算法，完整性算法这些）。</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/cd/db/7467ad23.jpg" width="30px"><span>Bachue Zhou</span> 👍（0） 💬（1）<div>感觉 openssl 从本地找到同名的证书后因为该证书过期就造成握手失败是一个设计缺陷，理论上应该始终是从服务器获取的，即使为了提高效率会使用本地缓存的证书，也不应该因为该缓存过期就判定握手失败，而是应该继续从服务器获取。另外，这也说明 tls 大幅增加了通讯复杂度，所以在内网里全部启用 https 通讯将大幅增加运维成本。所以我认为 http&#47;2 和 http&#47;3 强制要求启用 https 是设计错误，提高客户的使用成本，缩减了自己的适用范围。</div>2022-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/e4/79/0f0114ba.jpg" width="30px"><span>taochao_zs</span> 👍（0） 💬（3）<div>杨老师有微信群吗，后面还想多和杨老师多多请教。</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（2）<div>我们之前也遇到过tls偶尔握手失败的案例，抓包来看是，客户端发出client hello之后，收到服务器的rst消息，且这个rst消息的ttl的值是64，我们猜想是被防火墙阻止了。不知老师是否遇到这样的case？以及分析原因呢？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（1）<div>请问老师，PKI 里有交叉签名的技术，就是新老根证书对同一个新的中间证书进行签名，但并不适用于这个案例。 此时，对于这个中间证书签名的叶子证书，验证流程是如何呢？新老根证书都会验证么？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/50/33/9dcd30c4.jpg" width="30px"><span>斯蒂芬.赵</span> 👍（0） 💬（0）<div>使用go的http client对一个重定向短链发起curl get请求的时候报错：remote error: tls: internal errors是啥原因？</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>老师， 我看TLS 握手的时候 Server Key Exchange 里面除了 public_key 还有一个 signatrue,   Client Key Exchange 里面没有这个， 这个 signatrue 是起什么作用的？</div>2022-08-06</li><br/>
</ul>