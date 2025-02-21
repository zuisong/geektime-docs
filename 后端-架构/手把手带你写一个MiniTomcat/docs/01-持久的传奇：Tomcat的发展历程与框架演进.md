你好，我是郭屹，从今天开始我们来学习手写 MiniTomcat。

作为使用Java语言进行Web程序开发的人来说，对Tomcat想必是不陌生的。Tomcat是一款轻量级的Java应用服务器，最早是Sun公司在1998年开发的。当时开发Tomcat的目标是成为Sun公司的Java Servlet和JSP规范的参考实现。

如今Tomcat是业务开发首选的开源Web应用服务器，在Spring MVC项目中会把它作为程序的启动容器，甚至在Spring Boot框架中直接将Tomcat内置为Web应用的启动容器，不再需要程序开发者自行配置，进一步简化了开发门槛。可以说，虽然Tomcat不是Web服务器的唯一选择，但也和Spring一样，成为了Java开发领域事实上的标准。二十五年以来长盛不衰，在日新月异的IT领域，可谓是持久的传奇。

## 版本变化

跟任何一个成功的产品一样，Tomcat也不是一诞生就是现在这个样子的，它也是经历了逐渐完善和强大的发展历程。

![图片](https://static001.geekbang.org/resource/image/yy/ce/yy534ab3e199fe942495da89ab56bece.png?wh=1920x981 "图片源自网络")

Tomcat的发明人是James Duncan Davidson。他在1997年加入Sun公司，然后开始动手写Tomcat，这是Sun对外提供的一个Servlet容器的参考实现，后来大名鼎鼎的Spring发明人Rod Johnson也是Servlet专家组成员。1998年对外公开的时候标记为2.0版本，到了1999年，Sun公司就把它捐赠给了Apache基金会。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（2）<div>请教老师几个问题：
Q1：Tomcat为什么还支持JSP？
第01课中提到了Tomcat的发展历史，每个版本都支持JSP，包括最新的版本10。但JSP基本已经被废弃，没有人用JSP了。为什么还要支持JSP？
Q2：Tomcat中Engine只有一个实例吗？
Q3：一个context对应一个web应用，context下面有多个servlet。那么，context下面的servlet数量是怎么决定的？
Q4：端口和service对应吗？即一个端口对应一个service?
Q5：NIO实现中，为什么抛弃多个Acceptor和Poller的方案而采用单例的方案？</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（2） 💬（2）<div>🌝🌝看了本文更加期待老师的第五和第六部分， 不知道老师是否有计划，那部分也是重头戏。</div>2023-12-14</li><br/><li><img src="" width="30px"><span>Geek_50a5cc</span> 👍（1） 💬（1）<div>根据8.0的Server.xml 来看和老师讲解 的，基本上就是分为 Server,Service,Connector,Egine,Host,(Listener，Realm,Value一些小组件),Context,Servlet(Wrapper);</div>2023-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/64/62/8b20c551.jpg" width="30px"><span>Martito</span> 👍（1） 💬（1）<div>Container： 用于管理 Servlet 和 JSP 的生命周期。

Engine： Engine 是最高级别的容器，代表整个 Tomcat 服务器。一个 Tomcat 实例可以包含多个 Engine，每个 Engine 通常对应一个虚拟主机host。

Host： Host 定义了一个虚拟主机，可以包含多个 Context。

Context： Context 表示一个 Web 应用程序，每个 Context 定义了特定 Web 应用的配置信息。

Servlet：处理业务逻辑和数据存储的组件，通过 HttpServletRequest 和 HttpServletResponse 与客户端进行交互。</div>2023-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（0） 💬（3）<div>老师 希望把手写系列延续出去 之后还会手写什么中间件嘛</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ef/e8/076a6f59.jpg" width="30px"><span>张翀</span> 👍（0） 💬（1）<div>请问本系列课程会讲解Tomcat的nio实现和Apr等实现吗</div>2023-12-15</li><br/>
</ul>