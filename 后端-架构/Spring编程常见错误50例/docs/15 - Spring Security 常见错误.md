你好，我是傅健。前面几节课我们学习了 Spring Web 开发中请求的解析以及过滤器的使用。这一节课，我们接着讲 Spring Security 的应用。

实际上，在 Spring 中，对于 Security 的处理基本都是借助于过滤器来协助完成的。粗略使用起来不会太难，但是 Security 本身是个非常庞大的话题，所以这里面遇到的错误自然不会少。好在使用 Spring Security 的应用和开发者实在是太多了，以致于时至今日，也没有太多明显的坑了。

在今天的课程里，我会带着你快速学习下两个典型的错误，相信掌握它们，关于 Spring Security 的雷区你就不需要太担心了。不过需要说明的是，授权的种类千千万，这里为了让你避免纠缠于业务逻辑实现，我讲解的案例都将直接基于 Spring Boot 使用默认的 Spring Security 实现来讲解。接下来我们正式进入课程的学习。

## 案例 1：遗忘 PasswordEncoder

当我们第一次尝试使用 Spring Security 时，我们经常会忘记定义一个 PasswordEncoder。因为这在 Spring Security 旧版本中是允许的。而一旦使用了新版本，则必须要提供一个 PasswordEncoder。这里我们可以先写一个反例来感受下：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/18/8e69f7cf.jpg" width="30px"><span>一记妙蛙直拳</span> 👍（10） 💬（0）<div>当浏览器请求应用受保护的资源时，进入SecurityFilterChain过滤器链中的FilterSecurityInterceptor。由于这个请求是未鉴权的，就会抛出AccessDeniedException。后面的ExceptionTranslationFilter捕获异常后，根据配置的AuthenticationEntryPoint（大多数情况下是LoginUrlAuthenticationEntryPoint的对象）重定向到登录页面。</div>2021-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（1） 💬（0）<div>思考题：DefaultLoginPageGeneratingFilter  通过过滤器生成</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ab/1c3dc64b.jpg" width="30px"><span>夏目🐳</span> 👍（0） 💬（0）<div>对于公开的接口，怎么在Springboot3.0中设定，不需要鉴权就能访问</div>2023-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（0） 💬（0）<div>现在还是更推崇 iam oauth2 saml吧</div>2022-06-21</li><br/>
</ul>