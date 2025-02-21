你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们新增了**过滤器Filter和监听器Listener**。利用过滤器，对每一层的对象依次进行处理，最终构建出请求对象和返回对象；而监听器的存在，则是为了配合我们目前已有的Container、Session等机制，通过监听相关的事件，比如启动、超时、结束等，更好地对服务器进行管理。

目前我们的测试代码，都写在/webroot目录下，但如果有不同的应用，那就都混合在同一路径下了，这样不利于管理。所以这节课我们进一步考虑**支持多路由的转发**，通过路径的区分，将请求转发到不同应用之中，我们会引入**Context**这个概念来实现应用的相互隔离。

![图片](https://static001.geekbang.org/resource/image/2c/b7/2c646316dc669f18ef13998bc56065b7.png?wh=1920x1119)

如图所示，用户在url中分别输入路径hello/和another/，这就代表了两个不同的context，以此路径分别定位于不同的应用中。

在此基础上，我们再优化Bootstrap，去除多余的功能，确保它只是一个启动器，贯彻各司其职的设计理念。

下面我们一起来动手实现。

## 项目结构

这节课我们主要新增了StandardHost、StandardHostValve，以及WebappClassClassLoader类。还有一个重要的变化是在/webroot目录下新增app1和app2目录，用来区分不同的应用。你可以看一下改动后的项目结构。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/1G2rlRgNalXbcUnHibRNMibAeHQhWoKNl4e4EgkiawDynZZiaO4W3vSSMtlYEKrt6e7GW4mcu1sjcs7bGKjl0vRhWQ/132" width="30px"><span>Twein</span> 👍（0） 💬（1）<div>老师，上条留言说错了，应该是host的start方法没有启动过滤器的代码，源码少了这块逻辑</div>2024-02-21</li><br/><li><img src="" width="30px"><span>Geek_50a5cc</span> 👍（0） 💬（1）<div>感觉一路跟过来，好多概念有点模糊了，有空回头再看看</div>2024-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（1）<div>http:&#47;&#47;address:port&#47;context&#47;servlet
从一个整体出发，url --&gt; HttpRequest,  context --&gt; StandardHost, servlet --&gt; StandardWrapper,  当然背后还有涉及 HttpHeader、Filter 等等</div>2024-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师几个问题：
Q1：不同应用对应不同的加载类吗？？
本文中有这样一句话“每一个 context 都对应一个不同的 WebappClassLoader”，对于加载类，是不同的实例？还是不同的类？
比如context1和context2，理解1：context1对应WebappClassLoaderA；context2对应WebappClassLoaderB，是不同的类。
理解2：context1对应WebappClassLoader的实例1；context2对应WebappClassLoader的实例2，即同一个类的不同实例。
Q2：webroot目录下的测试代码，在实际的Tomcat中就是具体的web应用，对吗？
Q3：一个应用中，两个ClassLoader可以加载同一个类(版本也相同)吗？
Q4：WebappClassLoader不需要继承已有的接口或方法吗？
WebappClassLoader算是自定义ClassLoader吧。记得以前看过关于自定义ClassLoader的文章，好像要继承系统已有的接口或方法，就是说要和已有的东西建立联系。但本课中的WebappClassLoader是个单独的类，并无继承。
Q5：运行后找不到类，报错：
java.lang.ClassNotFoundException: test.TestListener
(StandardHost.java:120)
&#47;&#47; Instantiate a new instance of this filter and return it
                    Class&lt;?&gt; clazz = classLoader.getClassLoader().loadClass(listenerClass);
还没有调试。老师那边能正常运行吗？</div>2024-01-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/H6US70MyQlXGVIzSbrgdTiasc0mbJS503AJG9tuGwXL0cLTBmp1ib2yLQ7HeA8BKUX12TKHvgaDS3JfiacmuBBO4w/132" width="30px"><span>毛竹</span> 👍（0） 💬（0）<div>host  start代码里启用listenerStart 读的路径是 test.TestListener, 本章项目路径里并不存在这个路径</div>2024-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（0）<div>standardContext$start()都没有任何地方调用吧</div>2024-07-19</li><br/>
</ul>