你好，我是王新栋。

如果你是一个第三方软件开发者，在实现用户登录的逻辑时，除了可以让用户新注册一个账号再登录外，还可以接入微信、微博等平台，让用户使用自己的微信、微博账号去登录。同时，如果你的应用下面又有多个子应用，还可以让用户只登录一次就能访问所有的子应用，来提升用户体验。

这就是联合登录和单点登录了。再继续深究，它们其实都是OpenID Connect（简称OIDC）的应用场景的实现。那OIDC又是什么呢？

今天，我们就来学习下OIDC和OAuth 2.0的关系，以及如何用OAuth 2.0来实现一个OIDC用户身份认证协议。

## OIDC是什么？

OIDC其实就是一种用户身份认证的开放标准。使用微信账号登录极客时间的场景，就是这种开放标准的实践。

说到这里，你可能要发问了：“不对呀，使用微信登录第三方App用的不是OAuth 2.0开放协议吗，怎么又扯上OIDC了呢？”

没错，用微信登录某第三方软件，确实使用的是OAuth 2.0。但OAuth2.0是一种授权协议，而不是身份认证协议。OIDC才是身份认证协议，而且是基于OAuth 2.0来执行用户身份认证的互通协议。更概括地说，OIDC就是直接基于OAuth 2.0 构建的身份认证框架协议。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（18） 💬（7）<div>还是没有搞懂 id_token 的用处是什么…… 

1. 客户端需要解析 id_token 的话，需要和服务器端共享密钥，这怎么解决？会不会造成密钥泄漏？
2. 如果只是解析出一些用户信息，发请求给服务器，服务器用 access_token 拿到用户信息，返回给客户端，不是也行吗？只要 access_token 没过期（即还在登录态），客户端就能拿到用户信息。
3. 如果 access_token 过期（即登录已失效），客户端仍然可以用 id_token 解析出用户信息，这岂不是更不合理？</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/0b/0128ae45.jpg" width="30px"><span>工资不交税</span> 👍（12） 💬（8）<div>在应用oss中，一端退出是不是还需要通知认证服务？不然认证服务的状态还是登录，那其他端还是能直接登录，甚至自己都没法退出。

</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/4d/16/848d2722.jpg" width="30px"><span>DB聪</span> 👍（9） 💬（10）<div>图3中”重复上述1-6”陈述单点登录的描述感觉有点难理解，原因在第3步，如果分别登陆a1.com、a2.com、a3.com的时候，都有第3步的参与，那是否意味着End User每次都需要输入用户名和密码呢？</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a7/e4/5a4515e9.jpg" width="30px"><span>成立-Charlie</span> 👍（7） 💬（4）<div>老师，您好！关于ID Token和Access Token，还需要再请教一下。
如果Access Token没有使用JWT，第三方应用无法从Access Token中获取用户信息，这样我们就需要ID Token来存放用户信息，这比较容易理解。但是，如果Access Token是JWT格式的，第三方应用是可以从Access Token中解析出用户信息的，再使用ID Token显得不是很有必要。（JWT可以采用非对称证书的方式保证安全）这块老师能帮忙稍微再解释一下吗，谢谢！
另外，当我们继承一个认证服务的时候，ID Token是我们评断认证服务是否实现OIDC的标准吗？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/0f/d9d878f8.jpg" width="30px"><span>leros</span> 👍（6） 💬（1）<div>能不能比较下基于SAML和基于OIDC的SSO？一些大的授权服务平台可能二者都提供，不太清楚具体实践中如何选择</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/3f/40d1cd7f.jpg" width="30px"><span>stubborn</span> 👍（5） 💬（2）<div>老师您好，两个问题请教下。
1. access_token失效了可以用refresh_token重新获取。id_token失效了怎么办，这块有没有规范？ keycloak的实现中使用refresh_token可以重新生成id_token。 
2. Oauth2其实也可以实现认证的功能，只要把access_token定义包含认证信息就可以了，这样使用access-token就类似id_token了。不太明白为何OIDC需要突出这部分的定义？</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（4） 💬（4）<div>传统的登录基于Session，是不是使用JWT Token方案，就不需要Session了（也不需要Cookie参与了）？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（4） 💬（5）<div>代码中access_token中就包含用户信息，获取accesstoken 时候需要带上id_token中的用户唯一标识？</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（2） 💬（1）<div>前面的课程里讲到，一般来说 JWT 有个缺陷，为了克服“覆水难收”，需要一个额外的用户粒度的密钥管理。那么，这个用户粒度的密钥管理是针对 access_token 的吗？id_token 的密钥，也需要到用户粒度吗？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/a3/aee7ded7.jpg" width="30px"><span>在路上</span> 👍（1） 💬（1）<div>王老师，单点登录的步骤中，a2.com需要去解析，id_token的 ID值么？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/0a/df537a6f.jpg" width="30px"><span>冷锋</span> 👍（1） 💬（2）<div>CAS和SSO有什么区别？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2c/56/ff7a9730.jpg" width="30px"><span>许灵</span> 👍（1） 💬（4）<div>好像现在的第三方登录都是通过access_token来获取用户信息的，这是不是表示access_token与id_token合并了？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（5）<div>单点登陆的那个流程图没有看懂， 为什么 a1.com 输完用户名密码授权登陆后， 在访问 a2.com, a3.com 还有走 1-6的步骤呢？ 这就不符合一次输入授权 多处登陆了啊</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（1） 💬（2）<div>userinfo 端点是啥意思，就是请求时候，access _token会带上用户唯一标识？app_id算不算唯一标识，和用户绑定关系</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（0） 💬（1）<div>提个建议.  用例代码就算不用spring , 也得用maven啊, 这种纯web还得陪容器,只是增加了复杂而已. </div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/dc/b48a8b4b.jpg" width="30px"><span>Beyoung</span> 👍（0） 💬（1）<div>不能用jwttoken一次到位么，为什么还要两个</div>2020-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/b0/26c0e53f.jpg" width="30px"><span>贺宇</span> 👍（0） 💬（1）<div>这么说想要做单点登录还是要基于session，就很烦</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/df/866ed645.jpg" width="30px"><span>xuyd</span> 👍（0） 💬（1）<div>能不能比较下基于SAML和基于OIDC的SSO？一些大的授权服务平台可能二者都提供，不太清楚具体实践中如何选择</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/c3/61/6de4f2ce.jpg" width="30px"><span>Free</span> 👍（0） 💬（1）<div>想问一下老师，签发id_token和签发access_token一般是同一台服务器签发的吗？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/96/0f/d9d878f8.jpg" width="30px"><span>leros</span> 👍（0） 💬（1）<div>这篇文章描述了基于授权码许可类型来构建 OIDC ，有没有可能通过其他类型（比如隐式许可）来构建OIDC呢？</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/13/7d/1454db9c.jpg" width="30px"><span>KeepGoing</span> 👍（13） 💬（1）<div>感觉每节课都有一些细节没讲到，让很多人有同样的疑惑。</div>2021-07-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK40RCxCdCaKfDiaz9Ia8g4nNyUM8wJxAGfm9ZmG5wSMQeuhgqjibGzaibBkYcGxDV8vpxhvoFcF1vyw/132" width="30px"><span>Jason180915</span> 👍（4） 💬（7）<div>a2. com是靠什么让认证服务器知道它和a1.com是一组单点登录应用，而且怎么在a1登录后让a2知道的？没弄明白。</div>2021-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（2） 💬（0）<div>1. 一般OAuth只解决授权问题，比如小兔软件获取京东的订单，用户已经登录小兔软件，是小兔本身完成的认证，剩下的只是京东给小兔授权的问题。而OIDC要在此基础上解决认证的问题，就是我需要京东的账号登录小兔软件，然后再获取授权拿到订单数据。因此，小兔软件的用户头像那里其实是京东的用户信息，这是哪里来的？就是得需要access token发起一次请求，而参数一般就是id token里用户的ID。
2. 第三方软件解析ID token需要验证签名，这就需要key，这个key也得需要access token来获取。</div>2021-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d6/68/3855df56.jpg" width="30px"><span>胖大蟲</span> 👍（2） 💬（0）<div>不太理解id_token的必要性，既然已经有了access_token，那我拿access_token向服务请求用户信息不就可以了？</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4a/bd/f7f1b3b2.jpg" width="30px"><span>好好生活</span> 👍（1） 💬（0）<div>EU的唯一id 值是怎么来的呢</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/39/7e/abb7bfe3.jpg" width="30px"><span>Geek_c53s4g</span> 👍（1） 💬（1）<div>老师：问个问题，前后端分离的SSO中，主域名相同可以使用cookie，但是跨域名的sso怎么实现呢？，还有就是SSO是否需要session？还是纯前端cookie保存</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（0）<div>老师，您好，有点疑问：
1.单点登录流程那里，用户从 a1 登录后，第三方软件访问 a2, a3 时需要携带什么信息供客户端进行登录状态的判断？id_token 吗？
2.如果不是第三方软件访问 a2, a3，而是浏览器访问，比如登录淘宝后，访问天猫，这样的单点登录的过程？
</div>2020-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/09/d6/5f366427.jpg" width="30px"><span>码农Kevin亮</span> 👍（0） 💬（0）<div>单点登录“重复1-6步”好像不对，我体验过的单点登录都不需要用户重新做第三步的登录动作，不然也称不上是单点登录了</div>2023-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnv4h4j5tWywnuIKJHXwhkXImSCMsx1CDD2dmoNUjOBACyicHZvuNN125wnDYgnSLyboIfCytEzRw/132" width="30px"><span>杨栋</span> 👍（0） 💬（0）<div>怎么确保a2.com和a1.com都属于同一个第三方呢</div>2023-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c7/11/107a25e8.jpg" width="30px"><span>草帽路飞</span> 👍（0） 💬（0）<div>还有好多不明白的点。
1. id_token, access_token与refresh_token的关系，很明确，id_token是用于身份认证的，access_token是用于请求受保护的资源的。 
所以，是不是小兔打单软件请求自己本身需要登录的资源(api接口)的时候，只需要带上id_token就行，而access_token是用来访问京东认证平台的(比如userInfo)必须带上。
那问题是id_token,access_token都有过期时间，为了保证安全性, id_token, access_token都是设置的短时间的，那这个refresh_token听说只是用来刷新access_token的。那id_token怎么刷新？

2. 关于单点登录的问题
假设rp1 a1.com是小兔打单软件，rp2  a2.com是小狗管理系统，op是京东用户身份认证服务。架构都是采用前后端分离。

    1. a1.com --&gt; 未登录(前端一般就判断cookie或storage里有没有，后端一般就解析前端传过来的idtoken来判断有没有过期) --&gt; 重定向至京东认证服务登录页面--&gt;登录成功(前端记录cookie？) --&gt; 最终返回id_token, refresh_token, access_token三件套
    2. a2.com --&gt; 未登录  --&gt; 重定向至京东认证服务(前端判断已登录) --&gt; 返回授权码 及 state --&gt; 获取id_token,refresh_token,access_token

想问下，a2.com这里的id_token,refresh_token,access_token 和 a1.com的是一套么？ 或者这一套是新生成的一套？

3. 对于单点登录与登出，我看oidc有自己的一套规范，意思是还需要维护会话管理？如果是使用的jwt，又有一套会话管理，那使用jwt的意义是什么</div>2023-10-12</li><br/>
</ul>