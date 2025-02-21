你好，我是王新栋。

今天这一讲，我并不打算带你去解决新的什么问题，而是把我们已经讲过的内容再串一遍，就像学生时代每个学期即将结束时的一次串讲，来 “回味”下 OAuth 2.0的整个知识体系。当然了，我也会在这个过程中，与你分享我在实践OAuth 2.0的过程中，积累的最值得分享的经验。

好，接下来就让我们先串一串OAuth 2.0的工作流程吧。

## OAuth 2.0工作流程串讲

![](https://static001.geekbang.org/resource/image/be/2a/beb02a5baf3654c5025238552cd26a2a.jpg?wh=1706%2A498)

我们一直在讲OAuth 2.0是一种授权协议，这种协议可以让第三方软件**代表**用户去执行被允许的操作。那么，第三方软件就需要向用户索取**授权**来获得那个令牌。

我们回想下[第1讲](https://time.geekbang.org/column/article/254565)拜访百度王总的例子。只有拿到前台小姐姐给你的门禁卡，你才能够进入百度大楼。这个过程就相当于前台小姐姐给你做了一次授权，而这个授权的凭证就是门禁卡。对应到我们的系统中，门禁卡便相当于访问令牌。

通过“代表”“授权”这样的关键词，我们可以认识到，OAuth 2.0是一个授权协议，也是一个安全协议。那么，如果我说它也是一种委托协议，你也不要吃惊。

试想一下，用户在微信平台上有修改昵称、修改头像、修改个人兴趣的权限，当第三方软件请求让自己代表用户来操作这些权限的时候，就是第三方软件请求用户把这些权限**委托**给自己，用户在批准了委托请求之后，才可以代表用户去执行这些操作。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/fa/dd/f640711f.jpg" width="30px"><span>哈德韦</span> 👍（22） 💬（2）<div>1、一定要启用 https；2、一定要把 app_secret 放在后端；3、收到 code 时，一定要校验 state 的值</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/a3/aee7ded7.jpg" width="30px"><span>在路上</span> 👍（0） 💬（1）<div>感谢老师， 从开始学习到现在，被老师纠正了思想，OAuth2.0的核心授权协议，而不是身份认证协议。面粉和面包的关系，感谢老师。安全那块 对RSCF 和XSS的理解还没到位，是自身对这块接触不多，不熟悉。在接下来的时间，多熟悉。</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/0a/7d/ac715471.jpg" width="30px"><span>独孤九剑</span> 👍（7） 💬（0）<div>安全无小事！！！
防止CSRF攻击--授权码附加STATE参数；
防止XSS攻击--服务端对非法信息转义过滤+客户端Cookie设置httponly；
防止令牌劫持--服务端启用HTTPS避免传输层泄漏+跟踪客户端登录设备信息；
防止水平越权--代码中增加“数据归属”逻辑判断。</div>2021-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e4/a1/178387da.jpg" width="30px"><span>25ma</span> 👍（3） 💬（0）<div>如何校验status的值</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ea/e7/9ce305ec.jpg" width="30px"><span>Sancho</span> 👍（2） 💬（4）<div>哈哈，我见过某互联网公司的APP，就把是把微信的appId，appSecret打包在APP里。然后以一种你想不到的方式来获取access_token：APP用授权码code+appId+appSecret，先请求自已的Server端，Server端把请求转发给微信Server，拿到access_token，再返回给APP。后续与微信Server的交互都是：APP带着access_token先请求自己的Server端，然后自己的Server端把请求转发给微信Server，再把结果返回给APP。。。</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（1） 💬（0）<div>&lt;script&gt;&lt;alert&gt;under attack&lt;&#47;alert&gt;&lt;&#47;script&gt;</div>2024-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/69/bf/58f70a2a.jpg" width="30px"><span>程序员花卷</span> 👍（1） 💬（0）<div>为了防范CSRF攻击：
1. 重要的操作尽量使用POST请求(依旧还是有风险)
2. 在条件允许的情况下，尽量引入第三方的验证码，智能的验证码破解成本高甚至几乎无法破解
3. 在请求头中加入referer字段

为了防范XSS攻击
1.对输入进行过滤、对输出进行转义

为了防范水平越权
1. 服务端一定要校验数据的归属

为了防范授权码失窃
1. 授权服务一定要对重定向URI进行完整性校验
2. 授权码只能使用一次，使用完毕立马失效
3. 授权服务一定要对appId进行校验
</div>2023-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/1c/b39d7fe2.jpg" width="30px"><span>꧁平常心꧂</span> 👍（0） 💬（1）<div>老师你好，我始终有一个盲点没想通，

OIDC场景下：

1 受保护的资源服务，要如何去鉴权？
2 我猜是在认证服务器中对access token做非对称加密处理，不知道想的对不对？ 
3 如果受保护资源服务器，使用非对称或者对称加密去和认证中心去鉴权，那么密钥在什么时候进行传输比较合适？</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>OAuth 2.0 是一个授权协议，它通过访问令牌来表示这种授权。第三软件拿到访问令牌之后，就可以使用访问令牌来代表用户去访问用户的数据了。所以，我们说授权的核心就是获取访问令牌和使用访问令牌。OAuth 2.0 是一个安全协议，但是如果你使用不当，它并不能保证一定是安全的。如果你不按照 OAuth 2.0 规范中的建议来实施，就会有安全风险。比如，你没有遵循授权服务中的授权码只能使用一次、第三方软件的重定向 URL 要精确匹配等建议。安全防护的过程一直都是“魔高一尺道高一丈”，相互攀升的过程。因此，在使用 OAuth 2.0 的过程中，第三方软件和平台方都要有足够的安全意识，来把“安全的墙”筑得更高。</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（0）<div>思考题，1 熟悉平台方的说明文档；2 掌握网络安全的基础知识；3 定期关注网络安全的最新动态。</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（0） 💬（0）<div>按照协议来开发，还有提供一个监控系统监控，时刻注意，纠正</div>2020-07-21</li><br/>
</ul>