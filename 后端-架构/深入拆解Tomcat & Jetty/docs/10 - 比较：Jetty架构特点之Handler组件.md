在专栏上一期，我们学习了Jetty的整体架构。先来回顾一下，Jetty 就是由多个Connector（连接器）、多个Handler（处理器），以及一个线程池组成，整体结构图如下。

![](https://static001.geekbang.org/resource/image/66/6a/66e55e89fd621c0eba6321471da2016a.png?wh=1354%2A714)

上一期我们分析了Jetty Connector组件的设计，Connector会将Servlet请求交给Handler去处理，那Handler又是如何处理请求的呢？

Jetty的Handler在设计上非常有意思，可以说是Jetty的灵魂，Jetty通过Handler实现了高度可定制化，那具体是如何实现的呢？我们能从中学到怎样的设计方法呢？接下来，我就来聊聊这些问题。

## Handler是什么

**Handler就是一个接口，它有一堆实现类**，Jetty的Connector组件调用这些接口来处理Servlet请求，我们先来看看这个接口定义成什么样子。

```
public interface Handler extends LifeCycle, Destroyable
{
    //处理请求的方法
    public void handle(String target, Request baseRequest, HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException;
    
    //每个Handler都关联一个Server组件，被Server管理
    public void setServer(Server server);
    public Server getServer();

    //销毁方法相关的资源
    public void destroy();
}
```

你会看到Handler接口的定义非常简洁，主要就是用handle方法用来处理请求，跟Tomcat容器组件的service方法一样，它有ServletRequest和ServletResponse两个参数。除此之外，这个接口中还有setServer和getServer方法，因为任何一个Handler都需要关联一个Server组件，也就是说Handler需要被Server组件来管理。一般来说Handler会加载一些资源到内存，因此通过设置destroy方法来销毁。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（22） 💬（1）<div>hadler只算是一层wrapper，真正处理得还是真正处理servlet逻辑的servlet</div>2019-07-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI1ibgEPxRmTaEYWYnv8QHwL4ic7ibcjMEGTeb66LtzFCgR6mqOMjr4kvZgfuMIEibzG5Yp2JIaxtNeIA/132" width="30px"><span>夏天</span> 👍（15） 💬（2）<div>想学习tomcat架构，大佬有没有推荐的书籍</div>2019-06-01</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqLcWH3mSPmhjrs1aGL4b3TqI7xDqWWibM4nYFrRlp0z7FNSWaJz0mqovrgIA7ibmrPt8zRScSfRaqQ/132" width="30px"><span>易儿易</span> 👍（7） 💬（2）<div>老师讲的这篇知识点脉络清晰，看完之后能够明确课程内容，但是考虑到开发使用，我却更迷糊了，web开发要怎样跟Jetty这样的容器相结合呢？我们跑在tomcat上的项目能拿下来直接放到Jetty上吗？感觉Jetty需要在项目中增加很多配置才行，对开发的要求也多……没有用过Jetty</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（6） 💬（1）<div>老师有jetty源码下载地址链接么？git的下不动😂</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（3） 💬（1）<div>Handler实现了 Servlet 规范中的 Servlet、Filter 和 Listener 功能中的一个或者多个。handler可以持有别的handle，servlet不持有别的servlet。servlet的调用关系通过servlet容器来控制。handler的调用关系通过wabappcontext控制。老师好!
Tomcat通过连接器来区分协议和端口号，host区分虚拟主机(二级域名)。jetty里面是怎么绑定的呢?jetty的连接器和容器没有对应关系，所有的容器都可以处理各种的协议么?mapping具体又是在哪里起作用的呢?是handlecollection通过mapping找到对应的wabappcontext吗?</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/23/31e5e984.jpg" width="30px"><span>空知</span> 👍（1） 💬（1）<div>老师问下
server是一个 handlerWrapper 内部应该只有一个hanlder 可是他内部又维护一个handlerCollection,当请求过来时候 去handlerCollection 里面根据url判断是哪个项目 那定义的那个 单独的hanlder 有啥用?</div>2019-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/c9/d3439ca4.jpg" width="30px"><span>why</span> 👍（11） 💬（0）<div>- Handler 是一个接口, 有一堆实现类
    - Handler 接口用 handle 方法处理请求, 类似 Tomcat 的 service
    - 有 set&#47;getServer 用于关联一个 Server
    - 用 destroy 销毁释放资源
- Handler 继承关系
    - Handler→AbstractHandler→AbstractHandlerContainer
    - AbstractHandlerContainer 中有其他 handler 的引用, 可实现链式调用
    - AbstractHandlerContainer  子类有 HandlerWrapper 和 HandlerCollection. HandlerWrapper 包含一个 Handler 引用; HandlerCollection 包含多个 Handler 引用, 存于数组中
    - HandlerWrapper 有两个子类: Server 和 ScopedHandler
        - Server, 是 Handler 的入口, 必须将请求传递给其他的 Handler 处理
        - ScopedHandler 实现具有上下文信息的责任链调用; 有一堆子类来实现 Servlet 规范: ServletHandler; ContextHandler; ContextHandler; ServletContextHandler; WebAppContext
    - HandlerCollection 用于支持多个 Web 应用, 每个 Web 应用对应一个 Handler 入口
        - Server 中有 HandlerCollection, Server 根据 URL 从数组中选择 Handler 处理请求
    - Handler 的类型
        - 协调 Handler: 负责将请求路由到一组 handler, 如 HandlerCollection
        - 过滤器 Handler: 自己会处理请求, 再转发给下一个 Handler, 如 HandlerWrapper 及其子类
        - 内容 Handler: 调用真正 Servlet 处理请求, 响应内容, 如 ServletHandler, 或 ResourceHandler 响应静态资源请求
    - 实现 Servlet 规范
        - ServletHandler, ContextHandler, WebAppContext
        - Jetty 启动 Web 应用分为两步
            - 创建 WebAppContext 并配置 WAR 包和应用路径
            - 将 WebAppContext 添加到 Server, 并启动 Server
        - Servlet 规范有: Context, Servlet, Filter, Listen, Session, Jetty 对应的实现为 ContextHandler, ServletHandler, SessionHandler
            - WebAppContext 是一个 ContextHandler, 并负责管理 ServletHandler 和 SessionHandler
        - ContextHandler 负责创建并初始化 ServletContext 对象, 另外还包含一组 Handler, 处理特定 URL 的请求(ServletHandler)
            - ServletHandler 实现 Servlet, Filter, Listen 的功能; 其依赖 Filter&#47;ServletHandler(Filter 和 Serlvet 的包装类) 以及 Filter&#47;ServletMapping 封装 Filter&#47;Servlet 及其映射的路径
        - SessionHandler 管理 Session
    - WebAppContext 将这些 Handler 构成执行链: Connection→SessionHandler→SecurityHandler→...→SevletHandler→Servlet.</div>2019-06-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/wIWrciav7DRkOaD7vUtr084sxprq2U4obfH1ibls4RIsAw5foQlDGIt98x1RHATznNbh0iasibWV2Y7I7QpyFJ4TVA/132" width="30px"><span>Wipeher</span> 👍（2） 💬（1）<div>老师。看了下源码。Server中并没有HandlerCollection。而只有一个private final List&lt;Connector&gt; _connectors = new CopyOnWriteArrayList&lt;&gt;(); 所以不太明白，文中为何提到Server有HandlerCollection，而且，从类图上来说，也不符合逻辑，已经声明为HandleWrapper了，为何要维护一个HandlerCollection，不如一开始直接实现一个HandlerCollection就可以了。望老师指教</div>2020-06-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLNRjRHibgf1ia8RrhPJSZBiawk5OOb5VsVva5cmwickaV58WsaOkljD5rVeibWnlic62c2ZqcPsapOqCdw/132" width="30px"><span>east</span> 👍（2） 💬（0）<div>1.H和S都能处理请求，
2.H可以调用S，S不能调用H，
3.H更多处理通用的处理并且是抽象的，S是处理具体的且比较特定化请求</div>2019-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8a/76/4abc8ac1.jpg" width="30px"><span>完美世界</span> 👍（1） 💬（0）<div>Jetty Server 就是由多个 Connector、多个 Handler，以及一个线程池组成。

Jetty 的 Handler 设计是它的一大特色，Jetty 本质就是一个 Handler 管理器，Jetty 本身就提供了一些默认 Handler 来实现 Servlet 容器的功能，你也可以定义自己的 Handler 来添加到 Jetty 中，这体现了“微内核 + 插件”的设计思想。

handler 应该会把请求字节流转换为servlet request</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0c/86/8e52afb8.jpg" width="30px"><span>花花大脸猫</span> 👍（0） 💬（0）<div>老是，有一个问题，HandleWrapper可以看做是特殊的HandleCollection的话，那是不是可以说明HandleWrapper实现的功能，对应的HandleCollection也能实现，从而间接说明两者并不是对等的，而且将HandleWrapper作为HandleCollection的一种简易的handle实现方式？</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b6/d9/4d8a4d4c.jpg" width="30px"><span>红豆成香</span> 👍（0） 💬（0）<div>jetty这两节不太好肯</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0f/f2/3f3c0946.jpg" width="30px"><span>美好时光海苔</span> 👍（0） 💬（0）<div>老师，过滤器 Handler 和 Servlet 规范中的 Filter 有什么区别？如果已经有 Servlet 规范中的 Filter，为什么我们还需要 过滤器类 的 Handler ？ </div>2021-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/9e/9337ca8e.jpg" width="30px"><span>jaryoung</span> 👍（0） 💬（0）<div>handler 是指挥官？serlvet 真正的执行者</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/51/0d/14d9364a.jpg" width="30px"><span>L.B.Q.Y</span> 👍（0） 💬（0）<div>Servlet用于处理业务逻辑，Handler用于路由请求到指定的Servlet上。</div>2019-07-30</li><br/>
</ul>