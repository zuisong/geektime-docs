你好，我是王新栋。

从6月29日这门课上线，到现在已经过去一个多月了。我看到了很多同学的留言，有思考，也有提出的问题。那我首先，在这里要感谢你对咱们这门课的支持、鼓励和反馈。

在回复你们的留言时，我也把你们提出的问题记了下来。在梳理今天这期答疑的时候，我又从头到尾看了一遍这些问题，也进一步思考了每个问题背后的元认知，最后我归纳出了6个问题：

1. 发明 OAuth 的目的到底是什么？
2. OAuth 2.0 是身份认证协议吗？
3. 有了刷新令牌，是不是就可以让访问令牌一直有效了？
4. 使用了HTTPS，是不是就能确保JWT格式令牌的数据安全？
5. ID令牌和访问令牌之间有联系吗？
6. PKCE协议到底解决的是什么问题？

接下来，我们就一一看看这些问题吧。

## 发明 OAuth 的目的到底是什么？

OAuth 协议的设计初衷，就是让最终用户也就是资源拥有者（小明），将他们在受保护资源服务器（京东商家开放平台）上的部分权限（查询当天订单）**委托**给第三方应用（小兔打单软件），使得第三方应用（小兔）能够代表最终用户（小明）执行操作（查询当天订单）。

这便是OAuth 协议设计的目的。在OAuth 协议中，通过为**每个第三方软件和每个用户的组合**分别生成对受保护资源具有**受限的访问权限的凭据，也就是访问令牌**，来代替之前的用户名和密码。**而生成访问令牌之前的登录操作，又是在用户跟平台之间进行的，第三方软件根本无从得知用户的任何信息。**
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkeOAC8k7aPMfQZ4ickiavpfR9mTQs1wGhGtIicotzAoszE5qkLfFTabkDU2E39ovSgoibJ1IiaLXtGicg/132" width="30px"><span>bigben</span> 👍（5） 💬（2）<div>“尽管生成了新的刷新令牌，但它的有效期不会改变，有效期的时间戳仍然是上一个刷新令牌的。刷新令牌的有效期到了，就不能再继续用它来申请新的访问令牌了。”
我所见到的开放平台新的刷新令牌的有效期都是重新开始算的啊，并不是从第一个刷新令牌产生的时候算起的啊？</div>2020-08-26</li><br/><li><img src="" width="30px"><span>Geek_bb8d16</span> 👍（4） 💬（2）<div>第三方登陆，比如微信登陆这个就很迷惑，这个是用OAuth2来实现登陆流程</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/12/73/349124f5.jpg" width="30px"><span>秋千岁</span> 👍（2） 💬（1）<div>如果用户注销或者退出了登录，ID 令牌的生命周期就随之结束了。老师，请问这句话怎么理解？已经派发出去的ID令牌 如何使得用户注销或退出登录 失效呢？</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（2）<div> ID 令牌要能够被解析 : 这句话要怎么理解的？ ID 要怎么进行解析呢？ </div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/92/fa/25b63c06.jpg" width="30px"><span>.</span> 👍（5） 💬（0）<div>您好，oauth2.0用来授权不是认证，但是springsecurity oauth2里面的实现有一个check_token接口，传入access_token会返回userinfo信息，是不是可以用来认证了，不需要ID_token。。。</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3c/7e/5e115510.jpg" width="30px"><span>Mr_Bangb</span> 👍（0） 💬（0）<div>用jwt生成令牌发现CPU高负荷运转了 请问有解吗？</div>2022-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/54/30/5f146e1b.jpg" width="30px"><span>garyhimself</span> 👍（0） 💬（0）<div>小兔打单软件获取到access_token，也不能直接调用打单api去打单吧，小兔打单软件至少得知道小明的用户信息，知道是要给小明打单吧，否则怎么调用打单api？</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/a8/6766847a.jpg" width="30px"><span>Blue</span> 👍（0） 💬（0）<div>刷新令牌，access_token在有效期之内和有效期之外，这两种情况下去刷新令牌，access_token会变化么【比较疑惑】，另外，如果access_token变化了，我们该如何告知调用方</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/a8/dfe4cade.jpg" width="30px"><span>电光火石</span> 👍（0） 💬（0）<div>“尽管生成了新的刷新令牌，但它的有效期不会改变，有效期的时间戳仍然是上一个刷新令牌的。刷新令牌的有效期到了，就不能再继续用它来申请新的访问令牌了。”
既然可以用刷新令牌在有效期内重新申请访问令牌，这么做是否可以：只用访问令牌，不用刷新令牌，访问令牌的有效期和之前刷新令牌的有效期一样，这样是否可以呢？会有什么安全隐患吗？谢谢老师。</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/03/f753fda7.jpg" width="30px"><span>JianXu</span> 👍（0） 💬（0）<div>“第三，在使用上，刷新令牌只能用在授权服务上，而访问令牌只能用在受保护资源服务上。” — 如果我有需要在平台一侧把access token 发到授权服务上，会有什么风险吗？</div>2020-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK4ibibOsboHycltqqicSIkm9eibSBu86BRNc0LQnTRTMEPGDvJXYpBicWOW4srMt7c9iaUT7b5mTmicgkjw/132" width="30px"><span>Geek_6a58c7</span> 👍（0） 💬（0）<div>老师你好，可以说说刷新令牌使用流程吗?生成的新令牌怎么传回给第三方?</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/11/7198f98e.jpg" width="30px"><span>龙堂修罗</span> 👍（0） 💬（1）<div>如果刷新令牌是有时间限制的话，那就不能无限制的保证访问令牌有效了吧。客户端访问失效是迟早的事。
那还不还得让用户再次授权么</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（0） 💬（0）<div>能借问下吗？像雪花算法之类的，不一定是顺序插入吧？有可能先申请的反而后面才插入。这样的话插入性能鬼扯uuid好？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/c9/1361a7ba.jpg" width="30px"><span>陶陶</span> 👍（0） 💬（7）<div>没理解OIDC的使用场景是什么？因为就算没有id令牌，直接使用访问令牌也是可以通过请求用户信息接口获取当前登录人信息的</div>2020-07-30</li><br/>
</ul>