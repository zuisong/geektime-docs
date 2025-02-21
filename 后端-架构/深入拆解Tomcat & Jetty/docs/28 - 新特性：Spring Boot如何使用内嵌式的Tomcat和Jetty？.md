为了方便开发和部署，Spring Boot在内部启动了一个嵌入式的Web容器。我们知道Tomcat和Jetty是组件化的设计，要启动Tomcat或者Jetty其实就是启动这些组件。在Tomcat独立部署的模式下，我们通过startup脚本来启动Tomcat，Tomcat中的Bootstrap和Catalina会负责初始化类加载器，并解析`server.xml`和启动这些组件。

在内嵌式的模式下，Bootstrap和Catalina的工作就由Spring Boot来做了，Spring Boot调用了Tomcat和Jetty的API来启动这些组件。那Spring Boot具体是怎么做的呢？而作为程序员，我们如何向Spring Boot中的Tomcat注册Servlet或者Filter呢？我们又如何定制内嵌式的Tomcat？今天我们就来聊聊这些话题。

## Spring Boot中Web容器相关的接口

既然要支持多种Web容器，Spring Boot对内嵌式Web容器进行了抽象，定义了**WebServer**接口：

```
public interface WebServer {
    void start() throws WebServerException;
    void stop() throws WebServerException;
    int getPort();
}
```

各种Web容器比如Tomcat和Jetty需要去实现这个接口。

Spring Boot还定义了一个工厂**ServletWebServerFactory**来创建Web容器，返回的对象就是上面提到的WebServer。
<div><strong>精选留言（26）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/eXiaOuxJ7sb9llibl0FVSZxicWXy1Ws28ONe4pbYsypZtJaFU8fjtHibjuv18nruWnAE1Eaq06libeicibcMabsP3WdtA/132" width="30px"><span>壳</span> 👍（0） 💬（0）<div>现在使用SpringMVC是不是不太这么直接使用servlet了？SpringMVC底层使用了servlet了吗？</div>2023-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（13） 💬（3）<div>老师 sprongboot 不注册servlet 给tomcat 直接用@controller 就能实现servlet功能是咋回事呀</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（11） 💬（1）<div>&quot;这段代码实现的方法返回一个 ServletRegistrationBean，并将它当作Bean 注册到 Spring 中&quot;, 这句话中“注册到Spring中” 是不是错的？  怎么会注册到Spring中？  应该是注册到tomcat servlet容器中吧。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（10） 💬（1）<div>servletContextInitializer实现该接口被spring管理，而不是被servletcontainer管理，是这个意思吗？</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/63/c5/a85ade71.jpg" width="30px"><span>刘冬</span> 👍（7） 💬（2）<div>和&quot;飞翔&quot;同问： 有@RestController，为什么还要自己去注册Servlet给Tomcat? 
我感觉老师很善于将负责的问题、长的逻辑链讲的简洁清晰，还请老师帮忙详细说明一下。
谢谢！</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e0/40/3301e490.jpg" width="30px"><span>despacito</span> 👍（5） 💬（3）<div>老师，springboot 中 getWebServer方法的实现类不仅有tomcat，还有其他web容器，比如jetty，那为什么我们在运行启动类的时候默认都是用的tomcat容器，如果我运行启动类的时候想用jetty作为应用容器，应该怎么做？</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/3b/cfdc8bf2.jpg" width="30px"><span>Royal</span> 👍（0） 💬（1）<div>您好，想请教下jetty的NetworkTrafficListener.Adapter机制，有什么博客可以推荐吗？谢谢</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5a/d9/e74791a9.jpg" width="30px"><span>雪山飞狐</span> 👍（4） 💬（0）<div>通过 ServletContextInitializer 接口可以向 Web 容器注册 Servlet，实现 ServletContextInitializer 接口的Bean被speing管理，但是在什么时机触发其onStartup()方法的呢？
谜底就是通过 Tomcat 中的 ServletContainerInitializer 接口实现者，如TomcatStarter，创建tomcat时设置了该类，在tomcat启动时会触发ServletContainerInitializer实现者的onStartup()方法，在这个方法中触发ServletContextInitializer接口的onStartup()方法，如注册DispatcherServlet。</div>2020-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/4a/1f/8e21395b.jpg" width="30px"><span>张凤霞在三门峡</span> 👍（2） 💬（1）<div>更多细节：
DispatcherServletRegistrationBean实现了ServletContextInitializer接口，它的作用就是向Tomcat注册DispatcherServlet，那它是在什么时候、如何被使用的呢？

答案：老师提到了prepareContext方法，但没展示代码内容，它调用了另一个私有方法configureContext，这个方法就包括了往tomcat的Context添加ServletContainerInitializer对象：
context.addServletContainerInitializer(starter, NO_CLASSES);
其中有上面提到的DispatcherServletRegistrationBean。</div>2020-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1b/4a/f9df2d06.jpg" width="30px"><span>蒙开强</span> 👍（2） 💬（0）<div>老师，你好，如果我不想使用内嵌的Tomcat，想用自己装的Tomcat，那需要怎么做呢</div>2019-08-15</li><br/><li><img src="" width="30px"><span>红颜铭心</span> 👍（1） 💬（0）<div>相同点：向ServletContext容器注册Servlet,Filter或EventListener
不同点：生命周期由不同的容器托管，在不同的地方调用，最终的结果都是一样。
内嵌容器不支持ServletContainerInitializer，因此不能通过spi方式加载ServletContainerInitializer，
而是用TomcatStarter的onStartup，间接启动ServletContextInitializers，来达到ServletContainerInitializer的效果。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（1） 💬（0）<div>这篇文章让人受益匪浅，读了几遍，又对着源码看了一下，并且实验了一下。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>怎么动态注册spring websocket的处理器</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>在源码中对二者的区别已经有比较明确的阐述，在ServletContextInitializer类中的注释中，有如下说明：This interface is designed to act in a similar way to ServletContainerInitializer, but have a lifecycle that&#39;s managed by Spring and not the Servlet container.</div>2022-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/0d/fc1652fe.jpg" width="30px"><span>James</span> 👍（0） 💬（0）<div>ServletContainerInitializer调用所有实现ServletContextInitializer接口类的方法。
ServletContextInitializer是通过ServletContextInitializer类型依赖查找的，是Spring管理的。

ServletContainerInitializer是启动的时候调用，具体看StandardContext#startInternal方法中的entry.getKey().onStartup(entry.getValue(),getServletContext());
此方法会调用ServletContainerInitializer.onStartup，而在springboot中，是TomcatStarter来实现ServletContainerInitializer接口并调用所有实现ServletContextInitializer方法的类的onStartup方法


</div>2021-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/14/6cb28332.jpg" width="30px"><span>罗力友</span> 👍（0） 💬（1）<div>老师，tomcat启动是靠startup.sh文件来启动jvm的，springboot是怎么启动的呢，main方法吗</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/b8/92178ccd.jpg" width="30px"><span>ECHO</span> 👍（0） 💬（0）<div>这期内容值得细细品味</div>2020-08-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/OYzqUOhEXUl99HaOJtrjAVGIwmbDNlE6cYwwTnBWricEUaTubrJ9aO23qA0lrXfiaEib8SicZPM1icUKibElWZ93jRtQ/132" width="30px"><span>柠檬</span> 👍（0） 💬（0）<div>老师，springboot的tomcat怎么设置keeplive的时间啊，现在感觉默认springboot的tomcat keeplive不生效</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5a/6f/62c03303.jpg" width="30px"><span>前路漫漫</span> 👍（0） 💬（1）<div>老师请教个问题，springboot启动并未调用SpringServletContainerInitializer 的onStartup 方法，也就是SpringBootServletInitializer的onStartup 方法没执行，请问这个是什么原因呢？怎么整合SpringMVC的呢?</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1f/09/abb7bfe3.jpg" width="30px"><span>斑斑驳驳</span> 👍（0） 💬（0）<div>老师，最后一个示例Valve 为什么是addEngineValves 而不是 addContextValves；我觉得加到Context中也是一样的，只不过是执行前后的问题。</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/08/2bef230f.jpg" width="30px"><span>慎独</span> 👍（0） 💬（0）<div>老师讲的很棒</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fc/b5/ac717737.jpg" width="30px"><span>肖臧</span> 👍（0） 💬（1）<div>Spring boot启动Tomcat的源码里面把protocal写死了，我想把SIP相关的支持挪进来，该从哪里入手呢。
@Override
	public WebServer getWebServer(ServletContextInitializer... initializers) {
		Tomcat tomcat = new Tomcat();
		File baseDir = (this.baseDirectory != null) ? this.baseDirectory : createTempDir(&quot;tomcat&quot;);
		tomcat.setBaseDir(baseDir.getAbsolutePath());
		Connector connector = new Connector(this.protocol);
		tomcat.getService().addConnector(connector);
		customizeConnector(connector);
		tomcat.setConnector(connector);
		tomcat.getHost().setAutoDeploy(false);
		configureEngine(tomcat.getEngine());
		for (Connector additionalConnector : this.additionalTomcatConnectors) {
			tomcat.getService().addConnector(additionalConnector);
		}
		prepareContext(tomcat.getHost(), initializers);
		return getTomcatWebServer(tomcat);
	}</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e8/4b/57fa0e34.jpg" width="30px"><span>brianway</span> 👍（0） 💬（0）<div>springboot 1.0版本如何定制web容器呢？</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/1b/f4b786b9.jpg" width="30px"><span>飞翔</span> 👍（0） 💬（0）<div>老师 在digester 类里边的createStartDigester，方法，把enginer，host，context都实例化了，那wrapper是在哪里实例化的呢</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/53/86/7c6476bc.jpg" width="30px"><span>大漠落木</span> 👍（0） 💬（0）<div>@FunctionalInterface
org.springframework.boot.web.servlet.ServletContextInitializer
This interface is primarily designed to allow ServletContextInitializers to bemanaged by Spring and not the Servlet container. 
javax.servlet.ServletContainerInitializer
ServletContainerInitializers (SCIs) are registered via an entry in the file META-INF&#47;services&#47;javax.servlet.ServletContainerInitializer that must beincluded in the JAR file that contains the SCI implementation. </div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（0） 💬（0）<div>感觉还是要跟着操作一下才能懂了</div>2019-07-13</li><br/>
</ul>