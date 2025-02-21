你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们引入了自定义的类加载器，先尝试了用系统提供的ClassLoader加载某个类，如果是delegate模式，那么父级类加载器去加载这个类，之后再试着由原本的类加载器加载类；如果不是delegate模式，使用父级类加载器加载，如果父级类加载器为空，就用系统级类加载器加载。

随后我们还进一步区分了Context、Host，对MiniTomcat进行了两层容器包装，实现解耦。

而这节课我们计划做进一步的优化调整，一是在进入Host层之前，预先装载Context，二是对Servlet访问路径支持自定义。最后通过配置文件来配置服务器，跟Tomcat一样。

现在我们一起来动手实现。

## 项目结构

这节课我们把所有的ClassLoader移到/loader目录里，随后使用server.xml和web.xml分别管理Host启动配置与Servlet加载配置，这也是我们这节课的重点，你可以看一下现在的目录结构。

```plain
MiniTomcat
├─ conf
│  ├─ server.xml
├─ src
│  ├─ main
│  │  ├─ java
│  │  │  ├─ com
│  │  │  │  ├─ minit
│  │  │  │  │  ├─ connector
│  │  │  │  │  │  ├─ http
│  │  │  │  │  │  │  ├─ DefaultHeaders.java
│  │  │  │  │  │  │  ├─ HttpConnector.java
│  │  │  │  │  │  │  ├─ HttpHeader.java
│  │  │  │  │  │  │  ├─ HttpProcessor.java
│  │  │  │  │  │  │  ├─ HttpRequestImpl.java
│  │  │  │  │  │  │  ├─ HttpRequestLine.java
│  │  │  │  │  │  │  ├─ HttpResponseImpl.java
│  │  │  │  │  │  │  ├─ ServletProcessor.java
│  │  │  │  │  │  │  ├─ SocketInputStream.java
│  │  │  │  │  │  │  ├─ StatisResourceProcessor.java
│  │  │  │  │  │  ├─ HttpRequestFacade.java
│  │  │  │  │  │  ├─ HttpResponseFacade.java
│  │  │  │  │  ├─ core
│  │  │  │  │  │  ├─ ApplicationFilterChain.java
│  │  │  │  │  │  ├─ ApplicationFilterConfig.java
│  │  │  │  │  │  ├─ ContainerBase.java
│  │  │  │  │  │  ├─ ContainerListenerDef.java
│  │  │  │  │  │  ├─ FilterDef.java
│  │  │  │  │  │  ├─ FilterMap.java
│  │  │  │  │  │  ├─ StandardContext.java
│  │  │  │  │  │  ├─ StandardContextValve.java
│  │  │  │  │  │  ├─ StandardHost.java
│  │  │  │  │  │  ├─ StandardHostValve.java
│  │  │  │  │  │  ├─ StandardPipeline.java
│  │  │  │  │  │  ├─ StandardWrapper.java
│  │  │  │  │  │  ├─ StandardWrapperValve.java
│  │  │  │  │  ├─ loader
│  │  │  │  │  │  ├─ CommonClassLoader.java
│  │  │  │  │  │  ├─ CommonLoader.java
│  │  │  │  │  │  ├─ WebappClassLoader.java
│  │  │  │  │  │  ├─ WebappLoader.java
│  │  │  │  │  ├─ logger
│  │  │  │  │  │  ├─ Constants.java
│  │  │  │  │  │  ├─ FileLogger.java
│  │  │  │  │  │  ├─ LoggerBase.java
│  │  │  │  │  │  ├─ SystemErrLogger.java
│  │  │  │  │  │  ├─ SystemOutLogger.java
│  │  │  │  │  ├─ session
│  │  │  │  │  │  ├─ StandardSession.java
│  │  │  │  │  │  ├─ StandardSessionFacade.java
│  │  │  │  │  ├─ startup
│  │  │  │  │  │  ├─ BootStrap.java
│  │  │  │  │  ├─ util
│  │  │  │  │  │  ├─ CookieTools.java
│  │  │  │  │  │  ├─ StringManager.java
│  │  │  │  │  │  ├─ URLDecoder.java
│  │  │  │  │  ├─ valves
│  │  │  │  │  │  ├─ AccessLogValve.java
│  │  │  │  │  │  ├─ ValveBase.java
│  │  │  │  ├─ Connector.java
│  │  │  │  ├─ Container.java
│  │  │  │  ├─ ContainerEvent.java
│  │  │  │  ├─ ContainerListener.java
│  │  │  │  ├─ Context.java
│  │  │  │  ├─ InstanceEvent.java
│  │  │  │  ├─ InstanceListener.java
│  │  │  │  ├─ Loader.java
│  │  │  │  ├─ Logger.java
│  │  │  │  ├─ Pipeline.java
│  │  │  │  ├─ Request.java
│  │  │  │  ├─ Response.java
│  │  │  │  ├─ Session.java
│  │  │  │  ├─ SessionEvent.java
│  │  │  │  ├─ SessionListener.java
│  │  │  │  ├─ Valve.java
│  │  │  │  ├─ ValveContext.java
│  │  │  │  ├─ Wrapper.java
│  │  ├─ resources
│  ├─ test
│  │  ├─ java
│  │  │  ├─ test
│  │  │  │  ├─ HelloServlet.java
│  │  │  │  ├─ TestFilter.java
│  │  │  │  ├─ TestListener.java
│  │  │  │  ├─ TestServlet.java
│  │  ├─ resources
├─ webapps
│  ├─ app1
│  │  ├─ WEB-INF
│  │  │  ├─ classes
│  │  │  │  ├─ test
│  │  │  │  │  ├─ HelloServlet.class
│  │  │  │  │  ├─ TestFilter.class
│  │  │  │  │  ├─ TestListener.class
│  │  │  │  │  ├─ TestServlet.class
│  │  │  ├─ web.xml
│  │  ├─ hello.txt
│  ├─ app2
│  │  ├─ WEB-INF
│  │  │  ├─ classes
│  │  │  │  ├─ test
│  │  │  │  │  ├─ HelloServlet.class
│  │  │  │  │  ├─ TestFilter.class
│  │  │  │  │  ├─ TestListener.class
│  │  │  │  │  ├─ TestServlet.class
│  │  │  ├─ web.xml
│  │  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（1）<div>目前能想到的是 Servlet 注解或者直接增加 mapping 配置</div>2024-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：server.xml中为什么配置两个端口？
&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;Server port=&quot;8005&quot; shutdown=&quot;SHUTDOWN&quot;&gt;
  &lt;Service name=&quot;Catalina&quot;&gt;
    &lt;Connector executor=&quot;tomcatThreadPool&quot;
               port=&quot;8080&quot; protocol=&quot;HTTP&#47;1.1&quot;
               connectionTimeout=&quot;20000&quot;
               redirectPort=&quot;8443&quot; &#47;&gt;
    &lt;Engine name=&quot;Catalina&quot; defaultHost=&quot;localhost&quot;&gt;
    &lt;&#47;Engine&gt;
  &lt;&#47;Service&gt;
&lt;&#47;Server&gt;

一个8005，另外一个8080，有什么区别？到底有哪一个？

Q2:Tomcat为什么用Digester？
既然Digester比较复杂，使用的人也比较少，为什么Tomcat还用它？

Q3：Tomcat内部怎么表示多个Host？
一个主机有一套处理实例吗？类似于“类”，一样的代码，但一个具体的主机就是一个实例，比如有3个主机，就有3个实例。是这样吗？</div>2024-01-12</li><br/><li><img src="" width="30px"><span>Geek_f1f069</span> 👍（0） 💬（0）<div>课程已经学的差不多了,说一下总体的学习感受。不知道是因为老师讲的不够透彻,
还是因为自己本身功力的不足，目前感觉理解的不够透彻，想多看代码消化理解,但感觉代码很多地方组织混乱,逻辑不清晰明了。</div>2024-07-28</li><br/>
</ul>