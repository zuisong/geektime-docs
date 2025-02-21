你好，我是姚秋辰。

在上节课中，我们了解了Spring Cloud Gateway网关在微服务架构中的定位，我还介绍了Gateway的三大核心组件路由、谓词和过滤器的基本概念。今天，我们就来进一步认识Gateway的内置功能，了解在Gateway中如何声明一个路由，以及路由中的谓词判断逻辑有什么作用。

Spring Cloud Gateway（以下简称Gateway）提供了非常丰富的内置谓词，你可以通过内置谓词来构建复杂的路由条件，甚至连“整点秒杀”这个场景都能在网关层做控制。这些内置谓词就像乐高积木一样，你可以随意组合在自己的业务逻辑中，构建五花八门的网关层判断逻辑。如果这还不够，那么Gateway还提供了自定义的谓词工厂扩展点，让你构建自定义谓词。

由于这些个谓词都要附着于一个路由之上，所以在介绍谓词之前，我得先和你聊一下怎么声明一个路由。这一节不涉及微服务项目改造，只是让你能够用最直观的方式体验Gateway的功能特点。

## 声明路由的几种方式

在上一节中我们讲到，路由是Gateway中的一条基本转发规则。网关在启动的时候，必须将这些路由规则加载到上下文中，它才能正确处理服务转发请求。那么网关可以从哪些地方加载路由呢？
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（7） 💬（1）<div>请教老师几个问题啊：
Q1：SpringCloud Gateway和zuul相比哪个更好
Q2：Gateway只对用户的请求起作用吗？对微服务之间的请求起作用吗？
Q3：gateway路由的具体效果是什么？
比如这个路由：
.path(&quot;&#47;geekbang&#47;**&quot;)
.uri(&quot;http:&#47;&#47;time.geekbang.org&quot;)
其最终效果是什么？
是说请求的开头是“http:&#47;&#47;time.geekbang.org”，后面只要跟的是“&#47;geekbang&#47;**”就允许通过吗？ 即完整的请求是“http:&#47;&#47;time.geekbang.org&#47;geekbang&#47;**”。
Q4：gateway路由信息中没有微服务的信息？
比如这个路由：
.path(&quot;&#47;geekbang&#47;**&quot;)
.uri(&quot;http:&#47;&#47;time.geekbang.org&quot;)
Gateway的目的是将请求路由到某一个微服务，但这个路由中并没有微服务的信息啊。
Q5：actuator是SpringCloud的一个组件吗？
Q6：声明路由的三种方式会混合使用吗？
Q7：Nginx和Gateway可以合二为一吗？
情况1：去掉gateway，只有nginx，用户请求直接到nginx，nginx直接到微服务；情况2：去掉nginx，只有gateway，用户请求直接到gateway，gateway再到微服务。</div>2022-02-09</li><br/><li><img src="" width="30px"><span>hhhhhh</span> 👍（2） 💬（1）<div>微服务网关的作用，就是整合各个微服务功能，形成一套或多套系统  看了半天感觉好像是这意思</div>2022-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/60/1b/37a1eb91.jpg" width="30px"><span>威威威小哥</span> 👍（2） 💬（1）<div>老师，几个问题请教下
1. Gateway 转发到目标服务是重新发起一次http请求吗？
2. Gateway有没有类似舱壁模式， 如何防止一个下游服务不可用导致整个gateway雪崩？
3. 哪里可以学习gateway的内部细节？</div>2022-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/e3/9f3077f3.jpg" width="30px"><span>Charles</span> 👍（1） 💬（1）<div>请教老师，是否推荐使用谓词实现金丝雀测试方案?</div>2022-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ed/c5/0d908da3.jpg" width="30px"><span>微笑的起点</span> 👍（0） 💬（1）<div>老师，请教个问题，springcloudgateway配置几个路由来测试，每个路由地址首次访问都要比后面多将近500ms，调试发现某些filter耗时比较多，每个地址第二次访问都会快很多，这是什么原因呢</div>2023-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/8b/74d2ab6b.jpg" width="30px"><span>斜杠青年</span> 👍（0） 💬（2）<div>老师你好，我一直有一个疑问，nginx、gateWay、FeignClient 他们三者之间的分工怎么洋才是合理的，例如服务A于服务B之间的调用才用 Feign 进行 LB，还是A调用gateway 来进行转发合适？  </div>2022-12-12</li><br/><li><img src="" width="30px"><span>Geek_1aaf73</span> 👍（0） 💬（1）<div>请问下 半仙，

我们现在的架构是阿里云SLB--&gt;NGINX---&gt;微服务，缺少API网关，
我们这里准备开发自己的API网关，然后链路请求是阿里云SLB--&gt;API网关--&gt;微服务，请问这个架构是否OK？

相当于API网关替代的NGINX，API网关中包含了负载均衡，还可以配置限流、鉴权、路由等，希望这个条没理解错，求回复~</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/96/b3/942aaf99.jpg" width="30px"><span>swagger～</span> 👍（0） 💬（1）<div>请问老师同时满足两个路由是用order设置优先级吗</div>2022-02-22</li><br/>
</ul>