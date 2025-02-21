你好，我是王新栋。

当知道这一讲的主题是OAuth 2.0的安全漏洞时，你可能要问了：“OAuth 2.0 不是一种安全协议吗，不是保护Web API的吗？为啥OAuth 2.0自己还有安全的问题了呢？”

首先，OAuth 2.0 的确是一种安全协议。这没啥问题，但是它有很多使用规范，比如授权码是一个临时凭据只能被使用一次，要对重定向URI做校验等。那么，如果使用的时候你没有按照这样的规范来实施，就会有安全漏洞了。

其次，OAuth 2.0既然是“生长”在互联网这个大环境中，就一样会面对互联网上常见安全风险的攻击，比如跨站请求伪造（Cross-site request forgery，CSRF）、跨站脚本攻击（Cross Site Scripting，XSS）。

最后，除了这些常见攻击类型外，OAuth 2.0 自身也有可被利用的安全漏洞，比如授权码失窃、重定向URI伪造。

所以，我们**在实践OAuth 2.0的过程中，安全问题一定是重中之重**。接下来，我挑选了5个典型的安全问题，其中CSRF、XSS、水平越权这三种是互联网环境下常见的安全风险，授权码失窃和重定向URI被篡改属于OAuth2.0“专属”的安全风险。接下来，我就和你一起看看这些安全风险的由来，以及如何应对吧。
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="" width="30px"><span>Geek_94f887</span> 👍（12） 💬（4）<div>codeA绑定了appIdA和userIdA，为啥B能拿着appIdB和codeA，userIdB，userIdB不会验证通过，怎么可以获取到access_token？
另外，老师举例的CSRF例子我看了三遍，都没看明白，有点混乱，不够清晰，建议重写一下，感谢！~</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/41/709e9677.jpg" width="30px"><span>袁帅</span> 👍（3） 💬（2）<div>对于CSRF攻击有以下疑惑
    1.  攻击者A软件怎么知道  极课时间(B)的用于接受授权码的回调URL?
    2.&quot;如果这个时候用户 G 被攻击者软件 A 诱导而点击了这个恶意页面，那结果就是，极客时间使用 codeA 值去继续 OAuth 2.0 的流程了。这其实就走完了一个 CSRF 攻击的过程&quot;                              
           软件A的诱导页面是怎么放到极课时间平台里的？
3.极客时间通过codeA获取到了accessToken,但这一切都是在极客时间的后台完成的呀，攻击者A又是怎么得到token的？
</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/54/9c214885.jpg" width="30px"><span>kylexy_0817</span> 👍（0） 💬（1）<div>王老师好，目前的开放平台接入服务，基本都要求在其管理后台配置回调地址吧？这样只要指定回调地址，用回调地址来校验，感觉不需要state参数也能避免CSRF攻击了吧？</div>2020-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5c/a8/0fc3dce5.jpg" width="30px"><span>Invincible(･ิϖ･ิ)っ</span> 👍（0） 💬（5）<div>对于CSRF攻击有一个疑问：”有一个软件 A，我们让它来扮演攻击者，让它的开发者按照正常的流程使用极客时间。当该攻击者授权后，拿到授权码的值 codeA 之后，“立即按下了暂停键”，不继续往下走了。“ 这里授权码应该是返回到极客时间网站指定的的回调地址上了，攻击者是怎么控制流程不往下走的？ </div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4d/09/da292a37.jpg" width="30px"><span>林光铣</span> 👍（0） 💬（1）<div>老师你好，如果要将一批硬件接入OAuth2.0系统，每个硬件作为一个动态客户端注册合适呢，还是硬件配套的后台服务作为一个客户端合适？

</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（0） 💬（1）<div>CSRF的本质是身份失窃，被恶意软件或者代码使用。下图中，恶意软件A正是通过将CODE_A和软件B的身份appid_b结合在一起。从而窃取了B的身份，进行了恶意操作。

老师在课中提到，不能将OAuth2.0用于身份认证，在XSRF场景下具体指的是哪一步？因为OAuth2.0不就是利用appid和app_secret对三方软件的身份做认证的么？
或者这里指的是用户G的身份？</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/7d/1454db9c.jpg" width="30px"><span>KeepGoing</span> 👍（13） 💬（7）<div>关于CSRF的例子特别是那个配图看来看去还是很难理解。关于State的解释更是让人困惑。
攻击者到底是在具体哪一步替换CODE的？既然授权服务会原封不动的返回State值。那攻击者又为什么需要自己来构造State值？</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/f7/6ff76318.jpg" width="30px"><span>Dolphin</span> 👍（3） 💬（6）<div>老师好，关于 CSRF 中 state 的问题，原文中支出：
当极客时间请求授权码的时候附带一个自己生成 state 参数值，同时授权服务也要按照规则将这个随机的 state 值跟授权码 code 一起返回给极客时间。这样，当极客时间接收到授权码的时候，就要在极客时间这一侧做一个 state 参数值的比对校验，如果相同就继续流程，否则直接拒绝后续流程。

我的问题：
在请求授权码的时候 附带了一个 state 的值，然后 state 会和授权码一起被返回，这时候攻击者按下暂停，然后在钓鱼页面中同样携带这个 state 是不是同样不安全？

我理解的是这样？是我哪儿理解错了嘛？</div>2021-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（2） 💬（0）<div>“在https:&#47;&#47;time.geekbang.org&#47;page&#47;下，创建了一个页面 hacker.html。” — 老师，黑客是怎么才能在这里新创建一个自己的页面呢？</div>2020-10-13</li><br/><li><img src="" width="30px"><span>Geek_0cinhr</span> 👍（1） 💬（1）<div>关于csrf的state我是这样理解的: 攻击者在截取到 “回调地址？code=自己的code”这个链接后，也就是原本从 开放平台跳转到第三方平台的动作被暂停了，攻击者想让受害者点击这个链接来完成这个跳转动作。 所以如果第三方平台每次在申请code时如果加上了state参数，并且保存当前用户和state的关联关系, 那就好办了，当受害者点击 攻击者准备好的这个链接时，第三方平台首先会检查 state和当前操作的用户的关联关系是否正确，结果发现当前用户(受害者)在本平台没有与此state关联！ 应该就是这么回事</div>2024-09-06</li><br/><li><img src="" width="30px"><span>Geek_0cinhr</span> 👍（1） 💬（1）<div>csrf那里有个问题，问题是，既然攻击者能拿到code肯定也能拿到state啊。原模原样做个链接，不就能继续诱导用户走后半段流程获取access_token了么？ state反正又不用攻击者自己构造，直接截获拿来用就行了啊</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/e6/9eb1e7c1.jpg" width="30px"><span>gjc</span> 👍（1） 💬（0）<div>这个讲的非常好，https:&#47;&#47;www.jianshu.com&#47;p&#47;c7c8f51713b6</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（1） 💬（2）<div>“如果这个时候用户 G 被攻击者软件 A 诱导而点击了这个恶意页面，那结果就是，极客时间使用 codeA 值去继续 OAuth 2.0 的流程了。” 第三讲中有说，code会和用户以及appid做关联，如果codeA关联的是用户A，那用户G点击回调函数，也只能获取用户A的access_Token吧。如果传输了G用户的相关信息，授权服务应该拒绝。 所以CSRF攻击有一些前提，如授权服务没有校验codeA是属于哪个用户的code</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/c7/e6/70a131a5.jpg" width="30px"><span>Der Kaiser</span> 👍（0） 💬（0）<div>state可以在用户点击第三方软件上的授权的时候，第三方软件生成一个state值并保存在session中。当受害者A用户点击了钓鱼链接，该钓鱼链接回调第三方软件时，第三方软件服务端发现A用户的session的state和钓鱼链接中的state不同，从而拒绝执行后续的操作。流程图如下：
用户点击登录 → 服务端生成 state → 保存到 Session → 跳转到授权服务器（携带 state） 
                  ↑                                  ↓
              攻击者伪造请求（无&#47;假 state）        用户同意授权
                  ↓                                  ↓
              验证失败 ← 服务端对比 state ← 回调携带 state 和 code</div>2025-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0e/56/2c5691b2.jpg" width="30px"><span>布兜兜</span> 👍（0） 💬（0）<div>结合https:&#47;&#47;www.jianshu.com&#47;p&#47;c7c8f51713b6，个人OAuth 2.0 协议中csrf攻击的梳理一下：
1. 攻击者通过合法手段或者对应的authorization code
2. 通过钓鱼手段将已经登录的受害者点击带有攻击者授权码的链接
3. 将受害者和授权码发到对应的验证服务器进行绑定操作获取对应的access code
4. 因为攻击者账号和受害者账号做了关联，攻击者账号就可以访问受害者所有资源

由于第二部操作的URL是静态的，如果授权服务器和第三方约定有state 参数并且进行检验，授权服务如果发现state 和 authorization code 不是一一对应，就可以直接抛出异常而不是生成access code.
</div>2024-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（0） 💬（0）<div>水平越权攻击
水平越权指的是攻击者尝试访问与它拥有相同权限的用户资源，例如系统中有个人资料的功能，A账号和B账号都可以访问这个功能，但是A账号和B账号的信息不同，可以理解为A账号和B账号在个人资料这个功能上具有水平权限的划分，此时A账号如果访问到了B账号的个人资料，说明就发生了 &quot;水平越权&quot;的问题</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d5/3e/7f3a9c2b.jpg" width="30px"><span>Jaising</span> 👍（0） 💬（0）<div>补充一下，最后总结部分，在OAuth2.1规范中，已经明确重定向URI必须严格按照字符串匹配来做校验，“Redirect URIs must be compared using exact string matching”</div>2022-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/7e/79/fe67256e.jpg" width="30px"><span>赵小骄</span> 👍（0） 💬（0）<div>这个CSRF攻击的讲解不清楚，可以用之前的京东订单的例子讲好了</div>2022-09-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK40RCxCdCaKfDiaz9Ia8g4nNyUM8wJxAGfm9ZmG5wSMQeuhgqjibGzaibBkYcGxDV8vpxhvoFcF1vyw/132" width="30px"><span>Jason180915</span> 👍（0） 💬（1）<div>csrf里面。如果appid和授权码有绑定关系。也可以避免这个漏洞吧。用攻击者的授权码a+被攻击者的appid b 去获取token。检验绑定绑定关系就可以判断出来。</div>2021-03-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI8sG1WWiaN5gehJ5w7IIJ6HibkPhgQsUnajY5yvPU9zf4em3jNTrybVUFNv3FsOudaUpYVZApmibTiaQ/132" width="30px"><span>涂诗棉</span> 👍（0） 💬（0）<div>水平权限有个问题：接口提供者如果是第三方平台（有自己的用户系统），这时候如何打通三方用户关系</div>2021-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>https:&#47;&#47;wooyun.x10sec.org&#47;static&#47;bugs&#47;wooyun-2013-017306.html 
老师，
1. 当应用拿到 Access Token以后为什么要上传到“啪啪”的服务后端去换取认证字符串呢？按照标准OAuth 那样拿着Access Token 来做后续访问不可以吗？
2. 文章中提到修复建议一：“手机客户端有关认证交换的主体部分，一定要有一个服务器把关，这是最基础的。“， 能具体说说什么样的服务器把关吗？
3. 文章中提到的修复建议二：“手机服务器端在接收手机客户端的access token来对换取自家服务的认证凭据时，必须对access token进行来源查询、证明或签名校验。” ， 具体怎么做校验呢？</div>2020-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>CSRF 中为什么一定要G 现在极客时间有登陆状态呢？而且要G 先登陆过极客时间，还要能让用户点击黑客的网站，这样好像太难了。</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（2）<div>“只要我们在授权服务验证第三方软件的请求时做了签名校验，那么攻击者在只拿到授权码 code 的情况下，仍然无法获取访问令牌，因为第三方软件只有通过访问令牌才能够访问用户的数据。” — 老师，你这里说的 签名校验具体是谁的签名，放在哪里，怎么校验呢？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/49/94/55e70da0.jpg" width="30px"><span>HeRui</span> 👍（0） 💬（0）<div>状态码那个不清楚，攻击脚本在用攻击者自己的授权码发给后端服务换取access_token不知道与授权码有什么关系</div>2020-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/6d/b623562a.jpg" width="30px"><span>霹雳大仙pp</span> 👍（0） 💬（0）<div>极客时间A盗用极客时间B的授权码，绕过appid和authorization_code绑定关系检查。可以通过state参数来避免</div>2020-07-16</li><br/>
</ul>