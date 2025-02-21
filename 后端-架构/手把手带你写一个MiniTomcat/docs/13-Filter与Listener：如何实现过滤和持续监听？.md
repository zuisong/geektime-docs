你好，我是郭屹。今天我们继续手写MiniTomcat。

上一节课我们实现了Pipeline和Valve，这样我们在流程走通的前提下，可以在每一层Container之间增加权限校验、日志打印、错误输出等自定义的处理逻辑。此外我们引入了责任链这一设计模式，来依次调用这些处理逻辑。

这节课我们继续来完善MiniTomcat，我们计划引入两个组件——Filter（过滤器）以及Listener（监听器），并且还是使用经典的职责链模式。

过滤器可以检查请求对象以及返回对象，并通过请求对象和返回对象的包装类进行修改，而且多个过滤器之间可以串联，就像流水线一样一层层进行过滤，协同起来组装成最终的请求对象和响应对象。

而监听器的存在是为了配合我们目前已有的Container、Session等机制，通过监听这些机制的事件，比如启动、超时、结束等，更好地对服务器进行处理。

我们一起来动手实现。

## 项目结构

这节课我们主要新增了Filter相关处理方法类，还有Container、Instance与Session的事件和监听器，具体类的功能我们后面会详细介绍。你可以看一下现在的项目结构。

```plain
MiniTomcat
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
│  │  │  │  │  │  ├─ StandardPipeline.java
│  │  │  │  │  │  ├─ StandardWrapper.java
│  │  │  │  │  │  ├─ StandardWrapperValve.java
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
├─ webroot
│  ├─ test
│  │  ├─ HelloServlet.class
│  │  ├─ TestFilter.class
│  │  ├─ TestListener.class
│  │  ├─ TestServlet.class
│  ├─ hello.txt
├─ pom.xml
```
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>抓大放小， 个人觉得核心流程： ApplicationFilterChain.doFilter()  --&gt;  ApplicationFilterChain.internalDoFilter()   --&gt;   Filter.doFilter()  --&gt; ApplicationFilterChain.doFilter()   一个环状； 入口 StandardWrapperValve ， 出口是否有下一个Filter。 </div>2024-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：BootStrap代替了HttpServer吗？为什么这么做？
Q2：Filter、Listener可以扩展吗？
比如，用户自定义Filter、Listener，是否支持？
Q3：用 ArrayList 存放所有的 filter和listener，有什么考虑？
用Map不行吗？
Q4：对于Filter，是FilterChain最后调用servlet吗？
按说不应该由Filter调用servlet，而是由一个更高层的一个东西来调用，类似于控制器或调度器一类的来调用。
Q5：有浏览器上的servlet吗？
我们这里说的servlet，都是运行在后端。我听说有运行在浏览器上的servlet，是否有？</div>2024-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/7a/ac307bfc.jpg" width="30px"><span>到不了的塔</span> 👍（0） 💬（0）<div>郭老师，你好，请问下为啥StandardContext中会有listenerDefs字段来保存listener config呢, 有listeners字段来保存listener实例应该就足够满足需求了吧。 
我看filter的设计也跟这类似，也有filter config，这种设计的好处是啥？</div>2024-05-02</li><br/>
</ul>