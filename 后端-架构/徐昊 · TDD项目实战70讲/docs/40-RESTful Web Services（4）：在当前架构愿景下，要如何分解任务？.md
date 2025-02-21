你好，我是徐昊。今天我们继续使用TDD的方式实现RESTful Web Services。

现在请回想一下TDD的流程（参看[第11讲](https://time.geekbang.org/column/article/496703)）：

![](https://static001.geekbang.org/resource/image/d0/3a/d0f2ee19dba1881d14013930de7c173a.jpg?wh=8000x4500)

目前的架构愿景如下：

![](https://static001.geekbang.org/resource/image/b8/c4/b889c031c6dff9254522928cc50856c4.jpg?wh=2284x1315)  
![](https://static001.geekbang.org/resource/image/cc/97/cc54561589ff2ab51df4150fed195997.jpg?wh=8000x4500)

## 将需求分解为任务列表

JAX-RS的需求非常庞杂，根据前面我们介绍过的部分（参看第36讲），主要的功能有这样几个方面：

- 将请求派分给对应的资源（Resource），并根据返回的状态、超媒体类型、内容，响应Http请求。
- 在处理请求派分时，可以支持多级子资源（Sub-Resource）。
- 在处理请求派分时，可以根据客户端提供的超媒体类型，选择对应的资源方法（Resource Method）。
- 在处理请求派分时，可以根据客户端提供的Http方法，选择对应的资源方法。
- 资源方法可以返回Java对象，由Runtime自行推断正确的返回状态。
- 资源方法可以不明确指定返回的超媒体类型，由Runtime自行推断。比如资源方法标注了Produces，那么就使用标注提供的超媒体类型等。
- 可通过扩展点MessageBodyWriter处理不同类型的返回内容。
- 当资源方法抛出异常时，根据异常影响Http请求。
- 可通过扩展点ExceptionMapper处理不同类型的异常。
- 资源方法可按照期望的类型，访问Http请求的内容。
- 可通过扩展点MessageBodyReader处理不同类型的请求内容。
- 资源对象和资源方法可接受环境组件的注入。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/2d/93/0f1cbf44.jpg" width="30px"><span>枫中的刀剑</span> 👍（3） 💬（0）<div>缺少两个依赖
    implementation(&quot;org.slf4j:slf4j-api:2.0.0-alpha7&quot;)
    implementation(&quot;org.slf4j:slf4j-simple:2.0.0-alpha7&quot;)
不然在视频最后那几个因缺少stub的报错无法出现。

</div>2022-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（0）<div>你是怎么理解任务分解的？

将抽象的任务不断具体化，直到可以编码实现。
例如：用户登录是一个抽象的任务。
第一步可以分解为通过手机短信、微信、微博登录；
第二步再对上面步骤中的每个任务进行分解，例如：手机短信登陆需要获得手机号码、生成验证码、发送验证码
以此类推直到消除抽象，实现愿望

代码 https:&#47;&#47;github.com&#47;wyyl1&#47;geektime-tdd-framework&#47;tree&#47;4</div>2022-06-17</li><br/>
</ul>