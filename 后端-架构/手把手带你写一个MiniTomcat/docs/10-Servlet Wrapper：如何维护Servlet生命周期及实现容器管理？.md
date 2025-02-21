你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们把Request和Response从无状态变成了有状态，实现了Session和Cookie的管理，还实现了同一页面的资源请求复用Socket，减少了性能消耗。

到目前为止，我们已经基本将浏览器与服务器之间的通信处理完毕。接下来我们再看后端服务器，现在我们还是使用ServletProcessor简单地调用Servlet的service方法，接下来我们考虑将其扩展，对Servlet进行管理，这就引入了Container容器的概念。**我们计划让Container和Connector配合在一起工作，前者负责后端Servlet管理，而后者则负责通信管理。**

![图片](https://static001.geekbang.org/resource/image/6e/42/6e0069a19d16f6ddf482820a06b8d242.png?wh=1920x998)

初步构建容器后，我们还会考虑使用Wrapper进行包装，用于维护Servlet的生命周期：初始化、提供服务、销毁这个全过程，把Servlet完全纳入程序自动管理之中，让应用程序员更少地感知到底层的配置，更专注于业务逻辑本身。

接下来我们一起来动手实现。

## 项目结构

这节课我们新增ServletContainer与ServletWrapper两个类，分别定义Container与Wrapper，你可以看一下现在的程序结构。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：为什么Cookie有实现而Session没有实现？
代码中的Session类实现了HttpSession接口，但代码中用的Cookie是系统提供的。为什么Session就没有系统提供的实现类？

Q2：C++服务器有哪些？
看到一篇介绍用C++开发服务器的文章，说明有C++开发的服务器。Tomcat是用Java开发的。那么，有什么C++开发的服务器产品？用在什么场景下？互联网公司一般不用C++服务器吧。</div>2023-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/6e/5435e214.jpg" width="30px"><span>HH🐷🐠</span> 👍（0） 💬（2）<div>请一个副总吧， 管理每个部门的 Connector 和 Container， 负责他们两个创建和相互引用</div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/33/74/d9d143fa.jpg" width="30px"><span>silentyears</span> 👍（0） 💬（0）<div>老师，connector和container互相指引，这种类的依赖关系是不是不太好？像在spring中就是循环依赖</div>2024-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>发的留言怎么没有显示出来，再发一次：
Q1：为什么Cookie有实现而Session没有实现？
代码中的Session类实现了HttpSession接口，但代码中用的Cookie是系统提供的。为什么Session就没有系统提供的实现类？

Q2：C++服务器有哪些？
看到一篇介绍用C++开发服务器的文章，说明有C++开发的服务器。Tomcat是用Java开发的。那么，有什么C++开发的服务器产品？用在什么场景下？互联网公司一般不用C++服务器吧。</div>2024-01-01</li><br/>
</ul>