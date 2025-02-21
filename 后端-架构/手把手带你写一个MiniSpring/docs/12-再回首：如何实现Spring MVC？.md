你好，我是郭屹。

恭喜你学完MiniSpring的第二部分——MVC了。你是不是跟着我的脚步自己也实现了一个MVC呢？如果已经完成了，欢迎你把你的实现代码放到评论区，我们一起交流讨论。

为了让你更好地掌握这部分内容，我们来对这一整章做一个重点回顾。

### MVC重点回顾

MVC是Spring框架的核心组成部分之一，负责实现一个Web应用程序的模型视图控制器模式。Spring框架提供了丰富的组件和工具，而MVC负责处理一个Web应用程序中的核心过程，例如请求处理、数据转换、模板渲染和视图管理等。而MVC和Spring的结合，就像是车与引擎的结合一样，给Web应用程序提供了强大而且可靠的性能和灵活性，让我们能够快速、方便地搭建高性能、可靠的Web应用程序。

因为Spring是Java实现的，也因为发明人Rod Johnson先生自己是Java团队Servlet规范的专家组成员，所以很自然，他的MVC的实现是基于Servlet的。利用Servlet的机制，把这种功效发挥到了极致，快速构造了完整的Web程序结构，让我们大开眼界。

### 那我们在课程中是怎么实现MVC的呢？

首先我们利用Servlet机制，用一个单一的Servlet拦截所有请求，由它来分派任务，这样实现了原始的MVC结构。然后呢，我们把MVC和IoC结合在一起，在Servlet容器启动的时候，给上下文环境里注入IoC容器，使得在Servlet里可以访问到IoC容器里的Bean。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XWv3mvIFORNgRk9wF8QLb9aXfh1Uz1hADtUmlFwQJVxIzhBf8HWc4QqU7iaTzj8wB5p5QJLRAvlQNrOqXtrg1Og/132" width="30px"><span>Geek_320730</span> 👍（4） 💬（1）<div>https:&#47;&#47;github.com&#47;kuifir&#47;practice&#47;tree&#47;master&#47;miniSpring 跟着老师每节课程跟着学完都很有收获，完成一个课程的内容并且测试成功后也很有成就感。</div>2023-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/SGicbDM2syIuJKTOkQqboZGD5E0UzhZpbbwOceWg4ZJwS6sR1Uyapo1L0wBZqf9cYiaFrniaSQ4bhAq1QLQDzPvTQ/132" width="30px"><span>欧阳利</span> 👍（1） 💬（1）<div>怎么感觉越到后面，内容越简单了</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（2）<div>请教老师几个问题：
Q1：SpringMVC与Spring是什么关系？
SpringMVC是Spring的一个子模块或子组件吗？或者两者不是包含关系，是平等、相互独立的两个东西？
Q2：SpringMVC是基于servlet，可以基于其他的吗？
Q3：SpringMVC需要依赖于一个容器，比如tomcat，但spring不需要依赖tomcat，是这样吗？
Q4：servlet具体是一个进程还是一个线程？ Redis速度快，因为是单线程，现在servlet处理全部请求，是不是类似于redis的单线程？
Q5：前后盾分离开发，前端用vue，应该会有一个“vue引擎”一类的东西。前端开发完成后，页面会打包放到后端idea项目中，那么，此时，后端会有一个“vue引擎”吗？
Q6：wac访问不到servlet，是不需要吗？还是技术上不可行？可以把wac放到ServletContext中，为什么不可以把DispatchServlet放到wac中？</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/44/93/2d3d5868.jpg" width="30px"><span>Jay</span> 👍（0） 💬（1）<div>请教老师，有个问题一直没想明白，RequestMappingHandlerMapping和RequestMappingHandlerAdapter都是配置在applicationContext.xml里面由IOC容器管理的，DispatcherServlet中通过wac.getBean()方法获取，这一步没有问题。但是，RequestMappingHandlerMapping依赖的WebApplicationContext必须是MVC容器（initMapping方法中需要获取MVC容器中维护的controllerNames），我一直没有看到RequestMappingHandlerMapping依赖的这个wac是如何注入的。master代码里面实现了ApplicationContextAware接口，但是我想即便实现了这里也只能得到IOC容器对应的ApplicationContext，好像依然不能解决这个问题？不知道到我理解的有没有问题？</div>2023-04-07</li><br/>
</ul>