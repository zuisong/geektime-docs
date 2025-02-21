你好，我是王新栋。

在[第3讲](https://time.geekbang.org/column/article/257101)，我已经讲了授权服务的流程，如果你还记得的话，当时我特意强调了一点，就是**授权服务将OAuth 2.0的复杂性都揽在了自己身上**，这也是授权服务为什么是OAuth 2.0体系的核心的原因之一。

虽然授权服务做了大部分工作，但是呢，在OAuth 2.0的体系里面，除了资源拥有者是作为用户参与，还有另外两个系统角色，也就是第三方软件和受保护资源服务。那么今天这一讲，我们就站在这两个角色的角度，看看它们应该做哪些工作，才能接入到OAuth 2.0的体系里面呢？

现在，就让我们来看看，作为第三方软件的小兔和京东的受保护资源服务，具体需要着重处理哪些工作吧。

> 注：另外说明一点，为了脱敏的需要，在下面的讲述中，我只是把京东商家开放平台作为一个角色使用，以便有场景感，来帮助你理解。

## 构建第三方软件应用

我们先来思考一下：如果要基于京东商家开放平台构建一个小兔打单软件的应用，小兔软件的研发人员应该做哪些工作？

是不是要到京东商家开放平台申请注册为开发者，在成为开发者以后再创建一个应用，之后我们就开始开发了，对吧？没错，一定是这样的流程。那么，开发第三方软件应用的过程中，我们需要重点关注哪些内容呢？

我先来和你总结下，这些内容包括4部分，分别是：**注册信息、引导授权、使用访问令牌、使用刷新令牌。**
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（8） 💬（2）<div>刷新令牌是一次性的，使用之后就会失效
----------------------
在获取访问令牌的时候同时也会把 刷新令牌 返回， 后面可以使用 刷新令牌 重新获取访问令牌，然后也会同时获取新的刷新令牌，这样的话不是可以一直获取访问令牌了吗？</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2a/a5/625c0a2e.jpg" width="30px"><span>hhhh</span> 👍（6） 💬（3）<div>“建议在平台和第三方软件约定好的前提下，优先采用 Post 表单提交的方式。”，如果这样，每个请求都需要带有token，那三方软件和开放平台只能使用post方式通信了吗？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/f3/41d5ba7d.jpg" width="30px"><span>iLeGeND</span> 👍（5） 💬（2）<div>老师以后要不要出一门spring security的课
</div>2020-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkeOAC8k7aPMfQZ4ickiavpfR9mTQs1wGhGtIicotzAoszE5qkLfFTabkDU2E39ovSgoibJ1IiaLXtGicg/132" width="30px"><span>bigben</span> 👍（3） 💬（3）<div>第三方调用授权服务也是通过api网关的吧？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4f/26/f21afb83.jpg" width="30px"><span>暖色浮余生</span> 👍（2） 💬（2）<div>Oauth2 的 scope权限检验和springsecurity的权限检验有什么区别呢，这两个不是通常放在一块么，做的东西应该差不多吧</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/a3/aee7ded7.jpg" width="30px"><span>在路上</span> 👍（1） 💬（6）<div>老师  令牌采用定时刷新的方式，令牌永远不会过期，除非用户主动操作，这样理解是都正确。</div>2020-07-19</li><br/><li><img src="" width="30px"><span>suhuijie</span> 👍（1） 💬（1）<div>对于服务市场的第三方软件，流程如何处理的，那块讲述的不清晰</div>2020-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/46/bf/87a57b8e.jpg" width="30px"><span>土豆</span> 👍（0） 💬（1）<div>老师我想请下，redistoken的缺点是只能单点，不支持多点，jwt是在认证服务器加密一次，在各个资源服务器随时解密，没有失效时间，如果配置多资源服务器，是不是要考虑私钥的区分，两个都有缺点，现在主流的使用方式是哪种，希望老师解惑</div>2020-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dc/71/859a59d5.jpg" width="30px"><span>hom</span> 👍（0） 💬（1）<div>请问下老师：刷新令牌的作用是什么？为什么不直接延长访问令牌的初始化时效，而是需要去手工刷新呢？  </div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/af/1cb42cd3.jpg" width="30px"><span>马以</span> 👍（19） 💬（1）<div>思考题：方法1：根据服务的响应时间，两个access_token要有一个重叠窗口期，过了重叠窗口期，旧的token就失效了；方法2：或者说和mysql数据库事务控制一样，在用refresh_token 换取 access_token 这里记录一个节点（水位线）；如果请求在这个节点之前，那么就的token就还有效，如果请求在这个节点之后，旧的token就失效；</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/7e/fb725950.jpg" width="30px"><span>罗 乾 林</span> 👍（4） 💬（0）<div>课后题：
access_token失效后请求必定失败，比较本地access_token是否更新或是否正在刷新access_token,若已更新，采用新的access_token 重新请求。若正在刷新将请求放入队列作为挂起任务，待access_token更新后重新发出请求</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/ff/52/cdb633a8.jpg" width="30px"><span>自在如风</span> 👍（3） 💬（0）<div>查询通过redis去查。在调用refresh接口之后,新的access_token插入到redis中,同时设置过期时间为access_token的过期时间。同时老的access_token可以重新插入redis中,设置过期时间为1min,这样应该能解决那个思考题的问题</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/a6/188817b6.jpg" width="30px"><span>郭嵩阳</span> 👍（1） 💬（0）<div>想问下老师,你们的平台是否后台持久化了access_token,如果存储数据存储选用的是那种数据库,或者建议是那种数据库,比如mongodb 或mysql 或者其他类型的数据库</div>2020-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（1） 💬（1）<div>“按照一般规则授权服务上旧的访问令牌应该要立即失效，但是如果在这之前已经有使用旧的访问令牌发出去的请求，不就受到影响了吗，这种情况下应该如何处理呢？”  这个有点类似缓存的处理机制，如果是随机字符串的访问令牌，受保护资源服务网关层，应该在缓存数据库和持久化数据库都保存该访问令牌，一旦有刷新令牌请求（授权服务通知资源层网关刷新令牌），就直接更新缓存令牌，然后记录日志，异步更新持久化数据库。
如果此时有旧的访问令牌过来，先和缓存令牌比对，缓存找不到就拒绝请求。
如果资源服务先接收旧访问令牌请求，后刷新令牌，那旧访问请求应该正常返回（也可以在返回前，再校验一次访问令牌，缓存变更就不返回结果）。

如果是JWT访问令牌，由于令牌信息不保存，第三方应用发出旧令牌和新令牌时，如果是按用户粒度的密码管理系统分配密码，资源服务需要提供密码系统获取密钥（刷新令牌时，同时刷新密钥），旧令牌会被拒绝；如果是按用户登录密码，那旧令牌只能等它自动过期了，存在新旧令牌同时存在的情况。</div>2020-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2c/7d/840cdc02.jpg" width="30px"><span>阿左不是蜗牛</span> 👍（0） 💬（0）<div>如果使用刷新令牌 refresh_token 请求回来一个新的访问令牌 access_token，按照一般规则授权服务上旧的访问令牌应该要立即失效...
------------------------------------
有个疑问，这个访问令牌前提是非结结构令牌，是存储在后端数据库或缓存中。要是像JWT这种令牌，它做不到让旧的令牌立即失效吧。</div>2022-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/5e/81/82709d6e.jpg" width="30px"><span>码小呆</span> 👍（0） 💬（0）<div>现在我们有一个这种的场景,就是不返回还有过期一分钟的token,我们这边是,在判断当前token过期时间少于等于60的时候,就用refresh_token 在重新生成一个 access_token,老的access_token 还会有一分钟存活时间,感觉是不是影响的</div>2022-10-09</li><br/><li><img src="" width="30px"><span>Geek_cha</span> 👍（0） 💬（0）<div>老师，想请教一下第三方软件获取了accesstoken之后，存在哪里。浏览器会存Accesstoken吗？
我的理解是： 因为获取accesstoken是通过后端通信获取的，那么后端应该是会存储这个accesstoken，那浏览器端也会存储吗，如果不存储的话，下一次用户通过浏览器访问第三方软件的时候，是通过什么标识让第三方软件知道他已经通过授权流程了（这个场景是在accesstoken没过期的情况下）。</div>2022-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqXSb2jAzlMM0JdTjWrNiaq2uR9eeloBYp906POddb9evmuj5f4CUoO6ge8TibibwtZicnl1sRHic9rW7g/132" width="30px"><span>紫龙</span> 👍（0） 💬（0）<div>三方应用开发者要做的注册信息、引导授权、使用访问令牌、使用刷新令牌；受保护资源最终指的还是 Web API，不同的权限会有不同的操作，不同的权限也会对应不同的数据，不同的用户也会对应不同的数据。</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f0/58/87104eab.jpg" width="30px"><span>Apologize</span> 👍（0） 💬（0）<div>我的处理方式是将所有失败的请求（因为access token失效导致）使用新的access token进行重试，理由如下：
1、请求失败是很正常的，资源服务器无法或者很困难保证请求100%正确响应，面向失败编程是一种积极应对策略。
2、基于面向失败编程的思想，即使access token没有失效请求也可能失败，只是失败的原因不同，因此请求失败重试（有条件重试）是一种可靠的编程模型。
3、既然失败需要重试，那么因为access token失效导致的失败进行重试也是比较自然的操作。
下面我可能会写的简单代码：
public class ThirdPartClient {
    private AccessTokenProvider accessTokenProvider;
    private OkHttpClient okHttpClient;

    public ThirdPartClient(AccessTokenProvider accessTokenProvider) {
        this.accessTokenProvider = accessTokenProvider;
        this.okHttpClient = new OkHttpClient.Builder()
                .addInterceptor(chain -&gt; {
                    Request request = chain.request();

                    Response response = chain.proceed(request);
                    &#47;&#47; 假设返回401表示access token失效
                    if (response.code() == 401) {
                        request = request.newBuilder()
                                .addHeader(&quot;Authorization&quot;, &quot;Bearer &quot; + accessTokenProvider.get())
                                .build();
                        return chain.proceed(request);
                    }
                    
                    return response;
                })
                .build();
    }
}</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b2/17/3161b49c.jpg" width="30px"><span>达叔灬</span> 👍（0） 💬（0）<div>针对权限校验存放网关的问题，若是采用 Authorization Request Header Field 方式使用访问令牌那么网关需要怎么处理呢？
我们现在网关只是做了验证的需求 具体的权限还是下放到了具体的API服务，不同的API 其实也是做了重复性的权限相关工作？
针对这种情况 不知道 老师 或者 同学们都是怎么处理的(net 程序员)。</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/b0/d32c895d.jpg" width="30px"><span>熊能</span> 👍（0） 💬（0）<div>思考题，最简单的方式是请求失败后的重试机制吧。</div>2021-10-31</li><br/><li><img src="" width="30px"><span>Geek_f586a6</span> 👍（0） 💬（0）<div>思考题，一般客户端会缓存accessToken，过期了就直接失败，添加重试机制机制即可。不需特别的处理。</div>2021-07-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er8I0UfHsvn66T1BxW7sniaWXpTLqQ5X2qNlwuEWFfw9666dt1kAKmoScgRkjGfbRIpbDXY5dgEAnw/132" width="30px"><span>Geek_9f3b9b</span> 👍（0） 💬（0）<div>为什么Spring cloud服务之间调用接口，没有共用到权限，加到请求头中，另一个服务验证的时候得不到请求头数据</div>2021-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（0） 💬（1）<div>请问老师
oauth2中 调动刷新令牌服务, 会发放新的访问令牌和刷新令牌, 这时刷新令牌的过期时间也是重置吗 ? 还是用原来的过期时间 ??</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/f9/6ed6cb43.jpg" width="30px"><span>zil</span> 👍（0） 💬（0）<div>在网关做校验，可以针对外部请求。

资源服务间的请求是否也需要权限校验呢？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>我在本讲开始的时候，提到 OAuth 2.0 的复杂性实际上都给了授权服务来承担，接着我从第三方软件和受保护资源的角度，分别介绍了这两部分系统在接入 OAuth 2.0 的时候应该注意哪些方面。总结下来，我其实希望你能够记住以下两点。
对于第三方软件，比如小兔打单软件来讲，它的主要目的就是获取访问令牌，使用访问令牌，这当然也是整个 OAuth 2.0 的目的，就是让第三方软件来做这两件事。在这个过程中需要强调的是，第三方软件在使用访问令牌的时候有三种方式，我们建议在平台和第三方软件约定好的前提下，优先采用 Post 表单提交的方式。
受保护资源系统，比如小兔软件要访问开放平台的订单数据服务，它需要注意的是权限的问题，这个权限范围主要包括，不同的权限会有不同的操作，不同的权限也会对应不同的数据，不同的用户也会对应不同的数据。</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（0） 💬（0）<div>“如果这时采用参数传递的方式呢，整个 URI 会被整体复制，安全性是最差的。”   这个是指access_token会整体复制到URI后面么？</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/81/2727b475.jpg" width="30px"><span>Leododo</span> 👍（0） 💬（0）<div>一般情况下，刷新token，都是因为请求返回token已经过期了，才会启动refreshtoken。授权服务一般情况下是不允许2个token同时存在的。</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/d9/3328dd12.jpg" width="30px"><span>心浮天空</span> 👍（0） 💬（0）<div>有两个问题，希望老师解答：
1. 第一次获取令牌和后续通过刷新令牌获得令牌，授权服务器都会返回访问令牌和新的刷新令牌，只要第三方应用在刷新令牌过期之前刷新令牌，就可以获得新的访问令牌和刷新令牌，所以只要第三方应用一直在运行，不断的刷新令牌，就可以无休止的拥有访问权限了？
2.课程中提到，访问令牌本身是有权限设定的(可能存储在token中，也可能存储在授权服务器中)，例如，token被授予了删除订单的权限，当第三方应用调用删除订单操作时，需要验证token是否有删除订单的权限，这个验证应该是由授权服务器验证，还是资源服务器验证？同时，除了验证是否删除订单权限外，还应该验证要删除的订单是否为token关联用户的订单，防止恶意删除其他用户的数据，这种验证应该由谁验证？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（1）<div>缩短之前access token和refresh token的超时时间为几秒，这样可以让换token失败的三方软件有机会重试。重试的时候返回上次成功的新token</div>2020-07-15</li><br/>
</ul>