你好，我是郭屹。今天我们继续手写MiniTomcat。

上节课我们实现了Context类的预加载，并引入server.xml和web.xml，分别对服务端和Servlet进行自定义配置。到目前为止我们的MiniTomcat已经是一个完整的小型Tomcat了。

考虑到在目前大部分的场景中，依托于Spring框架编写的项目大多使用Tomcat服务器进行启动，而我们之前已经完成过MiniSpring框架的构建，所以很自然地，我们就会想到**将现有的MiniTomcat与之前完成的MiniSpring进行集成。**

从原理上来说，只要是按照Servlet规范实现的服务器，就可以将MiniSpring直接放在webapps目录下运行，不用做任何额外的工作。所以从道理上讲，MiniTomcat和MiniSpring的集成也是这样的。

不过，因为MiniTomcat毕竟是一个麻雀版的Tomcat，并没有完整地实现Servlet规范，所以现在这么直接绑在一起是不能顺利运行的，我们还需要做一点完善的工作。

我们先回顾一下，MiniSpring启动的时候，依赖Tomcat环境做什么事情。一切的起点都在web.xml文件中，里面定义了Listener、Filter和Servlet。为了让MiniSpring启动起来，我们要实现一个ContextLoaderListener，这个Listener的目的是启动MiniSpring的IoC容器。然后用一个DispatcherServlet来拦截一切路径，通过这个DispatcherServlet来使用MiniSpring的MVC。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：从编码角度怎么遵守servlet规范？
写出符合servlet规范的servlet，需要怎么做？查看规范文档，照着文档写吗？还是继承某个已经存在的符合规范的接口？

Q2：以前开发的项目中spring与tomcat是什么关系？
本课程中，spring是作为一个webapp，放到tomcat的应用目录中；用户请求是先到tomcat，tomcat再转发给spring；而且spring是tomcat负责启动的。总之，tomcat好像是spring的管理者。

比较早的时候，还没有使用springBoot的时候，用IDE创建一个项目，直接创建的是spring项目，直接感觉到的是spring MVC，并没有感觉到tomcat的存在，但需要配置tomcat。 此种情况下，tomcat和spring是什么关系？还是我们本专栏的关系吗？即tomcat管理spring？

现在的开发中，IDE一般都是用Idea，然后使用springBoot创建项目，直接创建的也是spring项目，也没有感觉到tomcat的存在，甚至感觉不到spring的存在。不过还是需要配置tomcat。 此种情况下，springBoot和tomcat、spring是什么样的关系？

Q3：miniSpring相当于原来的servlet处理部分吗？？
本课之前，servlet由miniT的servlet部分处理。本课集成minis以后，原来的servlet处理部分就没有了，由minis处理。这样的话，minis相当于接管了原来的servlet处理部分，相当于一个大的servlet。是这样吗？

Q4：集成mins以后，原来的静态处理部分由谁处理？
本课之前，一部分是处理servelt，另外一部分是处理静态文本文件。集成minis以后，处理静态文本文件部分是谁处理？

Q5：集成minis以后，正常的应用怎么办？
Minit集成了minis,那其他web应用怎么办？原来是把应用放在webapp目录下面，那现在怎么办？</div>2024-01-16</li><br/>
</ul>