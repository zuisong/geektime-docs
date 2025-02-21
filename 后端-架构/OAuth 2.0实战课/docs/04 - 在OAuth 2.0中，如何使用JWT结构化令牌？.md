你好，我是王新栋。

在上一讲，我们讲到了授权服务的核心就是**颁发访问令牌**，而OAuth 2.0规范并没有约束访问令牌内容的生成规则，只要符合唯一性、不连续性、不可猜性就够了。这就意味着，我们可以灵活选择令牌的形式，既可以是没有内部结构且不包含任何信息含义的随机字符串，也可以是具有内部结构且包含有信息含义的字符串。

随机字符串这样的方式我就不再介绍了，之前课程中我们生成令牌的方式都是默认一个随机字符串。而在结构化令牌这方面，目前用得最多的就是JWT令牌了。

接下来，我就要和你详细讲讲，JWT是什么、原理是怎样的、优势是什么，以及怎么使用，同时我还会讲到令牌生命周期的问题。

## JWT结构化令牌

关于什么是JWT，官方定义是这样描述的：

> JSON Web Token（JWT）是一个开放标准（RFC 7519），它定义了一种紧凑的、自包含的方式，用于作为JSON对象在各方之间安全地传输信息。

这个定义是不是很费解？我们简单理解下，JWT就是用一种结构化封装的方式来生成token的技术。结构化后的token可以被赋予非常丰富的含义，这也是它与原先毫无意义的、随机的字符串形式token的最大区别。

结构化之后，令牌本身就可以被“塞进”一些有用的信息，比如小明为小兔软件进行了授权的信息、授权的范围信息等。或者，你可以形象地将其理解为这是一种“自编码”的能力，而这些恰恰是无结构化令牌所不具备的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/e9/97/c190359c.jpg" width="30px"><span>Neo</span> 👍（27） 💬（5）<div>老师，您好，有2个疑问：
1. 在jwt.io网站上验证的时候，如果不输入密钥，返回invalid Signature, 但是header和payload信息依然可以正确显示。我的理解是，在生成header和payload部分的时候，是通过base64编码，没有进行加密处理。最后的签名是保证整个body在传输的过程中没有被篡改。那么是不是意味着使用JWT方式，信息的主体还是依然能被未授信的第三方获取到？
2. 您提到JWT的一个优势是资源服务器不需要依赖数据库存储相关的信息，从而易于横向扩容。但是密钥部分还是躲不过需要查询的，可能依然需要存储。另外，如果采取一个用户用一个密钥的方式，资源服务器如何知道某个JWT token是给哪个用户使用的？（用户信息包含在header or payload中？）
谢谢</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（14） 💬（4）<div>我对JWT的理解是：JWT本身只对payload进行了签名，并没有做加密（base64编码不算加密）。文中多次提到加密，我比较疑惑，是我的理解错了吗？</div>2020-07-10</li><br/><li><img src="" width="30px"><span>Geek_7932</span> 👍（11） 💬（3）<div>老师，感觉JWT在文章中的讲解在加密、解密这一块稍微有点模糊，不易理解
JWT在这里的作用主要是将用户授权信息保存在结构体中，生成和内容校验都是在授权服务和受保护资源这一方
对于第三方应用来说，JWT和UUID的token都是一样的，就是个授权字符串；而对于授权服务这方来说，是不太一样的，JWT上存用户授权信息，而UUID则是在数据库存授权信息
对于JWT是否使用对称和非对称加密，密钥&#47;（公钥、私钥）都只是授权服务&#47;受保护资源这一方用到了，选择哪种加密方式其实在这差别不大，密钥&#47;（公钥、私钥）都不会公开出去，而且对称加密还有速度更快的优势，或许对称加密在这更加合适</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（8） 💬（1）<div>另外，文中提到的两种方式来让JWT失效，我觉得并不一定可行，这两种方式有效的前提应该是资源服务器每次验证jwt的时候都会先去授权服务器要一遍秘钥，这样才能通过秘钥的变更来导致jwt失效。

但很多时候，为了进一步发挥jwt的去中心化优势，资源服务器在获取秘钥后通常会进行缓存，后续的请求并不会再去获取秘钥，这样即使更改秘钥也无济于事。除非同时重启资源服务器。

还是推荐让jwt不要保存敏感数据，同时让有效期尽可能短，比如 15 分钟，来减少风险。

如果实在安全性要求高，就弃用jwt这种格式。</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/81/1c614f4a.jpg" width="30px"><span>stg609</span> 👍（5） 💬（2）<div>讲的很精彩，但是似乎少了一部分，就是服务端到底是如何来验证一个jwt是否合法的？</div>2020-08-14</li><br/><li><img src="" width="30px"><span>赵嘚住</span> 👍（4） 💬（1）<div>老师，您好，还有个问题，既然说了减少和数据库的调用次数，那jwt的第三部分秘钥如果验证他的准确性？这个秘钥不也是要存储在数据库，当接受到token解密以后，通过信息在数据库中查出来对比以后才能验证通过，或者rpc以后验证？这样总还是要查询数据的，只是没有暴露密码而已，但很多问题还是没有解决？求老师解答</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（3） 💬（3）<div>老师，jwt中signature已经在签名的时候用到了一个secret，这样已经能保证只有知道secret的第三个方才能验证jwt合法性，为什么还要加密，为了防止解密出head和payload？</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（3） 💬（1）<div>如果需要从服务器端直接暴力将某些用户“踢出下线”，是不是就不能使用 JWT 令牌？除非在另外的密钥管理系统里，将这些用户的密钥强行改掉？</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（3） 💬（2）<div>请问一个用户一个密钥这种方案用的多么。
我感觉无论怎么设计，受保护资源都要存储额外存储一些信息才行，这样JWT的优势就没了。
既然这样我们为什么不用一个随机生成的token代替JWT，让受保护资源通过调用授权服务的接口来验证token以及权限呢？
确实这JWT方案可以减少对授权服务的请求，但还多了同步密钥信息的功能，如果有多个资源服务需要验证token，那是不是密钥信息要冗余多处，增加了泄漏的风险？</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b3/b4/3237ba96.jpg" width="30px"><span>老烟斗</span> 👍（2） 💬（2）<div>把用户密码当做秘钥不合适吧，如果用户修改密码，所有的授权都会失效</div>2020-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（2） 💬（1）<div>jwt如果每个用户一个密钥，就还需要访问数据库，这种方式和无结构的token优化没那么明显，只是省了token的存储。</div>2020-07-14</li><br/><li><img src="" width="30px"><span>Max</span> 👍（2） 💬（2）<div>老师您好，如果传输层已经是加密的（TLS），JWT就不用加密了吧（用签名来保证数据完整性应该就够了）</div>2020-07-11</li><br/><li><img src="" width="30px"><span>Geek_7c4953</span> 👍（1） 💬（1）<div>如果JWT需要加密，那解密的秘钥要存储在哪呢？如果是web场景，在JS中存储秘钥跟明文没有差别啊。还是说JWT只能用于服务器之间的授权访问？</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（1） 💬（1）<div>文中说JWT的加密算法，既可以是对称加密，也可以是非对称加密。这里的对称加密是不是不包括 base64？感觉只用base64的话，和不加密没有区别（贴到https:&#47;&#47;jwt.io&#47;就可以看到明文）。</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（1） 💬（1）<div>请问老师，既然不能让JWT不可控，就要用户粒度的密钥管理，在我的理解，就是至少维护一个用户和密钥的键值对，那这和 Session 管理是不是本质上一样？</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/8a/b5ca7286.jpg" width="30px"><span>业余草</span> 👍（1） 💬（3）<div>JWT 令牌如何刷新，有没有好的方案给我们讲一讲？</div>2020-07-09</li><br/><li><img src="" width="30px"><span>赵嘚住</span> 👍（1） 💬（2）<div>老师，你好，想问一下，既然令牌信息不在服务端存储，我怎么知道他失效了呢，是判断失效时间？如果主动让令牌失效，我服务端什么都没有记录，怎么知道这个令牌已经不能用了？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a9/f6/35b55830.jpg" width="30px"><span>阿秋</span> 👍（1） 💬（1）<div>最近正好在研究JWT令牌撤回的实现方式，第一次听说老师说的这种密钥管理系统的方式，我还是有些疑问，每个用户一组秘钥，用户多了会不会使我们的应用性能下降</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/c6/6f39a982.jpg" width="30px"><span>Yuhui</span> 👍（0） 💬（1）<div>请教老师，图4令牌生命周期序列图里最后两项“撤回访问令牌”和“撤回刷新令牌”是否应该调换一下顺序？</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/c0/1c0f00ca.jpg" width="30px"><span>lign</span> 👍（0） 💬（2）<div>老师，如果对JWT加密，资源服务器收到加密后的JWT串，需要解密时，JWT里面的内容，怎么获取解密密码？需要到独立密钥管理系统请求解密密码？ 如果是这样，JWT协议本身是不是相当于信息在裸奔？如果不额外增加加密过程的话</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/6e/edd2da0c.jpg" width="30px"><span>蓝魔丶</span> 👍（0） 💬（1）<div>老师，我看了评论说jwt这种token不传递前端进行交互，如果是之前的授权码方式觉得可以不传，如果是用户名密码方式呢？不是还是要传递前端嘛？而且给我的感觉jwt这种token会随着存入的json数据越多越长，基本的json数据就感觉很长了</div>2020-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/a5/625c0a2e.jpg" width="30px"><span>hhhh</span> 👍（0） 💬（3）<div>对于小兔来说，jwt放在前端不知道可不可行，老师您觉得在实际中有这么用的吗？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（0） 💬（2）<div>现在使用JWT令牌在网络传输中是否一定要进行加密，不加密的话是不是相当于裸奔？</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/4f/6e/bff1e33e.jpg" width="30px"><span>Awake  Dreaming</span> 👍（11） 💬（4）<div>老师，我这边是主要负责公司三方授权服务的，对oauth2.0的流程也算比较熟悉，但是在阅读这一节的时候有些看不懂，主要是下面这个点：
令牌是授权服务颁发给接入方的（小兔软件），正常流程应该是小兔软件想要获取受保护资源时拿着令牌去受保护资源服务，受保护资源服务通过调用授权服务的rpc接口确认并解析令牌；但是在这篇文章中，老师讲到受保护资源服务对于JWT令牌的解析并不需要依赖授权服务，那它是如何解析的呢？
我这边的理解（猜测）是除非令牌的解密密钥和验签算法在受保护资源服务这边都有，否则解密和验签还是都要调用授权服务，还是会对授权服务有依赖</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c3/ab/c2ca35e6.jpg" width="30px"><span>名贤集</span> 👍（4） 💬（9）<div>用户粒度秘钥有问题啊！你如何确定传递过来的jwt是哪个用户的？用户信息存储在jwt里面啊。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（3） 💬（0）<div>密钥肯定要定期更换吧？如果是的话，密钥的管理是个问题，密钥换的话，客户端和服务端都要换的吧，关于密钥管理，老师有没有什么好的实践吗？</div>2020-07-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/aiaO77mTsCalcia49ElevPn988pgwcL3rD5ic1DTD6E8rbAwfmguiaPsibHicsYGQID7VbmD21GUAV9bbuNMfDhDGGyg/132" width="30px"><span>穿针土豆丝</span> 👍（2） 💬（0）<div>服务端不再存储 JWT 令牌，自然过期好理解，但如何主动销毁 JWT 令牌呢？</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/a6/29ac6f6a.jpg" width="30px"><span>XXG</span> 👍（1） 💬（0）<div>JWT 的签名机制确保了令牌的完整性和真实性，但它并不能防止令牌信息被暴露。JWT 的载荷信息是以 Base64 编码的形式进行传输，因此可以被解码和读取。

如果你希望令牌信息不被暴露，可以考虑以下几点：

最小化敏感信息：避免在 JWT 的载荷中包含敏感信息。将敏感数据存储在服务端，而不是放在令牌中。

加密令牌：除了签名以外，你可以选择对整个 JWT 进行加密。这样即使令牌被拦截，攻击者也无法解密和读取其内容。

使用 HTTPS：确保在令牌的传输过程中使用安全的通信协议（如 HTTPS），以加密传输中的数据，从而降低令牌被窃听的风险。

令牌的有效期限制：为令牌设置适当的有效期限制，以降低被滥用的风险。较短的有效期限制可以减少令牌的暴露时间窗口。</div>2023-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/3d/76638f13.jpg" width="30px"><span>paul</span> 👍（1） 💬（0）<div>理解老师的方案其实就是：
1. 在access token加入信息，在授权服务-&gt;第3方-&gt;资源服务的传递间，目的是减少这部分信息的存储，而为了不让第3方知道这些信息，采用加解密方式（授权服务加密，资源服务解密）。
2. 和jwt没什么关系，只是参考了格式，完全自定义结构化格式就可以。这里引入jwt反而使读者更迷惑</div>2022-02-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（1） 💬（0）<div>“不论是结构化的令牌还是非结构化的令牌，对于第三方软件来讲，它都不关心，因为令牌在 OAuth 2.0 系统中对于第三方软件都是不透明的。需要关心令牌的，是授权服务和受保护资源服务。”  对第三方是透明的吧，因为第三方应用不需要解析令牌，只需要当一个数据包，发给授权服务和受保护资源服务就行了</div>2020-09-14</li><br/>
</ul>