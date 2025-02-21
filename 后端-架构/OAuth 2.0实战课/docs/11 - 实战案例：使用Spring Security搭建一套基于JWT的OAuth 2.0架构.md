你好，我朱晔，是[《Java业务开发常见错误100例》](https://time.geekbang.org/column/intro/294)专栏课程的作者。

《OAuth 2.0实战课》上线之后，我也第一时间关注了这门课。在开篇词中，我看到有一些同学留言问道：“如何使用Spring Security来实现OAuth 2.0？”这时，我想到之前自己写过一篇相关的文章，于是就直接在开篇词下留了言。后面我很快收到了不少用户的点赞和肯定，紧接着极客时间编辑也邀请我从自己的角度为专栏写篇加餐。好吧，功不唐捐，于是我就将之前我写的那篇老文章再次迭代、整理为今天的这一讲内容，希望可以帮助你掌握OAuth 2.0。

如果你熟悉Spring Security的话，肯定知道它因为功能多、组件抽象程度高、配置方式多样，导致了强大且复杂的特性。也因此，Spring Security的学习成本几乎是Spring家族中最高的。但不仅于此，在结合实际的复杂业务场景使用Spring Security时，我们还要去理解一些组件的工作原理和流程，不然需要自定义和扩展框架的时候就会手足无措。这就让使用Spring Security的门槛更高了。

因此，在决定使用Spring Security搭建整套安全体系（授权、认证、权限、审计）之前，我们还需要考虑的是：将来我们的业务会多复杂，徒手写一套安全体系来得划算，还是使用Spring Security更好？我相信，这也是王老师给出课程配套代码中，并没有使用Spring Security来演示OAuth 2.0流程的原因之一。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/fe/874b172b.jpg" width="30px"><span>benxiong</span> 👍（2） 💬（2）<div>创建表的时候报错了：
CREATE TABLE `oauth_client_details` (
  `client_id` varchar(255) NOT NULL,
  `resource_ids` varchar(255) DEFAULT NULL,
  `client_secret` varchar(255) DEFAULT NULL,
  `scope` varchar(255) DEFAULT NULL,
  `authorized_grant_types` varchar(255) DEFAULT NULL,
  `web_server_redirect_uri` varchar(255) DEFAULT NULL,
  `authorities` varchar(255) DEFAULT NULL,
  `access_token_validity` int(11) DEFAULT NULL,
  `refresh_token_validity` int(11) DEFAULT NULL,
  `additional_information` varchar(255) DEFAULT NULL,
  `autoapprove` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
&gt; 1071 - Specified key was too long; max key length is 767 bytes
&gt; 时间: 0s

网上说是 mysql innodb存储引擎 的 varchar 主键只支持不超过767个字节 或者 768&#47;2=384个双字节 或者767&#47;3=255个三字节 或者 767&#47;4=191个四字节的字段，GBK是双字节的，UTF8是三字节的，utf8mb4是四字节的，我按照这个说法，把主键 client_id 字段长度改为 VARCHAR(111)，就创建成功了。

但是我是很信服朱晔老师的，他非常严谨，他肯定是测试通过以后才发表的文章，所以我觉得应该还有别的原因导致他可以创建，而我却报错。

这个原因期待老师和别的小伙伴帮忙解答。</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b2/87/833d9bb6.jpg" width="30px"><span>布吉岛</span> 👍（1） 💬（1）<div>csrf攻击不讲嘛？</div>2020-08-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mZrw2nVk1Aw8eYh5GPWpI9OHVBhXdFpMZx9mDyAHJuSZlpXCfKcOUxSUTewtibW8KBb0d9ftNl9F0n6ptudxBwQ/132" width="30px"><span>Geek_fb74a8</span> 👍（1） 💬（3）<div>请教一下老师，使用jwt的话应该怎么处理过期以及登出等处理？可否将jwt令牌存入Redis？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/88/23/a0966b4d.jpg" width="30px"><span>Tim Zhang</span> 👍（1） 💬（1）<div>有个问题，请指教：
我的需求是想开发一个统一认证平台，公司内所有应用需要认证，资源权限管控的都走这个应用

用户首先访问a应用的某个webapi(受保护应用)，a应用发现token不存在，跳转到我的统一认证授权中心的登录界面，选择使用微信进行认证，认证成功后，根据我的数据库中的rbac表，查询这个用户在a应用的权限与角色，生成token，将token返回给受保护资源的应用a，然后a应用进行验证。

我的问题如下：
1、那些刷新accesstoken，refrshtoken过期的重新跳转的逻辑，是否只能写在不同a、b、c、d这些受保护资源应用的filter逻辑中

2、比如公司有100个应用需要做认证授权，是否这些应用的(用户，角色，资源)表结构都维护在统一认证中心所对应的db中。

3、我看老师引用了网关，是否网关可以切面做掉点通用逻辑

4、受保护资源保护的资源(webapi)，假设是基于http rest的spring mvc编写的，是否就是那些control
ler中的路由url，在这些url之上使用切面逻辑来验证token中的资源权限是否与当前路由匹配（比如验证http方法+url路径）

5、受保护资源应用自己的数据库中假设存有用户表，是否还要与统一认证中的用户表进行实时关联，比如a应用的用户aa删除了，还需要实时删除统一认证中的aa用户在a应用中的数据

问题较多，乱，请老师抽空回复下，谢谢了</div>2020-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9c/c6/05a6798f.jpg" width="30px"><span>苗</span> 👍（10） 💬（1）<div>导出公钥证书的命令：keytool -list -rfc --keystore mytest.jks | openssl x509 -inform pem -pubkey</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/1a/389eab84.jpg" width="30px"><span>而立斋</span> 👍（6） 💬（0）<div>爱了，我要去手撸一遍，验证一下真伪。哈哈</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/30/5e/c42bc33f.jpg" width="30px"><span>Younger Ku</span> 👍（5） 💬（0）<div>能把源码带着看一遍，再把经常需要定制化的地方讲一下就好了。无论如何只停留在demo使用层面总感觉心里不踏实。</div>2020-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/00/7ba54f5c.jpg" width="30px"><span>行一善</span> 👍（2） 💬（0）<div> 生成jks密钥库	生成.jks文件
 keytool -genkey -alias tutorialspedia -keyalg RSA -keystore &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;tutorialspedia.jks&quot;
  keytool -genkey -alias jwt -keyalg RSA -keystore &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;jwt.jks&quot;

 导出公共证书 .cer文件
 keytool -export -alias tutorialspedia -file &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;tutorialspedia_public_cert.cer&quot; -keystore &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;tutorialspedia.jks&quot;
  keytool -export -alias jwt -file &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;public.cert&quot; -keystore &quot;&#47;home&#47;yaoshenglu&#47;keytool&#47;jwt.jks&quot;
 
 查看公钥
 keytool -list -rfc --keystore tutorialspedia.jks | openssl x509 -inform pem -pubkey
  keytool -list -rfc --keystore jwt.jks | openssl x509 -inform pem -pubkey</div>2022-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqdH1VzVC9fJ3ZrSicnCjPXyvicYRkC3LFzVWcsjhibnAPCHBicia8Wk7J6rJfEuGGLqLV9wuWnqWuxFFQ/132" width="30px"><span>Geek_0d99c9</span> 👍（2） 💬（3）<div>代码有点问题.直接访问8082&#47; 还是被重定向到login页面.OAuth2ClientApplication这个里面的EnableOAuth2Sso注解会覆盖WebSecurityConfig里面的免登录配置.所以应该把两个合并下

package me.josephzhu.springsecurity101.cloud.auth.client;

import org.springframework.boot.autoconfigure.security.oauth2.client.EnableOAuth2Sso;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.oauth2.client.OAuth2ClientContext;
import org.springframework.security.oauth2.client.OAuth2RestTemplate;
import org.springframework.security.oauth2.client.resource.OAuth2ProtectedResourceDetails;

@EnableOAuth2Sso
@Configuration
@Order(200)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    &#47;**
     * &#47;路径和&#47;login路径允许访问，其它路径需要身份认证后才能访问
     *
     * @param http
     * @throws Exception
     *&#47;
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .authorizeRequests()
                .antMatchers(&quot;&#47;test&quot;,&quot;&#47;&quot;, &quot;&#47;login**&quot;,&quot;&#47;**&#47;test&quot;,&quot;&#47;ui&#47;test&quot;, &quot;&#47;logout&quot;)
                .permitAll()
                .anyRequest()
                .authenticated().and()
                .logout().logoutSuccessUrl(&quot;&#47;&quot;);;
    }

      @Bean
  public OAuth2RestTemplate oauth2RestTemplate(OAuth2ClientContext oAuth2ClientContext,
                                               OAuth2ProtectedResourceDetails details) {
  return new OAuth2RestTemplate(details, oAuth2ClientContext);
  }

}

</div>2020-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ec/cd/52753b9e.jpg" width="30px"><span>Anony</span> 👍（2） 💬（1）<div>客户端使用了@EnableOAuth2Sso，里面包含自己的WebSecurity会拦截所有请求。而后自己定义的WebSecurity，Order是200，实际上是不起作用的吧，即使让某些url permitAll，也会直接跳转到授权服务器的登录页。请求都会直接被靠前的EnableOAuth2Sso里的过滤链处理 。</div>2020-12-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrqLEic7DVicYY1s9ldH0vGBialDoplVGpicZUJ0Fdaklw27Frv8Ac67eicb5LibhL74SUxAzlick2nfltA/132" width="30px"><span>jiangb</span> 👍（1） 💬（0）<div>实操了一遍，运行OK。</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f3/0b/0128ae45.jpg" width="30px"><span>工资不交税</span> 👍（1） 💬（2）<div>对于sso的实现还是不理解。看起来全程没有用到cookie，那授权服务是如何知道来自两个域名的请求是同一个用户？</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/ce/53392e44.jpg" width="30px"><span>BingoJ</span> 👍（0） 💬（0）<div>一直报这个错，
生成jks和公钥的命令如下，也不知道哪里不对
   keytool -genkeypair -alias jwt -keyalg RSA -keysize 2048 -validity 365 -keystore jwt.jks
    keytool -exportcert -alias jwt -file public.cert -keystore jwt.jks -rfc

Caused by: java.lang.IllegalStateException: For MAC signing you do not need to specify the verifier key separately, and if you do it must match the signing key
	at org.springframework.util.Assert.state(Assert.java:73) ~[spring-core-5.2.1.RELEASE.jar:5.2.1.RELEASE]
	at org.springframework.security.oauth2.provider.token.store.JwtAccessTokenConverter.afterPropertiesSet(JwtAccessTokenConverter.java:318) ~[spring-security-oauth2-2.3.4.RELEASE.jar:na]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.invokeInitMethods(AbstractAutowireCapableBeanFactory.java:1862) ~[spring-beans-5.2.1.RELEASE.jar:5.2.1.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1799) ~[spring-beans-5.2.1.RELEASE.jar:5.2.1.RELEASE]
	... 53 common frames omitted
</div>2024-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/f9/31/b75cc6d5.jpg" width="30px"><span>ξ！</span> 👍（0） 💬（0）<div>可不可以出一期加餐security6.0的版本啊</div>2024-06-19</li><br/><li><img src="" width="30px"><span>Geek_4b4d7b</span> 👍（0） 💬（0）<div>老师好，请教下单点登录为啥会有http:&#47;&#47;localhost:8083&#47;ui&#47;login的访问地址，登录页面不是在认证服务8080上吗？</div>2022-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/39/93/914db62f.jpg" width="30px"><span>孩童的心，永远在迷失</span> 👍（0） 💬（0）<div>客户端端口是先设置为8082，测试完8082，又改为8083。菜鸡的我一开始没注意，还奇怪8082端口为啥没跳转login成功。</div>2022-03-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK5dh80UCnDwic7jHWRGVMbqFBjFbBAKO4bqzB5Sr39iaib5JPmF3d06dV1ibXHflNdQKgcKBsEkfXc6g/132" width="30px"><span>Geek_16e01a</span> 👍（0） 💬（0）<div>老师您好，下面是我在你的课件中看到的两句话：
“首先，Token 可以保存在数据库或 Redis 中，资源服务器和授权服务器共享底层的 TokenStore 来验证；然后，资源服务器可以使用 RemoteTokenServices，来从授权服务器的 &#47;oauth&#47;check_token 端点进行 Token 校验。”
我在实践中发现，只要共享tokenStore共享同一个jdbc的数据源，那么在我并没有配置RemoteTokenService的情况下，token也是能被校验的。就是说我传错误的token会被识别出来是invalid的。请问老师，这个是什么情况，我不是很清楚，是否有什么默认的配置</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/5c/13/d1a75b2e.jpg" width="30px"><span>ascend</span> 👍（0） 💬（0）<div>前后端分离的情况下，oauth2的认证流程怎么走呢</div>2022-03-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK5dh80UCnDwic7jHWRGVMbqFBjFbBAKO4bqzB5Sr39iaib5JPmF3d06dV1ibXHflNdQKgcKBsEkfXc6g/132" width="30px"><span>Geek_16e01a</span> 👍（0） 💬（0）<div>老师，我再使用客户端使用这个方法的时候    public OAuth2RestTemplate oauth2RestTemplate(OAuth2ClientContext oAuth2ClientContext, OAuth2ProtectedResourceDetails details)   代码里会报这个错误Could not autowire. There is more than one bean of &#39;OAuth2ClientContext&#39; type.
您遇到过这个问题么，该怎么解决</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/37/7e/219dd994.jpg" width="30px"><span>liuyong</span> 👍（0） 💬（1）<div>现在Spring OAuth2已经被标记为deprecate了，新系统应该不推荐继续用这个了吧？</div>2021-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ojfRyNRvy1x3Mia0nssz6CNPHrHXwPPmibvds1URgoHQuKXrGiaxrEbsT6sAvuK4N4AOicySh8S9iaWcOLjteOl6Kgg/132" width="30px"><span>泥鳅儿</span> 👍（0） 💬（1）<div>老师你好，oauth2.0客户端如何自动注册呢 ？oauth_client_details这个表里的数据怎么新增的 是手动往里加记录吗</div>2021-07-03</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er8I0UfHsvn66T1BxW7sniaWXpTLqQ5X2qNlwuEWFfw9666dt1kAKmoScgRkjGfbRIpbDXY5dgEAnw/132" width="30px"><span>Geek_9f3b9b</span> 👍（0） 💬（0）<div>github取不到代码了</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c0/09/f1280359.jpg" width="30px"><span>达尼亚尔</span> 👍（0） 💬（3）<div>老师，您好！ 您是怎么用keytool生成的秘钥对？我生成秘钥对在受保护服务启动的过程中报错了，但是授权服务中正常。能把keytool的使用方法讲一下吗？谢谢！！
以下是报错信息：
 For MAC signing you do not need to specify the verifier key separately, and if you do it must match the signing key</div>2021-04-28</li><br/><li><img src="" width="30px"><span>杨毅</span> 👍（0） 💬（0）<div>老师您好， 这块的sso如果是基于多个不同的一级域名还好使吗？ 如果不好使大致要怎么做啊</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（0） 💬（0）<div>老师，你好.
这篇案例的sso实现，不是基于oidc实现的啊？还是底层屏蔽ID令牌的细节？</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/13/5197f8d2.jpg" width="30px"><span>永旭</span> 👍（0） 💬（1）<div>老师你好. 
我生成了私钥库 jks文件, 使用命令只能导出cer, crt文件 . 通过-rfc查询后放到cert文件里还是报错.
能说下使用keytool生成cert文件的命令吗 ? 
非常感谢</div>2020-11-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIq15Qq887bH7Z5aQHfXu5vHUj4Iz68RotmUIR12vG5Y3L7icUcYgL4hicwAKYyicAmPTtoZPNPfDPOg/132" width="30px"><span>流云</span> 👍（0） 💬（0）<div>请教老师，公司内部系统登录怎么对接oauth平台呢？还是要单独做一套登录系统比价合适，希望老师能够指导一下，感谢</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/ca/cbce6e94.jpg" width="30px"><span>梦想的优惠券</span> 👍（0） 💬（0）<div>老师，我在验证授权码许可类型的时候，授权服务器不返回Code，表oauth_code也没写进去值，页面跳转后返回的是【https:&#47;&#47;www.baidu.com&#47;?error=access_denied&amp;error_description=User%20denied%20access】</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（0） 💬（0）<div>向老师请教 资源拥有者凭据许可 模式，也就是俗称的 密码 模式；主要是提供给第一方的客户端使用的模式。
这种情况下，使用的是 资源拥有者（也就是用户）的【用户名】+【密码】+【客户端id】+【客户端Secret】来获取token。
客户端的id和Secret应该是不能存放在页面应用中的吧》？感觉会不安全。

我看到的其他的文章和博客，描述的意思大概是： 用户把自己的用户名和密码告诉客户端，客户端再带着自己的 客户端ic和Secret 向授权服务器交换用户的token。把token返给用户后，用户再带着token请求自己的资源。请问是这样嘛？如果是这样，实际客户端时如何向授权服务交换用户token的呢？查阅多个博客，文档的demo，样例都是使用postman，输入 客户端id+Secret+用户名+密码 直接请求tokne的。。。</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/82/a1/76878dc5.jpg" width="30px"><span>十九路军</span> 👍（0） 💬（0）<div>微服务架构中，一般都有网关，请问你这个资源服务器，应该搭建在哪里呢</div>2020-09-16</li><br/>
</ul>