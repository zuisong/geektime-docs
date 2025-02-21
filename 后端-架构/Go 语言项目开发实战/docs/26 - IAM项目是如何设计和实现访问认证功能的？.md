你好，我是孔令飞。

上一讲，我们学习了应用认证常用的四种方式：Basic、Digest、OAuth、Bearer。这一讲，我们再来看下IAM项目是如何设计和实现认证功能的。

IAM项目用到了Basic认证和Bearer认证。其中，Basic认证用在前端登陆的场景，Bearer认证用在调用后端API服务的场景下。

接下来，我们先来看下IAM项目认证功能的整体设计思路。

## 如何设计IAM项目的认证功能？

在认证功能开发之前，我们要根据需求，认真考虑下如何设计认证功能，并在设计阶段通过技术评审。那么我们先来看下，如何设计IAM项目的认证功能。

首先，我们要**梳理清楚认证功能的使用场景和需求**。

- IAM项目的iam-apiserver服务，提供了IAM系统的管理流功能接口，它的客户端可以是前端（这里也叫控制台），也可以是App端。
- 为了方便用户在Linux系统下调用，IAM项目还提供了iamctl命令行工具。
- 为了支持在第三方代码中调用iam-apiserver提供的API接口，还支持了API调用。
- 为了提高用户在代码中调用API接口的效率，IAM项目提供了Go SDK。

可以看到，iam-apiserver有很多客户端，每种客户端适用的认证方式是有区别的。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（8） 💬（1）<div>本文的意思是说正常的生产环境下，iam-apiserver和iam-authz-server的api的认证功能其实都应该放到网关来实现的，本文之所以由iam项目亲自来实现就是为了方便讲解认证的具体实现方法，我理解的对不对？</div>2021-07-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIW5xLKMIwlibBXdP5sGVqhXAGuLYk7XFBrhzkFytlKicjNpSHIKXQclDUlSbD9s2HDuOiaBXslCqVbg/132" width="30px"><span>Geek_f23c82</span> 👍（3） 💬（1）<div>麻烦问下authserver什么时候派发的jwt token？</div>2022-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（3） 💬（1）<div>jwt需要后端解析并从缓存中拿用户对应秘钥在进行运算进行鉴权，这些流程是不是有点复杂和多余啊，登录时候直接随机生成一个token（uuid hash）传给前端并保存到缓存中，缓存中token直接对应用户的session，每次前端传过来token 根据是否能用token获取缓存中的session来鉴权 这样岂不是实现简单 也安全啊  </div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/84/5b7d4d95.jpg" width="30px"><span>冷峰</span> 👍（3） 💬（11）<div>为什么每个用户都要有一个SecretKey， 所有的用户用同一个SecretKey不行吗？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/df/367f2c75.jpg" width="30px"><span>🌀🐑hfy🐣</span> 👍（2） 💬（2）<div>请问老师为什么bearer认证里面还要basic认证？
</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/8e/4d24c872.jpg" width="30px"><span>season</span> 👍（1） 💬（1）<div>第四步，设置HTTP Header username: colin 。

应该是 第四步，给gin.Context中添加 username: colin 。  ？
</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/8e/4d24c872.jpg" width="30px"><span>season</span> 👍（1） 💬（1）<div>ParseWithClaims怎么理解？
func (p *Parser) ParseWithClaims(tokenString string, claims Claims, keyFunc Keyfunc) (*Token, error) {}

使用Claims来解析，并返回 token？</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/8e/4d24c872.jpg" width="30px"><span>season</span> 👍（1） 💬（1）<div>技巧2:使用抽象工厂模式
auth.go文件中，通过newBasicAuth、newJWTAuth、newAutoAuth创建认证策略时，返回的 都是接口。通过返回接口，可以在不公开内部实现的情况下，让调用者使用你提供的各种认证 功能。


1. 不公开内部实现的情况下，是指不公开哪个函数的内部实现？
2. 让调用者使用你提供的各种认证功能，指的是哪些方法？</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（1） 💬（4）<div>jwt貌似不可以实现实时踢人吧 一个账号登录了 在登录一次 让上次的token失效 这个jwt不可以吧</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（1）<div>总结：
IAM系统采用 Basic + bearer 两种认证方式。Basic 认证要求输入用户名和密码，返回 JWT Token；虽然客户端在访问 iam-apiserver 或者 iam-auth-server 时，在 bearer 认证中携带该 Token，服务端对该请求进行认证。
1. 服务端basic认证实现逻辑：通过 gin middleware 实现了签发 JWT 的功能。jwt.New 对象在实例化时，传递多个回调函数，比如 Authentiactor, LoginResponse 等。
2. 服务端bearer认证实现逻辑：在 gin 中以 middleware 的方式存在，借助 jwt package 完成认证。认证完成后，会在 Context 中保存Username，方便后面的handler使用</div>2021-11-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（1） 💬（2）<div>根据文中所说
 秘钥对是给iam-authz-server使用的
 每个用户维护一个密钥
请问:
1. iam-authz-server jwt认证中的jwt token谁谁生成的？是客户端还是iam-auth-server
2. 如果是客户端生成的jwt token，说明客户端是需要有secret秘钥对的信息的，请问这样设计有什么优势？
跟通过用户名密码登陆后，由服务端生成jwt token这种方式相比较有什么优势
</div>2021-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/59/a2/b28b1ffb.jpg" width="30px"><span>姚力晓</span> 👍（0） 💬（6）<div>如果 Redis down 掉，或者出现网络抖动，老师说会在新一期的特别放送里专门介绍下， 这个内容没看到？</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/d2/4ba67c0c.jpg" width="30px"><span>Sch0ng</span> 👍（5） 💬（0）<div>服务端实现Basic和Bearer认证的详细方案。
配合源码和架构图理解。</div>2021-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/55/05/72d9aa41.jpg" width="30px"><span>指尖”^^的童话</span> 👍（1） 💬（1）<div>项目有点大，如果是一步步实现的就更好了</div>2021-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/a4/4c/dd02fab5.jpg" width="30px"><span>shy</span> 👍（0） 💬（0）<div>Basic认证通用户名和密码进行认证，并使用配置文件中的JWT密钥来签发token，那么为什么iam-authz-server需要根据token的header得到密钥ID和密钥来进行token的认证呢，在什么情况下会根据用户使用不同的密钥来生成Token呢？</div>2023-09-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/a4/4c/dd02fab5.jpg" width="30px"><span>shy</span> 👍（0） 💬（0）<div>请问，为什么iam-apiserver使用配置文件中的密钥签发JWT token，而iam-authz-server确需要根据token header中的kid字段来获取sercetId，来获取密钥呢？</div>2023-09-06</li><br/>
</ul>